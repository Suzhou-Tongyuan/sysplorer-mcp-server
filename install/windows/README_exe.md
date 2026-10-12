# Sysplorer MCP Server（modelica-lite exe 包）

本目录是给 **modelica-lite / mols** 集成用的 PyInstaller 发布包，不是 Sysplorer Tools 目录式包。

## 交付物

| 文件 | 用途 |
|------|------|
| `sysplorer_mcp_server.exe` | MCP 服务端（交给 modelica-lite 侧随产品启动） |
| `resources/` | 语料与 modeling skills（含 `resources_mogick` 覆盖层） |
| `install-helper.exe` | 模型库安装提权辅助（依赖下载/落盘时使用） |
| `install_mcp.ps1` | 可选：把 exe 写入本机 Claude / OpenCode / Codex / Modelex 配置 |
| `MCP_BUILD_INFO.json` | 版本与 `pack_variant=modelica_lite` |

宿主启动 exe 时请注入：

- `--sysplorer-platform-label modelica_lite`（或 `mols`）
- `SYSPLORER_API_PORT`（连接已运行的 mols/Sysplorer，仅 `ConnectSysplorer`）
- 需要真实下载模型库时：`--user-workspace <可写目录>`

打包机仍需能 `import mworks.sysplorer`（PyInstaller 收集 API）；运行机不要求 `External\python64\python.exe`。

## 与完整 Sysplorer 包不同的 skills

- **有**：`ty-sysplorer-dependency-guard`；lite 版 `ty-sysplorer-modeling-rules`（依赖守卫、进程内 `run_sysplorer_api`）
- **无**：`ty-cadtool-modeling`、`sysplorer-mds-docs`，以及 `cad_toolbox_api` 语料

安装脚本同步 skills 时，会从本机全局 skills 目录清掉上述已排除的旧目录，避免完整版残留。

## 可选本机 MCP 配置

```powershell
.\install_mcp.ps1
```

默认平台标签为 `modelica_lite`。`--mworks-install-dir` 可留空。skills 同步优先用 PATH 上的 Python；没有 Python 时用脚本内置复制。
