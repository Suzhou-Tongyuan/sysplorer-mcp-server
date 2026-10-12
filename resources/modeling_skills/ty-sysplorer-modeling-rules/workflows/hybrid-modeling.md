# Modelica 与 Sysblock 混合建模工作流

仅当路径判断确认“物理 Modelica plant/顶层 + 一个或多个已完成 Sysblock 控制器或算法子模型”时使用本工作流。它组合两种层级，但不改变职责：Sysblock 子模型由对应 Sysblock 专业 Skill 通过官方 API 构建和接线；物理 plant 与顶层边界 `connect(...)` 图由 Modelica `.mo` 文本构建。

## 1. 边界与包含规则

- 将块图、状态机、离散控制、传递函数、PID、CCaller 及其内部信号连线保留在 Sysblock 子模型中。
- 明确 Sysblock 子模型的归属 Skill：控制块图、子系统、StateMachine、PID、离散逻辑、CCaller、块参数和内部连线使用 `ty-sysblock-diagram-modeling`；滤波、频谱、多速率处理、特征提取、基带链路、BER、调制解调、同步、DSSS 或 `TYDSPSystem` / `TYCommunication` / `TYMixedSignal` 使用 `ty-sysblock-signal-modeling`。同一混合任务同时存在两类独立子模型时，按实际子模型边界分别使用相应 Skill。
- 将物理组件、物理连接器、商业物理库组件、物理方程和顶层 Modelica `connect(...)` 图保留在 Modelica plant 或 wrapper 中。
- 允许 Modelica 物理顶层通过已识别的 SEC/混合实例嵌入已完成的 Sysblock 模型；禁止在 Sysblock 内嵌入物理 Modelica 模型。
- 禁止在普通模型的同一层混放物理组件和 Sysblock 基础块；不得手写 Sysblock 拓扑 `.mo`，也不得对其使用 `SetModelText`。

## 2. 使用受支持的 SEC/混合边界

普通同层 `AddComponent` 被拒绝，并不等同于 Sysplorer 不支持混合建模，通常只说明插入路径不正确。

1. 先用其归属 Skill 独立构建并检查 Sysblock 控制器/算法。
2. 物理 Modelica 顶层中若已有已识别的 SEC/混合实例，优先复用，并保留其 Sysplorer 识别语义，包括已有的 `__MWORKS(SECInstance=true)` 元数据。
3. 若不存在该实例，使用 Sysplorer 支持的 SEC/混合实例插入流程；不得用普通 `AddComponent` 将 Sysblock 基础块强行插入物理层。
4. 若受支持的插入路径不可用，且用户未提供可复用或已插入的 SEC 实例，应准确报告该边界，并请求所需实例或授权；不得以虚构的 Modelica 控制拓扑替代 Sysblock 子模型。

## 3. 构建前定义接口契约

在任何跨层连接前建立边界表。每个暴露信号都要记录名称、方向、生产者、消费者、类型、维度、采样周期、单位、物理含义、初始/默认处理和所需转换。

| Sysblock 侧 | Modelica/物理侧 | 必须明确的决定 |
|---|---|---|
| `float` / `double` | `Real`、`RealInput` 或 `RealOutput` | 单位、信号方向、范围和采样时间解释 |
| 有符号/无符号整数 | `Integer`、`IntegerInput` 或 `IntegerOutput` | 范围、符号、饱和与显式转换 |
| `fixdt` | 不假定通用映射 | 显式确认受支持的转换和缩放 |
| `enum` | 不假定通用映射 | 定义显式的语义转换 |
| 数组或 Bus | 兼容的结构化连接器或选定数组分量 | 确认成员顺序、维度和连接规则 |

连接前检查实际暴露的 `Inport` / `Outport`。必须确认两端类型和维度；不得仅凭名称推断 Bus、数组、枚举、定点转换或物理单位映射。

## 4. 按层构建

1. **定义控制意图和契约。** 明确命令、反馈、控制输出、显示、故障、时序和单位转换边界；每个信号有稳定可读的名称和唯一责任方。
2. **构建 Sysblock 子模型。** 使用其专业 Skill 和官方 API 定义块、参数、布局及内部连线；嵌入前必须先通过子模型检查。
3. **构建或验证物理 plant。** 遵循 Modelica 工作流：基于公开证据选择标准/自建/商业组件，编写 `.mo` 物理拓扑；可独立实例化时先独立检查。
4. **嵌入或复用 SEC 实例。** 只能通过已识别混合边界放置完成的 Sysblock 子模型；在假定端口名称或方向前查询/检查其暴露端口。
5. **连接顶层。** 仅在 Modelica wrapper 中连接暴露的边界端口；为重要边界实例和连接提供可用的 `Placement` / `Line` 信息；不得修改 Sysblock 子模型文本以添加物理连接。
6. **分层检查。** 按“Sysblock 子模型 → 可独立检查的物理 plant/组件 → 混合顶层”顺序检查；后续检查发现边界问题时，返回受影响层修复。
7. **按需验证混合顶层。** 仅执行验收范围内的翻译/仿真阶段，目标为混合顶层而非任意子模型。只有父 Gate 5 将结果验收判为 `required` 时，才通过顶层或有效嵌套结果路径核验所需变量。验收仅止于 check + translate + simulate 时，`verify_result_var` 留空，结果为 `not_required`；三项成功后只收完适用 Gate 6、必要图形复检与交付证据，不读取结果或追加 KPI。

## 5. Gate 6 与图形验收

对每一个已改变的图形层执行 Full Gate 6；其全局通过条件和记录字段以 `workflows/seven-gates-validation.md` 为准。各专业 Skill 检查自己负责的层，本 Skill 只汇总状态，不重复执行相同图面检查。

- **Sysblock 子模型**：在其检查通过后，由归属 Skill 完成图面流程并返回状态。
- **物理 plant/组件**：检查外部连接器位置、关键内部实例、计划可见连接以及 Icon/Diagram 可读性。
- **混合顶层**：检查 SEC 实例、物理组件和每条跨域连接。首次验收不主动追加布局修复；Full Gate 6 失败后才按需修复。MCP 检查内部可能自动写回 Modelica 图形，授权、变更记录及复检按主 Gate 6 处理。

只验收本次实际修改的图形层；已修改的子模型或物理组件也是图形交付对象时，不得只验收顶层图面。未修改层不展开检查。

## 6. 修复与验收清单

边界检查失败时，先区分原因是 SEC 实例缺失、暴露端口不匹配、类型/维度/单位不匹配、转换缺失、物理连接器无效、初始化/时序不匹配，还是布局元数据问题。修复已识别的层后，重新执行所有受影响的后续检查。重试与同一假设停止条件引用 shared-standards，不另设次数政策；必要时隔离最小 child/plant/boundary 案例取证，再由七门闸闭环继续。

- [ ] Sysblock 子模型和物理 Modelica plant 的责任边界、建模形式正确且相互独立。
- [ ] 每个跨域信号都有记录在案的契约和已验证的暴露端点。
- [ ] 已复用或通过受支持流程插入已识别的 SEC/混合实例；未使用同层混放规避手段。
- [ ] 子模型、可独立测试的 plant 和混合顶层按顺序通过适用检查。
- [ ] 每个已修改图形层都已完成 Full Gate 6；专业 Skill 的状态已汇总，Modelica 实际写回后已重新检查。
- [ ] 所选验证深度要求时，翻译、仿真和 KPI/结果证据覆盖混合顶层。
