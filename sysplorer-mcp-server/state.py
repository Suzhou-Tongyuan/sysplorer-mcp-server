"""MWorks MCP Server — mutable global state + driver initialization."""
from __future__ import annotations

import threading
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional

from mworks_driver import MWorksDriver, MWorksDriverError  # noqa: F401
from core.stack_health import StackHealthManager

# ── Stack health singleton (the only source of driver + recovery logic) ──────
_stack_health = StackHealthManager()

# ── Mutable globals (non-driver) ─────────────────────────────────────────────
_driver_lock = threading.Lock()
_driver_session_id: Optional[int] = None

_rag_module: Optional[ModuleType] = None
_rag_lock = threading.Lock()

_help_html_index_cache: Dict[str, Dict[str, List[Path]]] = {}
_known_libs_cache: Optional[Dict[str, str]] = None
_known_libs_lock = threading.Lock()
_load_cache_lock = threading.Lock()
_loaded_file_cache: Dict[str, Dict[str, Any]] = {}
_loaded_libs_cache: Dict[str, Dict[str, Any]] = {}


# ── Driver access (delegates to StackHealthManager) ──────────────────────────

def _get_driver() -> MWorksDriver:
    """The single entry point for all MCP tools to obtain a working driver."""
    return _stack_health.driver


def reset_session_caches() -> None:
    """Clear load-library / file caches after Sysplorer Exit or driver reset."""
    with _load_cache_lock:
        global _driver_session_id
        _driver_session_id = None
        _loaded_file_cache.clear()
        _loaded_libs_cache.clear()
