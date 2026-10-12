"""Sysplorer stack health manager — recovery uses official API only (Find/Connect/Start/Exit).

**启动策略（硬性）**：默认通过 ``MWorksDriver(..., force_start=True)`` →
``mworks.sysplorer.StartSysplorer`` 拉起 Sysplorer。若环境变量 ``SYSPLORER_API_PORT``
为正整数，则**不**调用 ``StartSysplorer``，改为 ``ConnectSysplorer(port=…)`` 连接已运行的实例。
禁止在本模块或会话栈内使用 ``subprocess`` / 按进程名等方式直接启动 ``mworks.exe``。
"""
from __future__ import annotations

import logging
import os
import socket
import threading
import time
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Dict, Optional, Set

from mworks_driver import (
    MWorksDriver,
    MWorksDriverError,
    find_sysplorer_ports,
    is_modelica_lite_platform,
    pick_new_sysplorer_port,
    exit_sysplorer_on_port,
)
from constants import _SYSPLORER_CONNECT_ERROR_HINTS

log = logging.getLogger(__name__)

_PORT_PROBE_TIMEOUT_SEC = 0.4
# Skip even the TCP check when a recent probe already succeeded (burst of MCP tools).
_DEFAULT_PROBE_TTL_SEC = 2.0


def sysplorer_port_is_open(port: int, timeout: float = _PORT_PROBE_TIMEOUT_SEC) -> bool:
    """Return True when TCP connect to ``127.0.0.1:port`` succeeds.

    Used to detect a user-closed Sysplorer before ``ConnectSysplorer`` hangs on a
    dead dedicated port.
    """
    try:
        p = int(port)
    except (TypeError, ValueError):
        return False
    if p <= 0:
        return False
    try:
        with socket.create_connection(("127.0.0.1", p), timeout=timeout):
            return True
    except OSError:
        return False


def _probe_ttl_sec() -> float:
    raw = os.environ.get("MWORKS_SESSION_PROBE_TTL_SEC", "").strip()
    if not raw:
        return _DEFAULT_PROBE_TTL_SEC
    try:
        return max(0.0, float(raw))
    except ValueError:
        return _DEFAULT_PROBE_TTL_SEC


def _sysplorer_api_port_from_env() -> Optional[int]:
    """若 ``SYSPLORER_API_PORT`` 为正整数则返回该端口；未设置、空、0 或非整数则返回 None。"""
    raw = os.environ.get("SYSPLORER_API_PORT", "").strip()
    if not raw:
        return None
    try:
        port = int(raw, 10)
    except ValueError:
        log.warning(
            "SYSPLORER_API_PORT=%r is not an integer; falling back to StartSysplorer",
            raw,
        )
        return None
    if port <= 0:
        return None
    return port


def _modelica_lite_requires_api_port_error() -> str:
    label = os.environ.get("SYSPLORER_PLATFORM_LABEL", "").strip() or "modelica_lite"
    raw = os.environ.get("SYSPLORER_API_PORT", "").strip()
    if not raw:
        return (
            f"Platform label '{label}' requires env SYSPLORER_API_PORT. "
            "Host must start mols first (e.g. mols.exe --bind-addr 127.0.0.1:<port>), "
            "inject that port into the Agent/MCP process; MCP will ConnectSysplorer only "
            "(no StartSysplorer, no MWORKS_BIN64 resolution)."
        )
    return (
        f"Platform label '{label}' requires a positive integer SYSPLORER_API_PORT; "
        f"got {raw!r}."
    )


def _sysplorer_api_mols_from_env() -> bool:
    """Return True when StartSysplorer should use MOLS quiet mode."""
    raw = os.environ.get("SYSPLORER_API_MOLS", "").strip().lower()
    return raw in ("1", "true", "yes", "on")


def _find_sysplorer_wait_seconds() -> float:
    """How long to poll FindSysplorer after the GUI window can already be visible."""
    raw = os.environ.get("MWORKS_FIND_SYSPLORER_WAIT_SECONDS", "").strip()
    if not raw:
        return 25.0
    try:
        return max(0.0, float(raw))
    except ValueError:
        return 25.0


def _find_sysplorer_poll_seconds() -> float:
    raw = os.environ.get("MWORKS_FIND_SYSPLORER_POLL_SECONDS", "").strip()
    if not raw:
        return 1.0
    try:
        return max(0.1, float(raw))
    except ValueError:
        return 1.0


