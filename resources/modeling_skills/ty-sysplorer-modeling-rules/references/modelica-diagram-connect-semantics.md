# Modelica 图形与连接语义

本文件只说明图解中“连什么、放在哪里、如何显示”的语义边界。它不替代 `workflows/seven-gates-validation.md` 对 Gate 6 的验收时序、结构化字段和交付判定。

## 1. `connect`：结构和方程

```modelica
connect(a, b);
```

`connect(a, b)` 定义模型结构，语义由连接器类型决定，而不是“画一根线”。

- 对非 `flow` 变量，兼容连接器产生相等约束。
- 对 `flow` 变量，产生守恒关系；复合连接器按成员递归展开。
- 改变 `connect` 的端点、连接器类型或连接关系可能改变模型行为。
- 仅改变图形折点、颜色或线型通常不改变方程，但不能以此替代正确的端点和连接器兼容性检查。

在写入 `connect(...)` 前，必须从类文档、公开内省或已确认的模型接口验证两端端口、单位和类型。不得凭名称猜测连接器。

## 2. `Placement` 与 `iconTransformation`：实例几何

实例上的 `Placement(transformation(...))` 描述其在 Diagram 中的位置、尺寸和朝向，为编辑器和后续布线提供锚点。`iconTransformation` 描述外部连接器在 Icon 层的几何关系。

- 系统、子系统和需要图形交付的组件，应使关键实例的位置与真实连接器锚点一致。
- 对外可见连接器，应同时检查 `Placement` 和必要的 `iconTransformation`，避免图标层端口悬空、重叠或方向错误。
- 20×20 尺寸、网格间距和 `%name` 属于项目约定或风险检查；若项目已有约定应遵守，否则以经评审的布局结果为准，不把它们误写成通用 Gate。
- 修改 Placement 通常只改变图形呈现，不改变方程；但错误几何会妨碍图面审查和自动布局，不能忽略。

## 3. `Line`：可见走线而非方程

`connect` 可附带 `annotation(Line(...))`，用于描述折线、颜色和粗细等可见路由：

```modelica
connect(sensor.y, controller.u)
  annotation(Line(points={{10,0},{30,0}}, color={0,0,127}));
```

- `Line.points` 是显示折点序列，不决定 `connect` 生成的方程。
- 对计划在 Diagram 中可见的连接，Line 应能反映真实端点和路由意图；不得让线条明显偏离连接器锚点、穿越关键图元或遮挡标签。
- 物理域颜色、信号颜色和线宽可遵循项目或现有库约定；若没有可靠约定，不得臆造工具专属显示规则。

## 4. 与 Gate 6 的协作

本次新建或修改的图形对象在 Gate 4 成功后、最终图形交付前执行 Full Gate 6。纯视觉布局缺陷不阻止翻译或仿真。按七门闸工作流检查外部连接器位置/图标变换、关键内部实例、计划可见连接和 Icon/Diagram 可读性。

图面验收、显式布局修复条件与写回后复检统一引用 `workflows/seven-gates-validation.md` 的 Gate 6。首次验收不主动追加布局工具，但 MCP 检查/翻译/仿真可自动改写无 Placement 的用户文件；按 `references/shared-standards.md` 判断授权并记录实际图形变更。显式 writeback_mo 必须给出目标类及模型文件，区分结构写回、官方布线与持久化证据。布局成功不代替模型检查，检查成功不代替图面验收。

一句话区分：**`connect` 决定结构和方程；`Placement` 决定实例在图上的位置；`Line` 决定连接在图上如何显示。**
