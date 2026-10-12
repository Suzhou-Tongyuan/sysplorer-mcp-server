"""Model operation MCP tools: load, open, check, translate, simulate."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from mcp_instance import mcp, readonly_annotations, writable_annotations
from path_config import (
    DIAGRAM_EXPORT_TEMP_DIR,
    TEMP_CODE_FOLDER,
)
from constants import (
    commercial_lib_load_without_version,
    normalize_load_library_call,
    split_trailing_version_from_library_display_name,
)
from core.utils import (
    _json,
    _sync_load_caches,
    _extract_dep_libs,
    infer_modelica_top_class_fq_from_mo,
    looks_like_modelica_file_path,
    looks_like_qualified_class_name,
    modelica_class_name_candidates,
    modelica_load_cache_signature,
    resolve_modelica_load_target,
)
from core.library_lookup import (
    attach_class_library_fields,
    attach_library_diagnostics,
    classify_library_failure,
    classify_missing_class,
    lookup_failure_payload,
)
from core.tool_envelope import (
    CODE_CLASS_NOT_FOUND,
    CODE_LIBRARY_LOAD_FAILED,
    CODE_LIBRARY_NOT_INSTALLED,
    error_looks_like_class_not_found,
    error_looks_like_library_file_missing,
    error_looks_like_library_load_failed,
    hint_for,
)
from core.model_dependencies import (
    DEFAULT_ARCH,
    DEFAULT_BUCKET,
    dependency_download_gate,
    fetch_latest_version,
    filter_dependency_api_records,
    fill_missing_versions_from_latest,
    install_dependencies_recursive,
    merge_workspace_dependency_lock,
    normalize_dependency_records,
    read_workspace_dependency_lock,
    resolve_dependency_library_names,
)
import state as _state
from state import _get_driver
from mworks_driver import is_modelica_lite_platform
from path_config import library_download_tools_enabled


_DEPENDENCY_LIBRARY_ACTIONS = frozenset(
    {"resolve", "plan", "latest", "download", "prepare", "repair"}
)

_LIBRARY_PREPARE_TOOL = "library_prepare"
_LIBRARY_PREPARE_HINT = (
    'library_prepare(action="plan" then "prepare", dry_run=false, download_missing=true)'
)

_LOAD_LIBRARY_DOC_CORE = """Load or list locally installed libraries (Sysplorer ``LoadLibrary`` / ``GetInstalledLibraries``).

| action | required |
|--------|----------|
| ``installed`` (list) | none |
| ``load`` (default) | ``library_name``; optional ``library_version``, ``use_cache`` |

``load`` skips when ``ClassExist`` is already true (``already_loaded``).
"""

_LIBRARY_PREPARE_DOC = """modelica_lite / mols only: resolve, plan, latest, download, or prepare missing libraries.

