"""
Sysplorer Python API driver wrapper for MCP tools.

This driver uses `mworks.sysplorer` package (mworks-sysplorer) instead of
direct kernel bindings (PyMwService).

**Launch policy (hard requirement for this repo):** start the Sysplorer GUI / stack
only via ``mworks.sysplorer.StartSysplorer`` (optionally with ``processPath`` pointing
at ``Bin64/mworks.exe``). Do **not** spawn ``mworks.exe`` from MCP server code using
``subprocess``, ``os.startfile``, shell ``Start-Process``, or process-name hacks.
"""

from __future__ import annotations

import logging
import os
import platform
import sys
import threading
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


from path_config import (
    MWORKS_BIN64 as _CFG_BIN64,
    MWORKS_SITE_PACKAGES as _CFG_SITE_PACKAGES,
    MWORKS_WORKDIR as _CFG_WORKDIR,
    ensure_modelica_lite_site_helpers,
    is_modelica_lite_platform,
)
from constants import normalize_load_library_call
from launch_context import start_sysplorer_in_desktop_context

DEFAULT_SYSPLORER_SITE_PACKAGES = _CFG_SITE_PACKAGES
DEFAULT_MWORKS_BIN64 = _CFG_BIN64
DEFAULT_MWORKS_WORKDIR = _CFG_WORKDIR



def _looks_like_openmodelfile_duplicate_or_loaded_error(message: str) -> bool:
    """Heuristic: OpenModelFile failed because the file/model is already in workspace."""
    if not message:
        return False
    if any(z in message for z in ("已加载", "重复加载", "已经加载", "模型已", "重复打开")):
        return True
    low = message.lower()
    return any(
        phrase in low
        for phrase in (
            "already loaded",
            "already open",
            "duplicate",
            "re-open",
            "file already",
        )
    )


def _build_full_path() -> str:
    """Return the full Windows PATH by merging registry entries with os.environ['PATH'].

    When the MCP server is started by Claude Code (or any launcher that strips
    the environment), os.environ['PATH'] may be minimal and miss compilers,
    runtime DLLs, and other tools that Sysplorer depends on.  Reading from the
    Windows registry provides the true system-wide + user PATH.

    Merge order (highest priority first):
      1. HKCU\\Environment\\Path  (user PATH)
      2. HKLM\\...\\Environment\\Path  (system PATH)
      3. os.environ['PATH']  (virtualenv / conda / dynamic additions)

    Entries are deduplicated case-insensitively while preserving order.
    Falls back to os.environ['PATH'] on non-Windows platforms.
    """
    if platform.system() != "Windows":
        return os.environ.get("PATH", "")

    segments: list[str] = []
    try:
        import winreg  # type: ignore[import]
        for hive, subkey in [
            (
                winreg.HKEY_CURRENT_USER,
                r"Environment",
            ),
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            ),
        ]:
            try:
                with winreg.OpenKey(hive, subkey) as key:
                    val, _ = winreg.QueryValueEx(key, "Path")
                    # Registry values may contain unexpanded %variables%.
                    segments.append(os.path.expandvars(str(val)))
            except OSError:
                pass
    except ImportError:
        pass

    # Include current process PATH last so virtualenv/conda activations survive.
    current = os.environ.get("PATH", "")
    if current:
        segments.append(current)

    # Deduplicate preserving order (case-insensitive on Windows).
    seen: set[str] = set()
    result: list[str] = []
    for seg in segments:
        for entry in seg.split(os.pathsep):
            entry = entry.strip()
            if not entry:
                continue
            key_lower = entry.lower()
            if key_lower not in seen:
                seen.add(key_lower)
                result.append(entry)

    return os.pathsep.join(result)


class MWorksDriverError(RuntimeError):
    """Raised when Sysplorer API init or execution fails."""


_log = logging.getLogger(__name__)


def _win_short_path_enabled() -> bool:
    raw = os.environ.get("MWORKS_WIN_SHORT_PATH", "1").strip().lower()
    return raw not in ("0", "false", "no", "off")


def _windows_short_path_if_exists(path: Path) -> Path:
    """On Windows, map an existing path to its 8.3 short form when possible.

    Native Sysplorer bindings and some DLL loaders still mishandle Unicode paths;
    ``GetShortPathNameW`` yields ASCII-only paths that survive those code paths.
    If the path does not exist, short-name generation is skipped (caller still
    gets the original).  Disable via ``MWORKS_WIN_SHORT_PATH=0``.
    """
    if platform.system() != "Windows" or not _win_short_path_enabled():
        return path
    try:
        resolved = path.resolve()
    except OSError:
        return path
    if not resolved.exists():
        return path
    long_s = str(resolved)
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        GetShortPathNameW = kernel32.GetShortPathNameW
        GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        GetShortPathNameW.restype = wintypes.DWORD

        buf = ctypes.create_unicode_buffer(4096)
        copied = GetShortPathNameW(long_s, buf, len(buf))
        if copied == 0:
            return path
        while copied >= len(buf):
            buf = ctypes.create_unicode_buffer(copied + 8)
            copied = GetShortPathNameW(long_s, buf, len(buf))
            if copied == 0:
                return path
        short_s = buf.value
        if short_s and short_s != long_s:
            _log.debug("Windows short path: %s -> %s", long_s, short_s)
        return Path(short_s) if short_s else path
    except Exception:
        return path


def _normalize_mworks_install_paths(bin64_path: Path, site_packages: Path) -> tuple[Path, Path]:
    """Prefer short paths for Bin64 and site-packages on Windows (Unicode-safe DLL load)."""
    b = _windows_short_path_if_exists(bin64_path)
    sp = _windows_short_path_if_exists(site_packages)
    return b, sp


def _ensure_windows_processor_architecture() -> None:
    """If ``PROCESSOR_ARCHITECTURE`` is missing or empty on Windows, infer and set it.

    Some MCP / IDE launchers start Python with a trimmed environment. Sysplorer's
    ``verify_vc.bat`` branches on ``PROCESSOR_ARCHITECTURE`` to choose
    ``vcvarsall.bat amd64`` vs ``x86_amd64``; when the variable is blank, 64-bit VC
    verification can fail while 32-bit still passes.

    Does nothing on non-Windows, and leaves a non-empty caller-provided value unchanged.
    """
    if platform.system() != "Windows":
        return
    raw = os.environ.get("PROCESSOR_ARCHITECTURE")
    if raw is not None and raw.strip():
        return
    machine = (platform.machine() or "").upper().replace("-", "_")
    if machine in ("AMD64", "X86_64", "X64"):
        os.environ["PROCESSOR_ARCHITECTURE"] = "AMD64"
    elif machine in ("X86", "I386", "I686"):
        os.environ["PROCESSOR_ARCHITECTURE"] = "x86"
    elif sys.maxsize > 2**32:
        os.environ["PROCESSOR_ARCHITECTURE"] = "AMD64"
    else:
        os.environ["PROCESSOR_ARCHITECTURE"] = "x86"


def _prepare_runtime_without_bin64() -> None:
    """``modelica_lite`` attach: skip ``MWORKS_BIN64`` / site-packages path resolution."""
    _ensure_windows_processor_architecture()
    warnings.filterwarnings("ignore", category=SyntaxWarning)


