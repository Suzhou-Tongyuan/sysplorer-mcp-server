---
name: ty-sysblock-signal-modeling
description: 在 Sysplorer 中执行 Sysblock 信号处理或通信链路建模，包括滤波、频谱验证、多速率处理、特征提取、基带链路、BER、QPSK/QAM、同步、DSSS、TYDSPSystem、TYCommunication 或 TYMixedSignal。仅在 `ty-sysplorer-modeling-rules` 将任务分类为 Sysblock 路径后继续使用；不得用于 Modelica 物理建模、纯 API 查询或手写/修补 Modelica 文本。
metadata:
  short-description: Sysblock signal-processing and communication modeling guidance
  version: 1.0.0
  managed-by: sysplorer-mcp
---

# Sysblock Signal And Communication Modeling

Use this only after `ty-sysplorer-modeling-rules` routes the task to the Sysblock path. The parent skill owns session health, routing, seven gates, layout timing, repair loop, and delivery evidence.

## Scope

- Signal processing: filters, spectrum checks, multirate processing, feature extraction.
- Communication links: baseband chains, BER, QPSK/QAM, synchronization, DSSS.
- Libraries such as `TYDSPSystem`, `TYCommunication`, `TYMixedSignal`, and `SysplorerEmbeddedCoder`.

Do not use for Modelica physical models, pure API lookup, or isolated block parameter/port checks that do not need signal-domain workflow guidance.

## Non-Negotiable Sysblock Rules

- Invoke parent routing before modeling; do not override it.
- Use official Sysplorer APIs through `call_code(mode="run_sysplorer_api")`.
- Never call `SetModelText`, handwrite `.mo`, or patch source text for Sysblock topology.
- Do not mix Modelica physical libraries into a Sysblock signal path.
- Load `SysplorerEmbeddedCoder` first; query concrete source blocks only after the source category is known.

## Minimal Reading

All `references/...` paths in this skill are relative to **this skill directory** (the folder that contains this `SKILL.md`), not the workspace root or any parent `skills/` directory.

| Need | Read |
|---|---|
| Overview / reading order | `references/workflow-overview.md` |
| Template and level selection | `references/template-selector.md` |
| Modeling methods | `references/modeling-methods.md` |
| Chosen playbook | `references/playbooks.md` |
| Parameters / observability | `references/parameter-contracts.md` |
| Checkpoints / evidence | `references/execution-checkpoints.md` |
| Troubleshooting | `references/troubleshooting-and-fallback.md` |
| Concrete block docs | `sysblock_model_library` via MCP |

## Domain Additions

- Classify the task before designing: filtering, spectrum, multirate, feature extraction, communication link, BER, synchronization, or mixed-signal task.
- Build the smallest runnable signal chain before expanding scenarios.
- Define observability early: required output variables, spectra, BER, synchronization state, or timing metrics.
- Treat `run_sysplorer_api` success as only script success; parent `check_model` still determines model validity.
- If the minimum loop runs but user metrics are not met, return to the parent optimization loop.

## Delivery Additions

In addition to parent delivery evidence, state:

- Task category, template/playbook used, library scope, key parameters, observed variables, verification conclusions, and unresolved risks.
