"""Unified index manager: ingestion + lexical + vector index."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

from tools.rag.ingest import RawDocument, extract_text, iter_source_files, metadata_docs_from_json, source_type
from tools.rag.path_utils import posix_relative_to_anchor
from tools.rag.index.lexical_index import search_lexical, split_text
from tools.rag.index.vector_index import build_vector_index, search_vector
from tools.rag.retrieve import build_query_plan, hybrid_retrieve, rerank_results


def _tokenize(text: str) -> List[str]:
    # Keep tokenization close to previous behavior for compatibility.
    import re

    word_re = re.compile(r"[A-Za-z_][A-Za-z0-9_\.:/-]*|[0-9]+(?:\.[0-9]+)?")
    lowered = str(text).lower()
    tokens = [m.group(0) for m in word_re.finditer(lowered)]
    cjk_chars = [ch for ch in lowered if "\u4e00" <= ch <= "\u9fff"]
    tokens.extend(cjk_chars)
    if len(cjk_chars) > 1:
        tokens.extend(cjk_chars[i] + cjk_chars[i + 1] for i in range(len(cjk_chars) - 1))
    return tokens


def build_index_payload(
    sources: Iterable[str],
    chunk_size: int,
    overlap: int,
    extensions: set[str],
    max_file_size_mb: float = 8.0,
    min_chunk_chars: int = 60,
    max_files: int | None = None,
    path_relativize_to: Path | str | None = None,
    max_chunks: int | None = None,
    lexical_only: bool = False,
) -> Dict[str, Any]:
    anchor: Path | None = None
    if path_relativize_to is not None:
        anchor = Path(path_relativize_to).expanduser().resolve()

    docs: List[RawDocument] = []
    read_count = 0
    for path in iter_source_files(sources, extensions, max_file_size_mb=max_file_size_mb):
        if max_files is not None and read_count >= max_files:
            break
        if path.name.lower() == "privatelib_metadata.json":
            docs.extend(metadata_docs_from_json(path, relativize_to=anchor))
            read_count += 1
            continue
        text = extract_text(path)
        if not text.strip():
            continue
        display_path = posix_relative_to_anchor(path, anchor)
        docs.append(
            RawDocument(
                path=display_path,
                title=path.stem,
                text=text,
                metadata={"kind": "file", "suffix": path.suffix.lower(), "source_type": source_type(display_path)},
            )
        )
        read_count += 1

    cap = max_chunks if max_chunks is not None and max_chunks > 0 else None

    chunks: List[Dict[str, Any]] = []
    df: Dict[str, int] = defaultdict(int)
    total_len = 0
    for doc_idx, doc in enumerate(docs):
        if cap is not None and len(chunks) >= cap:
            break
        for piece_idx, (piece, start, end) in enumerate(split_text(doc.text, chunk_size, overlap)):
            if cap is not None and len(chunks) >= cap:
                break
            if len(piece.strip()) < min_chunk_chars:
                continue
            token_freq = Counter(_tokenize(piece))
            token_freq = Counter({k: v for k, v in token_freq.items() if len(k) > 1 or ("\u4e00" <= k <= "\u9fff")})
            if not token_freq:
                continue
            chunk = {
                "id": len(chunks),
                "doc_id": doc_idx,
                "path": doc.path,
                "title": doc.title,
                "piece": piece_idx,
                "start": start,
                "end": end,
                "text": piece,
                "metadata": dict(doc.metadata),
                "token_freq": dict(token_freq),
                "len": int(sum(token_freq.values())),
            }
            chunks.append(chunk)
            total_len += int(chunk["len"])
            for tok in token_freq:
                df[tok] += 1
        if cap is not None and len(chunks) >= cap:
            break

    avg_doc_len = (total_len / len(chunks)) if chunks else 0.0
    vectors: List[Dict[str, float]] = [] if lexical_only else build_vector_index(chunks)
    stored_sources = [posix_relative_to_anchor(Path(s), anchor) for s in sources]
    return {
        "version": 3,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "chunk_size": chunk_size,
        "overlap": overlap,
        "paths_relative_to": "resources" if anchor is not None else None,
        "sources": stored_sources,
        "extensions": sorted(extensions),
        "max_file_size_mb": max_file_size_mb,
        "min_chunk_chars": min_chunk_chars,
        "docs": [{"path": d.path, "title": d.title, "metadata": d.metadata} for d in docs],
        "chunks": chunks,
        "df": dict(df),
        "avg_doc_len": avg_doc_len,
        "num_docs": len(docs),
        "num_chunks": len(chunks),
        "vector_index": vectors,
        "retrieval": {"mode": "lexical" if lexical_only else "hybrid_rrf"},
    }


def persist_index(index: Dict[str, Any], index_path: str) -> Dict[str, Any]:
    out = Path(index_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    return index


def load_index(index_path: str) -> Dict[str, Any]:
    return json.loads(Path(index_path).read_text(encoding="utf-8"))


def search_index(index: Dict[str, Any], query: str, top_k: int = 5, path_contains: str | None = None) -> List[Dict[str, Any]]:
    plan = build_query_plan(query)
    chunks = list(index.get("chunks", []))
    lexical = search_lexical(
        chunks=chunks,
        df=dict(index.get("df", {})),
        avg_doc_len=float(index.get("avg_doc_len", 0.0)),
        query=query,
        top_k=max(20, top_k * 4),
        path_contains=path_contains,
    )
    mode = str((index.get("retrieval") or {}).get("mode", "") or "").lower()
    vectors = list(index.get("vector_index") or [])
    if mode == "lexical" or not vectors:
        return rerank_results(lexical, plan, top_k=max(1, int(top_k)))
    semantic = search_vector(chunks=chunks, vectors=vectors, query=query, top_k=max(20, top_k * 4), path_contains=path_contains)
    fused = hybrid_retrieve(plan, lexical, semantic)
    return rerank_results(fused, plan, top_k=max(1, int(top_k)))


__all__ = ["build_index_payload", "persist_index", "load_index", "search_index"]
