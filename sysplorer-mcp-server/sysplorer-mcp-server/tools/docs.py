"""RAG documentation search tools."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from mcp_instance import mcp
from path_config import (
    RAG_INDEX_PATH,
    effective_rag_lexical_only,
    effective_rag_max_chunks,
    get_resources_manifest_path,
    get_resources_root,
    get_rag_max_index_load_bytes,
)
from core.metadata_index import _get_rag_module
from core.resources_manifest import load_manifest, resolve_corpus_path
from core.utils import (
    _json,
    _resolve_rag_index_path,
    _resolve_rag_source_strings,
    _get_default_rag_sources,
)

MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL = "mworks_sysplorer_resources_retrieval"


def _prepare_rag_sources(
    rag: Any,
    sources: Optional[List[str]],
) -> List[str]:
    if sources is not None:
        return _resolve_rag_source_strings(list(sources))
    rag_sources = _get_default_rag_sources(rag)
    if not rag_sources:
        raise ValueError(
            "no indexable default corpora: check resources_manifest.json has default_index entries "
            "and paths exist under MCP_RESOURCES_DIR / resources root"
        )
    return rag_sources


def _docs_corpora(
    corpus_id: str = "", tool_name: str = MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL, action: str = "corpora"
) -> str:
    try:
        entries, version, manifest_path, root = load_manifest()
    except FileNotFoundError as exc:
        return _json(
            {
                "ok": False,
                "tool": tool_name,
                "action": action,
                "error": str(exc),
                "hint": "Set MCP_RESOURCES_DIR or place resources_manifest.json under the resources folder "
                "(exe directory/resources when packaged).",
                "resources_root": str(get_resources_root()),
                "manifest_path": str(get_resources_manifest_path()),
            }
        )
    except (ValueError, json.JSONDecodeError, TypeError, OSError) as exc:
        return _json(
            {
                "ok": False,
                "tool": tool_name,
                "action": action,
                "error": f"invalid manifest: {exc}",
                "manifest_path": str(get_resources_manifest_path()),
            }
        )

    want = (corpus_id or "").strip()
    corpora_out: List[Dict[str, Any]] = []
    default_ids: List[str] = []
    for entry in entries:
        rp = resolve_corpus_path(entry, root)
        if want and entry.id != want:
            continue
        d = entry.to_public_dict(rp)
        if entry.default_index:
            default_ids.append(entry.id)
        corpora_out.append(d)

    if want and not corpora_out:
        return _json(
            {
                "ok": False,
                "tool": tool_name,
                "action": action,
                "error": f"unknown corpus_id: {want}",
                "resources_root": str(root),
            }
        )

    return _json(
        {
            "ok": True,
            "tool": tool_name,
            "action": action,
            "resources_root": str(root),
            "manifest_path": str(manifest_path),
            "manifest_version": version,
            "default_index_corpora_ids": default_ids,
            "corpora": corpora_out,
        }
    )


def _load_docs_index(
    *,
    tool_name: str,
    action: str,
    index_path: str,
    sources: Optional[List[str]],
    rebuild_index: bool,
    extensions_csv: str = "",
    chunk_size: int = 900,
    overlap: int = 120,
    max_file_size_mb: float = 8.0,
    min_chunk_chars: int = 60,
    max_files: int = 0,
    max_chunks: int = 0,
    lexical_only: bool = False,
) -> tuple[Optional[Any], Optional[Any], Optional[str], Optional[List[str]], Optional[bool], Optional[str]]:
    try:
        rag = _get_rag_module()
        index_file = _resolve_rag_index_path(index_path)
        index_file.parent.mkdir(parents=True, exist_ok=True)
        eff_mc = effective_rag_max_chunks(max_chunks)
        eff_lex = effective_rag_lexical_only(lexical_only)
        mc_arg = eff_mc if eff_mc > 0 else None
        try:
            rag_sources = _prepare_rag_sources(rag, sources)
        except FileNotFoundError as exc:
            return None, None, None, None, None, _json(
                {
                    "ok": False,
                    "tool": tool_name,
                    "action": action,
                    "error": str(exc),
                    "hint": (
                        f"Run {MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL}(action=\"corpora\") "
                        "or set MCP_RESOURCES_DIR and add resources_manifest.json."
                    ),
                    "manifest_path": str(get_resources_manifest_path()),
                }
            )
        except (ValueError, RuntimeError) as exc:
            return None, None, None, None, None, _json(
                {"ok": False, "tool": tool_name, "action": action, "error": str(exc)}
            )

        rag_extensions = (
            {x.strip().lower() for x in extensions_csv.split(",") if x.strip()}
            if extensions_csv.strip()
            else set(rag.DEFAULT_EXTENSIONS)
        )

        max_load = get_rag_max_index_load_bytes()
        if (not rebuild_index) and max_load > 0 and index_file.exists():
            try:
                if index_file.stat().st_size > max_load:
                    return None, None, None, None, None, _json(
                        {
                            "ok": False,
                            "tool": tool_name,
                            "action": action,
                            "error": (
                                f"index file exceeds MCP_RAG_MAX_INDEX_LOAD_MB "
                                f"({index_file.stat().st_size} bytes > {max_load} bytes): {index_file}"
                            ),
                            "hint": "Raise the limit, delete the index to rebuild with tighter caps "
                            "(MCP_RAG_MAX_CHUNKS / max_chunks, MCP_RAG_LEXICAL_ONLY), "
                            "or set MCP_RAG_MAX_INDEX_LOAD_MB=0 to disable this guard.",
                        }
                    )
            except OSError:
                pass

        rebuilt = False
        if rebuild_index or (not index_file.exists()):
            rag.build_index(
                sources=rag_sources,
                index_path=str(index_file),
                chunk_size=chunk_size,
                overlap=overlap,
                extensions=rag_extensions,
                max_file_size_mb=max_file_size_mb,
                min_chunk_chars=min_chunk_chars,
                max_files=(max_files if max_files > 0 else None),
                path_relativize_to=get_resources_root(),
                max_chunks=mc_arg,
                lexical_only=eff_lex,
            )
            rebuilt = True

        index = rag.load_index(str(index_file))
        return rag, index, str(index_file), rag_sources, rebuilt, None
    except Exception as exc:
        return None, None, None, None, None, _json(
            {"ok": False, "tool": tool_name, "action": action, "error": str(exc)}
        )


def _docs_search(
    *,
    query: str,
    top_k: int = 5,
    path_contains: str = "",
    rebuild_index: bool = False,
    index_path: str = RAG_INDEX_PATH,
    sources: Optional[List[str]] = None,
    extensions_csv: str = "",
    chunk_size: int = 900,
    overlap: int = 120,
    max_file_size_mb: float = 8.0,
    min_chunk_chars: int = 60,
    max_files: int = 0,
    max_chunks: int = 0,
    lexical_only: bool = False,
    tool_name: str = MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL,
    action: str = "search",
) -> str:
    query_text = (query or "").strip()
    if not query_text:
        return _json({"ok": False, "tool": tool_name, "action": action, "error": "query is required"})

    eff_mc = effective_rag_max_chunks(max_chunks)
    eff_lex = effective_rag_lexical_only(lexical_only)

    rag, index, index_file, rag_sources, rebuilt, error = _load_docs_index(
        tool_name=tool_name,
        action=action,
        index_path=index_path,
        sources=sources,
        rebuild_index=rebuild_index,
        extensions_csv=extensions_csv,
        chunk_size=chunk_size,
        overlap=overlap,
        max_file_size_mb=max_file_size_mb,
        min_chunk_chars=min_chunk_chars,
        max_files=max_files,
        max_chunks=max_chunks,
        lexical_only=lexical_only,
    )
    if error:
        return error

    results = rag.search_index(
        index=index,
        query=query_text,
        top_k=max(1, int(top_k)),
        path_contains=path_contains.strip() or None,
    )
    return _json(
        {
            "ok": True,
            "tool": tool_name,
            "action": action,
            "query": query_text,
            "top_k": max(1, int(top_k)),
            "path_contains": path_contains,
            "index_path": index_file,
            "sources_used": rag_sources,
            "index_rebuilt": rebuilt,
            "num_docs": int(index.get("num_docs", 0)),
            "num_chunks": int(index.get("num_chunks", 0)),
            "results": results,
            "rag_limits": {
                "max_chunks_effective": eff_mc if eff_mc > 0 else None,
                "lexical_only": eff_lex,
                "retrieval_mode": str((index.get("retrieval") or {}).get("mode", "")),
            },
        }
    )


def _docs_list(
    *,
    keyword: str = "",
    limit: int = 30,
    index_path: str = RAG_INDEX_PATH,
    sources: Optional[List[str]] = None,
    rebuild_index: bool = False,
    max_chunks: int = 0,
    lexical_only: bool = False,
    tool_name: str = MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL,
    action: str = "list",
) -> str:
    _rag, index, index_file, _rag_sources, _rebuilt, error = _load_docs_index(
        tool_name=tool_name,
        action=action,
        index_path=index_path,
        sources=sources,
        rebuild_index=rebuild_index,
        max_chunks=max_chunks,
        lexical_only=lexical_only,
    )
    if error:
        return error

    docs = list(index.get("docs", []))
    kw = (keyword or "").strip().lower()
    out: List[Dict[str, Any]] = []
    for d in docs:
        path = str(d.get("path", ""))
        title = str(d.get("title", ""))
        if kw and kw not in path.lower() and kw not in title.lower():
            continue
        meta = dict(d.get("metadata", {}))
        out.append({"path": path, "title": title, "source_type": meta.get("source_type", ""), "metadata": meta})
        if len(out) >= max(1, int(limit)):
            break
    return _json(
        {"ok": True, "tool": tool_name, "action": action, "total": len(out), "docs": out, "index_path": index_file}
    )


def _docs_explain(
    *,
    model_name: str,
    detail_level: str = "normal",
    top_k: int = 5,
    index_path: str = RAG_INDEX_PATH,
    sources: Optional[List[str]] = None,
    max_chunks: int = 0,
    lexical_only: bool = False,
    tool_name: str = MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL,
    action: str = "explain",
) -> str:
    if not (model_name or "").strip():
        return _json({"ok": False, "tool": tool_name, "action": action, "error": "model_name is required"})

    search_ret = json.loads(
        _docs_search(
            query=model_name,
            top_k=max(1, int(top_k)),
            index_path=index_path,
            sources=sources,
            max_chunks=max_chunks,
            lexical_only=lexical_only,
            tool_name=tool_name,
            action=action,
        )
    )
    if not search_ret.get("ok"):
        return _json(
            {"ok": False, "tool": tool_name, "action": action, "error": search_ret.get("error", "search failed")}
        )
    refs = list(search_ret.get("results", []))
    snippets = [str(x.get("snippet", "")) for x in refs if str(x.get("snippet", "")).strip()]
    joined = " ".join(snippets).strip()
    cap = 220 if detail_level == "brief" else (520 if detail_level == "normal" else 900)
    principle = joined[:cap] if joined else f"No strong evidence snippets found for {model_name}."
    return _json(
        {
            "ok": True,
            "tool": tool_name,
            "action": action,
            "model_name": model_name,
            "detail_level": detail_level,
            "principle": principle,
            "references": [{"path": x.get("path", ""), "title": x.get("title", ""), "score": x.get("score", 0)} for x in refs],
        }
    )


@mcp.tool()
def mworks_sysplorer_resources_retrieval(
    action: str,
    query: str = "",
    model_name: str = "",
    corpus_id: str = "",
    keyword: str = "",
    limit: int = 30,
    top_k: int = 5,
    detail_level: str = "normal",
    path_contains: str = "",
    rebuild_index: bool = False,
    index_path: str = RAG_INDEX_PATH,
    sources: Optional[List[str]] = None,
    extensions_csv: str = "",
    chunk_size: int = 900,
    overlap: int = 120,
    max_file_size_mb: float = 8.0,
    min_chunk_chars: int = 60,
    max_files: int = 0,
    max_chunks: int = 0,
    lexical_only: bool = False,
) -> str:
    """Unified Sysplorer resources retrieval: corpora | search | list | explain."""
    action_norm = (action or "").strip().lower()
    if action_norm == "corpora":
        return _docs_corpora(
            corpus_id=corpus_id, tool_name=MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL, action=action_norm
        )
    if action_norm == "search":
        return _docs_search(
            query=query,
            top_k=top_k,
            path_contains=path_contains,
            rebuild_index=rebuild_index,
            index_path=index_path,
            sources=sources,
            extensions_csv=extensions_csv,
            chunk_size=chunk_size,
            overlap=overlap,
            max_file_size_mb=max_file_size_mb,
            min_chunk_chars=min_chunk_chars,
            max_files=max_files,
            max_chunks=max_chunks,
            lexical_only=lexical_only,
            tool_name=MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL,
            action=action_norm,
        )
    if action_norm == "list":
        return _docs_list(
            keyword=keyword,
            limit=limit,
            index_path=index_path,
            sources=sources,
            rebuild_index=rebuild_index,
            max_chunks=max_chunks,
            lexical_only=lexical_only,
            tool_name=MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL,
            action=action_norm,
        )
    if action_norm == "explain":
        return _docs_explain(
            model_name=model_name,
            detail_level=detail_level,
            top_k=top_k,
            index_path=index_path,
            sources=sources,
            max_chunks=max_chunks,
            lexical_only=lexical_only,
            tool_name=MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL,
            action=action_norm,
        )
    return _json(
        {
            "ok": False,
            "tool": MWORKS_SYSPLORER_RESOURCES_RETRIEVAL_TOOL,
            "action": action_norm,
            "error": 'unsupported action (use "corpora", "search", "list", or "explain")',
        }
    )
