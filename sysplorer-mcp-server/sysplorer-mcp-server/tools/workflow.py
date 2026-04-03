"""Workflow: MCP 仅注册 ``mworks_sysplorer_call_code``；其余为 Python 内部/测试辅助。"""
from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

from mcp_instance import mcp
from path_config import TEMP_CODE_FOLDER
from core.utils import _json, _disk_free_mb, _sync_load_caches
from core.job_manager import job_manager
from state import _get_driver


def _submit_job_core(action: str, payload: Dict[str, Any]) -> str:
    action_norm = action.strip().lower()
    if action_norm not in {"check", "translate", "simulate"}:
        return _json({"ok": False, "error": f"Unsupported action: {action}"})
    job = job_manager.submit(action=action_norm, payload=payload or {})
    return _json(
        {
            "ok": True,
            "job_id": job.job_id,
            "action": action_norm,
            "status": job.status,
            "created_at": job.created_at,
        }
    )


def _get_job_result_core(job_id: str) -> str:
    job = job_manager.get(job_id)
    if not job:
        return _json({"ok": False, "error": f"job not found: {job_id}"})
    return _json(
        {
            "ok": job.status == "done",
            "job_id": job.job_id,
            "action": job.action,
            "status": job.status,
            "elapsed": job.elapsed(),
            "result": job.result,
            "error": job.error,
        }
    )


def mworks_submit_job(action: str, payload: Dict[str, Any]) -> str:
    """Python 辅助：等价于 ``mworks_sysplorer_call_code(mode=\"submit_job\", ...)``；**非 MCP 工具**。"""
    return _submit_job_core(action, payload)


def mworks_get_job_result(job_id: str) -> str:
    """Python 辅助：等价于 ``mworks_sysplorer_call_code(mode=\"get_job_result\", ...)``；**非 MCP 工具**。"""
    return _get_job_result_core(job_id)


