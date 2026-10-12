"""Model dependency resolution and package download helpers."""
from __future__ import annotations

import difflib
import hashlib
import json
import os
import shutil
import tarfile
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from path_config import (
    DEPLOY_ROOT,
    MWORKS_LIBRARY_ROOT,
    PLATFORM,
    USER_WORKSPACE_ROOT,
    WORKSPACE_ROOT,
    dependency_downloads_enabled,
    get_resources_root,
    library_download_tools_enabled,
)


ENDPOINT = "https://releases.tongyuan.cc"
DEFAULT_BUCKET = "modelica"
DEFAULT_ARCH = "noarch"
HTTP_TIMEOUT_SECONDS = 30
PUBLIC_PACKAGES = {"modelica", "modelicareference"}
DEFAULT_MODEL_DEPENDENCY_VERSIONS = {"modelica": "4.0.0.TY.1"}
DEPENDENCY_MANIFEST_FILENAME = "Manifest.toml"
LIBRARY_DOWNLOAD_CATALOG_FILENAME = "library_download_catalog.json"
S3_NS = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
CUSTOM_LIBRARY_MARKER = "MWORKSCustomLibrary.ini"
INSTALLING_DIR_NAME = ".mworks_mcp_installing"
STAGING_ENV_VAR = "MCP_LIBRARY_STAGING_ROOT"
INSTALL_HELPER_ENV_VAR = "MCP_INSTALL_HELPER_EXE"
DEPENDENCY_API_ALLOWED_EXACT_NAMES = {
    "DynamicBlocks",
    "NetlistLibrary",
    "NPSLibrary",
    "PythonIO",
    "SyslabWorkspace",
    "SysplorerEmbeddedCoder",
}
DEPENDENCY_API_ALLOWED_PREFIXES = ("Modelica", "TY")
FUZZY_LIBRARY_MATCH_MIN_SCORE = 0.88
FUZZY_LIBRARY_MATCH_MIN_MARGIN = 0.08
FUZZY_LIBRARY_CANDIDATE_MIN_SCORE = 0.75
DEFAULT_DOWNLOADABLE_LIBRARY_NAMES = [
    "DynamicBlocks",
    "Modelica",
    "ModelicaReference",
    "NetlistLibrary",
    "NPSLibrary",
    "PythonIO",
    "SyslabWorkspace",
    "SysplorerEmbeddedCoder",
    "TABattery",
    "TADynamics",
    "TAEconomy",
    "TAElectronic",
    "TAEngine",
    "TAThermalSystem",
    "TYAirTreatmentAndVentilation",
    "TYBase",
    "TYCommunication",
    "TYContact",
    "TYDriveline",
    "TYDriveline3D",
    "TYDSPSystem",
    "TYElectrical",
    "TYElectricPower",
    "TYFlexBody",
    "TYFuelCellSys",
    "TYGasMedia",
    "TYHydraulicComponents",
    "TYHydraulics",
    "TYIntegratedEnergySys",
    "TYMechanics",
    "TYMechanics2D",
    "TYMedia",
    "TYMixedSignal",
    "TYMotor",
    "TYMultibody",
    "TYOilMedia",
    "TYPhotovoltaicPower",
    "TYPneumaticComponents",
    "TYPneumatics",
    "TYThermalHydraulicComponents",
    "TYThermalHydraulics",
    "TYThermals",
    "TYThermoFluidSys",
    "TYWebHandling",
    "TYWindPower",
]
_DOWNLOADABLE_LIBRARY_CATALOG_CACHE: Optional[List[str]] = None


def _clean_name(value: Any) -> str:
    return str(value or "").strip()


def _normalize_library_lookup_name(value: Any) -> str:
    text = _clean_name(value).lower()
    return "".join(ch for ch in text if ch not in " -_.")


def downloadable_library_catalog_path() -> Path:
    return get_resources_root() / LIBRARY_DOWNLOAD_CATALOG_FILENAME


def load_downloadable_library_catalog() -> List[str]:
    global _DOWNLOADABLE_LIBRARY_CATALOG_CACHE
    if _DOWNLOADABLE_LIBRARY_CATALOG_CACHE is not None:
        return list(_DOWNLOADABLE_LIBRARY_CATALOG_CACHE)

    external_names: List[str] = []
    path = downloadable_library_catalog_path()
    if path.exists():
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(raw, dict) and isinstance(raw.get("libraries"), list):
                external_names = [_clean_name(item) for item in raw.get("libraries") or [] if _clean_name(item)]
        except Exception:
            external_names = []

    deduped: List[str] = []
    seen: Set[str] = set()
    for name in list(DEFAULT_DOWNLOADABLE_LIBRARY_NAMES) + external_names:
        key = _normalize_library_lookup_name(name)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(name)
    _DOWNLOADABLE_LIBRARY_CATALOG_CACHE = deduped
    return list(deduped)


def _library_match_payload(
    input_name: str,
    resolved_name: str,
    matched_by: str,
    score: Optional[float] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "ok": True,
        "input_name": input_name,
        "resolved_name": resolved_name,
        "matched_by": matched_by,
    }
    if score is not None:
        payload["score"] = round(float(score), 4)
    if input_name != resolved_name:
        payload["warning"] = (
            "library name was fuzzy-matched before download"
            if matched_by == "fuzzy"
            else "library name was normalized before download"
        )
    return payload


def resolve_downloadable_library_name(input_name: str) -> Dict[str, Any]:
    clean = _clean_name(input_name)
    if not clean:
        return {"ok": False, "status": "invalid_library_name", "input_name": clean, "error": "name is required"}

    catalog = load_downloadable_library_catalog()
    if clean in catalog:
        return _library_match_payload(clean, clean, "exact")

    lower_matches = [name for name in catalog if name.lower() == clean.lower()]
    if len(lower_matches) == 1:
        return _library_match_payload(clean, lower_matches[0], "case_insensitive")
    if len(lower_matches) > 1:
        return {
            "ok": False,
            "status": "ambiguous_library_name",
            "input_name": clean,
            "candidates": [{"name": name, "score": 1.0} for name in lower_matches],
            "message": "library name is ambiguous; choose one candidate before downloading",
        }

    normalized_input = _normalize_library_lookup_name(clean)
    normalized_matches = [name for name in catalog if _normalize_library_lookup_name(name) == normalized_input]
    if len(normalized_matches) == 1:
        return _library_match_payload(clean, normalized_matches[0], "normalized")
    if len(normalized_matches) > 1:
        return {
            "ok": False,
            "status": "ambiguous_library_name",
            "input_name": clean,
            "candidates": [{"name": name, "score": 1.0} for name in normalized_matches],
            "message": "library name is ambiguous; choose one candidate before downloading",
        }

    scored = sorted(
        (
            {
                "name": name,
                "score": difflib.SequenceMatcher(
                    None,
                    normalized_input,
                    _normalize_library_lookup_name(name),
                ).ratio(),
            }
            for name in catalog
        ),
        key=lambda item: item["score"],
        reverse=True,
    )
    candidates = [
        {"name": item["name"], "score": round(float(item["score"]), 4)}
        for item in scored[:5]
        if item["score"] >= FUZZY_LIBRARY_CANDIDATE_MIN_SCORE
    ]
    if scored:
        top = scored[0]
        second_score = float(scored[1]["score"]) if len(scored) > 1 else 0.0
        margin = float(top["score"]) - second_score
        if top["score"] >= FUZZY_LIBRARY_MATCH_MIN_SCORE and margin >= FUZZY_LIBRARY_MATCH_MIN_MARGIN:
            return _library_match_payload(clean, str(top["name"]), "fuzzy", float(top["score"]))

    if candidates:
        return {
            "ok": False,
            "status": "ambiguous_library_name",
            "input_name": clean,
            "candidates": candidates,
            "message": "library name is ambiguous; choose one candidate before downloading",
        }
    return {
        "ok": False,
        "status": "unknown_library_name",
        "input_name": clean,
        "message": "library is not in downloadable catalog",
    }


