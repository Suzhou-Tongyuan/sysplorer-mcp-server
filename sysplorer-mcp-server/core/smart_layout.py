"""Smart Layout Engine — domain-aware, pure-Python Modelica diagram layout."""
from __future__ import annotations

import heapq
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from constants import (
    _SL_PORT_SIDE_MAP, _SL_DOMAIN_COLORS, _SL_PORT_DOMAIN,
    _SL_H_SPACING, _SL_V_SPACING, _SL_DEFAULT_HW, _SL_DEFAULT_HH,
    _SL_MIN_GAP, _SL_PRIMARY_PORTS, _SL_ROTATION_MAP,
    _SMART_LAYOUT_TEMP_DIR,
    _SL_CIRCUIT_MODE_THRESHOLD,
    _SL_CIRC_H_STEP, _SL_CIRC_V_STEP,
    _SL_CIRC_RAIL_Y, _SL_CIRC_GND_Y, _SL_CIRC_GND_SYM_Y,
    _SL_CIRC_SIG_Y, _SL_CIRC_COMP_HW, _SL_CIRC_COMP_HH,
)

def _fmt_layout_num(value: float) -> str:
    try:
        return str(int(round(float(value))))
    except Exception:
        return "0"


def _sl_port_short_name(port_id: str, node_id: str) -> str:
    """Return the short port name by stripping the 'nodeId.' prefix."""
    if port_id.startswith(node_id + "."):
        return port_id[len(node_id) + 1:]
    return port_id.rsplit(".", 1)[-1] if "." in port_id else port_id


def _sl_port_anchor(
    cx: float, cy: float, hw: float, hh: float, side: str
) -> Tuple[float, float]:
    """Return the boundary connection point for a port on a given side."""
    if side == "WEST":
        return (cx - hw, cy)
    if side == "EAST":
        return (cx + hw, cy)
    if side == "SOUTH":
        return (cx, cy - hh)
    if side == "NORTH":
        return (cx, cy + hh)
    return (cx + hw, cy)  # fallback -> EAST


def _sl_median_sorted_ints(values: List[int]) -> float:
    """Median of integer positions; empty → NaN for stable-sort fallback."""
    if not values:
        return float("nan")
    s = sorted(values)
    n = len(s)
    m = n // 2
    if n % 2 == 1:
        return float(s[m])
    return (s[m - 1] + s[m]) / 2.0


def _sl_median_sorted_floats(values: List[float]) -> float:
    if not values:
        return float("nan")
    s = sorted(values)
    n = len(s)
    m = n // 2
    if n % 2 == 1:
        return float(s[m])
    return (s[m - 1] + s[m]) / 2.0


def _sl_reorder_layers_minimize_crossings(
    layer_groups: Dict[int, List[str]],
    layer_sorted_keys: List[int],
    adj_fwd: Dict[str, List[str]],
    adj_bwd: Dict[str, List[str]],
    iterations: int = 5,
) -> None:
    """Reorder nodes within each layer to reduce edge crossings (median heuristic).

    Classic Sugiyama-style alternating sweeps (left→right by predecessors,
    right→left by successors). Long-range edges fall back to any neighbor
    in earlier / later layers with a coarse layer-weighted rank.
    """
    if len(layer_sorted_keys) <= 1:
        return

    layer_weight = 10000.0

    for _ in range(max(1, iterations)):
        # Left → right: align with median position of predecessors in previous layer
        for ki in range(1, len(layer_sorted_keys)):
            lyr = layer_sorted_keys[ki]
            prev_lyr = layer_sorted_keys[ki - 1]
            prev_pos = {n: i for i, n in enumerate(layer_groups[prev_lyr])}
            cur = layer_groups[lyr]

            scores: List[Tuple[float, str]] = []
            for nid in cur:
                neigh_idx = [prev_pos[p] for p in adj_bwd.get(nid, []) if p in prev_pos]
                if neigh_idx:
                    med = _sl_median_sorted_ints(neigh_idx)
                else:
                    alt: List[float] = []
                    for pj in range(ki):
                        pl = layer_sorted_keys[pj]
                        pmap = {n: float(i) + pj * layer_weight for i, n in enumerate(layer_groups[pl])}
                        for p in adj_bwd.get(nid, []):
                            if p in pmap:
                                alt.append(pmap[p])
                    med = _sl_median_sorted_floats(alt) if alt else float("nan")
                if med != med:  # NaN
                    med = float("inf")
                scores.append((med, nid))
            scores.sort(key=lambda t: (t[0], t[1]))
            layer_groups[lyr] = [t[1] for t in scores]

        # Right → left: align with successors in next layer
        for ki in range(len(layer_sorted_keys) - 2, -1, -1):
            lyr = layer_sorted_keys[ki]
            next_lyr = layer_sorted_keys[ki + 1]
            next_pos = {n: i for i, n in enumerate(layer_groups[next_lyr])}
            cur = layer_groups[lyr]

            scores = []
            for nid in cur:
                neigh_idx = [next_pos[s] for s in adj_fwd.get(nid, []) if s in next_pos]
                if neigh_idx:
                    med = _sl_median_sorted_ints(neigh_idx)
                else:
                    alt = []
                    for nj in range(ki + 1, len(layer_sorted_keys)):
                        nl = layer_sorted_keys[nj]
                        nmap = {n: float(i) + nj * layer_weight for i, n in enumerate(layer_groups[nl])}
                        for s in adj_fwd.get(nid, []):
                            if s in nmap:
                                alt.append(nmap[s])
                    med = _sl_median_sorted_floats(alt) if alt else float("nan")
                if med != med:
                    med = float("inf")
                scores.append((med, nid))
            scores.sort(key=lambda t: (t[0], t[1]))
            layer_groups[lyr] = [t[1] for t in scores]


# ═══════════════════════════════════════════════════════════════════════════════
# Circuit-schematic layout engine (electrical domain)
# ═══════════════════════════════════════════════════════════════════════════════

def _is_circuit_mode(children: List[Dict[str, Any]]) -> bool:
    """Return True when the majority of nodes are single-phase electrical devices."""
    if not children:
        return False
    elec = 0
    coupled_or_mechanical = 0
    for node in children:
        nid = str(node.get("id", ""))
        pnames = {
            _sl_port_short_name(str(p.get("id", "")), nid)
            for p in (node.get("ports") or [])
            if isinstance(p, dict)
        }
        has_elec  = bool({"p", "n", "pin_p", "pin_n"} & pnames)
        has_mech  = bool({"flange_a", "flange_b", "frame_a", "frame_b"} & pnames)
        has_fluid = bool({"port_a", "port_b", "inlet", "outlet"} & pnames)
        if has_elec and not has_mech and not has_fluid:
            elec += 1
        elif has_mech:
            coupled_or_mechanical += 1
    if coupled_or_mechanical:
        return False
    return (elec / max(len(children), 1)) >= _SL_CIRCUIT_MODE_THRESHOLD


