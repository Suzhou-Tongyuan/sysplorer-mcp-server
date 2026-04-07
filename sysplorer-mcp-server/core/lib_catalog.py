"""Library catalog management — metadata extraction and catalog CRUD."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from mworks_driver import MWorksDriver
from constants import (
    _CLASS_RE,
    _CLASS_TOKEN_RE,
    _LIB_NAME_VERSION_RE,
    _PREFERRED_LIBRARY_VERSIONS,
    commercial_lib_load_without_version,
    normalize_load_library_call,
    _DOM_THERMAL,
    _DOM_FLUID,
    _DOM_MULTIBODY,
    _DOM_ROTATIONAL,
    _DOM_FLANGE,
    _DOM_ELECTRICAL,
    _DOM_ROT_KW,
    _DOM_TRANS_KW,
    _DOM_ELEC_KW,
    _DOM_FLUID_KW,
    _DOM_THERM_KW,
)
from core.model_parser import _parse_model_text
from core.mol_extractor import (
    _build_iface_registry,
    _help_parameters_for_class,
    _api_extract_mol,
)


def _infer_model_name_from_file(file_path: Path) -> str:
    if not file_path.exists():
        return ""
    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    m = _CLASS_RE.search(text)
    if m:
        return m.group(2)
    if file_path.name.lower() == "package.mo":
        return file_path.parent.name
    return file_path.stem


def _load_library_try(driver: MWorksDriver, name: str) -> Tuple[bool, List[str]]:
    tried: List[str] = []
    lib = str(name or "").strip()
    fam, _ = normalize_load_library_call(lib, "")
    if commercial_lib_load_without_version(fam):
        desc = f"LoadLibrary({fam!r})"
        tried.append(desc)
        result = driver.load_library(fam, "")
        if result.ok and bool(result.data):
            return True, tried
        return False, tried

    preferred = _PREFERRED_LIBRARY_VERSIONS.get(fam, "")
    versions: List[str] = []
    if preferred:
        versions.append(preferred)
    versions.extend(["4.0", "3.2.3", ""])

    seen: set[str] = set()
    for ver in versions:
        key = ver.strip()
        if key in seen:
            continue
        seen.add(key)
        desc = f"LoadLibrary({fam!r}, {key!r})" if key else f"LoadLibrary({fam!r})"
        tried.append(desc)
        result = driver.load_library(fam, key)
        if result.ok and bool(result.data):
            return True, tried
    return False, tried


def _upsert_component(components: List[Dict[str, Any]], new_comp: Dict[str, Any]) -> List[Dict[str, Any]]:
    by_name: Dict[str, Dict[str, Any]] = {}
    for item in components:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        by_name[name] = item
    by_name[new_comp["name"]] = new_comp
    return [by_name[k] for k in sorted(by_name.keys())]


def _now_utc_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _make_id(prefix: str, fqname: str) -> str:
    key = (fqname or "").strip().lower()
    if not key:
        return f"{prefix}:unknown"
    return f"{prefix}:{key.replace(' ', '_')}"


def _to_quantity_kind(unit: str) -> Optional[str]:
    mapping = {
        "Ohm": "resistance",
        "K": "temperature",
        "A": "current",
        "V": "voltage",
        "W": "power",
        "J": "energy",
        "Pa": "pressure",
        "F": "capacitance",
        "H": "inductance",
    }
    return mapping.get(unit)


def _to_domain(type_name: str) -> str:
    """Infer domain from connector TYPE name (works when type is fully qualified)."""
    t = type_name.lower()
    if "electrical" in t or "analog" in t or ".pin" in t:
        return "electrical"
    if "fluid" in t or "hydraulic" in t or "pneumatic" in t:
        return "fluid"
    if "thermal" in t or "heat" in t:
        return "thermal"
    if "multibody" in t or ".frame" in t:
        return "multibody"
    if "rotational" in t or "flange" in t:
        return "rotational"
    if "translational" in t:
        return "translational"
    if "blocks" in t or "signal" in t or "realinput" in t or "realoutput" in t:
        return "signal"
    return ""   # unknown 鈥?caller should fall back to name-based inference


def _infer_domain_by_name(conn_name: str, fqname: str = "") -> str:
    """
    Infer connector domain from connector name + optional fully-qualified class name.
    Used as fallback when _to_domain() cannot identify the domain from the type string.
    """
    n   = conn_name.lower()
    fq  = fqname.lower()
    if n in _DOM_THERMAL or n.startswith("heat"):
        return "thermal"
    if n.startswith("port_") or n in _DOM_FLUID:
        return "fluid"
    if n.startswith("frame") or n in _DOM_MULTIBODY:
        return "multibody"
    if n in _DOM_ROTATIONAL:
        return "rotational"
    if n in _DOM_FLANGE:
        # Check explicit rotational context first; then translational; default rotational.
        is_rot   = any(kw in fq for kw in _DOM_ROT_KW)
        is_trans = any(kw in fq for kw in _DOM_TRANS_KW)
        if is_rot and not is_trans:
            return "rotational"
        if is_trans and not is_rot:
            return "translational"
        return "rotational"   # flanges are rotational by default
    if n in ("p", "n"):
        if any(kw in fq for kw in _DOM_ELEC_KW):
            return "electrical"
        return "electrical"   # p/n default to electrical
    if n in _DOM_ELECTRICAL or n.startswith("pin_") or n.startswith("terminal"):
        return "electrical"
    # library/fqname keywords
    if any(kw in fq for kw in _DOM_THERM_KW):
        return "thermal"
    if any(kw in fq for kw in _DOM_FLUID_KW):
        return "fluid"
    if any(kw in fq for kw in _DOM_ELEC_KW):
        return "electrical"
    if any(kw in fq for kw in _DOM_ROT_KW):
        return "rotational"
    if any(kw in fq for kw in _DOM_TRANS_KW):
        return "translational"
    return "signal"


def _connector_domain(type_name: str, conn_name: str, fqname: str = "") -> str:
    """Combined domain inference: type-based first, name-based as fallback."""
    dom = _to_domain(type_name)
    if not dom:
        dom = _infer_domain_by_name(conn_name, fqname)
    return dom or "signal"


def _upsert_by_id(items: List[Dict[str, Any]], new_item: Dict[str, Any]) -> List[Dict[str, Any]]:
    by_id: Dict[str, Dict[str, Any]] = {}
    for item in items:
        key = str(item.get("id", "")).strip()
        if key:
            by_id[key] = item
    new_key = str(new_item.get("id", "")).strip()
    if new_key:
        by_id[new_key] = new_item
    return [by_id[k] for k in sorted(by_id.keys())]


def _parse_library_name_and_version(lib_name: str) -> Tuple[str, str]:
    name = str(lib_name or "").strip()
    m = _LIB_NAME_VERSION_RE.match(name)
    if not m:
        return name, ""
    return m.group("family").strip(), m.group("version").strip()


def _version_rank(version: str) -> Tuple[int, ...]:
    if not version:
        return (0,)
    nums: List[int] = []
    for part in re.split(r"[^\d]+", version):
        if not part:
            continue
        try:
            nums.append(int(part))
        except Exception:
            nums.append(0)
    return tuple(nums or [0])


def _compute_default_library_ids(libraries: List[Dict[str, Any]]) -> set[str]:
    by_family: Dict[str, List[Dict[str, Any]]] = {}
    for lib in libraries:
        family = str(lib.get("family", lib.get("name", ""))).strip()
        by_family.setdefault(family, []).append(lib)

    defaults: set[str] = set()
    for family, items in by_family.items():
        preferred = _PREFERRED_LIBRARY_VERSIONS.get(family, "")
        chosen: Optional[Dict[str, Any]] = None
        if preferred:
            for x in items:
                if str(x.get("version", "")) == preferred:
                    chosen = x
                    break
        if chosen is None:
            chosen = sorted(
                items,
                key=lambda x: _version_rank(str(x.get("version", ""))),
                reverse=True,
            )[0]
        lib_id = str(chosen.get("id", "")).strip()
        if lib_id:
            defaults.add(lib_id)
    return defaults


def _apply_library_version_policy(libraries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    defaults = _compute_default_library_ids(libraries)
    out: List[Dict[str, Any]] = []
    for lib in libraries:
        item = dict(lib)
        lid = str(item.get("id", ""))
        is_default = lid in defaults if defaults else bool(item.get("is_default", True))
        item["is_default"] = is_default
        item["preferred_rank"] = 0 if is_default else int(item.get("preferred_rank", 100))
        item["status"] = "active" if is_default else (str(item.get("status", "")) or "legacy")
        item["version_policy"] = "preferred_for_modeling" if is_default else "available_non_default"
        out.append(item)
    return out


def _new_base_payload() -> Dict[str, Any]:
    return {
        "schema": {"id": "com.tyautomodelica.private-lib-meta", "version": "1.0.0"},
        "snapshot": {},
        "catalog": {"libraries": [], "classes": [], "interfaces": [], "relations": [], "artifacts": []},
        "quality": {
            "errors": [],
            "warnings": [],
            "coverage": {"class_text_available": 0.0, "interface_extracted": 0.0},
        },
    }


def _read_metadata_payload(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return _new_base_payload()
    try:
        raw = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
        if isinstance(raw, dict):
            return raw
    except Exception:
        pass
    return _new_base_payload()


def _scan_library_signature(lib_dir: Path) -> Dict[str, Any]:
    mo_count = 0
    total_size = 0
    newest_ns = 0
    first_package = ""
    package_count = 0
    for mo_file in lib_dir.rglob("*.mo"):
        mo_count += 1
        try:
            st = mo_file.stat()
            total_size += int(st.st_size)
            newest_ns = max(newest_ns, int(getattr(st, "st_mtime_ns", int(st.st_mtime * 1_000_000_000))))
        except Exception:
            pass
        if mo_file.name.lower() == "package.mo":
            package_count += 1
            if not first_package:
                first_package = str(mo_file)
    sig_text = f"{lib_dir.name}|{mo_count}|{total_size}|{newest_ns}|{package_count}"
    sig = hashlib.sha1(sig_text.encode("utf-8")).hexdigest()
    return {
        "signature": sig,
        "mo_count": mo_count,
        "total_size": total_size,
        "newest_mtime_ns": newest_ns,
        "package_count": package_count,
        "first_package_mo": first_package,
    }


def _purge_library_from_catalog(catalog: Dict[str, Any], library_id: str) -> Dict[str, Any]:
    classes = list(catalog.get("classes", []))
    remove_class_ids = {str(x.get("id", "")) for x in classes if str(x.get("library_id", "")) == library_id}

    catalog["libraries"] = [x for x in list(catalog.get("libraries", [])) if str(x.get("id", "")) != library_id]
    catalog["classes"] = [x for x in classes if str(x.get("id", "")) not in remove_class_ids]
    catalog["interfaces"] = [
        x for x in list(catalog.get("interfaces", [])) if str(x.get("class_id", "")) not in remove_class_ids
    ]
    catalog["artifacts"] = [
        x for x in list(catalog.get("artifacts", [])) if str(x.get("class_id", "")) not in remove_class_ids
    ]
    catalog["relations"] = [
        x
        for x in list(catalog.get("relations", []))
        if str(x.get("from_id", "")) not in remove_class_ids and str(x.get("to_id", "")) not in remove_class_ids
    ]
    return catalog


def _compute_coverage(catalog: Dict[str, Any]) -> Dict[str, float]:
    class_count = len(catalog.get("classes", []))
    text_available = len([x for x in catalog.get("classes", []) if str(x.get("text_hash", "")).strip()])
    interface_count = len(catalog.get("interfaces", []))
    return {
        "class_text_available": round(text_available / class_count, 4) if class_count else 0.0,
        "interface_extracted": round(interface_count / class_count, 4) if class_count else 0.0,
    }


def _parse_root_class_from_package(package_mo_path: Path) -> str:
    try:
        text = package_mo_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return package_mo_path.parent.name
    m = _CLASS_RE.search(text)
    if m:
        return m.group(2)
    return package_mo_path.parent.name


def _fqname_from_mo_file(mo_file: Path, package_base: Path, root_class: str) -> str:
    rel = mo_file.relative_to(package_base)
    parts = list(rel.parts)
    if mo_file.name.lower() == "package.mo":
        if len(parts) == 1:
            return root_class
        return root_class + "." + ".".join(parts[:-1])
    stem = mo_file.stem
    if len(parts) == 1:
        return root_class + "." + stem
    return root_class + "." + ".".join(parts[:-1] + [stem])


def _normalize_classes_result(raw: Any, root_guess: str) -> List[str]:
    out: List[str] = []
    seen: set[str] = set()

    def add_name(name: str) -> None:
        s = str(name or "").strip()
        if not s:
            return
        # Skip obvious booleans/noise payloads.
        if s.lower() in {"true", "false", "none", "null"}:
            return
        if "." not in s and root_guess:
            if s != root_guess:
                s = f"{root_guess}.{s}"
        if s not in seen:
            seen.add(s)
            out.append(s)

    if isinstance(raw, (list, tuple, set)):
        for item in raw:
            if isinstance(item, str):
                add_name(item)
            elif isinstance(item, (list, tuple)) and item:
                add_name(str(item[0]))
            elif isinstance(item, dict):
                add_name(str(item.get("name", "") or item.get("fqname", "")))
    elif isinstance(raw, dict):
        for value in raw.values():
            if isinstance(value, (list, tuple, set)):
                for x in value:
                    add_name(str(x))
            else:
                add_name(str(value))
    elif isinstance(raw, str):
        for tok in _CLASS_TOKEN_RE.findall(raw):
            add_name(tok)

    if root_guess:
        add_name(root_guess)
    return sorted(out)


def _normalize_name_list(raw: Any) -> List[str]:
    out: List[str] = []
    seen: set[str] = set()

    def add_item(name: Any) -> None:
        s = str(name or "").strip()
        if not s:
            return
        if s not in seen:
            seen.add(s)
            out.append(s)

    if isinstance(raw, (list, tuple, set)):
        for item in raw:
            if isinstance(item, dict):
                add_item(item.get("name", "") or item.get("id", "") or item.get("fqname", ""))
            elif isinstance(item, (list, tuple)) and item:
                add_item(item[0])
            else:
                add_item(item)
    elif isinstance(raw, dict):
        for v in raw.values():
            if isinstance(v, (list, tuple, set)):
                for x in v:
                    add_item(x)
            else:
                add_item(v)
    elif isinstance(raw, str):
        for tok in re.split(r"[\s,;|]+", raw):
            add_item(tok)
    return out


def _collect_classes_recursive(
    driver: MWorksDriver,
    root_fqname: str,
    max_depth: int = 3,
    max_nodes: int = 5000,
) -> Tuple[List[str], Dict[str, List[str]], Dict[str, int]]:
    root = str(root_fqname or "").strip()
    if not root:
        return [], {}, {}
    visited: set[str] = {root}
    depth_map: Dict[str, int] = {root: 0}
    children_map: Dict[str, List[str]] = {}
    queue: List[str] = [root]

    while queue and len(visited) < max_nodes:
        cur = queue.pop(0)
        dep = depth_map.get(cur, 0)
        if dep >= max_depth:
            continue
        res = driver.get_classes(cur)
        raw = res.data if res.ok else []
        children = _normalize_classes_result(raw, cur)
        cleaned: List[str] = []
        for name in children:
            c = str(name or "").strip()
            if not c or c == cur:
                continue
            if c.startswith(cur + ".") or c == cur:
                cleaned.append(c)
            elif "." not in c:
                cleaned.append(cur + "." + c)
            else:
                cleaned.append(c)
        cleaned = sorted(set(cleaned))
        children_map[cur] = cleaned
        for child in cleaned:
            if child in visited:
                continue
            visited.add(child)
            depth_map[child] = dep + 1
            queue.append(child)
            if len(visited) >= max_nodes:
                break

    all_classes = sorted(visited)
    return all_classes, children_map, depth_map


def _export_from_mol_files_into_catalog(
    driver: MWorksDriver,
    lib_dir: Path,
    library_id: str,
    catalog: Dict[str, Any],
    warnings: List[Dict[str, Any]],
    is_default: bool,
) -> Tuple[int, str]:
    mol_files = sorted(lib_dir.rglob("*.mol"), key=lambda p: str(p).lower())
    if not mol_files:
        warnings.append({"code": "L001", "target_id": lib_dir.name, "message": "no package.mo or .mol found; skipped"})
        return 0, ""

    exported_class_count = 0
    lib_fqname = ""
    seen_fqnames: set[str] = set()
    for mol_file in mol_files:
        load_res = driver.load_file(str(mol_file))
        if not (load_res.ok and load_res.data):
            warnings.append(
                {
                    "code": "L003",
                    "target_id": lib_dir.name,
                    "message": f"OpenModelFile failed for .mol: {mol_file} => {load_res.error or 'returned false'}",
                }
            )
            continue

        root_guess = mol_file.stem
        class_names, child_map, depth_map = _collect_classes_recursive(
            driver=driver,
            root_fqname=root_guess,
            max_depth=3,
            max_nodes=5000,
        )
        if not class_names:
            class_res = driver.get_classes(root_guess)
            class_names = _normalize_classes_result(class_res.data if class_res.ok else "", root_guess)
            child_map = {}
            depth_map = {x: 0 for x in class_names}
        if not class_names:
            class_names = [root_guess]
            child_map = {}
            depth_map = {root_guess: 0}

        if not lib_fqname and class_names:
            lib_fqname = class_names[0].split(".")[0]

        # Build interface registry once per .mol for connector/parameter inheritance resolution
        iface_registry = _build_iface_registry(driver, class_names)

        for fqname in class_names:
            if fqname in seen_fqnames:
                continue
            seen_fqnames.add(fqname)
            text_res = driver.get_model_text(fqname)
            model_text = text_res.data if text_res.ok and isinstance(text_res.data, str) else ""
            parsed = _parse_model_text(model_text) if model_text else {
                "class_kind": "",
                "class_name": "",
                "extends": [],
                "imports": [],
                "parameters": [],
                "connectors": [],
            }
            help_params = []
            if not parsed.get("parameters"):
                help_params = _help_parameters_for_class(fqname=fqname, class_name=(parsed["class_name"] or fqname.split(".")[-1]))
                if help_params:
                    parsed["parameters"] = [
                        {
                            "name": str(x.get("name", "")),
                            "type": str(x.get("type", "Real")),
                            "unit": str(x.get("unit", "1")),
                            "description": str(x.get("description", "")),
                            "default": x.get("default"),
                        }
                        for x in help_params
                    ]

            # For protected .mol (no model_text) or when parameters/connectors still empty,
            # use probe-based extraction via GetComponentDescription.
            # Always probe for connectors when they are missing 鈥?MSL and .mo libs inherit
            # connectors via `extends` so _parse_model_text() finds none directly.
            if not model_text or not parsed.get("parameters"):
                mol_params, mol_connectors = _api_extract_mol(driver, fqname, iface_registry)
                if mol_params and not parsed.get("parameters"):
                    parsed["parameters"] = mol_params
                if mol_connectors and not parsed.get("connectors"):
                    parsed["connectors"] = mol_connectors
            elif not parsed.get("connectors"):
                # Has source text and parameters but no connectors 鈥?probe connectors only
                _, mol_connectors = _api_extract_mol(driver, fqname, iface_registry)
                if mol_connectors:
                    parsed["connectors"] = mol_connectors

            class_name = parsed["class_name"] or fqname.split(".")[-1]
            # If connectors were found and no explicit kind from source, treat as model
            class_kind = parsed["class_kind"] or ("model" if parsed.get("connectors") else "class")
            if class_kind not in {"package", "model", "block", "record", "connector", "class", "partial"}:
                class_kind = "class"
            class_id = _make_id("cls", f"{lib_dir.name}|{fqname}")

            desc_res = driver.get_model_description(fqname)
            model_desc = desc_res.data if desc_res.ok and isinstance(desc_res.data, str) else ""
            text_hash = hashlib.sha256(model_text.encode("utf-8")).hexdigest() if model_text else ""
            class_entry = {
                "id": class_id,
                "library_id": library_id,
                "fqname": fqname,
                "name": class_name,
                "kind": class_kind,
                "abstract": False,
                "description": model_desc or "",
                "source_ref": str(mol_file),
                "text_hash": f"sha256:{text_hash}" if text_hash else "",
                "status": "active" if is_default else "legacy",
            }
            catalog["classes"] = _upsert_by_id(catalog.get("classes", []), class_entry)

            interface_item = {
                "class_id": class_id,
                "interface_hash": f"sha256:{hashlib.sha256((json.dumps(parsed, ensure_ascii=False, sort_keys=True)).encode('utf-8')).hexdigest()}",
                "parameters": [
                    {
                        "name": p["name"],
                        "type": p["type"],
                        "unit": p["unit"],
                        "quantity_kind": _to_quantity_kind(p["unit"]),
                        "default": p["default"],
                        "required": False,
                        "range": None,
                        "enum": None,
                        "tunable": True,
                        "description": p["description"],
                    }
                    for p in parsed["parameters"]
                ],
                "connectors": [
                    {
                        "name": c["name"],
                        "direction": "inout",
                        "type": c["type"],
                        "domain": _connector_domain(c["type"], c["name"], fqname),
                        "dimension": "scalar",
                        "optional": False,
                        "description": c["description"],
                    }
                    for c in parsed["connectors"]
                ],
                "events": [],
                "annotations": {
                    "mol_source": str(mol_file),
                    "class_depth": int(depth_map.get(fqname, 0)),
                    "child_classes": child_map.get(fqname, []),
                },
            }
            if int(depth_map.get(fqname, 0)) <= 2:
                comps_res = driver.get_components(fqname)
                ports_res = driver.get_component_ports(fqname, "")
                components = _normalize_name_list(comps_res.data if comps_res.ok else [])
                ports = _normalize_name_list(ports_res.data if ports_res.ok else [])
                interface_item["annotations"]["components"] = components[:200]
                interface_item["annotations"]["component_count"] = len(components)
                interface_item["annotations"]["ports"] = ports[:200]
                interface_item["annotations"]["port_count"] = len(ports)
                if not interface_item["connectors"] and ports:
                    interface_item["connectors"] = [
                        {
                            "name": p,
                            "direction": "inout",
                            "type": "",
                            "domain": "signal",
                            "dimension": "scalar",
                            "optional": False,
                            "description": "",
                        }
                        for p in ports[:200]
                    ]
            interfaces = list(catalog.get("interfaces", []))
            interfaces = [x for x in interfaces if str(x.get("class_id", "")) != class_id]
            interfaces.append(interface_item)
            catalog["interfaces"] = interfaces

            for base in parsed["extends"]:
                rel = {
                    "id": _make_id("rel", f"{lib_dir.name}|{fqname}->extends->{base}"),
                    "from_id": class_id,
                    "to_id": _make_id("cls", f"{lib_dir.name}|{base}"),
                    "type": "extends",
                    "cardinality": "1:1",
                    "condition": None,
                }
                catalog["relations"] = _upsert_by_id(catalog.get("relations", []), rel)

            if model_text:
                art = {
                    "id": _make_id("art", f"{lib_dir.name}|{fqname}:mol_text"),
                    "class_id": class_id,
                    "kind": "source",
                    "uri": f"{mol_file}#{fqname}",
                    "sha256": text_hash,
                    "size": len(model_text.encode("utf-8")),
                    "license": None,
                }
                catalog["artifacts"] = _upsert_by_id(catalog.get("artifacts", []), art)
            exported_class_count += 1

    if exported_class_count == 0:
        warnings.append({"code": "L004", "target_id": lib_dir.name, "message": "found .mol but failed to extract classes"})
    return exported_class_count, lib_fqname


def _export_one_library_into_catalog(
    driver: MWorksDriver,
    lib_dir: Path,
    catalog: Dict[str, Any],
    warnings: List[Dict[str, Any]],
    include_non_default: bool,
    include_legacy: bool,
) -> Tuple[bool, int, str]:
    family, version = _parse_library_name_and_version(lib_dir.name)
    preferred = _PREFERRED_LIBRARY_VERSIONS.get(family, "")
    is_default = bool((not preferred) or preferred == version)
    if not include_non_default and not is_default:
        return False, 0, ""
    if not include_legacy and not is_default:
        return False, 0, ""

    library_id = _make_id("lib", lib_dir.name)
    _purge_library_from_catalog(catalog, library_id)

    lib_entry = {
        "id": library_id,
        "name": lib_dir.name,
        "fqname": lib_dir.name,
        "family": family or lib_dir.name,
        "version": version,
        "vendor": "",
        "domain_tags": [],
        "status": "active" if is_default else "legacy",
        "is_default": is_default,
        "preferred_rank": 0 if is_default else 100,
        "version_policy": "preferred_for_modeling" if is_default else "available_non_default",
        "description": f"Imported from {lib_dir}",
    }
    catalog["libraries"] = _upsert_by_id(catalog.get("libraries", []), lib_entry)

    package_candidates = sorted(lib_dir.rglob("package.mo"), key=lambda p: len(p.parts))
    if not package_candidates:
        mol_count, mol_root = _export_from_mol_files_into_catalog(
            driver=driver,
            lib_dir=lib_dir,
            library_id=library_id,
            catalog=catalog,
            warnings=warnings,
            is_default=is_default,
        )
        if mol_root:
            lib_entry["fqname"] = mol_root
            catalog["libraries"] = _upsert_by_id(catalog.get("libraries", []), lib_entry)
        return True, mol_count, library_id

    package_mo = package_candidates[0]
    root_class = _parse_root_class_from_package(package_mo)
    package_base = package_mo.parent

    load_res = driver.load_file(str(package_mo))
    if not (load_res.ok and load_res.data):
        warnings.append(
            {
                "code": "L002",
                "target_id": lib_dir.name,
                "message": f"OpenModelFile failed for package.mo: {load_res.error or 'returned false'}",
            }
        )

    lib_entry["fqname"] = root_class
    catalog["libraries"] = _upsert_by_id(catalog.get("libraries", []), lib_entry)

    exported_class_count = 0
    mo_files = sorted(package_base.rglob("*.mo"), key=lambda p: str(p).lower())
    for mo_file in mo_files:
        try:
            model_text = mo_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            model_text = ""
        parsed = _parse_model_text(model_text) if model_text else {
            "class_kind": "",
            "class_name": "",
            "extends": [],
            "imports": [],
            "parameters": [],
            "connectors": [],
        }
        fqname = _fqname_from_mo_file(mo_file, package_base, root_class)
        if not parsed.get("parameters"):
            help_params = _help_parameters_for_class(fqname=fqname, class_name=(parsed["class_name"] or mo_file.stem))
            if help_params:
                parsed["parameters"] = [
                    {
                        "name": str(x.get("name", "")),
                        "type": str(x.get("type", "Real")),
                        "unit": str(x.get("unit", "1")),
                        "description": str(x.get("description", "")),
                        "default": x.get("default"),
                    }
                    for x in help_params
                ]

        # MSL and other .mo libs often inherit connectors via `extends` rather than
        # declaring them directly, so _parse_model_text() finds 0 connectors.
        # Probe with GetComponentDescription as a fallback when connectors are missing.
        if not parsed.get("connectors"):
            _, probe_conns = _api_extract_mol(driver, fqname, {})
            if probe_conns:
                parsed["connectors"] = probe_conns

        class_name = parsed["class_name"] or mo_file.stem
        # Infer kind from connectors when source doesn't declare it explicitly
        if mo_file.name.lower() == "package.mo":
            _default_kind = "package"
        elif parsed.get("connectors"):
            _default_kind = "model"
        else:
            _default_kind = "class"
        class_kind = parsed["class_kind"] or _default_kind
        if class_kind not in {"package", "model", "block", "record", "connector", "class", "partial"}:
            class_kind = "class"
        class_id = _make_id("cls", f"{lib_dir.name}|{fqname}")

        desc_res = driver.get_model_description(fqname)
        model_desc = desc_res.data if desc_res.ok and isinstance(desc_res.data, str) else ""
        text_hash = hashlib.sha256(model_text.encode("utf-8")).hexdigest() if model_text else ""
        class_entry = {
            "id": class_id,
            "library_id": library_id,
            "fqname": fqname,
            "name": class_name,
            "kind": class_kind,
            "abstract": False,
            "description": model_desc or "",
            "source_ref": str(mo_file),
            "text_hash": f"sha256:{text_hash}" if text_hash else "",
            "status": "active" if is_default else "legacy",
        }
        catalog["classes"] = _upsert_by_id(catalog.get("classes", []), class_entry)

        interface_item = {
            "class_id": class_id,
            "interface_hash": f"sha256:{hashlib.sha256((json.dumps(parsed, ensure_ascii=False, sort_keys=True)).encode('utf-8')).hexdigest()}",
            "parameters": [
                {
                    "name": p["name"],
                    "type": p["type"],
                    "unit": p["unit"],
                    "quantity_kind": _to_quantity_kind(p["unit"]),
                    "default": p["default"],
                    "required": False,
                    "range": None,
                    "enum": None,
                    "tunable": True,
                    "description": p["description"],
                }
                for p in parsed["parameters"]
            ],
            "connectors": [
                {
                    "name": c["name"],
                    "direction": "inout",
                    "type": c["type"],
                    "domain": _connector_domain(c["type"], c["name"], fqname),
                    "dimension": "scalar",
                    "optional": False,
                    "description": c["description"],
                }
                for c in parsed["connectors"]
            ],
            "events": [],
            "annotations": {},
        }
        interfaces = list(catalog.get("interfaces", []))
        interfaces = [x for x in interfaces if str(x.get("class_id", "")) != class_id]
        interfaces.append(interface_item)
        catalog["interfaces"] = interfaces

        for base in parsed["extends"]:
            rel = {
                "id": _make_id("rel", f"{lib_dir.name}|{fqname}->extends->{base}"),
                "from_id": class_id,
                "to_id": _make_id("cls", f"{lib_dir.name}|{base}"),
                "type": "extends",
                "cardinality": "1:1",
                "condition": None,
            }
            catalog["relations"] = _upsert_by_id(catalog.get("relations", []), rel)

        if model_text:
            art = {
                "id": _make_id("art", f"{lib_dir.name}|{fqname}:mo_text"),
                "class_id": class_id,
                "kind": "mo_text",
                "uri": str(mo_file),
                "sha256": text_hash,
                "size": len(model_text.encode("utf-8")),
                "license": None,
            }
            catalog["artifacts"] = _upsert_by_id(catalog.get("artifacts", []), art)
        else:
            warnings.append({"code": "Q001", "target_id": class_id, "message": "model text unavailable"})
        exported_class_count += 1

    return True, exported_class_count, library_id
