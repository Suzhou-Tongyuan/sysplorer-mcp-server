#!/usr/bin/env python3
"""Prepare or audit a geometry-free Sysblock layout input."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from audit_layout_input import audit
from prepare_layout_input import prepare
from lib.sysblock_core import read_json, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("prepare", "audit"):
        child = sub.add_parser(command)
        child.add_argument("input", type=Path)
        child.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = prepare(read_json(args.input)) if args.command == "prepare" else audit(read_json(args.input))
    if args.output:
        write_json(result, args.output)
    else:
        sys.stdout.write(write_json(result))
    if args.command == "audit":
        raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
