"""Create a deterministic one-pass Sysblock layout manifest.

Input JSON:

{
  "profile": { ... optional calibrated geometry ... },
  "nodes": [
    {
      "id": "logic",
      "kind": "LogicalOperator",
      "name": "logic",
      "inputs": ["u1", "u2"],
      "outputs": ["y"],
      "layer": 1,
      "row": 0
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "in",
      "source_port": "y",
      "target": "logic",
      "target_port": "u1",
      "kind": "forward"
    }
  ]
}

The planner never edits a model.  In the default ``full`` mode it freezes
component sizes, label protection zones, port anchors, and orthogonal route
points.  In ``preconnect`` mode it freezes topology and checks spatial
feasibility without making ordinary route bends authoritative.  Use explicit
``layer`` and ``row`` for business-significant placement.  When layers are
omitted, the planner derives a deterministic longest-path layering from
non-feedback edges; cycles must be marked as ``kind=feedback``.
"""

from __future__ import annotations

from collections import defaultdict

from audit_layout_input import audit as audit_layout_input


DEFAULT_PROFILE = {
    "default_block_width": 20.0,
    "default_block_height": 20.0,
    "minimum_subsystem_width": 90.0,
    "minimum_subsystem_height": 60.0,
    "port_pitch": 24.0,
    "character_width": 7.0,
    "name_band_height": 18.0,
    "horizontal_margin": 12.0,
    "vertical_margin": 12.0,
    "horizontal_gap": 44.0,
    "vertical_gap": 28.0,
    "routing_lane_pitch": 12.0,
    "feedback_stub": 16.0,
    "outer_margin": 20.0,
    "max_outer_margin": 24.0,
    "max_horizontal_gap": 64.0,
}

RESIZABLE_KINDS = {
    "SubSystem",
    "Chart",
    "Mux",
    "DeMux",
    "VectorConcatenate",
    "BusCreator",
    "BusSelector",
    "Switch",
    "MultiportSwitch",
}


def text_width(text: str, profile: dict) -> float:
    return max(profile["default_block_width"], len(str(text)) * profile["character_width"])


def node_size(node: dict, profile: dict) -> tuple[float, float]:
    if "width" in node and "height" in node:
        return float(node["width"]), float(node["height"])
    kind = str(node.get("kind", "Block"))
    if kind not in RESIZABLE_KINDS:
        return profile["default_block_width"], profile["default_block_height"]
    inputs = [str(item) for item in node.get("inputs", [])]
    outputs = [str(item) for item in node.get("outputs", [])]
    port_count = max(len(inputs), len(outputs), 1)
    effective_port_pitch = max(
        profile["port_pitch"],
        profile["default_block_height"] + profile["name_band_height"] + 4.0,
    )
    longest_port = max([len(item) for item in inputs + outputs] or [0])
    name = str(node.get("name", node["id"]))
    width = max(
        profile["minimum_subsystem_width"],
        text_width(name, profile) + 2 * profile["horizontal_margin"],
        longest_port * profile["character_width"] + 2 * profile["horizontal_margin"],
    )
    height = max(
        profile["minimum_subsystem_height"],
        2 * profile["vertical_margin"] + port_count * effective_port_pitch,
    )
    return width, height


def derive_layers(nodes: list[dict], edges: list[dict]) -> dict[str, int]:
    node_ids = {node["id"] for node in nodes}
    outgoing: dict[str, list[str]] = defaultdict(list)
    indegree = {node_id: 0 for node_id in node_ids}
    for edge in edges:
        if edge.get("kind", "forward") == "feedback":
            continue
        source = edge["source"]
        target = edge["target"]
        if source not in node_ids or target not in node_ids:
            raise ValueError(f"Unknown edge endpoint: {source} -> {target}")
        outgoing[source].append(target)
        indegree[target] += 1
    queue = sorted(node_id for node_id, degree in indegree.items() if degree == 0)
    layers = {
        node["id"]: int(node["layer"])
        for node in nodes
        if node.get("layer") is not None
    }
    visited = []
    while queue:
        source = queue.pop(0)
        visited.append(source)
        layers.setdefault(source, 0)
        for target in sorted(outgoing[source]):
            if target not in layers:
                layers[target] = max(layers.get(target, 0), layers[source] + 1)
            elif layers[target] <= layers[source]:
                raise ValueError(
                    f"Explicit layer violates forward flow: {source} -> {target}"
                )
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
                queue.sort()
    if len(visited) != len(nodes):
        raise ValueError("Forward graph contains a cycle; mark feedback edges explicitly")
    return layers


