"""
统一 MCP 进程及其子进程在 Windows 上的标准 I/O / Python 文本编码为 UTF-8。

OpenCode、Codex、Cursor 等宿主常以系统默认代码页创建 MCP 子进程；不处理时易出现
日志、JSON-RPC 与 Sysplorer worker 管道中的乱码。本模块在入口尽早设置环境变量并对
``sys.stdin``/``stdout``/``stderr`` 做 ``reconfigure``，并对 ``subprocess.run``/``Popen``
使用的子进程环境做合并。

禁用（排障）：``MWORKS_MCP_DISABLE_UTF8_BOOTSTRAP=1`` 跳过宿主引导；
``MWORKS_MCP_CHILD_UTF8=0`` 跳过向子进程注入 ``PYTHONUTF8``/``PYTHONIOENCODING``。

**Sysplorer 子进程（Windows）**：部分 MCP 宿主（如 OpenCode）会给 MCP 根进程设 ``PYTHONUTF8=1``，
``os.environ.copy()`` 会把它带进 Sysplorer 自带的 ``python.exe``。解释器在 UTF-8 模式下与 ``mwk_*.dll``
等原生栈对窄字节串（ACP/CP936）的约定不一致，易出现中文路径/参数乱码。对 **仅** 用于加载 MWorks 的
子进程环境应调用 :func:`windows_mworks_bundled_python_env` 剥掉这些变量；JSON 管道仍由
``Popen(..., encoding="utf-8")`` 显式处理，不依赖上述环境变量。

保留 UTF-8 模式（排障）：``MWORKS_KEEP_UTF8_IN_SYSPLORER_PYTHON=1``。

**MCP 根进程（Windows）**：OpenCode 等会给 **当前** 解释器打开 UTF-8 模式；若 ``mworks.sysplorer``
在本进程内加载，则 ``mwk_compiler*.dll`` 仍会得到错误的路径编码。此时必须在 import 任何业务代码
**之前**用 :func:`maybe_reexec_windows_mcp_host_for_mworks_native` 做一次 ``execve``：去掉
``PYTHONUTF8`` / ``-X utf8``，并显式设 ``PYTHONIOENCODING=utf-8`` 以保持 MCP JSON-RPC 与日志仍按 UTF-8 读写。

跳过重启（排障）：``MWORKS_MCP_SKIP_WINDOWS_UTF8_REEXEC=1``。

若宿主用 ``python -c ...`` 启动 MCP，须用 ``[-c, 代码, …]`` 重建 ``exec`` 参数；旧实现曾误跳过此类启动，导致 OpenCode 等仍带 UTF-8 模式加载原生栈。

排障快照：设 ``MWORKS_MCP_DEBUG_STARTUP=1`` 后，会在系统临时目录写入
``mworks_sysplorer_mcp_startup_debug_<phase>.json``（``before_reexec`` / ``after_bootstrap``）；
可选 ``MWORKS_MCP_DEBUG_STARTUP_FILE=C:\\path\\base.json`` 指定基名（会写成 ``base_before_reexec.json`` 等）。
"""
from __future__ import annotations

import os
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, List, MutableMapping


def _truthy_off(val: str) -> bool:
    return val.strip().lower() in ("1", "true", "yes", "on")


def _truthy_on(val: str) -> bool:
    return val.strip().lower() in ("1", "true", "yes", "on")


def _child_utf8_disabled() -> bool:
    raw = os.environ.get("MWORKS_MCP_CHILD_UTF8", "").strip().lower()
    return raw in ("0", "false", "no", "off")


def _encoding_debug_environ_snapshot() -> Dict[str, str]:
    """与编码 / MWorks 相关的环境变量子集（避免把任意密钥整表导出）。"""
    out: Dict[str, str] = {}
    for k, v in os.environ.items():
        ku = k.upper()
        if (
            ku.startswith("PYTHON")
            or ku.startswith("MWORKS")
            or ku.startswith("MCP_")
            or ku.startswith("LANG")
            or ku.startswith("LC_")
            or k == "PROCESSOR_ARCHITECTURE"
        ):
            out[k] = v
    return dict(sorted(out.items()))


