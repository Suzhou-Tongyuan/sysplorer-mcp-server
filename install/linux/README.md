# Linux Distribution

Linux now has a packaging path for layout validation, config installation, and a PyInstaller-built native executable.

## Current Status

The current `sysplorer_mcp_server` runtime is still not feature-complete on Linux.

Windows-only dependencies remain in the codebase, including:

- `mworks.sysplorer`
- Windows process discovery and kill commands such as `tasklist`, `wmic`, and `taskkill`
- Windows solver/runtime binaries such as `MWSolver.exe`
- Windows registry PATH recovery

Because of those dependencies, the Linux package is **limited support**, not full parity with Windows.

## What This Linux Package Supports

- build a Linux distribution folder under `install/dist/linux-x64/`
- build a native Linux executable with PyInstaller
- install `sysplorer_mcp` entries into Claude Code and OpenCode config files
- validate package layout, binary startup, templates, and client wiring on a Linux machine

## What It Does Not Promise

- no Sysplorer-backed simulation workflow on Linux
- no claim that `mworks_sysplorer_session_manager` or modeling tools will succeed on Linux
- no claim of Sysplorer feature parity with Windows even though a native Linux binary is produced

## Scripts

- `scripts/build_publish.sh` — 与 Windows 上 `install/build_publish.ps1` 等价：生成 `publish/sysplorer_mcp/`（`main.py`、`sysplorer-mcp-server/`、`resources/`、`MCP_BUILD_INFO.json`、`README.md`（自 `install/windows/README.md` 复制）、`install_mcp.sh`）。**不包含** PyInstaller / exe。
- `scripts/build.sh` — Linux 原生可执行文件 + `tar.gz`（PyInstaller）；与 Windows `install/build.ps1` 的 exe 流程对应；若仅需源码发布目录请用 `build_publish.sh`。
- `scripts/install_mcp.sh` — 一键写入 Claude / OpenCode / Codex 配置；自动识别**源码包**（存在 `main.py` 与 `sysplorer-mcp-server/`）或**二进制包**（存在 `sysplorer_mcp_server`）。

## 发布目录（推荐，与 ps1 发布一致）

在仓库根目录执行：

```bash
bash install/linux/scripts/build_publish.sh
```

内部版（`version_base.<git 提交数>`）：

```bash
bash install/linux/scripts/build_publish.sh --internal
```

输出：`publish/sysplorer_mcp/`。将该目录复制到目标机后执行：

```bash
cd publish/sysplorer_mcp
bash ./install_mcp.sh
```

可选参数与环境变量：`./install_mcp.sh -d /opt/MWORKS/Sysplorer-2026a -p 'Sysplorer 2026a'`，或设置 `MWORKS_INSTALL_DIR`、`SYSPLORER_PLATFORM_LABEL`。

## Build（PyInstaller 二进制分发）

Run:

```bash
bash install/linux/scripts/build.sh
```

The build output is written to `install/dist/linux-x64/`.

## Distribution Contents

### `publish/sysplorer_mcp/`（`build_publish.sh`，与 Windows 发布目录一致）

- `main.py`、`sysplorer-mcp-server/`、`resources/`
- `install_mcp.sh`、`MCP_BUILD_INFO.json`、`README.md`

### `install/dist/linux-x64/`（`build.sh`，PyInstaller）

- `sysplorer_mcp_server` 可执行文件
- `install_mcp.sh`、`.mcp.json.example`、`claude.desktop.json.example`、`opencode.json.example`
- `requirements.txt`、`README.md`（自 `install/windows/README.md` 复制）、`manifest.json`

## Install on Target Machine

### 源码发布目录（推荐与 `build_publish.ps1` 对齐）

1. 构建机安装 `python3`（无需 PyInstaller）
2. 在仓库根执行 `bash install/linux/scripts/build_publish.sh`
3. 将 `publish/sysplorer_mcp/` 拷到目标机任意路径
4. 在该目录执行 `bash ./install_mcp.sh`（可选 `-d` / `-p` 或环境变量）
5. 重启 Claude Code / OpenCode / Codex CLI

