#!/usr/bin/env python3
"""Resolve only requested Sysblock APIs; never enumerate or mutate models."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lib.sysblock_core import read_json, write_json


DEFAULT_CONTRACTS = Path(__file__).resolve().parents[1] / "references" / "api-contracts.json"


def resolve(api_names: list[str], version: str | None, contracts: dict) -> dict:
    index = {item["api_name"]: item for item in contracts.get("contracts", [])}
    unique_names = list(dict.fromkeys(api_names))
    known = []
    needs_exact_doc = []
    needs_behavior_probe = []
    unsupported = []
    for name in unique_names:
        contract = index.get(name)
        if contract is None:
            needs_exact_doc.append({
                "api_name": name,
                "code": "API_EXACT_DOC_REQUIRED",
                "query_limit": 1,
                "next": "query the exact API name; do not enumerate all functions",
            })
            continue
        versions = contract.get("verified_versions", [])
        if version and versions and version not in versions:
            needs_exact_doc.append({
                "api_name": name,
                "code": "API_EXACT_DOC_REQUIRED",
                "query_limit": 1,
                "reason": f"contract is not verified for {version}",
            })
            continue
        if version in contract.get("unsupported_versions", []):
            unsupported.append({"api_name": name, "code": "API_UNSUPPORTED", "fallback": contract.get("fallback")})
            continue
        known.append({
            "api_name": name,
            "probe_count": 0,
            "minimal_arguments": contract.get("minimal_arguments", []),
            "return_contract": contract.get("return_contract"),
            "side_effects": contract.get("side_effects", []),
            "fallback": contract.get("fallback"),
        })
        if contract.get("behavior_unverified") is True:
            needs_behavior_probe.append({
                "api_name": name,
                "code": "API_BEHAVIOR_PROBE_REQUIRED",
                "probe_limit": 1,
                "safe_probe": contract.get("safe_probe"),
            })
    return {
        "schema": "sysblock-api-resolution/v1",
        "runtime_version": version,
        "requested_count": len(api_names),
        "unique_count": len(unique_names),
        "known": known,
        "needs_exact_doc": needs_exact_doc,
        "needs_behavior_probe": needs_behavior_probe,
        "unsupported": unsupported,
        "full_enumeration_allowed": False,
        "target_model_probe_allowed": False,
        "estimated_probe_count": len(needs_behavior_probe),
        "passed": not needs_exact_doc and not needs_behavior_probe and not unsupported,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apis", nargs="*", help="exact API names used by this task")
    parser.add_argument("--version")
    parser.add_argument("--contracts", type=Path, default=DEFAULT_CONTRACTS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.apis:
        parser.error("provide at least one exact API name")
    report = resolve(args.apis, args.version, read_json(args.contracts))
    rendered = write_json(report, args.output)
    if args.output is None:
        sys.stdout.write(rendered)
    raise SystemExit(0 if report["passed"] else 2)


if __name__ == "__main__":
    main()