def _configure_sysplorer_python_env(bin64_path: Path, site_packages: Path) -> None:
    """Prepare ``sys.path`` and ``PATH`` so ``import mworks.sysplorer`` works.

    Shared by :class:`MWorksDriver` and :func:`find_sysplorer_ports` (official
    ``FindSysplorer`` / ``ConnectSysplorer``).
    """
    _ensure_windows_processor_architecture()
    bin64_path, site_packages = _normalize_mworks_install_paths(bin64_path, site_packages)

    if site_packages.exists() and str(site_packages) not in sys.path:
        sys.path.append(str(site_packages))

    install_dir = bin64_path.parent
    extra_dirs = [
        bin64_path,
        install_dir / "Simulator" / "mingw64" / "bin",
        install_dir / "Simulator" / "Bin64",
        install_dir / "simulator" / "bin64",
    ]

    full_path = _build_full_path()
    # Prepend short-resolved dirs so PATH entries stay ASCII-only on Windows when possible.
    prepend_resolved: list[str] = []
    for d in extra_dirs:
        if not d.exists():
            continue
        d_use = _windows_short_path_if_exists(d)
        ds = str(d_use)
        if ds.lower() not in full_path.lower():
            prepend_resolved.append(ds)

    new_path = os.pathsep.join(prepend_resolved + [full_path]) if prepend_resolved else full_path
    os.environ["PATH"] = new_path

    warnings.filterwarnings("ignore", category=SyntaxWarning)


def _resolve_sysplorer_process_path(bin64_path: Path) -> str:
    """Return the platform-appropriate Sysplorer launcher path for StartSysplorer."""
    if platform.system() == "Windows":
        return str(bin64_path / "mworks.exe")

    candidates = [
        bin64_path / "mworks.sh",
        bin64_path / "mworks",
        bin64_path.parent / "mworks.sh",
        bin64_path.parent / "mworks",
    ]
    existing = next((candidate for candidate in candidates if candidate.exists()), None)
    return str(existing or candidates[0])


def find_sysplorer_ports(
    bin64_path: Optional[str] = None,
    site_packages: Optional[str] = None,
    workdir: Optional[str] = None,
) -> List[int]:
    """Return listening ports for all fully running Sysplorer instances (official API).

    Wraps ``mworks.sysplorer.FindSysplorer()`` after the same runtime setup as
    :class:`MWorksDriver`. On any failure, returns an empty list.
    """
    wd = Path(workdir or os.environ.get("MWORKS_WORKDIR", str(DEFAULT_MWORKS_WORKDIR)))
    wd.mkdir(parents=True, exist_ok=True)

    try:
        if is_modelica_lite_platform():
            _prepare_runtime_without_bin64()
        else:
            bin64 = Path(bin64_path or os.environ.get("MWORKS_BIN64", str(DEFAULT_MWORKS_BIN64)))
            sp = Path(
                site_packages
                or os.environ.get("MWORKS_SYSPLORER_SITE_PACKAGES", str(DEFAULT_SYSPLORER_SITE_PACKAGES))
            )
            _configure_sysplorer_python_env(bin64, sp)
        from mworks.sysplorer import FindSysplorer  # type: ignore

        raw = FindSysplorer()
    except Exception:
        return []

    if raw is None:
        return []
    try:
        out: List[int] = []
        for p in list(raw):
            out.append(int(p))
        return out
    except (TypeError, ValueError):
        return []


def pick_new_sysplorer_port(before: Set[int], after: List[int]) -> Optional[int]:
    """Infer the port of a Sysplorer instance that appeared between two FindSysplorer snapshots.

    Used so each MCP host process can bind to *its* ``StartSysplorer`` instance instead of
    always using ``after[0]`` (which would attach every MCP to the same GUI).

    If several ports are new at once (e.g. concurrent ``StartSysplorer`` from multiple
    processes), the port that appears **last** in ``after`` (API list order) is returned
    and a warning is logged — callers may use an inter-process lock if they need a
    stronger guarantee.
    """
    log = logging.getLogger(__name__)
    before_set = {int(x) for x in before}
    new_in_order = [int(p) for p in after if int(p) not in before_set]
    if not new_in_order:
        return None
    if len(new_in_order) > 1:
        chosen = new_in_order[-1]
        log.warning(
            "FindSysplorer reported %d new port(s) after StartSysplorer; "
            "using last in API order (%s) for this MCP. "
            "Stagger MCP startup or serialize StartSysplorer if you need strict 1:1.",
            len(new_in_order),
            chosen,
        )
        return chosen
    return new_in_order[0]


def shutdown_all_sysplorer_via_exit(
    bin64_path: Optional[str] = None,
    site_packages: Optional[str] = None,
    workdir: Optional[str] = None,
) -> Dict[str, Any]:
    """Gracefully shut down every running Sysplorer instance via official API.

    Flow: ``FindSysplorer`` (via :func:`find_sysplorer_ports`) → for each port,
    purge ``mworks`` modules → ``ConnectSysplorer(port=…)`` → ``Exit()`` → purge
    again.  Callers that hold an :class:`MWorksDriver` to one of these instances
    should drop that reference before calling; each ``Exit()`` invalidates the
    GUI process.

    Returns a dict with ``ok``, ``exited_ports`` (int list), and ``errors``
    (str list).  When no instances are found, ``ok`` is True and lists are empty.
    """
    log = logging.getLogger(__name__)
    ports = find_sysplorer_ports(
        bin64_path=bin64_path,
        site_packages=site_packages,
        workdir=workdir,
    )
    MWorksDriver.purge_sysplorer_modules()

    unique_ports = sorted({int(p) for p in ports})
    if not unique_ports:
        return {"ok": True, "exited_ports": [], "errors": []}

    lite = is_modelica_lite_platform()
    bin64: Optional[Path] = None
    sp: Optional[Path] = None
    if not lite:
        bin64 = Path(bin64_path or os.environ.get("MWORKS_BIN64", str(DEFAULT_MWORKS_BIN64)))
        sp = Path(
            site_packages or os.environ.get("MWORKS_SYSPLORER_SITE_PACKAGES", str(DEFAULT_SYSPLORER_SITE_PACKAGES))
        )
    wd = Path(workdir or os.environ.get("MWORKS_WORKDIR", str(DEFAULT_MWORKS_WORKDIR)))
    wd.mkdir(parents=True, exist_ok=True)

    exited: List[int] = []
    errors: List[str] = []

    for port in unique_ports:
        try:
            MWorksDriver.purge_sysplorer_modules()
            if lite:
                _prepare_runtime_without_bin64()
            else:
                assert bin64 is not None and sp is not None
                _configure_sysplorer_python_env(bin64, sp)
            from mworks.sysplorer import ConnectSysplorer, Exit  # type: ignore

            ConnectSysplorer(port=port)
            raw = Exit()
            exited.append(port)
            log.info("Exit() on Sysplorer port %s returned %s", port, raw)
        except Exception as exc:
            msg = f"port {port}: {exc}"
            errors.append(msg)
            log.warning("shutdown_all_sysplorer_via_exit: %s", msg)
        finally:
            try:
                MWorksDriver.purge_sysplorer_modules()
            except Exception:
                pass

    ok = len(errors) == 0
    return {"ok": ok, "exited_ports": exited, "errors": errors}


def exit_sysplorer_on_port(
    port: int,
    bin64_path: Optional[str] = None,
    site_packages: Optional[str] = None,
    workdir: Optional[str] = None,
) -> Dict[str, Any]:
    """ConnectSysplorer(port) then Exit() for one instance (official API)."""
    log = logging.getLogger(__name__)
    wd = Path(workdir or os.environ.get("MWORKS_WORKDIR", str(DEFAULT_MWORKS_WORKDIR)))
    wd.mkdir(parents=True, exist_ok=True)
    try:
        MWorksDriver.purge_sysplorer_modules()
        if is_modelica_lite_platform():
            _prepare_runtime_without_bin64()
        else:
            bin64 = Path(bin64_path or os.environ.get("MWORKS_BIN64", str(DEFAULT_MWORKS_BIN64)))
            sp = Path(
                site_packages
                or os.environ.get("MWORKS_SYSPLORER_SITE_PACKAGES", str(DEFAULT_SYSPLORER_SITE_PACKAGES))
            )
            _configure_sysplorer_python_env(bin64, sp)
        from mworks.sysplorer import ConnectSysplorer, Exit  # type: ignore

        ConnectSysplorer(port=int(port))
        raw = Exit()
        log.info("Exit() on Sysplorer port %s returned %s", port, raw)
        return {"ok": True, "exited_ports": [int(port)], "errors": []}
    except Exception as exc:
        msg = f"port {port}: {exc}"
        log.warning("exit_sysplorer_on_port: %s", msg)
        return {"ok": False, "exited_ports": [], "errors": [msg]}
    finally:
        try:
            MWorksDriver.purge_sysplorer_modules()
        except Exception:
            pass


