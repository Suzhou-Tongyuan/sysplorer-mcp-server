---
description: 用于修复已存在的 NPSLibrary 模型
---

# Repair Existing NPS Model Workflow

适用于“已有 NPS 模型、但 check / translate / simulate / result verify 失败”的任务。

## Process

1. 读取已有模型、报错日志、用户描述
2. 判断失败位置：Check / Translate / Simulate / Result Verify
3. 读取 `references/error-repair-playbook.md` 和 `references/nps-common-errors.md`
4. 定位问题并执行修复
5. 重跑失败步骤
6. 更新修复记录

## Common Shortcuts

- 若是连接类问题，优先检查 Ground、Reference、`Powergui`、测量参考点
- 若是结果异常，优先检查参数量级、边界条件、控制方向、相序和功率方向
- 若是高频开关或并网问题，优先检查 `PLL`、PWM、开关频率、采样周期和滤波参数
- 若是潮流问题，优先检查 `LoadFlowBus`、P/Q 约束和基准电压
