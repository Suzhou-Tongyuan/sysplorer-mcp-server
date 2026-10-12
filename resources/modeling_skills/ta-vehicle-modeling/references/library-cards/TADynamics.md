# TADynamics

## 定位

整车与子系统动力学、底盘、操稳、平顺性、K&C 和道路工况分析主库。

## 目录关键词

- `车身`
- `悬架`
- `转向`
- `轮胎`
- `制动`
- `传动`
- `动力`
- `道路`
- `驾驶员`

## 典型层级结构

- `UserGuide`
  用户指南、案例入口和使用说明
- `Example`
  多体悬架、KC 悬架及典型操稳/平顺性工况案例
- `车身`
  集成车身、多体车身等主体模型
- `悬架`
  麦弗逊、双叉臂、多连杆和 KC 悬架相关模型
- `轮胎`
  轮胎和轮端相关模型
- `转向` / `制动` / `动力`
  转向、制动和驱动相关子系统
- `道路` / `驾驶员`
  工况和驾驶输入模型
- `控制系统`
  ABS、TCS、助力等控制相关模型

## 优先使用场景

- 悬架
- K&C
- 操稳
- 平顺性
- 转向
- 制动
- 双移线、阶跃转向、蛇形等工况

## 常见辅助库

- `TAEconomy`：当驱动或传动细化必须影响动力学响应时再补

## Samples 参考案例

- 官方 Samples 入口：当前 Sysplorer 安装目录下相对路径 `Docs\VehLib\Samples\TADynamics`。
- 建模时可参考其中的车辆骨架、子系统拼接方式、接口组织和图面排布。
- 轮胎相关案例可优先看 `TADynamics.Vehicle.Wheels.Example`：
  `Wheel2Test`、`Wheel2Test2`、`Wheel2Test3`、`Wheel4Test`、`WheelExternalExample`、`Wheel6Test`
- 转向相关案例可优先看 `TADynamics.Vehicle.Steering.Example`：
  `TierodTest2`、`TierodTest3`
- 闭环驾驶员与典型工况案例可优先看 `TADynamics.Drivers.CloseloopDrivers.Examples`：
  `DoublelaneChange`、`Circles`、`CirCles2`、`DoublelaneChange14DOF`、`SlalomCase`、`SlalomCaseWithCones`、`LinearCase`、`LinearCase2`
- 这些案例只用于参考，不得直接 `extends` 过来，也不要整套复制后作为正式交付模型。


## 帮助文档入口

- 当当前工具能读取本地文件，且用户 MWorks 文档目录已展开该库时，可在 `%USERPROFILE%\Documents\MWorks` 下查看 `mw_mol\TADynamics\TADynamics\Resource\Doc`。

## 速查起步

| 任务意图 | 优先骨架 / 入口 | 可优先参考的案例 |
| --- | --- | --- |
| 四驱 KC 整车动力学、实时整车、先做可检查/可翻译模型 | `Vehicle.Chassis.RealTime2AxlesCar` + `Vehicle.Driveline.PowerTrain.MotorSource.WheelHubMotor4` | `KCVehiclerealtime`、`KCVehicleBenchmark` |
| 阶跃转向、蛇形、双移线等开环工况 | `Drivers.OpenLoopDriver.SteerControl` + `Experiment.SteerSource.*` | `StepSteer`、`StepSteer2`、`DoubleChangeLane` |
| KC 悬架查表、K&C 对标 | `Vehicle.Suspension.FrontSuspension.FSModel.TableBased`、`Vehicle.Suspension.RearSuspension.RSModel.TableBased` | `KCVehicleBenchmark`、`KCVehicleSuspControl` |
| 集总参数转向 / 实时转向 | `Vehicle.Steering.EPS.SteeringSystem2`、`Vehicle.Steering.EPS.RealTimeSteering` | `Vehicle.Steering.Example` 下 `TierodTest2`、`TierodTest3` |
| 轮胎单体、四轮或多轮测试 | `Vehicle.Wheels.Example` | `Wheel2Test`、`Wheel4Test`、`Wheel6Test` |
| 闭环驾驶员与典型操稳工况 | `Drivers.CloseloopDrivers.Examples` | `DoublelaneChange`、`SlalomCase`、`LinearCase` |

## 默认组合方式

- 整车运动学 / 动力学主框架默认由 `TADynamics` 承担
- 只有当驱动或传动细化必须影响动力学响应时，才补 `TAEconomy` 相关动力传动部分
- 用户未指定车身类型时，默认 `KC / 集成车身`

## 图面与结构要点

- 未指定车身类型时默认 `KC / 集成车身`
- 高度集成布局通常从左到右放驾驶员、驱动、整车、制动
- 分散布局时四轮围绕车身按真实位置排布

## 结果关注点

- 横摆角速度
- 侧偏
- 纵横向加速度
- 悬架位移
- 轮胎力

## 常见风险

- 把四轮压成抽象串行结构
- 明明是操稳任务却过早引入大量经济性组件
- 转向、悬架、轮胎、道路与车身接口未对齐
- 把局部子系统案例当整车直接交付
