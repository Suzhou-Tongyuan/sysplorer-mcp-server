"""Utilities for discovering and managing simulation result variables."""
from __future__ import annotations

from typing import Any, Dict, List, Tuple


def truncate_result_variable_list(data: Any, cap: int) -> Tuple[Any, int, bool]:
    """Truncate a result variable list to at most *cap* entries.

    Returns:
        (trimmed, total, was_truncated)
    """
    if not isinstance(data, list):
        return data, 0, False
    total = len(data)
    if total <= cap:
        return data, total, False
    return data[:cap], total, True


def discover_result_variables_via_model(
    drv: Any,
    model_name: str,
    max_depth: int = 8,
    max_instances: int = 120,
    max_probes: int = 400,
) -> Dict[str, Any]:
    """Walk the model component tree and confirm result variables via GetResultVariableInfo.

    Strategy:
      1. BFS-traverse ``GetComponents`` up to *max_depth* levels / *max_instances* instances.
      2. For each instance path, call ``GetComponentPorts`` to obtain leaf variable names.
      3. Build candidate strings ``<instance_path>.<port_name>``.
      4. Probe each candidate with ``GetResultVariableInfo(name, "Type")`` (up to *max_probes*).
      5. Return confirmed variables with sample type info.

    Returns a plain dict with keys:
      ok, variables, variable_count, probes_attempted, instances_scanned,
      candidates_built, sample_details, error (only on failure)
    """
    probes_attempted = 0
    instances_scanned = 0
    candidates_built = 0
    confirmed: List[str] = []
    sample_details: List[Dict[str, str]] = []

    try:
        # ── BFS component traversal ──────────────────────────────────────────
        # queue items: (full_path_prefix, depth)
        # full_path_prefix="" means top-level variables of model_name itself
        queue: List[Tuple[str, int]] = [("", 0)]
        visited_prefixes: set = set()

        while queue and instances_scanned < max_instances and probes_attempted < max_probes:
            prefix, depth = queue.pop(0)

            # Determine what to pass to GetComponents
            comp_arg = prefix if prefix else ""
            res = drv.get_components(model_name, comp_arg)
            if not res.ok:
                continue

            raw = res.data
            component_names: List[str] = []
            if isinstance(raw, list):
                for item in raw:
                    if isinstance(item, str):
                        component_names.append(item)
                    elif isinstance(item, (list, tuple)) and len(item) >= 1:
                        # Some APIs return [name, type, ...] tuples
                        component_names.append(str(item[0]))
                    elif isinstance(item, dict):
                        n = item.get("name") or item.get("instanceName") or ""
                        if n:
                            component_names.append(str(n))
            elif isinstance(raw, str) and raw.strip():
                component_names = [s.strip() for s in raw.split(",") if s.strip()]

            for comp_name in component_names:
                if instances_scanned >= max_instances:
                    break
                full_path = f"{prefix}.{comp_name}" if prefix else comp_name
                if full_path in visited_prefixes:
                    continue
                visited_prefixes.add(full_path)
                instances_scanned += 1

                # Get variables/ports of this component
                port_res = drv.get_component_ports(model_name, full_path, 0)
                port_names: List[str] = []
                if port_res.ok and port_res.data is not None:
                    praw = port_res.data
                    if isinstance(praw, list):
                        for item in praw:
                            if isinstance(item, str):
                                port_names.append(item)
                            elif isinstance(item, (list, tuple)) and len(item) >= 1:
                                port_names.append(str(item[0]))
                            elif isinstance(item, dict):
                                n = item.get("name") or item.get("portName") or ""
                                if n:
                                    port_names.append(str(n))
                    elif isinstance(praw, str) and praw.strip():
                        port_names = [s.strip() for s in praw.split(",") if s.strip()]

                # Build candidate variable names
                for port in port_names:
                    candidate = f"{full_path}.{port}"
                    candidates_built += 1
                    if probes_attempted >= max_probes:
                        break
                    probes_attempted += 1
                    info_res = drv.get_result_variable_info(candidate, "Type")
                    if info_res.ok and info_res.data is not None:
                        type_str = str(info_res.data).strip()
                        if type_str and type_str.lower() not in {"", "none", "null"}:
                            confirmed.append(candidate)
                            if len(sample_details) < 20:
                                sample_details.append({"name": candidate, "type": type_str})

                # Enqueue children if not at max depth
                if depth + 1 < max_depth and instances_scanned < max_instances:
                    next_key = (full_path, depth + 1)
                    if full_path not in {p for p, _ in queue}:
                        queue.append(next_key)

        # Also probe top-level variables of the model itself (time, der(...), etc.)
        top_ports_res = drv.get_component_ports(model_name, "", 0)
        if top_ports_res.ok and top_ports_res.data is not None:
            traw = top_ports_res.data
            top_ports: List[str] = []
            if isinstance(traw, list):
                for item in traw:
                    if isinstance(item, str):
                        top_ports.append(item)
                    elif isinstance(item, dict):
                        n = item.get("name") or item.get("portName") or ""
                        if n:
                            top_ports.append(str(n))
            elif isinstance(traw, str) and traw.strip():
                top_ports = [s.strip() for s in traw.split(",") if s.strip()]

            for port in top_ports:
                if probes_attempted >= max_probes:
                    break
                candidates_built += 1
                probes_attempted += 1
                info_res = drv.get_result_variable_info(port, "Type")
                if info_res.ok and info_res.data is not None:
                    type_str = str(info_res.data).strip()
                    if type_str and type_str.lower() not in {"", "none", "null"}:
                        confirmed.append(port)
                        if len(sample_details) < 20:
                            sample_details.append({"name": port, "type": type_str})

        return {
            "ok": True,
            "variables": confirmed,
            "variable_count": len(confirmed),
            "probes_attempted": probes_attempted,
            "instances_scanned": instances_scanned,
            "candidates_built": candidates_built,
            "sample_details": sample_details,
        }

    except Exception as exc:
        return {
            "ok": False,
            "variables": confirmed,
            "variable_count": len(confirmed),
            "probes_attempted": probes_attempted,
            "instances_scanned": instances_scanned,
            "candidates_built": candidates_built,
            "sample_details": sample_details,
            "error": str(exc),
        }
