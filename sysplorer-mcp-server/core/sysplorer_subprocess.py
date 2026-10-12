"""
Execute Sysplorer ``mworks.sysplorer`` API only inside Sysplorer's bundled python.exe.

- Long-lived NDJSON worker for :class:`MWorksDriver` session (init + all tool calls).
- One-shot subprocesses for ``FindSysplorer`` and per-port ``ConnectSysplorer`` + ``Exit``.
"""
from __future__ import annotations

import json
import logging
import os
import platform
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from launch_context import sanitize_sysplorer_child_env
from path_config import SYSPLORER_PYTHON, resolve_sysplorer_python_path

_WORKER_SCRIPT = Path(__file__).resolve().parent / "sysplorer_worker_main.py"

_active_worker: Optional["SysplorerSubprocessWorker"] = None
_worker_lock = threading.Lock()

_log = logging.getLogger(__name__)


def _same_python_executable(host: Path, bundled: Path) -> bool:
    try:
        a = host.resolve()
        b = bundled.resolve()
    except OSError:
        return False
    if platform.system() == "Windows":
        return os.path.normcase(str(a)) == os.path.normcase(str(b))
    return a == b


def should_route_sysplorer_api_via_subprocess() -> bool:
    """When True, :class:`MWorksDriver` talks to ``mworks.sysplorer`` only inside ``SYSPLORER_PYTHON``.

    - ``MWORKS_SYSPLORER_API_IN_SUBPROCESS=0`` → in-process (legacy; may break on Python 3.12).
    - ``1`` / ``always`` → always subprocess (if bundled python exists).
    - default / ``auto`` → subprocess when MCP host executable is not the MWorks-bundled python.
    """
    raw = os.environ.get("MWORKS_SYSPLORER_API_IN_SUBPROCESS", "").strip().lower()
    if not raw:
        raw = "auto"
    if raw in ("0", "false", "no", "off", "inproc", "in-process"):
        return False
    bundled = resolve_sysplorer_python_path(
        Path(os.environ.get("SYSPLORER_PYTHON", str(SYSPLORER_PYTHON))).expanduser()
    )
    if raw in ("1", "true", "yes", "on", "subprocess", "always"):
        if not bundled.exists():
            _log.warning(
                "MWORKS_SYSPLORER_API_IN_SUBPROCESS=%s but bundled python missing at %s; falling back to in-process",
                raw,
                bundled,
            )
            return False
        return True
    # auto
    if not bundled.exists():
        _log.warning(
            "Sysplorer bundled python not found at %s; using in-process mworks.sysplorer (often fails on non-3.11 hosts)",
            bundled,
        )
        return False
    host = Path(sys.executable)
    return not _same_python_executable(host, bundled)


def use_subprocess_api() -> bool:
    """Deprecated alias for :func:`should_route_sysplorer_api_via_subprocess`."""
    return should_route_sysplorer_api_via_subprocess()


def _build_full_path_windows() -> str:
    if platform.system() != "Windows":
        return os.environ.get("PATH", "")
    segments: list[str] = []
    try:
        import winreg  # type: ignore[import]

        for hive, subkey in [
            (winreg.HKEY_CURRENT_USER, r"Environment"),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
        ]:
            try:
                with winreg.OpenKey(hive, subkey) as key:
                    val, _ = winreg.QueryValueEx(key, "Path")
                    segments.append(os.path.expandvars(str(val)))
            except OSError:
                pass
    except ImportError:
        pass
    current = os.environ.get("PATH", "")
    if current:
        segments.append(current)
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


def _merged_path_for_sysplorer(bin64_path: Path) -> str:
    install_dir = bin64_path.parent
    extra_dirs = [
        bin64_path,
        install_dir / "Simulator" / "mingw64" / "bin",
        install_dir / "Simulator" / "Bin64",
    ]
    full_path = _build_full_path_windows() if platform.system() == "Windows" else os.environ.get("PATH", "")
    prepend = [str(d) for d in extra_dirs if d.exists() and str(d).lower() not in full_path.lower()]
    return os.pathsep.join(prepend + [full_path]) if prepend else full_path


