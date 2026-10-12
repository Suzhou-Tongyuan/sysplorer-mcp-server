"""Official RouteLine backend (loaded Sysplorer session required)."""
from __future__ import annotations

import json
import re
from typing import Any, Dict


_SAVE_EXISTS_RE = re.compile(
    r"(同名|已存在|already exists|file exists|already exist)",
    re.IGNORECASE,
)


def save_name_conflict(error: str) -> bool:
    return bool(_SAVE_EXISTS_RE.search(error or ""))


def official_routeline(model_name: str, left_port: str = "", right_port: str = "") -> Dict[str, Any]:
    """Call ModelingPy.RouteLine. Empty ports route every connection on the layer."""
    name = (model_name or "").strip()
    if not name:
        return {"ok": False, "error": "RouteLine requires a loaded model_name."}
    try:
        import mworks.sysplorer as ModelingPy  # type: ignore
    except Exception as exc:
        return {"ok": False, "error": f"mworks.sysplorer import failed: {exc}"}
    try:
        fn = getattr(ModelingPy, "RouteLine", None)
        if fn is None:
            return {"ok": False, "error": "ModelingPy.RouteLine is not available on this Sysplorer."}
        ok = fn(name, left_port or "", right_port or "")
        return {"ok": bool(ok), "error": "" if ok else "RouteLine returned false"}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def persist_official_routeline(
    model_name: str,
    save_folder: str = "",
    left_port: str = "",
    right_port: str = "",
    overwrite_existing: bool = False,
) -> Dict[str, Any]:
    """Route connections, then persist.

    After ``smart_layout`` already wrote Placement/Line to disk, pass
    ``overwrite_existing=True`` and use official ``SaveModel`` (same file).
    ``SaveModelAs`` into that folder often returns False (same-name file) and
    must not be treated as a layout writeback failure.
    """
    routed = official_routeline(model_name, left_port=left_port, right_port=right_port)
    out: Dict[str, Any] = {
        "ok": bool(routed.get("ok")),
        "error": routed.get("error") or "",
        "persisted": False,
        "save_conflict": False,
        "persist_api": "",
        "router": "official" if routed.get("ok") else "",
    }
    if not routed.get("ok"):
        return out

    if overwrite_existing:
        save = _save_loaded_model_json(model_name)
        out["save"] = save
        out["persist_api"] = "SaveModel"
        out["persisted"] = bool(save.get("ok"))
        if not out["persisted"]:
            err = str(save.get("error") or "SaveModel after RouteLine failed")
            out["save_conflict"] = save_name_conflict(err)
            out["warning"] = (
                f"{err}. RouteLine ran in session; this is not a layout writeback failure "
                "(Placement/Line may already be on disk)."
            )
        return out

    folder = (save_folder or "").strip()
    if not folder:
        out["warning"] = "RouteLine ran in the session but no save_folder was given to persist Line annotations."
        return out
    try:
        from tools.model_ops import mworks_save_model

        raw = mworks_save_model(model_name, folder=folder)
        save = json.loads(raw) if isinstance(raw, str) else (raw or {})
        out["save"] = save
        out["persist_api"] = "SaveModelAs"
        out["persisted"] = bool(save.get("ok"))
        if out["persisted"]:
            return out
        err = str(save.get("error") or "SaveModelAs after RouteLine failed")
        if save_name_conflict(err):
            retry = _save_loaded_model_json(model_name)
            out["save_conflict"] = True
            out["save_as_error"] = err
            out["save"] = retry
            out["persist_api"] = "SaveModel"
            out["persisted"] = bool(retry.get("ok"))
            if out["persisted"]:
                out["warning"] = (
                    "SaveModelAs refused an existing file; overwrote via SaveModel. "
                    "Layout writeback on disk was already done."
                )
            else:
                out["warning"] = (
                    f"{err}. Placement/Line writeback on disk is unchanged. "
                    "This SaveModelAs False is a persist conflict, not a layout failure."
                )
            return out
        out["warning"] = err
    except Exception as exc:
        out["warning"] = f"RouteLine succeeded but persist failed: {exc}"
    return out


def _save_loaded_model_json(model_name: str) -> Dict[str, Any]:
    try:
        from state import _get_driver

        result = _get_driver().save_loaded_model(model_name)
        raw = _get_driver().as_json(result)
        return json.loads(raw) if isinstance(raw, str) else (raw or {})
    except Exception as exc:
        return {"ok": False, "api": "SaveModel", "error": str(exc)}
