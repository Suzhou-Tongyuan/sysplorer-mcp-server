#!/usr/bin/env python3
"""Project a semantic/API inventory into a geometry-free layout testcase."""

from __future__ import annotations

import json

from audit_layout_input import RESIZABLE_KINDS, audit


NODE_FIELDS = ("id", "kind", "name", "inputs", "outputs", "parameters", "semantic_role", "required")
EDGE_FIELDS = ("id", "source", "source_port", "target", "target_port", "one_to_one_interface")
FEEDBACK_FIELDS = ("id", "edge_ids", "member_node_ids", "signal_flow")
STATE_FIELDS = ("id", "name", "label", "parent", "decomposition")
TRANSITION_FIELDS = ("id", "source", "target", "label", "priority")


def select(item: dict, fields: tuple[str, ...]) -> dict:
    return {field: item[field] for field in fields if field in item}


def prepare(source: dict) -> dict:
    result = {
        "schema": "sysblock-layout-input/v1",
        "case_id": str(source.get("case_id", "layout-case")),
        "description": str(source.get("description", "")),
        "levels": [],
        "charts": [],
        "policies": {
            "ordinary_size": "standard",
            "resizable_kinds": sorted(RESIZABLE_KINDS),
            "topology_frozen": True,
            "uniform_subsystem_size_allowed": bool(
                source.get("policies", {}).get("uniform_subsystem_size_allowed", True)
            ),
        },
    }
    for level in source.get("levels", []):
        result["levels"].append({
            "path": level["path"],
            "nodes": [select(item, NODE_FIELDS) for item in level.get("nodes", [])],
            "edges": [select(item, EDGE_FIELDS) for item in level.get("edges", [])],
            "feedback_paths": [select(item, FEEDBACK_FIELDS) for item in level.get("feedback_paths", [])],
        })
    for chart in source.get("charts", []):
        result["charts"].append({
            "path": chart["path"],
            "decomposition": chart.get("decomposition", "exclusive"),
            "default_state": chart.get("default_state"),
            "states": [select(item, STATE_FIELDS) for item in chart.get("states", [])],
            "transitions": [select(item, TRANSITION_FIELDS) for item in chart.get("transitions", [])],
        })
    report = audit(result)
    if not report["passed"]:
        raise ValueError(json.dumps(report, ensure_ascii=False))
    return result
