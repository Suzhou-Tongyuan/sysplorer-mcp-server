"""Load and validate resources_manifest.json for RAG doc corpora."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from path_config import RESOURCES_MANIFEST_FILENAME, get_resources_root


@dataclass
class CorpusEntry:
    id: str
    title: str
    description: str
    path: str
    default_index: bool
    keywords: List[str]

    def to_public_dict(self, resolved: Path) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "path": self.path,
            "default_index": self.default_index,
            "keywords": list(self.keywords),
            "resolved_paths": [str(resolved.resolve())] if resolved.exists() else [],
            "exists": resolved.exists(),
        }


def _as_str(v: Any, field: str) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    raise TypeError(f"{field} must be a string")


def _as_bool(v: Any, field: str) -> bool:
    if isinstance(v, bool):
        return v
    raise TypeError(f"{field} must be a boolean")


def _as_optional_str(v: Any) -> str:
    if isinstance(v, str):
        return v.strip()
    return ""


def _as_str_list(v: Any, field: str) -> List[str]:
    if v is None:
        return []
    if not isinstance(v, list):
        raise TypeError(f"{field} must be a list")
    out: List[str] = []
    for i, x in enumerate(v):
        if not isinstance(x, str):
            raise TypeError(f"{field}[{i}] must be a string")
        t = x.strip()
        if t:
            out.append(t)
    return out


def _coerce_manifest_version(v: Any) -> int:
    """JSON may decode 1 as int, 1.0 as float, or hand-edited files may use \"1\" string."""
    if v is None:
        return 1
    if isinstance(v, bool):
        raise ValueError("manifest version must be a positive integer")
    if isinstance(v, int):
        n = v
    elif isinstance(v, float):
        if not v.is_integer():
            raise ValueError("manifest version must be a positive integer")
        n = int(v)
    elif isinstance(v, str):
        t = v.strip()
        if not t:
            return 1
        try:
            f = float(t)
        except ValueError as exc:
            raise ValueError("manifest version must be a positive integer") from exc
        if f < 1 or not f.is_integer():
            raise ValueError("manifest version must be a positive integer")
        n = int(f)
    else:
        raise ValueError("manifest version must be a positive integer")
    if n < 1:
        raise ValueError("manifest version must be a positive integer")
    return n


def _keywords_from_item(item: Dict[str, Any]) -> List[str]:
    raw = item.get("keywords")
    if raw is None:
        raw = item.get("query_keywords")
    return _as_str_list(raw, "keywords")


def _parse_corpus_entries_v1(raw_corpora: List[Any]) -> List[CorpusEntry]:
    entries: List[CorpusEntry] = []
    seen_ids: set = set()
    for i, item in enumerate(raw_corpora):
        if not isinstance(item, dict):
            raise ValueError(f"corpora[{i}] must be an object")
        cid = _as_str(item.get("id"), "id")
        if not cid:
            raise ValueError(f"corpora[{i}].id is required")
        if cid in seen_ids:
            raise ValueError(f"duplicate corpus id: {cid}")
        seen_ids.add(cid)
        rel = _as_str(item.get("path"), "path")
        if not rel:
            raise ValueError(f"corpora[{i}].path is required")
        if os.path.isabs(rel):
            raise ValueError(f"corpora[{i}].path must be relative to resources root")
        entries.append(
            CorpusEntry(
                id=cid,
                title=_as_str(item.get("title"), "title") or cid,
                description=_as_str(item.get("description"), "description"),
                path=rel.rstrip("/\\").replace("\\", "/"),
                default_index=_as_bool(item.get("default_index", False), "default_index"),
                keywords=_as_str_list(item.get("keywords"), "keywords"),
            )
        )
    return entries


