#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import zipfile
from collections import Counter
from pathlib import Path


def scan_directory(root: Path) -> dict:
    packages = []
    counters = Counter()
    for path in root.rglob("*"):
        if path.is_dir():
            name = path.name.lower()
            if name in {"tests", "test", "examples", "example", "resources", "basic", "components", "types"}:
                counters[name] += 1
        elif path.is_file():
            if path.name == "package.mo":
                packages.append(str(path.parent))
            if "simulink" in path.name.lower():
                counters["simulink_named_files"] += 1
            if path.suffix.lower() == ".modd":
                counters["modd_files"] += 1
    return {
        "source_type": "directory",
        "root": str(root),
        "package_count": len(packages),
        "packages": packages,
        "counters": dict(counters),
    }


def scan_archive(archive_path: Path) -> dict:
    counters = Counter()
    top_levels = Counter()
    package_entries = []
    with zipfile.ZipFile(archive_path) as zf:
        for name in zf.namelist():
            lower = name.lower()
            parts = [p for p in name.split("/") if p]
            if len(parts) >= 2:
                top_levels[parts[1]] += 1
            if lower.endswith("package.moc") or lower.endswith("package.mo"):
                package_entries.append(name)
            for key in ("tests", "test", "examples", "example", "resources", "basic", "components", "types"):
                if f"/{key}/" in lower:
                    counters[key] += 1
            if "simulink" in lower:
                counters["simulink_named_files"] += 1
            if lower.endswith(".modd"):
                counters["modd_files"] += 1
    return {
        "source_type": "archive",
        "root": str(archive_path),
        "package_count": len(package_entries),
        "top_levels": dict(top_levels),
        "sample_packages": package_entries[:50],
        "counters": dict(counters),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory a Modelica directory or .mol archive.")
    parser.add_argument("path", help="Directory or .mol/.zip file to inspect.")
    args = parser.parse_args()

    target = Path(args.path).resolve()
    if target.is_dir():
        result = scan_directory(target)
    elif target.is_file():
        result = scan_archive(target)
    else:
        raise SystemExit(f"Path does not exist: {target}")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
