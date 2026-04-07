# Sysblock 框图建模规范（Run Script / ModelingPy）

> **适用范围**：经 `resources/modeling_rules/modeling_path_router.md` 判别为 **Sysblock 框图**路径时，通过 **`call_code`**（`mode="run_script"`）执行的 **ModelingPy（Sysplorer Python API）** 建模脚本，须遵守本文。
>
> **与 Modelica 分支对照**：手写 `.mo`、package 文本与 7 Gates 见 `modelica_style_guide.md` 与 `CLAUDE.md`；本文**不**重复物理方程与 `connect()` 规范，只约束 **程序化建 Sysblock** 的脚本结构与 Run Script 循环。

---

## 系统库名称（硬性约定）

- **Sysblock 框图所依赖的系统库**，在 Sysplorer / ModelingPy / MCP 中作为**顶层包（库）**使用的**唯一正确名字**是 **`SysplorerEmbeddedCoder`**（大小写一致）。
- **凡需要传入「库名」字符串的操作**，一律使用 **`SysplorerEmbeddedCoder`**，例如：
  - 脚本内 **`LoadLibrary("SysplorerEmbeddedCoder", ...)`**（及同义 API 的库名参数）；
  - MCP **`load_library`** 等需要指定已安装库时，**库名字符串为 `SysplorerEmbeddedCoder`**；
  - 其它文档或工具说明里写「加载 Sysblock 系统库」「块图标准库」时，**实际传参仍必须是 `SysplorerEmbeddedCoder`**。
- **勿与模型限制混淆**：**`NewModel(..., restriction="Sysblock")`** 中的 **`"Sysblock"`** 表示**模型类型/限制（块图模型）**，**不是**系统库的顶层包名。**禁止**用 **`Sysblock`** 作为 **`LoadLibrary` / `load_library`** 等处的库名替代 **`SysplorerEmbeddedCoder`**。
- 块的全限定类名仍以 **`SysplorerEmbeddedCoder.<子包>.<块类名>`** 为准（任务书指定其它库时除外）。

---

## Part 0：Run Script 大前提 — Sysplorer 必须已启动且已连接

- **调用 `run_script` 模式之前**，**必须**先保证 **Sysplorer 已启动**，且 **MCP 驱动已与当前 Sysplorer 会话建立连接、可执行 ModelingPy**（与工具说明一致：**同进程**执行脚本）。这是 **Run Script 路径的总前提**；不满足则 **禁止**指望脚本能正确执行。
- **推荐顺序**（与 `CLAUDE.md` 会话开场一致）：
  1. 调用 **`session_manager(action="health")`**：若返回 **`ok=True`** 且 **`driver_ready=True`**，表示会话可用，可进入设计与脚本阶段。
  2. 若健康检查失败：依次尝试 **`action="ensure"`**、**`action="restart"`**（必要时 **`restart_mode="full_reset"`**）等，**直至** `driver_ready` 后再调用 **`call_code`**（`mode="run_script"`）。
- **禁止**在未确认 Sysplorer + 驱动就绪的情况下连续重试 `run_script` 调用代替环境修复。

---

## Part 1：设计先于编码

- **禁止**在未完成设计的情况下直接堆砌 `AddComponent` / `ConnectPorts` / `SetModelParamValue` 等 API。
- **编写任何建模脚本之前**，须先完成（可写在任务内设计说明或注释清单中）：
  1. **组件选型**：列出所需的 **`SysplorerEmbeddedCoder.*`** 全限定类名；每个实例的**建议实例名**；不确定的类名、**端口方向与语义**时，优先对 **`sysblock_model_library`** 语料检索：`resources_retrieval(action="corpora", corpus_id="sysblock_model_library")` 取解析路径，再 `action="search", query=..., sources=<上述路径>, index_path="resources/indexes/sysblock_model_library_index.json"`；并对已加载库中的**具体类**调用 **`get_lib_model_document(全名)`** 获取 Sysplorer 导出的类文档；**ModelingPy / Run Script 的 API 用法**调用 **`get_api_document(函数名)`**（官方 `Help`），辅以 **`SysblockParameters.md`** 与 Demo 示例，**禁止臆造**。
  2. **布局**：各块在框图中的**大致位置**（网格或坐标规划，与 `AddComponent` 的 x/y/宽/高等参数对应），避免脚本中随意摆放导致不可读或重叠。
  3. **连线**：**信号流拓扑表**（源实例.端口 → 目标实例.端口），与 `ConnectPorts`（或语料中的等价 API）一一对应，先核对端口存在性与方向再写脚本。
  4. **参数**：**参数表**（实例名、参数在 API 中的**合法键名**、目标值/枚举）；键名必须与 **`SysblockParameters.md`** 或语料一致。
