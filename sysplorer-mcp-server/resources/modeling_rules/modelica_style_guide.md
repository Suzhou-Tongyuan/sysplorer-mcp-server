# Modelica 建模规范（统一版）

> **强制要求**：创建或修改任何 `.mo` 文件前，必须先读本文档。禁止通过阅读 `src/` 下现有代码来推断风格。

---

## Part 1：库目录与文件组织规范

### 核心原则

禁止将整个库写入单一 `.mo` 文件。必须按库结构生成对应的目录树和文件，以支持按需编译、便于维护。

### 1.1 目录结构规则

```
<LibraryName>/           ← 根文件夹，名字与顶层 package 定义完全一致（大小写相同）
├── package.mo           ← 顶层 package 声明文件（必须存在）
├── <SubPackageA>/       ← 子 package，文件夹名与 package 名相同
│   ├── package.mo
│   └── <ModelA>.mo
├── <SubPackageB>/
│   ├── package.mo
│   ├── <SubSubPackage>/
│   │   ├── package.mo
│   │   └── <ModelB>.mo
│   └── <ModelC>.mo
├── <StandaloneModel>.mo ← 直接属于顶层 package 的单一模型
├── Resources/           ← 资源文件夹（图片、源码、文档等）（可选）
│   ├── Images/          ← 图片资源（图标、架构图等）
│   ├── C-Sources/       ← 外部函数（C 源码）
│   ├── Include/         ← 外部函数（头文件.h）
│   └── Library/         ← 外部函数（.lib/.dll 库文件）
└── Utilities/           ← 子 package：通用工具与辅助模型库（可选）
    ├── package.mo
    └── Functions.mo     ← 通用函数模型示例
```

### 1.2 典型库示例（航空库）

```
AircraftLib/
├── package.mo
├── Common/
│   └── package.mo
├── Examples/
│   └── package.mo
├── FlightControlSystem/
│   └── package.mo
├── HydraulicSystem/
│   └── package.mo
├── LandingGearSystem/
│   └── package.mo
├── Tests/
│   └── package.mo
├── UsersGuide/
│   └── package.mo
├── Resources/
│   ├── Images/
│   ├── C-Sources/
│   ├── Include/
│   └── Library/
└── Utilities/
    └── package.mo
```

### 1.3 package.mo 格式

每个目录必须有一个 `package.mo`，声明该层的 package：

```modelica
within <ParentPath>;        // 根目录 package.mo 省略 within 或写库名
package <PackageName>
  "包的说明注释";
  annotation(
    preferredView = "info",
    Documentation(info = "<html>...</html>"),
    uses(Modelica(version = "4.0.0.TY.1"),
         <OtherLib>(version = "x.y.z"))
  );
end <PackageName>;
```

> **规则**：凡引用了外部库（MSL、私有库），**必须**在顶层 `package.mo` 的 `uses(...)` 中声明库名及版本号。未声明会导致跨平台加载失败或版本冲突。
>
> **默认标准库版本**：Sysplorer 2024b 内置的 Modelica 标准库为 **`4.0.0.TY.1`**（同元科技定制版），**不是** 原版 `4.0.0`。所有新建模型库的 `uses()` 声明中，MSL 版本号**必须**写 `Modelica(version = "4.0.0.TY.1")`。写成 `"4.0.0"` 会导致 Sysplorer 找不到匹配版本而加载失败。

### 1.4 package.order 格式

Sysplorer 通过每个 package 目录下的 `package.order` 纯文本文件控制该 package 内子项在库浏览器中的**显示顺序**。

**格式规则：**
- 文件名固定为 `package.order`，与 `package.mo` 位于同一目录
- 每行写一个子类名（子 package 名或单一模型类名），不含路径、不含扩展名
- 顺序即为库浏览器中的显示顺序
- 文件末尾保留一个空行（Sysplorer 标准库的惯例）
- 不支持注释

**示例**（某 `HydraulicSystem/package.order`）：
```
Interfaces
Sources
Components
Sensors
Examples
```

**覆盖范围：** 只列该目录直属的子 package 和 `.mo` 类名，不递归到子目录。

