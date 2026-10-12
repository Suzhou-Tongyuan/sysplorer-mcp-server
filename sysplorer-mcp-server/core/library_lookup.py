"""Top-level library vs class lookup — shared by docs, open, check, and load."""
from __future__ import annotations

from typing import Any, Dict, Optional

from core.tool_envelope import (
    CODE_CLASS_NOT_FOUND,
    CODE_LIBRARY_LOAD_FAILED,
    CODE_LIBRARY_NOT_INSTALLED,
    error_looks_like_library_file_missing,
    error_looks_like_library_load_failed,
)


def top_level_library_name(full_class_name: str) -> str:
    name = (full_class_name or "").strip()
    if not name:
        return ""
    return name.split(".", 1)[0].strip()


def attach_class_library_fields(
    payload: Dict[str, Any],
    full_class_name: str,
    top: str = "",
) -> Dict[str, Any]:
    name = (full_class_name or "").strip()
    lib = (top or top_level_library_name(name)).strip()
    if lib:
        payload["top_level_library"] = lib
        payload["topLevelLibrary"] = lib
    if name:
        payload.setdefault("full_class_name", name)
        payload["className"] = name
    return payload


def _class_exist_true(driver: Any, name: str) -> bool:
    fn = getattr(driver, "class_exist", None)
    if not callable(fn):
        return False
    try:
        ce = fn(name)
    except Exception:
        return False
    return bool(ce is not None and getattr(ce, "ok", False) and getattr(ce, "data", False))


def _installed_row(driver: Any, top: str) -> tuple[Optional[Dict[str, Any]], bool]:
    """Return ``(row_or_none, catalog_ok)``. ``catalog_ok`` is false when the list cannot be read."""
    getter = getattr(driver, "get_installed_libraries", None)
    if not callable(getter):
        return None, False
    try:
        listed = getter()
    except Exception:
        return None, False
    if not getattr(listed, "ok", False):
        return None, False
    raw = getattr(listed, "data", None)
    if not isinstance(raw, list):
        return None, False
    needle = (top or "").strip().lower()
    for item in raw:
        if isinstance(item, dict):
            name = str(item.get("name") or "").strip()
            if name.lower() == needle:
                return item, True
        elif str(item).strip().lower() == needle:
            return {"name": str(item).strip(), "is_load": False}, True
    return None, True


def library_workspace_status(driver: Any, top: str) -> str:
    """Return ``loaded``, ``installed``, ``absent``, or ``unknown``."""
    lib = (top or "").strip()
    if not lib:
        return "absent"
    if _class_exist_true(driver, lib):
        return "loaded"
    row, catalog_ok = _installed_row(driver, lib)
    if row is not None:
        flag = row.get("is_load")
        if flag is True or str(flag).strip().lower() in ("1", "true", "yes"):
            return "loaded"
        return "installed"
    if catalog_ok:
        return "absent"
    return "unknown"


def attach_library_diagnostics(
    payload: Dict[str, Any],
    driver: Any,
    library_name: str,
) -> Dict[str, Any]:
    """Add catalog snapshot fields: installed, version, load flag, optional path."""
    lib = (library_name or "").strip()
    row, catalog_ok = _installed_row(driver, lib)
    payload["installed"] = bool(row)
    payload["catalog_ok"] = bool(catalog_ok)
    if row:
        version = str(row.get("version") or row.get("library_version") or "").strip()
        flag = row.get("is_load", row.get("is_loaded", row.get("loaded", False)))
        payload["is_load"] = flag is True or str(flag).strip().lower() in ("1", "true", "yes")
        if version:
            payload["library_version"] = version
        for key in ("path", "library_path", "file", "file_path", "location"):
            loc = str(row.get(key) or "").strip()
            if loc:
                payload["library_path"] = loc
                break
    else:
        payload["is_load"] = False
    return payload


def classify_library_failure(driver: Any, library_name: str, error: str = "") -> str:
    """``library_not_installed`` when the file/catalog is missing; else ``library_load_failed``."""
    blob = {"error": error or ""}
    if error_looks_like_library_file_missing(blob):
        return CODE_LIBRARY_NOT_INSTALLED
    status = library_workspace_status(driver, library_name)
    if status == "absent":
        return CODE_LIBRARY_NOT_INSTALLED
    if status in ("installed", "loaded"):
        return CODE_LIBRARY_LOAD_FAILED
    if error_looks_like_library_load_failed(blob):
        return CODE_LIBRARY_LOAD_FAILED
    return CODE_LIBRARY_NOT_INSTALLED


def classify_missing_class(driver: Any, full_class_name: str) -> str:
    """``library_not_installed`` when the dotted name's top library is not in the workspace."""
    name = (full_class_name or "").strip()
    top = top_level_library_name(name)
    if not top or "." not in name:
        return CODE_CLASS_NOT_FOUND
    status = library_workspace_status(driver, top)
    if status == "loaded":
        return CODE_CLASS_NOT_FOUND
    if status in ("installed", "absent"):
        return CODE_LIBRARY_NOT_INSTALLED
    return CODE_CLASS_NOT_FOUND


def lookup_failure_payload(
    api: str,
    full_class_name: str,
    code: str,
    error: str = "",
) -> Dict[str, Any]:
    name = (full_class_name or "").strip()
    top = top_level_library_name(name)
    if code == CODE_LIBRARY_NOT_INSTALLED:
        err = error or f"top-level library {top!r} is not loaded or not installed"
    elif code == CODE_LIBRARY_LOAD_FAILED:
        err = error or f"LoadLibrary failed for cataloged library {top!r}"
    else:
        err = error or f'The model "{name}" does not exist.'
    out: Dict[str, Any] = {"ok": False, "api": api, "code": code, "error": err}
    attach_class_library_fields(out, name, top)
    return out
