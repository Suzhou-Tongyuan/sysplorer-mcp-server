#!/usr/bin/env python3
"""Plan ordinary Sysblock levels or cyclic/acyclic StateMachine Charts."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict, deque
from pathlib import Path

from audit_layout_input import audit as audit_layout_input
from layout_geometry_audit import audit as audit_chart_layout
from lib.layout_core import Rect, ensure_transition_projection, projection_overlaps
from lib.sysblock_core import read_json, write_json


def _text_size(state: dict) -> tuple[float, float]:
    text = str(state.get("label", state.get("name", state["id"])))
    lines = text.splitlines() or [text]
    return min(280.0, max(100.0, max(map(len, lines)) * 6.0 + 24.0)), max(60.0, len(lines) * 18.0 + 24.0)


def _select_chart(layout_input: dict, chart_path: str | None) -> dict:
    charts = layout_input.get("charts", [])
    if chart_path is None:
        if len(charts) != 1:
            raise ValueError("--chart is required when the input has zero or multiple Charts")
        return charts[0]
    matches = [item for item in charts if item.get("path") == chart_path]
    if len(matches) != 1:
        raise ValueError(f"Unknown or duplicate Chart: {chart_path}")
    return matches[0]


def _acyclic_ranks(state_ids: list[str], transitions: list[dict]) -> dict[str, int] | None:
    outgoing: dict[str, list[str]] = defaultdict(list)
    indegree = {state_id: 0 for state_id in state_ids}
    for transition in transitions:
        source, target = transition["source"], transition["target"]
        if source == target:
            return None
        outgoing[source].append(target)
        indegree[target] += 1
    queue = deque(state_id for state_id in state_ids if indegree[state_id] == 0)
    rank = {state_id: 0 for state_id in queue}
    visited = []
    while queue:
        source = queue.popleft()
        visited.append(source)
        for target in outgoing[source]:
            rank[target] = max(rank.get(target, 0), rank[source] + 1)
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return rank if len(visited) == len(state_ids) else None


def _base_rects(states: list[dict], transitions: list[dict]) -> tuple[dict[str, Rect], str]:
    state_ids = [item["id"] for item in states]
    sizes = {item["id"]: _text_size(item) for item in states}
    ranks = _acyclic_ranks(state_ids, transitions)
    positions: dict[str, tuple[int, int]] = {}
    strategy = "acyclic-ranks"
    if ranks is not None:
        by_rank: dict[int, list[str]] = defaultdict(list)
        for state_id in state_ids:
            by_rank[ranks[state_id]].append(state_id)
        for column, rank_value in enumerate(sorted(by_rank)):
            for row, state_id in enumerate(by_rank[rank_value]):
                positions[state_id] = (column, row)
    else:
        strategy = "cyclic-serpentine"
        columns = max(2, (len(state_ids) + 1) // 2)
        for index, state_id in enumerate(state_ids):
            if index < columns:
                positions[state_id] = (index, 0)
            else:
                positions[state_id] = (columns - 1 - (index - columns), 1)
    column_widths: dict[int, float] = defaultdict(float)
    row_heights: dict[int, float] = defaultdict(float)
    for state_id, (column, row) in positions.items():
        width, height = sizes[state_id]
        column_widths[column] = max(column_widths[column], width)
        row_heights[row] = max(row_heights[row], height)
    x_centers: dict[int, float] = {}
    cursor = 0.0
    for column in sorted(column_widths):
        x_centers[column] = cursor + column_widths[column] / 2.0
        cursor += column_widths[column] + 60.0
    y_centers: dict[int, float] = {}
    cursor = 0.0
    for row in sorted(row_heights):
        y_centers[row] = -(cursor + row_heights[row] / 2.0)
        cursor += row_heights[row] + 80.0
    rects = {}
    for state_id, (column, row) in positions.items():
        width, height = sizes[state_id]
        cx, cy = x_centers[column], y_centers[row]
        rects[state_id] = Rect(state_id, cx - width / 2.0, cy - height / 2.0, cx + width / 2.0, cy + height / 2.0)
    return rects, strategy


def _oclock(rect: Rect, point: list[float]) -> float:
    cx, cy = rect.center
    px, py = point
    return (math.atan2(px - cx, py - cy) * 6.0 / math.pi) % 12.0


def _route(rects: dict[str, Rect], source_name: str, target_name: str, min_overlap: float) -> tuple[str, list[list[float]], float, float]:
    source, target = rects[source_name], rects[target_name]
    overlaps = projection_overlaps(source, target)
    dx = abs(source.center[0] - target.center[0])
    dy = abs(source.center[1] - target.center[1])
    if overlaps["y"] >= min_overlap and (dx >= dy or overlaps["x"] < min_overlap):
        low, high = max(source.y1, target.y1), min(source.y2, target.y2)
        y = (low + high) / 2.0
        if source.center[0] < target.center[0]:
            points = [[source.x2, y], [target.x1, y]]
        else:
            points = [[source.x1, y], [target.x2, y]]
        return "horizontal", points, _oclock(source, points[0]), _oclock(target, points[1])
    if overlaps["x"] >= min_overlap:
        low, high = max(source.x1, target.x1), min(source.x2, target.x2)
        x = (low + high) / 2.0
        if source.center[1] < target.center[1]:
            points = [[x, source.y2], [x, target.y1]]
        else:
            points = [[x, source.y1], [x, target.y2]]
        return "vertical", points, _oclock(source, points[0]), _oclock(target, points[1])
    raise ValueError(f"STATE_PROJECTION_INSUFFICIENT: {source_name}->{target_name}")


def plan_statechart(layout_input: dict, chart_path: str | None = None, min_overlap: float = 30.0) -> dict:
    report = audit_layout_input(layout_input)
    if not report["passed"]:
        raise ValueError(f"Invalid geometry-free layout input: {report['issues']}")
    chart = _select_chart(layout_input, chart_path)
    states = chart["states"]
    state_ids = {item["id"] for item in states}
    decomposition = chart["decomposition"]
    default = [item for item in chart["transitions"] if item.get("source") is None]
    if decomposition == "exclusive" and len(default) != 1:
        raise ValueError("An exclusive Chart requires exactly one default transition")
    if decomposition == "parallel" and default:
        raise ValueError("A parallel Chart allows no top-level default transition")
    ordinary = [item for item in chart["transitions"] if item.get("source") is not None]
    self_routes = [item for item in ordinary if item["source"] == item["target"]]
    if self_routes:
        names = ", ".join(item["id"] for item in self_routes)
        raise ValueError(f"Self transitions require an explicit self-loop strategy: {names}")
    if any(item["source"] not in state_ids or item["target"] not in state_ids for item in ordinary):
        raise ValueError("Transition refers to an unknown state")
    rects, strategy = _base_rects(states, ordinary)
    adjustments = []
    for _ in range(max(1, len(ordinary) * 2)):
        changed = False
        for transition in ordinary:
            source, target = transition["source"], transition["target"]
            overlaps = projection_overlaps(rects[source], rects[target])
            if max(overlaps.values()) >= min_overlap:
                continue
            result = ensure_transition_projection(rects, source, target, min_overlap=min_overlap, min_gap=30.0)
            if result.get("method") == "failed":
                raise ValueError(json.dumps({"transition": transition["id"], **result}, ensure_ascii=False))
            adjustments.append({"transition": transition["id"], **result})
            changed = changed or result.get("changed", False)
        if not changed:
            break
    blocks = [{"name": item["id"], "kind": "State", "rect": rects[item["id"]].as_list()} for item in states]
    routes = []
    for transition in ordinary:
        axis, points, source_oclock, destination_oclock = _route(rects, transition["source"], transition["target"], min_overlap)
        routes.append({
            "name": transition["id"], "kind": "transition", "source": transition["source"],
            "destination": transition["target"], "label": transition["label"],
            "label_position": [-0.55 * len(transition["label"]), 0], "priority": transition["priority"],
            "axis": axis, "source_oclock": source_oclock, "destination_oclock": destination_oclock,
            "points": points,
        })
    default_state = chart["default_state"]
    if decomposition == "exclusive":
        rect = rects[default_state]
        cx = rect.center[0]
        routes.append({
            "name": default[0]["id"], "kind": "transition", "source": "DEFAULT", "destination": default_state,
            "label": default[0]["label"], "label_position": [-0.55 * len(default[0]["label"]), 0],
            "priority": default[0]["priority"], "axis": "vertical", "source_oclock": None, "destination_oclock": 0,
            "points": [[cx, rect.y2 + 30.0], [cx, rect.y2]],
        })
    result = {
        "schema": "sysblock-statechart-layout/v1", "chart_path": chart["path"],
        "layout_input_sha256": report["canonical_sha256"], "layout_input_case_id": layout_input["case_id"],
        "chart_decomposition": decomposition, "default_state": default_state,
        "strategy": strategy, "geometry_adjustments": adjustments,
        "blocks": blocks, "routes": routes,
    }
    geometry_audit = audit_chart_layout(result)
    if not geometry_audit["passed"]:
        raise ValueError(json.dumps({
            "code": "STATECHART_LAYOUT_AUDIT_FAILED",
            "issues": geometry_audit["issues"],
        }, ensure_ascii=False))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    block = sub.add_parser("block")
    block.add_argument("input", type=Path)
    block.add_argument("--level")
    block.add_argument("--mode", choices=("full", "preconnect", "readback"))
    block.add_argument("--output", type=Path)
    chart = sub.add_parser("statechart")
    chart.add_argument("input", type=Path)
    chart.add_argument("--chart")
    chart.add_argument("--min-overlap", type=float, default=30.0)
    chart.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "block":
        from plan_sysblock_layout import plan as plan_block
        result = plan_block(read_json(args.input), args.level, args.mode)
    else:
        result = plan_statechart(read_json(args.input), args.chart, args.min_overlap)
    if args.output:
        write_json(result, args.output)
    else:
        sys.stdout.write(write_json(result))


if __name__ == "__main__":
    main()
