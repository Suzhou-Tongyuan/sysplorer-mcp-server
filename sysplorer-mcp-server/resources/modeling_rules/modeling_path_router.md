# 建模路径分流规则（Modelica 物理模型 vs Sysblock 框图）

> 当用户意图为**搭建、编辑模型**时，先按本节判别走哪条路径，再执行对应规范。**不要**在未判别前混用两套流程。

### 路径约定（MCP 打包 exe 时必读）

- **查阅文档**：`resources/` 语料默认在 **MCP 部署目录（exe 同目录）** 下，由 `get_resources_root` / `MCP_RESOURCES_DIR` 决定，**不是**建模输出目录。
- **建模产物**：`.mo`、`src/`、`private_lib/` 等必须落在 **工作区根**（`MCP_WORKSPACE_DIR` 或 `--workspace-dir`，未设置时 frozen 下为启动 MCP 时的 **当前工作目录**）。**勿**写到 exe 目录。
- 不确定时查看 `mworks_sysplorer_session_manager(action="health")` 返回 JSON 中 `paths.workspace_root` 与 `paths.resources_root`。

---

## 1. 判别流程

### 1.1 Modelica 物理模型（连续/多物理域方程与连接器）

优先归为此类，当用户明确涉及：

- `.mo` 文本模型、`package` / `model` / `equation` / `connect()`、物理连接器（电气、热、流体、多体等）
- 私有库 / MSL 组件、参数与单位、DAE 与仿真工况在 Modelica 层配置

### 1.2 Sysblock 框图模型（SysplorerEmbeddedCoder 块图）

归为此类，当用户明确涉及：

- **Sysblock**、**框图**、**方框图**、**信号流**、**Embedded Coder**、**SysplorerEmbeddedCoder**
- 用 **Python / ModelingPy（或 Sysblock API）** 在工具里**程序化建图、改块、设参数**，而非手写 `.mo` 拓扑

### 1.3 不确定时

**必须**向用户确认一句：目标是否为 **Sysblock 框图（基于 SysplorerEmbeddedCoder）**，还是 **传统 Modelica 物理模型（.mo）**。

---

## 2. Modelica 物理模型分支

1. **必读**：`resources/modeling_rules/modelica_style_guide.md`（与开发侧 `.claude/modelica_style_guide.md` 同步的完整规范）。
2. **执行**：仓库 `CLAUDE.md` / `AGENTS.md` 中的 **7 Gates**、编译驱动开发、testbench、KPI；多组件 / 多 **`connect()`** 模型在逻辑完成后须执行 **Smart Layout**（`mworks_sysplorer_smart_layout`，`mode=writeback_mo`，`graph_json`，见 Gate 6），随后 **`mworks_sysplorer_model_manager`**（`action=export_model_diagram`，别名 `export_diagram`；底层 `ExportDiagram`）导出原理图并做 **视觉验收与迭代修复**（见 Gate 6 后续）。
3. **检索补充**：组件选型先查工作区 **`private_lib/MetaDataLib.json`** 定候选 **`fqname`**；对已安装 **库模型类** 的说明、参数与端口，调用 **`mworks_sysplorer_get_lib_model_document(full_class_name)`**（经 Sysplorer `ClassExist` / `LoadLibrary` / `ExportDocumentation`）；辅以商业库语料 RAG 等。**不要**再从 `resources/` 翻 Markdown 代替 Sysplorer 导出的类文档。

---

## 3. Sysblock 框图模型分支

**库约束**：在必须使用 Sysplorer 块图库的前提下，**默认模型库为 `SysplorerEmbeddedCoder`**（任务书另行指定其他库时除外）。

**系统库名字符串**：Sysblock 框图依赖的**系统库**顶层包名**固定为 `SysplorerEmbeddedCoder`**。所有需要传「库名」的操作（脚本内 `LoadLibrary`、**`mworks_sysplorer_load_library`** 等）**必须**使用 **`SysplorerEmbeddedCoder`**，**不要**误用 **`Sysblock`**（后者仅用于 `NewModel` 的 **`restriction="Sysblock"`**，表示块图模型类型，**不是**库名）。详见 `sysblock_style_guide.md` 文首「系统库名称（硬性约定）」。

