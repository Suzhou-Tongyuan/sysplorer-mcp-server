"""Launch-context helpers for starting Sysplorer under agent-hosted MCP servers.

Goal on Windows: do not let an MCP host's UTF-8 console/pipe context leak into
``StartSysplorer()`` and then further into ``mworks.exe -> cmd.exe -> build.bat``.

The default strategy is intentionally conservative:

- remove a small set of env vars that force Python UTF-8 / code-page behavior
- temporarily detach ``stdin/stdout/stderr`` from agent pipes by redirecting them
  to ``os.devnull`` while calling ``StartSysplorer``
- best-effort detach from any inherited console before launch

This approximates a desktop-style GUI launch without hardcoding a code page such
as 936, so user/system defaults can take effect naturally.
"""
from __future__ import annotations

import contextlib
import logging
import os
import platform
import sys
import time
from pathlib import Path
from typing import Dict, Iterator, Mapping, MutableMapping, Optional

_log = logging.getLogger(__name__)

_ENV_VARS_TO_CLEAR = (
    "CHCP",
    "PYTHONIOENCODING",
    "PYTHONLEGACYWINDOWSFSENCODING",
    "PYTHONLEGACYWINDOWSSTDIO",
    "PYTHONUTF8",
)

_DEBUG_ENV_KEYS = (
    "CHCP",
    "PYTHONIOENCODING",
    "PYTHONLEGACYWINDOWSFSENCODING",
    "PYTHONLEGACYWINDOWSSTDIO",
    "PYTHONUTF8",
    "COMSPEC",
    "PATH",
)


def sanitize_sysplorer_child_env(
    env: Optional[Mapping[str, str]] = None,
    *,
    for_windows: Optional[bool] = None,
) -> Dict[str, str]:
    """Return a child env with agent-forced UTF-8/code-page knobs removed.

    The input environment is copied. On non-Windows platforms the copy is
    returned unchanged.
    """
    is_windows = platform.system() == "Windows" if for_windows is None else bool(for_windows)
    out = dict(os.environ if env is None else env)
    if not is_windows:
        return out
    for key in _ENV_VARS_TO_CLEAR:
        out.pop(key, None)
    return out


def _debug_enabled() -> bool:
    raw = os.environ.get("MWORKS_STARTSYSPLORER_DEBUG", "1").strip().lower()
    return raw not in ("0", "false", "no", "off")


def _debug_log(message: str) -> None:
    if _debug_enabled():
        _log.warning("launch_context %s", message)


def _snapshot_selected_env(env: Optional[Mapping[str, str]] = None) -> Dict[str, str]:
    source = os.environ if env is None else env
    snap: Dict[str, str] = {}
    for key in _DEBUG_ENV_KEYS:
        value = source.get(key)
        if value is None:
            snap[key] = "<unset>"
        elif key == "PATH":
            parts = [p for p in value.split(os.pathsep) if p]
            snap[key] = os.pathsep.join(parts[:8])
            if len(parts) > 8:
                snap[key] += f"{os.pathsep}...(+{len(parts) - 8} more)"
        else:
            snap[key] = value
    return snap


def desktop_like_sysplorer_launch_enabled() -> bool:
    """Whether Windows StartSysplorer isolation is enabled."""
    raw = os.environ.get("MWORKS_STARTSYSPLORER_DESKTOP_CONTEXT", "1").strip().lower()
    return raw not in ("0", "false", "no", "off")


@contextlib.contextmanager
def desktop_like_sysplorer_launch_context() -> Iterator[None]:
    """Best-effort temporary context for launching Sysplorer like a desktop GUI app."""
    if platform.system() != "Windows" or not desktop_like_sysplorer_launch_enabled():
        _debug_log(
            "desktop_like_sysplorer_launch_context bypassed "
            f"platform={platform.system()} enabled={desktop_like_sysplorer_launch_enabled()} "
            f"env={_snapshot_selected_env()}"
        )
        yield
        return

    saved_env = {key: os.environ.get(key) for key in _ENV_VARS_TO_CLEAR}
    _debug_log(f"desktop context enter saved_env={saved_env} selected_env={_snapshot_selected_env()}")
    for key in _ENV_VARS_TO_CLEAR:
        os.environ.pop(key, None)
    _debug_log(f"desktop context after env clear selected_env={_snapshot_selected_env()}")

    try:
        with _windows_stdio_detached_to_devnull():
            yield
    finally:
        _restore_env(os.environ, saved_env)
        _debug_log(f"desktop context restored selected_env={_snapshot_selected_env()}")


