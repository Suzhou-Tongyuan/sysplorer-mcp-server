"""Lightweight local vector index based on hashed token vectors."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Dict, List

WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_\.:/-]*|[0-9]+(?:\.[0-9]+)?")


def tokenize(text: str) -> List[str]:
    lowered = str(text or "").lower()
    tokens = [m.group(0) for m in WORD_RE.finditer(lowered)]
    cjk_chars = [ch for ch in lowered if "\u4e00" <= ch <= "\u9fff"]
    tokens.extend(cjk_chars)
    if len(cjk_chars) > 1:
        tokens.extend(cjk_chars[i] + cjk_chars[i + 1] for i in range(len(cjk_chars) - 1))
    return tokens


def _normalize(vec: Dict[str, float]) -> Dict[str, float]:
    norm = math.sqrt(sum(v * v for v in vec.values()))
    if norm <= 1e-12:
        return {}
    return {k: v / norm for k, v in vec.items()}


def vectorize_text(text: str) -> Dict[str, float]:
    counts = Counter(tokenize(text))
    return _normalize({k: float(v) for k, v in counts.items()})


def cosine_sparse(a: Dict[str, float], b: Dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    if len(a) > len(b):
        a, b = b, a
    return float(sum(v * b.get(k, 0.0) for k, v in a.items()))


def build_vector_index(chunks: List[Dict[str, object]]) -> List[Dict[str, float]]:
    return [vectorize_text(str(ch.get("text", ""))) for ch in chunks]


def search_vector(
    chunks: List[Dict[str, object]],
    vectors: List[Dict[str, float]],
    query: str,
    top_k: int = 10,
    path_contains: str | None = None,
) -> List[Dict[str, object]]:
    qv = vectorize_text(query)
    if not qv:
        return []
    scored: List[Dict[str, object]] = []
    for i, ch in enumerate(chunks):
        path = str(ch.get("path", ""))
        if path_contains and path_contains.lower() not in path.lower():
            continue
        s = cosine_sparse(qv, vectors[i] if i < len(vectors) else {})
        if s <= 0:
            continue
        txt = str(ch.get("text", ""))
        scored.append(
            {
                "score": round(float(s), 6),
                "path": path,
                "title": str(ch.get("title", "")),
                "piece": int(ch.get("piece", 0)),
                "snippet": txt[:220].replace("\n", " ").strip(),
                "metadata": dict(ch.get("metadata", {})),
            }
        )
    scored.sort(key=lambda x: float(x["score"]), reverse=True)
    return scored[: max(1, int(top_k))]


__all__ = ["build_vector_index", "search_vector"]
