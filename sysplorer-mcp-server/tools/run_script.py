"""Execute Sysplorer Python API scripts for ``call_code(mode=\"run_sysplorer_api\")``.

``run_sysplorer_api`` is **only** for invoking Sysplorer APIs (ModelingPy / Sysblock /
toolbox).

- **modelica_lite / mols**: always the **original in-process** path (live driver session).
  No child ``python.exe`` lookup — the lite pack does not ship one.
- **其它平台**: prefer a **subprocess** (``stdin=DEVNULL`` + wall-clock timeout) when a
  usable interpreter exists; otherwise fall back to in-process.
  Override with ``MWORKS_RUN_SCRIPT_IN_SUBPROCESS``: ``0`` / ``inproc`` force in-process;
  ``1`` / ``always`` force subprocess (fails if runner missing).
"""
from __future__ import annotations

import ast
import builtins
import importlib
import io
import json
import logging
import os
import platform
import re
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

from path_config import (
    MWORKS_WORKDIR,
    PROJECT_ROOT,
    SYSPLORER_PYTHON,
    ensure_modelica_lite_site_helpers,
    resolve_sysplorer_python_path,
)
from core.stack_health import _sysplorer_api_port_from_env
from core.subprocess_encoding import merge_subprocess_utf8_env, subprocess_text_kw
from core.sysplorer_subprocess import build_sysplorer_child_environ
from core.utils import _json, looks_like_modelica_file_path
from mworks_driver import is_modelica_lite_platform
from state import _get_driver

_RUN_SCRIPT_ENV_DISABLE = "MWORKS_RUN_SCRIPT_DISABLED"
_RUN_SCRIPT_TIMEOUT_ENV = "MWORKS_RUN_SCRIPT_TIMEOUT"
_RUN_SCRIPT_SUBPROCESS_ENV = "MWORKS_RUN_SCRIPT_IN_SUBPROCESS"
_MAX_SOURCE_CHARS = 600_000
_MAX_CAPTURE_CHARS = 400_000
_DEFAULT_TIMEOUT_SEC = 7200.0
_WORKER_SCRIPT = Path(__file__).resolve().parent.parent / "core" / "run_script_worker.py"
_RESULT_MARKER = "___MWORKS_RUN_SCRIPT_RESULT___"
_log = logging.getLogger(__name__)


def _resolve_readable_script_path(script_path: str) -> tuple[Optional[Path], str]:
    """Resolve ``script_path`` to an existing file.

    Policy is **purpose** (Sysplorer API only), not a directory whitelist.
    ``python_source`` already executes caller-supplied text with no path gate;
    pinning ``script_path`` to MCP/deploy/workspace trees does not enforce that
    and only rejects legitimate ModelingPy files outside those trees.
    Relative paths resolve against the MCP workspace (``PROJECT_ROOT``).
    """
    raw = (script_path or "").strip()
    if not raw:
        return None, ""
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = (PROJECT_ROOT / p).resolve()
    else:
        p = p.resolve()
    if not p.exists():
        return None, f"script_path does not exist: {p}"
    if not p.is_file():
        return None, f"script_path is not a file: {p}"
    return p, ""


def _truncate(s: str, max_chars: int) -> str:
    if len(s) <= max_chars:
        return s
    return s[:max_chars] + f"\n... (truncated, total {len(s)} chars)"


def _inject_script_namespace(namespace: Dict[str, Any]) -> None:
    namespace["__builtins__"] = builtins
    try:
        namespace["mworks"] = importlib.import_module("mworks")
        namespace["sysplorer"] = importlib.import_module("mworks.sysplorer")
    except Exception:
        pass
    for mod in ("ModelingPy", "SysblockPy"):
        try:
            namespace[mod] = importlib.import_module(mod)
        except Exception:
            pass
    # Sysplorer docs call it ModelingPy; in-process that is usually mworks.sysplorer.
    if "ModelingPy" not in namespace:
        sp = namespace.get("sysplorer")
        if sp is not None:
            namespace["ModelingPy"] = sp


def _eof_input(*_args: Any, **_kwargs: Any) -> str:
    """Match subprocess stdin=DEVNULL: interactive input() must not hang MCP."""
    raise EOFError("EOF when reading a line (run_sysplorer_api is non-interactive)")


