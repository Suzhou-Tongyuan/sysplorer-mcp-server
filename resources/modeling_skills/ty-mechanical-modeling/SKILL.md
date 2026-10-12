---
name: ty-mechanical-modeling
description: 在 ty-sysplorer-modeling-rules 之后，为已选 TY/同元商业机械组件提供建模、修复与按需验证指导。适用于用户明确指定 TYDriveline、TYFlexBody、TYContact、TYMechanics、TYMultibody、TYDriveline3D、TYMechanics2D，已有上下文或模型已确认使用这些库，或父级依据标准库功能缺口选定标准库与商业库组合的任务；纯标准库或自建机械任务仍由父级处理，机械主题本身不触发本技能。
metadata:
  short-description: TY commercial mechanical-system modeling guidance
  version: 1.1.3
  managed-by: sysplorer-mcp
---

# TY Mechanical Modeling

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

## Hard Entry Guard

- Enter after an explicit commercial-library request, effective prior context/existing-model selection, or the parent has selected TY mechanical components to fill evidenced standard-library gaps; the current prompt need not repeat a library name.
- If the user specifies the Modelica Standard Library, a self-authored implementation, or another non-TY mechanical library and does not request TY commercial components, do not load this skill or any of its references/workflows. Return immediately to the parent Modelica workflow.
- Mechanical subject matter alone—including pendulums, rigid bodies, joints, drivetrains, multibody motion, contact, or animation—is not a trigger.
- This add-on never increases the validation depth selected by the parent workflow. Result variables, plots, curves, KPI analysis, or animation are required only when the user requests them or the parent acceptance contract explicitly includes them.
- If the acceptance contract ends at `check + translate + simulate`, stop execution after that chain succeeds and finish only applicable Gate 6 and delivery evidence; do not add result steps or post-processing.

## Minimal Reading

All `references/...`, `workflows/...`, and `templates/...` paths in this skill are relative to **this skill directory** (the folder that contains this `SKILL.md`), not the workspace root or any parent `skills/` directory.

| Need | Read |
|---|---|
| Requirement classification | `references/requirement-map.md` |
| Component mapping and query scope | `references/component-map.md` |
| Parameters and interface confirmation | `references/parameter-rules.md` |
| Preflight, validation, and result checks | `references/validation-rules.md` |
| MCP query/tool efficiency | `references/mcp-modeling-toolkit.md` |
| Repair | `references/common-errors.md`, then `references/error-repair-playbook.md` |
| Acceptance | `references/acceptance-checklist.md` |
| Sparse input | `templates/scenarios/user-input-minimum-form.md` |

## Specialized Workflows

- New TY mechanical model: `workflows/build-from-scenario.md`
- Existing model repair: `workflows/repair-existing-model.md`
- Example validation: `workflows/verify-example.md`

## Entry Path Routing

Before choosing a workflow or loading libraries, split the task into one of these paths:

| Path | Use when | Initial library boundary |
|---|---|---|
| 1D simplified model | The system can be represented as lumped translational/rotational mechanics, shaft dynamics, or power transmission without spatial pose, frame geometry, contact, flexible bodies, or multibody animation. Treat this as an intentional simplification even if the real machine is physically 3D. | Only `TYMechanics` and `TYDriveline` at first. Use `TYMechanics` for basic translational/rotational mechanics and `TYDriveline` for driveline/transmission elements. |
| 2D planar model | The user explicitly asks for planar, x-y, around-z, or `TYMechanics2D` behavior. | `TYMechanics2D` and its required world/reference components. |
| 3D model | The user needs spatial bodies, pose, frames, world coordinates, multibody motion, animation, 3D driveline elements, contact/collision, flexible bodies, or any mechanical TY task that is not a 1D simplified model and not explicitly 2D planar. | Any relevant TY mechanical library except the 2D planar path library: commonly `TYMultibody`, `TYDriveline3D`, `TYContact`, `TYFlexBody`, and when needed `TYMechanics` / `TYDriveline` as confirmed compatible 1D submodels. |

If the route is ambiguous, ask one blocking clarification only when the modeling dimension changes the deliverable. Otherwise prefer the 1D simplified path only when the requested output is an equivalent/simplified model and does not require pose, animation, contact, flexible deformation, or spatial constraints. The route controls the first library search scope; still confirm real component paths, ports, and parameters before writing the model.

## Domain Additions

- Identify task type: new TY mechanical model, repair, example validation, or result review.
- Apply the entry path routing above: choose 1D simplified, 2D planar, or 3D before selecting TY sub-libraries.
- Classify whether the task is model building or library information retrieval. For information retrieval, prefer a bounded library/class overview and local filtering over repeated deep document reads.
- Before writing a model, run a short preflight: selected TY sub-library, component interface types, world/reference needs, expected degrees of freedom, key parameters, and the smallest physics sanity check. Include expected result variables only when result verification is in scope.
- For multibody models, ensure `TYMultibody.World` or equivalent world/reference component exists.
- For planar closed-loop mechanisms, use and report the cut joint strategy.
- Build the smallest checkable mechanical loop before adding losses, contact, flexible bodies, monitoring, or extra operating cases.
- Query real component parameters before assigning values.
- Query component docs in a staged way: first package/classes, then only the candidate components and interfaces needed for the current model. Avoid repeatedly querying the same component or subpackage.
- For 1D rotational chains, check grounding/reference and degrees of freedom before `check`: an inertia/load should not be rigidly grounded at both ends unless the intent is a locked element.
- For mixed 1D/3D or driveline/multibody models, confirm connector compatibility (`flange`, `frame`, signal ports, inner/outer world) before connecting across library boundaries.
- When the selected acceptance contract requires result evidence, verify only the applicable displacement, velocity, angular velocity, force, torque, reaction force, contact force, penetration, pose, joint, constraint, deformation, or modal variables.
- Open and judge multibody animation only when animation or motion-visual acceptance is explicitly requested. Do not add animation to a build/check/translate/simulate-only task.
- When result verification is required, retrieve only the minimum variables needed and compare them against a simple hand calculation or sign/trend expectation. Do not read results automatically after a successful simulation.
- Follow the parent shared standards for error classification, session evidence and bounded retries; use domain docs, a component-level minimal model or static inspection to isolate the cause instead of repeating failed calls.

## Repair Priority

Prefer the shortest blocking chain:

`TY library boundary -> component/interface confirmation -> world/reference -> structural connection -> equation balance/DOF -> parameters -> initialization/constraints -> solver -> result interpretation (only if required)`

Preserve existing valid structure and return to the failed parent Step/Gate after repair.

## Delivery Additions

In addition to parent delivery evidence, state:

- TY sub-library boundary, selected components, parameter sources, completed requested verification actions, and known risks; list verified variables only when result verification was in scope.
- Substitution reason and expected impact for any TY component substitution.
- Cut joint details for planar closed loops.
- Animation status and animation-based judgment only when animation was part of the requested acceptance contract.
- For information-query deliverables, state the query scope, libraries/classes inspected, and any deliberate omissions to show the result is complete enough without exhaustive token-heavy exploration.
- For generated model libraries or reusable packages, enter the parent Documentation route only for an explicit documentation request and follow its requested content and format. The default target is `Documentation(info=...)`; create separate Markdown only when explicitly requested. If documentation was not requested, mark documentation `not_required`; retain necessary code-level descriptions and parameter units without expanding them into formal documentation.
