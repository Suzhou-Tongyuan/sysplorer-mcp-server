# TY 液压 / 气动建模

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

## 最小读取

| 需求 | 读取 |
|---|---|
| 需求分类 | `references/requirement-map.md` |
| 库/组件映射 | `references/library-selection.md`, `references/component-map.md` |
| 介质选择 | `references/media-selection.md` |
| 参数 | `references/parameter-rules.md` |
| 验证 | `references/validation-rules.md` |
| 容阻拓扑 | 使用 `TYHydraulics` / `TYHydraulicComponents`，或检查/翻译/仿真症状指向流体容阻不匹配时读取 `references/capacitor-resistive-check.md` |
| 修复 | `references/error-repair-playbook.md`，再读 `references/common-errors.md` |
| 验收 | `references/acceptance-checklist.md`, `references/output-contract.md` |
| 图解专项 | 任务包含建图或修图时读取 `references/diagram-layout-rules.md` |
| 手册查询 | 仅在精简参考不足时读取 `references/manual-index.md` |

## 专项流程

- 从场景/表格/CSV 新建模型：`workflows/build-from-scenario.md`
- 现有模型或图解修复：`workflows/repair-existing-model.md`
- 官方或企业样例验证：`workflows/verify-example.md`

## 领域增量

- 先判断任务类型：新建、修复、样例验证、结果复核或仅指导。
- 建模前先选定流体家族：液压、热液压、气动、气体介质或热支撑。
- 介质选择属于结构性决策；压力、气体或温度行为重要时，不得在介质未知或错误的情况下继续。
- 结构范围内检查液压/气动拓扑、介质和边界/参考完整性；压力、流量、位移、阀状态及执行器方向仅在结果验收范围内验证。
- 对阀 `Signal` 控制输入口，电流型命令必须先换算成 `mA` 数值后再输入，电压型命令必须先换算成 `V` 数值后再输入；不得因为其他参数声明采用 SI 基本单位 `A`，就把用户给出的 `40 mA` 改写成 `0.04` 再送入信号口，正确输入值必须是 `40`。对三位换向阀，必须按“左位负值、中位 `0`、右位正值”解释，除非项目资料已明确给出相反的极性约定。
- 使用 `TYHydraulics` 或 `TYHydraulicComponents` 的液压模型，在请求的长仿真前，以及阀、泵、管路、容腔、容积开关等拓扑修复后，纳入适用容阻拓扑复核。按 `references/capacitor-resistive-check.md` 区分离线复核、只读诊断和授权实时修复；MCP 能力可用不等于允许启动软件、实时检查或修复。
- 热液压模型需确认热端口和热边界假设；温度响应仅在结果验证属于验收范围时校核。
- 结果验证为 required 时，预期动作下零流量、非物理压力、位移反向、NaN/发散、温度无响应视为结果验证失败；不为未请求结果的任务追加取值。
- 图解任务中关键实例和关键连线必须可见、可审阅；布局时机仍由父级 Gate 6 控制。

## 修复优先级

优先沿最短阻塞链排查：

`source/boundary -> library dependency -> component mapping -> parameters -> topology -> capacitor/resistive topology -> medium -> initialization -> translation -> simulation -> result variables -> diagram annotations`

修复后回到失败的父级 Step/Gate；若拓扑、参数或图解语义变化，重跑受影响父级链路。

## 交付增量

在父级交付证据基础上补充：

- 实际使用的 TY 库、模型名/路径、拓扑摘要、介质、参数假设和未确认项。
- 使用 `TYHydraulics` / `TYHydraulicComponents` 或修复路径涉及容阻问题时，说明容阻检查状态。
- 仅在结果属于验收范围时列已验证变量及通过/失败/无参考判断；否则为 `not_required`。
- 对建模或图解修复任务，说明图面可读性。
