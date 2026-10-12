"""
One-shot child process for ``call_code(mode=\"run_sysplorer_api\")``.

Runs under Sysplorer's bundled python (preferred) or the host interpreter.
stdin is intentionally unused (parent passes ``DEVNULL``) so ``input()`` raises
``EOFError`` instead of blocking the MCP request forever.
"""
from __future__ import annotations

import builtins
import importlib
import io
import json
import os
import sys
import traceback
import warnings
from pathlib import Path
from typing import Any, Dict, Optional


_PKG_DIR = Path(__file__).resolve().parent.parent
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

_MAX_CAPTURE_CHARS = 400_000
_RESULT_MARKER = "___MWORKS_RUN_SCRIPT_RESULT___"


def _truncate(s: str, max_chars: int) -> str:
    if len(s) <= max_chars:
        return s
    return s[:max_chars] + f"\n... (truncated, total {len(s)} chars)"


def _prepare_runtime() -> None:
    sp_raw = (os.environ.get("MWORKS_SYSPLORER_SITE_PACKAGES") or "").strip()
    if not sp_raw:
        return
    sp = Path(sp_raw)
    if sp.exists():
        p = str(sp)
        if p not in sys.path:
            sys.path.insert(0, p)
    warnings.filterwarnings("ignore", category=SyntaxWarning)


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
    if "ModelingPy" not in namespace:
        sp = namespace.get("sysplorer")
        if sp is not None:
            namespace["ModelingPy"] = sp


def _maybe_connect_sysplorer() -> Optional[str]:
    """Connect to an existing Sysplorer session when a port is provided.

    Returns a soft warning string on failure (script may still be pure Python).
    """
    raw = (os.environ.get("MWORKS_RUN_SCRIPT_CONNECT_PORT") or "").strip()
    if not raw:
        return None
    try:
        port = int(raw)
    except ValueError:
        return f"invalid MWORKS_RUN_SCRIPT_CONNECT_PORT={raw!r}"
    try:
        from mworks.sysplorer import ConnectSysplorer  # type: ignore

        ConnectSysplorer(port=port)
        return None
    except Exception as exc:
        return f"ConnectSysplorer(port={port}) failed: {exc}"


def _emit_result(path: Path, payload: Dict[str, Any]) -> None:
    text = json.dumps(payload, ensure_ascii=False, default=str)
    path.write_text(text, encoding="utf-8")
    # Also print a marked line so parent can recover if the result file is missing.
    sys.__stdout__.write(_RESULT_MARKER + text + "\n")
    sys.__stdout__.flush()


def main() -> int:
    _prepare_runtime()
    source_path = Path(os.environ.get("MWORKS_RUN_SCRIPT_SOURCE", ""))
    result_path = Path(os.environ.get("MWORKS_RUN_SCRIPT_RESULT", ""))
    capture_stdout = (os.environ.get("MWORKS_RUN_SCRIPT_CAPTURE_STDOUT", "1") or "1").strip() not in (
        "0",
        "false",
        "no",
        "off",
    )
    capture_stderr = (os.environ.get("MWORKS_RUN_SCRIPT_CAPTURE_STDERR", "1") or "1").strip() not in (
        "0",
        "false",
        "no",
        "off",
    )

    data: Dict[str, Any] = {
        "ok": False,
        "stdout": "",
        "stderr": "",
        "exception": "",
        "traceback": "",
        "run_script_result": None,
        "connect_warning": "",
        "execution_mode": "subprocess",
    }

    if not source_path.is_file() or not str(result_path):
        data["exception"] = "worker missing MWORKS_RUN_SCRIPT_SOURCE or MWORKS_RUN_SCRIPT_RESULT"
        if str(result_path):
            _emit_result(result_path, data)
        else:
            print(json.dumps(data, ensure_ascii=False), file=sys.__stderr__)
        return 2

    try:
        src = source_path.read_text(encoding="utf-8")
    except OSError as exc:
        data["exception"] = f"read source failed: {exc}"
        _emit_result(result_path, data)
        return 2

    warn = _maybe_connect_sysplorer()
    if warn:
        data["connect_warning"] = warn

    namespace: Dict[str, Any] = {"__name__": "__mworks_run_script__"}
    _inject_script_namespace(namespace)

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
        _emit_result(result_path, data)
        return 1
    finally:
        sys.stdout = old_out
        sys.stderr = old_err

    data["ok"] = True
    data["stdout"] = _truncate(buf_out.getvalue(), _MAX_CAPTURE_CHARS)
    data["stderr"] = _truncate(buf_err.getvalue(), _MAX_CAPTURE_CHARS)
    if "RUN_SCRIPT_RESULT" in namespace:
        data["run_script_result"] = namespace["RUN_SCRIPT_RESULT"]
    _emit_result(result_path, data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
