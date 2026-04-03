"""Local RAG index API (backward compatible) with hybrid retrieval backend."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from tools.rag.index.index_manager import (
    build_index_payload,
    load_index as _load_index,
    persist_index,
    search_index as _search_index,
)
# Default RAG corpora are defined at runtime via resources/resources_manifest.json
# (entries with default_index: true). This list is kept for API compatibility only.
DEFAULT_SOURCES: list[str] = []
DEFAULT_EXTENSIONS = {".mo", ".md", ".txt", ".json", ".yaml", ".yml", ".rst", ".html", ".htm"}
DEFAULT_INDEX_PATH = "tools/rag/modelica_doc_index.json"
WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_\.:/-]*|[0-9]+(?:\.[0-9]+)?")


def tokenize(text: str) -> List[str]:
    lowered = str(text or "").lower()
    tokens = [m.group(0) for m in WORD_RE.finditer(lowered)]
    cjk_chars = [ch for ch in lowered if "\u4e00" <= ch <= "\u9fff"]
    tokens.extend(cjk_chars)
    if len(cjk_chars) > 1:
        tokens.extend(cjk_chars[i] + cjk_chars[i + 1] for i in range(len(cjk_chars) - 1))
    return tokens


def bm25_build_index(
    sources: Iterable[str],
    index_path: str,
    chunk_size: int,
    overlap: int,
    extensions: set[str],
    max_file_size_mb: float = 8.0,
    min_chunk_chars: int = 60,
    max_files: int | None = None,
    path_relativize_to: Optional[Path | str] = None,
    max_chunks: int | None = None,
    lexical_only: bool = False,
) -> Dict[str, Any]:
    index = build_index_payload(
        sources=sources,
        chunk_size=chunk_size,
        overlap=overlap,
        extensions=extensions,
        max_file_size_mb=max_file_size_mb,
        min_chunk_chars=min_chunk_chars,
        max_files=max_files,
        path_relativize_to=path_relativize_to,
        max_chunks=max_chunks,
        lexical_only=lexical_only,
    )
    return persist_index(index, index_path)


def load_index(index_path: str) -> Dict[str, Any]:
    return _load_index(index_path)


def search_index(
    index: Dict[str, Any],
    query: str,
    top_k: int = 5,
    path_contains: str | None = None,
) -> List[Dict[str, Any]]:
    return _search_index(index=index, query=query, top_k=top_k, path_contains=path_contains)


__all__ = [
    "DEFAULT_SOURCES",
    "DEFAULT_EXTENSIONS",
    "DEFAULT_INDEX_PATH",
    "tokenize",
    "bm25_build_index",
    "load_index",
    "search_index",
]
