# -*- mode: python ; coding: utf-8 -*-
import glob
import os

from PyInstaller.utils.hooks import collect_all

_REPO_ROOT = os.path.normpath(os.path.join(SPECPATH, '..', '..', '..'))
_MCP_ROOT = os.path.join(_REPO_ROOT, 'sysplorer-mcp-server')
_TOOLS_ROOT = os.path.join(_MCP_ROOT, 'tools')

_tools_datas = []
for _dirpath, _dirnames, _filenames in os.walk(_TOOLS_ROOT):
    for _filename in _filenames:
        if _filename == 'modelica_doc_index.json':
            continue
        _src = os.path.normpath(os.path.join(_dirpath, _filename))
        _rel_dir = os.path.relpath(_dirpath, _TOOLS_ROOT)
        _dest = 'tools' if _rel_dir == '.' else os.path.normpath(os.path.join('tools', _rel_dir))
        _tools_datas.append((_src, _dest))

_mcp_root_py = [(path, '.') for path in glob.glob(os.path.join(_MCP_ROOT, '*.py'))]
_optional_datas = []
_meta_data = os.path.join(_REPO_ROOT, 'private_lib', 'MetaDataLib.json')
if os.path.isfile(_meta_data):
    _optional_datas.append((_meta_data, 'private_lib'))

mcp_datas, mcp_binaries, mcp_hiddenimports = collect_all('mcp')
zstandard_datas, zstandard_binaries, zstandard_hiddenimports = collect_all('zstandard')

hiddenimports = [
    'uuid', 'asyncio', 'concurrent.futures', 'json', 'html', 'http', 'urllib',
    'datetime', 'typing', 'collections', 'functools', 'itertools', 're',
    'subprocess', 'threading', 'multiprocessing', 'queue', 'time', 'math',
    'random', 'hashlib', 'base64', 'struct', 'socket', 'ssl', 'tempfile',
    'shutil', 'glob', 'tarfile', 'zstandard',
    'pydoc', 'pydoc_data', 'pydoc_data.topics',
] + mcp_hiddenimports + zstandard_hiddenimports

a = Analysis(
    [os.path.join(_MCP_ROOT, 'main.py')],
    pathex=[_REPO_ROOT, _MCP_ROOT],
    binaries=mcp_binaries + zstandard_binaries,
    datas=[
        (os.path.join(_MCP_ROOT, 'core'), 'core'),
        *_tools_datas,
        *_mcp_root_py,
        *_optional_datas,
    ] + mcp_datas + zstandard_datas,
    hiddenimports=hiddenimports,
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