def _parse_corpus_entries_v2_resource_categories(data: Dict[str, Any]) -> List[CorpusEntry]:
    raw = data.get("resource_categories")
    if not isinstance(raw, list) or not raw:
        raise ValueError("manifest resource_categories must be a non-empty list")
    default_ids: set = set()
    for x in data.get("default_sources", []) or []:
        if isinstance(x, str) and x.strip():
            default_ids.add(x.strip())
    entries: List[CorpusEntry] = []
    seen_ids: set = set()
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"resource_categories[{i}] must be an object")
        cid = _as_str(item.get("id"), "id")
        if not cid:
            raise ValueError(f"resource_categories[{i}].id is required")
        if cid in seen_ids:
            raise ValueError(f"duplicate resource category id: {cid}")
        seen_ids.add(cid)
        rel = _as_str(item.get("path"), "path")
        if not rel:
            raise ValueError(f"resource_categories[{i}].path is required")
        if os.path.isabs(rel):
            raise ValueError(f"resource_categories[{i}].path must be relative to resources root")
        title = _as_optional_str(item.get("title")) or _as_optional_str(item.get("name")) or cid
        desc = _as_str(item.get("description"), "description")
        entries.append(
            CorpusEntry(
                id=cid,
                title=title,
                description=desc,
                path=rel.rstrip("/\\").replace("\\", "/"),
                default_index=cid in default_ids,
                keywords=_keywords_from_item(item),
            )
        )
    return entries


def parse_manifest_payload(data: Dict[str, Any]) -> Tuple[List[CorpusEntry], int]:
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a JSON object")
    version = _coerce_manifest_version(data.get("version", 1))
    raw_corpora = data.get("corpora")
    if isinstance(raw_corpora, list) and raw_corpora:
        entries = _parse_corpus_entries_v1(raw_corpora)
    elif isinstance(data.get("resource_categories"), list) and data["resource_categories"]:
        entries = _parse_corpus_entries_v2_resource_categories(data)
    else:
        raise ValueError("manifest must contain a non-empty corpora or resource_categories array")
    return entries, version


def resolve_corpus_path(entry: CorpusEntry, resources_root: Optional[Path] = None) -> Path:
    root = (resources_root if resources_root is not None else get_resources_root()).resolve()
    candidate = (root / entry.path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"corpus path escapes resources root: {entry.path}") from exc
    return candidate


def load_manifest(
    manifest_path: Optional[Path] = None,
    resources_root: Optional[Path] = None,
) -> Tuple[List[CorpusEntry], int, Path, Path]:
    root = (resources_root if resources_root is not None else get_resources_root()).resolve()
    path = manifest_path if manifest_path is not None else (root / RESOURCES_MANIFEST_FILENAME)
    if not path.is_file():
        raise FileNotFoundError(f"resources manifest not found: {path}")
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    entries, version = parse_manifest_payload(data)
    return entries, version, path, root


def corpora_paths_for_default_index(entries: List[CorpusEntry], resources_root: Path) -> List[str]:
    out: List[str] = []
    seen: set = set()
    for e in entries:
        if not e.default_index:
            continue
        p = resolve_corpus_path(e, resources_root)
        if not p.exists():
            continue
        key = str(p)
        if key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


def _manifest_item_priority(item: Dict[str, Any]) -> int:
    p = item.get("priority", 99)
    if isinstance(p, bool):
        return 99
    if isinstance(p, int):
        return p
    if isinstance(p, float) and p.is_integer():
        return int(p)
    if isinstance(p, str) and p.strip().isdigit():
        return int(p.strip())
    return 99


