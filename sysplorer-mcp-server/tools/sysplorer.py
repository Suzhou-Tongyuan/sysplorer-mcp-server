"""Sysplorer session MCP tool — official API only (Find/Connect/Start/Exit).

**启动策略（硬性）**：在本仓库 MCP 服务端中，**禁止**用 ``subprocess`` / ``os.startfile`` /
按进程名拉起 ``mworks.exe`` / PowerShell ``Start-Process`` 等方式启动 Sysplorer。
**唯一允许**的启动入口为官方 ``mworks.sysplorer.StartSysplorer``（由 ``MWorksDriver``
在需要拉起进程时调用；``processPath`` 仅为该 API 的参数）。
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from mcp_instance import mcp, writable_annotations
from mworks_driver import MWorksDriver
from core.utils import _json
from path_config import (
    DEPLOY_ROOT,
    MWORKS_SIM_DIR,
    USER_WORKSPACE_ROOT,
    WORKSPACE_ROOT,
    dependency_downloads_enabled,
    get_resources_root,
    library_download_tools_enabled,
)
from state import _get_driver, _stack_health, reset_session_caches
from version import get_version_info


def _normalize_session_action(action: str) -> str:
    raw = (action or "health").strip().lower()
    aliases = {
        "status": "health",
        "start": "ensure",
        "connect": "ensure",
        "soft_restart": "restart",
        "close": "shutdown",
        "exit": "shutdown",
        "mcp_version": "version",
        "workdir": "get_directory",
        "working_dir": "get_directory",
        "working_directory": "get_directory",
        "get_workdir": "get_directory",
        "getdirectory": "get_directory",
        "sim_result_dir": "get_sim_result_directory",
        "sim_dir": "get_sim_result_directory",
        "get_sim_dir": "get_sim_result_directory",
        "getsimresultdirectory": "get_sim_result_directory",
        "sim_result_directory": "get_sim_result_directory",
        "installed_libraries": "get_installed_libraries",
        "list_installed_libraries": "get_installed_libraries",
        "getinstalledlibraries": "get_installed_libraries",
        "installed": "get_installed_libraries",
        "loaded_models": "get_loaded_models",
        "list_loaded_models": "get_loaded_models",
        "getloadedmodels": "get_loaded_models",
        "loaded": "get_loaded_models",
    }
    return aliases.get(raw, raw)


def _paths_block() -> Dict[str, Any]:
    paths: Dict[str, Any] = {
        "workspace_root": str(WORKSPACE_ROOT.resolve()),
        "user_workspace_root": str(USER_WORKSPACE_ROOT.resolve()) if USER_WORKSPACE_ROOT is not None else "",
        "deploy_root": str(DEPLOY_ROOT.resolve()),
        "resources_root": str(get_resources_root().resolve()),
    }
    # Full Sysplorer: do not expose the download flag — agents misread false as “no TA/Modelica libs”.
    if library_download_tools_enabled():
        paths["dependency_download_enabled"] = dependency_downloads_enabled()
        paths["library_load_policy"] = (
            "try load_library(action=load) first; "
            "after a failed load use library_prepare; "
            "dependency_download_enabled=false only gates remote install, not local libraries"
        )
    return paths


def _paths_aligned(left: str, right: Path) -> bool:
    try:
        return Path(left).expanduser().resolve() == right.expanduser().resolve()
    except OSError:
        a = left.replace("\\", "/").rstrip("/")
        b = str(right).replace("\\", "/").rstrip("/")
        return a == b


def _live_directory_payload(
    *,
    action: str,
    api: str,
    getter_name: str,
    aligned_field: str,
    compare_to: Path,
    note: str,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "ok": False,
        "tool": "session_manager",
        "action": action,
        "api": api,
        "mcp_server": get_version_info(),
        "directory": "",
        "paths": _paths_block(),
        aligned_field: False,
        "note": note,
        "driver_error": "",
    }
    if extra:
        data.update(extra)
    try:
        result = getattr(_get_driver(), getter_name)()
        raw = result.data if result.ok else None
        directory = str(raw or "").strip()
        if result.ok and directory:
            data["ok"] = True
            data["directory"] = directory
            data[aligned_field] = _paths_aligned(directory, compare_to)
        else:
            data["driver_error"] = result.error or f"{api} returned an empty path"
            if result.warning:
                data["warning"] = result.warning
    except Exception as exc:
        data["driver_error"] = str(exc)
        if _stack_health.driver_error:
            data["driver_error"] = _stack_health.driver_error
    return data


@mcp.tool(annotations=writable_annotations())
def session_manager(
    action: str = "health",
    wait_seconds: int = 45,
    restart_mode: str = "reconnect",
    exit_port: Optional[int] = None,
) -> str:
    """Sysplorer session: start/connect, health, directories, installed/loaded lists.

    MCP path split: get_directory / get_sim_result_directory are Sysplorer dirs;
    paths.workspace_root is the MCP project root and may differ. Do not use
    ChangeDirectory / ChangeSimResultDirectory / ClearAll. Attach
    (SYSPLORER_API_PORT) blocks shutdown / force_restart / restart(full_reset).
    get_loaded_models is one package child layer; deeper via model_inspect get_classes.

    | action | notes |
    |--------|-------|
    | ``health`` / ``probe`` / ``version`` | status; ``version`` does not connect. ``health`` Connects if a port is already up; otherwise StartSysplorer runs in the background and this call returns ``starting`` so the client does not time out |
    | ``get_directory`` / ``get_sim_result_directory`` | official GetDirectory / GetSimResultDirectory |
    | ``get_installed_libraries`` / ``get_loaded_models`` | snapshots (loaded models: top + one package layer) |
    | ``ensure`` / ``restart`` / ``shutdown`` | attach mode blocks Exit / full_reset |
    """
    act = _normalize_session_action(action)
    _ = wait_seconds

    if act == "version":
        return _json(
            {
                "ok": True,
                "tool": "session_manager",
                "action": "version",
                "mcp_server": get_version_info(),
            }
        )

    if act == "probe":
        snap = _stack_health.probe_snapshot()
        py_info = MWorksDriver.python_compatibility()
        return _json(
            {
                "ok": True,
                "tool": "session_manager",
                "action": act,
                "mcp_server": get_version_info(),
                "python": py_info,
                "paths": _paths_block(),
                "probe": snap,
                "sysplorer_startup": _stack_health.startup_state,
            }
        )

    if act == "health":
        py_info = MWorksDriver.python_compatibility()
        data: Dict[str, Any] = {
            "ok": False,
            "mcp_server": get_version_info(),
            "python": py_info,
            "driver_ready": False,
            "driver_error": "",
            "advice": [],
            "starting": False,
            "sysplorer_startup": _stack_health.startup_state,
            "paths": _paths_block(),
        }
        if not py_info["compatible"]:
            data["advice"].append("Use Python 3.11/3.12 for MCP host and Python 3.8 runtime for helper.")
        retry_health = (
            "Retry session_manager(action=health). Do not call ensure/restart "
            "or reload MCP while the window is coming up — that starts a second GUI."
        )
        try:
            if _stack_health.startup_in_progress and not _stack_health.instance_is_visible():
                data["starting"] = True
                data["driver_error"] = (
                    "Sysplorer is starting in the background. " + retry_health
                )
                data["advice"].append(retry_health)
                data["sysplorer_startup"] = _stack_health.startup_state
                return _json(data)
            if not _stack_health.instance_is_visible() and not _stack_health.attached_to_existing_gui:
                _stack_health.start_in_background()
                data["starting"] = True
                data["driver_error"] = (
                    "StartSysplorer is running in the background. " + retry_health
                )
                data["advice"].append(retry_health)
                data["sysplorer_startup"] = _stack_health.startup_state
                return _json(data)
            driver = _get_driver()
            driver_info = driver.health_check()
            data.update(driver_info)
            data["ok"] = True
            data["driver_ready"] = True
            data["starting"] = False
            data["sysplorer_startup"] = _stack_health.startup_state
        except Exception as exc:
            data["driver_error"] = str(exc)
            if _stack_health.driver_error:
                data["driver_error"] = _stack_health.driver_error
            data["advice"].append("Set MWORKS_BIN64 to your MWorks Bin64 folder if needed.")
            if "FindSysplorer" in data["driver_error"] or "API port" in data["driver_error"]:
                data["advice"].append(
                    "If the Sysplorer window is already visible, retry health only. "
                    "Do not restart MCP or call ensure/restart — that starts a second GUI."
                )
            if (os.environ.get("SYSPLORER_PLATFORM_LABEL") or "").strip().lower() in (
                "modelica_lite",
                "mols",
            ):
                data["advice"] = [
                    "modelica_lite requires SYSPLORER_API_PORT after host starts "
                    "mols.exe --bind-addr 127.0.0.1:<port> (ConnectSysplorer only; no MWORKS_BIN64)."
                ]
            data["sysplorer_startup"] = _stack_health.startup_state
        return _json(data)

    if act == "get_directory":
        return _json(
            _live_directory_payload(
                action="get_directory",
                api="GetDirectory",
                getter_name="get_directory",
                aligned_field="aligned_with_mcp_workspace",
                compare_to=WORKSPACE_ROOT,
                note=(
                    "Sysplorer places user-generated content under this working directory. "
                    "Do not call ChangeDirectory. MCP paths.workspace_root is the agent project root "
                    "and may differ."
                ),
            )
        )

    if act == "get_sim_result_directory":
        return _json(
            _live_directory_payload(
                action="get_sim_result_directory",
                api="GetSimResultDirectory",
                getter_name="get_sim_result_directory",
                aligned_field="aligned_with_mcp_sim_dir",
                compare_to=MWORKS_SIM_DIR,
                extra={"mcp_sim_dir": str(MWORKS_SIM_DIR.expanduser().resolve())},
                note=(
                    "Sysplorer writes simulation result files under this directory "
                    "(GetSimResultDirectory). Do not call ChangeSimResultDirectory, including "
                    "ChangeSimResultDirectory(\"\") which only prints the current path. "
                    "mcp_sim_dir is the MCP default (MWORKS_SIM_DIR) and may differ from the live path."
                ),
            )
        )

    if act == "get_installed_libraries":
        from tools.model_ops import list_installed_libraries_payload

        data = list_installed_libraries_payload(
            tool="session_manager", action="get_installed_libraries"
        )
        data["mcp_server"] = get_version_info()
        data["paths"] = _paths_block()
        return _json(data)

    if act == "get_loaded_models":
        from tools.model_ops import list_loaded_models_payload

        data = list_loaded_models_payload(tool="session_manager", action="get_loaded_models")
        data["mcp_server"] = get_version_info()
        data["paths"] = _paths_block()
        return _json(data)

    if act == "ensure":
        result: Dict[str, Any] = {
            "ok": False,
            "tool": "session_manager",
            "action": act,
            "mcp_server": get_version_info(),
            "sysplorer_startup": {},
            "driver_ready": False,
            "driver_error": "",
        }
        try:
            _stack_health.ensure_healthy()
            result["ok"] = True
            result["driver_ready"] = True
            result["sysplorer_startup"] = _stack_health.startup_state
        except Exception as exc:
            result["driver_error"] = str(exc)
            if _stack_health.driver_error:
                result["driver_error"] = _stack_health.driver_error
            result["sysplorer_startup"] = _stack_health.startup_state
        return _json(result)

    if act == "force_restart":
        act = "restart"
        restart_mode = "full_reset"

    if act == "restart":
        result: Dict[str, Any] = {
            "ok": False,
            "tool": "session_manager",
            "action": "restart",
            "mcp_server": get_version_info(),
            "restart_mode": (restart_mode or "reconnect").strip().lower(),
            "driver_reset": True,
            "sysplorer_startup": {},
            "driver_ready": False,
            "driver_error": "",
        }
        try:
            drv = _stack_health.api_restart(restart_mode=result["restart_mode"])
            reset_session_caches()
            info = drv.health_check()
            result.update(info)
            result["ok"] = True
            result["driver_ready"] = True
            result["driver_error"] = ""
            result["sysplorer_startup"] = _stack_health.startup_state
        except Exception as exc:
            result["driver_error"] = str(exc)
            result["sysplorer_startup"] = _stack_health.startup_state
        return _json(result)

    if act == "shutdown":
        result: Dict[str, Any] = {
            "ok": False,
            "tool": "session_manager",
            "action": "shutdown",
            "mcp_server": get_version_info(),
            "exit_port": exit_port,
            "exit_api": {},
            "driver_ready": False,
            "driver_error": "",
        }
        try:
            exit_api = _stack_health.exit_sessions(exit_port=exit_port)
            result["exit_api"] = exit_api
            result["ok"] = bool(exit_api.get("ok", False))
            if exit_api.get("code"):
                result["code"] = exit_api["code"]
            if exit_api.get("reason"):
                result["error"] = exit_api["reason"]
            reset_session_caches()
            result["driver_ready"] = False
        except Exception as exc:
            result["driver_error"] = str(exc)
        return _json(result)

    return _json(
        {
            "ok": False,
            "tool": "session_manager",
            "action": act,
            "mcp_server": get_version_info(),
            "error": (
                f"Unknown action: {action!r} "
                "(use version|health|probe|get_directory|get_sim_result_directory|"
                "get_installed_libraries|get_loaded_models|ensure|restart|force_restart|shutdown)"
            ),
        }
    )
