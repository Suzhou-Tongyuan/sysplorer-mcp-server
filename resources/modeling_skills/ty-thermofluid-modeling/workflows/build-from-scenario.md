# 从场景新建模型

## 适用场景

- 用户要求从零搭建热流体、换热、空气处理或通风系统。
- 用户需要最小可运行骨架，并继续扩展到可检查、可翻译、可仿真和可验证的模型。

## 推荐输入

- 系统目标、主要设备和介质类型。
- 边界工况、控制目标和关键结果变量。
- 必须保留的结构、组件或接口约束。

## 执行边界

先记录用户要求的终态与验收范围；本地 GATE 标题只是本流程步骤，不另设父级门闸。父级 `../../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md` 决定验证深度及 Gate 6，`../../ty-sysplorer-modeling-rules/references/shared-standards.md` 决定会话与分类重试。离线/源码任务不调用会话；check/translate/simulate 可能自动布局写回，不用于无写入保证的只读评审。结果、KPI、曲线、动画和正式文档不在范围时记 `not_required`。

## 执行流程

### GATE 1：需求收口

1. 先用 `references/requirement-map.md` 判断任务类型与默认路径。
2. 若介质、相态、关键边界或控制目标缺失，先补问；若不能补问，明确写出临时假设。

### GATE 1.5：库预检

1. 用 `references/library-selection.md` 和 `references/fallback-strategy.md` 判断首选库，并在放大正式模型前完成可用性预检。
2. 在本次运行验收范围内预检目标库、依赖及同领域最小代表模型；只要求 check 不追加翻译/仿真，要求仿真时才做短时 bring-up。只读/源码任务不增加运行预检。
3. 若预检失败，不要直接扩大正式模型，先进入回退判定：报告阻塞或改用允许的替代库。

### GATE 2：库与组件映射

1. 用 `references/library-selection.md` 选择优先库。
2. 用 `references/component-map.md` 确定核心设备、边界、传感器和控制器映射。
3. 用 `references/media-selection.md` 确认介质和介质约束。

### GATE 3：最小骨架

1. 先搭主能量链路和主回路，再补边界、测点和必要控制。
2. 若系统暂时无法闭环，优先补最小等效边界，使模型先可 `check` / `translate`。
3. 需要骨架模板时，优先参考 `templates/model-skeletons/` 和 `templates/scenarios/`。

### GATE 4：参数化与布局

1. 按 `references/parameter-rules.md` 设定参数，确保关键设备和控制阈值可配置。
2. 按 `references/modeling-rules.md` 复核拓扑、边界和求解可行性。
3. 按 `references/diagram-routing-rules.md` 整理布局、对齐接口并清理低质量连线。
4. 按父 Gate 6 检查本次新建/实际修改的图形对象，未修改的继承层级不展开。纯视觉缺陷不阻塞 check/translate/simulate；图形语法/结构错误由检查阻断。图片按用户要求或可用且有帮助的能力选用，并单列图片交付状态。

### GATE 5：按请求验证

1. 按父级七门闸执行到本次请求终态，不无条件执行完整仿真链。
2. 仅结果核验在范围时，使用 `references/validation-rules.md` 检查约定变量、方向性和量纲；否则记 `not_required`，不设默认 `verify_result_var`。
3. 结构尚未稳定时，优先整体写入最小模型后 check，再执行适用的 translate/simulate；只在约定结果标准需要时读取一组关键变量。
4. 按父 shared-standards 分类停止无新证据的重复策略，回到介质、边界、拓扑、初始化等上层定位。
5. 仅适用的 KPI、图面或用户目标未达成时继续对应修复；不得因未请求结果而阻止任务完成。实际自动布局写回纳入 Gate 6。
6. 输出前对照验收与输出契约，说明本轮已达阶段和临时等效边界。

## 输出重点

- 说明采用的库、介质、组件映射和模板来源。
- 说明已完成的真实执行阶段，以及仍依赖的临时假设或等效边界。
- 结果验收适用时说明关键变量与结论，否则标记 `not_required`。