@dataclass
class CallResult:
    ok: bool
    api: str
    data: Any = None
    raw: Any = None
    error: str = ""
    warning: str = ""
    already_loaded: bool = False
    save_folder: str = ""
    saved_path: str = ""
    upstream_code: str = ""

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"ok": self.ok, "api": self.api}
        if self.data is not None:
            result["data"] = self.data
        if self.error:
            result["error"] = self.error
        if self.warning:
            result["warning"] = self.warning
        if self.already_loaded:
            result["already_loaded"] = True
        if self.save_folder:
            result["save_folder"] = self.save_folder
        if self.saved_path:
            result["saved_path"] = self.saved_path
        if self.upstream_code:
            result["upstreamCode"] = self.upstream_code
        return result

    def attach_official_upstream(self) -> "CallResult":
        """Parse ``错误(N)`` / ``Error(N)`` from ``error`` into ``upstreamCode``."""
        if self.ok or self.upstream_code:
            return self
        from core.tool_envelope import extract_official_error_code

        code = extract_official_error_code(self.error)
        if code:
            self.upstream_code = code
        return self



class MWorksDriver:
    """
    Wrapper around official Sysplorer Python API (`mworks.sysplorer`).
    """

    def __init__(
        self,
        bin64_path: Optional[str] = None,
        workdir: Optional[str] = None,
        force_start: bool = False,
        connect_port: Optional[int] = None,
        start_mode: str = "-gui",
    ) -> None:
        # modelica_lite attach: ConnectSysplorer only — do not resolve MWORKS_BIN64.
        self._skip_bin64 = is_modelica_lite_platform() and not force_start
        if self._skip_bin64:
            self.bin64_path = Path("")
            self.site_packages = Path("")
        else:
            self.bin64_path = Path(bin64_path or os.environ.get("MWORKS_BIN64", str(DEFAULT_MWORKS_BIN64)))
            self.site_packages = Path(
                os.environ.get("MWORKS_SYSPLORER_SITE_PACKAGES", str(DEFAULT_SYSPLORER_SITE_PACKAGES))
            )
        self.workdir = Path(workdir or os.environ.get("MWORKS_WORKDIR", str(DEFAULT_MWORKS_WORKDIR)))
        self._connect_port = connect_port
        self.workdir.mkdir(parents=True, exist_ok=True)
        try:
            self.workdir = _windows_short_path_if_exists(self.workdir.resolve())
            os.environ["MWORKS_WORKDIR"] = str(self.workdir)
        except OSError:
            pass

        if not self._skip_bin64:
            self.bin64_path, self.site_packages = _normalize_mworks_install_paths(
                self.bin64_path, self.site_packages
            )

        self._lock = threading.Lock()
        self._api: Dict[str, Any] = {}
        self._last_error: str = ""

        self._setup_environment()
        self._init_api(force_start=force_start, start_mode=start_mode)

    @staticmethod
    def python_compatibility() -> Dict[str, Any]:
        version = sys.version_info
        compatible = version.major == 3 and 10 <= version.minor <= 12
        return {
            "python_version": platform.python_version(),
            "major": version.major,
            "minor": version.minor,
            "compatible": compatible,
            "required": "3.10+ (recommended 3.11 for mworks-sysplorer)",
        }

    def _setup_environment(self) -> None:
        if self._skip_bin64:
            _prepare_runtime_without_bin64()
        else:
            _configure_sysplorer_python_env(self.bin64_path, self.site_packages)

    @staticmethod
    def purge_sysplorer_modules() -> None:
        """Remove all cached ``mworks.*`` modules from ``sys.modules``.

        The ``mworks.sysplorer`` package maintains a process-level singleton
        connection.  After the Sysplorer process is killed and restarted, the
        stale singleton prevents new connections.  Purging the module cache
        forces a fresh ``import`` which re-initialises the singleton.
        """
        to_remove = [key for key in sys.modules if key == "mworks" or key.startswith("mworks.")]
        for key in to_remove:
            del sys.modules[key]

    def _init_api(self, force_start: bool = False, start_mode: str = "-gui") -> None:
        try:
            # Import lazily after path setup.
            import mworks.sysplorer as sysplorer  # type: ignore
            from mworks.sysplorer import (  # type: ignore
                CheckModel,
                ClearAll,
                ConnectSysplorer,
                FindSysplorer,
                Exit,
                GetClasses,
                GetComponentDescription,
                GetComponentInfo,
                GetComponentPorts,
                GetComponents,
                GetModelDescription,
                GetModelText,
                LoadLibrary,
                NewModel,
                OpenModel,
                OpenModelFile,
                SaveModel,
                SetModelParamValue,
                SimulateModel,
                StartSysplorer,
                TranslateModel,
            )
        except Exception as exc:
            raise MWorksDriverError(f"Failed to import mworks.sysplorer: {exc}") from exc

        self._api = {
            "StartSysplorer": StartSysplorer,
            "ConnectSysplorer": ConnectSysplorer,
            "Exit": Exit,
            "ClearAll": ClearAll,
            "LoadLibrary": LoadLibrary,
            "NewModel": NewModel,
            "OpenModelFile": OpenModelFile,
            "OpenModel": OpenModel,
            "GetModelText": GetModelText,
            "GetModelDescription": GetModelDescription,
            "GetComponentDescription": GetComponentDescription,
            "SetModelParamValue": SetModelParamValue,
            "GetComponentInfo": GetComponentInfo,
            "GetComponentPorts": GetComponentPorts,
            "GetComponents": GetComponents,
            "GetClasses": GetClasses,
            "SaveModel": SaveModel,
            "CheckModel": CheckModel,
            "TranslateModel": TranslateModel,
            "SimulateModel": SimulateModel,
        }
        _erase = getattr(sysplorer, "EraseClasses", None)
        if callable(_erase):
            self._api["EraseClasses"] = _erase
        _class_exist = getattr(sysplorer, "ClassExist", None)
        if callable(_class_exist):
            self._api["ClassExist"] = _class_exist
        # Optional result/query APIs may be unavailable in certain runtimes.
        optional_api_names = [
            "ClassExist",
            "ExportDiagram",
            "CompareModel",
            "ExportDocumentation",
            "Help",
            "GetVarValueAt",
            "GetVarValues",
            "GetVarsValueAt",
            "GetVarsValues",
            "GetVarTimes",
            "GetResultVariables",
            "GetResultVariableInfo",
            "GetResultVariablesInfo",
            "CreatePlot",
            "CreatePlotEx",
            "ClearPlot",
            "CreateAnimation",
            "ExportResult",
            "ExportResultEx",
            "OpenResult",
            "RemoveResult",
            "RemoveResults",
            "GetLastErrors",
            "MessageText",
            "GetModelDependencies",
            "GetInstalledLibraries",
            "GetDirectory",
            "GetSimResultDirectory",
            "UpdateLibrary",
            "SaveModelAs",
            "SimulateModelEx",
            "StartSimulate",
            "GetSimulationState",
            "GetSimulationExitState",
            "ResimulateCurrentResult",
            "SetCompileSolver64",
            "GetCompileSolver64",
            "GetRestriction",
            "GetComponentTypeName",
        ]
        for name in optional_api_names:
            fn = getattr(sysplorer, name, None)
            if callable(fn):
                self._api[name] = fn

        # Cache SimulationTime enum values for GetVarValueAt time_point mapping.
        # SimulationTime.Begin / SimulationTime.End are used as special sentinel values.
        try:
            from mworks.sysplorer import SimulationTime  # type: ignore
            self._sim_time_begin = SimulationTime.Begin
            self._sim_time_end = SimulationTime.End
        except Exception:
            self._sim_time_begin = None
            self._sim_time_end = None

        # Connection strategy:
        #   force_start=False → ConnectSysplorer (attach to running instance)
        #   force_start=True  → StartSysplorer (launch full stack，官方API优先)
        # All retry/recovery logic lives in StackHealthManager.
        if force_start:
            try:
                # 唯一允许的启动路径：官方 StartSysplorer（禁止在本仓库用 subprocess 等直接起 mworks.exe）
                start_sysplorer_in_desktop_context(
                    self._api["StartSysplorer"],
                    _resolve_sysplorer_process_path(self.bin64_path),
                    start_mode=start_mode,
                )
            except Exception as exc:
                raise MWorksDriverError(f"StartSysplorer API failed: {exc}") from exc
        else:
            try:
                port = self._connect_port
                if port is None:
                    ports = FindSysplorer()
                    if ports:
                        port = int(ports[0])
                if port is not None:
                    self._api["ConnectSysplorer"](port=port)
                else:
                    raise MWorksDriverError(
                        "ConnectSysplorer requires an explicit port. "
                        "Official ConnectSysplorer() with no port calls StartSysplorer when "
                        "FindSysplorer is empty, which starts a second GUI."
                    )
            except Exception as exc:
                raise MWorksDriverError(f"ConnectSysplorer failed: {exc}") from exc

        # NOTE: Do NOT call ClearAll here. ClearAll clears Sysplorer's
        # compilation cache (translated binaries), causing SimulateModel /
        # TranslateModel to fail until the model is re-translated, which can
        # take minutes and may block the GUI. Instead, rely on explicit model
        # loading (LoadLibrary / OpenModelFile) to manage session state.

    def _best_effort_call(self, api: str, *args: Any, **kwargs: Any) -> None:
        try:
            fn = self._api.get(api)
            if callable(fn):
                fn(*args, **kwargs)
        except Exception:
            pass

    _MAX_DIAG_CHARS = 500
    _MAX_DIAG_ERRORS = 3

    def _get_last_diagnostics(self) -> str:
        """Collect diagnostic info from GetLastErrors/MessageText after a failed API call.

        Truncates output to at most _MAX_DIAG_ERRORS error items and _MAX_DIAG_CHARS total
        to avoid bloating MCP responses with multi-KB Sysplorer error dumps.
        """
        parts: list[str] = []
        try:
            fn_err = self._api.get("GetLastErrors")
            if callable(fn_err):
                errors = fn_err()
                if errors:
                    if isinstance(errors, list):
                        shown = errors[:self._MAX_DIAG_ERRORS]
                        text = "; ".join(str(e) for e in shown)
                        if len(errors) > self._MAX_DIAG_ERRORS:
                            text += f" ... (+{len(errors) - self._MAX_DIAG_ERRORS} more)"
                        parts.append("GetLastErrors: " + text)
                    else:
                        parts.append(f"GetLastErrors: {errors}")
        except Exception:
            pass
        try:
            fn_msg = self._api.get("MessageText")
            if callable(fn_msg):
                msg = fn_msg()
                if msg:
                    parts.append(f"MessageText: {msg}")
        except Exception:
            pass
        result = "\n".join(parts)
        if len(result) > self._MAX_DIAG_CHARS:
            result = result[:self._MAX_DIAG_CHARS] + "... (truncated)"
        return result

    def _open_model_file_result(self, path: str, auto_reload: Optional[bool]) -> CallResult:
        """Call official ``OpenModelFile(path)`` or ``OpenModelFile(path, autoReload=…)``."""
        with self._lock:
            fn = self._api.get("OpenModelFile")
            if not callable(fn):
                return CallResult(ok=False, api="OpenModelFile", error="API not found: OpenModelFile")
            try:
                if auto_reload is None:
                    raw = fn(path)
                else:
                    try:
                        raw = fn(path, auto_reload)
                    except TypeError:
                        raw = fn(path, autoReload=auto_reload)
            except Exception as exc:
                self._last_error = str(exc)
                return CallResult(ok=False, api="OpenModelFile", error=f"OpenModelFile failed: {exc}").attach_official_upstream()

            if isinstance(raw, bool) and not raw:
                diag = self._get_last_diagnostics()
                err_msg = "OpenModelFile returned False"
                if diag:
                    err_msg += f"\n{diag}"
                return CallResult(ok=False, api="OpenModelFile", data=raw, raw=raw, error=err_msg).attach_official_upstream()

        if isinstance(raw, bool):
            return CallResult(ok=True, api="OpenModelFile", data=raw, raw=raw)
        if raw is None:
            return CallResult(ok=True, api="OpenModelFile", data=None, raw=None)
        return CallResult(ok=True, api="OpenModelFile", data=raw, raw=raw)

    def _call(self, api: str, *args: Any, **kwargs: Any) -> CallResult:
        with self._lock:
            fn = self._api.get(api)
            if not callable(fn):
                return CallResult(ok=False, api=api, error=f"API not found: {api}")

            try:
                raw = fn(*args, **kwargs)
            except Exception as exc:
                self._last_error = str(exc)
                return CallResult(ok=False, api=api, error=f"{api} failed: {exc}").attach_official_upstream()

            # Collect diagnostics while still holding the lock (last-command state is global)
            if isinstance(raw, bool) and not raw:
                diag = self._get_last_diagnostics()
                err_msg = f"{api} returned False"
                if diag:
                    err_msg += f"\n{diag}"
                return CallResult(ok=False, api=api, data=raw, raw=raw, error=err_msg).attach_official_upstream()

        if isinstance(raw, bool):
            return CallResult(ok=True, api=api, data=raw, raw=raw)
        if raw is None:
            return CallResult(ok=True, api=api, data=None, raw=None)
        return CallResult(ok=True, api=api, data=raw, raw=raw)

    def health_check(self) -> Dict[str, Any]:
        return {
            "ok": True,
            "python": self.python_compatibility(),
            "bin64_path": str(self.bin64_path),
            "workdir": str(self.workdir),
            "site_packages": str(self.site_packages),
            "api_ready": bool(self._api),
        }

    def load_file(self, file_path: str, auto_reload: Optional[bool] = None) -> CallResult:
        """Load a ``.mo`` / ``.mol`` via ``OpenModelFile``.

        ``auto_reload``: official second argument *autoReload* — when ``True``, reload if the model
        is already open. When ``None`` (default), a first attempt uses the single-arg call; if the
        failure looks like “already loaded / duplicate”, automatically retries with ``autoReload=True``
        instead of clearing the workspace.

        Before ``OpenModelFile``, drops the last session result (``RemoveResult``) so
        ``GetResultVariables`` does not keep listing a prior same-name run.
        """
        path = str(Path(file_path).resolve())
        drop = self.drop_last_session_result()
        res = self._open_model_file_result(path, auto_reload)
        if res.ok:
            res.warning = self._merge_warning(res.warning, drop.warning)
            return res
        if auto_reload is True:
            res.warning = self._merge_warning(res.warning, drop.warning)
            return res
        if _looks_like_openmodelfile_duplicate_or_loaded_error(res.error or ""):
            res2 = self._open_model_file_result(path, True)
            if res2.ok:
                res2.warning = (
                    (res2.warning + " ") if res2.warning else ""
                ) + "OpenModelFile succeeded after retry with autoReload=True (duplicate/already-loaded style error)."
            res2.warning = self._merge_warning(res2.warning, drop.warning)
            return res2
        res.warning = self._merge_warning(res.warning, drop.warning)
        return res

    def load_library(self, library_name: str, library_version: str = "") -> CallResult:
        lib, ver = normalize_load_library_call(library_name, library_version)
        if not lib:
            return CallResult(ok=False, api="LoadLibrary", error="library_name is required")
        # 先 ClassExist(顶层包名)：已加载则跳过 LoadLibrary，避免重复解析大库与无意义 API 往返。
        if callable(self._api.get("ClassExist")):
            ce = self.class_exist(lib)
            if ce.ok and ce.data:
                return CallResult(
                    ok=True,
                    api="LoadLibrary",
                    data=True,
                    raw=True,
                    warning="已跳过 LoadLibrary：ClassExist 表明该顶层包已在工作区加载",
                    already_loaded=True,
                )
        if ver:
            return self._call("LoadLibrary", lib, ver)
        return self._call("LoadLibrary", lib)

    def get_model_dependencies(self, model_name: str) -> CallResult:
        """Return model library dependencies via official GetModelDependencies API."""
        name = (model_name or "").strip()
        if not name:
            return CallResult(ok=False, api="GetModelDependencies", error="model_name is required")
        return self._call("GetModelDependencies", name)

    def get_installed_libraries(self) -> CallResult:
        """Return installed model libraries via official GetInstalledLibraries API."""
        return self._call("GetInstalledLibraries")

    def get_directory(self) -> CallResult:
        """Return Sysplorer working directory via official ``GetDirectory()`` (no args).

        User-generated content (new/saved models, etc.) is placed under this directory.
        Distinct from MCP ``WORKSPACE_ROOT`` / ``MWORKS_WORKDIR``.
        """
        return self._call("GetDirectory")

    def get_sim_result_directory(self) -> CallResult:
        """Return Sysplorer simulation-result directory via official ``GetSimResultDirectory()``.

        Distinct from MCP ``MWORKS_SIM_DIR`` (config default) and from ``GetDirectory()`` (working dir).
        """
        return self._call("GetSimResultDirectory")

    def update_library(self) -> CallResult:
        """Refresh Sysplorer's library catalog via official UpdateLibrary API."""
        with self._lock:
            fn = self._api.get("UpdateLibrary")
            if not callable(fn):
                return CallResult(ok=False, api="UpdateLibrary", error="API not found: UpdateLibrary")
            try:
                raw = fn()
            except Exception as exc:
                self._last_error = str(exc)
                return CallResult(ok=False, api="UpdateLibrary", error=f"UpdateLibrary failed: {exc}")
        if isinstance(raw, bool):
            return CallResult(ok=raw, api="UpdateLibrary", data=raw, raw=raw, error="" if raw else "UpdateLibrary returned False")
        return CallResult(ok=False, api="UpdateLibrary", data=raw, raw=raw, error="UpdateLibrary returned non-bool result")

    def open_model(self, model_name: str) -> CallResult:
        model_name = (model_name or "").strip()
        if not model_name:
            return CallResult(ok=False, api="OpenModel", error="model_name is required")
        return self._call("OpenModel", model_name)

    def export_documentation(self, model_name: str, doc_file: str) -> CallResult:
        """Export class documentation to an HTML file via ModelingPy ``ExportDocumentation``."""
        name = (model_name or "").strip()
        path = (doc_file or "").strip()
        if not name:
            return CallResult(ok=False, api="ExportDocumentation", error="model_name is required")
        if not path:
            return CallResult(ok=False, api="ExportDocumentation", error="doc_file is required")
        return self._call("ExportDocumentation", name, path)

    def api_help(self, cmd: str = "") -> CallResult:
        """Return Sysplorer Python API help via official ``Help`` / ``Help(cmd)``.

        Official 26.6 ``Help(cmd)`` prints ``help(fn)`` to stdout and returns ``None``.
        Capture that print; do not treat a ``None`` return as empty documentation.
        """
        from core.official_help import help_text_from_invoke, invoke_modelingpy_help

        ensure_modelica_lite_site_helpers()
        with self._lock:
            fn = self._api.get("Help")
            if not callable(fn):
                return CallResult(ok=False, api="Help", error="API not found: Help")
            try:
                raw, printed = invoke_modelingpy_help(fn, (cmd or "").strip())
            except Exception as exc:
                self._last_error = str(exc)
                return CallResult(ok=False, api="Help", error=f"Help failed: {exc}")
        text = help_text_from_invoke(raw, printed)
        if not str(text).strip() and key:
            target = self._api.get(key)
            if callable(target) and key.lower() != "help":
                from core.official_help import render_function_help

                rendered = render_function_help(target)
                if rendered.strip():
                    text = rendered
        return CallResult(ok=True, api="Help", data=text, raw=raw)

    def export_diagram(
        self,
        model_name: str,
        output_path: str,
        width: int = 800,
        height: int = 600,
    ) -> CallResult:
        """Export the model Diagram view to a raster image (ModelingPy ExportDiagram)."""
        name = (model_name or "").strip()
        path = (output_path or "").strip()
        if not name:
            return CallResult(ok=False, api="ExportDiagram", error="model_name is required")
        if not path:
            return CallResult(ok=False, api="ExportDiagram", error="output_path is required")
        try:
            w = int(width)
            h = int(height)
        except (TypeError, ValueError):
            return CallResult(ok=False, api="ExportDiagram", error="width and height must be integers")
        return self._call("ExportDiagram", name, path, w, h)

    def compare_model(
        self,
        model_name_a: str,
        model_name_b: str,
        is_file: bool = False,
    ) -> CallResult:
        """Open the GUI model comparison view (ModelingPy ``CompareModel``).

        Current official shape (verify at runtime): ``CompareModel(firstModel, secondModel, isFile) -> bool``.
        Use ``get_api_document("CompareModel")`` or ``ListFunctions()`` when the installed Sysplorer build may differ.
        ``is_file=False``: ``firstModel`` / ``secondModel`` are fully-qualified loaded model names.
        ``is_file=True``: both arguments are ``.mo`` file paths.
        """
        a = (model_name_a or "").strip()
        b = (model_name_b or "").strip()
        if not a:
            return CallResult(ok=False, api="CompareModel", error="model_name_a is required")
        if not b:
            return CallResult(ok=False, api="CompareModel", error="model_name_b is required")
        fn = self._api.get("CompareModel")
        if not callable(fn):
            return CallResult(
                ok=False,
                api="CompareModel",
                error="CompareModel is not available in this Sysplorer runtime",
                data={
                    "hint": (
                        "Run ModelingPy.ListFunctions() on this instance, then "
                        "get_api_document('CompareModel') for Help text."
                    ),
                },
            )
        return self._call("CompareModel", a, b, bool(is_file))

    def new_model(self, model_name: str, restriction: str = "model") -> CallResult:
        """Create a new model via official ``NewModel``.

        Args:
            model_name: Name of the new model
            restriction: Official class restriction (``model`` / ``package`` / ``block`` / …).
                ``Sysblock`` is still accepted when the caller asks for a block diagram.
        """
        model_name = (model_name or "").strip()
        if not model_name:
            return CallResult(ok=False, api="NewModel", error="model_name is required")
        kind = (restriction or "model").strip() or "model"
        result = self._call("NewModel", model_name, kind)
        if not result.ok:
            return result
        created = result.data
        if created is None or (isinstance(created, str) and not str(created).strip()):
            diag = self._get_last_diagnostics()
            err = "NewModel returned an empty name (model was not created)"
            if diag:
                err += f"\n{diag}"
            return CallResult(ok=False, api="NewModel", data=created, raw=result.raw, error=err).attach_official_upstream()
        return result

    def unload_file(self, model_name: str) -> CallResult:
        """Unload a loaded class tree via official ``EraseClasses`` (tuple of fully-qualified names).

        Does **not** call ``ClearAll`` (which wipes libraries, translation cache, and results).
        """
        name = (model_name or "").strip()
        if not name:
            return CallResult(ok=False, api="EraseClasses", error="model_name is required")
        erase = self._api.get("EraseClasses")
        if not callable(erase):
            return CallResult(
                ok=False,
                api="EraseClasses",
                error="EraseClasses is not available in this Sysplorer runtime",
            )
        return self._call("EraseClasses", (name,))

    def get_last_errors(self) -> CallResult:
        """Official ``GetLastErrors()`` (plural). There is no ``GetLastError``."""
        fn = self._api.get("GetLastErrors")
        if not callable(fn):
            return CallResult(
                ok=False,
                api="GetLastErrors",
                error="GetLastErrors is not available in this Sysplorer runtime (not GetLastError)",
            )
        with self._lock:
            try:
                raw = fn()
            except Exception as exc:
                self._last_error = str(exc)
                return CallResult(ok=False, api="GetLastErrors", error=f"GetLastErrors failed: {exc}")
        return CallResult(ok=True, api="GetLastErrors", data=raw, raw=raw)

    def class_exist(self, class_name: str) -> CallResult:
        """官方 ``ClassExist(className)`` → 类型是否已在工作区加载。

        注意：返回值 ``False`` 表示「未加载」，仍视为调用成功；不可用 :meth:`_call`（其将 bool False 当作 API 失败）。
        """
        name = (class_name or "").strip()
        if not name:
            return CallResult(ok=False, api="ClassExist", error="class_name is required")
        fn = self._api.get("ClassExist")
        if not callable(fn):
            return CallResult(ok=False, api="ClassExist", error="ClassExist is not available in this Sysplorer runtime")
        with self._lock:
            try:
                raw = fn(name)
            except Exception as exc:
                self._last_error = str(exc)
                return CallResult(ok=False, api="ClassExist", error=f"ClassExist failed: {exc}")
        return CallResult(ok=True, api="ClassExist", data=bool(raw), raw=raw)

    def unload_loaded_classes_for_mo(self, mo_path: str) -> CallResult:
        """重载磁盘 ``.mo`` 前：对目录式 package 只 ``EraseClasses`` 根包；独立文件只卸该类全名。

        不再沿 ``within`` 前缀链误卸父包后再单独打开子 ``.mo``（会丢失 package 上下文）。
        无 ``ClassExist`` 时退化为对候选名依次 ``EraseClasses``（失败忽略），以兼容旧运行时。
        """
        from core.utils import erase_candidates_for_mo_path

        path = Path(str(mo_path)).resolve()
        candidates = erase_candidates_for_mo_path(path)
        details: List[Dict[str, Any]] = []
        use_ce = callable(self._api.get("ClassExist"))

        for cname in candidates:
            if use_ce:
                ce = self.class_exist(cname)
                if not ce.ok:
                    return CallResult(
                        ok=False,
                        api="unload_loaded_classes_for_mo",
                        error=f"ClassExist({cname!r}): {ce.error}",
                        data=details,
                    )
                if not ce.data:
                    details.append({"class": cname, "class_exist": False, "erased": False})
                    continue
                er = self.unload_file(cname)
                row = {"class": cname, "class_exist": True, "erased": er.ok}
                if not er.ok:
                    row["erase_error"] = er.error
                    return CallResult(
                        ok=False,
                        api="unload_loaded_classes_for_mo",
                        error=f"EraseClasses({cname!r}) failed: {er.error}",
                        data=details + [row],
                    )
                details.append(row)
            else:
                er = self.unload_file(cname)
                details.append(
                    {
                        "class": cname,
                        "class_exist": None,
                        "erased": er.ok,
                        "erase_error": er.error or "",
                    }
                )

        return CallResult(ok=True, api="unload_loaded_classes_for_mo", data=details, raw=candidates)

    def lookup_component(self, model_name: str, comp_name: str, info_type: str = "") -> CallResult:
        # Sysplorer GetComponentInfo requires infoType.
        return self._call("GetComponentInfo", model_name, comp_name, info_type)

    def get_model_text(self, model_name: str) -> CallResult:
        return self._call("GetModelText", model_name)

    def get_model_description(self, model_name: str) -> CallResult:
        return self._call("GetModelDescription", model_name)

    def get_component_description(self, model_name: str, comp_name: str) -> CallResult:
        return self._call("GetComponentDescription", model_name, comp_name)

    def get_classes(self, model_name: str) -> CallResult:
        """Official ``GetClasses``. Empty name is the top-level list; a missing class is failure."""
        name = "" if model_name is None else str(model_name)
        if name.strip() and callable(self._api.get("ClassExist")):
            ce = self.class_exist(name.strip())
            if ce.ok and not ce.data:
                return CallResult(
                    ok=False,
                    api="GetClasses",
                    data=[],
                    error=f"class not found: {name.strip()!r} (ClassExist is false)",
                )
        return self._call("GetClasses", name)

    def get_restriction(self, class_name: str) -> CallResult:
        """Official ``GetRestriction(className)`` — package / model / block / connector / …"""
        name = (class_name or "").strip()
        if not name:
            return CallResult(ok=False, api="GetRestriction", error="class_name is required")
        return self._call("GetRestriction", name)

    def get_components(self, model_name: str, component: str = "") -> CallResult:
        return self._call("GetComponents", model_name, component)

    def get_component_type_name(
        self,
        model_name: str,
        component_name: str,
        full_name: bool = False,
    ) -> CallResult:
        """Official ``GetComponentTypeName``: type name of a component (or a parameter name from GetComponents)."""
        return self._call("GetComponentTypeName", model_name, component_name, bool(full_name))

    def get_component_ports(self, model_name: str, component_name: str, port_direction: int = 0) -> CallResult:
        """Official ``GetComponentPorts``. Model must already be ``OpenModel``'d or the result is often ``[]``."""
        return self._call("GetComponentPorts", model_name, component_name, port_direction)

    def save_loaded_model(self, model_name: str, saved_path: str = "") -> CallResult:
        """Official ``SaveModel``: overwrite the file this class was loaded from."""
        name = (model_name or "").strip()
        if not name:
            return CallResult(ok=False, api="SaveModel", error="model_name is required")
        result = self._call("SaveModel", name)
        path = (saved_path or "").strip()
        if path:
            result.saved_path = path
        return result

    def save_model(self, model_name: str, folder: str = "", save_type: int = 0) -> CallResult:
        # save_type has no corresponding Sysplorer API parameter and is ignored.
        # Never SaveModel into GetDirectory() itself: that writes package.mo as if the
        # working directory were the task package root. Always SaveModelAs into a subfolder.
        from core.utils import guess_saved_model_path, resolve_model_save_folder

        name = (model_name or "").strip()
        if not name:
            return CallResult(ok=False, api="SaveModelAs", error="model_name is required")

        workdir = ""
        gd = self.get_directory()
        if gd.ok and gd.data not in (None, ""):
            workdir = str(gd.data).strip()
        if not workdir:
            workdir = str(getattr(self, "workdir", "") or "").strip()
        if not workdir:
            return CallResult(
                ok=False,
                api="SaveModelAs",
                error="cannot resolve Sysplorer working directory for save",
            )

        try:
            resolved = resolve_model_save_folder(name, folder, workdir)
        except ValueError as exc:
            return CallResult(ok=False, api="SaveModelAs", error=str(exc))

        target: Path = resolved["folder"]
        try:
            target.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            return CallResult(
                ok=False,
                api="SaveModelAs",
                error=f"cannot create save folder {target}: {exc}",
            )

        save_as = self._api.get("SaveModelAs")
        if not callable(save_as):
            return CallResult(
                ok=False,
                api="SaveModelAs",
                error=(
                    "SaveModelAs is not available; refusing SaveModel into GetDirectory() "
                    "(that would place package.mo in the working directory itself)"
                ),
                save_folder=str(target),
            )

        result = self._call("SaveModelAs", name, str(target))
        result.save_folder = str(target.resolve()) if target.exists() else str(target)
        result.saved_path = guess_saved_model_path(target, name)
        if resolved["redirected"]:
            note = (
                f"Saved to task subfolder {result.save_folder} "
                f"(not GetDirectory itself). Pass folder= that subfolder to keep this location."
            )
            result.warning = f"{result.warning} {note}".strip() if result.warning else note
        return result

    def check_model(self, model_name: str, model_type: str = "MODELICA") -> CallResult:
        # Sysplorer CheckModel(modelName) only accepts the model name;
        # model_type has no corresponding API parameter and is ignored.
        return self._call("CheckModel", model_name)

    def _ensure_modelica_lite_compile_solver_64(self) -> str:
        """``modelica_lite``: default translate/simulate to 64-bit via ``SetCompileSolver64(1)``.

        Returns a warning string only when the preference could not be applied; empty on
        success or when the platform is not ``modelica_lite``.
        """
        if not is_modelica_lite_platform():
            return ""
        if not callable(self._api.get("SetCompileSolver64")):
            return (
                "modelica_lite: SetCompileSolver64 unavailable; "
                "cannot force 64-bit compile solver before translate/simulate"
            )
        set_res = self._call("SetCompileSolver64", 1)
        if not set_res.ok:
            return (
                "modelica_lite: SetCompileSolver64(1) failed "
                f"({set_res.error or 'unknown'}); translate/simulate may not use 64-bit"
            )
        return ""

    @staticmethod
    def _merge_warning(existing: str, note: str) -> str:
        note = (note or "").strip()
        if not note:
            return existing or ""
        existing = (existing or "").strip()
        if not existing:
            return note
        if note in existing:
            return existing
        return f"{note} | {existing}"

    def translate_model(
        self,
        model_name: str,
        code_folder: str,
        model_type: str = "MODELICA",
        code_type: str = "NORMAL",
        build_type: str = "BINARY",
        run_to: str = "MAKING",
        config_json: str = "",
    ) -> CallResult:
        # Sysplorer TranslateModel(modelName) only accepts the model name.
        # code_folder, model_type, code_type, build_type, run_to, config_json
        # have no corresponding parameters in this API version and are ignored.
        lite_note = self._ensure_modelica_lite_compile_solver_64()
        result = self._call("TranslateModel", model_name)
        result.warning = self._merge_warning(result.warning, lite_note)
        return result

    # SIM_MODE constants (Sysplorer API official values)
    # Authoritative semantics: MCP get_api_document("SimulateModel") (runtime Help(cmd)).
    #   0 = use current simulation mode (Sysplorer auto-handles translate if needed)
    #   1 = standalone simulation
    #   2 = real-time simulation
    SIM_MODE_CURRENT = 0
    SIM_MODE_STANDALONE = 1
    SIM_MODE_REALTIME = 2

    _VALID_API_SIM_MODES = {0, 1, 2}

    def simulate_model(
        self,
        model_name: str,
        sim_mode: int = 0,
        target_time: Optional[List[float]] = None,
        ext_res_path: str = "",
    ) -> CallResult:
        """Run simulation via Sysplorer SimulateModel API.

        sim_mode semantics (see MCP get_api_document("SimulateModel")):
            0 → use current simulation mode (Sysplorer auto-handles translate if needed)
            1 → standalone simulation
            2 → real-time simulation

        NOTE: sim_mode values other than 0/1/2 are clamped to 0 with a warning.
        On ``modelica_lite``, calls ``SetCompileSolver64(1)`` first so auto-translate
        and simulate default to 64-bit.

        target_time[0] → startTime, target_time[1] → stopTime.
        ext_res_path → path (result output directory).

        Drops the last session result before ``SimulateModel`` so result APIs bind
        to this run, not a leftover same-name simulation.
        """
        model_name = model_name.strip()
        if not model_name:
            return CallResult(ok=False, api="SimulateModel", error="model_name is required")

        lite_note = self._ensure_modelica_lite_compile_solver_64()

        if sim_mode in self._VALID_API_SIM_MODES:
            api_sim_mode = sim_mode
            translate_warning = ""
        else:
            # Unknown sim_mode: clamp to 0 and add warning
            api_sim_mode = self.SIM_MODE_CURRENT
            translate_warning = (
                f"sim_mode={sim_mode} is not a valid Sysplorer API value (valid: 0/1/2). "
                f"Clamped to simMode=0."
            )

        kwargs: Dict[str, Any] = {"simMode": api_sim_mode}
        if target_time:
            if len(target_time) >= 1:
                kwargs["startTime"] = float(target_time[0])
            if len(target_time) >= 2:
                kwargs["stopTime"] = float(target_time[1])
        if ext_res_path:
            kwargs["path"] = str(ext_res_path)

        drop = self.drop_last_session_result()
        result = self._call("SimulateModel", model_name, **kwargs)
        result.warning = self._merge_warning(result.warning, translate_warning)
        result.warning = self._merge_warning(result.warning, lite_note)
        result.warning = self._merge_warning(result.warning, drop.warning)
        return result

    def remove_result(self) -> CallResult:
        return self._call("RemoveResult")

    def remove_results(self) -> CallResult:
        return self._call("RemoveResults")

    def drop_last_session_result(self) -> CallResult:
        """Drop the last/current session result so later reads are not a prior run.

        Same-name ``OpenModelFile`` / ``SimulateModel`` often leave ``GetResultVariables``
        bound to the previous result with no error. ``RemoveResult`` closes that last
        result; if that command is missing, fall back to ``RemoveResults``.
        A False return (nothing open) is treated as success. Missing both APIs is a
        warning, not a hard failure.
        """
        api_map = getattr(self, "_api", None) or {}
        if callable(api_map.get("RemoveResult")):
            r = self._call("RemoveResult")
            if r.ok:
                return r
            if "returned False" in (r.error or ""):
                return CallResult(ok=True, api="RemoveResult", data=r.data, raw=r.raw)
            return CallResult(
                ok=True,
                api="RemoveResult",
                warning=r.error or "RemoveResult failed",
                data=r.data,
                raw=r.raw,
            )
        if callable(api_map.get("RemoveResults")):
            r = self._call("RemoveResults")
            note = "RemoveResult unavailable; used RemoveResults"
            if r.ok or "returned False" in (r.error or ""):
                return CallResult(
                    ok=True,
                    api="RemoveResults",
                    warning=note,
                    data=r.data,
                    raw=r.raw,
                )
            return CallResult(
                ok=True,
                api="RemoveResults",
                warning=self._merge_warning(note, r.error or "RemoveResults failed"),
                data=r.data,
                raw=r.raw,
            )
        return CallResult(
            ok=True,
            api="RemoveResult",
            warning=(
                "RemoveResult/RemoveResults not available; session result was not cleared. "
                "GetResultVariables may still list a prior same-name run."
            ),
        )

    def open_result(self, result_file: str) -> CallResult:
        result_file = result_file.strip()
        if not result_file:
            return CallResult(ok=False, api="OpenResult", error="result_file is required")
        return self._call("OpenResult", result_file)

    def get_result_variables(self, var_type: int = 0) -> CallResult:
        return self._call("GetResultVariables", int(var_type))

    def get_result_variable_info(self, var_name: str, info_type: str) -> CallResult:
        """Official ``GetResultVariableInfo(varName, infoType)`` — infoType e.g. Type, Unit, Variability."""
        var_name = (var_name or "").strip()
        it = (info_type or "").strip()
        if not var_name:
            return CallResult(ok=False, api="GetResultVariableInfo", error="var_name is required")
        if not it:
            return CallResult(ok=False, api="GetResultVariableInfo", error="info_type is required")
        return self._call("GetResultVariableInfo", var_name, it)

    def get_var_values(self, var_name: str) -> CallResult:
        var_name = var_name.strip()
        if not var_name:
            return CallResult(ok=False, api="GetVarValues", error="var_name is required")
        return self._call("GetVarValues", var_name)

    def _resolve_time_point(self, time_point: Any) -> Any:
        """Map MCP time_point to SimulationTime enum or float.

        See MCP get_api_document("GetVarValueAt"). GetVarValueAt accepts:
          - numeric float/int value
          - SimulationTime.Begin  (start of simulation)
          - SimulationTime.End    (end of simulation)
        """
        from core.result_time import parse_result_time_point

        parsed = parse_result_time_point(time_point)
        if parsed.kind == "error":
            raise ValueError(parsed.error)
        if parsed.kind == "end":
            return self._sim_time_end if self._sim_time_end is not None else "end"
        if parsed.kind == "begin":
            return self._sim_time_begin if self._sim_time_begin is not None else "begin"
        return float(parsed.numeric)

    def _interpolate_var_at(self, var_name: str, t: float) -> CallResult:
        from core.result_time import interpolate_series_at_time, series_to_floats

        times_r = self.get_var_times()
        vals_r = self.get_var_values(var_name)
        if not times_r.ok:
            return CallResult(ok=False, api="GetVarValueAt", error=times_r.error or "GetVarTimes failed")
        if not vals_r.ok:
            return CallResult(ok=False, api="GetVarValueAt", error=vals_r.error or "GetVarValues failed")
        times = series_to_floats(times_r.data)
        values = series_to_floats(vals_r.data)
        y = interpolate_series_at_time(times, values, t)
        if y is None:
            return CallResult(
                ok=False,
                api="GetVarValueAt",
                error=f"cannot interpolate {var_name!r} at t={t}: empty GetVarTimes/GetVarValues",
            )
        return CallResult(
            ok=True,
            api="GetVarValueAt",
            data=y,
            raw=y,
            warning=f"GetVarValueAt empty at t={t}; interpolated from GetVarTimes/GetVarValues",
        )

    def _interpolate_vars_at(self, names: List[str], t: float) -> CallResult:
        from core.result_time import interpolate_series_at_time, series_to_floats

        times_r = self.get_var_times()
        vals_r = self.get_vars_values(names)
        if not times_r.ok:
            return CallResult(ok=False, api="GetVarsValueAt", error=times_r.error or "GetVarTimes failed")
        if not vals_r.ok:
            return CallResult(ok=False, api="GetVarsValueAt", error=vals_r.error or "GetVarsValues failed")
        times = series_to_floats(times_r.data)
        payload = vals_r.data
        series_list: List[Any]
        if isinstance(payload, dict):
            series_list = [payload.get(n) for n in names]
        elif isinstance(payload, (list, tuple)):
            series_list = list(payload)
        else:
            series_list = [payload]
        out: List[Any] = []
        for i, name in enumerate(names):
            raw_s = series_list[i] if i < len(series_list) else None
            values = series_to_floats(raw_s)
            y = interpolate_series_at_time(times, values, t)
            if y is None:
                return CallResult(
                    ok=False,
                    api="GetVarsValueAt",
                    error=f"cannot interpolate {name!r} at t={t}: empty series",
                )
            out.append(y)
        return CallResult(
            ok=True,
            api="GetVarsValueAt",
            data=out,
            raw=out,
            warning=f"GetVarsValueAt empty at t={t}; interpolated from GetVarTimes/GetVarsValues",
        )

    def get_var_value_at(self, var_name: str, time_point: Any = "end") -> CallResult:
        from core.result_time import is_empty_at_value, parse_result_time_point

        var_name = var_name.strip()
        if not var_name:
            return CallResult(ok=False, api="GetVarValueAt", error="var_name is required")
        parsed = parse_result_time_point(time_point)
        if parsed.kind == "error":
            return CallResult(ok=False, api="GetVarValueAt", error=parsed.error)
        try:
            resolved = self._resolve_time_point(time_point)
        except ValueError as exc:
            return CallResult(ok=False, api="GetVarValueAt", error=str(exc))
        result = self._call("GetVarValueAt", var_name, resolved)
        if parsed.kind == "numeric" and (not result.ok or is_empty_at_value(result.data)):
            filled = self._interpolate_var_at(var_name, float(parsed.numeric))
            if filled.ok:
                return filled
            err = filled.error or result.error or f"no value at t={parsed.numeric}"
            return CallResult(ok=False, api="GetVarValueAt", error=err, data=result.data, raw=result.raw)
        return result

    def get_vars_values(self, var_names: Optional[List[str]] = None) -> CallResult:
        names = [str(x).strip() for x in (var_names or []) if str(x).strip()]
        return self._call("GetVarsValues", names)

    def get_vars_value_at(self, var_names: Optional[List[str]] = None, time_point: Any = "end") -> CallResult:
        from core.result_time import is_empty_at_value, parse_result_time_point

        names = [str(x).strip() for x in (var_names or []) if str(x).strip()]
        parsed = parse_result_time_point(time_point)
        if parsed.kind == "error":
            return CallResult(ok=False, api="GetVarsValueAt", error=parsed.error)
        try:
            resolved = self._resolve_time_point(time_point)
        except ValueError as exc:
            return CallResult(ok=False, api="GetVarsValueAt", error=str(exc))
        result = self._call("GetVarsValueAt", names, resolved)
        if parsed.kind == "numeric" and (not result.ok or is_empty_at_value(result.data)):
            filled = self._interpolate_vars_at(names, float(parsed.numeric))
            if filled.ok:
                return filled
            err = filled.error or result.error or f"no values at t={parsed.numeric}"
            return CallResult(ok=False, api="GetVarsValueAt", error=err, data=result.data, raw=result.raw)
        return result

    def get_var_times(self) -> CallResult:
        return self._call("GetVarTimes")

    def create_plot(
        self,
        variables: Optional[List[str]] = None,
        heading: str = "",
        clear_first: bool = False,
        result_file: str = "",
    ) -> CallResult:
        """Create a plot window in Sysplorer.

        CreatePlot signature (see MCP get_api_document("CreatePlot") / "CreatePlotEx"):
            CreatePlot(id, position, x, y, heading, grid, ...)
            id=0 → new window
            position=[] → default position (reserved, not supported in 2026a)
            x="time" → independent variable (string)
            y=[...] → list of variable names to plot
            heading → plot title

        Tries CreatePlotEx as fallback if CreatePlot returns False.
        Always returns ok=True with a warning if both fail (headless/no-window mode).
        """
        vars_clean = [str(x).strip() for x in (variables or []) if str(x).strip()]
        if not vars_clean:
            return CallResult(ok=False, api="CreatePlot", error="variables is required")
        if clear_first:
            self._best_effort_call("ClearPlot", True)

        # Correct parameter order per API docs:
        # CreatePlot(id, position, x, y, heading, ...)
        #   id=0 (new window), position=[] (default), x="time" (independent var),
        #   y=vars_clean (variable list), heading=heading (title)
        plot_kwargs: Dict[str, Any] = {}
        if result_file:
            plot_kwargs["resultFile"] = result_file

        result = self._call("CreatePlot", 0, [], "time", vars_clean, heading or "", **plot_kwargs)
        if not result.ok:
            # Fallback: CreatePlotEx with option dict
            ex_option: Dict[str, Any] = {"heading": heading or ""}
            if result_file:
                ex_option["resultFile"] = result_file
            fn = self._api.get("CreatePlotEx")
            if callable(fn):
                try:
                    raw2 = fn(variables=vars_clean, option=ex_option)
                    if raw2:
                        return CallResult(ok=True, api="CreatePlotEx", data=raw2, raw=raw2,
                                          warning="CreatePlot returned False; used CreatePlotEx fallback")
                except Exception:
                    pass
            # Both failed — likely headless mode. Return non-blocking warning.
            return CallResult(ok=True, api="CreatePlot", data=None, raw=False,
                              warning="plot_api_unavailable: CreatePlot and CreatePlotEx both returned False "
                                      "(headless or no active window). Use matplotlib to visualize result data.")
        return result

    def create_animation(self) -> CallResult:
        return self._call("CreateAnimation")

    def set_model_param(self, model_name: str, param_name: str, value: Any, component: str = "") -> CallResult:
        # Sysplorer SetModelParamValue(modelName, component, paramName, value).
        # component identifies the sub-component owning the parameter; use "" for top-level params.
        # String-typed params need quoted literals in value, e.g. '"平均值"' not 平均值.
        return self._call("SetModelParamValue", model_name, component, param_name, str(value))

    def as_json(self, result: CallResult) -> str:
        from core.tool_envelope import dumps

        return dumps(result.to_dict())
