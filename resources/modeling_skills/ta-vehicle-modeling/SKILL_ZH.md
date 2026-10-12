# TA 车辆库建模

本文件是 `SKILL.md` 的中文阅读版。本 skill 只能作为 `ty-sysplorer-modeling-rules` 之后的车辆领域薄补丁使用；父级 skill 负责 Modelica/Sysblock/混合建模分流、七门闸、布局时机、修复闭环、Sysplorer 安全规则和交付证据。本 skill 补充车辆领域入口路由、TA 六库建模决策、库边界、样例使用规则和结果验证重点。

## 入口契约

任何 Sysplorer 任务只要目标对象是车辆、整车、汽车子系统或车辆运行工况，即使用户没有点名 TA 库，也必须使用本 skill。

触发示例包括：

- 整车或子系统构建、修复、打包、评审、布局注解编写、翻译、仿真或结果验证。
- 集总参数、质点、等效质量、滑行、加速、制动、循环工况、续航、经济性、操稳、平顺性、热管理、发动机、电池、电器负载、底盘、轮胎、悬架、转向、制动、传动、动力总成和电机驱动车辆任务。
- 用户只说“车辆模型”“整车模型”“滑行工况”“动力性”“经济性”“续航”“操稳”“平顺性”“热管理”“发动机”“电池”“低压电器”等车辆领域词。

触发后，先应用 `ty-sysplorer-modeling-rules` 完成 Modelica / Sysblock / 混合建模分流。然后用本 skill 判断实现方式：使用 TA 六库组件、使用更简单的 Modelica/MSL/自建集总模型，或因 TA 证据不可用/超出范围而记录 fallback。不要因为用户说“简单”或“集总参数”就跳过本 skill。

## 硬约束

以下规则是阻断项，不是建议项：

- Sysplorer 车辆任务必须停留在 Sysplorer MCP / ModelingPy 工具体系中；除非用户明确要求 Syslab，不得路由到 Syslab skill 或 Syslab 工具。
- 新交付模型不得直接复制或 `extends` 完整官方示例、完整整车架构、完整子系统模板或完整样例交付物。
- 建模困难、内部信号接线找不到、修复失败或时间压力，都不能放宽上一条规则。遇阻时应缩小范围、手工搭建可见拓扑，或明确报告阻塞点；不得用继承完整模板来隐藏用户要求的模型结构。
- 除非任务只是验证或解释已有样例，交付源码必须通过显式组件实例和 `connect(...)` 展示用户要求的车辆拓扑。
- 对交付 `.mo` 执行 `CheckModel`、`TranslateModel` 或 `SimulateModel` 前，只要有文件路径，就必须运行 `scripts/audit_modelica_source.py`。包内模型通过 `--dependency-root` 显式传入已获准读取的顶层包目录，审计其上层 `package.mo` 依赖；未传时仅读取模型文件，不自行推定授权根或向根外搜索。审计失败是停止条件，不是警告。
- 仿真前必须确认用户要求的终止时间已经绑定到工具或模型的 stop-time 设置；不得把 `target_time` 等结果采样/探针时刻当成仿真终止时间，除非当前工具 schema 明确说明二者等价。
- 最终交付必须声明官方/样例使用状态：`仅参考`、`直接复用已有样例` 或 `未使用`。若为 `直接复用已有样例`，不得表述为新建交付模型已完成。
- 本次新建或实际修改的图形对象（含工具自动布局写回）按父级 Gate 6 验收。以层级、`Placement`、`Line(...)`、端点和布局诊断作为结构化证据；图片按用户需求和可用能力选用。只读、Documentation-only、无图形对象的纯代码、未改变图形目标的任务标记 `not_required`，不展开未修改的继承对象与层级，不虚构目视结论。

## 父规则与 MCP 0.4

会话复用、工具分类、错误解析及重试统一引用 `../ty-sysplorer-modeling-rules/references/shared-standards.md`；验证深度、Gate 6 与完成状态引用 `../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md`。离线/源码任务不调用会话。已有具体故障由父规则规定的独立调试入口主导；此时应用父规则仅表示复用其约束，不重启 Modelica/Sysblock/混合分流或 TA/非 TA 选型。本领域只提供定向证据，不重启完整建模；新建中的失败保留原任务。

执行到用户要求的终端阶段即停止。结果变量、KPI、曲线、动画和正式文档仅在用户要求或约定验收标准确需时执行，否则标记 `not_required`；不得为填表自动推定 proxy 指标。仿真成功与物理结果达标分别表述。

MCP 0.4 的类、组件、端口与文本查询使用 `model_inspect`，比较使用 `compare_model`，生命周期操作使用 `model_manager`。`call_code` 仅接受 `run_sysplorer_api` 或兼容别名 `run_script`，必须传对象 `payload` 并显式导入 ModelingPy。检查/翻译/仿真即使未传 `reload_mo_path`，也可能对已加载用户文件自动布局写回，不能作为无写入的只读评审工具；遵守父级授权边界，并把实际图形改动纳入 Gate 6。

