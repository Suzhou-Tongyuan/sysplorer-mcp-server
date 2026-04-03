"""Programmatic evaluator for RAG retrieval regression checks."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from .dataset import load_samples
from .metrics import summarize_retrieval


def run_regression(samples_path: str, search_fn: Callable[[str, int], List[Dict[str, Any]]]) -> Dict[str, Any]:
    rows = load_samples(samples_path)
    eval_rows: List[Dict[str, object]] = []
    for row in rows:
        query = str(row.get("query", ""))
        gold_paths = [str(x) for x in row.get("gold_paths", [])]
        hits = search_fn(query, 5)
        pred_paths = [str(h.get("path", "")) for h in hits]
        eval_rows.append({"query": query, "gold_paths": gold_paths, "pred_paths": pred_paths})
    metrics = summarize_retrieval(eval_rows)
    return {"sample_count": len(rows), "metrics": metrics}


__all__ = ["run_regression"]

