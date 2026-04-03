"""Raw file loader for local documentation/model sources."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .normalizer import normalize_text


ENCODINGS = ("utf-8-sig", "utf-8", "gb18030", "gbk", "latin-1")


def read_text_with_fallback(path: Path) -> str:
    for enc in ENCODINGS:
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_bytes().decode("utf-8", errors="ignore")


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt", ".mo", ".rst", ".html", ".htm", ".yaml", ".yml"}:
        return normalize_text(read_text_with_fallback(path))
    if suffix == ".json":
        raw = read_text_with_fallback(path)
        try:
            obj = json.loads(raw)
            return normalize_text(json.dumps(obj, ensure_ascii=False, indent=2))
        except json.JSONDecodeError:
            return normalize_text(raw)
    return ""


def iter_source_files(
    sources: Iterable[str],
    extensions: set[str],
    max_file_size_mb: float = 8.0,
) -> Iterable[Path]:
    max_bytes = int(max_file_size_mb * 1024 * 1024)
    for src in sources:
        p = Path(src)
        if not p.exists():
            continue
        if p.is_file():
            try:
                if p.stat().st_size <= max_bytes:
                    yield p
            except OSError:
                pass
            continue
        for file in p.rglob("*"):
            if not file.is_file():
                continue
            if file.suffix.lower() not in extensions:
                continue
            try:
                if file.stat().st_size <= max_bytes:
                    yield file
            except OSError:
                continue


__all__ = ["extract_text", "iter_source_files", "read_text_with_fallback"]

