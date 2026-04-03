"""
MWorks MCP Server — 路径配置中心。

所有本地文件系统路径的硬编码集中管理于此文件。
配置优先级：命令行参数 > 环境变量 > 此文件默认值。
命令行参数通过 main.py 的 --mworks-install-dir 等选项传递，会被自动设置为环境变量。
本模块在首次 import 时固化 MWORKS_* 等路径，故 main 须在 import path_config 之前调用 _apply_mcp_env_from_argv()。

路径语义（重要）：
- **DEPLOY_ROOT**：frozen 时为 exe 目录；非 frozen 时若设置环境变量 **MCP_DEPLOY_ROOT**（如 Tools/sysplorer_mcp 根），则为该目录；否则为仓库根（sysplorer-mcp-server 上级）。
- **WORKSPACE_ROOT / PROJECT_ROOT**：Agent 打开的**工程工作区**（新建/保存 .mo、private_lib、src 等）。打包 exe 时
  默认取进程 **当前工作目录**；务必在 MCP 配置中设置 **MCP_WORKSPACE_DIR** 指向用户工程根，或保证启动 MCP 时的 cwd
  即为该工程目录。**勿**与 exe 目录混用。
- **get_resources_root()**：查阅用语料根（frozen 或 MCP_DEPLOY_ROOT 时为 DEPLOY_ROOT/resources；纯开发态为工作区 resources/；可被 MCP_RESOURCES_DIR 覆盖）。
- **get_mcp_system_temp_root() / ensure_mcp_scratch_subdir()**：进程级「系统临时目录」下的统一命名空间（默认
  ``%TEMP%/mworks_sysplorer_mcp``），供日志 fallback、`mkstemp(dir=...)`、**MWORKS_WORKDIR 在包内 temp 不可写时**等使用；
  可由 **MCP_SYSTEM_TEMP_ROOT** 覆盖整根路径。
- **resolve_mcp_server_log_dir()**：``sysplorer-mcp-server/logs`` 可写则用该目录；否则与 **ensure_mcp_scratch_subdir(\"logs\")** 一致
  （供 ``main`` 的 server.log、``health_logging`` 的 health_check.log 等）。
"""
from __future__ import annotations
import platform
import os
import sys
import tempfile
from pathlib import Path

_IS_FROZEN = getattr(sys, "frozen", False)
# sysplorer-mcp-server 包目录（PyInstaller onefile 下可能在 _MEIPASS，仅作服务端内部 temp 等）
MCP_PACKAGE_ROOT = Path(__file__).resolve().parent
PLATFORM = platform.system()


