"""Fail-closed audit of saved/readback Sysblock structured evidence.

The audit recomputes Sysblock and Chart layout results from raw evidence. It
never accepts a project-authored ``passed`` value as a substitute for the
canonical auditors. Missing, partial, stale, or policy-violating evidence is
failure. Deterministic negative-path checks live in ``tests/test_skill.py``.
"""

from __future__ import annotations

import copy
import math
from pathlib import Path
from typing import Any

from audit_layout_input import audit as audit_layout_input
from audit_sysblock_layout import audit as audit_sysblock
from layout_geometry_audit import audit as audit_chart
from lib.sysblock_core import sha256_file


SCHEMA = "sysblock-modeling-evidence/v2"
TASK_TYPES = {"build", "edit", "audit"}
CHART_ELEMENT_ALLOWLIST = {
    "state",
    "childstate",
    "nestedstate",
    "parallelstate",
    "subchartstate",
    "transition",
    "defaulttransition",
    "data",
    "event",
    "junction",
}


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def numeric_vector(value: Any, length: int) -> bool:
    return isinstance(value, list) and len(value) == length and all(finite_number(item) for item in value)


def template(model_file: str = "C:/absolute/path/Model.mo") -> dict[str, Any]:
    layout_input = {
        "schema": "sysblock-layout-input/v1",
        "case_id": "Model-layout",
        "levels": [
            {
                "path": "Model",
                "nodes": [
                    {"id": "u", "kind": "Inport", "name": "u", "inputs": [], "outputs": ["y"]},
                    {"id": "y", "kind": "Outport", "name": "y", "inputs": ["u"], "outputs": []},
                ],
                "edges": [
                    {"id": "u_to_y", "source": "u", "source_port": "y", "target": "y", "target_port": "u", "one_to_one_interface": True}
                ],
                "feedback_paths": [],
            }
        ],
        "charts": [],
        "policies": {
            "ordinary_size": "standard",
            "resizable_kinds": ["SubSystem", "Chart", "State", "Mux", "DeMux"],
            "topology_frozen": True,
            "uniform_subsystem_size_allowed": True,
        },
    }
    input_hash = audit_layout_input(layout_input)["canonical_sha256"]
    straight_manifest = {
        "schema": "sysblock-layout-manifest/v1",
        "mode": "readback",
        "level": "Model",
        "profile": {"feedback_stub": 16.0, "max_outer_margin": 40.0},
        "nodes": [
            {
                "id": "u",
                "kind": "Inport",
                "frame": [-110, -10, -90, 10],
                "name_zone": [-110, -28, -90, -10],
                "inputs": [],
                "outputs": ["y"],
                "port_anchors": {"inputs": {}, "outputs": {"y": [-90, 0]}},
                "port_label_zones": {"inputs": {}, "outputs": {}},
            },
            {
                "id": "y",
                "kind": "Outport",
                "frame": [90, -10, 110, 10],
                "name_zone": [90, -28, 110, -10],
                "inputs": ["u"],
                "outputs": [],
                "port_anchors": {"inputs": {"u": [90, 0]}, "outputs": {}},
                "port_label_zones": {"inputs": {}, "outputs": {}},
            },
        ],
        "edges": [
            {
                "id": "u_to_y",
                "source": "u",
                "source_port": "y",
                "target": "y",
                "target_port": "u",
                "points": [[-90, 0], [90, 0]],
            }
        ],
        "canvas": [-130, -40, 130, 30],
        "contract": {
            "placement_frozen_before_modeling": True,
            "topology_frozen_before_modeling": True,
            "space_feasibility_checked": True,
            "routes_frozen_before_modeling": True,
            "ordinary_route_points_authoritative": True,
        },
    }
    preconnect_manifest = copy.deepcopy(straight_manifest)
    preconnect_manifest["mode"] = "preconnect"
    preconnect_manifest["contract"]["routes_frozen_before_modeling"] = False
    preconnect_manifest["contract"]["ordinary_route_points_authoritative"] = False
    preconnect_manifest["layout_input_sha256"] = input_hash
    return {
        "schema": SCHEMA,
        "task_type": "edit",
        "model_file": model_file,
        "model_sha256": "REPLACE_WITH_CURRENT_SHA256",
        "affected_levels": ["Model"],
        "affected_charts": [],
        "change_scope": {"topology_or_layout_changed": True},
        "layout_input": {
            "status": "required",
            "canonical_sha256": input_hash,
            "data": layout_input,
        },
        "delivery": {"clean_warnings_required": True},
        "save_reload": {
            "executed": True,
            "passed": True,
            "force_reload": True,
            "reload_path": model_file,
        },
        "pre_layout": {
            "status": "required",
            "levels": [
                {
                    "path": "Model",
                    "source": "static_plan",
                    "manifest": preconnect_manifest,
                }
            ],
            "charts": [],
        },
        "check_model": {"executed": True, "passed": True},
        "warnings": {"executed": True, "count": 0, "messages": []},
        "hierarchy": {
            "executed": True,
            "complete": True,
            "source": "force_reloaded_api",
            "root": "Model",
            "levels": ["Model"],
            "charts": [],
        },
        "levels": [
            {
                "path": "Model",
                "source": "force_reloaded_api",
                "model_sha256": "REPLACE_WITH_CURRENT_SHA256",
                "routing": {
                    "executed": True,
                    "route_line_passes": [
                        {"pass": 1, "reason": "initial_routing"}
                    ],
                    "final_interface_feedback_adjustment": True,
                    "explicit_routes": [],
                    "route_line_after_explicit_routes": False,
                },
                "manifest": straight_manifest,
            }
        ],
        "charts": [],
    }


