"""Argument adapters used by permissive compatibility APIs."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .contracts import RAGConfig


def config_from_legacy_args(args: tuple[Any, ...], kwargs: Dict[str, Any]) -> RAGConfig:
    """Build RAGConfig from a permissive legacy arg/kwarg payload."""
    top_k = kwargs.get("top_k")
    return RAGConfig(
        index_path=kwargs.get("index_path"),
        embedding_model=kwargs.get("embedding_model"),
        top_k=int(top_k) if top_k is not None else 5,
        extra={
            "args": list(args),
            "kwargs": {k: v for k, v in kwargs.items() if k not in {"top_k", "index_path", "embedding_model"}},
        },
    )


def resolve_question(args: tuple[Any, ...], kwargs: Dict[str, Any]) -> str:
    """Resolve query text from permissive legacy signatures."""
    question: Optional[Any] = kwargs.pop("question", None)
    if question is None and args:
        question = args[0]
    return str(question or "")

