"""Execute Python Sysblock / ModelingPy scripts in-process with the live MWorks driver."""
from __future__ import annotations

import builtins
import importlib
import io
import os
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

from path_config import MWORKS_WORKDIR, PROJECT_ROOT, get_resources_root
from core.utils import _json
from state import _get_driver

_RUN_SCRIPT_ENV_DISABLE = "MWORKS_RUN_SCRIPT_DISABLED"
_MAX_SOURCE_CHARS = 600_000
_MAX_CAPTURE_CHARS = 400_000


def _allowed_roots() -> List[Path]:
    roots = [PROJECT_ROOT.resolve(), MWORKS_WORKDIR.resolve(), get_resources_root().resolve()]
    extra = os.environ.get("MWORKS_RUN_SCRIPT_EXTRA_ROOTS", "").strip()
    if extra:
        roots.append(Path(extra).expanduser().resolve())
    return roots


def _is_under_any_root(path: Path, roots: List[Path]) -> bool:
    rp = path.resolve()
    for root in roots:
        try:
            rp.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def _resolve_readable_script_path(script_path: str) -> tuple[Optional[Path], str]:
    raw = (script_path or "").strip()
    if not raw:
        return None, ""
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = (PROJECT_ROOT / p).resolve()
    else:
        p = p.resolve()
    roots = _allowed_roots()
    if not _is_under_any_root(p, roots):
        return None, f"script_path not under allowed roots: {p}"
    if not p.is_file():
        return None, f"script_path is not a file: {p}"
    return p, ""


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
    # Sysplorer 文档中的「ModelingPy」在独立 Python 进程里通常对应已配置的 `mworks.sysplorer`，
    # 而非顶层包名 ModelingPy；导入失败时别名为同一会话模块，避免 ListFunctions 等 NameError。
    if "ModelingPy" not in namespace:
        sp = namespace.get("sysplorer")
        if sp is not None:
            namespace["ModelingPy"] = sp


def _truncate(s: str, max_chars: int) -> str:
    if len(s) <= max_chars:
        return s
    return s[:max_chars] + f"\n... (truncated, total {len(s)} chars)"


def _mworks_run_script_impl(
    python_source: str = "",
    script_path: str = "",
    capture_stdout: bool = True,
    capture_stderr: bool = True,
) -> str:
    """In-process ModelingPy / Sysblock execution; used by ``mworks_sysplorer_call_code(mode=\"run_script\")``."""
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
    }

    if os.environ.get(_RUN_SCRIPT_ENV_DISABLE, "").strip() in ("1", "true", "yes", "on"):
        data["hint"] = f"Tool disabled via {_RUN_SCRIPT_ENV_DISABLE}."
        return _json(data)

    src = (python_source or "").strip()
    resolved: Optional[Path] = None
    if not src:
        resolved, err = _resolve_readable_script_path(script_path)
        if err:
            data["exception"] = err
            data["hint"] = "Provide non-empty python_source or a valid script_path under allowed roots."
            return _json(data)
        if resolved is None:
            data["exception"] = "python_source is empty and script_path is missing."
            return _json(data)
        try:
            src = resolved.read_text(encoding="utf-8")
        except OSError as exc:
            data["exception"] = f"read script_path failed: {exc}"
            return _json(data)
        data["script_path_resolved"] = str(resolved)
    else:
        if len(src) > _MAX_SOURCE_CHARS:
            data["exception"] = f"python_source exceeds {_MAX_SOURCE_CHARS} characters."
            return _json(data)
        if script_path.strip():
            rp, _ = _resolve_readable_script_path(script_path)
            if rp is not None:
                data["script_path_resolved"] = str(rp)
                data["hint"] = "script_path noted but python_source was used."

    try:
        driver = _get_driver()
    except Exception as exc:
        data["exception"] = f"driver not available: {exc}"
        data["hint"] = "Call mworks_sysplorer_session_manager(action=\"health\" or \"ensure\") first."
        return _json(data)

    namespace: Dict[str, Any] = {"__name__": "__mworks_run_script__"}
    _inject_script_namespace(namespace)
    namespace["driver"] = driver

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


def mworks_run_script(
    python_source: str = "",
    script_path: str = "",
    capture_stdout: bool = True,
    capture_stderr: bool = True,
) -> str:
    """Python 单元测试辅助；Agent 请用 ``mworks_sysplorer_call_code(mode=\"run_script\", payload={...})``。"""
    return _mworks_run_script_impl(
        python_source=python_source,
        script_path=script_path,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
    )
