"""Modelica model text parsing utilities."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from constants import (
    _CLASS_RE,
    _EXTENDS_RE,
    _IMPORT_RE,
    _PARAM_RE,
    _DECL_RE,
    _CONNECTOR_SUFFIXES,
)


def _parse_default(value: Optional[str]) -> Any:
    if value is None:
        return None
    raw = value.strip()
    if raw == "":
        return None
    if raw in {"true", "false"}:
        return raw == "true"
    try:
        if "." in raw or "e" in raw.lower():
            return float(raw)
        return int(raw)
    except Exception:
        return raw


def _infer_unit(type_name: str) -> str:
    if type_name.startswith("Modelica.Units.SI."):
        return type_name.split(".")[-1]
    return "1"


def _looks_like_connector(type_name: str) -> bool:
    return ".Interfaces." in type_name or type_name.endswith(_CONNECTOR_SUFFIXES)


def _parse_model_text(model_text: str) -> Dict[str, Any]:
    class_kind = ""
    class_name = ""
    class_match = _CLASS_RE.search(model_text)
    if class_match:
        class_kind = class_match.group(1)
        class_name = class_match.group(2)

    extends = sorted({m.group(1).strip() for m in _EXTENDS_RE.finditer(model_text)})
    imports = sorted({m.group(1).strip() for m in _IMPORT_RE.finditer(model_text)})

    parameters: List[Dict[str, Any]] = []
    for m in _PARAM_RE.finditer(model_text):
        type_name = m.group(1).strip()
        name = m.group(2).strip()
        default_raw = m.group(3)
        desc = (m.group(4) or "").strip()
        parameters.append(
            {
                "name": name,
                "type": type_name,
                "unit": _infer_unit(type_name),
                "description": desc,
                "default": _parse_default(default_raw),
            }
        )

    connectors: List[Dict[str, Any]] = []
    seen_conn: set[Tuple[str, str]] = set()
    for m in _DECL_RE.finditer(model_text):
        type_name = m.group(1).strip()
        name = m.group(2).strip()
        desc = (m.group(3) or "").strip()
        if not _looks_like_connector(type_name):
            continue
        key = (name, type_name)
        if key in seen_conn:
            continue
        seen_conn.add(key)
        connectors.append({"name": name, "type": type_name, "description": desc})

    return {
        "class_kind": class_kind,
        "class_name": class_name,
        "extends": extends,
        "imports": imports,
        "parameters": parameters,
        "connectors": connectors,
    }


def _strip_annotations(text: str) -> str:
    """Remove annotation(...) blocks to avoid regex false-matches."""
    out: List[str] = []
    depth, i = 0, 0
    while i < len(text):
        if depth == 0 and text[i:].lstrip().startswith("annotation"):
            j = text.find("(", i)
            if j == -1:
                break
            depth = 1
            i = j + 1
            continue
        if depth:
            if text[i] == "(":
                depth += 1
            elif text[i] == ")":
                depth -= 1
                if depth == 0:
                    i += 1
                    continue
        else:
            out.append(text[i])
        i += 1
    return "".join(out)
