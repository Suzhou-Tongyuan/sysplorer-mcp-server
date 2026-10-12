"""MWorks MCP Server — FastMCP singleton."""
from __future__ import annotations

import logging
import os
import sys
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
    from mcp.types import ToolAnnotations
    _FASTMCP_AVAILABLE = True
except ImportError:
    _FASTMCP_AVAILABLE = False

    class ToolAnnotations:  # type: ignore[override]
        def __init__(self, **kwargs: Any) -> None:
            self.readOnlyHint = kwargs.get("readOnlyHint")
            self.destructiveHint = kwargs.get("destructiveHint")
            self.idempotentHint = kwargs.get("idempotentHint")

    class FastMCP:  # type: ignore[override]
        """Lightweight fallback to keep local tool functions importable for tests."""

        def __init__(self, _name: str, instructions: str | None = None) -> None:
            self._name = _name
            self.instructions = instructions

        def tool(self, *args: Any, **kwargs: Any):
            def _decorator(func):
                return func
            return _decorator

        def run(self) -> None:
            raise RuntimeError("FastMCP not installed")


def readonly_annotations(*, idempotent: bool = False) -> ToolAnnotations:
    """User-asset read-only: no user .mo rewrite, no library download."""
    return ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=idempotent,
    )


def writable_annotations(*, destructive: bool = False) -> ToolAnnotations:
    """May change user models/results, download libraries, or control the session."""
    return ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=destructive,
        idempotentHint=False,
    )


_log = logging.getLogger(__name__)

_BASE_INSTRUCTIONS = (
    "Sysplorer automation via dedicated MCP tools. Failures are MCP "
    "``isError`` plus one next-step sentence.\n"
    "\n"
    "Dedicated tools first (MCP routing): if a registered tool can do the job, "
    "call it. Do not open with ``call_code`` / ModelingPy for session, lifecycle, "
    "libraries, check/translate/simulate, results, layout, or docs.\n"
    "- session_manager: health / ensure / restart / get_directory / "
    "get_sim_result_directory / get_installed_libraries / get_loaded_models. "
    "get_loaded_models is top-level plus one package child layer; go deeper with "
    "model_inspect(action=get_classes).\n"
    "- model_manager: new; open (loaded FQ class name only); load_file (.mo / "
    "package.mo); unload (MCP wraps EraseClasses tuple); save "
    "(SaveModel in place); save_as (SaveModelAs).\n"
    "- model_inspect: get_classes / components / ports / text / descriptions / "
    "lookup_component / get_last_errors.\n"
    "- compare_model: two loaded names (is_file=false) or two .mo paths "
    "(is_file=true).\n"
    "- load_library: installed | load. check_model / translate_model / "
    "simulate_model (auto-layout a user .mo with no Placement; library "
    "classes are not rewritten). result_manager / plot_manager / smart_layout. "
    "get_lib_model_document / get_api_document / resources_retrieval.\n"
    "Do not use run_sysplorer_api for OpenModel, OpenModelFile, EraseClasses, "
    "GetLastErrors, CompareModel, LoadLibrary, CheckModel, SimulateModel, "
    "GetDirectory, GetSimResultDirectory, GetInstalledLibraries, GetClasses "
    "when the matching MCP tool exists.\n"
    "call_code is last resort: unwrapped Sysplorer APIs or toolbox batch. "
    "Only mode=run_sysplorer_api (old name run_script still works). "
    "python_source / script_path must be inside payload (siblings of mode are "
    "dropped). Import mworks.sysplorer as ModelingPy in the script. "
    "Not a general Python runner. Do not use it for check / translate / "
    "simulate / layout / inspect; those have dedicated tools. "
    "SetModelParamValue: get_api_document then this tool.\n"
    "Compare two models with compare_model; do not script CompareModel unless "
    "batching unwrapped APIs.\n"
    "Directory packages: load_file on a nested .mo opens the top-level "
    "package.mo (load_path / load_target); force_reload erases only the root "
    "package, not the within parent chain.\n"
)

