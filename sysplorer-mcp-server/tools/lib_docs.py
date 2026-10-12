"""MCP tools: live Sysplorer class documentation and API help (no resources/RAG for these)."""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from constants import normalize_load_library_call
from path_config import ensure_mcp_scratch_subdir
from core.library_lookup import (
    attach_class_library_fields,
    attach_library_diagnostics,
    classify_library_failure,
    classify_missing_class,
    library_workspace_status,
    top_level_library_name,
)
from core.tool_envelope import (
    CODE_CLASS_NOT_FOUND,
    CODE_LIBRARY_LOAD_FAILED,
    CODE_LIBRARY_NOT_INSTALLED,
    CODE_PARTIAL_FAILURE,
    hint_for,
)
from core.utils import _json, modelica_class_name_candidates
from mcp_instance import mcp, readonly_annotations
from state import _get_driver


def _top_level_library(full_class_name: str) -> str:
    return top_level_library_name(full_class_name)


_SKIP_TAGS = frozenset({"style", "script", "xml", "noscript"})
_BLOCK_TAGS = frozenset(
    {"br", "p", "div", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "li", "table", "title"}
)
_CELL_TAGS = frozenset({"td", "th"})
_SKIP_BLOCK_RE = re.compile(r"(?is)<(style|script|xml)\b[^>]*>.*?</\1>")
_CSS_NOISE_RE = re.compile(
    r"@font-face|@page\b|panose-1:|/\*\s*Font Definitions|\.docmanager-equation|"
    r"\bmso-|\{font-family:",
    re.I,
)


def _attr_map(attrs: Any) -> Dict[str, str]:
    return {str(key).lower(): ("" if value is None else str(value)) for key, value in (attrs or [])}


def _keep_href(href: str) -> bool:
    text = (href or "").strip()
    if not text or text.startswith("#"):
        return False
    low = text.lower()
    return not low.startswith(("javascript:", "data:", "vbscript:"))


def _img_placeholder(attrs: Dict[str, str]) -> str:
    alt = (attrs.get("alt") or "").strip()
    title = (attrs.get("title") or "").strip()
    src = (attrs.get("src") or attrs.get("o:href") or "").strip()
    cls = (attrs.get("class") or "").strip().lower()
    kind = "公式" if any(token in cls for token in ("equation", "omath", "math")) else "图片"
    label = alt or title
    if not label and src and not src.lower().startswith("data:"):
        label = Path(src.split("?", 1)[0]).name
    if label:
        return f"[{kind}: {label}]"
    return f"[{kind}]"


