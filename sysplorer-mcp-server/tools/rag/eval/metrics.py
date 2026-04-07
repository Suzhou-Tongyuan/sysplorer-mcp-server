"""Core evaluation metrics for retrieval quality."""

from __future__ import annotations

from typing import Dict, Iterable, List


def recall_at_k(pred_paths: List[str], gold_paths: Iterable[str], k: int) -> float:
    g = {x for x in gold_paths}
    if not g:
        return 0.0
    return 1.0 if any(p in g for p in pred_paths[: max(1, int(k))]) else 0.0


def mean(values: List[float]) -> float:
    return (sum(values) / len(values)) if values else 0.0


def summarize_retrieval(eval_rows: List[Dict[str, object]]) -> Dict[str, float]:
    r1: List[float] = []
    r5: List[float] = []
    for row in eval_rows:
        pred = [str(x) for x in row.get("pred_paths", [])]
        gold = [str(x) for x in row.get("gold_paths", [])]
        r1.append(recall_at_k(pred, gold, 1))
        r5.append(recall_at_k(pred, gold, 5))
    return {"recall_at_1": mean(r1), "recall_at_5": mean(r5)}


__all__ = ["recall_at_k", "summarize_retrieval"]