_DOC_RETRIEVAL_HINT = (
    "Search corpora with resources_retrieval (action=corpora then search). "
    "Do not walk or summarize the resources tree at session start.\n"
)


def _is_modelica_lite_label() -> bool:
    label = os.environ.get("SYSPLORER_PLATFORM_LABEL", "").strip().lower().replace("-", "_")
    return label in ("modelica_lite", "mols")


_MODELICA_LITE_HINT = (
    "modelica_lite: try load_library(action=load) first. "
    "dependency_download_enabled=false only blocks download, not local libraries. "
    "Missing packs: library_prepare(action=plan then prepare/download, "
    "dry_run=false, download_missing=true); do not loop load. "
    "Real download needs --user-workspace. load_file may prepare when that gate "
    "is open. run_sysplorer_api is in-process on this platform.\n"
)

try:
    from path_config import DEPLOY_ROOT, USER_WORKSPACE_ROOT, WORKSPACE_ROOT, get_resources_root
except Exception:  # pragma: no cover - import order / tests without package path
    _PATH_HINT = _DOC_RETRIEVAL_HINT
else:
    _PATH_HINT = (
        f"Workspace: `{WORKSPACE_ROOT}`. Resources: `{get_resources_root()}`.\n"
    )
    if _is_modelica_lite_label():
        _PATH_HINT += (
            f"- **User workspace (dependency downloads enabled only when set)**: "
            f"`{USER_WORKSPACE_ROOT or ''}`\n"
        )
    if getattr(sys, "frozen", False):
        _PATH_HINT += f"- **MCP deploy directory (exe)**: `{DEPLOY_ROOT}`\n"
    elif os.environ.get("MCP_DEPLOY_ROOT", "").strip():
        _PATH_HINT += f"- **MCP deploy directory (Tools layout)**: `{DEPLOY_ROOT}`\n"
    _PATH_HINT += (
        "Do not write modeling outputs into the MCP exe directory; set "
        "MCP_WORKSPACE_DIR / --workspace-dir to the agent project root.\n"
        "MCP session bans: never ClearAll, ChangeDirectory, or "
        "ChangeSimResultDirectory. Unload with model_manager unload. "
        "Use session_manager get_directory / get_sim_result_directory "
        "(not MCP MWORKS_SIM_DIR as truth). paths.workspace_root is the MCP "
        "project root and may differ. Attach via SYSPLORER_API_PORT: "
        "run_sysplorer_api rejects Exit; session_manager blocks shutdown / "
        "force_restart / restart(full_reset).\n"
    )
    _PATH_HINT += _DOC_RETRIEVAL_HINT

_INSTRUCTIONS = _BASE_INSTRUCTIONS + _PATH_HINT
if _is_modelica_lite_label():
    _INSTRUCTIONS = _BASE_INSTRUCTIONS + _MODELICA_LITE_HINT + _PATH_HINT

mcp = FastMCP(
    "sysplorer",
    instructions=_INSTRUCTIONS,
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
        from core.tool_envelope import promote_mcp_result

        if fn_is_async:
            return promote_mcp_result(await fn(**arguments_parsed_dict))
        return promote_mcp_result(
            await anyio.to_thread.run_sync(lambda: fn(**arguments_parsed_dict), limiter=limiter)
        )

    FuncMetadata.call_fn_with_arg_validation = call_fn_with_arg_validation  # type: ignore[method-assign]

    _orig_convert = getattr(FuncMetadata, "convert_result", None)
    if callable(_orig_convert):

        def convert_result(self, result):  # type: ignore[no-untyped-def]
            if getattr(result, "isError", False):
                return result
            return _orig_convert(self, result)

        FuncMetadata.convert_result = convert_result  # type: ignore[method-assign]


_install_fastmcp_sync_tool_offload()
