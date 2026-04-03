"""Intent-aware query planning for doc retrieval."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


_SYNONYMS = {
    "全局力": "globalforce",
    "直线力": "linearforce",
    "世界坐标力": "worldforce",
    "api": "interface",
}


@dataclass(frozen=True)
class QueryPlan:
    query: str
    normalized_query: str
    tokens: List[str]
    expanded_tokens: List[str]
    intent: str


def _norm(text: str) -> str:
    return " ".join(str(text or "").lower().split())


def _tokenize(text: str) -> List[str]:
    return [t for t in re.split(r"[\s,;|/\\]+", _norm(text)) if t]


def detect_intent(text: str) -> str:
    q = _norm(text)
    if any(k in q for k in ("列出", "list", "all api", "所有接口")):
        return "enumeration"
    if "." in q or "/" in q or "\\" in q:
        return "exact_locate"
    return "explain"


def expand_tokens(tokens: List[str]) -> List[str]:
    out = set(tokens)
    for tok in list(tokens):
        if tok in _SYNONYMS:
            out.add(_SYNONYMS[tok])
    return sorted(out)


def build_query_plan(query: str) -> QueryPlan:
    tokens = _tokenize(query)
    return QueryPlan(
        query=query,
        normalized_query=_norm(query),
        tokens=tokens,
        expanded_tokens=expand_tokens(tokens),
        intent=detect_intent(query),
    )


__all__ = ["QueryPlan", "build_query_plan", "detect_intent"]

