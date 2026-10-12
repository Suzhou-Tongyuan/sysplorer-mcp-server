# TY 机械建模

本文件是 `SKILL.md` 的中文阅读版。本 skill 只能作为 `ty-sysplorer-modeling-rules` 之后的领域薄补丁使用；父级 skill 负责分流、七门闸、布局时机、修复闭环和交付证据。
共同规则以 `../ty-sysplorer-modeling-rules/references/shared-standards.md`（MCP 0.4 会话、工具、错误与重试）和 `../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md`（验证深度与七门闸）为准，本领域不建立第二套流程。

- 继承明确选择、有效上下文与已有模型的库边界。未选库时，父级先判断标准库功能；满足则使用标准库，不足则保留可用标准库部分并补充商业组件。文档或工具失败不等于功能缺口；同一 Modelica 实现的组合选库不自动进入 Modelica＋Sysblock 混合流程。
- 白名单仅约束本领域负责的子系统；保留已选标准库部分及其他领域组件，通过真实接口核对完成跨域连接。
- 商业路径及标准库＋商业库组合固定使用 `Modelica 4.0.0.TY.1`；与工程版本冲突时记录不一致，不静默改写依赖。
- 继承用户验收范围，未要求的结果、曲线、KPI 和动画为 `not_required`。正式报告与报告模板仅按请求使用，普通交付提供简洁证据和适用状态。
- 已有故障由父级调试路线主导，本领域补充定位证据和最小修复；新建流程中的故障修复后返回原流程失败阶段。
- 本次新建或实际修改图形对象（含 MCP 自动布局写回）触发适用 Gate 6；只读、Documentation-only、纯代码无图形对象或未改变图形目标时为 `not_required`，不展开未修改的继承对象和层级。
- 结构化图面证据为共同基础，图片按请求和能力补充；明确要求图片而无法提供时记录未完成，不把文本结论称为目视验收。纯视觉缺陷不阻止 check、翻译或仿真，注解语法/结构错误由模型检查处理；完整图形交付前仍完成适用 Gate 6。
- MCP 0.4 的 check/translate/simulate 即使不传 `reload_mo_path` 也可能自动布局并写回用户文件。只读诊断先核对该边界，可在获授权副本验证，无法保证只读时记录限制；不得承诺 check 无写入或用脚本绕过专用工具。

## 强制入口守卫

- 用户明确指定、有效上下文/已有模型已选定，或父级为标准库功能缺口选定 TY 机械组件后进入本 skill；本轮提示不必重复库名。
- 用户指定 Modelica 标准库、自建实现或其他非 TY 机械库，且未要求 TY 商业组件时，禁止加载本 skill 及其 references/workflows，立即返回父级 Modelica 工作流。
- 机械主题本身不是触发条件；摆、刚体、关节、传动、多体运动、接触或动画等词不能单独触发本 skill。
- 本领域补丁不得提高父级已经选定的验证深度。结果变量、曲线、KPI 分析或动画，只有用户明确要求或父级验收合同明确包含时才执行。
- 验收止于 `check + translate + simulate` 时，该链成功后结束执行并完成适用 Gate 6 与交付证据，不追加结果步骤或后处理。

## 最小读取

本文与对应 `SKILL.md` 中所有 `references/...`、`workflows/...`、`templates/...` 路径均相对于**本 skill 目录**（包含 `SKILL.md` 的文件夹），不是工作区根目录，也不是上层 `skills/` 目录。

| 需求 | 读取 |
|---|---|
| 需求分类 | `references/requirement-map.md` |
| 组件映射与查询范围 | `references/component-map.md` |
| 参数与接口确认 | `references/parameter-rules.md` |
| 预检、验证与结果判断 | `references/validation-rules.md` |
| MCP 查询与工具效率 | `references/mcp-modeling-toolkit.md` |
| 修复 | `references/common-errors.md`，再读 `references/error-repair-playbook.md` |
| 验收 | `references/acceptance-checklist.md` |
| 输入稀疏 | `templates/scenarios/user-input-minimum-form.md` |

## 专项流程

- 新建 TY 机械模型：`workflows/build-from-scenario.md`
- 修复现有模型：`workflows/repair-existing-model.md`
- 验证样例：`workflows/verify-example.md`

## 入口路径分流

选择流程或加载库之前，先把任务分到以下路径之一：

