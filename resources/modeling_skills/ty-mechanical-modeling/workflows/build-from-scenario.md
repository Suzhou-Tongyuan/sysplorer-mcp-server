# 从场景新建模型 / Build From Scenario

## 默认读取集

- 必读：`references/requirement-map.md`
- 必读：`references/component-map.md`
- 必读：`references/mcp-modeling-toolkit.md`
- 按需：`templates/scenarios/user-input-minimum-form.md`，用户输入不足、目标过宽或缺少运动维度/驱动/约束时读取；结果验证在范围内时才补结果变量
- 按需：`references/parameter-rules.md`，仅在组件名单稳定、准备赋值前读取
- 必读：`references/validation-rules.md` 的“建模前静态预检”；完整结果验证部分仅在用户明确要求且 `simulate` 成功后读取
- 按需：`templates/scenarios/mechanical-system-min-loop.example.json`，仅在用户输入过 sparse 时读取

## 适用场景

- 用户要求基于 TY 商业机械库从零搭建机械系统、传动系统、接触系统、平面机构或多体模型。
- 用户已经给出目标机构、工况和关键结果，希望直接进入自动建模闭环。

## 最短闭环

1. 先抽取最小输入：机械系统类型、运动维度、目标机构、驱动方式、约束或连接关系；仅在结果验证属于验收范围时抽取关注结果。
2. 若任一必须字段缺失，读取 `templates/scenarios/user-input-minimum-form.md`，只追问阻塞建模的字段；可默认假设字段必须记录来源和风险。
3. 先读取 `references/requirement-map.md` 判断任务类型，再读取 `references/component-map.md` 的“需求到 TY 子库快速分流表”收敛 TY 子库、首选建模路径和首轮最小闭环。
4. 若快速分流表无法命中，先输出分流依据和不确定点，再补齐用户输入，不得直接自由猜测组件。
5. 按 `references/mcp-modeling-toolkit.md` 先查包/类列表，再批量查询候选子包；确认候选组件端口域后再写模型。
6. 先搭最小可检查闭环，不预先加入非必要损耗、柔性体、接触细节和扩展工况。
7. 写模型前执行 `references/validation-rules.md` 的静态预检：库边界、端口兼容、世界/参考、自由度/方程直觉、关键参数；仅在要求结果验证时补充预期结果变量。
8. 对最终候选组件集中查询真实参数名，再按 `references/parameter-rules.md` 的顺序赋值。
9. 按父级闭环推进；若为 3D、多体或空间机构任务，显式检查 `TYMultibody.World` 或等价世界组件。
10. 新建失败保留当前流程，领域定位后回到受影响阶段；错误分类与重试继承父级 shared-standards，必要时用最小模型、静态源码或文档隔离根因。
11. 若用户要求的运动趋势、动画、KPI 或其他验收目标未达成，回到父级优化循环；未要求的结果项不得阻止结束。

## 输出重点

- 说明采用的 TY 子库、核心组件和最小闭环结构。
- 说明用户输入最小表单中的已知字段、默认假设字段和仍缺失字段。
- 说明快速分流表命中的用户说法、推荐子库、建模路径和首轮最小闭环。
- 说明建模前静态预检结果，尤其是端口兼容、世界/参考和自由度判断。
- 说明关键参数来源和已执行动作；仅在结果验证属于验收范围时说明关键变量验证结论。
- 说明仍需补充的工况、参数或扩展结构。
