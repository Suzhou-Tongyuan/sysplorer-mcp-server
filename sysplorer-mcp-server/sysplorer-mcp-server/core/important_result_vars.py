"""Heuristic selection of a small set of “important” variables from a simulation result list."""

from __future__ import annotations

import re
from typing import Iterable, List, Set

# Penalise internal / bookkeeping signals common in MSL Blocks hierarchies.
_LOW_SIGNAL_FRAGMENTS = (
    "initType",
    "strict",
    "limitsAtInit",
    "controllerType",
    "lossPower",
    "phi_nominal",
    ".P.k",
    ".I.k",
    "addPID",
    "addI",
    "addSat",
    "gainPID",
    "gainTrack",
    "Dzero",
    "limiter.uMax",
    "limiter.uMin",
    ".nout",
    "deltaq[",
)

# Prefer these terminal segments (outputs / states / efforts).
_HIGH_SUFFIXES = (
    ".y",
    ".u_s",
    ".u_m",
    ".controlError",
    ".tau",
    ".phi_rel",
    ".w_rel",
    ".phi",
    ".w",
    ".a",
)


def _score(name: str) -> float:
    n = name.strip()
    if not n or n == "time":
        return -1000.0
    low = n.lower()
    s = 0.0
    for frag in _LOW_SIGNAL_FRAGMENTS:
        if frag.lower() in low:
            s -= 12.0
    if "flange_a" in low or "flange_b" in low:
        s -= 4.0
    for suf in _HIGH_SUFFIXES:
        if n.endswith(suf):
            s += 10.0 - 0.05 * len(suf)
            break
    else:
        if re.search(r"\.u\d*$", n):
            s += 5.0
    depth = n.count(".")
    s -= depth * 0.35
    if "[" in n:
        s -= 0.5
    return s


def _top_instance(name: str) -> str:
    if "." not in name:
        return name
    return name.split(".", 1)[0]


def pick_important_result_vars(
    names: Iterable[str],
    min_n: int = 3,
    max_n: int = 5,
    max_per_top_instance: int = 2,
) -> List[str]:
    """Return 3–5 variable names prioritising outputs/states and diversity across instances.

    ``names`` should be dynamic variables (e.g. ``GetResultVariables(2)``).
    """
    uniq: List[str] = []
    seen: Set[str] = set()
    for raw in names:
        n = str(raw).strip()
        if n and n not in seen:
            seen.add(n)
            uniq.append(n)

    min_n = max(1, min(min_n, max_n))
    max_n = max(min_n, max_n)

    ranked = sorted(uniq, key=lambda x: (-_score(x), len(x), x))
    picked: List[str] = []
    per_top: dict[str, int] = {}

    for n in ranked:
        if len(picked) >= max_n:
            break
        if _score(n) < -100:
            continue
        top = _top_instance(n)
        if per_top.get(top, 0) >= max_per_top_instance and len(picked) >= min_n:
            continue
        picked.append(n)
        per_top[top] = per_top.get(top, 0) + 1

    if len(picked) < min_n:
        for n in sorted(uniq, key=lambda x: (len(x), x)):
            if n in picked:
                continue
            picked.append(n)
            if len(picked) >= min_n:
                break

    return picked[:max_n]
