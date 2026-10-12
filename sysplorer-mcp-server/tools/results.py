"""Simulation result MCP tools."""
from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional

from mcp_instance import mcp, readonly_annotations, writable_annotations
from core.result_variables import discover_result_variables_via_model, truncate_result_variable_list
from core.utils import _json
from state import _get_driver


def _to_plain_sequence(data: Any) -> Any:
    """Turn numpy arrays / array-likes into nested lists for summarization."""
    if data is None or isinstance(data, (str, bytes, dict)):
        return data
    tolist = getattr(data, "tolist", None)
    if callable(tolist):
        try:
            return tolist()
        except Exception:
            return data
    return data


def _summarize_series(data: Any) -> Any:
    """Reduce a large numeric series to count/first/last/min/max/mean.

    Official ``GetVarsValues`` is a list of per-variable series (optionally numpy
    arrays), not a row-wise ``[t, v1, …]`` table. Nested sequences are summarized
    one series at a time so the outer list-of-arrays is not passed through raw.
    """
    data = _to_plain_sequence(data)
    if not isinstance(data, (list, tuple)):
        return data
    if data and isinstance(_to_plain_sequence(data[0]), (list, tuple)):
        return [_summarize_series(item) for item in data]
    if len(data) <= 20:
        return list(data)
    nums = [float(x) for x in data if isinstance(x, (int, float))]
    if not nums:
        return list(data)
    return {
        "count": len(nums),
        "first": nums[0],
        "last": nums[-1],
        "min": min(nums),
        "max": max(nums),
        "mean": round(sum(nums) / len(nums), 6),
    }


def _summarize_vars_values(data: Any, names: List[str]) -> Any:
    """Map ``GetVarsValues`` payload onto ``var_names`` and summarize each series."""
    data = _to_plain_sequence(data)
    if isinstance(data, dict):
        return {str(k): _summarize_series(v) for k, v in data.items()}
    if isinstance(data, (list, tuple)):
        series = [_summarize_series(item) for item in data]
        clean = [str(x).strip() for x in names if str(x).strip()]
        if clean and len(clean) == len(series):
            return {clean[i]: series[i] for i in range(len(clean))}
        return series
    return _summarize_series(data)


MWORKS_RESULT_MANAGER_ACTIONS = frozenset(
    {
        "open_result",
        "remove_result",
        "remove_results",
        "get_result_variables",
        "get_result_variable_info",
        "get_var_values",
        "get_var_value_at",
        "get_vars_values",
        "get_vars_value_at",
        "get_var_times",
    }
)

MWORKS_PLOT_MANAGER_ACTIONS = frozenset({"plot_variables", "create_animation"})


