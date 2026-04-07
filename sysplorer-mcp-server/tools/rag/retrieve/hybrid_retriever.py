"""Hybrid retrieval fusion (lexical + vector)."""

from __future__ import annotations

from typing import Dict, List

from .query_planner import QueryPlan


def _rrf_fuse(
    lexical: List[Dict[str, object]],
    vector: List[Dict[str, object]],
    k: int = 60,
) -> List[Dict[str, object]]:
    by_key: Dict[str, Dict[str, object]] = {}

    for rank, row in enumerate(lexical, 1):
        key = f"{row.get('path','')}#{row.get('piece',0)}"
        cur = by_key.setdefault(key, dict(row))
        cur["score"] = float(cur.get("score", 0.0)) + 1.0 / (k + rank)

    for rank, row in enumerate(vector, 1):
        key = f"{row.get('path','')}#{row.get('piece',0)}"
        cur = by_key.setdefault(key, dict(row))
        cur["score"] = float(cur.get("score", 0.0)) + 1.0 / (k + rank)

    rows = list(by_key.values())
    rows.sort(key=lambda x: float(x.get("score", 0.0)), reverse=True)
    return rows


def hybrid_retrieve(
    plan: QueryPlan,
    lexical_results: List[Dict[str, object]],
    vector_results: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    if plan.intent == "enumeration":
        # Enumeration prefers lexical precision and stable ordering.
        return lexical_results
    return _rrf_fuse(lexical_results, vector_results)


__all__ = ["hybrid_retrieve"]

