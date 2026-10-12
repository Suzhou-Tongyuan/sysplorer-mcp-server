# TABattery

## 定位

从电芯到模组、整包的电池电学、热学、老化和模板化建模库。

## 目录关键词

- `Template`
- `Interface`
- `Component`
- `CellModel`
- `ModuleModel`
- `PackModel`
- `Utilities`

## 典型层级结构

- `UserGuide`
  用户指南、案例入口和帮助说明
- `Example`
  电池包热应用和充放电相关案例
- `Template`
  `CellTemplate`、`ModuleTemplate`、`PackTemplate` 等模板层
- `Interface`
  电接口、热接口和适配接口
- `Component`
  通用组件和辅助部件
- `CellModel`
  电芯级模型
- `ModuleModel`
  模组级模型
- `PackModel`
  电池包级模型
- `Utilities`
  公共基础模型和辅助工具

## 优先使用场景

- 电芯 / 模组 / 电池包建模
- SOC 与充放电分析
- 电池热管理
- BMS 验证

## 常见辅助库

- `TAThermalSystem`：热回路耦合
- `TAEconomy`：整车工况与能耗框架
- `TAElectronic`：电器和控制附件

## Samples 参考案例

- 官方 Samples 入口：当前 Sysplorer 安装目录下相对路径 `Docs\VehLib\Samples\TABattery`。
- 建模时可参考其中的模型拓扑、接口组织、参数分层和图面排布。
- 这些案例只用于参考，不得直接 `extends` 过来，也不要整套复制后作为正式交付模型。


## 帮助文档入口

- 当当前工具能读取本地文件，且用户 MWorks 文档目录已展开该库时，可在 `%USERPROFILE%\Documents\MWorks` 下查看 `mw_mol\TABattery\TABattery\Resource\Doc`。

## 速查起步

| 任务意图 | 优先入口 | 可优先参考的案例 |
| --- | --- | --- |
| 单体充放电与 SOC 校核 | `Docs\\VehLib\\Samples\\TABattery` | `ChargeCell` |
| 模组级充放电与接口组织 | `Docs\\VehLib\\Samples\\TABattery` | `ChargeModule` |
| 电池包级充放电与 pack 层拓扑 | `Docs\\VehLib\\Samples\\TABattery` | `ChargePack` |
| 电池包热行为与热接口耦合 | `Docs\\VehLib\\Samples\\TABattery` | `ThermalPack` |

## 默认组合方式

- 电池主体层级和模板化建模默认由 `TABattery` 承担
- 做电热耦合时，再补 `TAThermalSystem`
- 做整车工况和能耗闭环时，可由 `TAEconomy` 提供上层工况
- 做低压控制和附件耦合时，再补 `TAElectronic`

## 图面与结构要点

- 保持 `cell -> module -> pack` 层级
- 先在层内建好，再向上一层实例化

## 结果关注点

- 电压
- 电流
- SOC
- 温度
- 单体 / 模组一致性

## 常见风险

- 跳过层级，直接在整包层堆大量单体细节
- 电热职责没分清，导致和 `TAThermalSystem` 边界混乱
- 只接电接口，没有接热接口或总线接口
- 想做整车电池包却误用了单体模板
