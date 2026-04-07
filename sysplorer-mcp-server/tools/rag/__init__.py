"""RAG package skeleton for Modelica docs."""

from .compat import build_index, get_service, health_check, init_service, query
from .contracts import Document, QueryResponse, RAGConfig, RetrievalResult
from .service import RAGService

__all__ = [
    "RAGConfig",
    "Document",
    "RetrievalResult",
    "QueryResponse",
    "RAGService",
    "get_service",
    "init_service",
    "build_index",
    "query",
    "health_check",
]
