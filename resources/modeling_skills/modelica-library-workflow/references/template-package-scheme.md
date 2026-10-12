# TY 模板包结构方案

## 适用边界与权威

本文件集中维护采用 `TYComponentsTemplate` 或明确选定同类骨架时的专属结构约定。固定公共层、接口本地包装、包展示顺序、中文名和 `Basics` 约定仅在该前提下适用；通用 Modelica 项目无需为了本模板迁移兼容原生接口、增建空包或重命名现有类。其他清单只引用/核对本方案，不另定义一套模板要求。

Examples / Tests 的文件与运行深度由 `executor-base.md` 和 `acceptance-checklist.md` 按请求决定。骨架中的位置不意味着需要生成可运行模型或启动 Sysplorer。`within` 与文件组织沿用父级规则，不在此另立通用建模约束。

## 顶层结构

沿 `TYComponentsTemplate.mo` 组织时，优先保留以下顶层并列结构：

```text
<LibraryName>
  UsersGuide
  Examples
  <BusinessPackage1>
  <BusinessPackage2>
  ...
  Sensors
  Sources
  Interfaces
  Utilities
  Tests
```

目录式 package 交付时，需同步写顶层 `package.order`，按上述顺序显式列出各子包；不要依赖工具默认字母序。仅含 `package.mo` 的叶子包可不单独维护 `package.order`。

## 正式包名替换

不要将以下占位名称直接用于正式库：

- `Components1`
- `Components2`

顶层库命名补充要求：

- 不要与 Sysplorer 中已有商业库重名。
- 不要以 `TY` 开头，避免与商业库命名风格混淆。

应按领域改成正式业务包名，例如液压库可用：

```text
Pumps
Valves
Actuators
Resistances
```

气动库可用：

```text
AirSources
Valves
Actuators
AirTreatment
Resistances
```

## `Basics` 放置规则

- 各业务包内部复用的基础模型放 `<BusinessPackage>.Basics`
- `Basics` 的中文显示名默认写为“基础模型库”
- 跨全库复用的基础内容不要放业务包，改放 `Interfaces` 或 `Utilities`

## 顶层功能包中文显示名

- 顶层功能包的中文显示名默认按“XX库”命名。
- 推荐写法：
  - `Examples` -> “典型示例”
  - `Pumps` -> “泵库”
  - `Valves` -> “阀库”
  - `Actuators` -> “执行机构库”
  - `Interfaces` -> “接口库”
  - `Sources` -> “边界库”
  - `Sensors` -> “传感器库”
  - `Utilities` -> “公用库”
- 不再使用“接口层”“公用层”“边界源”这类同层级命名混杂的中文显示名。

示例：

```text
Valves
  Basics
  PressureControl
  FlowControl
  DirectionalControl

Resistances
  Basics
  Orifices
  Junctions
  PipeLines
```

目录式业务包同样要补 `package.order`，并优先写成：

```text
Basics
<ConcreteModel1>
<ConcreteModel2>
...
```

## `Interfaces` 推荐子包

```text
Interfaces
  HydraulicsInterfaces
    HydraulicPort
    HydraulicPort_a
    HydraulicPort_b
    PartialHydraulicOnePort
    PartialHydraulicTwoPort
    PartialHydraulicTwoPortTransport
    PartialHydraulicFourPort
  MechanicsInterfaces
  FluidInterfaces
  HeatInterfaces
  ElectricalInterfaces
```

只在确有该领域需求时保留对应子包；不要为了对齐模板而保留空洞分层或把当前组件根本用不到的接口预先移植进库。

若 `Interfaces` 采用目录式 package，推荐同步维护：

```text
HydraulicsInterfaces
MechanicsInterfaces
FluidInterfaces
HeatInterfaces
ElectricalInterfaces
```

并在各子包自己的 `package.order` 中先列通用接口，再列方向型接口，最后列 partial 基类。

补充约束：

