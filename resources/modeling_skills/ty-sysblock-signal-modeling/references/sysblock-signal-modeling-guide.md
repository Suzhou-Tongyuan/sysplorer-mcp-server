---
name: sysblock-signal-modeling
description: 用于指导在 Sysplorer 中完成 Sysblock 信号/通信建模，提供领域方法、模板、参数契约、KPI 口径与验证建议。
---

# Sysblock 信号/通信建模指南

## 拆分说明

本文件仍保留原有完整内容，作为历史主文档与集中参考。
为避免单文件过大，当前已将工作流与专题内容拆分到更小的参考文件中；新任务应优先按以下顺序阅读：

1. `workflow-overview.md`
2. `template-selector.md`
3. `modeling-methods.md`
4. `playbooks.md`
5. `parameter-contracts.md`
6. `execution-checkpoints.md`
7. `troubleshooting-and-fallback.md`

若只需要快速进入主流程，优先看 `workflow-overview.md` 与 `execution-checkpoints.md`。
若需要完整旧版集中说明，再继续阅读本文件正文。

## 1. 文档定位

本文件定位为 **Sysblock 信号/通信建模指导层（Domain Guidance Layer）** 的方法主文档（SSOT）。
其职责是提供领域方法、模板、参数契约、KPI 口径与常见错误处置，用于增强 Sysblock 建模质量与可复现性。

定位边界：
- 本文档不是全局流程裁决层，不替代 `modeling_rules`。
- 与全局流程规则冲突时，以 `modeling_rules` 为准；与本层执行细节冲突时，以本指南与 `sysblock-signal-modeling-handbook.md` 的一致定义为准。
- 本文档不负责 Sysplorer 会话健康管理、`run_sysplorer_api` 全局调用纪律、Modelica 分支规则。

策略原则：
- 默认“基础 Sysblock 优先、专业库按证据增强”。
- 专业库（`TYDSPSystem`）是能力增强选项，不是默认前置依赖。

## 2. 信号/通信建模基础能力

领域核心规范：信号处理建模以“采样、频谱、统计可解释”为基本准则，通信建模以“链路分段、收发一致、同步与误码可验证”为基本准则；二者统一遵循“参数可追溯、约束可检查、结果可复现、证据可审计”的工程规范。

Sysblock 建模约束索引：任务分流与资源路由见第 3 节，参数一致性见第 6 节，结果判定与 KPI 建议见第 10 节。

1. 能力分层知识：
- 基础库承担通用建模骨架：`Sources`、`Sinks`、`SignalRouting`、`SignalAttributes`、`MathOperation`、`LookupTable`、`Continuous`、`Discrete`、`SubSystems`、`ModelVerification`、`Utilities`、`Port`、`Discontinuities`、`LogicAndBitOperation`。
- 专项库承担专业需求场景：`TYDSPSystem`（滤波/频谱/统计）。

2. 信号链路组织知识（可解释拓扑优先）：
- 优先按 `Source -> Processing -> Channel -> Receiver -> Observation` 五段建模。
- 先打通数据流与可观测路径，再叠加算法复杂度，避免“模块堆叠但行为不可解释”。
- 复杂链路按 Tx/Channel/Rx/Monitor 分段封装。

3. 信号路由与数据管理知识：
- 向量/总线组织：`Mux`、`DeMux`、`BusCreator`、`BusSelector`、`Selector`。
- 分支切换：`Switch` / `MultiportSwitch` / `ManualSwitch`。
- 跨层共享：`DataStoreMemory/Read/Write` 或 `Goto/From`。

4. 通信建模核心知识：
- 调制/解调、信道与同步设计应保持收发两端参数一致，并优先保证链路可解释与观测闭环。
- 评测观测应覆盖误码、同步状态与关键波形，确保问题可定位。

5. DSP 建模核心知识：
- 滤波：`DiscreteFIRFilter`、`BiquadFilter`、`FIRInterpolation`。
- 频谱与统计：`SpectrumAnalyzer`、`RMS`、`Mean`、`Variance`、`MovingAverage`。

## 3. 任务说明与建模分流（必须进行）

1. 先做任务分流：
- Sysblock 方框图建模：继续本指南，并遵守 `modeling_rules` 中 Sysblock 路径。
- Modelica 物理建模：切换 `modeling_rules` 走物理建模路径。

2. 指导层挂接顺序（固定）：
- `modeling_rules`（流程层） -> `sysblock-signal-modeling`（指导层） -> `sysblock_model_library`（块级细节）。

3. 资源路由必须显式化：
- 流程规范：`modeling_rules`
- 建模方法：`sysblock-signal-modeling`
- 块参数/端口：`sysblock_model_library`

4. 标准检索模板：

```text
resources_retrieval(action="search", sources=["modeling_rules"], query="<流程约束或建模分流问题>")
resources_retrieval(action="search", sources=["sysblock-signal-modeling"], query="<通用信号处理或通信链路问题>")
resources_retrieval(action="search", sources=["sysblock_model_library"], index_path="resources/indexes/sysblock_model_library_index.json", query="<具体模块名或子库名>")
```

5. 硬约束：块级问题不能只用 `default_sources`。