def resolve_dependency_library_names(dependencies: List[Dict[str, Any]]) -> Dict[str, Any]:
    resolved: List[Dict[str, Any]] = []
    resolutions: Dict[str, Any] = {}
    errors: List[Dict[str, Any]] = []
    ok = True
    for dep in dependencies:
        item = dict(dep)
        name = _clean_name(item.get("name"))
        if not name:
            resolved.append(item)
            continue
        match = resolve_downloadable_library_name(name)
        resolutions[name] = match
        if match.get("ok"):
            resolved_name = _clean_name(match.get("resolved_name"))
            item["input_name"] = name
            item["name"] = resolved_name
            item["library_name_resolution"] = match
            if match.get("warning"):
                item["warning"] = match.get("warning")
        else:
            ok = False
            errors.append(match)
            item["library_name_resolution"] = match
        resolved.append(item)
    return {"ok": ok, "dependencies": resolved, "resolutions": resolutions, "errors": errors}


def normalize_dependency_records(raw: Any, source: str = "") -> List[Dict[str, Any]]:
    """Normalize dependency API/list output to [{name, version, ...}]."""
    if raw is None:
        return []
    if isinstance(raw, dict):
        if isinstance(raw.get("dependencies"), list):
            raw_items = raw.get("dependencies") or []
        elif isinstance(raw.get("data"), list):
            raw_items = raw.get("data") or []
        else:
            raw_items = [raw]
    elif isinstance(raw, list):
        raw_items = raw
    else:
        raw_items = [raw]

    out: List[Dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in raw_items:
        if isinstance(item, dict):
            name = _clean_name(
                item.get("name")
                or item.get("library_name")
                or item.get("library")
                or item.get("package")
            )
            version = _clean_name(item.get("version") or item.get("library_version"))
            license_feature = _clean_name(item.get("licenseFeature") or item.get("license_feature"))
            install = item.get("install", True)
            raw_item: Any = item
        else:
            name = _clean_name(item)
            version = ""
            license_feature = ""
            install = True
            raw_item = item
        if not name:
            continue
        key = (name, version)
        if key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "name": name,
                "version": version,
                "version_source": source if version and source else "",
                "licenseFeature": license_feature,
                "install": bool(install),
                "raw": raw_item,
            }
        )
    return out


def is_allowed_dependency_api_name(name: str) -> bool:
    """Temporary allowlist for noisy GetModelDependencies output."""
    clean = _clean_name(name)
    if not clean:
        return False
    if clean in DEPENDENCY_API_ALLOWED_EXACT_NAMES:
        return True
    return any(clean.startswith(prefix) for prefix in DEPENDENCY_API_ALLOWED_PREFIXES)