_LAUNCH_COOLDOWN_SEC = 45.0
_NO_API_PORT_HINT = (
    "Sysplorer GUI can appear before FindSysplorer registers an API port. "
    "Retry session_manager(action=health). Do not StartSysplorer again "
    "(official ConnectSysplorer() with no port would launch a second window)."
)


def _attached_via_sysplorer_api_port() -> bool:
    """Whether this MCP is attached to a user-managed existing Sysplorer GUI."""
    return _sysplorer_api_port_from_env() is not None


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
        #: Port for *this* MCP process's Sysplorer (set after Start/Connect). Kept in memory so
        #: API idle-timeout recovery can ConnectSysplorer(port) without StartSysplorer.
        self._dedicated_sysplorer_port: Optional[int] = None
        #: monotonic timestamp of last successful cheap liveness check (TCP).
        self._last_liveness_ok_mono: float = 0.0
        #: Last StartSysplorer attempt; used so a retry does not launch a second GUI.
        self._last_startsysplorer_mono: float = 0.0
        #: Start/Connect off the MCP request thread so Cursor's ~30s tool timeout
        #: cannot cancel health and then crash the stdio server on the late reply.
        self._start_thread: Optional[threading.Thread] = None
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

    @property
    def attached_to_existing_gui(self) -> bool:
        return _attached_via_sysplorer_api_port()

    def assess(self) -> StackHealth:
        """Classify health without side effects (FindSysplorer + optional driver probe)."""
        with self._lock:
            drv = self._driver

        if drv is not None and self._probe_driver(drv):
            return StackHealth.HEALTHY

        if self.attached_to_existing_gui:
            return StackHealth.DRIVER_STALE

        try:
            ports = find_sysplorer_ports()
        except Exception:
            ports = []

        if ports:
            return StackHealth.DRIVER_STALE
        return StackHealth.NO_INSTANCE

    def probe_snapshot(self) -> Dict[str, Any]:
        """Read-only snapshot for diagnostics (no recovery)."""
        attach_port = _sysplorer_api_port_from_env()
        if attach_port is not None:
            ports = []
            ports_error = "skipped: SYSPLORER_API_PORT attach mode uses ConnectSysplorer directly"
        else:
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
            "startup_in_progress": self.startup_in_progress,
        }

    @property
    def startup_in_progress(self) -> bool:
        t = self._start_thread
        return t is not None and t.is_alive()

    def instance_is_visible(self) -> bool:
        """True when FindSysplorer or a known API port is already listening."""
        attach = _sysplorer_api_port_from_env()
        if attach is not None and sysplorer_port_is_open(int(attach)):
            return True
        with self._lock:
            ded = self._dedicated_sysplorer_port
        if ded is not None and sysplorer_port_is_open(int(ded)):
            return True
        try:
            return bool(find_sysplorer_ports())
        except Exception:
            return False

    def start_in_background(self) -> bool:
        """Run ``ensure_healthy`` on a daemon thread. Return True if a start is in flight."""
        if self._driver is not None and self._liveness_cache_fresh():
            return False
        if self.startup_in_progress:
            return True
        t = threading.Thread(target=self._bg_ensure, name="sysplorer-ensure", daemon=True)
        with self._lock:
            if self._start_thread is not None and self._start_thread.is_alive():
                return True
            self._start_thread = t
        t.start()
        return True

    def _bg_ensure(self) -> None:
        try:
            self.ensure_healthy()
        except Exception as exc:
            log.warning("background ensure_healthy failed: %s", exc)

    def ensure_healthy(self) -> MWorksDriver:
        with self._lock:
            if self._driver is not None and self._liveness_cache_fresh():
                return self._driver
            if self._driver is not None and self._probe_driver(self._driver):
                self._mark_liveness_ok_unlocked()
                return self._driver

        with self._recover_lock:
            with self._lock:
                if self._driver is not None and self._liveness_cache_fresh():
                    return self._driver
                if self._driver is not None and self._probe_driver(self._driver):
                    self._mark_liveness_ok_unlocked()
                    return self._driver
            return self._recover()

    def api_restart(self, restart_mode: str = "reconnect") -> MWorksDriver:
        """Drop cached connection and re-attach or start.

        reconnect: purge Python singleton, then ConnectSysplorer(dedicated) if that port
        is still listening, otherwise StartSysplorer. Does not FindSysplorer to attach to
        some other instance.
        full_reset: Exit() on this MCP's dedicated port only (if recorded), then StartSysplorer.
        """
        mode = (restart_mode or "reconnect").strip().lower()
        if mode == "full_reset" and self.attached_to_existing_gui:
            raise MWorksDriverError(
                "sysplorer.forbidden: Embedded mode detected via SYSPLORER_API_PORT; "
                "restart(full_reset)/force_restart is disabled because it would call Exit() "
                "on the user's existing Sysplorer window."
            )
        with self._recover_lock:
            with self._lock:
                self._driver = None
                self._driver_error = ""
                self._last_liveness_ok_mono = 0.0
            MWorksDriver.purge_sysplorer_modules()

            if mode == "full_reset":
                exit_result = self._exit_dedicated_sysplorer()
                if not exit_result.get("ok", True):
                    log.warning(
                        "full_reset: Exit on dedicated port failed (%s); continuing with StartSysplorer",
                        exit_result.get("errors"),
                    )
                time.sleep(1.0)
                MWorksDriver.purge_sysplorer_modules()
                return self._start_and_cache(force_launch=True)

            MWorksDriver.purge_sysplorer_modules()
            if self.attached_to_existing_gui:
                return self._start_and_cache()

            with self._lock:
                ded = self._dedicated_sysplorer_port
            if ded is not None and sysplorer_port_is_open(int(ded)):
                try:
                    return self._connect_to_port_with_retry(
                        int(ded), max_attempts=6, base_delay=1.5
                    )
                except Exception as exc:
                    log.warning(
                        "api_restart reconnect to dedicated port %s failed: %s",
                        ded,
                        exc,
                    )
                    self._drop_cached_session(f"reconnect to dedicated port {ded} failed: {exc}")
            elif ded is not None:
                log.warning(
                    "api_restart: dedicated port %s is not listening; recovering",
                    ded,
                )
                self._drop_cached_session(f"dedicated port {ded} not listening")
            return self._start_and_cache()

    def exit_sessions(self, exit_port: Optional[int] = None) -> Dict[str, Any]:
        """Official Exit(): dedicated instance (default) or a single ``exit_port``."""
        if self.attached_to_existing_gui:
            target = f"port {int(exit_port)}" if exit_port is not None else "dedicated instance"
            return {
                "ok": False,
                "blocked": True,
                "code": "sysplorer.forbidden",
                "reason": (
                    "Embedded mode detected via SYSPLORER_API_PORT; session_manager(shutdown) is disabled "
                    f"because it would call Exit() on {target} and close the user's existing Sysplorer window."
                ),
            }
        with self._recover_lock:
            with self._lock:
                self._driver = None
                self._driver_error = ""
                self._last_liveness_ok_mono = 0.0
                ded = self._dedicated_sysplorer_port
            MWorksDriver.purge_sysplorer_modules()
            if exit_port is not None:
                result = exit_sysplorer_on_port(int(exit_port))
                if ded is not None and int(exit_port) == int(ded):
                    with self._lock:
                        self._dedicated_sysplorer_port = None
            else:
                result = self._exit_dedicated_sysplorer()
            MWorksDriver.purge_sysplorer_modules()
            return result

    def _exit_dedicated_sysplorer(self) -> Dict[str, Any]:
        """Exit only this MCP process's dedicated Sysplorer instance (official API)."""
        with self._lock:
            ded = self._dedicated_sysplorer_port
        if ded is None:
            log.info("No dedicated_sysplorer_port recorded; skipping Exit()")
            return {"ok": True, "exited_ports": [], "errors": [], "skipped": "no_dedicated_port"}
        result = exit_sysplorer_on_port(int(ded))
        with self._lock:
            self._dedicated_sysplorer_port = None
        return result

    def force_restart_via_api(self) -> MWorksDriver:
        """Exit this MCP's dedicated Sysplorer, then StartSysplorer (same as api_restart full_reset)."""
        return self.api_restart(restart_mode="full_reset")

    def invalidate(self) -> None:
        with self._lock:
            self._driver = None
            self._last_liveness_ok_mono = 0.0
            self._driver_error = "invalidated by caller"

    def _recover(self) -> MWorksDriver:
        if self.attached_to_existing_gui:
            return self._start_and_cache()

        # Connect only to *this* MCP's dedicated port, and only while it is still
        # listening (API idle-timeout). Do not FindSysplorer / Connect someone else's
        # instance. If the user closed Sysplorer, StartSysplorer.
        with self._lock:
            ded = self._dedicated_sysplorer_port
        if ded is not None and sysplorer_port_is_open(int(ded)):
            try:
                log.info(
                    "recover: reconnecting to dedicated Sysplorer port %s "
                    "(API may have timed out; prefer Connect over Start)",
                    ded,
                )
                drv = self._connect_to_port_with_retry(
                    int(ded), max_attempts=6, base_delay=1.5
                )
                self._update_startup_state(started=True, already_running=True)
                return drv
            except Exception as exc:
                log.warning(
                    "reconnect to dedicated port %s failed (%s); StartSysplorer",
                    ded,
                    exc,
                )
                self._drop_cached_session(f"reconnect to dedicated port {ded} failed: {exc}")
                return self._start_and_cache()

        if ded is not None:
            log.warning(
                "recover: dedicated port %s is not listening "
                "(Sysplorer was likely closed); StartSysplorer",
                ded,
            )
            self._drop_cached_session(f"dedicated port {ded} not listening")
        return self._start_and_cache()

    def _drop_cached_session(self, reason: str) -> None:
        with self._lock:
            log.info(
                "dropping cached Sysplorer session (port=%s): %s",
                self._dedicated_sysplorer_port,
                reason,
            )
            self._driver = None
            self._dedicated_sysplorer_port = None
            self._last_liveness_ok_mono = 0.0
            self._driver_error = reason

    def _start_and_cache(self, force_launch: bool = False) -> MWorksDriver:
        drv = self._start_fresh(force_launch=force_launch)
        with self._lock:
            self._driver = drv
            self._driver_error = ""
            self._mark_liveness_ok_unlocked()
        return drv

    def _start_fresh(self, force_launch: bool = False) -> MWorksDriver:
        """StartSysplorer, or connect to ``SYSPLORER_API_PORT`` if set to a positive port.

        ``modelica_lite`` / ``mols``: require ``SYSPLORER_API_PORT`` and ConnectSysplorer only
        (no StartSysplorer; no ``MWORKS_BIN64`` path setup).
        """
        if is_modelica_lite_platform():
            attach_port = _sysplorer_api_port_from_env()
            if attach_port is None:
                err = _modelica_lite_requires_api_port_error()
                self._driver_error = err
                self._update_startup_state(started=False, error=err)
                raise MWorksDriverError(err)
            if force_launch:
                err = (
                    f"Platform label '{os.environ.get('SYSPLORER_PLATFORM_LABEL', '').strip()}' "
                    "does not support StartSysplorer/force_launch; keep mols running and "
                    "reconnect with SYSPLORER_API_PORT."
                )
                self._driver_error = err
                self._update_startup_state(started=False, error=err)
                raise MWorksDriverError(err)
            log.info(
                "modelica_lite: SYSPLORER_API_PORT=%s attaching (ConnectSysplorer; skip MWORKS_BIN64)",
                attach_port,
            )
            try:
                drv = self._connect_to_port_with_retry(
                    attach_port, max_attempts=6, base_delay=1.5
                )
                self._update_startup_state(started=True, already_running=True)
                return drv
            except Exception as exc:
                self._driver_error = (
                    f"Cannot connect to Sysplorer on SYSPLORER_API_PORT={attach_port}: {exc}"
                )
                self._update_startup_state(started=False, error=self._driver_error)
                raise MWorksDriverError(self._driver_error) from exc

        attach_port = None if force_launch else _sysplorer_api_port_from_env()
        if attach_port is not None:
            log.info(
                "SYSPLORER_API_PORT=%s: attaching to existing Sysplorer (ConnectSysplorer)",
                attach_port,
            )
            try:
                drv = self._connect_to_port_with_retry(
                    attach_port, max_attempts=6, base_delay=1.5
                )
                self._update_startup_state(started=True, already_running=True)
                return drv
            except Exception as exc:
                self._driver_error = (
                    f"Cannot connect to Sysplorer on SYSPLORER_API_PORT={attach_port}: {exc}"
                )
                self._update_startup_state(started=False, error=self._driver_error)
                raise MWorksDriverError(self._driver_error) from exc

        existing = [int(p) for p in find_sysplorer_ports()]
        before_ports: Set[int] = set(existing)
        if existing and not force_launch:
            candidate = existing[-1]
            log.info(
                "FindSysplorer already has port(s) %s; ConnectSysplorer(%s) instead of StartSysplorer",
                existing,
                candidate,
            )
            try:
                drv = self._connect_to_port_with_retry(
                    candidate, max_attempts=6, base_delay=1.5
                )
                self._update_startup_state(started=True, already_running=True)
                return drv
            except Exception as exc:
                self._driver_error = (
                    f"Sysplorer is already on port {candidate} but ConnectSysplorer failed: {exc}. "
                    "Retry session_manager(action=health). Do not start a second GUI."
                )
                self._update_startup_state(
                    started=False, already_running=True, error=self._driver_error
                )
                raise MWorksDriverError(self._driver_error) from exc

        wait_budget = _find_sysplorer_wait_seconds()
        if self._recent_startsysplorer() and not force_launch:
            log.info(
                "StartSysplorer was attempted %.1fs ago; polling FindSysplorer instead of launching again",
                time.monotonic() - self._last_startsysplorer_mono,
            )
            _after, candidate, wait_ms = self._wait_for_find_sysplorer_ports(
                before_ports, timeout_sec=wait_budget
            )
            if candidate is None:
                self._driver_error = _NO_API_PORT_HINT
                self._update_startup_state(
                    started=False, wait_ms=wait_ms, error=self._driver_error
                )
                raise MWorksDriverError(self._driver_error)
            try:
                drv = self._connect_to_port_with_retry(
                    candidate, max_attempts=6, base_delay=1.5
                )
                self._update_startup_state(
                    started=True, already_running=True, wait_ms=wait_ms
                )
                return drv
            except Exception as exc:
                self._driver_error = (
                    f"FindSysplorer reported port {candidate} but ConnectSysplorer failed: {exc}. "
                    + _NO_API_PORT_HINT
                )
                self._update_startup_state(
                    started=False, wait_ms=wait_ms, error=self._driver_error
                )
                raise MWorksDriverError(self._driver_error) from exc

        try:
            start_mode = "-q" if _sysplorer_api_mols_from_env() else "-gui"
            MWorksDriver(force_start=True, start_mode=start_mode)
        except Exception as exc:
            err = str(exc)
            if not self._is_connection_error(err):
                self._driver_error = err
                self._update_startup_state(started=False, error=err)
                raise
            log.warning("StartSysplorer raised a connection-class error: %s", err[:200])
        self._last_startsysplorer_mono = time.monotonic()

        MWorksDriver.purge_sysplorer_modules()
        _after, candidate, wait_ms = self._wait_for_find_sysplorer_ports(
            before_ports, timeout_sec=wait_budget
        )
        if candidate is None:
            self._driver_error = (
                "StartSysplorer returned but FindSysplorer has no API port yet. "
                + _NO_API_PORT_HINT
            )
            self._update_startup_state(
                started=False, wait_ms=wait_ms, error=self._driver_error
            )
            raise MWorksDriverError(self._driver_error)

        try:
            drv = self._connect_to_port_with_retry(candidate, max_attempts=6, base_delay=1.5)
            self._update_startup_state(started=True, wait_ms=wait_ms)
            return drv
        except Exception as exc:
            self._driver_error = f"Sysplorer launch did not produce a connectable instance: {exc}"
            self._update_startup_state(
                started=False, wait_ms=wait_ms, error=self._driver_error
            )
            raise MWorksDriverError(self._driver_error) from exc

    def _recent_startsysplorer(self) -> bool:
        if self._last_startsysplorer_mono <= 0:
            return False
        return (time.monotonic() - self._last_startsysplorer_mono) < _LAUNCH_COOLDOWN_SEC

    def _wait_for_find_sysplorer_ports(
        self, before: Set[int], *, timeout_sec: float
    ) -> tuple[List[int], Optional[int], int]:
        """Poll FindSysplorer until a new (or first) port appears."""
        started = time.monotonic()
        interval = _find_sysplorer_poll_seconds()
        after: List[int] = []
        candidate: Optional[int] = None
        while True:
            after = [int(p) for p in find_sysplorer_ports()]
            candidate = pick_new_sysplorer_port(before, after)
            if candidate is None and after and not before:
                candidate = int(after[-1])
            if candidate is not None:
                return after, candidate, int((time.monotonic() - started) * 1000)
            elapsed = time.monotonic() - started
            if elapsed >= timeout_sec:
                return after, None, int(elapsed * 1000)
            time.sleep(min(interval, max(0.0, timeout_sec - elapsed) or interval))

    def _liveness_cache_fresh(self) -> bool:
        ttl = _probe_ttl_sec()
        if ttl <= 0 or self._last_liveness_ok_mono <= 0:
            return False
        return (time.monotonic() - self._last_liveness_ok_mono) < ttl

    def _mark_liveness_ok_unlocked(self) -> None:
        self._last_liveness_ok_mono = time.monotonic()

    def _probe_driver(self, drv: MWorksDriver) -> bool:
        """Cheap liveness: localhost TCP to the dedicated API port (no Sysplorer API call)."""
        port = getattr(drv, "_connect_port", None)
        if port is None:
            port = self._dedicated_sysplorer_port
        if port is None:
            return False
        return sysplorer_port_is_open(int(port))

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
                    self._mark_liveness_ok_unlocked()
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