def browse_resources_manifest_for_instructions(
    resources_root: Optional[Path] = None,
) -> Tuple[str, Dict[str, Any]]:
    """
    Read resources_manifest.json once and produce a short markdown fragment for MCP server
    instructions (no corpus walk, no RAG index build). Returns (text, meta) for logging.
    """
    root = (resources_root if resources_root is not None else get_resources_root()).resolve()
    manifest_path = root / RESOURCES_MANIFEST_FILENAME
    meta: Dict[str, Any] = {
        "ok": False,
        "resources_root": str(root),
        "manifest_path": str(manifest_path),
        "categories": 0,
        "error": None,
    }
    if not manifest_path.is_file():
        meta["error"] = "manifest_missing"
        frag = (
            "\n## 旁置文档语料\n\n"
            f"未在资源根目录找到 `{RESOURCES_MANIFEST_FILENAME}`。\n"
            f"预期路径: `{manifest_path}`\n\n"
            "若需检索文档，可先调用 `mworks_sysplorer_resources_retrieval(action=\"corpora\")` 确认是否已部署语料目录。\n"
        )
        return frag, meta

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        meta["error"] = f"read_or_json: {exc}"
        frag = f"\n## 旁置文档语料\n\n清单文件无法读取或解析: `{manifest_path}`\n"
        return frag, meta

    lines: List[str] = [
        "",
        "## 旁置文档语料（检索时机）",
        "",
        "摘要来自 exe/进程旁置的 `resources/resources_manifest.json`，**不要在会话开头对语料做全文搜索**；"
        "仅当用户任务与下述某一类主题相关时，再调用 `mworks_sysplorer_resources_retrieval(action=\"search\")`，"
        "或用 `mworks_sysplorer_resources_retrieval(action=\"corpora\")` 查看解析后的路径与 `corpus_id`。",
        "",
        f"- 资源根目录: `{root}`",
    ]
    ver = data.get("version", "")
    if ver != "" and ver is not None:
        lines.append(f"- 清单 version: {ver}")
    lu = data.get("last_updated")
    if lu is not None:
        last_updated = str(lu).strip()
        if last_updated:
            lines.append(f"- last_updated: {last_updated}")

    default_sources = data.get("default_sources") or []
    if isinstance(default_sources, list) and default_sources:
        ids = [str(x).strip() for x in default_sources if str(x).strip()]
        if ids:
            lines.append(f"- 默认合并检索的语料 id: {', '.join(ids)}")
    lines.append("")

    categories = data.get("resource_categories")
    corpora = data.get("corpora")
    items: List[Dict[str, Any]] = []
    if isinstance(categories, list) and categories:
        items = [x for x in categories if isinstance(x, dict)]
        items.sort(key=_manifest_item_priority)
    elif isinstance(corpora, list) and corpora:
        items = [x for x in corpora if isinstance(x, dict)]

    meta["categories"] = len(items)
    meta["ok"] = True

    for item in items:
        cid = str(item.get("id", "")).strip() or "?"
        title = str(item.get("name") or item.get("title") or cid).strip()
        desc = str(item.get("description", "")).strip()
        rel_path = str(item.get("path", "")).strip()
        kws = item.get("query_keywords")
        if kws is None:
            kws = item.get("keywords")
        kw_list: List[str] = []
        if isinstance(kws, list):
            kw_list = [str(k).strip() for k in kws if str(k).strip()]
        elif isinstance(kws, str) and kws.strip():
            kw_list = [kws.strip()]
        kw_preview = "、".join(kw_list[:14])
        if len(kw_list) > 14:
            kw_preview += "…"
        lines.append(f"### `{cid}` — {title}")
        if desc:
            lines.append(f"- 说明: {desc}")
        if rel_path:
            lines.append(f"- 相对目录: `{rel_path}`")
        if kw_preview:
            lines.append(f"- 何时检索: 任务/问题与上述主题或关键词相关时 → {kw_preview}")
        lines.append("")

    lines.append(
        "English: Use `mworks_sysplorer_resources_retrieval(action=\"corpora\")` for resolved paths; "
        "call `action=\"search\"` only when the user task matches a corpus above.\n"
    )
    return "\n".join(lines), meta


MODELING_PATH_ROUTER_REL = "modeling_rules/modeling_path_router.md"
SEVEN_GATES_WORKFLOW_REL = "modeling_rules/seven_gates_workflow.md"
_MAX_MODELING_ROUTER_BYTES = 512_000
_MAX_SEVEN_GATES_WORKFLOW_BYTES = 512_000


