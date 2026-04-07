"""Helpers for VuePress-like doc artifacts."""

from __future__ import annotations

from pathlib import Path


def is_aggregate_doc(path: str) -> bool:
    p = path.lower()
    return any(marker in p for marker in ("page-data-list.json", "/404.html", "\\404.html"))


def source_type(path: str) -> str:
    p = Path(path).as_posix().lower()
    if ".vuepress/" in p or "page-data" in p:
        return "front_end_doc"
    return "raw_file"


__all__ = ["is_aggregate_doc", "source_type"]

