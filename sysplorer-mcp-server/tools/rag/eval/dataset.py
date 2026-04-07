"""Evaluation dataset utilities for RAG regression."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List


def load_samples(path: str) -> List[Dict[str, object]]:
    p = Path(path)
    rows: List[Dict[str, object]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def iter_samples(path: str) -> Iterable[Dict[str, object]]:
    for row in load_samples(path):
        yield row


__all__ = ["load_samples", "iter_samples"]

