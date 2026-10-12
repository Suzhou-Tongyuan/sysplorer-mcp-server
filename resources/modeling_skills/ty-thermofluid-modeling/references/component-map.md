# 组件映射

本文件用于把典型热流体与空气处理场景映射为优先组件族和连接关注点。

## 系统级映射

| 场景 | 优先库 | 推荐组件族 | 连接关注点 |
| --- | --- | --- | --- |
| 液体单相主回路 | `TYThermoFluidSys` | `Boundaries`、`Machines`、`Pipelines`、`Valves`、`Volumes`、`HeatExchangers`、`Sensors` | 优先开环；检查边界、泵阀、管段、负载段与出口边界顺序 |
| 乙二醇/丙二醇冷却回路 | `TYThermoFluidSys` + `TYMedia` 或 `Modelica.Media` | `Boundaries`、`Machines`、`Pipelines`、`HeatExchangers`、`Sensors` | 先确认浓度定义，再检查连续回路介质一致性 |
| 蒸汽/两相热流体回路 | `TYThermoFluidSys` + `TYMedia` | `HeatExchangers`、`Machines`、`Volumes`、`Sensors` | 先确认相变与介质，再锁定换热器和汽轮机类组件 |
| 空气处理与通风主链路 | `TYAirTreatmentAndVentilation` | `Sources`、`CompressorsAndFans`、`AirTreatment`、`Pipes`、`HeatExchangers`、`Sensors` | 先确认混合气体成分，再连接处理段与传感器 |
| 湿空气处理、除湿、增湿 | `TYAirTreatmentAndVentilation` + 混合气体介质 | `AirTreatment`、湿度相关传感器 | 介质中必须包含水蒸气 |
| `CO2` 控制或净化 | `TYAirTreatmentAndVentilation` + 混合气体介质 | `AirTreatment`、`Sensors` | 介质中必须包含 `CO2` |
| 空气侧-液体侧耦合换热 | 联合使用两个专业库 | 空气侧组件 + 液体侧组件 + 换热接口 | 先分别完成两侧在本次请求范围内的校核，再在接口处耦合；文件/check-only 任务不增加仿真 |

## 组件族选择规则

### `TYThermoFluidSys`

- 泵、汽轮机、主管段、阀门、容积、热边界、传感器，优先从 `TYThermoFluidSys` 选择。
- 需要体现沿程分布、压降和换热分布时，优先在 `Pipelines` 中选离散管道。
- 只需要极简骨架或占位验证时，才优先退回集总管道。

### `TYAirTreatmentAndVentilation`

- 风机、压缩机、空气处理段、气体管路、湿度和 `CO2` 处理，优先从本库选择。
- 涉及空气品质控制时，优先把传感器与处理器件一并纳入设计。

## 传感器优先放置位置

| 观测目标 | 推荐位置 |
| --- | --- |
| 入口压力/温度/流量 | 入口边界后、第一段主体组件前 |
| 主管段压降 | 受热段或测试段上下游各放一个压力测点 |
| 换热效果 | 换热器两侧入口和出口 |
| 风机或压缩机效果 | 设备前后各放压力或流量测点 |
| 湿度、焓值、`CO2` | 空气处理段出口或控制对象附近 |

## 默认模板对应关系

| 模板 | 适用场景 |
| --- | --- |
| `templates/scenarios/single-phase-liquid-open-loop.md` | 液体单相主回路 |
| `templates/scenarios/single-phase-liquid-open-loop.md` | 乙二醇或丙二醇冷却回路 |
| `templates/scenarios/air-treatment-open-loop.md` | 空气处理开环主链路 |
| `templates/scenarios/coupled-heat-exchange.md` | 空气侧与液体侧耦合换热 |
