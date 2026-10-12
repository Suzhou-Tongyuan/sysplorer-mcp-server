# Execution Standards

This file defines hard execution standards for TY hydraulic, thermal-hydraulic, and pneumatic Sysplorer tasks.

## Parent Gate Mapping

The authority is `../../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md`; session/tool discovery and retries belong to parent shared standards and are not extra gates.

| Parent gate | Fluid-domain addition |
|---|---|
| Gate 1 — scope and authorization | Task/system type, permitted edits, requested verification depth and output/image/report scope. |
| Gate 2 — evidence and component boundary | Selected TY/standard components for the fluid subsystem; medium, ports, main loop, control chain and units. |
| Gate 3 — construction | Minimal loop and local parameter assumptions; planned topology and applicable Placement/Line/Diagram annotations. |
| Gate 4 — check | Check exact required targets and applicable capacitor/resistive topology in the Gate 1 mode: offline tasks use static review; authorized live checks record automatic layout writeback. Actual model check failure blocks dependent runtime actions without authorizing patches. |
| Gate 5 — validation design | Requested translation/simulation; result/KPI/curve/animation evidence only when required. |
| Gate 6 — diagram acceptance | Newly created or modified graphical targets, structured evidence first and images according to request/capability. Visual defects do not prohibit check, translation or simulation. |
| Gate 7 — delivery evidence | Accurate per-stage status, unique current model, domain findings and remaining gaps; formal reports only when requested. |

Read-only, Documentation-only and unchanged graphical targets use `not_required` for change-based Gate 6. Untouched inherited objects/layers are not expanded. An explicit diagram-review/image request retains its requested evidence.

## Non-Negotiable Domain Rules

- Within the selected fluid subsystem, prefer TY system-level components for the commercial portion unless component design is requested. Preserve sufficient standard-library components and selected other domains; this list does not whitelist the entire project.
- Select `TYHydraulics`, `TYThermalHydraulics`, or `TYPneumatics` according to fluid domain before choosing component models.
- Select `TYOilMedia` for hydraulic and thermal-hydraulic media and `TYGasMedia` for pneumatic media unless the user provides a specific compatible medium.
- Do not silently assume 4/3 valve center type, single-acting actuator return mode, pump type when performance matters, thermal boundary conditions, or pneumatic exhaust boundary.
- For directional-valve `Signal` control inputs, convert current-type commands to an `mA` numeric value before entry and convert voltage-type commands to a `V` numeric value before entry. Do not reinterpret current commands in SI base-unit `A` when the interface semantics are `mA`; a user command such as `40 mA` must be entered as `40`, not `0.04`.
- For 3-position directional valves, enforce the signal polarity convention left negative, center `0`, right positive unless the project documents a different polarity explicitly.
- Do not deliver an official example, wrapper, or `extends` chain as the user-owned model unless requested.
- State every equivalent component substitution with reason and risk.

## Graphical Completion Rules

- Key instances must be placed in the diagram with `annotation(Placement(...))`.
- Key instances must follow a zone-based layout with no overlaps, no crowding, and no out-of-bounds placements.
- For model-creation tasks, every planned visible `connect(...)` must include `annotation(Line(points=...))`.
- The model must include `Diagram(coordinateSystem(...))`.
- Applicable diagram review uses structured Placement/Line/Diagram, instance/connection counts, anchors, coordinate/routing and readability evidence as its common basis. Images are supplementary by request and capability; do not turn inferred geometry into a claimed visual observation. Keep unmet explicit image requests visible.
- If the diagram does not display the created model normally, the model-creation task is incomplete even if the model tree, source text, check, or simulation succeeded.

## Reporting Rules

- Separate executed facts from assumptions.
- Report exact tool actions that succeeded in the current session.
- Report unresolved items as `to confirm` / `待确认`.
- Do not output intermediate iteration versions unless the user explicitly requests them.
- If a gate cannot be passed, state the blocker and the next executable action instead of claiming completion.
