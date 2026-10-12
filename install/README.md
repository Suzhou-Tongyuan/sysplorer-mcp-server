# 构建发布包（Sysplorer Tools）

面向 **Sysplorer Tools** 的目录式发布包。Windows 入口为 `install/build_publish.ps1`，Linux 入口为 `install/linux/scripts/build_publish.sh`，都会输出到仓库根目录下的 `publish/sysplorer_mcp/`（布局与 Tools 侧 `sysplorer_mcp` 一致），并在 `publish/` 下生成 `sysplorer_mcp_v{version}.zip`。

## 调用 `build_publish.ps1` 的流程

1. **环境**
   - **PowerShell**（Windows；脚本使用 `robocopy` 复制 `sysplorer-mcp-server`，为系统自带能力）。
   - **Python**：用于执行 `install/write_build_meta.py` 写入版本与 `MCP_BUILD_INFO.json`。Windows 需本机 PATH 上存在 **`py -3`** 或 **`python`**；Linux 需 **`python3`** 或 **`python`**（打 zip 也走 Python 标准库 `zipfile`，不依赖系统 `zip` 命令）。

2. **在仓库中执行**（默认以 `install` 的父目录为仓库根）：

```powershell
cd install
.\build_publish.ps1
```

Linux：

```bash
bash install/linux/scripts/build_publish.sh
# 内部版：bash install/linux/scripts/build_publish.sh --internal
```

3. **脚本会做的事（概要）**
   - 清空并准备输出目录：`publish/sysplorer_mcp/`。
   - 写入启动器：`publish_assets/sysplorer_mcp_main.py` → `publish/sysplorer_mcp/main.py`。
   - 用 `robocopy` 复制 `sysplorer-mcp-server/` 到包内（排除 `__pycache__`、`tests`、`.pytest_cache`、`*.pyc` 等；不包含根目录的 `modelica_doc_index.json`）。
   - 整树复制 `resources/`；包内会**省略**大型 RAG 索引 `modelica_doc_index.json`，并校验除该文件外的文件数量与源一致。
   - 复制根目录 `install_sysplorer_mcp_tools.ps1` → 包内 `install_mcp.ps1`（并规范为 UTF-8 BOM），以及 `install_mcp.sh`。
   - 调用 `write_build_meta.py` 生成包内 `sysplorer-mcp-server/_build_meta.py`，并在包根写入 `MCP_BUILD_INFO.json`。
   - Windows 包将 `install/windows/README.md` 复制为包内 `README.md`；Linux 包将 `install/linux/README.md` 复制为包内 `README.md`。两者都会清理若干历史遗留文件名（旧版 README / 安装手册等）。
   - 将 `publish/sysplorer_mcp/` **整目录**打成 zip（解压后仍是 `sysplorer_mcp/`）：生成 `publish/sysplorer_mcp_v{version}.zip`。Windows 与 Linux 脚本都会做这一步。打包前删除 `publish/` 下既有 `sysplorer_mcp_v*.zip`；先写入临时目录再移入 `publish/`，避免把压缩包打进自身。

4. **参数**
   - **`-RepoRoot <路径>`**（Windows）/ 位置参数（Linux）：可选。不指定时，仓库根为 `install` 的上一级目录。
   - **`-Internal`** / **`--internal`**：内部版版本号（`version_base.x`，`x` 为 `git rev-list --count HEAD`）。**不加**时为发布版，版本号仅为 `install/package_version.json` 中的 `version_base`。

5. **产出位置**

   - 目录：`../publish/sysplorer_mcp/`（相对 `install` 即仓库根下 `publish/sysplorer_mcp`）。
   - 压缩包：`../publish/sysplorer_mcp_v{version}.zip`（`{version}` 与包内版本号一致，发布版如 `0.5`，内部版如 `0.5.x`）。
   - 目录主要内容：`main.py`、`sysplorer-mcp-server/`、`resources/`、`install_mcp.ps1`、`install_mcp.sh`、`MCP_BUILD_INFO.json`、`README.md`。

`resources/` 下任意子目录新增或更新的 Markdown（例如说明文档）会随整树一并进入发布包，无需改复制清单。

## 版本号

- 手工配置：`install/package_version.json` 中的 `version_base`（默认 `0.5`），**只能**是两位数字段如 `0.5`，**不要**写成 `0.5.x`（内部版时 `x` 由脚本用 Git 提交总数追加）。
- **`build_publish.ps1`（默认）** / **`build_publish.sh`**：发布版，版本仅为 `version_base`。
- **`build_publish.ps1 -Internal`** / **`build_publish.sh --internal`**：内部版，`0.5.x`（`x` = `git rev-list --count HEAD`）。

## 另：打包 exe（`build.ps1`）

若需要 **PyInstaller 单文件 exe** 与 `dist/` 归档，仍在 `install` 目录使用 `build.ps1`（需 Python 3.12、按需设置 `MWORKS_INSTALL_DIR` 等）。详见脚本头部注释；内部版 / 发布版与 `build.ps1 -Release` 的约定与上文版本说明一致。

## modelica-lite exe 包（`build_publish_exe.ps1`）

给 **modelica-lite / mols** 侧交付的是 `publish/sysplorer_mcp_exe/`（`sysplorer_mcp_server.exe` + `resources/` + 安装脚本），不是 `publish/sysplorer_mcp/` 目录式 Tools 包。

```powershell
cd install
.\build_publish_exe.ps1
# 或：.\build_publish_exe.ps1 -PythonExe D:\Python311\python.exe -Internal
```

- **打包机**仍需能 `import mworks.sysplorer`（PyInstaller 收集 API）。运行侧由宿主拉起 exe，并注入 `SYSPLORER_API_PORT` 与 `--sysplorer-platform-label modelica_lite`。
- **resources**：先复制仓库 `resources/`（省略 `modelica_doc_index.json`、`generated/`），再叠加 `resources_mogick/`。排除 `ty-cadtool-modeling`、`sysplorer-mds-docs`、`cad_toolbox_api`；带上 `ty-sysplorer-dependency-guard` 与 lite 版 modeling-rules。
- 包内 README 为 `install/windows/README_exe.md`；`MCP_BUILD_INFO.json` 含 `pack_variant=modelica_lite`。
