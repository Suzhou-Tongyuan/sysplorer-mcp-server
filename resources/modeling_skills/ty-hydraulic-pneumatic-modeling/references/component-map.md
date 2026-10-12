# 组件与库映射

本文件面向 `sysplorer26a` 记录的内置 `TY*` 流体类模型库。权威库范围与版本以 `references/sysplorer26a-builtins.md` 和当前实际连接的 Sysplorer 会话为准。

## 选型顺序

1. 先判断系统级还是元件设计级问题。
2. 再确定是液压、热液压还是气动。
3. 再选择介质库。
4. 最后在 `references/mworks-fluid-library-index.json` 中查精确模型。

## 库优先级

| 任务类型 | 优先库 | 说明 |
|---|---|---|
| 常规液压系统 | `TYHydraulics` | 泵、阀、缸、管路、油箱、传感器等系统级装配优先从这里选 |
| 热液压系统 | `TYThermalHydraulics` | 涉及温度、焓流、热边界、热交换时优先使用 |
| 气动系统 | `TYPneumatics` | 气动回路、气缸、阀、气源、热交换腔等优先使用 |
| 液压元件设计 | `TYHydraulicComponents` | 阀芯、活塞、孔板、泵等元件设计级问题 |
| 热液压元件设计 | `TYThermalHydraulicComponents` | 热液压元件设计级问题 |
| 气动元件设计 | `TYPneumaticComponents` | 气动元件设计级问题 |
| 液压 / 热液压介质 | `TYOilMedia` | 油液牌号和介质选择优先项 |
| 气动介质 | `TYGasMedia` | 气体种类和气体介质选择优先项 |
| 独立热网络补充 | `TYThermals` | 仅当问题外延到独立热网络时补充使用 |
| 介质物性 | `TYMedia` | 用于物性与介质扩展，不作为系统装配主库 |

## 常见对象映射

### 液压泵

| 用户意图 | 推荐模型 | 优先库 | 备注 |
|---|---|---|---|
| 液压泵，未说明变量特性 | `ConstantPump` | `TYHydraulics` | 默认先按定量泵处理，性能依赖时需确认 |
| 双向定量泵 | `BiConstantPump` | `TYHydraulics` |  |
| 双向定量泵，需效率插值 | `BiConstantPumpwithTabulatedEfficiencies` | `TYHydraulics` |  |
| 双向定量泵，考虑流量脉动 | `BiConstantPumpwithFlowRipple` | `TYHydraulics` |  |
| 变量泵 | `VariablePump` | `TYHydraulics` |  |
| 双向变量泵 | `BiVariablePump` | `TYHydraulics` |  |
| 调压泵 | `PressureRegulatedPump` | `TYHydraulics` / `TYThermalHydraulics` |  |
| 离心泵 | `CentrifugalPump` | `TYHydraulics` |  |
| 射流泵 | `EjectorPump` | `TYThermalHydraulics` |  |

### 液压执行器

| 用户意图 | 推荐模型 | 优先库 | 备注 |
|---|---|---|---|
| 双作用非对称液压缸 | `FixDActingSRodCylinder` | `TYHydraulics` |  |
| 双作用非对称液压缸，带质量 | `FixDActingSRodCylinderWithMass` | `TYHydraulics` |  |
| 双作用对称液压缸 | `FixDActingDRodCylinder` | `TYHydraulics` |  |
| 双作用对称液压缸，带质量 | `FixDActingDRodCylinderWithMass` | `TYHydraulics` |  |
| 单作用液压缸 | `FixSActingSRodCylinderWithSpring` | `TYHydraulics` | 需要确认是否弹簧返回 |
| 单作用液压缸，带质量 | `FixSActingSRodCylinderWithMassSpring` | `TYHydraulics` |  |
| 摆缸 | `RotaryActuator` | `TYHydraulics` |  |

### 液压阀

| 用户意图 | 推荐模型 | 优先库 | 备注 |
|---|---|---|---|
| 溢流阀 | `ReliefValve` | `TYHydraulics` / `TYThermalHydraulics` |  |
| 减压阀 | `ReducingValve` | `TYHydraulics` |  |
| 单向阀 | `CheckValve` | `TYHydraulics` |  |
| 液控单向阀 | `PilotedCheckValve` | `TYHydraulics` |  |
| 单向节流阀 | `OrificewithCheckValve` | `TYHydraulics` |  |
| 梭阀 | `ShuttleValve` | `TYHydraulics` |  |
| 双压阀 | `DualValve` | `TYHydraulics` |  |
| 2/2 换向阀 | `DirectionalValve22` | `TYHydraulics` |  |
| 4/2 换向阀 | `DirectionalValve24` | `TYHydraulics` |  |
| 4/3 换向阀，全断中位 | `DirectionalValve34_O` | `TYHydraulics` | 未说明中位机能时必须标 `待确认` |
| 4/3 换向阀，全通中位 | `DirectionalValve34_H` | `TYHydraulics` |  |
| 4/3 换向阀，PT 通中位 | `DirectionalValve34_M` | `TYHydraulics` |  |
| 4/3 换向阀，ABT 通中位 | `DirectionalValve34_Y` | `TYHydraulics` |  |
| 3/6 换向阀 | `DirectionalValve36` | `TYHydraulics` |  |

