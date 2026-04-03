# MWorks MCP Server

基于 Sysplorer 官方 Python API（`mworks.sysplorer`）的 MCP 服务，为 Claude Code 提供模型编译、仿真、类文档导出、Smart Layout 布局等全链路建模能力。

## 模块结构

```
sysplorer-mcp-server/
├── main.py                 # MCP Server 入口（薄壳，仅 import 触发工具注册）
├── mcp_instance.py         # FastMCP 单例
├── path_config.py          # 路径配置中心（所有本地路径的唯一定义点）
├── constants.py            # 不可变常量（正则、端口映射、域关键词等）
├── state.py                # 可变全局状态 + driver 获取
├── mworks_driver.py        # Sysplorer Python API 封装
├── core/                   # 核心逻辑模块
│   ├── smart_layout.py     # 域感知 Smart Layout 布局引擎
│   ├── stack_health.py     # Sysplorer 全栈健康管理与恢复
│   ├── process_mgmt.py     # 进程管理（mworks.exe / mols.exe / mwrsvc.exe）
│   ├── metadata_index.py   # RAG 模块懒加载（`_get_rag_module`）
│   ├── job_manager.py      # 异步任务（check/translate/simulate，workflow 使用）
│   ├── lib_catalog.py      # 库目录扫描与分类
│   ├── model_parser.py     # Modelica 源码解析
│   ├── mol_extractor.py    # .mol 帮助文档参数提取
│   └── utils.py            # 通用工具函数
├── tools/                  # MCP 工具定义（每个文件注册一组 @mcp.tool）
│   ├── sysplorer.py        # 健康检查、driver 重启、进程管理
│   ├── model_ops.py        # 模型加载、编译检查、翻译、仿真
│   ├── results.py          # 仿真结果读取、变量查询、绘图
│   ├── workflow.py         # mworks_sysplorer_call_code（统一脚本/工作流/异步）
│   ├── layout.py           # Smart Layout 布局工具
│   ├── docs.py             # RAG 文档检索工具
│   ├── lib_docs.py         # `mworks_sysplorer_get_lib_model_document` + `mworks_sysplorer_get_api_document`
│   ├── run_script.py       # `_mworks_run_script_impl`（由 call_code 引用，无独立 MCP 工具）
│   └── rag/                # RAG 子系统（BM25 索引、混合检索）
└── temp/                   # 运行时临时文件（不提交）
```

## 前置条件

1. **Sysplorer 2026a 已安装**（默认路径 `C:\Program Files\MWORKS\Sysplorer 2026a`）
2. **Python 3.10 ~ 3.12**
3. 安装依赖：
   ```bash
   pip install -r sysplorer-mcp-server/requirements.txt
   ```

## 路径配置

所有本地路径集中定义在 `path_config.py`，均可通过同名环境变量覆盖。

**工作区 vs 部署目录（打包 exe）**：`DEPLOY_ROOT` 为 exe 所在目录（旁置 `resources/` 供查阅）；`WORKSPACE_ROOT` / `PROJECT_ROOT` 为 Agent 工程根（`src`、`private_lib`、保存的模型）。打包后请设置 **`MCP_WORKSPACE_DIR`**（或启动参数 **`--workspace-dir`**）指向用户工程，勿与 exe 目录混用。详见 `mworks_sysplorer_session_manager(action="health")` 返回 JSON 中的 `paths` 字段。

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `MCP_WORKSPACE_DIR` | Agent 工程根（建模输出、private_lib） | 未设置且 frozen 时为进程 **cwd**；开发态为仓库根 |
| `MCP_RESOURCES_DIR` | 语料 `resources` 根（查阅） | frozen 时为 `{exe 目录}/resources` |
| `MWORKS_INSTALL_DIR` | Sysplorer 安装根目录 | `C:\Program Files\MWORKS\Sysplorer 2026a` |
| `MWORKS_BIN64` | Bin64 目录 | `{INSTALL_DIR}\Bin64` |
| `MWORKS_SYSPLORER_SITE_PACKAGES` | Sysplorer Python 包路径 | `{INSTALL_DIR}\External\python64\Lib\site-packages` |
| `MWORKS_LIBRARY_ROOT` | 库文件目录 | `{INSTALL_DIR}\Library` |
| `MWORKS_SIMULATOR_BIN` | Simulator Bin 目录 | `{INSTALL_DIR}\Simulator\Bin` |
| `MWORKS_WORKDIR` | 工作目录 | `sysplorer-mcp-server/temp` |
| `MWORKS_SIM_DIR` | 仿真输出目录 | `~/Documents/MWORKS/Simulation` |
| `MWORKS_MW_MOL_DIR` | mw_mol 帮助文档目录 | `~/Documents/MWORKS/mw_mol` |
| `SYSPLORER_PLATFORM_LABEL` | 元数据中的平台标识 | `Sysplorer 2026a` |

## 启动方式

通过 `.mcp.json` 自动加载（推荐），Claude Code 启动时自动连接：

```json
{
  "mcpServers": {
    "sysplorer_mcp": {
      "command": "python",
      "args": ["sysplorer-mcp-server/main.py", "--workspace-dir", "D:/path/to/your/project"]
    }
  }
}
```

打包 exe 时建议在宿主配置里设置 `MCP_WORKSPACE_DIR` 或 `--workspace-dir`，使建模目录与 exe 旁 `resources` 分离。

手动启动：
```bash
python sysplorer-mcp-server/main.py
```

## 测试

```bash
pytest tests/
```

## 核心 MCP 工具一览

与 `main.py` 当前导入一致，**共 13 个**；参数与 `action` / `mode` 细分见 **[MCP_TOOLS.md](./MCP_TOOLS.md)**。

| 工具 | 说明 |
|------|------|
| `mworks_sysplorer_resources_retrieval` | 语料（`action=corpora` / `search` / `list` / `explain`） |
| `mworks_sysplorer_get_lib_model_document` | 已解析库类文档（`ExportDocumentation`） |
| `mworks_sysplorer_get_api_document` | Python API `Help(cmd)` |
| `mworks_sysplorer_session_manager` | 会话（`health` / `ensure` / `restart` / …） |
| `mworks_sysplorer_call_code` | **统一**：`run_script` / `submit_job` / `get_job_result` / `run_with_ready`（分派，含 `set_model_param`）/ `fast_workflow`（见 MCP_TOOLS.md） |
| `mworks_sysplorer_load_library` | 加载库（`.mol` 等） |
| `mworks_sysplorer_model_manager` | **统一模型**：生命周期 + 原理图导出（`export_model_diagram` / `export_diagram`）+ 内省（`lookup_component` / `get_components` / `get_component_ports` / `get_model_text` / `get_model_description` / `get_component_description` / `get_classes`），均用 `action=` |
| `mworks_sysplorer_check_model` | 编译/实例化检查 |
| `mworks_sysplorer_translate_model` | `TranslateModel` |
| `mworks_sysplorer_simulate_model` | `SimulateModel` + 结果校验 |
| `mworks_sysplorer_result_manager` | 结果文件与变量（`open_result` / `get_var_values` / …） |
| `mworks_sysplorer_plot_manager` | 结果绘图 / 动画（`action`：`plot_variables` \| `create_animation`） |
| `mworks_sysplorer_smart_layout` | Smart Layout（`layout_only` / `finalize_generation` / `writeback_mo`） |
