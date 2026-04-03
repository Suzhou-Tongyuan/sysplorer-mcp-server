"""Optional file logging hook for session/health diagnostics (see logs/health_check.log)."""
from __future__ import annotations

import logging
from pathlib import Path

from path_config import resolve_mcp_server_log_dir

_parent_ready = False


def _ensure_parent() -> None:
    global _parent_ready
    if _parent_ready:
        return
    _parent_ready = True
    root = logging.getLogger("mworks_mcp.health")
    root.setLevel(logging.INFO)
    log_path = resolve_mcp_server_log_dir() / "health_check.log"
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root.addHandler(fh)
    root.propagate = False


def get_health_log(sub: str = "") -> logging.Logger:
    """Return child logger under mworks_mcp.health（与 main 共用 resolve_mcp_server_log_dir 下的 health_check.log）。"""
    _ensure_parent()
    name = "mworks_mcp.health" + (f".{sub}" if sub else "")
    return logging.getLogger(name)


def health_log_path() -> Path:
    """Absolute path to the health check log file (for CLI messages)."""
    return resolve_mcp_server_log_dir() / "health_check.log"
