#!/usr/bin/env python3
"""Return bounded matches from the active Sysplorer installation help."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
from typing import Any


CORPUS_DIRS = {"diagnostic": "FAQ", "topic": "DevelopingModels"}
DIAGNOSTIC_KINDS = {
    "error": ("Error", "Error"),
    "warning": ("Warning", "Warning"),
    "message": ("Message", "Message"),
}


def index_path(root: Path) -> Path:
    return root / "pageData" / "page-data-list.json"


def infer_installation_root(root: Path) -> Path | None:
    for candidate in (root, *root.parents):
        if re.fullmatch(r"Sysplorer\s+.+", candidate.name, flags=re.IGNORECASE):
            return candidate
    return None


def resolve_corpus(candidate: Path, corpus: str) -> tuple[Path, Path | None] | None:
    """Resolve an installation, Docs directory, or direct help corpus root."""
    try:
        directory = CORPUS_DIRS[corpus]
        if index_path(candidate).is_file():
            sibling = candidate.parent / directory
            if candidate.name.casefold() != directory.casefold() and index_path(sibling).is_file():
                return sibling, infer_installation_root(sibling)
            if candidate.name.casefold() != directory.casefold():
                return None
            return candidate, infer_installation_root(candidate)
        for root in (candidate / "Docs" / directory, candidate / directory):
            if index_path(root).is_file():
                installation = candidate if root == candidate / "Docs" / directory else candidate.parent
                return root, installation
    except OSError as exc:
        raise SystemExit(f"cannot inspect Sysplorer help root {candidate}: {exc}") from exc
    return None


def discover_root(explicit: str | None, corpus: str) -> tuple[Path, Path | None]:
    preferred: list[Path] = []
    if explicit:
        preferred.append(Path(explicit))
    if os.environ.get("SYSPLORER_DOCS_ROOT"):
        preferred.append(Path(os.environ["SYSPLORER_DOCS_ROOT"]))
    if os.environ.get("MWORKS_INSTALL_DIR"):
        preferred.append(Path(os.environ["MWORKS_INSTALL_DIR"]))
    for candidate in preferred:
        resolved = resolve_corpus(candidate, corpus)
        if resolved is not None:
            root, installation = resolved
            return root.resolve(), installation.resolve() if installation else None
    if preferred:
        directory = CORPUS_DIRS[corpus]
        raise SystemExit(
            "specified Sysplorer installation/help root does not contain "
            f"Docs/{directory}/pageData/page-data-list.json"
        )

    program_files = Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
    mworks = program_files / "MWORKS"
    discovered: list[tuple[Path, Path | None]] = []
    if mworks.is_dir():
        for installation in sorted(mworks.glob("Sysplorer *")):
            resolved = resolve_corpus(installation, corpus)
            if resolved is not None:
                discovered.append((resolved[0].resolve(), installation.resolve()))
    if len(discovered) == 1:
        return discovered[0]
    if len(discovered) > 1:
        rendered = "\n  ".join(str(path) for path, _ in discovered)
        raise SystemExit(
            "multiple Sysplorer help versions found; pass the current "
            f"GetInstallationDirectory() value with --root:\n  {rendered}"
        )
    raise SystemExit("Sysplorer help root not found; pass --root or set SYSPLORER_DOCS_ROOT")


def product_version(installation: Path | None, help_root: Path) -> str:
    for candidate in (installation, help_root, *help_root.parents):
        if candidate is None:
            continue
        match = re.fullmatch(r"Sysplorer\s+(.+)", candidate.name, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return "unknown"


def excerpt(content: str, terms: list[str], context: int) -> str:
    lower = content.casefold()
    offsets = [lower.find(term.casefold()) for term in terms]
    offsets = [offset for offset in offsets if offset >= 0]
    start = max(0, (min(offsets) if offsets else 0) - context)
    end = min(len(content), start + context * 2)
    return ("..." if start else "") + content[start:end].strip() + ("..." if end < len(content) else "")


def load_pages(path: Path) -> list[dict[str, Any]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
    except OSError as exc:
        raise SystemExit(f"cannot read Sysplorer help index {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid Sysplorer help index JSON {path}: {exc}") from exc

    if isinstance(raw, list):
        pages = raw
    elif isinstance(raw, dict):
        pages = next(
            (raw[key] for key in ("pages", "pageData", "items", "data") if isinstance(raw.get(key), list)),
            None,
        )
    else:
        pages = None
    if pages is None or any(not isinstance(page, dict) for page in pages):
        raise SystemExit(
            "unsupported Sysplorer help index schema: expected a page list or "
            "an object containing pages/pageData/items/data"
        )
    return pages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="Topic terms, or diagnostic context terms")
    parser.add_argument("--root")
    parser.add_argument("--error-code", help="Exact numeric product diagnostic candidate")
    parser.add_argument(
        "--kind",
        choices=("auto", *DIAGNOSTIC_KINDS),
        default="auto",
        help="Product diagnostic category; auto returns every exact category candidate",
    )
    parser.add_argument("--path", help="Optional case-insensitive path substring for topic queries")
    parser.add_argument("--max-records", type=int, default=5)
    parser.add_argument("--context-chars", type=int, default=700)
    parser.add_argument("--max-output-chars", type=int, default=12000)
    args = parser.parse_args()
    if not args.query and not args.error_code:
        parser.error("provide at least one query term or --error-code")
    if args.kind != "auto" and not args.error_code:
        parser.error("--kind requires --error-code")
    if not 1 <= args.max_records <= 20:
        parser.error("--max-records must be between 1 and 20")
    if not 100 <= args.context_chars <= 5000:
        parser.error("--context-chars must be between 100 and 5000")
    if not 1000 <= args.max_output_chars <= 100000:
        parser.error("--max-output-chars must be between 1000 and 100000")
    if args.error_code and not re.fullmatch(r"\d{1,8}", args.error_code):
        parser.error("--error-code must contain between one and eight digits")
    return args


def page_text(page: dict[str, Any]) -> tuple[str, str, str]:
    path = str(page.get("path", ""))
    raw_content = page.get("content", "")
    content = raw_content if isinstance(raw_content, str) else json.dumps(raw_content, ensure_ascii=False)
    return path, content, f"{page.get('title', '')}\n{path}\n{content}"


def diagnostic_kind(path: str, code: str) -> str | None:
    normalized = path.replace("\\", "/")
    for kind, (folder, prefix) in DIAGNOSTIC_KINDS.items():
        suffix = f"/ErrorsReference/{folder}/{prefix}{code}.html"
        if normalized.casefold().endswith(suffix.casefold()):
            return kind
    return None


def diagnostic_records(pages: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    terms = [value.casefold() for value in args.query]
    for page in pages:
        path, content, haystack = page_text(page)
        kind = diagnostic_kind(path, args.error_code)
        if kind is None or (args.kind != "auto" and kind != args.kind):
            continue
        folded = haystack.casefold()
        matched = [term for term in terms if term in folded]
        records.append(
            {
                "path": path,
                "title": page.get("title", ""),
                "kind": kind,
                "context_match": len(matched) == len(terms),
                "matched_terms": matched,
                "excerpt": excerpt(content, args.query or [args.error_code], args.context_chars),
            }
        )
    return sorted(records, key=lambda item: (not item["context_match"], item["kind"]))


def topic_records(pages: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    terms = [value.casefold() for value in args.query]
    path_filter = args.path.casefold() if args.path else None
    records: list[dict[str, Any]] = []
    for page in pages:
        path, content, haystack = page_text(page)
        if path_filter and path_filter not in path.casefold():
            continue
        if not all(term in haystack.casefold() for term in terms):
            continue
        records.append(
            {"path": path, "title": page.get("title", ""), "excerpt": excerpt(content, args.query, args.context_chars)}
        )
    return records


def bounded_result(result: dict[str, Any], max_records: int, max_chars: int) -> str:
    records = result["records"]
    result["truncated"] = len(records) > max_records
    del records[max_records:]
    output = json.dumps(result, ensure_ascii=True, indent=2) + "\n"
    while records and len(output) > max_chars:
        records.pop()
        result["truncated"] = True
        output = json.dumps(result, ensure_ascii=True, indent=2) + "\n"
    if len(output) > max_chars:
        output = json.dumps(result, ensure_ascii=True, separators=(",", ":")) + "\n"
    if len(output) > max_chars:
        raise SystemExit("--max-output-chars is too small for the help query metadata")
    return output


def main() -> int:
    args = parse_args()
    mode = "diagnostic" if args.error_code else "topic"
    root, installation = discover_root(args.root, mode)
    path = index_path(root)
    pages = load_pages(path)
    records = diagnostic_records(pages, args) if args.error_code else topic_records(pages, args)
    context_conflict = bool(
        args.error_code and args.query and records and not any(record["context_match"] for record in records)
    )
    result = {
        "ok": True,
        "status": "documented" if records else ("not_documented" if args.error_code else "no_match"),
        "mode": mode,
        "product_version": product_version(installation, root),
        "installation_root": str(installation) if installation else "",
        "help_root": str(root),
        "index": str(path),
        "query": args.query,
        "error_code": args.error_code,
        "kind": args.kind if args.error_code else None,
        "context_conflict": context_conflict,
        "records": records,
        "truncated": False,
    }
    print(bounded_result(result, args.max_records, args.max_output_chars), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
