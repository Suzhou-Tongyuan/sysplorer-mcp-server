# 修复现有模型

## 适用场景

- 用户已有模型在 `check`、`translate`、`simulate` 或结果验证阶段失败。
- 用户要求修复连接、介质、参数、边界、布局或控制逻辑问题。

## 推荐输入

- 模型名称或文件路径。
- 报错信息、异常现象和最近一次修改点。
- 必须保持不变的结构、接口或组件。

## 任务归属与执行边界

已有具体故障由父规则定义的独立调试入口主导；本流程只补充热流体诊断，不重启完整建模。新建过程中失败保留原任务，修复后回到受影响阶段。会话、错误与重试引用 `../../ty-sysplorer-modeling-rules/references/shared-standards.md`，验证范围与图面引用父七门闸。只复验本次请求内受影响阶段；结果未要求则 `not_required`。check/translate/simulate 可能自动布局写回，不得破坏只读边界。

## 执行流程

### GATE 1：定位失败阶段

1. 先确认问题卡在 `check`、`translate`、`simulate` 还是结果解释阶段。
2. 用 `references/common-errors.md` 缩小最短排查路径。

### GATE 2：聚焦根因

1. 涉及介质时先查 `references/media-selection.md`。
2. 涉及拓扑、离散、边界或回路组织时查 `references/modeling-rules.md`。
3. 若是开口回路、悬空端口或初始化困难，优先补最小边界让模型先恢复到可执行状态。

### GATE 3：最小修复

1. 每次只改一类问题，不同时混改介质、拓扑和控制逻辑。
2. 修复后立即重跑受影响阶段；必要时退回开环或分段验证。
3. 仅本次确有图形修改且父 Gate 6 适用时，用 `references/diagram-routing-rules.md` 验收受影响对象；不顺带修改未触及图面。

### GATE 4：结果复核

1. 在本次约定验证深度内核验异常是否消除；只有结果异常或结果验收在范围时读取 `references/validation-rules.md` 和结果变量。
2. 输出前对照 `references/acceptance-checklist.md` 和 `references/output-contract.md`，说明修复范围、残留风险和新增临时边界。

## 输出重点

- 说明失败位置、根因判断和最小修复范围。
- 说明修复是否改变了介质、拓扑、参数或控制策略。
- 说明修复后的真实执行结果与残留风险。