def _circuit_route_wire(
    sp: Tuple[float, float],
    tp: Tuple[float, float],
    s_pname: str,
    t_pname: str,
    s_nid: str,
    t_nid: str,
    ground_nodes: set,
    rail_y: float,
) -> List[Tuple[float, float]]:
    """Compute orthogonal bend points for one circuit wire.

    Rules (all orthogonal, at most one bend):
    - Same x or same y            → straight (no bend).
    - Signal port (y/u/control)   → rise at source-x first, then horizontal.
    - Target is ground symbol     → drop at source-x to target-y, then horizontal.
    - Source is on main rail AND target is below  → horizontal first, drop at target-x
      (T-junction: rail node to shunt top pin).
    - Any other downward wire     → drop at source-x first, then horizontal.
    - Upward wire                 → rise at source-x first, then horizontal.
    """
    sx, sy = sp
    tx, ty = tp

    if abs(sx - tx) < 0.5 and abs(sy - ty) < 0.5:
        return []
    if abs(sx - tx) < 0.5 or abs(sy - ty) < 0.5:
        return []  # already straight

    is_signal  = s_pname in ("y", "u", "u1", "u2") or t_pname in ("control", "u", "u1", "u2")
    to_ground  = t_nid in ground_nodes
    from_ground = s_nid in ground_nodes

    if is_signal:
        return [(sx, ty)]          # rise at source-x, then horizontal

    if to_ground:
        return [(sx, ty)]          # drop at source-x to ground-bus y, then horizontal

    if from_ground:
        return [(tx, sy)]          # leave ground horizontally, then rise

    if ty < sy:                    # downward
        if abs(sy - rail_y) < 1.0:
            return [(tx, sy)]      # on rail → horizontal first, drop at target-x
        return [(sx, ty)]          # off rail → drop first, then horizontal

    return [(sx, ty)]              # upward → rise first, then horizontal


