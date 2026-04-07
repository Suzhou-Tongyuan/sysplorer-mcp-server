"""RAG module contracts and shared data models.

This file intentionally contains only stable interfaces and data structures.
No retrieval strategy or ranking business logic is implemented here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class RAGConfig:
    """Configuration for RAG service wiring."""

    index_path: Optional[str] = None
    embedding_model: Optional[str] = None
    top_k: int = 5
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Document:
    """Raw input document record."""

    doc_id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievalResult:
    """Single retrieval result item."""

    doc_id: str
    text: str
    score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class QueryResponse:
    """Structured response returned by the RAG service."""

    question: str
    results: List[RetrievalResult]
    trace: Dict[str, Any] = field(default_factory=dict)