def load_modeling_path_router_for_instructions(
    resources_root: Optional[Path] = None,
) -> Tuple[str, Dict[str, Any]]:
    """
    Load modeling_path_router.md from resources for MCP server instructions (single file, no RAG).
    """
    root = (resources_root if resources_root is not None else get_resources_root()).resolve()
    path = (root / MODELING_PATH_ROUTER_REL.replace("\\", "/")).resolve()
    meta: Dict[str, Any] = {
        "ok": False,
        "resources_root": str(root),
        "router_path": str(path),
        "error": None,
        "size_bytes": 0,
    }
    try:
        path.relative_to(root)
    except ValueError:
        meta["error"] = "path_escape"
        frag = f"\n## 建模分流规则\n\n路径异常，已跳过注入: `{path}`\n"
        return frag, meta

    if not path.is_file():
        meta["error"] = "router_missing"
        frag = (
            "\n## 建模分流规则\n\n"
            f"未找到 `{MODELING_PATH_ROUTER_REL}`。\n"
            f"预期路径: `{path}`\n\n"
            "搭建/编辑模型前请调用 `mworks_sysplorer_resources_retrieval(action=\"search\", query=...)` 并指定语料路径或 `corpus_id`（见 manifest），或检索 `modeling_path_router`。\n"
        )
        return frag, meta

    try:
        st = path.stat()
        if st.st_size > _MAX_MODELING_ROUTER_BYTES:
            meta["error"] = f"file_too_large:{st.st_size}"
            frag = f"\n## 建模分流规则\n\n文件过大已跳过注入: `{path}`\n"
            return frag, meta
        body = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        meta["error"] = f"read: {exc}"
        frag = f"\n## 建模分流规则\n\n无法读取: `{path}`\n"
        return frag, meta

    meta["ok"] = True
    meta["size_bytes"] = len(body.encode("utf-8"))
    frag = (
        "\n## 建模分流规则（会话开始前必读）\n\n"
        "以下内容来自旁置 `resources/` 下的分流说明，**搭建或编辑模型时必须先判别 Modelica 物理模型与 Sysblock 框图**，再选对应流程。\n\n"
        "---\n\n"
        f"{body.rstrip()}\n\n"
        "---\n"
    )
    return frag, meta


def load_seven_gates_workflow_for_instructions(
    resources_root: Optional[Path] = None,
) -> Tuple[str, Dict[str, Any]]:
    """
    Load seven_gates_workflow.md (7 Gates + closed-loop workflow from AGENTS.md) for MCP instructions.
    """
    root = (resources_root if resources_root is not None else get_resources_root()).resolve()
    path = (root / SEVEN_GATES_WORKFLOW_REL.replace("\\", "/")).resolve()
    meta: Dict[str, Any] = {
        "ok": False,
        "resources_root": str(root),
        "workflow_path": str(path),
        "error": None,
        "size_bytes": 0,
    }
    try:
        path.relative_to(root)
    except ValueError:
        meta["error"] = "path_escape"
        frag = f"\n## 七 Gate 与建模执行闭环\n\n路径异常，已跳过注入: `{path}`\n"
        return frag, meta

    if not path.is_file():
        meta["error"] = "workflow_missing"
        frag = (
            "\n## 七 Gate 与建模执行闭环\n\n"
            f"未找到 `{SEVEN_GATES_WORKFLOW_REL}`。\n"
            f"预期路径: `{path}`\n\n"
            "请在工作区查阅 `AGENTS.md` / `CLAUDE.md`，或通过语料检索 modeling_rules。\n"
        )
        return frag, meta

    try:
        st = path.stat()
        if st.st_size > _MAX_SEVEN_GATES_WORKFLOW_BYTES:
            meta["error"] = f"file_too_large:{st.st_size}"
            frag = f"\n## 七 Gate 与建模执行闭环\n\n文件过大已跳过注入: `{path}`\n"
            return frag, meta
        body = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        meta["error"] = f"read: {exc}"
        frag = f"\n## 七 Gate 与建模执行闭环\n\n无法读取: `{path}`\n"
        return frag, meta

    meta["ok"] = True
    meta["size_bytes"] = len(body.encode("utf-8"))
    frag = (
        "\n## 七 Gate 与建模执行闭环（会话开始前必读）\n\n"
        "以下内容来自旁置 `resources/modeling_rules/seven_gates_workflow.md`，与仓库 `AGENTS.md` 对齐。\n\n"
        "---\n\n"
        f"{body.rstrip()}\n\n"
        "---\n"
    )
    return frag, meta
