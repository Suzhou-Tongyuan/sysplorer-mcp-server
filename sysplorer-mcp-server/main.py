"""
MWorks MCP Server based on FastMCP — thin entry point.

All tool implementations live in:
  tools/docs.py           resources_retrieval (corpora/search/list/explain)
  tools/layout.py         Smart layout and system model generation tools
  tools/sysplorer.py      Sysplorer health / restart management tools
  tools/workflow.py       call_code（统一 run_script / 异步任务 / 就绪分派 / fast_workflow）
  tools/model_ops.py      Model load / check / translate / simulate（改参经 workflow run_with_ready，无独立工具）
  tools/results.py        Simulation result query and plot_manager tools
  tools/lib_docs.py     get_lib_model_document + get_api_document
"""
from __future__ import annotations

import argparse
import logging
import os
import sys


def _apply_mcp_env_from_argv() -> None:
    """Parse env-related flags before any import of path_config (which freezes MWORKS_* from os.environ)."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--mworks-install-dir", type=str, default=None)
    parser.add_argument("--sysplorer-platform-label", type=str, default=None)
    parser.add_argument("--resources-dir", type=str, default=None)
    parser.add_argument("--workspace-dir", type=str, default=None)
    parser.add_argument("--rag-index-path", type=str, default=None)
    args, _ = parser.parse_known_args()
    if args.mworks_install_dir:
        os.environ["MWORKS_INSTALL_DIR"] = args.mworks_install_dir.strip()
    if args.sysplorer_platform_label:
        os.environ["SYSPLORER_PLATFORM_LABEL"] = args.sysplorer_platform_label.strip()
    if args.resources_dir:
        os.environ["MCP_RESOURCES_DIR"] = args.resources_dir.strip()
    if args.workspace_dir:
        os.environ["MCP_WORKSPACE_DIR"] = args.workspace_dir.strip()
    if args.rag_index_path:
        os.environ["MCP_RAG_INDEX_PATH"] = args.rag_index_path.strip()


# Must run before `import path_config`: that module binds MWORKS_BIN64 etc. at import time.
_apply_mcp_env_from_argv()

from path_config import resolve_mcp_server_log_dir


# ── Redirect stderr to log file ───────────────────────────────────────────────
# Sysplorer API writes large amounts of compilation/simulation progress to
# stderr (including C-level printf).  This floods the Claude Code terminal and
# pushes conversation history out of view.  Open the log early so subsequent
# native output (after stdio_isolate) is captured; CLI env is applied above
# before path_config so MWORKS_* paths match --mworks-install-dir.
_LOG_DIR = resolve_mcp_server_log_dir()
_LOG_FILE = _LOG_DIR / "server.log"
_log_fh = open(_LOG_FILE, "a", encoding="utf-8", buffering=1)  # line-buffered
# 仅 dup2(stderr) 不够：StartSysplorer 及 mworks 原生层会向 stdout（CRT fd1 /
# Win32 GetStdHandle(STD_OUTPUT)）写调试信息，污染 MCP 的 stdio JSON-RPC 导致断开。
from stdio_isolate import isolate_mcp_stdio_from_native_output

# 保留专用 fd 供 MCP JSON-RPC 写入；sys.stdout 已指向日志，避免 mworks.sysplorer 的 print 污染协议。
MCP_STDIO_RPC_OUT_FD = isolate_mcp_stdio_from_native_output(_log_fh)
try:
    os.set_inheritable(MCP_STDIO_RPC_OUT_FD, False)
except (OSError, AttributeError):
    pass

# ── Python logging → same log file ───────────────────────────────────────────
logging.basicConfig(
    stream=_log_fh,
    level=logging.WARNING,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# ─────────────────────────────────────────────────────────────────────────────

from mcp_instance import mcp, _FASTMCP_AVAILABLE  # noqa: E402

# Register all tools by importing tool modules (side-effect: @mcp.tool() decorators run)
import tools.docs            # noqa: F401
import tools.layout          # noqa: F401
import tools.sysplorer       # noqa: F401
import tools.workflow        # noqa: F401
import tools.model_ops       # noqa: F401
import tools.results         # noqa: F401
import tools.lib_docs        # noqa: F401
from tools.sysplorer import session_manager  # noqa: E402, F401
from tools.results import (  # noqa: E402, F401
    plot_manager,
    result_manager,
)
from tools.model_ops import (  # noqa: E402, F401
    model_manager,
    check_model,
    simulate_model,
    translate_model,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MWorks MCP Server")
    parser.add_argument("--mworks-install-dir", type=str, help="Path to MWorks/Sysplorer installation directory")
    parser.add_argument("--sysplorer-platform-label", type=str, help="Sysplorer platform version label")
    parser.add_argument(
        "--resources-dir",
        type=str,
        help="Directory containing resources_manifest.json and doc corpora (sets MCP_RESOURCES_DIR)",
    )
    parser.add_argument(
        "--rag-index-path",
        type=str,
        help="Absolute or exe-relative path to BM25 index JSON (sets MCP_RAG_INDEX_PATH)",
    )
    parser.add_argument(
        "--workspace-dir",
        type=str,
        help="Agent project root for src/private_lib/.mo outputs (sets MCP_WORKSPACE_DIR); exe 旁 resources 与此无关",
    )

    if any(a in ("--version", "-V") for a in sys.argv[1:]):
        from version import format_version_banner

        with os.fdopen(os.dup(MCP_STDIO_RPC_OUT_FD), "w", encoding="utf-8", closefd=True) as vout:
            print(format_version_banner(), file=vout)
        sys.exit(0)

    parser.parse_args()  # validate argv / show --help; env flags already applied in _apply_mcp_env_from_argv()

    if not _FASTMCP_AVAILABLE:
        print("FastMCP not found. Install with: pip install mcp", file=sys.stderr)
        sys.exit(1)
    from version import format_version_banner

    print(format_version_banner(), file=sys.stderr)
    print("Starting MWorks MCP Server...", file=sys.stderr)

    import anyio
    from io import TextIOWrapper

    from mcp.server.stdio import stdio_server

    rpc_bin = os.fdopen(MCP_STDIO_RPC_OUT_FD, "wb", closefd=False)
    rpc_text = TextIOWrapper(rpc_bin, encoding="utf-8", line_buffering=True)

    async def _serve_stdio() -> None:
        async with stdio_server(stdout=anyio.wrap_file(rpc_text)) as (read_stream, write_stream):
            await mcp._mcp_server.run(
                read_stream,
                write_stream,
                mcp._mcp_server.create_initialization_options(),
            )

    anyio.run(_serve_stdio)
