# 跨专业业务包生成策略

## 目的

当模型库领域不是液压模板中的典型场景，或者属于电气、热、机械、气动、控制、跨域耦合等其他专业时，不再依赖“为每个专业单独硬编码一套包名模板”，而是通过统一骨架加角色分类的方式稳定生成业务包结构。

本文只解决一类问题：

- 如何在不同专业下确定 `<BusinessPackage1>`、`<BusinessPackage2>` 等正式业务包
- 如何避免把所有具体组件都堆进 `Basics`
- 如何在新领域或混合领域中保持结构稳定

本文不重复顶层骨架、接口归口、图面规则和交付口径；这些仍分别以 `template-package-scheme.md`、`executor-base.md`、`workflow-checklist.md` 和 `input-output-contract.md` 为准。

## 核心原则

### 1. 采用同一模板时骨架一致，业务包按角色变化

已采用 TY 模板时顶层结构参考如下；其他项目沿用现有兼容骨架，本文件只辅助需要的业务包分层：

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

变化的不是顶层骨架，而是“业务包如何切分”。

### 2. 先按组件职责分角色，再映射成业务包名

不要先问“这个领域是不是一定要有 `Resistors` / `Capacitors` / `Inductors`”；先问每个组件承担什么职责：

- 储能类
- 阻性/耗散类
- 传输/连接类
- 转换/执行类
- 源类
- 传感/测量类
- 控制/调节类
- 边界/环境类

然后再把这些角色映射为专业包名。

### 3. `Basics` 只放业务包内部复用基础内容

`Basics` 的职责始终不变：

- 放本业务包内部复用的 partial、基类、局部公共函数、局部记录或枚举
- 不放整个模型库的所有具体组件
- 不用来替代业务包分层

若具体组件已经具备稳定的角色语义，应优先进入对应业务包，而不是继续堆在 `Basics` 中。

### 4. 跨包复用内容仍归口到 `Interfaces` 或 `Utilities`

采用上述模板时，以下内容不因专业变化而改变归位；模板外保留项目既有兼容接口及分层：

- connector、端口基类、接口族：归 `Interfaces`
- 类型、常数、跨多个组件复用的函数、图标、查表数据：归 `Utilities`
- 边界件：归 `Sources`
- 传感器：归 `Sensors`

## 生成步骤

### 步骤 1：识别领域画像

先识别当前库属于：

- 单一领域：液压、气动、热、机械、电气、控制等
- 混合领域：如机电、热液压、电液控制、气电控制等

若是混合领域，进一步识别主领域与辅领域。

输出至少包括：

- 主领域
- 次领域
- 是否需要跨域耦合包

### 步骤 2：为组件打角色标签

对计划生成或已存在的组件，按以下维度做角色判断：

1. 端口/connector 语义
2. 端口数量与方向
3. 是否包含储能状态
4. 是否承担边界、测量、控制、执行、连接、转换等职责
5. 是否主要服务于某一个组件族

推荐的判别信号：

- 单端口边界件，优先考虑 `Sources`
- 传感输出件，优先考虑 `Sensors`
- 两端口传输、阻性或分配件，优先考虑阻性类、连接类或阀/管路类
- 含显著储能状态的件，优先考虑储能类业务包
- 负责把一种能量域映射为另一种能量域的件，优先考虑转换/执行类

### 步骤 3：按角色形成候选业务包

将角色聚合为候选业务包，而不是直接把组件名当包名列表。

示例角色到候选包：

```text
储能类         -> EnergyStorage / Capacitors / Inductors / ThermalCapacitances
阻性/耗散类    -> Resistances / Resistors / Frictions / Orifices
传输/连接类    -> PipeLines / Junctions / Connectors / GearTrains
转换/执行类    -> Actuators / Motors / Pumps / Transformers
控制/调节类    -> Controllers / Regulators / Valves
```

### 步骤 4：应用专业命名映射

当候选业务包形成后，再套用专业命名。

#### 电气领域示例

```text
阻性/耗散类 -> Resistors
储能类     -> Capacitors / Inductors
源类       -> VoltageSources / CurrentSources
转换类     -> Transformers / Converters / Machines
```

#### 液压领域示例

```text
源类/供能类     -> Pumps
控制/调节类     -> Valves
执行类         -> Actuators
阻性/连接类     -> Resistances
```

#### 热领域示例

```text
边界/热源类     -> HeatSources
阻性类         -> ThermalResistances
储能类         -> HeatCapacitances
传输/换热类     -> HeatExchangers
```

#### 机械领域示例

```text
惯性/储能类     -> Inertias / Springs
阻性类         -> Dampers / Frictions
执行类         -> Actuators / Drives
传动/连接类     -> Transmissions / Joints / GearSets
```

### 步骤 5：决定是否拆成独立业务包

以下情况优先拆成独立业务包：

- 同角色下已有两个及以上语义稳定的组件
- 该角色在该领域中是用户显式关心的核心对象
- 该角色会持续扩展
- 组件族已经形成独立 `Basics`

以下情况可以暂时不单独拆包，但也不要放进总 `Basics`：

- 当前只有一个很小的具体组件，且预计不会扩展
- 当前阶段只是最小闭环验证，需要先落一个组合业务包

此时可用一个更宽的临时业务包名，例如：

- `PassiveComponents`
- `EnergyStorage`
- `ConversionComponents`

等后续组件族增多后再拆分。

## 混合领域策略

### 1. 先按主领域切主业务包

例如电液控制库，可先形成：

```text
HydraulicActuators
HydraulicValves
ElectricalDrives
Controllers
```

而不是把所有跨域组件混成一个 `Basics`。

### 2. 跨域耦合件单独成包

若组件的核心价值是跨域转换，而不是属于某一单域组件族，可单独形成：

- ElectroHydraulicConverters
- ThermalFluidCouplings
- MechatronicActuators

### 3. 接口仍按领域族归口

混合领域不意味着 `Interfaces` 混成一个平面层。优先保留：

```text
Interfaces
  ElectricalInterfaces
  HydraulicInterfaces
  ThermalInterfaces
  MechanicalInterfaces
```

## 反模式

以下做法默认视为错误：

1. 因为领域不熟，就把所有具体组件都放进 `Basics`
2. 因为需要先跑通加载，就把业务包全部并回一个总包
3. 因为当前组件数量少，就放弃角色分类
4. 只按组件名字猜包，不看 connector、端口职责和状态特征
5. 用 `package.order`、`Basics` 或加载顺序问题替代真正的业务分层设计

## 输出要求

当使用本文生成业务包时，结论中应至少说明：

1. 当前领域画像
2. 组件角色分类结果
3. 角色到业务包名的映射
4. 哪些内容进入业务包，哪些进入 `Basics`
5. 哪些内容归 `Interfaces`、`Utilities`、`Sources`、`Sensors`

## 与其他参考的分工

- 顶层骨架、`Basics` 基本规则：`template-package-scheme.md`
- 执行顺序与最小闭环：`executor-base.md`
- 结构检查：`workflow-checklist.md`
- 常见结构错误：`common-errors.md`

只有本轮需要新建/调整业务包且领域映射不明确时才读本文；实际采用模板时再引用 `template-package-scheme.md`，不因跨域关键词自动加载全部结构资料。