def _run_with_ready_impl(action: str, payload: Dict[str, Any]) -> str:
    """
    先确保 Sysplorer 就绪，再按 ``action`` 分派。**仅供** ``mworks_sysplorer_call_code(mode=\"run_with_ready\")`` 与单元测试调用。
    """
    try:
        _get_driver()  # triggers StackHealthManager recovery if needed
    except Exception as exc:
        return _json(
            {
                "ok": False,
                "tool": "mworks_run_with_ready",
                "action": action,
                "error": f"Sysplorer is not ready: {exc}",
            }
        )

    action_norm = (action or "").strip().lower()
    req = payload or {}

    try:
        from tools.model_ops import (
            mworks_load_file,
            mworks_sysplorer_load_library,
            mworks_open_model,
            mworks_unload_file,
            mworks_sysplorer_model_manager,
            mworks_save_model,
            mworks_set_model_param,
            mworks_sysplorer_check_model,
            mworks_sysplorer_translate_model,
            mworks_sysplorer_simulate_model,
        )
        from tools.results import (
            MWORKS_PLOT_MANAGER_ACTIONS,
            MWORKS_RESULT_MANAGER_ACTIONS,
            mworks_sysplorer_plot_manager,
            mworks_sysplorer_result_manager,
        )
        from tools.layout import mworks_sysplorer_smart_layout

        if action_norm == "load_file":
            raw = mworks_load_file(req.get("file_path", ""))
        elif action_norm == "load_library":
            raw = mworks_sysplorer_load_library(
                req.get("library_name", ""),
                library_version=req.get("library_version", ""),
            )
        elif action_norm == "open_model":
            raw = mworks_open_model(req.get("model_name", ""))
        elif action_norm == "unload_file":
            raw = mworks_unload_file(req.get("model_name", ""))
        elif action_norm == "lookup_component":
            raw = mworks_sysplorer_model_manager(
                action="lookup_component",
                model_name=str(req.get("model_name", "") or ""),
                comp_name=str(req.get("comp_name", "") or ""),
                info_type=str(req.get("info_type", "") or ""),
            )
        elif action_norm == "get_components":
            raw = mworks_sysplorer_model_manager(
                action="get_components",
                model_name=str(req.get("model_name", "") or ""),
                component=str(req.get("component", "") or ""),
            )
        elif action_norm == "get_component_ports":
            raw = mworks_sysplorer_model_manager(
                action="get_component_ports",
                model_name=str(req.get("model_name", "") or ""),
                component_name=str(req.get("component_name", "") or ""),
                port_direction=int(req.get("port_direction", 0)),
            )
        elif action_norm == "get_model_text":
            raw = mworks_sysplorer_model_manager(
                action="get_model_text",
                model_name=str(req.get("model_name", "") or ""),
            )
        elif action_norm == "get_model_description":
            raw = mworks_sysplorer_model_manager(
                action="get_model_description",
                model_name=str(req.get("model_name", "") or ""),
            )
        elif action_norm == "get_component_description":
            raw = mworks_sysplorer_model_manager(
                action="get_component_description",
                model_name=str(req.get("model_name", "") or ""),
                comp_name=str(req.get("comp_name", "") or ""),
            )
        elif action_norm == "get_classes":
            raw = mworks_sysplorer_model_manager(
                action="get_classes",
                model_name=str(req.get("model_name", "") or ""),
            )
        elif action_norm == "save_model":
            raw = mworks_save_model(
                req.get("model_name", ""),
                folder=req.get("folder", ""),
                save_type=int(req.get("save_type", 0)),
            )
        elif action_norm in ("set_model_param", "sysplorer_set_model_param", "mworks_set_model_param"):
            v_raw = req.get("value", "")
            v_str = v_raw if isinstance(v_raw, str) else ("" if v_raw is None else str(v_raw))
            raw = mworks_set_model_param(
                model_name=str(req.get("model_name", "") or ""),
                param_name=str(req.get("param_name", "") or ""),
                value=v_str,
                component=str(req.get("component", "") or ""),
            )
        elif action_norm in ("export_model_diagram", "export_diagram"):
            raw = mworks_sysplorer_model_manager(
                action="export_model_diagram",
                model_name=str(req.get("model_name", "") or ""),
                output_path=str(req.get("output_path", "") or ""),
                width=int(req.get("width", 800)),
                height=int(req.get("height", 600)),
                open_model_first=bool(req.get("open_model_first", True)),
            )
        elif action_norm in ("check_model", "batch_check_models", "sysplorer_check_model"):
            raw = mworks_sysplorer_check_model(
                model_names=req.get("model_names"),
                model_name=str(req.get("model_name", "") or ""),
                model_type=req.get("model_type", "MODELICA"),
                stop_on_error=bool(req.get("stop_on_error", False)),
                reload_mo_path=str(req.get("reload_mo_path", "") or ""),
                smart_layout_graph_json=str(req.get("smart_layout_graph_json", "") or ""),
                smart_layout_graph_json_path=str(req.get("smart_layout_graph_json_path", "") or ""),
                smart_layout_model_path=str(req.get("smart_layout_model_path", "") or ""),
                smart_layout_output_json_path=str(req.get("smart_layout_output_json_path", "") or ""),
                smart_layout_timeout_seconds=int(req.get("smart_layout_timeout_seconds", 120)),
            )
        elif action_norm in ("translate_model", "sysplorer_translate_model"):
            raw = mworks_sysplorer_translate_model(
                model_name=req.get("model_name", ""),
                code_folder=req.get("code_folder", TEMP_CODE_FOLDER),
                model_type=req.get("model_type", "MODELICA"),
                code_type=req.get("code_type", "NORMAL"),
                build_type=req.get("build_type", "BINARY"),
                run_to=req.get("run_to", "MAKING"),
                config_json=req.get("config_json", ""),
                reload_mo_path=str(req.get("reload_mo_path", "") or ""),
                smart_layout_graph_json=str(req.get("smart_layout_graph_json", "") or ""),
                smart_layout_graph_json_path=str(req.get("smart_layout_graph_json_path", "") or ""),
                smart_layout_model_path=str(req.get("smart_layout_model_path", "") or ""),
                smart_layout_output_json_path=str(req.get("smart_layout_output_json_path", "") or ""),
                smart_layout_timeout_seconds=int(req.get("smart_layout_timeout_seconds", 120)),
            )
        elif action_norm in ("simulate_model", "sysplorer_simulate_model"):
            raw = mworks_sysplorer_simulate_model(
                model_name=req.get("model_name", ""),
                sim_mode=int(req.get("sim_mode", 0)),  # default 0 = current mode (auto translate)
                target_time=req.get("target_time", []),
                ext_res_path=req.get("ext_res_path", ""),
                verify_result_var=str(req.get("verify_result_var", "") or ""),
                verify_time_point=req.get("verify_time_point", "end"),
                result_var_type=int(req.get("result_var_type", 0)),
                reload_mo_path=str(req.get("reload_mo_path", "") or ""),
                smart_layout_graph_json=str(req.get("smart_layout_graph_json", "") or ""),
                smart_layout_graph_json_path=str(req.get("smart_layout_graph_json_path", "") or ""),
                smart_layout_model_path=str(req.get("smart_layout_model_path", "") or ""),
                smart_layout_output_json_path=str(req.get("smart_layout_output_json_path", "") or ""),
                smart_layout_timeout_seconds=int(req.get("smart_layout_timeout_seconds", 120)),
            )
        elif action_norm in MWORKS_RESULT_MANAGER_ACTIONS:
            vraw = req.get("var_names") or []
            vnames = list(vraw) if isinstance(vraw, (list, tuple)) else []
            raw = mworks_sysplorer_result_manager(
                action=action_norm,
                result_file=str(req.get("result_file", "") or ""),
                var_type=int(req.get("var_type", 0)),
                var_name=str(req.get("var_name", "") or ""),
                var_names=vnames,
                time_point=req.get("time_point", "end"),
                model_name=str(req.get("model_name", "") or ""),
                list_all_result_variables=bool(req.get("list_all_result_variables", False)),
                max_variables_returned=int(req.get("max_variables_returned", 300)),
                info_type=str(req.get("info_type", "Type") or "Type"),
                model_discovery_max_depth=int(req.get("model_discovery_max_depth", 8)),
                model_discovery_max_instances=int(req.get("model_discovery_max_instances", 120)),
                model_discovery_max_probes=int(req.get("model_discovery_max_probes", 400)),
            )
        elif action_norm in MWORKS_PLOT_MANAGER_ACTIONS:
            vraw = req.get("variables") or []
            vlist = list(vraw) if isinstance(vraw, (list, tuple)) else []
            raw = mworks_sysplorer_plot_manager(
                action=action_norm,
                variables=vlist,
                heading=str(req.get("heading", "") or ""),
                clear_first=bool(req.get("clear_first", False)),
                result_file=str(req.get("result_file", "") or ""),
            )
        elif action_norm in (
            "auto_layout_smart",
            "finalize_generated_model_with_auto_layout",
            "generate_system_model_with_auto_layout",
            "sysplorer_smart_layout",
            "mworks_sysplorer_smart_layout",
        ):
            mode_map = {
                "auto_layout_smart": "layout_only",
                "finalize_generated_model_with_auto_layout": "finalize_generation",
                "generate_system_model_with_auto_layout": "writeback_mo",
            }
            mode = (req.get("mode") or "").strip()
            if not mode:
                mode = mode_map.get(action_norm, "layout_only")
            raw = mworks_sysplorer_smart_layout(
                mode=mode,
                input_graph_json=req.get("input_graph_json", ""),
                input_json_path=req.get("input_json_path", ""),
                output_json_path=req.get("output_json_path", ""),
                generation_result_json=req.get("generation_result_json", ""),
                graph_key=req.get("graph_key", ""),
                model_name=req.get("model_name", ""),
                modelica_code=req.get("modelica_code", ""),
                model_output_path=req.get("model_output_path", ""),
                graph_json_path=req.get("graph_json_path", ""),
                graph_json=req.get("graph_json", ""),
                auto_layout=bool(req.get("auto_layout", True)),
                layout_output_json_path=req.get("layout_output_json_path", ""),
                timeout_seconds=int(req.get("timeout_seconds", 120)),
            )
        elif action_norm == "fast_workflow":
            raw = _fast_workflow_impl(
                file_paths=req.get("file_paths", []),
                check_models=req.get("check_models", []),
                simulate_models=req.get("simulate_models", []),
                result_vars=req.get("result_vars", []),
                time_point=req.get("time_point", "end"),
                auto_load_deps=bool(req.get("auto_load_deps", True)),
                skip_unchanged_loads=bool(req.get("skip_unchanged_loads", True)),
                sim_mode=int(req.get("sim_mode", 0)),
                stop_on_error=bool(req.get("stop_on_error", True)),
                use_batch_check=bool(req.get("use_batch_check", True)),
                min_free_mb_for_sim=float(req.get("min_free_mb_for_sim", 512)),
                sim_output_dir=req.get("sim_output_dir", ""),
                force_reload=bool(req.get("force_reload", False)),
                run_smart_layout_before_check=bool(req.get("run_smart_layout_before_check", True)),
                run_smart_layout_after=bool(req.get("run_smart_layout_after", False)),
                smart_layout_graph_json=str(req.get("smart_layout_graph_json", "") or ""),
                smart_layout_graph_json_path=str(req.get("smart_layout_graph_json_path", "") or ""),
                smart_layout_model_path=str(req.get("smart_layout_model_path", "") or ""),
                smart_layout_output_json_path=str(req.get("smart_layout_output_json_path", "") or ""),
                smart_layout_timeout_seconds=int(req.get("smart_layout_timeout_seconds", 120)),
                reload_after_smart_layout=bool(req.get("reload_after_smart_layout", True)),
            )
        elif action_norm == "submit_job":
            raw = _submit_job_core(req.get("action", ""), req.get("payload", {}))
        elif action_norm == "get_job_result":
            raw = _get_job_result_core(req.get("job_id", ""))
        elif action_norm == "sysplorer_session_manager":
            from tools.sysplorer import mworks_sysplorer_session_manager

            ep = req.get("exit_port")
            exit_pt = None
            if ep is not None and str(ep).strip() != "":
                try:
                    exit_pt = int(ep)
                except (TypeError, ValueError):
                    exit_pt = None
            raw = mworks_sysplorer_session_manager(
                action=str(req.get("manager_action") or req.get("session_action") or "health"),
                wait_seconds=int(req.get("wait_seconds", 45)),
                restart_mode=str(req.get("restart_mode", "reconnect")),
                exit_port=exit_pt,
            )
        else:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_run_with_ready",
                    "action": action_norm,
                    "error": f"Unsupported action: {action_norm}",
                }
            )

        # Return inner tool result directly (no wrapper nesting)
        return raw
    except Exception as exc:
        return _json({"ok": False, "tool": "mworks_run_with_ready", "action": action_norm, "error": str(exc)})


