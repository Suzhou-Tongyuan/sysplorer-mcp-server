"""MCP tools: live Sysplorer class documentation and API help (no resources/RAG for these)."""
from __future__ import annotations

import os
import re
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict

from constants import normalize_load_library_call
from path_config import ensure_mcp_scratch_subdir
from core.utils import _json
from mcp_instance import mcp
from state import _get_driver


def _top_level_library(full_class_name: str) -> str:
    name = (full_class_name or "").strip()
    if not name:
        return ""
    return name.split(".", 1)[0].strip()


class _HTMLToText(HTMLParser):
    """Minimal HTML → plain text for ExportDocumentation output."""

    _BLOCK = frozenset(
        {"br", "p", "div", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "li", "table", "title"}
    )

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag.lower() in self._BLOCK:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self._BLOCK:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        self._chunks.append(data)

    def get_text(self) -> str:
        raw = "".join(self._chunks)
        raw = re.sub(r"[ \t\r\f\v]+", " ", raw)
        lines = [ln.strip() for ln in raw.split("\n")]
        return "\n".join(line for line in lines if line).strip()


def _html_file_to_plain_text(path: Path) -> str:
    html = path.read_text(encoding="utf-8", errors="replace")
    parser = _HTMLToText()
    try:
        parser.feed(html)
        parser.close()
        return parser.get_text()
    except Exception:
        return re.sub(r"<[^>]+>", " ", html)
        # fallback: strip tags crudely


@mcp.tool()
def get_lib_model_document(full_class_name: str) -> str:
    """
    获取已在 Sysplorer 中解析的 **库模型类** 的文档（说明、参数、端口等汇总的导出文档）。

    流程：`ClassExist(全名)` → 若不存在则对顶层包名调用 `LoadLibrary`（Modelica 使用项目约定的默认版本策略）→
    按需 `OpenModel` → `ExportDocumentation` 将 HTML 写入 path_config 下的 scratch 目录，读取为纯文本后删除该文件。

    Args:
        full_class_name: Modelica 语义下的类全名，例如 `Modelica.Blocks.Continuous.PI`、`TYMultibody.Joints.Revolute`。

    Returns:
        JSON：`ok`、`documentation_text`（纯文本）、`documentation_html_path`（scratch 目录下曾用于导出的路径；
        成功读取后该 HTML 文件会删除，路径仅作排错参考）、
        `class_exist_before` / `load_library_called` / `open_model_called` 等诊断字段；失败时含 `error`。

    **耗时与超时**：当类尚不存在时会内部调用 `LoadLibrary`，与 MCP 工具 `load_library` 相同，大库首次加载可能很慢。
    MCP 客户端若因超时而中断，**不等于**本次逻辑已判定失败（Sysplorer 侧可能仍在加载）。请 **稍后对同一 `full_class_name` 再试一次**。
    """
    name = (full_class_name or "").strip()
    if not name:
        return _json({"ok": False, "tool": "get_lib_model_document", "error": "full_class_name is required"})

    out: Dict[str, Any] = {
        "ok": False,
        "tool": "get_lib_model_document",
        "full_class_name": name,
        "documentation_text": "",
        "documentation_html_path": "",
        "class_exist_before": None,
        "class_exist_after_load": None,
        "load_library_called": False,
        "open_model_called": False,
        "top_level_library": "",
        "error": "",
    }

    top = _top_level_library(name)
    if not top:
        out["error"] = "cannot derive top-level library from full_class_name"
        return _json(out)
    out["top_level_library"] = top

    try:
        driver = _get_driver()
    except Exception as exc:
        out["error"] = f"driver not available: {exc}"
        return _json(out)

    if not callable(driver._api.get("ClassExist")):
        out["error"] = "ClassExist API not available in this Sysplorer runtime"
        return _json(out)
    if not callable(driver._api.get("ExportDocumentation")):
        out["error"] = "ExportDocumentation API not available in this Sysplorer runtime"
        return _json(out)

    ce0 = driver.class_exist(name)
    if not ce0.ok:
        out["error"] = ce0.error
        return _json(out)
    out["class_exist_before"] = bool(ce0.data)

    if not out["class_exist_before"]:
        lib, ver = normalize_load_library_call(top, "")
        if not lib:
            out["error"] = f"invalid library name derived from class: {top!r}"
            return _json(out)
        lr = driver.load_library(lib, ver)
        out["load_library_called"] = True
        if not lr.ok:
            out["error"] = f"LoadLibrary failed: {lr.error}"
            return _json(out)

        ce1 = driver.class_exist(name)
        if not ce1.ok:
            out["error"] = ce1.error
            return _json(out)
        out["class_exist_after_load"] = bool(ce1.data)
        if not out["class_exist_after_load"]:
            om = driver.open_model(name)
            out["open_model_called"] = True
            if not om.ok:
                out["error"] = (
                    f"class not loaded after LoadLibrary; OpenModel failed: {om.error}"
                )
                return _json(out)
            ce2 = driver.class_exist(name)
            if not ce2.ok:
                out["error"] = ce2.error
                return _json(out)
            if not ce2.data:
                out["error"] = "class still not visible after LoadLibrary and OpenModel"
                return _json(out)
    else:
        om = driver.open_model(name)
        out["open_model_called"] = True
        if not om.ok:
            out["warning_open_model"] = om.error

    scratch = ensure_mcp_scratch_subdir("lib_docs")
    fd, tmp_name = tempfile.mkstemp(
        prefix="mworks_class_doc_", suffix=".html", dir=str(scratch)
    )
    os.close(fd)
    safe_file = Path(tmp_name)
    out["documentation_html_path"] = str(safe_file.resolve())
    try:
        ed = driver.export_documentation(name, str(safe_file))
        if not ed.ok:
            out["error"] = ed.error
            return _json(out)

        if not safe_file.is_file():
            out["error"] = f"ExportDocumentation reported success but file missing: {safe_file}"
            return _json(out)

        try:
            plain = _html_file_to_plain_text(safe_file)
        except OSError as exc:
            out["error"] = f"read exported documentation failed: {exc}"
            return _json(out)

        out["ok"] = True
        out["documentation_text"] = plain
        return _json(out)
    finally:
        try:
            safe_file.unlink(missing_ok=True)
        except OSError:
            pass


