"""General utility functions."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from mworks_driver import MWorksDriver
from constants import _PROJECT_ROOT, _WITHIN_RE, _NS_REF_RE, _METADATA_LIB_PATH, _CLASS_RE
from path_config import (
    DEPLOY_ROOT,
    MWORKS_MW_MOL_DIR,
    WORKSPACE_ROOT,
    deploy_sidecar_layout,
    ensure_mcp_scratch_subdir,
    get_resources_root,
)
import state as _state

_PACKAGE_NAME_RE = re.compile(
    r"\b(?:encapsulated\s+|partial\s+|operator\s+|expandable\s+)*package\s+([A-Za-z_]\w*)",
    re.MULTILINE,
)


def looks_like_modelica_file_path(text: str) -> bool:
    """True if ``text`` is a filesystem path / ``.mo`` file, not a dotted class name."""
    raw = (text or "").strip()
    if not raw:
        return False
    if re.search(r"\.(mo|mol|moc)\b", raw, re.IGNORECASE):
        return True
    if re.match(r"^[A-Za-z]:[\\/]", raw):
        return True
    if raw.startswith("\\\\") or raw.startswith("//"):
        return True
    if "/" in raw or "\\" in raw:
        return True
    return False


def looks_like_qualified_class_name(text: str) -> bool:
    """True if ``text`` looks like ``Pkg`` or ``Pkg.Model``, not a file path."""
    raw = (text or "").strip()
    if not raw or looks_like_modelica_file_path(raw):
        return False
    return bool(re.match(r"^[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*$", raw))


# Sysplorer MSL spelling often differs from upstream Modelica (MultiBody vs Multibody).
_CLASS_SEGMENT_ALIASES: Dict[str, Tuple[str, ...]] = {
    "multibody": ("Multibody", "MultiBody"),
}


def modelica_class_name_candidates(name: str, *, limit: int = 8) -> List[str]:
    """Return the original class name first, then common Sysplorer/MSL spelling variants."""
    raw = (name or "").strip()
    if not raw:
        return []
    choices: List[List[str]] = []
    for seg in raw.split("."):
        opts = [seg]
        for alias in _CLASS_SEGMENT_ALIASES.get(seg.lower(), ()):
            if alias not in opts:
                opts.append(alias)
        choices.append(opts)
    out: List[str] = []
    seen: set[str] = set()
    from itertools import product

    for combo in product(*choices):
        joined = ".".join(combo)
        if joined in seen:
            continue
        seen.add(joined)
        out.append(joined)
        if len(out) >= max(1, int(limit)):
            break
    return out


def _normalize_dir_key(path: Path) -> str:
    try:
        resolved = path.expanduser().resolve()
    except OSError:
        resolved = path.expanduser()
    return str(resolved).replace("\\", "/").rstrip("/").casefold()


def resolve_model_save_folder(model_name: str, folder: str, workdir: str) -> Dict[str, Any]:
    """Pick a save directory that is never Sysplorer's working directory itself.

    Directory packages must live in ``{GetDirectory()}/{TopPackage}/``, not as
    ``package.mo`` directly under ``GetDirectory()``.
    """
    top = (model_name or "").strip().split(".", 1)[0].strip()
    if not top:
        raise ValueError("model_name is required")
    wd_raw = str(workdir or "").strip()
    if not wd_raw:
        raise ValueError("workdir is required")
    wd = Path(wd_raw)
    requested = str(folder or "").strip()
    redirected = False
    if requested:
        target = Path(requested)
        if _normalize_dir_key(target) == _normalize_dir_key(wd):
            target = wd / top
            redirected = True
    else:
        target = wd / top
        redirected = True
    return {
        "folder": target,
        "top_class_name": top,
        "workdir": wd,
        "redirected": redirected,
    }


def guess_saved_model_path(folder: Path, model_name: str) -> str:
    """Best-effort file written by ``SaveModelAs(model, folder)``."""
    name = (model_name or "").strip()
    simple = name.split(".")[-1].strip() if name else ""
    top = name.split(".", 1)[0].strip() if name else ""
    target = Path(folder)
    candidates = []
    if simple:
        candidates.append(target / f"{simple}.mo")
    if top and top != simple:
        candidates.append(target / f"{top}.mo")
    candidates.append(target / "package.mo")
    for cand in candidates:
        if cand.is_file():
            return str(cand.resolve())
    if simple:
        return str(target / f"{simple}.mo")
    return str(target)


def _json(data: Dict[str, Any]) -> str:
    from core.tool_envelope import dumps

    return dumps(data)


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

_IMPORT_STMT_RE = re.compile(
    r"^\s*import\s+(?:(?P<eq_alias>[A-Za-z_]\w*)\s*=\s*)?(?P<target>[\w.]+)(?:\s*\.\s*\*)?(?:\s+as\s+(?P<as_alias>[A-Za-z_]\w*))?\s*;",
    re.MULTILINE,
)


def _import_introduced_names(text: str) -> set[str]:
    """Names brought into scope by ``import``; they are not LoadLibrary library ids."""
    names: set[str] = set()
    for m in _IMPORT_STMT_RE.finditer(text or ""):
        eq_alias = (m.group("eq_alias") or "").strip()
        as_alias = (m.group("as_alias") or "").strip()
        target = (m.group("target") or "").strip()
        if eq_alias:
            names.add(eq_alias)
        if as_alias:
            names.add(as_alias)
        parts = [p for p in target.split(".") if p]
        if parts:
            names.add(parts[-1])
    return names


def _looks_like_autoload_library(name: str) -> bool:
    """Conservative top-level library names when MetaDataLib is missing."""
    if name in {"Modelica", "ModelicaReference", "ModelicaServices", "ModelicaTest"}:
        return True
    if len(name) >= 4 and name[:2] in {"TY", "TA"} and name[2:3].isupper():
        return True
    return False


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
    # uses(Lib(version="..."), Other(...)) — take the identifier before '(', not inner tokens.
    pat = re.compile(r"\b([A-Z][A-Za-z0-9_]*)\s*\(")
    out: List[str] = []
    seen: set[str] = set()
    for m in pat.finditer(body):
        name = m.group(1)
        if name and name not in seen:
            seen.add(name)
            out.append(name)
    return out


def _qualified_name_roots(text: str) -> set[str]:
    """First segment of each dotted name (``TYMultibody.Bodies.Body`` → ``TYMultibody``)."""
    roots: set[str] = set()
    for raw in _NS_REF_RE.findall(text or ""):
        root = (raw or "").split(".", 1)[0].strip()
        if root:
            roots.add(root)
    return roots


def _extract_dep_libs(mo_path: str) -> List[str]:
    """解析 .mo：``uses(Lib(...))`` 与限定名**第一段**作为 LoadLibrary 候选（``A.B.C`` 只认 ``A``）。"""
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
    import_names = _import_introduced_names(text)
    from_ns: List[str] = []
    for ref in sorted(_qualified_name_roots(text)):
        if ref == own_pkg or ref in _SKIP_NS_AUTOLOAD_ROOTS:
            continue
        if ref in import_names:
            continue
        if ref in known:
            from_ns.append(ref)
        elif not known and _looks_like_autoload_library(ref):
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


def _read_mo_within_prefix(path: Path, max_chars: int = 200_000) -> str:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if len(raw) > max_chars:
        raw = raw[:max_chars]
    wm = _WITHIN_RE.search(raw)
    return wm.group(1).strip() if wm else ""


def _read_package_class_name(package_mo: Path, max_chars: int = 200_000) -> Optional[str]:
    try:
        raw = package_mo.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if len(raw) > max_chars:
        raw = raw[:max_chars]
    m = _PACKAGE_NAME_RE.search(raw)
    return m.group(1) if m else None


def _ancestor_package_mo_files(start_dir: Path, max_up: int = 64) -> List[Path]:
    """Walk upward from ``start_dir`` collecting ``package.mo`` (nearest first)."""
    found: List[Path] = []
    cur = start_dir.resolve()
    for _ in range(max_up):
        candidate = cur / "package.mo"
        if candidate.is_file():
            found.append(candidate.resolve())
        parent = cur.parent
        if parent == cur:
            break
        cur = parent
    return found


def _pick_top_level_package_mo(package_mos: List[Path]) -> Optional[Path]:
    """Prefer outermost ``package.mo`` with empty ``within``; else outermost found."""
    if not package_mos:
        return None
    for pkg in reversed(package_mos):
        if not _read_mo_within_prefix(pkg):
            return pkg
    return package_mos[-1]


@dataclass(frozen=True)
class ModelicaLoadTarget:
    """Where ``OpenModelFile`` should point for a requested ``.mo`` path."""

    requested_path: Path
    load_path: Path
    redirected_to_package: bool
    root_package_name: Optional[str]
    within_prefix: str

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "requested_path": str(self.requested_path),
            "load_path": str(self.load_path),
            "redirected_to_package": bool(self.redirected_to_package),
            "root_package_name": self.root_package_name or "",
            "within_prefix": self.within_prefix or "",
        }


def resolve_modelica_load_target(mo_path: Path) -> ModelicaLoadTarget:
    """Resolve directory-based Modelica packages to their top-level ``package.mo``.

    Nested files with ``within Parent;`` must not be opened alone via ``OpenModelFile``:
    Sysplorer expects the package root. When an ancestor ``package.mo`` exists, load that
    top-level package file instead of the nested class file.
    """
    path = Path(mo_path).resolve()
    suffix = path.suffix.lower()
    if suffix == ".mol":
        return ModelicaLoadTarget(path, path, False, None, "")

    within = _read_mo_within_prefix(path) if path.is_file() else ""
    start_dir = path.parent if path.is_file() else path
    package_mos = _ancestor_package_mo_files(start_dir)
    top_pkg = _pick_top_level_package_mo(package_mos)

    if top_pkg is None:
        # Standalone / non-directory file: never invent a package root from ``within``.
        return ModelicaLoadTarget(path, path, False, None, within)

    root_name = _read_package_class_name(top_pkg)
    if not root_name and within:
        root_name = within.split(".", 1)[0]
    if not root_name:
        root_name = top_pkg.parent.name

    if path == top_pkg:
        return ModelicaLoadTarget(path, path, False, root_name, within)

    # Directory package present: always open the root package.mo (nested class / nested package.mo).
    return ModelicaLoadTarget(path, top_pkg, True, root_name, within)


def modelica_load_cache_signature(target: ModelicaLoadTarget) -> Dict[str, Any]:
    """Cache signature for load_file: requested file + resolved package.mo when redirected."""
    sig: Dict[str, Any] = {"load": _file_signature(target.load_path)}
    if target.redirected_to_package and target.requested_path != target.load_path:
        sig["requested"] = _file_signature(target.requested_path)
    return sig


def modelica_fq_erase_candidates(fq: Optional[str]) -> List[str]:
    """由内向外的全名列表（遗留辅助）。目录式 package 请用 ``erase_candidates_for_mo_path``。

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