def _restore_env(target: MutableMapping[str, str], saved: Mapping[str, Optional[str]]) -> None:
    for key, value in saved.items():
        if value is None:
            target.pop(key, None)
        else:
            target[key] = value


@contextlib.contextmanager
def _windows_stdio_detached_to_devnull() -> Iterator[None]:
    import ctypes
    import msvcrt
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    DUPLICATE_SAME_ACCESS = 0x00000002
    STD_INPUT_HANDLE = wintypes.DWORD(-10 & 0xFFFFFFFF)
    STD_OUTPUT_HANDLE = wintypes.DWORD(-11 & 0xFFFFFFFF)
    STD_ERROR_HANDLE = wintypes.DWORD(-12 & 0xFFFFFFFF)
    ATTACH_PARENT_PROCESS = wintypes.DWORD(-1 & 0xFFFFFFFF)

    GetStdHandle = kernel32.GetStdHandle
    GetStdHandle.argtypes = (wintypes.DWORD,)
    GetStdHandle.restype = wintypes.HANDLE

    SetStdHandle = kernel32.SetStdHandle
    SetStdHandle.argtypes = (wintypes.DWORD, wintypes.HANDLE)
    SetStdHandle.restype = wintypes.BOOL

    GetCurrentProcess = kernel32.GetCurrentProcess
    GetCurrentProcess.restype = wintypes.HANDLE

    DuplicateHandle = kernel32.DuplicateHandle
    DuplicateHandle.argtypes = [
        wintypes.HANDLE,
        wintypes.HANDLE,
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.HANDLE),
        wintypes.DWORD,
        wintypes.BOOL,
        wintypes.DWORD,
    ]
    DuplicateHandle.restype = wintypes.BOOL

    CloseHandle = kernel32.CloseHandle
    CloseHandle.argtypes = (wintypes.HANDLE,)
    CloseHandle.restype = wintypes.BOOL

    GetConsoleWindow = kernel32.GetConsoleWindow
    GetConsoleWindow.restype = wintypes.HWND

    GetConsoleCP = kernel32.GetConsoleCP
    GetConsoleCP.restype = wintypes.UINT

    GetConsoleOutputCP = kernel32.GetConsoleOutputCP
    GetConsoleOutputCP.restype = wintypes.UINT

    GetFileType = kernel32.GetFileType
    GetFileType.argtypes = (wintypes.HANDLE,)
    GetFileType.restype = wintypes.DWORD

    FreeConsole = kernel32.FreeConsole
    FreeConsole.restype = wintypes.BOOL

    AttachConsole = kernel32.AttachConsole
    AttachConsole.argtypes = (wintypes.DWORD,)
    AttachConsole.restype = wintypes.BOOL

    devnull_in = devnull_out = None
    saved_py_stdin = saved_py_stdout = saved_py_stderr = None
    saved_handles = {
        STD_INPUT_HANDLE.value: None,
        STD_OUTPUT_HANDLE.value: None,
        STD_ERROR_HANDLE.value: None,
    }
    had_console = bool(GetConsoleWindow())

    inv = ctypes.c_void_p(-1).value

    def _handle_value(handle: wintypes.HANDLE) -> int:
        return ctypes.cast(handle, ctypes.c_void_p).value or 0

    def _file_type(handle: wintypes.HANDLE) -> int:
        value = _handle_value(handle)
        if value == 0 or value == inv:
            return -1
        return int(GetFileType(handle))

    def _duplicate_handle(handle: wintypes.HANDLE) -> Optional[wintypes.HANDLE]:
        value = _handle_value(handle)
        if value == 0 or value == inv:
            return None
        dup = wintypes.HANDLE()
        ok = DuplicateHandle(
            GetCurrentProcess(),
            handle,
            GetCurrentProcess(),
            ctypes.byref(dup),
            0,
            True,
            DUPLICATE_SAME_ACCESS,
        )
        if not ok:
            return None
        dup_value = _handle_value(dup)
        if dup_value == 0 or dup_value == inv:
            try:
                CloseHandle(dup)
            except Exception:
                pass
            return None
        return dup

    def _stdio_snapshot(label: str) -> None:
        _debug_log(
            f"{label} console={had_console} "
            f"console_cp={int(GetConsoleCP())} console_output_cp={int(GetConsoleOutputCP())} "
            f"stdin=0x{_handle_value(GetStdHandle(STD_INPUT_HANDLE)):x}/type={_file_type(GetStdHandle(STD_INPUT_HANDLE))} "
            f"stdout=0x{_handle_value(GetStdHandle(STD_OUTPUT_HANDLE)):x}/type={_file_type(GetStdHandle(STD_OUTPUT_HANDLE))} "
            f"stderr=0x{_handle_value(GetStdHandle(STD_ERROR_HANDLE)):x}/type={_file_type(GetStdHandle(STD_ERROR_HANDLE))}"
        )

    try:
        detach_started = time.monotonic()
        _stdio_snapshot("before_detach")
        saved_handles = {
            STD_INPUT_HANDLE.value: _duplicate_handle(GetStdHandle(STD_INPUT_HANDLE)),
            STD_OUTPUT_HANDLE.value: _duplicate_handle(GetStdHandle(STD_OUTPUT_HANDLE)),
            STD_ERROR_HANDLE.value: _duplicate_handle(GetStdHandle(STD_ERROR_HANDLE)),
        }

        devnull_in = open(os.devnull, "r", encoding="utf-8", buffering=1)
        devnull_out = open(os.devnull, "a", encoding="utf-8", buffering=1)
        in_handle = wintypes.HANDLE(msvcrt.get_osfhandle(devnull_in.fileno()))
        out_handle = wintypes.HANDLE(msvcrt.get_osfhandle(devnull_out.fileno()))

        if had_console:
            try:
                FreeConsole()
            except Exception:
                pass

        SetStdHandle(STD_INPUT_HANDLE, in_handle)
        SetStdHandle(STD_OUTPUT_HANDLE, out_handle)
        SetStdHandle(STD_ERROR_HANDLE, out_handle)

        saved_py_stdin, saved_py_stdout, saved_py_stderr = sys.stdin, sys.stdout, sys.stderr
        sys.stdin = devnull_in
        sys.stdout = devnull_out
        sys.stderr = devnull_out
        _stdio_snapshot("after_detach")
        _debug_log(f"after_detach elapsed_ms={int((time.monotonic() - detach_started) * 1000)}")
        yield
    finally:
        try:
            if saved_py_stdin is not None:
                sys.stdin = saved_py_stdin
            if saved_py_stdout is not None:
                sys.stdout = saved_py_stdout
            if saved_py_stderr is not None:
                sys.stderr = saved_py_stderr
        except Exception:
            _log.debug("Failed to restore Python stdio objects after StartSysplorer isolation", exc_info=True)

        if had_console:
            try:
                AttachConsole(ATTACH_PARENT_PROCESS)
            except Exception:
                pass

        for std_id, handle in saved_handles.items():
            if handle is None:
                continue
            try:
                SetStdHandle(wintypes.DWORD(std_id), handle)
            except Exception:
                pass
        _stdio_snapshot("after_restore")

        for fh in (devnull_in, devnull_out):
            if fh is not None:
                try:
                    fh.close()
                except OSError:
                    pass

        for handle in saved_handles.values():
            if handle is not None:
                try:
                    CloseHandle(handle)
                except Exception:
                    pass


def start_sysplorer_in_desktop_context(
    start_fn,
    process_path: Path | str,
    start_mode: str = "-gui",
) -> None:
    """Call ``StartSysplorer`` under the temporary desktop-like launch context."""
    process_path = str(process_path)
    _debug_log(
        f"StartSysplorer begin start_mode={start_mode} "
        f"process_path={process_path} selected_env={_snapshot_selected_env()}"
    )
    with desktop_like_sysplorer_launch_context():
        start_fn(start_mode, processPath=process_path)
    _debug_log(
        f"StartSysplorer end start_mode={start_mode} "
        f"process_path={process_path} selected_env={_snapshot_selected_env()}"
    )
