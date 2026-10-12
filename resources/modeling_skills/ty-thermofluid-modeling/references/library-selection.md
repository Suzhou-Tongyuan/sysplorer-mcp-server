# 库选择指南

本文件仅在用户/父规则/有效上下文已选 TY 热流体组件后补充选型。未指定库时先由父规则评估标准库能力：满足则标准库，不足则保留可用标准库并补充商业组件，不因首次文档或工具失败认定功能不足。库边界只约束负责的子系统，保留项目已选标准库和支持领域组件。

## 目录

- `依赖与版本边界`：确认库之间的依赖关系和版本注意事项。
- `库可用性预检`：在正式建模前确认首选库当前可用。
- `选哪个库`：按主要物理域选择优先库。
- `联合使用两个库`：处理空气侧与液体侧耦合或跨域系统。
- `选择判断表`：按任务类型快速落到推荐库。
- `首选库与实际交付库不一致时`：定义回退后的说明要求。

## 依赖与版本边界

- `TYThermoFluidSys` 手册给出的依赖是 `Modelica 4.0.0.TY.1` 和 `TYMedia V1.4.0`。
- `TYAirTreatmentAndVentilation` 手册给出的依赖是 `Modelica 4.0.0.TY.1` 和 `TYMedia V1.4.0`。
- `TYMedia` 手册给出的依赖是 `Modelica 4.0.0.TY.1`。
- 商业库路径的 Modelica 固定为 `4.0.0.TY.1`；记录实际装载版本并核对，若工程指定其他版本则报告冲突，不因环境存在新版或 latest 能力自动替换。商业库自身版本与依赖按官方证据核对。
- 若生成的是“系统模型库”，而不是单次验证模型，需把这些依赖落实到顶层 `package.mo` 的 `annotation(uses(...))` 中，而不是只依赖当前会话已加载状态。

## 库可用性预检

- 仅在本次授权运行构建范围内，放大模型前完成适用预检；离线/只读任务不因此增加会话。预检不超过请求终态，仍按父 shared-standards 处理自动布局写回边界。
- 预检至少包括：
  - 目标库可加载。
  - 依赖库可加载。
  - 同领域最小代表模型可 `check`。
  - 若任务涉及仿真，最小代表模型可完成一次短时 `translate` 和 `simulate`。
- 预检失败时，先进入 `references/fallback-strategy.md` 的回退判定，不要直接以全量正式模型继续试错。

## 选哪个库

### 优先选 `TYThermoFluidSys`

适合以下任务：

- 水、蒸汽、制冷剂、一般热流体回路建模
- 管网、阀门、容器、三通、弯头、泵、汽轮机、换热器、热组件建模
- 热流体系统的压力、流量、温度、换热、机械能与流体能量耦合分析

该库的主要分类包括：

- `Pipelines`
- `Valves`
- `Volumes`
- `Junctions`
- `Machines`
- `HeatExchangers`
- `Thermals`
- `Blocks`
- `Sources`
- `Sensors`
- `Interfaces`

### 优先选 `TYAirTreatmentAndVentilation`

适合以下任务：

- 空调、送风、排风、通风、空气品质控制系统
- 风机、压缩机、气体管路、湿度处理、CO2 处理、空气换热建模
- 建筑暖通、舱室环控、氧气供给、空气净化、除湿、增湿任务

该库的主要分类包括：

- `Valves`
- `Pipes`
- `CompressorsAndFans`
- `AirTreatment`
- `HeatExchangers`
- `Controllers`
- `Auxiliaries`
- `Sources`
- `Sensors`
- `Interfaces`
- `Media`

## 联合使用两个库

以下场景可以联合使用：

- 空气侧与液体侧通过换热器耦合
- 通风系统中存在制冷剂回路或热流体二次回路
- 暖通主系统属于空气处理，但某些二次侧更适合用热流体库描述

联合建模时注意：

- 优先在各自擅长的物理域内选组件。
- 耦合点先确认接口和介质类型是否兼容。
- 不要因为一个系统含空气和液体，就强行全部放进同一个库里。

## 选择判断表

| 任务类型 | 优先库 | 说明 |
| --- | --- | --- |
| 蒸汽动力循环、水箱系统、二次回路系统 | `TYThermoFluidSys` | 属于典型热流体系统 |
| 空调系统、通风系统、除湿系统、氧气供给系统 | `TYAirTreatmentAndVentilation` | 属于典型空气处理与通风系统 |
| 泵、汽轮机、流体管道、容积、热组件 | `TYThermoFluidSys` | 设备与接口更贴合热流体回路 |
| 风机、压缩机、增湿器、干燥器、CO2 净化器 | `TYAirTreatmentAndVentilation` | 组件直接面向空气处理任务 |
| 介质物性本身 | `TYMedia` 或 `Modelica.Media` | 不是主系统库，但必须作为介质来源 |

## 首选库与实际交付库不一致时

- 若最终交付使用的不是首选库，必须通过回退策略显式说明。
- 对于只求“得到可运行模型”的基础验证场景，可评估以 `Modelica.Fluid` 作为热流体系统的替代。
- 对于明确要求专用库特性、专用设备、专用离散方式或专用介质能力的任务，不应静默回退，应明确报告阻塞。

## 来源

- `references/manuals/thermofluid-library-manual.md`
- `references/manuals/air-treatment-library-manual.md`
- `references/manuals/media-library-manual.md`