def filter_dependency_api_records(dependencies: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Split normalized GetModelDependencies records into allowed and ignored."""
    allowed: List[Dict[str, Any]] = []
    filtered: List[Dict[str, Any]] = []
    for dep in dependencies:
        name = _clean_name(dep.get("name"))
        if is_allowed_dependency_api_name(name):
            allowed.append(dep)
        else:
            filtered.append(dep)
    return allowed, filtered


def filter_manifest_or_lock_dependency_records(
    dependencies: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Drop MOLS/workspace noise from Manifest.toml while keeping downloadable libs.

    MOLS may write non-library names (e.g. ``BaseWorkspace``) into Manifest.toml.
    Those must not fail ``load_library`` name resolution. Keep a name when it
    matches the API allowlist **or** resolves in the downloadable catalog (covers TA*).
    """
    kept: List[Dict[str, Any]] = []
    dropped: List[Dict[str, Any]] = []
    for dep in dependencies:
        name = _clean_name(dep.get("name"))
        if not name:
            dropped.append(dep)
            continue
        if is_allowed_dependency_api_name(name):
            kept.append(dep)
            continue
        match = resolve_downloadable_library_name(name)
        if match.get("ok"):
            item = dict(dep)
            resolved_name = _clean_name(match.get("resolved_name")) or name
            item["input_name"] = name
            item["name"] = resolved_name
            item["library_name_resolution"] = match
            if match.get("warning"):
                item["warning"] = match.get("warning")
            kept.append(item)
        else:
            item = dict(dep)
            item["library_name_resolution"] = match
            item["skipped_reason"] = "not_in_downloadable_catalog"
            dropped.append(item)
    return kept, dropped


def default_dependency_manifest_path() -> Path:
    root = USER_WORKSPACE_ROOT or WORKSPACE_ROOT
    return root / DEPENDENCY_MANIFEST_FILENAME


def default_dependency_toml_path() -> Path:
    """Backward-compatible alias for the dependency Manifest TOML path."""
    return default_dependency_manifest_path()


def dependency_download_gate() -> Dict[str, Any]:
    """Return whether dependency download/install side effects are startup-authorized."""
    if not library_download_tools_enabled():
        return {
            "enabled": False,
            "reason": (
                "library download/install is disabled outside modelica_lite/mols; "
                "use load_library(action=load) for locally installed libraries"
            ),
            "user_workspace": str(USER_WORKSPACE_ROOT) if USER_WORKSPACE_ROOT is not None else "",
            "platform_gated": True,
        }
    user_workspace = USER_WORKSPACE_ROOT
    if not dependency_downloads_enabled():
        return {
            "enabled": False,
            "reason": "start the server with --user-workspace to enable dependency download/install",
            "user_workspace": str(user_workspace) if user_workspace is not None else "",
        }
    if user_workspace is None:
        return {
            "enabled": False,
            "reason": "MCP_USER_WORKSPACE_DIR is not set",
            "user_workspace": "",
        }
    try:
        user_workspace.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return {
            "enabled": False,
            "reason": f"failed to create user workspace: {exc}",
            "user_workspace": str(user_workspace),
        }
    if not user_workspace.is_dir():
        return {
            "enabled": False,
            "reason": "user workspace is not a directory",
            "user_workspace": str(user_workspace),
        }
    return {
        "enabled": True,
        "reason": "",
        "user_workspace": str(user_workspace),
    }


def read_workspace_dependency_lock(path: Optional[Path] = None) -> Dict[str, Any]:
    """Read read-only global [[dependencies]] from Manifest.toml."""
    lock_path = Path(path) if path is not None else default_dependency_manifest_path()
    if not lock_path.exists():
        return {"ok": True, "used": False, "path": str(lock_path), "dependencies": [], "warnings": []}

    try:
        try:
            import tomllib
        except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
            import tomli as tomllib  # type: ignore[import-not-found]
        raw = tomllib.loads(lock_path.read_text(encoding="utf-8"))
        manifest_format = _clean_name(raw.get("manifest_format"))
        if manifest_format != "2.0":
            return {
                "ok": False,
                "used": True,
                "path": str(lock_path),
                "manifest_format": manifest_format,
                "dependencies": [],
                "warnings": [],
                "error": 'manifest_format must be "2.0"',
            }
        raw_deps = raw.get("dependencies", [])
        if not isinstance(raw_deps, list):
            return {
                "ok": False,
                "used": True,
                "path": str(lock_path),
                "manifest_format": manifest_format,
                "dependencies": [],
                "warnings": [],
                "error": "dependencies must be a TOML array of tables",
            }
        deps = normalize_dependency_records(raw_deps, source="manifest_toml")
        deps, dropped = filter_manifest_or_lock_dependency_records(deps)
        warnings: List[str] = []
        if dropped:
            names = ", ".join(
                sorted({_clean_name(d.get("name")) for d in dropped if _clean_name(d.get("name"))})
            )
            warnings.append(
                f"ignored non-downloadable Manifest.toml entries (not in catalog): {names}"
            )
        return {
            "ok": True,
            "used": True,
            "path": str(lock_path),
            "manifest_format": manifest_format,
            "dependencies": deps,
            "filtered_dependencies": dropped,
            "warnings": warnings,
        }
    except Exception as exc:
        return {
            "ok": False,
            "used": True,
            "path": str(lock_path),
            "manifest_format": "",
            "dependencies": [],
            "warnings": [],
            "error": str(exc),
        }


def merge_workspace_dependency_lock(
    dependencies: List[Dict[str, Any]],
    lock_dependencies: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Merge global Manifest dependencies. Manifest version/install override API/latest input."""
    merged_by_name: Dict[str, Dict[str, Any]] = {}
    order: List[str] = []

    for dep in normalize_dependency_records(dependencies, source="input"):
        name = _clean_name(dep.get("name"))
        if not name:
            continue
        key = name.lower()
        if key not in merged_by_name:
            order.append(key)
        merged_by_name[key] = dict(dep)

    for dep in normalize_dependency_records(lock_dependencies, source="manifest_toml"):
        name = _clean_name(dep.get("name"))
        if not name:
            continue
        key = name.lower()
        if key not in order:
            order.append(key)
        base = dict(merged_by_name.get(key, {}))
        base.update(dep)
        base["name"] = name
        if dep.get("version"):
            base["version_source"] = "manifest_toml"
        base["install"] = bool(dep.get("install", True))
        merged_by_name[key] = base

    return {"ok": True, "dependencies": [merged_by_name[key] for key in order if key in merged_by_name]}


def infer_visibility(name: str) -> str:
    if name.strip().lower() in PUBLIC_PACKAGES:
        return "public"
    return "private"


def to_url(bucket: str, key: str) -> str:
    return f"{ENDPOINT}/{bucket}/{key}"


def latest_url(name: str, visibility: Optional[str] = None, bucket: str = DEFAULT_BUCKET) -> str:
    match = resolve_downloadable_library_name(name)
    resolved_name = _clean_name(match.get("resolved_name")) if match.get("ok") else _clean_name(name)
    resolved_visibility = visibility or infer_visibility(resolved_name)
    return to_url(bucket, f"{resolved_visibility}/{resolved_name.lower()}/latest")


def fetch_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT_SECONDS) as response:
        return response.read().decode("utf-8").strip()


def fetch_latest_version(
    name: str,
    visibility: Optional[str] = None,
    bucket: str = DEFAULT_BUCKET,
) -> Dict[str, Any]:
    clean = _clean_name(name)
    if not clean:
        return {"ok": False, "name": clean, "error": "name is required"}
    name_resolution = resolve_downloadable_library_name(clean)
    if not name_resolution.get("ok"):
        return {"ok": False, "name": clean, "error": name_resolution.get("message", "library name resolution failed"), "library_name_resolution": name_resolution}
    resolved_name = _clean_name(name_resolution.get("resolved_name"))
    default_version = DEFAULT_MODEL_DEPENDENCY_VERSIONS.get(resolved_name.lower())
    if default_version:
        return {
            "ok": True,
            "name": resolved_name,
            "input_name": clean,
            "version": default_version,
            "version_source": "default_version",
            "url": None,
            "visibility": visibility or infer_visibility(resolved_name),
            "bucket": bucket,
            "skipped_remote_latest": True,
            "reason": "default version is configured for this library",
            "library_name_resolution": name_resolution,
        }
    url = latest_url(resolved_name, visibility, bucket)
    try:
        version = fetch_text(url)
        return {
            "ok": True,
            "name": resolved_name,
            "input_name": clean,
            "version": version,
            "version_source": "remote_latest",
            "url": url,
            "visibility": visibility or infer_visibility(resolved_name),
            "bucket": bucket,
            "library_name_resolution": name_resolution,
        }
    except Exception as exc:
        return {
            "ok": False,
            "name": resolved_name,
            "input_name": clean,
            "error": str(exc),
            "url": url,
            "visibility": visibility or infer_visibility(resolved_name),
            "bucket": bucket,
            "library_name_resolution": name_resolution,
        }


def package_key(
    name: str,
    version: str,
    visibility: Optional[str] = None,
    arch: str = DEFAULT_ARCH,
) -> str:
    match = resolve_downloadable_library_name(name)
    resolved_name = _clean_name(match.get("resolved_name")) if match.get("ok") else _clean_name(name)
    resolved_visibility = visibility or infer_visibility(resolved_name)
    filename = f"{resolved_name}-{version}-{arch}.tar.zst"
    return f"{resolved_visibility}/{resolved_name.lower()}/{version}/{arch}/{filename}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def parse_sha256_text(text: str) -> str:
    return (text or "").strip().split()[0].lower()


def download_url(url: str, dest: Path) -> None:
    with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT_SECONDS) as response, dest.open("wb") as file:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                return
            file.write(chunk)


def default_library_download_dir() -> Path:
    return MWORKS_LIBRARY_ROOT


def default_library_staging_root() -> Path:
    env = os.environ.get(STAGING_ENV_VAR, "").strip()
    if env:
        return Path(env).expanduser().resolve()
    local_app_data = os.environ.get("LOCALAPPDATA", "").strip()
    if local_app_data:
        return Path(local_app_data).resolve() / "MWORKS" / "sysplorer-mcp-server" / "library-staging"
    return Path.home().resolve() / "AppData" / "Local" / "MWORKS" / "sysplorer-mcp-server" / "library-staging"


def create_staging_transaction(staging_root: Optional[Path] = None) -> Path:
    root = Path(staging_root) if staging_root is not None else default_library_staging_root()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    tx = (root / f"install-{stamp}-{uuid.uuid4().hex[:8]}").resolve()
    tx.mkdir(parents=True, exist_ok=False)
    return tx


def preflight_writable_directory(path: Path, create: bool = True) -> Dict[str, Any]:
    root = Path(path)
    token = uuid.uuid4().hex[:8]
    probe_file = root / f".mcp_write_test_{token}.tmp"
    probe_dir = root / f".mcp_write_test_dir_{token}"
    created_file = False
    created_dir = False
    try:
        if create:
            root.mkdir(parents=True, exist_ok=True)
        if not root.exists():
            return {"ok": False, "path": str(root), "error": "directory does not exist"}
        if not root.is_dir():
            return {"ok": False, "path": str(root), "error": "path is not a directory"}
        probe_file.write_text("mworks mcp write probe", encoding="utf-8")
        created_file = True
        probe_file.unlink()
        created_file = False
        probe_dir.mkdir()
        created_dir = True
        probe_dir.rmdir()
        created_dir = False
        return {"ok": True, "path": str(root)}
    except Exception as exc:
        return {"ok": False, "path": str(root), "error": str(exc)}
    finally:
        try:
            if created_file or probe_file.exists():
                probe_file.unlink(missing_ok=True)
        except OSError:
            pass
        try:
            if created_dir or probe_dir.exists():
                probe_dir.rmdir()
        except OSError:
            pass


def dependency_key(name: str, version: str) -> str:
    return f"{_clean_name(name)}@{_clean_name(version)}"


def library_install_dir(root: Path, name: str, version: str) -> Path:
    clean_name = _clean_name(name)
    clean_version = _clean_name(version)
    if not clean_name or not clean_version:
        raise ValueError("name and version are required")
    if any(ch in clean_name or ch in clean_version for ch in ('\\', '/', ':')):
        raise ValueError("name and version must not contain path separators")
    dirname = f"{clean_name} {clean_version}"
    root_resolved = Path(root).resolve()
    target = (root_resolved / dirname).resolve()
    try:
        target.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"install path escapes library root: {target}") from exc
    return target


def parse_uses_ini(path: Path) -> Dict[str, Any]:
    uses_path = Path(path)
    if not uses_path.exists():
        return {"ok": True, "path": str(uses_path), "exists": False, "dependencies": [], "warnings": []}

    try:
        text = uses_path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = uses_path.read_text(encoding="gbk", errors="replace")

    dependencies: List[Dict[str, Any]] = []
    warnings: List[str] = []
    seen: Set[Tuple[str, str]] = set()
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        parts = line.split()
        if len(parts) < 2:
            warnings.append(f"line {lineno}: missing version, skipped")
            continue
        name, version = parts[0].strip(), parts[1].strip()
        if not name or not version:
            warnings.append(f"line {lineno}: missing name or version, skipped")
            continue
        key = (name, version)
        if key in seen:
            continue
        seen.add(key)
        dependencies.append(
            {
                "name": name,
                "version": version,
                "version_source": "uses_ini",
                "install": True,
                "raw": raw_line,
            }
        )
    return {
        "ok": True,
        "path": str(uses_path),
        "exists": True,
        "dependencies": dependencies,
        "warnings": warnings,
    }


def _cleanup_paths(paths: Iterable[Path]) -> None:
    for path in paths:
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink(missing_ok=True)
        except OSError:
            pass


def cleanup_staging_transaction(path: Optional[Path]) -> Dict[str, Any]:
    if path is None:
        return {"ok": True, "status": "skipped", "reason": "no staging transaction"}
    target = Path(path)
    if not target.exists():
        return {"ok": True, "status": "not_found", "path": str(target)}
    try:
        shutil.rmtree(target)
        return {"ok": True, "status": "cleaned", "path": str(target)}
    except Exception as exc:
        return {"ok": False, "status": "cleanup_failed", "path": str(target), "error": str(exc)}


def _safe_tar_member_target(root: Path, member_name: str) -> Path:
    if not member_name or member_name.startswith(("/", "\\")):
        raise ValueError(f"unsafe absolute tar member path: {member_name!r}")
    member_path = Path(member_name)
    if member_path.drive:
        raise ValueError(f"unsafe tar member drive path: {member_name!r}")
    root_resolved = root.resolve()
    target = (root_resolved / member_name).resolve()
    try:
        target.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"unsafe tar member path escapes target dir: {member_name!r}") from exc
    return target


def extract_tar_zst(archive_path: Path, target_dir: Path) -> Dict[str, Any]:
    try:
        import zstandard as zstd  # type: ignore[import]
    except Exception as exc:
        return {
            "ok": False,
            "status": "missing_dependency",
            "error": f"Python package zstandard is required to extract .tar.zst: {exc}",
        }

    archive = Path(archive_path)
    target = Path(target_dir)
    try:
        target.mkdir(parents=True, exist_ok=True)
        extracted = 0
        with archive.open("rb") as compressed:
            dctx = zstd.ZstdDecompressor()
            with dctx.stream_reader(compressed) as reader:
                with tarfile.open(fileobj=reader, mode="r|") as tar:
                    for member in tar:
                        _safe_tar_member_target(target, member.name)
                        if member.issym() or member.islnk():
                            return {
                                "ok": False,
                                "status": "unsupported_tar_link",
                                "member": member.name,
                                "error": "symbolic links and hard links are not supported",
                            }
                        if not (member.isfile() or member.isdir()):
                            return {
                                "ok": False,
                                "status": "unsupported_tar_member",
                                "member": member.name,
                                "error": "only regular files and directories are supported",
                            }
                        tar.extract(member, path=target)
                        extracted += 1
        return {"ok": True, "status": "extracted", "archive": str(archive), "target_dir": str(target), "members": extracted}
    except Exception as exc:
        return {"ok": False, "status": "extract_failed", "archive": str(archive), "target_dir": str(target), "error": str(exc)}


def download_package(
    name: str,
    version: str,
    dest_dir: Optional[Path] = None,
    visibility: Optional[str] = None,
    arch: str = DEFAULT_ARCH,
    bucket: str = DEFAULT_BUCKET,
    dry_run: bool = True,
    keep_sha256: bool = False,
) -> Dict[str, Any]:
    clean_name = _clean_name(name)
    clean_version = _clean_name(version)
    if not clean_name:
        return {"ok": False, "error": "name is required"}
    if not clean_version:
        return {"ok": False, "name": clean_name, "error": "version is required"}
    name_resolution = resolve_downloadable_library_name(clean_name)
    if not name_resolution.get("ok"):
        return {
            "ok": False,
            "status": name_resolution.get("status", "library_name_resolution_failed"),
            "name": clean_name,
            "version": clean_version,
            "error": name_resolution.get("message", "library name resolution failed"),
            "library_name_resolution": name_resolution,
            "dry_run": bool(dry_run),
        }
    resolved_name = _clean_name(name_resolution.get("resolved_name"))

    key = package_key(resolved_name, clean_version, visibility, arch)
    url = to_url(bucket, key)
    sha_url = f"{url}.sha256"
    target_dir = Path(dest_dir) if dest_dir is not None else default_library_download_dir()
    dest = target_dir / Path(urllib.parse.unquote(Path(key).name)).name
    sha_dest = target_dir / f"{dest.name}.sha256"
    base = {
        "name": resolved_name,
        "input_name": clean_name,
        "version": clean_version,
        "bucket": bucket,
        "visibility": visibility or infer_visibility(resolved_name),
        "arch": arch,
        "archive_url": url,
        "sha256_url": sha_url,
        "dest": str(dest),
        "sha256_dest": str(sha_dest),
        "dry_run": bool(dry_run),
        "library_name_resolution": name_resolution,
    }
    if dry_run:
        return {"ok": True, "status": "planned", **base}

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            download_url(sha_url, sha_dest)
            expected_existing = parse_sha256_text(sha_dest.read_text(encoding="utf-8"))
            actual_existing = sha256_file(dest)
            if expected_existing and expected_existing == actual_existing:
                if not keep_sha256:
                    sha_dest.unlink(missing_ok=True)
                return {"ok": True, "status": "already_downloaded", "sha256": actual_existing, **base}
            _cleanup_paths([dest, sha_dest])

        download_url(url, dest)
        download_url(sha_url, sha_dest)
        expected = parse_sha256_text(sha_dest.read_text(encoding="utf-8"))
        actual = sha256_file(dest)
        if expected != actual:
            _cleanup_paths([dest, sha_dest])
            return {
                "ok": False,
                "status": "sha256_mismatch",
                "expected": expected,
                "actual": actual,
                **base,
            }
        if not keep_sha256:
            sha_dest.unlink(missing_ok=True)
        return {"ok": True, "status": "downloaded", "sha256": actual, **base}
    except Exception as exc:
        _cleanup_paths([dest, sha_dest])
        return {"ok": False, "status": "failed", "error": str(exc), **base}


def stage_package(
    name: str,
    version: str,
    staging_transaction: Optional[Path] = None,
    visibility: Optional[str] = None,
    arch: str = DEFAULT_ARCH,
    bucket: str = DEFAULT_BUCKET,
    dry_run: bool = True,
) -> Dict[str, Any]:
    clean_name = _clean_name(name)
    clean_version = _clean_name(version)
    if not clean_name:
        return {"ok": False, "error": "name is required"}
    if not clean_version:
        return {"ok": False, "name": clean_name, "error": "version is required"}
    name_resolution = resolve_downloadable_library_name(clean_name)
    if not name_resolution.get("ok"):
        return {
            "ok": False,
            "status": name_resolution.get("status", "library_name_resolution_failed"),
            "name": clean_name,
            "version": clean_version,
            "error": name_resolution.get("message", "library name resolution failed"),
            "library_name_resolution": name_resolution,
            "dry_run": bool(dry_run),
        }
    resolved_name = _clean_name(name_resolution.get("resolved_name"))

    transaction = Path(staging_transaction) if staging_transaction is not None else create_staging_transaction()
    downloads_dir = transaction / "downloads"
    packages_dir = transaction / "packages"
    package_dir = packages_dir / f"{resolved_name} {clean_version}"
    base = {
        "name": resolved_name,
        "input_name": clean_name,
        "version": clean_version,
        "key": dependency_key(resolved_name, clean_version),
        "staging_transaction": str(transaction),
        "downloads_dir": str(downloads_dir),
        "package_dir": str(package_dir),
        "marker": str(package_dir / CUSTOM_LIBRARY_MARKER),
        "dry_run": bool(dry_run),
        "library_name_resolution": name_resolution,
    }

    if dry_run:
        download_plan = download_package(
            resolved_name,
            clean_version,
            dest_dir=downloads_dir,
            visibility=visibility,
            arch=arch,
            bucket=bucket,
            dry_run=True,
        )
        return {"ok": True, "status": "planned", "download": download_plan, "uses_ini": None, **base}

    preflight = preflight_writable_directory(transaction, create=True)
    if not preflight.get("ok"):
        return {"ok": False, "status": "staging_preflight_failed", "preflight": preflight, **base}

    download_result = download_package(
        resolved_name,
        clean_version,
        dest_dir=downloads_dir,
        visibility=visibility,
        arch=arch,
        bucket=bucket,
        dry_run=False,
        keep_sha256=False,
    )
    if not download_result.get("ok"):
        return {"ok": False, "status": "download_failed", "download": download_result, **base}

    archive_path = Path(str(download_result.get("dest") or ""))
    try:
        _cleanup_paths([package_dir])
        package_dir.mkdir(parents=True, exist_ok=True)
        extract_result = extract_tar_zst(archive_path, package_dir)
        if not extract_result.get("ok"):
            _cleanup_paths([archive_path, package_dir])
            return {
                "ok": False,
                "status": "extract_failed",
                "download": download_result,
                "extract": extract_result,
                **base,
            }

        marker = package_dir / CUSTOM_LIBRARY_MARKER
        marker.touch(exist_ok=True)
        uses = parse_uses_ini(package_dir / "uses.ini")
        _cleanup_paths([archive_path])
        return {
            "ok": True,
            "status": "staged",
            "download": download_result,
            "extract": extract_result,
            "uses_ini": uses,
            **base,
        }
    except Exception as exc:
        _cleanup_paths([archive_path, package_dir])
        return {"ok": False, "status": "stage_failed", "download": download_result, "error": str(exc), **base}


def _package_install_entry(staged: Dict[str, Any], install_root: Path) -> Dict[str, Any]:
    name = _clean_name(staged.get("name"))
    version = _clean_name(staged.get("version"))
    target_dir = library_install_dir(install_root, name, version)
    return {
        "name": name,
        "version": version,
        "key": dependency_key(name, version),
        "source_dir": str(Path(str(staged.get("package_dir") or "")).resolve()),
        "target_dir": str(target_dir),
    }


def _copy_staged_package_direct(entry: Dict[str, Any], install_root: Path) -> Dict[str, Any]:
    name = _clean_name(entry.get("name"))
    version = _clean_name(entry.get("version"))
    key = dependency_key(name, version)
    source = Path(str(entry.get("source_dir") or "")).resolve()
    target = library_install_dir(install_root, name, version)
    tmp_root = Path(install_root).resolve() / INSTALLING_DIR_NAME
    tmp_target = tmp_root / f"{name} {version}"
    base = {
        "name": name,
        "version": version,
        "key": key,
        "source_dir": str(source),
        "target_dir": str(target),
        "tmp_target": str(tmp_target),
    }
    if target.exists():
        return {"ok": True, "status": "already_installed", **base}
    if not source.exists() or not source.is_dir():
        return {"ok": False, "status": "missing_staged_package", "error": "source package directory does not exist", **base}
    try:
        tmp_root.mkdir(parents=True, exist_ok=True)
        _cleanup_paths([tmp_target])
        shutil.copytree(source, tmp_target, symlinks=False)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp_target.rename(target)
        return {"ok": True, "status": "installed", **base}
    except Exception as exc:
        _cleanup_paths([tmp_target])
        return {"ok": False, "status": "install_failed", "error": str(exc), **base}


def _default_install_helper_path() -> Path:
    env = os.environ.get(INSTALL_HELPER_ENV_VAR, "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return Path(DEPLOY_ROOT).resolve() / "install-helper.exe"


def _write_install_manifest(
    staging_transaction: Path,
    install_root: Path,
    entries: List[Dict[str, Any]],
) -> Dict[str, Any]:
    manifest_path = Path(staging_transaction) / "manifest.json"
    result_path = Path(staging_transaction) / "result.json"
    manifest = {
        "schema_version": 1,
        "operation": "install_model_libraries",
        "staging_root": str(Path(staging_transaction).resolve()),
        "install_root": str(Path(install_root).resolve()),
        "packages": entries,
        "result_path": str(result_path.resolve()),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"manifest": manifest, "manifest_path": str(manifest_path.resolve()), "result_path": str(result_path.resolve())}


def _run_windows_install_helper(manifest_path: Path, helper_path: Optional[Path] = None, timeout_seconds: int = 600) -> Dict[str, Any]:
    helper = Path(helper_path) if helper_path is not None else _default_install_helper_path()
    helper = helper.resolve()
    manifest = Path(manifest_path).resolve()
    if PLATFORM != "Windows":
        return {"ok": False, "status": "unsupported_platform", "platform": PLATFORM, "error": "elevated helper is Windows-only"}
    if not helper.exists():
        return {
            "ok": False,
            "status": "helper_not_found",
            "helper": str(helper),
            "error": f"install helper not found: {helper}",
        }

    try:
        # Windows-only: ShellExecuteExW "runas" for elevated library install helper.
        # Keep ctypes off the module import path so Linux MCP startup does not load _ctypes/libffi.
        import ctypes
        import ctypes.wintypes as wintypes  # type: ignore[attr-defined]

        SEE_MASK_NOCLOSEPROCESS = 0x00000040
        WAIT_OBJECT_0 = 0x00000000
        WAIT_TIMEOUT = 0x00000102
        INFINITE_TIMEOUT = max(1, int(timeout_seconds * 1000))

        class SHELLEXECUTEINFOW(ctypes.Structure):
            _fields_ = [
                ("cbSize", wintypes.DWORD),
                ("fMask", wintypes.ULONG),
                ("hwnd", wintypes.HWND),
                ("lpVerb", wintypes.LPCWSTR),
                ("lpFile", wintypes.LPCWSTR),
                ("lpParameters", wintypes.LPCWSTR),
                ("lpDirectory", wintypes.LPCWSTR),
                ("nShow", ctypes.c_int),
                ("hInstApp", wintypes.HINSTANCE),
                ("lpIDList", wintypes.LPVOID),
                ("lpClass", wintypes.LPCWSTR),
                ("hkeyClass", wintypes.HKEY),
                ("dwHotKey", wintypes.DWORD),
                ("hIcon", wintypes.HANDLE),
                ("hProcess", wintypes.HANDLE),
            ]

        params = f'--manifest "{manifest}"'
        sei = SHELLEXECUTEINFOW()
        sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFOW)
        sei.fMask = SEE_MASK_NOCLOSEPROCESS
        sei.lpVerb = "runas"
        sei.lpFile = str(helper)
        sei.lpParameters = params
        sei.lpDirectory = str(helper.parent)
        sei.nShow = 0
        ok = ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei))
        if not ok:
            err = ctypes.GetLastError()
            return {"ok": False, "status": "launch_failed", "helper": str(helper), "manifest": str(manifest), "winerror": err}
        wait = ctypes.windll.kernel32.WaitForSingleObject(sei.hProcess, INFINITE_TIMEOUT)
        exit_code = wintypes.DWORD()
        ctypes.windll.kernel32.GetExitCodeProcess(sei.hProcess, ctypes.byref(exit_code))
        ctypes.windll.kernel32.CloseHandle(sei.hProcess)
        if wait == WAIT_TIMEOUT:
            return {"ok": False, "status": "timeout", "helper": str(helper), "manifest": str(manifest)}
        if wait != WAIT_OBJECT_0:
            return {"ok": False, "status": "wait_failed", "helper": str(helper), "manifest": str(manifest), "wait": int(wait)}
        return {"ok": exit_code.value == 0, "status": "finished", "helper": str(helper), "manifest": str(manifest), "exit_code": int(exit_code.value)}
    except Exception as exc:
        return {"ok": False, "status": "helper_failed", "helper": str(helper), "manifest": str(manifest), "error": str(exc)}


def submit_staged_packages(
    staged_packages: List[Dict[str, Any]],
    install_root: Optional[Path] = None,
    staging_transaction: Optional[Path] = None,
    allow_elevation: bool = True,
    elevation_mode: str = "auto",
    helper_path: Optional[Path] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    root = Path(install_root) if install_root is not None else default_library_download_dir()
    root = root.resolve()
    mode = (elevation_mode or "auto").strip().lower()
    if mode not in ("auto", "never", "require"):
        return {"ok": False, "stage": "submit", "error": f"unknown elevation_mode: {elevation_mode!r}"}

    entries: List[Dict[str, Any]] = []
    for staged in staged_packages:
        if not staged.get("ok"):
            continue
        try:
            entries.append(_package_install_entry(staged, root))
        except Exception as exc:
            return {"ok": False, "stage": "submit", "install_root": str(root), "error": str(exc), "staged": staged}

    response: Dict[str, Any] = {
        "ok": True,
        "stage": "submit",
        "install_root": str(root),
        "dry_run": bool(dry_run),
        "elevation": {"needed": False, "used": False, "method": ""},
        "results": {},
    }
    if not entries:
        response["status"] = "nothing_to_install"
        return response
    if dry_run:
        response["status"] = "planned"
        response["packages"] = entries
        return response

    preflight = preflight_writable_directory(root, create=True)
    direct_allowed = bool(preflight.get("ok")) and mode != "require"
    response["preflight"] = preflight

    if direct_allowed:
        ok = True
        results: Dict[str, Any] = {}
        for entry in entries:
            result = _copy_staged_package_direct(entry, root)
            results[entry["key"]] = result
            ok = ok and bool(result.get("ok"))
        response["ok"] = ok
        response["status"] = "installed" if ok else "install_failed"
        response["results"] = results
        return response

    response["elevation"]["needed"] = True
    if mode == "never" or not allow_elevation:
        response.update(
            {
                "ok": False,
                "status": "needs_elevation",
                "needs_elevation": True,
                "error": "install root is not writable",
            }
        )
        return response

    tx = Path(staging_transaction).resolve() if staging_transaction is not None else Path(entries[0]["source_dir"]).resolve().parents[1]
    manifest_info = _write_install_manifest(tx, root, entries)
    response["manifest"] = manifest_info
    helper_result = _run_windows_install_helper(Path(manifest_info["manifest_path"]), helper_path=helper_path)
    response["elevation"] = {"needed": True, "used": bool(helper_result.get("ok")), "method": "windows_uac_helper"}
    response["helper"] = helper_result

    result_path = Path(str(manifest_info.get("result_path") or ""))
    if result_path.exists():
        try:
            helper_payload = json.loads(result_path.read_text(encoding="utf-8"))
            response["results"] = helper_payload.get("results", {})
            response["ok"] = bool(helper_payload.get("ok")) and bool(helper_result.get("ok"))
            response["status"] = helper_payload.get("status", "helper_result")
            response["helper_result"] = helper_payload
            return response
        except Exception as exc:
            response["result_read_error"] = str(exc)

    response["ok"] = False
    response["status"] = helper_result.get("status", "helper_failed")
    response["error"] = helper_result.get("error", "elevated install helper failed")
    return response


def install_package(
    name: str,
    version: str,
    dest_dir: Optional[Path] = None,
    staging_transaction: Optional[Path] = None,
    staging_root: Optional[Path] = None,
    allow_elevation: bool = True,
    elevation_mode: str = "auto",
    helper_path: Optional[Path] = None,
    visibility: Optional[str] = None,
    arch: str = DEFAULT_ARCH,
    bucket: str = DEFAULT_BUCKET,
    dry_run: bool = True,
) -> Dict[str, Any]:
    clean_name = _clean_name(name)
    clean_version = _clean_name(version)
    if not clean_name:
        return {"ok": False, "error": "name is required"}
    if not clean_version:
        return {"ok": False, "name": clean_name, "error": "version is required"}
    name_resolution = resolve_downloadable_library_name(clean_name)
    if not name_resolution.get("ok"):
        return {
            "ok": False,
            "status": name_resolution.get("status", "library_name_resolution_failed"),
            "name": clean_name,
            "version": clean_version,
            "error": name_resolution.get("message", "library name resolution failed"),
            "library_name_resolution": name_resolution,
            "dry_run": bool(dry_run),
        }
    resolved_name = _clean_name(name_resolution.get("resolved_name"))

    library_root = Path(dest_dir) if dest_dir is not None else default_library_download_dir()
    try:
        target_dir = library_install_dir(library_root, resolved_name, clean_version)
    except ValueError as exc:
        return {"ok": False, "name": resolved_name, "input_name": clean_name, "version": clean_version, "error": str(exc)}

    base = {
        "name": resolved_name,
        "input_name": clean_name,
        "version": clean_version,
        "key": dependency_key(resolved_name, clean_version),
        "library_root": str(library_root),
        "target_dir": str(target_dir),
        "marker": str(target_dir / CUSTOM_LIBRARY_MARKER),
        "dry_run": bool(dry_run),
        "library_name_resolution": name_resolution,
    }

    if target_dir.exists():
        uses = parse_uses_ini(target_dir / "uses.ini")
        return {"ok": True, "status": "already_installed", "uses_ini": uses, **base}

    if dry_run:
        tx = Path(staging_transaction) if staging_transaction is not None else Path(staging_root) if staging_root is not None else default_library_staging_root()
        stage_plan = stage_package(
            resolved_name,
            clean_version,
            staging_transaction=tx,
            visibility=visibility,
            arch=arch,
            bucket=bucket,
            dry_run=True,
        )
        submit_plan = submit_staged_packages(
            [stage_plan],
            install_root=library_root,
            staging_transaction=tx,
            allow_elevation=allow_elevation,
            elevation_mode=elevation_mode,
            helper_path=helper_path,
            dry_run=True,
        )
        return {"ok": True, "status": "planned", "stage": stage_plan, "submit": submit_plan, "uses_ini": None, **base}

    tx = Path(staging_transaction) if staging_transaction is not None else create_staging_transaction(staging_root)
    stage_result = stage_package(
        resolved_name,
        clean_version,
        staging_transaction=tx,
        visibility=visibility,
        arch=arch,
        bucket=bucket,
        dry_run=False,
    )
    if not stage_result.get("ok"):
        cleanup = cleanup_staging_transaction(tx)
        return {"ok": False, "status": "stage_failed", "stage": stage_result, "staging_cleanup": cleanup, **base}

    submit_result = submit_staged_packages(
        [stage_result],
        install_root=library_root,
        staging_transaction=tx,
        allow_elevation=allow_elevation,
        elevation_mode=elevation_mode,
        helper_path=helper_path,
        dry_run=False,
    )
    cleanup = cleanup_staging_transaction(tx)
    install_ok = bool(stage_result.get("ok")) and bool(submit_result.get("ok"))
    return {
        "ok": install_ok and bool(cleanup.get("ok")),
        "status": "installed" if submit_result.get("ok") else submit_result.get("status", "install_failed"),
        "stage": stage_result,
        "submit": submit_result,
        "staging_cleanup": cleanup,
        "download": stage_result.get("download"),
        "extract": stage_result.get("extract"),
        "uses_ini": stage_result.get("uses_ini"),
        **base,
    }


def install_dependencies_recursive(
    dependencies: List[Dict[str, Any]],
    dest_dir: Optional[Path] = None,
    staging_root: Optional[Path] = None,
    staging_transaction: Optional[Path] = None,
    allow_elevation: bool = True,
    elevation_mode: str = "auto",
    helper_path: Optional[Path] = None,
    visibility: Optional[str] = None,
    arch: str = DEFAULT_ARCH,
    bucket: str = DEFAULT_BUCKET,
    dry_run: bool = True,
    stop_on_error: bool = True,
    max_depth: int = 32,
    installed_keys: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    queue: List[Tuple[Dict[str, Any], int, str]] = [(dict(dep), 0, "input") for dep in dependencies]
    processed: Set[str] = set()
    queued: Set[str] = set()
    installed_key_set = {str(key).strip().lower() for key in (installed_keys or set()) if str(key).strip()}
    results: Dict[str, Any] = {}
    staged_packages: List[Dict[str, Any]] = []
    ok = True
    transaction = (
        Path(staging_transaction)
        if staging_transaction is not None
        else (Path(staging_root) if dry_run and staging_root is not None else None)
    )
    if not dry_run and transaction is None:
        transaction = create_staging_transaction(staging_root)

    while queue:
        dep, depth, source = queue.pop(0)
        input_name = _clean_name(dep.get("name"))
        version = _clean_name(dep.get("version"))
        if not input_name or not version:
            continue
        name_resolution = resolve_downloadable_library_name(input_name)
        if not name_resolution.get("ok"):
            ok = False
            result_key = f"{input_name}@{version}" if version else input_name
            results[result_key] = {
                "ok": False,
                "status": name_resolution.get("status", "library_name_resolution_failed"),
                "name": input_name,
                "version": version,
                "source": source,
                "error": name_resolution.get("message", "library name resolution failed"),
                "library_name_resolution": name_resolution,
            }
            processed.add(result_key)
            queued.add(result_key)
            if stop_on_error:
                break
            continue
        name = _clean_name(name_resolution.get("resolved_name"))
        key = dependency_key(name, version)
        key_norm = key.lower()
        if key in processed:
            results.setdefault(key, {"ok": True, "status": "already_processed", "name": name, "version": version})
            continue
        if key_norm in installed_key_set:
            results[key] = {
                "ok": True,
                "status": "already_installed",
                "name": name,
                "input_name": input_name,
                "version": version,
                "source": source,
                "installed_source": "GetInstalledLibraries",
                "library_name_resolution": name_resolution,
            }
            processed.add(key)
            queued.add(key)
            continue
        if depth > max_depth:
            ok = False
            results[key] = {"ok": False, "status": "max_depth_exceeded", "name": name, "input_name": input_name, "version": version, "source": source}
            if stop_on_error:
                break
            continue

        library_root = Path(dest_dir) if dest_dir is not None else default_library_download_dir()
        try:
            target_dir = library_install_dir(library_root, name, version)
        except ValueError as exc:
            ok = False
            results[key] = {
                "ok": False,
                "status": "invalid_install_path",
                "name": name,
                "input_name": input_name,
                "version": version,
                "source": source,
                "error": str(exc),
                "library_name_resolution": name_resolution,
            }
            processed.add(key)
            queued.add(key)
            if stop_on_error:
                break
            continue

        if target_dir.exists():
            uses = parse_uses_ini(target_dir / "uses.ini")
            result = {
                "ok": True,
                "status": "already_installed",
                "name": name,
                "input_name": input_name,
                "version": version,
                "key": key,
                "library_root": str(library_root),
                "target_dir": str(target_dir),
                "marker": str(target_dir / CUSTOM_LIBRARY_MARKER),
                "uses_ini": uses,
                "depth": depth,
                "source": source,
                "library_name_resolution": name_resolution,
            }
            results[key] = result
            processed.add(key)
            queued.add(key)
        else:
            result = stage_package(
                name,
                version,
                staging_transaction=transaction,
                visibility=visibility,
                arch=arch,
                bucket=bucket,
                dry_run=dry_run,
            )
            result["depth"] = depth
            result["source"] = source
            result["library_root"] = str(library_root)
            result["target_dir"] = str(target_dir)
            result["input_name"] = input_name
            result["library_name_resolution"] = name_resolution
            results[key] = result
            processed.add(key)
            queued.add(key)
            if result.get("ok") and not dry_run:
                staged_packages.append(result)

        if not result.get("ok"):
            ok = False
            if stop_on_error:
                break
            continue

        uses = result.get("uses_ini")
        if not isinstance(uses, dict):
            continue
        for child in normalize_dependency_records(uses.get("dependencies") or [], source="uses_ini"):
            child_name = _clean_name(child.get("name"))
            child_version = _clean_name(child.get("version"))
            child_key = dependency_key(child_name, child_version)
            if not child_name or not child_version or child_key in processed or child_key in queued:
                continue
            queue.append((child, depth + 1, key))
            queued.add(child_key)

    submit_result: Dict[str, Any] = {"attempted": False, "reason": "no staged packages"}
    if staged_packages:
        library_root = Path(dest_dir) if dest_dir is not None else default_library_download_dir()
        submit_result = submit_staged_packages(
            staged_packages,
            install_root=library_root,
            staging_transaction=transaction,
            allow_elevation=allow_elevation,
            elevation_mode=elevation_mode,
            helper_path=helper_path,
            dry_run=dry_run,
        )
        ok = ok and bool(submit_result.get("ok"))
        submit_results = submit_result.get("results", {})
        if isinstance(submit_results, dict):
            for submit_key, submit_item in submit_results.items():
                if submit_key in results and isinstance(submit_item, dict):
                    results[submit_key]["submit"] = submit_item
                    if submit_item.get("ok"):
                        results[submit_key]["status"] = submit_item.get("status", results[submit_key].get("status"))
                    else:
                        results[submit_key]["ok"] = False
                        results[submit_key]["status"] = submit_item.get("status", "install_failed")
                        ok = False

    cleanup_result = cleanup_staging_transaction(transaction) if not dry_run else {"ok": True, "status": "skipped", "reason": "dry_run"}
    ok = ok and bool(cleanup_result.get("ok"))

    return {
        "ok": ok,
        "results": results,
        "processed": sorted(processed),
        "staging_transaction": str(transaction) if transaction is not None else "",
        "submit": submit_result,
        "staging_cleanup": cleanup_result,
    }

def fill_missing_versions_from_latest(
    dependencies: List[Dict[str, Any]],
    visibility: Optional[str] = None,
    bucket: str = DEFAULT_BUCKET,
) -> Dict[str, Any]:
    resolved: List[Dict[str, Any]] = []
    latest_results: Dict[str, Any] = {}
    ok = True
    for dep in dependencies:
        item = dict(dep)
        input_name = _clean_name(item.get("name"))
        version = _clean_name(item.get("version"))
        name_resolution = resolve_downloadable_library_name(input_name) if input_name else {"ok": False}
        if input_name and name_resolution.get("ok"):
            name = _clean_name(name_resolution.get("resolved_name"))
            item["input_name"] = input_name
            item["name"] = name
            item["library_name_resolution"] = name_resolution
            if name_resolution.get("warning"):
                item["warning"] = name_resolution.get("warning")
        else:
            name = input_name
            if input_name:
                item["library_name_resolution"] = name_resolution
                ok = False
        if name and not version:
            latest = fetch_latest_version(name, visibility=visibility, bucket=bucket)
            latest_results[name] = latest
            if latest.get("ok"):
                item["version"] = latest.get("version", "")
                item["version_source"] = latest.get("version_source") or "remote_latest"
            else:
                ok = False
        resolved.append(item)
    return {"ok": ok, "dependencies": resolved, "latest": latest_results}


def build_list_url(bucket: str, prefix: Optional[str] = None, continuation_token: Optional[str] = None) -> str:
    query = {"list-type": "2"}
    if prefix:
        query["prefix"] = prefix
    if continuation_token:
        query["continuation-token"] = continuation_token
    return f"{ENDPOINT}/{bucket}/?{urllib.parse.urlencode(query)}"


def fetch_xml(url: str) -> ET.Element:
    with urllib.request.urlopen(url) as response:
        return ET.fromstring(response.read())


def _get_text(root: ET.Element, path: str) -> Optional[str]:
    element = root.find(path, S3_NS)
    return element.text if element is not None else None


def list_storage_keys(bucket: str = DEFAULT_BUCKET, prefix: str = "public/") -> Dict[str, Any]:
    keys: List[str] = []
    continuation_token: Optional[str] = None
    try:
        while True:
            root = fetch_xml(build_list_url(bucket, prefix, continuation_token))
            for element in root.findall("s3:Contents/s3:Key", S3_NS):
                if element.text:
                    keys.append(element.text)
            is_truncated = (_get_text(root, "s3:IsTruncated") or "").lower() == "true"
            if not is_truncated:
                return {"ok": True, "bucket": bucket, "prefix": prefix, "keys": keys}
            continuation_token = _get_text(root, "s3:NextContinuationToken")
            if not continuation_token:
                return {
                    "ok": False,
                    "bucket": bucket,
                    "prefix": prefix,
                    "keys": keys,
                    "error": "bucket listing is truncated but no continuation token was returned",
                }
    except Exception as exc:
        return {"ok": False, "bucket": bucket, "prefix": prefix, "keys": keys, "error": str(exc)}