def _circuit_layout_engine(
    graph: Dict[str, Any],
    children: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    node_by_id: Dict[str, Dict[str, Any]],
    port_to_node: Dict[str, str],
) -> Dict[str, Any]:
    """Electrical circuit schematic layout.

    Conventions
    -----------
    Top rail (RAIL_Y=+30): sources + series devices (horizontal, left→right).
    Ground bus (GND_Y=−20): all n-pins terminate here.
    Ground symbol: centred at GND_SYM_Y=−30 below the bus.
    Shunt devices (C, R, diode …): vertical, body centred at y=0.
      - n→ground (C, R): rotation=270 → p=top (+y), n=bottom (−y).
      - p→ground (freewheeling diode): rotation=90 → p=bottom (−y), n=top (+y).
    Sources: vertical, rotation=270, centred at y=0, placed to the left.
    Signal blocks (PWM …): horizontal, centred at SIG_Y=−20 below switch.
    """
    import copy
    from collections import defaultdict

    RAIL_Y    = _SL_CIRC_RAIL_Y      # +30
    GND_Y     = _SL_CIRC_GND_Y       # −20
    GND_SYM_Y = _SL_CIRC_GND_SYM_Y  # −30
    SIG_Y     = _SL_CIRC_SIG_Y       # −20
    HW        = _SL_CIRC_COMP_HW     # 10
    HH        = _SL_CIRC_COMP_HH     # 10
    H_STEP    = _SL_CIRC_H_STEP      # 40

    result = copy.deepcopy(graph)

    # ── helpers ───────────────────────────────────────────────────────────────
    def get_pnames(node: Dict) -> set:
        nid = str(node.get("id", ""))
        return {
            _sl_port_short_name(str(p.get("id", "")), nid)
            for p in (node.get("ports") or [])
            if isinstance(p, dict)
        }

    # ── 1. Classify nodes by port structure ───────────────────────────────────
    ground_nodes: set = set()
    signal_nodes: set = set()
    switch_nodes: set = set()    # has 'control' port + p/n
    two_terminal: set = set()    # has p and n (but no control)
    other_nodes:  set = set()

    for node in children:
        nid  = str(node.get("id", ""))
        pn   = get_pnames(node)
        elec = {"p", "n"} & pn or {"pin_p", "pin_n"} & pn

        if pn <= {"p"}:                            # only p (Ground)
            ground_nodes.add(nid)
        elif "y" in pn and not elec:              # signal source/block
            signal_nodes.add(nid)
        elif "control" in pn and elec:            # controlled switch
            switch_nodes.add(nid)
            two_terminal.add(nid)
        elif elec:                                # generic two-terminal
            two_terminal.add(nid)
        else:
            other_nodes.add(nid)

    # ── 2. Pin-level adjacency ─────────────────────────────────────────────────
    pin_adj: Dict = defaultdict(list)
    for edge in edges:
        srcs = list(edge.get("sources") or [])
        tgts = list(edge.get("targets") or [])
        for s_pid in srcs:
            s_nid = port_to_node.get(str(s_pid), str(s_pid).split(".")[0])
            s_pn  = _sl_port_short_name(str(s_pid), s_nid)
            for t_pid in tgts:
                t_nid = port_to_node.get(str(t_pid), str(t_pid).split(".")[0])
                t_pn  = _sl_port_short_name(str(t_pid), t_nid)
                if s_nid != t_nid:
                    pin_adj[(s_nid, s_pn)].append((t_nid, t_pn))
                    pin_adj[(t_nid, t_pn)].append((s_nid, s_pn))

    # ── 3. Ground-connected detection ─────────────────────────────────────────
    gnd_via_p: set = set()   # this node's p pin touches ground
    gnd_via_n: set = set()   # this node's n pin touches ground

    for nid in two_terminal:
        for gnd, _ in pin_adj.get((nid, "p"), []):
            if gnd in ground_nodes:
                gnd_via_p.add(nid)
        for gnd, _ in pin_adj.get((nid, "n"), []):
            if gnd in ground_nodes:
                gnd_via_n.add(nid)

    # ── 4. Classify: source / series / shunt ──────────────────────────────────
    source_nodes: set = set()
    shunt_nodes:  set = set()
    series_nodes: set = set()

    # Source: n→ground AND p connects to a switch's p
    for nid in two_terminal - switch_nodes:
        if nid not in gnd_via_n:
            continue
        for conn, cpn in pin_adj.get((nid, "p"), []):
            if conn in switch_nodes and cpn == "p":
                source_nodes.add(nid)
                break

    if not source_nodes:                          # fallback
        source_nodes = gnd_via_n - switch_nodes

    for nid in two_terminal - switch_nodes:
        if nid in source_nodes:
            continue
        if nid in gnd_via_p or nid in gnd_via_n:
            shunt_nodes.add(nid)
        else:
            series_nodes.add(nid)

    series_nodes |= switch_nodes

    # ── 5. Build series chain ─────────────────────────────────────────────────
    series_chain: List[str] = []
    chain_start = None
    for src in sorted(source_nodes):
        for conn, cpn in pin_adj.get((src, "p"), []):
            if conn in series_nodes:
                chain_start = conn
                break
        if chain_start:
            break

    if chain_start:
        visited: set = set()
        cur = chain_start
        while cur and cur not in visited:
            series_chain.append(cur)
            visited.add(cur)
            nxt = None
            for conn, cpn in pin_adj.get((cur, "n"), []):
                if conn in series_nodes and conn not in visited and cpn == "p":
                    nxt = conn
                    break
            cur = nxt

    for nid in series_nodes:
        if nid not in series_chain:
            series_chain.append(nid)

    # ── 6. Assign x centres ───────────────────────────────────────────────────
    n_series = len(series_chain)
    src_cx   = -(n_series * H_STEP / 2 + H_STEP)     # source sits left of chain

    series_cx: Dict[str, float] = {
        nid: src_cx + H_STEP + i * H_STEP
        for i, nid in enumerate(series_chain)
    }

    # ── 7. Map shunts to junction x ───────────────────────────────────────────
    shunt_jx: Dict[str, float] = {}
    for sh in shunt_nodes | (gnd_via_p - source_nodes):
        rail_pin = "n" if sh in gnd_via_p else "p"
        for conn, cpn in pin_adj.get((sh, rail_pin), []):
            if conn in series_nodes and conn in series_cx:
                jx = series_cx[conn] + (HW if cpn == "n" else -HW)
                shunt_jx[sh] = jx
                break

    # ── 8. Final (cx, cy, rotation) assignments ───────────────────────────────
    node_pos: Dict[str, Tuple[float, float, int]] = {}

    for i, src in enumerate(sorted(source_nodes)):
        node_pos[src] = (src_cx - i * H_STEP, 0.0, 270)

    for nid in series_chain:
        node_pos[nid] = (series_cx[nid], RAIL_Y, 0)

    junc_groups: Dict[float, List[str]] = defaultdict(list)
    for sh, jx in shunt_jx.items():
        junc_groups[jx].append(sh)

    for jx, sh_list in junc_groups.items():
        # First shunt AT the junction; additional shunts step right by H_STEP
        for i, sh in enumerate(sh_list):
            rot = 90 if sh in gnd_via_p else 270
            node_pos[sh] = (jx + i * H_STEP, 0.0, rot)

    for sh in shunt_nodes:
        if sh not in node_pos:
            node_pos[sh] = (0.0, 0.0, 270)

    all_xs  = [cx for cx, _, _ in node_pos.values()] or [0.0]
    gnd_cx  = (min(all_xs) + max(all_xs)) / 2.0
    for i, gnd in enumerate(sorted(ground_nodes)):
        # rotation=270 → p pin at NORTH (top), y = GND_SYM_Y + HH = −20
        node_pos[gnd] = (gnd_cx, GND_SYM_Y, 270)

    for sig in signal_nodes:
        sw_ref = None
        for conn, cpn in pin_adj.get((sig, "y"), []):
            if conn in switch_nodes:
                sw_ref = conn
                break
        ref_cx = series_cx.get(sw_ref, src_cx)
        node_pos[sig] = (ref_cx, SIG_Y, 0)

    max_x = max(cx for cx, _, _ in node_pos.values()) if node_pos else 0.0
    for i, nid in enumerate(sorted(other_nodes)):
        if nid not in node_pos:
            node_pos[nid] = (max_x + (i + 1) * H_STEP, RAIL_Y, 0)

    # ── 9. Write positions to graph ───────────────────────────────────────────
    for node in (result.get("children") or []):
        nid = str(node.get("id", ""))
        if nid not in node_pos:
            continue
        cx, cy, rot = node_pos[nid]
        nw = float(node.get("width",  HW * 2))
        nh = float(node.get("height", HH * 2))
        node["x"]        = cx - nw / 2
        node["y"]        = cy - nh / 2
        node["width"]    = nw
        node["height"]   = nh
        node["rotation"] = rot

    # ── 10. Pin-position helper ───────────────────────────────────────────────
    def pin_xy(nid: str, pname: str) -> Tuple[float, float]:
        if nid not in node_pos:
            return (0.0, 0.0)
        cx, cy, rot = node_pos[nid]
        hw = float(node_by_id.get(nid, {}).get("width",  HW * 2)) / 2
        hh = float(node_by_id.get(nid, {}).get("height", HH * 2)) / 2
        # rotation=270 (CW): local +x → global +y  →  p=NORTH, n=SOUTH
        # rotation=90  (CCW): local +x → global −y  →  p=SOUTH, n=NORTH
        # rotation=0 (default): p=WEST, n=EAST, control=SOUTH, y=EAST
        if rot == 270:
            if pname in ("p", "pin_p"):   return (cx, cy + hh)
            if pname in ("n", "pin_n"):   return (cx, cy - hh)
        elif rot == 90:
            if pname in ("p", "pin_p"):   return (cx, cy - hh)
            if pname in ("n", "pin_n"):   return (cx, cy + hh)
        if pname in ("p", "pin_p"):       return (cx - hw, cy)
        if pname in ("n", "pin_n"):       return (cx + hw, cy)
        if pname == "control":            return (cx, cy - hh)
        if pname in ("y", "y1", "y2"):    return (cx + hw, cy)
        if pname in ("u", "u1", "u2"):    return (cx - hw, cy)
        return (cx + hw, cy)

    # ── 11. Route edges ───────────────────────────────────────────────────────
    elec_color = (0,   0, 255)
    bool_color = (255, 0, 255)

    for edge in (result.get("edges") or []):
        srcs = list(edge.get("sources") or [])
        tgts = list(edge.get("targets") or [])
        if not srcs or not tgts:
            continue
        s_pid = str(srcs[0]);  t_pid = str(tgts[0])
        s_nid = port_to_node.get(s_pid, s_pid.split(".")[0])
        t_nid = port_to_node.get(t_pid, t_pid.split(".")[0])
        s_pn  = _sl_port_short_name(s_pid, s_nid)
        t_pn  = _sl_port_short_name(t_pid, t_nid)
        if s_nid not in node_pos and t_nid not in node_pos:
            continue
        sp    = pin_xy(s_nid, s_pn)
        tp    = pin_xy(t_nid, t_pn)
        color = bool_color if (s_pn in ("y", "control") or t_pn in ("y", "control")) else elec_color
        bends = _circuit_route_wire(sp, tp, s_pn, t_pn, s_nid, t_nid, ground_nodes, RAIL_Y)
        edge["sections"] = [{
            "id":         f"sec_{edge.get('id', 'e')}",
            "startPoint": {"x": sp[0], "y": sp[1]},
            "endPoint":   {"x": tp[0], "y": tp[1]},
            "bendPoints": [{"x": b[0], "y": b[1]} for b in bends],
        }]
        edge["_color"] = color

    result["_modelica_coords"] = True
    return result


