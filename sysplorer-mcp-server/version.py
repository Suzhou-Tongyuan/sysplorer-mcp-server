"""MCP 服务端版本。

- **手工配置**：与仓库 ``install/package_version.json`` 中的 ``version_base``（如 ``0.5``）保持一致。
- **打包元数据**：由 ``install/write_build_meta.py`` 生成 ``_build_meta.py``（含 ``VERSION_BASE``、``BUILD_COUNTER`` 等）。
- **内部版**：完整版本为 ``{VERSION_BASE}.{BUILD_COUNTER}``，其中 ``BUILD_COUNTER`` 为打包时 ``git rev-list --count HEAD``。
- **发布版**：仅 ``VERSION_BASE``（``BUILD_COUNTER`` 为 0）；开发态无 ``_build_meta`` 时展示 ``VERSION_BASE`` 默认值。
"""
from __future__ import annotations

from typing import Any, Dict

# 与 install/package_version.json 的 version_base 保持一致（无 _build_meta 时的回退）
VERSION_BASE = "0.5"
VERSION_CORE = VERSION_BASE  # 历史字段，等价于 version_base

try:
    import _build_meta as _bm
except ImportError:
    BUILD_COUNTER = 0
    BUILD_TIME_ISO = ""
    GIT_REVISION = ""
    SOURCE_GIT_COMMIT_COUNT = 0
else:
    VERSION_BASE = _bm.VERSION_BASE
    VERSION_CORE = VERSION_BASE
    BUILD_COUNTER = _bm.BUILD_COUNTER
    BUILD_TIME_ISO = _bm.BUILD_TIME_ISO
    GIT_REVISION = _bm.GIT_REVISION
    SOURCE_GIT_COMMIT_COUNT = getattr(_bm, "SOURCE_GIT_COMMIT_COUNT", BUILD_COUNTER)


def get_version_full() -> str:
    if BUILD_COUNTER:
        return f"{VERSION_BASE}.{BUILD_COUNTER}"
    return VERSION_BASE


def get_version_display() -> str:
    """人类可读版本号；内部构建（BUILD_COUNTER > 0）附加 (Internal)。"""
    v = get_version_full()
    if BUILD_COUNTER > 0:
        return f"{v}(Internal)"
    return v


def get_build_time_display() -> str:
    return BUILD_TIME_ISO if BUILD_TIME_ISO else "（开发态，未执行打包脚本）"


def get_version_info() -> Dict[str, Any]:
    if not BUILD_TIME_ISO:
        kind = "dev"
    elif BUILD_COUNTER > 0:
        kind = "internal"
    else:
        kind = "release"
    return {
        "version": get_version_full(),
        "version_display": get_version_display(),
        "version_base": VERSION_BASE,
        "version_core": VERSION_CORE,
        "build_counter": BUILD_COUNTER,
        "git_commit_count": SOURCE_GIT_COMMIT_COUNT,
        "build_kind": kind,
        "build_time": BUILD_TIME_ISO or None,
        "git_revision": GIT_REVISION or None,
    }


def format_version_banner() -> str:
    return f"MWorks MCP {get_version_display()} | 打包时间: {get_build_time_display()}"
