"""Interface registry and .mol connector/parameter extraction utilities."""
from __future__ import annotations

import html as _html
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from constants import (
    _IFACE_CONN_DECL_RE,
    _IFACE_CONN_KEYWORDS,
    _PROBE_CONNECTORS,
    _PROBE_PARAMS,
)
import state as _state
from core.model_parser import _parse_default, _strip_annotations


def _build_iface_registry(driver: Any, all_classes: List[str]) -> Dict[str, Any]:
    """
    Parse GetModelText for *.Interfaces.* classes (accessible in protected .mol).
    Returns registry[fqname] = {kind, description, extends, variables, connectors, parameters}
    where:
      - 'variables'  : connector effort/flow variables  (kind='connector')
      - 'connectors' : declared port names + types      (kind='partial'/'model')
      - 'parameters' : declared parameter names          (any)
    """
    registry: Dict[str, Any] = {}
    _SKIP_KW = {
        "end", "annotation", "model", "connector", "partial", "package",
        "protected", "public", "equation", "algorithm", "extends", "import",
        "parameter", "record", "block", "type", "function",
    }
    for fq in all_classes:
        if ".Interfaces." not in fq and not fq.endswith(".Interfaces"):
            continue
        text_r = driver.get_model_text(fq)
        text = text_r.data if (text_r.ok and text_r.data) else ""
        desc_r = driver.get_model_description(fq)
        desc = str(desc_r.data or "").strip()

        m = re.search(r"\b(connector|partial\s+model|model|package|record)\b", text or "")
        raw_kind = m.group(1) if m else ""
        kind = "partial" if "partial" in raw_kind else (raw_kind.split()[0] if raw_kind else "?")

        clean = _strip_annotations(text) if text else ""

        # extends chain
        extends = [em.group(1) for em in re.finditer(r"^\s*extends\s+([\w.]+)", clean, re.M)]

        # connector variables (effort/flow)
        variables: List[Dict[str, Any]] = []
        if kind == "connector" and clean:
            seen_v: set = set()
            for vm in re.finditer(
                r"^\s*(flow\s+)?((?:Modelica\.|SI\.)?[\w.]+)\s+(\w+)\s*(?:\([^;]*?\))?\s*(?:\"([^\"]*)\")?\s*;",
                clean, re.M,
            ):
                is_flow = bool(vm.group(1))
                vname = vm.group(3).strip()
                vdesc = (vm.group(4) or "").strip()
                if vname.lower() in _SKIP_KW or not vname[0].isalpha():
                    continue
                if vname in seen_v:
                    continue
                seen_v.add(vname)
                variables.append({"name": vname, "flow": is_flow, "description": vdesc})

        # connector port declarations (in partial/model classes)
        connectors: List[Dict[str, Any]] = []
        if kind != "connector" and clean:
            seen_c: set = set()
            for cm in _IFACE_CONN_DECL_RE.finditer(clean):
                type_name = cm.group(1).strip()
                port_name = cm.group(2).strip()
                cdesc = (cm.group(3) or "").strip()
                if not any(kw in type_name for kw in _IFACE_CONN_KEYWORDS):
                    continue
                if port_name.lower() in _SKIP_KW:
                    continue
                if port_name in seen_c:
                    continue
                seen_c.add(port_name)
                connectors.append({"name": port_name, "type": type_name, "description": cdesc})

        # parameters declared in partial/base classes
        parameters: List[Dict[str, Any]] = []
        if clean:
            seen_p: set = set()
            for pm in re.finditer(
                r"^\s*parameter\s+([\w.]+)\s+(\w+)\s*(?:\([^;\"\\n]*\))?\s*(?:=\s*([^;\"\\n]+?))?\s*(?:\"([^\"]*)\")?\s*;",
                clean, re.M,
            ):
                pname = pm.group(2).strip()
                if pname in seen_p:
                    continue
                seen_p.add(pname)
                parameters.append({
                    "name": pname,
                    "type": pm.group(1).strip(),
                    "default": (pm.group(3) or "").strip() or None,
                    "description": (pm.group(4) or "").strip(),
                })

        registry[fq] = {
            "kind": kind,
            "description": desc,
            "extends": extends,
            "variables": variables,
            "connectors": connectors,
            "parameters": parameters,
        }
    return registry


