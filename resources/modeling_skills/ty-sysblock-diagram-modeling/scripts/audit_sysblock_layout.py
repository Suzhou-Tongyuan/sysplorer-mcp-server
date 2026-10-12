"""Audit planned or saved/readback Sysblock layout geometry."""

from __future__ import annotations

import json

from lib.layout_core import nonduplicate_points


EPSILON = 1e-9


def overlap(a: list[float], b: list[float]) -> bool:
    return (
        min(a[2], b[2]) - max(a[0], b[0]) > EPSILON
        and min(a[3], b[3]) - max(a[1], b[1]) > EPSILON
    )


def point_inside_rect(point: list[float], rect: list[float]) -> bool:
    return (
        rect[0] + EPSILON < point[0] < rect[2] - EPSILON
        and rect[1] + EPSILON < point[1] < rect[3] - EPSILON
    )


def segment_hits_rect(a: list[float], b: list[float], rect: list[float]) -> bool:
    if abs(a[0] - b[0]) < EPSILON:
        x = a[0]
        low, high = sorted((a[1], b[1]))
        return rect[0] + EPSILON < x < rect[2] - EPSILON and min(high, rect[3]) - max(low, rect[1]) > EPSILON
    if abs(a[1] - b[1]) < EPSILON:
        y = a[1]
        low, high = sorted((a[0], b[0]))
        return rect[1] + EPSILON < y < rect[3] - EPSILON and min(high, rect[2]) - max(low, rect[0]) > EPSILON
    return True


def orthogonal(a: list[float], b: list[float]) -> bool:
    return abs(a[0] - b[0]) < EPSILON or abs(a[1] - b[1]) < EPSILON


def interface_adjacent_horizontal(points: list[list[float]], source_side: bool) -> bool:
    """Return whether the first nonzero segment next to an interface is horizontal."""
    ordered = points if source_side else list(reversed(points))
    if len(ordered) < 2:
        return False
    anchor = ordered[0]
    for point in ordered[1:]:
        if abs(point[0] - anchor[0]) < EPSILON and abs(point[1] - anchor[1]) < EPSILON:
            continue
        return abs(point[1] - anchor[1]) < EPSILON
    return False


def normalized_kind(node: dict) -> str:
    return str(node.get("class", node.get("kind", ""))).split(".")[-1].lower()


def segment_intersection_kind(
    a1: list[float],
    a2: list[float],
    b1: list[float],
    b2: list[float],
) -> str:
    a_vertical = abs(a1[0] - a2[0]) < EPSILON
    b_vertical = abs(b1[0] - b2[0]) < EPSILON
    if a_vertical and b_vertical:
        if abs(a1[0] - b1[0]) >= EPSILON:
            return ""
        a_low, a_high = sorted((a1[1], a2[1]))
        b_low, b_high = sorted((b1[1], b2[1]))
        return "collinear_overlap" if min(a_high, b_high) - max(a_low, b_low) > EPSILON else ""
    if not a_vertical and not b_vertical:
        if abs(a1[1] - b1[1]) >= EPSILON:
            return ""
        a_low, a_high = sorted((a1[0], a2[0]))
        b_low, b_high = sorted((b1[0], b2[0]))
        return "collinear_overlap" if min(a_high, b_high) - max(a_low, b_low) > EPSILON else ""
    vertical_start, vertical_end = (a1, a2) if a_vertical else (b1, b2)
    horizontal_start, horizontal_end = (b1, b2) if a_vertical else (a1, a2)
    x = vertical_start[0]
    y = horizontal_start[1]
    v_low, v_high = sorted((vertical_start[1], vertical_end[1]))
    h_low, h_high = sorted((horizontal_start[0], horizontal_end[0]))
    if h_low - EPSILON <= x <= h_high + EPSILON and v_low - EPSILON <= y <= v_high + EPSILON:
        return "route_crossing"
    return ""


def normalize_port(node: dict, port: object) -> str:
    """Normalize local and component-qualified port names."""
    name = "" if port is None else str(port)
    prefix = f'{node["id"]}.'
    return name[len(prefix):] if name.startswith(prefix) else name


def port_exists(node: dict, port: object, direction: str) -> bool:
    """Resolve ordinary, qualified, and implicit boundary ports."""
    name = normalize_port(node, port)
    ports = {normalize_port(node, item) for item in node.get(direction, [])}
    if node.get("kind") == "Inport" and direction == "outputs":
        return name in ports | {"", "$boundary", "y", str(node["id"])}
    if node.get("kind") == "Outport" and direction == "inputs":
        return name in ports | {"", "$boundary", "u", str(node["id"])}
    return name in ports


