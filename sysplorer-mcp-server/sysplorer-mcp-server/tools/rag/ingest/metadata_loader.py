"""Metadata JSON adapters for RAG ingestion."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from tools.rag.path_utils import posix_relative_to_anchor

from .raw_loader import read_text_with_fallback


@dataclass
class RawDocument:
    path: str
    title: str
    text: str
    metadata: Dict[str, Any]


def metadata_docs_from_json(path: Path, relativize_to: Path | None = None) -> List[RawDocument]:
    try:
        data = json.loads(read_text_with_fallback(path))
    except Exception:
        return []

    docs: List[RawDocument] = []
    base_path = posix_relative_to_anchor(path, relativize_to)
    components = data.get("components", [])
    for comp in components:
        name = str(comp.get("name", "Unknown"))
        mo_file = str(comp.get("mo_file", ""))
        lines = [
            f"Component: {name}",
            f"Type: {comp.get('type', '')}",
            f"Description: {comp.get('description', '')}",
            f"ModelicaFile: {mo_file}",
        ]
        params = comp.get("parameters", [])
        if isinstance(params, list):
            lines.append("Parameters:")
            for p in params:
                lines.append(
                    f"- {p.get('name', '')} ({p.get('type', '')}, default={p.get('default', '')}, unit={p.get('unit', '')}): {p.get('description', '')}"
                )
        docs.append(
            RawDocument(
                path=f"{base_path}::{name}",
                title=f"metadata:{name}",
                text="\n".join(lines),
                metadata={"kind": "metadata_component", "component": name, "mo_file": mo_file},
            )
        )

    if not docs:
        docs.append(
            RawDocument(
                path=base_path,
                title=path.name,
                text=json.dumps(data, ensure_ascii=False, indent=2),
                metadata={"kind": "metadata_json"},
            )
        )
    return docs


__all__ = ["RawDocument", "metadata_docs_from_json"]