**操作规则：**
- 新建 `package.order` 时，按推荐顺序列出所有已有子项：`Interfaces → Sources/Loads → Components → Sensors → Examples`
- 新增 `.mo` 文件或子 package 后，将类名追加（或插入）到此文件对应位置
- 该文件**只影响显示顺序，不影响加载**；未列入此文件的类仍可被正常加载和编译
- **禁止**使用 Dymola 私有注解 `__Dymola_classOrder`，Sysplorer 不识别该注解

### 1.5 单一模型文件格式

```modelica
within <FullPackagePath>;
model <ModelName>
  // ...
end <ModelName>;
```

### 1.6 命名规则

| 对象 | 规则 | 示例 |
|------|------|------|
| 根文件夹 | 与顶层 package 名完全一致 | `AircraftLib/` |
| 子 package 文件夹 | 与 package 名完全一致 | `HydraulicSystem/` |
| 单一模型文件 | `<ClassName>.mo` | `Pump.mo` |
| 图片文件夹 | 固定为 `Resources/Images/` | — |
| 外部函数文件夹 | 固定为 `Resources/C-Sources/`、`Resources/Include/`、`Resources/Library/` | — |

### 1.7 特殊文件夹说明

**Resources/**
- 资源文件夹，统一存放图片、外部源码、库文件等
- 下级子目录：
  - `Images/` — 组件图标、架构示意图（格式：`.png`、`.svg`、`.jpg`）
  - `C-Sources/` — 外部 C 源码文件（`.c`）
  - `Include/` — 外部头文件（`.h`）
  - `Library/` — 外部库文件（`.lib`、`.dll`）
- 引用方式：
  - 图片：`Icon(graphics={Bitmap(fileName="modelica://<LibName>/Resources/Images/xxx.png")})`
  - 外部函数：`annotation(Include="#include \"xxx.h\"")`

**Utilities/**
- 通用工具与辅助模型库（可选）
- 存放通用函数、辅助模型等

### 1.8 与当前项目的对应关系

当前项目已将 `src/` 定义为模型库仓库根目录。`src/` 下每个模型库都是一个独立文件夹，并按标准 Modelica package 目录树组织，不再使用 `Components/`、`Systems/` 顶层分类目录。

---

## Part 2：代码质量与可维护性规范

### 2.1 命名与可读性

- 类名使用 `PascalCase`：`SteamHeater`, `ChuaDiode`
- 参数、变量、连接器实例使用 `camelCase`：`heatFlowRate`, `outletPort`
- 常量使用 `UPPER_SNAKE_CASE`（仅限少量全局常量）
- 名称应体现物理意义，避免 `x1/x2/tmp`

### 2.2 单位与类型

- 优先使用 `Modelica.Units.SI` 类型，避免裸 `Real`
- 每个关键参数都要写单位与默认值：

```modelica
parameter Modelica.Units.SI.Resistance R = 10 "Load resistance";
```

- 量纲无关变量显式注释为 `unit="1"` 或说明其无量纲含义

### 2.3 方程与算法块

- 连续物理模型优先 `equation`，只有离散流程/程序式逻辑才用 `algorithm`
- 避免在 `equation` 中引入隐式副作用表达式
- 同一模型内按顺序组织：`parameters → variables → equations → annotations`

### 2.4 连接与接口

- 对外接口优先使用标准连接器（`Modelica.Electrical`、`Modelica.Thermal`、`Modelica.Fluid`）
- `connect()` 只连接兼容端口，不做跨域"硬拼接"
- 对每个公开连接器写注释，说明方向和物理含义

### 2.5 初始化与事件

- 显式写 `initial equation` 或关键参数初值，避免依赖工具默认初始化
- 事件逻辑集中在 `when`，避免分散触发条件
- 使用 `noEvent()` 前说明理由（数值稳定性或避免非必要事件）

### 2.6 注释与文档

- 每个公开类必须有简短类注释（1-3 行）
- 复杂方程前写"物理来源/假设"注释，而不是复述代码
- 在 `annotation(Documentation(info="<html>..."))` 中记录：
  - 建模假设
  - 参数范围
  - 已验证工况

### 2.7 可复用与扩展

- 抽象共性到 `partial model`，具体实现再 `extends`
- 公共参数保持一致命名（如 `m`、`Cp`、`R`、`L`、`C`），减少集成摩擦
- 避免把仿真工况硬编码进组件，工况放到 testbench/system 层

### 2.8 函数使用规范

`function` 用于无状态的显式计算，与 `model`（可含微分方程和事件）本质不同。

**格式要点：**
- 函数体内必须用 `algorithm` 块而非 `equation`
- 输入参数声明 `input`，输出参数声明 `output`
- 赋值使用 `:=` 操作符

**适用场景：**
- 纯数学计算（插值、拟合）、单位转换、查表映射 → 使用 `function`
- 涉及微分方程 `der()`、离散事件 `when`、状态依赖 → 使用 `model`

**调用方式：**
- 直接作为表达式调用：`y = myFunc(x)`
- 多输出用元组：`(a, b) = myFunc(x)`

**常用内置函数：**
- `sin/cos/exp/log/sqrt/abs/min/max` 等在 `Modelica.Math` 中
- 线性代数在 `Modelica.Math.Matrices`

**外部函数：**
- 通过 `external "C"` 声明接口
- 配合 `Resources/Library/` 和 `Resources/Include/` 下的库文件和头文件

**性能优化：**
- 使用 `annotation(Inline = true)` 建议编译器内联，提高调用效率

### 2.9 禁止项

- 禁止把多个核心类塞进一个 `.mo`（工具私有 helper 除外）
- 禁止未声明依赖库版本（见 `package.mo` 的 `uses(...)`）
- 禁止无单位 `Real` 泛滥和魔法数字直写
- **禁止出现未连接的孤立组件**——每个声明的组件实例必须至少有一个端口被 `connect()` 连接。孤立组件会触发 `cardinality() > 0` 断言失败（编译器错误 4259），且说明模型拓扑有误
- **禁止组件声明时使用全部默认参数**（如裸写 `TYMultibody.Bodies.BodyCylinder bodyCylinder;`）——这通常是误操作残留，必须显式写出关键物理参数

---

## Part 3：图形视图与注解规范

> **适用范围**：在工具中打开 `.mo` 文件时显示的 Icon / Diagram 视图。AI 只需在**组件级**提供最小 Icon 注解；系统级 Placement/Line 由 Smart Layout 自动布局工具（Gate 6）生成，**禁止手写**。

### 3.1 Modelica 的三种视图

| 视图 | 注解关键字 | 用途 |
|------|-----------|------|
| 文本视图 | —（正文代码） | 方程、参数、连接器声明 |
| 图标视图 | `Icon(...)` | 组件在系统图中显示的外观 |
| 图形视图 | `Diagram(...)` + 各组件 `Placement` + `connect()` `Line` | 子组件的拓扑图 |

### 3.2 Icon 注解（组件图标）

**坐标系**：MSL 惯例为 `{{-100,-100},{100,100}}`（绝对单位，工具缩放后显示）。

```modelica
annotation(
  Icon(
    coordinateSystem(extent = {{-100,-100},{100,100}}),
    graphics = {
      Rectangle(
        extent = {{-80,-40},{80,40}},
        lineColor = {0,0,255},
        fillColor = {255,255,255},
        fillPattern = FillPattern.Solid
      ),
      Text(
        extent = {{-80,60},{80,40}},
        textString = "%name",          // 实例名（必写）
        lineColor = {0,0,255}
      ),
      Text(
        extent = {{-80,-40},{80,-60}},
        textString = "R=%R",           // 关键参数（按需）
        lineColor = {0,0,0}
      )
    }
  )
);
```

**Icon 书写规则：**
- `%name` 文本元素**必须**存在，位于图标框上方或内部
- 关键物理参数（如 `R=`, `m=`）可选，帮助在图中快速识别实例
- 无特殊需求时**不必手工绘制复杂图形**；留空 `Icon()` 或仅写 `%name` 文本也可接受

### 3.3 各物理域线色惯例

工具按域为连线着色，帮助区分物理域。编写 Icon 外框和 `Line` 注解时应遵循同域颜色：

| 物理域 | 线色（RGB） | 说明 |
|--------|------------|------|
| 电气（Electrical.Analog） | `{0,0,255}` | 蓝色 |
| 旋转机械（Rotational） | `{64,64,64}` | 深灰 |
| 直线机械（Translational） | `{0,127,0}` | 绿色 |
| 热（Thermal.HeatTransfer） | `{192,192,192}` | 浅灰 |
| 多体（MultiBody） | `{95,95,95}` | 中灰 |
| 流体（Fluid） | `{0,127,255}` | 浅蓝 |
| 信号（Blocks） | `{0,0,127}` | 深蓝（连线）/ `{192,192,192}`（边框） |
| 跨域信号线 | `{0,0,0}` | 黑色（默认） |

### 3.4 Placement 注解（组件实例位置）

在系统/组装模型的 `annotation` 中，**每个子组件实例都必须有 `Placement`**——包括 `inner World`、`inner Modelica.Mechanics.MultiBody.World` 等全局环境组件。没有 Placement 的组件在 GUI 图形视图中**不可见**。

#### 3.4.1 标准格式：origin + 固定 extent

**必须**使用 `origin` 定位 + **固定** `extent = {{-10, -10}, {10, 10}}`（20×20）格式。**禁止**使用绝对坐标 extent（如 `extent = {{-105, -15}, {-75, 15}}`），这种写法容易导致组件尺寸不一致（30×30、40×30 等）。

```modelica
// ✅ 正确：origin + 固定 extent
TYMultibody.Joints.Revolute rev1(...)
  annotation(Placement(transformation(origin = {-100, 0}, extent = {{-10, -10}, {10, 10}})));

// ❌ 错误：绝对坐标 extent（尺寸为 30×30，不符合 20×20 标准）
TYMultibody.Joints.Revolute rev1(...)
  annotation(Placement(transformation(extent = {{-105, -15}, {-75, 15}})));
```

#### 3.4.2 尺寸与间距规则

| 规则 | 值 | 说明 |
|------|---|------|
| 标准组件尺寸 | **20×20** | `extent = {{-10, -10}, {10, 10}}`（固定不变） |
| 组件中心间距 | **40** 单位（典型） | 相邻组件 origin 之差，最小 30 |
| 网格对齐 | **10 单位** | origin 的 x/y 值应为 10 的倍数 |
| 坐标基准 | `{0, 0}` | 模型坐标系中心，左/上为负、右/下为正 |

#### 3.4.3 典型布局示例

```modelica
// 串联链：水平排列，中心 y=0，间距 40 单位
inner TYMultibody.World world(...)
  annotation(Placement(transformation(origin = {-140, 0}, extent = {{-10, -10}, {10, 10}})));
TYMultibody.Joints.Revolute rev1(...)
  annotation(Placement(transformation(origin = {-100, 0}, extent = {{-10, -10}, {10, 10}})));
TYMultibody.Bodies.BodyCylinder body1(...)
  annotation(Placement(transformation(origin = {-60, 0}, extent = {{-10, -10}, {10, 10}})));
```

> **⚠️ AI 规则**：**不得手写系统模型 Placement**。系统级模型（含多个子组件的组装）必须调用 `generate_system_model_with_auto_layout`（Gate 6），由 Smart Layout 布局引擎计算位置。只在单一组件的 `Icon` 中允许手工指定图形元素。**但若手工编写 testbench 或示例模型**，必须严格遵守上述 origin + 固定 extent 格式。

### 3.5 connect() 的 Line 注解

`connect()` 语句可附加 `annotation(Line(...))` 指定连线外观：

```modelica
connect(R1.p, V1.p)
  annotation(Line(
    points = {{-40, 0}, {-80, 0}},  // 折线拐点列表
    color  = {0, 0, 255},           // 按域颜色（见 3.3）
    thickness = 0.5                 // 物理线 0.5，信号线省略（默认 0.25）
  ));
```

**规则：**
- 物理域连线（电气、机械、热、流体）：`thickness = 0.5`
- 信号线（Blocks RealInput/Output）：省略 thickness（默认 0.25）
- `points` 列表中每个点 `{x, y}` 代表一个折角；起点和终点由工具自动衔接到连接器位置
- **连线端点坐标**必须与组件边缘对齐：对于 20×20 组件（origin ± 10），连线起点/终点为 `origin.x ± 10`
  ```modelica
  // body1 origin={-60,0} → 右边缘 x=-50；rev2 origin={-20,0} → 左边缘 x=-30
  connect(body1.frame_b, rev2.frame_a)
    annotation(Line(points = {{-50, 0}, {-30, 0}}, color = {95, 95, 95}));
  ```
- 同样：**系统级模型的 Line 注解由 Smart Layout 布局工具自动生成**，AI 不手工填写 `points`

### 3.6 Diagram 注解

系统模型顶层可有 `Diagram` 注解，用于指定组装视图的坐标系范围：

```modelica
annotation(
  Diagram(coordinateSystem(extent = {{-200,-100},{200,100}}))
);
```

**规则：**
- 简单组件（无子图）：省略 `Diagram`
- 系统级模型：Smart Layout 布局工具会自动写入 `Diagram` 坐标范围，无需手写

### 3.7 旋转与镜像

连接器方向默认朝左（`frame_a`）或朝右（`frame_b`、`pin_p`）。当布局需要翻转组件时，使用 `rotation` 参数：

```modelica
annotation(Placement(transformation(
  extent   = {{-10,-10},{10,10}},
  rotation = 90    // 顺时针旋转角度：0 / 90 / 180 / 270
)));
```

---

## AI 执行清单（创建或修改库时必须逐项检查）

### 目录与文件结构
- [ ] 根文件夹名 == 顶层 package 名（大小写完全一致）
- [ ] 每个 package 目录内都有 `package.mo`，`within` 路径正确
- [ ] 顶层 `package.mo` 的 `annotation` 中用 `uses(...)` 声明所有外部库依赖及版本号，MSL 版本必须为 `"4.0.0.TY.1"`
- [ ] 每个 `.mo` 文件的 `within` 路径与其所在目录对应
- [ ] 每个 `.mo` 文件名与类名完全一致（大小写）
- [ ] 图片资源放入 `Resources/Images/`，外部函数/库放入 `Resources/C-Sources/`、`Resources/Include/`、`Resources/Library/`
- [ ] 不存在将多个 package 写入同一 `.mo` 文件的情况
- [ ] 子 package 文件夹名与 package 名完全一致

### 代码质量
- [ ] 类名 PascalCase，变量/参数 camelCase
- [ ] 关键参数使用 `Modelica.Units.SI` 类型，附单位和默认值
- [ ] 无裸 `Real` 泛滥，无魔法数字
- [ ] `connect()` 端口类型已通过 `query_private_library` 或快速参考手册确认匹配
- [ ] 显式写 `initial equation` 或初值

### 图形注解
- [ ] **每个组件实例**（包括 `inner World`）都有 `Placement` 注解
- [ ] Placement 使用 `origin` + `extent = {{-10, -10}, {10, 10}}`（20×20）格式，**禁止**绝对坐标 extent
- [ ] 组件 `Icon` 包含 `%name` 文本元素
- [ ] 线色与物理域一致（见 3.3）；物理线 `thickness=0.5`，信号线省略
- [ ] connect Line 端点坐标与组件边缘对齐（origin ± 10）
- [ ] 无孤立未连接的组件实例
- [ ] 系统模型 Placement/Line **未手写**——已调用 `generate_system_model_with_auto_layout`（Gate 6）

### 验证
- [ ] `mworks_check_model` 无编译错误
- [ ] 至少 1 个 testbench 覆盖关键动态行为，并已运行仿真
- [ ] `mworks_get_var_values` / `extract_physics_kpi` 无 `NaN/Inf`，关键变量范围合理
