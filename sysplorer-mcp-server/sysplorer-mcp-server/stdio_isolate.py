"""
Isolate native (C/C++) and third-party Python ``print`` from MCP JSON-RPC on stdio.

POSIX: dup fd 1 to keep the client pipe, dup2 log onto fd 1/2.

Windows: additionally call SetStdHandle(STD_OUTPUT/ERROR) so DLLs that use
GetStdHandle (typical for MSVC/UCRT) do not keep writing to the MCP pipe —
os.dup2 alone only affects the CRT file descriptor table, which Sysplorer
native code may not use.

**Important:** ``mworks.sysplorer`` prints Chinese progress lines (e.g. "连接失败!",
"连接成功!") to **Python ``sys.stdout``**.  MCP's ``stdio_server`` also writes JSON-RPC
to stdout.  Therefore we bind ``sys.stdout`` / ``sys.stderr`` to the log file and
return a **dedicated fd** for MCP to use via ``stdio_server(stdout=...)`` only.
"""
from __future__ import annotations

import os
import sys
from typing import TextIO

__all__ = ["isolate_mcp_stdio_from_native_output"]


def isolate_mcp_stdio_from_native_output(log_fh: TextIO) -> int:
    """
    Redirect OS-level stdout/stderr and **Python** ``sys.stdout`` / ``sys.stderr``
    to ``log_fh``.  Return a duplicated fd that still writes to the original
    process stdout (the MCP client pipe when launched by Cursor).

    Caller must pass this fd to ``stdio_server(stdout=...)`` so JSON-RPC does not
    share ``sys.stdout`` with Sysplorer bindings.
    """
    log_fileno = log_fh.fileno()
    if sys.platform == "win32":
        return _isolate_windows(log_fh, log_fileno)
    return _isolate_posix(log_fh, log_fileno)


def _isolate_posix(log_fh: TextIO, log_fileno: int) -> int:
    mcp_fd = os.dup(1)
    os.dup2(log_fileno, 1)
    sys.stdout = log_fh
    os.dup2(log_fileno, 2)
    sys.stderr = log_fh
    return mcp_fd


def _isolate_windows(log_fh: TextIO, log_fileno: int) -> int:
    import ctypes
    import msvcrt
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    DUPLICATE_SAME_ACCESS = 0x00000002
    STD_OUTPUT_HANDLE = wintypes.DWORD(-11 & 0xFFFFFFFF)
    STD_ERROR_HANDLE = wintypes.DWORD(-12 & 0xFFFFFFFF)

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

    try:
        log_handle = msvcrt.get_osfhandle(log_fileno)
    except OSError:
        return _isolate_posix(log_fh, log_fileno)

    orig_out = GetStdHandle(STD_OUTPUT_HANDLE)
    inv = ctypes.c_void_p(-1).value
    orig_v = ctypes.cast(orig_out, ctypes.c_void_p).value
    if not orig_v or orig_v == inv:
        return _isolate_posix(log_fh, log_fileno)

    mcp_copy = wintypes.HANDLE()
    ok = DuplicateHandle(
        GetCurrentProcess(),
        orig_out,
        GetCurrentProcess(),
        ctypes.byref(mcp_copy),
        0,
        False,
        DUPLICATE_SAME_ACCESS,
    )
    if not ok:
        return _isolate_posix(log_fh, log_fileno)

    mcp_copy_v = mcp_copy.value or 0
    if mcp_copy_v == 0 or mcp_copy_v == inv:
        return _isolate_posix(log_fh, log_fileno)

    log_h = wintypes.HANDLE(log_handle)

    def _fail() -> int:
        CloseHandle(mcp_copy)
        return _isolate_posix(log_fh, log_fileno)

    if not SetStdHandle(STD_OUTPUT_HANDLE, log_h):
        return _fail()
    if not SetStdHandle(STD_ERROR_HANDLE, log_h):
        return _fail()

    try:
        os.dup2(log_fileno, 1)
        os.dup2(log_fileno, 2)
    except OSError:
        return _fail()

    try:
        rpc_fd = msvcrt.open_osfhandle(mcp_copy_v, os.O_WRONLY)
    except OSError:
        return _fail()

    sys.stdout = log_fh
    sys.stderr = log_fh
    return int(rpc_fd)
