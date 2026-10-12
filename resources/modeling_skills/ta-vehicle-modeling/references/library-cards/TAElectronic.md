# TAElectronic

## 定位

整车低压电子电器、附件系统和相关热管理附件模型库。

## 目录关键词

- `Electronic`
- `Loads`
- `Accessories`
- `Converters`
- `Utilities`

## 典型层级结构

- `UserGuide`
  用户指南、案例入口和帮助说明
- `Example`
  低压负载示例和整车电平衡案例
- `座舱域`
  鼓风机、座椅、玻璃升降等座舱相关电器
- `车身域`
  灯光、雨刮、门把手等车身电器
- `底盘域`
  底盘相关电器与执行件
- `动力域`
  燃油泵、起动机等动力域附件
- `Converters` / `Loads`
  DCDC、母线、通用负载和电气连接件
- `Utilities`
  公共基础模型和辅助组件

## 优先使用场景

- 低压电网
- DCDC
- 车身电器
- 电子负载
- 热管理附件功耗

## 常见辅助库

- `TAEconomy`：整车运行工况
- `TABattery`：供电侧细化
- `TAThermalSystem`：附件热负载耦合

## Samples 参考案例

- 官方 Samples 入口：当前 Sysplorer 安装目录下相对路径 `Docs\VehLib\Samples\TAElectronic`，包含 `System` 和 `Component` 等案例目录。
- 建模时可参考其中的负载组织、电气接口连接、控制信号接入方式和图面排布。
- 这些案例只用于参考，不得直接 `extends` 过来，也不要整套复制后作为正式交付模型。


## 帮助文档入口

- 当当前工具能读取本地文件，且用户 MWorks 文档目录已展开该库时，可在 `%USERPROFILE%\Documents\MWorks` 下查看 `mw_mol\TAElectronic\TAElectronic\Resource\Doc`。

## 速查起步

| 任务意图 | 优先入口 | 可优先参考的案例 |
| --- | --- | --- |
| 低压母线、DCDC、电网基础闭合 | `Docs\\VehLib\\Samples\\TAElectronic\\System` | `ElecNetwork`、`ElecNetworkComplex` |
| 工况驱动下的整车低压网络 | `Docs\\VehLib\\Samples\\TAElectronic\\System` | `ECE15` |
| 热管理附件功耗：鼓风机、除霜、风机类负载 | `Docs\\VehLib\\Samples\\TAElectronic\\Component` | `BlowerDemo`、`DefrosterDemo` |
| 车身/座舱电器：灯光、车窗、座椅、雨刮 | `Docs\\VehLib\\Samples\\TAElectronic\\Component` | `LampDemo`、`LedDemo`、`LifterDemo`、`SeatSystemDemo`、`WiperDemo` |
| 动力域附件：燃油泵、喷油、电动助力 | `Docs\\VehLib\\Samples\\TAElectronic\\Component` | `FuelPumpDemo`、`InjectionDemo`、`EPSDemo` |

## 默认组合方式

- 低压网络、DCDC 和附件功耗默认由 `TAElectronic` 承担
- 若需要整车运行工况，通常由 `TAEconomy` 提供
- 若需要热负载进入热管理网络，再补 `TAThermalSystem`
- 若供电侧需要更细电池结构，再补 `TABattery`

## 图面与结构要点

- 公共供电点通常放下方
- 负载向供电点汇接
- 功率路径和控制信号路径尽量分开

## 结果关注点

- 电压母线
- 负载电流
- 功耗
- 附件工作状态

## 常见风险

- 把热管理附件误当作整车热管理主框架
- 负载连接无层次，图面上形成杂乱扇出
- 低压电源、DCDC、母线和负载没有真正闭合
- 热管理附件选了无热接口版本，热量没有进入热网络
