"""MCP tool JSON (internal) and PROTOCOL-0381 wire failures."""
from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional

CODE_INVALID_ARGUMENTS = "invalid_arguments"
CODE_NOT_READY = "sysplorer.not_ready"
CODE_API_FAILED = "sysplorer.api_failed"
CODE_CLASS_NOT_FOUND = "sysplorer.class_not_found"
CODE_LIBRARY_NOT_INSTALLED = "sysplorer.library_not_installed"
CODE_LIBRARY_LOAD_FAILED = "sysplorer.library_load_failed"
CODE_FORBIDDEN = "sysplorer.forbidden"
CODE_TIMEOUT = "sysplorer.timeout"
CODE_PARTIAL_FAILURE = "sysplorer.partial_failure"

TOOL_FAILURE_KEY = "cc.tongyuan.mogick/toolFailure"
# Full business error object for clients. Not 0381-sanitized (message/hint may exceed 64 bytes).
ERROR_OBJECT_KEY = "sysplorer/error"
FAILURE_STAGES = frozenset(
    ("parse_input", "authorize", "lookup", "availability", "upstream", "execute")
)
HOST_INVOKE_STAGES = frozenset(("ensure_ready", "call_tool", "resolve_live_session"))
LOOKUP_OUTCOMES = frozenset(
    ("unknown", "ambiguous", "qualified_miss", "no_servers", "not_found")
)

_REASON_RE = re.compile(r"^[a-z][a-z0-9_]*[a-z0-9]$")
_STABLE_UPSTREAM_RE = re.compile(r"^(SYSPLORER_[A-Z0-9_]+|http_\d+|jsonrpc_-?\d+)$")
# Official GetLastErrors / exceptions, e.g. `错误(1001):无效的本地路径` or `Error(1001):...`.
_OFFICIAL_ERRNO_RE = re.compile(r"(?:错误|Error)\s*[\(（]\s*(\d+)\s*[\)）]", re.IGNORECASE)
_META_STR_MAX_BYTES = 64

_NEVER = {"mode": "never"}
_BACKOFF = {"mode": "backoff"}
_UNKNOWN = {"mode": "unknown"}
_RETRY_MODES = frozenset(("never", "immediate", "backoff", "poll", "after_change", "unknown"))


def retry_for(code: str) -> Dict[str, str]:
    if code in (CODE_INVALID_ARGUMENTS, CODE_FORBIDDEN, CODE_LIBRARY_NOT_INSTALLED):
        return dict(_NEVER)
    if code in (CODE_NOT_READY, CODE_TIMEOUT, CODE_LIBRARY_LOAD_FAILED):
        return dict(_BACKOFF)
    return dict(_UNKNOWN)


def _sanitize_retry(value: Any) -> Optional[Dict[str, str]]:
    if not isinstance(value, dict):
        return None
    mode = str(value.get("mode") or "").strip()
    if mode not in _RETRY_MODES:
        return None
    return {"mode": mode}


HINTS_BY_CODE: Dict[str, str] = {
    CODE_INVALID_ARGUMENTS: (
        "Change arguments and retry: fill required fields for this tool or action."
    ),
    CODE_NOT_READY: (
        "Do not change arguments. Call session_manager(action=health or ensure), "
        "then retry the same call."
    ),
    CODE_API_FAILED: "Read the error. Use get_api_document only for unwrapped command names.",
    CODE_CLASS_NOT_FOUND: "Change arguments: check the fully-qualified class name.",
    CODE_LIBRARY_NOT_INSTALLED: (
        "Do not retry load. Call load_library(action=installed) first; "
        "waiting will not install a missing library file. "
        "After a failed load on modelica_lite, use library_prepare."
    ),
    CODE_LIBRARY_LOAD_FAILED: (
        "Do not change the library name. Retry the same load_library later; "
        "the catalog lists this library but LoadLibrary failed."
    ),
    CODE_FORBIDDEN: (
        "Do not retry. Unload with model_manager; use session_manager for directories."
    ),
    CODE_TIMEOUT: (
        "Retry the same call later without changing arguments. "
        "A client timeout is not a confirmed API failure."
    ),
    CODE_PARTIAL_FAILURE: (
        "Some items failed. Read results[] and failed_class_names; "
        "successful items are still present."
    ),
}