## 4. 通用建模框架矩阵

| 任务类型 | 推荐架构骨架 | 基础模块优先 | 可选 TY 增强 |
|---|---|---|---|
| 时域信号整形 | 源 -> 增益/求和 -> 延迟/传函 -> 汇 | `Sources` `MathOperation` `Discrete` `Sinks` | `TYDSPSystem` 滤波器模块 |
| 频域特性评估 | 源 -> 滤波/重采样 -> 频谱观测 | `Sources` `Discrete` `SignalAttributes` `Sinks` | `SpectrumAnalyzer` |
| 多速率处理 | 源 -> 插值/抽取 -> 速率过渡 -> 路由 | `SignalAttributes` `SignalRouting` | `FIRInterpolation` |
| 通信基带链路 | 比特源 -> 调制 -> 信道 -> 同步 -> 解调 -> 误码率 | `Sources` `SignalRouting` `ModelVerification` | 同步/信道增强模块按需引入 |
| DSSS 扩频链路 | 信源 -> 调制 -> 扩频 -> 信道 -> 解扩 -> 解调 -> 接收 | `Sources` `LookupTable` `SignalRouting` `MathOperation` | 同步/信道专业模块按需增强 |
## 5. 分层方法（四层说明）

每次方案输出都按四层组织：

1. 拓扑层：源/处理/信道/接收/观测分段。
2. 算法层：各段模块组合与替代策略。
3. 参数层：采样、维度、映射、同步、求解配置。
4. 验证层：结构检查 -> 行为验证 -> 结果取证。

## 6. 实务规则与参数契约

### 6.1 实务规则

- `TYDSPSystem` 当前仅支持 64 位仿真。
- 多数模块不自动识别维度，需要手工设置关键参数。
- 调制映射、相位偏移、采样设置在收发两端必须一致。
- 速率转换节点优先显式放置，避免隐式时序耦合。

### 6.2 参数一致性契约（最小集合）

1. 采样相关：采样率、符号率、每符号采样数、插值/抽取因子。
2. 维度相关：输入维度、索引维度、系数维度。
3. 映射相关：Gray/Binary 映射、相位偏移、判决类型。
4. 仿真相关：起止时间、步长/求解器、关键观测变量。

### 6.3 分层增强策略（L0/L1/L2）

- L0（基础层）：仅使用 Sysblock 基础模块完成最小可验证链路与观测闭环。
- L1（局部增强层）：仅在局部能力不足时引入 TY 模块（例如频谱增强）。
- L2（全链路增强层）：仅在高保真目标明确且 L1 仍不满足 KPI 时启用。

升级触发条件（必须满足其一）：
- KPI 缺口证据：L0/L1 无法达到阈值。
- 能力缺口证据：基础模块无法表达目标机理。

### 6.4 DSSS 参数契约（PG=15/31/63）

- `PG ∈ {15, 31, 63}`，且必须由单模型参数切换链路显式选择。
- PN 长度必须与 PG 一致；Tx/Rx 使用一致 PN 表。
- `CounterLimited` 上限必须满足 `p = PG - 1`，`LookupTable1D` 的轴长度与表长度必须与 PG 一致。
- 同步口径必须明确：S0（理想同步）或 S1（显式同步算法）。
- PG 变更时，源脉冲时序、PN 选择支路与解调后滤波/时间常数必须联动。
- 必须存在对 `PG ∈ {15,31,63}` 的断言或等价约束。
- 信道噪声/窄带干扰参数必须可追溯。

## 7. 能力域索引

- 基础 Sysblock 能力域：信号源、路由组织、算术组合、状态/延迟、查表逻辑、断言与观测。
- 通信增强能力域：调制解调、信道扰动、同步恢复、误码与星座观测。
- DSP 增强能力域：FIR/IIR 滤波、重采样、频谱分析、统计量评估。
- 具体块名、端口与参数细节统一到 `sysblock_model_library` 查询；本节只保留能力域索引，不重复块级目录。

## 8. Playbooks（A/B/C/D/F0/F1）

### 8.0 模板选择器（先选再读）

| 任务特征 | 推荐模板 | 最小验收关注点 |
|---|---|---|
| 基带通信 BER 验证 | A | BER/SER 收敛、误码统计有效 |
| 滤波与频谱一致性评估 | B | 通带/阻带指标、频谱偏移 |
| 快速原型与基础链路验证 | C | 基础信号流可运行且结果可读 |
| 基础骨架 + 通信增强 | D | 通信链路连贯、同步后误码可控 |
| DSSS 单模型切换（基础优先） | F0 | PG切换有效、同步解扩可验证、BER可复读 |
| DSSS 专业增强 | F1 | 在 F0 基础上提升同步/信道真实性与KPI |

### 8.0.1 共用执行规则

- 参数一致性先执行第 6 节契约；模板只补充增量约束。
- KPI 判定口径统一按第 10 节执行。

### 8.1 模板 A：QPSK + AWGN + BER

