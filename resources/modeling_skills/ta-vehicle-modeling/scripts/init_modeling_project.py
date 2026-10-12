#!/usr/bin/env python3
"""
Initialize a Sysplorer modeling project workspace.
"""

from __future__ import annotations

import argparse
from pathlib import Path


SUBDIRS = [
    "sources",
    "inputs",
    "artifacts",
    "deliverables",
    "logs",
]


def init_project(project_name: str, output_root: Path) -> Path:
    project_dir = output_root / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    for subdir in SUBDIRS:
        (project_dir / subdir).mkdir(exist_ok=True)
    return project_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize a Sysplorer modeling project directory."
    )
    parser.add_argument("project_name", help="Project folder name")
    parser.add_argument(
        "-o",
        "--output-root",
        default="projects",
        help="Root directory for project creation (default: projects)",
    )
    args = parser.parse_args()

    project_dir = init_project(args.project_name, Path(args.output_root))
    print(f"[OK] Project initialized: {project_dir}")
    for subdir in SUBDIRS:
        print(f"  - {project_dir / subdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