class _HTMLToText(HTMLParser):
    """ExportDocumentation HTML → plain text.

    Word-exported help puts CSS in ``<style><!-- ... --></style>``. HTMLParser
    treats that as CDATA and would otherwise dump it through ``handle_data``.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._chunks: list[str] = []
        self._skip_depth = 0
        self._in_cell = 0
        self._cell_index = 0
        self._link_hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        name = tag.lower()
        if name in _SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        attr_map = _attr_map(attrs)
        if name in {"img", "v:imagedata"} or name.endswith(":imagedata"):
            self._chunks.append(_img_placeholder(attr_map))
            return
        if name == "a":
            self._link_hrefs.append((attr_map.get("href") or "").strip())
            return
        if name == "table":
            self._chunks.append("\n")
            return
        if name == "tr":
            self._cell_index = 0
            self._chunks.append("\n")
            return
        if name in _CELL_TAGS:
            if self._cell_index:
                self._chunks.append(" | ")
            self._cell_index += 1
            self._in_cell += 1
            return
        if name in _BLOCK_TAGS:
            self._chunks.append(" " if self._in_cell else "\n")

    def handle_endtag(self, tag: str) -> None:
        name = tag.lower()
        if name in _SKIP_TAGS:
            if self._skip_depth:
                self._skip_depth -= 1
            return
        if self._skip_depth:
            return
        if name == "a":
            href = self._link_hrefs.pop() if self._link_hrefs else ""
            if _keep_href(href):
                self._chunks.append(f" ({href})")
            return
        if name == "table":
            self._chunks.append("\n")
            return
        if name == "tr":
            self._chunks.append("\n")
            return
        if name in _CELL_TAGS:
            if self._in_cell:
                self._in_cell -= 1
            return
        if name in _BLOCK_TAGS and not self._in_cell:
            self._chunks.append("\n")

    def handle_startendtag(self, tag: str, attrs: Any) -> None:
        self.handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._in_cell:
            data = re.sub(r"\s+", " ", data)
        self._chunks.append(data)

    def handle_comment(self, data: str) -> None:
        return

    def get_text(self) -> str:
        raw = "".join(self._chunks).replace("\xa0", " ")
        raw = re.sub(r"[ \t\r\f\v]+", " ", raw)
        lines = [ln.strip() for ln in raw.split("\n")]
        kept = [line for line in lines if line and not _CSS_NOISE_RE.search(line)]
        return "\n".join(kept).strip()


# 单次 MCP 调用允许的最大类全名数量（避免响应过大与过长阻塞）
_MAX_LIB_MODEL_DOC_BATCH = 50


def _html_to_plain_text(html: str) -> str:
    cleaned = _SKIP_BLOCK_RE.sub(" ", html or "")
    parser = _HTMLToText()
    try:
        parser.feed(cleaned)
        parser.close()
        return parser.get_text()
    except Exception:
        stripped = re.sub(r"<[^>]+>", " ", cleaned)
        stripped = re.sub(r"[ \t\r\f\v]+", " ", stripped)
        lines = [ln.strip() for ln in stripped.split("\n")]
        return "\n".join(line for line in lines if line and not _CSS_NOISE_RE.search(line)).strip()


def _html_file_to_plain_text(path: Path) -> str:
    return _html_to_plain_text(path.read_text(encoding="utf-8", errors="replace"))


def _resolve_lib_model_class_names(
    full_class_name: str, full_class_names: Optional[List[str]]
) -> Union[List[str], str]:
    """Return ordered unique non-empty class names, or an error message string."""
    if full_class_names is not None:
        raw: List[str] = []
        for item in full_class_names:
            s = (item or "").strip()
            if s:
                raw.append(s)
        if raw:
            names = list(dict.fromkeys(raw))
            if len(names) > _MAX_LIB_MODEL_DOC_BATCH:
                return (
                    f"too many class names ({len(names)}); "
                    f"maximum per call is {_MAX_LIB_MODEL_DOC_BATCH}"
                )
            return names
    s = (full_class_name or "").strip()
    if not s:
        return "full_class_name or full_class_names is required"
    return [s]


def _class_exist_bool(driver: Any, name: str) -> Optional[bool]:
    class_exist = getattr(driver, "class_exist", None)
    if not callable(class_exist):
        return None
    ce = class_exist(name)
    if not ce.ok:
        raise RuntimeError(ce.error or "ClassExist failed")
    return bool(ce.data)


def _top_library_is_loaded(driver: Any, top: str) -> bool:
    return library_workspace_status(driver, top) == "loaded"


def _safe_lib_doc_filename(class_name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", (class_name or "").strip()) or "class"
    return cleaned[:180] + ".html"


def _get_lib_model_document_one(name: str) -> Dict[str, Any]:
    """Export documentation for a single fully qualified class name (JSON-serializable dict)."""
    out: Dict[str, Any] = {
        "ok": False,
        "tool": "get_lib_model_document",
        "full_class_name": name,
        "documentation_text": "",
        "documentation_html_path": "",
        "class_exist_before": None,
        "class_exist_after_load": None,
        "load_library_called": False,
        "open_model_called": False,
        "top_level_library": "",
        "error": "",
    }

    top = _top_level_library(name)
    if not top:
        out["error"] = "cannot derive top-level library from full_class_name"
        return out
    out["top_level_library"] = top
    candidates = modelica_class_name_candidates(name)
    out["tried_class_names"] = candidates

    try:
        driver = _get_driver()
    except Exception as exc:
        out["error"] = f"driver not available: {exc}"
        return out

    if not callable(driver._api.get("ClassExist")):
        out["error"] = "ClassExist API not available in this Sysplorer runtime"
        return out
    if not callable(driver._api.get("ExportDocumentation")):
        out["error"] = "ExportDocumentation API not available in this Sysplorer runtime"
        return out

    try:
        exists_map = {cand: _class_exist_bool(driver, cand) for cand in candidates}
    except RuntimeError as exc:
        out["error"] = str(exc)
        return out
    out["class_exist_before"] = bool(exists_map.get(name))
    resolved = next((cand for cand in candidates if exists_map.get(cand)), "")

    if not resolved:
        already_loaded = _top_library_is_loaded(driver, top)
        out["library_already_loaded"] = already_loaded
        if not already_loaded:
            lib, ver = normalize_load_library_call(top, "")
            if not lib:
                out["error"] = f"invalid library name derived from class: {top!r}"
                return out
            lr = driver.load_library(lib, ver)
            out["load_library_called"] = True
            if not lr.ok:
                _set_library_failure_error(out, name, driver, lr.error or "LoadLibrary failed")
                return out
        try:
            exists_map = {cand: _class_exist_bool(driver, cand) for cand in candidates}
        except RuntimeError as exc:
            out["error"] = str(exc)
            return out
        out["class_exist_after_load"] = bool(exists_map.get(name) or any(exists_map.values()))
        resolved = next((cand for cand in candidates if exists_map.get(cand)), "")

    if not resolved and classify_missing_class(driver, name) == CODE_LIBRARY_NOT_INSTALLED:
        _set_library_failure_error(
            out,
            name,
            driver,
            str(out.get("error") or "LoadLibrary did not make the top-level library visible"),
        )
        return out

    if not resolved:
        for cand in candidates:
            om = driver.open_model(cand)
            out["open_model_called"] = True
            if not om.ok:
                out["warning_open_model"] = om.error
                continue
            try:
                if _class_exist_bool(driver, cand):
                    resolved = cand
                    break
            except RuntimeError as exc:
                out["error"] = str(exc)
                return out
        if not resolved:
            _set_missing_class_or_library_error(out, name, candidates, driver)
            return out

    if resolved != name:
        out["resolved_class_name"] = resolved
        out["requested_class_name"] = name

    if not out.get("open_model_called"):
        om = driver.open_model(resolved)
        out["open_model_called"] = True
        if not om.ok:
            out["warning_open_model"] = om.error

    scratch = ensure_mcp_scratch_subdir("lib_docs")
    safe_file = scratch / _safe_lib_doc_filename(resolved)
    out["documentation_html_path"] = str(safe_file.resolve())
    ed = driver.export_documentation(resolved, str(safe_file))
    if not ed.ok:
        out["error"] = ed.error
        out["documentation_html_path"] = ""
        return out

    if not safe_file.is_file():
        out["error"] = f"ExportDocumentation reported success but file missing: {safe_file}"
        out["documentation_html_path"] = ""
        return out

    try:
        plain = _html_file_to_plain_text(safe_file)
    except OSError as exc:
        out["error"] = f"read exported documentation failed: {exc}"
        return out

    out["ok"] = True
    out["documentation_text"] = plain
    return out


def _get_lib_model_document_one_safe(name: str) -> Dict[str, Any]:
    """One class: never raise; missing/invalid stays ``ok:false`` with tried names."""
    try:
        return _get_lib_model_document_one(name)
    except Exception as exc:
        return {
            "ok": False,
            "tool": "get_lib_model_document",
            "full_class_name": name,
            "documentation_text": "",
            "documentation_html_path": "",
            "error": f"{type(exc).__name__}: {exc}",
            "tried_class_names": modelica_class_name_candidates(name),
        }


def _batch_lib_model_documents(names: List[str]) -> Dict[str, Any]:
    results = [_get_lib_model_document_one_safe(n) for n in names]
    failed = [
        str(row.get("full_class_name") or name)
        for name, row in zip(names, results)
        if not row.get("ok")
    ]
    ok_count = len(results) - len(failed)
    out: Dict[str, Any] = {
        "tool": "get_lib_model_document",
        "count": len(results),
        "ok_count": ok_count,
        "failed_count": len(failed),
        "results": results,
    }
    if not failed:
        out["ok"] = True
        return out
    out["failed_class_names"] = failed
    out["error"] = f"{len(failed)} of {len(results)} classes failed: " + ", ".join(failed)
    if ok_count:
        # Keep successful documentation on the success wire (isError would drop results[]).
        out["ok"] = True
        out["partial"] = True
        out["code"] = CODE_PARTIAL_FAILURE
        out["hint"] = hint_for(CODE_PARTIAL_FAILURE)
        return out
    out["ok"] = False
    first_code = next((str(row.get("code") or "").strip() for row in results if row.get("code")), "")
    if first_code:
        out["code"] = first_code
    return out


@mcp.tool(annotations=readonly_annotations())
def get_lib_model_document(
    full_class_name: str = "",
    full_class_names: Optional[List[str]] = None,
) -> str:
    """Export documentation for loaded library classes (``ExportDocumentation``).

    Prefer one call with ``full_class_names`` (list, max 50) over many single-class calls.
    Single class: ``full_class_name``. Returns ``documentation_text`` (and HTML path).
    ``documentation_text`` drops ``<style>``/``<script>`` (Word CSS), keeps table columns,
    and turns ``<img>`` / ``<a href>`` into ``[图片]`` / ``text (url)``.
    Missing class names stay per-item ``ok:false`` (not a LoadLibrary failure by themselves).
    A mixed batch keeps successful items and lists ``failed_class_names`` with
    ``code=sysplorer.partial_failure``.
    """
    resolved = _resolve_lib_model_class_names(full_class_name, full_class_names)
    if isinstance(resolved, str):
        return _json({"ok": False, "tool": "get_lib_model_document", "error": resolved})

    if len(resolved) == 1:
        return _json(_get_lib_model_document_one_safe(resolved[0]))
    return _json(_batch_lib_model_documents(resolved))


def _set_library_not_installed_error(
    out: Dict[str, Any],
    name: str,
    detail: str = "",
    driver: Any = None,
) -> None:
    top = str(out.get("top_level_library") or top_level_library_name(name) or "").strip()
    extra = (detail or "").strip()
    out["error"] = (
        f"top-level library {top!r} is not loaded or not installed"
        + (f": {extra}" if extra else "")
    )
    out["code"] = CODE_LIBRARY_NOT_INSTALLED
    out["hint"] = hint_for(CODE_LIBRARY_NOT_INSTALLED)
    attach_class_library_fields(out, name, top)
    if driver is not None:
        attach_library_diagnostics(out, driver, top)


def _set_library_load_failed_error(
    out: Dict[str, Any],
    name: str,
    detail: str = "",
    driver: Any = None,
) -> None:
    top = str(out.get("top_level_library") or top_level_library_name(name) or "").strip()
    extra = (detail or "").strip()
    out["error"] = (
        f"LoadLibrary failed for cataloged library {top!r}"
        + (f": {extra}" if extra else "")
    )
    out["code"] = CODE_LIBRARY_LOAD_FAILED
    out["hint"] = hint_for(CODE_LIBRARY_LOAD_FAILED)
    attach_class_library_fields(out, name, top)
    if driver is not None:
        attach_library_diagnostics(out, driver, top)


def _set_library_failure_error(
    out: Dict[str, Any],
    name: str,
    driver: Any,
    detail: str = "",
) -> None:
    top = str(out.get("top_level_library") or top_level_library_name(name) or "").strip()
    code = classify_library_failure(driver, top, detail)
    if code == CODE_LIBRARY_LOAD_FAILED:
        _set_library_load_failed_error(out, name, detail, driver)
        return
    _set_library_not_installed_error(out, name, detail, driver)


def _set_class_not_found_error(out: Dict[str, Any], name: str, candidates: List[str]) -> None:
    """ClassExist stayed false while the top-level library is already in the workspace."""
    top = str(out.get("top_level_library") or "").strip() or "(unknown library)"
    already = bool(out.get("library_already_loaded"))
    load_called = bool(out.get("load_library_called"))
    open_warn = str(out.get("warning_open_model") or "").strip()
    tried = ", ".join(candidates) if candidates else name
    if already and not load_called:
        out["error"] = (
            f"class not found: {name!r} is not visible in already-loaded library {top!r}. "
            "This is not a LoadLibrary failure — check the fully-qualified class name "
            "(typo / missing package path). ClassExist is false."
        )
    elif load_called:
        out["error"] = (
            f"class not found after LoadLibrary({top!r}): {name!r} still does not exist. "
            + (open_warn or "OpenModel did not make the class visible")
        )
    else:
        out["error"] = (
            f"class not found: {name!r}. "
            + (open_warn or "ClassExist is false")
        )
    out["code"] = CODE_CLASS_NOT_FOUND
    out["hint"] = hint_for(CODE_CLASS_NOT_FOUND) + (
        f" Tried names: {tried}."
    )
    attach_class_library_fields(out, name, top)


def _set_missing_class_or_library_error(
    out: Dict[str, Any],
    name: str,
    candidates: List[str],
    driver: Any,
) -> None:
    if classify_missing_class(driver, name) == CODE_LIBRARY_NOT_INSTALLED:
        detail = str(out.get("warning_open_model") or out.get("error") or "").strip()
        _set_library_failure_error(out, name, driver, detail)
        return
    _set_class_not_found_error(out, name, candidates)


def _apply_api_document_hints(out: Dict[str, Any], cmd: str) -> None:
    key = (cmd or "").strip().lower()
    if key == "comparemodel":
        out["mcp_preferred_tool"] = (
            'compare_model(model_name="...", model_name_b="...", is_file=false)'
        )
        out["mcp_hint"] = (
            "Prefer compare_model over run_sysplorer_api. "
            "Current builds: CompareModel(firstModel: str, secondModel: str, isFile: bool) -> bool; "
            "is_file=false for loaded qualified names, is_file=true for two .mo paths. "
            "APIs vary by Sysplorer version—confirm CompareModel is listed in ListFunctions() "
            "and re-read this Help on the connected instance before scripting."
        )
        return
    if key == "eraseclasses":
        out["mcp_preferred_tool"] = 'model_manager(action="unload", model_name="...")'
        out["mcp_hint"] = (
            "EraseClasses takes a tuple of fully-qualified names, e.g. EraseClasses(('ElevatorLib',)), "
            "not a single str. Prefer model_manager unload."
        )
        return
    if key == "openmodel":
        out["mcp_preferred_tool"] = 'model_manager(action="open", model_name="...")'
        out["mcp_hint"] = (
            "OpenModel opens an already-loaded class by qualified name. "
            "To load a .mo / package.mo file use OpenModelFile or model_manager(action='load_file')."
        )
        return
    if key == "openmodelfile":
        out["mcp_preferred_tool"] = 'model_manager(action="load_file", file_path="...")'
        out["mcp_hint"] = (
            "OpenModelFile takes a filesystem path. Nested directory packages should load the top-level "
            "package.mo (model_manager load_file does this)."
        )
        return
    if key in ("getlasterror", "getlasterrors"):
        out["mcp_preferred_tool"] = 'model_inspect(action="get_last_errors")'
        out["mcp_hint"] = (
            "Use model_inspect(action='get_last_errors'). ModelingPy name is GetLastErrors (plural); "
            "there is no GetLastError."
        )
        if key == "getlasterror":
            out["ok"] = False
            out["error"] = "No API named GetLastError; use model_inspect(action='get_last_errors')."
            out["suggested_api_function_name"] = "GetLastErrors"


@mcp.tool(annotations=readonly_annotations(idempotent=True))
def get_api_document(api_function_name: str) -> str:
    """Official ``Help(cmd)`` for an unwrapped ModelingPy command name.

    MCP routing: if OpenModel / OpenModelFile / EraseClasses / GetLastErrors /
    CompareModel / LoadLibrary already have a dedicated tool, use that tool —
    do not ListFunctions first. This tool is Help(cmd) on the main session only.
    """
    cmd = (api_function_name or "").strip()
    if not cmd:
        return _json({"ok": False, "tool": "get_api_document", "error": "api_function_name is required"})

    out: Dict[str, Any] = {
        "ok": False,
        "tool": "get_api_document",
        "api_function_name": cmd,
        "help_text": "",
        "error": "",
    }

    try:
        driver = _get_driver()
    except Exception as exc:
        out["error"] = f"driver not available: {exc}"
        return _json(out)

    if not callable(driver._api.get("Help")):
        out["error"] = "Help API not available in this Sysplorer runtime"
        return _json(out)

    hr = driver.api_help(cmd)
    if not hr.ok:
        out["error"] = hr.error
        _apply_api_document_hints(out, cmd)
        return _json(out)

    text = hr.data
    if text is None:
        text = hr.raw
    if text is None:
        text = ""
    help_text = str(text)
    out["ok"] = True
    out["help_text"] = help_text
    out["help_text_empty"] = not help_text.strip()
    _apply_api_document_hints(out, cmd)
    return _json(out)
