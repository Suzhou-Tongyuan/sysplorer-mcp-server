"""Sysplorer-related OS process helpers.

**MCP 会话生命周期**（`StackHealthManager` / `mworks_sysplorer_session_manager`）仅使用官方
``FindSysplorer`` / ``ConnectSysplorer`` / ``StartSysplorer`` / ``Exit``，不依赖本模块。

**禁止**：本模块**不得**用于启动 Sysplorer；不得以进程名 / ``taskkill`` 的反面逻辑
“代劳启动”。**唯一允许**的启动方式仍是官方 ``StartSysplorer``（见 ``mworks_driver``）。

本模块保留 ``kill_all`` 等能力供需要时**强制清理残留 OS 进程**（先对已知端口走 ``Exit()``，
再按进程名 ``taskkill``/``kill``）；默认自动化路径不应依赖进程名发现 Sysplorer 实例。
"""
from __future__ import annotations

import os
import platform
import subprocess
import time
import threading
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol

from mworks_driver import find_sysplorer_ports, shutdown_all_sysplorer_via_exit


# ── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class StackProcessStatus:
    """Snapshot of Sysplorer stack availability (from official FindSysplorer)."""

    gui_alive: bool = False
    compiler_alive: bool = False
    solver_alive: bool = False
    timestamp: float = 0.0
    #: Ports returned by ``FindSysplorer()`` for each fully running instance (may be empty).
    sysplorer_ports: List[int] = field(default_factory=list)

    @property
    def full_stack_alive(self) -> bool:
        return self.gui_alive and self.compiler_alive and self.solver_alive

    @property
    def any_alive(self) -> bool:
        return self.gui_alive or self.compiler_alive or self.solver_alive


@dataclass
class KillResult:
    killed: Dict[str, List[int]] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    #: Populated when ``include_gui=True``: result of ``shutdown_all_sysplorer_via_exit``.
    exit_api: Dict[str, Any] = field(default_factory=dict)


# ── Protocol for dependency injection in tests ───────────────────────────────

class ProcessManagerProtocol(Protocol):
    def full_stack_status(self) -> StackProcessStatus: ...
    def kill_all(self, include_gui: bool = True) -> KillResult: ...
    def invalidate_cache(self) -> None: ...


# ── Platform-specific configuration ──────────────────────────────────────────

IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MACOS = platform.system() == "Darwin"

# 不同平台的进程名定义
if IS_WINDOWS:
    _PROC_GUI = "mworks.exe"
    _PROC_COMPILER = "mols.exe"
    _PROC_SOLVER = "mwsolver.exe"
else:
    # Linux/macOS 无.exe后缀
    _PROC_GUI = "mworks"
    _PROC_COMPILER = "mols"
    _PROC_SOLVER = "mwsolver"

_PROC_NAMES = (_PROC_GUI, _PROC_COMPILER, _PROC_SOLVER)
_BACKEND_NAMES = (_PROC_COMPILER, _PROC_SOLVER)
_CACHE_TTL = 3.0  # seconds


# ── Implementation ───────────────────────────────────────────────────────────

class ProcessManager:
    """Query running Sysplorer instances (``FindSysplorer``) and kill OS processes.

    Uses a TTL cache so multiple callers within ~3s only invoke ``FindSysplorer`` once.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._cached: Optional[StackProcessStatus] = None

    def full_stack_status(self) -> StackProcessStatus:
        """查询所有Sysplorer进程状态，带3s TTL缓存."""
        with self._lock:
            now = time.monotonic()
            if self._cached is not None and (now - self._cached.timestamp) < _CACHE_TTL:
                return self._cached

        # Run outside the lock to avoid blocking other threads during I/O
        status = self._query_processes()
        with self._lock:
            self._cached = status
        return status

    def kill_all(self, include_gui: bool = True) -> KillResult:
        """杀死所有Sysplorer相关进程.

        When ``include_gui`` is True, first attempts official ``Exit()`` on each
        port reported by ``FindSysplorer``, then force-kills OS processes as a
        fallback.  Backend-only kills skip ``Exit()`` so a running GUI is not
        closed by this path.

        Args:
            include_gui: 是否包含主界面进程(mworks/mworks.exe)，False表示只杀后台服务进程
        """
        result = KillResult()

        if include_gui:
            try:
                result.exit_api = shutdown_all_sysplorer_via_exit()
                if not result.exit_api.get("ok", True):
                    for err in result.exit_api.get("errors", []):
                        result.errors.append(f"Exit API: {err}")
            except Exception as exc:
                result.exit_api = {"ok": False, "exited_ports": [], "errors": [str(exc)]}
                result.errors.append(f"Exit API: {exc}")
            time.sleep(1.0)

        targets = list(_PROC_NAMES) if include_gui else list(_BACKEND_NAMES)

        for proc_name in targets:
            try:
                pids = self._get_pids(proc_name)
                if not pids:
                    continue

                result.killed[proc_name] = []
                for pid in pids:
                    try:
                        self._kill_pid(pid)
                        result.killed[proc_name].append(pid)
                    except Exception as exc:
                        result.errors.append(f"kill {proc_name}:{pid} failed: {exc}")
            except Exception as exc:
                result.errors.append(f"list {proc_name} failed: {exc}")

        self.invalidate_cache()
        return result

    def invalidate_cache(self) -> None:
        """清空进程状态缓存."""
        with self._lock:
            self._cached = None

    # ── Platform-specific internal methods ───────────────────────────────────

    @staticmethod
    def _query_processes() -> StackProcessStatus:
        """Detect fully running Sysplorer instances via official ``FindSysplorer``."""
        status = StackProcessStatus(timestamp=time.monotonic())
        try:
            ports = find_sysplorer_ports()
        except Exception:
            ports = []
        status.sysplorer_ports = list(ports)
        if ports:
            # API reports complete running instances; treat stack as fully up for health classification.
            status.gui_alive = True
            status.compiler_alive = True
            status.solver_alive = True
        return status

    @staticmethod
    def _get_pids(proc_name: str) -> List[int]:
        """获取指定进程名的所有PID，跨平台实现."""
        pids: List[int] = []
        if IS_WINDOWS:
            # Windows 使用 wmic 查询PID
            r = subprocess.run(
                ["wmic", "process", "where", f"name='{proc_name}'", "get", "processid"],
                capture_output=True, text=True, timeout=8,
            )
            pids = [int(tok.strip()) for tok in r.stdout.split() if tok.strip().isdigit()]
        else:
            # Linux/macOS 使用 pgrep 查询PID
            try:
                r = subprocess.run(
                    ["pgrep", proc_name],
                    capture_output=True, text=True, timeout=8,
                )
                pids = [int(line.strip()) for line in r.stdout.strip().split('\n') if line.strip()]
            except subprocess.CalledProcessError:
                # pgrep返回非零表示没有找到进程，返回空列表
                pass
        return pids

    @staticmethod
    def _kill_pid(pid: int) -> None:
        """杀死指定PID的进程，跨平台实现."""
        if IS_WINDOWS:
            subprocess.run(
                ["taskkill", "/F", "/PID", str(pid)],
                capture_output=True, timeout=5,
                check=True
            )
        else:
            # Linux/macOS 使用 kill -9
            subprocess.run(
                ["kill", "-9", str(pid)],
                capture_output=True, timeout=5,
                check=True
            )
