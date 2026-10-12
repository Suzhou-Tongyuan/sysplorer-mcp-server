# TAEconomy

## 定位

整车动力性、经济性、续航、驾驶循环和车型架构分析的主框架库。

## 目录关键词

- `VehicleArchitectures`
- `Vehicle`
- `PowerSystem`
- `Driveline`
- `Drivers`
- `Electronic`
- `Controller`
- `SignalBus`
- `Utilities`

## 典型层级结构

- `UserGuide`
  用户指南、案例入口和使用说明
- `Examples`
  传统燃油、混动、纯电、增程等典型整车案例
- `VehicleArchitectures`
  各类整车架构模板
- `Vehicle`
  整车主体和系统集成相关模型
- `PowerSystem`
  动力源与能量转换相关模型
- `Driveline`
  传动与驱动链相关模型
- `Drivers`
  驾驶员与循环工况相关模型
- `Electronic`
  附件和电子负载相关模型
- `Controller` / `SignalBus` / `Utilities`
  控制、总线和公共基础模型

## 优先使用场景

- `0-100`
- 最高车速
- 爬坡
- 驾驶循环
- 能耗和续航
- 车型架构对比

## 常见辅助库

- `TAEngine`：发动机高保真细化
- `TABattery`：电池包或热状态细化
- `TAElectronic`：低压负载和附件功耗
- `TAThermalSystem`：热管理子框架

## Samples 参考案例

- 官方 Samples 入口：当前 Sysplorer 安装目录下相对路径 `Docs\VehLib\Samples\TAEconomy`，包含 `EV`、`Hybrid`、`Conventional` 等整车案例。
- 建模时可参考其中的整车拼接方式、能量链组织、工况接入方式和图面排布。
- 这些案例只用于参考，不得直接 `extends` 过来，也不要整套复制后作为正式交付模型。

## 帮助文档入口

- 当当前工具能读取本地文件，且用户 MWorks 文档目录已展开该库时，可在 `%USERPROFILE%\Documents\MWorks` 下查看 `mw_mol\TAEconomy\TAEconomy\Resources\doc`。

## 速查起步

| 任务意图 | 优先入口 | 可优先参考的案例 |
| --- | --- | --- |
| 纯电 `0-100`、最高车速、爬坡、循环工况 | `Docs\\VehLib\\Samples\\TAEconomy\\EV` | `EV_0_100`、`EV_Max_Speed_30min`、`EV_Climbing`、`EV_Cycle` |
| 双电机 / 四驱纯电性能与能耗 | `Docs\\VehLib\\Samples\\TAEconomy\\EV` | `DualEAuto_0_100`、`DualEAuto_Cycle`、`ERVExample\\DAWD` |
| 增程车型动力性、巡航、制动、循环 | `Docs\\VehLib\\Samples\\TAEconomy\\EV` | `EREVEAuto_0_100`、`EREVEAuto_Cruising`、`EREVEAuto_Brake`、`EREVEAuto_Cycle` |
| 混动架构对比 | `Docs\\VehLib\\Samples\\TAEconomy\\Hybrid` | `P0_0_100`、`P1_Cycle`、`P2_Cycle`、`P3_0_100`、`P4_Cycle`、`SPHEV_Cycle` |
| 传统燃油车 `0-100`、最高车速、制动、循环 | `Docs\\VehLib\\Samples\\TAEconomy\\Conventional` | `CVT_0_100`、`CVT_Cycle`、`DCT_0_100`、`DCT_MaxVelocity`、`DCT_Brake` |
| 采用动力学库车身 | `Docs\\VehLib\\Samples\\TAEconomy\\EV` | `DualEAutoMultiBody`、`EAutoWithMultiBody` |

## 默认组合方式

- 整车骨架默认由 `TAEconomy` 承担
- 发动机高保真细化补 `TAEngine`
- 电池包或热状态细化补 `TABattery`
- 低压负载和附件功耗补 `TAElectronic`
- 若涉及整车热管理，再补 `TAThermalSystem`
- 支持经济性架构集成动力学库车身模型，动力学库车身模型中参数UseTAEconomyInput设置为true可以和经济性架构连接

## 图面与结构要点

- 顶层按中轴结构布置
- 驾驶员通常放最左侧
- 驱动链、制动链、信号链尽量分开

## 结果关注点

- 车速
- 里程
- 油耗 / 电耗
- SOC
- 驱动功率

## 常见风险

- 一开始就把过多高保真子系统全补进来，导致结构过重
- 把动力学目标误路由到 `TAEconomy`
- 驾驶员 / 循环工况没有真正驱动车辆
- 主动力链、传动链和制动链没有闭合