def port_y(node: dict, direction: str, port_name: str) -> float:
    names = node["inputs"] if direction == "input" else node["outputs"]
    if port_name not in names:
        raise ValueError(f"{node['id']}: unknown {direction} port {port_name}")
    index = names.index(port_name) + 1
    count = len(names)
    return node["y"] + node["height"] / 2 - (index - 0.5) * node["height"] / count


def unambiguous_fanin_orders(
    nodes: list[dict], edges: list[dict], layers: dict[str, int]
) -> dict[int, list[list[str]]]:
    node_map = {node["id"]: node for node in nodes}
    outgoing: dict[str, list[dict]] = defaultdict(list)
    incoming: dict[str, list[dict]] = defaultdict(list)
    for edge in edges:
        if edge.get("kind", "forward") == "feedback":
            continue
        outgoing[edge["source"]].append(edge)
        incoming[edge["target"]].append(edge)

    groups: dict[int, list[list[str]]] = defaultdict(list)
    for target_id in sorted(incoming):
        target = node_map.get(target_id)
        target_edges = incoming[target_id]
        if target is None or len(target_edges) < 2:
            continue
        source_ids = [edge["source"] for edge in target_edges]
        target_ports = [str(edge["target_port"]) for edge in target_edges]
        source_layers = [layers.get(source_id) for source_id in source_ids]
        if (
            len(source_ids) != len(set(source_ids))
            or len(target_ports) != len(set(target_ports))
            or any(port not in target["inputs"] for port in target_ports)
            or any(len(outgoing[source_id]) != 1 for source_id in source_ids)
            or any(layer is None for layer in source_layers)
            or len(set(source_layers)) != 1
        ):
            continue
        ordered = sorted(
            target_edges,
            key=lambda edge: target["inputs"].index(str(edge["target_port"])),
        )
        groups[int(source_layers[0])].append([edge["source"] for edge in ordered])
    return groups


def _level_spec(layout_input: dict, level_path: str | None = None) -> tuple[dict, str, str]:
    report = audit_layout_input(layout_input)
    if not report["passed"]:
        raise ValueError(f"Invalid geometry-free layout input: {report['issues']}")
    levels = layout_input.get("levels", [])
    if level_path is None:
        if len(levels) != 1:
            raise ValueError("--level is required when a layout input has zero or multiple levels")
        level = levels[0]
    else:
        matches = [item for item in levels if item.get("path") == level_path]
        if len(matches) != 1:
            raise ValueError(f"Unknown or duplicate level: {level_path}")
        level = matches[0]
    feedback_edge_ids = {
        edge_id
        for path in level.get("feedback_paths", [])
        for edge_id in path.get("edge_ids", [])
    }
    feedback_node_ids = {
        node_id
        for path in level.get("feedback_paths", [])
        for node_id in path.get("member_node_ids", [])
    }
    nodes = []
    for raw in level.get("nodes", []):
        node = dict(raw)
        if node["id"] in feedback_node_ids:
            node.update({"feedback_path": True, "signal_flow": "right_to_left", "expected_rotation": 180})
        nodes.append(node)
    edges = []
    for raw in level.get("edges", []):
        edge = dict(raw)
        edge["kind"] = "feedback" if edge["id"] in feedback_edge_ids else "forward"
        edges.append(edge)
    return (
        {"mode": "full", "nodes": nodes, "edges": edges},
        str(level["path"]),
        report["canonical_sha256"],
    )