_FORBIDDEN_MWORKS_CALL_MSG: Dict[str, str] = {
    "ChangeDirectory": (
        "不允许调用 ChangeDirectory；请使用 session_manager(action=\"get_directory\") "
        "（官方 GetDirectory）获取 Sysplorer 当前工作目录后再拼接路径。"
    ),
    "ChangeSimResultDirectory": (
        "不允许调用 ChangeSimResultDirectory（含空字符串显示当前目录）；"
        "请使用 session_manager(action=\"get_sim_result_directory\") "
        "（官方 GetSimResultDirectory）获取仿真结果目录。"
    ),
    "ClearAll": (
        "不允许调用 ClearAll；请逐个使用 EraseClasses 卸载模型/类，并使用 RemoveResults 关闭仿真结果。"
    ),
}


def _forbidden_mworks_messages() -> Dict[str, str]:
    """Always-on bans plus Exit when MCP attaches via SYSPLORER_API_PORT (shared user Sysplorer)."""
    out = dict(_FORBIDDEN_MWORKS_CALL_MSG)
    if _sysplorer_api_port_from_env() is not None:
        out["Exit"] = (
            "不允许在 run_sysplorer_api 中调用 Exit()；当前 MCP 已通过环境变量 SYSPLORER_API_PORT 连接到用户已打开的 "
            "Sysplorer 实例，Exit() 会关闭该界面。请保存工作；需要管理会话时使用 MCP 的 session_manager，勿在脚本中 Exit。"
        )
    return out


class _ForbiddenMworksCallFinder(ast.NodeVisitor):
    """检测对 Sysplorer API 上若干禁止名的显式调用（见 _forbidden_mworks_messages）。"""

    def __init__(self, forbidden_names: frozenset[str]) -> None:
        self._forbidden = forbidden_names
        self.hits: List[tuple[str, int]] = []

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Name) and func.id in self._forbidden:
            self.hits.append((func.id, getattr(node, "lineno", 0) or 0))
        elif isinstance(func, ast.Attribute) and func.attr in self._forbidden:
            self.hits.append((func.attr, getattr(node, "lineno", 0) or 0))
        self.generic_visit(node)


def _scan_forbidden_mworks_calls(src: str) -> Optional[str]:
    """
    若脚本中调用了当前策略禁止的 API，返回禁止说明（可含多行）；否则 None。
    优先用 AST 避免注释/字符串误报；源码无法解析时回退正则（匹配 name( 形式）。
    """
    forbidden_msgs = _forbidden_mworks_messages()
    hits_order: List[str] = []
    seen: set[str] = set()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        for name in sorted(forbidden_msgs):
            if re.search(rf"\b{re.escape(name)}\s*\(", src):
                if name not in seen:
                    seen.add(name)
                    hits_order.append(name)
    else:
        finder = _ForbiddenMworksCallFinder(frozenset(forbidden_msgs))
        finder.visit(tree)
        for name, _ in sorted(finder.hits, key=lambda x: (x[1], x[0])):
            if name not in seen:
                seen.add(name)
                hits_order.append(name)

    if not hits_order:
        return None
    return "\n".join(forbidden_msgs[n] for n in hits_order)