### PyInstaller 二进制目录

1. 构建机安装 `python3` 与 PyInstaller
2. 执行 `bash install/linux/scripts/build.sh`
3. 将 `install/dist/linux-x64/` 拷到目标机
4. 执行 `bash install_mcp.sh`
5. 重启客户端并验证 MCP 进程能启动

## Linux Real-Machine Validation Checklist

Use this checklist on an actual Linux machine.

### 1. Environment Check

- [ ] `python3 --version` succeeds on the build machine
- [ ] `python3 -m PyInstaller --version` succeeds on the build machine
- [ ] `pwd` is inside the repository root when building
- [ ] `install/linux/pyinstaller/*.spec` is present

Recommended command:

```bash
python3 --version && python3 -m PyInstaller --version && ls -la install/linux/pyinstaller
```

### 2. Package Layout Check

Confirm these files exist:

- [ ] `sysplorer_mcp_server`
- [ ] `install_mcp.sh`
- [ ] `.mcp.json.example`
- [ ] `manifest.json`

Recommended command:

```bash
ls -la sysplorer_mcp_server install_mcp.sh .mcp.json.example manifest.json
file sysplorer_mcp_server || true
```

### 3. Native Binary Check

Build the executable:

```bash
bash install/linux/scripts/build.sh
```

Then confirm the binary can start:

- [ ] `./sysplorer_mcp_server --help` prints the argparse help text
- [ ] no shell permission error occurs
- [ ] the binary is directly executable without invoking Python manually

Recommended command:

```bash
chmod +x sysplorer_mcp_server install_mcp.sh && ./sysplorer_mcp_server --help
```

### 4. Client Config Check

Run:

```bash
bash install_mcp.sh
```

Then verify:

- [ ] `~/.claude.json` exists
- [ ] `~/.config/opencode/opencode.json` exists
- [ ] `~/.codex/config.toml` contains `[mcp_servers.sysplorer_mcp]`（`install_mcp.sh` 会写入）
- [ ] `mcpServers.sysplorer_mcp.command` 指向 Python 可执行文件（源码包）或 `sysplorer_mcp_server` 路径（二进制包）
- [ ] `mcp.sysplorer_mcp.type` equals `local`
- [ ] 上述配置均含 `--mworks-install-dir` 与 `--sysplorer-platform-label`

Recommended command:

```bash
python3 - <<'PY'
import json, pathlib
claude = pathlib.Path.home() / '.claude.json'
opencode = pathlib.Path.home() / '.config' / 'opencode' / 'opencode.json'
print(json.dumps(json.loads(claude.read_text(encoding='utf-8'))['mcpServers']['sysplorer_mcp'], indent=2, ensure_ascii=False))
print(json.dumps(json.loads(opencode.read_text(encoding='utf-8'))['mcp']['sysplorer_mcp'], indent=2, ensure_ascii=False))
PY
```

### 5. Client Wiring Check

After restarting Claude Code or OpenCode:

- [ ] the client can see the `sysplorer_mcp` entry
- [ ] launching the MCP process does not immediately fail because of missing script permissions
- [ ] the process at least reaches binary startup and argument parsing

Suggested checks:

- Claude Code: inspect MCP list/status in the client
- OpenCode: inspect MCP status or startup logs in the client

### 7. Expected Linux Limitation Check

These outcomes are currently acceptable on Linux:

- [ ] `mworks_sysplorer_session_manager` may fail because `mworks.sysplorer` is unavailable
- [ ] Sysplorer/model/simulation tools may fail because the runtime is Windows-dependent
- [ ] failures mentioning `tasklist`, `wmic`, `taskkill`, `mworks.sysplorer`, or `MWSolver.exe` are consistent with the current support boundary

### 8. Pass Criteria

Treat the Linux package as validated if all of the following are true:

- [ ] distribution folder builds successfully
- [ ] native executable runs and shows `--help`
- [ ] Claude config is written correctly
- [ ] OpenCode config is written correctly
- [ ] the MCP client can attempt to launch the process
- [ ] any remaining failure is clearly due to the known Windows-only runtime dependency, not packaging or config wiring