class EvidenceAudit:
    def __init__(self, model_file: Path, evidence: dict[str, Any]) -> None:
        self.model_file = model_file.resolve()
        self.evidence = evidence
        self.failures: list[dict[str, Any]] = []
        self.level_results: list[dict[str, Any]] = []
        self.chart_results: list[dict[str, Any]] = []
        self.model_sha256 = ""

    def fail(self, code: str, **detail: Any) -> None:
        self.failures.append({"code": code, **detail})

    def require_true(self, obj: Any, key: str, code: str) -> None:
        if not isinstance(obj, dict) or obj.get(key) is not True:
            self.fail(code)

    def section(self, name: str, value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            return value
        self.fail(f"{name.upper()}_SECTION_INVALID")
        return {}

    def path_list(self, name: str, value: Any, *, nonempty: bool = False) -> list[str]:
        code = name.upper()
        if not isinstance(value, list):
            self.fail(f"{code}_INVALID")
            return []
        paths = [item for item in value if isinstance(item, str) and item.strip()]
        if len(paths) != len(value):
            self.fail(f"{code}_INVALID")
        if len(paths) != len(set(paths)):
            self.fail(f"{code}_DUPLICATE", actual=paths)
        if nonempty and not paths:
            self.fail(f"{code}_MISSING")
        return paths

    def records(self, name: str, value: Any, source: str) -> list[dict[str, Any]]:
        code = name.upper()
        if not isinstance(value, list):
            self.fail(f"{code}_INVALID")
            return []
        records = []
        for index, item in enumerate(value):
            if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not item["path"].strip():
                self.fail(f"{code}_RECORD_INVALID", index=index)
                continue
            if item.get("source") != source:
                self.fail(f"{code}_SOURCE_INVALID", path=item["path"], expected=source)
            records.append(item)
        self.path_list(code, [item["path"] for item in records])
        return records

    def require_exact_paths(self, name: str, expected: list[str], actual: list[str]) -> None:
        if set(expected) != set(actual):
            self.fail(
                f"{name.upper()}_INCOMPLETE",
                missing=sorted(set(expected) - set(actual)),
                unexpected=sorted(set(actual) - set(expected)),
            )

    def audit_manifest(self, phase: str, path: str, manifest: Any) -> dict[str, Any] | None:
        if not isinstance(manifest, dict):
            self.fail("MANIFEST_MISSING", phase=phase, path=path)
            return None
        invalid = False
        if manifest.get("level") != path:
            self.fail("MANIFEST_LEVEL_MISMATCH", phase=phase, path=path)
            invalid = True
        nodes = manifest.get("nodes")
        edges = manifest.get("edges")
        if not isinstance(nodes, list) or not nodes:
            self.fail("MANIFEST_NODES_MISSING", phase=phase, path=path)
            invalid = True
            nodes = []
        if not isinstance(edges, list) or not edges:
            self.fail("MANIFEST_EDGES_MISSING", phase=phase, path=path)
            invalid = True
            edges = []
        if not numeric_vector(manifest.get("canvas"), 4):
            self.fail("MANIFEST_CANVAS_MISSING", phase=phase, path=path)
            invalid = True
        profile = manifest.get("profile")
        max_margin = profile.get("max_outer_margin") if isinstance(profile, dict) else None
        if not finite_number(max_margin) or max_margin < 0:
            self.fail("MANIFEST_WHITESPACE_POLICY_MISSING", phase=phase, path=path)
            invalid = True
        required_node_fields = {
            "id", "kind", "frame", "name_zone", "inputs", "outputs", "port_anchors", "port_label_zones"
        }
        node_ids = []
        for index, node in enumerate(nodes):
            if not isinstance(node, dict) or not required_node_fields.issubset(node):
                self.fail("MANIFEST_NODE_INCOMPLETE", phase=phase, path=path, index=index)
                invalid = True
                continue
            if not isinstance(node.get("id"), str) or not node["id"].strip():
                self.fail("MANIFEST_NODE_ID_INVALID", phase=phase, path=path, index=index)
                invalid = True
            else:
                node_ids.append(node["id"])
            if not numeric_vector(node.get("frame"), 4) or not numeric_vector(node.get("name_zone"), 4):
                self.fail("MANIFEST_NODE_GEOMETRY_INVALID", phase=phase, path=path, node=node.get("id"))
                invalid = True
        if len(node_ids) != len(set(node_ids)):
            self.fail("MANIFEST_NODE_ID_DUPLICATE", phase=phase, path=path)
            invalid = True
        edge_ids = []
        required_edge_fields = {"id", "source", "source_port", "target", "target_port", "points"}
        for index, edge in enumerate(edges):
            if not isinstance(edge, dict) or not required_edge_fields.issubset(edge):
                self.fail("MANIFEST_EDGE_INCOMPLETE", phase=phase, path=path, index=index)
                invalid = True
                continue
            points = edge.get("points")
            if (
                not isinstance(edge.get("id"), str)
                or not edge["id"].strip()
                or not isinstance(points, list)
                or len(points) < 2
                or not all(numeric_vector(point, 2) for point in points)
            ):
                self.fail("MANIFEST_EDGE_INVALID", phase=phase, path=path, index=index)
                invalid = True
            else:
                edge_ids.append(edge["id"])
        if len(edge_ids) != len(set(edge_ids)):
            self.fail("MANIFEST_EDGE_ID_DUPLICATE", phase=phase, path=path)
            invalid = True
        if phase == "pre":
            contract = manifest.get("contract", {})
            if (
                manifest.get("mode") != "preconnect"
                or contract.get("placement_frozen_before_modeling") is not True
                or contract.get("topology_frozen_before_modeling") is not True
                or contract.get("space_feasibility_checked") is not True
                or contract.get("ordinary_route_points_authoritative") is not False
            ):
                self.fail("PRE_LAYOUT_CONTRACT_INCOMPLETE", path=path)
                invalid = True
        if invalid:
            return None
        try:
            result = audit_sysblock(manifest)
        except Exception as exc:  # fail closed on auditor or evidence errors
            self.fail("SYSBLOCK_AUDITOR_ERROR", phase=phase, path=path, error=str(exc))
            return None
        if not result.get("passed"):
            self.fail(
                "SYSBLOCK_AUDIT_FAILED",
                phase=phase,
                path=path,
                issues=result.get("issues", []),
            )
        integrity = result.get("connection_integrity", {})
        if integrity.get("executed") is not True or integrity.get("passed") is not True:
            self.fail("CONNECTION_INTEGRITY_FAILED", phase=phase, path=path)
        return result

    def audit_chart_layout(self, phase: str, path: str, layout: Any) -> dict[str, Any] | None:
        if not isinstance(layout, dict):
            self.fail("CHART_LAYOUT_MISSING", phase=phase, path=path)
            return None
        blocks = layout.get("blocks")
        routes = layout.get("routes")
        if layout.get("chart_path") != path:
            self.fail("CHART_LAYOUT_PATH_MISMATCH", phase=phase, path=path)
            return None
        if not isinstance(blocks, list) or not blocks or not isinstance(routes, list) or not routes:
            self.fail("CHART_LAYOUT_EMPTY", phase=phase, path=path)
            return None
        try:
            result = audit_chart(layout, min_gap=30.0)
        except Exception as exc:
            self.fail("CHART_AUDITOR_ERROR", phase=phase, path=path, error=str(exc))
            return None
        if not result.get("passed"):
            self.fail(
                "CHART_LAYOUT_FAILED",
                phase=phase,
                path=path,
                issues=result.get("issues", []),
            )
        return result

    def check_plan_input_binding(
        self,
        layout_input: dict[str, Any],
        input_hash: str,
        pre_levels: list[dict[str, Any]],
        pre_charts: list[dict[str, Any]],
    ) -> None:
        level_map = {item.get("path"): item for item in layout_input.get("levels", [])}
        chart_map = {item.get("path"): item for item in layout_input.get("charts", [])}
        for record in pre_levels:
            path = record["path"]
            manifest = record.get("manifest")
            expected = level_map.get(path)
            if not isinstance(manifest, dict) or manifest.get("layout_input_sha256") != input_hash:
                self.fail("PLAN_INPUT_MISMATCH", path=path, detail="hash")
                continue
            if not isinstance(expected, dict):
                self.fail("PLAN_INPUT_MISMATCH", path=path, detail="level")
                continue
            expected_nodes = {item.get("id") for item in expected.get("nodes", [])}
            actual_nodes = {item.get("id") for item in manifest.get("nodes", [])}
            expected_edges = {
                (item.get("id"), item.get("source"), item.get("source_port"), item.get("target"), item.get("target_port"))
                for item in expected.get("edges", [])
            }
            actual_edges = {
                (item.get("id"), item.get("source"), item.get("source_port"), item.get("target"), item.get("target_port"))
                for item in manifest.get("edges", [])
            }
            if expected_nodes != actual_nodes or expected_edges != actual_edges:
                self.fail("PLAN_INPUT_MISMATCH", path=path, detail="topology")
        for record in pre_charts:
            path = record["path"]
            layout = record.get("layout")
            expected = chart_map.get(path)
            if not isinstance(layout, dict) or layout.get("layout_input_sha256") != input_hash:
                self.fail("PLAN_INPUT_MISMATCH", path=path, detail="hash")
                continue
            if not isinstance(expected, dict):
                self.fail("PLAN_INPUT_MISMATCH", path=path, detail="chart")
                continue
            if layout.get("chart_decomposition") != expected.get("decomposition"):
                self.fail("PLAN_INPUT_MISMATCH", path=path, detail="chart decomposition")
            expected_states = {item.get("id") for item in expected.get("states", [])}
            actual_states = {item.get("name") for item in layout.get("blocks", [])}
            expected_transitions = {
                (item.get("id"), "DEFAULT" if item.get("source") is None else item.get("source"), item.get("target"), item.get("priority"))
                for item in expected.get("transitions", [])
            }
            actual_transitions = {
                (item.get("name"), item.get("source"), item.get("destination"), item.get("priority"))
                for item in layout.get("routes", [])
            }
            if expected_states != actual_states or expected_transitions != actual_transitions:
                self.fail("PLAN_INPUT_MISMATCH", path=path, detail="chart topology")

    def check_chart_ports(self, path: str, record: Any) -> None:
        ports = record.get("port_integrity", {}) if isinstance(record, dict) else {}
        if not isinstance(ports, dict):
            self.fail("CHART_PORT_EVIDENCE_MISSING", path=path)
            return
        if ports.get("executed") is not True:
            self.fail("CHART_PORT_INTEGRITY_FAILED", path=path)
        for key in ("unconnected_inputs", "unconnected_outputs", "invalid_endpoints"):
            value = ports.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                self.fail("CHART_PORT_EVIDENCE_MISSING", path=path, field=key)
            elif value != 0:
                self.fail("CHART_PORT_UNCONNECTED", path=path, field=key, count=value)

    def check_chart_element_allowlist(self, path: str, record: Any) -> None:
        inventory = record.get("element_inventory") if isinstance(record, dict) else None
        if not isinstance(inventory, dict) or inventory.get("source") != "force_reloaded_api":
            self.fail("CHART_ELEMENT_INVENTORY_MISSING", path=path)
            return
        elements = inventory.get("elements")
        if not isinstance(elements, list):
            self.fail("CHART_ELEMENT_INVENTORY_INVALID", path=path)
            return
        for index, element in enumerate(elements):
            kind = element.get("kind") if isinstance(element, dict) else element
            normalized = str(kind).replace(" ", "").lower()
            if normalized not in CHART_ELEMENT_ALLOWLIST:
                self.fail(
                    "CHART_ELEMENT_NOT_IN_ALLOWLIST",
                    path=path,
                    index=index,
                    kind=kind,
                )

    def check_routing(self, path: str, record: Any) -> None:
        routing = record.get("routing") if isinstance(record, dict) else None
        if not isinstance(routing, dict) or routing.get("executed") is not True:
            self.fail("ROUTING_EVIDENCE_MISSING", path=path)
            return
        passes = routing.get("route_line_passes")
        if not isinstance(passes, list) or not passes:
            self.fail("ROUTELINE_NOT_EXECUTED", path=path)
        else:
            for index, item in enumerate(passes, start=1):
                if (
                    not isinstance(item, dict)
                    or item.get("pass") != index
                    or not isinstance(item.get("reason"), str)
                    or not item["reason"].strip()
                ):
                    self.fail("ROUTELINE_PASS_INVALID", path=path, index=index)
        if routing.get("final_interface_feedback_adjustment") is not True:
            self.fail("FINAL_INTERFACE_FEEDBACK_ADJUSTMENT_MISSING", path=path)
        explicit_routes = routing.get("explicit_routes")
        if not isinstance(explicit_routes, list):
            self.fail("EXPLICIT_ROUTE_EVIDENCE_INVALID", path=path)
            explicit_routes = []
        for index, item in enumerate(explicit_routes):
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("connection"), str)
                or not item["connection"].strip()
                or not isinstance(item.get("remaining_violation"), str)
                or not item["remaining_violation"].strip()
            ):
                self.fail("EXPLICIT_ROUTE_JUSTIFICATION_MISSING", path=path, index=index)
        if explicit_routes and routing.get("route_line_after_explicit_routes") is not False:
            self.fail("ROUTELINE_AFTER_EXPLICIT_ROUTE", path=path)

    def run(self) -> dict[str, Any]:
        if not self.model_file.is_file():
            self.fail("MODEL_FILE_MISSING", path=str(self.model_file))
            return self.report()
        hash_before = sha256_file(self.model_file)
        self.model_sha256 = hash_before

        e = self.evidence
        if not isinstance(e, dict) or e.get("schema") != SCHEMA:
            self.fail("EVIDENCE_SCHEMA_INVALID")
            return self.finish(hash_before)
        task_type = e.get("task_type")
        if task_type not in TASK_TYPES:
            self.fail("TASK_TYPE_INVALID", value=task_type)
        try:
            evidence_model = Path(str(e.get("model_file", ""))).resolve()
        except Exception:
            evidence_model = Path()
        if evidence_model != self.model_file:
            self.fail("MODEL_PATH_MISMATCH", evidence=str(evidence_model))
        if str(e.get("model_sha256", "")).upper() != hash_before:
            self.fail("MODEL_HASH_MISMATCH", actual=hash_before)

        save_reload = self.section("SAVE_RELOAD", e.get("save_reload"))
        self.require_true(save_reload, "executed", "SAVE_RELOAD_NOT_EXECUTED")
        self.require_true(save_reload, "passed", "SAVE_RELOAD_FAILED")
        self.require_true(save_reload, "force_reload", "FORCE_RELOAD_MISSING")
        try:
            reload_path = Path(str(save_reload.get("reload_path", ""))).resolve()
        except Exception:
            reload_path = Path()
        if reload_path != self.model_file:
            self.fail("RELOAD_PATH_MISMATCH", reload_path=str(reload_path))

        check_model = self.section("CHECK_MODEL", e.get("check_model"))
        self.require_true(check_model, "executed", "CHECK_MODEL_NOT_EXECUTED")
        self.require_true(check_model, "passed", "CHECK_MODEL_FAILED")
        delivery = self.section("DELIVERY", e.get("delivery"))
        clean_warnings_required = delivery.get("clean_warnings_required")
        if not isinstance(clean_warnings_required, bool):
            self.fail("WARNING_POLICY_MISSING")
        warnings = self.section("WARNINGS", e.get("warnings"))
        self.require_true(warnings, "executed", "WARNING_CAPTURE_NOT_EXECUTED")
        warning_count = warnings.get("count")
        warning_messages = warnings.get("messages")
        if (
            not isinstance(warning_count, int)
            or isinstance(warning_count, bool)
            or warning_count < 0
            or not isinstance(warning_messages, list)
            or len(warning_messages) != warning_count
            or not all(isinstance(message, str) and message.strip() for message in warning_messages)
        ):
            self.fail("WARNING_EVIDENCE_INVALID")
        elif clean_warnings_required and warning_count:
            self.fail("WARNINGS_PRESENT", count=warning_count, messages=warning_messages)

        hierarchy = self.section("HIERARCHY", e.get("hierarchy"))
        self.require_true(hierarchy, "executed", "HIERARCHY_NOT_EXECUTED")
        self.require_true(hierarchy, "complete", "HIERARCHY_INCOMPLETE")
        if hierarchy.get("source") != "force_reloaded_api":
            self.fail("HIERARCHY_SOURCE_INVALID")
        expected_levels = self.path_list("HIERARCHY_LEVELS", hierarchy.get("levels"), nonempty=True)
        expected_charts = self.path_list("HIERARCHY_CHARTS", hierarchy.get("charts"))
        root = hierarchy.get("root")
        if not isinstance(root, str) or not expected_levels or root != expected_levels[0]:
            self.fail("HIERARCHY_ROOT_INVALID", root=root)
        elif (
            any(path != root and not path.startswith(root + ".") for path in expected_levels)
            or any(not path.startswith(root + ".") for path in expected_charts)
            or any(
                left.count(".") > right.count(".")
                for left, right in zip(expected_levels, expected_levels[1:])
            )
        ):
            self.fail("HIERARCHY_ORDER_OR_PARENT_INVALID")

        affected_levels = self.path_list("AFFECTED_LEVELS", e.get("affected_levels"))
        affected_charts = self.path_list("AFFECTED_CHARTS", e.get("affected_charts"))
        if not set(affected_levels).issubset(expected_levels) or not set(affected_charts).issubset(expected_charts):
            self.fail("AFFECTED_INVENTORY_OUTSIDE_HIERARCHY")

        pre = self.section("PRE_LAYOUT", e.get("pre_layout"))
        change_scope = self.section("CHANGE_SCOPE", e.get("change_scope"))
        topology_or_layout_changed = change_scope.get("topology_or_layout_changed")
        if not isinstance(topology_or_layout_changed, bool):
            self.fail("CHANGE_SCOPE_MISSING")
            topology_or_layout_changed = False
        if task_type == "build" and topology_or_layout_changed is not True:
            self.fail("BUILD_CHANGE_SCOPE_INVALID")
        if task_type == "audit" and topology_or_layout_changed is not False:
            self.fail("AUDIT_CHANGE_SCOPE_INVALID")
        pre_required = task_type == "build" or (task_type == "edit" and topology_or_layout_changed)
        expected_chart_decompositions: dict[str, str] = {}
        pre_levels = self.records("PRE_LEVELS", pre.get("levels"), "static_plan")
        pre_charts = self.records("PRE_CHARTS", pre.get("charts"), "static_plan")
        if pre_required:
            if pre.get("status") != "required":
                self.fail("PRE_LAYOUT_STATUS_INVALID", expected="required")
            if not affected_levels and not affected_charts:
                self.fail("PRE_LAYOUT_AFFECTED_INVENTORY_MISSING")
            if task_type == "build":
                self.require_exact_paths("BUILD_AFFECTED_LEVEL", expected_levels, affected_levels)
                self.require_exact_paths("BUILD_AFFECTED_CHART", expected_charts, affected_charts)
            self.require_exact_paths(
                "pre_level",
                affected_levels,
                [item["path"] for item in pre_levels],
            )
            self.require_exact_paths(
                "pre_chart",
                affected_charts,
                [item["path"] for item in pre_charts],
            )
            for item in pre_levels:
                self.audit_manifest("pre", item["path"], item.get("manifest"))
            for item in pre_charts:
                self.audit_chart_layout("pre", item["path"], item.get("layout"))
            input_record = e.get("layout_input")
            if not isinstance(input_record, dict) or input_record.get("status") != "required":
                self.fail("LAYOUT_INPUT_MISSING")
            else:
                input_data = input_record.get("data")
                try:
                    input_report = audit_layout_input(input_data)
                except Exception as exc:
                    input_report = {"passed": False, "canonical_sha256": "", "issues": [{"detail": str(exc)}]}
                if not input_report.get("passed"):
                    codes = {item.get("code") for item in input_report.get("issues", []) if isinstance(item, dict)}
                    if "GEOMETRY_PRESENT" in codes:
                        self.fail("GEOMETRY_PRESENT", issues=input_report.get("issues", []))
                    if "TOPOLOGY_INVALID" in codes:
                        self.fail("TOPOLOGY_INVALID", issues=input_report.get("issues", []))
                    if codes - {"GEOMETRY_PRESENT", "TOPOLOGY_INVALID"} or not codes:
                        self.fail("LAYOUT_INPUT_SCHEMA_INVALID", issues=input_report.get("issues", []))
                input_hash = input_report.get("canonical_sha256", "")
                if input_record.get("canonical_sha256") != input_hash:
                    self.fail("LAYOUT_INPUT_HASH_MISMATCH")
                if input_report.get("passed"):
                    expected_chart_decompositions = {
                        item.get("path"): item.get("decomposition")
                        for item in input_data.get("charts", [])
                        if isinstance(item, dict)
                    }
                    self.check_plan_input_binding(input_data, input_hash, pre_levels, pre_charts)
        elif (
            pre.get("status") != "not_required"
            or affected_levels
            or affected_charts
            or pre_levels
            or pre_charts
        ):
            self.fail("PRE_LAYOUT_NOT_REQUIRED_EVIDENCE_INVALID")
        elif e.get("layout_input") != {"status": "not_required"}:
            self.fail("LAYOUT_INPUT_NOT_REQUIRED_EVIDENCE_INVALID")

        level_records = self.records("SAVED_LEVELS", e.get("levels"), "force_reloaded_api")
        chart_records = self.records("SAVED_CHARTS", e.get("charts"), "force_reloaded_api")
        self.require_exact_paths(
            "saved_level",
            expected_levels,
            [item["path"] for item in level_records],
        )
        self.require_exact_paths(
            "saved_chart",
            expected_charts,
            [item["path"] for item in chart_records],
        )
        for item in level_records:
            path = item["path"]
            if str(item.get("model_sha256", "")).upper() != hash_before:
                self.fail("LEVEL_EVIDENCE_STALE", path=path)
            if pre_required and path in affected_levels:
                self.check_routing(path, item)
            result = self.audit_manifest("saved", path, item.get("manifest"))
            self.level_results.append(
                {
                    "path": path,
                    "passed": bool(result and result.get("passed")),
                    "issue_count": None if result is None else result.get("issue_count"),
                }
            )
        for item in chart_records:
            path = item["path"]
            if str(item.get("model_sha256", "")).upper() != hash_before:
                self.fail("CHART_EVIDENCE_STALE", path=path)
            saved_layout = item.get("layout")
            expected_decomposition = expected_chart_decompositions.get(path)
            if (
                expected_decomposition is not None
                and (
                    not isinstance(saved_layout, dict)
                    or saved_layout.get("chart_decomposition") != expected_decomposition
                )
            ):
                self.fail("CHART_DECOMPOSITION_MISMATCH", path=path)
            self.check_chart_ports(path, item)
            self.check_chart_element_allowlist(path, item)
            result = self.audit_chart_layout("saved", path, saved_layout)
            self.chart_results.append(
                {
                    "path": path,
                    "passed": bool(result and result.get("passed")),
                    "issue_count": None if result is None else result.get("issue_count"),
                }
            )

        return self.finish(hash_before)

    def finish(self, hash_before: str) -> dict[str, Any]:
        hash_after = sha256_file(self.model_file) if self.model_file.is_file() else ""
        if hash_after != hash_before:
            self.fail("MODEL_CHANGED_DURING_AUDIT", before=hash_before, after=hash_after)
        return self.report()

    def report(self) -> dict[str, Any]:
        return {
            "model_file": str(self.model_file),
            "model_sha256": self.model_sha256,
            "audit_script_sha256": sha256_file(Path(__file__).resolve()),
            "levels": self.level_results,
            "charts": self.chart_results,
            "failure_count": len(self.failures),
            "failure_codes": [item["code"] for item in self.failures],
            "failures": self.failures,
            "audit_passed": not self.failures,
        }


def audit_evidence(model_file: Path, evidence: dict[str, Any]) -> dict[str, Any]:
    return EvidenceAudit(model_file, evidence).run()
