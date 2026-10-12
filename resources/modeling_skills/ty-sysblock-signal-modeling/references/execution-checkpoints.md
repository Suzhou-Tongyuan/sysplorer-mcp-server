# 执行检查点与交付门禁

## 用途

本文件用于维护详细执行检查点、交付门禁与证据打包要求。

## 执行检查点

### CP0 分流与定位确认

- 确认任务属于 Sysblock 信号/通信建模指导层路径
- 确认没有误用本资源覆盖全局流程规则

### CP1 模板与层级选择

- 完成任务归类
- 选择模板与层级
- 记录当前目标与预期 KPI

### CP2 参数契约审计

- 核查采样、维度、映射、同步、信道参数一致性
- DSSS 场景核查 PG、PN 长度、选择器绑定、Tx/Rx 对称与断言状态

### CP3 结构检查

- 执行 `check_model`
- 未通过不得进入行为验证

### CP4 行为验证

- 执行 `simulate_model`
- 未通过不得给出达标结论

### CP5 证据与 KPI

- 用 `result_manager` 读取关键变量与 KPI
- 至少明确当前结论属于结构层、行为层或 KPI 层

### CP6 风险闭环

- 记录未关闭风险
- 记录升级、回退或下一轮动作

## 交付门禁

1. 结构门禁：模型检查通过
2. 执行门禁：仿真正常完成
3. 证据门禁：关键变量可复读、可追溯
4. 质量门禁：至少一个 KPI 达到阈值，或明确说明证据缺口
5. 安全门禁：关键断言未失败

## 证据打包模板

```json
{
  "task": {
    "type": "整形 | 滤波 | 多速率 | 通信链路 | DSSS",
    "objective": "...",
    "template_id": "A|B|C|D|F0|F1",
    "model_level": "L0|L1|L2"
  },
  "retrieval": {
    "queries": [],
    "decision_basis": "...",
    "retrieval_status": "ok|partial|failed",
    "fallback_used": true
  },
  "execution": {
    "check_model": "pass|fail",
    "simulate_model": "pass|fail",
    "check_model_log_ref": "...",
    "simulate_log_ref": "..."
  },
  "kpi": {
    "name": "...",
    "value": "...",
    "threshold": "...",
    "pass": true
  },
  "risk": {
    "open_items": [],
    "next_actions": []
  }
}
```