- **设计定稿后再编码**：将调用序列写入 **Part 2** 的 **新建模型脚本** 或 **编辑模型脚本**，与上表严格对齐。

---

## Part 2：新建脚本与编辑脚本分离

### 2.1 职责划分

| 脚本类型 | 用途 | 典型内容 |
|----------|------|----------|
| **新建模型脚本** | 工程内**首次**创建该 Sysblock 模型 | `LoadLibrary`、`NewModel`（含显式 `restriction="Sysblock"`）、初始 `SaveModel` / 包结构创建 |
| **编辑模型脚本** | 模型报错后，**迭代**修改拓扑与参数 | `OpenModel`、 `RemoveComponent`、`AddComponent`、`ConnectPorts`、`SetModelParamValue`、移动块等；**不**重复完整「从零 NewModel」链，除非任务要求重建 |

### 2.2 `NewModel` 与 `restriction="Sysblock"`

- 创建 Sysblock 框图模型时，**必须显式传入** `restriction="Sysblock"`（字符串大小写与工具一致）。
- **禁止**依赖 `NewModel` 的默认参数隐含为 Sysblock；默认行为可能创建普通 `model` 或其它类型，导致后续块图 API 与预期不符。
- `NewModel` 等 API 的细节以 **`get_api_document("NewModel")`** 为准；示例流程仍可参阅 `SysplorerAPI/Examples/Demo_Python.md`（如 `NewModel("BounceBall", "Sysblock")`，第二个位置参数即为 `restriction`）。

### 2.3 加载块库

- 脚本中在添加组件前，须确保 **`SysplorerEmbeddedCoder`** 已按需 **`LoadLibrary`**（**只传库名、不传版本号**，由官方 API 自选合适版本；可通过 **`ClassExist`** 判断），否则 `AddComponent("SysplorerEmbeddedCoder....", ...)` 会失败。

---

## Part 3：块类型与参数（零臆造）

- **组件类型前缀**：框图内实例的类名**必须**使用 **`SysplorerEmbeddedCoder.*`**（任务书指定其它库时除外）。
- **模块用法与端口**：功能、端口含义、推荐接法、示例模型引用等以 **`resources/SysblockModelLibrary/`** 下对应 **`.md`** 为准（经 RAG 语料 **`sysblock_model_library`** 检索），并与 **`get_lib_model_document("SysplorerEmbeddedCoder....")`** 导出的类文档交叉核对；文档中的块名与库路径需映射到 **`SysplorerEmbeddedCoder.<子包>.<块名>`** 后再写入脚本。
- **参数名与枚举值**：与随包 **`resources/SysplorerAPI/SysblockParameters.md`**（**非 RAG**，直接读文件）一致；**API 函数签名与说明**以 **`get_api_document`** 为准，**禁止**猜测参数键名或中文说明在 API 中的拼写。

---

## Part 4：目录结构（与 package 层级一致）

### 4.1 磁盘与库浏览器对齐

- 工作区内的库目录建议与 Modelica **package** 习惯一致：例如 `src/<LibraryName>/` 为根包，其下子文件夹对应子 package（参见 `modelica_style_guide.md` Part 1 的目录思想）。
- Sysblock 模型作为该库中的**可检查、可仿真类**，应落在正确的包路径下，便于与手写 `.mo` 库共存及统一工具链。

### 4.2 `NewModel` 的 `parent` 与 `modelName`

- **`parent`**：传入**父 package 的全限定名**（full name），例如 `MyLib.Examples`，使新模型出现在库树中正确节点下。
- **`modelName`**：传入**完整限定名**，与 `parent` 层级一致，例如 `MyLib.Examples.MyController`。
- 创建 **package** 层级时，`restriction="package"` 的 `NewModel` 同样通过 **`parent`** 指定上级包，与文件夹中的 `package.mo` / 子目录结构同步（具体 `.mo` 落盘仍遵循工具保存逻辑）。

