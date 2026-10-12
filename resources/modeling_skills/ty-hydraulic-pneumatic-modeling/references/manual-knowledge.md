# 手册增强能力

本文件基于 `references/manual-text/` 下同步后的 8 份 Markdown 手册整理，用于增强 `ty-hydraulic-pneumatic-modeling` skill 在“库介绍、如何使用、注意事项、示例参考、依赖排查”方面的稳定回答能力。

使用原则：

- 只总结手册中可稳定验证的信息，不编造手册原句。
- 优先回答“库定位 + 推荐入口 + 依赖 + 典型示例 + 注意事项”。
- 如果需要原文细节，继续搜索 `references/manual-text/*.md`。

## 来源 Markdown

- `附录A-10 液压模型库V2.4.0产品用户手册-C.md`
- `附录A-10 液压元件设计模型库V2.5.0产品用户手册-C.md`
- `附录A-10 热液压模型库V1.3.0产品用户手册-C.md`
- `附录A-10 热液压元件设计模型库V1.5.0产品用户手册-C.md`
- `附录A-10 气动模型库V2.1.0产品用户手册-C.md`
- `附录A-10 气动元件设计模型库V2.3.0产品用户手册-C.md`
- `附录A-10 热模型库V1.1.0产品用户手册-C.md`
- `附录A-10 热流介质库V1.4.0产品用户手册-C.md`

## Skill 应具备的增强能力

1. 当用户询问“模型库介绍”时，给出库定位、主要包结构、适用场景和典型示例。
2. 当用户询问“如何使用”时，优先引导到 `UsersGuide`、`ExampleEntryGuide`、典型示例和快速入门章节。
3. 当用户询问“为什么跑不起来”时，优先排查 `Modelica 4.0.0.TY.1`、介质库版本、接口类型和加载环境。
4. 当用户做系统级自动建模时，说明应优先使用系统库，不要误拿元件设计库直接替代整机装配库。
5. 当用户做元件级自动建模或二次开发时，说明应优先从 `UsersGuide.Template`、接口库和基础模板出发。

## 共性知识

### 1. 手册结构高度一致

8 份手册大多包含以下章节：

- 模型库介绍
- 使用环境
- 使用须知
- 使用说明
- 快速入门
- 二次开发说明
- 典型应用案例
- 注意事项

因此 skill 在回答时可以优先按这几个维度组织输出。

### 2. 通用推荐入口

手册中稳定出现的推荐入口：

- `UsersGuide`
- `ExampleEntryGuide`
- 快速入门
- 典型应用案例
- 二次开发说明中的 `UsersGuide.Template`

建议回答优先级：

1. 用户想了解库做什么：先说库定位和包结构，再引导 `UsersGuide`
2. 用户想快速上手：先引导 `ExampleEntryGuide`、快速入门和典型案例
3. 用户想做二次开发：先引导 `UsersGuide.Template` 和接口库

### 3. 运行环境与版本依赖

手册中可稳定识别到的环境信息：

- 平台涉及 `MWORKS.Sysplorer`
- 在线方式涉及 `MoHub / Sysplorer Online`
- 架构涉及 `x64`、`arm64`
- 操作系统涉及 `Windows 7/10/11`、`CentOS 7.9`、`Ubuntu 18.04`、银河麒麟桌面系统 V10、统信
- 标准库版本反复出现 `Modelica 4.0.0.TY.1`

技能侧的默认排查顺序：

1. 当前 Sysplorer / MWORKS 版本和许可证是否正常
2. `Modelica 4.0.0.TY.1` 是否已加载
3. 是否加载了正确的介质库
4. 接口类型和模板是否匹配
5. 是否把元件设计库误当成系统库使用

### 4. 介质库依赖规则

- `TYHydraulics` 依赖 `TYOilMedia 2.3.0`
- `TYHydraulicComponents` 依赖 `TYOilMedia 2.3.0`
- `TYThermalHydraulics` 依赖 `TYOilMedia 2.3.0`
- `TYThermalHydraulicComponents` 依赖 `TYOilMedia 2.3.0`
- `TYPneumatics` 依赖 `TYGasMedia`，手册中也出现 `TYGasMedia 2.0.2`
- `TYPneumaticComponents` 依赖 `TYGasMedia 2.0.2`
- `TYThermals` 主要强调标准库适配，不以流体介质库为主
- `TYMedia` 主要提供物性与介质模型，不是系统装配库

因此：

- 液压 / 热液压问题优先提醒检查 `TYOilMedia`
- 气动问题优先提醒检查 `TYGasMedia`
- 热流物性问题优先指向 `TYMedia`

### 5. 接口与模板规则

元件设计库和系统库手册里稳定出现以下接口 / 模板：

