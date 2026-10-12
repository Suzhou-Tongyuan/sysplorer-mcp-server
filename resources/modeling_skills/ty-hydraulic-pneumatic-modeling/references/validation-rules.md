# 验证规则

本文件只补充父级验收范围内的流体检查项。结果、KPI、曲线和动画仅按请求执行；未要求时为 `not_required`。图面触发与状态以 `../../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md` 为准，本次新建或实际修改图形对象才执行适用 Full Gate 6；只读、Documentation-only、纯代码无图形对象、未改变图形目标的任务为 `not_required`，不展开未修改继承对象和层级。

## 结果验证规则（仅 result_verification 为 required 时）

| 场景 | 关键变量 | 判断标准 | 风险提示 |
|---|---|---|---|
| 阀控缸基础回路 | `cylinder displacement` | 位移方向与命令和负载设定一致 | 反向时优先检查负载方向、A/B 腔连接、阀口语义 |
| 阀控缸基础回路 | `pressure at supply / A / B / return` | 压力水平与回路拓扑一致，无明显物理矛盾 | 压力异常时优先查边界、溢流支路、回油闭合性 |
| 阀控缸基础回路 | `flow rate` | 有动作时主工作线不应长期为零 | 零流量时优先查介质、边界、阀芯状态、断线 |
| 泵阀系统 | `pump outlet pressure` | 与负载和阀状态变化一致 | 不合理高压常见于回路堵塞或回油缺失 |
| 热液压系统 | `temperature` | 温度变化与热边界和工况一致 | 温度无变化时优先查是否误用普通液压库 |
| 热液压系统 | `enthalpy / heat-transfer related variables` | 与热交换对象和边界一致 | 结果缺失时优先查热端口和热边界 |
| 气动回路 | `cylinder position` | 动作方向与阀状态和负载设定一致 | 不动作时优先查气源、排气、阀位 |
| 气动回路 | `gas pressure` | 压力变化符合充气、放气与节流逻辑 | 压力不变时优先查边界和排气路径 |

## 图面与连线验证规则

| 校核项 | 必须通过的标准 | 失败时优先排查 |
|---|---|---|
| `planned_connection_count_vs_connect_count` | 拓扑连接表与真实 `connect(...)` 数量一致 | 漏连、误连、连接表未更新 |
| `placement_annotations_present` | 每个关键实例都有 `annotation(Placement(...))` | 图面缺失、悬空端点、红色虚线 |
| `diagram_layout_preflight_passed` | 对本次目标调用 `scripts/check_modelica_diagram_layout.ps1 <model.mo> -TargetClass <FQClass> -Json`，保留 passed / failed / undetermined；未确定时补充父级 Gate 6 所需证据，不冒充脚本通过 | 目标范围、表达式支持限制、旋转后的包围盒、拥挤和越界 |
| `line_annotations_present` | 创建模型任务中每条计划可见的 `connect(...)` 都带 `annotation(Line(points=...))` | 图面无连线、折线异常 |
| `line_annotation_preflight_passed` | 对本次目标调用 `scripts/check_modelica_line_annotations.ps1 <model.mo> -TargetClass <FQClass> -Json`，保留 passed / failed / undetermined；零连接通过仍须核对计划，循环语句数不等于展开连接数 | 目标范围、未支持表达式、漏写 Line 注解、零长度连线 |
| `diagram_annotation_present` | 模型中存在 `Diagram(coordinateSystem(...))` | 图面布局失控 |
| `graphical_instances_present` | 创建任务中的关键元件已经实例化并在图形图面中可见 | 只写了文本结构、未完成图形实例化、图面中看不到模型主体 |
| `visible_instance_count_matches_plan` | 图面中可见的关键实例数与计划实例数一致或差异已解释 | 模型树里有元件，但图面里缺实例 |
| `visible_connection_count_matches_plan` | 图面中可见的关键连线与计划连线一致或差异已解释 | 文本里有连接，图面中看不到关键连线 |
| `critical_wires_visible` | 关键压力线、工作线、回油 / 回气线、控制线在图中可见 | 连线被图标或文字完全遮挡 |
| `layer_separation` | 主流体回路和控制线分层清晰 | 就近最短线导致交叉混乱 |
| `symbol_scaling` | 阀、缸、主要流体元件保持等比例缩放 | `extent` 非等比拉伸 |
| `connector_anchor_quality` | 对外暴露的 connector 实例带 `Placement` 和 `iconTransformation` | 红色虚线、悬空端点、端口锚点异常 |
| `capacitor_resistive_topology_checked` | `TYHydraulics` / `TYHydraulicComponents` 模型按 `references/capacitor-resistive-check.md` 及任务授权完成静态复核或实时检查；离线复核不等同自动检查通过，未请求的实时项为 `not_required` | 阻性件直连、容性件直连、接口容腔开关不当、自建端口缺容阻标识 |

## 图形层正常显示最低要求

1. 关键元件实例在图形图面中可见，而不只是在模型树中存在。
2. 关键连线在图形图面中可见，而不只是在文本 `connect(...)` 中存在。
3. 图面布局在导图、直接图形复核或结构化图面复核时可正常阅读，没有主体缺失。
4. 若任一项不满足，则该创建任务仍视为图形层未闭环。

## 图面复核最低要求

1. 对适用 Gate 6 的变更图形目标完成图面复核。结构化证据是共同基础；按用户需要和工具能力补充图片，图片无法提供时记录明确请求的缺口，不虚构目视验收。
2. 对创建模型任务，必须确认关键元件实例已经在图形图面中可见，用户可直观看到模型结构。
3. 对创建模型任务，必须确认关键连线在图形图面中可见，而不是只有模型树或文本结构正确。
4. 图面复核要明确写出是否检查了 `Placement`、`Line`、`Diagram` 三类注解。
5. 必须确认长标签没有遮挡阀、缸或关键端口。
6. 必须确认没有关键断线、明显乱线或明显拉伸变形图元。
7. 必须确认 `Line(points=...)` 至少有两个不同坐标点，且坐标落在 `Diagram(coordinateSystem(...))` 范围内。
8. 记录 `.mo` 布局和连线预检查结果。纯视觉缺陷不阻止 `check_model`、翻译或仿真；注解语法/结构错误由模型检查阻断依赖执行。适用图面问题须在完整图形交付前修复，不把模型检查通过当作 Gate 6 通过。
9. 记录结构化证据路径：脚本结果、实例/连线计数、坐标范围、锚点、关键路由和图形状态；使用图片时补充图片来源。自动布局导致的实际图形改动纳入目标范围，分别记录文件写回与会话持久化。

## 结果通过阈值（仅已要求结果的任务）

1. 关键变量已经命名并可读取。
2. 关键变量与用户目标存在直接映射关系。
3. 变量变化趋势与拓扑和参数设定一致。
4. 结果判断与图形层状态分别记录；图面验收的适用性和完成状态依父级 Gate 6 判断。
5. 分别说明请求结果与适用图面的完成情况；图面未闭环不改判已成功仿真。MCP 0.4 仿真失败不能用残留结果判成功；时间插值和端点回退保留 warning，不冒充原始采样。