**禁止**：在已知应属于子包时省略 `parent`，导致模型落到错误包或工作区根散乱命名。

---

## Part 5：`call_code`（`run_script`）建模—编辑循环与结束条件

### 5.1 推荐循环

1. **满足 Part 0**（Sysplorer 已就绪）。
2. **首轮**：执行 **新建模型脚本**（含 Part 2–4 的约定）。
3. **后续轮次**：执行 **编辑模型脚本**，根据 `run_script` 分支返回的 `stdout` / `stderr` / `exception` / `traceback` 以及可选的 **`RUN_SCRIPT_RESULT`** 修正脚本。
4. **脚本执行成功**：以该分支返回 **`ok=True`** 且无未处理异常为**脚本侧**完成标准（见 `modeling_path_router.md` 3.3）。

### 5.2 循环结束标志：模型检查成功

- **「建图—改脚本」循环的终止条件**是：**目标模型在 MCP 工具链中检查通过**——即对**全限定模型名**调用 **`check_model`**（或 **`call_code`** 的 **`fast_workflow`** 模式中的检查阶段）**成功**，无编译 / 实例化错误。
- **`run_script` 分支返回的 `ok=True` 不能替代 `check_model`**：脚本跑通只说明 Python/API 未抛错；**交付前必须**得到检查通过结果，再进入仿真。

### 5.3 与路由文档一致

- 若部署设置 **`MWORKS_RUN_SCRIPT_DISABLED=1`**，`run_script` 模式不可用；须改用允许的执行方式或调整部署配置。

---

## Part 6：仿真与读结果（与 Modelica 物理模型统一）

- 在 **`check_model`（或等效检查）通过后**，**仿真、扫参、打开结果、KPI、`result_manager`** 等与 **Modelica 物理模型**分支**共用同一套 MCP 工具**（如 `simulate_model`、`call_code`（`mode="fast_workflow"`）等，按任务选用）。
- **不再**为 Sysblock 单独规定第二套仿真脚本规范；Sysblock 模型在工具中即为可仿真类，变量名通过结果文件或 **`result_manager`（如 `action=get_result_variables`）** 获取。

---

## AI 执行清单（Sysblock + Run Script）

- [ ] **`session_manager(action="health")`（或 ensure/restart 等效步骤）通过**、`driver_ready`，再调用 **`call_code`**（`mode="run_script"`）
- [ ] **设计清单**已完成：组件（`SysplorerEmbeddedCoder.*`）、布局、连线表、参数表；再编写脚本
- [ ] **新建**与**编辑**分为两个脚本；首次构建只跑新建脚本
- [ ] **`NewModel(..., restriction="Sysblock", ...)`** 显式传入 **`"Sysblock"`**
- [ ] 已 **`LoadLibrary("SysplorerEmbeddedCoder", ...)`**（不传版本，由 Sysplorer 解析）
- [ ] 块类型均为 **`SysplorerEmbeddedCoder.*`**；用法/端口对照 **`sysblock_model_library`** 与 **`get_lib_model_document`**；参数键名对照 **`SysblockParameters.md`**；API 说明对照 **`get_api_document`**
- [ ] **`parent` / `modelName`** 与 package 层级、磁盘目录规划一致
- [ ] 迭代以 **`check_model`（或 fast_workflow 检查）成功**作为建图循环结束标志
- [ ] 仿真与 KPI 使用与 Modelica 相同的 MCP 工具链

---

## 参阅路径（仓库内）

| 路径 | 说明 |
|------|------|
| `modeling_rules/modeling_path_router.md` | 分流与 Run Script 总流程 |
| `modeling_rules/modelica_style_guide.md` | package 目录与工程习惯（对齐 Part 4） |
| `SysblockModelLibrary/` | 各子库模块**用法文档**（RAG：`sysblock_model_library`，索引 `indexes/sysblock_model_library_index.json`） |
| `SysplorerAPI/Examples/Demo_Python.md` | Sysblock 示例（`NewModel`、`AddComponent`）；细节以 **`get_api_document`** 为准 |
| `SysplorerAPI/SysblockParameters.md` | 块参数名速查 |
| （无静态文件替代） | **`get_api_document("NewModel")`** 等 — `NewModel` / 其它 API 的权威说明 |
