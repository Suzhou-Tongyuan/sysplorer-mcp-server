"""Layout tools: unified Smart Layout MCP tool (replaces three separate layout tools)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Tuple, List

from mcp_instance import mcp, writable_annotations
from constants import _CLASS_RE, _PROJECT_ROOT, _WITHIN_RE
from core.smart_layout import (
    _normalize_graph_format,
    _smart_layout_engine,
    _apply_layout_graph_to_modelica_code,
)
from core.layout_official import persist_official_routeline
from core.modelica_graph_builder import build_graph_from_modelica_34_source
from core.utils import _json, infer_modelica_top_class_fq_from_mo


def _normalize_smart_layout_mode(mode: str) -> str:
    raw = (mode or "layout_only").strip().lower()
    aliases = {
        "layout": "layout_only",
        "compute": "layout_only",
        "graph": "layout_only",
        "auto_layout_smart": "layout_only",
        "finalize": "finalize_generation",
        "finalize_payload": "finalize_generation",
        "finalize_generated_model_with_auto_layout": "finalize_generation",
        "writeback": "writeback_mo",
        "generate": "writeback_mo",
        "generate_system_model": "writeback_mo",
        "generate_system_model_with_auto_layout": "writeback_mo",
    }
    return aliases.get(raw, raw)


def _layout_only_missing_graph_error(
    graph_json: str = "",
    graph_json_path: str = "",
    model_name: str = "",
    modelica_code: str = "",
    model_output_path: str = "",
) -> str:
    parts = [
        "mode=layout_only requires input_graph_json or input_json_path (pre-built graph JSON). "
        "It does not parse .mo files."
    ]
    if (graph_json or "").strip() or (graph_json_path or "").strip():
        parts.append(
            "graph_json/graph_json_path are writeback_mo fields; pass the same JSON as "
            "input_graph_json/input_json_path."
        )
    if (model_name or "").strip() or (modelica_code or "").strip() or (model_output_path or "").strip():
        parts.append(
            "model_name, modelica_code, model_output_path and auto_generate_graph are ignored "
            "in layout_only; use mode=writeback_mo to generate a graph from a .mo."
        )
    return " ".join(parts)


def _layout_only_core(
    input_graph_json: str = "",
    input_json_path: str = "",
    output_json_path: str = "",
    graph_json: str = "",
    graph_json_path: str = "",
    model_name: str = "",
    modelica_code: str = "",
    model_output_path: str = "",
) -> Dict[str, Any]:
    if not input_graph_json and not input_json_path:
        return {
            "success": False,
            "mode": "layout_only",
            "error": _layout_only_missing_graph_error(
                graph_json=graph_json,
                graph_json_path=graph_json_path,
                model_name=model_name,
                modelica_code=modelica_code,
                model_output_path=model_output_path,
            ),
        }

    if input_graph_json:
        graph = json.loads(input_graph_json)
    else:
        p = Path(input_json_path).resolve()
        if not p.exists():
            return {"success": False, "error": f"Input JSON not found: {p}"}
        graph = json.loads(p.read_text(encoding="utf-8"))

    if isinstance(graph, dict):
        graph = _normalize_graph_format(graph)

    layout_data = _smart_layout_engine(graph)

    out_str = ""
    if output_json_path:
        out_p = Path(output_json_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(layout_data, ensure_ascii=False, indent=2), encoding="utf-8")
        out_str = str(out_p)

    return {
        "success": True,
        "engine": "smart_layout",
        "mode": "layout_only",
        "output_path": out_str,
        "nodes": len(layout_data.get("children", [])),
        "edges": len(layout_data.get("edges", [])),
        "layout": layout_data,
        "_layout": layout_data,
    }


def _finalize_core(
    generation_result_json: str,
    graph_key: str = "",
    output_json_path: str = "",
    timeout_seconds: int = 120,
) -> Dict[str, Any]:
    _ = timeout_seconds
    try:
        payload = json.loads(generation_result_json)
    except json.JSONDecodeError as exc:
        return {"success": False, "error": f"Invalid generation_result_json: {exc}"}

    if not isinstance(payload, dict):
        return {"success": False, "error": "generation_result_json must be a JSON object."}

    candidate_keys = [graph_key] if graph_key else [
        "graph",
        "elk_graph",
        "layout_graph",
        "layout_input_json",
        "layout_input_path",
        "graph_json_path",
    ]

    selected_key = ""
    graph_value = None
    for key in candidate_keys:
        if not key:
            continue
        if key in payload and payload[key] not in (None, ""):
            selected_key = key
            graph_value = payload[key]
            break

    if graph_value is None:
        return {
            "success": False,
            "error": "No graph payload found. Provide graph_key or include one of "
            "['graph','elk_graph','layout_graph','layout_input_json','layout_input_path','graph_json_path'].",
        }

    def _resolve_graph_json(gv: Any) -> str:
        if isinstance(gv, (dict, list)):
            return json.dumps(gv, ensure_ascii=False)
        if isinstance(gv, str):
            return gv.strip()
        raise TypeError(f"Unsupported graph payload type: {type(gv).__name__}")

    graph_json_str = _resolve_graph_json(graph_value)

    use_file_path = graph_json_str and not (
        graph_json_str.startswith("{") or graph_json_str.startswith("[")
    )

    if use_file_path:
        layout_result = _layout_only_core(
            input_json_path=graph_json_str,
            output_json_path=output_json_path,
        )
    else:
        layout_result = _layout_only_core(
            input_graph_json=graph_json_str,
            output_json_path=output_json_path,
        )

    layout_graph = layout_result.get("_layout", {})
    merged = dict(payload)
    if layout_result.get("success") and layout_graph:
        merged["layout_graph"] = layout_graph

    return {
        "success": bool(layout_result.get("success")),
        "engine": "smart",
        "mode": "finalize_generation",
        "output_path": layout_result.get("output_path", ""),
        "nodes": layout_result.get("nodes", 0),
        "edges": layout_result.get("edges", 0),
        "selected_graph_key": selected_key,
        "generation_result": merged,
    }


def _infer_model_name_from_modelica_text(text: str) -> str:
    raw = text or ""
    wm = _WITHIN_RE.search(raw)
    prefix = wm.group(1).strip() if wm else ""
    m = _CLASS_RE.search(raw)
    if not m:
        return ""
    name = m.group(2)
    return f"{prefix}.{name}" if prefix else name


def _resolve_writeback_model_name(
    model_name: str = "",
    modelica_code: str = "",
    model_output_path: str = "",
) -> Tuple[str, str]:
    """Return (resolved_name, source). source is explicit|modelica_code|mo_file|path_stem|""."""
    explicit = (model_name or "").strip()
    if explicit:
        return explicit, "explicit"
    code = (modelica_code or "").strip()
    if code:
        inferred = _infer_model_name_from_modelica_text(code)
        if inferred:
            return inferred, "modelica_code"
    path_text = (model_output_path or "").strip()
    if path_text:
        p = Path(path_text)
        if p.is_file():
            from_file = infer_modelica_top_class_fq_from_mo(p)
            if from_file:
                return from_file, "mo_file"
        stem = p.stem.strip()
        if stem and stem.lower() != "package":
            return stem, "path_stem"
    return "", ""


def _writeback_mo_core(
    model_name: str,
    modelica_code: str = "",
    model_output_path: str = "",
    graph_json_path: str = "",
    graph_json: str = "",
    auto_layout: bool = True,
    auto_generate_graph: bool = True,
    graph_parser: str = "modelica_34_ast",
    layout_output_json_path: str = "",
    timeout_seconds: int = 120,
) -> Dict[str, Any]:
    name, name_source = _resolve_writeback_model_name(model_name, modelica_code, model_output_path)
    if not name:
        return {
            "success": False,
            "mode": "writeback_mo",
            "error": (
                "mode=writeback_mo requires model_name (fully-qualified class name, "
                "e.g. MassSpringDamper.StepForceTest). Pass model_name explicitly, or "
                "provide modelica_code / an existing model_output_path so it can be inferred."
            ),
        }

    output_path = (
        Path(model_output_path).resolve()
        if model_output_path
        else (_PROJECT_ROOT / "src" / "GeneratedLibrary" / "Examples" / f"{name}.mo")
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wrote_model = False
    if modelica_code.strip():
        output_path.write_text(modelica_code, encoding="utf-8")
        wrote_model = True

    result: Dict[str, Any] = {
        "success": True,
        "mode": "writeback_mo",
        "model_name": name,
        "model_name_source": name_source,
        "model_output_path": str(output_path),
        "model_written": wrote_model,
        "auto_layout_requested": bool(auto_layout),
    }

    if not auto_layout:
        if wrote_model:
            try:
                from tools.model_ops import mworks_load_file

                raw_r = mworks_load_file(
                    str(output_path),
                    auto_load_deps=False,
                    skip_if_unchanged=False,
                    force_reload=True,
                )
                result["reload_after_writeback"] = json.loads(raw_r)
            except Exception as exc:
                result["reload_after_writeback"] = {"ok": False, "error": str(exc)}
        return result

    graph_source = ""
    graph_diagnostics: List[Dict[str, Any]] = []
    payload: Dict[str, object] = {"model_name": name}
    if graph_json.strip():
        payload["graph"] = json.loads(graph_json)
        graph_source = "graph_json"
    elif graph_json_path.strip():
        payload["graph_json_path"] = graph_json_path.strip()
        graph_source = "graph_json_path"
    elif auto_generate_graph and graph_parser != "off":
        if not output_path.exists():
            return {
                **result,
                "success": False,
                "error": f"auto_generate_graph=True requires an existing .mo file: {output_path}",
            }
        source_text = output_path.read_text(encoding="utf-8")
        gb = build_graph_from_modelica_34_source(source_text, model_name=name)
        graph_diagnostics = list(gb.diagnostics or [])
        if gb.ok and gb.graph and not gb.error:
            payload["graph"] = gb.graph
            graph_source = gb.source or "modelica_34_ast"
        elif gb.ok and gb.graph and gb.error and "无需布局" in gb.error:
            return {
                **result,
                "success": True,
                "skipped": True,
                "reason": gb.error,
                "graph_source": gb.source or "modelica_34_ast",
                "diagnostics": graph_diagnostics,
                "components_updated": 0,
                "connects_updated": 0,
            }
        else:
            # Fall back to the legacy regex extractor while the AST parser is maturing.
            legacy_ok, legacy_graph, legacy_err = _parse_modelica_to_graph_legacy(source_text, model_name=name)
            if legacy_ok:
                payload["graph"] = legacy_graph
                graph_source = "legacy_regex"
                graph_diagnostics.append(
                    {
                        "severity": "warning",
                        "code": "modelica_34_ast_fallback",
                        "message": gb.error or "Modelica 3.4 parser failed; used legacy regex graph extractor",
                    }
                )
            elif "无需布局" in (legacy_err or ""):
                return {
                    **result,
                    "success": True,
                    "skipped": True,
                    "reason": legacy_err,
                    "graph_source": "legacy_regex",
                    "diagnostics": graph_diagnostics,
                    "components_updated": 0,
                    "connects_updated": 0,
                }
            else:
                return {
                    **result,
                    "success": False,
                    "error": f"自动生成graph失败: {gb.error or legacy_err}",
                    "graph_source": gb.source or "modelica_34_ast",
                    "diagnostics": graph_diagnostics,
                }
    else:
        return {
            **result,
            "success": False,
            "error": "auto_layout=True requires graph_json/graph_json_path, or auto_generate_graph=True with model_output_path.",
        }

    layout_dict = _finalize_core(
        generation_result_json=json.dumps(payload, ensure_ascii=False),
        output_json_path=layout_output_json_path,
        timeout_seconds=timeout_seconds,
    )
    comp_updated = 0
    conn_updated = 0
    writeback_error = ""
    writeback_applied = False
    writeback_diagnostics: List[Dict[str, Any]] = []
    try:
        layout_payload = layout_dict.get("generation_result", {}) if isinstance(layout_dict, dict) else {}
        layout_graph = layout_payload.get("layout_graph", {}) if isinstance(layout_payload, dict) else {}
        if layout_dict.get("success") and isinstance(layout_graph, dict) and output_path.exists():
            original_code = output_path.read_text(encoding="utf-8")
            patched_code, stats = _apply_layout_graph_to_modelica_code(original_code, layout_graph)
            comp_updated = int(stats.get("components_updated", 0))
            conn_updated = int(stats.get("connects_updated", 0))
            writeback_diagnostics = list(stats.get("diagnostics", []) or [])
            writeback_applied = patched_code != original_code
            if writeback_applied:
                output_path.write_text(patched_code, encoding="utf-8")
    except Exception as exc:
        writeback_error = str(exc)

    out: Dict[str, Any] = {
        **result,
        "success": bool(layout_dict.get("success")),
        "nodes": layout_dict.get("nodes", 0),
        "edges": layout_dict.get("edges", 0),
        "components_updated": comp_updated,
        "connects_updated": conn_updated,
        "writeback_applied": writeback_applied,
        "source_text_written": wrote_model,
        "annotations_written": writeback_applied,
        "disk_changed": bool(wrote_model or writeback_applied),
        "graph_source": graph_source,
        "flag_notes": {
            "model_written": (
                "True only if incoming modelica_code was saved as the whole .mo. "
                "Patching Placement/Line on an existing file leaves this false."
            ),
            "writeback_applied": (
                "True if Placement/Line annotations in the .mo were changed. "
                "This is the flag that means diagram writeback hit disk."
            ),
        },
    }
    if graph_diagnostics:
        out["diagnostics"] = graph_diagnostics
        if out.get("success"):
            out["diagnostics_are_fatal"] = False
            out["agent_hint"] = (
                "diagnostics are non-fatal parser notes. "
                "If writeback_applied is true, Placement/Line were written; "
                "do not hand-edit the .mo to 'fix' layout."
            )
    if writeback_diagnostics:
        out["writeback_diagnostics"] = writeback_diagnostics
    if writeback_error:
        out["writeback_error"] = writeback_error
    if out.get("success") and output_path.exists():
        try:
            from tools.model_ops import mworks_load_file

            raw_r = mworks_load_file(
                str(output_path),
                auto_load_deps=False,
                skip_if_unchanged=False,
                force_reload=True,
            )
            out["reload_after_writeback"] = json.loads(raw_r)
        except Exception as exc:
            out["reload_after_writeback"] = {"ok": False, "error": str(exc)}
        reload_info = out.get("reload_after_writeback")
        reload_ok = isinstance(reload_info, dict) and bool(reload_info.get("ok"))
        if reload_ok and int(out.get("edges") or 0) >= 1:
            # Placement + connect() are on disk; official RouteLine owns the wire geometry.
            official = persist_official_routeline(
                name,
                save_folder=str(output_path.parent),
                overwrite_existing=True,
            )
            out["official_route"] = official
            if official.get("ok"):
                out["router"] = "official"
            else:
                out["router"] = "builtin"
                out["official_route_fallback"] = official.get("error") or "RouteLine unavailable"
            if out.get("disk_changed") and not official.get("persisted"):
                out["layout_writeback_ok"] = True
                out["session_persist_ok"] = False
                out["agent_hint"] = (
                    (out.get("agent_hint") + " ") if out.get("agent_hint") else ""
                ) + (
                    "disk_changed=true means Placement/Line are already on disk. "
                    "SaveModel/SaveModelAs False after RouteLine is a persist conflict, "
                    "not a smart_layout writeback failure."
                )
        else:
            out["router"] = "builtin"
    return out


@mcp.tool(annotations=writable_annotations())
def smart_layout(
    mode: str = "layout_only",
    input_graph_json: str = "",
    input_json_path: str = "",
    output_json_path: str = "",
    generation_result_json: str = "",
    graph_key: str = "",
    model_name: str = "",
    modelica_code: str = "",
    model_output_path: str = "",
    graph_json_path: str = "",
    graph_json: str = "",
    auto_layout: bool = True,
    auto_generate_graph: bool = True,
    graph_parser: str = "modelica_34_ast",
    layout_output_json_path: str = "",
    timeout_seconds: int = 120,
) -> str:
    """Place components and route wires. Response includes ``ok`` aligned with ``success``.

    | mode | required |
    |------|----------|
    | ``layout_only`` | ``input_graph_json`` or ``input_json_path`` |
    | ``finalize_generation`` | ``generation_result_json`` |
    | ``writeback_mo`` | ``model_name`` and a ``.mo`` (``model_output_path`` and/or ``modelica_code``) |
    """
    m = _normalize_smart_layout_mode(mode)
    try:
        if m == "layout_only":
            try:
                return _json(
                    _layout_only_core(
                        input_graph_json,
                        input_json_path,
                        output_json_path,
                        graph_json=graph_json,
                        graph_json_path=graph_json_path,
                        model_name=model_name,
                        modelica_code=modelica_code,
                        model_output_path=model_output_path,
                    )
                )
            except json.JSONDecodeError as exc:
                return _json({"success": False, "error": f"Invalid JSON: {exc}", "mode": m})
            except Exception as exc:
                return _json({"success": False, "error": f"Smart layout failed: {str(exc)}", "mode": m})

        if m == "finalize_generation":
            try:
                return _json(_finalize_core(generation_result_json, graph_key, output_json_path, timeout_seconds))
            except Exception as exc:
                return _json({"success": False, "error": f"Finalize with auto layout failed: {str(exc)}", "mode": m})

        if m == "writeback_mo":
            try:
                return _json(
                    _writeback_mo_core(
                        model_name=model_name,
                        modelica_code=modelica_code,
                        model_output_path=model_output_path,
                        graph_json_path=graph_json_path,
                        graph_json=graph_json,
                        auto_layout=auto_layout,
                        auto_generate_graph=auto_generate_graph,
                        graph_parser=graph_parser,
                        layout_output_json_path=layout_output_json_path,
                        timeout_seconds=timeout_seconds,
                    )
                )
            except json.JSONDecodeError as exc:
                return _json({"success": False, "error": f"Invalid graph_json: {exc}", "mode": m})
            except Exception as exc:
                return _json({"success": False, "error": f"Writeback failed: {str(exc)}", "mode": m})

        return _json(
            {
                "success": False,
                "error": f"Unknown mode: {mode!r}. Use layout_only | finalize_generation | writeback_mo.",
                "mode": m,
            }
        )
    except Exception as exc:
        return _json({"success": False, "error": str(exc), "mode": m})


def _parse_modelica_to_graph_legacy(modelica_code: str, model_name: str = "") -> Tuple[bool, Dict[str, Any], str]:
    """
    解析 Modelica 代码，自动提取组件和连接生成 layout graph
    返回: (success, graph_dict, error_msg)
    """
    try:
        # 匹配组件声明：类似 "Sources.StepVoltage stepVoltage(...)" 或 "Basic.Resistor R1(...)"
        comp_pattern = re.compile(
            r'^\s*(?:[a-zA-Z0-9_.]+\s+)+([a-zA-Z0-9_]+)\s*(?:\([^)]*\))?\s*(?:"[^"]*")?\s*(?:annotation\([^)]*\))?;',
            re.MULTILINE
        )
        # 匹配 connect 语句：connect(a.b, c.d)
        connect_pattern = re.compile(
            r'^\s*connect\s*\(\s*([a-zA-Z0-9_.]+)\s*,\s*([a-zA-Z0-9_.]+)\s*\)\s*(?:annotation\([^)]*\))?;',
            re.MULTILINE
        )

        # 提取所有组件名
        components: List[str] = []
        for match in comp_pattern.finditer(modelica_code):
            comp_name = match.group(1)
            # 排除非组件声明（如Real、Integer等变量声明）
            if not comp_name[0].isupper():  # 组件实例名通常首字母小写，类名首字母大写
                components.append(comp_name)

        # 提取所有连接
        edges: List[Dict[str, Any]] = []
        ports_set: set[str] = set()
        for match in connect_pattern.finditer(modelica_code):
            source = match.group(1)
            target = match.group(2)
            edges.append({
                "sources": [source],
                "targets": [target]
            })
            ports_set.add(source)
            ports_set.add(target)

        # 构建组件节点（每个组件包含它的所有端口）
        children: List[Dict[str, Any]] = []
        for comp in components:
            # 收集这个组件的所有端口
            comp_ports = [p for p in ports_set if p.startswith(f"{comp}.")]
            ports = [{"id": p} for p in comp_ports]
            # 默认节点大小
            children.append({
                "id": comp,
                "width": 30,
                "height": 40,
                "ports": ports
            })

        # 构建graph
        graph = {
            "id": model_name or "auto_generated_graph",
            "children": children,
            "edges": edges
        }

        # 至少要有2个组件和1条连接才需要布局
        if len(children) < 2 or len(edges) < 1:
            return False, {}, "模型组件少于2个或无连接，无需布局"

        return True, graph, ""

    except Exception as exc:
        return False, {}, f"解析Modelica代码失败: {str(exc)}"


def _parse_modelica_to_graph(modelica_code: str, model_name: str = "") -> Tuple[bool, Dict[str, Any], str]:
    """
    Generate a Smart Layout graph from Modelica source.

    Prefer the Modelica 3.4 structure parser and keep the legacy regex extractor
    as a compatibility fallback for partially supported sources.
    """
    try:
        result = build_graph_from_modelica_34_source(modelica_code, model_name=model_name)
        if result.ok and result.graph and not result.error:
            return True, result.graph, ""
        if result.ok and result.graph and "无需布局" in (result.error or ""):
            return False, result.graph, result.error
        legacy_ok, legacy_graph, legacy_err = _parse_modelica_to_graph_legacy(modelica_code, model_name=model_name)
        if legacy_ok:
            legacy_graph.setdefault("metadata", {})
            if isinstance(legacy_graph["metadata"], dict):
                legacy_graph["metadata"]["parser"] = "legacy_regex"
                legacy_graph["metadata"]["fallback_from"] = "modelica_34_ast"
                legacy_graph["metadata"]["modelica_34_ast_error"] = result.error
            return True, legacy_graph, ""
        return False, {}, result.error or legacy_err
    except Exception as exc:
        legacy_ok, legacy_graph, legacy_err = _parse_modelica_to_graph_legacy(modelica_code, model_name=model_name)
        if legacy_ok:
            legacy_graph.setdefault("metadata", {})
            if isinstance(legacy_graph["metadata"], dict):
                legacy_graph["metadata"]["parser"] = "legacy_regex"
                legacy_graph["metadata"]["fallback_error"] = str(exc)
            return True, legacy_graph, ""
        return False, {}, f"解析Modelica代码失败: {str(exc)}; legacy: {legacy_err}"


def run_smart_layout_for_fast_workflow(
    graph_json: str = "",
    graph_json_path: str = "",
    model_output_path: str = "",
    model_name: str = "",
    layout_output_json_path: str = "",
    timeout_seconds: int = 120,
    auto_generate_graph: bool = True,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Internal helper：供 ``fast_workflow`` 流程前置/后置布局与 ``model_ops`` 预检调用。返回 (ok, result_dict)。
    """
    mo = (model_output_path or "").strip()
    if not mo:
        return False, {"success": False, "error": "model_output_path is required for writeback."}
    p = Path(mo).resolve()
    if not p.exists():
        return False, {"success": False, "error": f"model file not found: {p}"}
    stem = (model_name or "").strip() or p.stem

    final_graph_json = graph_json.strip()
    final_graph_json_path = graph_json_path.strip()

    if not final_graph_json and not final_graph_json_path and not auto_generate_graph:
        return False, {"success": False, "error": "graph_json/graph_json_path is required, or enable auto_generate_graph."}

    raw = smart_layout(
        mode="writeback_mo",
        model_name=stem,
        model_output_path=str(p),
        graph_json=final_graph_json,
        graph_json_path=final_graph_json_path,
        auto_layout=True,
        auto_generate_graph=auto_generate_graph,
        graph_parser="modelica_34_ast",
        layout_output_json_path=layout_output_json_path,
        timeout_seconds=timeout_seconds,
    )
    data = json.loads(raw)
    return bool(data.get("success")), data
