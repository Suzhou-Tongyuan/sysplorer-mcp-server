"""General utility functions."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from mworks_driver import MWorksDriver
from constants import _PROJECT_ROOT, _WITHIN_RE, _NS_REF_RE, _METADATA_LIB_PATH, _CLASS_RE
from path_config import DEPLOY_ROOT, MWORKS_MW_MOL_DIR, deploy_sidecar_layout, get_resources_root
import state as _state


def _json(data: Dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def _decode_process_output(raw: bytes) -> str:
    """Best-effort decode for subprocess outputs across common Windows code pages."""
    if not raw:
        return ""
    for enc in ("utf-8", "cp936", "gbk", "cp1252"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode("utf-8", errors="ignore")


def _file_signature(path_obj: Path) -> Dict[str, Any]:
    try:
        st = path_obj.stat()
        return {"size": int(st.st_size), "mtime_ns": int(st.st_mtime_ns)}
    except Exception:
        return {"size": -1, "mtime_ns": -1}


def _current_driver_session_id(driver: MWorksDriver) -> int:
    return id(driver)


def _sync_load_caches(driver: MWorksDriver) -> None:
    sid = _current_driver_session_id(driver)
    with _state._load_cache_lock:
        if _state._driver_session_id != sid:
            _state._driver_session_id = sid
            _state._loaded_file_cache = {}
            _state._loaded_libs_cache = {}


def _disk_free_mb(path_text: str) -> Dict[str, Any]:
    target = Path(path_text).expanduser()
    probe = target
    if not probe.exists():
        probe = probe.parent if probe.parent != probe else Path.cwd()
    try:
        usage = shutil.disk_usage(str(probe))
        free_mb = usage.free / (1024 * 1024)
        return {
            "ok": True,
            "path": str(probe.resolve()),
            "free_mb": round(free_mb, 2),
            "total_mb": round(usage.total / (1024 * 1024), 2),
        }
    except Exception as exc:
        return {"ok": False, "path": str(target), "error": str(exc)}


def _resolve_project_path(path_text: str) -> Path:
    path_obj = Path(path_text)
    if path_obj.is_absolute():
        return path_obj
    return (_PROJECT_ROOT / path_obj).resolve()


def _get_known_sysplorer_libs() -> Dict[str, str]:
    """Return {fqname: display_name} for all default/preferred Sysplorer libraries."""
    with _state._known_libs_lock:
        if _state._known_libs_cache is not None:
            return _state._known_libs_cache
        result: Dict[str, str] = {}
        try:
            if _METADATA_LIB_PATH.exists():
                data = json.loads(_METADATA_LIB_PATH.read_text(encoding="utf-8"))
                for lib in data.get("catalog", {}).get("libraries", []):
                    fqname = lib.get("fqname", "").strip()
                    name = lib.get("name", "").strip()
                    if fqname and lib.get("is_default", False):
                        result[fqname] = name
        except Exception:
            pass
        _state._known_libs_cache = result
        return result


_SKIP_NS_AUTOLOAD_ROOTS = frozenset({"Real", "Integer", "Boolean", "String", "Enumeration"})


def _extract_uses_library_names(text: str) -> List[str]:
    """从 ``annotation(uses(...))`` 中解析顶层库名（忽略各库 version=，由 LoadLibrary 策略处理）。"""
    low = text.lower()
    key = "uses("
    idx = low.find(key)
    if idx < 0:
        return []
    i = idx + len(key)
    depth = 1
    start = i
    n = len(text)
    while i < n and depth:
        c = text[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        i += 1
    if depth != 0:
        return []
    body = text[start : i - 1]
    pat = re.compile(r"\b([A-Z][A-Za-z0-9_]*)\s*(?:\(\s*version\s*=\s*\"[^\"]*\"\s*\))?")
    out: List[str] = []
    seen: set[str] = set()
    for m in pat.finditer(body):
        name = m.group(1)
        if name and name not in seen:
            seen.add(name)
            out.append(name)
    return out


def _extract_dep_libs(mo_path: str) -> List[str]:
    """解析 .mo：从 uses() 与限定名首段收集需预加载的库；LoadLibrary 仅对 Modelica 带版本（由 driver 层规范化）。"""
    try:
        text = Path(mo_path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    own_pkg = ""
    m = _WITHIN_RE.search(text)
    if m:
        own_pkg = m.group(1).split(".")[0]
    known = _get_known_sysplorer_libs()
    from_uses = _extract_uses_library_names(text)
    refs = set(_NS_REF_RE.findall(text))
    from_ns: List[str] = []
    for ref in sorted(refs):
        if ref == own_pkg or ref in _SKIP_NS_AUTOLOAD_ROOTS:
            continue
        if ref in known:
            from_ns.append(ref)
        elif not known and len(ref) >= 2 and ref[0].isupper():
            # 无 MetaDataLib 时仍预加载形如 TYMultibody.xxx 的根命名空间，避免仅依赖 Sysplorer 按 uses 版本解析
            from_ns.append(ref)
    seen: set[str] = set()
    ordered: List[str] = []
    for x in from_uses + from_ns:
        if x == own_pkg or x in seen:
            continue
        seen.add(x)
        ordered.append(x)
    if "Modelica" in seen:
        return ["Modelica"] + [x for x in ordered if x != "Modelica"]
    return ordered


def infer_modelica_top_class_fq_from_mo(path: Path, max_chars: int = 600_000) -> Optional[str]:
    """Best-effort: first top-level ``package|model|... Name`` + optional ``within P;`` → ``P.Name`` or ``Name``."""
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if len(raw) > max_chars:
        raw = raw[:max_chars]
    wm = _WITHIN_RE.search(raw)
    prefix = wm.group(1).strip() if wm else ""
    m = _CLASS_RE.search(raw)
    if not m:
        return None
    name = m.group(2)
    if prefix:
        return f"{prefix}.{name}"
    return name


def modelica_fq_erase_candidates(fq: Optional[str]) -> List[str]:
    """由内向外的全名列表，供重载前按序 ``ClassExist`` / ``EraseClasses``（先卸子类/内层再卸外层包）。

    例：``RCExamples.SecondOrderRC`` → ``[RCExamples.SecondOrderRC, RCExamples]``；
    ``SecondOrderRC`` → ``[SecondOrderRC]``。
    """
    if not fq:
        return []
    parts = [x for x in str(fq).strip().split(".") if x]
    if not parts:
        return []
    n = len(parts)
    return [".".join(parts[:i]) for i in range(n, 0, -1)]


def _now_utc_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ── RAG helper functions (migrated from core/sysplorer_mgmt.py) ──────────────

def _discover_mw_mol_roots() -> list:
    candidates = [
        MWORKS_MW_MOL_DIR,
    ]
    out = []
    seen: set = set()
    for p in candidates:
        key = str(p.resolve()) if p.exists() else str(p)
        if key in seen:
            continue
        seen.add(key)
        if p.exists() and p.is_dir():
            out.append(p.resolve())
    return out


def _resolve_rag_index_path(path_text: str) -> Path:
    """Resolve BM25 index path: env MCP_RAG_INDEX_PATH; frozen/sidecar = relative to deploy dir; else workspace root."""
    p = Path(path_text)
    if p.is_absolute():
        return p.resolve()
    env = os.environ.get("MCP_RAG_INDEX_PATH", "").strip()
    if env:
        ep = Path(env)
        if ep.is_absolute():
            return ep.expanduser().resolve()
        if getattr(sys, "frozen", False):
            base = Path(sys.executable).resolve().parent
        elif deploy_sidecar_layout():
            base = DEPLOY_ROOT
        else:
            base = _PROJECT_ROOT
        return (base / env).expanduser().resolve()
    if getattr(sys, "frozen", False):
        return (Path(sys.executable).resolve().parent / path_text).resolve()
    if deploy_sidecar_layout():
        return (DEPLOY_ROOT / path_text).resolve()
    return (_PROJECT_ROOT / path_text).resolve()


def _resolve_rag_source_strings(sources: List[str]) -> List[str]:
    """Turn agent-provided source paths into absolute paths (no cwd dependence)."""
    out: List[str] = []
    seen: set = set()
    res_root = get_resources_root()
    for raw in sources:
        s = (raw or "").strip()
        if not s:
            continue
        p = Path(s)
        if p.is_absolute():
            key = str(p.resolve())
        else:
            rel = p.as_posix()
            pr = _PROJECT_ROOT / rel
            rr = res_root / rel
            if pr.exists():
                key = str(pr.resolve())
            elif rr.exists():
                key = str(rr.resolve())
            elif getattr(sys, "frozen", False) or deploy_sidecar_layout():
                # frozen / Tools 旁置：相对路径默认相对 resources 根
                key = str(rr.resolve())
            else:
                key = str(pr.resolve())
        if key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


def _get_default_rag_sources(rag_module: Any) -> list:
    del rag_module  # default corpora come from resources_manifest.json, not bm25.DEFAULT_SOURCES
    from core.resources_manifest import corpora_paths_for_default_index, load_manifest

    try:
        entries, _, _, root = load_manifest()
    except FileNotFoundError:
        raise
    except (ValueError, json.JSONDecodeError, TypeError, OSError) as exc:
        raise RuntimeError(f"invalid resources manifest: {exc}") from exc

    base = corpora_paths_for_default_index(entries, root)
    out: List[str] = []
    seen: set = set()
    for x in base:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out
