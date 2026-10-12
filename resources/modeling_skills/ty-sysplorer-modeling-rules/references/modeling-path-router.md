# 建模路径判定规则

仅在任务边界存在歧义时读取本文件。明确的普通 Sysblock 框图、StateMachine、信号处理或通信任务应直接使用对应 Sysblock 专业 Skill，不进入本总规则。

已有模型的具体故障诊断/修复优先独立使用物理或 Sysblock 调试 Skill，未知故障域使用 `ty-sysplorer-debugging`。这不是先经过本文件的强制链路。调试为修改或交付读取本文件时，只取适用约束并返回当前步骤，不再次分流。新建过程中发生故障时保持原任务上下文，按需使用调试能力后继续建模。

## 1. 先判定建模形式

| 线索 | 判定 | 后续动作 |
|---|---|---|
| `.mo`、物理连接器、连续方程、`connect(...)`、物理参数、Modelica 库组件 | Modelica 物理 | 读取 Modelica 规范，完成类/端口证据和领域映射 |
| 物理 Modelica plant/顶层，需要协调已完成的 Sysblock 控制器或算法 | 混合建模 | 读取混合 workflow；Sysblock 子模型和物理顶层分层处理 |
| `NewModel(..., restriction="Sysblock")`、块图、状态机、信号链、嵌入式编码器，且无物理顶层集成 | 普通 Sysblock | 直接交给 Sysblock 专业 Skill |
| 只询问 API、结果或帮助文本 | 非建模任务 | 分别走 API、结果或文档路由，不创建模型 |

混合建模中，物理 Modelica 顶层通过已识别的 SEC/混合实例协调 Sysblock 子模型；不得在同一层混放物理组件与 Sysblock 基础块。仍无法判断时，只提出一个澄清问题：目标是纯物理 Modelica，还是“物理顶层 + Sysblock 子模型”？

## 2. 再判定实现和证据边界

1. 按 `domain-routing-and-library-versions.md` 复用有效实现边界。未指定库时先评估标准库功能，满足则使用标准库；显式标准/自建要求继续优先，不因机械等领域词引入 TY 商业 Skill。
2. 标准库有证据确认的功能缺口时，保留可用标准组件并选商业组件补足；查询/加载失败不代表功能不足。商业类须有公开类、端口或行为证据；不得以能否读取源码为选择条件。组合选库不自动成为混合建模。
3. 对商业类，转入 `references/shared-standards.md` 的受保护证据流程。文档不足时只能进行公开内省和最小黑盒验证。
4. 类、端口、连接器、单位或维度仍不明确时，在扩展系统前先解决证据缺口或隔离最小案例。

## 3. 领域 Skill 的选择

选择一个负责主要组件边界的领域 Skill，再仅为真实跨领域边界追加支持 Skill：

| 主要边界 | 首选 Skill |
|---|---|
| 液压、热液压、气动 | `ty-hydraulic-pneumatic-modeling` |
| 已明确选择 TY/同元商业机械库的机械、多体、传动或接触 | `ty-mechanical-modeling` |
| 热流体、换热、空气处理、HVAC | `ty-thermofluid-modeling` |
| 明确的 `NPSLibrary` 电力电子/电机驱动任务 | `ty-nps-library-modeling` |
| TY 电气/电机、电力或能量系统 | `ty-electrical-machine-power-modeling` 或 `ty-energy-modeling` |
| TA 车辆系统 | `ta-vehicle-modeling` |
| 库级包结构、公共接口、Examples/Tests 组织、本地化、库扩展或库评审 | 在本 Skill 分流后追加 `modelica-library-workflow` |

领域 Skill 负责已选商业组件边界的建模、检查和仿真细节；本 Skill 负责路径判断、商业库边界、跨层协调和全局 Gate。纯 Modelica 标准库、自建或其他非 TY 机械/多体任务留在父级 Modelica 路径，禁止加载 `ty-mechanical-modeling`。不得同时无理由加载多个领域 Skill，也不得用本总规则替代已适用的专业领域规则。跨领域冲突和库名优先级以 `references/domain-routing-and-library-versions.md` 为准。
