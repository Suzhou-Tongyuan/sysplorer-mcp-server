# 模板与专题方案

## 用途

本文件用于承载 A/B/C/D/F0/F1 模板的适用条件、目标、最小链路和最小关注点。
本文件默认前置条件是：已在 `template-selector.md` 中完成模板选择；本文件不重复承担模板筛选职责。

## 与 `template-selector.md` 的关系

- `template-selector.md` 负责“选哪个模板”
- 当前文件负责“选定后如何展开”
- 若模板尚未确定，应先回到 `template-selector.md`

## 模板总表

| 模板 | 适用任务 | 最小关注点 |
|---|---|---|
| `A` | 基带通信 BER 验证 | BER/SER 收敛、误码统计有效 |
| `B` | 滤波与频谱一致性评估 | 通带/阻带指标、频谱偏移 |
| `C` | 快速原型与基础链路验证 | 基础信号流可运行且结果可读 |
| `D` | 基础骨架 + 通信增强 | 通信链路连贯、同步后误码可控 |
| `F0` | DSSS 单模型切换 | PG 切换有效、同步解扩可验证、BER 可复读 |
| `F1` | DSSS 专业增强 | 在 F0 基础上提升同步/信道真实性与 KPI |

## 模板 A：QPSK + AWGN + BER

- 目标：快速建立 Tx -> Channel -> Rx 基带闭环并量化误码
- 最小链路：`BernoulliBinaryGenerator -> QPSKModulatorBaseband -> AWGNChannel -> QPSKDemodulatorBaseband -> ErrorRateCalculation`
- 最小关注点：BER/SER 可读且趋势与噪声设置一致

## 模板 B：滤波链路与频谱验证

- 目标：验证滤波器时域/频域效果与重采样策略
- 最小链路：`SignalSource -> Filter -> (Resample) -> Spectrum/Stats`
- 最小关注点：通带/阻带与主峰位置满足预期

## 模板 C：通用信号处理原型

- 目标：建立不依赖专项库的可运行原型
- 最小链路：`Sine/Chirp -> Gain/Sum -> Delay/TransferFcn -> Lookup -> RateTransition -> PSD`
- 最小关注点：至少一项统计指标可复读

## 模板 D：通信链路骨架

- 目标：在基础骨架上引入增强模块，提高链路真实性
- 最小关注点：同步前后指标趋势可解释，BER/SER 改善方向正确

## 模板 F0：DSSS 单模型参数切换

适用条件：

- 目标是用基础 Sysblock 构建 DSSS 扩频-解扩链路
- 要求在单模型内切换 `PG=15/31/63`

固定链路：

1. 信源
2. 调制
3. 扩频
4. 信道
5. 同步解扩
6. 解调判决
7. 接收与误差统计

最小强约束：

- `PG ∈ {15,31,63}`
- 单一 PG 选择源同时驱动信源、Tx PN、Rx PN 与相关支路
- PN 长度与 PG 一致
- `CounterLimited` 与 `LookupTable1D` 维度匹配
- Tx/Rx PN 对称
- 至少保留 `bitErr` 与 `berApprox` 等关键观测语义槽位

## 模板 F1：DSSS 专业增强

适用条件：

- F0 无法满足 KPI
- 需要更高真实性，例如同步环路或更复杂信道

执行原则：

- 仅替换必要子链路
- 不推翻 F0 的单选择源绑定、Tx/Rx 对称、观测闭环与断言机制
- 必须记录从 F0 升级到 F1 的证据与收益
