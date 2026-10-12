---
name: sysblock-signal-modeling-handbook
description: 执行与审计手册。只维护指导层最小执行闭环、验收门禁、交付证据与失败处置；方法细节统一引用主文档 sysblock-signal-modeling-guide.md。
---

# Sysblock 信号/通信建模手册（执行与审计）

## 拆分说明

本文件仍保留原有完整内容，作为历史执行与审计主文档。
为避免单文件过大，当前已将执行闭环相关内容拆分到更小的参考文件中；新任务应优先阅读：

1. `workflow-overview.md`
2. `execution-checkpoints.md`
3. `troubleshooting-and-fallback.md`

若需要模板与方法层信息，再结合阅读：

1. `template-selector.md`
2. `modeling-methods.md`
3. `playbooks.md`
4. `parameter-contracts.md`

若只需要快速推进执行闭环，优先看 `execution-checkpoints.md`。
若需要完整旧版集中说明，再继续阅读本文件正文。

## 文档职责边界

本手册属于指导层执行文档，不是全局流程裁决文档。

- 方法主源：`sysblock-signal-modeling-guide.md`
- 执行主源：本手册（检查点、门禁、证据、风险闭环）
- 冲突裁决：与 `modeling_rules` 冲突时，以 `modeling_rules` 为准。
- 分工边界：`sysblock-signal-modeling-guide.md` 定义方法，`sysblock-signal-modeling-handbook.md` 定义执行与审计留痕。
- 本手册给出的是指导层最小执行闭环，不替代 `modeling_rules` 的全局 Gates。

使用原则：遇到“怎么搭模型”回到 `sysblock-signal-modeling-guide.md`；遇到“怎么验收交付”使用本手册。

定位裁决：
- 本手册属于指导层执行文档，不是全局流程规则文档。
- 与 `modeling_rules` 冲突时，以 `modeling_rules` 为准。
- 与 `sysblock-signal-modeling-guide.md` 冲突时，方法定义以 `sysblock-signal-modeling-guide.md` 为准，执行留痕以本手册为准。

## 1. 执行入口（先判别再建模）

1. 判别任务是否属于 Sysblock 信号/通信建模主路径；若涉及混合信号，仅按扩展专题纳入。
2. 确认当前使用的是“指导层增强路径”，而非替代全局流程路径。
3. 到 `sysblock-signal-modeling-guide.md` 选择主路径模板（A/B/C/D/F0/F1）或扩展专题模板 E，并确定层级（L0/L1/L2）。
4. 准备本轮执行输入：任务目标、模型边界、关键参数来源、预期 KPI。

## 2. 执行检查点（CP0-CP6）

### CP0 分流与定位确认

- 确认任务属于 Sysblock 信号/通信建模主路径，或属于其扩展专题。
- 确认本资源作为“指导层”被调用，而不是替代全局流程层。

### CP1 模板与层级选择

- 选择主路径模板（A/B/C/D/F0/F1）或扩展专题模板 E。
- 选择能力层级（L0/L1/L2），默认 L0 起步。

### CP2 参数契约审计

- 核查采样、维度、映射、同步、信道参数一致性。
- DSSS 场景必须核查 PG 与 PN 长度一致性。
- DSSS 场景必须核查单一 PG 选择源是否同时驱动信源、Tx PN、Rx PN、滤波/判决支路。
- DSSS 场景必须核查 Tx/Rx PN 对称性与断言是否启用。

### CP3 结构检查

- 执行 `check_model`。
- 未通过禁止进入 CP4。

### CP4 行为验证

- 执行 `simulate_model`。
- 未通过不得给出达标结论。

### CP5 证据与 KPI

- 用 `result_manager` 读取关键变量与 KPI。
- 至少一个 KPI 达标且可复读。
- DSSS 场景必须确认选择器、发端、信道、收端、误差统计等语义槽位可识别，且至少包含 `bitErr` 与 `berApprox`。

### CP6 风险闭环

- 记录未关闭风险、升级/回退决策、下一轮动作。

## 3. 交付门禁（必须全部满足）

1. 结构门禁：模型检查通过。
2. 执行门禁：仿真正常完成。
3. 证据门禁：关键变量可复读、可追溯。
4. 质量门禁：至少一个 KPI 达到阈值。
5. 安全门禁：关键断言未失败。
6. 边界门禁：本手册只作为指导层最小执行闭环使用，不替代 `modeling_rules` 的全局 Gates。

## 4. 审计规则

### 4.0 定位审计（新增）

- 是否明确将本资源作为“指导层”使用。
- 是否错误地用本资源覆盖全局流程规则。

### 4.1 来源审计

- 是否记录并显式使用流程规则源与块库参数源。
- 是否避免“仅靠 default_sources”做块级决策。
- 是否记录检索失败与回退动作。

### 4.2 方案审计

- 是否输出四层方案说明。
- 是否说明为何采用基础方案、为何升级增强方案。
- 是否标注关键参数来源和单位。
- 混合信号内容是否被明确标记为扩展专题，而非主定位并列范围。

### 4.3 结果审计

- 是否有变量名、时间点、结果值与阈值。
- 是否存在“仅看波形主观判断”的结论。
- 是否记录未关闭风险与后续动作。

## 5. 证据打包模板

```json
{
  "task": {
    "type": "整形 | 滤波 | 多速率 | 通信链路 | DSSS",
    "extension_topic": "none|mixed_signal",
    "objective": "...",
    "template_id": "A|B|C|D|F0|F1|E",
    "model_level": "L0|L1|L2",
    "sync_level": "S0|S1"
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
  "dsss_contract": {
    "pg_selected": "15|31|63|N/A",
    "selector_binding": "ok|failed|n/a",
    "pn_tx_rx_consistent": true,
    "filter_linked": true,
    "assertion_enabled": true,
    "observability_complete": true
  },
  "risk": {
    "open_items": [],
    "next_actions": []
  }
}
```

## 6. 失败处置规则

- `check_model` 失败：只能报告“未通过结构检查”，不得宣称建模完成。
- 仿真失败：只能报告“未通过行为验证”，不得给出达标结论。
- KPI 不达标：必须附改进方向与下一轮计划，不得仅给结论。
- 检索失败：不得中断建模闭环，必须走回退路径并记录 `fallback_used=true` 与原因。

## 7. 快速排障流程

1. 分辨失败类型：结构失败、执行失败、指标失败、检索失败。
2. 结构失败：优先回查连线、维度、采样配置。
3. 执行失败：优先回查求解设置、时序设置、关键参数一致性。
4. DSSS 专项失败：优先回查选择器绑定、Tx/Rx PN 对称、PG 切换后的滤波联动与断言接通。
5. 指标失败：回到 `sysblock-signal-modeling-guide.md` 对应模板章节逐项复核。
6. 检索失败：改用模板法 + 库文档/API 文档回退，并补充证据留痕。

## 8. 维护原则

- 任何“方法内容”变更只改 `sysblock-signal-modeling-guide.md`。
- `sysblock-signal-modeling-handbook.md` 只维护执行流程与审计留痕。
- 当两文档出现语义冲突：流程裁决以 `modeling_rules` 为准；方法定义以 `sysblock-signal-modeling-guide.md` 为准；执行留痕以 `sysblock-signal-modeling-handbook.md` 为准。
