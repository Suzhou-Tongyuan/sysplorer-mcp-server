"""Sysplorer session MCP tool — official API only (Find/Connect/Start/Exit).

**启动策略（硬性）**：在本仓库 MCP 服务端中，**禁止**用 ``subprocess`` / ``os.startfile`` /
按进程名拉起 ``mworks.exe`` / PowerShell ``Start-Process`` 等方式启动 Sysplorer。
**唯一允许**的启动入口为官方 ``mworks.sysplorer.StartSysplorer``（由 ``MWorksDriver``
在需要拉起进程时调用；``processPath`` 仅为该 API 的参数）。
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from mcp_instance import mcp
from mworks_driver import MWorksDriver
from core.utils import _json
from path_config import DEPLOY_ROOT, WORKSPACE_ROOT, get_resources_root
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
    }
    return aliases.get(raw, raw)


def _paths_block() -> Dict[str, str]:
    return {
        "workspace_root": str(WORKSPACE_ROOT.resolve()),
        "deploy_root": str(DEPLOY_ROOT.resolve()),
        "resources_root": str(get_resources_root().resolve()),
    }


@mcp.tool()
def mworks_sysplorer_session_manager(
    action: str = "health",
    wait_seconds: int = 45,
    restart_mode: str = "reconnect",
    exit_port: Optional[int] = None,
) -> str:
    """
    Sysplorer session lifecycle via official API: FindSysplorer → ConnectSysplorer(port)
    or StartSysplorer; shutdown uses Exit().

    **MCP 与 Sysplorer 绑定**：每个 MCP 进程在首次 ``StartSysplorer`` 前记录 FindSysplorer
    端口集合，启动后再次 Find 并与启动前做差分，得到本进程专属端口并写入内存；后续恢复时
    若该端口仍在列表中则只连该端口，否则重新 Start 并更新记录（避免多个 MCP 共连 ``ports[0]``）。

    **启动**：仅通过上述官方 ``StartSysplorer`` 拉起；本工具及关联栈**不会**用进程名或
    ``subprocess`` 直接启动 ``mworks.exe``。

    action (aliases in parentheses):
      version (mcp_version) — 仅返回当前 MCP 服务端版本与构建元数据，不连接 Sysplorer。
      health (status) — Python/paths + obtain driver (triggers recovery if needed).
      probe — read-only: FindSysplorer ports + cached driver probe; no recovery.
      ensure (start, connect) — ensure_healthy().
      restart (soft_restart) — drop singleton and reconnect; restart_mode=reconnect|full_reset.
      force_restart — Exit all instances then StartSysplorer (same as restart full_reset).
      shutdown (close, exit) — Exit(); optional exit_port for one instance.

    wait_seconds is reserved for future connect/start polling (currently unused).
    """
    _ = wait_seconds  # reserved for polling budgets
    act = _normalize_session_action(action)

    if act == "version":
        return _json(
            {
                "ok": True,
                "tool": "mworks_sysplorer_session_manager",
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
                "tool": "mworks_sysplorer_session_manager",
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
            "sysplorer_startup": _stack_health.startup_state,
            "paths": _paths_block(),
        }
        if not py_info["compatible"]:
            data["advice"].append("Use Python 3.11/3.12 for MCP host and Python 3.8 runtime for helper.")
        try:
            driver = _get_driver()
            driver_info = driver.health_check()
            data.update(driver_info)
            data["ok"] = True
            data["driver_ready"] = True
            data["sysplorer_startup"] = _stack_health.startup_state
        except Exception as exc:
            data["driver_error"] = str(exc)
            if _stack_health.driver_error:
                data["driver_error"] = _stack_health.driver_error
            data["advice"].append("Set MWORKS_BIN64 to your MWorks Bin64 folder if needed.")
            data["sysplorer_startup"] = _stack_health.startup_state
        return _json(data)

    if act == "ensure":
        result: Dict[str, Any] = {
            "ok": False,
            "tool": "mworks_sysplorer_session_manager",
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
            "tool": "mworks_sysplorer_session_manager",
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
            "tool": "mworks_sysplorer_session_manager",
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
            reset_session_caches()
            result["driver_ready"] = False
        except Exception as exc:
            result["driver_error"] = str(exc)
        return _json(result)

    return _json(
        {
            "ok": False,
            "tool": "mworks_sysplorer_session_manager",
            "action": act,
            "mcp_server": get_version_info(),
            "error": f"Unknown action: {action!r} (use version|health|probe|ensure|restart|force_restart|shutdown)",
        }
    )