1. **必读**：`resources/modeling_rules/sysblock_style_guide.md`（**Run Script 前 Sysplorer 必须已启动且驱动已连接**；**编写脚本前先完成组件/布局/连线/参数设计**；`NewModel(restriction="Sysblock")`、新建/编辑脚本分离、package 级 `parent`、以 **`mworks_sysplorer_check_model` 成功**为建图循环结束条件、仿真与 Modelica 共用 MCP 工具链）。
2. **执行**：下文 3.1–3.4 与本文档表格中的语料路径；Run Script 细节以 `sysblock_style_guide.md` 为准。

### 3.1 查阅资料（RAG）

| 目的 | 操作 |
|------|------|
| **具体模块怎么用**（功能说明、端口、参数语义、示例、子库索引） | 对 **`resources/SysblockModelLibrary/`** 语料检索：`mworks_sysplorer_resources_retrieval(action="corpora", corpus_id="sysblock_model_library")` 取解析路径，再 `action="search", query=..., sources=<上述路径>, index_path="resources/indexes/sysblock_model_library_index.json", rebuild_index=按需)`；可按块名或子库关键词（如 `Continuous`、`PIDController`）检索，各子目录下的 `*_Main.md` 为该类模块总览 |
| **库模型类文档**（Modelica 全名类的说明、参数、端口等，含 `SysplorerEmbeddedCoder.*` 等已加载库） | 调用 **`mworks_sysplorer_get_lib_model_document(full_class_name)`**（Sysplorer `ClassExist` → 必要时 `LoadLibrary` → `ExportDocumentation`）；**不要**用 `resources/SysplorerAPI/` 下的 Markdown 代替从 Sysplorer 导出的类文档 |
| API 用法、函数名、调用顺序（`mworks_sysplorer_call_code` 的 `run_script` 模式 / ModelingPy） | 调用 **`mworks_sysplorer_get_api_document(api_function_name)`**（官方 `Help(cmd)`）；**不要**再用 `resources/SysplorerAPI/` 语料检索代替本工具 |
| 各块**参数合法名称**（API 键名） | 若随包存在，直接打开 **`resources/SysplorerAPI/SysblockParameters.md`**（**非 RAG**，未列入 `resources_manifest.json`）；**与上表配合**：块级语义与端口以 `sysblock_model_library` 与/或 `mworks_sysplorer_get_lib_model_document` 为准；脚本 API 细节可 **`mworks_sysplorer_get_api_document`** 核对 |

说明：`sysblock_model_library` **未**列入 `resources_manifest.json` 的 `default_sources`，默认合并检索不会扫模块库全文；查块用法时**必须**显式传入该语料的 `sources`（及建议的专用 `index_path`），避免与默认索引混淆。

### 3.2 编写建模脚本

- **先读** `sysblock_style_guide.md`：**Part 0**（调用 `run_script` 模式前 **`mworks_sysplorer_session_manager(action="health")` / `ensure` 等确保就绪**）、**Part 1**（**先设计** `SysplorerEmbeddedCoder` 组件清单、布局、连线表、参数表，**再写脚本**）、**新建脚本 / 编辑脚本分离**、**`NewModel(..., restriction="Sysblock")`**、**`parent` 传父包全名**、循环结束以 **`mworks_sysplorer_check_model` 成功**为准。
- 使用文档中的 **Sysplorer Python API**（如 ModelingPy / Sysblock 相关接口）生成或修改框图。
- 块类型、参数名须与 **`SysplorerEmbeddedCoder.*`** 及 `SysblockParameters.md` 一致，避免臆造。

### 3.3 运行与调试循环（RunScript）

