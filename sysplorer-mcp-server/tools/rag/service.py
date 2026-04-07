"""RAG service skeleton.

The implementation is intentionally a no-op baseline to keep API contracts
stable while deferring retrieval strategy details to later milestones.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Iterable, List, Optional

from .contracts import Document, QueryResponse, RAGConfig, RetrievalResult


class RAGService:
    """Framework-agnostic RAG service interface with no business strategy."""

    def __init__(self, config: Optional[RAGConfig] = None) -> None:
        self.config = config or RAGConfig()
        self._documents: List[Document] = []

    def build_index(self, documents: Optional[Iterable[Document]] = None, **_: Any) -> Dict[str, Any]:
        """Build or refresh index metadata without strategy details."""
        if documents is not None:
            self._documents = list(documents)
        return {
            "ok": True,
            "status": "skeleton",
            "indexed_documents": len(self._documents),
            "note": "Index strategy is intentionally not implemented in P0-1.",
        }

    def add_documents(self, documents: Iterable[Document], **_: Any) -> Dict[str, Any]:
        """Append documents into in-memory placeholder store."""
        incoming = list(documents)
        self._documents.extend(incoming)
        return {
            "ok": True,
            "status": "skeleton",
            "added_documents": len(incoming),
            "total_documents": len(self._documents),
        }

    def query(self, question: str, top_k: Optional[int] = None, **_: Any) -> QueryResponse:
        """Return deterministic empty result set until strategy is implemented."""
        return QueryResponse(
            question=question,
            results=[],
            trace={
                "status": "skeleton",
                "top_k": top_k if top_k is not None else self.config.top_k,
                "note": "Retrieval strategy is intentionally not implemented in P0-1.",
            },
        )

    def query_dict(self, question: str, top_k: Optional[int] = None, **kwargs: Any) -> Dict[str, Any]:
        """JSON-friendly query result helper."""
        response = self.query(question=question, top_k=top_k, **kwargs)
        return asdict(response)

    def health_check(self) -> Dict[str, Any]:
        """Module health endpoint for compatibility wrappers."""
        return {
            "ok": True,
            "status": "ready",
            "mode": "skeleton",
            "documents_buffered": len(self._documents),
        }


def to_document(payload: Dict[str, Any]) -> Document:
    """Lightweight adapter from dict payload into Document model."""
    return Document(
        doc_id=str(payload.get("doc_id") or payload.get("id") or ""),
        text=str(payload.get("text") or ""),
        metadata=dict(payload.get("metadata") or {}),
    )


def to_retrieval_result(payload: Dict[str, Any]) -> RetrievalResult:
    """Lightweight adapter from dict payload into RetrievalResult model."""
    return RetrievalResult(
        doc_id=str(payload.get("doc_id") or payload.get("id") or ""),
        text=str(payload.get("text") or ""),
        score=float(payload.get("score") or 0.0),
        metadata=dict(payload.get("metadata") or {}),
    )
