"""Portable path strings for RAG indexes (relative to resources root when possible)."""

from __future__ import annotations

from pathlib import Path


def posix_relative_to_anchor(path: Path, anchor: Path | None) -> str:
    """Return posix path relative to anchor when under anchor; else absolute posix (resolved)."""
    rp = path.resolve()
    if anchor is None:
        return rp.as_posix()
    try:
        return rp.relative_to(anchor.resolve()).as_posix()
    except ValueError:
        return rp.as_posix()


__all__ = ["posix_relative_to_anchor"]
