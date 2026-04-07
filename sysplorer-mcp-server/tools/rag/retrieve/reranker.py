"""Post-retrieval reranking and explainability helpers."""

from __future__ import annotations

from typing import Dict, List

from .query_planner import QueryPlan
from tools.rag.ingest.vuepress_loader import is_aggregate_doc


def rerank_results(results: List[Dict[str, object]], plan: QueryPlan, top_k: int) -> List[Dict[str, object]]:
    rescored: List[Dict[str, object]] = []
    for row in results:
        score = float(row.get("score", 0.0))
        path = str(row.get("path", ""))
        title = str(row.get("title", "")).lower()
        text = str(row.get("snippet", "")).lower()
        reasons: List[str] = []

        if plan.normalized_query and plan.normalized_query in path.lower():
            score += 0.9
            reasons.append("path_hit")
        if plan.normalized_query and plan.normalized_query in title:
            score += 0.7
            reasons.append("title_hit")
        if plan.normalized_query and plan.normalized_query in text:
            score += 0.5
            reasons.append("content_hit")
        if is_aggregate_doc(path):
            score -= 0.6
            reasons.append("aggregate_penalty")

        row2 = dict(row)
        row2["score"] = round(score, 6)
        row2["match_reason"] = ",".join(reasons[:3]) if reasons else "token_overlap"
        rescored.append(row2)

    rescored.sort(key=lambda x: float(x.get("score", 0.0)), reverse=True)
    return rescored[: max(1, int(top_k))]


__all__ = ["rerank_results"]