def plan(spec: dict, level_path: str | None = None, mode_override: str | None = None) -> dict:
    input_case_id = None
    input_hash = None
    level_name = spec.get("level")
    if spec.get("schema") == "sysblock-layout-input/v1":
        input_case_id = spec.get("case_id")
        spec, level_name, input_hash = _level_spec(spec, level_path)
    if mode_override is not None:
        spec["mode"] = mode_override
    mode = str(spec.get("mode", "full"))
    if mode not in {"full", "preconnect", "readback"}:
        raise ValueError(f"Unsupported layout mode: {mode}")
    profile = dict(DEFAULT_PROFILE)
    profile.update(spec.get("profile", {}))
    nodes = [dict(node) for node in spec.get("nodes", [])]
    edges = [dict(edge) for edge in spec.get("edges", [])]
    if not nodes:
        raise ValueError("nodes must not be empty")
    ids = [str(node["id"]) for node in nodes]
    if len(ids) != len(set(ids)):
        raise ValueError("node ids must be unique")
    for node in nodes:
        node["id"] = str(node["id"])
        node["name"] = str(node.get("name", node["id"]))
        node["inputs"] = [str(item) for item in node.get("inputs", [])]
        node["outputs"] = [str(item) for item in node.get("outputs", [])]
        if node.get("feedback_path") is True and node.get("signal_flow") == "right_to_left":
            node.setdefault("expected_rotation", 180)
        node["width"], node["height"] = node_size(node, profile)

    layers = derive_layers(nodes, edges)
    next_feedback_row = 1 + max(
        [int(node.get("row", 0)) for node in nodes if node.get("feedback_path") is not True] or [0]
    )
    for node in sorted(nodes, key=lambda item: item["id"]):
        if node.get("feedback_path") is True and node.get("layer") is None:
            neighbor_layers = []
            for edge in edges:
                if edge["source"] == node["id"] and edge["target"] in layers:
                    neighbor_layers.append(layers[edge["target"]])
                elif edge["target"] == node["id"] and edge["source"] in layers:
                    neighbor_layers.append(layers[edge["source"]])
            layers[node["id"]] = round(sum(neighbor_layers) / len(neighbor_layers)) if neighbor_layers else max(layers.values(), default=0)
            node.setdefault("row", next_feedback_row)
            next_feedback_row += 1
    node_lookup = {node["id"]: node for node in nodes}
    for node in nodes:
        if node.get("row") is not None:
            continue
        kind = str(node.get("kind", "")).lower()
        if kind == "inport":
            candidates = []
            for edge in edges:
                if edge["source"] != node["id"]:
                    continue
                target = node_lookup[edge["target"]]
                if edge["target_port"] in target["inputs"]:
                    candidates.append(target["inputs"].index(edge["target_port"]))
            if candidates:
                node["row"] = min(candidates)
        elif kind == "outport":
            candidates = []
            for edge in edges:
                if edge["target"] != node["id"]:
                    continue
                source = node_lookup[edge["source"]]
                if edge["source_port"] in source["outputs"]:
                    candidates.append(source["outputs"].index(edge["source_port"]))
            if candidates:
                node["row"] = min(candidates)
    by_layer: dict[int, list[dict]] = defaultdict(list)
    for node in nodes:
        node["layer"] = layers[node["id"]]
        by_layer[node["layer"]].append(node)
    fanin_orders = unambiguous_fanin_orders(nodes, edges, layers)
    for layer, layer_nodes in by_layer.items():
        layer_nodes.sort(
            key=lambda item: (
                int(item.get("row", 10**6)),
                int(item.get("order", 0)),
                item["id"],
            )
        )
        for ordered_ids in fanin_orders.get(layer, []):
            positions = sorted(
                index for index, node in enumerate(layer_nodes) if node["id"] in ordered_ids
            )
            ordered_nodes = [node_lookup[node_id] for node_id in ordered_ids]
            for position, node in zip(positions, ordered_nodes):
                layer_nodes[position] = node
        used_rows = set()
        next_row = 0
        for node in layer_nodes:
            if node.get("row") is None:
                while next_row in used_rows:
                    next_row += 1
                node["row"] = next_row
            node["row"] = int(node["row"])
            if node["row"] in used_rows:
                raise ValueError(
                    f"Layer {node['layer']} has duplicate row {node['row']}"
                )
            used_rows.add(node["row"])

    layer_width = {
        layer: max(node["width"] for node in layer_nodes)
        for layer, layer_nodes in by_layer.items()
    }
    layer_centers = {}
    previous_right = 0.0
    for index, layer in enumerate(sorted(by_layer)):
        width = layer_width[layer]
        center = width / 2 if index == 0 else previous_right + profile["horizontal_gap"] + width / 2
        layer_centers[layer] = center
        previous_right = center + width / 2
    for layer, layer_nodes in by_layer.items():
        row_pitch = (
            max(node["height"] for node in layer_nodes)
            + profile["name_band_height"]
            + profile["vertical_gap"]
        )
        rows = [node["row"] for node in layer_nodes]
        row_center = (min(rows) + max(rows)) / 2
        for node in layer_nodes:
            node["x"] = layer_centers[layer]
            node["y"] = -(node["row"] - row_center) * row_pitch
    node_map = {node["id"]: node for node in nodes}
    for edge in edges:
        source = node_map[edge["source"]]
        target = node_map[edge["target"]]
        if str(source.get("kind", "")).lower() == "inport":
            source["y"] = port_y(target, "input", str(edge["target_port"]))
        if str(target.get("kind", "")).lower() == "outport":
            target["y"] = port_y(source, "output", str(edge["source_port"]))
    for node in nodes:
        half_width = node["width"] / 2
        half_height = node["height"] / 2
        node["frame"] = [
            node["x"] - half_width,
            node["y"] - half_height,
            node["x"] + half_width,
            node["y"] + half_height,
        ]
        label_width = text_width(node["name"], profile)
        node["name_zone"] = [
            node["x"] - label_width / 2,
            node["y"] - half_height - profile["name_band_height"],
            node["x"] + label_width / 2,
            node["y"] - half_height,
        ]
        right_to_left = (
            node.get("feedback_path") is True
            and node.get("signal_flow") == "right_to_left"
            and float(node.get("expected_rotation", 180)) == 180
        )
        input_x = node["x"] + half_width if right_to_left else node["x"] - half_width
        output_x = node["x"] - half_width if right_to_left else node["x"] + half_width
        node["port_anchors"] = {
            "inputs": {
                name: [input_x, port_y(node, "input", name)]
                for name in node["inputs"]
            },
            "outputs": {
                name: [output_x, port_y(node, "output", name)]
                for name in node["outputs"]
            },
        }
        if right_to_left:
            node["rotation"] = 180
        label_half_height = profile["name_band_height"] / 2
        def port_label_zone(name: str, anchor: list[float], side: str) -> list[float]:
            width = text_width(name, profile) + profile["horizontal_margin"]
            if side == "left":
                return [
                    node["x"] - half_width,
                    anchor[1] - label_half_height,
                    min(node["x"] + half_width, node["x"] - half_width + width),
                    anchor[1] + label_half_height,
                ]
            return [
                max(node["x"] - half_width, node["x"] + half_width - width),
                anchor[1] - label_half_height,
                node["x"] + half_width,
                anchor[1] + label_half_height,
            ]

        input_side = "right" if right_to_left else "left"
        output_side = "left" if right_to_left else "right"
        node["port_label_zones"] = {
            "inputs": {
                name: port_label_zone(name, anchor, input_side)
                for name, anchor in node["port_anchors"]["inputs"].items()
            },
            "outputs": {
                name: port_label_zone(name, anchor, output_side)
                for name, anchor in node["port_anchors"]["outputs"].items()
            },
        }

    node_map = {node["id"]: node for node in nodes}
    min_x = min(node["frame"][0] for node in nodes)
    max_x = max(node["frame"][2] for node in nodes)
    min_y = min(node["name_zone"][1] for node in nodes)
    max_y = max(node["frame"][3] for node in nodes)
    feedback_counts = {"top": 0, "bottom": 0}
    planned_edges = []
    for index, edge in enumerate(edges):
        source = node_map[edge["source"]]
        target = node_map[edge["target"]]
        source_port = str(edge.get("source_port", source["outputs"][0]))
        target_port = str(edge.get("target_port", target["inputs"][0]))
        start = source["port_anchors"]["outputs"][source_port]
        end = target["port_anchors"]["inputs"][target_port]
        kind = edge.get("kind", "forward")
        if mode == "preconnect":
            points = [start, end]
        elif kind == "feedback":
            side = edge.get("feedback_side", "bottom")
            if side not in feedback_counts:
                raise ValueError(f"Unsupported feedback_side: {side}")
            lane_index = feedback_counts[side]
            feedback_counts[side] += 1
            delta = profile["outer_margin"] + (lane_index + 1) * profile["routing_lane_pitch"]
            lane_y = max_y + delta if side == "top" else min_y - delta
            source_rtl = source.get("feedback_path") is True and source.get("signal_flow") == "right_to_left"
            target_rtl = target.get("feedback_path") is True and target.get("signal_flow") == "right_to_left"
            source_stub_x = start[0] + (-profile["feedback_stub"] if source_rtl else profile["feedback_stub"])
            target_stub_x = end[0] + (profile["feedback_stub"] if target_rtl else -profile["feedback_stub"])
            points = [
                start,
                [source_stub_x, start[1]],
                [source_stub_x, lane_y],
                [target_stub_x, lane_y],
                [target_stub_x, end[1]],
                end,
            ]
        elif abs(start[1] - end[1]) < 1e-9:
            points = [start, end]
        else:
            lane_x = (start[0] + end[0]) / 2
            points = [start, [lane_x, start[1]], [lane_x, end[1]], end]
        planned_edges.append(
            {
                "id": str(edge.get("id", f"edge_{index + 1}")),
                "source": source["id"],
                "source_port": source_port,
                "target": target["id"],
                "target_port": target_port,
                "kind": kind,
                "one_to_one_interface": bool(edge.get("one_to_one_interface", False)),
                "points": points,
            }
        )

    all_points = [point for edge in planned_edges for point in edge["points"]]
    route_min_x = min([point[0] for point in all_points] or [min_x])
    route_max_x = max([point[0] for point in all_points] or [max_x])
    route_min_y = min([point[1] for point in all_points] or [min_y])
    route_max_y = max([point[1] for point in all_points] or [max_y])
    margin = profile["outer_margin"]
    canvas = [
        min(min_x, route_min_x) - margin,
        min(min_y, route_min_y) - margin,
        max(max_x, route_max_x) + margin,
        max(max_y, route_max_y) + margin,
    ]
    result = {
        "schema": "sysblock-layout-manifest/v1",
        "mode": mode,
        "profile": profile,
        "nodes": nodes,
        "edges": planned_edges,
        "canvas": canvas,
        "contract": {
            "placement_frozen_before_modeling": True,
            "topology_frozen_before_modeling": True,
            "space_feasibility_checked": True,
            "routes_frozen_before_modeling": mode != "preconnect",
            "ordinary_route_points_authoritative": mode != "preconnect",
            "topology_mutation_allowed": False,
        },
    }
    if level_name:
        result["level"] = level_name
    if input_hash:
        result["layout_input_sha256"] = input_hash
        result["layout_input_case_id"] = input_case_id
    return result
