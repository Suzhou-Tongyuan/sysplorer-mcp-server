---
name: ta-vehicle-modeling
description: 在 Sysplorer 中构建、修复、验证、评审并打包车辆模型时使用，凡任务涉及车辆、整车、汽车、底盘、动力系统、传动、轮胎、悬架、制动、转向、发动机、电机、电池、热管理、低压电器、动力性、经济性、续航、操稳、平顺性、滑行、制动、加速、循环工况、车辆结果曲线核验，或任何车辆/子系统模型搭建与仿真，都必须在 `ty-sysplorer-modeling-rules` 之后使用本技能。若明确提到 `TAEconomy`、`TADynamics`、`TAThermalSystem`、`TAEngine`、`TABattery`、`TAElectronic` 或要求使用 TA 车辆库，则优先按 TA 六库流程执行；若用户要求简单集总参数/教学极简/无 TA 库依赖，也仍使用本技能做车辆领域分流、参数假设和验证约束。
metadata:
  short-description: TA vehicle modeling and validation guidance
  version: 1.1.3
  managed-by: sysplorer-mcp
---

# TA Vehicle Modeling

Use this only as a thin domain add-on to `ty-sysplorer-modeling-rules`. The parent skill owns routing, seven gates, layout timing, repair loop, Sysplorer safety rules, and delivery evidence. This skill adds vehicle-domain entry routing, TA six-library vehicle modeling decisions, library boundaries, examples, and validation focus.

## Entry Contract

Treat this skill as mandatory for any Sysplorer task whose target object is a vehicle, whole vehicle, automotive subsystem, or vehicle operating scenario, even when the user does not name a TA library.

Trigger examples include:

- Whole-vehicle or subsystem construction, repair, packaging, review, layout-annotation authoring, translation, simulation, or result validation.
- Lumped-parameter, point-mass, equivalent-mass, coast-down, acceleration, braking, drive-cycle, range, economy, handling, ride, thermal-management, engine, battery, electrical-load, chassis, tire, suspension, steering, brake, driveline, powertrain, and motor-drive vehicle tasks.
- Requests that say only "车辆模型", "整车模型", "滑行工况", "动力性", "经济性", "续航", "操稳", "平顺性", "热管理", "发动机", "电池", "低压电器", or similar vehicle-domain wording.

After triggering, first apply `ty-sysplorer-modeling-rules` for Modelica/Sysblock/hybrid routing. Then use this skill to decide whether the implementation should use TA six-library components, a simpler Modelica/MSL/custom lumped model, or a documented fallback because TA evidence is unavailable or out of scope. Do not skip this skill merely because the user asks for a "simple" or "lumped-parameter" vehicle model.

## Hard Constraints

Treat these as blocking requirements, not preferences:

- For Sysplorer vehicle tasks, stay in the Sysplorer MCP / ModelingPy tool domain. Do not route to Syslab skills or Syslab tools unless the user explicitly asks for Syslab.
- Do not directly copy or `extends` a complete official example, complete vehicle architecture, complete subsystem template, or complete sample deliverable as a new user deliverable.
- Modeling difficulty, missing internal signal wiring, failed repair attempts, or schedule pressure never relaxes the previous rule. If blocked, reduce scope, hand-build the visible topology, or report the blocker; do not hide the requested model behind an inherited complete template.
- Deliverable source must expose the requested vehicle topology through explicit component instances and `connect(...)` statements unless the task is only to verify or explain an existing example.
- Before `CheckModel`, `TranslateModel`, or `SimulateModel` on a deliverable `.mo`, run `scripts/audit_modelica_source.py` when a file path exists. For packaged models, pass `--dependency-root` with the already authorized top-level package directory so the audit can read enclosing `package.mo` dependencies; without that option it reads only the model file. Never infer an authorization root or search outside it. A failed audit is a stop condition, not a warning.
- Before simulation, verify that the requested end time is actually bound to the tool/model stop-time setting. Do not use result probe times such as `target_time` as a substitute for stop time unless the active tool schema documents that mapping.
- Final delivery must state the official/example usage status: `reference only`, `directly reused existing example`, or `not used`. `directly reused existing example` cannot be reported as a newly built deliverable.
- Apply parent Gate 6 to graphical objects actually created or changed, including automatic layout writes. Use hierarchy, `Placement`, `Line(...)`, endpoints, and layout diagnostics as structural evidence; image export/inspection follows user needs and available capability. Record `not_required` for read-only, Documentation-only, code-only without graphical objects, or unchanged graphical targets. Do not expand unchanged inherited levels or claim visual inspection without viewing images.

## Parent Contract and MCP 0.4

Use `../ty-sysplorer-modeling-rules/references/shared-standards.md` as the authority for MCP classification, session reuse, failure parsing, and retry control; use `../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md` for validation depth, Gate 6, and completion status. Offline/source-only tasks make no session calls. Existing concrete failures are led by the independent debugging entry defined by the parent; in that case, applying the parent means reusing its constraints only, not restarting Modelica/Sysblock/hybrid routing or TA/non-TA selection. This domain skill supplies targeted evidence without restarting a build. Failures during a new build remain in the original task.

Stop at the requested terminal stage. Result variables, KPI, plots, animation, and formal reports are required only when requested or necessary for the agreed acceptance criterion; otherwise mark them `not_required`. Do not infer proxy metrics merely to fill a checklist. A successful simulation and verified physical results are separate claims.

