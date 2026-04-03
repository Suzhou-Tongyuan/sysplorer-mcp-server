"""Simulation result MCP tools."""
from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional

from mcp_instance import mcp
from core.result_variables import discover_result_variables_via_model, truncate_result_variable_list
from core.utils import _json
from state import _get_driver


def _summarize_series(data: Any) -> Any:
    """Reduce a large numeric list to a compact KPI summary dict."""
    if not isinstance(data, (list, tuple)) or len(data) <= 20:
        return data
    nums = [float(x) for x in data if isinstance(x, (int, float))]
    if not nums:
        return data
    return {
        "count": len(nums),
        "first": nums[0],
        "last": nums[-1],
        "min": min(nums),
        "max": max(nums),
        "mean": round(sum(nums) / len(nums), 6),
    }


MWORKS_RESULT_MANAGER_ACTIONS = frozenset(
    {
        "open_result",
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


@mcp.tool()
def mworks_sysplorer_result_manager(
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
    """
    仿真结果统一入口（打开结果、列变量、读时序、读时刻值、时间轴）。

    action:
      open_result — 显式 ``OpenResult(path)``；工作流默认不依赖磁盘路径推断结果。
      get_result_variables — 优先策略：若提供 ``model_name`` 且未设 ``list_all_result_variables``，
        用 ``GetComponents``+``GetComponentPorts`` 拼候选名并以 ``GetResultVariableInfo`` 确认（无超大全量列表）。
        否则调用 ``GetResultVariables(var_type)``，超长列表会截断至 ``max_variables_returned``。
      get_result_variable_info — 需要 ``var_name`` 与 ``info_type``（如 Type、Unit、Variability、Description）。
      get_var_values — 需要 var_name。
      get_var_value_at — 需要 var_name；可选 time_point（begin/end 或数值）。
      get_vars_values — 需要 var_names（列表）；长时序会摘要。
      get_vars_value_at — 需要 var_names；可选 time_point。
      get_var_times — 无额外参数。
    """
    act = (action or "").strip().lower()
    if act not in MWORKS_RESULT_MANAGER_ACTIONS:
        return _json(
            {
                "ok": False,
                "tool": "mworks_sysplorer_result_manager",
                "error": f"Unsupported action: {action!r}",
                "supported_actions": sorted(MWORKS_RESULT_MANAGER_ACTIONS),
            }
        )

    try:
        if act == "open_result":
            result = _get_driver().open_result(result_file=result_file)
            return _get_driver().as_json(result)
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
                out = {
                    "ok": disc.get("ok", False),
                    "api": "GetResultVariableInfo",
                    "strategy": "model_scoped",
                    "model_name": mn,
                    "data": disc.get("variables", []),
                    "variable_count": disc.get("variable_count", 0),
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
            names = var_names or []
            result = _get_driver().get_vars_values(var_names=names)
            out = result.to_dict()
            data = out.get("data")
            if isinstance(data, dict):
                out["data"] = {k: _summarize_series(v) for k, v in data.items()}
            elif isinstance(data, (list, tuple)):
                out["data"] = _summarize_series(data)
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
            "get_result_variables": "GetResultVariables",
            "get_result_variable_info": "GetResultVariableInfo",
            "get_var_values": "GetVarValues",
            "get_var_value_at": "GetVarValueAt",
            "get_vars_values": "GetVarsValues",
            "get_vars_value_at": "GetVarsValueAt",
            "get_var_times": "GetVarTimes",
        }
        return _json({"ok": False, "api": api_map.get(act, act), "error": str(exc)})

    return _json({"ok": False, "tool": "mworks_sysplorer_result_manager", "error": f"internal: unhandled action {act!r}"})


@mcp.tool()
def mworks_sysplorer_plot_manager(
    action: str,
    variables: Optional[List[str]] = None,
    heading: str = "",
    clear_first: bool = False,
    result_file: str = "",
) -> str:
    """
    仿真结果可视化统一入口（Sysplorer 内绘图、动画）。

    action:
      plot_variables — 需要 ``variables``（非空列表）；可选 ``heading``、``clear_first``、``result_file``
        （非空时先 ``OpenResult`` 再绘图）。
      create_animation — 创建动画；其余参数可忽略。
    """
    act = (action or "").strip().lower()
    if act not in MWORKS_PLOT_MANAGER_ACTIONS:
        return _json(
            {
                "ok": False,
                "tool": "mworks_sysplorer_plot_manager",
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
                    "tool": "mworks_sysplorer_plot_manager",
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
