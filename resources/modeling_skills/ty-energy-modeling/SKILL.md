---
name: ty-energy-modeling
description: 使用 Sysplorer 中的 TY 商业能源模型库构建、修复、验证、翻译、仿真并复核综合能源、光伏、风电与电池相关模型。当用户明确指定 TY 能源库/商业库路径，或父规则/有效上下文已选定 TY 光伏发电库、风力发电库、电池库、综合能源系统库组件时使用。未指定库时先判断标准库能力，满足则使用标准库，不足则保留可用标准库并用商业组件补足，再加载本技能。仅出现“光伏”“风机”“储能”“综合能源”等场景词而未明确 TY 能源库范围时，不足以单独触发本 skill。这是一个领域附加 skill，必须仅在 `ty-sysplorer-modeling-rules` 之后使用。
metadata:
  short-description: TY energy-system modeling and validation guidance
  version: 1.1.1
  managed-by: sysplorer-mcp
---

# TY Energy Modeling

Use this only as a thin TY energy-domain add-on to `ty-sysplorer-modeling-rules`. The parent skill owns routing, gate discipline, layout timing, repair-loop control, and delivery evidence.

## Parent Contract and MCP 0.4

Use `../ty-sysplorer-modeling-rules/references/shared-standards.md` as the authority for MCP classification, session reuse, failure parsing, and retry control; use `../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md` for validation depth, Gate 6, and completion status. Offline/source-only tasks make no session calls. Existing concrete failures are led by the independent debugging entry defined by the parent; this domain skill supplies targeted evidence without restarting a build. Failures during a new build remain in the original task.

Stop at the requested terminal stage. Result variables, KPI, plots, animation, and formal reports are required only when requested or necessary for the agreed acceptance criterion; otherwise mark them `not_required`. Do not infer proxy metrics merely to fill a checklist. A successful simulation and verified physical results are separate claims.

MCP 0.4 uses `model_inspect` for classes/components/ports/text queries, `compare_model` for comparisons, and `model_manager` for lifecycle operations. `call_code` accepts only `run_sysplorer_api` or its `run_script` alias with a required object `payload` and explicit ModelingPy import. Check/translate/simulate may automatically write layout back to a loaded user file, even without `reload_mo_path`; they are not read-only review tools. Follow the parent authorization boundary and record any actual graphical change under Gate 6.

## Minimal Reading

All `references/...` and `workflows/...` paths in this skill are relative to **this skill directory** (the folder that contains this `SKILL.md`), not the workspace root or any parent `skills/` directory.

| Need | Read |
|---|---|
| Inputs / contract | `references/standard-input-checklist.md`, `references/input-output-contract.md` |
| Domain rules | `references/energy-domain-rules.md` |
| Component selection | `references/component-mapping.md` |
| Typical scenarios | `references/energy-typical-scenarios.md` |
| Repair | `references/error-repair-playbook.md` |
| Acceptance | `references/acceptance-checklist.md` |
| Tool mapping | `references/mcp-modeling-toolkit.md` when tool choice is unclear |
| Resource routing | `references/resource-map.md` |
| Manual lookup | `references/manual-index.md` only when concise references are insufficient |

## Specialized Workflows

- Scenario build: `workflows/build-from-scenario.md`
- Existing failed model repair: `workflows/repair-existing-model.md`
- Manual/example verification: `workflows/verify-example.md`

## Domain Additions

- The energy subsystem uses 光伏发电库、风力发电库、电池库、综合能源系统库 and `Modelica 4.0.0.TY.1`; this whitelist does not restrict the entire delivery. Preserve parent-selected standard and support-domain components. The commercial path fixes Modelica at `4.0.0.TY.1`; report conflicting project versions without silently rewriting them.
- Preserve user-specified topology, key components, and explicit parameter targets unless they are proven incompatible and the user approves a change.
- Map the main energy path first, control chain second, and economic/dispatch auxiliaries third.
- Preserve standard-library components already selected by the parent. For a documented capability gap assigned to this energy subsystem, choose a direct TY domain class with compatible interfaces; do not replace sufficient standard components merely because a commercial example exists.
- Keep the model GUI-editable and diagram-reviewable; prefer Sysplorer-native placement and connection generation whenever feasible.
- Use conservative bring-up settings first, then expand simulation horizon, solver aggressiveness, or optimization scope only after stability is confirmed.
- Verify functional correctness, trend reasonableness, numerical acceptability, and consistency with the stated energy-system objective.
- When manual lookup is needed, prefer the concise references first and open the copied energy-library manuals only as a last step.

## Repair Priority

Use this diagnostic order only within the requested terminal stage; it does not require every later runtime or result action:

`session/tool readiness -> allowed-library/class scope -> boundary/source completeness -> connection topology -> interface compatibility -> parameter/unit consistency -> CheckModel -> TranslateModel -> simulation stability -> result interpretation`

Do not leave the parent-confirmed energy-subsystem library scope merely to make a model pass; preserve the other already-selected subsystem libraries. Do not delete required energy sources, storage, converters, loads, boundary conditions, or probes merely to silence diagnostics.

## Delivery Additions

In addition to the parent delivery evidence, state:

- Model structure, component mapping, library usage, parameter summary, key assumptions, diagram review, simulation setup, verified variables, acceptance judgment, and limitations.
- By default, save one final model or identify one final model name/path; package extra reports only when explicitly requested.