def _layout_node_id_from_port(port_id: str, port_to_node: Dict[str, str]) -> str:
    pid = str(port_id)
    return port_to_node.get(pid, pid.split(".")[0])


def _classify_layout_satellites(
    children: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    port_to_node: Dict[str, str],
    node_by_id: Dict[str, Dict[str, Any]],
) -> set:
    """One-port nodes are satellites only when attached to a multi-port main node.

    A single port on the layout graph (often only the connectors that appear in
    ``connect()``) does not by itself mean a satellite. Two one-port components
    wired together are the main topology, not a pair of hanging satellites.
    """
    one_port: set = set()
    for node in children:
        nid = str(node.get("id", ""))
        ports = [pp for pp in (node.get("ports") or []) if isinstance(pp, dict)]
        if nid and len(ports) == 1:
            one_port.add(nid)
    if not one_port:
        return set()

    attached_to_main: set = set()
    for edge in edges:
        srcs_e = list(edge.get("sources") or [])
        tgts_e = list(edge.get("targets") or [])
        for s_pid_e in srcs_e:
            s_nid_e = _layout_node_id_from_port(s_pid_e, port_to_node)
            for t_pid_e in tgts_e:
                t_nid_e = _layout_node_id_from_port(t_pid_e, port_to_node)
                if s_nid_e == t_nid_e:
                    continue
                if s_nid_e in one_port and t_nid_e not in one_port and t_nid_e in node_by_id:
                    attached_to_main.add(s_nid_e)
                if t_nid_e in one_port and s_nid_e not in one_port and s_nid_e in node_by_id:
                    attached_to_main.add(t_nid_e)

    if not any(nid not in attached_to_main for nid in node_by_id):
        return set()
    return attached_to_main


