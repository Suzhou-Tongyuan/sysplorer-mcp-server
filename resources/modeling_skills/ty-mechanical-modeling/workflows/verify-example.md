# 验证样例 / Verify Example

## 默认读取集

- 必读：`references/validation-rules.md`
- 按需：`references/common-errors.md`，仅在样例结果异常时读取
- 若任务转为“基于样例重建模型”，停止当前路线并切到 `workflows/build-from-scenario.md`

## 适用场景

- 用户要求运行 TY 官方样例或企业样例并验证关键结果。
- 用户要求用样例做对照、学习参数习惯或复核结果，不要求直接把样例改壳成交付模型。

## 最短闭环

1. 先确认任务是“验证样例”还是“基于样例重建模型”；若是后者，转到 `workflows/build-from-scenario.md`。
2. 样例只可用于参考拓扑、参数习惯、观测变量和排障路径，不得通过 `extends`、wrapper 或直接改名交付。
3. 按父级已选 check / translate / simulate / result-review 深度执行，结果与动画仅按请求核验。只读样例验证需先考虑自动布局写回，使用获授权副本或说明限制；未改图形对象时 Gate 6 为 `not_required`。
4. 若结果异常，先核对结果来源、变量名、查询时间和后处理逻辑；仅查询/后处理错误按 `references/error-repair-playbook.md` 复用有效既有结果并重做受影响核验，不自动重新仿真。确认属于模型行为异常后，再按 `references/common-errors.md` 回溯结构、参数和工况，不要直接归因于求解器。

## 输出重点

- 说明样例用途、实际完成阶段；仅在结果验证范围内列关键变量与对照结论。
- 说明样例中哪些内容可复用，哪些内容不可直接交付。
- 说明若要迁移到用户场景，下一步需要重建或替换的部分。
