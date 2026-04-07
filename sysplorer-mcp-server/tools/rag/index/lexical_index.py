"""Lexical (BM25-like) index construction and search."""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Tuple

WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_\.:/-]*|[0-9]+(?:\.[0-9]+)?")


def tokenize(text: str) -> List[str]:
    lowered = str(text or "").lower()
    tokens = [m.group(0) for m in WORD_RE.finditer(lowered)]
    cjk_chars = [ch for ch in lowered if "\u4e00" <= ch <= "\u9fff"]
    tokens.extend(cjk_chars)
    if len(cjk_chars) > 1:
        tokens.extend(cjk_chars[i] + cjk_chars[i + 1] for i in range(len(cjk_chars) - 1))
    return tokens


def split_text(text: str, chunk_size: int, overlap: int) -> List[Tuple[str, int, int]]:
    text = str(text or "").strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [(text, 0, len(text))]
    step = max(1, int(chunk_size) - int(overlap))
    out: List[Tuple[str, int, int]] = []
    i = 0
    while i < len(text):
        part = text[i : i + chunk_size]
        out.append((part, i, i + len(part)))
        i += step
    return out


def search_lexical(
    chunks: List[Dict[str, object]],
    df: Dict[str, int],
    avg_doc_len: float,
    query: str,
    top_k: int = 10,
    path_contains: str | None = None,
) -> List[Dict[str, object]]:
    q_tokens = tokenize(query)
    if not q_tokens:
        return []
    n_docs = max(int(len(chunks)), 1)
    avg_len = max(float(avg_doc_len), 1e-6)
    q_counts = Counter(q_tokens)
    scores: Dict[int, float] = defaultdict(float)
    k1, b = 1.5, 0.75

    for cid, chunk in enumerate(chunks):
        path = str(chunk.get("path", ""))
        if path_contains and path_contains.lower() not in path.lower():
            continue
        tf_map = chunk.get("token_freq", {})
        doc_len = max(int(chunk.get("len", 0)), 1)
        s = 0.0
        for tok, qf in q_counts.items():
            tf = int(tf_map.get(tok, 0))
            if tf <= 0:
                continue
            tok_df = int(df.get(tok, 0))
            if tok_df <= 0:
                continue
            idf = math.log(1.0 + (n_docs - tok_df + 0.5) / (tok_df + 0.5))
            denom = tf + k1 * (1 - b + b * (doc_len / avg_len))
            s += idf * ((tf * (k1 + 1)) / denom) * (1.0 + 0.15 * (qf - 1))
        if s > 0:
            scores[cid] = s

    rows: List[Dict[str, object]] = []
    qlow = query.lower()
    for cid, s in scores.items():
        ch = chunks[cid]
        txt = str(ch.get("text", ""))
        if qlow and qlow in txt.lower():
            s += 0.5
        rows.append(
            {
                "score": round(float(s), 6),
                "path": str(ch.get("path", "")),
                "title": str(ch.get("title", "")),
                "piece": int(ch.get("piece", 0)),
                "snippet": txt[:220].replace("\n", " ").strip(),
                "metadata": dict(ch.get("metadata", {})),
            }
        )
    rows.sort(key=lambda x: float(x["score"]), reverse=True)
    return rows[: max(1, int(top_k))]


__all__ = ["split_text", "search_lexical"]