def audit_connections(nodes: list[dict], edges: list[dict]) -> list[dict]:
    """Audit essential endpoint validity and explicitly declared connectivity."""
    issues = []
    node_map = {node["id"]: node for node in nodes}
    incident = {node_id: 0 for node_id in node_map}
    valid_outgoing = {node_id: 0 for node_id in node_map}
    valid_incoming_by_node = {node_id: 0 for node_id in node_map}
    valid_incoming_ports: dict[tuple[str, str], int] = {}

    for edge in edges:
        edge_id = edge.get("id")
        source_id = edge.get("source")
        target_id = edge.get("target")
        source_port = edge.get("source_port")
        target_port = edge.get("target_port")
        source = node_map.get(source_id)
        target = node_map.get(target_id)

        source_valid = source is not None
        target_valid = target is not None
        if source is None:
            issues.append(
                {"code": "unknown_source_component", "edge": edge_id, "component": source_id}
            )
        elif not port_exists(source, source_port, "outputs"):
            source_valid = False
            issues.append(
                {
                    "code": "unknown_source_port",
                    "edge": edge_id,
                    "component": source_id,
                    "port": source_port,
                }
            )

        if target is None:
            issues.append(
                {"code": "unknown_target_component", "edge": edge_id, "component": target_id}
            )
        elif not port_exists(target, target_port, "inputs"):
            target_valid = False
            issues.append(
                {
                    "code": "unknown_target_port",
                    "edge": edge_id,
                    "component": target_id,
                    "port": target_port,
                }
            )

        if source_valid and target_valid:
            incident[source_id] += 1
            incident[target_id] += 1
            valid_outgoing[source_id] += 1
            valid_incoming_by_node[target_id] += 1
            key = (target_id, normalize_port(target, target_port))
            valid_incoming_ports[key] = valid_incoming_ports.get(key, 0) + 1

    interface_kinds = {"Inport", "Outport"}
    ignored_kinds = {"Annotation", "Note"}
    for node in nodes:
        node_id = node["id"]
        kind = node.get("kind")
        if kind == "Inport" and valid_outgoing[node_id] == 0:
            issues.append({"code": "interface_unconnected", "node": node_id, "side": "Inport"})
        if kind == "Outport" and valid_incoming_by_node[node_id] == 0:
            issues.append({"code": "interface_unconnected", "node": node_id, "side": "Outport"})

        if node.get("required") is True and kind not in interface_kinds | ignored_kinds:
            if incident[node_id] == 0:
                issues.append({"code": "isolated_declared_required_component", "node": node_id})

        if kind in ignored_kinds:
            continue
        for port in node.get("required_inputs", []):
            normalized_port = normalize_port(node, port)
            if valid_incoming_ports.get((node_id, normalized_port), 0) == 0:
                issues.append(
                    {
                        "code": "unconnected_declared_required_input",
                        "node": node_id,
                        "port": port,
                    }
                )
    return issues