def _bbox_center(xs: List[float], ys: List[float]) -> Tuple[float, float]:
    if not xs or not ys:
        return 0.0, 0.0
    return (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0


# ═══════════════════════════════════════════════════════════════════════════════
# Original block-diagram layout engine
# ═══════════════════════════════════════════════════════════════════════════════

def _smart_layout_engine(graph: Dict[str, Any]) -> Dict[str, Any]:
    """Domain-aware Modelica layout engine — pure Python, no external dependency."""
    import copy
    from collections import defaultdict

    result = copy.deepcopy(graph)
    if not result.get("id"):
        result["id"] = "smart_layout_root"

    children: List[Dict[str, Any]] = [
        c for c in (result.get("children") or []) if isinstance(c, dict)
    ]
    edges: List[Dict[str, Any]] = [
        e for e in (result.get("edges") or []) if isinstance(e, dict)
    ]

    if not children:
        result["_modelica_coords"] = True
        return result

    # ── 1. Normalise edge format ──────────────────────────────────────────────
    for i, edge in enumerate(edges):
        if "source" in edge and "sources" not in edge:
            edge["sources"] = [edge.pop("source")]
        if "target" in edge and "targets" not in edge:
            edge["targets"] = [edge.pop("target")]
        if not edge.get("id"):
            s = (edge.get("sources") or ["?"])[0]
            t = (edge.get("targets") or ["?"])[0]
            edge["id"] = f"sl_e{i}_{s}__{t}"

    # ── 2. Build port→node index ──────────────────────────────────────────────
    port_to_node: Dict[str, str] = {}
    node_by_id: Dict[str, Dict[str, Any]] = {}
    node_ids: List[str] = []
    for node in children:
        nid = str(node.get("id", ""))
        node_ids.append(nid)
        node_by_id[nid] = node
        port_to_node[nid] = nid
        for port in node.get("ports") or []:
            if isinstance(port, dict):
                port_to_node[str(port.get("id", ""))] = nid

    # ── 2b. Dispatch to circuit layout engine when appropriate ────────────────
    if _is_circuit_mode(children):
        return _circuit_layout_engine(result, children, edges, node_by_id, port_to_node)

    # ── 3. Assign port sides from MSL name conventions ────────────────────────
    for node in children:
        nid = str(node.get("id", ""))
        for port in node.get("ports") or []:
            if not isinstance(port, dict):
                continue
            if port.get("side", ""):
                continue  # user explicitly specified side — don't override
            pid = str(port.get("id", ""))
            pname = _sl_port_short_name(pid, nid)
            side = _SL_PORT_SIDE_MAP.get(pname, "")
            if side:
                port.setdefault("properties", {}).setdefault("port.side", side)

    # ── 2.5. Identify satellite nodes (one-port hanging off a multi-port hub)
    satellite_nodes = _classify_layout_satellites(children, edges, port_to_node, node_by_id)
    satellite_connected_to: Dict[str, str] = {}
    satellite_edge_ports: Dict[str, Tuple[str, str]] = {}

    for edge in edges:
        srcs_e = list(edge.get("sources") or [])
        tgts_e = list(edge.get("targets") or [])
        for s_pid_e in srcs_e:
            s_nid_e = port_to_node.get(str(s_pid_e), str(s_pid_e).split(".")[0])
            for t_pid_e in tgts_e:
                t_nid_e = port_to_node.get(str(t_pid_e), str(t_pid_e).split(".")[0])
                if s_nid_e == t_nid_e:
                    continue
                if s_nid_e in satellite_nodes and t_nid_e not in satellite_nodes and t_nid_e in node_by_id:
                    if s_nid_e not in satellite_connected_to:
                        satellite_connected_to[s_nid_e] = t_nid_e
                        satellite_edge_ports[s_nid_e] = (str(s_pid_e), str(t_pid_e))
                elif t_nid_e in satellite_nodes and s_nid_e not in satellite_nodes and s_nid_e in node_by_id:
                    if t_nid_e not in satellite_connected_to:
                        satellite_connected_to[t_nid_e] = s_nid_e
                        satellite_edge_ports[t_nid_e] = (str(t_pid_e), str(s_pid_e))

    topo_node_ids = [n for n in node_ids if n not in satellite_nodes]
    if not topo_node_ids and node_ids:
        satellite_nodes.clear()
        satellite_connected_to.clear()
        satellite_edge_ports.clear()
        topo_node_ids = list(node_ids)

    # ── 4. Build directed graph for topological sort ──────────────────────────
    adj_fwd: Dict[str, List[str]] = {n: [] for n in topo_node_ids}
    adj_bwd: Dict[str, List[str]] = {n: [] for n in topo_node_ids}
    in_degree: Dict[str, int] = {n: 0 for n in topo_node_ids}

    def _get_port_side(port_id: str, node_id: str) -> str:
        node = node_by_id.get(node_id, {})
        for port in (node.get("ports") or []):
            if isinstance(port, dict) and str(port.get("id", "")) == port_id:
                explicit = port.get("side", "")
                if explicit:
                    return explicit
                props_side = (port.get("properties") or {}).get("port.side", "")
                if props_side:
                    return props_side
        return _SL_PORT_SIDE_MAP.get(_sl_port_short_name(port_id, node_id), "")

    for edge in edges:
        srcs = list(edge.get("sources") or [])
        tgts = list(edge.get("targets") or [])
        for s_pid in srcs:
            s_nid = port_to_node.get(str(s_pid), str(s_pid).split(".")[0])
            for t_pid in tgts:
                t_nid = port_to_node.get(str(t_pid), str(t_pid).split(".")[0])
                if s_nid not in node_by_id or t_nid not in node_by_id or s_nid == t_nid:
                    continue
                if s_nid in satellite_nodes or t_nid in satellite_nodes:
                    continue
                if t_nid in adj_fwd.get(s_nid, []):
                    continue
                s_side = _get_port_side(str(s_pid), s_nid)
                t_side = _get_port_side(str(t_pid), t_nid)
                if s_side == "WEST" and t_side == "EAST":
                    adj_fwd[t_nid].append(s_nid)
                    adj_bwd[s_nid].append(t_nid)
                    in_degree[s_nid] += 1
                else:
                    adj_fwd[s_nid].append(t_nid)
                    adj_bwd[t_nid].append(s_nid)
                    in_degree[t_nid] += 1

    # ── 4b. Remove back-edges via iterative DFS ───────────────────────────────
    visited_dfs: set = set()
    on_stack_dfs: set = set()
    back_edge_set: set = set()

    for start in topo_node_ids:
        if start in visited_dfs:
            continue
        dfs_iter_stack = [(start, iter(list(adj_fwd.get(start, []))))]
        visited_dfs.add(start)
        on_stack_dfs.add(start)
        while dfs_iter_stack:
            dfs_node, dfs_ch_iter = dfs_iter_stack[-1]
            try:
                child = next(dfs_ch_iter)
                if child in on_stack_dfs:
                    back_edge_set.add((dfs_node, child))
                elif child not in visited_dfs:
                    visited_dfs.add(child)
                    on_stack_dfs.add(child)
                    dfs_iter_stack.append((child, iter(list(adj_fwd.get(child, [])))))
            except StopIteration:
                dfs_iter_stack.pop()
                on_stack_dfs.discard(dfs_node)

    for s_nid, t_nid in back_edge_set:
        if t_nid in adj_fwd.get(s_nid, []):
            adj_fwd[s_nid].remove(t_nid)
        if s_nid in adj_bwd.get(t_nid, []):
            adj_bwd[t_nid].remove(s_nid)
        in_degree[t_nid] = max(0, in_degree[t_nid] - 1)

    # ── 5. Layer assignment: Kahn topological sort + longest-path depth ───────
    temp_indeg = dict(in_degree)
    heap: List[str] = [n for n in topo_node_ids if temp_indeg[n] == 0]
    heapq.heapify(heap)
    topo_order: List[str] = []
    seen_topo: set = set()
    while heap:
        n = heapq.heappop(heap)
        if n in seen_topo:
            continue
        seen_topo.add(n)
        topo_order.append(n)
        for s in adj_fwd[n]:
            temp_indeg[s] -= 1
            if temp_indeg[s] == 0:
                heapq.heappush(heap, s)
    topo_order.extend(sorted(n for n in topo_node_ids if n not in seen_topo))

    layers: Dict[str, int] = {}
    for n in topo_order:
        preds = adj_bwd.get(n, [])
        layers[n] = (max(layers.get(p, 0) for p in preds) + 1) if preds else 0

    satellite_stack_height: Dict[str, float] = {}
    satellites_by_target: Dict[str, List[str]] = defaultdict(list)
    for sat_nid, target_nid in satellite_connected_to.items():
        if target_nid:
            satellites_by_target[target_nid].append(sat_nid)
    for target_nid, sat_ids in satellites_by_target.items():
        sat_total_h = 0.0
        max_sat_h = 0.0
        for sat_nid in sat_ids:
            sat_h = float(node_by_id.get(sat_nid, {}).get("height", _SL_DEFAULT_HH * 2))
            sat_total_h += sat_h
            max_sat_h = max(max_sat_h, sat_h)
        if len(sat_ids) > 1:
            sat_total_h += _SL_MIN_GAP * (len(sat_ids) - 1)
        base_h = float(node_by_id.get(target_nid, {}).get("height", _SL_DEFAULT_HH * 2))
        satellite_stack_height[target_nid] = max(base_h, sat_total_h, base_h + _SL_MIN_GAP + max_sat_h)

    # ── 6. Grid positions: column = layer, row order = crossing minimization ──
    layer_groups: Dict[int, List[str]] = defaultdict(list)
    for nid in topo_node_ids:
        layer_groups[layers.get(nid, 0)].append(nid)
    layer_sorted_keys = sorted(layer_groups.keys())
    for lyr in layer_sorted_keys:
        layer_groups[lyr].sort()
    _sl_reorder_layers_minimize_crossings(
        layer_groups, layer_sorted_keys, adj_fwd, adj_bwd, iterations=5
    )

    max_hw_per_layer: Dict[int, float] = {}
    max_hh_per_layer: Dict[int, float] = {}
    for nid in topo_node_ids:
        lyr = layers.get(nid, 0)
        nw = float(node_by_id[nid].get("width", _SL_DEFAULT_HW * 2))
        nh = satellite_stack_height.get(nid, float(node_by_id[nid].get("height", _SL_DEFAULT_HH * 2)))
        max_hw_per_layer[lyr] = max(max_hw_per_layer.get(lyr, 0.0), nw / 2)
        max_hh_per_layer[lyr] = max(max_hh_per_layer.get(lyr, 0.0), nh / 2)

    layer_cx_map: Dict[int, float] = {}
    cum_x = 0.0
    prev_max_hw = max_hw_per_layer.get(layer_sorted_keys[0], _SL_DEFAULT_HW) if layer_sorted_keys else _SL_DEFAULT_HW
    for i, lyr in enumerate(layer_sorted_keys):
        curr_max_hw = max_hw_per_layer.get(lyr, _SL_DEFAULT_HW)
        if i == 0:
            layer_cx_map[lyr] = 0.0
        else:
            h_spacing = max(prev_max_hw + curr_max_hw + _SL_MIN_GAP, _SL_H_SPACING)
            cum_x += h_spacing
            layer_cx_map[lyr] = cum_x
        prev_max_hw = curr_max_hw

    node_center: Dict[str, Tuple[float, float]] = {}
    for lyr in layer_sorted_keys:
        col_nodes = layer_groups[lyr]
        cx_col = layer_cx_map[lyr]
        y_offsets: List[float] = [0.0]
        for row_i in range(1, len(col_nodes)):
            prev_id = col_nodes[row_i - 1]
            curr_id = col_nodes[row_i]
            prev_hh = satellite_stack_height.get(
                prev_id, float(node_by_id[prev_id].get("height", _SL_DEFAULT_HH * 2))
            ) / 2
            curr_hh = satellite_stack_height.get(
                curr_id, float(node_by_id[curr_id].get("height", _SL_DEFAULT_HH * 2))
            ) / 2
            v_step = max(prev_hh + curr_hh + _SL_MIN_GAP, _SL_V_SPACING)
            y_offsets.append(y_offsets[-1] + v_step)
        max_offset = y_offsets[-1]
        for row_i, nid in enumerate(col_nodes):
            cy_row = -(y_offsets[row_i] - max_offset / 2.0)
            node_center[nid] = (cx_col, cy_row)

    all_cx = [cx for cx, _ in node_center.values()]
    all_cy = [cy for _, cy in node_center.values()]
    origin_cx, origin_cy = _bbox_center(all_cx, all_cy)
    node_center = {
        nid: (cx - origin_cx, cy - origin_cy)
        for nid, (cx, cy) in node_center.items()
    }

    # ── 7. Write positions back to nodes ─────────────────────────────────────
    for node in children:
        nid = str(node.get("id", ""))
        if nid not in node_center:
            continue
        cx, cy = node_center[nid]
        nw = float(node.get("width", 0)) or (_SL_DEFAULT_HW * 2)
        nh = float(node.get("height", 0)) or (_SL_DEFAULT_HH * 2)
        hw, hh = nw / 2.0, nh / 2.0
        node["x"] = cx - hw
        node["y"] = cy - hh
        node["width"] = nw
        node["height"] = nh

    # ── 6.5. Place satellite nodes around their connected main node ───────────
    satellite_port_side_override: Dict[str, str] = {}
    satellites_by_slot: Dict[Tuple[str, str], List[str]] = defaultdict(list)
    satellite_slot: Dict[str, str] = {}
    for sat_nid in satellite_nodes:
        target_nid = satellite_connected_to.get(sat_nid)
        sat_pid, target_pid = satellite_edge_ports.get(sat_nid, ("", ""))
        sat_side = _get_port_side(sat_pid, sat_nid) or _SL_PORT_SIDE_MAP.get(
            _sl_port_short_name(sat_pid, sat_nid), ""
        )
        target_side = _get_port_side(target_pid, target_nid or "") or _SL_PORT_SIDE_MAP.get(
            _sl_port_short_name(target_pid, target_nid or ""), ""
        )
        sat_pname = _sl_port_short_name(sat_pid, sat_nid)
        target_pname = _sl_port_short_name(target_pid, target_nid or "")
        is_signal_satellite = (
            _SL_PORT_DOMAIN.get(sat_pname) == "signal"
            or _SL_PORT_DOMAIN.get(target_pname) == "signal"
        )
        if is_signal_satellite and sat_side == "EAST" and target_side in ("", "WEST"):
            slot = "WEST"
        elif is_signal_satellite and sat_side == "WEST" and target_side == "EAST":
            slot = "EAST"
        else:
            slot = "SOUTH"
        satellite_slot[sat_nid] = slot
        satellites_by_slot[(target_nid or "", slot)].append(sat_nid)

    satellite_slot_index: Dict[str, Tuple[int, int]] = {}
    for sats in satellites_by_slot.values():
        sats.sort()
        for idx, sat_nid in enumerate(sats):
            satellite_slot_index[sat_nid] = (idx, len(sats))

    for sat_nid in satellite_nodes:
        sat_node = node_by_id[sat_nid]
        sat_hw = float(sat_node.get("width", _SL_DEFAULT_HW * 2)) / 2
        sat_hh = float(sat_node.get("height", _SL_DEFAULT_HH * 2)) / 2
        target_nid = satellite_connected_to.get(sat_nid)
        slot = satellite_slot.get(sat_nid, "SOUTH")
        idx, count = satellite_slot_index.get(sat_nid, (0, 1))
        if target_nid and target_nid in node_center:
            tx, ty = node_center[target_nid]
            t_node = node_by_id[target_nid]
            t_hw = float(t_node.get("width", _SL_DEFAULT_HW * 2)) / 2
            t_hh = float(t_node.get("height", _SL_DEFAULT_HH * 2)) / 2
            spread = max(float(sat_node.get("height", _SL_DEFAULT_HH * 2)) + _SL_MIN_GAP, _SL_V_SPACING)
            offset = (idx - (count - 1) / 2.0) * spread
            if slot == "WEST":
                node_center[sat_nid] = (tx - t_hw - _SL_MIN_GAP - sat_hw, ty - offset)
                satellite_port_side_override[sat_nid] = "EAST"
            elif slot == "EAST":
                node_center[sat_nid] = (tx + t_hw + _SL_MIN_GAP + sat_hw, ty - offset)
                satellite_port_side_override[sat_nid] = "WEST"
            else:
                h_spread = max(float(sat_node.get("width", _SL_DEFAULT_HW * 2)) + _SL_MIN_GAP, _SL_H_SPACING)
                x_offset = (idx - (count - 1) / 2.0) * h_spread
                sat_y = ty - t_hh - _SL_MIN_GAP - sat_hh
                node_center[sat_nid] = (tx + x_offset, sat_y)
                satellite_port_side_override[sat_nid] = "NORTH"
        else:
            node_center[sat_nid] = (0.0, -_SL_MIN_GAP - sat_hh)
            satellite_port_side_override[sat_nid] = "NORTH"
        scx, scy = node_center[sat_nid]
        sat_node["x"] = scx - sat_hw
        sat_node["y"] = scy - sat_hh
        sat_node.setdefault("width",  sat_hw * 2)
        sat_node.setdefault("height", sat_hh * 2)
        sat_node["rotation"] = 0

    # ── 7.5. Compute component rotation ──────────────────────────────────────
    for node in children:
        nid = str(node.get("id", ""))
        if nid in satellite_nodes:
            continue
        rotation = 0
        for port in (node.get("ports") or []):
            if not isinstance(port, dict):
                continue
            pid = str(port.get("id", ""))
            pname = _sl_port_short_name(pid, nid)
            if pname not in _SL_PRIMARY_PORTS:
                continue
            natural_side = _SL_PORT_SIDE_MAP.get(pname, "WEST")
            assigned_side = (
                port.get("side", "")
                or (port.get("properties") or {}).get("port.side", "")
                or _SL_PORT_SIDE_MAP.get(pname, "")
            )
            if assigned_side and assigned_side != natural_side:
                rotation = _SL_ROTATION_MAP.get((natural_side, assigned_side), 0)
            break
        node["rotation"] = rotation

    # ── 8. Orthogonal edge routing ────────────────────────────────────────────
    if node_center:
        main_bottoms = [
            cy - float(node_by_id[nid].get("height", _SL_DEFAULT_HH * 2)) / 2
            for nid, (cx, cy) in node_center.items()
        ]
        min_bottom_y = min(main_bottoms)
        backward_bus_y = min_bottom_y - _SL_MIN_GAP * 3
    else:
        backward_bus_y = -50.0

    def _effective_side(pid: str, nid: str, fallback: str) -> str:
        if nid in satellite_port_side_override:
            return satellite_port_side_override[nid]
        return _get_port_side(pid, nid) or _SL_PORT_SIDE_MAP.get(
            _sl_port_short_name(pid, nid), fallback
        )

    for edge in edges:
        srcs = list(edge.get("sources") or [])
        tgts = list(edge.get("targets") or [])
        if not srcs or not tgts:
            continue
        s_pid = str(srcs[0])
        t_pid = str(tgts[0])
        s_nid = port_to_node.get(s_pid, s_pid.split(".")[0])
        t_nid = port_to_node.get(t_pid, t_pid.split(".")[0])

        if s_nid not in node_center or t_nid not in node_center:
            continue

        s_node = node_by_id.get(s_nid, {})
        t_node = node_by_id.get(t_nid, {})
        s_hw = float(s_node.get("width",  _SL_DEFAULT_HW * 2)) / 2
        s_hh = float(s_node.get("height", _SL_DEFAULT_HH * 2)) / 2
        t_hw = float(t_node.get("width",  _SL_DEFAULT_HW * 2)) / 2
        t_hh = float(t_node.get("height", _SL_DEFAULT_HH * 2)) / 2

        sx, sy = node_center[s_nid]
        tx, ty = node_center[t_nid]
        s_pname = _sl_port_short_name(s_pid, s_nid)
        t_pname = _sl_port_short_name(t_pid, t_nid)
        s_side = _effective_side(s_pid, s_nid, "EAST")
        t_side = _effective_side(t_pid, t_nid, "WEST")

        sp = _sl_port_anchor(sx, sy, s_hw, s_hh, s_side)
        tp = _sl_port_anchor(tx, ty, t_hw, t_hh, t_side)

        s_lyr = layers.get(s_nid, 0)
        t_lyr = layers.get(t_nid, 0)
        is_back_edge = (s_nid, t_nid) in back_edge_set or s_lyr > t_lyr

        if is_back_edge and s_side not in ("SOUTH", "NORTH") and t_side not in ("SOUTH", "NORTH"):
            bend_pts: List[Tuple[float, float]] = [(sp[0], backward_bus_y), (tp[0], backward_bus_y)]
        elif abs(sp[1] - tp[1]) < 1.0 and abs(sp[0] - tp[0]) > 0.5:
            bend_pts = []
        elif s_side == "NORTH" and sp[1] <= tp[1]:
            bend_pts = [(sp[0], tp[1])]
        elif t_side == "SOUTH" and tp[1] <= sp[1]:
            bend_pts = [(tp[0], sp[1])]
        elif s_side in ("SOUTH", "NORTH") or t_side in ("SOUTH", "NORTH"):
            bus_y = min(sp[1], tp[1]) - 4.0
            bend_pts = [(sp[0], bus_y), (tp[0], bus_y)]
        else:
            mid_x = (sp[0] + tp[0]) / 2.0
            bend_pts = [(mid_x, sp[1]), (mid_x, tp[1])]

        domain = (
            _SL_PORT_DOMAIN.get(s_pname)
            or _SL_PORT_DOMAIN.get(t_pname)
            or "unknown"
        )
        color = _SL_DOMAIN_COLORS.get(domain, _SL_DOMAIN_COLORS["unknown"])

        edge["sections"] = [
            {
                "id": f"sec_{edge['id']}",
                "startPoint": {"x": sp[0], "y": sp[1]},
                "endPoint":   {"x": tp[0], "y": tp[1]},
                "bendPoints": [{"x": p[0], "y": p[1]} for p in bend_pts],
            }
        ]
        edge["_color"] = color

    result["_modelica_coords"] = True
    return result


def _sections_to_points_str(sections: List[Dict[str, Any]]) -> str:
    """Convert layout edge sections (with bendPoints) to Modelica Line points string."""
    if not sections:
        return ""
    sec = sections[0]
    sp = sec.get("startPoint") or {}
    ep = sec.get("endPoint") or {}
    bps = sec.get("bendPoints") or []
    all_pts = [sp] + list(bps) + [ep]
    pts = ",".join(
        f"{{{_fmt_layout_num(pt.get('x', 0))},{_fmt_layout_num(pt.get('y', 0))}}}"
        for pt in all_pts
        if pt
    )
    return f"{{{pts}}}" if pts else ""


def _sl_resolve_instance_for_port(port: str, child_ids: set) -> str:
    """Map a connect port path to the diagram instance name (longest matching child id).

    Modelica allows hierarchical connector paths; graph children are keyed by instance
    name. Using only the first segment breaks for names that share prefixes — prefer
    the longest child id prefix match.
    """
    if not port:
        return ""
    if not child_ids:
        return port.split(".", 1)[0] if "." in port else port
    best = ""
    for cid in child_ids:
        if not cid:
            continue
        if port == cid or port.startswith(cid + "."):
            if len(cid) > len(best):
                best = cid
    if best:
        return best
    return port.split(".", 1)[0] if "." in port else port


def _sl_port_suffix(port: str) -> str:
    return port.rsplit(".", 1)[-1] if port else ""


def _sl_build_edge_route_lookups(
    layout_edges: List[Any],
    child_ids: set,
) -> Tuple[
    Dict[Any, List[Dict[str, Any]]],
    Dict[Any, Tuple[int, int, int]],
    Dict[frozenset, List[Tuple[frozenset, List[Dict[str, Any]], Optional[Tuple[int, int, int]]]]],
]:
    """Port-pair routes plus instance-pair fallbacks when graph vs .mo port strings differ."""
    edge_route_map: Dict[Any, List[Dict[str, Any]]] = {}
    edge_color_map: Dict[Any, Tuple[int, int, int]] = {}
    inst_pair_routes: Dict[
        frozenset, List[Tuple[frozenset, List[Dict[str, Any]], Optional[Tuple[int, int, int]]]]
    ] = {}

    for edge in layout_edges:
        if not isinstance(edge, dict):
            continue
        srcs = list(edge.get("sources") or [])
        tgts = list(edge.get("targets") or [])
        sections = edge.get("sections") or []
        if not (srcs and tgts and sections):
            continue
        s = str(srcs[0])
        t = str(tgts[0])
        key = frozenset([s, t])
        edge_route_map[key] = sections
        color_tuple: Optional[Tuple[int, int, int]] = None
        color_hint = edge.get("_color")
        if isinstance(color_hint, (list, tuple)) and len(color_hint) >= 3:
            try:
                color_tuple = (int(color_hint[0]), int(color_hint[1]), int(color_hint[2]))
            except (TypeError, ValueError):
                color_tuple = None
        if color_tuple is not None:
            edge_color_map[key] = color_tuple

        s_i = _sl_resolve_instance_for_port(s, child_ids)
        t_i = _sl_resolve_instance_for_port(t, child_ids)
        ip = frozenset([s_i, t_i])
        inst_pair_routes.setdefault(ip, []).append((key, sections, color_tuple))

    return edge_route_map, edge_color_map, inst_pair_routes


def _sl_resolve_sections_for_connect(
    a_port: str,
    b_port: str,
    edge_route_map: Dict[Any, List[Dict[str, Any]]],
    edge_color_map: Dict[Any, Tuple[int, int, int]],
    inst_pair_routes: Dict[
        frozenset, List[Tuple[frozenset, List[Dict[str, Any]], Optional[Tuple[int, int, int]]]]
    ],
    child_ids: set,
) -> Tuple[Optional[List[Dict[str, Any]]], Optional[Tuple[int, int, int]]]:
    """Resolve routed sections for one connect(a,b), tolerating port id mismatches."""
    edge_key = frozenset([a_port, b_port])
    sections = edge_route_map.get(edge_key)
    color_rgb = edge_color_map.get(edge_key)
    if sections and _sections_to_points_str(sections):
        return sections, color_rgb

    a_i = _sl_resolve_instance_for_port(a_port, child_ids)
    b_i = _sl_resolve_instance_for_port(b_port, child_ids)
    ip = frozenset([a_i, b_i])
    cands = inst_pair_routes.get(ip, [])

    if len(cands) == 1:
        _pk, sec, col = cands[0]
        if sec and _sections_to_points_str(sec):
            return sec, col if col is not None else edge_color_map.get(_pk)

    if len(cands) > 1:
        for pk, sec, col in cands:
            if pk == edge_key and sec and _sections_to_points_str(sec):
                return sec, col if col is not None else edge_color_map.get(pk)
        ap = _sl_port_suffix(a_port)
        bp = _sl_port_suffix(b_port)
        if ap and bp:
            matched: List[Tuple[List[Dict[str, Any]], Optional[Tuple[int, int, int]]]] = []
            for pk, sec, col in cands:
                parts = list(pk)
                if len(parts) != 2:
                    continue
                s0 = _sl_port_suffix(parts[0])
                s1 = _sl_port_suffix(parts[1])
                if {s0, s1} == {ap, bp} and sec and _sections_to_points_str(sec):
                    matched.append((sec, col))
            if len(matched) == 1:
                return matched[0][0], matched[0][1]

    if sections and not _sections_to_points_str(sections):
        return None, color_rgb
    return None, None


def _apply_layout_graph_to_modelica_code(
    modelica_code: str, layout_graph: Dict[str, Any]
) -> Tuple[str, Dict[str, Any]]:
    from core.modelica_layout_writer import apply_layout_graph_to_modelica_code

    patched, stats = apply_layout_graph_to_modelica_code(modelica_code, layout_graph)
    return patched, {
        "components_updated": int(stats.get("components_updated", 0)),
        "connects_updated": int(stats.get("connects_updated", 0)),
        "diagnostics": stats.get("diagnostics", []),
    }


def _normalize_graph_format(graph: Dict[str, Any]) -> Dict[str, Any]:
    """Convert simplified graph dict to standard layout-compatible format."""
    if not isinstance(graph, dict):
        return graph

    result = dict(graph)
    if not result.get("id"):
        result["id"] = "smart_layout_root"

    if "nodes" in result and "children" not in result:
        result["children"] = result.pop("nodes")

    raw_edges = result.get("edges", [])
    if isinstance(raw_edges, list):
        normalized_edges = []
        for i, edge in enumerate(raw_edges):
            if not isinstance(edge, dict):
                normalized_edges.append(edge)
                continue
            e = dict(edge)
            if "source" in e and "sources" not in e:
                e["sources"] = [e.pop("source")]
            if "target" in e and "targets" not in e:
                e["targets"] = [e.pop("target")]
            if not e.get("id"):
                src = (e.get("sources") or ["?"])[0]
                tgt = (e.get("targets") or ["?"])[0]
                e["id"] = f"edge_{src}__{tgt}_{i}"
            normalized_edges.append(e)
        result["edges"] = normalized_edges

    return result
