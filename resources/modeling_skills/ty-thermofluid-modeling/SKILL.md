---
name: ty-thermofluid-modeling
description: 在 Sysplorer 中构建、修复、验证、评审并打包热流体、换热、空气处理、通风、HVAC 和环境控制模型。当用户明确指定 `TYMedia`、`TYThermoFluidSys`、`TYAirTreatmentAndVentilation` 或相关商业库路径，或父规则/有效上下文已选定这些商业组件时使用。未指定库先由父规则判断标准库能力；满足则使用标准库，不足则保留可用标准库部分并补充商业组件，再加载本技能。这是一个领域附加技能，必须仅在 `ty-sysplorer-modeling-rules` 之后使用。
metadata:
  short-description: TY thermo-fluid, HVAC, and ventilation modeling guidance
  version: 1.1.3
  managed-by: sysplorer-mcp
---

# TY Thermofluid Modeling

Use this only as a thin domain add-on to `ty-sysplorer-modeling-rules`. The parent skill owns routing, seven gates, layout timing, repair loop, and delivery evidence.

## Parent Contract and MCP 0.4

Use `../ty-sysplorer-modeling-rules/references/shared-standards.md` as the authority for MCP classification, session reuse, failure parsing, and retry control; use `../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md` for validation depth, Gate 6, and completion status. Offline/source-only tasks make no session calls. Existing concrete failures are led by the independent debugging entry defined by the parent; this domain skill supplies targeted evidence without restarting a build. Failures during a new build remain in the original task.

Stop at the requested terminal stage. Result variables, KPI, plots, animation, and formal reports are required only when requested or necessary for the agreed acceptance criterion; otherwise mark them `not_required`. Do not infer proxy metrics merely to fill a checklist. A successful simulation and verified physical results are separate claims.

MCP 0.4 uses `model_inspect` for classes/components/ports/text queries, `compare_model` for comparisons, and `model_manager` for lifecycle operations. `call_code` accepts only `run_sysplorer_api` or its `run_script` alias with a required object `payload` and explicit ModelingPy import. Check/translate/simulate may automatically write layout back to a loaded user file, even without `reload_mo_path`; they are not read-only review tools. Follow the parent authorization boundary and record any actual graphical change under Gate 6.

## Minimal Reading

All `references/...` and `workflows/...` paths in this skill are relative to **this skill directory** (the folder that contains this `SKILL.md`), not the workspace root or any parent `skills/` directory.

| Need | Read |
|---|---|
| Requirement classification | `references/requirement-map.md` |
| Library / component mapping | `references/library-selection.md`, `references/component-map.md`, `references/fallback-strategy.md` |
| Media | `references/media-selection.md` |
| Parameters / modeling rules | `references/parameter-rules.md`, `references/modeling-rules.md` |
| Validation | `references/validation-rules.md` |
| Repair | `references/common-errors.md` |
| Acceptance | `references/acceptance-checklist.md`, `references/output-contract.md` |
| Manual lookup | `references/manual-index.md` only when concise references are insufficient |

## Specialized Workflows

- Build from scenario: `workflows/build-from-scenario.md`
- Repair existing model: `workflows/repair-existing-model.md`
- Verify example or existing model: `workflows/verify-example.md`

## Domain Additions

- This commercial-library path, including standard/commercial combinations, requires `Modelica 4.0.0.TY.1`. A conflicting user/project version is a reported dependency conflict; do not silently rewrite it. The standard-only override of the parent alone does not apply here. Limit the thermal-library boundary to its responsible subsystem and preserve parent-selected standard and support-domain components.
- Identify task type: new build, repair, example validation, or result review.
- For an authorized runtime build using `TYThermoFluidSys` or `TYAirTreatmentAndVentilation`, preflight only the selected libraries/dependencies and minimum representative model to the requested depth. Source-only/read-only work does not acquire live checks; check-only work does not acquire translation or simulation.
- If the preferred domain library fails preflight or repeatedly fails at the same minimal simulation step, do not keep scaling up the full model blindly. Enter an explicit fallback decision: either report the domain library as blocked, or downgrade to an approved substitute library only when the user's goal is still satisfiable.
- Choose media and phase assumptions before committing topology.
- Build the minimum energy/fluid path first, then add controls, sensors, and secondary loops.
- If falling back from a domain library to a substitute such as `Modelica.Fluid`, explicitly state the original target library, fallback trigger, actual substitute library, lost library-specific assumptions, and any remaining fidelity gaps.
- For delivered graphical models, every instantiated component must carry an explicit `annotation(Placement(...))` so its icon appears in the diagram layer; relying on tool auto-placement is not acceptable for delivery.
- When instantiating and arranging components, preserve the component's default icon size and aspect ratio whenever possible; prefer moving components over stretching, elongating, or compressing them merely for alignment.
- Every required `connect(...)` must also be visible in the diagram layer via explicit `annotation(Line(...))`; semantic connectivity without visible routing is not acceptable for delivery. When two array interfaces are connected one-to-one, use a single array connection such as `connect(a[:], b[:])` instead of expanding redundant per-element lines.
- Top-level deliverable models should include at least a basic `Icon(...)` and `Diagram(...)` coordinate system annotation unless the parent workflow explicitly replaces them later with smart layout output.
- State actual libraries and actual media used.
- Verify pressure, temperature, flow, humidity, enthalpy, heat-transfer rate, compressor power, COP, or user-specified metrics as applicable.
- Within the requested verification scope, treat wrong medium, missing boundary/reference, impossible pressure/temperature, divergence, or unverified required variables as failures. If result verification is outside scope, its status is `not_required` and a successful requested simulation may complete the task.
- Control iteration cost using the parent shared standards: distinguish infrastructure retries, retries of the same repair hypothesis, and new task evidence. Stop an unchanged failing strategy without new evidence and review medium, boundaries, topology, or initialization; execute only the requested check/translate/simulate depth.
- For diagram tasks, parent Gate 6 still controls layout timing and re-check requirements. Satisfy layout acceptance from model structure and tool-readable evidence: inspect `Placement`, `Line`, coordinate systems, connector endpoints, and any available layout-tool diagnostics.
- Image export/inspection follows parent Gate 6: use it when explicitly requested or when both capabilities are available and useful. If unavailable, stop retrying and report the missing capability; an explicit image delivery remains unfulfilled separately from functional/structural acceptance. Do not claim visually observed properties without inspecting images.

## Repair Priority

Use the following diagnostic order only up to the requested terminal stage; it does not require every later validation action:

`medium selection -> boundary/reference -> topology -> parameters -> discretization/resistance organization -> initialization -> translation -> simulation -> result interpretation`

Preserve existing valid structure and return to the failed parent Step/Gate after repair.

## Delivery Additions

In addition to parent delivery evidence, state:

- Temporary assumptions, media assumptions, remaining risks, unresolved items, and next-step recommendations.
- Whether the preferred library and the actual delivered library are the same; if not, state the fallback reason and the resulting fidelity downgrade.
- Whether all required process, heat, and control connections have explicit diagram-layer evidence such as valid `annotation(Line(...))`, rather than only semantic connectivity.
- The layout review method actually used: structural/code inspection, layout-tool diagnostics, and optional exported-image inspection. Include an export path/status only when export was requested or attempted. Lack of image capability alone does not leave structural layout acceptance open.
- If delivering a library, state the top-level package and bound dependencies.