@mcp.tool()
def get_api_document(api_function_name: str) -> str:
    """
    获取 **Sysplorer Python API**（建模脚本 / ``call_code(mode="run_script")`` 中使用的函数）的说明文本。

    实现为调用官方 API 的 `Help(cmd)`；`api_function_name` 即 `cmd`，必须是当前 Sysplorer 会话里存在的**命令名**
    （与脚本里调用的 ModelingPy 接口名一致）。本工具描述**不**枚举全部命令，名称集合因版本而异。

    **首次使用前请先列举命令**：在第一次需要「知道有哪些 API / 该传什么命令名」时，先调用 **`call_code`**
    （``mode="run_script"``，``payload`` 含 ``python_source``），
    用内联脚本执行 `ListFunctions`，例如：`python_source` 设为
    `RUN_SCRIPT_RESULT = ModelingPy.ListFunctions()`（`ModelingPy` 由 run_script 分支注入）。
    **独立工具箱**（如 DesignOptMpe、CADToolbox、SimulinkImporter）的命令**不在**上述列表中；应分别用
    `import mworks.sysplorer.DesignOptMpe as mpe` / `import mworks.sysplorer.CADToolbox as cadtool` /
    `import mworks.sysplorer.SimulinkImporter as slximport` 后调用对应
    `ListFunctions()`，并用 `help(mpe.xxx)` / `help(cadtool.xxx)` / `help(slximport.xxx)` 查文档（勿对本工具传上述工具箱函数名指望 `Help(cmd)`）。
    **MPE / 参数估计**：旁置语料 `resources/design_opt_mpe_api/参数估计使用说明.md`（流程与常见问题）、`DesignOptMpe.md`（接口说明）；或用 `resources_retrieval` 指定 `sources` 含 `design_opt_mpe_api` 检索。
    从返回 JSON 的 `run_script_result` 读取列表（通常为每行「命令名 + 简短描述」），再将要查帮助的名称（**无括号、无参数**）
    传入本工具的 `api_function_name`。

    Args:
        api_function_name: 与 `ListFunctions` 输出及 `Help(cmd)` 一致的命令名字符串，例如 `OpenModel`、`AddComponent`、`LoadLibrary`。

    Returns:
        JSON：`ok`、`help_text`（`Help` 返回值）；不可用或失败时 `ok=false` 与 `error`。
    """
    cmd = (api_function_name or "").strip()
    if not cmd:
        return _json({"ok": False, "tool": "get_api_document", "error": "api_function_name is required"})

    out: Dict[str, Any] = {
        "ok": False,
        "tool": "get_api_document",
        "api_function_name": cmd,
        "help_text": "",
        "error": "",
    }

    try:
        driver = _get_driver()
    except Exception as exc:
        out["error"] = f"driver not available: {exc}"
        return _json(out)

    if not callable(driver._api.get("Help")):
        out["error"] = "Help API not available in this Sysplorer runtime"
        return _json(out)

    hr = driver.api_help(cmd)
    if not hr.ok:
        out["error"] = hr.error
        return _json(out)

    text = hr.data
    if text is None:
        text = hr.raw
    if text is None:
        text = ""
    out["ok"] = True
    out["help_text"] = str(text)
    return _json(out)
