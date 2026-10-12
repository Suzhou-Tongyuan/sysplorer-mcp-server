#!/usr/bin/env python3
"""Extract bounded literal-anchor evidence from large debug artifacts."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import time
from typing import Iterable


DEFAULT_EXTENSIONS = {".rmf", ".xml", ".mo", ".c", ".h", ".log", ".sync", ".txt"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search large Sysplorer artifacts without loading them into model context."
    )
    parser.add_argument("paths", nargs="+", help="Files or directories to scan")
    parser.add_argument("-a", "--anchor", action="append", default=[], help="Literal search anchor")
    parser.add_argument(
        "--anchor-file",
        action="append",
        default=[],
        help="UTF-8 text file containing one literal anchor per line",
    )
    parser.add_argument("--ignore-case", action="store_true", help="ASCII case-insensitive matching")
    parser.add_argument("--context-bytes", type=int, default=2048)
    parser.add_argument("--chunk-bytes", type=int, default=1024 * 1024)
    parser.add_argument("--max-files", type=int, default=8)
    parser.add_argument("--max-hits-per-file", type=int, default=5)
    parser.add_argument("--max-output-chars", type=int, default=20000)
    parser.add_argument("--max-scan-seconds", type=float, default=30.0)
    parser.add_argument(
        "--extensions",
        default=",".join(sorted(DEFAULT_EXTENSIONS)),
        help="Comma-separated extensions used when a directory is supplied",
    )
    args = parser.parse_args()

    if not 64 <= args.context_bytes <= 65536:
        parser.error("--context-bytes must be between 64 and 65536")
    if not 4096 <= args.chunk_bytes <= 16 * 1024 * 1024:
        parser.error("--chunk-bytes must be between 4096 and 16777216")
    if not 1 <= args.max_files <= 100:
        parser.error("--max-files must be between 1 and 100")
    if not 1 <= args.max_hits_per_file <= 100:
        parser.error("--max-hits-per-file must be between 1 and 100")
    if not 1000 <= args.max_output_chars <= 1_000_000:
        parser.error("--max-output-chars must be between 1000 and 1000000")
    if not 0.1 <= args.max_scan_seconds <= 3600:
        parser.error("--max-scan-seconds must be between 0.1 and 3600")
    for anchor_file in args.anchor_file:
        try:
            lines = Path(anchor_file).read_text(encoding="utf-8-sig").splitlines()
        except OSError as exc:
            parser.error(f"cannot read --anchor-file {anchor_file}: {exc}")
        args.anchor.extend(line for line in lines if line)
    if not args.anchor:
        parser.error("provide at least one --anchor or --anchor-file")
    if len(args.anchor) > 64:
        parser.error("at most 64 anchors are allowed")
    if any(not anchor for anchor in args.anchor):
        parser.error("anchors must not be empty")
    return args


def discover_files(raw_paths: Iterable[str], extensions: set[str], max_files: int) -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    warnings: list[str] = []
    seen: set[str] = set()

    for raw in raw_paths:
        path = Path(raw).expanduser()
        candidates: Iterable[Path]
        if path.is_dir():
            candidates = (p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in extensions)
        elif path.is_file():
            candidates = [path]
        else:
            warnings.append(f"path not found: {path}")
            continue

        for candidate in candidates:
            try:
                key = str(candidate.resolve()).lower()
            except OSError:
                key = str(candidate.absolute()).lower()
            if key in seen:
                continue
            seen.add(key)
            files.append(candidate)
            if len(files) >= max_files:
                warnings.append(f"file limit reached: {max_files}")
                return files, warnings
    return files, warnings


def encoded_patterns(anchors: list[str], ignore_case: bool) -> list[tuple[str, bytes]]:
    patterns: list[tuple[str, bytes]] = []
    seen: set[tuple[str, bytes]] = set()
    for anchor in anchors:
        for encoding in ("utf-8", "gb18030", "utf-16-le", "utf-16-be"):
            try:
                value = anchor.encode(encoding)
            except UnicodeEncodeError:
                continue
            if ignore_case:
                value = value.lower()
            item = (anchor, value)
            if value and item not in seen:
                seen.add(item)
                patterns.append(item)
    return patterns


def find_offsets(
    path: Path,
    patterns: list[tuple[str, bytes]],
    ignore_case: bool,
    chunk_bytes: int,
    max_hits: int,
    deadline: float,
) -> tuple[list[tuple[int, str]], bool, int, int]:
    max_pattern = max(len(value) for _, value in patterns)
    overlap = max_pattern - 1
    carry = b""
    absolute_read = 0
    hits: list[tuple[int, str]] = []
    seen_offsets: set[tuple[int, str]] = set()
    timed_out = False
    bytes_scanned = 0

    with path.open("rb") as stream:
        logical_size = stream.seek(0, os.SEEK_END)
        stream.seek(0)
        bom = stream.read(2)
        utf16 = {b"\xff\xfe": "utf-16-le", b"\xfe\xff": "utf-16-be"}.get(bom)
        if utf16:
            patterns = [(anchor, value) for anchor, value in patterns
                        if value == (anchor.encode(utf16).lower() if ignore_case else anchor.encode(utf16))]
        stream.seek(0)
        while len(hits) < max_hits:
            if time.monotonic() >= deadline:
                timed_out = True
                break
            block = stream.read(chunk_bytes)
            if not block:
                break
            bytes_scanned += len(block)
            data = carry + block
            searchable = data.lower() if ignore_case else data
            base_offset = absolute_read - len(carry)
            for anchor, pattern in patterns:
                start = 0
                while len(hits) < max_hits:
                    index = searchable.find(pattern, start)
                    if index < 0:
                        break
                    absolute_offset = base_offset + index
                    if utf16 and absolute_offset % 2:
                        start = index + 1
                        continue
                    key = (absolute_offset, anchor)
                    if key not in seen_offsets:
                        seen_offsets.add(key)
                        hits.append(key)
                    start = index + max(1, len(pattern))
            absolute_read += len(block)
            carry = data[-overlap:] if overlap else b""
    hits.sort(key=lambda item: (item[0], item[1]))
    return hits[:max_hits], timed_out, bytes_scanned, logical_size


def decode_snippet(data: bytes) -> tuple[str, str]:
    if data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff"):
        try:
            return data.decode("utf-16"), "utf-16"
        except UnicodeDecodeError:
            pass
    for encoding in ("utf-8", "gb18030"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace"), "utf-8-replacement"


def read_context(path: Path, offset: int, anchor: str, context_bytes: int) -> tuple[str, str, int]:
    anchor_bytes = max(len(value) for _, value in encoded_patterns([anchor], False))
    start = max(0, offset - context_bytes)
    length = context_bytes * 2 + anchor_bytes
    with path.open("rb") as stream:
        bom = stream.read(2)
        encoding = {b"\xff\xfe": "utf-16-le", b"\xfe\xff": "utf-16-be"}.get(bom)
        if encoding is None:
            # A BOM-less UTF-16 hit can be identified by the matched literal.
            stream.seek(offset)
            probe = stream.read(anchor_bytes)
            for candidate in ("utf-16-le", "utf-16-be"):
                if probe.startswith(anchor.encode(candidate)) and b"\x00" in anchor.encode(candidate):
                    encoding = candidate
                    break
        if encoding:
            start -= start % 2
            length += length % 2
        stream.seek(start)
        data = stream.read(length)
    if encoding:
        text = data.decode(encoding, errors="replace").lstrip("\ufeff")
    else:
        text, encoding = decode_snippet(data)
    return text.replace("\x00", "\\0"), encoding, start


def main() -> int:
    args = parse_args()
    extensions = {value.strip().lower() for value in args.extensions.split(",") if value.strip()}
    extensions = {value if value.startswith(".") else f".{value}" for value in extensions}
    files, warnings = discover_files(args.paths, extensions, args.max_files)
    patterns = encoded_patterns(args.anchor, args.ignore_case)
    deadline = time.monotonic() + args.max_scan_seconds
    records: list[dict[str, object]] = []
    scanned_bytes = 0
    truncated = False

    for path in files:
        if time.monotonic() >= deadline:
            warnings.append("global scan timeout reached")
            truncated = True
            break
        try:
            stat = path.stat()
            offsets, timed_out, file_bytes_scanned, logical_size = find_offsets(
                path,
                patterns,
                args.ignore_case,
                args.chunk_bytes,
                args.max_hits_per_file,
                deadline,
            )
            scanned_bytes += file_bytes_scanned
            if timed_out:
                warnings.append(f"scan timeout while reading: {path}")
                truncated = True
            for offset, anchor in offsets:
                snippet, encoding, context_start = read_context(path, offset, anchor, args.context_bytes)
                record = {
                    "path": str(path.resolve()),
                    "size_bytes": logical_size,
                    "mtime_ns": stat.st_mtime_ns,
                    "anchor": anchor,
                    "byte_offset": offset,
                    "context_start_offset": context_start,
                    "encoding": encoding,
                    "snippet": snippet,
                }
                trial = records + [record]
                envelope = {"ok": True, "records": trial, "warnings": warnings, "truncated": truncated}
                if len(json.dumps(envelope, ensure_ascii=False)) > args.max_output_chars:
                    warnings.append(f"output character limit reached: {args.max_output_chars}")
                    truncated = True
                    break
                records.append(record)
            if truncated and warnings and warnings[-1].startswith("output character limit"):
                break
        except (OSError, ValueError) as exc:
            warnings.append(f"failed to scan {path}: {exc}")

    result = {
        "ok": True,
        "files_considered": len(files),
        "scanned_file_bytes": scanned_bytes,
        "anchors": args.anchor,
        "records": records,
        "warnings": warnings,
        "truncated": truncated,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if len(rendered) > args.max_output_chars:
        result["records"] = []
        result["warnings"].append("metadata exceeded output limit; records omitted")
        result["truncated"] = True
        rendered = json.dumps(result, ensure_ascii=False, indent=2)
    sys.stdout.write(rendered + os.linesep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
