# 构建发布包（Sysplorer Tools）

面向 **Sysplorer Tools** 的目录式发布包，由 `install/build_publish.ps1` 生成，输出到仓库根目录下的 `publish/sysplorer_mcp/`（布局与 Tools 侧 `sysplorer_mcp` 一致）。

## 调用 `build_publish.ps1` 的流程

1. **环境**
   - **PowerShell**（Windows；脚本使用 `robocopy` 复制 `sysplorer-mcp-server`，为系统自带能力）。
   - **Python**：仅用于执行 `install/write_build_meta.py` 写入版本与 `MCP_BUILD_INFO.json`。需本机 PATH 上存在 **`py -3`** 或 **`python`**。

2. **在仓库中执行**（默认以 `install` 的父目录为仓库根）：

```powershell
cd install
.\build_publish.ps1
```

3. **脚本会做的事（概要）**
   - 清空并准备输出目录：`publish/sysplorer_mcp/`。
   - 写入启动器：`publish_assets/sysplorer_mcp_main.py` → `publish/sysplorer_mcp/main.py`。
   - 用 `robocopy` 复制 `sysplorer-mcp-server/` 到包内（排除 `__pycache__`、`tests`、`.pytest_cache`、`*.pyc` 等；不包含根目录的 `modelica_doc_index.json`）。
   - 整树复制 `resources/`；包内会**省略**大型 RAG 索引 `modelica_doc_index.json`，并校验除该文件外的文件数量与源一致。
   - 复制根目录 `install_sysplorer_mcp_tools.ps1` → 包内 `install_mcp.ps1`（并规范为 UTF-8 BOM），以及 `install_mcp.sh`。
   - 调用 `write_build_meta.py` 生成包内 `sysplorer-mcp-server/_build_meta.py`，并在包根写入 `MCP_BUILD_INFO.json`。
   - 将 `install/windows/README.md` 复制为包内 `README.md`；并清理若干历史遗留文件名（旧版 README / 安装手册等）。

4. **参数**
   - **`-RepoRoot <路径>`**：可选。不指定时，仓库根为 `install` 的上一级目录。
   - **`-Internal`**：内部版版本号（`version_base.x`，`x` 为 `git rev-list --count HEAD`）。**不加**时为发布版，版本号仅为 `install/package_version.json` 中的 `version_base`。

5. **产出位置**

   - 目录：`../publish/sysplorer_mcp/`（相对 `install` 即仓库根下 `publish/sysplorer_mcp`）。
   - 主要内容：`main.py`、`sysplorer-mcp-server/`、`resources/`、`install_mcp.ps1`、`install_mcp.sh`、`MCP_BUILD_INFO.json`、`README.md`。

`resources/` 下任意子目录新增或更新的 Markdown（例如说明文档）会随整树一并进入发布包，无需改复制清单。

## 版本号

- 手工配置：`install/package_version.json` 中的 `version_base`（默认 `0.1`），**只能**是两位数字段如 `0.1`，**不要**写成 `0.1.x`（内部版时 `x` 由脚本用 Git 提交总数追加）。
- **`build_publish.ps1`（默认）**：发布版，版本仅为 `version_base`。
- **`build_publish.ps1 -Internal`**：内部版，`0.1.x`（`x` = `git rev-list --count HEAD`）。

## 另：打包 exe（`build.ps1`）

若需要 **PyInstaller 单文件 exe** 与 `dist/` 归档，仍在 `install` 目录使用 `build.ps1`（需 Python 3.12、按需设置 `MWORKS_INSTALL_DIR` 等）。详见脚本头部注释；内部版 / 发布版与 `build.ps1 -Release` 的约定与上文版本说明一致。
