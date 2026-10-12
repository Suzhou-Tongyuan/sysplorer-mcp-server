#!/usr/bin/env python3
"""Validate a geometry-free, repeatable Sysblock layout input."""

from __future__ import annotations

from typing import Any

from lib.sysblock_core import canonical_bytes, canonical_sha256


SCHEMA = "sysblock-layout-input/v1"
FORBIDDEN_KEYS = {
    "x", "y", "position", "origin", "extent", "frame", "rect", "width", "height",
    "rotation", "layer", "row", "order", "canvas", "anchor", "anchors", "port_anchor",
    "port_anchors", "point", "points", "route", "routes", "lane", "lane_index",
    "feedback_side", "feedback_zone", "oclock", "labelposition", "label_position",
    "geometry", "layout", "blocks",
}
RESIZABLE_KINDS = {
    "SubSystem", "Chart", "State", "Mux", "DeMux", "VectorConcatenate",
    "BusCreator", "BusSelector", "MultiportSwitch", "Switch",
}


def _geometry_hits(value: Any, path: str = "$") -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            child = f"{path}.{key_text}"
            if key_text.replace("-", "_").lower() in FORBIDDEN_KEYS:
                hits.append({"path": child, "field": key_text})
            hits.extend(_geometry_hits(item, child))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(_geometry_hits(item, f"{path}[{index}]"))
    return hits


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item for item in value)


