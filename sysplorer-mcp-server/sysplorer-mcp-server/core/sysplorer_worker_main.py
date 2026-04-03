"""
Runs inside Sysplorer's bundled python.exe only.

Reads NDJSON requests from stdin, writes one JSON response per line to stdout.
Commands: init | call | ping | shutdown

**Launch policy:** when this worker must start Sysplorer, use only ``StartSysplorer``
from ``mworks.sysplorer`` (see ``init`` with ``force_start``). Do not subprocess
``mworks.exe`` from here.
"""
from __future__ import annotations

import json
import os
import sys
import traceback
import warnings
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


def _send(obj: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, default=str) + "\n")
    sys.stdout.flush()


def _prepare_runtime() -> None:
    sp = Path(os.environ["MWORKS_SYSPLORER_SITE_PACKAGES"])
    if sp.exists():
        p = str(sp)
        if p not in sys.path:
            sys.path.insert(0, p)
    warnings.filterwarnings("ignore", category=SyntaxWarning)


def _json_default(obj: Any) -> Any:
    return str(obj)


def _map_time_strings(
    sim_begin: Any,
    sim_end: Any,
    value: Any,
) -> Any:
    if not isinstance(value, str):
        return value
    t = value.strip().lower()
    if t in ("end", "stop", "final"):
        return sim_end if sim_end is not None else value
    if t in ("begin", "start", "initial"):
        return sim_begin if sim_begin is not None else value
    return value


def _normalize_call_args(
    api: str,
    args: List[Any],
    kwargs: Dict[str, Any],
    sim_begin: Any,
    sim_end: Any,
) -> Tuple[List[Any], Dict[str, Any]]:
    out_args = list(args)
    out_kw = dict(kwargs)
    if api in ("GetVarValueAt",) and len(out_args) >= 2:
        out_args[1] = _map_time_strings(sim_begin, sim_end, out_args[1])
    if api in ("GetVarsValueAt",) and len(out_args) >= 2:
        out_args[1] = _map_time_strings(sim_begin, sim_end, out_args[1])
    if "time_point" in out_kw:
        out_kw["time_point"] = _map_time_strings(sim_begin, sim_end, out_kw["time_point"])
    return out_args, out_kw


_MAX_DIAG_CHARS = 500
_MAX_DIAG_ERRORS = 3


def _get_last_diagnostics(api: Dict[str, Callable[..., Any]]) -> str:
    parts: List[str] = []
    try:
        fn_err = api.get("GetLastErrors")
        if callable(fn_err):
            errors = fn_err()
            if errors:
                if isinstance(errors, list):
                    shown = errors[:_MAX_DIAG_ERRORS]
                    text = "; ".join(str(e) for e in shown)
                    if len(errors) > _MAX_DIAG_ERRORS:
                        text += f" ... (+{len(errors) - _MAX_DIAG_ERRORS} more)"
                    parts.append("GetLastErrors: " + text)
                else:
                    parts.append(f"GetLastErrors: {errors}")
    except Exception:
        pass
    try:
        fn_msg = api.get("MessageText")
        if callable(fn_msg):
            msg = fn_msg()
            if msg:
                parts.append(f"MessageText: {msg}")
    except Exception:
        pass
    result = "\n".join(parts)
    if len(result) > _MAX_DIAG_CHARS:
        result = result[:_MAX_DIAG_CHARS] + "... (truncated)"
    return result


def _do_call(api: Dict[str, Callable[..., Any]], name: str, args: List[Any], kwargs: Dict[str, Any]) -> Dict[str, Any]:
    fn = api.get(name)
    if not callable(fn):
        return {"ok": False, "api": name, "error": f"API not found: {name}"}
    try:
        raw = fn(*args, **kwargs)
    except Exception as exc:
        return {"ok": False, "api": name, "error": f"{name} failed: {exc}"}

    # ClassExist(False) 表示「未加载」，不是 API 失败
    if name == "ClassExist":
        return {"ok": True, "api": name, "data": bool(raw), "raw": raw}

    if isinstance(raw, bool) and not raw:
        diag = _get_last_diagnostics(api)
        err_msg = f"{name} returned False"
        if diag:
            err_msg += f"\n{diag}"
        return {"ok": False, "api": name, "data": raw, "raw": raw, "error": err_msg}

    return {"ok": True, "api": name, "data": raw, "raw": raw}


def main() -> int:
    _prepare_runtime()
    api: Dict[str, Callable[..., Any]] = {}
    sim_begin: Any = None
    sim_end: Any = None

    try:
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
        _send({"ok": False, "cmd": "fatal", "error": f"Failed to import mworks.sysplorer: {exc}"})
        return 1

    api.update(
        {
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
            "FindSysplorer": FindSysplorer,
        }
    )

    optional_api_names = [
        "ExportDiagram",
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
        "GetLastErrors",
        "MessageText",
        "SaveModelAs",
        "SimulateModelEx",
        "StartSimulate",
        "GetSimulationState",
        "GetSimulationExitState",
        "ResimulateCurrentResult",
        "Plot",
    ]
    for name in optional_api_names:
        fn = getattr(sysplorer, name, None)
        if callable(fn):
            api[name] = fn

    _erase = getattr(sysplorer, "EraseClasses", None)
    if callable(_erase):
        api["EraseClasses"] = _erase
    _class_exist = getattr(sysplorer, "ClassExist", None)
    if callable(_class_exist):
        api["ClassExist"] = _class_exist

    try:
        from mworks.sysplorer import SimulationTime  # type: ignore

        sim_begin = SimulationTime.Begin
        sim_end = SimulationTime.End
    except Exception:
        pass

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as exc:
            _send({"ok": False, "error": f"invalid json: {exc}"})
            continue

        cmd = req.get("cmd")
        if cmd == "ping":
            _send({"ok": True, "cmd": "ping"})
            continue
        if cmd == "shutdown":
            _send({"ok": True, "cmd": "shutdown"})
            return 0
        if cmd == "init":
            force_start = bool(req.get("force_start", False))
            connect_port = req.get("connect_port")
            mworks_exe = req.get("mworks_exe", "")
            try:
                if force_start:
                    api["StartSysplorer"](processPath=str(mworks_exe))
                else:
                    port = connect_port
                    if port is None:
                        raw = FindSysplorer()
                        if raw:
                            port = int(list(raw)[0])
                    if port is None:
                        raise RuntimeError(
                            "No Sysplorer instance reported by FindSysplorer(); "
                            "init with force_start=true to run StartSysplorer."
                        )
                    api["ConnectSysplorer"](port=port)
                optional_loaded = [n for n in optional_api_names if n in api]
                _send({"ok": True, "cmd": "init", "optional_apis": optional_loaded})
            except Exception as exc:
                _send({"ok": False, "cmd": "init", "error": str(exc)})
            continue

        if cmd == "call":
            name = req.get("api", "")
            args = req.get("args") or []
            kwargs = req.get("kwargs") or {}
            if not isinstance(args, list):
                args = []
            if not isinstance(kwargs, dict):
                kwargs = {}
            nargs, nkw = _normalize_call_args(str(name), args, kwargs, sim_begin, sim_end)
            _send(_do_call(api, str(name), nargs, nkw))
            continue

        _send({"ok": False, "error": f"unknown cmd: {cmd}"})

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
