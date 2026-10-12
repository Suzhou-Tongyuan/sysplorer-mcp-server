# TAThermalSystem

## 定位

整车热管理、热泵空调、制冷剂回路、水冷回路、换热网络和舱内热舒适主框架库。

## 目录关键词

- `HeatExchangers`
- `Pipes`
- `PumpAndFan`
- `Compressor`
- `Valves`
- `Sources`
- `Interfaces`
- `Sensors`
- `Utilities`

## 典型层级结构

- `UserGuide`
  用户指南、案例入口和帮助说明
- `Examples`
  乘员舱、热泵、电机冷却、电池冷却和多回路热管理案例
- `HeatExchangers`
  蒸发器、冷凝器、板换、冷却器等换热器
- `Pipes`
  水路、制冷剂和管道相关模型
- `PumpAndFan`
  泵、风机和流量驱动件
- `Compressor` / `Valves`
  压缩机、阀门和节流相关模型
- `Heating` / `Sources` / `Reservoirs`
  加热、热源、边界和储液相关模型
- `Interfaces` / `Sensors` / `Utilities`
  系统连接接口、传感器和公共基础模型

## 优先使用场景

- 整车热管理
- 热泵空调
- 制冷剂回路
- 水冷回路
- 乘员舱热舒适
- 多热源热耦合

## 常见辅助库

- `TABattery`：电池电热耦合细化
- `TAEngine`：发动机热源与冷却
- `TAElectronic`：压缩机、鼓风机、PTC 等附件
- `TAEconomy` 或 `TADynamics`：车辆工况来源

## Samples 参考案例

- 官方 Samples 入口：当前 Sysplorer 安装目录下相对路径 `Docs\VehLib\Samples\TAThermalSystem`，包含 `System`、`Component`、`Application` 等案例目录。
- 建模时可参考其中的回路分区、热流体连接关系、附件组织和图面排布。
- 这些案例只用于参考，不得直接 `extends` 过来，也不要整套复制后作为正式交付模型。


## 帮助文档入口

- 当当前工具能读取本地文件，且用户 MWorks 文档目录已展开该库时，可在 `%USERPROFILE%\Documents\MWorks` 下查看 `mw_mol\TAThermalSystem\TAThermalSystem\Resource\Doc`。

## 速查起步

| 任务意图 | 优先入口 | 可优先参考的案例 |
| --- | --- | --- |
| 乘员舱热舒适、舱内换热网络 | `Docs\\VehLib\\Samples\\TAThermalSystem\\System` | `CabinDemoSimple`、`CarCabinDemo`、`CabinHeatExchangeNetwork` |
| 热泵空调、制冷剂回路 | `Docs\\VehLib\\Samples\\TAThermalSystem\\System` | `HeatPumpCircuit`、`HeatPumpCircuitR290`、`ACR290`、`RefrigerantLoop_IHX` |
| 电机 / 电池 / HVAC 综合热管理 | `Docs\\VehLib\\Samples\\TAThermalSystem\\System` | `MotorCool`、`MotorplsBattPlsHVAC`、`MotorplsBattPlsHVACparallel`、`MotorplsBattPlsHVACseries` |
| HIL / 多回路热管理骨架 | `Docs\\VehLib\\Samples\\TAThermalSystem\\System` | `SingleLoopHIL`、`MultiLoopHIL` |
| 水路、管路、泵风机、阀门等部件级验证 | `Docs\\VehLib\\Samples\\TAThermalSystem\\Component` | `BatteryCool`、`R134aPipeDemo`、`CoolingPump`、`CoolingFan`、`CoolingValveDemo`、`TXVDemo`、`OctoValveCase` |

## 默认组合方式

- 整车热管理骨架默认由 `TAThermalSystem` 承担
- 电池电热细化补 `TABattery`
- 发动机热源和冷却补 `TAEngine`
- 压缩机、鼓风机、PTC 等附件补 `TAElectronic`
- 车辆工况通常由 `TAEconomy` 或 `TADynamics` 提供

## 图面与结构要点

- 先分清热源、热汇、热回路和工况来源
- 热路径、信号链和附件功率路径分开布置

## 结果关注点

- 温度
- 流量
- 压降
- 换热量
- 压缩机功耗
- 舱内舒适指标

## 常见风险

- 没先判清主热回路就开始拼组件
- 工况来源和热管理本体职责混在一起
- 只放局部换热器或附件，没有形成完整热回路
- 水冷、空气、制冷剂回路边界混用或方向错误
