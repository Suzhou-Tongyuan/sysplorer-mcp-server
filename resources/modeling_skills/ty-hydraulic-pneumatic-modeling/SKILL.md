---
name: ty-hydraulic-pneumatic-modeling
description: 在 ty-sysplorer-modeling-rules 之后，为已选 TY 液压、热液压和气动组件提供领域建模、修复与按需验证指导。适用于用户明确指定 TYOilMedia、TYHydraulics、TYHydraulicComponents、TYThermalHydraulics、TYThermalHydraulicComponents、TYGasMedia、TYPneumatics、TYPneumaticComponents、TYThermals，已有上下文或模型已确认使用这些库，或父级依据标准库功能缺口选定标准库与商业库组合的任务；纯标准库流体任务由父级处理。
metadata:
  short-description: TY hydraulic, thermal-hydraulic, and pneumatic modeling guidance
  version: 1.1.3
  managed-by: sysplorer-mcp
---

# TY Hydraulic / Pneumatic Modeling

Use this only as a thin domain add-on to `ty-sysplorer-modeling-rules`. The parent skill owns routing, seven gates, layout timing, repair loop, and delivery evidence.
Common authority: `../ty-sysplorer-modeling-rules/references/shared-standards.md` owns MCP 0.4 session, tool, error and retry contracts; `../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md` owns the seven gates, validation depth and Gate 6. This domain add-on supplies checks, not a second execution pipeline.

- Respect explicit choices and effective prior context. Without a selected library, the parent first checks whether the standard library meets the requirements; keep sufficient standard components and add commercial components only for evidenced gaps. A documentation or tool failure is not a functional gap. This Modelica library combination is not Modelica/Sysblock mixed modeling.
- The domain library list constrains only this skill's responsible subsystem. Preserve selected standard components and other domains in the project library set; confirm cross-domain interfaces instead of deleting them.
- Commercial-library paths, including standard/commercial combinations, use `Modelica 4.0.0.TY.1`. Record a conflicting project version without silently rewriting dependencies.
- Inherit requested check/translate/simulate/result/plot/animation scope; unrequested actions are `not_required`. Formal reports and report templates are used only when requested; ordinary delivery uses concise evidence and applicable status fields.
- Existing fault diagnosis is led by the parent's debugging route; provide domain evidence and minimal repair without restarting model construction. A failure during new construction stays in its originating workflow and returns to its failed stage after repair.
- Gate 6 applies to newly created or actually modified graphical objects, including MCP automatic layout changes. Read-only, Documentation-only, pure code without graphical objects, and tasks that do not change graphical targets use `not_required`; untouched inherited objects/layers are not expanded.
- Structured diagram evidence is the common basis; images supplement it when requested or useful and available. Preserve explicit image requests as pending when unavailable and never claim visual inspection from text. Visual layout defects do not block check, translation or simulation; annotation syntax/structure errors are handled by model check. Applicable Gate 6 remains required for complete graphical delivery.
- MCP 0.4 check/translate/simulate can automatically write and reload a user `.mo` even without `reload_mo_path`. Read-only diagnosis must assess that boundary before calling them, use an authorized copy when possible, or report the limitation; do not promise a write-free check or bypass dedicated tools.

## Minimal Reading

Read only the files needed for the current task:

| Need | Read |
|---|---|
| Requirement classification | `references/requirement-map.md` |
| Library / component mapping | `references/library-selection.md`, `references/component-map.md` |
| Medium selection | `references/media-selection.md` |
| Parameters | `references/parameter-rules.md` |
| Validation | `references/validation-rules.md` |
| Capacitor-resistive topology | `references/capacitor-resistive-check.md` when using `TYHydraulics` / `TYHydraulicComponents` or when check/translate/simulate symptoms suggest fluid capacitance/resistance mismatch |
| Repair | `references/error-repair-playbook.md`, then `references/common-errors.md` |
| Acceptance | `references/acceptance-checklist.md`, `references/output-contract.md` |
| Diagram specifics | `references/diagram-layout-rules.md` when the task includes diagram creation or repair |
| Manual lookup | `references/manual-index.md` only when concise references are insufficient |