### 油箱、边界、蓄能器、管路

| 用户意图 | 推荐模型 | 优先库 | 备注 |
|---|---|---|---|
| 油箱 | `Tank` | `TYHydraulics` / `TYThermalHydraulics` |  |
| 压力边界 | `PressureSource` | `TYHydraulics` / `TYThermalHydraulics` / `TYPneumatics` |  |
| 流量边界 | `FlowSource` | `TYHydraulics` |  |
| 质量流焓流边界 | `MHFlowSource` | `TYThermalHydraulics` / `TYPneumatics` |  |
| 温度边界 | `TemperatureSource` | `TYThermalHydraulics` / `TYPneumatics` / `TYThermals` |  |
| 零流量源 | `ZeroFlowSource` | `TYHydraulics` / `TYThermalHydraulics` / `TYPneumatics` |  |
| 弹簧式蓄能器 | `SpringAccumulator` | `TYHydraulics` / `TYThermalHydraulics` |  |
| 气体式蓄能器 | `GasAccumulator` | `TYHydraulics` / `TYThermalHydraulics` |  |
| 过滤器 | `Filter` | `TYHydraulics` / `TYThermalHydraulics` / `TYPneumatics` |  |
| 冷却器 | `Cooler` | `TYHydraulics` / `TYThermalHydraulics` |  |
| 容性管路 | `Pipe_C` | `TYHydraulics` / `TYThermalHydraulics` / `TYPneumatics` |  |
| 阻性管路 | `Pipe_R` | `TYHydraulics` / `TYThermalHydraulics` / `TYPneumatics` |  |
| CR 管路 | `Pipe_CR` | `TYHydraulics` / `TYThermalHydraulics` / `TYPneumatics` |  |

### 气动系统

| 用户意图 | 推荐模型 | 优先库 | 备注 |
|---|---|---|---|
| 节流阀 | `ThrottleValve` | `TYPneumatics` |  |
| 可变节流阀 | `VarThrottleValve` | `TYPneumatics` |  |
| 单向阀 | `CheckValve` | `TYPneumatics` |  |
| 2/2 换向阀 | `DirectionalValve22` | `TYPneumatics` |  |
| 4/2 换向阀 | `DirectionalValve24` | `TYPneumatics` |  |
| 4/3 换向阀 | `DirectionalValve34_*` | `TYPneumatics` | 需结合中位机能确认具体型号 |
| 压气机 | `Compressor` | `TYPneumatics` |  |
| 风扇 | `Fan` | `TYPneumatics` |  |
| 双作用非对称气缸 | `FixDActingAsysmCylinder` | `TYPneumatics` |  |
| 双作用非对称气缸，带质量 | `FixDActingAsymCylinderWithMass` | `TYPneumatics` |  |
| 单作用气缸 | `FixSActingAsysmCylinderWithSpring` | `TYPneumatics` |  |
| 两接口气腔 | `GasVolume2ports` | `TYPneumatics` |  |
| 气瓶 | `GasCylinder` | `TYPneumatics` |  |
| 大气出口 | `Surroundings` | `TYPneumatics` | 排气边界常用项 |

## 图面组织默认模板

- 左侧放压力源、气源与保护支路。
- 中央放主阀、主执行链和主要被控对象。
- 右侧放执行器、负载与输出对象。
- 下侧放回油、回气、油箱和回路总线。
- 上侧放命令源、控制器与反馈链。

## 不允许静默假设的情况

- 4/3 换向阀未说明中位机能。
- 单作用缸未说明是否弹簧返回。
- 泵未说明定量 / 变量，但系统性能依赖该差异。
- 输入已经涉及温度、焓流或热交换，但尚未确认是否切换到 `TYThermalHydraulics`。

## 执行规则

1. 先在 `references/sysplorer26a-builtins.md` 中确认库属于内置范围。
2. 再在 `references/mworks-fluid-library-index.json` 中查精确模型。
3. 输出时优先写英文包名、完整包路径和模型名。
4. 不使用文件系统里发现的副本库、私有库或非 TY 库替代默认交付路径。