MCP 0.4 uses `model_inspect` for classes/components/ports/text queries, `compare_model` for comparisons, and `model_manager` for lifecycle operations. `call_code` accepts only `run_sysplorer_api` or its `run_script` alias with a required object `payload` and explicit ModelingPy import. Check/translate/simulate may automatically write layout back to a loaded user file, even without `reload_mo_path`; they are not read-only review tools. Follow the parent authorization boundary and record any actual graphical change under Gate 6.

## Minimal Reading

All `references/...`, `workflows/...`, `scripts/...`, and `templates/...` paths in this skill are relative to **this skill directory** (the folder that contains this `SKILL.md`), not the workspace root or any parent `skills/` directory.

Read only the files needed for the current task:

| Need | Read |
|---|---|
| New model preflight | `references/preflight-checklist.md` before any new whole-vehicle or subsystem modeling workflow |
| Requirement classification | `references/requirement-map.md` |
| Library selection | `references/library-selection.md`, then one relevant `references/library-cards/<library>.md` |
| Manual/example lookup | `workflows/verify-example.md`; directly use `load_library` + class/document exploration for the named or inferred TA library |
| Multi-library whole vehicle | `references/combination-rules.md` |
| Build / modify model | `references/build-rules.md`; add `references/package-design.md` when forming vehicle-specific business layers in a user library |
| Parameters | `references/parameter-rules.md` |
| Result validation in the agreed scope | `references/validation-rules.md` |
| Repair | `references/error-repair-playbook.md`, then `references/common-errors.md` |
| Acceptance | `references/acceptance-checklist.md`, `references/output-contract.md` |
| Layout annotations | `references/diagram-layout-rules.md` when source-level `Placement` or `Line` annotations are created or repaired |
| Sparse input | `templates/scenarios/case-selection-template.md` |

## Specialized Workflows

- New whole-vehicle or subsystem model: `workflows/build-from-scenario.md`
- Existing vehicle model repair: `workflows/repair-existing-model.md`
- Official or enterprise example validation: `workflows/verify-example.md`

## Domain Additions

- Use the Minimal Reading table as the router; do not load all TA references or all library cards by default.
- For information lookup tasks such as "find an example and open it", use `workflows/verify-example.md` and directly explore the named or inferred TA library with `load_library`, class listing, and targeted class/document queries.
- Use `references/requirement-map.md` and `references/library-selection.md` for task classification, TA library responsibility, and primary/support library selection.
- For new whole-vehicle or subsystem models, treat `references/preflight-checklist.md` as a blocking preflight gate before editing or checking model source.
- For common whole-vehicle requests, prefer the quick-start entries in the selected library card before broad class exploration: `TAEconomy` for `0-100` / CLTC / cycle / conventional / EV / hybrid architecture, `TADynamics` for KC suspension, six-wheel or chassis dynamics, and `TAThermalSystem` for HVAC / cabin / refrigerant loops.
- For repair, validation, layout annotations, package design, parameters, and delivery wording, follow the matching workflow/reference and return to `references/output-contract.md` plus `references/acceptance-checklist.md` before final delivery.
- Use Chinese by default for user-visible descriptions, diagram text, and comments; preserve library names, class names, variable names, and interface names.

## Repair Priority

Existing concrete failures follow the Parent Contract and debugging owner directly without restarting parent routing or vehicle discovery. The following is a diagnostic search order, truncated at the requested terminal stage; it is not a requirement to run every later stage.

Prefer the shortest blocking chain:

`primary-library boundary -> library dependency -> model hierarchy/interfaces -> topology/connections -> parameters/units -> initialization -> check/translate -> simulation -> result variables -> diagram annotations`

Preserve existing valid structure and return to the failed parent Step/Gate after repair. Keep diagnostic edits separate from final deliverable edits when possible.

## Time Budget Discipline

- For large whole-vehicle or multi-axle assemblies, split work into discovery -> skeleton -> check, then only the requested translate/simulate/result stages. Apply Gate 6 independently to actual graphical changes; pure visual defects do not block runtime stages. Do not spend the whole turn on open-ended library exploration.
- Prefer known quick-start examples/classes from the selected library card before recursive browsing.
- If model construction or repair is timing out, freeze a smaller runnable contract, validate that, and report the exact remaining subsystem/interface blocker instead of silently continuing with unbounded exploration.

## Delivery Additions

In addition to parent delivery evidence, state:

- Primary TA library, support libraries, base dependencies, selected official/example references, and the final model entry point. The TA boundary applies to its responsible subsystem; retain parent-selected standard-library and support-domain components in the project library set.
- Vehicle scope and scenario: architecture, subsystem boundary, drive cycle/road/thermal condition, or operating case as applicable.
- Build contract and source audit result, including whether any official templates/examples were only referenced, directly reused as existing examples, or not used.
- Verified actions: `CheckModel`, `TranslateModel`, `SimulateModel`, source-level layout-annotation checks, and result-variable validation status.
- Verified variables and pass/fail/no-reference judgment for performance, economy, range, dynamics, thermal, engine, battery, or electrical-load results.
- Any TA library substitution, unresolved assumption, blocked example lookup, or open-loop item.