def mworks_run_with_ready(action: str, payload: Dict[str, Any]) -> str:
    """Python 辅助；Agent 请用 ``mworks_sysplorer_call_code(mode=\"run_with_ready\", ...)``。"""
    return _run_with_ready_impl(action, payload)


def _fast_workflow_impl(
    file_paths: Optional[List[str]] = None,
    check_models: Optional[List[str]] = None,
    simulate_models: Optional[List[str]] = None,
    result_vars: Optional[List[str]] = None,
    time_point: Any = "end",
    auto_load_deps: bool = True,
    skip_unchanged_loads: bool = True,
    sim_mode: int = 0,
    stop_on_error: bool = True,
    use_batch_check: bool = True,
    min_free_mb_for_sim: float = 512,
    sim_output_dir: str = "",
    force_reload: bool = False,
    run_smart_layout_before_check: bool = True,
    run_smart_layout_after: bool = False,
    smart_layout_graph_json: str = "",
    smart_layout_graph_json_path: str = "",
    smart_layout_model_path: str = "",
    smart_layout_output_json_path: str = "",
    smart_layout_timeout_seconds: int = 120,
    reload_after_smart_layout: bool = True,
) -> str:
    """
    Fast-path workflow runner in one tool call:
    load files ->（可选）Smart Layout 写回并重载 -> check -> simulate -> KPI ->（可选）再次 Smart Layout。

    sim_mode: 0=current mode (auto translate if needed), 1=standalone, 2=real-time.
    当 ``run_smart_layout_before_check=True``（默认）且能解析到目标 ``.mo``（``smart_layout_model_path`` 或 ``file_paths`` 中唯一 ``.mo``）时，
    在**检查与仿真之前**先跑 Smart Layout（无 graph 时按模型文本自动生成），写回 Placement/Line 后通过 ``mworks_load_file(..., force_reload=True)``
    与 ``mworks_sysplorer_model_manager`` 的 ``load_file`` 同路径重载，保证 Sysplorer Diagram 与磁盘一致。
    另可提供 ``smart_layout_graph_json`` / ``smart_layout_graph_json_path`` 覆盖自动生成。
    ``run_smart_layout_after`` 默认 False；``reload_after_smart_layout`` 在「后置布局」成功时对该 ``.mo`` 再强制重载。
    ``sim_output_dir`` 为空时不向 ``SimulateModel`` 传输出目录（由 Sysplorer 会话默认处理），也不再做基于该路径的磁盘预检；
    仅当显式传入非空目录时，才把其作为 ``ext_res_path`` 并检查剩余空间。
    """
    from tools.model_ops import (
        mworks_load_file,
        mworks_sysplorer_check_model,
        mworks_sysplorer_simulate_model,
        _preflight_smart_layout_reload,
    )
    from tools.results import mworks_sysplorer_result_manager
    from tools.layout import run_smart_layout_for_fast_workflow

    started = time.perf_counter()
    # _get_driver() now includes full health recovery via StackHealthManager
    try:
        drv = _get_driver()
        _sync_load_caches(drv)
    except Exception as exc:
        return _json(
            {
                "ok": False,
                "tool": "mworks_fast_workflow",
                "error": f"Sysplorer is not ready: {exc}",
            }
        )

    files = [str(x).strip() for x in (file_paths or []) if str(x).strip()]
    checks = [str(x).strip() for x in (check_models or []) if str(x).strip()]
    sims = [str(x).strip() for x in (simulate_models or []) if str(x).strip()]
    kpis = [str(x).strip() for x in (result_vars or []) if str(x).strip()]

    steps: List[Dict[str, Any]] = []
    summary: Dict[str, List] = {
        "load": [],
        "preflight_layout": [],
        "check": [],
        "simulate": [],
        "kpi": [],
        "smart_layout": [],
        "reload_after_layout": [],
    }
    sim_dir_effective = sim_output_dir.strip()

    def _sum_dt(rows: Any) -> float:
        if not isinstance(rows, list):
            return 0.0
        return round(sum(float(x.get("dt_s", 0.0)) for x in rows if isinstance(x, dict)), 3)

    def _run_step(step: str, target: str, fn) -> Dict[str, Any]:
        t0 = time.perf_counter()
        try:
            raw = fn()
            result = json.loads(raw) if isinstance(raw, str) else {"ok": False, "error": "non-json response"}
        except Exception as exc:
            result = {"ok": False, "error": str(exc)}
        elapsed = round(time.perf_counter() - t0, 3)
        ok = bool(result.get("ok", False))
        # Compact row: only essential fields, plus error/data on failure or for KPI
        row: Dict[str, Any] = {"step": step, "target": target, "ok": ok, "dt_s": elapsed}
        if not ok and result.get("error"):
            row["error"] = result["error"]
        if step == "kpi" and ok:
            row["value"] = result.get("data")
        if not ok and result.get("warning"):
            row["warning"] = result["warning"]
        steps.append(row)
        summary[step].append(row)
        return row

    for p in files:
        row = _run_step(
            "load",
            p,
            lambda p=p: mworks_load_file(
                file_path=p,
                auto_load_deps=auto_load_deps,
                skip_if_unchanged=skip_unchanged_loads,
                force_reload=force_reload,
            ),
        )
        if stop_on_error and not row["ok"]:
            break

    # Smart Layout + 重载须在检查 / 仿真之前执行（与磁盘一致、布线写回后再实例化）
    need_ops = bool(checks or sims)
    if (
        need_ops
        and run_smart_layout_before_check
        and not (stop_on_error and steps and not steps[-1]["ok"])
    ):
        gj = (smart_layout_graph_json or "").strip()
        gjp = (smart_layout_graph_json_path or "").strip()
        mo_explicit = (smart_layout_model_path or "").strip()
        mo_path = mo_explicit
        if not mo_path and len(files) == 1 and files[0].lower().endswith(".mo"):
            mo_path = files[0]
        # 条件：要么有graph，要么有mo路径（自动生成graph）
        if not gj and not gjp and not mo_path:
            pass
        elif not mo_path:
            row_pf: Dict[str, Any] = {
                "step": "preflight_layout",
                "target": "",
                "ok": False,
                "dt_s": 0.0,
                "error": "smart_layout_model_path 或 file_paths 中唯一 .mo 为必填（已提供 graph）",
            }
            steps.append(row_pf)
            summary["preflight_layout"].append(row_pf)
        else:
            t0 = time.perf_counter()
            hint = checks[0] if checks else (sims[0] if sims else "")
            pf_ok, pf_steps, pf_err = _preflight_smart_layout_reload(
                smart_layout_graph_json=gj,
                smart_layout_graph_json_path=gjp,
                smart_layout_model_path=mo_explicit,
                reload_mo_path=mo_path,
                layout_output_json_path=smart_layout_output_json_path,
                timeout_seconds=int(smart_layout_timeout_seconds),
                model_name_hint=hint,
            )
            elapsed_pf = round(time.perf_counter() - t0, 3)
            row_pf = {
                "step": "preflight_layout",
                "target": mo_path,
                "ok": pf_ok,
                "dt_s": elapsed_pf,
                "preflight_steps": pf_steps,
            }
            if not pf_ok:
                row_pf["error"] = pf_err
            steps.append(row_pf)
            summary["preflight_layout"].append(row_pf)

    if not (stop_on_error and steps and not steps[-1]["ok"]):
        if use_batch_check and checks:
            row = _run_step(
                "check",
                f"batch({len(checks)})",
                lambda: mworks_sysplorer_check_model(model_names=checks, stop_on_error=stop_on_error),
            )
        else:
            for m in checks:
                row = _run_step("check", m, lambda m=m: mworks_sysplorer_check_model(model_names=[m]))
                if stop_on_error and not row["ok"]:
                    break

    if not (stop_on_error and steps and not steps[-1]["ok"]):
        if sims and sim_dir_effective:
            disk = _disk_free_mb(sim_dir_effective)
            disk_ok = bool(disk.get("ok", False) and float(disk.get("free_mb", 0.0)) >= float(min_free_mb_for_sim))
            if not disk_ok and stop_on_error:
                return _json({"ok": False, "tool": "mworks_fast_workflow",
                              "error": f"insufficient disk space ({disk.get('free_mb',0):.0f} MB < {min_free_mb_for_sim} MB)"})
        # 部分 Sysplorer 版本对默认探测变量 ``time`` 的 GetResultVariableInfo 不可靠；若已指定 KPI，用首个变量做结果存在性探测。
        verify_v = (kpis[0] if kpis else "").strip()
        for m in sims:
            row = _run_step(
                "simulate",
                m,
                lambda m=m, vv=verify_v: mworks_sysplorer_simulate_model(
                    model_name=m,
                    sim_mode=sim_mode,
                    ext_res_path=sim_dir_effective,
                    verify_result_var=vv,
                ),
            )
            if stop_on_error and not row["ok"]:
                break

    if not (stop_on_error and steps and not steps[-1]["ok"]):
        if kpis:
            # Prefer a single batch read to reduce round-trips.
            t0 = time.perf_counter()
            try:
                batch_raw = mworks_sysplorer_result_manager(
                    action="get_vars_value_at",
                    var_names=kpis,
                    time_point=time_point,
                )
                batch_res = json.loads(batch_raw) if isinstance(batch_raw, str) else {"ok": False}
            except Exception as exc:
                batch_res = {"ok": False, "error": str(exc)}
            elapsed = round(time.perf_counter() - t0, 3)

            if batch_res.get("ok") and isinstance(batch_res.get("data"), list):
                values = batch_res["data"]
                per_dt = round(elapsed / len(kpis), 3) if kpis else elapsed
                for i, v in enumerate(kpis):
                    val = values[i] if i < len(values) else None
                    row: Dict[str, Any] = {"step": "kpi", "target": v, "ok": True, "dt_s": per_dt, "value": val}
                    steps.append(row)
                    summary["kpi"].append(row)
            else:
                # Batch failed — fall back to individual reads.
                for v in kpis:
                    _run_step(
                        "kpi",
                        v,
                        lambda v=v: mworks_sysplorer_result_manager(
                            action="get_var_value_at",
                            var_name=v,
                            time_point=time_point,
                        ),
                    )

    if (
        run_smart_layout_after
        and not (stop_on_error and steps and not steps[-1]["ok"])
    ):
        gj = (smart_layout_graph_json or "").strip()
        gjp = (smart_layout_graph_json_path or "").strip()
        mo_explicit = (smart_layout_model_path or "").strip()
        mo_path = mo_explicit
        if not mo_path and len(files) == 1 and files[0].lower().endswith(".mo"):
            mo_path = files[0]
        if not gj and not gjp and not mo_path:
            steps.append(
                {
                    "step": "smart_layout",
                    "target": "",
                    "ok": True,
                    "dt_s": 0.0,
                    "skipped": True,
                    "reason": "no smart_layout_graph_json/smart_layout_graph_json_path or .mo file path",
                }
            )
        elif not mo_path:
            row_sl: Dict[str, Any] = {
                "step": "smart_layout",
                "target": "",
                "ok": False,
                "dt_s": 0.0,
                "error": "smart_layout_model_path or a single .mo in file_paths is required when graph is set",
            }
            steps.append(row_sl)
        else:
            t0 = time.perf_counter()
            sok, sdata = run_smart_layout_for_fast_workflow(
                graph_json=gj,
                graph_json_path=gjp,
                model_output_path=mo_path,
                layout_output_json_path=smart_layout_output_json_path,
                timeout_seconds=int(smart_layout_timeout_seconds),
                auto_generate_graph=True,
            )
            elapsed_sl = round(time.perf_counter() - t0, 3)
            row_sl = {
                "step": "smart_layout",
                "target": mo_path,
                "ok": sok,
                "dt_s": elapsed_sl,
            }
            if not sok:
                row_sl["error"] = sdata.get("error", "")
            else:
                row_sl["components_updated"] = sdata.get("components_updated", 0)
                row_sl["connects_updated"] = sdata.get("connects_updated", 0)
            steps.append(row_sl)
            if reload_after_smart_layout and sok:
                _run_step(
                    "reload_after_layout",
                    mo_path,
                    lambda mp=mo_path: mworks_load_file(
                        file_path=mp,
                        auto_load_deps=False,
                        skip_if_unchanged=False,
                        force_reload=True,
                    ),
                )

    elapsed_total = round(time.perf_counter() - started, 3)
    ok = all(bool(x.get("ok", False)) for x in steps) if steps else True
    return _json(
        {
            "ok": ok,
            "tool": "mworks_fast_workflow",
            "total_s": elapsed_total,
            "steps": steps,
        }
    )