- 目标：快速建立 Tx -> Channel -> Rx 基带闭环并量化误码。
- 最小链路：`BernoulliBinaryGenerator -> QPSKModulatorBaseband -> AWGNChannel -> QPSKDemodulatorBaseband -> ErrorRateCalculation`。
- 最小 KPI：BER/SER 可读且趋势与噪声设置一致。

### 8.2 模板 B：滤波链路与频谱验证

- 目标：验证滤波器时域/频域效果与重采样策略。
- 最小链路：`SignalSource -> Filter -> (Resample) -> Spectrum/Stats`。
- 最小 KPI：通带/阻带与主峰位置满足预期。

### 8.3 模板 C：通用信号处理模型（基础模块主导）

- 目标：建立不依赖专项库的可运行原型。
- 最小链路：`Sine/Chirp -> Gain/Sum -> Delay/TransferFcn -> Lookup -> RateTransition -> PSD`。
- 最小 KPI：至少一项统计指标可复读。

### 8.4 模板 D：通信链路骨架（基础 + 按需增强）

- 目标：在基础骨架上引入通信专用模块提升真实性。
- 最小 KPI：同步前后指标趋势可解释，BER/SER 改善方向正确。

### 8.5 模板 F0：DSSS 单模型参数切换（基础优先）

适用触发：
- 目标是用基础 Sysblock 构建 DSSS 扩频-解扩通信链路，并在单模型内切换 PG=15/31/63。

固定链路：
1. 信源
2. 调制
3. 扩频（PN 码）
4. 信道（AWGN + 窄带干扰）
5. 同步解扩
6. 解调判决
7. 接收与误差统计

参数契约（最小强约束）：
- `PG ∈ {15, 31, 63}`
- 必须由单一 PG 选择源同时驱动信源、Tx PN、Rx PN、解调后滤波/判决支路
- PN 长度与 PG 一致
- `CounterLimited` 上限满足 `p = PG - 1`
- `LookupTable1D` 的轴长度与表长度与 PG 一致
- Tx/Rx PN 表一致，且同步口径一致（理想同步或显式同步）
- PG 变更时，源脉冲时序与滤波/时间常数联动
- 必须具备 `PG ∈ {15,31,63}` 的 `Assertion` 或等价约束
- 噪声与干扰参数可追溯

推荐基础骨架（抽象）：
- `Constant` / `DiscretePulseGenerator` / `CounterLimited` / `LookupTable1D`
- `Switch` / `Product` / `Sum` / `TransferFcn`
- `CompareToZero` / `RelationalOperator` / `Assertion` / `Outport`

最小观测变量：
- `pgSel`、`srcBit`、`srcSym`、`pnTx`、`spread`、`channel`、`pnRx`、`despread`、`baseband`、`rxBit`、`bitErr`、`berApprox`。
- 具体变量名可随模型实现变化，但上述语义槽位不可缺。

### 8.6 模板 F1：DSSS 专业增强（可选）

适用触发：
- F0 不能满足 KPI 或需要更高真实性（同步环路、更复杂信道、更高阶指标）。

执行原则：
- 仅替换必要子链路，不推翻 F0 基础骨架。
- 不得破坏 F0 中的单选择源绑定、Tx/Rx PN 对称、观测闭环与断言机制。
- 必须记录从 F0 升级到 F1 的证据与收益。

## 9. 通用性增强要求

- 每次建模先做任务归类（整形/滤波/多速率/通信/DSSS 为主类型）。
- 每次交付都给出四层说明（拓扑/算法/参数/验证）。
- 默认先给出 L0 基础方案；仅在存在 KPI 或能力缺口证据时补充 L1/L2 增强方案。

## 10. 结果判定与 KPI 建议

结果判定应围绕关键观测量、断言状态与 KPI 口径展开；执行门禁与交付闭环统一由 `sysblock-signal-modeling-handbook.md` 维护。

### 10.1 建议 KPI 集合

| 模型类型 | KPI 建议 |
|---|---|
| 通用信号处理 | 峰值、RMS、频带能量、稳态误差 |
| 滤波与重采样 | 通带纹波、阻带抑制、频谱偏移 |
| 通信链路 | BER/SER、星座聚类、同步误差 |
| DSSS 扩频链路 | BER 趋势、bitErr 统计稳定性、解扩前后干扰抑制趋势、同步误差可解释性 |

## 11. 常见错误与不适用场景

### 11.1 常见错误

- 只查流程资料或通用资料，漏检 `sysblock_model_library` 中的块级细节。
- 在同一建模循环里混用 Sysblock 与 Modelica 流程。
- 把结构检查通过误判为行为达标或 KPI 达标。
- 收发两端映射、同步口径或采样设置不一致。
- DSSS 场景中 PG、PN 长度、选择器绑定、滤波联动未同步。

### 11.2 不适用场景

- 纯 Modelica 多物理域方程建模。
- 仅 API 文档查询且不涉及信号/通信方案设计。

## 12. 与 sysblock-signal-modeling-handbook.md 的关系

- 本指南：回答“怎么建模”（领域方法层）。
- `sysblock-signal-modeling-handbook.md`：回答“怎么执行交付与审计”（执行层）。
- 若与全局流程文档存在冲突，最终以 `modeling_rules` 为流程准绳；本指南提供领域方法增强。
