"""
Sidecar launcher: set MCP_DEPLOY_ROOT to this file's parent, then run sysplorer-mcp-server/main.py.

May live in any folder (not only Sysplorer Tools). Invoked as:
  <Sysplorer>/External/python64/python.exe <absolute_or_relative_path>/main.py ...
"""
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


def _run() -> None:
    deploy = Path(__file__).resolve().parent
    os.environ.setdefault("MCP_DEPLOY_ROOT", str(deploy))
    pkg_dir = deploy / "sysplorer-mcp-server"
    inner = pkg_dir / "main.py"
    if not inner.is_file():
        print(f"Error: missing server entry: {inner}", file=sys.stderr)
        sys.exit(1)
    # runpy.run_path() does not prepend the script directory to sys.path for a plain .py file
    # (unlike python sysplorer-mcp-server/main.py), so flat imports (stdio_isolate, mcp_instance, …) would fail.
    sys.path.insert(0, str(pkg_dir))
    runpy.run_path(str(inner), run_name="__main__")


if __name__ == "__main__":
    _run()
