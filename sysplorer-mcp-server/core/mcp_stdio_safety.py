"""Keep the stdio MCP process alive when the client times out first.

Cursor cancels a long tool call (~30s) and marks the request completed. The
server later finishes StartSysplorer/Connect and calls respond() again.
The upstream SDK then asserts ``Request already responded to`` and the
ExceptionGroup tears down the stdio TaskGroup — GUI is up, MCP is dead.
"""
from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger(__name__)

_PATCHED = False


def install_late_response_guard() -> None:
    """Idempotent patch: a second respond() after cancel/timeout is a no-op."""
    global _PATCHED
    if _PATCHED:
        return
    from mcp.shared.session import RequestResponder

    original = RequestResponder.respond

    async def respond(self: Any, response: Any) -> None:
        if getattr(self, "_completed", False):
            log.warning(
                "skip late MCP respond for request %s (client already completed/cancelled)",
                getattr(self, "request_id", "?"),
            )
            return
        try:
            await original(self, response)
        except AssertionError as exc:
            if "already responded" in str(exc).lower():
                log.warning(
                    "skip late MCP respond for request %s: %s",
                    getattr(self, "request_id", "?"),
                    exc,
                )
                return
            raise

    RequestResponder.respond = respond  # type: ignore[method-assign]
    _PATCHED = True