def get_mcp_system_temp_root() -> Path:
    """系统临时目录下本服务的统一根（默认 gettempdir()/mworks_sysplorer_mcp）。可由 MCP_SYSTEM_TEMP_ROOT 覆盖。"""
    env = os.environ.get("MCP_SYSTEM_TEMP_ROOT", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return Path(tempfile.gettempdir()).resolve() / "mworks_sysplorer_mcp"


def ensure_mcp_scratch_subdir(*parts: str) -> Path:
    """
    在 get_mcp_system_temp_root() 下创建子目录并返回，供 tempfile.mkstemp(..., dir=) 等使用。
    解析后的路径必须仍位于该根之下（防止 parts 中含 .. 逃逸）。
    """
    base = get_mcp_system_temp_root()
    p = base.joinpath(*parts) if parts else base
    p = p.resolve()
    try:
        p.relative_to(base.resolve())
    except ValueError as exc:
        raise ValueError(f"scratch path escapes MCP temp root: {p}") from exc
    p.mkdir(parents=True, exist_ok=True)
    return p


def resolve_mcp_server_log_dir() -> Path:
    """优先 ``MCP_PACKAGE_ROOT/logs``（探针可写）；失败则系统 scratch 下的 ``logs``。"""
    preferred = MCP_PACKAGE_ROOT / "logs"
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        probe = preferred / "server.log"
        with open(probe, "a", encoding="utf-8"):
            pass
        return preferred
    except OSError:
        return ensure_mcp_scratch_subdir("logs")


def _compute_deploy_root() -> Path:
    if _IS_FROZEN:
        return Path(sys.executable).resolve().parent
    env = os.environ.get("MCP_DEPLOY_ROOT", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


# ── 部署根（exe 目录；或 MCP_DEPLOY_ROOT；否则仓库根）──────────────────────────
DEPLOY_ROOT = _compute_deploy_root()

# frozen 或 Tools/sysplorer_mcp 旁置 Python（launcher 设置 MCP_DEPLOY_ROOT）时与 exe 同策略
_DEPLOY_SIDECAR = _IS_FROZEN or bool(os.environ.get("MCP_DEPLOY_ROOT", "").strip())


def deploy_sidecar_layout() -> bool:
    """是否与 frozen exe 一致使用 DEPLOY_ROOT 旁置 resources/ 与 RAG 索引路径。"""
    return _DEPLOY_SIDECAR


def _compute_workspace_root() -> Path:
    env = os.environ.get("MCP_WORKSPACE_DIR", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    if _IS_FROZEN:
        # 打包场景：未显式设置时退化为启动时的 cwd（应为 Agent 打开的工程目录）
        return Path(os.getcwd()).resolve()
    return Path(__file__).resolve().parent.parent


WORKSPACE_ROOT = _compute_workspace_root()
# 向后兼容：历史代码中的 PROJECT_ROOT 均指「工作区」，不是 exe 目录
PROJECT_ROOT = WORKSPACE_ROOT

def _default_mworks_install_dir() -> Path:
    if PLATFORM == "Windows":
        return Path(r"C:\Program Files\MWORKS\Sysplorer 2026a")
    if PLATFORM == "Linux":
        return Path("/usr/local/MWORKS/Sysplorer-2026a")
    return Path("/Applications/MWORKS/Sysplorer-2026a.app/Contents")


def _default_site_packages(install_dir: Path) -> Path:
    if PLATFORM == "Windows":
        return install_dir / "External" / "python64" / "Lib" / "site-packages"

    candidates = (
        install_dir / "external" / "python64" / "lib" / "python3.11" / "site-packages",
        install_dir / "external" / "python64" / "lib" / "python3.12" / "site-packages",
        install_dir / "external" / "python64" / "lib" / "python3.13" / "site-packages",
        install_dir / "external" / "python64" / "lib" / "site-packages",
    )
    return next((candidate for candidate in candidates if candidate.exists()), candidates[0])


def _default_bin64_dir(install_dir: Path) -> Path:
    bin_dir_name = "Bin64" if PLATFORM == "Windows" else "bin64"
    return install_dir / bin_dir_name


def _default_solver_exe(install_dir: Path) -> Path:
    solver_name = "MWSolver.exe" if PLATFORM == "Windows" else "MWSolver"
    return install_dir / "Simulator" / "Bin64" / solver_name

def _default_python_path(install_dir: Path) -> Path:
    if PLATFORM == "Windows":
        return install_dir / "External" / "python64" / "python.exe"
    else:
        return install_dir/ "external" / "python64" / "bin" / "python3"

# ── MWorks / Sysplorer 安装路径 ──────────────────────────────────────────────
MWORKS_INSTALL_DIR = Path(
    os.environ.get(
        "MWORKS_INSTALL_DIR",
        str(_default_mworks_install_dir()),
    )
)

MWORKS_BIN64 = Path(
    os.environ.get("MWORKS_BIN64", str(_default_bin64_dir(MWORKS_INSTALL_DIR)))
)

MWORKS_SITE_PACKAGES = Path(
    os.environ.get(
        "MWORKS_SYSPLORER_SITE_PACKAGES",
        str(_default_site_packages(MWORKS_INSTALL_DIR)),
    )
)

# Sysplorer 自带的Python解释器路径（优先使用这个执行API调用，避免版本兼容问题）
SYSPLORER_PYTHON = Path(
    os.environ.get(
        "SYSPLORER_PYTHON",
        str(MWORKS_INSTALL_DIR / "External" / "python64" / "python.exe"),
    )
)

MWORKS_LIBRARY_ROOT = Path(
    os.environ.get(
        "MWORKS_LIBRARY_ROOT",
        str(MWORKS_INSTALL_DIR / "Library"),
    )
)

MWORKS_SIMULATOR_BIN = Path(
    os.environ.get(
        "MWORKS_SIMULATOR_BIN",
        str(MWORKS_INSTALL_DIR / "Simulator" / "Bin64"),
    )
)

MWORKS_SOLVER_EXE = Path(
    os.environ.get("MWORKS_SOLVER_EXE", str(_default_solver_exe(MWORKS_INSTALL_DIR)))
)


def _default_mworks_workdir() -> str:
    """优先包内 ``sysplorer-mcp-server/temp``（开发态可写）；不可写时（Program Files、只读安装、PyInstaller 解压目录等）退回系统 scratch。"""
    pkg_temp = MCP_PACKAGE_ROOT / "temp"
    try:
        pkg_temp.mkdir(parents=True, exist_ok=True)
        probe = pkg_temp / ".m_write_probe"
        probe.write_text("", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return str(pkg_temp)
    except OSError:
        return str(ensure_mcp_scratch_subdir("mworks_work"))


# ── MWorks 工作目录 / 仿真输出 ──────────────────────────────────────────────
MWORKS_WORKDIR = Path(
    os.environ.get(
        "MWORKS_WORKDIR",
        _default_mworks_workdir(),
    )
)

MWORKS_SIM_DIR = Path(
    os.environ.get(
        "MWORKS_SIM_DIR",
        str(Path.home() / "Documents" / "MWORKS" / "Simulation"),
    )
)

MWORKS_MW_MOL_DIR = Path(
    os.environ.get(
        "MWORKS_MW_MOL_DIR",
        str(Path.home() / "Documents" / "MWORKS" / "mw_mol"),
    )
)

# ── Sysplorer 平台版本标识（嵌入元数据 JSON 的字符串） ───────────────────────
SYSPLORER_PLATFORM_LABEL = os.environ.get(
    "SYSPLORER_PLATFORM_LABEL", "Sysplorer 2026a"
)

# ── 工程内路径（相对 WORKSPACE_ROOT）────────────────────────────────────────
METADATA_LIB_PATH = WORKSPACE_ROOT / "private_lib" / "MetaDataLib.json"


def _resolve_smart_layout_temp_dir() -> Path:
    """
    Smart Layout 默认输出目录：优先工作区内（旁置布局用 .mworks_mcp/smart_layout，开发态用包 temp 树）。
    若工作区位于 Program Files、只读卷等导致不可写，退回 ensure_mcp_scratch_subdir("smart_layout")
    （与 _default_mworks_workdir 策略一致）。
    """
    if _DEPLOY_SIDECAR:
        preferred = WORKSPACE_ROOT / ".mworks_mcp" / "smart_layout"
    else:
        preferred = WORKSPACE_ROOT / "sysplorer-mcp-server" / "temp" / "smart_layout"
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        probe = preferred / ".m_write_probe"
        probe.write_text("", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return preferred
    except OSError:
        return ensure_mcp_scratch_subdir("smart_layout")


# Smart Layout 临时输出：见 _resolve_smart_layout_temp_dir
SMART_LAYOUT_TEMP_DIR = _resolve_smart_layout_temp_dir()

if _DEPLOY_SIDECAR:
    DIAGRAM_EXPORT_TEMP_DIR = WORKSPACE_ROOT / ".mworks_mcp" / "diagram_exports"
else:
    DIAGRAM_EXPORT_TEMP_DIR = WORKSPACE_ROOT / "sysplorer-mcp-server" / "temp" / "diagram_exports"

TEMP_CODE_FOLDER = "sysplorer-mcp-server/temp/code"

# 文档 RAG 默认索引：旁置布局（frozen / MCP_DEPLOY_ROOT）用 resources/indexes/；纯开发态用包内路径
RAG_INDEX_PATH = (
    "resources/indexes/modelica_doc_index.json"
    if _DEPLOY_SIDECAR
    else "sysplorer-mcp-server/tools/rag/modelica_doc_index.json"
)

RESOURCES_MANIFEST_FILENAME = "resources_manifest.json"


def get_resources_root() -> Path:
    """查阅用语料根目录：优先 MCP_RESOURCES_DIR；旁置布局为 DEPLOY_ROOT/resources；否则为工作区 resources/。"""
    env = os.environ.get("MCP_RESOURCES_DIR", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    if _DEPLOY_SIDECAR:
        return (DEPLOY_ROOT / "resources").resolve()
    return (WORKSPACE_ROOT / "resources").resolve()


def get_resources_manifest_path() -> Path:
    return get_resources_root() / RESOURCES_MANIFEST_FILENAME


# ── RAG / 语料检索内存与范围（环境变量）────────────────────────────────────────
# MCP_RAG_LOW_MEMORY=1：默认收紧索引规模并改用纯词法检索（不建 vector 侧），显著降内存。
# MCP_RAG_MAX_CHUNKS：索引中最多保留的 chunk 数（超出则停止收录，0=不限制）。
# MCP_RAG_LEXICAL_ONLY=1：建索引时不生成 vector_index，查询只走 BM25 词法分支。
# MCP_RAG_MAX_INDEX_LOAD_MB：索引 JSON 文件超过该大小时拒绝 load（0=不限制），避免一次性读入巨型索引拖垮内存。


def rag_low_memory_enabled() -> bool:
    return os.environ.get("MCP_RAG_LOW_MEMORY", "").strip().lower() in ("1", "true", "yes", "on")


def get_rag_max_chunks_cap() -> int:
    raw = os.environ.get("MCP_RAG_MAX_CHUNKS", "").strip()
    if raw:
        try:
            return max(0, int(raw))
        except ValueError:
            return 0
    if rag_low_memory_enabled():
        return 12_000
    return 0


def effective_rag_max_chunks(tool_value: int) -> int:
    if tool_value and tool_value > 0:
        return tool_value
    return get_rag_max_chunks_cap()


def effective_rag_lexical_only(tool_value: bool) -> bool:
    if tool_value:
        return True
    if os.environ.get("MCP_RAG_LEXICAL_ONLY", "").strip().lower() in ("1", "true", "yes", "on"):
        return True
    return rag_low_memory_enabled()


def get_rag_max_index_load_bytes() -> int:
    raw = os.environ.get("MCP_RAG_MAX_INDEX_LOAD_MB", "").strip()
    if raw:
        try:
            mb = float(raw)
            return int(mb * 1024 * 1024) if mb > 0 else 0
        except ValueError:
            return 0
    return 0