def _resolve_iface_connectors(reg_key: str, registry: Dict[str, Any], seen: Optional[set] = None) -> List[Dict[str, Any]]:
    """Recursively resolve connectors from partial model extends chain, same-namespace first."""
    if seen is None:
        seen = set()
    if reg_key in seen:
        return []
    seen.add(reg_key)
    entry = registry.get(reg_key, {})
    conns = list(entry.get("connectors", []))
    ns_prefix = ".".join(reg_key.split(".")[:2])  # e.g. "TYMechanics.Translational"
    for base in entry.get("extends", []):
        base_leaf = base.split(".")[-1]
        # prefer same namespace
        candidates = sorted(
            [k for k in registry if k.endswith("." + base_leaf) and k != reg_key],
            key=lambda k: (0 if k.startswith(ns_prefix) else 1),
        )
        for cand in candidates[:1]:
            extra = _resolve_iface_connectors(cand, registry, set(seen))
            for x in extra:
                if not any(e["name"] == x["name"] for e in conns):
                    conns.append(x)
    return conns


def _api_extract_mol(
    driver: Any,
    fqname: str,
    iface_registry: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    For protected .mol classes where GetModelText returns empty:
    1. OpenModel (needed for GetComponentDescription to work)
    2. GetComponents 鈫?param names if available (works for .mo, usually [] for .mol)
    3. Probe _PROBE_PARAMS with GetComponentDescription 鈫?params
    4. Probe _PROBE_CONNECTORS with GetComponentDescription 鈫?connectors
    Returns (parameters, connectors).
    """
    # OpenModel is needed before GetComponentDescription; for protected .mol it may
    # return False but GetComponentDescription can still work 鈥?do not exit on failure.
    driver.open_model(fqname)

    # Try GetComponents first (works for .mo, returns [] for protected .mol)
    comp_names: List[str] = []
    comps_r = driver.get_components(fqname)
    if comps_r.ok and comps_r.data:
        comp_names = list(comps_r.data)

    params: List[Dict[str, Any]] = []
    seen_p: set = set()

    if comp_names:
        # .mo path: GetComponents gave us names, get descriptions
        for name in comp_names:
            desc_r = driver.get_component_description(fqname, name)
            desc = str(desc_r.data or "").strip()
            params.append({"name": name, "description": desc, "type": "", "unit": "1", "default": None})
            seen_p.add(name)
    else:
        # .mol protected path: probe with known parameter names
        for pname in _PROBE_PARAMS:
            if pname in seen_p:
                continue
            desc_r = driver.get_component_description(fqname, pname)
            desc = str(desc_r.data or "").strip()
            if desc:
                params.append({"name": pname, "description": desc, "type": "", "unit": "1", "default": None})
                seen_p.add(pname)

    # Connector probe
    connectors: List[Dict[str, Any]] = []
    seen_c: set = set()
    for cname in _PROBE_CONNECTORS:
        desc_r = driver.get_component_description(fqname, cname)
        desc = str(desc_r.data or "").strip()
        if desc and cname not in seen_c:
            connectors.append({"name": cname, "description": desc, "type": "", "direction": "inout"})
            seen_c.add(cname)

    return params, connectors


def _build_help_html_index(roots: Tuple[Path, ...]) -> Dict[str, List[Path]]:
    key = "|".join(sorted(str(p) for p in roots))
    if key in _state._help_html_index_cache:
        return _state._help_html_index_cache[key]
    idx: Dict[str, List[Path]] = {}
    for root in roots:
        for p in root.rglob("*.html"):
            if "resources\\html" not in str(p).lower().replace("/", "\\"):
                continue
            name = p.stem.lower()
            idx.setdefault(name, []).append(p)
    _state._help_html_index_cache[key] = idx
    return idx


def _extract_parameters_from_help_html(help_html: Path) -> List[Dict[str, Any]]:
    try:
        text = help_html.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    rows: List[List[str]] = []
    for tm in re.finditer(r"<table[^>]*>(.*?)</table>", text, flags=re.I | re.S):
        table_html = tm.group(1)
        for rm in re.finditer(r"<tr[^>]*>(.*?)</tr>", table_html, flags=re.I | re.S):
            row_html = rm.group(1)
            row_cells: List[str] = []
            for cm in re.finditer(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, flags=re.I | re.S):
                cell_text = re.sub(r"<[^>]+>", "", cm.group(1))
                cell_text = _html.unescape(cell_text).replace("\xa0", " ").strip()
                if cell_text:
                    row_cells.append(cell_text)
            if row_cells:
                rows.append(row_cells)

    if not rows:
        return []

    def _is_param_header(r: List[str]) -> bool:
        joined = " ".join(r).lower()
        return "parameter name" in joined and ("default" in joined or "unit" in joined)

    start = -1
    for i, r in enumerate(rows):
        if _is_param_header(r):
            start = i + 1
            break
    if start < 0:
        return []

    out: List[Dict[str, Any]] = []
    skip_names = {
        "鍙傛暟",
        "鍙傛暟鍚嶇О",
        "tab鍙傛暟",
        "group鍙傛暟",
        "parameter",
        "parameter name",
    }
    for r in rows[start:]:
        if len(r) < 3:
            continue
        # Most docs are either:
        # 6 cols: tab, group, name, default, unit, desc
        # 5 cols: tab, name, default, unit, desc
        # 4 cols: name, default, unit, desc
        name = r[-4].strip() if len(r) >= 4 else ""
        default_raw = r[-3].strip() if len(r) >= 3 else ""
        unit = r[-2].strip() if len(r) >= 2 else ""
        desc = r[-1].strip() if len(r) >= 1 else ""

        # Some 4-col rows are effectively: group, name, "/", desc.
        if len(r) == 4 and unit == "/" and re.fullmatch(r"[A-Za-z][A-Za-z0-9_/.-]*", name):
            if re.search(r"[\u4e00-\u9fffA-Za-z_]", default_raw):
                name, default_raw = default_raw, "/"

        if not name:
            continue
        lname = name.lower()
        if lname in skip_names:
            continue
        if len(name) > 120 or " " in name or "/" in name:
            continue
        if name in {"閰嶇疆", "鍙傛暟璁剧疆", "棰戠巼璁剧疆", "娼祦璁＄畻", "鍐呴樆璁剧疆", "鍐呴樆鏍囩О鐢靛帇璁捐"}:
            continue

        # _to_quantity_kind is in lib_catalog; import lazily to avoid circular
        from core.lib_catalog import _to_quantity_kind
        out.append(
            {
                "name": name,
                "type": "Real",
                "unit": unit if unit and unit != "/" else "1",
                "quantity_kind": _to_quantity_kind(unit if unit and unit != "/" else "1"),
                "default": _parse_default(default_raw if default_raw not in {"/", ""} else None),
                "required": False,
                "range": None,
                "enum": None,
                "tunable": True,
                "description": desc if desc != "/" else "",
            }
        )
    # dedupe by name
    seen: set[str] = set()
    uniq: List[Dict[str, Any]] = []
    for p in out:
        n = str(p.get("name", ""))
        if n in seen:
            continue
        seen.add(n)
        uniq.append(p)
    return uniq


def _extract_connectors_from_help_html(help_html: Path) -> List[Dict[str, Any]]:
    try:
        text = help_html.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    def _rows_from_table(table_html: str) -> List[List[str]]:
        rows: List[List[str]] = []
        for rm in re.finditer(r"<tr[^>]*>(.*?)</tr>", table_html, flags=re.I | re.S):
            row_html = rm.group(1)
            cells: List[str] = []
            for cm in re.finditer(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, flags=re.I | re.S):
                cell_text = re.sub(r"<[^>]+>", "", cm.group(1))
                cell_text = _html.unescape(cell_text).replace("\xa0", " ").strip()
                if cell_text:
                    cells.append(cell_text)
            if cells:
                rows.append(cells)
        return rows

    def _is_interface_header(row: List[str]) -> bool:
        joined = " ".join(row).lower()
        return ("鎺ュ彛" in joined and "鍙橀噺" in joined) or ("interface" in joined and "variable" in joined)

    def _normalize_connector_name(name: str) -> str:
        n = (name or "").strip()
        n = re.sub(r"[锛?].*?[锛?]", "", n).strip()
        return n

    def _looks_like_connector_name(name: str) -> bool:
        n = (name or "").strip()
        if not n or len(n) > 120 or " " in n:
            return False
        if n in {"鎺ュ彛", "鍙橀噺", "鑼冨洿", "鍗曚綅", "鎻忚堪", "鏁版嵁绫诲瀷", "鏁版嵁缁村害"}:
            return False
        if n in {"p", "q", "V", "v", "f", "s", "m_flow", "H_flow", "T"}:
            return False
        low = n.lower()
        if any(k in low for k in ["port", "flange", "support", "signal", "pin", "frame", "heatport"]):
            return True
        return bool(re.fullmatch(r"[A-Za-z_]\w+", n) and "_" in n and len(n) >= 5)

    def _domain_by_name(name: str) -> str:
        low = name.lower()
        if "flange" in low or "support" in low or "frame" in low:
            return "mechanical"
        if "signal" in low:
            return "signal"
        if "heat" in low:
            return "thermal"
        if "pin" in low:
            return "electrical"
        return "fluid"

    out: List[Dict[str, Any]] = []
    seen: set[str] = set()
    for tm in re.finditer(r"<table[^>]*>(.*?)</table>", text, flags=re.I | re.S):
        rows = _rows_from_table(tm.group(1))
        if not rows:
            continue
        if not any(_is_interface_header(r) for r in rows[:2]):
            continue
        for row in rows[1:]:
            if not row:
                continue
            raw_name = row[0]
            name = _normalize_connector_name(raw_name)
            if not _looks_like_connector_name(name):
                continue
            if name in seen:
                continue
            seen.add(name)
            desc = row[-1].strip() if len(row) >= 2 else ""
            out.append(
                {
                    "name": name,
                    "direction": "inout",
                    "type": "",
                    "domain": _domain_by_name(name),
                    "dimension": "scalar",
                    "optional": False,
                    "description": desc if desc != "/" else "",
                }
            )
    return out


def _pick_help_candidates_for_class(fqname: str, class_name: str) -> List[Path]:
    from core.utils import _discover_mw_mol_roots
    roots = _discover_mw_mol_roots()
    if not roots:
        return []
    idx = _build_help_html_index(tuple(roots))
    family = fqname.split(".", 1)[0].lower() if "." in fqname else fqname.lower()
    candidates = idx.get(class_name.lower(), [])
    if not candidates:
        return []

    def _score(path: Path) -> Tuple[int, int]:
        p = str(path).lower()
        family_rank = 0 if family and family in p else 1
        fq_rank = 1
        try:
            txt = path.read_text(encoding="utf-8", errors="ignore")
            fq_rank = 0 if fqname and fqname.lower() in txt.lower() else 1
        except Exception:
            fq_rank = 1
        return (fq_rank, family_rank)

    return sorted(candidates, key=lambda p: (_score(p), len(str(p))))


def _help_parameters_for_class(fqname: str, class_name: str) -> List[Dict[str, Any]]:
    candidates = _pick_help_candidates_for_class(fqname=fqname, class_name=class_name)
    for p in candidates:
        params = _extract_parameters_from_help_html(p)
        if params:
            return params
    return []


def _help_connectors_for_class(fqname: str, class_name: str) -> List[Dict[str, Any]]:
    candidates = _pick_help_candidates_for_class(fqname=fqname, class_name=class_name)
    for p in candidates:
        connectors = _extract_connectors_from_help_html(p)
        if connectors:
            return connectors
    return []