def write_mcp_startup_debug_file(phase: str) -> None:
    """
    ``MWORKS_MCP_DEBUG_STARTUP=1`` 时写入 JSON 快照，便于对比 OpenCode / Cursor 等宿主差异。

    默认目录：``tempfile.gettempdir()``；文件名 ``mworks_sysplorer_mcp_startup_debug_<phase>.json``。
    若设置 ``MWORKS_MCP_DEBUG_STARTUP_FILE``，则为基路径 stem，实际写入 ``{stem}_{phase}.json`` 与同目录。
    """
    if not _truthy_on(os.environ.get("MWORKS_MCP_DEBUG_STARTUP", "")):
        return
    import json
    import locale
    import tempfile

    data: Dict[str, Any] = {
        "phase": phase,
        "executable": sys.executable,
        "version": sys.version.split()[0],
        "argv": list(sys.argv),
        "utf8_mode": int(getattr(sys.flags, "utf8_mode", 0)),
        "stdout_encoding": getattr(sys.stdout, "encoding", None),
        "preferredencoding": locale.getpreferredencoding(False),
        "environ_subset": _encoding_debug_environ_snapshot(),
    }
    if sys.platform == "win32":
        try:
            import ctypes

            k32 = ctypes.WinDLL("kernel32", use_last_error=True)
            data["windows_acp"] = int(k32.GetACP())
        except Exception as exc:
            data["windows_acp_error"] = str(exc)

    raw_base = os.environ.get("MWORKS_MCP_DEBUG_STARTUP_FILE", "").strip()
    if raw_base:
        base = Path(raw_base).expanduser()
        out_path = base.parent / f"{base.stem}_{phase}{base.suffix or '.json'}"
    else:
        out_path = Path(tempfile.gettempdir()) / f"mworks_sysplorer_mcp_startup_debug_{phase}.json"
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        return


def bootstrap_host_stdio_utf8() -> None:
    """
    在 ``main`` 最先调用：为当前 MCP 进程设置 UTF-8 默认值并尽量将标准流切到 UTF-8。

    在 ``stdio_isolate`` 之前调用仍有用：早期写往原 stdout 的文本与宿主解码一致。
    """
    if _truthy_off(os.environ.get("MWORKS_MCP_DISABLE_UTF8_BOOTSTRAP", "")):
        return
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    if sys.platform != "win32":
        return
    for name in ("stdin", "stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None or not hasattr(stream, "reconfigure"):
            continue
        try:
            if getattr(stream, "closed", False):
                continue
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError, TypeError):
            continue


def merge_subprocess_utf8_env(env: MutableMapping[str, str]) -> Dict[str, str]:
    """
    返回 ``env`` 的副本，并为 Sysplorer 捆绑 Python 子进程合并 UTF-8 相关变量。

    使用 ``setdefault``：宿主或用户已在 JSON/TOML 中配置的 ``PYTHON*`` 不被覆盖。
    设置 ``MWORKS_MCP_CHILD_UTF8=0`` 可关闭此合并（排障）。
    """
    out = dict(env)
    if _child_utf8_disabled():
        return out
    out.setdefault("PYTHONUTF8", "1")
    out.setdefault("PYTHONIOENCODING", "utf-8")
    return out


def subprocess_text_kw() -> Dict[str, object]:
    """``subprocess.run(..., text=True, **subprocess_text_kw())`` 的统一解码参数。"""
    return {"encoding": "utf-8", "errors": "replace"}


