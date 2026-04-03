"""Rebuild resources/indexes/*.json from resources/resources_manifest.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_RES = _REPO / "resources"
sys.path.insert(0, str(_REPO / "sysplorer-mcp-server"))

from tools.rag.bm25 import bm25_build_index  # noqa: E402


def main() -> int:
    manifest_path = _RES / "resources_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for cat in manifest["resource_categories"]:
        cid = cat["id"]
        rel = cat["path"].replace("\\", "/").rstrip("/")
        corp = (_RES / rel).resolve()
        if not corp.is_dir():
            print(f"SKIP {cid}: not a directory: {corp}")
            continue
        idx_rel = cat["index_file"].replace("\\", "/")
        idx = (_RES / idx_rel).resolve()
        exts = {x.lower() for x in cat.get("supported_extensions", [".md"])}
        print(f"Building {cid} -> {idx.name} ...")
        bm25_build_index(
            sources=[str(corp)],
            index_path=str(idx),
            chunk_size=900,
            overlap=120,
            extensions=exts,
            max_file_size_mb=8.0,
            min_chunk_chars=60,
            max_files=None,
            path_relativize_to=_RES,
        )
        data = json.loads(idx.read_text(encoding="utf-8"))
        print(f"  ok num_docs={data.get('num_docs')} num_chunks={data.get('num_chunks')}")
    print("All done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
