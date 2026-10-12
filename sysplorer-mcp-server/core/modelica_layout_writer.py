"""Token/span based Modelica layout writeback helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from core.modelica_graph_builder import Token, _tokenize_modelica, parse_modelica_34_source


@dataclass(frozen=True)
class SourceEdit:
    start: int
    end: int
    replacement: str
    kind: str


def _apply_edits(source: str, edits: Sequence[SourceEdit]) -> Tuple[str, List[Dict[str, Any]]]:
    diagnostics: List[Dict[str, Any]] = []
    ordered = sorted(edits, key=lambda e: e.start)
    for prev, cur in zip(ordered, ordered[1:]):
        if cur.start < prev.end:
            diagnostics.append(
                {
                    "severity": "error",
                    "code": "overlapping_writeback_edits",
                    "message": f"Overlapping edits: {prev.kind} [{prev.start},{prev.end}) and {cur.kind} [{cur.start},{cur.end})",
                    "offset": cur.start,
                }
            )
    if diagnostics:
        return source, diagnostics
    out = source
    for edit in sorted(edits, key=lambda e: e.start, reverse=True):
        out = out[: edit.start] + edit.replacement + out[edit.end :]
    return out, diagnostics


def _tokens_in_span(tokens: Sequence[Token], start: int, end: int) -> List[Token]:
    return [tok for tok in tokens if tok.start >= start and tok.end <= end and tok.kind != "EOF"]


def _matching_paren(tokens: Sequence[Token], open_idx: int) -> int:
    depth = 0
    for idx in range(open_idx, len(tokens)):
        value = tokens[idx].value
        if value == "(":
            depth += 1
        elif value == ")":
            depth -= 1
            if depth == 0:
                return idx
    return -1


def _find_named_call(tokens: Sequence[Token], name: str, start_idx: int = 0) -> Optional[Tuple[int, int, int]]:
    idx = start_idx
    while idx + 1 < len(tokens):
        if tokens[idx].value == name and tokens[idx + 1].value == "(":
            close_idx = _matching_paren(tokens, idx + 1)
            if close_idx >= 0:
                return idx, idx + 1, close_idx
        idx += 1
    return None


def _call_span(tokens: Sequence[Token], call: Tuple[int, int, int]) -> Tuple[int, int]:
    name_idx, _open_idx, close_idx = call
    return tokens[name_idx].start, tokens[close_idx].end


def _replace_or_insert_in_annotation(
    source: str,
    tokens: Sequence[Token],
    annotation_call: Tuple[int, int, int],
    child_call_name: str,
    new_child_text: str,
) -> SourceEdit:
    _name_idx, open_idx, close_idx = annotation_call
    inner_tokens = tokens[open_idx + 1 : close_idx]
    existing = _find_named_call(inner_tokens, child_call_name)
    if existing is not None:
        start, end = _call_span(inner_tokens, existing)
        if inner_tokens and inner_tokens[0].start == start and inner_tokens[-1].end == end:
            annotation_start = tokens[annotation_call[0]].start
            annotation_end = tokens[close_idx].end
            return SourceEdit(
                annotation_start,
                annotation_end,
                f"annotation({new_child_text})",
                f"replace_annotation_{child_call_name}",
            )
        return SourceEdit(start, end, new_child_text, f"replace_{child_call_name}")

    insert_pos = tokens[open_idx].end
    if inner_tokens:
        replacement = new_child_text + ", "
    else:
        replacement = new_child_text
    return SourceEdit(insert_pos, insert_pos, replacement, f"insert_{child_call_name}")


def _fmt_layout_num(value: float) -> str:
    try:
        return str(int(round(float(value))))
    except Exception:
        return "0"


def _component_placements(layout_graph: Dict[str, Any]) -> Dict[str, str]:
    placements: Dict[str, str] = {}
    children = layout_graph.get("children", [])
    if not isinstance(children, list):
        return placements
    for child in children:
        if not isinstance(child, dict):
            continue
        cid = str(child.get("id", "")).strip()
        if not cid:
            continue
        try:
            x = float(child.get("x", 0.0))
            y = float(child.get("y", 0.0))
            w = float(child.get("width", 120.0))
            h = float(child.get("height", 60.0))
        except Exception:
            continue
        # Style: origin at box center + relative half-extent (not absolute corners).
        hx = w / 2.0
        hy = h / 2.0
        ox = _fmt_layout_num(x + hx)
        oy = _fmt_layout_num(y + hy)
        ext = (
            "{{"
            f"-{_fmt_layout_num(hx)},-{_fmt_layout_num(hy)}"
            "},{"
            f"{_fmt_layout_num(hx)},{_fmt_layout_num(hy)}"
            "}}"
        )
        rot = child.get("rotation")
        if rot is not None:
            try:
                rot_val = int(rot)
            except (TypeError, ValueError):
                rot_val = 0
        else:
            rot_val = 0
        xf = f"origin={{{ox},{oy}}}, extent={ext}"
        if rot_val:
            placements[cid] = f"Placement(transformation({xf}, rotation={rot_val}))"
        else:
            placements[cid] = f"Placement(transformation({xf}))"
    return placements


def _trailing_semicolon(all_tokens: Sequence[Token], start: int, end: int) -> Optional[Token]:
    """Return the statement-ending ';' for a decl/connect span.

    Component/connect spans often exclude the terminator (parser strips it).
    Matrix row separators inside ``table=[0,0; 1,1]`` must not be treated as
    the statement terminator.
    """
    # Span already includes the terminator (rare but allowed).
    for tok in all_tokens:
        if tok.value == ";" and tok.start >= start and tok.end == end:
            return tok
    # Otherwise take the first ';' immediately after the span.
    for tok in all_tokens:
        if tok.start < end or tok.kind == "EOF":
            continue
        if tok.value == ";":
            return tok
        break
    return None


def _first_token_at_or_after(all_tokens: Sequence[Token], pos: int) -> Optional[Token]:
    for tok in all_tokens:
        if tok.kind == "EOF":
            continue
        if tok.start >= pos:
            return tok
    return None


def _insert_annotation_before_terminator(
    all_tokens: Sequence[Token],
    span_start: int,
    span_end: int,
    annotation_inner: str,
    kind_prefix: str,
) -> SourceEdit:
    """Insert ``annotation(...)`` without inventing a statement ``;``.

    A comma-separated component clause is one statement: ``Type a, b;``.
    Inserting ``annotation(...);`` after ``a`` produces ``Type a annotation(...);, b;``,
    which Sysplorer reports as ``unexpected ;``.
    """
    semicolon = _trailing_semicolon(all_tokens, span_start, span_end)
    if semicolon is not None:
        return SourceEdit(
            semicolon.start,
            semicolon.start,
            f" annotation({annotation_inner})",
            f"insert_{kind_prefix}",
        )
    nxt = _first_token_at_or_after(all_tokens, span_end)
    if nxt is not None and nxt.value == ",":
        return SourceEdit(
            span_end,
            span_end,
            f" annotation({annotation_inner})",
            f"insert_{kind_prefix}_before_comma",
        )
    return SourceEdit(
        span_end,
        span_end,
        f" annotation({annotation_inner});",
        f"insert_{kind_prefix}_no_semicolon",
    )


def _component_placement_edit(source: str, all_tokens: Sequence[Token], component: Any, placement_text: str) -> SourceEdit:
    stmt_tokens = _tokens_in_span(all_tokens, component.start, component.end)
    annotation_call = _find_named_call(stmt_tokens, "annotation")
    if annotation_call is not None:
        return _replace_or_insert_in_annotation(source, stmt_tokens, annotation_call, "Placement", placement_text)
    return _insert_annotation_before_terminator(
        all_tokens, component.start, component.end, placement_text, "component_placement"
    )


def _connect_key(lhs: str, rhs: str) -> frozenset[str]:
    return frozenset([str(lhs).strip(), str(rhs).strip()])


def _sections_to_points_str(sections: Sequence[Dict[str, Any]]) -> str:
    pts: List[Tuple[float, float]] = []
    for sec in sections:
        if not isinstance(sec, dict):
            continue
        sp = sec.get("startPoint") or {}
        ep = sec.get("endPoint") or {}
        if not pts and isinstance(sp, dict):
            pts.append((float(sp.get("x", 0.0)), float(sp.get("y", 0.0))))
        for bp in sec.get("bendPoints") or []:
            if isinstance(bp, dict):
                pts.append((float(bp.get("x", 0.0)), float(bp.get("y", 0.0))))
        if isinstance(ep, dict):
            pts.append((float(ep.get("x", 0.0)), float(ep.get("y", 0.0))))
    if len(pts) < 2:
        return ""
    return "{" + ",".join(f"{{{_fmt_layout_num(x)},{_fmt_layout_num(y)}}}" for x, y in pts) + "}"


def _edge_lines(layout_graph: Dict[str, Any]) -> Dict[frozenset[str], str]:
    lines: Dict[frozenset[str], str] = {}
    edges = layout_graph.get("edges", [])
    if not isinstance(edges, list):
        return lines
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        sources = edge.get("sources") or []
        targets = edge.get("targets") or []
        if not sources or not targets:
            continue
        sections = edge.get("sections") or []
        points = _sections_to_points_str(sections)
        if not points:
            continue
        color = edge.get("color")
        color_text = ""
        if isinstance(color, (list, tuple)) and len(color) >= 3:
            color_text = f", color={{{int(color[0])},{int(color[1])},{int(color[2])}}}"
        lines[_connect_key(str(sources[0]), str(targets[0]))] = f"Line(points={points}{color_text})"
    return lines


def _connect_line_edit(source: str, all_tokens: Sequence[Token], connect: Any, line_text: str) -> SourceEdit:
    stmt_tokens = _tokens_in_span(all_tokens, connect.start, connect.end)
    annotation_call = _find_named_call(stmt_tokens, "annotation")
    if annotation_call is not None:
        return _replace_or_insert_in_annotation(source, stmt_tokens, annotation_call, "Line", line_text)

    return _insert_annotation_before_terminator(
        all_tokens, connect.start, connect.end, line_text, "connect_line"
    )


def apply_layout_graph_to_modelica_code(
    modelica_code: str,
    layout_graph: Dict[str, Any],
    model_name: str = "",
) -> Tuple[str, Dict[str, Any]]:
    if not modelica_code or not isinstance(layout_graph, dict):
        return modelica_code, {"components_updated": 0, "connects_updated": 0, "diagnostics": []}

    target, parse_diagnostics = parse_modelica_34_source(modelica_code, model_name)
    if target is None:
        return modelica_code, {"components_updated": 0, "connects_updated": 0, "diagnostics": parse_diagnostics}

    tokens, token_diagnostics = _tokenize_modelica(modelica_code)
    placements = _component_placements(layout_graph)
    edits: List[SourceEdit] = []
    component_map = {comp.name: comp for comp in target.components}

    for comp_id, placement_text in placements.items():
        component = component_map.get(comp_id)
        if component is None:
            continue
        edits.append(_component_placement_edit(modelica_code, tokens, component, placement_text))

    edge_lines = _edge_lines(layout_graph)
    for connect in target.connects:
        line_text = edge_lines.get(_connect_key(connect.lhs, connect.rhs))
        if line_text is None:
            continue
        edits.append(_connect_line_edit(modelica_code, tokens, connect, line_text))

    patched, edit_diagnostics = _apply_edits(modelica_code, edits)
    diagnostics = list(parse_diagnostics)
    diagnostics.extend(
        {"severity": d.severity, "code": d.code, "message": d.message, "offset": d.offset}
        for d in token_diagnostics
    )
    diagnostics.extend(edit_diagnostics)
    component_count = sum(1 for e in edits if "component" in e.kind or "Placement" in e.kind or "placement" in e.kind.lower())
    connect_count = sum(1 for e in edits if "connect" in e.kind or "Line" in e.kind or "line" in e.kind.lower())
    return patched, {
        "components_updated": component_count,
        "connects_updated": connect_count,
        "diagnostics": diagnostics,
    }
