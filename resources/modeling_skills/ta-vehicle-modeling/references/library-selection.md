# 库选择

本文件只负责 TA 六库主库选择、辅助库边界和联合建模收范围。自然语言任务分类先看 `requirement-map.md`。

## 主库判定

| 用户目标 | 主库 | 常见辅助库 | 下一步读取 |
|---|---|---|---|
| 动力性、经济性、续航、驾驶循环、车型架构 | `TAEconomy` | `TAEngine`、`TABattery`、`TAElectronic` | `library-cards/TAEconomy.md` |
| 悬架、K&C、操稳、平顺性、转向、制动、道路工况、实时化动力学 | `TADynamics` | `TAEconomy` | `library-cards/TADynamics.md` |
| 整车热管理、热泵空调、制冷剂回路、水冷回路、热舒适、热耗能 | `TAThermalSystem` | `TABattery`、`TAEngine`、`TAElectronic`、`TAEconomy`、`TADynamics` | `library-cards/TAThermalSystem.md` |
| 发动机本体、进排气、增压、供油、发动机冷却 | `TAEngine` | `TAEconomy`、`TAThermalSystem` | `library-cards/TAEngine.md` |
| 电芯、模组、电池包、BMS、电池热管理 | `TABattery` | `TAThermalSystem`、`TAEconomy`、`TAElectronic` | `library-cards/TABattery.md` |
| 低压电器、DCDC、电子负载、车身电器、热管理附件 | `TAElectronic` | `TAEconomy`、`TABattery`、`TAThermalSystem` | `library-cards/TAElectronic.md` |
| 整车联合建模 | 先判主分析目标，再选一库为主 | 其余库只做局部细化 | `combination-rules.md` |

## 主框架与局部细化边界

- `TAEconomy`：整车纵向性能、能耗、续航和架构模板主框架；不作为整车操稳/悬架主框架。
- `TADynamics`：整车/底盘动力学主框架；不作为能耗/续航主框架。
- `TAThermalSystem`：整车热管理回路、HVAC、制冷剂/冷却液网络主框架。
- `TAEngine`：发动机本体、进排气、供油、增压和发动机热相关细化；默认不作为整车主框架。
- `TABattery`：cell/module/pack 层级和电热耦合细化；默认不作为整车主框架。
- `TAElectronic`：低压网络、DCDC、附件和电器负载；通常作为整车附件细化库。

## 不要误路由

- 电池热管理：电池内部层级和电热耦合优先 `TABattery`；整车冷却回路与热网络优先 `TAThermalSystem`。
- 发动机热管理：发动机本体和冷却侧细化优先 `TAEngine`；整车热回路和换热网络优先 `TAThermalSystem`。
- 热管理附件：压缩机、鼓风机、PTC、除霜器等附件本体优先 `TAElectronic`；附件所处热回路仍由 `TAThermalSystem` 承担主框架。
- 整车联合模型：先决定性能、动力学还是热管理为主，再选 `TAEconomy`、`TADynamics` 或 `TAThermalSystem` 之一做骨架。

## 不能静默假设

以下情况要么问一个澄清问题，要么在回复中说明推断依据：

- 用户同时提到热管理和操稳，但未说明主目标。
- 用户要整车模型，但没说明燃油、纯电、混动还是增程。
- 用户要热管理，但没说明电池热、发动机热、舱内热还是综合热管理。
- 用户要动力学分析，但没说明整车操稳、平顺性、K&C，还是转向/制动子系统。
- 用户说“整车联合模型”，但没说是否要求真实 Sysplorer 落地。
