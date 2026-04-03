"""MWorks MCP Server — FastMCP singleton."""
from __future__ import annotations

import logging
import os
import sys

try:
    from mcp.server.fastmcp import FastMCP
    _FASTMCP_AVAILABLE = True
except ImportError:
    _FASTMCP_AVAILABLE = False

    class FastMCP:  # type: ignore[override]
        """Lightweight fallback to keep local tool functions importable for tests."""

        def __init__(self, _name: str, instructions: str | None = None) -> None:
            self._name = _name
            self.instructions = instructions

        def tool(self):
            def _decorator(func):
                return func
            return _decorator

        def run(self) -> None:
            raise RuntimeError("FastMCP not installed")


_log = logging.getLogger(__name__)

_BASE_INSTRUCTIONS = (
    "You assist with MWorks Sysplorer automation via this MCP server. "
    "Prefer tools over guessing Sysplorer API behavior.\n"
)

try:
    from core.resources_manifest import (
        browse_resources_manifest_for_instructions,
        load_modeling_path_router_for_instructions,
        load_seven_gates_workflow_for_instructions,
    )
except Exception:  # pragma: no cover - import order / tests without package path
    _PATH_HINT = ""
    _ROUTER_FRAG = "\n## 建模分流规则\n\n（未加载 resources 模块，请检索 modeling_rules 语料。）\n"
    _ROUTER_META: dict = {"ok": False, "error": "import_failed"}
    _WORKFLOW_FRAG = "\n## 七 Gate 与建模执行闭环\n\n（未加载 resources 模块。）\n"
    _WORKFLOW_META: dict = {"ok": False, "error": "import_failed"}
    _DOC_CORPORA_FRAG = (
        "\n## 旁置文档语料\n\n（清单模块未加载，请使用 mworks_sysplorer_resources_retrieval(action=\"corpora\")。）\n"
    )
    _DOC_CORPORA_META: dict = {"ok": False, "error": "import_failed"}
else:
    from path_config import DEPLOY_ROOT, WORKSPACE_ROOT, get_resources_root

    _PATH_HINT = (
        "\n## 路径约定\n\n"
        f"- **工作区（新建/保存模型、private_lib、src）**: `{WORKSPACE_ROOT}`\n"
        f"- **语料 resources（查阅用，默认在 MCP 部署目录旁）**: `{get_resources_root()}`\n"
    )
    if getattr(sys, "frozen", False):
        _PATH_HINT += f"- **MCP 部署目录（exe）**: `{DEPLOY_ROOT}`\n"
    elif os.environ.get("MCP_DEPLOY_ROOT", "").strip():
        _PATH_HINT += f"- **MCP 部署目录（Tools 旁置）**: `{DEPLOY_ROOT}`\n"
    _PATH_HINT += (
        "打包 exe 时务必配置 **MCP_WORKSPACE_DIR** 或 **`--workspace-dir`** 为 Agent 打开的工程根；"
        "勿将建模输出写到 exe 目录。\n"
    )

    _ROUTER_FRAG, _ROUTER_META = load_modeling_path_router_for_instructions()
    if _ROUTER_META.get("ok"):
        _log.warning(
            "modeling path router loaded for instructions (%s bytes): %s",
            _ROUTER_META.get("size_bytes"),
            _ROUTER_META.get("router_path"),
        )
    else:
        _log.warning("modeling path router: %s (%s)", _ROUTER_META.get("error"), _ROUTER_META.get("router_path"))

    _WORKFLOW_FRAG, _WORKFLOW_META = load_seven_gates_workflow_for_instructions()
    if _WORKFLOW_META.get("ok"):
        _log.warning(
            "seven gates workflow loaded for instructions (%s bytes): %s",
            _WORKFLOW_META.get("size_bytes"),
            _WORKFLOW_META.get("workflow_path"),
        )
    else:
        _log.warning(
            "seven gates workflow: %s (%s)",
            _WORKFLOW_META.get("error"),
            _WORKFLOW_META.get("workflow_path"),
        )

    _DOC_CORPORA_FRAG, _DOC_CORPORA_META = browse_resources_manifest_for_instructions()
    if _DOC_CORPORA_META.get("ok"):
        _log.warning(
            "resources manifest browsed: %s categories (%s)",
            _DOC_CORPORA_META.get("categories"),
            _DOC_CORPORA_META.get("manifest_path"),
        )
    elif _DOC_CORPORA_META.get("error") == "manifest_missing":
        _log.warning("resources manifest missing: %s", _DOC_CORPORA_META.get("manifest_path"))
    else:
        _log.warning("resources manifest browse: %s", _DOC_CORPORA_META.get("error"))

mcp = FastMCP(
    "sysplorer_mcp",
    instructions=_BASE_INSTRUCTIONS + _PATH_HINT + _ROUTER_FRAG + _WORKFLOW_FRAG + _DOC_CORPORA_FRAG,
)


def _install_fastmcp_sync_tool_offload() -> None:
    """Run blocking sync tools on a worker thread so stdio JSON-RPC stays responsive.

    FastMCP (mcp SDK) calls synchronous ``@mcp.tool`` handlers directly on the asyncio
    event loop. Long calls (``CheckModel``, ``SimulateModel``, ``LoadLibrary``, …) then
    block stdin processing; Cursor's parallel ``listTools`` / UI sub-calls hit
    ``-32001 Request timed out`` and may mark the session as disconnected.

    A single-thread limiter keeps at most one tool body running at a time, matching the
    process-wide ``MWorksDriver`` singleton expectations.
    """
    if not _FASTMCP_AVAILABLE:
        return
    import anyio
    from mcp.server.fastmcp.utilities.func_metadata import FuncMetadata

    limiter = anyio.CapacityLimiter(1)

    async def call_fn_with_arg_validation(  # noqa: PLR0913
        self,
        fn,
        fn_is_async: bool,
        arguments_to_validate: dict,
        arguments_to_pass_directly: dict | None = None,
    ):
        arguments_pre_parsed = self.pre_parse_json(arguments_to_validate)
        arguments_parsed_model = self.arg_model.model_validate(arguments_pre_parsed)
        arguments_parsed_dict = arguments_parsed_model.model_dump_one_level()
        arguments_parsed_dict |= arguments_to_pass_directly or {}
        if fn_is_async:
            return await fn(**arguments_parsed_dict)
        return await anyio.to_thread.run_sync(lambda: fn(**arguments_parsed_dict), limiter=limiter)

    FuncMetadata.call_fn_with_arg_validation = call_fn_with_arg_validation  # type: ignore[method-assign]


_install_fastmcp_sync_tool_offload()
