# Build from Scenario

## Scope

Use this workflow when the user asks to build a hydraulic, thermal-hydraulic, pneumatic, or closely related control-system model from natural language, a component list, a table, CSV, or a scenario template.

## Required Inputs

- System type: hydraulic, thermal-hydraulic, pneumatic, or mixed.
- Main components and quantity.
- Medium, source, return/exhaust boundary, actuator/load, control method, and target variables.
- Whether the user requires a real Sysplorer model, a topology/parameter plan only, or a structured report.
- Allowed defaults and values that must remain `to confirm`.

## Execution

Session/tool evidence is a prerequisite only for authorized live actions, not another gate; offline file work uses existing source/index/document evidence without probing MCP or starting Sysplorer. Use the parent `../../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md` as the authority; the numbers below are local steps.

1. **Gate 1 — scope and authorization:** classify requirements through `references/requirement-map.md`; record build vs plan, permitted writes, required verification depth and report/image requests. A plan-only task stops after its requested evidence.
2. **Gate 2 — evidence and component boundary:** use `references/library-selection.md` and `references/component-map.md` to retain selected standard components and choose commercial components only for the responsible fluid subsystem. Confirm medium, ports, boundaries, component parameters and units; commercial paths use `Modelica 4.0.0.TY.1`.
3. Read `references/parameter-rules.md` when assigning parameters and `references/mcp-modeling-toolkit.md` only before actual platform actions.
4. **Gate 3 — construction:** build the smallest source-to-actuator/load loop. Write the topology connection table before `connect(...)`; create the user model from Modelica text unless the user explicitly selected example-based modification.
5. For actual graphical targets, use `references/diagram-layout-rules.md` and `references/diagram-line-annotation-rules.md`: prepare zone/route tables, key `Placement`, planned visible `Line(points=...)` and `Diagram(coordinateSystem(...))` as the model is built.
6. Run the two local annotation/layout preflight scripts when applicable with `-TargetClass <FQClass>` for each changed target and record findings; do not combine diagrams from different classes. Preserve `undetermined` and its diagnostics for unsupported syntax or ambiguous scope, and supplement the required Gate 6 evidence as described in `scripts/README.md`. Visual defects may be resolved at Gate 6 after physical execution; they do not prohibit `check_model`, translation or simulation. Annotation syntax/structure errors are handled by model check.
7. **Gate 4 — check:** check the exact changed model when required; keep an actual failed model check blocking dependent translation/simulation. MCP 0.4 can auto-layout and write the model, so record actual changes and include changed graphical targets in Gate 6.
8. For `TYHydraulics` / `TYHydraulicComponents`, apply `references/capacitor-resistive-check.md` to applicable topology before requested long simulation; after a topology or `UseVolume*` change, return to affected required stages in the original offline or authorized live mode. Offline work uses static topology review and does not acquire live checks.
9. **Gate 5 — validation design:** choose only the requested check/translate/simulate depth and runtime prerequisites. Run `translate_model` and `simulate_model` only when required.
10. Use `result_manager` and the result section of `references/validation-rules.md` only when result/KPI/curve acceptance is required. Simulate-only does not invent target variables or set `verify_result_var`.
11. **Gate 6 — diagram acceptance:** inspect newly created or actually changed graphical objects using structured annotation, instance/connection, coordinate, anchor and readability evidence. Untouched inherited layers, read-only or Documentation-only work use `not_required`. Images supplement evidence when requested or useful and available; unmet explicit image requests remain recorded gaps.
12. **Gate 7 — delivery evidence:** use `references/acceptance-checklist.md` and applicable fields in `references/output-contract.md`; report each required action's true status and the unique current model. Formal reports are produced only when requested.

## Failure Handling

- If any gate fails, enter `references/error-repair-playbook.md`.
- Repair the smallest active blocker and return to the failed gate.
- If full graphical delivery is applicable, unresolved visibility/readability prevents that delivery claim; it does not invalidate successful check/translation/simulation or create graphical work for a plan/read-only task.
- Do not output intermediate iteration versions unless the user explicitly asks.

## Delivery Focus

Include only fields required by this task; other actions/evidence use `not_required` or are omitted. Plan-only and read-only tasks do not acquire additional runtime, result or graphical requirements here.

- Final model name/path and actual Sysplorer version.
- Actual TY libraries and medium libraries used.
- Component mapping table and substitution notes.
- Topology connection table.
- Parameter table, assumptions, and `to confirm` items.
- Actual requested MCP actions and per-stage status; structured Gate 6 evidence with images only when requested or useful and available. Unrequested actions are `not_required`.
- Key result variables and judgments only when result acceptance is required; otherwise `not_required`.
- Diagram review status: visible instances, visible key wires, symbol scaling, routing readability, and annotation checks.