## 最小读取

本文与对应 `SKILL.md` 中所有 `references/...`、`workflows/...`、`scripts/...`、`templates/...` 路径均相对于**本 skill 目录**（包含 `SKILL.md` 的文件夹），不是工作区根目录，也不是上层 `skills/` 目录。

只读取当前任务需要的文件：

| 需求 | 读取 |
|---|---|
| 新建模型预检 | 新建整车或子系统建模 workflow 前先读 `references/preflight-checklist.md` |
| 需求分类 | `references/requirement-map.md` |
| 库选择 | `references/library-selection.md`，再读一个相关的 `references/library-cards/<library>.md` |
| 手册/案例查询 | `workflows/verify-example.md`；直接对已命名或已推断的 TA 库使用 `load_library` + 类/文档探索 |
| 多库整车联合建模 | `references/combination-rules.md` |
| 建模 / 改模 | `references/build-rules.md`；需要设计用户车辆库业务分层时加读 `references/package-design.md` |
| 参数 | `references/parameter-rules.md` |
| 约定范围内的结果核验 | `references/validation-rules.md` |
| 修复 | `references/error-repair-playbook.md`，再读 `references/common-errors.md` |
| 验收 | `references/acceptance-checklist.md`、`references/output-contract.md` |
| 布局注解 | 任务包含源码级 `Placement` 或 `Line` 注解创建、修复时读 `references/diagram-layout-rules.md` |
| 输入稀疏 | `templates/scenarios/case-selection-template.md` |

## 专项流程

- 新建整车或子系统模型：`workflows/build-from-scenario.md`
- 修复已有车辆模型：`workflows/repair-existing-model.md`
- 验证官方或企业样例：`workflows/verify-example.md`

## 领域增量

- 使用“最小读取”表作为入口路由；不得默认加载全部 TA reference 或全部库卡片。
- 对“查找并打开案例”等信息查询任务，使用 `workflows/verify-example.md`，直接对已命名或已推断的 TA 库执行 `load_library`、类列表和定向类文档查询。
- 使用 `references/requirement-map.md` 与 `references/library-selection.md` 完成任务分类、TA 库职责判断和主库/辅助库选择。
- 新建整车或子系统模型时，将 `references/preflight-checklist.md` 作为编辑或检查模型源码前的阻断性预检门禁。
- 常见整车任务优先使用选中库卡片中的速查入口：`TAEconomy` 用于 `0-100` / CLTC / 循环工况 / 传统车 / 纯电 / 混动架构，`TADynamics` 用于 KC 悬架、六轮或底盘动力学，`TAThermalSystem` 用于 HVAC、乘员舱和制冷剂回路。
- 修复、验证、布局注解、package 设计、参数和交付口径使用对应 workflow/reference，并在最终交付前回到 `references/output-contract.md` 与 `references/acceptance-checklist.md`。
- 用户可见说明、图面文字和注释默认用中文；库名、类名、变量名和接口名保持原文。

## 修复优先级

已有具体故障直接按“父规则与 MCP 0.4”的调试归属处理，不重新进行父级路由或车辆选型。下列顺序只是诊断定位顺序，执行到请求终态即停止，不要求运行全部后续阶段。

优先沿最短阻塞链排查：

`primary-library boundary -> library dependency -> model hierarchy/interfaces -> topology/connections -> parameters/units -> initialization -> check/translate -> simulation -> result variables -> diagram annotations`

保留已有有效结构，修复后回到失败的父级 Step/Gate。尽可能将诊断性修改与最终交付修改分开。

## 时间预算控制

- 大型整车、多轴总成先按“发现 -> 骨架 -> 检查”推进，再仅执行请求内的翻译/仿真/结果阶段；实际图形改动独立按 Gate 6 验收，纯视觉缺陷不阻塞运行阶段。不把整轮工作耗在无边界库探索上。
- 优先使用所选库卡片中的速查案例/类，再做必要的局部探索。
- 若建模或修复出现超时趋势，先冻结较小的可运行契约并验证，再报告具体未闭合的子系统或接口阻塞点，不要在无边界探索中静默继续。

## 交付增量

在父级交付证据基础上补充：

- TA 主库、辅助库、基础依赖、选用的官方/样例参考和最终模型入口。TA 库边界约束负责的子系统；保留父规则项目总库集合中已选标准库及支持领域组件。
- 车辆范围与工况：架构、子系统边界、驾驶循环 / 道路 / 热边界或运行工况。
- 建模契约与源码自检结果，包括官方模板/示例是否仅参考、是否直接复用已有样例，或未使用。
- 已验证动作：`CheckModel`、`TranslateModel`、`SimulateModel`、源码级布局注解检查和结果变量核验状态。
- 针对动力性、经济性、续航、动力学、热管理、发动机、电池或电器负载结果的已核验变量和通过 / 失败 / 无参考判定。
- TA 库替换、未确认假设、样例检索阻塞或未闭环项。
