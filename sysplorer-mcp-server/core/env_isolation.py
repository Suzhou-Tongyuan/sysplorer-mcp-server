"""Shared agent-host environment isolation for Sysplorer / MWorks native stacks.

Agent clients (OpenCode, Codex, Cursor, Claude Code, …) often inject UTF-8 mode,
locale, or code-page variables into MCP child processes. Sysplorer's native compiler
toolchain expects Windows ACP / desktop-like env instead.

This module centralizes which variables are stripped and where permanent vs temporary
sanitization applies.
"""
from __future__ import annotations

import os
import platform
import sys
from typing import Dict, Mapping, MutableMapping, Optional

AGENT_ENV_VARS_TO_CLEAR = (
    "CHCP",
    "LANG",
    "PYTHONWUTF8",
    "PYTHONIOENCODING",
    "PYTHONLEGACYWINDOWSFSENCODING",
    "PYTHONLEGACYWINDOWSSTDIO",
    "PYTHONUTF8",
    "LC_ALL",
)

# Debug / snapshot keys (subset shown in launch logs).
AGENT_ENV_DEBUG_KEYS = AGENT_ENV_VARS_TO_CLEAR + ("COMSPEC", "PATH")


def should_clear_agent_env_var(key: str) -> bool:
    upper = (key or "").upper()
    return upper in AGENT_ENV_VARS_TO_CLEAR or upper.startswith("LC_")


def strip_agent_env_from_mapping(
    env: Mapping[str, str],
    *,
    for_windows: Optional[bool] = None,
) -> Dict[str, str]:
    is_windows = platform.system() == "Windows" if for_windows is None else bool(for_windows)
    out = dict(env)
    if not is_windows:
        return out
    for key in list(out.keys()):
        if should_clear_agent_env_var(key):
            out.pop(key, None)
    return out


def strip_agent_env_from_process(*, for_windows: Optional[bool] = None) -> None:
    """Remove agent-injected UTF-8 / locale knobs from the current process env."""
    is_windows = platform.system() == "Windows" if for_windows is None else bool(for_windows)
    if not is_windows:
        return
    for key in list(os.environ.keys()):
        if should_clear_agent_env_var(key):
            os.environ.pop(key, None)


def agent_encoding_env_present() -> bool:
    """True when the current process likely carries agent-forced encoding/locale env."""
    if sys.platform == "win32" and bool(getattr(sys.flags, "utf8_mode", 0)):
        return True
    for key in os.environ:
        if should_clear_agent_env_var(key):
            return True
    return False


def ensure_mcp_host_env_for_sysplorer_native() -> None:
    """Permanently sanitize MCP host env: no UTF-8 *mode*, stdio still UTF-8 via PYTHONIOENCODING."""
    if platform.system() != "Windows":
        return
    strip_agent_env_from_process()
    # MCP JSON-RPC / logs stay UTF-8 without enabling Python UTF-8 mode for native DLLs.
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ.pop("PYTHONUTF8", None)
    os.environ.pop("PYTHONWUTF8", None)


def apply_bundled_python_stdio_utf8(env: MutableMapping[str, str]) -> Dict[str, str]:
    """After stripping agent knobs, set pipe stdio encoding for bundled-python workers."""
    out = dict(env)
    if sys.platform != "win32":
        return out
    out.setdefault("PYTHONIOENCODING", "utf-8")
    return out
