# 跨领域分流与库名版本表

本文件集中维护父级分流所需的库边界、规范名称和版本说明。库名和分流关系来自当前技能库已有信息；版本列用于人工审核，已有版本只作为待确认线索，缺少版本时统一标记为“待人工审核补充”，不得据此猜测或固定运行时版本。

## 1. 判定优先级

1. 保留用户显式指定或上下文已确认有效的库、包、实现边界。本轮未重复库名不重置选择；显式仅标准库的要求不能被默认策略覆盖。
2. 未指定库时，按功能、接口和验收条件评估 Modelica 标准库。足够则使用标准库；有公开证据确认的缺口时保留标准库可用部分，用商业组件补足，形成标准库＋商业库组合。文档未找到、查询失败、类名错误或加载失败都不是功能不足的证据。
3. 商业组件选定后加载其领域 Skill；不能因用户未说商业库名而拒绝已确认的商业补充。场景词只产生候选；仅在缺失信息实质改变方案时澄清。纯标准/自建机械任务不加载 TY 商业机械 Skill；车辆既有覆盖、入口和实现路径不因本次规则调整而改变。
4. 确认项目总库集合及各子系统责任域，只选择一个主领域并按真实组件边界追加支持域。领域白名单仅约束负责的子系统，不能删除其他已选域或保留的标准库组件；无关 uses 依赖不能独自决定主域。
5. 标准库＋商业库共存仍属于 Modelica，不自动触发混合建模。仅组织库结构、公共接口、Examples/Tests、本地化或库级治理时追加库工作流，普通模型或单个测试台不自动进入建库流程。电气与 NPS 专项路由维持原样；其专项冲突单独记录，不借共享规则重写排除项。

### Modelica 版本适用范围

- 车辆 Skill 的全部既有路径（包括标准库/自建车辆）以及商业库路径（包括标准库＋商业库组合）固定 `Modelica 4.0.0.TY.1`。
- 仅单独使用本主规则、且实际任务不涉及车辆/商业库路径时，默认 `4.0.0.TY.1`，允许用户明确要求或工程有效版本信息覆盖并记录来源。其他附加 Skill 组合不能自动套用此例外。
- 已有工程版本与固定版本约束冲突时报告未满足状态；不得静默重写 uses、删去商业组件或少加载 Skill 来绕过约束。MCP 的 latest/依赖解析结果不是版本政策。
- 下表商业库名称/版本线索不代替运行时清单；本节固定的是适用路径的 Modelica 标准库依赖，不臆造商业库自身版本。

## 2. 高交叉领域判定

| 输入特征 | 判定规则 |
|---|---|
| 光伏、风电、储能、综合能源 | 明确 TY 能源库或其四类中文库名时使用 `ty-energy-modeling`；明确 `NPSLibrary` 时使用 `ty-nps-library-modeling`；未指定时先评估标准库；有明确缺口时保留标准库并补充适用 TY 能源组件。NPS 的显式专项路由保持原样。 |
| 逆变器、电机驱动、电力电子 | 明确 `TYMotor`、`TYElectricPower` 或 `TYElectrical` 时使用 `ty-electrical-machine-power-modeling`；明确 `NPSLibrary` 时使用 `ty-nps-library-modeling`；均未指定且商业边界会改变实现时询问一次。 |
| 热液压、换热、HVAC | 明确 `TYThermalHydraulics` 或 `TYThermalHydraulicComponents` 时使用 `ty-hydraulic-pneumatic-modeling`；明确 `TYMedia`、`TYThermoFluidSys` 或 `TYAirTreatmentAndVentilation` 时使用 `ty-thermofluid-modeling`；未指定时先评估标准库，按功能缺口与接口证据补充对应商业组件，记录主域和支持域。 |
| 机械、多体、传动、接触、柔性体 | 用户或父规则已选择相应 TY 商业机械组件时使用 `ty-mechanical-modeling`；纯 Modelica 标准库或自建任务留在父级。 |
| Sysblock 滤波、频谱、通信、BER、调制或同步 | 使用 `ty-sysblock-signal-modeling`。 |
| Sysblock 纯框图、状态机、布局、子系统或普通控制拓扑 | 使用 `ty-sysblock-diagram-modeling`。 |

## 3. 规范库名、别名与版本

| 领域 | 规范库名或现有别名 | 主 Skill |
|---|---|---|
| Modelica 标准库 | `Modelica 4.0.0.TY.1` | `ty-sysplorer-modeling-rules` |
| NPS 电力系统 | `NPSLibrary`；简称 NPS | `ty-nps-library-modeling` |
| TY 电气/电机/电子 | `TYMotor`、`TYElectricPower`、`TYElectrical` | `ty-electrical-machine-power-modeling` |
| TY 能源 | 光伏发电库、风力发电库、电池库、综合能源系统库 | `ty-energy-modeling` |
| TY 液压/气动 | `TYOilMedia`、`TYHydraulics`、`TYHydraulicComponents`、`TYThermalHydraulics`、`TYThermalHydraulicComponents`、`TYGasMedia`、`TYPneumatics`、`TYPneumaticComponents`、`TYThermals` | `ty-hydraulic-pneumatic-modeling` |
| TY 机械 | `TYDriveline`、`TYFlexBody`、`TYContact`、`TYMechanics`、`TYMultibody`、`TYDriveline3D`、`TYMechanics2D` | `ty-mechanical-modeling` |
| TY 热流体/HVAC | `TYMedia`、`TYThermoFluidSys`、`TYAirTreatmentAndVentilation` | `ty-thermofluid-modeling` |
| TA 车辆 | `TAEconomy`、`TADynamics`、`TAThermalSystem`、`TAEngine`、`TABattery`、`TAElectronic` | `ta-vehicle-modeling` |
| Sysblock | `SysplorerEmbeddedCoder` | `ty-sysblock-diagram-modeling` |
| Sysblock 信号/通信 | `TYDSPSystem`、`TYCommunication`、`TYMixedSignal` | `ty-sysblock-signal-modeling` |
