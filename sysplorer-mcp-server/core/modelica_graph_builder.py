"""Modelica 3.4 source to Smart Layout graph extraction.

This module is intentionally a source-structure parser, not a Modelica
compiler.  It follows the Modelica 3.4 concrete-syntax shape closely enough
for diagram extraction: classes, component clauses, connect-equations and the
common Placement/Line annotations used by Sysplorer diagrams.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Literal, Optional, Sequence, Tuple


_CLASS_KINDS = {
    "class",
    "model",
    "operator",
    "block",
    "connector",
    "type",
    "package",
    "function",
    "record",
}

_CLASS_KIND_FOLLOWERS = _CLASS_KINDS | {"record"}  # "operator record" is normalized by the parser.

# Prefixes that may precede a nested class / short class definition.
_CLASS_PREFIXES = {"encapsulated", "partial", "replaceable", "redeclare", "final"}

_DECL_PREFIXES = {
    "redeclare",
    "final",
    "inner",
    "outer",
    "replaceable",
    "parameter",
    "constant",
    "discrete",
    "flow",
    "stream",
    "input",
    "output",
    "each",
}

_SKIP_DECL_PREFIXES = {"parameter", "constant", "discrete"}
_BUILTIN_TYPES = {"Real", "Integer", "Boolean", "String"}
_SECTION_KEYWORDS = {"public", "protected", "equation", "algorithm", "initial"}


@dataclass
class Token:
    kind: str
    value: str
    start: int
    end: int
    line: int
    column: int


@dataclass
class Diagnostic:
    severity: Literal["info", "warning", "error"]
    code: str
    message: str
    offset: int = 0


@dataclass
class ComponentDecl:
    name: str
    type_name: str
    prefixes: List[str]
    visibility: str
    statement_text: str
    annotation_text: str = ""
    start: int = 0
    end: int = 0


@dataclass
class ConnectEq:
    lhs: str
    rhs: str
    statement_text: str
    annotation_text: str = ""
    start: int = 0
    end: int = 0


@dataclass
class ClassNode:
    kind: str
    name: str
    full_name: str
    body_tokens: List[Token]
    components: List[ComponentDecl] = field(default_factory=list)
    connects: List[ConnectEq] = field(default_factory=list)
    children: List["ClassNode"] = field(default_factory=list)
    start: int = 0
    end: int = 0


@dataclass
class GraphBuildResult:
    ok: bool
    graph: Dict[str, Any] = field(default_factory=dict)
    diagnostics: List[Dict[str, Any]] = field(default_factory=list)
    error: str = ""
    source: str = "modelica_34_ast"


def _diag_dict(d: Diagnostic) -> Dict[str, Any]:
    return {"severity": d.severity, "code": d.code, "message": d.message, "offset": d.offset}


def _is_ident(tok: Optional[Token]) -> bool:
    return bool(tok and tok.kind in {"IDENT", "Q_IDENT"} and tok.value)


def _unquote_ident(value: str) -> str:
    if len(value) >= 2 and value[0] == "'" and value[-1] == "'":
        return value[1:-1].replace("\\'", "'")
    return value


def _tokenize_modelica(source: str) -> Tuple[List[Token], List[Diagnostic]]:
    """Tokenize a Modelica source file while respecting strings and comments."""
    tokens: List[Token] = []
    diags: List[Diagnostic] = []
    i = 0
    line = 1
    col = 1
    n = len(source)

    def advance_char() -> str:
        nonlocal i, line, col
        ch = source[i]
        i += 1
        if ch == "\n":
            line += 1
            col = 1
        else:
            col += 1
        return ch

    def add(kind: str, value: str, start: int, end: int, sline: int, scol: int) -> None:
        tokens.append(Token(kind, value, start, end, sline, scol))

    while i < n:
        ch = source[i]
        if ch.isspace():
            advance_char()
            continue
        s, sl, sc = i, line, col
        if ch == "/" and i + 1 < n and source[i + 1] == "/":
            while i < n and source[i] != "\n":
                advance_char()
            continue
        if ch == "/" and i + 1 < n and source[i + 1] == "*":
            advance_char()
            advance_char()
            closed = False
            while i < n:
                if source[i] == "*" and i + 1 < n and source[i + 1] == "/":
                    advance_char()
                    advance_char()
                    closed = True
                    break
                advance_char()
            if not closed:
                diags.append(Diagnostic("error", "unterminated_block_comment", "Unterminated block comment", s))
            continue
        if ch == '"':
            advance_char()
            escaped = False
            while i < n:
                c = advance_char()
                if escaped:
                    escaped = False
                    continue
                if c == "\\":
                    escaped = True
                    continue
                if c == '"':
                    break
            else:
                diags.append(Diagnostic("error", "unterminated_string", "Unterminated string literal", s))
            add("STRING", source[s:i], s, i, sl, sc)
            continue
        if ch == "'":
            advance_char()
            escaped = False
            while i < n:
                c = advance_char()
                if escaped:
                    escaped = False
                    continue
                if c == "\\":
                    escaped = True
                    continue
                if c == "'":
                    break
            else:
                diags.append(Diagnostic("error", "unterminated_q_ident", "Unterminated quoted identifier", s))
            add("Q_IDENT", source[s:i], s, i, sl, sc)
            continue
        if ch.isalpha() or ch == "_":
            advance_char()
            while i < n and (source[i].isalnum() or source[i] == "_"):
                advance_char()
            add("IDENT", source[s:i], s, i, sl, sc)
            continue
        if ch.isdigit() or (ch == "." and i + 1 < n and source[i + 1].isdigit()):
            advance_char()
            while i < n and (source[i].isalnum() or source[i] in "._+-"):
                # Stop at range/operator dots such as "a.b"; numeric tokens are not
                # consumed by graph extraction, so this only needs to keep spans safe.
                if source[i] == "." and i + 1 < n and not source[i + 1].isdigit():
                    break
                advance_char()
            add("NUMBER", source[s:i], s, i, sl, sc)
            continue
        two = source[i : i + 2]
        if two in {":=", "<=", ">=", "==", "<>", ".+", ".-", ".*", "./", ".^"}:
            advance_char()
            advance_char()
            add("SYMBOL", two, s, i, sl, sc)
            continue
        advance_char()
        add("SYMBOL", ch, s, i, sl, sc)

    tokens.append(Token("EOF", "", n, n, line, col))
    return tokens, diags


def _tokens_text(source: str, toks: Sequence[Token]) -> str:
    if not toks:
        return ""
    return source[toks[0].start : toks[-1].end]


def _split_top_level(tokens: Sequence[Token], sep: str) -> List[List[Token]]:
    parts: List[List[Token]] = []
    cur: List[Token] = []
    depth = 0
    pairs = {"(": ")", "[": "]", "{": "}"}
    opens = set(pairs)
    closes = set(pairs.values())
    for tok in tokens:
        if tok.value in opens:
            depth += 1
        elif tok.value in closes and depth > 0:
            depth -= 1
        if tok.value == sep and depth == 0:
            parts.append(cur)
            cur = []
        else:
            cur.append(tok)
    parts.append(cur)
    return parts


def _find_matching_paren(tokens: Sequence[Token], open_idx: int) -> int:
    if open_idx >= len(tokens) or tokens[open_idx].value != "(":
        return -1
    depth = 0
    for i in range(open_idx, len(tokens)):
        if tokens[i].value == "(":
            depth += 1
        elif tokens[i].value == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _qualified_name_at(tokens: Sequence[Token], idx: int) -> Tuple[str, int]:
    if idx >= len(tokens) or not _is_ident(tokens[idx]):
        return "", idx
    parts = [_unquote_ident(tokens[idx].value)]
    idx += 1
    while idx + 1 < len(tokens) and tokens[idx].value == "." and _is_ident(tokens[idx + 1]):
        parts.append(_unquote_ident(tokens[idx + 1].value))
        idx += 2
    return ".".join(parts), idx


class _ModelicaParser:
    def __init__(self, source: str, tokens: List[Token], diagnostics: List[Diagnostic]) -> None:
        self.source = source
        self.tokens = tokens
        self.diagnostics = diagnostics
        self.within = ""

    def parse(self) -> List[ClassNode]:
        idx = 0
        if self._peek(idx).value == "within":
            idx += 1
            if self._peek(idx).value != ";":
                self.within, idx = _qualified_name_at(self.tokens, idx)
            while self._peek(idx).value not in {";", ""}:
                idx += 1
            if self._peek(idx).value == ";":
                idx += 1
        classes: List[ClassNode] = []
        while self._peek(idx).kind != "EOF":
            parsed = self._parse_class(idx, self.within)
            if parsed is None:
                idx += 1
                continue
            node, idx = parsed
            classes.append(node)
        return classes

    def _peek(self, idx: int) -> Token:
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def _class_kind_at(self, idx: int) -> Tuple[str, int]:
        tok = self._peek(idx)
        if tok.value == "operator" and self._peek(idx + 1).value in {"record", "function"}:
            return f"operator {self._peek(idx + 1).value}", idx + 2
        if tok.value in _CLASS_KINDS:
            return tok.value, idx + 1
        return "", idx

    def _parse_class(self, idx: int, parent_name: str) -> Optional[Tuple[ClassNode, int]]:
        start_idx = idx
        while self._peek(idx).value in _CLASS_PREFIXES:
            idx += 1
        kind, idx_after_kind = self._class_kind_at(idx)
        if not kind:
            return None
        idx = idx_after_kind
        if not _is_ident(self._peek(idx)):
            return None
        name = _unquote_ident(self._peek(idx).value)
        idx += 1
        full = f"{parent_name}.{name}" if parent_name else name

        # Optional class string-comment: `model M "description"`.  If this
        # STRING stays in body_tokens it is glued onto the first component
        # clause and that declaration is dropped (then treated as synthetic).
        if self._peek(idx).kind == "STRING":
            idx += 1

        # Short class definitions (for example `connector Pin = ...;`) are
        # valid Modelica classes but do not contain a composition/end pair.
        if self._peek(idx).value == "=":
            after = idx
            while self._peek(after).kind != "EOF" and self._peek(after).value != ";":
                after += 1
            if self._peek(after).value == ";":
                after += 1
            return (
                ClassNode(
                    kind=kind,
                    name=name,
                    full_name=full,
                    body_tokens=[],
                    start=self._peek(start_idx).start,
                    end=self._peek(after - 1).end if after > start_idx else self._peek(idx).end,
                ),
                after,
            )

        # Find class body end by matching nested class definitions.
        # Ignore `model`/`class`/`end` inside (), [], {} so component
        # modifications such as `redeclare model Medium = ...` do not change depth.
        body_start = idx
        scan = idx
        depth = 1
        bracket_depth = 0
        end_idx = -1
        while self._peek(scan).kind != "EOF":
            val = self._peek(scan).value
            if val in {"(", "[", "{"}:
                bracket_depth += 1
                scan += 1
                continue
            if val in {")", "]", "}"}:
                bracket_depth = max(0, bracket_depth - 1)
                scan += 1
                continue
            if bracket_depth == 0:
                prefix_scan = scan
                while self._peek(prefix_scan).value in _CLASS_PREFIXES:
                    prefix_scan += 1
                ck, ck_next = self._class_kind_at(prefix_scan)
                if ck:
                    name_idx = ck_next
                    if _is_ident(self._peek(name_idx)) and self._peek(name_idx + 1).value == "=":
                        scan = name_idx + 2
                        while self._peek(scan).kind != "EOF" and self._peek(scan).value != ";":
                            scan += 1
                        if self._peek(scan).value == ";":
                            scan += 1
                        continue
                    depth += 1
                    scan = ck_next
                    continue
                if val == "end":
                    depth -= 1
                    if depth == 0:
                        end_idx = scan
                        break
            scan += 1
        if end_idx < 0:
            self.diagnostics.append(Diagnostic("error", "class_not_closed", f"Class {name!r} has no matching end", self._peek(start_idx).start))
            return None

        body = self.tokens[body_start:end_idx]
        after = end_idx + 1
        if _is_ident(self._peek(after)):
            after += 1
        if self._peek(after).value == ";":
            after += 1

        node = ClassNode(
            kind=kind,
            name=name,
            full_name=full,
            body_tokens=body,
            start=self._peek(start_idx).start,
            end=self._peek(after - 1).end if after > start_idx else self._peek(end_idx).end,
        )
        self._parse_body(node)
        return node, after

    def _parse_body(self, node: ClassNode) -> None:
        toks = node.body_tokens
        section = "public"
        stmt: List[Token] = []
        idx = 0
        # Depth of (), [], {} so matrix row separators like table=[0,0; 1,1]
        # are not treated as statement terminators.
        bracket_depth = 0
        while idx < len(toks):
            tok = toks[idx]
            # Nested class only at statement start. `redeclare model Medium = ...`
            # inside component modifications is not a nested class.
            if bracket_depth == 0 and not stmt:
                if tok.kind == "STRING":
                    idx += 1
                    continue
                parsed = self._parse_class_in_body(toks, idx, node.full_name)
                if parsed is not None:
                    child, idx = parsed
                    node.children.append(child)
                    stmt = []
                    continue
                if tok.value == "public":
                    self._flush_stmt(node, section, stmt)
                    stmt = []
                    section = "public"
                    idx += 1
                    continue
                if tok.value == "protected":
                    self._flush_stmt(node, section, stmt)
                    stmt = []
                    section = "protected"
                    idx += 1
                    continue
                if tok.value == "initial" and idx + 1 < len(toks) and toks[idx + 1].value in {"equation", "algorithm"}:
                    self._flush_stmt(node, section, stmt)
                    stmt = []
                    section = toks[idx + 1].value
                    idx += 2
                    continue
                if tok.value in {"equation", "algorithm"}:
                    self._flush_stmt(node, section, stmt)
                    stmt = []
                    section = tok.value
                    idx += 1
                    continue
            if tok.value in {"(", "[", "{"}:
                bracket_depth += 1
            elif tok.value in {")", "]", "}"}:
                bracket_depth = max(0, bracket_depth - 1)
            stmt.append(tok)
            if tok.value == ";" and bracket_depth == 0:
                self._flush_stmt(node, section, stmt)
                stmt = []
            idx += 1
        self._flush_stmt(node, section, stmt)

    def _parse_class_in_body(self, toks: Sequence[Token], idx: int, parent_name: str) -> Optional[Tuple[ClassNode, int]]:
        # Temporarily parse from a sliced token stream by creating a small parser
        # over the same source.  This keeps matching logic centralized.
        kind, _ = self._class_kind_at_in(toks, idx)
        if not kind:
            return None
        sub = _ModelicaParser(self.source, list(toks[idx:]) + [self.tokens[-1]], self.diagnostics)
        parsed = sub._parse_class(0, parent_name)
        if parsed is None:
            return None
        node, next_rel = parsed
        return node, idx + next_rel

    def _class_kind_at_in(self, toks: Sequence[Token], idx: int) -> Tuple[str, int]:
        i = idx
        while i < len(toks) and toks[i].value in _CLASS_PREFIXES:
            i += 1
        tok = toks[i] if i < len(toks) else None
        nxt = toks[i + 1] if i + 1 < len(toks) else None
        if tok and tok.value == "operator" and nxt and nxt.value in {"record", "function"}:
            return f"operator {nxt.value}", i + 2
        if tok and tok.value in _CLASS_KINDS:
            return tok.value, i + 1
        return "", idx

    def _flush_stmt(self, node: ClassNode, section: str, stmt: List[Token]) -> None:
        stmt = [t for t in stmt if t.kind != "EOF"]
        if not stmt:
            return
        if stmt[-1].value == ";":
            stmt = stmt[:-1]
        if not stmt:
            return
        if section in {"equation", "algorithm"}:
            conn = self._parse_connect(stmt)
            if conn:
                node.connects.append(conn)
            return
        comp = self._parse_component_clause(stmt, section)
        if comp:
            node.components.extend(comp)

    def _parse_connect(self, stmt: Sequence[Token]) -> Optional[ConnectEq]:
        if not stmt or stmt[0].value != "connect":
            return None
        if len(stmt) < 4 or stmt[1].value != "(":
            return None
        close = _find_matching_paren(stmt, 1)
        if close < 0:
            return None
        args = _split_top_level(stmt[2:close], ",")
        if len(args) != 2:
            return None
        lhs = _tokens_text(self.source, args[0]).strip()
        rhs = _tokens_text(self.source, args[1]).strip()
        ann = _extract_named_call_text(self.source, stmt[close + 1 :], "annotation")
        return ConnectEq(lhs=lhs, rhs=rhs, statement_text=_tokens_text(self.source, stmt), annotation_text=ann, start=stmt[0].start, end=stmt[-1].end)

    def _parse_component_clause(self, stmt: Sequence[Token], visibility: str) -> List[ComponentDecl]:
        if not stmt:
            return []
        if stmt[0].value in {"import", "extends", "annotation"}:
            return []
        if stmt[0].value in _SECTION_KEYWORDS:
            return []
        prefixes: List[str] = []
        idx = 0
        while idx < len(stmt) and stmt[idx].value in _DECL_PREFIXES:
            prefixes.append(stmt[idx].value)
            idx += 1
        if any(p in _SKIP_DECL_PREFIXES for p in prefixes):
            return []
        type_name, idx = _qualified_name_at(stmt, idx)
        if not type_name or type_name.split(".")[-1] in _BUILTIN_TYPES:
            return []
        decl_tokens = list(stmt[idx:])
        if not decl_tokens:
            return []
        result: List[ComponentDecl] = []
        for part in _split_top_level(decl_tokens, ","):
            part = [t for t in part if t.value]
            if not part:
                continue
            pidx = 0
            # Skip leading array subscripts that belong to the type specifier.
            while pidx < len(part) and part[pidx].value == "[":
                close = _matching_in(part, pidx, "[", "]")
                if close < 0:
                    break
                pidx = close + 1
            if pidx >= len(part) or not _is_ident(part[pidx]):
                continue
            name = _unquote_ident(part[pidx].value)
            ann = _extract_named_call_text(self.source, part[pidx + 1 :], "annotation")
            result.append(
                ComponentDecl(
                    name=name,
                    type_name=type_name,
                    prefixes=list(prefixes),
                    visibility=visibility,
                    statement_text=_tokens_text(self.source, part),
                    annotation_text=ann,
                    start=part[0].start,
                    end=part[-1].end,
                )
            )
        return result


def _matching_in(tokens: Sequence[Token], idx: int, open_value: str, close_value: str) -> int:
    depth = 0
    for i in range(idx, len(tokens)):
        if tokens[i].value == open_value:
            depth += 1
        elif tokens[i].value == close_value:
            depth -= 1
            if depth == 0:
                return i
    return -1


def _extract_named_call_text(source: str, tokens: Sequence[Token], name: str) -> str:
    for i, tok in enumerate(tokens):
        if tok.value == name and i + 1 < len(tokens) and tokens[i + 1].value == "(":
            close = _find_matching_paren(tokens, i + 1)
            if close >= 0:
                return source[tok.start : tokens[close].end]
    return ""


def _flatten_classes(classes: Sequence[ClassNode]) -> List[ClassNode]:
    out: List[ClassNode] = []
    for cls in classes:
        out.append(cls)
        out.extend(_flatten_classes(cls.children))
    return out


def _choose_target_class(classes: Sequence[ClassNode], model_name: str, diags: List[Diagnostic]) -> Optional[ClassNode]:
    flat = _flatten_classes(classes)
    if not flat:
        return None
    name = (model_name or "").strip()
    if name:
        matches = [c for c in flat if c.full_name == name or c.name == name or c.full_name.endswith("." + name)]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            exact = [c for c in matches if c.full_name == name]
            if len(exact) == 1:
                return exact[0]
            diags.append(Diagnostic("error", "ambiguous_model_name", f"Ambiguous Modelica class name: {name!r}"))
            return None
        diags.append(Diagnostic("info", "model_name_not_found", f"Modelica class {name!r} not found; using heuristic target selection"))
    preferred = [c for c in flat if c.kind in {"model", "block", "class"} and (c.components or c.connects)]
    if preferred:
        return preferred[-1]
    non_pkg = [c for c in flat if c.kind not in {"package", "type", "function"}]
    return non_pkg[-1] if non_pkg else flat[-1]


def _owner_from_ref(ref: str) -> str:
    ref = ref.strip()
    if not ref:
        return ""
    out: List[str] = []
    i = 0
    while i < len(ref):
        ch = ref[i]
        if ch == ".":
            break
        if ch == "[":
            depth = 1
            out.append(ch)
            i += 1
            while i < len(ref) and depth:
                out.append(ref[i])
                if ref[i] == "[":
                    depth += 1
                elif ref[i] == "]":
                    depth -= 1
                i += 1
            continue
        out.append(ch)
        i += 1
    owner = "".join(out).strip()
    return owner.split("[", 1)[0] if "[" in owner else owner


def _port_short_name(port: str, owner: str) -> str:
    if owner and port.startswith(owner + "."):
        return port[len(owner) + 1 :]
    return port.rsplit(".", 1)[-1]


def _parse_extent(text: str) -> Optional[List[List[float]]]:
    m = re.search(r"extent\s*=\s*\{\s*\{\s*([-+\d.eE]+)\s*,\s*([-+\d.eE]+)\s*\}\s*,\s*\{\s*([-+\d.eE]+)\s*,\s*([-+\d.eE]+)\s*\}\s*\}", text)
    if not m:
        return None
    try:
        return [[float(m.group(1)), float(m.group(2))], [float(m.group(3)), float(m.group(4))]]
    except ValueError:
        return None


def _parse_origin(text: str) -> Optional[List[float]]:
    m = re.search(r"origin\s*=\s*\{\s*([-+\d.eE]+)\s*,\s*([-+\d.eE]+)\s*\}", text or "")
    if not m:
        return None
    try:
        return [float(m.group(1)), float(m.group(2))]
    except ValueError:
        return None


def _apply_placement_geometry(node: Dict[str, Any], annotation_text: str) -> None:
    """Fill node x/y/width/height from Placement origin/extent text."""
    extent = _parse_extent(annotation_text or "")
    origin = _parse_origin(annotation_text or "")
    width = float(node.get("width") or 30)
    height = float(node.get("height") or 40)
    if extent:
        width = abs(float(extent[1][0]) - float(extent[0][0])) or width
        height = abs(float(extent[1][1]) - float(extent[0][1])) or height
        node["width"] = width
        node["height"] = height
    if origin:
        node["x"] = float(origin[0]) - width / 2.0
        node["y"] = float(origin[1]) - height / 2.0
    elif extent:
        node["x"] = min(float(extent[0][0]), float(extent[1][0]))
        node["y"] = min(float(extent[0][1]), float(extent[1][1]))


def _parse_rotation(text: str) -> Optional[int]:
    m = re.search(r"rotation\s*=\s*([-+]?\d+)", text)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def _parse_line_points(text: str) -> Optional[List[List[float]]]:
    m = re.search(r"points\s*=\s*\{(.*?)\}", text, flags=re.S)
    if not m:
        return None
    pairs = re.findall(r"\{\s*([-+\d.eE]+)\s*,\s*([-+\d.eE]+)\s*\}", text)
    pts: List[List[float]] = []
    for a, b in pairs:
        try:
            pts.append([float(a), float(b)])
        except ValueError:
            return None
    return pts or None


def parse_modelica_34_source(modelica_code: str, model_name: str = "") -> Tuple[Optional[ClassNode], List[Dict[str, Any]]]:
    """Parse Modelica source and return the selected class plus diagnostics.

    This is intentionally a structure parse for source-span consumers. It does
    not perform Modelica semantic checks.
    """
    tokens, diags = _tokenize_modelica(modelica_code or "")
    parser = _ModelicaParser(modelica_code or "", tokens, diags)
    classes = parser.parse()
    target = _choose_target_class(classes, model_name, diags)
    return target, [_diag_dict(d) for d in diags]


def build_graph_from_modelica_34_source(modelica_code: str, model_name: str = "") -> GraphBuildResult:
    tokens, diags = _tokenize_modelica(modelica_code or "")
    if any(d.severity == "error" for d in diags):
        return GraphBuildResult(False, diagnostics=[_diag_dict(d) for d in diags], error=diags[0].message)
    parser = _ModelicaParser(modelica_code or "", tokens, diags)
    classes = parser.parse()
    if any(d.severity == "error" for d in diags):
        return GraphBuildResult(False, diagnostics=[_diag_dict(d) for d in diags], error=diags[-1].message)
    target = _choose_target_class(classes, model_name, diags)
    if target is None:
        return GraphBuildResult(False, diagnostics=[_diag_dict(d) for d in diags], error="No Modelica class found")

    comp_by_name = {c.name: c for c in target.components}
    ports_by_node: Dict[str, Dict[str, str]] = {name: {} for name in comp_by_name}
    edges: List[Dict[str, Any]] = []
    synthetic_owners: Dict[str, Dict[str, str]] = {}
    for idx, conn in enumerate(target.connects):
        lhs = conn.lhs
        rhs = conn.rhs
        lhs_owner = _owner_from_ref(lhs)
        rhs_owner = _owner_from_ref(rhs)
        for owner, ref in ((lhs_owner, lhs), (rhs_owner, rhs)):
            if not owner:
                continue
            if owner in ports_by_node:
                ports_by_node[owner][ref] = _port_short_name(ref, owner)
                continue
            # Inherited / class-level connectors are not local component clauses.
            # Keep the edge and add a synthetic node instead of warning — those
            # warnings made agents treat a successful writeback as a failed layout.
            bucket = synthetic_owners.setdefault(owner, {})
            bucket[ref] = _port_short_name(ref, owner)
            ports_by_node[owner] = bucket
        edge: Dict[str, Any] = {
            "id": f"connect_{idx}_{lhs}__{rhs}",
            "sources": [lhs],
            "targets": [rhs],
            "metadata": {"lhs_owner": lhs_owner, "rhs_owner": rhs_owner, "span": [conn.start, conn.end]},
        }
        pts = _parse_line_points(conn.annotation_text)
        if pts:
            edge["line"] = {"points": pts}
        edges.append(edge)

    if synthetic_owners:
        diags.append(
            Diagnostic(
                "info",
                "synthetic_connect_owner",
                "Connect endpoints not declared as local components were added as "
                f"synthetic layout nodes: {', '.join(sorted(synthetic_owners))}",
            )
        )

    children: List[Dict[str, Any]] = []
    for comp in target.components:
        ports = [
            {"id": pid, "name": pname}
            for pid, pname in sorted(ports_by_node.get(comp.name, {}).items())
        ]
        if not ports:
            # Source-only parsing cannot introspect library connector declarations.
            # Declarations that never appear in connect(...) (for example typed
            # state variables with Placement annotations) should not become
            # isolated diagram nodes; otherwise they distort the auto-router bus.
            continue
        node: Dict[str, Any] = {
            "id": comp.name,
            "type": comp.type_name,
            "width": 30,
            "height": 40,
            "ports": ports,
            "metadata": {
                "visibility": comp.visibility,
                "prefixes": comp.prefixes,
                "span": [comp.start, comp.end],
            },
        }
        extent = _parse_extent(comp.annotation_text)
        if extent:
            node["placement"] = {"extent": extent}
        origin = _parse_origin(comp.annotation_text)
        if origin:
            node.setdefault("placement", {})
            if isinstance(node["placement"], dict):
                node["placement"]["origin"] = origin
        if comp.annotation_text:
            _apply_placement_geometry(node, comp.annotation_text)
        rot = _parse_rotation(comp.annotation_text)
        if rot is not None:
            node["rotation"] = rot
        children.append(node)

    seen_ids = {str(n.get("id")) for n in children}
    for owner, port_map in sorted(synthetic_owners.items()):
        if owner in seen_ids:
            continue
        children.append(
            {
                "id": owner,
                "type": "__connector__",
                "width": 10,
                "height": 10,
                "ports": [{"id": pid, "name": pname} for pid, pname in sorted(port_map.items())],
                "metadata": {"synthetic": True, "reason": "connect_owner_not_in_components"},
            }
        )

    if len(children) < 2 or len(edges) < 1:
        return GraphBuildResult(
            True,
            graph={
                "id": target.full_name,
                "children": children,
                "edges": edges,
                "metadata": {
                    "parser": "modelica_34_ast",
                    "modelica_version": "3.4",
                    "diagnostics": [_diag_dict(d) for d in diags],
                },
            },
            diagnostics=[_diag_dict(d) for d in diags],
            error="模型组件少于2个或无连接，无需布局",
        )

    graph = {
        "id": target.full_name,
        "children": children,
        "edges": edges,
        "metadata": {
            "parser": "modelica_34_ast",
            "modelica_version": "3.4",
            "target_class": target.full_name,
            "diagnostics": [_diag_dict(d) for d in diags],
        },
    }
    return GraphBuildResult(True, graph=graph, diagnostics=[_diag_dict(d) for d in diags])