| 路径 | 适用场景 | 初始库边界 |
|---|---|---|
| 一维简化模型 | 系统可以抽象为集总平动/转动机械、轴系动力学或动力传动，不需要空间姿态、frame 几何、接触、柔性体或多体动画。即使真实机器是三维实体，只要用户要的是等效/简化模型，也先按此路径处理。 | 初始只用 `TYMechanics` 和 `TYDriveline`。`TYMechanics` 用于基础平动/转动机械，`TYDriveline` 用于传动链和传动元件。 |
| 二维平面模型 | 用户明确要求平面、x-y、绕 z、或 `TYMechanics2D` 行为。 | `TYMechanics2D` 及其必需的 world/reference 组件。 |
| 三维模型 | 用户需要空间刚体、姿态、frame、世界坐标、多体运动、动画、三维传动、接触/碰撞、柔性体，或任务不是一维简化且不是明确二维平面。 | 可使用除二维平面路径库以外的相关 TY 机械库：常见为 `TYMultibody`、`TYDriveline3D`、`TYContact`、`TYFlexBody`，必要时可把 `TYMechanics` / `TYDriveline` 作为已确认接口兼容的一维子模型接入。 |

若路径不明确，只有当运动维度会改变交付物时才追问一个阻塞问题。否则仅在用户目标明确是等效/简化模型，且不需要姿态、动画、接触、柔性变形或空间约束时，才优先按一维简化路径推进。路径分流只限定首轮库搜索范围；写模型前仍必须确认真实组件路径、端口和参数。

## 领域增量

- 先判断任务类型：新建 TY 机械模型、修复、样例验证或结果复核。
- 先执行入口路径分流：在一维简化、二维平面、三维模型之间确定路径，再选择 TY 子库。
- 先区分任务是模型构建还是库信息查询。信息查询任务优先获取有限的库/类概览并在本地筛选，避免反复深读大段文档。
- 写模型前做短预检：所选 TY 子库、组件接口类型、世界/参考需求、预期自由度、关键参数和最小物理合理性校核；仅在结果验证属于验收范围时补充预期结果变量。
- 多体模型必须存在 `TYMultibody.World` 或等价世界/参考组件。
- 平面闭环机构必须使用并报告切割铰策略。
- 先搭最小可检查机械闭环，再添加损失、接触、柔性体、监测或扩展工况。
- 赋值前先查询真实组件参数。
- 组件文档按阶段查询：先查包/类列表，再只查当前模型需要的候选组件和接口；不要重复查询同一组件或子包。
- 一维转动链在 `check` 前先检查接地/参考与自由度：除非明确要锁死元件，惯量/负载不应两端都刚性接地。
- 一维/三维混合或传动/多体跨库连接前，先确认连接器兼容性（`flange`、`frame`、信号端、inner/outer world）。
- 只有验收合同要求结果证据时，才验证适用的位移、速度、角速度、力、力矩、反力、接触力、穿透、位姿、关节变量、约束反力、变形或模态响应。
- 只有用户明确要求动画或运动可视验收时，才打开并判断多体动画；仅要求搭建、检查、翻译和仿真的任务不得追加动画。
- 需要结果验证时只读取满足验收所需的最少变量，并用简单手算、符号或趋势预期做对照；仿真成功后不得自动读取结果。
- 错误分类、会话证据复用和受控重试继承父级 shared-standards；用文档、组件级最小模型或静态源码检查隔离根因，不重复无效调用。

## 修复优先级

优先沿最短阻塞链排查：

`TY library boundary -> component/interface confirmation -> world/reference -> structural connection -> equation balance/DOF -> parameters -> initialization/constraints -> solver -> result interpretation`

保留已有有效结构，修复后回到失败的父级 Step/Gate。

## 交付增量

在父级交付证据基础上补充：

- TY 子库边界、选用组件、参数来源、已完成的用户要求验证动作和已知风险；仅在结果验证属于任务范围时列出已验证变量。
- 如替换 TY 组件，说明替代理由和预期影响。
- 平面闭环机构说明切割铰细节。
- 仅在动画属于用户验收范围时，说明多体动画状态和基于动画的判断。
- 信息查询类交付说明查询范围、已检查的库/类和有意省略项，证明结果足够完整且没有做高 token 的无边界探索。
- 生成模型库或可复用包时，仅在用户明确请求文档时进入父级 Documentation 路径，并遵守请求的内容范围与格式；默认写入 `Documentation(info=...)`，只有明确要求时才创建独立 Markdown。未请求文档时为 `not_required`；保留必要的代码级简短描述与参数单位，不据此扩展为正式文档。