- 液压系统库接口：`FluidPort_a`、`FluidPort_b`
- 热液压系统库接口：`FluidPort_a`、`FluidPort_b`
- 气动系统库接口：`GasPort_A`、`GasPort_B`、`TwoPortsComponent`
- 液压元件设计库接口：`FluidPort_A`、`FluidPort_B`、`FluidPortV_A`、`FluidPortV_B`
- 热液压元件设计库接口：`FluidPort_A`、`FluidPort_B`、`FluidPortV_A`、`FluidPortV_B`
- 气动元件设计库接口：`GasPort_A`、`GasPort_B`、`GasPortV_A`、`GasPortV_B`
- 热模型库接口：`HeatPort_a`、`HeatPort_b`
- 二次开发入口：`UsersGuide.Template`

技能使用规则：

- 做二次开发时优先选择手册给出的模板，不从零定义接口
- 接口名称大小写和库内命名风格要保持一致
- 若手册出现 `V` 版本端口，说明其与体积变量或容腔计算相关，不能随意与普通接口混接

### 6. 关键开关参数

手册中反复出现的关键配置项：

- `InterfaceSwitch`
- `InterfaceSwitchA`
- `InterfaceSwitchB`
- `useHeatPort`

技能使用规则：

- 这些参数默认视为关键参数
- 不清楚边界条件时不要随意改值
- 如果模型连线方式与容腔是否保留有关，要明确说明为何开启或关闭

### 7. 常见单位和工程习惯

手册中稳定出现的显示单位和工程表达：

- `mm`
- `ml`
- `l/min`
- `bar`

技能生成参数表时应：

- 优先沿用手册中常见工程单位
- 必要时同时给出 SI 单位和工程单位
- 不要混用单位却不说明换算关系

## 分库摘要

### 液压模型库 `TYHydraulics` V2.4.0

库定位：

- 通用液压系统模型库
- 适合系统级搭建、液压回路装配、典型液压功能验证

主要包结构：

- `Valves`
- `Actuators`
- `Pipes`
- `Resistances`
- `Pumps`
- `Auxiliaries`
- `Sources`
- `Sensors`
- `Interfaces`
- `UsersGuide`
- `ExampleEntryGuide`

典型示例：

- `HydraulicServoControlSystem`
- `PressureRegulator`
- `HydrostaticTransmission`
- `BalanceLoop`
- `VenturiTube`
- `LubricatingSystem`
- `FourCylinderEngineLubricationCircuit`

Skill 规则：

- 做常规液压系统自动建模时优先选本库
- 先从系统级块装配，不要一上来拆成阀芯级和活塞级组件
- 默认提醒依赖 `TYOilMedia 2.3.0`

### 液压元件设计模型库 `TYHydraulicComponents` V2.5.0

库定位：

- 液压元件设计级模型库
- 适合阀芯、活塞、孔板、泵等机理级或细粒度建模

主要包结构：

- `Pistons`
- `SlideValveSpool`
- `ConicalValveSpool`
- `BallValveSpool`
- `NozzleFlapper`
- `DiaphragmLeakageSealings`
- `PistonPump`
- `Auxiliaries`
- `Sources`
- `Sensors`
- `Interfaces`
- `UsersGuide`
- `ExampleEntryGuide`

典型示例：

- `HydraulicJack`
- `ThreeWayValve`
- `FlowLimiter`
- `PistonPump`
- `OilFeedingSystem`

Skill 规则：

- 更适合元件级设计，不直接替代系统库装配整机
- 需要二次开发时优先看 `TYHydraulicComponents.UsersGuide.Template`
- 重点检查 `FluidPort_*`、`FluidPortV_*` 和 `InterfaceSwitch`
- 默认提醒依赖 `TYOilMedia 2.3.0`

### 热液压模型库 `TYThermalHydraulics` V1.3.0

库定位：

- 热液压系统模型库
- 适合同时关注压力、流量、温度、换热和热边界的系统问题

主要包结构：

- `Valves`
- `Actuators`
- `Pipes`
- `Resistances`
- `Pumps`
- `Auxiliaries`
- `Sources`
- `Sensors`
- `HeatExchangers`
- `Interfaces`
- `UsersGuide`
- `ExampleEntryGuide`

典型示例：

- `HydraulicServoControlSystem`
- `PressureRegulator`
- `HydrostaticTransmission`
- `InjectionCircuit`
- `VenturiTube`
- `LubricatingSystem`
- `FourCylinderEngineLubricationCircuit`

Skill 规则：

- 只要问题中出现温度、焓流、热交换、热边界，就优先切换到本库
- 若模型中出现换热管、热容、油液温升，不要退回普通液压库
- 关注 `HeatExchangers` 和 `useHeatPort`
- 默认提醒依赖 `TYOilMedia 2.3.0`

### 热液压元件设计模型库 `TYThermalHydraulicComponents` V1.5.0

库定位：

- 热液压元件设计级模型库
- 适合喷油器、热液压阀芯、泵和热耦合液压元件设计

主要包结构：

- `Pistons`
- `SlideValveSpool`
- `ConicalValveSpool`
- `BallValveSpool`
- `NozzleFlapper`
- `DiaphragmLeakageSealings`
- `PistonPump`
- `Auxiliaries`
- `Sources`
- `Sensors`
- `Interfaces`
- `UsersGuide`
- `ExampleEntryGuide`

典型示例：