def hint_for(code: str) -> str:
    return HINTS_BY_CODE.get(code, "Read the error and decide the next step.")


def _error_message(data: Dict[str, Any]) -> str:
    raw = data.get("error")
    if isinstance(raw, dict):
        return str(raw.get("message") or raw.get("error") or "").strip()
    return str(raw or "").strip()


def _join_error_text(data: Dict[str, Any]) -> str:
    parts = [
        _error_message(data),
        str(data.get("driver_error") or ""),
        str(data.get("message") or ""),
        str(data.get("hint") or ""),
        str(data.get("exception") or ""),
        str(data.get("reason") or ""),
    ]
    return " ".join(part for part in parts if part)


def error_looks_like_library_file_missing(data: Any) -> bool:
    """True when official text says the library file is absent (retrying will not help)."""
    err = _join_error_text(data) if isinstance(data, dict) else str(data or "")
    if not err.strip():
        return False
    low = err.lower()
    if "模型库文件" in err or "模型库不存在" in err or "库文件不存在" in err:
        return True
    if "library file" in low and (
        "does not exist" in low or "not exist" in low or "不存在" in err
    ):
        return True
    if "未安装" in err or "not installed" in low:
        return True
    return False


def error_looks_like_library_load_failed(data: Any) -> bool:
    """True when LoadLibrary failed without a confirmed missing-file phrase."""
    if error_looks_like_library_file_missing(data):
        return False
    err = _join_error_text(data) if isinstance(data, dict) else str(data or "")
    if not err.strip():
        return False
    low = err.lower()
    compact = low.replace(" ", "")
    return "loadlibraryreturnedfalse" in compact or "loadlibrary failed" in low


def error_looks_like_library_not_installed(data: Any) -> bool:
    """True when the library is missing from the catalog or the official file is absent."""
    return error_looks_like_library_file_missing(data)


def error_looks_like_class_not_found(data: Any) -> bool:
    """True when the failure is a missing Sysplorer class, not a missing argument or file."""
    err = _join_error_text(data) if isinstance(data, dict) else str(data or "")
    if not err.strip():
        return False
    low = err.lower()
    if any(
        token in low
        for token in (
            "class not found",
            "class does not exist",
            "class is missing",
        )
    ):
        return True
    # Official OpenModel / CheckModel / GetLastErrors: The model "X" does not exist.
    if "does not exist" in low and (
        "the model" in low or 'model "' in low or "model '" in low
    ):
        return True
    if "模型不存在" in err or "类不存在" in err:
        return True
    if "不存在" in err and ("模型" in err or "类" in err):
        if any(token in err for token in ("文件", "目录", "路径")):
            return False
        return True
    return False


def infer_code(data: Dict[str, Any]) -> str:
    existing = str(data.get("code") or "").strip()
    if existing:
        return existing
    err = _join_error_text(data)
    low = err.lower()
    compact = low.replace(" ", "")
    # Missing library before class-not-found: "模型库文件 X 不存在" also contains 模型/不存在.
    if error_looks_like_library_file_missing(data):
        return CODE_LIBRARY_NOT_INSTALLED
    if error_looks_like_library_load_failed(data):
        return CODE_LIBRARY_LOAD_FAILED
    # Class-not-found before "missing": GetModelText hints mention both.
    if error_looks_like_class_not_found(data):
        return CODE_CLASS_NOT_FOUND
    if any(
        token in low
        for token in (
            "required",
            "unsupported action",
            "unknown action",
            "unknown mode",
            "unsupported mode",
            "no longer handles",
            "is empty",
            "missing",
            "invalid json",
            "invalid graph",
        )
    ) or "不能为空" in err or "必填" in err:
        return CODE_INVALID_ARGUMENTS
    if "timeout" in low or "timed out" in low:
        return CODE_TIMEOUT
    if (
        "clearall" in compact
        or "forbidden" in low
        or "changedirectory" in compact
        or "changesimresultdirectory" in compact
        or "embedded mode" in low
        or ("exit()" in compact and "disabled" in low)
    ):
        return CODE_FORBIDDEN
    if any(
        token in low
        for token in (
            "driver not",
            "not connected",
            "not available",
            "driver_error",
        )
    ) or (str(data.get("driver_error") or "").strip() and not data.get("ok")):
        if str(data.get("driver_error") or "").strip():
            return CODE_NOT_READY
    return CODE_API_FAILED