def build_sysplorer_child_environ(bin64: Path, site_packages: Path, workdir: Path) -> Dict[str, str]:
    """Build env for Sysplorer bundled python / worker.

    Prefer 8.3 short paths for *existing* dirs on Windows so native/VC toolchains that
    still use narrow or ACP code pages do not corrupt Unicode in ``MWORKS_*`` paths.
    """
    from mworks_driver import _windows_short_path_if_exists

    env = sanitize_sysplorer_child_env()
    env["MWORKS_BIN64"] = str(bin64)
    env["MWORKS_SYSPLORER_SITE_PACKAGES"] = str(site_packages)
    wd = workdir
    try:
        wd = wd.resolve()
        wd.mkdir(parents=True, exist_ok=True)
        wd = _windows_short_path_if_exists(wd)
    except OSError:
        pass
    env["MWORKS_WORKDIR"] = str(wd)
    # 与仿真/翻译缓存常落在「文档\MWORKS\…」下；若已存在则改为短路径，减轻 cl 侧路径乱码。
    for key in ("MWORKS_SIM_DIR", "MWORKS_MW_MOL_DIR", "MCP_WORKSPACE_DIR", "MCP_USER_WORKSPACE_DIR"):
        raw = (env.get(key) or "").strip()
        if not raw:
            continue
        try:
            p = Path(raw).expanduser().resolve()
            if p.exists():
                env[key] = str(_windows_short_path_if_exists(p))
        except OSError:
            continue
    env["PATH"] = _merged_path_for_sysplorer(bin64)
    return env


def attach_subprocess_worker(worker: "SysplorerSubprocessWorker") -> None:
    global _active_worker
    with _worker_lock:
        if _active_worker is not None and _active_worker is not worker:
            _active_worker.stop()
        _active_worker = worker


def stop_subprocess_worker() -> None:
    global _active_worker
    with _worker_lock:
        if _active_worker is not None:
            _active_worker.stop()
            _active_worker = None


def release_subprocess_worker(worker: Optional["SysplorerSubprocessWorker"]) -> None:
    """Stop *worker* and clear the global slot if it was the active session."""
    if worker is None:
        return
    global _active_worker
    with _worker_lock:
        if _active_worker is worker:
            _active_worker = None
    worker.stop()