- `HighPressureFuelInjector`
- `PressureRegulator`
- `PistonPump`
- `InjectionCircuit`

Skill 规则：

- 适用于温度和液压性能共同起作用的元件级问题
- 需要额外关注 `InterfaceSwitchA`、`InterfaceSwitchB`、热边界和温度相关参数
- 默认提醒依赖 `TYOilMedia 2.3.0`

### 气动模型库 `TYPneumatics` V2.1.0

库定位：

- 通用气动系统模型库
- 适合气动回路、执行机构、热交换室和整机气动系统分析

主要包结构：

- `Valves`
- `Actuators`
- `Pipes`
- `HeatExchangers`
- `Auxiliaries`
- `Sources`
- `Sensors`
- `Interfaces`
- `UsersGuide`
- `ExampleEntryGuide`

典型示例：

- `GasProperties`
- `PneumaticCircuit`
- `HeatExchangeChamber`
- `PneumaticJack`
- `SimExhaustStack`
- `Start_system_of_CNC_machining_center`
- `Pneumatic_suspension`

Skill 规则：

- 做气动系统建模时优先选本库
- 重点检查 `GasPort` 接口和是否遗漏气体介质库
- 若问题涉及可压缩效应或气动换热，优先检查 `HeatExchangers`
- 默认提醒依赖 `TYGasMedia` / `TYGasMedia 2.0.2`

### 气动元件设计模型库 `TYPneumaticComponents` V2.3.0

库定位：

- 气动元件设计级模型库
- 适合阀芯、腔室、喷嘴、隔膜和密封泄漏等细粒度气动建模

主要包结构：

- `Pistons`
- `SlideValveSpool`
- `ConicalValveSpool`
- `BallValveSpool`
- `NozzleFlapper`
- `DiaphragmLeakageSealings`
- `PistonPump`
- `Auxiliaries`
- `Sources`
- `Sensors`
- `Interfaces`
- `UsersGuide`
- `ExampleEntryGuide`
- `Examples`

典型示例：

- `DirectionalValve33`
- `AdiabaticChamber`
- `AirPistol`
- `PneumaticJack`
- `CheckValve`
- `PressureRegulation`
- `ABSElectromagneticValve`
- `RelayValve`

Skill 规则：

- 更适合元件级设计，不直接替代系统库装配整机
- 优先检查 `GasPort_*`、`GasPortV_*`、`TwoFlangesOnePortV`、`partialFlanges`
- 对 `InterfaceSwitch` 的设置必须说明原因
- 默认提醒依赖 `TYGasMedia 2.0.2`

### 热模型库 `TYThermals` V1.1.0

库定位：

- 通用热模型库
- 适合独立热网络、导热、对流、辐射、热管理和湿空气问题

主要包结构：

- `Materials`
- `HeatCapacities`
- `HeatTransfers`
- `HeatExchangers`
- `Moistairs`
- `Sources`
- `Sensors`
- `Interfaces`
- `UsersGuide`
- `ExampleEntryGuide`

典型示例：

- `LinearConduction`
- `ComparisonConduction`
- `SolidCooling`
- `ThermalManagementSystem`
- `ThermalConcatenation`

Skill 规则：

- 当液压 / 气动问题外延到独立热网络时，用本库补充热学建模
- 需要热接口时优先检查 `HeatPort_a`、`HeatPort_b`
- 可在解释热学机理时引用手册中的 `Nu`、`Pr`、`Fij` 等概念，但不要脱离具体模型块

### 热流介质库 `TYMedia` V1.4.0

库定位：

- 热流介质和物性模型库
- 适合介质选型、热物性调用和物性扩展，不是系统级装配库

主要内容：

- `Helmholtz`
- `CoolProp`
- `Incomprssible`
- `Solid`
- `UsersGuide`
- `ExampleEntryGuide`
- `Interfaces`

Skill 规则：

- 用户问“介质如何选”“物性如何接入”“CoolProp 怎么用”时优先引用本库
- 该库侧重物性，不应拿来替代液压、热液压或气动系统库
- 与 `Modelica.Media.Interfaces.PartialMedium`、`TYMedia.Interfaces.ExtendedPartialTwoPhaseMedium` 相关的问题可优先从这里解释

## 回答规则

1. 如果用户问“这个库怎么用”，先回答：库定位、入口包、典型示例、依赖和注意事项。
2. 如果用户问“这个模型该放哪个库”，先判断是系统级还是元件设计级，再给出推荐库。
3. 如果用户问“为什么编译不过 / 跑不起来”，优先检查：许可证、Sysplorer 版本、`Modelica 4.0.0.TY.1`、介质库版本、接口类型、关键开关参数。
4. 如果用户问“有没有官方示例”，优先从各库“典型应用案例”章节列出的示例中推荐。
5. 如果用户问“怎么做二次开发”，优先引导到 `UsersGuide.Template`、接口库和手册中的开发示例。
6. 如果手册提取文本不完整，不要编造手册原句；只输出稳定可验证的总结，并可继续搜索 `references/manual-text/*.md`。
