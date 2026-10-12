---
name: ty-nps-library-modeling
description: Use Sysplorer's built-in commercial `NPSLibrary` to build, repair, validate, review, and package power-electronics, motor-drive, source-network, fault-protection, and load-flow models. Trigger only when the request explicitly mentions `NPSLibrary`, explicitly asks for Sysplorer built-in/commercial-library modeling, or clearly needs NPSLibrary sample reuse. Use this only after `ty-sysplorer-modeling-rules`; for graphical modeling, component creation, wiring, check, translate, and simulate tasks stay on Sysplorer MCP, while Syslab MCP is reserved for Julia/script/algorithm/data-processing work.
metadata:
  short-description: NPSLibrary power-electronics and motor-drive modeling guidance
  version: 1.1.0
  managed-by: sysplorer-mcp
---

# TY NPS Library Modeling

Use this only as a thin domain add-on to `ty-sysplorer-modeling-rules`. The parent skill owns routing, seven gates, layout timing, repair loop, and delivery evidence.

## Minimal Reading

All `references/...` and `workflows/...` paths in this skill are relative to **this skill directory** (the folder that contains this `SKILL.md`), not the workspace root or any parent `skills/` directory.

| Need | Read |
|---|---|
| Inputs / contract | `references/standard-input-checklist.md`, `references/input-output-contract.md` |
| Tool boundary or MCP choice | `references/mcp-modeling-toolkit.md`, then `references/sysplorer_api_usage.md` |
| High-frequency component lookup | `references/nps_component_quick_index.md` |
| Ground / reference fallback | `references/component_fallback_strategy.md` |
| Domain rules | `references/nps-domain-rules.md` |
| Component mapping | `references/component-mapping.md` |
| Typical scenarios | `references/nps-typical-scenarios.md` |
| Repair | `references/error-repair-playbook.md`, then `references/nps-common-errors.md` |
| Acceptance | `references/acceptance-checklist.md` |
| Search navigation | `references/resource-map.md` |
| Manual lookup | `references/manual-index.md` only when concise references are insufficient |

## Tool Boundary

- Use Sysplorer MCP for graphical modeling, model creation, component insertion, wiring, parameter placement decisions, `check_model`, `translate_model`, `simulate_model`, result opening, and model-file lifecycle.
- Use Syslab MCP only for script execution, algorithm validation, data processing, or Julia/Python/M-language style computation that is explicitly part of the task.
- Do not mix Syslab MCP into ordinary Sysplorer graphical modeling tasks unless the request explicitly includes script-side algorithm verification.
- Do not copy Syslab error-handling habits into Sysplorer API modeling. Fix the Sysplorer invocation path itself.

## Search Order

1. Read `references/nps_component_quick_index.md` for high-frequency component paths.
2. Check `Sysplorer 2026a\Docs\EleLib\Samples\NPSLibrary` when the user asks to reuse or reference an existing NPS example.
3. Read `references/component_fallback_strategy.md` when `Ground`, `Reference`, `Neutral`, or related primitives are missing.
4. Read `references/sysplorer_api_usage.md` when the task depends on `NewModel`, `AddComponent`, `.mo` parameter injection, or annotation handling.
5. Use `get_lib_model_document` only after the quick index and samples path are not enough to resolve a concrete class.

## Specialized Workflows

- Scenario build: `workflows/build-from-scenario.md`
- Example/environment verification: `workflows/verify-example.md`
- Existing failed model repair: `workflows/repair-existing-model.md`

## Domain Additions

- Stay inside `NPSLibrary` by default unless the fallback strategy explicitly points to Modelica Standard Library primitives.
- Preserve user-specified topology and key components unless proven incompatible and approved by the user.
- Map the main power path first and the control chain second; add `Ground`, `Reference`, `Powergui`, sensors, boundaries, and result probes only as needed.
- Prefer reusable sample topology and parameter patterns from `Sysplorer 2026a\Docs\EleLib\Samples\NPSLibrary` before rebuilding common NPS structures from scratch.
- For load-flow tasks, check `LoadFlowBus`, slack/PV/PQ bus definitions, and `Powergui` load-flow initialization.
- For graphical modeling, keep component placement and wiring GUI-editable and reviewable. If GUI-side `call_code` fails, repair the invocation path before considering text-level fallback.
- For every NPSLibrary modeling case that involves simulation, force the model-level experiment setup to use inline implicit Euler: `Algorithm=InlineImplicitEuler`. Do not leave the model on Dassl or an unspecified default solver.
- For switching/PWM/PLL-dominant models, use the required inline implicit Euler experiment annotation from `references/nps-domain-rules.md`; set the step from PWM frequency, the fastest physical sampling step, or the control period. Use `5e-5` as the normal default and a smaller value such as `1e-5` only when the case requires it.
- Verify functional correctness, trend reasonableness, numerical acceptability, and engineering/reference expectations.

## Search Discipline

- Batch similar component lookups; do not perform repeated one-by-one probing for the same category.
- Deduplicate semantically similar results such as `voltage source`, `three-phase voltage source`, and `AC voltage source`.
- Avoid repeated `get_lib_model_document` calls for the same path.
- After a quick index or sample confirms a class path, do not re-query its parent directories unless a mismatch appears.
- Keep manual traversal and repeated document reads to the minimum needed for the current modeling task.

## Repair Priority

Prefer the shortest blocking chain:

`GUI/call_code invocation -> grounding/reference -> connection completeness -> interface compatibility -> Powergui/load-flow -> initialization -> parameters -> translation -> simulation -> result interpretation`

Do not delete sensors, sources, converters, grounding, or required subsystems just to pass translation.

## Delivery Additions

In addition to parent delivery evidence, state:

- Model structure, component mapping, parameter summary, key assumptions, diagram review, simulation setup, verified variables, and limitations.
- Which quick-index paths, sample models, fallback rules, or manual documents were actually used.
- By default, save one final model file; create packaged reports only when explicitly requested.