def _fast_workflow_kwargs_from_payload(payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    p = payload or {}
    keys = (
        "file_paths",
        "check_models",
        "simulate_models",
        "result_vars",
        "time_point",
        "auto_load_deps",
        "skip_unchanged_loads",
        "sim_mode",
        "stop_on_error",
        "use_batch_check",
        "min_free_mb_for_sim",
        "sim_output_dir",
        "force_reload",
        "run_smart_layout_before_check",
        "run_smart_layout_after",
        "smart_layout_graph_json",
        "smart_layout_graph_json_path",
        "smart_layout_model_path",
        "smart_layout_output_json_path",
        "smart_layout_timeout_seconds",
        "reload_after_smart_layout",
    )
    return {k: p[k] for k in keys if k in p}


def mworks_fast_workflow(
    file_paths: Optional[List[str]] = None,
    check_models: Optional[List[str]] = None,
    simulate_models: Optional[List[str]] = None,
    result_vars: Optional[List[str]] = None,
    time_point: Any = "end",
    auto_load_deps: bool = True,
    skip_unchanged_loads: bool = True,
    sim_mode: int = 0,
    stop_on_error: bool = True,
    use_batch_check: bool = True,
    min_free_mb_for_sim: float = 512,
    sim_output_dir: str = "",
    force_reload: bool = False,
    run_smart_layout_before_check: bool = True,
    run_smart_layout_after: bool = False,
    smart_layout_graph_json: str = "",
    smart_layout_graph_json_path: str = "",
    smart_layout_model_path: str = "",
    smart_layout_output_json_path: str = "",
    smart_layout_timeout_seconds: int = 120,
    reload_after_smart_layout: bool = True,
) -> str:
    """
    Python 辅助：一键 load → check → simulate → KPI（及 Smart Layout）。**非 MCP 工具**；Agent 请用
    ``mworks_sysplorer_call_code(mode=\"fast_workflow\", payload={...})``。

    sim_mode: 0=current mode (auto translate if needed), 1=standalone, 2=real-time.
    """
    return _fast_workflow_impl(
        file_paths=file_paths,
        check_models=check_models,
        simulate_models=simulate_models,
        result_vars=result_vars,
        time_point=time_point,
        auto_load_deps=auto_load_deps,
        skip_unchanged_loads=skip_unchanged_loads,
        sim_mode=sim_mode,
        stop_on_error=stop_on_error,
        use_batch_check=use_batch_check,
        min_free_mb_for_sim=min_free_mb_for_sim,
        sim_output_dir=sim_output_dir,
        force_reload=force_reload,
        run_smart_layout_before_check=run_smart_layout_before_check,
        run_smart_layout_after=run_smart_layout_after,
        smart_layout_graph_json=smart_layout_graph_json,
        smart_layout_graph_json_path=smart_layout_graph_json_path,
        smart_layout_model_path=smart_layout_model_path,
        smart_layout_output_json_path=smart_layout_output_json_path,
        smart_layout_timeout_seconds=smart_layout_timeout_seconds,
        reload_after_smart_layout=reload_after_smart_layout,
    )


@mcp.tool()
def mworks_sysplorer_call_code(mode: str, payload: Optional[Dict[str, Any]] = None) -> str:
    """
    **唯一 MCP 入口**（替代已移除的 ``mworks_run_script`` / ``mworks_submit_job`` / ``mworks_get_job_result`` /
    ``mworks_run_with_ready`` / ``mworks_fast_workflow``）：按 ``mode`` 分流，返回 JSON 与原先各工具一致。

    ## 分流表（必填 ``mode``，大小写不敏感）

    | mode | 能力 | ``payload`` 约定 |
    |------|------|-------------------|
    | ``run_script`` | 进程内 ModelingPy / Sysblock | ``python_source``, ``script_path``, ``capture_stdout`` (默认 true), ``capture_stderr`` (默认 true) |
    | ``submit_job`` | 异步任务 | ``action`` 为 check / translate / simulate；嵌套 ``payload`` 为任务参数字典 |
    | ``get_job_result`` | 取异步结果 | ``job_id`` |
    | ``run_with_ready`` | 就绪后分派 | 顶层 ``action`` + 子参数字典 ``payload``（或别名 ``request``）。别名 mode：``dispatch``、``ready`` |
    | ``fast_workflow`` | 一键工作流 | 与原 ``fast_workflow`` 工具同名的可选字段扁平放入 ``payload`` |

    **run_with_ready** 支持的 ``action`` 列表见 ``MCP_TOOLS.md``（含 ``set_model_param`` 改参，原独立工具已并入）。

    ## 工具箱 API 文档（``run_script`` + ``help``；勿先用 ``get_api_document``）

    针对 **DesignOptMpe**（参数设计 / 优化 / MPE）、**CADToolbox**（CAD 工具箱）、**SimulinkImporter**（Simulink 导入）等 **Sysplorer 独立工具箱**：帮助文本通常不由主编程会话的 ``Help(cmd)`` 提供，**请勿**先调用 ``mworks_sysplorer_get_api_document`` 查询这些函数（常见返回空串或无有效文档）。

    应使用 ``mode="run_script"``：例如 ``import mworks.sysplorer.DesignOptMpe as mpe``、``import mworks.sysplorer.CADToolbox as cadtool`` 或 ``import mworks.sysplorer.SimulinkImporter as slximport``（按实际工具箱包名替换），用对应模块的 ``ListFunctions()`` 列举命令，用 ``help(模块.函数名)`` 查看帮助；若需随 JSON 返回，将 ``help`` 输出写入 ``RUN_SCRIPT_RESULT``（例如 ``io.StringIO`` 重定向 ``sys.stdout``）。
    **DesignOptMpe（参数估计 / 优化 / MPE）** 的补充说明：实操与排错见 ``resources/design_opt_mpe_api/参数估计使用说明.md``，接口全文见同目录 ``DesignOptMpe.md``；也可用 ``mworks_sysplorer_resources_retrieval`` 检索语料 ``design_opt_mpe_api``。
    **SimulinkImporter** 须先 ``OpenSimulinkImporter()`` 再 ``ImportSimulinkModel(.slx 绝对路径, ...)``（其余参数可选），见 ``resources/simulink_importer_api/SimulinkImporter.md``。

    **主编模 ModelingPy 命令**（如 ``OpenModel``、``AddComponent``、``LoadLibrary``）仍推荐使用 ``mworks_sysplorer_get_api_document``。

    **安全**：``run_script`` 为任意代码执行；``MWORKS_RUN_SCRIPT_DISABLED=1`` 时该 mode 拒绝执行。
    """
    from tools.run_script import _mworks_run_script_impl

    m = (mode or "").strip().lower()
    p = payload or {}

    if m == "run_script":
        return _mworks_run_script_impl(
            python_source=str(p.get("python_source", "") or ""),
            script_path=str(p.get("script_path", "") or ""),
            capture_stdout=bool(p.get("capture_stdout", True)),
            capture_stderr=bool(p.get("capture_stderr", True)),
        )

    if m == "submit_job":
        inner = p.get("payload")
        if not isinstance(inner, dict):
            inner = {}
        return _submit_job_core(str(p.get("action", "") or ""), inner)

    if m == "get_job_result":
        return _get_job_result_core(str(p.get("job_id", "") or ""))

    if m in ("run_with_ready", "dispatch", "ready"):
        sub = p.get("payload")
        if not isinstance(sub, dict):
            sub = p.get("request")
        if not isinstance(sub, dict):
            sub = {}
        return _run_with_ready_impl(action=str(p.get("action", "") or ""), payload=sub)

    if m == "fast_workflow":
        return _fast_workflow_impl(**_fast_workflow_kwargs_from_payload(p))

    return _json(
        {
            "ok": False,
            "tool": "mworks_sysplorer_call_code",
            "error": f"Unsupported mode: {mode!r}. "
            "Use run_script | submit_job | get_job_result | run_with_ready | fast_workflow.",
        }
    )
