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
│   ├── run_script_worker.py # run_sysplorer_api 子进程入口（stdin=DEVNULL + 超时）
│   └── utils.py            # 通用工具函数
├── tools/                  # MCP 工具定义（每个文件注册一组 @mcp.tool）
│   ├── sysplorer.py        # 健康检查、driver 重启、进程管理
│   ├── model_ops.py        # 模型加载、编译检查、翻译、仿真
│   ├── results.py          # 仿真结果读取、变量查询、绘图
│   ├── workflow.py         # call_code（仅 run_sysplorer_api，兼容 run_script）
│   ├── layout.py           # Smart Layout 布局工具
│   ├── docs.py             # RAG 文档检索工具
│   ├── lib_docs.py         # `get_lib_model_document` + `get_api_document`
│   ├── run_script.py       # `_mworks_run_script_impl`：子进程执行（由 call_code 引用）
│   └── rag/                # RAG 子系统（BM25 索引、混合检索）
└── temp/                   # 运行时临时文件（不提交）
```

## 前置条件

1. **Sysplorer 2026a 已安装**（Windows 默认路径 `C:\Program Files\MWORKS\Sysplorer 2026a`；Linux 优先探测 `/opt/MWORKS/Sysplorer-2026a`，其次 `/usr/local/MWORKS/Sysplorer-2026a`）
2. **Python 3.10 ~ 3.12**
3. 安装依赖：
   ```bash
   pip install -r sysplorer-mcp-server/requirements.txt
   ```

## 禁止在模块顶层 `import ctypes`

Linux 上 Sysplorer 自带 Python 加载 `ctypes` 会拉起扩展 `_ctypes`，进而依赖系统 `libffi`。版本对不上时，**打包后的 `main.py` 一启动就退出**（Cursor 只显示 `process exited with code 1`，细节在 `sysplorer-mcp-server/logs/server.log`）。

`main.py` 会 import `tools.model_ops` 等工具模块，这些模块再 import `core.model_dependencies` 等。**任何出现在这条启动链上的文件，都不要在模块顶层写 `import ctypes` / `from ctypes ...`。**

Windows 专用能力（短路径、`SetStdHandle`、提权安装助手等）必须：

1. 先判断操作系统（`platform.system() == "Windows"` 或已有的 `PLATFORM`）；
2. **只在该分支的函数内部**再 `import ctypes`。

回归约束见 `tests/test_no_module_level_ctypes.py`（扫描启动链源文件的顶层 import）。

## 路径配置

所有本地路径集中定义在 `path_config.py`，均可通过同名环境变量覆盖。

**工作区 vs 部署目录（打包 exe）**：`DEPLOY_ROOT` 为 exe 所在目录（旁置 `resources/` 供查阅）；`WORKSPACE_ROOT` / `PROJECT_ROOT` 为 Agent 工程根（`src`、`private_lib`、保存的模型）。打包后请设置 **`MCP_WORKSPACE_DIR`**（或启动参数 **`--workspace-dir`**）指向用户工程，勿与 exe 目录混用。详见 `session_manager(action="health")` 返回 JSON 中的 `paths` 字段。

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `MCP_WORKSPACE_DIR` | Agent 工程根（建模输出、private_lib） | 未设置且 frozen 时为进程 **cwd**；开发态为仓库根 |
| `MCP_RESOURCES_DIR` | 语料 `resources` 根（查阅） | frozen 时为 `{exe 目录}/resources` |
| `MWORKS_INSTALL_DIR` | Sysplorer 安装根目录 | Windows: `C:\Program Files\MWORKS\Sysplorer 2026a`；Linux: `/opt/MWORKS/Sysplorer-2026a` |
| `MWORKS_BIN64` | Bin64 目录 | Windows: `{INSTALL_DIR}\Bin64`；Linux 自动探测 `{INSTALL_DIR}/bin64` 或 `{INSTALL_DIR}/Bin64` |
| `MWORKS_SYSPLORER_SITE_PACKAGES` | Sysplorer Python 包路径 | Windows: `{INSTALL_DIR}\External\python64\Lib\site-packages`；Linux 自动探测 `External/external/python64/lib/python3.x/site-packages` |
| `MWORKS_LIBRARY_ROOT` | 库文件目录 | `{INSTALL_DIR}\Library` |
| `MWORKS_SIMULATOR_BIN` | Simulator Bin 目录 | Windows: `{INSTALL_DIR}\Simulator\Bin64`；Linux 自动探测 `Simulator/simulator` 下的 `bin64` |
| `MWORKS_WORKDIR` | 工作目录 | `sysplorer-mcp-server/temp` |
| `MWORKS_SIM_DIR` | MCP 侧仿真输出默认路径（配置默认，**不是** Sysplorer 实时目录） | `~/Documents/MWORKS/Simulation`；实时路径用 `session_manager(action="get_sim_result_directory")` |
| `MWORKS_MW_MOL_DIR` | mw_mol 帮助文档目录 | `~/Documents/MWORKS/mw_mol` |
| `SYSPLORER_PLATFORM_LABEL` | 平台标识；为 `modelica_lite` / `mols`（亦接受 `modelica-lite`）时必须注入 `SYSPLORER_API_PORT`，仅 `ConnectSysplorer`，不解析 `MWORKS_BIN64`、不 `StartSysplorer`；此时 `translate_model` / `simulate_model` 会先 `SetCompileSolver64(1)`，默认 64 位翻译与仿真。**非 lite**：`load_library` 只做本机 `LoadLibrary`，依赖解析/下载不注册、不写进工具说明。**lite**：先本地 `load`，失败再 `plan`（见 mogick `ty-sysplorer-dependency-guard`）；`run_sysplorer_api` 固定进程内 | `Sysplorer 2026a` |
| `SYSPLORER_API_PORT` | 正整数时连接已运行的 Sysplorer/mols 实例（优先于启动新实例）；`modelica_lite` 下为必填 | 未设置 |
| `SYSPLORER_API_MOLS` | 未设置 `SYSPLORER_API_PORT` 时选择启动模式；`true/1/yes/on` 使用 `StartSysplorer("-q", processPath=...)`，否则使用 `StartSysplorer("-gui", processPath=...)`（不适用于 `modelica_lite`） | `False` |
| `MWORKS_RUN_SCRIPT_DISABLED` | `1/true/yes/on` 时拒绝 `call_code(mode="run_sysplorer_api")` | 未设置 |
| `MWORKS_RUN_SCRIPT_TIMEOUT` | run_sysplorer_api 子进程墙钟超时（秒）；也可在 payload 传 `timeout_sec` | `7200` |
| `MWORKS_RUN_SCRIPT_IN_SUBPROCESS` | 仅非 lite 平台生效：`0/inproc` 强制进程内；`1/always` 强制子进程。**modelica_lite / mols 固定走原进程内路径，不查独立 python** | `auto` |

## 启动方式

通过 `.mcp.json` 自动加载（推荐），Claude Code 启动时自动连接：

```json
{
  "mcpServers": {
    "sysplorer": {
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
pytest sysplorer-mcp-server/tests/
```

## 核心 MCP 工具一览

与 `main.py` 当前导入一致；2026b **不注册** `library_prepare`。参数与 `action` / `mode` 细分见各工具 docstring。

| 工具 | 说明 |
|------|------|
| `resources_retrieval` | 语料（`action=corpora` / `search` / `list` / `explain`） |
| `get_lib_model_document` | 已解析库类文档（`ExportDocumentation`） |
| `get_api_document` | Python API `Help(cmd)` |
| `session_manager` | 会话（`health` / `ensure` / `restart` / `get_directory` / `get_sim_result_directory` / `get_installed_libraries` / `get_loaded_models` / …） |
| `call_code` | 最后手段：仅 `run_sysplorer_api`（旧名 `run_script` 仍兼容）。异步检查、就绪分派、一键流水线已从 tools/list 拿掉 |
| `load_library` | **列出已安装库**（`action=installed`）+ **加载本机库**（`action=load` / `LoadLibrary`）。schema 只有这 4 个参数 |
| `library_prepare` | **仅 modelica_lite / mols 注册**：`plan` / `resolve` / `latest` / `download` / `prepare`。2026b 不出现在 tools/list |
| `model_manager` | 生命周期：`new` / `open` / `load_file` / `unload` / `save` / `save_as`。查询走 `model_inspect`，对比走 `compare_model` |
| `model_inspect` | 子类、组件、端口、类文本、说明与最近错误查询 |
| `compare_model` | 图形界面对比两个已加载模型或两个 .mo 文件 |
| `check_model` | 编译/实例化检查 |
| `translate_model` | `TranslateModel` |
| `simulate_model` | `SimulateModel` + 结果校验 |
| `result_manager` | 结果文件与变量（`open_result` / `get_var_values` / …） |
| `plot_manager` | 结果绘图 / 动画（`action`：`plot_variables` \| `create_animation`） |
| `smart_layout` | Smart Layout（`layout_only` / `finalize_generation` / `writeback_mo`） |
