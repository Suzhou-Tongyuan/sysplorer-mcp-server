# MWorks MCP 服务器安装包

本目录包含 MWorks Sysplorer MCP 服务器的 Windows 可执行版本，无需 Python 环境即可运行。

## 快速安装（推荐）

1. 右键点击 `install_mcp.ps1`，选择「使用 PowerShell 运行」
2. 按照提示输入 Sysplorer 安装路径和平台标签（直接回车使用默认值）
3. 脚本会自动将 MCP 配置添加到 Claude、OpenCode 与 Codex CLI（`~/.codex/config.toml`）中
4. 重启 Claude Code / OpenCode / Codex CLI 后即可使用

## 手动安装

如果一键安装脚本运行失败，可以手动配置：

### 1. 配置 Claude Code

编辑用户目录下的 `.claude.json` 文件（通常在 `C:\Users\你的用户名\.claude.json`），添加以下内容：

```json
{
  "mcpServers": {
    "sysplorer_mcp": {
      "command": "C:\\完整路径到\\sysplorer_mcp_server.exe",
      "args": [
        "--mworks-install-dir", "C:\\Program Files\\MWORKS\\Sysplorer 2026a",
        "--sysplorer-platform-label", "Sysplorer 2026a"
      ]
    }
  }
}
```

请将 `--mworks-install-dir` 的值替换为你实际的 Sysplorer 安装路径。

### 2. 配置 OpenCode

编辑用户目录下的 `.config/opencode/opencode.json` 文件（通常在 `C:\Users\你的用户名\.config\opencode\opencode.json`），添加以下内容：

```json
{
  "mcp": {
    "sysplorer_mcp": {
      "type": "local",
      "command": [
        "C:\\完整路径到\\sysplorer_mcp_server.exe",
        "--mworks-install-dir", "C:\\Program Files\\MWORKS\\Sysplorer 2026a",
        "--sysplorer-platform-label", "Sysplorer 2026a"
      ]
    }
  }
}
```

请将 `--mworks-install-dir` 的值替换为你实际的 Sysplorer 安装路径。

### 3. 配置 Codex CLI

在用户主目录下创建或编辑 `~/.codex/config.toml`（Windows 上一般为 `C:\Users\你的用户名\.codex\config.toml`），在文件中添加：

```toml
[mcp_servers.sysplorer_mcp]
command = 'C:\\完整路径到\\sysplorer_mcp_server.exe'
args = [
    '--mworks-install-dir',
    'C:\\Program Files\\MWORKS\\Sysplorer 2026a',
    '--sysplorer-platform-label',
    'Sysplorer 2026a',
]
```

路径中含单引号时请在 TOML 中用 `''` 转义，或改用双引号并按 TOML 规则转义反斜杠。

## 验证安装

重启客户端后，可以通过以下方式验证 MCP 是否正常加载：

1. 在 Claude Code 中输入 `/mcp list`，确认 `sysplorer_mcp` 出现在列表中
2. 调用 `mworks_sysplorer_session_manager(action="health")`，返回 JSON 中 `ok: true` 表示运行正常

## 故障诊断

### 日志位置说明
本 MCP 服务**强制将所有日志写入固定位置，不受客户端影响**，最可靠的日志路径是：
👉 **EXE 所在目录下的 `logs/server.log` 文件**（服务启动时会自动创建 `logs` 目录）

### 不同客户端的额外日志位置
部分 MCP 客户端也会自行捕获服务输出并保存到自己的日志目录：
- **Claude Code**: `%USERPROFILE%\.claude\mcp\logs\sysplorer_mcp_server*.log`
- **OpenCode / 豆包编程助手**: `%USERPROFILE%\.config\opencode\mcp\logs\`
- **Cursor / Windsurf**: `%APPDATA%\Cursor\User\globalStorage\mcp.logs\` 或类似目录
- **其他客户端**: 可以搜索系统盘下的 `sysplorer_mcp_server*.log` 或 `server.log` 文件快速定位

### 日志内容
所有日志文件都会记录：
- 启动时的 Python 版本、工作目录、参数和环境变量
- 模块导入和预检查结果
- 完整的错误栈信息（启动失败时）
- 运行时的所有警告和错误

### 快速查找技巧
在客户端的 MCP 日志中搜索 `Log file:` 关键词，可以直接找到服务输出的日志文件路径。

## 卸载

1. 删除各客户端配置中的 `sysplorer_mcp` 条目：`.claude.json`、`opencode.json`，以及 `~/.codex/config.toml` 里的 `[mcp_servers.sysplorer_mcp]` 整段
2. 删除本目录的所有文件即可

## 系统要求

- Windows 10/11 64位
- 已安装 MWorks Sysplorer 2024b/2026a