def audit(spec: Any) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    if not isinstance(spec, dict) or spec.get("schema") != SCHEMA:
        issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": "$.schema"})
        return {
            "schema": "sysblock-layout-input-audit/v1",
            "passed": False,
            "canonical_sha256": "",
            "issue_count": len(issues),
            "issues": issues,
        }

    geometry_hits = _geometry_hits(spec)
    if geometry_hits:
        issues.append({"code": "GEOMETRY_PRESENT", "hits": geometry_hits})

    if not isinstance(spec.get("case_id"), str) or not spec["case_id"].strip():
        issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": "$.case_id"})
    levels = spec.get("levels")
    charts = spec.get("charts")
    policies = spec.get("policies")
    if not isinstance(levels, list) or not isinstance(charts, list) or not isinstance(policies, dict):
        issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": "$"})
        levels = levels if isinstance(levels, list) else []
        charts = charts if isinstance(charts, list) else []
        policies = policies if isinstance(policies, dict) else {}
    if policies.get("ordinary_size") != "standard" or policies.get("topology_frozen") is not True:
        issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": "$.policies"})
    kinds = policies.get("resizable_kinds")
    if not _string_list(kinds) or not set(kinds).issubset(RESIZABLE_KINDS):
        issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": "$.policies.resizable_kinds"})

    level_paths: set[str] = set()
    chart_paths: set[str] = set()
    for level_index, level in enumerate(levels):
        base = f"$.levels[{level_index}]"
        if not isinstance(level, dict):
            issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": base})
            continue
        path = level.get("path")
        if not isinstance(path, str) or not path or path in level_paths:
            issues.append({"code": "TOPOLOGY_INVALID", "path": f"{base}.path"})
        else:
            level_paths.add(path)
        nodes = level.get("nodes")
        edges = level.get("edges")
        feedback_paths = level.get("feedback_paths")
        if not isinstance(nodes, list) or not isinstance(edges, list) or not isinstance(feedback_paths, list):
            issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": base})
            continue
        node_map: dict[str, dict] = {}
        for node_index, node in enumerate(nodes):
            node_path = f"{base}.nodes[{node_index}]"
            if not isinstance(node, dict):
                issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": node_path})
                continue
            node_id = node.get("id")
            if (
                not isinstance(node_id, str) or not node_id or node_id in node_map
                or not isinstance(node.get("kind"), str)
                or not isinstance(node.get("name"), str)
                or not _string_list(node.get("inputs"))
                or not _string_list(node.get("outputs"))
                or len(node.get("inputs", [])) != len(set(node.get("inputs", [])))
                or len(node.get("outputs", [])) != len(set(node.get("outputs", [])))
            ):
                issues.append({"code": "TOPOLOGY_INVALID", "path": node_path})
            elif node_id:
                node_map[node_id] = node
        edge_map: dict[str, dict] = {}
        for edge_index, edge in enumerate(edges):
            edge_path = f"{base}.edges[{edge_index}]"
            if not isinstance(edge, dict):
                issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": edge_path})
                continue
            edge_id = edge.get("id")
            source = node_map.get(edge.get("source"))
            target = node_map.get(edge.get("target"))
            invalid = (
                not isinstance(edge_id, str) or not edge_id or edge_id in edge_map
                or source is None or target is None
                or edge.get("source_port") not in (source or {}).get("outputs", [])
                or edge.get("target_port") not in (target or {}).get("inputs", [])
            )
            if invalid:
                issues.append({"code": "TOPOLOGY_INVALID", "path": edge_path})
            elif edge_id:
                edge_map[edge_id] = edge
        feedback_edge_ids: set[str] = set()
        for feedback_index, feedback in enumerate(feedback_paths):
            feedback_path = f"{base}.feedback_paths[{feedback_index}]"
            if (
                not isinstance(feedback, dict)
                or not isinstance(feedback.get("id"), str)
                or not _string_list(feedback.get("edge_ids"))
                or not _string_list(feedback.get("member_node_ids"))
                or feedback.get("signal_flow") != "right_to_left"
                or not set(feedback.get("edge_ids", [])).issubset(edge_map)
                or not set(feedback.get("member_node_ids", [])).issubset(node_map)
                or feedback_edge_ids.intersection(feedback.get("edge_ids", []))
            ):
                issues.append({"code": "TOPOLOGY_INVALID", "path": feedback_path})
            else:
                feedback_edge_ids.update(feedback["edge_ids"])

    for chart_index, chart in enumerate(charts):
        base = f"$.charts[{chart_index}]"
        if not isinstance(chart, dict):
            issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": base})
            continue
        path = chart.get("path")
        if not isinstance(path, str) or not path or path in chart_paths:
            issues.append({"code": "TOPOLOGY_INVALID", "path": f"{base}.path"})
        else:
            chart_paths.add(path)
        states = chart.get("states")
        transitions = chart.get("transitions")
        if not isinstance(states, list) or not isinstance(transitions, list):
            issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": base})
            continue
        state_ids = [state.get("id") for state in states if isinstance(state, dict)]
        if len(state_ids) != len(states) or len(state_ids) != len(set(state_ids)) or not all(isinstance(item, str) and item for item in state_ids):
            issues.append({"code": "TOPOLOGY_INVALID", "path": f"{base}.states"})
        state_set = set(state_ids)
        decomposition = chart.get("decomposition")
        default_state = chart.get("default_state")
        if decomposition not in {"exclusive", "parallel"}:
            issues.append({"code": "TOPOLOGY_INVALID", "path": f"{base}.decomposition"})
        transition_ids: set[str] = set()
        priorities: dict[str | None, set[int]] = {}
        default_transitions = []
        for transition_index, transition in enumerate(transitions):
            transition_path = f"{base}.transitions[{transition_index}]"
            if not isinstance(transition, dict):
                issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": transition_path})
                continue
            transition_id = transition.get("id")
            source = transition.get("source")
            target = transition.get("target")
            priority = transition.get("priority")
            source_priorities = priorities.setdefault(source, set())
            if (
                not isinstance(transition_id, str) or not transition_id or transition_id in transition_ids
                or (source is not None and source not in state_set) or target not in state_set
                or not isinstance(transition.get("label"), str)
                or not isinstance(priority, int) or isinstance(priority, bool) or priority < 1
                or priority in source_priorities
            ):
                issues.append({"code": "TOPOLOGY_INVALID", "path": transition_path})
            else:
                transition_ids.add(transition_id)
                source_priorities.add(priority)
                if source is None:
                    default_transitions.append(transition)
        if decomposition == "exclusive":
            if default_state not in state_set:
                issues.append({"code": "TOPOLOGY_INVALID", "path": f"{base}.default_state"})
            if len(default_transitions) != 1 or default_transitions[0].get("target") != default_state:
                issues.append({"code": "TOPOLOGY_INVALID", "path": f"{base}.transitions", "detail": "an exclusive Chart requires exactly one default transition targeting default_state"})
        elif decomposition == "parallel":
            if default_state is not None:
                issues.append({"code": "TOPOLOGY_INVALID", "path": f"{base}.default_state", "detail": "a parallel Chart requires default_state=null"})
            if default_transitions:
                issues.append({"code": "TOPOLOGY_INVALID", "path": f"{base}.transitions", "detail": "a parallel Chart allows no top-level default transition"})

    digest = ""
    try:
        digest = canonical_sha256(spec)
    except (TypeError, ValueError):
        issues.append({"code": "LAYOUT_INPUT_SCHEMA_INVALID", "path": "$", "detail": "non-canonical JSON value"})
    return {
        "schema": "sysblock-layout-input-audit/v1",
        "passed": not issues,
        "canonical_sha256": digest,
        "level_count": len(levels),
        "chart_count": len(charts),
        "issue_count": len(issues),
        "issues": issues,
    }