def _payload_for_worker_wire(obj: Any) -> Any:
    """Normalize values for NDJSON: Path → posix; Windows abs paths → forward slashes (avoids fragile escapes)."""
    if isinstance(obj, Path):
        return obj.as_posix()
    if isinstance(obj, dict):
        return {str(k): _payload_for_worker_wire(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_payload_for_worker_wire(x) for x in obj]
    if (
        isinstance(obj, str)
        and platform.system() == "Windows"
        and len(obj) >= 3
        and obj[0].isalpha()
        and obj[1] == ":"
        and "\\" in obj
    ):
        return obj.replace("\\", "/")
    return obj


def _popen_kwargs() -> Dict[str, Any]:
    kw: Dict[str, Any] = {}
    if platform.system() == "Windows":
        cf = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        if cf:
            kw["creationflags"] = cf
    return kw


def _readline_with_timeout(stream: Any, timeout_sec: float) -> str:
    q: "queue.Queue[Optional[str]]" = queue.Queue()

    def _read() -> None:
        try:
            q.put(stream.readline())
        except Exception:
            q.put("")

    th = threading.Thread(target=_read, daemon=True)
    th.start()
    th.join(timeout_sec)
    if th.is_alive():
        raise TimeoutError(f"sysplorer worker read timed out after {timeout_sec}s")
    item = q.get_nowait()
    if item is None:
        return ""
    return item


_ONESHOT_FIND_CODE = r"""
import json, os, sys, traceback, warnings
from pathlib import Path
warnings.filterwarnings("ignore", category=SyntaxWarning)
sp = Path(os.environ["MWORKS_SYSPLORER_SITE_PACKAGES"])
sys.path.insert(0, str(sp))
try:
    from mworks.sysplorer import FindSysplorer
    raw = FindSysplorer()
    out = []
    if raw is not None:
        for p in list(raw):
            out.append(int(p))
    print(json.dumps({"ok": True, "ports": out}, ensure_ascii=False))
except Exception as e:
    print(json.dumps({"ok": False, "error": str(e), "traceback": traceback.format_exc()}, ensure_ascii=False))
"""

_ONESHOT_EXIT_CODE = r"""
import json, os, sys, traceback, warnings
from pathlib import Path
warnings.filterwarnings("ignore", category=SyntaxWarning)
sp = Path(os.environ["MWORKS_SYSPLORER_SITE_PACKAGES"])
sys.path.insert(0, str(sp))
port = int(os.environ["MWORKS_ONESHOT_PORT"])
try:
    from mworks.sysplorer import ConnectSysplorer, Exit
    ConnectSysplorer(port=port)
    Exit()
    print(json.dumps({"ok": True}, ensure_ascii=False))
except Exception as e:
    print(json.dumps({"ok": False, "error": str(e), "traceback": traceback.format_exc()}, ensure_ascii=False))
"""


def subprocess_find_sysplorer_ports(
    bin64: Path,
    site_packages: Path,
    workdir: Path,
    timeout_sec: Optional[float] = None,
) -> List[int]:
    if timeout_sec is None:
        timeout_sec = float(os.environ.get("MWORKS_SUBPROCESS_PROBE_TIMEOUT", "90"))
    py = resolve_sysplorer_python_path(Path(os.environ.get("SYSPLORER_PYTHON", str(SYSPLORER_PYTHON))).expanduser())
    if not py.exists():
        return []
    env = build_sysplorer_child_environ(bin64, site_packages, workdir)
    # Avoid locale GBK decoding failures when FindSysplorer prints non-GBK bytes before our JSON line.
    env = {**env, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    workdir.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(
            [str(py), "-c", _ONESHOT_FIND_CODE],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_sec,
            env=env,
            **_popen_kwargs(),
        )
    except subprocess.TimeoutExpired:
        return []
    except Exception:
        return []
    line = (r.stdout or "").strip().splitlines()[-1] if (r.stdout or "").strip() else ""
    if not line:
        return []
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return []
    if not data.get("ok"):
        return []
    ports = data.get("ports") or []
    try:
        return [int(p) for p in ports]
    except (TypeError, ValueError):
        return []


def subprocess_connect_exit_port(
    bin64: Path,
    site_packages: Path,
    workdir: Path,
    port: int,
    timeout_sec: Optional[float] = None,
) -> Dict[str, Any]:
    if timeout_sec is None:
        timeout_sec = float(os.environ.get("MWORKS_SUBPROCESS_EXIT_TIMEOUT", "120"))
    py = resolve_sysplorer_python_path(Path(os.environ.get("SYSPLORER_PYTHON", str(SYSPLORER_PYTHON))).expanduser())
    if not py.exists():
        return {"ok": False, "error": f"Sysplorer python not found: {py}"}
    env = build_sysplorer_child_environ(bin64, site_packages, workdir)
    env["MWORKS_ONESHOT_PORT"] = str(int(port))
    workdir.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(
            [str(py), "-c", _ONESHOT_EXIT_CODE],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env=env,
            **_popen_kwargs(),
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Exit() subprocess timed out after {timeout_sec}s"}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
    line = (r.stdout or "").strip().splitlines()[-1] if (r.stdout or "").strip() else ""
    if not line:
        return {"ok": False, "error": "empty subprocess stdout", "stderr": (r.stderr or "")[:500]}
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return {"ok": False, "error": f"invalid json: {line[:200]}"}


class SysplorerSubprocessWorker:
    """NDJSON RPC to ``sysplorer_worker_main.py`` running under Sysplorer's python.exe."""

    def __init__(self, bin64: Path, site_packages: Path, workdir: Path) -> None:
        self.bin64 = bin64
        self.site_packages = site_packages
        self.workdir = workdir
        self._python = resolve_sysplorer_python_path(
            Path(os.environ.get("SYSPLORER_PYTHON", str(SYSPLORER_PYTHON))).expanduser()
        )
        self._proc: Optional[subprocess.Popen[str]] = None
        self._call_timeout = float(os.environ.get("MWORKS_SUBPROCESS_CALL_TIMEOUT", "7200"))

    def start(self) -> None:
        if not self._python.exists():
            raise RuntimeError(f"Sysplorer bundled python not found: {self._python}")
        if not _WORKER_SCRIPT.is_file():
            raise RuntimeError(f"Worker script missing: {_WORKER_SCRIPT}")
        self.workdir.mkdir(parents=True, exist_ok=True)
        env = build_sysplorer_child_environ(self.bin64, self.site_packages, self.workdir)
        # Popen 仅启动「worker 解释器 + 脚本」；拉起 Sysplorer 本体须在 worker 内走 StartSysplorer
        self._proc = subprocess.Popen(
            [str(self._python), "-u", str(_WORKER_SCRIPT)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            **_popen_kwargs(),
        )

    def stop(self) -> None:
        proc = self._proc
        self._proc = None
        if proc is None:
            return
        try:
            if proc.stdin:
                proc.stdin.write(json.dumps({"cmd": "shutdown"}, ensure_ascii=True, separators=(",", ":")) + "\n")
                proc.stdin.flush()
        except Exception:
            pass
        try:
            proc.wait(timeout=5)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

    _IO_SNIPPET_CHARS = 1200
    _STDERR_TAIL_CHARS = 4000
    _STDERR_THREAD_READ_TIMEOUT = 0.35

    def _stderr_tail_for_diag(self) -> str:
        """Best-effort stderr tail for exceptions (worker uses stderr=PIPE)."""
        proc = self._proc
        if proc is None or proc.stderr is None:
            return ""
        try:
            if proc.poll() is not None:
                rest = proc.stderr.read()
                return (rest or "")[-self._STDERR_TAIL_CHARS :]
        except Exception as exc:
            return f"<read stderr failed: {exc}>"

        buf: List[str] = []

        def _read_chunk() -> None:
            try:
                chunk = proc.stderr.read(self._STDERR_TAIL_CHARS)
                if chunk:
                    buf.append(chunk)
            except Exception:
                pass

        th = threading.Thread(target=_read_chunk, daemon=True)
        th.start()
        th.join(timeout=self._STDERR_THREAD_READ_TIMEOUT)
        got = (buf[0] if buf else "")[-self._STDERR_TAIL_CHARS :]
        if got:
            return got
        return (
            "(no stderr captured within "
            f"{self._STDERR_THREAD_READ_TIMEOUT}s; worker process still running)"
        )

    def _parse_worker_response_line(self, line: str, context: str) -> Dict[str, Any]:
        """Parse one NDJSON line; on failure include stdout/stderr fragments in the error."""
        preview = (line or "")[: self._IO_SNIPPET_CHARS].replace("\r", "\\r").replace("\n", "\\n")
        try:
            return json.loads(line)
        except json.JSONDecodeError as exc:
            tail = self._stderr_tail_for_diag()
            raise RuntimeError(
                f"sysplorer worker {context}: JSONDecodeError: {exc}; "
                f"stdout_snippet={preview!r}; stderr_tail={tail!r}"
            ) from exc

    def _request_line(self, payload: Dict[str, Any], timeout_sec: Optional[float] = None) -> str:
        proc = self._proc
        if proc is None or proc.stdin is None or proc.stdout is None:
            raise RuntimeError("sysplorer worker not started")
        if timeout_sec is None:
            timeout_sec = self._call_timeout
        payload = _payload_for_worker_wire(payload)
        # UTF-8 管道：用非 ASCII 字面 JSON，避免 \\uXXXX 与宿主侧编码混用时的歧义。
        line_in = json.dumps(payload, ensure_ascii=False, default=str, separators=(",", ":")) + "\n"
        proc.stdin.write(line_in)
        proc.stdin.flush()
        # Sysplorer may print progress text (e.g. "正在连接...") to stdout before NDJSON.
        max_lines = int(os.environ.get("MWORKS_WORKER_STDOUT_MAX_NON_JSON_LINES", "128"))
        follow_timeout = float(os.environ.get("MWORKS_WORKER_JSON_LINE_TIMEOUT", "30"))
        skipped: List[str] = []
        for i in range(max(1, max_lines)):
            tl = timeout_sec if i == 0 else min(timeout_sec, follow_timeout)
            out = _readline_with_timeout(proc.stdout, tl)
            if not out:
                tail = self._stderr_tail_for_diag()
                cmd = payload.get("cmd", "?")
                hint = ""
                if skipped:
                    hint = f"; skipped_non_json_lines={skipped[:8]!r}"
                raise RuntimeError(
                    f"sysplorer worker cmd={cmd!r}: empty stdout line; stderr_tail={tail!r}{hint}"
                )
            raw = out.strip()
            if not raw:
                continue
            try:
                json.loads(raw)
                return raw
            except json.JSONDecodeError:
                skipped.append(raw[:200])
                continue
        tail = self._stderr_tail_for_diag()
        cmd = payload.get("cmd", "?")
        raise RuntimeError(
            f"sysplorer worker cmd={cmd!r}: no JSON line after {max_lines} stdout lines; "
            f"skipped_prefix={skipped[:5]!r}; stderr_tail={tail!r}"
        )

    def ping(self, timeout_sec: float = 30.0) -> Dict[str, Any]:
        line = self._request_line({"cmd": "ping"}, timeout_sec=timeout_sec)
        return self._parse_worker_response_line(line, "ping")

    def init(self, force_start: bool, connect_port: Optional[int], mworks_exe: str) -> Dict[str, Any]:
        init_timeout = float(os.environ.get("MWORKS_SUBPROCESS_INIT_TIMEOUT", "180"))
        line = self._request_line(
            {
                "cmd": "init",
                "force_start": force_start,
                "connect_port": connect_port,
                "mworks_exe": mworks_exe,
            },
            timeout_sec=init_timeout,
        )
        return self._parse_worker_response_line(line, "init")

    def call(self, api: str, args: List[Any], kwargs: Dict[str, Any]) -> Dict[str, Any]:
        line = self._request_line(
            {"cmd": "call", "api": api, "args": args, "kwargs": kwargs},
            timeout_sec=self._call_timeout,
        )
        return self._parse_worker_response_line(line, f"call({api})")
