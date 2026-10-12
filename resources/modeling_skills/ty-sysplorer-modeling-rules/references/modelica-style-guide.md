# Modelica 文本与包结构规范

本文件保留具体 Modelica 物理模型和小型包修改所需的通用规则。复杂模型库目录、示例、测试、本地化、发布和库级评审，应在路径分流后追加使用 `modelica-library-workflow`。

## 1. 包、文件和依赖完整性

- 根文件夹名、顶层 `package` 名、子 package 文件夹名、类名和 `.mo` 文件名必须在大小写与层级上保持一致；普通类 `.mo` 文件使用 `within` 时，其路径必须与所属 package 一致。
- 每个 package 目录都应有不含 `within` 的 `package.mo`；直接子 package 或类写入同目录的 `package.order`，每行一个直接子项，不含路径、扩展名或注释。
- 新建直接子类/子包后同步更新父目录 `package.order`。该文件只表示显示顺序，不得用私有排序注解替代。
- 在顶层 `package.mo` 的 `uses(...)` 中声明外部依赖和版本。按 `domain-routing-and-library-versions.md` 的适用范围选择版本：车辆/商业路径固定 `Modelica(version = "4.0.0.TY.1")`；仅主规则单独使用时允许用户/工程有效版本覆盖。下方示例展示默认版本，不用于覆盖已有依赖。
- 资源文件放入相应 `Resources/` 子目录；不得将互不相关的核心类压入单一 `.mo` 文件。
- 新建 Modelica `model` 类时，`.mo` 文件名和 `package.order` 条目必须与类名同步；名称与中文描述的硬性长度规则见下节。

### 1.1 `package.mo` 示例

顶层和子 package 均不写 `within`，描述字符串后不加分号。

顶层：

```modelica
package ExampleLib "示例模型库"
  annotation(
    uses(Modelica(version = "4.0.0.TY.1"))
  );
end ExampleLib;
```

子 package：

```modelica
package Components "组件包"
end Components;
```

## 2. 名称、类型、参数与文档

- 新建 Modelica 组件或模型时，英文类名必须使用有意义的 `PascalCase`，只包含 ASCII 字母和数字，且不超过 15 个字符；类声明中 `""` 内的全部内容必须为中文简短描述（例如 `model PumpUnit "泵单元模型"`），整体不得超过 20 个可见字符，换行后续行同样计入、不得借换行规避长度限制。用户或项目已有明确规范时以其为准；不得仅为满足本规则而重命名现有类。
- Modelica 类声明的描述字符串后不加分号；类体内语句仍按语法使用分号。
- 参数、变量和连接器实例使用描述性的 `camelCase`。避免 `x1`、`tmp`、未说明缩写和魔法数字。
- 物理量优先使用 `Modelica.Units.SI` 类型。关键参数应提供单位、默认值和简短说明；无量纲量应说明其物理/逻辑含义。
- 公开类应有简短类说明；复杂方程前说明物理来源、假设或适用范围，而不是逐字复述代码。
- 在适用的 `Documentation` 注解中记录建模假设、参数范围和已验证工况。不得将未经验证的结论写成已验证行为。

## 3. 方程、算法、连接与事件

1. 连续物理关系优先写在 `equation`；离散或程序式逻辑才使用 `algorithm`。
2. 对外接口优先使用适用标准连接器；`connect(...)` 只能连接已确认兼容的端口，不得跨物理域硬拼接。
3. 初始化会影响行为时，使用 `initial equation` 或显式 `start` / `fixed` 设置；不得把关键初值完全交给未知的工具默认行为。
4. 事件条件集中在一致的 `when` / `elsewhen` 结构中；使用 `noEvent()` 前说明其数值稳定性或事件控制理由。
5. 无状态的显式计算使用 `function` 与 `algorithm`；包含微分方程、离散事件或状态演化的对象使用 `model`。外部函数必须声明接口和资源依赖。
6. 可复用共性优先抽取为 `partial model` / `extends`；测试工况和系统级边界条件放在测试台或系统层，不隐藏在通用组件中。

## 4. 图形信息的最低质量

- `connect(...)` 是结构/方程，`Placement(...)` 是实例位置，`Line(...)` 是可见走线；详细语义以 `modelica-diagram-connect-semantics.md` 为准。
- 图形化交付对象应给关键实例和可见连接提供可审查的信息。外部连接器还应核对 Icon 层变换。
- 固定尺寸、网格、`%name`、线色和非默认参数展示属于项目约定或风险检查；有项目约定时必须遵守，没有时不应把它们抬升为通用交付门禁。
- 所有本次新建或修改的图形对象执行 Full Gate 6；未修改对象不展开。首次验收不自动调用 `smart_layout`，只有验收失败后才按需修复；实际写回模型文本后必须重新检查。

## 5. 修改前自检

- [ ] 类、端口、单位、参数和依赖库均有证据。
- [ ] `package.mo` 无 `within`、普通类 `.mo` 的 `within` 路径正确、类描述后无分号。
- [ ] package 目录名、`package.mo` 中的类名、`end <PackageName>;` 和 `package.order` 一致。
- [ ] 物理关系、初始化和事件表达方式与行为目标匹配。
- [ ] 图形信息与真实连接锚点一致，且未将 Line 当作方程。
- [ ] 若任务涉及库结构、示例、测试或本地化，已追加 `modelica-library-workflow`。
