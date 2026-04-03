"""Compatibility API plus local BM25 index helpers for Modelica doc RAG."""

from __future__ import annotations

from typing import Any, Dict, Optional

from tools.rag.bm25 import (
    DEFAULT_EXTENSIONS,
    DEFAULT_INDEX_PATH,
    DEFAULT_SOURCES,
    bm25_build_index,
    load_index,
    search_index,
    tokenize,
)
from tools.rag.compat import build_index as _build_index
from tools.rag.compat import get_service as _get_service
from tools.rag.compat import health_check as _health_check
from tools.rag.compat import init_service as _init_service
from tools.rag.compat import query as _query


class ModelicaDocRAG:
    """Legacy class wrapper kept for API compatibility."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Keep existing behavior for explicit config, but avoid implicit reset.
        if args or kwargs:
            _init_service(*args, **kwargs)
        else:
            _get_service()

    def build_index(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return build_index(*args, **kwargs)

    def query(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return _query(*args, **kwargs)

    def retrieve(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return _query(*args, **kwargs)

    def health_check(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return _health_check(*args, **kwargs)


def init_modelica_doc_rag(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _init_service(*args, **kwargs)


def initialize_modelica_doc_rag(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _init_service(*args, **kwargs)


def get_modelica_doc_rag(*_: Any, **__: Any) -> ModelicaDocRAG:
    return ModelicaDocRAG()


def build_modelica_doc_index(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return build_index(*args, **kwargs)


def rebuild_modelica_doc_index(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    kwargs = dict(kwargs)
    kwargs.setdefault("force_rebuild", True)
    return build_index(*args, **kwargs)


def query_modelica_doc(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _query(*args, **kwargs)


def retrieve_modelica_doc(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _query(*args, **kwargs)


def search_modelica_doc(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _query(*args, **kwargs)


def rag_query(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _query(*args, **kwargs)


def health_check(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _health_check(*args, **kwargs)


def get_context(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _query(*args, **kwargs)


def get_modelica_doc_context(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _query(*args, **kwargs)


def build_index(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    if {"sources", "index_path", "chunk_size", "overlap", "extensions"} & set(kwargs.keys()):
        return bm25_build_index(
            sources=kwargs.get("sources", DEFAULT_SOURCES),
            index_path=str(kwargs.get("index_path", DEFAULT_INDEX_PATH)),
            chunk_size=int(kwargs.get("chunk_size", 900)),
            overlap=int(kwargs.get("overlap", 120)),
            extensions={str(x).lower() for x in kwargs.get("extensions", DEFAULT_EXTENSIONS)},
            max_file_size_mb=float(kwargs.get("max_file_size_mb", 8.0)),
            min_chunk_chars=int(kwargs.get("min_chunk_chars", 60)),
            max_files=kwargs.get("max_files"),
            path_relativize_to=kwargs.get("path_relativize_to"),
            max_chunks=kwargs.get("max_chunks"),
            lexical_only=bool(kwargs.get("lexical_only", False)),
        )
    return _build_index(*args, **kwargs)


def query(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _query(*args, **kwargs)


def configure(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    return _init_service(*args, **kwargs)


def set_config(config: Optional[dict] = None, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    merged_kwargs = dict(kwargs)
    if isinstance(config, dict):
        merged_kwargs.update(config)
    return _init_service(*args, **merged_kwargs)


__all__ = [
    "DEFAULT_SOURCES",
    "DEFAULT_EXTENSIONS",
    "DEFAULT_INDEX_PATH",
    "ModelicaDocRAG",
    "init_modelica_doc_rag",
    "initialize_modelica_doc_rag",
    "get_modelica_doc_rag",
    "build_modelica_doc_index",
    "rebuild_modelica_doc_index",
    "query_modelica_doc",
    "retrieve_modelica_doc",
    "search_modelica_doc",
    "rag_query",
    "health_check",
    "get_context",
    "get_modelica_doc_context",
    "build_index",
    "load_index",
    "search_index",
    "query",
    "configure",
    "set_config",
    "tokenize",
]
