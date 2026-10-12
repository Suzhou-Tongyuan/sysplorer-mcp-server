#!/usr/bin/env python3
"""Small geometry audit helper for Sysblock-style block diagrams.

The helper is intentionally independent from Sysplorer. Use it to audit a
planned layout before creating blocks, or to check geometry read back from APIs.
"""

from __future__ import annotations


from lib.layout_core import Rect, nonduplicate_points, segments


AXIS_TOLERANCE = 1e-6


def is_transition_route(route: dict) -> bool:
    markers = [
        route.get("kind"),
        route.get("type"),
        route.get("route_type"),
        route.get("call"),
    ]
    return route.get("is_transition") is True or any(str(marker).lower() == "transition" for marker in markers)


def has_bezier_smoothing(route: dict) -> bool:
    smooth_markers = [
        route.get("smooth"),
        route.get("line_smooth"),
        route.get("line_style"),
        route.get("annotation_smooth"),
    ]
    return any("bezier" in str(marker).lower() for marker in smooth_markers if marker is not None)


def coordinates_equal(a: float, b: float) -> bool:
    return abs(a - b) <= AXIS_TOLERANCE


def points_equal(a: tuple[float, float], b: tuple[float, float]) -> bool:
    return coordinates_equal(a[0], b[0]) and coordinates_equal(a[1], b[1])


def is_axis_aligned(seg) -> bool:
    (x1, y1), (x2, y2) = seg
    return coordinates_equal(x1, x2) or coordinates_equal(y1, y2)


def segment_crosses_rect(seg, rect: Rect) -> bool:
    (x1, y1), (x2, y2) = seg
    if x1 == x2:
        x = x1
        lo, hi = sorted((y1, y2))
        return rect.x1 < x < rect.x2 and max(lo, rect.y1) < min(hi, rect.y2)
    if y1 == y2:
        y = y1
        lo, hi = sorted((x1, x2))
        return rect.y1 < y < rect.y2 and max(lo, rect.x1) < min(hi, rect.x2)
    return False


def axis_segments_cross(a, b) -> bool:
    if not (is_axis_aligned(a) and is_axis_aligned(b)):
        return False
    (ax1, ay1), (ax2, ay2) = a
    (bx1, by1), (bx2, by2) = b
    if ay1 == ay2 and bx1 == bx2:
        hx1, hx2 = sorted((ax1, ax2))
        vy1, vy2 = sorted((by1, by2))
        return hx1 < bx1 < hx2 and vy1 < ay1 < vy2
    if ax1 == ax2 and by1 == by2:
        vx1, vx2 = sorted((ay1, ay2))
        hx1, hx2 = sorted((bx1, bx2))
        return hx1 < ax1 < hx2 and vx1 < by1 < vx2
    return False


def axis_segments_overlap(a, b) -> bool:
    if not (is_axis_aligned(a) and is_axis_aligned(b)):
        return False
    (ax1, ay1), (ax2, ay2) = a
    (bx1, by1), (bx2, by2) = b
    if coordinates_equal(ay1, ay2) and coordinates_equal(by1, by2) and coordinates_equal(ay1, by1):
        a_lo, a_hi = sorted((ax1, ax2))
        b_lo, b_hi = sorted((bx1, bx2))
        return max(a_lo, b_lo) < min(a_hi, b_hi) - AXIS_TOLERANCE
    if coordinates_equal(ax1, ax2) and coordinates_equal(bx1, bx2) and coordinates_equal(ax1, bx1):
        a_lo, a_hi = sorted((ay1, ay2))
        b_lo, b_hi = sorted((by1, by2))
        return max(a_lo, b_lo) < min(a_hi, b_hi) - AXIS_TOLERANCE
    return False


def transition_label(route: dict) -> str | None:
    value = route.get("label")
    if value is None:
        value = route.get("label_string")
    if value is None:
        return None
    text = str(value)
    condition = route.get("condition", route.get("Condition"))
    if (
        is_default_transition(route)
        and text.strip().lower() == "[true]"
        and str(condition).strip().lower() == "true"
    ):
        return ""
    return text