## Specialized Workflows

- New model from scenario/table/CSV: `workflows/build-from-scenario.md`
- Existing model or diagram repair: `workflows/repair-existing-model.md`
- Official or enterprise example verification: `workflows/verify-example.md`

## Domain Additions

- Identify task type: build, repair, verify example, result review, or guidance only.
- Pick the correct fluid family before building: hydraulic, thermal-hydraulic, pneumatic, gas media, or thermal support.
- Medium choice is structural. Do not continue with an unspecified or wrong medium when pressure, gas, or temperature behavior matters.
- For component lookup, library selection, and documentation-only tasks, do not pre-load large TY libraries by default. First use concise references, `references/mworks-fluid-library-index.json`, `resources_retrieval`, or `get_lib_model_document`; call `load_library` only when building/checking/translating/simulating or when a required class cannot be resolved.
- Treat library-load timeout as inconclusive because parsing may continue. Follow parent error/retry rules, inspect class or loaded-library evidence before any retry, and use `load_library(use_cache=true)` only when a retry is justified; do not impose a domain restart loop.
- For incremental modeling tasks, maintain one active deliverable model and evolve it forward instead of leaving multiple ambiguous final candidates. Use step or checkpoint suffixes only as temporary backups; after validation, clearly promote exactly one model/file as the current final deliverable.
- Check hydraulic/pneumatic topology, medium and boundary/reference completeness at the requested structural depth; verify pressure, flow, displacement, valve state and actuator direction only when result verification is in scope.
- For valve `Signal` control inputs, current-type commands must be converted to an `mA` numeric value before being entered, and voltage-type commands must be converted to a `V` numeric value before being entered. Do not rescale a user command such as `40 mA` to `0.04` just because a parameter declaration elsewhere uses SI base unit `A`; the signal input value must be `40`. For 3-position directional valves, map left position to negative values, center position to `0`, and right position to positive values unless the project already provides an explicit opposite polarity convention.
- For hydraulic models using `TYHydraulics` or `TYHydraulicComponents`, include applicable capacitor-resistive topology review before requested long simulation and after topology repairs involving valves, pumps, pipes, volumes, cavities, or `UseVolume*` switches. Select offline review, read-only diagnosis, or authorized live repair through `references/capacitor-resistive-check.md`; available MCP capability does not authorize starting software, checking live models, or making repairs.
- For thermal-hydraulic models, confirm heat-port / thermal-boundary assumptions; verify temperature response only when results are in scope.
- When result verification is required, treat zero flow under expected actuation, unphysical pressure, reversed displacement, NaN/divergence and missing temperature response as failed verification.
- For diagram tasks, key instances and key wires must be visible and reviewable; parent Gate 6 still controls layout timing.

## Repair Priority

Prefer the shortest blocking chain:

`source/boundary -> library dependency -> component mapping -> parameters -> topology -> capacitor/resistive topology -> medium -> initialization -> translation -> simulation -> result variables -> diagram annotations`

After repair, return to the failed parent Step/Gate. If topology, parameters, or diagram semantics changed, re-run the affected parent chain.

## Delivery Additions

In addition to parent delivery evidence, state:

- Final deliverable model name/path as a single authoritative version; do not list every intermediate iteration unless the user asks for version history.
- Chinese system description (`系统描述`) covering circuit purpose, main subsystems, action logic, validation status, and any simplified substitutions.
- Actual TY libraries used, model name/path, topology summary, medium, parameter assumptions, and unresolved `to confirm` items.
- Capacitor-resistive check status when the model uses `TYHydraulics` / `TYHydraulicComponents` or when this check was part of the repair path.
- Verified variables and pass/fail/no-reference judgment only when result verification is in scope; otherwise `not_required`.
- Diagram readability for model-creation or diagram-repair tasks.
