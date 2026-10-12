#!/usr/bin/env python3
"""Create one Sysblock structured-evidence audit report.

This local CLI is read-only. It validates stale-evidence protection, recomputes
the canonical layout audits, and summarizes model, semantics, layout,
StateMachine, and recorded check sections. It does not prove complete model
validation or replace required Sysplorer save/reload, diagram review, checks,
translation, simulation, or tests.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lib.model_readback import evidence_summary
from lib.sysblock_core import read_json, write_json
from sysblock_evidence_audit import audit_evidence


def audit_model(model_file: Path, evidence: dict) -> dict:
    summary = evidence_summary(model_file, evidence)
    audit = audit_evidence(model_file, evidence)
    hierarchy = evidence.get("hierarchy", {}) if isinstance(evidence.get("hierarchy"), dict) else {}
    report = {
        "schema": "sysblock-evidence-audit/v1",
        "audit_passed": bool(audit.get("audit_passed")) and not summary["evidence_stale"] and summary["readback_sources_valid"],
        "model": summary,
        "semantics": {
            "task_type": evidence.get("task_type"),
            "topology_or_layout_changed": evidence.get("change_scope", {}).get("topology_or_layout_changed"),
            "hierarchy_complete": hierarchy.get("complete") is True,
        },
        "layout": {
            "affected_levels": evidence.get("affected_levels", []),
            "level_results": audit.get("levels", []),
        },
        "statechart": {
            "affected_charts": evidence.get("affected_charts", []),
            "chart_results": audit.get("charts", []),
        },
        "checks": {
            "check_model": evidence.get("check_model", {}),
            "warnings": evidence.get("warnings", {}),
        },
        "failure_count": audit.get("failure_count", 0),
        "failure_codes": audit.get("failure_codes", []),
        "failures": audit.get("failures", []),
    }
    if summary["evidence_stale"] and "MODEL_HASH_MISMATCH" not in report["failure_codes"]:
        report["failure_codes"].append("MODEL_HASH_MISMATCH")
        report["failures"].append({"code": "MODEL_HASH_MISMATCH"})
        report["failure_count"] += 1
    if not summary["readback_sources_valid"]:
        report["failure_codes"].append("READBACK_SOURCE_INVALID")
        report["failures"].append({"code": "READBACK_SOURCE_INVALID", "sources": summary["readback_sources"]})
        report["failure_count"] += 1
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-file", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit_model(args.model_file, read_json(args.evidence))
    if args.output:
        write_json(report, args.output)
    else:
        sys.stdout.write(write_json(report))
    raise SystemExit(0 if report["audit_passed"] else 1)


if __name__ == "__main__":
    main()