Try ``load_library(action=load)`` first. After ``LoadLibrary`` fails, ``plan`` then
``prepare`` / ``download`` (``dry_run=false``, ``download_missing=true``); do not loop
``load``. Real download needs ``--user-workspace``.
"""


def load_library_tool_documentation(*, deps_enabled: bool = False) -> str:
    if deps_enabled:
        return (
            _LOAD_LIBRARY_DOC_CORE
            + "\nAfter ``LoadLibrary`` fails, use ``library_prepare`` (this platform only).\n"
        )
    return _LOAD_LIBRARY_DOC_CORE


def library_prepare_tool_documentation() -> str:
    return _LIBRARY_PREPARE_DOC


_LOAD_LIBRARY_ACTION_ALIASES = {
    "": "load",
    "load": "load",
    "loadlibrary": "load",
    "load_library": "load",
    "resolve": "resolve",
    "resolve_dependencies": "resolve",
    "deps": "resolve",
    "latest": "latest",
    "plan": "plan",
    "download": "download",
    "download_missing": "download",
    "prepare": "prepare",
    "repair": "repair",
    "installed": "installed",
    "list": "installed",
    "list_installed": "installed",
    "get_installed_libraries": "installed",
    "getinstalledlibraries": "installed",
}


def _load_library_installed(
    library_name: str,
    library_version: str = "",
    use_cache: bool = True,
) -> str:
    """Load an already-installed library via Sysplorer ``LoadLibrary``."""
    try:
        driver = _get_driver()
        _sync_load_caches(driver)
        lib_raw = (library_name or "").strip()
        if not lib_raw:
            return _json(
                {
                    "ok": False,
                    "tool": "load_library",
                    "manager_action": "load",
                    "api": "LoadLibrary",
                    "error": "library_name is required for action=load",
                }
            )
        ver_raw = (library_version or "").strip()
        _, trailing_ver = split_trailing_version_from_library_display_name(lib_raw)
        lib, ver_eff = normalize_load_library_call(lib_raw, ver_raw)
        ver_ignored = bool(commercial_lib_load_without_version(lib) and (ver_raw or trailing_ver))
        key = f"{lib}@{ver_eff}"
        if use_cache:
            with _state._load_cache_lock:
                cached = _state._loaded_libs_cache.get(key)
            if cached and cached.get("ok", False):
                payload = {
                    "ok": True,
                    "tool": "load_library",
                    "manager_action": "load",
                    "api": "LoadLibrary",
                    "cached": True,
                    "library_name": lib,
                }
                if ver_ignored:
                    payload["library_version_ignored"] = ver_raw
                return _json(payload)

        result = driver.load_library(library_name=lib, library_version=ver_eff)
        out = json.loads(driver.as_json(result))
        out["tool"] = "load_library"
        out["manager_action"] = "load"
        out["cached"] = False
        out["library_name"] = lib
        if ver_ignored:
            out["library_version_ignored"] = ver_raw
        if result.ok and use_cache:
            with _state._load_cache_lock:
                _state._loaded_libs_cache[key] = {"ok": True, "ts": time.time()}
        if not result.ok:
            out["code"] = classify_library_failure(driver, lib, result.error or "")
            attach_class_library_fields(out, lib, lib)
            attach_library_diagnostics(out, driver, lib)
            if is_modelica_lite_platform():
                out["platform"] = "modelica_lite"
                out["hint"] = (
                    hint_for(str(out["code"]))
                    + " modelica_lite/mols: do not infer missing libraries from "
                    "session_manager paths.dependency_download_enabled. "
                    "Call %s with library_name=%r when --user-workspace is open."
                    % (_LIBRARY_PREPARE_HINT, lib)
                )
            else:
                out["hint"] = hint_for(str(out["code"]))
        return _json(out)
    except Exception as exc:
        hint = (
            "Use load_library(action=load) for locally installed libraries. "
            "Download/prepare is not available on this platform."
        )
        if is_modelica_lite_platform():
            hint = (
                "modelica_lite/mols: after a local load failure, call %s. "
                "Silent False is a missing-library signal."
                % _LIBRARY_PREPARE_HINT
            )
        return _json(
            {
                "ok": False,
                "tool": "load_library",
                "manager_action": "load",
                "api": "LoadLibrary",
                "error": str(exc),
                "hint": hint,
            }
        )


def load_library(
    library_name: str = "",
    library_version: str = "",
    use_cache: bool = True,
    action: str = "load",
) -> str:
    """Load or list locally installed libraries (Sysplorer ``LoadLibrary`` / ``GetInstalledLibraries``)."""
    norm = _LOAD_LIBRARY_ACTION_ALIASES.get((action or "").strip().lower())
    if not norm:
        return _json(
            {
                "ok": False,
                "tool": "load_library",
                "error": f"unknown action: {action!r}",
                "hint": "Use action=load or action=installed. Parse/download is library_prepare on modelica_lite/mols.",
            }
        )
    if norm in _DEPENDENCY_LIBRARY_ACTIONS:
        if not library_download_tools_enabled():
            return _json(
                {
                    "ok": False,
                    "tool": "load_library",
                    "manager_action": norm,
                    "disabled": True,
                    "error": (
                        f"dependency action {norm!r} is unavailable outside modelica_lite/mols. "
                        "Continue with load_library(action=load) for locally installed libraries."
                    ),
                }
            )
        return _moved_action_error(
            from_tool="load_library",
            action=action,
            use=f'{_LIBRARY_PREPARE_TOOL}(action="{norm}")',
        )
    if norm == "installed":
        return _json(list_installed_libraries_payload(tool="load_library", action="installed"))
    return _load_library_installed(library_name, library_version, use_cache=use_cache)


def library_prepare(
    action: str = "plan",
    library_name: str = "",
    library_version: str = "",
    model_name: str = "",
    dependencies: Optional[List[Dict[str, Any]]] = None,
    dependency_toml_path: str = "",
    dry_run: bool = True,
    resolve_latest: bool = True,
    download_missing: bool = False,
    load_after_download: bool = False,
    refresh_after_download: bool = True,
    respect_toml_install_flags: bool = True,
    visibility: str = "",
    bucket: str = DEFAULT_BUCKET,
    arch: str = DEFAULT_ARCH,
    download_dir: str = "",
    staging_root: str = "",
    allow_elevation: bool = True,
    elevation_mode: str = "auto",
    install_helper_path: str = "",
    stop_on_error: bool = True,
) -> str:
    """modelica_lite / mols: resolve, plan, latest, download, or prepare missing libraries."""
    if not library_download_tools_enabled():
        return _json(
            {
                "ok": False,
                "tool": _LIBRARY_PREPARE_TOOL,
                "disabled": True,
                "error": (
                    "library_prepare is modelica_lite/mols only. "
                    "Use load_library(action=load) for locally installed libraries."
                ),
            }
        )
    norm = _LOAD_LIBRARY_ACTION_ALIASES.get((action or "").strip().lower())
    if norm in ("load", "installed"):
        return _moved_action_error(
            from_tool=_LIBRARY_PREPARE_TOOL,
            action=action,
            use=f'load_library(action="{norm}")',
        )
    if norm not in _DEPENDENCY_LIBRARY_ACTIONS:
        return _json(
            {
                "ok": False,
                "tool": _LIBRARY_PREPARE_TOOL,
                "error": f"unknown action: {action!r}",
                "hint": "Use: resolve, latest, plan, download, prepare. Load installed libraries with load_library.",
            }
        )
    if norm == "repair":
        return _json(
            {
                "ok": False,
                "tool": _LIBRARY_PREPARE_TOOL,
                "manager_action": norm,
                "error": "repair is pending: diagnostic version extraction rules are not implemented yet",
            }
        )
    try:
        return _json(
            _dm_prepare_dependencies(
                norm,
                model_name=model_name,
                dependencies=dependencies,
                library_name=library_name,
                library_version=library_version,
                dependency_toml_path=dependency_toml_path,
                dry_run=dry_run,
                resolve_latest=resolve_latest,
                download_missing=download_missing,
                load_after_download=load_after_download,
                refresh_after_download=refresh_after_download,
                respect_toml_install_flags=respect_toml_install_flags,
                visibility=visibility,
                bucket=bucket,
                arch=arch,
                download_dir=download_dir,
                staging_root=staging_root,
                allow_elevation=allow_elevation,
                elevation_mode=elevation_mode,
                install_helper_path=install_helper_path,
                stop_on_error=stop_on_error,
            )
        )
    except Exception as exc:
        return _json(
            {"ok": False, "tool": _LIBRARY_PREPARE_TOOL, "manager_action": norm, "error": str(exc)}
        )


def _bind_library_tools_mcp() -> None:
    load_library.__doc__ = load_library_tool_documentation(
        deps_enabled=library_download_tools_enabled()
    )
    mcp.tool(annotations=readonly_annotations())(load_library)
    if library_download_tools_enabled():
        library_prepare.__doc__ = library_prepare_tool_documentation()
        mcp.tool(annotations=writable_annotations())(library_prepare)


_bind_library_tools_mcp()


# ── Model manager: one MCP tool + Python helpers for workflow/tests ───────────


def _dm_dedupe_dependencies(dependencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen: set[Tuple[str, str]] = set()
    for dep in dependencies:
        name = str(dep.get("name") or "").strip()
        version = str(dep.get("version") or "").strip()
        if not name:
            continue
        key = (name.lower(), version)
        if key in seen:
            continue
        seen.add(key)
        item = dict(dep)
        item["name"] = name
        item["version"] = version
        out.append(item)
    return out


def _dm_input_dependencies(
    dependencies: Optional[List[Dict[str, Any]]] = None,
    library_name: str = "",
    library_version: str = "",
) -> List[Dict[str, Any]]:
    deps = normalize_dependency_records(dependencies or [], source="input")
    lib = (library_name or "").strip()
    if lib:
        deps.extend(
            normalize_dependency_records(
                [{"name": lib, "version": (library_version or "").strip()}],
                source="input",
            )
        )
    return _dm_dedupe_dependencies(deps)


def _dm_resolve_dependencies(model_name: str) -> Dict[str, Any]:
    name = (model_name or "").strip()
    if not name:
        return {
            "ok": False,
            "api": "GetModelDependencies",
            "model_name": name,
            "dependencies": [],
            "error": "model_name is required",
        }
    driver = _get_driver()
    result = driver.get_model_dependencies(name)
    raw_dependencies = normalize_dependency_records(result.data, source="sysplorer_dependency_api") if result.ok else []
    dependencies, filtered_dependencies = filter_dependency_api_records(raw_dependencies)
    payload: Dict[str, Any] = {
        "ok": result.ok,
        "api": "GetModelDependencies",
        "model_name": name,
        "dependencies": dependencies,
    }
    if filtered_dependencies:
        payload["filtered_dependencies"] = filtered_dependencies
        payload["filter_warning"] = (
            "Temporary GetModelDependencies allowlist applied; ignored non-library names before latest/download."
        )
    if result.error:
        payload["error"] = result.error
    if result.warning:
        payload["warning"] = result.warning
    return payload


def _dm_installed_key(name: str, version: str) -> str:
    return f"{str(name or '').strip().lower()}@{str(version or '').strip()}"


_LIBRARY_DESC_KEYS = ("description", "comment", "title", "info", "desc", "summary")
_LIBRARY_DESC_MAX_CHARS = 400
_LOADED_LIBRARY_DESC_FETCH_CAP = 40
_LOADED_MODEL_DESC_FETCH_CAP = 24
_LOADED_PACKAGE_EXPAND_CAP = 20
_LOADED_PACKAGE_CHILD_LIST_CAP = 80


def _clip_library_description(text: str) -> str:
    compact = " ".join(str(text or "").split())
    if len(compact) <= _LIBRARY_DESC_MAX_CHARS:
        return compact
    return compact[: _LIBRARY_DESC_MAX_CHARS - 1] + "…"


def _library_description_from_raw(raw_item: Any) -> str:
    if not isinstance(raw_item, dict):
        return ""
    for key in _LIBRARY_DESC_KEYS:
        text = str(raw_item.get(key) or "").strip()
        if text:
            return _clip_library_description(text)
    return ""


def _dm_normalize_installed_libraries(raw: Any) -> List[Dict[str, Any]]:
    if raw is None:
        return []
    if isinstance(raw, dict):
        if isinstance(raw.get("installed"), list):
            raw_items = raw.get("installed") or []
        elif isinstance(raw.get("libraries"), list):
            raw_items = raw.get("libraries") or []
        elif isinstance(raw.get("data"), list):
            raw_items = raw.get("data") or []
        else:
            raw_items = [raw]
    elif isinstance(raw, list):
        raw_items = raw
    else:
        raw_items = [raw]

    out: List[Dict[str, Any]] = []
    seen: Set[str] = set()
    for item in raw_items:
        if isinstance(item, dict):
            name = str(item.get("name") or item.get("library_name") or item.get("library") or "").strip()
            version = str(item.get("version") or item.get("library_version") or "").strip()
            is_load = bool(item.get("is_load", item.get("is_loaded", item.get("loaded", False))))
            raw_item: Any = item
            description = _library_description_from_raw(item)
        else:
            text = str(item or "").strip()
            parts = text.rsplit(" ", 1)
            name = parts[0].strip()
            version = parts[1].strip() if len(parts) == 2 else ""
            is_load = False
            raw_item = item
            description = ""
        if not name:
            continue
        key = _dm_installed_key(name, version)
        if key in seen:
            continue
        seen.add(key)
        row: Dict[str, Any] = {
            "name": name,
            "version": version,
            "is_load": is_load,
            "description": description,
            "description_source": "GetInstalledLibraries" if description else "",
            "raw": raw_item,
        }
        out.append(row)
    return out


def _dm_get_installed_libraries() -> Dict[str, Any]:
    driver = _get_driver()
    result = driver.get_installed_libraries()
    installed = _dm_normalize_installed_libraries(result.data) if result.ok else []
    payload: Dict[str, Any] = {
        "ok": result.ok,
        "api": "GetInstalledLibraries",
        "installed": installed,
        "installed_keys": [_dm_installed_key(item.get("name", ""), item.get("version", "")) for item in installed],
    }
    if result.error:
        payload["error"] = result.error
    if result.warning:
        payload["warning"] = result.warning
    return payload


def _dm_enrich_loaded_library_descriptions(installed: List[Dict[str, Any]]) -> None:
    """Fill empty descriptions for already-loaded libraries via GetModelDescription.

    Does not LoadLibrary. Official GetInstalledLibraries has no description field.
    """
    driver = _get_driver()
    fetched = 0
    for item in installed:
        if str(item.get("description") or "").strip():
            continue
        if not item.get("is_load"):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        if fetched >= _LOADED_LIBRARY_DESC_FETCH_CAP:
            item["description_source"] = "skipped_cap"
            continue
        fetched += 1
        try:
            result = driver.get_model_description(name)
        except Exception:
            continue
        text = _clip_library_description(str(result.data or "").strip()) if result.ok else ""
        if text:
            item["description"] = text
            item["description_source"] = "GetModelDescription"


def list_installed_libraries_payload(*, tool: str, action: str) -> Dict[str, Any]:
    """Public snapshot of GetInstalledLibraries for session_manager / load_library."""
    base = _dm_get_installed_libraries()
    public: List[Dict[str, Any]] = []
    for item in base.get("installed") or []:
        public.append(
            {
                "name": item.get("name", ""),
                "version": item.get("version", ""),
                "is_load": bool(item.get("is_load")),
                "description": item.get("description") or "",
                "description_source": item.get("description_source") or "",
            }
        )
    if base.get("ok"):
        _dm_enrich_loaded_library_descriptions(public)
    loaded_count = sum(1 for item in public if item.get("is_load"))
    payload: Dict[str, Any] = {
        "ok": bool(base.get("ok")),
        "tool": tool,
        "action": action,
        "api": "GetInstalledLibraries",
        "installed": public,
        "installed_count": len(public),
        "loaded_count": loaded_count,
        "note": (
            "GetInstalledLibraries returns name, version, is_load. "
            "Use is_load=false rows as candidates for load_library(action=load). "
            "Description is present only when the API includes it, or via GetModelDescription "
            "for already-loaded (is_load=true) library roots. Unloaded libraries are not loaded "
            "just to fetch descriptions; after LoadLibrary use get_lib_model_document or "
            'model_inspect(action="get_model_description").'
        ),
    }
    if tool == "load_library":
        payload["manager_action"] = "installed"
    if base.get("error"):
        payload["error"] = base["error"]
        payload["driver_error"] = base["error"]
    if base.get("warning"):
        payload["warning"] = base["warning"]
    return payload


_SYSTEM_TOP_LEVEL_MODELS = frozenset({"BaseWorkspace", "SysplorerEmbeddedCoder"})


def _normalize_loaded_model_names(raw: Any) -> List[str]:
    names: List[str] = []
    seen: set[str] = set()

    def add(value: Any) -> None:
        text = str(value or "").strip()
        if not text or text in seen:
            return
        seen.add(text)
        names.append(text)

    if raw is None:
        return names
    if isinstance(raw, dict):
        for key, val in raw.items():
            add(key)
            if isinstance(val, str) and val and val != key:
                add(val)
        return names
    if isinstance(raw, str):
        add(raw)
        return names
    if isinstance(raw, (list, tuple, set)):
        for item in raw:
            if isinstance(item, dict):
                add(item.get("name") or item.get("fqname") or item.get("id"))
            else:
                add(item)
    else:
        add(raw)
    return names


def _classify_loaded_model(name: str, installed_names: set[str]) -> str:
    if name in _SYSTEM_TOP_LEVEL_MODELS:
        return "system"
    if name.lower() in installed_names:
        return "library"
    return "user_model"


def _normalize_restriction(raw: Any) -> str:
    return str(raw or "").strip().strip("'\"").strip()


def _restriction_is_package(raw: Any) -> bool:
    return _normalize_restriction(raw).lower() == "package"


def _child_fqname(parent: str, child: str) -> str:
    parent = str(parent or "").strip()
    child = str(child or "").strip()
    if not child:
        return parent
    if not parent or child == parent or child.startswith(parent + "."):
        return child
    return f"{parent}.{child}"


_LOADED_MODELS_HOW_TO_GO_DEEPER: Dict[str, Any] = {
    "depth_this_snapshot": "top_plus_package_children",
    "get_restriction": (
        "GetRestriction(className) returns package / model / block / connector / … "
        "Only packages have a useful next GetClasses layer."
    ),
    "get_classes": (
        'model_inspect(action="get_classes", model_name="<fully.qualified.Name>"). '
        "GetClasses often returns short names; the next fully-qualified name is "
        "parent + '.' + child unless the child is already fully qualified."
    ),
    "next_layer": (
        "Pick a child fqname F from this snapshot. If you need one more layer, call "
        'model_inspect(action="get_classes", model_name=F). Stop unless GetRestriction(F) '
        "is package. Do not expand grandchildren in a loop over large libraries (e.g. Modelica.*); "
        "that freezes Sysplorer."
    ),
    "do_not": (
        "Do not recurse past package children in get_loaded_models. "
        "Do not call GetChildrenClassesInfo from MCP scripts (it prints to the command window)."
    ),
}


def list_loaded_models_payload(*, tool: str, action: str) -> Dict[str, Any]:
    """Top-level ``GetClasses("")`` plus one package child layer (no grandchildren)."""
    driver = _get_driver()
    classes = driver.get_classes("")
    names = _normalize_loaded_model_names(classes.data) if classes.ok else []
    installed_names: set[str] = set()
    try:
        installed = _dm_get_installed_libraries()
        if installed.get("ok"):
            installed_names = {
                str(item.get("name") or "").strip().lower()
                for item in (installed.get("installed") or [])
                if str(item.get("name") or "").strip()
            }
    except Exception:
        installed_names = set()

    get_restriction = getattr(driver, "get_restriction", None)
    restriction_available = callable(get_restriction)

    models: List[Dict[str, Any]] = []
    desc_fetched = 0
    packages_expanded = 0
    packages_skipped_cap = 0
    warnings: List[str] = []
    if classes.warning:
        warnings.append(str(classes.warning))

    for name in names:
        row: Dict[str, Any] = {
            "name": name,
            "kind": _classify_loaded_model(name, installed_names),
            "restriction": "",
            "description": "",
            "description_source": "",
            "children": [],
            "child_count": 0,
            "children_truncated": False,
            "package_expanded": False,
        }
        if desc_fetched < _LOADED_MODEL_DESC_FETCH_CAP:
            desc_fetched += 1
            try:
                desc_r = driver.get_model_description(name)
            except Exception:
                desc_r = None
            text = (
                _clip_library_description(str(desc_r.data or "").strip())
                if desc_r is not None and desc_r.ok
                else ""
            )
            if text:
                row["description"] = text
                row["description_source"] = "GetModelDescription"
        else:
            row["description_source"] = "skipped_cap"

        restriction_raw: Any = ""
        if restriction_available:
            try:
                rest_r = get_restriction(name)
            except Exception:
                rest_r = None
            if rest_r is not None and rest_r.ok:
                restriction_raw = rest_r.data
                row["restriction"] = _normalize_restriction(restriction_raw)
                if rest_r.warning:
                    warnings.append(str(rest_r.warning))
            elif rest_r is not None and rest_r.warning:
                warnings.append(str(rest_r.warning))
        else:
            row["restriction_source"] = "GetRestriction_unavailable"

        if _restriction_is_package(restriction_raw) and row["kind"] == "system":
            row["expand_skipped"] = "system_root"
        elif _restriction_is_package(restriction_raw):
            if packages_expanded >= _LOADED_PACKAGE_EXPAND_CAP:
                packages_skipped_cap += 1
                row["expand_skipped"] = "package_expand_cap"
            else:
                try:
                    child_r = driver.get_classes(name)
                except Exception:
                    child_r = None
                if child_r is not None and child_r.ok:
                    child_names = _normalize_loaded_model_names(child_r.data)
                    truncated = len(child_names) > _LOADED_PACKAGE_CHILD_LIST_CAP
                    shown = child_names[:_LOADED_PACKAGE_CHILD_LIST_CAP]
                    row["children"] = [
                        {"name": child, "fqname": _child_fqname(name, child)} for child in shown
                    ]
                    row["child_count"] = len(child_names)
                    row["children_truncated"] = truncated
                    row["package_expanded"] = True
                    packages_expanded += 1
                    if child_r.warning:
                        warnings.append(str(child_r.warning))
                elif child_r is not None:
                    row["expand_skipped"] = child_r.error or "GetClasses_failed"
                    if child_r.warning:
                        warnings.append(str(child_r.warning))

        models.append(row)

    user_count = sum(1 for item in models if item.get("kind") == "user_model")
    payload: Dict[str, Any] = {
        "ok": bool(classes.ok),
        "tool": tool,
        "action": action,
        "api": "GetClasses",
        "depth": "top_plus_package_children",
        "models": models,
        "model_count": len(models),
        "user_model_count": user_count,
        "packages_expanded": packages_expanded,
        "packages_skipped_expand_cap": packages_skipped_cap,
        "package_expand_cap": _LOADED_PACKAGE_EXPAND_CAP,
        "package_child_list_cap": _LOADED_PACKAGE_CHILD_LIST_CAP,
        "how_to_go_deeper": _LOADED_MODELS_HOW_TO_GO_DEEPER,
        "note": (
            'Default snapshot: GetClasses("") (model-browser roots) plus GetClasses(name) only when '
            "GetRestriction(name) is package (system roots such as BaseWorkspace are listed but not expanded). "
            "Description is GetModelDescription on top-level names only (capped). "
            "Avoid GetChildrenClassesInfo; it prints to the Sysplorer command window."
        ),
    }
    if tool == "model_manager":
        payload["manager_action"] = "get_loaded_models"
    if not restriction_available:
        payload["restriction_available"] = False
        payload["note"] = (
            payload["note"]
            + " GetRestriction is unavailable on this driver; package children were not expanded."
        )
    if not classes.ok:
        payload["error"] = classes.error or "GetClasses returned no top-level list"
        payload["driver_error"] = payload["error"]
    if warnings:
        payload["warning"] = "; ".join(dict.fromkeys(warnings))
    return payload


def _dm_build_plan(
    dependencies: List[Dict[str, Any]],
    respect_toml_install_flags: bool = True,
    installed_keys: Optional[Set[str]] = None,
    installed_by_key: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    actions: List[Dict[str, Any]] = []
    installed_key_set = {str(key).strip().lower() for key in (installed_keys or set()) if str(key).strip()}
    installed_lookup = installed_by_key or {}
    ok = True
    for dep in dependencies:
        name = str(dep.get("name") or "").strip()
        version = str(dep.get("version") or "").strip()
        install_flag = dep.get("install", True)
        key = f"{name}@{version}" if version else name
        installed_key = _dm_installed_key(name, version) if version else ""
        if respect_toml_install_flags and install_flag is False:
            actions.append(
                {
                    "key": key,
                    "name": name,
                    "version": version,
                    "action": "skip",
                    "reason": "install=false",
                    "dependency": dep,
                }
            )
            continue
        if installed_key and installed_key in installed_key_set:
            actions.append(
                {
                    "key": key,
                    "name": name,
                    "version": version,
                    "action": "skip",
                    "reason": "already_installed",
                    "installed_source": "GetInstalledLibraries",
                    "installed": installed_lookup.get(installed_key),
                    "dependency": dep,
                }
            )
            continue
        if not version:
            ok = False
            actions.append(
                {
                    "key": key,
                    "name": name,
                    "version": version,
                    "action": "blocked",
                    "reason": "missing_version",
                    "dependency": dep,
                }
            )
            continue
        actions.append(
            {
                "key": key,
                "name": name,
                "version": version,
                "action": "install_if_missing",
                "reason": "模型库未安装",
                "dependency": dep,
            }
        )
    return {"ok": ok, "actions": actions}


def _dm_prepare_dependencies(
    action: str,
    model_name: str = "",
    dependencies: Optional[List[Dict[str, Any]]] = None,
    library_name: str = "",
    library_version: str = "",
    dependency_toml_path: str = "",
    dry_run: bool = True,
    resolve_latest: bool = True,
    download_missing: bool = False,
    load_after_download: bool = False,
    refresh_after_download: bool = True,
    respect_toml_install_flags: bool = True,
    visibility: str = "",
    bucket: str = DEFAULT_BUCKET,
    arch: str = DEFAULT_ARCH,
    download_dir: str = "",
    staging_root: str = "",
    allow_elevation: bool = True,
    elevation_mode: str = "auto",
    install_helper_path: str = "",
    stop_on_error: bool = True,
) -> Dict[str, Any]:
    norm = (action or "").strip().lower()
    tool = _LIBRARY_PREPARE_TOOL
    warnings: List[str] = []
    if norm in ("download", "prepare") and bool(download_missing) and not bool(dry_run):
        gate = dependency_download_gate()
        if not gate.get("enabled"):
            return {
                "ok": False,
                "tool": tool,
                "manager_action": norm,
                "dry_run": bool(dry_run),
                "dependency_download_gate": gate,
                "install": {
                    "attempted": False,
                    "reason": gate.get("reason", "dependency download/install is disabled"),
                },
                "warnings": warnings,
            }
    deps = _dm_input_dependencies(dependencies, library_name, library_version)
    resolved: Dict[str, Any] = {
        "ok": True,
        "api": "GetModelDependencies",
        "model_name": (model_name or "").strip(),
        "dependencies": [],
    }

    if (model_name or "").strip():
        resolved = _dm_resolve_dependencies(model_name)
        if not resolved.get("ok"):
            response = {
                "ok": False,
                "tool": tool,
                "manager_action": norm,
                "resolve": resolved,
                "error": resolved.get("error", "GetModelDependencies failed"),
                "warnings": warnings,
            }
            if stop_on_error:
                return response
            warnings.append("GetModelDependencies failed; continuing with explicit input dependencies only")
        else:
            deps = _dm_dedupe_dependencies(list(resolved.get("dependencies") or []) + deps)

    toml_path = Path(dependency_toml_path).resolve() if (dependency_toml_path or "").strip() else None
    toml = read_workspace_dependency_lock(toml_path)
    if toml.get("ok"):
        merged = merge_workspace_dependency_lock(deps, list(toml.get("dependencies") or []))
        deps = _dm_dedupe_dependencies(list(merged.get("dependencies") or []))
        for w in toml.get("warnings") or []:
            text = str(w).strip()
            if text:
                warnings.append(text)
    else:
        msg = f"TOML dependency lock failed: {toml.get('error', '')}"
        if stop_on_error:
            return {
                "ok": False,
                "tool": tool,
                "manager_action": norm,
                "resolve": resolved,
                "toml_merge": toml,
                "error": msg,
                "warnings": warnings,
            }
        warnings.append(msg)

    name_resolution = resolve_dependency_library_names(deps)
    deps = _dm_dedupe_dependencies(list(name_resolution.get("dependencies") or []))
    if not name_resolution.get("ok"):
        # Soft-skip unknown catalog names (MOLS Manifest noise); still hard-fail on ambiguity
        # or when every remaining dependency failed resolution.
        errors = list(name_resolution.get("errors") or [])
        ambiguous = [e for e in errors if e.get("status") == "ambiguous_library_name"]
        unknown = [e for e in errors if e.get("status") != "ambiguous_library_name"]
        if unknown:
            skipped_names = sorted(
                {
                    str(e.get("input_name") or "").strip()
                    for e in unknown
                    if str(e.get("input_name") or "").strip()
                }
            )
            if skipped_names:
                warnings.append(
                    "skipped non-downloadable dependency names: " + ", ".join(skipped_names)
                )
            deps = [
                d
                for d in deps
                if bool((d.get("library_name_resolution") or {}).get("ok"))
                or not str(d.get("name") or "").strip()
            ]
            name_resolution = dict(name_resolution)
            name_resolution["ok"] = not bool(ambiguous) and (
                bool(deps) or not bool(errors)
            )
            name_resolution["skipped_unknown"] = unknown
        if ambiguous or (not name_resolution.get("ok") and not deps):
            response = {
                "ok": False,
                "tool": tool,
                "manager_action": norm,
                "dry_run": bool(dry_run),
                "resolve": resolved,
                "toml_merge": toml,
                "library_name_resolution": name_resolution,
                "dependencies": deps,
                "error": "library name is not in downloadable catalog or is ambiguous",
                "warnings": warnings,
            }
            if stop_on_error:
                return response
            warnings.append("library name resolution failed for one or more dependencies")
        elif toml.get("warnings"):
            warnings.extend([str(w) for w in (toml.get("warnings") or []) if str(w).strip()])
    elif toml.get("warnings"):
        warnings.extend([str(w) for w in (toml.get("warnings") or []) if str(w).strip()])

    if norm == "resolve":
        return {
            "ok": bool(resolved.get("ok")) and bool(toml.get("ok")),
            "tool": tool,
            "manager_action": norm,
            "resolve": resolved,
            "toml_merge": toml,
            "library_name_resolution": name_resolution,
            "dependencies": deps,
            "warnings": warnings,
        }

    if norm == "latest":
        latest_items: Dict[str, Any] = {}
        ok = True
        for dep in deps:
            name = str(dep.get("name") or "").strip()
            if not name:
                continue
            latest = fetch_latest_version(name, visibility=(visibility or None), bucket=bucket or DEFAULT_BUCKET)
            latest_items[name] = latest
            ok = ok and bool(latest.get("ok"))
        return {
            "ok": ok,
            "tool": tool,
            "manager_action": norm,
            "resolve": resolved,
            "toml_merge": toml,
            "library_name_resolution": name_resolution,
            "latest": latest_items,
            "dependencies": deps,
            "warnings": warnings,
        }

    latest_result = (
        fill_missing_versions_from_latest(deps, visibility=(visibility or None), bucket=bucket or DEFAULT_BUCKET)
        if resolve_latest
        else {"ok": True, "dependencies": deps, "latest": {}, "skipped": True}
    )
    deps_with_versions = _dm_dedupe_dependencies(list(latest_result.get("dependencies") or []))
    installed = _dm_get_installed_libraries()
    if not installed.get("ok"):
        msg = f"GetInstalledLibraries failed: {installed.get('error', '')}"
        if stop_on_error:
            return {
                "ok": False,
                "tool": tool,
                "manager_action": norm,
                "dry_run": bool(dry_run),
                "resolve": resolved,
                "toml_merge": toml,
                "library_name_resolution": name_resolution,
                "latest": latest_result,
                "installed": installed,
                "error": msg,
                "warnings": warnings,
            }
        warnings.append(msg)
    installed_keys = {str(key).strip().lower() for key in installed.get("installed_keys", []) if str(key).strip()}
    installed_by_key = {
        _dm_installed_key(item.get("name", ""), item.get("version", "")): item
        for item in installed.get("installed", [])
        if item.get("name") and item.get("version")
    }
    plan = _dm_build_plan(
        deps_with_versions,
        respect_toml_install_flags=respect_toml_install_flags,
        installed_keys=installed_keys,
        installed_by_key=installed_by_key,
    )
    response: Dict[str, Any] = {
        "ok": bool(latest_result.get("ok")) and bool(plan.get("ok")) and bool(toml.get("ok")) and bool(installed.get("ok")),
        "tool": tool,
        "manager_action": norm,
        "dry_run": bool(dry_run),
        "resolve": resolved,
        "toml_merge": toml,
        "library_name_resolution": name_resolution,
        "latest": latest_result,
        "installed": installed,
        "plan": plan,
        "warnings": warnings,
    }
    if norm == "plan":
        return response

    should_install = norm in ("download", "prepare") and bool(download_missing) and not bool(dry_run)
    if not should_install:
        response["install"] = {
            "attempted": False,
            "reason": "set dry_run=false and download_missing=true to install dependencies",
        }
        return response

    install_inputs = [
        {"name": item.get("name", ""), "version": item.get("version", "")}
        for item in plan.get("actions", [])
        if item.get("action") == "install_if_missing"
    ]
    install_root = Path(download_dir).resolve() if (download_dir or "").strip() else None
    stage_root = Path(staging_root).resolve() if (staging_root or "").strip() else None
    helper = Path(install_helper_path).resolve() if (install_helper_path or "").strip() else None
    install_result = install_dependencies_recursive(
        install_inputs,
        dest_dir=install_root,
        staging_root=stage_root,
        allow_elevation=allow_elevation,
        elevation_mode=elevation_mode,
        helper_path=helper,
        visibility=(visibility or None),
        arch=arch or DEFAULT_ARCH,
        bucket=bucket or DEFAULT_BUCKET,
        dry_run=False,
        stop_on_error=stop_on_error,
        installed_keys=installed_keys,
    )
    response["download"] = {
        "attempted": True,
        "note": "download is part of install",
        "results": install_result.get("results", {}),
    }
    response["install"] = install_result
    response["ok"] = bool(response.get("ok")) and bool(install_result.get("ok"))

    if norm in ("download", "prepare") and refresh_after_download:
        driver = _get_driver()
        refresh = driver.update_library()
        response["refresh"] = json.loads(driver.as_json(refresh))
        if not refresh.ok:
            response["refresh"]["warning"] = "UpdateLibrary returned False or failed; no detailed diagnostics are available"

    if norm == "prepare" and load_after_download:
        driver = _get_driver()
        load_results: Dict[str, Any] = {}
        for item in install_inputs:
            name = item.get("name", "")
            version = item.get("version", "")
            key = f"{name}@{version}"
            result = driver.load_library(name, version)
            load_results[key] = json.loads(driver.as_json(result))
            if not result.ok and stop_on_error:
                response["ok"] = False
                break
        response["load"] = {"attempted": True, "results": load_results}
    elif norm == "prepare":
        response["load"] = {"attempted": False, "reason": "load_after_download=false"}

    return response


def _mm_attach_action(raw: str, action: str) -> str:
    """Merge manager_action into JSON response from driver helpers."""
    try:
        payload = json.loads(raw)
        if isinstance(payload, dict):
            payload["manager_action"] = action
        return _json(payload) if isinstance(payload, dict) else json.dumps(payload, ensure_ascii=False)
    except Exception:
        return raw


def _class_confirmed_missing(driver: Any, name: str) -> bool:
    """True only when official ClassExist succeeded and returned false."""
    class_exist = getattr(driver, "class_exist", None)
    if not callable(class_exist):
        return False
    try:
        ce = class_exist(name)
    except Exception:
        return False
    return bool(ce is not None and ce.ok and ce.data is False)


def _class_not_found_payload(api: str, name: str) -> Dict[str, Any]:
    return lookup_failure_payload(api, name, CODE_CLASS_NOT_FOUND)


def _lookup_fail_payload(driver: Any, api: str, name: str, error: str = "") -> Dict[str, Any]:
    code = classify_missing_class(driver, name)
    return lookup_failure_payload(api, name, code, error)


def _mark_class_not_found(payload: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(payload)
    out["ok"] = False
    out["code"] = CODE_CLASS_NOT_FOUND
    return out


def _mark_lookup_failure(driver: Any, payload: Dict[str, Any], name: str) -> Dict[str, Any]:
    out = dict(payload)
    out["ok"] = False
    if error_looks_like_library_file_missing(out) or error_looks_like_library_load_failed(out):
        top = str(out.get("topLevelLibrary") or name.split(".", 1)[0] if name else "")
        out["code"] = classify_library_failure(driver, top, str(out.get("error") or ""))
        attach_library_diagnostics(out, driver, top)
    else:
        out["code"] = classify_missing_class(driver, name)
    attach_class_library_fields(out, name)
    return out


def _mm_open(model_name: str) -> str:
    name = (model_name or "").strip()
    if looks_like_modelica_file_path(name):
        return _json(
            {
                "ok": False,
                "api": "OpenModel",
                "error": (
                    "action=open 的 model_name 必须是已加载类的全限定名，不能是 .mo 路径。"
                    "请改用 action=load_file 并传 file_path。"
                ),
                "hint": 'model_manager(action="load_file", file_path=...)',
            }
        )
    try:
        driver = _get_driver()
        if _class_confirmed_missing(driver, name):
            return _json(_lookup_fail_payload(driver, "OpenModel", name))
        result = driver.open_model(model_name=name)
        payload = result.to_dict() if hasattr(result, "to_dict") else {"ok": bool(getattr(result, "ok", False))}
        if not payload.get("ok") and (
            error_looks_like_library_file_missing(payload)
            or error_looks_like_library_load_failed(payload)
            or error_looks_like_class_not_found(payload)
        ):
            return _json(_mark_lookup_failure(driver, payload, name))
        return driver.as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "OpenModel", "error": str(exc)})


def _mm_new(model_name: str, restriction: str = "model") -> str:
    try:
        result = _get_driver().new_model(model_name=model_name, restriction=restriction)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "NewModel", "error": str(exc)})


def _mm_load_file(
    file_path: str,
    model_name: str = "",
    auto_load_deps: bool = True,
    skip_if_unchanged: bool = True,
    force_reload: bool = False,
    prepare_dependencies: bool = True,
    dependency_toml_path: str = "",
    dependency_dry_run: bool = False,
    download_missing_deps: bool = True,
    refresh_libraries_after_download: bool = True,
    load_dependencies_after_download: bool = True,
    respect_toml_install_flags: bool = True,
    stop_on_dep_error: bool = False,
    dependency_download_dir: str = "",
    dependency_staging_root: str = "",
    allow_dependency_elevation: bool = True,
    dependency_elevation_mode: str = "auto",
    dependency_install_helper_path: str = "",
) -> str:
    try:
        raw_fp = (file_path or "").strip()
        if raw_fp and looks_like_qualified_class_name(raw_fp) and not Path(raw_fp).exists():
            return _json(
                {
                    "ok": False,
                    "api": "OpenModelFile",
                    "error": (
                        "action=load_file 的 file_path 必须是磁盘上的 .mo/.mol 路径。"
                        f"{raw_fp!r} 看起来像类全名。打开已加载模型请用 action=open，model_name={raw_fp!r}。"
                    ),
                    "hint": f'model_manager(action="open", model_name="{raw_fp}")',
                }
            )
        requested = Path(file_path).resolve()
        load_target = resolve_modelica_load_target(requested)
        resolved = load_target.load_path
        file_key = str(requested)
        load_key = str(resolved)
        signature = modelica_load_cache_signature(load_target)
        driver = _get_driver()
        _sync_load_caches(driver)
        explicit_model_name = (model_name or "").strip()
        prepare_dependencies_requested = bool(prepare_dependencies) and library_download_tools_enabled()
        dependency_gate = dependency_download_gate() if prepare_dependencies_requested else {"enabled": False}
        prepare_dependencies_enabled = bool(prepare_dependencies_requested and dependency_gate.get("enabled"))
        inferred_model_name = ""
        if not explicit_model_name:
            # Prefer the caller's model file for FQ inference; fall back to package root name.
            inferred_model_name = (
                infer_modelica_top_class_fq_from_mo(requested)
                or load_target.root_package_name
                or requested.stem
            )
        dependency_model_name = explicit_model_name or inferred_model_name
        class_name = dependency_model_name or requested.stem
        prepare_after_load = bool(prepare_dependencies_enabled and dependency_model_name)

        if force_reload:
            with _state._load_cache_lock:
                _state._loaded_file_cache.pop(file_key, None)
                if load_key != file_key:
                    _state._loaded_file_cache.pop(load_key, None)

        dep_results: Dict[str, Any] = {}
        dependency_prepare_meta: Optional[Dict[str, Any]] = None
        if prepare_dependencies_requested and not prepare_dependencies_enabled:
            dependency_prepare_meta = {
                "attempted": False,
                "reason": dependency_gate.get("reason", "dependency download/install is disabled"),
                "dependency_download_gate": dependency_gate,
            }

        def _attach_load_target(payload: Dict[str, Any]) -> Dict[str, Any]:
            payload["file_path"] = file_key
            payload["load_path"] = load_key
            if load_target.redirected_to_package:
                payload["load_target"] = load_target.to_public_dict()
            return payload

        if not force_reload and skip_if_unchanged:
            with _state._load_cache_lock:
                cached = _state._loaded_file_cache.get(file_key)
            if cached and cached.get("ok", False) and cached.get("signature") == signature:
                payload = _attach_load_target(
                    {"ok": True, "api": "OpenModelFile", "cached": True}
                )
                if prepare_after_load:
                    dependency_prepare_meta = _dm_prepare_dependencies(
                        "prepare",
                        model_name=dependency_model_name,
                        dependency_toml_path=dependency_toml_path,
                        dry_run=dependency_dry_run,
                        resolve_latest=True,
                        download_missing=download_missing_deps,
                        load_after_download=load_dependencies_after_download,
                        refresh_after_download=refresh_libraries_after_download,
                        respect_toml_install_flags=respect_toml_install_flags,
                        download_dir=dependency_download_dir,
                        stop_on_error=stop_on_dep_error,
                    )
                    dependency_prepare_meta["timing"] = "after_cached_open_model_file"
                    if inferred_model_name:
                        dependency_prepare_meta["inferred_model_name"] = inferred_model_name
                    payload["dependency_prepare"] = dependency_prepare_meta
                elif dependency_prepare_meta is not None:
                    payload["dependency_prepare"] = dependency_prepare_meta
                return _json(payload)

        unload_meta: Optional[Dict[str, Any]] = None
        if force_reload:
            # Unload by requested path so erase_candidates resolves the package root once.
            ur = driver.unload_loaded_classes_for_mo(str(requested))
            unload_meta = json.loads(driver.as_json(ur))
            if not ur.ok:
                return _json(
                    _attach_load_target(
                        {
                            "ok": False,
                            "api": "OpenModelFile",
                            "error": ur.error,
                            "unload_loaded_classes_for_mo": unload_meta,
                        }
                    )
                )

        ar: Optional[bool] = True if force_reload else None
        result = driver.load_file(load_key, auto_reload=ar)
        out = _attach_load_target(json.loads(driver.as_json(result)))
        out["cached"] = False
        if not result.ok and (
            error_looks_like_library_file_missing(out) or error_looks_like_library_load_failed(out)
        ):
            top = (dependency_model_name or "").split(".", 1)[0].strip()
            out["code"] = classify_library_failure(driver, top, str(out.get("error") or ""))
            if dependency_model_name:
                attach_class_library_fields(out, dependency_model_name)
            if top:
                attach_library_diagnostics(out, driver, top)

        if prepare_after_load and result.ok:
            dependency_prepare_meta = _dm_prepare_dependencies(
                "prepare",
                model_name=dependency_model_name,
                dependency_toml_path=dependency_toml_path,
                dry_run=dependency_dry_run,
                resolve_latest=True,
                download_missing=download_missing_deps,
                load_after_download=load_dependencies_after_download,
                refresh_after_download=refresh_libraries_after_download,
                respect_toml_install_flags=respect_toml_install_flags,
                download_dir=dependency_download_dir,
                staging_root=dependency_staging_root,
                allow_elevation=allow_dependency_elevation,
                elevation_mode=dependency_elevation_mode,
                install_helper_path=dependency_install_helper_path,
                stop_on_error=stop_on_dep_error,
            )
            dependency_prepare_meta["timing"] = "after_open_model_file"
            dependency_prepare_meta["inferred_model_name"] = dependency_model_name
            if not dependency_prepare_meta.get("ok") and stop_on_dep_error:
                out["ok"] = False
                out["error"] = "dependency prepare failed"
            elif not dependency_dry_run:
                reload_after_deps = driver.load_file(load_key, auto_reload=True)
                out["reload_after_dependency_prepare"] = json.loads(driver.as_json(reload_after_deps))
                if not reload_after_deps.ok and stop_on_dep_error:
                    out["ok"] = False
                    out["error"] = reload_after_deps.error or "reload after dependency prepare failed"
        elif prepare_dependencies_enabled and not dependency_model_name:
            out["dependency_prepare"] = {
                "attempted": False,
                "reason": "model_name was not provided and could not be inferred from the .mo file",
            }

        # Prefer uses()/deps from package root when redirected; fall back to requested file.
        dep_scan_path = load_key if load_target.redirected_to_package else file_key
        if auto_load_deps and not prepare_dependencies_requested:
            deps = _extract_dep_libs(dep_scan_path)
            for lib_fqname in deps:
                lib_key = f"{lib_fqname}@"
                use_cached = False
                with _state._load_cache_lock:
                    if _state._loaded_libs_cache.get(lib_key, {}).get("ok", False):
                        use_cached = True
                if use_cached:
                    dep_results[lib_fqname] = {"ok": True, "error": "", "cached": True}
                    continue
                r = driver.load_library(library_name=lib_fqname)
                dep_results[lib_fqname] = {"ok": r.ok, "error": r.error if not r.ok else "", "cached": False}
                if r.ok:
                    with _state._load_cache_lock:
                        _state._loaded_libs_cache[lib_key] = {"ok": True, "ts": time.time()}
        elif auto_load_deps and prepare_dependencies_requested:
            out["auto_load_deps"] = {
                "attempted": False,
                "reason": (
                    "skipped legacy regex LoadLibrary because dependency download/install is disabled"
                    if not prepare_dependencies_enabled
                    else "skipped legacy regex LoadLibrary because prepare_dependencies handles dependency download/load after OpenModelFile"
                ),
            }

        if unload_meta is not None:
            out["unload_loaded_classes_for_mo"] = unload_meta
        if dep_results:
            out["auto_loaded_libs"] = dep_results
        if dependency_prepare_meta is not None:
            out["dependency_prepare"] = dependency_prepare_meta
        if result.ok:
            with _state._load_cache_lock:
                cache_row = {
                    "ok": True,
                    "signature": signature,
                    "auto_loaded_libs": dep_results,
                    "dependency_model_name": dependency_model_name,
                    "class_name": class_name,
                    "load_path": load_key,
                    "ts": time.time(),
                }
                _state._loaded_file_cache[file_key] = cache_row
                if load_key != file_key:
                    _state._loaded_file_cache[load_key] = dict(cache_row)
        return _json(out)

    except Exception as exc:
        return _json({"ok": False, "api": "loadFile", "error": str(exc)})


def _normalize_unload_class_name(model_name: str) -> str:
    """Accept a class FQ name; unwrap accidental quotes or EraseClasses tuple text."""
    raw = (model_name or "").strip()
    m = re.match(r"^\(\s*['\"]([^'\"]+)['\"]\s*,?\s*\)$", raw)
    if m:
        return m.group(1).strip()
    m = re.match(r"^['\"]([^'\"]+)['\"]$", raw)
    if m:
        return m.group(1).strip()
    return raw


def _mm_unload(model_name: str) -> str:
    name = _normalize_unload_class_name(model_name)
    if looks_like_modelica_file_path(name):
        return _json(
            {
                "ok": False,
                "api": "EraseClasses",
                "error": (
                    "action=unload 的 model_name 必须是已加载类的全限定名（MCP 会包装成 EraseClasses 元组），"
                    "不能传 .mo 路径。"
                ),
            }
        )
    try:
        result = _get_driver().unload_file(name)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "unloadFile", "error": str(exc)})


def _mm_get_last_errors() -> str:
    try:
        result = _get_driver().get_last_errors()
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetLastErrors", "error": str(exc)})


def _mm_save(
    model_name: str,
    folder: str = "",
    save_type: int = 0,
    save_as: bool = False,
) -> str:
    name = (model_name or "").strip()
    dest = (folder or "").strip()
    try:
        driver = _get_driver()
        origin = _user_mo_path_for_layout(name) if not save_as and not dest else ""
        if origin:
            result = driver.save_loaded_model(name, saved_path=origin)
            return driver.as_json(result)
        result = driver.save_model(name, folder=dest, save_type=save_type)
        if not save_as and not dest:
            note = (
                "No originating file in this session; first persist used SaveModelAs. "
                "Use save after load_file to overwrite that path; use save_as for a copy."
            )
            if result.warning:
                result.warning = f"{result.warning} {note}".strip()
            else:
                result.warning = note
        return driver.as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "SaveModelAs" if save_as or dest else "SaveModel", "error": str(exc)})


def _mm_lookup_component(model_name: str, comp_name: str, info_type: str = "") -> str:
    try:
        result = _get_driver().lookup_component(model_name, comp_name, info_type=info_type)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "lookupComp", "error": str(exc)})


def _mm_get_components(model_name: str, component: str = "") -> str:
    try:
        result = _get_driver().get_components(model_name, component=component)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetComponents", "error": str(exc)})


def _mm_get_component_type_name(
    model_name: str,
    component_name: str,
    full_name: bool = False,
) -> str:
    try:
        result = _get_driver().get_component_type_name(
            model_name, component_name, full_name=bool(full_name)
        )
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetComponentTypeName", "error": str(exc)})


def _prefix_instance_ports(component_name: str, ports: Any) -> List[str]:
    inst = (component_name or "").strip()
    out: List[str] = []
    if not isinstance(ports, (list, tuple)):
        return out
    for item in ports:
        name = str(item).strip()
        if not name:
            continue
        if not inst or name == inst or name.startswith(inst + "."):
            out.append(name)
        else:
            out.append(f"{inst}.{name}")
    return out


def _mm_get_component_ports(model_name: str, component_name: str, port_direction: int = 0) -> str:
    name = (model_name or "").strip()
    inst = (component_name or "").strip()
    if not name:
        return _json({"ok": False, "api": "GetComponentPorts", "error": "model_name is required"})
    try:
        driver = _get_driver()
        open_warning = ""
        om = driver.open_model(model_name=name)
        if not om.ok:
            open_warning = om.error or "OpenModel failed"

        result = driver.get_component_ports(
            model_name=name,
            component_name=inst,
            port_direction=int(port_direction),
        )
        payload = json.loads(driver.as_json(result))
        ports = payload.get("data")
        if isinstance(ports, list) and ports:
            payload["strategy"] = "instance"
            if open_warning:
                payload["warning_open_model"] = open_warning
            return _json(payload)

        fallback_type = ""
        fallback_ports: List[str] = []
        if inst:
            type_res = driver.get_component_type_name(name, inst, True)
            fallback_type = str(getattr(type_res, "data", "") or "").strip()
            if type_res.ok and fallback_type:
                class_res = driver.get_component_ports(
                    model_name=fallback_type,
                    component_name="",
                    port_direction=int(port_direction),
                )
                if class_res.ok:
                    fallback_ports = _prefix_instance_ports(inst, class_res.data)

        if fallback_ports:
            payload["ok"] = True
            payload["data"] = fallback_ports
            payload["variable_count"] = len(fallback_ports)
            payload["strategy"] = "class_connectors"
            payload["fallback_from"] = "GetComponentPorts"
            payload["component_type"] = fallback_type
            payload["hint"] = (
                "Official GetComponentPorts on the instance was empty; "
                "listed connectors from the component type instead."
            )
            if open_warning:
                payload["warning_open_model"] = open_warning
            return _json(payload)

        payload["data"] = []
        payload["strategy"] = "instance"
        payload["hint"] = (
            "Official GetComponentPorts returned []. Empty is the official miss: "
            "model not open, name is not a component, no diagram ports, or "
            "port_direction 1/2 on undirected connectors (use 0). "
            "Library classes: model_name=type, component_name empty."
        )
        if fallback_type:
            payload["component_type"] = fallback_type
        if open_warning:
            payload["warning_open_model"] = open_warning
        return _json(payload)
    except Exception as exc:
        return _json({"ok": False, "api": "GetComponentPorts", "error": str(exc)})


def _mm_get_model_text(model_name: str) -> str:
    requested = (model_name or "").strip()
    if not requested:
        return _json({"ok": False, "api": "GetModelText", "error": "model_name is required"})
    try:
        driver = _get_driver()
        candidates = modelica_class_name_candidates(requested)
        last_error = ""
        tried: List[str] = []
        for cand in candidates:
            tried.append(cand)
            exists: Optional[bool] = None
            class_exist = getattr(driver, "class_exist", None)
            if callable(class_exist):
                try:
                    ce = class_exist(cand)
                except Exception:
                    ce = None
                if ce is not None and ce.ok:
                    exists = bool(ce.data)
            result = driver.get_model_text(cand)
            if not result.ok:
                last_error = result.error or "GetModelText failed"
                continue
            text = str(result.data or "").strip()
            if text:
                payload = json.loads(driver.as_json(result))
                payload["ok"] = True
                payload["api"] = "GetModelText"
                if cand != requested:
                    payload["requested_class_name"] = requested
                    payload["resolved_class_name"] = cand
                return _json(payload)
            if exists is False:
                last_error = f"class does not exist: {cand}"
                continue
            last_error = f"GetModelText returned empty text for {cand}"
        code = classify_missing_class(driver, requested)
        if error_looks_like_library_file_missing({"error": last_error}) or error_looks_like_library_load_failed(
            {"error": last_error}
        ):
            code = classify_library_failure(driver, requested.split(".", 1)[0], last_error)
        hint = (
            hint_for(code)
            if code in (CODE_LIBRARY_NOT_INSTALLED, CODE_LIBRARY_LOAD_FAILED)
            else (
                "ok=false because the class is missing or GetModelText returned an empty string. "
                "Empty data is not a successful lookup. Sysplorer often uses MultiBody (capital B) "
                "instead of Multibody."
            )
        )
        payload = {
            "ok": False,
            "api": "GetModelText",
            "code": code,
            "error": last_error or "GetModelText returned empty text",
            "hint": hint,
            "requested_class_name": requested,
            "tried_class_names": tried,
        }
        attach_class_library_fields(payload, requested)
        return _json(payload)
    except Exception as exc:
        return _json({"ok": False, "api": "getModelText", "error": str(exc)})


def _mm_get_model_description(model_name: str) -> str:
    try:
        result = _get_driver().get_model_description(model_name)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetModelDescription", "error": str(exc)})


def _mm_get_component_description(model_name: str, comp_name: str) -> str:
    try:
        result = _get_driver().get_component_description(model_name, comp_name)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetComponentDescription", "error": str(exc)})


def _mm_get_classes(model_name: str) -> str:
    try:
        result = _get_driver().get_classes(model_name)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetClasses", "error": str(exc)})


def _mm_export_model_diagram(
    model_name: str,
    output_path: str = "",
    width: int = 800,
    height: int = 600,
    open_model_first: bool = True,
) -> str:
    try:
        driver = _get_driver()
        name = (model_name or "").strip()
        if not name:
            return _json({"ok": False, "api": "ExportDiagram", "error": "model_name is required"})

        if open_model_first:
            o = driver.open_model(model_name=name)
            if not o.ok:
                return _json(
                    {
                        "ok": False,
                        "api": "OpenModel",
                        "error": o.error or "OpenModel failed",
                        "hint": "Load the .mo first (model_manager action=load_file) before export.",
                    }
                )

        out = (output_path or "").strip()
        if not out:
            DIAGRAM_EXPORT_TEMP_DIR.mkdir(parents=True, exist_ok=True)
            safe = name.replace(".", "_")
            out = str(DIAGRAM_EXPORT_TEMP_DIR / f"{safe}_diagram.png")

        p = Path(out).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        result = driver.export_diagram(
            model_name=name,
            output_path=str(p),
            width=width,
            height=height,
        )
        payload = json.loads(driver.as_json(result))
        payload["output_path"] = str(p)
        return _json(payload)
    except Exception as exc:
        return _json({"ok": False, "api": "ExportDiagram", "error": str(exc)})


def _mm_compare_model(
    model_name: str,
    model_name_b: str,
    is_file: bool = False,
    open_models_first: bool = True,
) -> str:
    try:
        driver = _get_driver()
        name_a = (model_name or "").strip()
        name_b = (model_name_b or "").strip()
        if not name_a:
            return _json({"ok": False, "api": "CompareModel", "error": "model_name is required"})
        if not name_b:
            return _json({"ok": False, "api": "CompareModel", "error": "model_name_b is required"})

        compare_by_file = bool(is_file)
        if open_models_first and not compare_by_file:
            for name in (name_a, name_b):
                o = driver.open_model(model_name=name)
                if not o.ok:
                    return _json(
                        {
                            "ok": False,
                            "api": "OpenModel",
                            "error": o.error or "OpenModel failed",
                            "model_name": name,
                            "hint": "Load models first (model_manager action=load_file) before compare_model.",
                        }
                    )

        result = driver.compare_model(
            model_name_a=name_a,
            model_name_b=name_b,
            is_file=compare_by_file,
        )
        payload = json.loads(driver.as_json(result))
        payload["model_name"] = name_a
        payload["model_name_b"] = name_b
        payload["is_file"] = compare_by_file
        return _json(payload)
    except Exception as exc:
        return _json({"ok": False, "api": "CompareModel", "error": str(exc)})


def mworks_open_model(model_name: str) -> str:
    """Python helper (not an MCP tool). Prefer ``model_manager`` with action=open."""
    return _mm_open(model_name)


def mworks_new_model(model_name: str, restriction: str = "model") -> str:
    """Python helper (not an MCP tool). Prefer ``model_manager`` with action=new."""
    return _mm_new(model_name, restriction=restriction)


def mworks_load_file(
    file_path: str,
    model_name: str = "",
    auto_load_deps: bool = True,
    skip_if_unchanged: bool = True,
    force_reload: bool = False,
    prepare_dependencies: bool = True,
    dependency_toml_path: str = "",
    dependency_dry_run: bool = False,
    download_missing_deps: bool = True,
    refresh_libraries_after_download: bool = True,
    load_dependencies_after_download: bool = True,
    respect_toml_install_flags: bool = True,
    stop_on_dep_error: bool = False,
    dependency_download_dir: str = "",
    dependency_staging_root: str = "",
    allow_dependency_elevation: bool = True,
    dependency_elevation_mode: str = "auto",
    dependency_install_helper_path: str = "",
) -> str:
    """Python helper (not an MCP tool). Prefer ``model_manager`` with action=load_file."""
    return _mm_load_file(
        file_path,
        model_name=model_name,
        auto_load_deps=auto_load_deps,
        skip_if_unchanged=skip_if_unchanged,
        force_reload=force_reload,
        prepare_dependencies=prepare_dependencies,
        dependency_toml_path=dependency_toml_path,
        dependency_dry_run=dependency_dry_run,
        download_missing_deps=download_missing_deps,
        refresh_libraries_after_download=refresh_libraries_after_download,
        load_dependencies_after_download=load_dependencies_after_download,
        respect_toml_install_flags=respect_toml_install_flags,
        stop_on_dep_error=stop_on_dep_error,
        dependency_download_dir=dependency_download_dir,
        dependency_staging_root=dependency_staging_root,
        allow_dependency_elevation=allow_dependency_elevation,
        dependency_elevation_mode=dependency_elevation_mode,
        dependency_install_helper_path=dependency_install_helper_path,
    )


def mworks_unload_file(model_name: str) -> str:
    """Python helper (not an MCP tool). Prefer ``model_manager`` with action=unload."""
    return _mm_unload(model_name)


def mworks_save_model(model_name: str, folder: str = "", save_type: int = 0) -> str:
    """Python helper (not an MCP tool). Prefer ``model_manager`` with action=save_as."""
    return _mm_save(model_name, folder=folder, save_type=save_type, save_as=True)


def mworks_export_model_diagram(
    model_name: str,
    output_path: str = "",
    width: int = 800,
    height: int = 600,
    open_model_first: bool = True,
) -> str:
    """Python helper (not an MCP tool). Diagram PNG is not an MCP tool; use ExportDiagram via call_code."""
    return _mm_attach_action(
        _mm_export_model_diagram(
            model_name,
            output_path=output_path,
            width=width,
            height=height,
            open_model_first=open_model_first,
        ),
        "export_model_diagram",
    )


def mworks_compare_model(
    model_name: str,
    model_name_b: str,
    is_file: bool = False,
    open_models_first: bool = True,
) -> str:
    """Python helper (not an MCP tool). Prefer the ``compare_model`` MCP tool."""
    return _mm_attach_action(
        _mm_compare_model(
            model_name,
            model_name_b=model_name_b,
            is_file=is_file,
            open_models_first=open_models_first,
        ),
        "compare_model",
    )


_MM_LIFECYCLE_ALIASES = {
    "open": "open",
    "open_model": "open",
    "new": "new",
    "new_model": "new",
    "create": "new",
    "load_file": "load_file",
    "load": "load_file",
    "open_file": "load_file",
    "unload": "unload",
    "unload_file": "unload",
    "erase": "unload",
    "erase_classes": "unload",
    "save": "save",
    "save_model": "save",
    "save_as": "save_as",
    "savemodelas": "save_as",
    "save_model_as": "save_as",
}

_MI_INSPECT_ALIASES = {
    "lookup_component": "lookup_component",
    "get_components": "get_components",
    "get_component_type_name": "get_component_type_name",
    "getcomponenttypename": "get_component_type_name",
    "get_component_ports": "get_component_ports",
    "get_model_text": "get_model_text",
    "get_model_description": "get_model_description",
    "get_component_description": "get_component_description",
    "get_classes": "get_classes",
    "get_last_errors": "get_last_errors",
    "last_errors": "get_last_errors",
    "getlasterrors": "get_last_errors",
    "get_last_error": "get_last_errors",
    "getlasterror": "get_last_errors",
}

_CM_COMPARE_ALIASES = {
    "compare_model": "compare_model",
    "compare": "compare_model",
    "compare_models": "compare_model",
}

_EXPORT_ALIASES = frozenset({"export_model_diagram", "export_diagram"})
_LOADED_ALIASES = frozenset(
    {"get_loaded_models", "loaded_models", "list_loaded_models", "getloadedmodels"}
)

_EXPORT_HINT = (
    'get_api_document("ExportDiagram") then call_code(mode="run_sysplorer_api")'
)
_COMPARE_HINT = "compare_model(model_name=..., model_name_b=..., is_file=...)"
_LOADED_HINT = 'session_manager(action="get_loaded_models")'


def _moved_action_error(*, from_tool: str, action: str, use: str) -> str:
    return _json(
        {
            "ok": False,
            "tool": from_tool,
            "action": action,
            "error": f"{from_tool} no longer handles {action!r}. Use {use}.",
            "hint": use,
            "moved_to": use,
        }
    )


def _missing_action_fields(tool: str, action: str, *pairs: Tuple[str, str]) -> Optional[str]:
    missing = [name for name, value in pairs if not (value or "").strip()]
    if not missing:
        return None
    return _json(
        {
            "ok": False,
            "tool": tool,
            "manager_action": action,
            "error": f"{' and '.join(missing)} required for action={action}",
        }
    )


def _redirect_retired_model_action(from_tool: str, action: str) -> Optional[str]:
    key = (action or "").strip().lower()
    inspect = _MI_INSPECT_ALIASES.get(key)
    if inspect:
        return _moved_action_error(
            from_tool=from_tool,
            action=action,
            use=f'model_inspect(action="{inspect}")',
        )
    if key in _CM_COMPARE_ALIASES:
        return _moved_action_error(from_tool=from_tool, action=action, use=_COMPARE_HINT)
    if key in _EXPORT_ALIASES:
        return _moved_action_error(from_tool=from_tool, action=action, use=_EXPORT_HINT)
    if key in _LOADED_ALIASES:
        return _moved_action_error(from_tool=from_tool, action=action, use=_LOADED_HINT)
    lifecycle = _MM_LIFECYCLE_ALIASES.get(key)
    if lifecycle and from_tool != "model_manager":
        return _moved_action_error(
            from_tool=from_tool,
            action=action,
            use=f'model_manager(action="{lifecycle}")',
        )
    return None


@mcp.tool(annotations=writable_annotations())
def model_manager(
    action: str,
    model_name: str = "",
    file_path: str = "",
    restriction: str = "model",
    folder: str = "",
    save_type: int = 0,
    force_reload: bool = False,
    skip_if_unchanged: bool = True,
    auto_load_deps: bool = True,
) -> str:
    """Lifecycle only: new, open, load_file, unload, save, save_as.

    ``open`` / ``unload`` take a loaded FQ class name, never a ``.mo`` path.
    ``load_file`` takes a ``.mo`` / ``package.mo`` / ``.mol`` path; nested packages
    open the top-level package.mo (``load_path`` / ``load_target``).
    ``save`` is official SaveModel (overwrite the file this class was loaded from).
    ``save_as`` is official SaveModelAs into ``folder`` or a task subfolder under
    GetDirectory (never GetDirectory itself). Both return ``saved_path``.
    ``force_reload`` EraseClasses only the root package. Inspect with
    ``model_inspect``; compare with ``compare_model``.
    """
    key = (action or "").strip().lower()
    norm = _MM_LIFECYCLE_ALIASES.get(key)
    if not norm:
        moved = _redirect_retired_model_action("model_manager", action)
        if moved:
            return moved
        return _json(
            {
                "ok": False,
                "tool": "model_manager",
                "error": f"unknown action: {action!r}",
                "hint": (
                    "Use new, open, load_file, unload, save, save_as. "
                    "Inspect: model_inspect. Compare: compare_model. "
                    "Loaded list: session_manager(action=get_loaded_models)."
                ),
            }
        )

    mn = (model_name or "").strip()
    fp = (file_path or "").strip()
    if norm == "open":
        missing = _missing_action_fields("model_manager", norm, ("model_name", mn))
        return missing or _mm_attach_action(_mm_open(mn), norm)
    if norm == "new":
        missing = _missing_action_fields("model_manager", norm, ("model_name", mn))
        return missing or _mm_attach_action(
            _mm_new(mn, restriction=restriction or "model"),
            norm,
        )
    if norm == "load_file":
        missing = _missing_action_fields("model_manager", norm, ("file_path", fp))
        return missing or _mm_attach_action(
            _mm_load_file(
                fp,
                model_name=mn,
                auto_load_deps=auto_load_deps,
                skip_if_unchanged=skip_if_unchanged,
                force_reload=force_reload,
            ),
            norm,
        )
    if norm == "unload":
        missing = _missing_action_fields("model_manager", norm, ("model_name", mn))
        return missing or _mm_attach_action(_mm_unload(mn), norm)
    if norm == "save":
        missing = _missing_action_fields("model_manager", norm, ("model_name", mn))
        return missing or _mm_attach_action(
            _mm_save(mn, folder=folder or "", save_type=int(save_type), save_as=False),
            norm,
        )
    if norm == "save_as":
        missing = _missing_action_fields("model_manager", norm, ("model_name", mn))
        return missing or _mm_attach_action(
            _mm_save(mn, folder=folder or "", save_type=int(save_type), save_as=True),
            norm,
        )
    return _json({"ok": False, "tool": "model_manager", "error": "internal dispatch error"})


@mcp.tool(annotations=readonly_annotations(idempotent=True))
def model_inspect(
    action: str,
    model_name: str = "",
    component: str = "",
    component_name: str = "",
    comp_name: str = "",
    info_type: str = "",
    port_direction: int = 0,
    full_name: bool = False,
) -> str:
    """Read-only: classes, components, ports, text, descriptions, last errors.

    ``get_classes("")`` is one layer; pass a child FQ name to go deeper.
    ``get_component_ports`` is official GetComponentPorts (opens the model first).
    Empty [] is official when the instance has no diagram ports; then MCP lists
    the component type's connectors. ``port_direction`` 1/2 is often [] even when 0
    has ports. ``get_last_errors`` is official GetLastErrors (plural). Loaded
    snapshot is ``session_manager(action=get_loaded_models)``, not this tool.
    """
    key = (action or "").strip().lower()
    norm = _MI_INSPECT_ALIASES.get(key)
    if not norm:
        moved = _redirect_retired_model_action("model_inspect", action)
        if moved:
            return moved
        return _json(
            {
                "ok": False,
                "tool": "model_inspect",
                "error": f"unknown action: {action!r}",
                "hint": (
                    "Use get_classes, get_components, get_component_ports, "
                    "get_component_type_name, get_model_text, get_model_description, "
                    "get_component_description, lookup_component, get_last_errors."
                ),
            }
        )

    mn = (model_name or "").strip()
    cn = (comp_name or "").strip()
    cname = (component_name or "").strip()
    comp = (component or "").strip()
    if norm == "lookup_component":
        missing = _missing_action_fields(
            "model_inspect", norm, ("model_name", mn), ("comp_name", cn)
        )
        return missing or _mm_attach_action(
            _mm_lookup_component(mn, cn, info_type=info_type or ""),
            norm,
        )
    if norm == "get_components":
        missing = _missing_action_fields("model_inspect", norm, ("model_name", mn))
        return missing or _mm_attach_action(_mm_get_components(mn, component=comp), norm)
    if norm == "get_component_type_name":
        type_comp = cname or cn
        missing = _missing_action_fields(
            "model_inspect",
            norm,
            ("model_name", mn),
            ("component_name", type_comp),
        )
        return missing or _mm_attach_action(
            _mm_get_component_type_name(mn, type_comp, full_name=bool(full_name)),
            norm,
        )
    if norm == "get_component_ports":
        port_comp = cname or cn or comp
        missing = _missing_action_fields("model_inspect", norm, ("model_name", mn))
        return missing or _mm_attach_action(
            _mm_get_component_ports(mn, port_comp, port_direction=int(port_direction)),
            norm,
        )
    if norm == "get_model_text":
        missing = _missing_action_fields("model_inspect", norm, ("model_name", mn))
        return missing or _mm_attach_action(_mm_get_model_text(mn), norm)
    if norm == "get_model_description":
        missing = _missing_action_fields("model_inspect", norm, ("model_name", mn))
        return missing or _mm_attach_action(_mm_get_model_description(mn), norm)
    if norm == "get_component_description":
        missing = _missing_action_fields(
            "model_inspect", norm, ("model_name", mn), ("comp_name", cn)
        )
        return missing or _mm_attach_action(_mm_get_component_description(mn, cn), norm)
    if norm == "get_classes":
        missing = _missing_action_fields("model_inspect", norm, ("model_name", mn))
        return missing or _mm_attach_action(_mm_get_classes(mn), norm)
    if norm == "get_last_errors":
        return _mm_attach_action(_mm_get_last_errors(), norm)
    return _json({"ok": False, "tool": "model_inspect", "error": "internal dispatch error"})


@mcp.tool(annotations=readonly_annotations())
def compare_model(
    model_name: str,
    model_name_b: str,
    is_file: bool = False,
    open_model_first: bool = True,
) -> str:
    """Compare two models via official CompareModel.

    Loaded qualified names: ``is_file=false``. Two ``.mo`` paths: ``is_file=true``.
    """
    mn = (model_name or "").strip()
    mn_b = (model_name_b or "").strip()
    missing = _missing_action_fields(
        "compare_model",
        "compare_model",
        ("model_name", mn),
        ("model_name_b", mn_b),
    )
    if missing:
        return missing
    return _mm_attach_action(
        _mm_compare_model(
            mn,
            model_name_b=mn_b,
            is_file=bool(is_file),
            open_models_first=bool(open_model_first),
        ),
        "compare_model",
    )


def _reload_mo_via_model_manager(mo_path: str) -> Tuple[bool, Dict[str, Any]]:
    """与 ``model_manager(action=load_file, force_reload=True)`` 同路径，刷新磁盘写回后的模型与 Diagram。"""
    p = (mo_path or "").strip()
    if not p:
        return True, {"ok": True, "api": "OpenModelFile", "skipped": True, "reason": "empty mo_path"}
    raw = mworks_load_file(
        file_path=p,
        auto_load_deps=False,
        skip_if_unchanged=False,
        force_reload=True,
    )
    meta = json.loads(raw)
    return bool(meta.get("ok", False)), meta


def _norm_mo_path_key(mo_path: str) -> str:
    s = (mo_path or "").strip()
    if not s:
        return ""
    return str(Path(s).resolve())


def _preflight_smart_layout_reload(
    *,
    smart_layout_graph_json: str = "",
    smart_layout_graph_json_path: str = "",
    smart_layout_model_path: str = "",
    reload_mo_path: str = "",
    layout_output_json_path: str = "",
    timeout_seconds: int = 120,
    model_name_hint: str = "",
    auto_generate_graph: bool = False,
) -> Tuple[bool, List[Dict[str, Any]], str]:
    """
    在检查 / 翻译 / 仿真之前的可选预检。

    写回 ``.mo`` 仅在以下情况发生：已提供 graph（``smart_layout_graph_json`` /
    ``smart_layout_graph_json_path``），或调用方显式 ``auto_generate_graph=True`` 且有目标
    ``.mo``。默认不构图、不改磁盘——布局请走 ``smart_layout(mode="writeback_mo")``。

    ``reload_mo_path`` 单独出现时只强制重载，不写回。写回成功后会对该 ``.mo``
    ``mworks_load_file(..., force_reload=True)``；若 ``reload_mo_path`` 与写回路径不同再追加一次重载。
    """
    steps: List[Dict[str, Any]] = []
    gj = (smart_layout_graph_json or "").strip()
    gjp = (smart_layout_graph_json_path or "").strip()
    mo_sl = (smart_layout_model_path or "").strip()
    rp = (reload_mo_path or "").strip()
    reloaded: set[str] = set()

    write_mo = mo_sl or rp
    # 条件：要么有graph，要么开启自动生成且有目标mo文件
    if (gj or gjp) or (auto_generate_graph and write_mo):
        if not write_mo:
            return False, [], "smart_layout graph 已提供但未设置 smart_layout_model_path 或 reload_mo_path"
        from tools.layout import run_smart_layout_for_fast_workflow

        sok, sdata = run_smart_layout_for_fast_workflow(
            graph_json=gj,
            graph_json_path=gjp,
            model_output_path=write_mo,
            model_name=(model_name_hint or "").strip(),
            layout_output_json_path=(layout_output_json_path or "").strip(),
            timeout_seconds=int(timeout_seconds),
            auto_generate_graph=auto_generate_graph,
        )
        row_sl: Dict[str, Any] = {
            "kind": "smart_layout_writeback",
            "ok": sok,
            "target": write_mo,
        }
        if sdata.get("skipped"):
            row_sl["skipped"] = True
            row_sl["reason"] = sdata.get("reason", "")
            if sdata.get("graph_source"):
                row_sl["graph_source"] = sdata.get("graph_source")
            if sdata.get("diagnostics"):
                row_sl["diagnostics"] = sdata.get("diagnostics")
        elif sok:
            row_sl["components_updated"] = sdata.get("components_updated")
            row_sl["connects_updated"] = sdata.get("connects_updated")
            if sdata.get("graph_source"):
                row_sl["graph_source"] = sdata.get("graph_source")
            if sdata.get("diagnostics"):
                row_sl["diagnostics"] = sdata.get("diagnostics")
        else:
            row_sl["error"] = sdata.get("error", "")
            if sdata.get("graph_source"):
                row_sl["graph_source"] = sdata.get("graph_source")
            if sdata.get("diagnostics"):
                row_sl["diagnostics"] = sdata.get("diagnostics")
        steps.append(row_sl)
        if not sok:
            return False, steps, row_sl.get("error") or "smart_layout writeback failed"
        rr_ok, rj = _reload_mo_via_model_manager(write_mo)
        steps.append({"kind": "reload_mo", "ok": rr_ok, "target": write_mo, "api_meta": rj})
        if not rr_ok:
            return False, steps, f"smart_layout 后重载失败: {rj.get('error', '')}"
        k = _norm_mo_path_key(write_mo)
        if k:
            reloaded.add(k)

    rp_key = _norm_mo_path_key(rp)
    if rp_key and rp_key not in reloaded:
        rr2_ok, rj2 = _reload_mo_via_model_manager(rp)
        steps.append({"kind": "reload_mo", "ok": rr2_ok, "target": rp, "api_meta": rj2})
        if not rr2_ok:
            return False, steps, f"reload_mo_path 重载失败: {rj2.get('error', '')}"

    return True, steps, ""


_LIBRARY_CLASS_PREFIXES = (
    "Modelica.",
    "ModelicaServices.",
    "Complex.",
    "SysplorerEmbeddedCoder.",
)


def _is_standard_library_class(model_name: str) -> bool:
    n = (model_name or "").strip()
    if not n:
        return False
    for prefix in _LIBRARY_CLASS_PREFIXES:
        root = prefix[:-1]
        if n == root or n.startswith(prefix):
            return True
    return False


def _looks_like_mo_file(path: str) -> bool:
    s = (path or "").strip()
    if not s.lower().endswith(".mo"):
        return False
    try:
        return Path(s).is_file()
    except OSError:
        return False


def _mo_missing_placement(path: str) -> bool:
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return "annotation(Placement(" not in text and "annotation(Placement (" not in text


def _user_mo_path_for_layout(model_name: str = "", reload_mo_path: str = "") -> str:
    """Resolve a user ``.mo`` for auto-layout. Never invent a library path."""
    rp = (reload_mo_path or "").strip()
    if _looks_like_mo_file(rp):
        return rp
    hint = (model_name or "").strip()
    if not hint or _is_standard_library_class(hint):
        return ""
    short = hint.split(".")[-1]
    with _state._load_cache_lock:
        items = list(_state._loaded_file_cache.items())
    for key, row in items:
        if not isinstance(row, dict) or not row.get("ok"):
            continue
        path = str(row.get("load_path") or key or "").strip()
        if not _looks_like_mo_file(path):
            continue
        cached = str(row.get("class_name") or row.get("dependency_model_name") or "").strip()
        stem = Path(path).stem
        cached_short = cached.split(".")[-1] if cached else ""
        if hint in (cached, stem) or short in (cached, cached_short, stem):
            return path
        if cached and hint.endswith("." + cached_short):
            return path
        if hint.endswith("." + stem):
            return path
    return ""


def _compile_preflight(
    model_name: str = "",
    reload_mo_path: str = "",
) -> Tuple[bool, List[Dict[str, Any]], str]:
    """Reload and, for a user ``.mo`` with no Placement, auto-layout.

    Standard-library classes are never rewritten. Layout failure is recorded and
    does not block check / translate / simulate.
    """
    rp = (reload_mo_path or "").strip()
    mn = (model_name or "").strip()
    if _is_standard_library_class(mn):
        if rp:
            return _preflight_smart_layout_reload(reload_mo_path=rp)
        return True, [], ""

    mo = _user_mo_path_for_layout(mn, rp)
    if mo and _mo_missing_placement(mo):
        ok, steps, err = _preflight_smart_layout_reload(
            smart_layout_model_path=mo,
            reload_mo_path=rp or mo,
            auto_generate_graph=True,
            model_name_hint=mn or Path(mo).stem,
        )
        if ok:
            return True, steps, ""
        steps = list(steps)
        steps.append(
            {
                "kind": "smart_layout_skipped_continue",
                "ok": False,
                "target": mo,
                "error": err,
            }
        )
        return True, steps, ""

    if rp:
        return _preflight_smart_layout_reload(reload_mo_path=rp)
    return True, [], ""


def _last_reload_api_meta_from_preflight(steps: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for s in reversed(steps):
        if s.get("kind") == "reload_mo" and isinstance(s.get("api_meta"), dict):
            return s["api_meta"]
    return None


def _sysplorer_check_models_payload(
    names: List[str],
    model_type: str = "MODELICA",
    stop_on_error: bool = False,
    reload_mo_path: str = "",
) -> Dict[str, Any]:
    started = time.perf_counter()
    rows: List[Dict[str, Any]] = []
    driver = _get_driver()
    pf_ok, pf_steps, pf_err = _compile_preflight(
        names[0] if names else "",
        reload_mo_path,
    )
    if not pf_ok:
        out_fail: Dict[str, Any] = {
            "ok": False,
            "tool": "check_model",
            "model_type": model_type,
            "elapsed_s": round(time.perf_counter() - started, 3),
            "count": 0,
            "results": [],
            "preflight_steps": pf_steps,
            "error": pf_err,
        }
        lm = _last_reload_api_meta_from_preflight(pf_steps)
        if lm is not None:
            out_fail["reload_mo_before"] = lm
        return out_fail
    reload_meta: Optional[Dict[str, Any]] = None
    if pf_steps:
        reload_meta = _last_reload_api_meta_from_preflight(pf_steps)
    for name in names:
        t0 = time.perf_counter()
        if _class_confirmed_missing(driver, name):
            row = _lookup_fail_payload(driver, "CheckModel", name)
        else:
            result = driver.check_model(model_name=name, model_type=model_type)
            row = json.loads(driver.as_json(result))
            if not row.get("ok") and (
                error_looks_like_library_file_missing(row)
                or error_looks_like_library_load_failed(row)
                or error_looks_like_class_not_found(row)
            ):
                row = _mark_lookup_failure(driver, row, name)
        row["model_name"] = name
        row["dt_s"] = round(time.perf_counter() - t0, 3)
        rows.append(row)
        if stop_on_error and not bool(row.get("ok", False)):
            break
    out: Dict[str, Any] = {
        "ok": all(bool(x.get("ok", False)) for x in rows),
        "tool": "check_model",
        "model_type": model_type,
        "elapsed_s": round(time.perf_counter() - started, 3),
        "count": len(rows),
        "results": rows,
    }
    if not out["ok"]:
        failed = next((row for row in rows if not row.get("ok")), None)
        if failed:
            if failed.get("error"):
                out["error"] = failed["error"]
            if failed.get("api"):
                out["api"] = failed["api"]
            if failed.get("code"):
                out["code"] = failed["code"]
            elif error_looks_like_class_not_found(failed):
                out["code"] = CODE_CLASS_NOT_FOUND
    if pf_steps:
        out["preflight_steps"] = pf_steps
    if reload_meta is not None:
        out["reload_mo_before"] = reload_meta
    return out


@mcp.tool(annotations=writable_annotations())
def check_model(
    model_names: Optional[List[str]] = None,
    model_name: str = "",
    model_type: str = "MODELICA",
    stop_on_error: bool = False,
    reload_mo_path: str = "",
) -> str:
    """Check one or more models. Pass ``model_names`` and/or ``model_name``.

    Auto-layouts a user ``.mo`` that has no Placement (``load_file`` cache or
    ``reload_mo_path``). Library classes are not rewritten. Re-layout: ``smart_layout``.
    """
    try:
        names = [str(x).strip() for x in (model_names or []) if str(x).strip()]
        one = (model_name or "").strip()
        if one:
            names.append(one)
        # 去重且保序
        seen: set[str] = set()
        uniq: List[str] = []
        for n in names:
            if n not in seen:
                seen.add(n)
                uniq.append(n)
        names = uniq
        if not names:
            return _json(
                {
                    "ok": False,
                    "tool": "check_model",
                    "error": "Provide model_names (non-empty list) and/or a non-empty model_name",
                }
            )
        return _json(
            _sysplorer_check_models_payload(
                names,
                model_type=model_type,
                stop_on_error=stop_on_error,
                reload_mo_path=str(reload_mo_path or "").strip(),
            )
        )
    except Exception as exc:
        return _json({"ok": False, "tool": "check_model", "api": "checkModelEx", "error": str(exc)})


@mcp.tool(annotations=writable_annotations())
def translate_model(
    model_name: str,
    code_folder: str = TEMP_CODE_FOLDER,
    model_type: str = "MODELICA",
    code_type: str = "NORMAL",
    build_type: str = "BINARY",
    run_to: str = "MAKING",
    config_json: str = "",
    reload_mo_path: str = "",
) -> str:
    """Translate a model (official ``TranslateModel``). ``model_name`` required.

    Same user-``.mo`` auto-layout / reload as ``check_model``. Re-layout: ``smart_layout``.
    """
    try:
        driver = _get_driver()
        mn = (model_name or "").strip()
        rp = (reload_mo_path or "").strip()
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "translate_model",
                    "error": "model_name 不能为空",
                }
            )
        pf_ok, pf_steps, pf_err = _compile_preflight(mn, rp)
        if not pf_ok:
            out_pf: Dict[str, Any] = {
                "ok": False,
                "tool": "translate_model",
                "preflight_steps": pf_steps,
                "error": pf_err,
            }
            lm = _last_reload_api_meta_from_preflight(pf_steps)
            if lm is not None:
                out_pf["reload_mo_before"] = lm
            return _json(out_pf)
        reload_meta: Optional[Dict[str, Any]] = _last_reload_api_meta_from_preflight(pf_steps)
        result = driver.translate_model(
            model_name=model_name,
            code_folder=code_folder,
            model_type=model_type,
            code_type=code_type,
            build_type=build_type,
            run_to=run_to,
            config_json=config_json,
        )
        out = json.loads(driver.as_json(result))
        if pf_steps:
            out["preflight_steps"] = pf_steps
        if reload_meta is not None:
            out["reload_mo_before"] = reload_meta
        return _json(out)
    except Exception as exc:
        return _json(
            {
                "ok": False,
                "tool": "translate_model",
                "api": "TranslateModel",
                "error": str(exc),
            }
        )


def _apply_official_result_verification(
    driver: Any,
    out: Dict[str, Any],
    *,
    verify_result_var: str,
    verify_time_point: Any,
    result_var_type: int,
) -> None:
    """Augment SimulateModel JSON with GetResultVariableInfo probes + optional GetVarValueAt (mutates out).

    Avoids ``GetResultVariables`` (often huge); uses ``GetResultVariableInfo`` to confirm the
    session has readable results and that ``verify_result_var`` exists when specified.
    If ``verify_result_var`` is empty, does not call result APIs (no default probe; ``time`` is
    not reliable via ``GetResultVariableInfo`` on some Sysplorer builds).
    ``result_var_type`` is kept for API compatibility but no longer drives verification.

    Success semantics: ``SimulateModel`` failure always keeps ``ok=False``. Result probes only
    cross-check a successful SimulateModel; they must never promote a failed simulate to success,
    because GetResultVariableInfo / GetVarValueAt read the *current session* result set (which
    may be leftover from a prior model/run).
    """
    sim_reported_ok = bool(out.get("ok", False))
    sim_err = str(out.get("error", "") or "")

    var_name = (verify_result_var or "").strip()
    if not var_name:
        out["result_verification"] = {
            "skipped": True,
            "reason": "未指定 verify_result_var，已跳过 GetResultVariableInfo / GetVarValueAt。",
        }
        return

    info_r = driver.get_result_variable_info(var_name, "Type")
    has_results = bool(
        info_r.ok and info_r.data is not None and str(info_r.data).strip() != ""
    )
    grv_block: Dict[str, Any] = {
        "ok": info_r.ok,
        "api": "GetResultVariableInfo",
        "probe_var": var_name,
        "info_type": "Type",
        "has_readable_result": has_results,
        "result_var_type_unused": int(result_var_type),
        "note": "仿真结果存在性通过 GetResultVariableInfo 探测，未调用 GetResultVariables 全量列表。",
    }
    if info_r.ok and info_r.data is not None:
        grv_block["data"] = info_r.data
    elif info_r.error:
        grv_block["error"] = info_r.error

    rv: Dict[str, Any] = {"result_probe": grv_block}

    run_gv = bool(var_name and has_results)
    gv_blk: Optional[Dict[str, Any]] = None
    if var_name:
        if run_gv:
            gv = driver.get_var_value_at(var_name, verify_time_point)
            gv_blk = {
                "ok": gv.ok,
                "api": "GetVarValueAt",
                "var_name": var_name,
                "time_point": verify_time_point,
            }
            if gv.ok:
                gv_blk["data"] = gv.data
            elif gv.error:
                gv_blk["error"] = gv.error
            rv["get_var_value_at"] = gv_blk
        else:
            rv["get_var_value_at"] = {
                "ok": False,
                "api": "GetVarValueAt",
                "skipped": True,
                "reason": "GetResultVariableInfo 未确认该变量在当前结果中，未调用 GetVarValueAt",
                "var_name": var_name,
                "time_point": verify_time_point,
            }
            gv_blk = rv["get_var_value_at"]

    if sim_reported_ok:
        if not info_r.ok:
            out["ok"] = False
            out["error"] = f"SimulateModel 返回成功，但 GetResultVariableInfo 失败：{info_r.error or 'unknown'}"
        elif not has_results:
            out["ok"] = False
            out["error"] = (
                "SimulateModel 返回成功，但 GetResultVariableInfo 未确认可读结果变量 "
                f"({var_name!r})；请检查会话结果或核对 verify_result_var。"
            )
        elif var_name and gv_blk is not None:
            if gv_blk.get("skipped"):
                out["ok"] = False
                out["error"] = (
                    "已指定 verify_result_var，但 GetResultVariableInfo 未确认该变量存在于当前结果；"
                    "请核对变量全名或先对目标模型执行 get_result_variables(model_name=…)。"
                )
            elif not gv_blk.get("ok"):
                out["ok"] = False
                out["error"] = (
                    f"变量已在结果中，但 GetVarValueAt({var_name!r}) 失败：{gv_blk.get('error', 'unknown')}"
                )
            elif gv_blk.get("data") is None:
                out["ok"] = False
                out["error"] = (
                    f"GetVarValueAt({var_name!r}) 返回值为空，无法在指定时刻确认仿真数据。"
                )
            else:
                out["ok"] = True
    else:
        # Never promote SimulateModel failure to ok=true: session probes may see
        # stale/unrelated results from a previous run (including model-does-not-exist).
        out["ok"] = False
        out["simulate_api_reported_failure"] = True
        base_err = sim_err or "SimulateModel returned False"
        out["error"] = base_err
        if sim_err:
            out["simulate_model_error"] = sim_err

        residual_readable = (
            has_results
            and var_name
            and gv_blk is not None
            and not gv_blk.get("skipped")
            and bool(gv_blk.get("ok"))
            and gv_blk.get("data") is not None
        )
        if residual_readable:
            out["warning"] = (
                "SimulateModel 返回失败；会话中仍能通过 GetResultVariableInfo/GetVarValueAt "
                "读到 verify_result_var，可能是先前仿真的残留结果，不能视为本次仿真成功。"
            )
            out["stale_or_unrelated_result_suspected"] = True
        elif not has_results:
            out["error"] = (
                f"{base_err}; GetResultVariableInfo 未确认 verify_result_var 存在于当前结果。"
            )
        elif var_name and gv_blk is not None:
            if gv_blk.get("skipped"):
                out["error"] = (
                    f"{base_err}; 已指定 verify_result_var，但 GetResultVariableInfo "
                    "未确认该变量，未调用 GetVarValueAt。"
                )
            else:
                extra = gv_blk.get("error", "value empty or unknown")
                out["error"] = (
                    f"{base_err}; GetVarValueAt 未确认 {var_name!r} 有值：{extra}"
                )

    out["result_verification"] = rv


@mcp.tool(annotations=writable_annotations())
def simulate_model(
    model_name: str,
    sim_mode: int = 0,
    target_time: Optional[List[float]] = None,
    ext_res_path: str = "",
    verify_result_var: str = "",
    verify_time_point: Any = "end",
    result_var_type: int = 0,
    reload_mo_path: str = "",
) -> str:
    """Simulate a model (closes last result, then ``SimulateModel``).

    ``sim_mode``: 0 current / 1 standalone / 2 realtime.
    ``target_time``: optional ``[startTime, stopTime]``. Optional ``verify_result_var``.
    Same user-``.mo`` auto-layout / reload as ``check_model``. Re-layout: ``smart_layout``.
    """
    try:
        sim_mode_safe = sim_mode
        driver = _get_driver()
        rp = (reload_mo_path or "").strip()
        mn = (model_name or "").strip()
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "simulate_model",
                    "error": "model_name 不能为空",
                }
            )
        pf_ok, pf_steps, pf_err = _compile_preflight(mn, rp)
        if not pf_ok:
            out_pf: Dict[str, Any] = {
                "ok": False,
                "tool": "simulate_model",
                "preflight_steps": pf_steps,
                "error": pf_err,
            }
            lm = _last_reload_api_meta_from_preflight(pf_steps)
            if lm is not None:
                out_pf["reload_mo_before"] = lm
            return _json(out_pf)
        reload_meta: Optional[Dict[str, Any]] = _last_reload_api_meta_from_preflight(pf_steps)
        result = driver.simulate_model(
            model_name=model_name,
            sim_mode=sim_mode_safe,
            target_time=target_time or [],
            ext_res_path=ext_res_path,
        )
        out = json.loads(driver.as_json(result))
        out["sim_mode"] = sim_mode_safe
        if pf_steps:
            out["preflight_steps"] = pf_steps
        if reload_meta is not None:
            out["reload_mo_before"] = reload_meta
        _apply_official_result_verification(
            driver,
            out,
            verify_result_var=verify_result_var,
            verify_time_point=verify_time_point,
            result_var_type=result_var_type,
        )
        return _json(out)
    except Exception as exc:
        return _json(
            {
                "ok": False,
                "tool": "simulate_model",
                "api": "SimulateModel",
                "error": str(exc),
            }
        )


def mworks_set_model_param(
    model_name: str,
    param_name: str,
    value: str,
    component: str = "",
) -> str:
    """
    Set a parameter value on a loaded Modelica model (driver ``SetModelParamValue``).

    **MCP**：不注册独立改参工具。先 ``get_api_document("SetModelParamValue")``，
    再 ``call_code(mode="run_sysplorer_api")`` 调用官方接口。

    - model_name: fully-qualified model class name
    - param_name: parameter name (e.g. "m", "L", "ModelType")
    - value: new value as string (e.g. "1.5", "true"). **String-typed** parameters need an extra pair of
      double quotes inside the value, e.g. ``'"平均值"'`` / JSON ``"\\"平均值\\""``. Bare ``平均值``
      yields ``False`` and 「错误(4): 无效输入」. ``True`` only means the API accepted the string form;
      enum validity is checked later at instantiate / translate.
    - component: sub-component path owning the parameter; leave empty for top-level params
    """
    try:
        result = _get_driver().set_model_param(
            model_name=model_name,
            param_name=param_name,
            value=value,
            component=component,
        )
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "SetModelParamValue", "error": str(exc)})