def _invalid_arguments_reason(data: Dict[str, Any]) -> str:
    err = _join_error_text(data)
    low = err.lower()
    if any(
        token in low
        for token in ("required", "is empty", "missing")
    ) or "不能为空" in err or "必填" in err:
        return "missing_field"
    return "schema_mismatch"


def map_legacy_code(code: str, data: Dict[str, Any]) -> tuple[str, str, Dict[str, str]]:
    extra: Dict[str, str] = {}
    if code == CODE_INVALID_ARGUMENTS:
        return "parse_input", _invalid_arguments_reason(data), extra
    if code == CODE_FORBIDDEN:
        return "authorize", "forbidden", extra
    if code == CODE_CLASS_NOT_FOUND:
        extra["lookupOutcome"] = "not_found"
        return "lookup", "not_found", extra
    if code == CODE_LIBRARY_NOT_INSTALLED:
        return "availability", "not_found", extra
    if code == CODE_LIBRARY_LOAD_FAILED:
        return "upstream", "load_failed", extra
    if code == CODE_NOT_READY:
        return "availability", "object_not_ready", extra
    if code == CODE_TIMEOUT:
        stage = "upstream" if str(data.get("api") or "").strip() else "availability"
        return stage, "timeout", extra
    if code == CODE_API_FAILED:
        stage = "upstream" if str(data.get("api") or "").strip() else "execute"
        return stage, "internal", extra
    if code == CODE_PARTIAL_FAILURE:
        return "execute", "partial_failure", extra
    return "execute", "internal", extra


