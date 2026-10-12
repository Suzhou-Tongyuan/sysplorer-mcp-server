# -*- mode: python ; coding: utf-8 -*-
# Ship a copy of repo `resources/` beside the built exe (see path_config.get_resources_root).
#
# Exclude tools/rag/modelica_doc_index.json from the bundle: it can be hundreds of MB.
# Frozen runtime resolves the default merged index to DEPLOY_ROOT/resources/indexes/modelica_doc_index.json
# (path_config.RAG_INDEX_PATH); Sysblock 等语料索引同目录，见 resources_manifest.json 的 index_file。
# 也可设置 MCP_RAG_INDEX_PATH / --rag-index-path。
import glob
import os

from PyInstaller.utils.hooks import collect_all

# SPECPATH = directory containing this .spec (install/windows); repo root is two levels up.
_REPO_ROOT = os.path.normpath(os.path.join(SPECPATH, '..', '..'))
_MCP_ROOT = os.path.join(_REPO_ROOT, 'sysplorer-mcp-server')

# PyInstaller 6 Analysis.datas only accepts (src, dest_dir) 2-tuples, not Tree objects.
_tools_root = os.path.normpath(os.path.join(_MCP_ROOT, 'tools'))
_tools_datas = []
for _dirpath, _dirnames, filenames in os.walk(_tools_root):
    for fn in filenames:
        if fn == 'modelica_doc_index.json':
            continue
        src = os.path.normpath(os.path.join(_dirpath, fn))
        rel_dir = os.path.relpath(_dirpath, _tools_root)
        trg = 'tools' if rel_dir == '.' else os.path.normpath(os.path.join('tools', rel_dir))
        _tools_datas.append((src, trg))

# Collect all mcp package dependencies
mcp_datas, mcp_binaries, mcp_hiddenimports = collect_all('mcp')
zstandard_datas, zstandard_binaries, zstandard_hiddenimports = collect_all('zstandard')

# Add pywin32 dependencies for Windows
pywin32_datas, pywin32_binaries, pywin32_hiddenimports = collect_all('win32')
pywin32comext_datas, pywin32comext_binaries, pywin32comext_hiddenimports = collect_all('win32comext')

# Add mworks-sysplorer dependencies (package is mworks.sysplorer — there is no top-level "sysplorer")
mworks_datas, mworks_binaries, mworks_hiddenimports = collect_all('mworks')
mworks_sysplorer_datas, mworks_sysplorer_binaries, mworks_sysplorer_hiddenimports = collect_all('mworks.sysplorer')

# Align with Tools/sysplorer_python_api/offline_install.txt base deps.
# websocket/jsonrpcclient/psutil are often lazy; colorama is top-level in sysplorer_api.
websocket_datas, websocket_binaries, websocket_hiddenimports = collect_all('websocket')
colorama_datas, colorama_binaries, colorama_hiddenimports = collect_all('colorama')
jsonrpcclient_datas, jsonrpcclient_binaries, jsonrpcclient_hiddenimports = collect_all('jsonrpcclient')
psutil_datas, psutil_binaries, psutil_hiddenimports = collect_all('psutil')
packaging_datas, packaging_binaries, packaging_hiddenimports = collect_all('packaging')

_api_binaries = (
    websocket_binaries + colorama_binaries + jsonrpcclient_binaries
    + psutil_binaries + packaging_binaries
)
_api_datas = (
    websocket_datas + colorama_datas + jsonrpcclient_datas
    + psutil_datas + packaging_datas
)
_api_hiddenimports = (
    [
        'websocket', 'colorama', 'jsonrpcclient', 'psutil', 'packaging',
    ]
    + websocket_hiddenimports + colorama_hiddenimports + jsonrpcclient_hiddenimports
    + psutil_hiddenimports + packaging_hiddenimports
)

_mcp_root_py = [(p, '.') for p in glob.glob(os.path.join(_MCP_ROOT, '*.py'))]

a = Analysis(
    [os.path.join(_MCP_ROOT, 'main.py')],
    pathex=[_REPO_ROOT, _MCP_ROOT],
    binaries=(
        mcp_binaries + zstandard_binaries + pywin32_binaries + pywin32comext_binaries
        + mworks_binaries + mworks_sysplorer_binaries
        + _api_binaries
    ),
    datas=[
        (os.path.join(_MCP_ROOT, 'core'), 'core'),
        *_tools_datas,
        *_mcp_root_py,
    ] + (
        mcp_datas + zstandard_datas + pywin32_datas + pywin32comext_datas
        + mworks_datas + mworks_sysplorer_datas
        + _api_datas
    ),
    hiddenimports=(
        [
            'uuid', 'asyncio', 'concurrent.futures', 'json', 'html', 'http', 'urllib',
            'datetime', 'typing', 'collections', 'functools', 'itertools', 're',
            'subprocess', 'threading', 'multiprocessing', 'queue', 'time', 'math',
            'random', 'hashlib', 'base64', 'struct', 'socket', 'ssl', 'tempfile',
            'shutil', 'glob', 'tarfile', 'zstandard',
            # Frozen exe skips site.py; modelica_lite ModelingPy.Help needs pydoc.help.
            'pydoc', 'pydoc_data', 'pydoc_data.topics',
        ]
        + _api_hiddenimports
        + mcp_hiddenimports + zstandard_hiddenimports
        + pywin32_hiddenimports + pywin32comext_hiddenimports
        + mworks_hiddenimports + mworks_sysplorer_hiddenimports
    ),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='sysplorer_mcp_server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
