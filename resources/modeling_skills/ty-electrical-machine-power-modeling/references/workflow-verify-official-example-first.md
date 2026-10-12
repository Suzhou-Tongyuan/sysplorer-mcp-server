# Verify Official Example First

在开始自建测例前，优先尝试官方示例。

## Steps

1. 先查目标 Simulink 组件是否有官方 `openExample`
2. 若有，优先把该示例拆成最小必要子系统
3. 记录示例中的:
   - 输入源
   - 参数
   - 观测量
   - 停止时间
   - 离散/连续设置
4. 在 Sysplorer 中用允许库重建等效场景
5. 固定对比基线:
   - Simulink: `5e-5`, `backward Euler`
   - Sysplorer: `5e-5`, `ImplicitEuler`
6. 若官方示例过大，保留第一个“可单独验证该组件行为”的最小子系统

## Output

- 官方示例名称
- 被保留的最小场景
- 关键观测量
- 是否适合作为 `Tests/Case1`