def _short_meta_str(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    raw = text.encode("utf-8")
    if len(raw) <= _META_STR_MAX_BYTES:
        return text
    return raw[:_META_STR_MAX_BYTES].decode("utf-8", errors="ignore")


def extract_official_error_code(*texts: Any) -> Optional[str]:
    """Turn official ``错误(1001)`` / ``Error(1001)`` text into ``SYSPLORER_1001``.

    Official APIs (CompareModel, OpenModel, LoadLibrary, GetVarValueAt, …) return
    bool and put the numeric code in GetLastErrors text. PROTOCOL-0381 forwards
    that as ``upstreamCode``; do not invent a per-API ``reasonCode``.
    """
    for text in texts:
        if text is None:
            continue
        match = _OFFICIAL_ERRNO_RE.search(str(text))
        if match:
            return f"SYSPLORER_{match.group(1)}"
    return None


def _stable_upstream_code(data: Dict[str, Any]) -> Optional[str]:
    for key in ("upstreamCode", "upstream_code"):
        val = _short_meta_str(data.get(key))
        if val and _STABLE_UPSTREAM_RE.match(val):
            return val
    extracted = extract_official_error_code(
        data.get("error"),
        data.get("message"),
        data.get("driver_error"),
        data.get("exception"),
    )
    if extracted and _STABLE_UPSTREAM_RE.match(extracted):
        return extracted
    return None


def is_valid_attribution(package: Any) -> bool:
    if not isinstance(package, dict):
        return False
    stage = package.get("failure_stage")
    reason = package.get("reasonCode")
    if stage in HOST_INVOKE_STAGES:
        return False
    if stage not in FAILURE_STAGES:
        return False
    if not isinstance(reason, str) or not _REASON_RE.match(reason):
        return False
    return True


def _sanitize_business_code(value: Any) -> Optional[str]:
    text = _short_meta_str(value)
    if not text:
        return None
    if text == CODE_INVALID_ARGUMENTS or text.startswith("sysplorer."):
        return text
    return None


def _sanitize_attribution(package: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "failure_stage": str(package["failure_stage"]),
        "reasonCode": str(package["reasonCode"]),
    }
    business = _sanitize_business_code(package.get("code"))
    if business:
        out["code"] = business
    if out["failure_stage"] == "lookup":
        outcome = _short_meta_str(package.get("lookupOutcome"))
        if outcome in LOOKUP_OUTCOMES:
            out["lookupOutcome"] = outcome
    upstream = _short_meta_str(package.get("upstreamCode"))
    if upstream and _STABLE_UPSTREAM_RE.match(upstream):
        out["upstreamCode"] = upstream
    retry = _sanitize_retry(package.get("retry"))
    if retry:
        # Tool-owned Agent advice. Not a PROTOCOL-0108 runtime/circuit input.
        out["retry"] = retry
    return out


def build_error_object(data: Dict[str, Any]) -> Dict[str, Any]:
    """Unified client error object. Does not invent per-API reasonCodes."""
    code = str(data.get("code") or infer_code(data))
    attr = build_attribution(data)
    message = str(data.get("message") or "").strip() or _error_message(data) or "tool failed"
    obj: Dict[str, Any] = {
        "code": code,
        "message": message,
        "failure_stage": attr.get("failure_stage"),
        "reasonCode": attr.get("reasonCode"),
        "retry": attr.get("retry") or retry_for(code),
        "hint": str(data.get("hint") or "").strip() or hint_for(code),
    }
    if attr.get("upstreamCode"):
        obj["upstreamCode"] = attr["upstreamCode"]
    if attr.get("lookupOutcome"):
        obj["lookupOutcome"] = attr["lookupOutcome"]
    api = str(data.get("api") or "").strip()
    if api:
        obj["api"] = api
    for key in (
        "topLevelLibrary",
        "className",
        "installed",
        "is_load",
        "library_version",
        "library_path",
    ):
        if key in data:
            obj[key] = data[key]
    return obj


def is_valid_error_object(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    if not str(obj.get("code") or "").strip():
        return False
    retry = obj.get("retry")
    if not isinstance(retry, dict) or str(retry.get("mode") or "") not in _RETRY_MODES:
        return False
    if str(obj.get("failure_stage") or "") not in FAILURE_STAGES:
        return False
    if not isinstance(obj.get("reasonCode"), str) or not _REASON_RE.match(str(obj.get("reasonCode"))):
        return False
    return True


def build_attribution(data: Dict[str, Any]) -> Dict[str, Any]:
    code = str(data.get("code") or infer_code(data))
    retry = _sanitize_retry(data.get("retry")) or retry_for(code)
    nested = data.get("_meta")
    if isinstance(nested, dict):
        existing = nested.get(TOOL_FAILURE_KEY)
        if is_valid_attribution(existing):
            sanitized = _sanitize_attribution(existing)
            if "retry" not in sanitized:
                sanitized["retry"] = retry
            if "code" not in sanitized:
                business = _sanitize_business_code(code)
                if business:
                    sanitized["code"] = business
            return sanitized
    stage, reason, extra = map_legacy_code(code, data)
    package: Dict[str, Any] = {
        "failure_stage": stage,
        "reasonCode": reason,
        **extra,
        "code": code,
        "retry": retry,
    }
    upstream = _stable_upstream_code(data)
    if upstream:
        package["upstreamCode"] = upstream
    return _sanitize_attribution(package)


def failure_content(data: Dict[str, Any]) -> str:
    code = str(data.get("code") or infer_code(data))
    hint = str(data.get("hint") or "").strip() or hint_for(code)
    parts = [hint]
    api = str(data.get("api") or "").strip()
    if api and api.lower() not in hint.lower():
        parts.append(f"API: {api}")
    message = str(data.get("message") or data.get("error") or "").strip()
    if message and message not in hint:
        parts.append(message)
    failed_names = data.get("failed_class_names")
    if isinstance(failed_names, list) and failed_names:
        listed = ", ".join(str(name) for name in failed_names if str(name).strip())
        if listed and listed not in "\n".join(parts):
            parts.append(f"Failed classes: {listed}")
    results = data.get("results")
    if isinstance(results, list):
        for row in results:
            if not isinstance(row, dict) or row.get("ok"):
                continue
            name = str(row.get("full_class_name") or row.get("requested_class_name") or "").strip()
            err = str(row.get("error") or "").strip()
            line = f"{name}: {err}".strip(": ")
            if line and line not in "\n".join(parts):
                parts.append(line)
    text = "\n".join(parts).strip() or hint_for(code)
    if '"failure_stage"' in text.replace(" ", ""):
        return hint_for(code)
    return text


def normalize_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(data)
    if "ok" not in out and "success" in out:
        out["ok"] = bool(out["success"])
    if out.get("ok") is False:
        if not str(out.get("message") or "").strip():
            out["message"] = str(
                out.get("error")
                or out.get("driver_error")
                or out.get("exception")
                or out.get("reason")
                or "tool failed"
            )
        out["code"] = infer_code(out)
        if not isinstance(out.get("retry"), dict):
            out["retry"] = retry_for(str(out["code"]))
        if not str(out.get("hint") or "").strip():
            out["hint"] = hint_for(str(out["code"]))
        upstream = _stable_upstream_code(out)
        if upstream:
            out["upstreamCode"] = upstream
        out["tool_error"] = build_error_object(out)
    return out


def dumps(data: Dict[str, Any]) -> str:
    return json.dumps(normalize_payload(data), ensure_ascii=False, separators=(",", ":"))


def payload_is_failure(data: Any) -> bool:
    return isinstance(data, dict) and data.get("ok") is False


def _first_text_content(result: Any) -> str:
    content = getattr(result, "content", None) or []
    if not content:
        return ""
    return str(getattr(content[0], "text", "") or "")


def _payload_from_result(result: Any) -> Dict[str, Any]:
    text = _first_text_content(result)
    if not text:
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {"ok": False, "error": text}
    if isinstance(data, dict):
        return data
    return {"ok": False, "error": text}


def _result_meta(result: Any) -> Dict[str, Any]:
    meta = getattr(result, "meta", None)
    return dict(meta) if isinstance(meta, dict) else {}


def _call_tool_failure(data: Dict[str, Any], extra_meta: Optional[Dict[str, Any]] = None) -> Any:
    from mcp.types import CallToolResult, TextContent

    payload = normalize_payload(data)
    meta = dict(extra_meta or {})
    meta[TOOL_FAILURE_KEY] = build_attribution(payload)
    err_obj = payload.get("tool_error") if isinstance(payload.get("tool_error"), dict) else build_error_object(payload)
    meta[ERROR_OBJECT_KEY] = err_obj
    text = failure_content(payload)
    envelope = json.dumps({"ok": False, "error": err_obj}, ensure_ascii=False, separators=(",", ":"))
    # FastMCP convert_result validates CallToolResult.structuredContent against
    # the ``-> str`` wrap model ``{"result": str}``. Leaving it None makes Cursor
    # report model_*Output validation errors and drop the real failure text.
    # First content is the 0381 human sentence; the second keeps the business object.
    return CallToolResult(
        content=[
            TextContent(type="text", text=text),
            TextContent(type="text", text=envelope),
        ],
        structuredContent={"result": text},
        isError=True,
        **{"_meta": meta},
    )


def promote_mcp_result(result: Any) -> Any:
    """Mark business failures as isError and attach PROTOCOL-0381 ``_meta``."""
    try:
        from mcp.types import CallToolResult
    except ImportError:
        return result

    if isinstance(result, CallToolResult):
        if not result.isError:
            return result
        meta = _result_meta(result)
        if is_valid_attribution(meta.get(TOOL_FAILURE_KEY)):
            return result
        data = _payload_from_result(result)
        if not payload_is_failure(data):
            data = normalize_payload({"ok": False, "error": _first_text_content(result) or "tool failed"})
        return _call_tool_failure(data, extra_meta=meta)

    if not isinstance(result, str):
        return result
    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        return result
    if not payload_is_failure(data):
        return result
    return _call_tool_failure(data)