@mcp.tool(annotations=writable_annotations())
def result_manager(
    action: str,
    result_file: str = "",
    var_type: int = 0,
    var_name: str = "",
    var_names: Optional[List[str]] = None,
    time_point: Any = "end",
    model_name: str = "",
    list_all_result_variables: bool = False,
    max_variables_returned: int = 300,
    info_type: str = "Type",
    model_discovery_max_depth: int = 8,
    model_discovery_max_instances: int = 120,
    model_discovery_max_probes: int = 400,
) -> str:
    """Simulation results: open/close, list variables, read series or values at a time.

    | action | required |
    |--------|----------|
    | ``open_result`` | ``result_file`` |
    | ``remove_result`` / ``remove_results`` | none |
    | ``get_result_variables`` | optional ``model_name`` (empty scope falls back to official list) |
    | ``get_result_variable_info`` | ``var_name`` |
    | ``get_var_values`` / ``get_var_value_at`` | ``var_name`` |
    | ``get_vars_values`` / ``get_vars_value_at`` | ``var_names`` |
    | ``get_var_times`` | none |
    """
    act = (action or "").strip().lower()
    if act not in MWORKS_RESULT_MANAGER_ACTIONS:
        return _json(
            {
                "ok": False,
                "tool": "result_manager",
                "error": f"Unsupported action: {action!r}",
                "supported_actions": sorted(MWORKS_RESULT_MANAGER_ACTIONS),
            }
        )

    try:
        if act == "open_result":
            result = _get_driver().open_result(result_file=result_file)
            return _get_driver().as_json(result)
        if act == "remove_result":
            return _get_driver().as_json(_get_driver().remove_result())
        if act == "remove_results":
            return _get_driver().as_json(_get_driver().remove_results())
        if act == "get_result_variable_info":
            result = _get_driver().get_result_variable_info(
                var_name=var_name, info_type=info_type or "Type"
            )
            return _get_driver().as_json(result)
        if act == "get_result_variables":
            drv = _get_driver()
            mn = (model_name or "").strip()
            cap = max(1, int(max_variables_returned))
            if mn and not list_all_result_variables:
                disc = discover_result_variables_via_model(
                    drv,
                    mn,
                    max_depth=max(1, int(model_discovery_max_depth)),
                    max_instances=max(1, int(model_discovery_max_instances)),
                    max_probes=max(1, int(model_discovery_max_probes)),
                )
                scoped = list(disc.get("variables") or [])
                if scoped:
                    out = {
                        "ok": disc.get("ok", False),
                        "api": "GetResultVariableInfo",
                        "strategy": "model_scoped",
                        "model_name": mn,
                        "data": scoped,
                        "variable_count": disc.get("variable_count", len(scoped)),
                        "probes_attempted": disc.get("probes_attempted", 0),
                        "instances_scanned": disc.get("instances_scanned", 0),
                        "candidates_built": disc.get("candidates_built", 0),
                        "sample_details": disc.get("sample_details", []),
                    }
                    if not disc.get("ok"):
                        out["error"] = disc.get("error", "model-scoped discovery failed")
                    return _json(out)
                result = drv.get_result_variables(var_type=var_type)
                base = result.to_dict()
                scoped_meta = {
                    "model_name": mn,
                    "model_scoped_variable_count": 0,
                    "probes_attempted": disc.get("probes_attempted", 0),
                    "instances_scanned": disc.get("instances_scanned", 0),
                    "candidates_built": disc.get("candidates_built", 0),
                }
                official = base.get("data")
                if result.ok and isinstance(official, list) and official:
                    trimmed, total, trunc = truncate_result_variable_list(official, cap)
                    base["data"] = trimmed
                    base["variable_count"] = total
                    base["truncated"] = trunc
                    base["max_variables_returned"] = cap
                    base["strategy"] = "full_list"
                    base["fallback_from"] = "model_scoped"
                    base.update(scoped_meta)
                    base["hint"] = (
                        "model_scoped found no result names; used official GetResultVariables. "
                        "Pass list_all_result_variables=true to skip scoping."
                    )
                    return _json(base)
                out = {
                    "ok": bool(result.ok and disc.get("ok", True)),
                    "api": "GetResultVariables",
                    "strategy": "model_scoped",
                    "data": [],
                    "variable_count": 0,
                    "hint": (
                        "model_scoped and GetResultVariables are both empty. "
                        "Simulate or open_result first; or pass list_all_result_variables=true."
                    ),
                }
                out.update(scoped_meta)
                if not result.ok:
                    out["ok"] = False
                    out["error"] = result.error or "GetResultVariables failed"
                elif not disc.get("ok"):
                    out["ok"] = False
                    out["error"] = disc.get("error", "model-scoped discovery failed")
                return _json(out)
            result = drv.get_result_variables(var_type=var_type)
            base = result.to_dict()
            if result.ok and base.get("data") is not None:
                trimmed, total, trunc = truncate_result_variable_list(base["data"], cap)
                base["data"] = trimmed
                base["variable_count"] = total
                base["truncated"] = trunc
                base["max_variables_returned"] = cap
                base["strategy"] = "full_list"
            return _json(base)
        if act == "get_var_values":
            result = _get_driver().get_var_values(var_name=var_name)
            out = result.to_dict()
            out["data"] = _summarize_series(out.get("data"))
            return _json(out)
        if act == "get_var_value_at":
            result = _get_driver().get_var_value_at(var_name=var_name, time_point=time_point)
            return _get_driver().as_json(result)
        if act == "get_vars_values":
            names = [str(x).strip() for x in (var_names or []) if str(x).strip()]
            result = _get_driver().get_vars_values(var_names=names)
            out = result.to_dict()
            out["data"] = _summarize_vars_values(out.get("data"), names)
            out["layout"] = "one_series_per_requested_name"
            return _json(out)
        if act == "get_vars_value_at":
            names = var_names or []
            result = _get_driver().get_vars_value_at(var_names=names, time_point=time_point)
            return _get_driver().as_json(result)
        if act == "get_var_times":
            result = _get_driver().get_var_times()
            out = result.to_dict()
            out["data"] = _summarize_series(out.get("data"))
            return _json(out)
    except Exception as exc:
        api_map = {
            "open_result": "OpenResult",
            "remove_result": "RemoveResult",
            "remove_results": "RemoveResults",
            "get_result_variables": "GetResultVariables",
            "get_result_variable_info": "GetResultVariableInfo",
            "get_var_values": "GetVarValues",
            "get_var_value_at": "GetVarValueAt",
            "get_vars_values": "GetVarsValues",
            "get_vars_value_at": "GetVarsValueAt",
            "get_var_times": "GetVarTimes",
        }
        return _json({"ok": False, "api": api_map.get(act, act), "error": str(exc)})

    return _json({"ok": False, "tool": "result_manager", "error": f"internal: unhandled action {act!r}"})


@mcp.tool(annotations=readonly_annotations())
def plot_manager(
    action: str,
    variables: Optional[List[str]] = None,
    heading: str = "",
    clear_first: bool = False,
    result_file: str = "",
) -> str:
    """Plot or animate the current simulation result.

    ``plot_variables`` needs ``variables``. ``create_animation`` needs none.
    """
    act = (action or "").strip().lower()
    if act not in MWORKS_PLOT_MANAGER_ACTIONS:
        return _json(
            {
                "ok": False,
                "tool": "plot_manager",
                "error": f"Unsupported action: {action!r}",
                "supported_actions": sorted(MWORKS_PLOT_MANAGER_ACTIONS),
            }
        )

    try:
        if act == "create_animation":
            result = _get_driver().create_animation()
            return _get_driver().as_json(result)

        names = [str(x).strip() for x in (variables or []) if str(x).strip()]
        if not names:
            return _json(
                {
                    "ok": False,
                    "tool": "plot_manager",
                    "api": "CreatePlot",
                    "error": "plot_variables requires a non-empty variables list",
                }
            )
        rf = (result_file or "").strip()
        if rf:
            open_res = _get_driver().open_result(result_file=rf)
            if not open_res.ok:
                return _json(
                    {
                        "ok": False,
                        "api": "CreatePlot",
                        "error": f"OpenResult failed: {open_res.error or open_res.raw}",
                        "open_result": open_res.to_dict(),
                    }
                )
        result = _get_driver().create_plot(
            variables=names,
            heading=heading or "",
            clear_first=clear_first,
            result_file=rf,
        )
        out = result.to_dict()
        if rf:
            out["result_file"] = str(Path(rf).resolve())
        return _json(out)
    except Exception as exc:
        api = "CreateAnimation" if act == "create_animation" else "CreatePlot"
        return _json({"ok": False, "api": api, "error": str(exc)})