- `Interfaces` 中的 partial 基类默认不绘制自定义图标，优先只保留 connector 位置、方向和文档；其中文显示名优先写为“基类模型”，不要写成“基础模型”。
- 具体图标优先放到可实例化模型或业务包中的基类、具体元件上。
- 机械、流体、热、电气接口优先复用标准库 `Modelica` 中已有接口，并通过本地别名或本地包装类移植到自有 `Interfaces` 子包中，但“只移植当前组件实际会使用到的接口”应按接口族理解，不要只迁一个孤立的 `_b` 或 `_a`。
- 组件实现时默认只使用当前模型库 `Interfaces` 下的接口，不直接在组件类中声明或引用标准库原生接口；若确实需要标准库接口，先移植到本库 `Interfaces` 后再使用。
- 当标准库接口存在无图标通用基接口与 `_a` / `_b` 变体时，优先把通用基接口一起移植到本地子包中；若当前组件已涉及该接口族的双向连接语义，默认把 `_a` / `_b` 一起补齐。若希望图标与标准库完全一致，则本地 `_a` / `_b` 直接继承标准库对应接口模型。
- 例如机械直线平动接口若本库已使用 `Flange_b`，则本地 `MechanicsInterfaces` 至少同步具备对应的通用 `LinearFlange`、`LinearFlange_a`、`LinearFlange_b`，不要只保留一个 `LinearFlange_b`。
- 自定义接口与本地移植接口默认补 `defaultComponentName`，确保在 Sysplorer 中实例化时能得到稳定默认名称；通用接口优先使用通用名，方向型接口优先使用 `xxx_a` / `xxx_b`。
- 自建且带图标的方向型接口，默认在图标层补 `Text(..., textString = "%name")`，保证入口/出口等接口实例化后名称可见。
- 若标准库中没有对应接口，例如当前液压体积流量接口，则在 `HydraulicsInterfaces` 中新建。
- 本地接口类名不要与标准库已有接口重名；优先使用领域前缀或语义前缀区分，例如 `HydraulicPort`、`FluidMediumPort_a`、`ThermalHeatPort_a`、`AnalogPin_p`。
- 自定义接口库优先参考 `Modelica` 标准接口库的组织方式；若采用液压一维端口架构，可进一步参考 `Modelica.Fluid.Interfaces` 的组织方式：
  - `HydraulicPort` 用于类型继承或确有必要的双向抽象，不作为生成组件的默认声明接口
  - `HydraulicPort_a` 表示入口，`HydraulicPort_b` 表示出口
  - 单接口基类默认声明 `HydraulicPort_a`
  - `PartialHydraulicTwoPort` 默认流向为 `port_a -> port_b`
  - `PartialHydraulicTwoPortTransport` 适用于阀、简单泵、节流件等不显式建内部储能状态的元件
- 可实例化模型若需要在图标层展示名称，优先使用 `%name`，不把 `Pump`、`Tank`、`Valve` 这类写死文字长期放在实例标签位置。
- 创建组件时，对外接口应以 connector 实例形式显式落在组件中，并补齐 `Placement(...)` 与 `iconTransformation(...)`，保证图形层可见。

## `Utilities` 推荐子包

```text
Utilities
  Icons
  Types
  Functions
  Constants
  SIunits
  Tables
```

其中：

- `Icons` 放领域图标，如 `HydCommon`、`PneCommon`
- `Types` 放类型、枚举、记录
- `Functions` 放通用函数；组件内的局部函数若具备复用价值，默认迁到这里
- `Constants` 放领域常数
- `SIunits` 放显示单位和扩展量纲
- `Tables` 放查表数据

补充建议：

- 函数数量较少时，可直接放在 `Utilities.Functions` 下。
- 函数数量变多后，按主题继续拆子包，例如：

```text
Functions
  Flow
  Thermal
  Control
  Smoothing
```

- 不把多个组件共用的函数长期内嵌在单个元件类内部。
- 目录式 `Utilities` 包建议同步写 `package.order`，默认顺序为 `Icons`、`Types`、`Functions`、`Constants`、`SIunits`、`Tables`。

## 液压库参考方案

```text
TYHydraulicComponents
  UsersGuide
  Examples
  Pumps
    Basics
  Valves
    Basics
  Actuators
    Basics
  Resistances
    Basics
  Sensors
  Sources
  Interfaces
  Utilities
    Icons
      HydCommon
    Types
    Functions
    Constants
    SIunits
    Tables
  Tests
```

## 中文化要求

- 用户可见的字符串默认使用中文，包括类显示名、参数说明、文档 HTML、版本说明、示例说明、测试说明。
- 包名、类名、变量名是否保留英文标识符，按兼容性与项目约束决定；默认优先保留标识符不动，只把显示文本中文化。
- 若用户明确要求“参数改成中文”，优先修改参数后的说明字符串，而不是直接修改变量名。

## 采用模板时的第一阶段结构建议

按本轮范围从以下项目选取；骨架任务可保留入口结构，真实运行仅在请求时执行：

1. `Utilities`
2. `Interfaces`
3. `Sources`
4. `Sensors`
5. `Resistances.Basics` 或第一个业务包的 `Basics`
6. 一个 `Examples` 样例
7. 一个 `Tests` 验证模型