def erase_candidates_for_mo_path(mo_path: Path) -> List[str]:
    """Classes to ``EraseClasses`` before reloading ``mo_path``.

    For directory packages: only the **root** package name (children go with the root).
    Do **not** erase parent prefixes while later opening only a nested ``.mo`` — that strips
    ``within`` context and causes parse errors such as unexpected ``;``.

    For standalone files: erase only the fully-qualified class from the file (not parents).
    """
    target = resolve_modelica_load_target(Path(mo_path))
    if target.root_package_name:
        return [target.root_package_name]
    fq = infer_modelica_top_class_fq_from_mo(target.requested_path)
    return [fq] if fq else []


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


def _probe_directory_writable(directory: Path) -> bool:
    """True if ``directory`` can be created and written (same probe as Smart Layout temp)."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        probe = directory / ".m_write_probe"
        probe.write_text("", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True
    except OSError:
        return False


def _rag_index_location_fields(meta: Dict[str, Any]) -> Dict[str, Any]:
    used = str(meta.get("used") or "")
    out: Dict[str, Any] = {"index_path": used}
    if meta.get("fallback"):
        out["index_path_preferred"] = str(meta.get("preferred") or "")
        out["index_path_fallback"] = True
        out["index_path_fallback_reason"] = str(meta.get("fallback_reason") or "")
    return out


def _resolve_rag_index_for_use(path_text: str, *, need_write: bool) -> Tuple[Path, Dict[str, Any]]:
    """Pick a usable index JSON path; fall back when the default deploy dir is read-only.

    If ``need_write`` is false and the preferred file already exists, load it in place
    (typical prebuilt / read-only install). When the file is missing or must be rebuilt,
    probe the parent directory and, on Permission denied, use
    ``<workspace>/.mworks_mcp/rag/<name>`` then ``%TEMP%/mworks_sysplorer_mcp/rag``.
    """
    preferred = _resolve_rag_index_path(path_text)
    fname = preferred.name or "modelica_doc_index.json"
    meta: Dict[str, Any] = {"preferred": str(preferred), "used": str(preferred), "fallback": False}

    if not need_write and preferred.is_file():
        return preferred, meta

    if _probe_directory_writable(preferred.parent):
        return preferred, meta

    reason = f"preferred RAG index directory is not writable: {preferred.parent}"
    workspace_fb = (WORKSPACE_ROOT / ".mworks_mcp" / "rag" / fname).resolve()
    if _probe_directory_writable(workspace_fb.parent):
        meta.update(
            {
                "used": str(workspace_fb),
                "fallback": True,
                "fallback_reason": reason,
            }
        )
        return workspace_fb, meta

    scratch_fb = (ensure_mcp_scratch_subdir("rag") / fname).resolve()
    if _probe_directory_writable(scratch_fb.parent):
        meta.update(
            {
                "used": str(scratch_fb),
                "fallback": True,
                "fallback_reason": f"{reason}; workspace .mworks_mcp/rag also not writable",
            }
        )
        return scratch_fb, meta

    raise PermissionError(
        f"cannot write RAG index {fname!r}: preferred={preferred.parent} is not writable, "
        f"and fallbacks failed. Set MCP_RAG_INDEX_PATH to a writable .json path. "
        f"resources/indexes is often under the install/deploy directory (read-only) "
        f"and modelica_doc_index.json is not shipped with the package."
    )


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
