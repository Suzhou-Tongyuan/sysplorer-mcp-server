# 建模方法总览

## 用途

本文件用于承载通用方法层内容，包括能力分层、链路组织原则、通用建模骨架以及四层说明框架。

## 能力分层

### 基础能力域

- `Sources`、`Sinks`
- `SignalRouting`
- `SignalAttributes`
- `MathOperation`
- `LookupTable`
- `Continuous`
- `Discrete`
- `SubSystems`
- `ModelVerification`
- `Utilities`
- `Port`
- `Discontinuities`
- `LogicAndBitOperation`

### 增强能力域

- `TYDSPSystem`
  主要承担滤波、频谱与统计增强

## 链路组织原则

- 优先按 `Source -> Processing -> Channel -> Receiver -> Observation` 组织链路
- 先建立可观测闭环，再增加复杂度
- 复杂链路按 Tx / Channel / Rx / Monitor 分段封装
- 避免只堆模块、不保留关键观测与断言

## 通用建模框架矩阵

| 任务类型 | 推荐架构骨架 | 基础模块优先 | 可选增强 |
|---|---|---|---|
| 时域信号整形 | 源 -> 增益/求和 -> 延迟/传函 -> 汇 | `Sources` `MathOperation` `Discrete` `Sinks` | `TYDSPSystem` 滤波器模块 |
| 频域特性评估 | 源 -> 滤波/重采样 -> 频谱观测 | `Sources` `Discrete` `SignalAttributes` `Sinks` | `SpectrumAnalyzer` |
| 多速率处理 | 源 -> 插值/抽取 -> 速率过渡 -> 路由 | `SignalAttributes` `SignalRouting` | `FIRInterpolation` |
| 通信基带链路 | 比特源 -> 调制 -> 信道 -> 同步 -> 解调 -> 误码率 | `Sources` `SignalRouting` `ModelVerification` | 同步/信道增强模块按需引入 |
| DSSS 扩频链路 | 信源 -> 调制 -> 扩频 -> 信道 -> 解扩 -> 解调 -> 接收 | `Sources` `LookupTable` `SignalRouting` `MathOperation` | 同步/信道增强模块按需引入 |

## 四层说明框架

1. 拓扑层：源、处理、信道、接收、观测如何分段
2. 算法层：各段采用什么模块组合与替代策略
3. 参数层：采样、维度、映射、同步、求解配置
4. 验证层：结构检查、行为验证、结果取证

## 通用增强原则

- 默认先给出基础方案
- 仅在存在能力缺口或 KPI 缺口证据时再升级
- 不要在没有证据的情况下直接跳到增强层方案
