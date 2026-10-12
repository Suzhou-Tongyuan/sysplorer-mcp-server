# Recreate Simulink Component

## Input

- Simulink 组件名称
- 所属库域
- 目标行为
- 官方示例或用户案例

## Steps

1. 判断目标是否属于基础电气库、电机库或电力系统库
2. 读取 `references/allowed-libraries-and-boundaries.md`
3. 读取 `references/component-authoring-standard.md`
4. 用 `scripts/init_component_package.py` 创建 package
5. 只从允许库和标准库选组件进行搭建
6. 暴露全部用户参数，并补全中文注释和单位
7. 构建 `Tests` 中至少 2 个测例
8. 读取 `references/simulink-parity-testing.md`
9. 导出曲线并用 `scripts/compare_series.py` 对比
10. 通过后再进入帮助文档流程

## Decision Rules

- 如果允许库没有现成单块，允许组合实现
- 如果组合实现仍不足以覆盖行为，明确记录差距，不要偷用其他库
- 如果官方示例存在，优先作为 `Case1`
- 如果官方示例不存在，自建 `Case1/Case2`
