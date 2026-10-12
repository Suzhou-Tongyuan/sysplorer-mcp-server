#!/usr/bin/env python3
"""Content-addressed checkpoints for a Sysplorer debug workspace."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any


MANIFEST_NAME = "debug-workspace-manifest.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def load_manifest(session_dir: Path) -> dict[str, Any]:
    path = session_dir / MANIFEST_NAME
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"manifest not found: {path}") from exc


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def normalize_files(workspace: Path, raw_files: list[str]) -> list[Path]:
    files: list[Path] = []
    seen: set[str] = set()
    for raw in raw_files:
        path = Path(raw)
        if not path.is_absolute():
            path = workspace / path
        path = path.resolve()
        if not inside(path, workspace):
            raise SystemExit(f"file is outside debug workspace: {path}")
        if path.exists() and not path.is_file():
            raise SystemExit(f"only files are supported: {path}")
        key = os.path.normcase(str(path))
        if key not in seen:
            seen.add(key)
            files.append(path)
    return files


def store_blob(session_dir: Path, path: Path, digest: str) -> None:
    target = session_dir / "blobs" / digest
    if target.exists():
        if not target.is_file() or sha256(target) != digest:
            raise RuntimeError(f"existing blob is corrupt: {digest}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".blob.", dir=target.parent)
    os.close(fd)
    try:
        shutil.copyfile(path, temp_name)
        if sha256(Path(temp_name)) != digest:
            raise RuntimeError(f"blob verification failed: {path}")
        os.replace(temp_name, target)
    except BaseException:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def make_checkpoint(
    manifest: dict[str, Any], session_dir: Path, label: str, files: list[Path]
) -> dict[str, Any]:
    if any(item["label"] == label for item in manifest["checkpoints"]):
        raise SystemExit(f"checkpoint label already exists: {label}")
    workspace = Path(manifest["workspace"])
    records: dict[str, Any] = {}
    for path in files:
        relative = path.relative_to(workspace).as_posix()
        if path.exists():
            digest = sha256(path)
            store_blob(session_dir, path, digest)
            records[relative] = {
                "exists": True,
                "sha256": digest,
                "size": path.stat().st_size,
            }
        else:
            records[relative] = {"exists": False, "sha256": None, "size": 0}
    checkpoint = {"label": label, "created_at": now(), "files": records}
    manifest["checkpoints"].append(checkpoint)
    manifest["tracked_files"] = sorted(set(manifest.get("tracked_files", [])) | set(records))
    return checkpoint


def command_start(args: argparse.Namespace) -> dict[str, Any]:
    workspace = Path(args.workspace).resolve()
    if not workspace.is_dir():
        raise SystemExit(f"workspace is not a directory: {workspace}")
    session_dir = Path(args.session_dir).resolve()
    session_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = session_dir / MANIFEST_NAME
    if manifest_path.exists() and not args.force:
        raise SystemExit(f"manifest already exists: {manifest_path}")
    files = normalize_files(workspace, args.files)
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "created_at": now(),
        "workspace": str(workspace),
        "session_dir": str(session_dir),
        "tracked_files": [],
        "checkpoints": [],
    }
    checkpoint = make_checkpoint(manifest, session_dir, "baseline", files)
    atomic_json(manifest_path, manifest)
    return {"ok": True, "manifest": str(manifest_path), "checkpoint": checkpoint}


def command_checkpoint(args: argparse.Namespace) -> dict[str, Any]:
    session_dir = Path(args.session_dir).resolve()
    manifest = load_manifest(session_dir)
    workspace = Path(manifest["workspace"])
    raw_files = args.files or manifest.get("tracked_files", [])
    files = normalize_files(workspace, raw_files)
    checkpoint = make_checkpoint(manifest, session_dir, args.label, files)
    atomic_json(session_dir / MANIFEST_NAME, manifest)
    return {"ok": True, "checkpoint": checkpoint}


def find_checkpoint(manifest: dict[str, Any], label: str) -> dict[str, Any]:
    for checkpoint in manifest["checkpoints"]:
        if checkpoint["label"] == label:
            return checkpoint
    raise SystemExit(f"checkpoint not found: {label}")


def atomic_restore(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    os.close(fd)
    try:
        shutil.copyfile(source, temp_name)
        os.replace(temp_name, target)
    except BaseException:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def command_restore(args: argparse.Namespace) -> dict[str, Any]:
    session_dir = Path(args.session_dir).resolve()
    manifest = load_manifest(session_dir)
    workspace = Path(manifest["workspace"]).resolve()
    checkpoint = find_checkpoint(manifest, args.label)
    actions: list[dict[str, Any]] = []
    plan = []
    for relative, record in checkpoint["files"].items():
        target = (workspace / relative).resolve()
        if not inside(target, workspace):
            raise SystemExit(f"unsafe manifest target: {target}")
        if inside(target, session_dir):
            raise SystemExit(f"refusing to restore session metadata: {target}")
        if target.exists() and not target.is_file():
            raise SystemExit(f"refusing to replace non-file: {target}")
        parent = target.parent
        while not parent.exists():
            parent = parent.parent
        if not parent.is_dir():
            raise SystemExit(f"target parent is not a directory: {parent}")
        action = "restore" if record["exists"] else "remove"
        actions.append({"path": str(target), "action": action})
        blob = None
        if record["exists"]:
            digest = record["sha256"]
            if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                raise SystemExit("invalid blob digest")
            blob = session_dir / "blobs" / record["sha256"]
            if not blob.is_file() or sha256(blob) != record["sha256"]:
                raise SystemExit(f"missing or corrupt blob: {record['sha256']}")
        plan.append((target, record, blob))
    # Complete preflight (including all blobs) before touching any target.
    if args.dry_run:
        return {"ok": True, "label": args.label, "dry_run": True, "actions": actions}

    recovery_dir = Path(tempfile.mkdtemp(prefix="restore-recovery-", dir=session_dir))
    before = []
    for index, (target, _, _) in enumerate(plan):
        backup = recovery_dir / str(index)
        digest = sha256(target) if target.is_file() else None
        if digest is not None:
            shutil.copyfile(target, backup)
            if sha256(backup) != digest:
                raise RuntimeError(f"concurrent change while snapshotting: {target}")
        before.append({"target": str(target), "backup": str(backup), "sha256": digest})
    atomic_json(recovery_dir / "recovery.json", {"files": before, "label": args.label})
    attempted = []
    try:
        for index, (target, record, blob) in enumerate(plan):
            current = sha256(target) if target.is_file() else None
            if current != before[index]["sha256"]:
                raise RuntimeError(f"concurrent change before restore: {target}")
            # Include this target even if verification fails after os.replace.
            attempted.append(index)
            if record["exists"]:
                atomic_restore(blob, target)
                if sha256(target) != record["sha256"]:
                    raise RuntimeError(f"restore verification failed: {target}")
            elif target.exists():
                target.unlink()
    except Exception as exc:
        compensation = []
        for index in reversed(attempted):
            target, _, _ = plan[index]
            prior = before[index]
            try:
                if prior["sha256"] is not None:
                    atomic_restore(Path(prior["backup"]), target)
                    if sha256(target) != prior["sha256"]:
                        raise RuntimeError("compensation hash mismatch")
                elif target.exists():
                    if not target.is_file():
                        raise RuntimeError("compensation target is not a file")
                    target.unlink()
                compensation.append({"path": str(target), "status": "restored"})
            except Exception as rollback_exc:
                compensation.append({"path": str(target), "status": "failed", "error": str(rollback_exc)})
        return {"ok": False, "label": args.label, "error": str(exc),
                "compensation": compensation,
                "compensation_complete": all(r["status"] == "restored" for r in compensation),
                "recovery_dir": str(recovery_dir), "actions": actions}
    for backup in recovery_dir.iterdir():
        backup.unlink()
    recovery_dir.rmdir()
    return {"ok": True, "label": args.label, "dry_run": args.dry_run, "actions": actions}


def command_status(args: argparse.Namespace) -> dict[str, Any]:
    session_dir = Path(args.session_dir).resolve()
    manifest = load_manifest(session_dir)
    workspace = Path(manifest["workspace"])
    checkpoint = find_checkpoint(manifest, args.label)
    files: dict[str, Any] = {}
    all_match = True
    for relative, expected in checkpoint["files"].items():
        target = workspace / relative
        exists = target.is_file()
        digest = sha256(target) if exists else None
        match = exists == expected["exists"] and digest == expected["sha256"]
        files[relative] = {"exists": exists, "sha256": digest, "match": match}
        all_match = all_match and match
    return {"ok": True, "label": args.label, "all_match": all_match, "files": files}


def command_finalize(args: argparse.Namespace) -> dict[str, Any]:
    session_dir = Path(args.session_dir).resolve()
    manifest = load_manifest(session_dir)
    keep = {"baseline"}
    if args.keep_label:
        find_checkpoint(manifest, args.keep_label)
        keep.add(args.keep_label)
    manifest["checkpoints"] = [c for c in manifest["checkpoints"] if c["label"] in keep]
    referenced = {
        record["sha256"]
        for checkpoint in manifest["checkpoints"]
        for record in checkpoint["files"].values()
        if record["exists"]
    }
    removed: list[str] = []
    blob_dir = session_dir / "blobs"
    if blob_dir.is_dir():
        for blob in blob_dir.iterdir():
            if blob.is_file() and blob.name not in referenced:
                removed.append(blob.name)
                if not args.dry_run:
                    blob.unlink()
    if not args.dry_run:
        manifest["finalized_at"] = now()
        atomic_json(session_dir / MANIFEST_NAME, manifest)
    return {"ok": True, "kept": sorted(keep), "removed_blobs": removed, "dry_run": args.dry_run}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start")
    start.add_argument("--session-dir", required=True)
    start.add_argument("--workspace", required=True)
    start.add_argument("--force", action="store_true")
    start.add_argument("files", nargs="+")
    start.set_defaults(func=command_start)

    checkpoint = sub.add_parser("checkpoint")
    checkpoint.add_argument("--session-dir", required=True)
    checkpoint.add_argument("--label", required=True)
    checkpoint.add_argument("files", nargs="*")
    checkpoint.set_defaults(func=command_checkpoint)

    restore = sub.add_parser("restore")
    restore.add_argument("--session-dir", required=True)
    restore.add_argument("--label", required=True)
    restore.add_argument("--dry-run", action="store_true")
    restore.set_defaults(func=command_restore)

    status = sub.add_parser("status")
    status.add_argument("--session-dir", required=True)
    status.add_argument("--label", default="baseline")
    status.set_defaults(func=command_status)

    finalize = sub.add_parser("finalize")
    finalize.add_argument("--session-dir", required=True)
    finalize.add_argument("--keep-label")
    finalize.add_argument("--dry-run", action="store_true")
    finalize.set_defaults(func=command_finalize)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = args.func(args)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result.get("ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