def is_default_transition(route: dict) -> bool:
    source = route.get("source")
    return source is None or str(source).strip().upper() in ("", "DEFAULT")


def valid_label_position(value) -> bool:
    return (
        isinstance(value, (list, tuple))
        and len(value) == 2
        and all(isinstance(item, (int, float)) for item in value)
    )


def audit(layout: dict, min_gap: float = 30.0) -> dict:
    rects = [Rect(item["name"], *item["rect"]) for item in layout.get("blocks", [])]
    routes = layout.get("routes", [])
    issues = []

    for i, a in enumerate(rects):
        for b in rects[i + 1 :]:
            if a.overlaps(b):
                issues.append({"type": "block_overlap", "items": [a.name, b.name]})
            elif a.overlaps(b, margin=min_gap):
                issues.append({"type": "gap_below_minimum", "items": [a.name, b.name]})

    all_segments = []
    transition_multipoint_count = 0
    transition_bezier_risk_count = 0
    transition_bezier_visual_risk_count = 0
    transition_diagonal_two_point_count = 0
    transition_missing_label_count = 0
    transition_label_offset_issue_count = 0
    transition_label_relative_offset_issue_count = 0
    transition_label_absolute_position_issue_count = 0
    label_overlap_count = 0
    label_block_overlap_count = 0
    label_unrelated_route_intersection_count = 0
    transition_endpoints = []
    label_boxes = []
    for route in routes:
        points = nonduplicate_points(route["points"])
        route_segments = segments(points)
        bends = max(0, len(route_segments) - 1)
        non_axis = sum(1 for seg in route_segments if not is_axis_aligned(seg))
        is_transition = is_transition_route(route)
        bezier_smoothing = has_bezier_smoothing(route)
        if is_transition:
            label = transition_label(route)
            label_position = route.get("label_position")
            is_default = is_default_transition(route)
            if (
                label is None
                or (not is_default and not label.strip())
                or not valid_label_position(label_position)
            ):
                transition_missing_label_count += 1
                issues.append({
                    "type": "transition_label_evidence_missing",
                    "route": route["name"],
                    "rule": "Every transition requires a string label field and two-number label_position; ordinary transition labels must be nonempty.",
                })
            elif label.strip() and route_segments:
                expected_x = -0.55 * len(label)
                x_tolerance = max(2.0, 0.2 * len(label))
                label_x = float(label_position[0])
                label_y = float(label_position[1])
                straight_axis_aligned = (
                    len(points) == 2 and is_axis_aligned(route_segments[0])
                )
                if straight_axis_aligned:
                    if (
                        abs(label_x - expected_x) > x_tolerance
                        or abs(label_y) > 4.0
                    ):
                        transition_label_offset_issue_count += 1
                        transition_label_relative_offset_issue_count += 1
                        issues.append({
                            "type": "transition_label_relative_offset_out_of_range",
                            "route": route["name"],
                            "label": label,
                            "label_position": [label_x, label_y],
                            "expected_x": expected_x,
                            "x_tolerance": x_tolerance,
                            "y_tolerance": 4.0,
                            "rule": "A two-point horizontal/vertical transition uses a small relative LabelPosition offset.",
                        })
                    midpoint_x = (points[0][0] + points[1][0]) / 2.0
                    midpoint_y = (points[0][1] + points[1][1]) / 2.0
                    box_x = midpoint_x + label_x
                    box_y = midpoint_y + label_y
                else:
                    main_segment = max(
                        route_segments,
                        key=lambda seg: (
                            (seg[1][0] - seg[0][0]) ** 2
                            + (seg[1][1] - seg[0][1]) ** 2
                        ),
                    )
                    expected_absolute_x = (main_segment[0][0] + main_segment[1][0]) / 2.0
                    expected_absolute_y = (main_segment[0][1] + main_segment[1][1]) / 2.0
                    absolute_x_tolerance = max(4.0, 0.2 * len(label))
                    if (
                        abs(label_x - expected_absolute_x) > absolute_x_tolerance
                        or abs(label_y - expected_absolute_y) > 4.0
                    ):
                        transition_label_offset_issue_count += 1
                        transition_label_absolute_position_issue_count += 1
                        issues.append({
                            "type": "transition_label_absolute_position_out_of_range",
                            "route": route["name"],
                            "label": label,
                            "label_position": [label_x, label_y],
                            "expected_longest_segment_midpoint": [expected_absolute_x, expected_absolute_y],
                            "x_tolerance": absolute_x_tolerance,
                            "y_tolerance": 4.0,
                            "rule": "A non-orthogonal, curved, or intermediate-point transition uses an absolute Chart coordinate near its longest visible segment midpoint.",
                        })
                    box_x = label_x
                    box_y = label_y
                width = max(6.0, 1.1 * len(label))
                height = 8.0
                label_boxes.append((
                    route["name"],
                    Rect(
                        route["name"],
                        box_x,
                        box_y - height / 2.0,
                        box_x + width,
                        box_y + height / 2.0,
                    ),
                ))
        if is_transition and len(points) == 2 and non_axis:
            transition_diagonal_two_point_count += 1
            issues.append({
                "type": "transition_non_orthogonal",
                "route": route["name"],
                "point_count": len(points),
                "rule": "Every StateMachine transition must be a two-point horizontal or vertical line. Redesign state placement, hierarchy, or semantically valid topology before modeling.",
            })
            if bezier_smoothing:
                transition_bezier_visual_risk_count += 1
                issues.append({
                    "type": "transition_bezier_visual_risk",
                    "route": route["name"],
                    "point_count": len(points),
                    "smooth": route.get("smooth") or route.get("line_smooth") or route.get("line_style") or route.get("annotation_smooth"),
                    "rule": "A diagonal StateMachine transition with Bezier smoothing is non-orthogonal and can render as a curve; it always fails.",
                })
        elif non_axis:
            issues.append({"type": "non_axis_aligned_route", "route": route["name"], "count": non_axis})
        if bends and not is_transition:
            issues.append({"type": "route_bends", "route": route["name"], "count": bends})
        if is_transition and len(points) > 2:
            transition_multipoint_count += 1
            issues.append({
                "type": "transition_multipoint_route",
                "route": route["name"],
                "point_count": len(points),
                "rule": "StateMachine transition audit accepts only two-point horizontal or vertical lines.",
            })
        if is_transition and bezier_smoothing and len(points) > 2:
            transition_bezier_risk_count += 1
            issues.append({
                "type": "transition_bezier_risk",
                "route": route["name"],
                "point_count": len(points),
                "smooth": route.get("smooth") or route.get("line_smooth") or route.get("line_style") or route.get("annotation_smooth"),
            })
        for seg in route_segments:
            for rect in rects:
                if rect.name in (route.get("source"), route.get("destination")):
                    continue
                if segment_crosses_rect(seg, rect):
                    issues.append({"type": "route_crosses_block", "route": route["name"], "block": rect.name})
            all_segments.append((route["name"], seg))
        if is_transition and len(points) >= 2:
            transition_endpoints.extend([
                (route["name"], "source", (points[0][0], points[0][1])),
                (route["name"], "destination", (points[-1][0], points[-1][1])),
            ])

    for i, (name_a, seg_a) in enumerate(all_segments):
        for name_b, seg_b in all_segments[i + 1 :]:
            if name_a != name_b and axis_segments_cross(seg_a, seg_b):
                issues.append({"type": "route_crossing", "routes": [name_a, name_b]})
            if name_a != name_b and axis_segments_overlap(seg_a, seg_b):
                issues.append({"type": "route_collinear_overlap", "routes": [name_a, name_b]})

    for label_name, label_box in label_boxes:
        for rect in rects:
            if label_box.overlaps(rect):
                label_block_overlap_count += 1
                issues.append({
                    "type": "transition_label_overlaps_block",
                    "route": label_name,
                    "block": rect.name,
                })
        for route_name, segment in all_segments:
            if route_name != label_name and segment_crosses_rect(segment, label_box):
                label_unrelated_route_intersection_count += 1
                issues.append({
                    "type": "transition_label_intersects_unrelated_route",
                    "route": label_name,
                    "other_route": route_name,
                })

    for i, (name_a, box_a) in enumerate(label_boxes):
        for name_b, box_b in label_boxes[i + 1 :]:
            if box_a.overlaps(box_b):
                label_overlap_count += 1
                issues.append({
                    "type": "transition_label_overlap",
                    "routes": [name_a, name_b],
                })

    for i, (name_a, endpoint_a, point_a) in enumerate(transition_endpoints):
        for name_b, endpoint_b, point_b in transition_endpoints[i + 1 :]:
            if name_a != name_b and points_equal(point_a, point_b):
                issues.append({
                    "type": "transition_shared_endpoint",
                    "routes": [name_a, name_b],
                    "endpoints": [endpoint_a, endpoint_b],
                    "point": list(point_a),
                })

    if layout.get("chart") or "default_state" in layout or "chart_decomposition" in layout:
        decomposition = layout.get("chart_decomposition", "exclusive")
        default_state = layout.get("default_state")
        if not default_state:
            default_state = (
                layout.get("business_semantics", {}).get("default_state")
            )
        rect_by_name = {rect.name: rect for rect in rects}
        default_routes = [
            route for route in routes
            if is_transition_route(route) and is_default_transition(route)
        ]
        if decomposition == "parallel":
            if default_state is not None:
                issues.append({
                    "type": "parallel_chart_default_state_present",
                    "default_state": default_state,
                })
            if default_routes:
                issues.append({
                    "type": "parallel_chart_default_transition_present",
                    "count": len(default_routes),
                })
        elif decomposition != "exclusive":
            issues.append({
                "type": "chart_decomposition_invalid",
                "chart_decomposition": decomposition,
            })
        elif not default_state or default_state not in rect_by_name:
            issues.append({
                "type": "chart_default_state_evidence_missing",
                "default_state": default_state,
            })
        else:
            default_rect = rect_by_name[default_state]
            highest_top = max(rect.y2 for rect in rects)
            if default_rect.y2 < highest_top - AXIS_TOLERANCE:
                issues.append({
                    "type": "chart_default_state_not_in_highest_row",
                    "default_state": default_state,
                    "default_top": default_rect.y2,
                    "highest_top": highest_top,
                })
            matching_default_routes = [
                route for route in routes
                if is_transition_route(route)
                and is_default_transition(route)
                and route.get("destination") == default_state
            ]
            if len(default_routes) != 1 or len(matching_default_routes) != 1:
                issues.append({
                    "type": "chart_default_transition_count",
                    "default_state": default_state,
                    "count": len(default_routes),
                })
            else:
                default_points = nonduplicate_points(matching_default_routes[0]["points"])
                valid_default_geometry = (
                    len(default_points) == 2
                    and coordinates_equal(
                        default_points[0][0], default_points[1][0]
                    )
                    and default_points[0][1] > default_points[1][1]
                    and coordinates_equal(
                        default_points[1][1], default_rect.y2
                    )
                )
                if not valid_default_geometry:
                    issues.append({
                        "type": "chart_default_transition_not_vertical_from_above",
                        "route": matching_default_routes[0]["name"],
                        "points": default_points,
                    })

    return {
        "block_count": len(rects),
        "route_count": len(routes),
        "transition_multipoint_route_count": transition_multipoint_count,
        "transition_bezier_risk_count": transition_bezier_risk_count,
        "transition_bezier_visual_risk_count": transition_bezier_visual_risk_count,
        "transition_diagonal_two_point_count": transition_diagonal_two_point_count,
        "transition_missing_label_count": transition_missing_label_count,
        "transition_label_offset_issue_count": transition_label_offset_issue_count,
        "transition_label_relative_offset_issue_count": transition_label_relative_offset_issue_count,
        "transition_label_absolute_position_issue_count": transition_label_absolute_position_issue_count,
        "label_overlap_count": label_overlap_count,
        "label_block_overlap_count": label_block_overlap_count,
        "label_unrelated_route_intersection_count": label_unrelated_route_intersection_count,
        "issue_count": len(issues),
        "passed": len(issues) == 0,
        "issues": issues,
    }