0. **大前提**：调用 **`mworks_sysplorer_call_code`**（`mode="run_script"`）**之前**，须已通过 **`mworks_sysplorer_session_manager(action="health")`**（或等价步骤）确认 **Sysplorer 已启动且 `driver_ready`**；失败时依次 **`action="ensure"`**、**`action="restart"`**（必要时 **`restart_mode="full_reset"`**）等，详见 `sysblock_style_guide.md` Part 0 与 `CLAUDE.md`。
1. 调用 MCP 工具 **`mworks_sysplorer_call_code`**，`mode="run_script"`，`payload` 含 `python_source` 或 `script_path`（与当前 Sysplorer 会话同进程；路径白名单同旧约定）。
2. 根据返回 JSON 中的 **`stdout` / `stderr` / `exception` / `traceback`** 以及可选的全局返回值 **`RUN_SCRIPT_RESULT`** 修改脚本。
3. **重复**「`run_script` 调用 → 修脚本」直到 **`ok` 为 true** 且无未处理异常（必要时先 `mworks_sysplorer_session_manager` 做 health/ensure/restart）。
4. **建图阶段结束**：在脚本侧稳定后，还须 **`mworks_sysplorer_check_model`（或 `mworks_sysplorer_call_code` 的 `fast_workflow` 模式中的检查）通过**，才算完成 Sysblock 建图—编辑循环；详见 `sysblock_style_guide.md` Part 5。

说明：部署若设置环境变量 **`MWORKS_RUN_SCRIPT_DISABLED=1`**，`run_script` 模式会拒绝执行。

### 3.4 后续仿真（与 Modelica 统一）

脚本侧建图/编译通过后，**仿真、扫参、读结果、KPI** 等环节回到与 Modelica 项目相同的 MCP 工具链（例如 `mworks_sysplorer_check_model`、`mworks_sysplorer_simulate_model`、`mworks_sysplorer_call_code`（`mode="fast_workflow"`）、`mworks_sysplorer_result_manager` 等，按任务选用），**不再单独搞一套仿真规范**。

---

## 4. 语料与清单对应

| 路径 | 说明 |
|------|------|
| `modeling_rules/modeling_path_router.md` | 本文（分流 + Sysblock 流程） |
| `modeling_rules/modelica_style_guide.md` | Modelica 分支完整规范 |
| `modeling_rules/sysblock_style_guide.md` | Sysblock 分支 Run Script / ModelingPy 脚本规范 |
| `SysplorerAPI/`（磁盘可选） | **未**编入 RAG 索引；示例 Markdown 仅人工查阅；**API 说明**以 **`mworks_sysplorer_get_api_document`** 为准 |
| `SysplorerAPI/SysblockParameters.md`（磁盘可选） | Sysblock 参数名速查（非 RAG） |
| `resources/private_lib/`（磁盘可选） | **未**编入 RAG；工程内私有库与元数据在工作区 **`private_lib/`**，读 **`MetaDataLib.json`** 并用 **`mworks_sysplorer_get_lib_model_document(fqname)`** 核对类文档 |
| `SysblockModelLibrary/` | Sysblock 各子库**模块说明文档**（用法、端口、参数释义、示例）；RAG 语料 id：`sysblock_model_library`，索引文件：`indexes/sysblock_model_library_index.json` |

在 `resources_manifest.json` 中，当前 RAG 类别为 **`modeling_rules`**、**`sysblock_model_library`**、**`design_opt_mpe_api`**、**`cad_toolbox_api`**、**`simulink_importer_api`**、**`commercial_library`**；`default_sources` **不含** `sysblock_model_library`，查块用法时须按 §3.1 显式指定 `sources` 与索引。**`SysplorerAPI/`** 与 **`resources/private_lib/`** 已从清单与索引中移除；**类级文档**用 **`mworks_sysplorer_get_lib_model_document`**，**API 帮助**用 **`mworks_sysplorer_get_api_document`**，**私有库候选与 fqname** 来自工作区 **`private_lib/MetaDataLib.json`**（无 MCP 元数据检索工具）。