def audit(manifest: dict) -> dict:
    issues = []
    nodes = manifest.get("nodes", [])
    edges = manifest.get("edges", [])
    node_map = {node["id"]: node for node in nodes}
    profile = manifest.get("profile", {})
    mode = str(manifest.get("mode", "full"))
    preconnect = mode == "preconnect"
    if manifest.get("schema") != "sysblock-layout-manifest/v1":
        issues.append({"code": "schema", "message": "Unsupported or missing manifest schema"})
    contract = manifest.get("contract", {})
    if "placement_frozen_before_modeling" in contract and not contract["placement_frozen_before_modeling"]:
        issues.append({"code": "contract", "message": "Placement is not frozen"})
    if (
        not preconnect
        and "routes_frozen_before_modeling" in contract
        and not contract["routes_frozen_before_modeling"]
    ):
        issues.append({"code": "contract", "message": "Routes are not frozen"})
    connection_issues = audit_connections(nodes, edges)
    issues.extend(connection_issues)

    contains_chart = any(normalized_kind(node) == "chart" for node in nodes)
    for node in nodes:
        kind = normalized_kind(node)
        node_id = str(node.get("id", ""))
        class_name = str(node.get("class", ""))
        if class_name.startswith("SysplorerEmbeddedCoder.StateMachine.") and kind != "chart":
            issues.append({"code": "state_machine_block_not_in_allowlist", "node": node_id})
        timing_leaf = kind in {"clock", "digitalclock", "counter", "counterfreerunning", "counterlimited"}
        timing_marked = node.get("business_timing") is True or node.get("timing_role") is not None
        if contains_chart and (timing_marked or timing_leaf) and kind != "subsystem":
            issues.append(
                {
                    "code": "business_timing_not_encapsulated",
                    "node": node_id,
                    "rule": "Business timing must be inside Cond_*, Act_*, or shared Timing_*.",
                }
            )
        if node.get("feedback_path") is True and node.get("signal_flow") == "right_to_left":
            expected = node.get("expected_rotation")
            if expected != 180:
                issues.append({"code": "feedback_expected_rotation_invalid", "node": node_id})
            if not preconnect and node.get("rotation") != 180:
                issues.append(
                    {
                        "code": "feedback_rotation_mismatch",
                        "node": node_id,
                        "expected": 180,
                        "actual": node.get("rotation"),
                    }
                )
            frame = node.get("frame", [])
            if len(frame) == 4:
                for port, anchor in node.get("port_anchors", {}).get("inputs", {}).items():
                    if len(anchor) != 2 or abs(anchor[0] - frame[2]) >= EPSILON:
                        issues.append({"code": "feedback_input_not_on_right", "node": node_id, "port": port})
                for port, anchor in node.get("port_anchors", {}).get("outputs", {}).items():
                    if len(anchor) != 2 or abs(anchor[0] - frame[0]) >= EPSILON:
                        issues.append({"code": "feedback_output_not_on_left", "node": node_id, "port": port})

    for index, left in enumerate(nodes):
        for right in nodes[index + 1 :]:
            if overlap(left["frame"], right["frame"]):
                issues.append(
                    {
                        "code": "component_overlap",
                        "items": [left["id"], right["id"]],
                    }
                )
            if overlap(left["name_zone"], right["frame"]) or overlap(right["name_zone"], left["frame"]):
                issues.append(
                    {
                        "code": "name_component_overlap",
                        "items": [left["id"], right["id"]],
                    }
                )
            if overlap(left["name_zone"], right["name_zone"]):
                issues.append(
                    {
                        "code": "name_overlap",
                        "items": [left["id"], right["id"]],
                    }
                )

    for edge in edges:
        points = edge.get("points", [])
        if len(points) < 2:
            issues.append({"code": "route_missing", "edge": edge.get("id")})
            continue
        if preconnect:
            continue
        for a, b in zip(points, points[1:]):
            if not orthogonal(a, b):
                issues.append({"code": "non_orthogonal_route", "edge": edge["id"]})
                continue
            for node in nodes:
                if node["id"] in {edge["source"], edge["target"]}:
                    continue
                if segment_hits_rect(a, b, node["frame"]):
                    issues.append(
                        {
                            "code": "line_through_component",
                            "edge": edge["id"],
                            "node": node["id"],
                        }
                    )
                if segment_hits_rect(a, b, node["name_zone"]):
                    issues.append(
                        {
                            "code": "line_through_name",
                            "edge": edge["id"],
                            "node": node["id"],
                        }
                    )
                for zones in node.get("port_label_zones", {}).values():
                    for port_name, zone in zones.items():
                        if segment_hits_rect(a, b, zone):
                            issues.append(
                                {
                                    "code": "line_through_port_label",
                                    "edge": edge["id"],
                                    "node": node["id"],
                                    "port": port_name,
                                }
                            )
        source = node_map.get(edge.get("source"))
        target = node_map.get(edge.get("target"))
        if source is not None:
            source_anchor = source.get("port_anchors", {}).get("outputs", {}).get(
                edge.get("source_port")
            )
            if source_anchor is not None and not (
                abs(points[0][0] - source_anchor[0]) < EPSILON
                and abs(points[0][1] - source_anchor[1]) < EPSILON
            ):
                issues.append({"code": "source_anchor_mismatch", "edge": edge["id"]})
        if target is not None:
            target_anchor = target.get("port_anchors", {}).get("inputs", {}).get(
                edge.get("target_port")
            )
            if target_anchor is not None and not (
                abs(points[-1][0] - target_anchor[0]) < EPSILON
                and abs(points[-1][1] - target_anchor[1]) < EPSILON
            ):
                issues.append({"code": "target_anchor_mismatch", "edge": edge["id"]})
        if source is not None and target is not None:
            interface_clearance = profile.get(
                "interface_bend_clearance",
                profile.get("feedback_stub", 0),
            )
            if source.get("kind") == "Inport" and len(points) > 2:
                first_length = abs(points[1][0] - points[0][0]) + abs(points[1][1] - points[0][1])
                if first_length + EPSILON < interface_clearance:
                    issues.append(
                        {
                            "code": "interface_bend_too_close",
                            "edge": edge["id"],
                            "side": "Inport",
                            "actual": first_length,
                            "required": interface_clearance,
                        }
                    )
            if target.get("kind") == "Outport" and len(points) > 2:
                last_length = abs(points[-1][0] - points[-2][0]) + abs(points[-1][1] - points[-2][1])
                if last_length + EPSILON < interface_clearance:
                    issues.append(
                        {
                            "code": "interface_bend_too_close",
                            "edge": edge["id"],
                            "side": "Outport",
                            "actual": last_length,
                            "required": interface_clearance,
                        }
                    )

            direct_inport_to_chart = (
                source.get("kind") == "Inport"
                and normalized_kind(target) == "chart"
                and (
                    edge.get("one_to_one_interface") is True
                    or (
                        sum(other.get("source") == source.get("id") for other in edges) == 1
                        and sum(
                            other.get("target") == target.get("id")
                            and other.get("target_port") == edge.get("target_port")
                            for other in edges
                        ) == 1
                    )
                )
            )
            if direct_inport_to_chart and edge.get("blocking_region") is None:
                reduced = nonduplicate_points(points)
                if len(reduced) != 2 or abs(reduced[0][1] - reduced[1][1]) >= EPSILON:
                    issues.append(
                        {
                            "code": "one_to_one_inport_chart_not_horizontal",
                            "edge": edge.get("id"),
                        }
                    )

    route_xs = [] if preconnect else [
        point[0]
        for edge in edges
        for point in edge.get("points", [])
    ]
    inports = [node for node in nodes if node.get("kind") == "Inport"]
    outports = [node for node in nodes if node.get("kind") == "Outport"]
    for node in ([] if preconnect else inports):
        for edge in (edge for edge in edges if edge.get("source") == node["id"]):
            if not interface_adjacent_horizontal(edge.get("points", []), source_side=True):
                issues.append({"code": "interface_adjacent_segment_not_horizontal", "node": node["id"], "edge": edge.get("id")})
    for node in ([] if preconnect else outports):
        for edge in (edge for edge in edges if edge.get("target") == node["id"]):
            if not interface_adjacent_horizontal(edge.get("points", []), source_side=False):
                issues.append({"code": "interface_adjacent_segment_not_horizontal", "node": node["id"], "edge": edge.get("id")})
    if route_xs and inports:
        inport_boundary = min(node["frame"][0] for node in inports)
        if min(route_xs) < inport_boundary - EPSILON:
            issues.append(
                {
                    "code": "route_outside_inport_boundary",
                    "route_left": min(route_xs),
                    "inport_left": inport_boundary,
                }
            )
    if route_xs and outports:
        outport_boundary = max(node["frame"][2] for node in outports)
        if max(route_xs) > outport_boundary + EPSILON:
            issues.append(
                {
                    "code": "route_outside_outport_boundary",
                    "route_right": max(route_xs),
                    "outport_right": outport_boundary,
                }
            )

    ordinary_outgoing: dict[str, list[dict]] = {}
    incoming_by_target: dict[str, list[dict]] = {}
    for edge in edges:
        if edge.get("kind", "forward") != "feedback":
            ordinary_outgoing.setdefault(str(edge.get("source")), []).append(edge)
        target_id = edge.get("target")
        target = node_map.get(target_id)
        points = edge.get("points", [])
        target_port = edge.get("target_port")
        if (
            target is None
            or target_port not in target.get("inputs", [])
            or len(points) < 2
        ):
            continue
        incoming_by_target.setdefault(target_id, []).append(
            {
                "edge": edge.get("id"),
                "source": edge.get("source"),
                "target_port": target_port,
                "input_index": target["inputs"].index(target_port),
                "source_lane_y": points[0][1],
            }
        )

    for target_id, incoming in incoming_by_target.items():
        source_ids = [str(item["source"]) for item in incoming]
        target_ports = [str(item["target_port"]) for item in incoming]
        source_layers = [node_map.get(source_id, {}).get("layer") for source_id in source_ids]
        unambiguous = (
            len(incoming) >= 2
            and len(source_ids) == len(set(source_ids))
            and len(target_ports) == len(set(target_ports))
            and all(len(ordinary_outgoing.get(source_id, [])) == 1 for source_id in source_ids)
            and all(layer is not None for layer in source_layers)
            and len(set(source_layers)) == 1
        )
        if not unambiguous:
            continue
        ordered = sorted(incoming, key=lambda item: item["input_index"])
        for upper_index, upper in enumerate(ordered):
            for lower in ordered[upper_index + 1 :]:
                if upper["source_lane_y"] < lower["source_lane_y"] - EPSILON:
                    issues.append(
                        {
                            "code": "input_source_order_inversion",
                            "target": target_id,
                            "upper_input": upper["target_port"],
                            "upper_source": upper["source"],
                            "upper_source_lane_y": upper["source_lane_y"],
                            "lower_input": lower["target_port"],
                            "lower_source": lower["source"],
                            "lower_source_lane_y": lower["source_lane_y"],
                        }
                    )

    for index, left_edge in enumerate([] if preconnect else edges):
        for right_edge in edges[index + 1 :]:
            shared_component_endpoint = bool({
                left_edge.get("source"),
                left_edge.get("target"),
            } & {
                right_edge.get("source"),
                right_edge.get("target"),
            })
            same_source = (
                left_edge.get("source"),
                left_edge.get("source_port"),
            ) == (
                right_edge.get("source"),
                right_edge.get("source_port"),
            )
            for left_a, left_b in zip(left_edge.get("points", []), left_edge.get("points", [])[1:]):
                for right_a, right_b in zip(right_edge.get("points", []), right_edge.get("points", [])[1:]):
                    kind = segment_intersection_kind(left_a, left_b, right_a, right_b)
                    if kind == "collinear_overlap" and not same_source:
                        issues.append(
                            {
                                "code": "different_source_collinear_overlap",
                                "edges": [left_edge["id"], right_edge["id"]],
                            }
                        )
                    elif kind == "route_crossing" and not shared_component_endpoint:
                        issues.append(
                            {
                                "code": kind,
                                "edges": [left_edge["id"], right_edge["id"]],
                            }
                        )

    if profile.get("horizontal_gap", 0) > profile.get("max_horizontal_gap", float("inf")):
        issues.append({"code": "excess_horizontal_gap"})
    canvas = manifest.get("canvas")
    if canvas and nodes:
        content_left = min(node["frame"][0] for node in nodes)
        content_right = max(node["frame"][2] for node in nodes)
        max_margin = profile.get("max_outer_margin", float("inf"))
        if content_left - canvas[0] > max_margin + profile.get("feedback_stub", 0) + profile.get("routing_lane_pitch", 0) * max(1, sum(edge.get("kind") == "feedback" for edge in edges)):
            issues.append({"code": "excess_left_margin"})
        if canvas[2] - content_right > max_margin + profile.get("feedback_stub", 0) + profile.get("routing_lane_pitch", 0) * max(1, sum(edge.get("kind") == "feedback" for edge in edges)):
            issues.append({"code": "excess_right_margin"})

    unique_issues = []
    seen = set()
    for issue in issues:
        key = json.dumps(issue, ensure_ascii=False, sort_keys=True)
        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)
    connection_issue_counts = {
        "invalid_endpoint": sum(
            issue["code"] in {
                "unknown_source_component",
                "unknown_target_component",
                "unknown_source_port",
                "unknown_target_port",
            }
            for issue in connection_issues
        ),
        "unconnected_interface": sum(
            issue["code"] == "interface_unconnected"
            for issue in connection_issues
        ),
        "unconnected_declared_required_input": sum(
            issue["code"] == "unconnected_declared_required_input"
            for issue in connection_issues
        ),
        "isolated_declared_required_component": sum(
            issue["code"] == "isolated_declared_required_component"
            for issue in connection_issues
        ),
    }
    return {
        "passed": not unique_issues,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "connection_integrity": {
            "executed": True,
            "level": manifest.get("level", manifest.get("model")),
            "edge_count": len(edges),
            "endpoint_count": len(edges) * 2,
            "issue_counts": connection_issue_counts,
            "passed": not connection_issues,
        },
        "issue_count": len(unique_issues),
        "issues": unique_issues,
    }
