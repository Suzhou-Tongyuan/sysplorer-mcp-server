"""Capture official ModelingPy ``Help`` output.

Sysplorer 26.6 ``Help(cmd)`` looks up the function in ``sysplorer_api`` globals
and calls Python ``help()``, which **prints** the docstring and **returns None**.
MCP must read stdout for that call, not the return value.
"""
from __future__ import annotations

import contextlib
import io
from typing import Any, Callable, Tuple


def invoke_modelingpy_help(help_fn: Callable[..., Any], cmd: str = "") -> Tuple[Any, str]:
    """Run official ``Help`` / ``Help(cmd)`` and return ``(return_value, printed_text)``."""
    import builtins
    import pydoc

    key = (cmd or "").strip()
    buf = io.StringIO()
    helper = getattr(builtins, "help", None)
    old_helper_out = getattr(helper, "_output", None) if isinstance(helper, pydoc.Helper) else None
    try:
        if isinstance(helper, pydoc.Helper):
            helper._output = buf
        with contextlib.redirect_stdout(buf):
            raw = help_fn(key) if key else help_fn()
    finally:
        if isinstance(helper, pydoc.Helper):
            helper._output = old_helper_out
    return raw, buf.getvalue()


def render_function_help(fn: Callable[..., Any]) -> str:
    """Same channel as ``help(fn)``: live function docstring via pydoc, not a copied handbook."""
    import pydoc

    try:
        return pydoc.render_doc(fn, title="%s")
    except Exception:
        return (getattr(fn, "__doc__", None) or "") if callable(fn) else ""


def help_text_from_invoke(raw: Any, printed: str) -> str:
    """Prefer a string return (if a future build adds one); otherwise use captured stdout."""
    if isinstance(raw, str) and raw.strip():
        return raw
    return printed or ""
