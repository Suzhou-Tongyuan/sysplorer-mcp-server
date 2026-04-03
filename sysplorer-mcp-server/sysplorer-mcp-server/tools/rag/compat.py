"""Compatibility helpers for legacy modelica doc rag entry points."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Iterable, Optional

from .adapters import config_from_legacy_args, resolve_question
from .contracts import Document, RAGConfig
from .service import RAGService, to_document


_DEFAULT_SERVICE: Optional[RAGService] = None


def get_service(*, reset: bool = False, config: Optional[RAGConfig] = None) -> RAGService:
    """Get singleton service used by legacy compatibility APIs."""
    global _DEFAULT_SERVICE
    if reset or _DEFAULT_SERVICE is None:
        _DEFAULT_SERVICE = RAGService(config=config)
    return _DEFAULT_SERVICE


def init_service(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Legacy-friendly initializer accepting broad argument shapes."""
    cfg = config_from_legacy_args(args, kwargs)
    get_service(reset=True, config=cfg)
    return {"ok": True, "status": "initialized", "mode": "skeleton"}


def build_index(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Legacy-friendly index build wrapper."""
    service = get_service()

    docs_payload = kwargs.pop("documents", None)
    docs: Optional[Iterable[Document]] = None
    if isinstance(docs_payload, list):
        docs = [to_document(item) if isinstance(item, dict) else item for item in docs_payload]

    result = service.build_index(documents=docs, **kwargs)
    result["args"] = list(args)
    return result


def query(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Legacy-friendly query wrapper with permissive signature."""
    service = get_service()

    question = resolve_question(args, kwargs)
    response = service.query(question=question, top_k=kwargs.pop("top_k", None), **kwargs)
    result = asdict(response)
    result["status"] = "skeleton"
    return result


def health_check(*_: Any, **__: Any) -> Dict[str, Any]:
    """Legacy-friendly health endpoint."""
    return get_service().health_check()
