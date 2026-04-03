"""Lazy loader for the Modelica documentation RAG module."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import state as _state


def _get_rag_module() -> ModuleType:
    with _state._rag_lock:
        if _state._rag_module is not None:
            return _state._rag_module
        # Resolve next to this package (not PROJECT_ROOT), so layouts like
        # `repo/sysplorer-mcp-server/...` and flat copies of `sysplorer-mcp-server/` both work.
        _pkg_root = Path(__file__).resolve().parent.parent
        rag_file = _pkg_root / "tools" / "rag" / "modelica_doc_rag.py"
        if not rag_file.exists():
            raise FileNotFoundError(f"RAG module not found: {rag_file}")
        spec = importlib.util.spec_from_file_location("modelica_doc_rag_local", rag_file)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"failed to load RAG module spec: {rag_file}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        _state._rag_module = module
        return module
