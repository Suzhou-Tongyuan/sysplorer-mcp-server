"""Elevated helper for installing staged model libraries on Windows.

This helper intentionally supports one narrow operation: copy staged package
directories into the configured Sysplorer Library root. It must not become a
general-purpose elevated file operation tool.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List


INSTALLING_DIR_NAME = ".mworks_mcp_installing"


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _result_path(manifest: Dict[str, Any], fallback: Path) -> Path:
    raw = _clean(manifest.get("result_path"))
    return Path(raw).resolve() if raw else fallback.with_name("result.json")


def _write_result(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _validate_name_version(name: str, version: str) -> None:
    if not name or not version:
        raise ValueError("name and version are required")
    if any(ch in name or ch in version for ch in ("\\", "/", ":")):
        raise ValueError("name and version must not contain path separators")


def _reject_links(source: Path) -> None:
    for child in source.rglob("*"):
        if child.is_symlink():
            raise ValueError(f"symbolic links are not allowed in staged package: {child}")


def _install_one(pkg: Dict[str, Any], staging_root: Path, install_root: Path) -> Dict[str, Any]:
    name = _clean(pkg.get("name"))
    version = _clean(pkg.get("version"))
    _validate_name_version(name, version)
    dirname = f"{name} {version}"
    source = Path(_clean(pkg.get("source_dir"))).resolve()
    target = Path(_clean(pkg.get("target_dir"))).resolve()
    expected_target = (install_root / dirname).resolve()
    tmp_target = (install_root / INSTALLING_DIR_NAME / dirname).resolve()
    base = {
        "name": name,
        "version": version,
        "key": f"{name}@{version}",
        "source_dir": str(source),
        "target_dir": str(target),
        "tmp_target": str(tmp_target),
    }

    if not _is_relative_to(source, staging_root):
        return {"ok": False, "status": "invalid_source", "error": "source_dir is outside staging_root", **base}
    if not _is_relative_to(target, install_root):
        return {"ok": False, "status": "invalid_target", "error": "target_dir is outside install_root", **base}
    if target != expected_target:
        return {"ok": False, "status": "invalid_target", "error": "target_dir does not match name/version", **base}
    if target.exists():
        return {"ok": True, "status": "already_installed", **base}
    if not source.exists() or not source.is_dir():
        return {"ok": False, "status": "missing_source", "error": "source_dir does not exist", **base}

    try:
        _reject_links(source)
        tmp_target.parent.mkdir(parents=True, exist_ok=True)
        if tmp_target.exists():
            shutil.rmtree(tmp_target)
        shutil.copytree(source, tmp_target, symlinks=False)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp_target.rename(target)
        return {"ok": True, "status": "installed", **base}
    except Exception as exc:
        try:
            if tmp_target.exists():
                shutil.rmtree(tmp_target)
        except OSError:
            pass
        return {"ok": False, "status": "install_failed", "error": str(exc), **base}


def run(manifest_path: Path) -> int:
    manifest_file = manifest_path.resolve()
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except Exception as exc:
        fallback_result = manifest_file.with_name("result.json")
        _write_result(fallback_result, {"ok": False, "status": "manifest_read_failed", "error": str(exc)})
        return 2

    result_file = _result_path(manifest, manifest_file)
    try:
        if manifest.get("schema_version") != 1:
            raise ValueError("schema_version must be 1")
        if manifest.get("operation") != "install_model_libraries":
            raise ValueError("unsupported operation")
        staging_root = Path(_clean(manifest.get("staging_root"))).resolve()
        install_root = Path(_clean(manifest.get("install_root"))).resolve()
        packages = manifest.get("packages")
        if not staging_root.exists() or not staging_root.is_dir():
            raise ValueError("staging_root does not exist")
        if not isinstance(packages, list):
            raise ValueError("packages must be a list")

        results: Dict[str, Any] = {}
        ok = True
        for pkg in packages:
            if not isinstance(pkg, dict):
                ok = False
                results[f"invalid@{len(results)}"] = {"ok": False, "status": "invalid_package"}
                continue
            result = _install_one(pkg, staging_root, install_root)
            results[result.get("key", f"unknown@{len(results)}")] = result
            ok = ok and bool(result.get("ok"))

        payload = {"ok": ok, "status": "installed" if ok else "install_failed", "results": results}
        _write_result(result_file, payload)
        return 0 if ok else 1
    except Exception as exc:
        _write_result(result_file, {"ok": False, "status": "failed", "error": str(exc), "results": {}})
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Install staged MWORKS model libraries.")
    parser.add_argument("--manifest", required=True, help="Path to manifest.json generated by the MCP server.")
    args = parser.parse_args()
    return run(Path(args.manifest))


if __name__ == "__main__":
    sys.exit(main())