def _strip_utf8_x_flags_from_argv(argv: List[str]) -> List[str]:
    """Drop ``-X utf8`` / ``-X utf-8`` so a restarted interpreter does not re-enable UTF-8 mode."""
    out: List[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-X", "/X") and i + 1 < len(argv):
            nxt = argv[i + 1].strip().lower()
            if nxt in ("utf8", "utf-8"):
                i += 2
                continue
        low = a.lstrip("-/").lower()
        if low.startswith("xutf8") or low.startswith("x utf8"):
            i += 1
            continue
        out.append(a)
        i += 1
    return out


def maybe_reexec_windows_mcp_host_for_mworks_native() -> None:
    """
    在 Windows 上，若解释器以 UTF-8 模式启动，则 ``execve`` 为本进程换一套环境：**关闭** UTF-8 模式，
    **保留** ``PYTHONIOENCODING=utf-8``（stdio 仍按 UTF-8，满足 MCP JSON-RPC）。

    须在 ``main`` 中、在 ``import path_config`` / ``import mworks`` 之前调用，且仅执行一次。
    """
    if sys.platform != "win32":
        return
    if _truthy_on(os.environ.get("MWORKS_MCP_SKIP_WINDOWS_UTF8_REEXEC", "")):
        return
    if os.environ.get("MWORKS_MCP_REEXEC_DONE") == "1":
        return

    utf8_on = bool(getattr(sys.flags, "utf8_mode", 0))
    env_utf8 = _truthy_on(os.environ.get("PYTHONUTF8", ""))
    if not utf8_on and not env_utf8:
        return

    new_env = dict(os.environ)
    new_env.pop("PYTHONUTF8", None)
    new_env.pop("PYTHONWUTF8", None)
    new_env["PYTHONIOENCODING"] = "utf-8"
    new_env["MWORKS_MCP_REEXEC_DONE"] = "1"

    # OpenCode 等常用 ``python -c "<inline>"`` 起 MCP：argv[0] 为 ``-c``，须整段保留，不可当脚本路径。
    if getattr(sys, "frozen", False):
        exec_argv = [sys.executable] + _strip_utf8_x_flags_from_argv(list(sys.argv[1:]))
    elif not sys.argv:
        return
    elif sys.argv[0] == "-c":
        exec_argv = [sys.executable] + _strip_utf8_x_flags_from_argv(list(sys.argv))
    else:
        script = str(Path(sys.argv[0]).resolve())
        rest = _strip_utf8_x_flags_from_argv(list(sys.argv[1:]))
        exec_argv = [sys.executable, script] + rest

    write_mcp_startup_debug_file("before_reexec")
    try:
        os.execve(sys.executable, exec_argv, new_env)
    except OSError:
        # 若 exec 失败，继续运行；此时仍可能乱码，用户可改用子进程 worker 或调整宿主环境
        return


@contextmanager
def windows_strip_utf8_mode_env_while_calling_native() -> Iterator[None]:
    """
    在调用 ``StartSysplorer`` 等会拉起/触碰 MWorks 原生栈的 API 前后，暂时从 ``os.environ`` 去掉
    ``PYTHONUTF8`` / ``PYTHONWUTF8``，避免子进程（如 ``mworks.exe``）继承宿主 CLI 注入的 UTF-8 模式变量。

    与 :func:`windows_mworks_bundled_python_env` 同属「与原生 DLL 窄字节约定对齐」的隔离措施。
    跳过：``MWORKS_KEEP_UTF8_IN_SYSPLORER_PYTHON=1``。
    """
    if sys.platform != "win32":
        yield
        return
    if _truthy_on(os.environ.get("MWORKS_KEEP_UTF8_IN_SYSPLORER_PYTHON", "")):
        yield
        return
    keys = ("PYTHONUTF8", "PYTHONWUTF8")
    saved: Dict[str, str] = {}
    for k in keys:
        if k in os.environ:
            saved[k] = os.environ[k]
            del os.environ[k]
    try:
        yield
    finally:
        for k, v in saved.items():
            os.environ[k] = v


def windows_mworks_bundled_python_env(env: MutableMapping[str, str]) -> Dict[str, str]:
    """
    从传给 Sysplorer **捆绑** ``python.exe`` 的环境副本中移除 UTF-8 模式相关变量（仅 Windows）。

    宿主注入的 ``PYTHONUTF8`` 等在子解释器启动时生效，会导致与 MWorks 原生 DLL 的编码约定冲突；
    与 MCP↔worker 的 NDJSON 传输无关（由 ``Popen`` 的 ``encoding=`` 决定）。
    """
    out = dict(env)
    if sys.platform != "win32":
        return out
    if _truthy_on(os.environ.get("MWORKS_KEEP_UTF8_IN_SYSPLORER_PYTHON", "")):
        return out
    for key in ("PYTHONUTF8", "PYTHONWUTF8", "PYTHONIOENCODING"):
        out.pop(key, None)
    # 无 UTF-8 模式时仍让捆绑 Python 的 stdio 用 UTF-8（与 Popen(encoding=) 一致），窄字节路径走 ACP
    out.setdefault("PYTHONIOENCODING", "utf-8")
    return out
