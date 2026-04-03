"""Model operation MCP tools: load, open, check, translate, simulate."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from mcp_instance import mcp
from path_config import (
    DIAGRAM_EXPORT_TEMP_DIR,
    TEMP_CODE_FOLDER,
)
from constants import (
    commercial_lib_load_without_version,
    normalize_load_library_call,
    split_trailing_version_from_library_display_name,
)
from core.utils import (
    _json,
    _sync_load_caches,
    _file_signature,
    _extract_dep_libs,
)
import state as _state
from state import _get_driver


@mcp.tool()
def mworks_sysplorer_load_library(library_name: str, library_version: str = "", use_cache: bool = True) -> str:
    """加载库。内置 Modelica 标准库默认使用 4.0.0.TY.1；其余商业库请勿向官方 LoadLibrary 传版本号（由 Sysplorer 自选）。

    **耗时与超时**：内部会调用 Sysplorer `LoadLibrary`，大型 .mol 库首次加载常需数秒至数十秒。若 MCP 客户端对单次工具有超时限制，
    可能在服务端仍在加载时出现「请求超时」——**这不表示 LoadLibrary 一定失败**（后台可能仍在解析）。可在稍候后 **再次调用本工具**
    （`use_cache=true` 时若已成功会走缓存快速返回）；仍不确定时可结合 `mworks_sysplorer_session_manager(action="health")` 与会话状态判断。
    """
    try:
        driver = _get_driver()
        _sync_load_caches(driver)
        lib_raw = (library_name or "").strip()
        ver_raw = (library_version or "").strip()
        _, trailing_ver = split_trailing_version_from_library_display_name(lib_raw)
        lib, ver_eff = normalize_load_library_call(lib_raw, ver_raw)
        ver_ignored = bool(commercial_lib_load_without_version(lib) and (ver_raw or trailing_ver))
        key = f"{lib}@{ver_eff}"
        if use_cache:
            with _state._load_cache_lock:
                cached = _state._loaded_libs_cache.get(key)
            if cached and cached.get("ok", False):
                payload = {"ok": True, "api": "LoadLibrary", "cached": True, "library_name": lib}
                if ver_ignored:
                    payload["library_version_ignored"] = ver_raw
                return _json(payload)

        result = driver.load_library(library_name=lib, library_version=ver_eff)
        out = json.loads(driver.as_json(result))
        out["cached"] = False
        out["library_name"] = lib
        if ver_ignored:
            out["library_version_ignored"] = ver_raw
        if result.ok and use_cache:
            with _state._load_cache_lock:
                _state._loaded_libs_cache[key] = {"ok": True, "ts": time.time()}
        return _json(out)
    except Exception as exc:
        return _json({"ok": False, "api": "LoadLibrary", "error": str(exc)})


# ── Model manager: one MCP tool + Python helpers for workflow/tests ───────────


def _mm_attach_action(raw: str, action: str) -> str:
    """Merge manager_action into JSON response from driver helpers."""
    try:
        payload = json.loads(raw)
        if isinstance(payload, dict):
            payload["manager_action"] = action
        return json.dumps(payload, ensure_ascii=False)
    except Exception:
        return raw


def _mm_open(model_name: str) -> str:
    try:
        result = _get_driver().open_model(model_name=model_name)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "OpenModel", "error": str(exc)})


def _mm_new(model_name: str, restriction: str = "Modelica") -> str:
    try:
        result = _get_driver().new_model(model_name=model_name, restriction=restriction)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "NewModel", "error": str(exc)})


def _mm_load_file(
    file_path: str,
    auto_load_deps: bool = True,
    skip_if_unchanged: bool = True,
    force_reload: bool = False,
) -> str:
    try:
        driver = _get_driver()
        _sync_load_caches(driver)
        resolved = Path(file_path).resolve()
        file_key = str(resolved)
        signature = _file_signature(resolved)

        if force_reload:
            with _state._load_cache_lock:
                _state._loaded_file_cache.pop(file_key, None)

        if not force_reload and skip_if_unchanged:
            with _state._load_cache_lock:
                cached = _state._loaded_file_cache.get(file_key)
            if cached and cached.get("ok", False) and cached.get("signature") == signature:
                return _json({"ok": True, "api": "OpenModelFile", "cached": True, "file_path": file_key})

        dep_results: Dict[str, Any] = {}
        if auto_load_deps:
            deps = _extract_dep_libs(str(resolved))
            for lib_fqname in deps:
                lib_key = f"{lib_fqname}@"
                use_cached = False
                with _state._load_cache_lock:
                    if _state._loaded_libs_cache.get(lib_key, {}).get("ok", False):
                        use_cached = True
                if use_cached:
                    dep_results[lib_fqname] = {"ok": True, "error": "", "cached": True}
                    continue
                r = driver.load_library(library_name=lib_fqname)
                dep_results[lib_fqname] = {"ok": r.ok, "error": r.error if not r.ok else "", "cached": False}
                if r.ok:
                    with _state._load_cache_lock:
                        _state._loaded_libs_cache[lib_key] = {"ok": True, "ts": time.time()}

        unload_meta: Optional[Dict[str, Any]] = None
        if force_reload:
            ur = driver.unload_loaded_classes_for_mo(str(resolved))
            unload_meta = json.loads(driver.as_json(ur))
            if not ur.ok:
                return _json(
                    {
                        "ok": False,
                        "api": "OpenModelFile",
                        "error": ur.error,
                        "unload_loaded_classes_for_mo": unload_meta,
                        "file_path": file_key,
                    }
                )

        ar: Optional[bool] = True if force_reload else None
        result = driver.load_file(str(resolved), auto_reload=ar)
        out = json.loads(driver.as_json(result))
        out["cached"] = False
        out["file_path"] = file_key
        if unload_meta is not None:
            out["unload_loaded_classes_for_mo"] = unload_meta
        if dep_results:
            out["auto_loaded_libs"] = dep_results
        if result.ok:
            with _state._load_cache_lock:
                _state._loaded_file_cache[file_key] = {
                    "ok": True,
                    "signature": signature,
                    "auto_loaded_libs": dep_results,
                    "ts": time.time(),
                }
        return _json(out)

    except Exception as exc:
        return _json({"ok": False, "api": "loadFile", "error": str(exc)})


def _mm_unload(model_name: str) -> str:
    try:
        result = _get_driver().unload_file(model_name)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "unloadFile", "error": str(exc)})


def _mm_save(model_name: str, folder: str = "", save_type: int = 0) -> str:
    try:
        result = _get_driver().save_model(model_name, folder=folder, save_type=save_type)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "saveModel", "error": str(exc)})


def _mm_lookup_component(model_name: str, comp_name: str, info_type: str = "") -> str:
    try:
        result = _get_driver().lookup_component(model_name, comp_name, info_type=info_type)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "lookupComp", "error": str(exc)})


def _mm_get_components(model_name: str, component: str = "") -> str:
    try:
        result = _get_driver().get_components(model_name, component=component)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetComponents", "error": str(exc)})


def _mm_get_component_ports(model_name: str, component_name: str, port_direction: int = 0) -> str:
    try:
        result = _get_driver().get_component_ports(
            model_name=model_name,
            component_name=component_name,
            port_direction=port_direction,
        )
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetComponentPorts", "error": str(exc)})


def _mm_get_model_text(model_name: str) -> str:
    try:
        result = _get_driver().get_model_text(model_name)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "getModelText", "error": str(exc)})


def _mm_get_model_description(model_name: str) -> str:
    try:
        result = _get_driver().get_model_description(model_name)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetModelDescription", "error": str(exc)})


def _mm_get_component_description(model_name: str, comp_name: str) -> str:
    try:
        result = _get_driver().get_component_description(model_name, comp_name)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetComponentDescription", "error": str(exc)})


def _mm_get_classes(model_name: str) -> str:
    try:
        result = _get_driver().get_classes(model_name)
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "GetClasses", "error": str(exc)})


def _mm_export_model_diagram(
    model_name: str,
    output_path: str = "",
    width: int = 800,
    height: int = 600,
    open_model_first: bool = True,
) -> str:
    try:
        driver = _get_driver()
        name = (model_name or "").strip()
        if not name:
            return _json({"ok": False, "api": "ExportDiagram", "error": "model_name is required"})

        if open_model_first:
            o = driver.open_model(model_name=name)
            if not o.ok:
                return _json(
                    {
                        "ok": False,
                        "api": "OpenModel",
                        "error": o.error or "OpenModel failed",
                        "hint": "Load the .mo first (mworks_sysplorer_model_manager action=load_file) before export.",
                    }
                )

        out = (output_path or "").strip()
        if not out:
            DIAGRAM_EXPORT_TEMP_DIR.mkdir(parents=True, exist_ok=True)
            safe = name.replace(".", "_")
            out = str(DIAGRAM_EXPORT_TEMP_DIR / f"{safe}_diagram.png")

        p = Path(out).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        result = driver.export_diagram(
            model_name=name,
            output_path=str(p),
            width=width,
            height=height,
        )
        payload = json.loads(driver.as_json(result))
        payload["output_path"] = str(p)
        return _json(payload)
    except Exception as exc:
        return _json({"ok": False, "api": "ExportDiagram", "error": str(exc)})


def mworks_open_model(model_name: str) -> str:
    """Python helper (not an MCP tool). Prefer ``mworks_sysplorer_model_manager`` with action=open."""
    return _mm_open(model_name)


def mworks_new_model(model_name: str, restriction: str = "Modelica") -> str:
    """Python helper (not an MCP tool). Prefer ``mworks_sysplorer_model_manager`` with action=new."""
    return _mm_new(model_name, restriction=restriction)


def mworks_load_file(
    file_path: str,
    auto_load_deps: bool = True,
    skip_if_unchanged: bool = True,
    force_reload: bool = False,
) -> str:
    """Python helper (not an MCP tool). Prefer ``mworks_sysplorer_model_manager`` with action=load_file."""
    return _mm_load_file(
        file_path,
        auto_load_deps=auto_load_deps,
        skip_if_unchanged=skip_if_unchanged,
        force_reload=force_reload,
    )


def mworks_unload_file(model_name: str) -> str:
    """Python helper (not an MCP tool). Prefer ``mworks_sysplorer_model_manager`` with action=unload."""
    return _mm_unload(model_name)


def mworks_save_model(model_name: str, folder: str = "", save_type: int = 0) -> str:
    """Python helper (not an MCP tool). Prefer ``mworks_sysplorer_model_manager`` with action=save."""
    return _mm_save(model_name, folder=folder, save_type=save_type)


def mworks_export_model_diagram(
    model_name: str,
    output_path: str = "",
    width: int = 800,
    height: int = 600,
    open_model_first: bool = True,
) -> str:
    """Python helper (not an MCP tool). Prefer ``mworks_sysplorer_model_manager`` with action=export_model_diagram."""
    return _mm_attach_action(
        _mm_export_model_diagram(
            model_name,
            output_path=output_path,
            width=width,
            height=height,
            open_model_first=open_model_first,
        ),
        "export_model_diagram",
    )


_MM_ACTION_ALIASES = {
    "open": "open",
    "open_model": "open",
    "new": "new",
    "new_model": "new",
    "load_file": "load_file",
    "load": "load_file",
    "unload": "unload",
    "unload_file": "unload",
    "save": "save",
    "save_model": "save",
    "lookup_component": "lookup_component",
    "get_components": "get_components",
    "get_component_ports": "get_component_ports",
    "get_model_text": "get_model_text",
    "get_model_description": "get_model_description",
    "get_component_description": "get_component_description",
    "get_classes": "get_classes",
    "export_model_diagram": "export_model_diagram",
    "export_diagram": "export_model_diagram",
}


@mcp.tool()
def mworks_sysplorer_model_manager(
    action: str,
    model_name: str = "",
    file_path: str = "",
    restriction: str = "Modelica",
    auto_load_deps: bool = True,
    skip_if_unchanged: bool = True,
    force_reload: bool = False,
    folder: str = "",
    save_type: int = 0,
    comp_name: str = "",
    component: str = "",
    component_name: str = "",
    info_type: str = "",
    port_direction: int = 0,
    output_path: str = "",
    width: int = 800,
    height: int = 600,
    open_model_first: bool = True,
) -> str:
    """统一入口：模型生命周期（打开/新建/加载/卸载/保存）、原理图导出与已加载模型的内省查询。

    **必选**：``action``（不区分大小写）。合法取值与必填参数：

    | action | 含义 | 必填参数 |
    |--------|------|----------|
    | ``open`` 或 ``open_model`` | 在 Sysplorer 中打开已加载模型 | ``model_name`` |
    | ``new`` 或 ``new_model`` | 新建模型 | ``model_name``；可选 ``restriction``：``Modelica`` / ``Sysblock`` |
    | ``load_file`` 或 ``load`` | 加载磁盘上的 ``.mo``（可自动 LoadLibrary 依赖） | ``file_path`` |
    | ``unload`` 或 ``unload_file`` | 官方 ``EraseClasses`` 按全名卸载（**不**调用 ``ClearAll``） | ``model_name`` |
    | ``save`` 或 ``save_model`` | 保存模型到文件夹 | ``model_name``；可选 ``folder``、``save_type`` |
    | ``export_model_diagram`` 或 ``export_diagram`` | 将 Diagram 导出为图片（``ExportDiagram``） | ``model_name``；可选 ``output_path``、``width``、``height``、``open_model_first`` |
    | ``lookup_component`` | ``lookupComp`` 查询组件信息 | ``model_name``, ``comp_name``；可选 ``info_type`` |
    | ``get_components`` | 列出子组件 | ``model_name``；可选 ``component``（父路径） |
    | ``get_component_ports`` | 查询组件端口 | ``model_name``；可选 ``component_name``、``port_direction`` |
    | ``get_model_text`` | 获取模型/类源文本 | ``model_name`` |
    | ``get_model_description`` | 模型/类描述字符串 | ``model_name`` |
    | ``get_component_description`` | 子组件描述 | ``model_name``, ``comp_name`` |
    | ``get_classes`` | 嵌套类名列表 | ``model_name`` |

    **load_file 专用**：``auto_load_deps``、``skip_if_unchanged``、``force_reload``。

    **export_model_diagram 专用**：``output_path``（空则写入服务端临时目录下默认 PNG）、``width``、``height``、``open_model_first``（默认先 ``OpenModel``）。

    成功/失败时返回与各底层 API 相同的 JSON，并额外带 ``manager_action`` 字段标明规范化后的动作名。
    """
    key = (action or "").strip().lower()
    norm = _MM_ACTION_ALIASES.get(key)
    if not norm:
        return _json(
            {
                "ok": False,
                "tool": "mworks_sysplorer_model_manager",
                "error": f"unknown action: {action!r}",
                "hint": (
                    "Use: open, new, load_file, unload, save, export_model_diagram, lookup_component, get_components, "
                    "get_component_ports, get_model_text, get_model_description, get_component_description, get_classes"
                ),
            }
        )

    mn = (model_name or "").strip()
    fp = (file_path or "").strip()
    cn = (comp_name or "").strip()
    comp = (component or "").strip()
    cname = (component_name or "").strip()

    if norm == "open":
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name is required for action=open",
                }
            )
        return _mm_attach_action(_mm_open(mn), norm)
    if norm == "new":
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name is required for action=new",
                }
            )
        return _mm_attach_action(_mm_new(mn, restriction=restriction or "Modelica"), norm)
    if norm == "load_file":
        if not fp:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "file_path is required for action=load_file",
                }
            )
        return _mm_attach_action(
            _mm_load_file(
                fp,
                auto_load_deps=auto_load_deps,
                skip_if_unchanged=skip_if_unchanged,
                force_reload=force_reload,
            ),
            norm,
        )
    if norm == "unload":
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name is required for action=unload",
                }
            )
        return _mm_attach_action(_mm_unload(mn), norm)
    if norm == "save":
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name is required for action=save",
                }
            )
        return _mm_attach_action(_mm_save(mn, folder=folder or "", save_type=int(save_type)), norm)
    if norm == "export_model_diagram":
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name is required for action=export_model_diagram",
                }
            )
        return _mm_attach_action(
            _mm_export_model_diagram(
                mn,
                output_path=output_path or "",
                width=int(width),
                height=int(height),
                open_model_first=bool(open_model_first),
            ),
            norm,
        )
    if norm == "lookup_component":
        if not mn or not cn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name and comp_name are required for action=lookup_component",
                }
            )
        return _mm_attach_action(_mm_lookup_component(mn, cn, info_type=info_type or ""), norm)
    if norm == "get_components":
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name is required for action=get_components",
                }
            )
        return _mm_attach_action(_mm_get_components(mn, component=comp), norm)
    if norm == "get_component_ports":
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name is required for action=get_component_ports",
                }
            )
        return _mm_attach_action(
            _mm_get_component_ports(mn, cname, port_direction=int(port_direction)),
            norm,
        )
    if norm == "get_model_text":
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name is required for action=get_model_text",
                }
            )
        return _mm_attach_action(_mm_get_model_text(mn), norm)
    if norm == "get_model_description":
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name is required for action=get_model_description",
                }
            )
        return _mm_attach_action(_mm_get_model_description(mn), norm)
    if norm == "get_component_description":
        if not mn or not cn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name and comp_name are required for action=get_component_description",
                }
            )
        return _mm_attach_action(_mm_get_component_description(mn, cn), norm)
    if norm == "get_classes":
        if not mn:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_model_manager",
                    "manager_action": norm,
                    "error": "model_name is required for action=get_classes",
                }
            )
        return _mm_attach_action(_mm_get_classes(mn), norm)

    return _json({"ok": False, "tool": "mworks_sysplorer_model_manager", "error": "internal dispatch error"})


def _reload_mo_via_model_manager(mo_path: str) -> Tuple[bool, Dict[str, Any]]:
    """与 ``mworks_sysplorer_model_manager(action=load_file, force_reload=True)`` 同路径，刷新磁盘写回后的模型与 Diagram。"""
    p = (mo_path or "").strip()
    if not p:
        return True, {"ok": True, "api": "OpenModelFile", "skipped": True, "reason": "empty mo_path"}
    raw = mworks_load_file(
        file_path=p,
        auto_load_deps=False,
        skip_if_unchanged=False,
        force_reload=True,
    )
    meta = json.loads(raw)
    return bool(meta.get("ok", False)), meta


def _norm_mo_path_key(mo_path: str) -> str:
    s = (mo_path or "").strip()
    if not s:
        return ""
    return str(Path(s).resolve())


def _preflight_smart_layout_reload(
    *,
    smart_layout_graph_json: str = "",
    smart_layout_graph_json_path: str = "",
    smart_layout_model_path: str = "",
    reload_mo_path: str = "",
    layout_output_json_path: str = "",
    timeout_seconds: int = 120,
    model_name_hint: str = "",
    auto_generate_graph: bool = True,
) -> Tuple[bool, List[Dict[str, Any]], str]:
    """
    在检查 / 翻译 / 仿真之前：若提供 graph 或开启自动生成，则 Smart Layout 写回目标 ``.mo``，
    再通过 ``mworks_load_file(..., force_reload=True)``（与模型管理 ``load_file`` 同路径）强制重载，使 Sysplorer 刷新 Diagram。
    若另有 ``reload_mo_path`` 且与已重载路径不同，再追加一次重载。
    无 graph 且未开启自动生成时，行为与仅传 ``reload_mo_path`` 时一致（只重载）。
    """
    steps: List[Dict[str, Any]] = []
    gj = (smart_layout_graph_json or "").strip()
    gjp = (smart_layout_graph_json_path or "").strip()
    mo_sl = (smart_layout_model_path or "").strip()
    rp = (reload_mo_path or "").strip()
    reloaded: set[str] = set()

    write_mo = mo_sl or rp
    # 条件：要么有graph，要么开启自动生成且有目标mo文件
    if (gj or gjp) or (auto_generate_graph and write_mo):
        if not write_mo:
            return False, [], "smart_layout graph 已提供但未设置 smart_layout_model_path 或 reload_mo_path"
        from tools.layout import run_smart_layout_for_fast_workflow

        sok, sdata = run_smart_layout_for_fast_workflow(
            graph_json=gj,
            graph_json_path=gjp,
            model_output_path=write_mo,
            model_name=(model_name_hint or "").strip(),
            layout_output_json_path=(layout_output_json_path or "").strip(),
            timeout_seconds=int(timeout_seconds),
            auto_generate_graph=auto_generate_graph,
        )
        row_sl: Dict[str, Any] = {
            "kind": "smart_layout_writeback",
            "ok": sok,
            "target": write_mo,
        }
        if sdata.get("skipped"):
            row_sl["skipped"] = True
            row_sl["reason"] = sdata.get("reason", "")
        elif sok:
            row_sl["components_updated"] = sdata.get("components_updated")
            row_sl["connects_updated"] = sdata.get("connects_updated")
        else:
            row_sl["error"] = sdata.get("error", "")
        steps.append(row_sl)
        if not sok:
            return False, steps, row_sl.get("error") or "smart_layout writeback failed"
        rr_ok, rj = _reload_mo_via_model_manager(write_mo)
        steps.append({"kind": "reload_mo", "ok": rr_ok, "target": write_mo, "api_meta": rj})
        if not rr_ok:
            return False, steps, f"smart_layout 后重载失败: {rj.get('error', '')}"
        k = _norm_mo_path_key(write_mo)
        if k:
            reloaded.add(k)

    rp_key = _norm_mo_path_key(rp)
    if rp_key and rp_key not in reloaded:
        rr2_ok, rj2 = _reload_mo_via_model_manager(rp)
        steps.append({"kind": "reload_mo", "ok": rr2_ok, "target": rp, "api_meta": rj2})
        if not rr2_ok:
            return False, steps, f"reload_mo_path 重载失败: {rj2.get('error', '')}"

    return True, steps, ""


def _last_reload_api_meta_from_preflight(steps: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for s in reversed(steps):
        if s.get("kind") == "reload_mo" and isinstance(s.get("api_meta"), dict):
            return s["api_meta"]
    return None


def _sysplorer_check_models_payload(
    names: List[str],
    model_type: str = "MODELICA",
    stop_on_error: bool = False,
    reload_mo_path: str = "",
    smart_layout_graph_json: str = "",
    smart_layout_graph_json_path: str = "",
    smart_layout_model_path: str = "",
    smart_layout_output_json_path: str = "",
    smart_layout_timeout_seconds: int = 120,
) -> Dict[str, Any]:
    started = time.perf_counter()
    rows: List[Dict[str, Any]] = []
    driver = _get_driver()
    pf_ok, pf_steps, pf_err = _preflight_smart_layout_reload(
        smart_layout_graph_json=smart_layout_graph_json,
        smart_layout_graph_json_path=smart_layout_graph_json_path,
        smart_layout_model_path=smart_layout_model_path,
        reload_mo_path=reload_mo_path,
        layout_output_json_path=smart_layout_output_json_path,
        timeout_seconds=smart_layout_timeout_seconds,
        model_name_hint=names[0] if names else "",
        auto_generate_graph=True,
    )
    if not pf_ok:
        out_fail: Dict[str, Any] = {
            "ok": False,
            "tool": "mworks_sysplorer_check_model",
            "model_type": model_type,
            "elapsed_s": round(time.perf_counter() - started, 3),
            "count": 0,
            "results": [],
            "preflight_steps": pf_steps,
            "error": pf_err,
        }
        lm = _last_reload_api_meta_from_preflight(pf_steps)
        if lm is not None:
            out_fail["reload_mo_before"] = lm
        return out_fail
    reload_meta: Optional[Dict[str, Any]] = None
    if pf_steps:
        reload_meta = _last_reload_api_meta_from_preflight(pf_steps)
    for name in names:
        t0 = time.perf_counter()
        result = driver.check_model(model_name=name, model_type=model_type)
        row = json.loads(driver.as_json(result))
        row["model_name"] = name
        row["dt_s"] = round(time.perf_counter() - t0, 3)
        rows.append(row)
        if stop_on_error and not bool(row.get("ok", False)):
            break
    out: Dict[str, Any] = {
        "ok": all(bool(x.get("ok", False)) for x in rows),
        "tool": "mworks_sysplorer_check_model",
        "model_type": model_type,
        "elapsed_s": round(time.perf_counter() - started, 3),
        "count": len(rows),
        "results": rows,
    }
    if pf_steps:
        out["preflight_steps"] = pf_steps
    if reload_meta is not None:
        out["reload_mo_before"] = reload_meta
    return out


@mcp.tool()
def mworks_sysplorer_check_model(
    model_names: Optional[List[str]] = None,
    model_name: str = "",
    model_type: str = "MODELICA",
    stop_on_error: bool = False,
    reload_mo_path: str = "",
    smart_layout_graph_json: str = "",
    smart_layout_graph_json_path: str = "",
    smart_layout_model_path: str = "",
    smart_layout_output_json_path: str = "",
    smart_layout_timeout_seconds: int = 120,
) -> str:
    """在 Sysplorer 中对一个或多个模型执行检查（实例化/编译）。传 model_names，或仅传单个 model_name。

    在检查前可先做 Smart Layout 写回并重载：提供 ``smart_layout_graph_json`` 或 ``smart_layout_graph_json_path``，
    并设置 ``smart_layout_model_path`` 或 ``reload_mo_path`` 指向目标 ``.mo``（与 ``mworks_sysplorer_call_code`` 的 ``fast_workflow`` 模式一致）。

    ``reload_mo_path`` 非空时：在无 graph 时仅执行强制重载；有 graph 时通常在写回后已重载，若路径不同会再重载一次。
    """
    try:
        names = [str(x).strip() for x in (model_names or []) if str(x).strip()]
        one = (model_name or "").strip()
        if one:
            names.append(one)
        # 去重且保序
        seen: set[str] = set()
        uniq: List[str] = []
        for n in names:
            if n not in seen:
                seen.add(n)
                uniq.append(n)
        names = uniq
        if not names:
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_check_model",
                    "error": "Provide model_names (non-empty list) and/or a non-empty model_name",
                }
            )
        return _json(
            _sysplorer_check_models_payload(
                names,
                model_type=model_type,
                stop_on_error=stop_on_error,
                reload_mo_path=str(reload_mo_path or "").strip(),
                smart_layout_graph_json=str(smart_layout_graph_json or "").strip(),
                smart_layout_graph_json_path=str(smart_layout_graph_json_path or "").strip(),
                smart_layout_model_path=str(smart_layout_model_path or "").strip(),
                smart_layout_output_json_path=str(smart_layout_output_json_path or "").strip(),
                smart_layout_timeout_seconds=int(smart_layout_timeout_seconds),
            )
        )
    except Exception as exc:
        return _json({"ok": False, "tool": "mworks_sysplorer_check_model", "api": "checkModelEx", "error": str(exc)})


@mcp.tool()
def mworks_sysplorer_translate_model(
    model_name: str,
    code_folder: str = TEMP_CODE_FOLDER,
    model_type: str = "MODELICA",
    code_type: str = "NORMAL",
    build_type: str = "BINARY",
    run_to: str = "MAKING",
    config_json: str = "",
    reload_mo_path: str = "",
    smart_layout_graph_json: str = "",
    smart_layout_graph_json_path: str = "",
    smart_layout_model_path: str = "",
    smart_layout_output_json_path: str = "",
    smart_layout_timeout_seconds: int = 120,
) -> str:
    """在 Sysplorer 中翻译模型（生成仿真代码等），底层为官方 TranslateModel API。

    翻译前先执行与检查接口相同的预检：可选 Smart Layout 写回 + 强制重载目标 ``.mo``（参数同 ``mworks_sysplorer_check_model``）。
    """
    try:
        driver = _get_driver()
        mn = (model_name or "").strip()
        rp = (reload_mo_path or "").strip()
        gj = (smart_layout_graph_json or "").strip()
        gjp = (smart_layout_graph_json_path or "").strip()
        if not mn and (rp or gj or gjp):
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_translate_model",
                    "error": "model_name 不能为空（在需要重载或 Smart Layout 时亦必填）",
                }
            )
        pf_ok, pf_steps, pf_err = _preflight_smart_layout_reload(
            smart_layout_graph_json=gj,
            smart_layout_graph_json_path=gjp,
            smart_layout_model_path=str(smart_layout_model_path or "").strip(),
            reload_mo_path=rp,
            layout_output_json_path=str(smart_layout_output_json_path or "").strip(),
            timeout_seconds=int(smart_layout_timeout_seconds),
            model_name_hint=mn,
            auto_generate_graph=True,
        )
        if not pf_ok:
            out_pf: Dict[str, Any] = {
                "ok": False,
                "tool": "mworks_sysplorer_translate_model",
                "preflight_steps": pf_steps,
                "error": pf_err,
            }
            lm = _last_reload_api_meta_from_preflight(pf_steps)
            if lm is not None:
                out_pf["reload_mo_before"] = lm
            return _json(out_pf)
        reload_meta: Optional[Dict[str, Any]] = _last_reload_api_meta_from_preflight(pf_steps)
        result = driver.translate_model(
            model_name=model_name,
            code_folder=code_folder,
            model_type=model_type,
            code_type=code_type,
            build_type=build_type,
            run_to=run_to,
            config_json=config_json,
        )
        out = json.loads(driver.as_json(result))
        if pf_steps:
            out["preflight_steps"] = pf_steps
        if reload_meta is not None:
            out["reload_mo_before"] = reload_meta
        return _json(out)
    except Exception as exc:
        return _json(
            {
                "ok": False,
                "tool": "mworks_sysplorer_translate_model",
                "api": "TranslateModel",
                "error": str(exc),
            }
        )


def _apply_official_result_verification(
    driver: Any,
    out: Dict[str, Any],
    *,
    verify_result_var: str,
    verify_time_point: Any,
    result_var_type: int,
) -> None:
    """Augment SimulateModel JSON with GetResultVariableInfo probes + optional GetVarValueAt (mutates out).

    Avoids ``GetResultVariables`` (often huge); uses ``GetResultVariableInfo`` to confirm the
    session has readable results and that ``verify_result_var`` exists when specified.
    ``result_var_type`` is kept for API compatibility but no longer drives verification.
    """
    sim_reported_ok = bool(out.get("ok", False))
    sim_err = str(out.get("error", "") or "")

    var_name = (verify_result_var or "").strip()
    probe_target = var_name if var_name else "time"
    info_r = driver.get_result_variable_info(probe_target, "Type")
    has_results = bool(
        info_r.ok and info_r.data is not None and str(info_r.data).strip() != ""
    )
    grv_block: Dict[str, Any] = {
        "ok": info_r.ok,
        "api": "GetResultVariableInfo",
        "probe_var": probe_target,
        "info_type": "Type",
        "has_readable_result": has_results,
        "result_var_type_unused": int(result_var_type),
        "note": "仿真结果存在性通过 GetResultVariableInfo 探测，未调用 GetResultVariables 全量列表。",
    }
    if info_r.ok and info_r.data is not None:
        grv_block["data"] = info_r.data
    elif info_r.error:
        grv_block["error"] = info_r.error

    rv: Dict[str, Any] = {"result_probe": grv_block}

    run_gv = bool(var_name and has_results)
    gv_blk: Optional[Dict[str, Any]] = None
    if var_name:
        if run_gv:
            gv = driver.get_var_value_at(var_name, verify_time_point)
            gv_blk = {
                "ok": gv.ok,
                "api": "GetVarValueAt",
                "var_name": var_name,
                "time_point": verify_time_point,
            }
            if gv.ok:
                gv_blk["data"] = gv.data
            elif gv.error:
                gv_blk["error"] = gv.error
            rv["get_var_value_at"] = gv_blk
        else:
            rv["get_var_value_at"] = {
                "ok": False,
                "api": "GetVarValueAt",
                "skipped": True,
                "reason": "GetResultVariableInfo 未确认该变量在当前结果中，未调用 GetVarValueAt",
                "var_name": var_name,
                "time_point": verify_time_point,
            }
            gv_blk = rv["get_var_value_at"]

    if sim_reported_ok:
        if not info_r.ok:
            out["ok"] = False
            out["error"] = f"SimulateModel 返回成功，但 GetResultVariableInfo 失败：{info_r.error or 'unknown'}"
        elif not has_results:
            out["ok"] = False
            out["error"] = (
                "SimulateModel 返回成功，但 GetResultVariableInfo 未确认可读结果变量 "
                f"({probe_target!r})；请检查会话结果或改用 verify_result_var 指定已知变量。"
            )
        elif var_name and gv_blk is not None:
            if gv_blk.get("skipped"):
                out["ok"] = False
                out["error"] = (
                    "已指定 verify_result_var，但 GetResultVariableInfo 未确认该变量存在于当前结果；"
                    "请核对变量全名或先对目标模型执行 get_result_variables(model_name=…)。"
                )
            elif not gv_blk.get("ok"):
                out["ok"] = False
                out["error"] = (
                    f"变量已在结果中，但 GetVarValueAt({var_name!r}) 失败：{gv_blk.get('error', 'unknown')}"
                )
            elif gv_blk.get("data") is None:
                out["ok"] = False
                out["error"] = (
                    f"GetVarValueAt({var_name!r}) 返回值为空，无法在指定时刻确认仿真数据。"
                )
            else:
                out["ok"] = True
        else:
            out["ok"] = True
    else:
        if has_results:
            if var_name and gv_blk is not None and not gv_blk.get("skipped"):
                if gv_blk.get("ok") and gv_blk.get("data") is not None:
                    out["ok"] = True
                    out["warning"] = (
                        "SimulateModel 返回失败，但 GetResultVariableInfo 确认变量存在且 GetVarValueAt 取到数值；"
                        "已按官方结果 API 判定为存在可用结果。"
                    )
                    out["simulate_api_reported_failure"] = True
                    if sim_err:
                        out["simulate_model_error"] = sim_err
                else:
                    out["ok"] = False
                    extra = gv_blk.get("error", "value empty or unknown")
                    out["error"] = (f"{sim_err}; " if sim_err else "") + (
                        f"GetVarValueAt 未确认 {var_name!r} 有值：{extra}"
                    )
            elif not var_name:
                out["ok"] = True
                out["warning"] = (
                    "SimulateModel 返回失败，但 GetResultVariableInfo 显示当前会话存在可读结果；"
                    "可能为本次或其它仿真的残留结果，建议设置 verify_result_var + verify_time_point "
                    "通过 GetVarValueAt 交叉确认。"
                )
                out["simulate_api_reported_failure"] = True
                if sim_err:
                    out["simulate_model_error"] = sim_err
            else:
                out["ok"] = False
                out["error"] = (f"{sim_err}; " if sim_err else "") + (
                    "已指定 verify_result_var，但 GetResultVariableInfo 未确认该变量，未调用 GetVarValueAt。"
                )
        else:
            if not var_name:
                out["ok"] = False
                out["error"] = (
                    (f"{sim_err}; " if sim_err else "")
                    + "SimulateModel 失败且 GetResultVariableInfo 未探测到默认 time 结果；"
                    "可设置 verify_result_var 指向已知结果变量再试。"
                )
            else:
                out["ok"] = False
                out["error"] = (f"{sim_err}; " if sim_err else "") + (
                    "GetResultVariableInfo 未确认 verify_result_var 存在于当前结果。"
                )

    out["result_verification"] = rv


@mcp.tool()
def mworks_sysplorer_simulate_model(
    model_name: str,
    sim_mode: int = 0,
    target_time: Optional[List[float]] = None,
    ext_res_path: str = "",
    verify_result_var: str = "",
    verify_time_point: Any = "end",
    result_var_type: int = 0,
    reload_mo_path: str = "",
    smart_layout_graph_json: str = "",
    smart_layout_graph_json_path: str = "",
    smart_layout_model_path: str = "",
    smart_layout_output_json_path: str = "",
    smart_layout_timeout_seconds: int = 120,
) -> str:
    """在 Sysplorer 中仿真：先 SimulateModel，再用官方 GetResultVariableInfo（及可选 GetVarValueAt）确认结果。

    sim_mode: 0 当前模式；1 独立仿真；2 实时仿真。
    verify_result_var 非空时，先用 GetResultVariableInfo 确认变量存在，再调用 GetVarValueAt；
    未指定时默认探测 ``time``，不调用 GetResultVariables 全量列表。
    仿真前预检：可选 Smart Layout 写回 + 重载（参数同 ``mworks_sysplorer_check_model``）；无 graph 时 ``reload_mo_path`` 仅触发重载。
    """
    try:
        sim_mode_safe = sim_mode
        driver = _get_driver()
        rp = (reload_mo_path or "").strip()
        mn = (model_name or "").strip()
        gj = (smart_layout_graph_json or "").strip()
        gjp = (smart_layout_graph_json_path or "").strip()
        if not mn and (rp or gj or gjp):
            return _json(
                {
                    "ok": False,
                    "tool": "mworks_sysplorer_simulate_model",
                    "error": "model_name 不能为空（在需要重载或 Smart Layout 时亦必填）",
                }
            )
        pf_ok, pf_steps, pf_err = _preflight_smart_layout_reload(
            smart_layout_graph_json=gj,
            smart_layout_graph_json_path=gjp,
            smart_layout_model_path=str(smart_layout_model_path or "").strip(),
            reload_mo_path=rp,
            layout_output_json_path=str(smart_layout_output_json_path or "").strip(),
            timeout_seconds=int(smart_layout_timeout_seconds),
            model_name_hint=mn,
            auto_generate_graph=True,
        )
        if not pf_ok:
            out_pf: Dict[str, Any] = {
                "ok": False,
                "tool": "mworks_sysplorer_simulate_model",
                "preflight_steps": pf_steps,
                "error": pf_err,
            }
            lm = _last_reload_api_meta_from_preflight(pf_steps)
            if lm is not None:
                out_pf["reload_mo_before"] = lm
            return _json(out_pf)
        reload_meta: Optional[Dict[str, Any]] = _last_reload_api_meta_from_preflight(pf_steps)
        result = driver.simulate_model(
            model_name=model_name,
            sim_mode=sim_mode_safe,
            target_time=target_time or [],
            ext_res_path=ext_res_path,
        )
        out = json.loads(driver.as_json(result))
        out["sim_mode"] = sim_mode_safe
        if pf_steps:
            out["preflight_steps"] = pf_steps
        if reload_meta is not None:
            out["reload_mo_before"] = reload_meta
        _apply_official_result_verification(
            driver,
            out,
            verify_result_var=verify_result_var,
            verify_time_point=verify_time_point,
            result_var_type=result_var_type,
        )
        return _json(out)
    except Exception as exc:
        return _json(
            {
                "ok": False,
                "tool": "mworks_sysplorer_simulate_model",
                "api": "SimulateModel",
                "error": str(exc),
            }
        )


def mworks_set_model_param(
    model_name: str,
    param_name: str,
    value: str,
    component: str = "",
) -> str:
    """
    Set a parameter value on a loaded Modelica model (driver ``SetModelParamValue``).

    **MCP**：请使用 ``mworks_sysplorer_call_code(mode=\"run_with_ready\", payload={\"action\": \"set_model_param\", \"payload\": {...}})``，
    与 ``run_script`` 程序化建图同一入口，不再注册独立工具。

    - model_name: fully-qualified model class name
    - param_name: parameter name (e.g. "m", "L")
    - value: new value as string (e.g. "1.5", "true")
    - component: sub-component path owning the parameter; leave empty for top-level params
    """
    try:
        result = _get_driver().set_model_param(
            model_name=model_name,
            param_name=param_name,
            value=value,
            component=component,
        )
        return _get_driver().as_json(result)
    except Exception as exc:
        return _json({"ok": False, "api": "SetModelParamValue", "error": str(exc)})
