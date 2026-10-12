# TAEngine

## 定位

发动机本体、进排气、增压、供油、冷却和热相关模型库。

## 目录关键词

- `Interface`
- `EngineModel`
- `Component`
- `Utilities`

## 典型层级结构

- `UserGuide`
  用户指南、案例入口和帮助说明
- `Example`
  发动机均值模型、增压和典型发动机系统案例
- `EngineModel`
  发动机本体和整机级模型
- `Component`
  进气、排气、供油、增压、冷却等部件
- `Interface`
  二次开发和系统集成接口
- `Utilities`
  公共基础组件和辅助模型

## 优先使用场景

- 发动机性能仿真
- 进排气系统分析
- 增压与供油细化
- 发动机热管理
- 为整车模型补高保真发动机

## 常见辅助库

- `TAEconomy`：整车驱动与工况框架
- `TAThermalSystem`：热管理回路耦合

## Samples 参考案例

- 官方 Samples 入口：当前 Sysplorer 安装目录下相对路径 `Docs\VehLib\Samples\TAEngine`。
- 建模时可参考其中的进排气结构、控制接口、热流体连接和图面排布。
- 这些案例只用于参考，不得直接 `extends` 过来，也不要整套复制后作为正式交付模型。


## 帮助文档入口

- 当当前工具能读取本地文件，且用户 MWorks 文档目录已展开该库时，可在 `%USERPROFILE%\Documents\MWorks` 下查看 `mw_mol\TAEngine\TAEngine\Resource\Doc`。

## 速查起步

| 任务意图 | 优先入口 | 可优先参考的案例 |
| --- | --- | --- |
| 发动机均值模型、整机级快速搭模 | `Docs\\VehLib\\Samples\\TAEngine` | `MVEM` |
| 带涡轮 / 增压的均值模型 | `Docs\\VehLib\\Samples\\TAEngine` | `MVEMTurbine` |
| 进气增压、压力充气、进排气边界分析 | `Docs\\VehLib\\Samples\\TAEngine` | `PressureCharge` |

## 默认组合方式

- 单独做发动机本体和进排气分析时，以 `TAEngine` 为主
- 做整车动力性/经济性细化时，由 `TAEconomy` 提供整车工况
- 做发动机热管理耦合时，再补 `TAThermalSystem`

## 图面与结构要点

- 先分清空气、燃油、热和机械连接边界
- 热管理耦合时，不把热回路直接混到发动机内部层次之外

## 结果关注点

- 转速
- 扭矩
- 进排气状态
- 燃油消耗
- 热负荷

## 常见风险

- 把热管理职责全部塞进发动机主模型
- 为了排障临时切断关键物理链后忘记回退
- 进气、排气、供油或冷却边界没有闭合
- 发动机模型与外部控制器或整车模板接口不匹配
