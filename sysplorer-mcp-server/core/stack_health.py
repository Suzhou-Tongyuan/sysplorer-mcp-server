"""Sysplorer stack health manager — recovery uses official API only (Find/Connect/Start/Exit).

**启动策略（硬性）**：拉起 Sysplorer 仅通过 ``MWorksDriver(..., force_start=True)`` →
``mworks.sysplorer.StartSysplorer``。禁止在本模块或会话栈内使用 ``subprocess`` /
按进程名等方式直接启动 ``mworks.exe``。
"""
from __future__ import annotations

import logging
import os
import threading
import time
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Dict, Optional, Set

from mworks_driver import (
    MWorksDriver,
    MWorksDriverError,
    find_sysplorer_ports,
    pick_new_sysplorer_port,
    shutdown_all_sysplorer_via_exit,
    exit_sysplorer_on_port,
)
from constants import _SYSPLORER_CONNECT_ERROR_HINTS

log = logging.getLogger(__name__)


class StackHealth(Enum):
    """Stack state derived from FindSysplorer + driver probe only."""

    HEALTHY = auto()
    DRIVER_STALE = auto()  # API reports instance(s) but MCP driver is missing or dead
    NO_INSTANCE = auto()   # FindSysplorer returned no ports


class StackHealthManager:
    """Single authority for Sysplorer health: FindSysplorer / ConnectSysplorer / StartSysplorer / Exit."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._recover_lock = threading.Lock()
        self._driver: Optional[MWorksDriver] = None
        self._driver_error: str = ""
        #: Port returned by FindSysplorer for *this* MCP process's Sysplorer (set after StartSysplorer + diff).
        self._dedicated_sysplorer_port: Optional[int] = None
        self._last_startup_state: Dict[str, Any] = {
            "attempted": False,
            "started": False,
            "already_running": False,
            "wait_ms": 0,
            "error": "",
            "timestamp": "",
        }

    @property
    def driver(self) -> MWorksDriver:
        return self.ensure_healthy()

    @property
    def driver_error(self) -> str:
        return self._driver_error

    @property
    def startup_state(self) -> Dict[str, Any]:
        return dict(self._last_startup_state)

    def assess(self) -> StackHealth:
        """Classify health without side effects (FindSysplorer + optional driver probe)."""
        with self._lock:
            drv = self._driver

        if drv is not None and self._probe_driver(drv):
            return StackHealth.HEALTHY

        try:
            ports = find_sysplorer_ports()
        except Exception:
            ports = []

        if ports:
            return StackHealth.DRIVER_STALE
        return StackHealth.NO_INSTANCE

    def probe_snapshot(self) -> Dict[str, Any]:
        """Read-only snapshot for diagnostics (no recovery)."""
        try:
            ports = find_sysplorer_ports()
        except Exception as exc:
            ports = []
            ports_error = str(exc)
        else:
            ports_error = ""

        with self._lock:
            drv = self._driver
        probe_ok: Optional[bool] = None
        if drv is not None:
            probe_ok = self._probe_driver(drv)

        with self._lock:
            dedicated = self._dedicated_sysplorer_port
        return {
            "find_sysplorer_ports": list(ports),
            "find_sysplorer_error": ports_error,
            "cached_driver_present": drv is not None,
            "cached_driver_probe_ok": probe_ok,
            "dedicated_sysplorer_port": dedicated,
        }

    def ensure_healthy(self) -> MWorksDriver:
        with self._lock:
            if self._driver is not None and self._probe_driver(self._driver):
                return self._driver

        with self._recover_lock:
            with self._lock:
                if self._driver is not None and self._probe_driver(self._driver):
                    return self._driver
            health = self.assess()
            return self._recover(health)

    def api_restart(self, restart_mode: str = "reconnect") -> MWorksDriver:
        """Drop cached connection and re-attach or start.

        reconnect: purge Python singleton, FindSysplorer → ConnectSysplorer(port) or StartSysplorer.
        full_reset: Exit() on all instances (official API), then StartSysplorer.
        """
        with self._recover_lock:
            with self._lock:
                self._driver = None
                self._driver_error = ""
            MWorksDriver.purge_sysplorer_modules()

            mode = (restart_mode or "reconnect").strip().lower()
            if mode == "full_reset":
                with self._lock:
                    self._dedicated_sysplorer_port = None
                shutdown_all_sysplorer_via_exit()
                time.sleep(1.0)
                MWorksDriver.purge_sysplorer_modules()
                return self._start_and_cache()

            MWorksDriver.purge_sysplorer_modules()
            ports = find_sysplorer_ports()
            port_set: Set[int] = {int(p) for p in ports}
            with self._lock:
                ded = self._dedicated_sysplorer_port
            if ded is not None and int(ded) in port_set:
                try:
                    drv = MWorksDriver(force_start=False, connect_port=int(ded))
                    with self._lock:
                        self._driver = drv
                        self._driver_error = ""
                    return drv
                except Exception as exc:
                    log.warning("api_restart reconnect to dedicated port %s failed: %s", ded, exc)
            return self._start_and_cache()

    def exit_sessions(self, exit_port: Optional[int] = None) -> Dict[str, Any]:
        """Official Exit(): all instances (default) or a single port."""
        with self._recover_lock:
            with self._lock:
                self._driver = None
                self._driver_error = ""
                ded = self._dedicated_sysplorer_port
            MWorksDriver.purge_sysplorer_modules()
            if exit_port is not None:
                result = exit_sysplorer_on_port(int(exit_port))
                if ded is not None and int(exit_port) == int(ded):
                    with self._lock:
                        self._dedicated_sysplorer_port = None
            else:
                result = shutdown_all_sysplorer_via_exit()
                with self._lock:
                    self._dedicated_sysplorer_port = None
            MWorksDriver.purge_sysplorer_modules()
            return result

    def force_restart_via_api(self) -> MWorksDriver:
        """Exit all running Sysplorer instances, then StartSysplorer (same as api_restart full_reset)."""
        return self.api_restart(restart_mode="full_reset")

    def invalidate(self) -> None:
        with self._lock:
            self._driver = None
            self._driver_error = "invalidated by caller"

    def _recover(self, health: StackHealth) -> MWorksDriver:
        if health == StackHealth.HEALTHY:
            with self._lock:
                if self._driver is not None:
                    return self._driver
            health = StackHealth.DRIVER_STALE

        if health == StackHealth.DRIVER_STALE:
            ports = find_sysplorer_ports()
            port_set: Set[int] = {int(p) for p in ports}
            with self._lock:
                ded = self._dedicated_sysplorer_port
            if ded is not None and int(ded) in port_set:
                try:
                    return self._reconnect_to_dedicated(int(ded))
                except Exception as exc:
                    log.warning("reconnect to dedicated port %s failed (%s); starting new Sysplorer", ded, exc)
            return self._start_and_cache()

        return self._start_and_cache()

    def _reconnect_to_dedicated(self, port: int) -> MWorksDriver:
        MWorksDriver.purge_sysplorer_modules()
        drv = MWorksDriver(force_start=False, connect_port=int(port))
        with self._lock:
            self._driver = drv
            self._driver_error = ""
        return drv

    def _start_and_cache(self) -> MWorksDriver:
        drv = self._start_fresh()
        with self._lock:
            self._driver = drv
            self._driver_error = ""
        return drv

    def _start_fresh(self) -> MWorksDriver:
        """StartSysplorer, diff FindSysplorer ports vs pre-start snapshot, connect to the new port."""
        before_ports: Set[int] = {int(p) for p in find_sysplorer_ports()}
        try:
            MWorksDriver(force_start=True)
        except Exception as exc:
            err = str(exc)
            if not self._is_connection_error(err):
                self._driver_error = err
                self._update_startup_state(started=False, error=err)
                raise

            MWorksDriver.purge_sysplorer_modules()
            grace = float(os.environ.get("MWORKS_POST_STARTSYSPLORER_GRACE_SECONDS", "1.5"))
            if grace > 0:
                time.sleep(grace)

            after_list = find_sysplorer_ports()
            if after_list:
                log.warning(
                    "StartSysplorer raised (%s) but FindSysplorer reports an instance; reconnecting.",
                    err[:200],
                )
                try:
                    candidate = pick_new_sysplorer_port(before_ports, after_list)
                    if candidate is None and after_list:
                        candidate = int(after_list[-1])
                    if candidate is None:
                        raise MWorksDriverError("FindSysplorer returned no ports after StartSysplorer error path")
                    drv = self._connect_to_port_with_retry(
                        candidate, max_attempts=6, base_delay=1.5
                    )
                    self._update_startup_state(started=True)
                    return drv
                except Exception as retry_exc:
                    log.warning("Reconnect after StartSysplorer error failed: %s", retry_exc)

            self._driver_error = f"Cannot start Sysplorer: {err}"
            self._update_startup_state(started=False, error=self._driver_error)
            raise MWorksDriverError(self._driver_error) from exc

        grace = float(os.environ.get("MWORKS_POST_STARTSYSPLORER_GRACE_SECONDS", "1.5"))
        if grace > 0:
            time.sleep(grace)

        MWorksDriver.purge_sysplorer_modules()
        after_list = find_sysplorer_ports()
        candidate = pick_new_sysplorer_port(before_ports, after_list)
        if candidate is None and after_list:
            log.warning(
                "Could not infer new Sysplorer port via set-diff; using last FindSysplorer entry %s",
                after_list[-1],
            )
            candidate = int(after_list[-1])
        if candidate is None:
            self._driver_error = "Sysplorer launch did not add any FindSysplorer port"
            self._update_startup_state(started=False, error=self._driver_error)
            raise MWorksDriverError(self._driver_error)

        try:
            drv = self._connect_to_port_with_retry(candidate, max_attempts=6, base_delay=1.5)
            self._update_startup_state(started=True)
            return drv
        except Exception as exc:
            self._driver_error = f"Sysplorer launch did not produce a connectable instance: {exc}"
            self._update_startup_state(started=False, error=self._driver_error)
            raise MWorksDriverError(self._driver_error) from exc

    @staticmethod
    def _probe_driver(drv: MWorksDriver) -> bool:
        try:
            result = drv.get_model_description("Modelica.SIunits")
            return result.ok or isinstance(result.data, str)
        except Exception:
            return False

    @staticmethod
    def _is_connection_error(error_text: str) -> bool:
        text = (error_text or "").lower()
        return any(hint in text for hint in _SYSPLORER_CONNECT_ERROR_HINTS)

    def _connect_to_port_with_retry(
        self,
        port: int,
        max_attempts: int = 4,
        base_delay: float = 1.0,
    ) -> MWorksDriver:
        """Connect to a specific Sysplorer port; record it as this MCP's dedicated instance."""
        last_exc: Optional[Exception] = None
        for idx in range(max(1, max_attempts)):
            try:
                MWorksDriver.purge_sysplorer_modules()
                drv = MWorksDriver(force_start=False, connect_port=int(port))
                with self._lock:
                    self._driver = drv
                    self._driver_error = ""
                    self._dedicated_sysplorer_port = int(port)
                return drv
            except Exception as exc:
                last_exc = exc
                if not self._is_connection_error(str(exc)):
                    raise
                if idx >= max_attempts - 1:
                    break
                time.sleep(base_delay * (idx + 1))

        assert last_exc is not None
        self._driver_error = str(last_exc)
        raise last_exc

    def _update_startup_state(
        self,
        started: bool = False,
        already_running: bool = False,
        error: str = "",
        wait_ms: int = 0,
    ) -> None:
        with self._lock:
            dedicated = self._dedicated_sysplorer_port
        self._last_startup_state = {
            "attempted": True,
            "started": started,
            "already_running": already_running,
            "wait_ms": wait_ms,
            "error": error,
            "dedicated_sysplorer_port": dedicated,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