def _ast_call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def _ast_str_const(node: ast.AST) -> Optional[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


class _SysplorerApiMisuseFinder(ast.NodeVisitor):
    """Catch common ModelingPy calling mistakes before they crash a diagnostic script."""

    def __init__(self) -> None:
        self.messages: List[str] = []

    def visit_Call(self, node: ast.Call) -> None:
        name = _ast_call_name(node)
        args = list(node.args)
        if name == "EraseClasses" and args:
            first = args[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                self.messages.append(
                    "EraseClasses 需要全名元组，例如 EraseClasses(('ElevatorLib',))，"
                    "不能传单个 str。更稳妥：model_manager(action='unload', model_name='ElevatorLib')。"
                )
            elif isinstance(first, ast.List):
                self.messages.append(
                    "EraseClasses 参数须是 tuple 而非 list：EraseClasses(('Name',))。"
                    "更稳妥：model_manager(action='unload', model_name='Name')。"
                )
        elif name == "OpenModel" and args:
            pathish = _ast_str_const(args[0])
            if pathish and looks_like_modelica_file_path(pathish):
                self.messages.append(
                    "OpenModel 只接受已加载类的全限定名，不接受 .mo 路径（与斜杠无关）。"
                    "加载文件请用 OpenModelFile(path) 或 model_manager(action='load_file', file_path=...);"
                    "打开已加载模型用 model_manager(action='open', model_name=...)。"
                )
        elif name == "GetLastError":
            self.messages.append(
                "mworks.sysplorer 没有 GetLastError()（那是 Win32 风格）。"
                "请用 model_inspect(action='get_last_errors')（底层 GetLastErrors，复数）；"
                "不要调用 GetLastError。失败时也可看各 MCP 工具 JSON 的 diagnostics。"
            )
        self.generic_visit(node)


def _scan_sysplorer_api_misuse(src: str) -> Optional[str]:
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    finder = _SysplorerApiMisuseFinder()
    finder.visit(tree)
    if not finder.messages:
        return None
    # Preserve order, drop exact duplicates.
    seen: set[str] = set()
    ordered: List[str] = []
    for msg in finder.messages:
        if msg not in seen:
            seen.add(msg)
            ordered.append(msg)
    return "\n".join(ordered)


def _popen_kwargs() -> Dict[str, Any]:
    kw: Dict[str, Any] = {}
    if platform.system() == "Windows":
        cf = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        if cf:
            kw["creationflags"] = cf
    return kw


def _resolve_runner_python() -> Path:
    """Prefer Sysplorer bundled python (has mworks); fall back to host interpreter.

    Frozen MCP hosts are not usable as script runners — return the (possibly missing)
    bundled path so callers can fall back to in-process execution.
    """
    bundled = resolve_sysplorer_python_path(
        Path(os.environ.get("SYSPLORER_PYTHON", str(SYSPLORER_PYTHON))).expanduser()
    )
    if bundled.exists():
        return bundled
    if getattr(sys, "frozen", False):
        return bundled
    return Path(sys.executable)


def _prefer_subprocess_runner() -> tuple[bool, str]:
    """Decide whether ``run_sysplorer_api`` should spawn a child Python.

    - **modelica_lite / mols**: always the original **in-process** path (same as pre-ba581ab).
      Do **not** look for a second ``python.exe`` — the lite pack does not ship one.
    - **其它平台**: 有可用 runner 时走 subprocess；可用 ``MWORKS_RUN_SCRIPT_IN_SUBPROCESS`` 覆盖。
    """
    # modelica_lite: original in-process route only — never gate on python existence.
    if is_modelica_lite_platform():
        return False, "modelica_lite/mols: in-process (original run_script path; no child python)"

    raw = os.environ.get(_RUN_SCRIPT_SUBPROCESS_ENV, "").strip().lower()
    if raw in ("0", "false", "no", "off", "inproc", "in-process"):
        return False, f"forced in-process via {_RUN_SCRIPT_SUBPROCESS_ENV}={raw}"

    runner = _resolve_runner_python()
    if not runner.exists():
        return False, f"runner python missing at {runner}; falling back to in-process"

    if not _WORKER_SCRIPT.is_file():
        return False, f"run_script worker missing: {_WORKER_SCRIPT}; falling back to in-process"

    if raw in ("1", "true", "yes", "on", "subprocess", "always"):
        return True, f"forced subprocess via {_RUN_SCRIPT_SUBPROCESS_ENV}={raw}"

    return True, f"subprocess via {runner}"


def _resolve_connect_port(driver: Any) -> Optional[int]:
    port = _sysplorer_api_port_from_env()
    if port is not None:
        return int(port)
    stored = getattr(driver, "_connect_port", None)
    if stored is not None:
        try:
            return int(stored)
        except (TypeError, ValueError):
            pass
    try:
        from mworks_driver import find_sysplorer_ports

        skip = bool(getattr(driver, "_skip_bin64", False))
        if skip:
            ports = find_sysplorer_ports(workdir=str(getattr(driver, "workdir", MWORKS_WORKDIR)))
        else:
            ports = find_sysplorer_ports(
                bin64_path=str(getattr(driver, "bin64_path", "") or ""),
                site_packages=str(getattr(driver, "site_packages", "") or ""),
                workdir=str(getattr(driver, "workdir", MWORKS_WORKDIR)),
            )
        if ports:
            return int(ports[0])
    except Exception:
        pass
    return None


def _resolve_timeout_sec(timeout_sec: Optional[float]) -> float:
    if timeout_sec is not None:
        try:
            val = float(timeout_sec)
            if val > 0:
                return val
        except (TypeError, ValueError):
            pass
    raw = os.environ.get(_RUN_SCRIPT_TIMEOUT_ENV, "").strip()
    if raw:
        try:
            val = float(raw)
            if val > 0:
                return val
        except ValueError:
            pass
    return _DEFAULT_TIMEOUT_SEC


def _parse_worker_result(result_path: Path, stdout: str) -> Dict[str, Any]:
    if result_path.is_file():
        try:
            return json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    # Recover from marked stdout line if the result file was not written.
    for line in reversed((stdout or "").splitlines()):
        if line.startswith(_RESULT_MARKER):
            try:
                return json.loads(line[len(_RESULT_MARKER) :])
            except json.JSONDecodeError:
                break
    return {}


def _build_child_env(driver: Any, source_path: Path, result_path: Path, connect_port: Optional[int]) -> Dict[str, str]:
    skip = bool(getattr(driver, "_skip_bin64", False))
    if skip:
        env = dict(os.environ)
        env["MWORKS_WORKDIR"] = str(getattr(driver, "workdir", MWORKS_WORKDIR))
    else:
        bin64 = Path(getattr(driver, "bin64_path", "") or os.environ.get("MWORKS_BIN64", ""))
        site = Path(
            getattr(driver, "site_packages", "")
            or os.environ.get("MWORKS_SYSPLORER_SITE_PACKAGES", "")
        )
        workdir = Path(getattr(driver, "workdir", MWORKS_WORKDIR))
        if bin64.exists() and site.exists():
            env = build_sysplorer_child_environ(bin64, site, workdir)
        else:
            env = dict(os.environ)
            env["MWORKS_WORKDIR"] = str(workdir)
            if site.exists():
                env["MWORKS_SYSPLORER_SITE_PACKAGES"] = str(site)

    env = merge_subprocess_utf8_env(env)
    env["MWORKS_RUN_SCRIPT_SOURCE"] = str(source_path)
    env["MWORKS_RUN_SCRIPT_RESULT"] = str(result_path)
    if connect_port is not None:
        env["MWORKS_RUN_SCRIPT_CONNECT_PORT"] = str(int(connect_port))
    else:
        env.pop("MWORKS_RUN_SCRIPT_CONNECT_PORT", None)
    return env


def _prepare_source_and_base(
    python_source: str,
    script_path: str,
) -> tuple[Optional[str], Dict[str, Any]]:
    """Validate inputs / forbidden APIs; return ``(src, data)`` or ``(None, error_data)``."""
    data: Dict[str, Any] = {
        "ok": False,
        "tool": "mworks_run_script",
        "stdout": "",
        "stderr": "",
        "exception": "",
        "traceback": "",
        "run_script_result": None,
        "script_path_resolved": "",
        "hint": "",
        "execution_mode": "",
    }

    if os.environ.get(_RUN_SCRIPT_ENV_DISABLE, "").strip() in ("1", "true", "yes", "on"):
        data["error"] = f"Tool disabled via {_RUN_SCRIPT_ENV_DISABLE}."
        return None, data

    src = (python_source or "").strip()
    resolved: Optional[Path] = None
    if not src:
        resolved, err = _resolve_readable_script_path(script_path)
        if err:
            data["exception"] = err
            data["hint"] = (
                "Provide non-empty python_source, or an existing script_path file. "
                "run_sysplorer_api is for Sysplorer Python API only, not a general Python runner."
            )
            return None, data
        if resolved is None:
            data["exception"] = "python_source is empty and script_path is missing."
            data["error"] = (
                "call_code has only two top-level arguments: mode and payload. "
                "Put python_source (or script_path) inside payload, not next to mode."
            )
            return None, data
        try:
            src = resolved.read_text(encoding="utf-8")
        except OSError as exc:
            data["exception"] = f"read script_path failed: {exc}"
            return None, data
        if len(src) > _MAX_SOURCE_CHARS:
            data["exception"] = f"script_path source exceeds {_MAX_SOURCE_CHARS} characters."
            return None, data
        data["script_path_resolved"] = str(resolved)
    else:
        if len(src) > _MAX_SOURCE_CHARS:
            data["exception"] = f"python_source exceeds {_MAX_SOURCE_CHARS} characters."
            return None, data
        if script_path.strip():
            rp, _ = _resolve_readable_script_path(script_path)
            if rp is not None:
                data["script_path_resolved"] = str(rp)
                data["hint"] = "script_path noted but python_source was used."

    blocked = _scan_forbidden_mworks_calls(src)
    if blocked:
        data["code"] = "sysplorer.forbidden"
        data["exception"] = "脚本包含禁止调用的 Sysplorer API。"
        data["error"] = blocked
        return None, data

    misuse = _scan_sysplorer_api_misuse(src)
    if misuse:
        data["exception"] = "脚本含有常见 ModelingPy 调用错误，已拒绝执行以免中断诊断。"
        data["error"] = misuse
        return None, data

    return src, data


def _run_script_in_process(
    data: Dict[str, Any],
    src: str,
    driver: Any,
    capture_stdout: bool,
    capture_stderr: bool,
    mode_reason: str,
) -> str:
    """Exec script in the MCP process against the live driver session."""
    data["execution_mode"] = "in-process"
    data["hint"] = (data.get("hint") or "")
    if data["hint"]:
        data["hint"] += "\n"
    data["hint"] += (
        f"in-process mode ({mode_reason}). "
        "timeout_sec is not hard-enforced here; input() raises EOFError."
    )

    ensure_modelica_lite_site_helpers()

    namespace: Dict[str, Any] = {"__name__": "__mworks_run_script__"}
    _inject_script_namespace(namespace)
    namespace["driver"] = driver
    # Non-interactive: never block MCP on input().
    bi = dict(vars(builtins))
    bi["input"] = _eof_input
    if not callable(bi.get("help")):
        ensure_modelica_lite_site_helpers()
        bi = dict(vars(builtins))
        bi["input"] = _eof_input
    namespace["__builtins__"] = bi

    buf_out = io.StringIO()
    buf_err = io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        if capture_stdout:
            sys.stdout = buf_out
        if capture_stderr:
            sys.stderr = buf_err
        exec(compile(src, "<mworks_run_script>", "exec"), namespace, namespace)
    except Exception as exc:
        data["exception"] = str(exc)
        data["traceback"] = _truncate(traceback.format_exc(), _MAX_CAPTURE_CHARS)
        data["stdout"] = _truncate(buf_out.getvalue(), _MAX_CAPTURE_CHARS)
        data["stderr"] = _truncate(buf_err.getvalue(), _MAX_CAPTURE_CHARS)
        return _json(data)
    finally:
        sys.stdout = old_out
        sys.stderr = old_err

    data["ok"] = True
    data["stdout"] = _truncate(buf_out.getvalue(), _MAX_CAPTURE_CHARS)
    data["stderr"] = _truncate(buf_err.getvalue(), _MAX_CAPTURE_CHARS)
    if "RUN_SCRIPT_RESULT" in namespace:
        data["run_script_result"] = namespace["RUN_SCRIPT_RESULT"]
    return _json(data)


def _run_script_subprocess(
    data: Dict[str, Any],
    src: str,
    driver: Any,
    capture_stdout: bool,
    capture_stderr: bool,
    timeout_sec: Optional[float],
) -> str:
    data["execution_mode"] = "subprocess"

    runner = _resolve_runner_python()
    if not runner.exists():
        data["exception"] = f"Python interpreter for run_script not found: {runner}"
        data["hint"] = (
            f"Set SYSPLORER_PYTHON to Sysplorer's bundled python.exe, or set "
            f"{_RUN_SCRIPT_SUBPROCESS_ENV}=0 for in-process execution."
        )
        return _json(data)

    if not _WORKER_SCRIPT.is_file():
        data["exception"] = f"run_script worker missing: {_WORKER_SCRIPT}"
        return _json(data)

    connect_port = _resolve_connect_port(driver)
    timeout = _resolve_timeout_sec(timeout_sec)
    data["timeout_sec"] = timeout
    if connect_port is not None:
        data["connect_port"] = connect_port

    scratch = Path(tempfile.mkdtemp(prefix="mworks_run_script_"))
    source_file = scratch / "source.py"
    result_file = scratch / "result.json"
    try:
        source_file.write_text(src, encoding="utf-8")
        env = _build_child_env(driver, source_file, result_file, connect_port)
        env["MWORKS_RUN_SCRIPT_CAPTURE_STDOUT"] = "1" if capture_stdout else "0"
        env["MWORKS_RUN_SCRIPT_CAPTURE_STDERR"] = "1" if capture_stderr else "0"

        try:
            completed = subprocess.run(
                [str(runner), "-u", str(_WORKER_SCRIPT)],
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                cwd=str(getattr(driver, "workdir", MWORKS_WORKDIR)),
                **subprocess_text_kw(),
                **_popen_kwargs(),
            )
        except subprocess.TimeoutExpired as exc:
            data["exception"] = (
                f"run_script timed out after {timeout}s "
                "(non-interactive subprocess; input()/blocking I/O cannot wait for a user)."
            )
            data["stdout"] = _truncate((exc.stdout or "") if isinstance(exc.stdout, str) else "", _MAX_CAPTURE_CHARS)
            data["stderr"] = _truncate((exc.stderr or "") if isinstance(exc.stderr, str) else "", _MAX_CAPTURE_CHARS)
            data["hint"] = (
                "run_script is batch-only. Replace input() with argv/env parameters, "
                f"or raise {_RUN_SCRIPT_TIMEOUT_ENV} / payload timeout_sec for long automation."
            )
            return _json(data)
        except OSError as exc:
            data["exception"] = f"failed to spawn run_script subprocess: {exc}"
            return _json(data)

        child = _parse_worker_result(result_file, completed.stdout or "")
        if child:
            data["ok"] = bool(child.get("ok"))
            data["stdout"] = _truncate(str(child.get("stdout") or ""), _MAX_CAPTURE_CHARS)
            data["stderr"] = _truncate(str(child.get("stderr") or ""), _MAX_CAPTURE_CHARS)
            data["exception"] = str(child.get("exception") or "")
            data["traceback"] = _truncate(str(child.get("traceback") or ""), _MAX_CAPTURE_CHARS)
            if "run_script_result" in child:
                data["run_script_result"] = child.get("run_script_result")
            warn = str(child.get("connect_warning") or "").strip()
            if warn:
                data["hint"] = (data.get("hint") or "")
                if data["hint"]:
                    data["hint"] += "\n"
                data["hint"] += warn
            if not data["ok"] and not data["exception"]:
                data["exception"] = f"run_script worker exited {completed.returncode}"
            return _json(data)

        data["stdout"] = _truncate(completed.stdout or "", _MAX_CAPTURE_CHARS)
        data["stderr"] = _truncate(completed.stderr or "", _MAX_CAPTURE_CHARS)
        data["exception"] = (
            f"run_script worker produced no result JSON (exit={completed.returncode})"
        )
        if completed.returncode:
            data["hint"] = "See stderr for worker diagnostics."
        return _json(data)
    finally:
        try:
            for p in (source_file, result_file):
                try:
                    p.unlink(missing_ok=True)
                except OSError:
                    pass
            scratch.rmdir()
        except OSError:
            pass


def _mworks_run_script_impl(
    python_source: str = "",
    script_path: str = "",
    capture_stdout: bool = True,
    capture_stderr: bool = True,
    timeout_sec: Optional[float] = None,
) -> str:
    """Sysplorer API script execution; used by ``call_code(mode=\"run_sysplorer_api\")``.

    **仅用于调用 Sysplorer API**（ModelingPy / Sysblock / 工具箱），勿作通用 Python 执行入口。
    Prefer subprocess when a runner python exists; fall back to in-process for
    frozen / modelica_lite packs without a bundled interpreter.
    脚本内若需调用主编模 API，须显式 ``import mworks.sysplorer as ModelingPy``（或等价导入），
    **勿**假定裸名 ``ModelingPy`` 可用（与 MCP 侧已封装工具的路径区分，见 ``call_code`` 工具说明）。
    脚本内**禁止** ``ClearAll``、``ChangeDirectory`` 与 ``ChangeSimResultDirectory``；
    若进程环境中设置了正整数 ``SYSPLORER_API_PORT``（连接已有 Sysplorer），还**禁止** ``Exit()``。
    """
    src, data = _prepare_source_and_base(python_source, script_path)
    if src is None:
        return _json(data)

    try:
        driver = _get_driver()
    except Exception as exc:
        data["exception"] = f"driver not available: {exc}"
        data["hint"] = "Call session_manager(action=\"health\" or \"ensure\") first."
        return _json(data)

    use_sub, reason = _prefer_subprocess_runner()
    _log.info("run_sysplorer_api mode decision: subprocess=%s (%s)", use_sub, reason)
    if use_sub:
        return _run_script_subprocess(
            data, src, driver, capture_stdout, capture_stderr, timeout_sec
        )
    return _run_script_in_process(data, src, driver, capture_stdout, capture_stderr, reason)


def mworks_run_script(
    python_source: str = "",
    script_path: str = "",
    capture_stdout: bool = True,
    capture_stderr: bool = True,
    timeout_sec: Optional[float] = None,
) -> str:
    """Python 单元测试辅助；Agent 请用 ``call_code(mode=\"run_sysplorer_api\", payload={...})``。"""
    return _mworks_run_script_impl(
        python_source=python_source,
        script_path=script_path,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        timeout_sec=timeout_sec,
    )
