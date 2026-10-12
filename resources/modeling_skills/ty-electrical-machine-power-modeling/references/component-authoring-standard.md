# Component Authoring Standard

## Package Layout

本文件只适用于“可复用组件 package”。如果交付物只是单独案例，则直接交付单个 `.mo` 文件，不要为了形式强行创建 `Tests/Examples/Resources` 目录树。

最低推荐结构:

```text
ComponentName/
|- ComponentName.mo
|- package.mo
|- package.order
|- Tests/
|- Examples/
`- Resources/
```

复杂组件可扩展为:

```text
ComponentName/
|- ComponentName.mo
|- package.mo
|- package.order
|- Basic/
|- Components/
|- Types/
|- Tests/
|- Examples/
`- Resources/
```

Nested package rule:

- 如果普通组件 `.mo` 文件嵌套在现有工程包内，必须明确其 `within` 路径；`package.mo` 按父级规则省略 `within`。
- 不要假设脚手架能自动推断正确的父包名。

## Main Component File

主组件文件应满足:

- 名称与 package 同名或语义稳定
- 顶部就能看出继承关系和外部接口
- 用户可调参数位于文件前部
- `annotation(Icon(...), Diagram(...))` 完整
- 需要时带 `Documentation(info=...)`

## Parameters

每个用户可调参数都必须:

- 出现在参数区
- 带中文注释
- 有单位时写明单位或意义
- 需要分类时使用 `Dialog(group="...")`

## Interfaces

每个端口都必须:

- 带中文注释
- 若为电压/电流/速度/转矩等，说明单位或物理含义
- 放置在合理方向并保持图标可读

## Internal Structure

- 能拆出内部子模块时，优先放入 `Basic/` 或 `Components/`
- 枚举、类型、记录等放入 `Types/`
- 若要复现 Simulink 初始化、保持、边沿或离散更新逻辑，优先显式编码，不要依赖模糊默认行为

## Tests

- `Tests` 至少 2 个
- 测试类名应直接表达目的
- 每个测试都要有 `Documentation(info=...)` 或模型内文字说明测试目的
- 每个测试都要显式 experiment 设置

## Reload And Sign Checks

- 修改 `.mo` 文件后，重新验证前先强制 reload 根 `package.mo`
- 对机械源、受控源、传感器类元件，先确认符号方向与测试意图一致
- 对离散或混合系统，保持测试中的 `Interval`、`IntegratorStep`、`Algorithm` 显式可读

## Resources

以下内容可放入 `Resources/`:

- Simulink 导出 CSV
- Sysplorer 导出 CSV
- MAT 文件
- 对标截图
- 说明文档

## Naming Guidance

- 与 Simulink 强对标时，可使用 `*SimulinkCompat`、`*AgainstSimulink`
- `Tests` 用 `Test_*` 或 `*Case`
- 不要混用大小写风格
