---
name: ty-sysblock-diagram-modeling
description: >-
  Create, edit, repair, lay out, audit, and verify concrete Sysblock block-diagram
  models in Sysplorer with SysplorerEmbeddedCoder, including subsystems,
  parameters, ports, feedback, simulation, compact layout, and StateMachine
  Charts. Use for actual Sysblock model-structure work, saved/readback layout
  repair, or repeatable layout evaluation. Concrete existing-model fault diagnosis
  or repair is led by ty-sysblock-model-debugging, which reuses these edit/delivery
  constraints without restarting this workflow. Do not use for Modelica physical
  modeling, pure API lookup, requirements architecture, or persistent MBD test
  planning.
metadata:
  short-description: Sysblock diagram creation, layout, and verification guidance
  version: 1.3.1
  managed-by: sysplorer-mcp
---

# Sysblock Block Diagram Modeling

Use this skill directly for ordinary Sysblock construction and editing. Concrete existing-model failures are led by `ty-sysblock-model-debugging`, which reuses this skill's applicable API, layout, save/reload, and audit constraints. When loaded as those constraints, stay in the debugger; do not reroute or restart its baseline. Construction-stage failures retain the original task context. Build and edit topology through official Sysplorer APIs; never write or patch Sysblock `.mo` topology text.

## Core workflow

1. Classify the task as parameter-only, topology, layout, StateMachine, repair, audit-only, or delivery.
2. Freeze controller boundary, semantics, ports, types, dimensions, units, sample time, and required verification.
3. Resolve only the APIs the task will call with `scripts/api_contract_resolver.py`. Known contracts require zero probes. For an unknown API, query its exact documentation once; treat `ok=true` with empty `help_text` as unresolved and use the targeted stdout/signature fallback in `references/runtime-contracts.md`. Probe one unresolved behavior once in a disposable task-owned model. Never probe on the target model or enumerate the full API by default.
4. For topology/layout changes, create a coordinate-free `sysblock-layout-input/v1` and run `scripts/layout_input_tool.py prepare|audit`. Plan before model mutation with `scripts/layout_plan_tool.py block|statechart`; use block `--mode preconnect` when `RouteLine` will run after connection. Read `references/layout-workflow.md`.
5. Create components, configure variable ports, connect with `ConnectPort`, check every API return, and stop dependent work on failure. Use `RouteLine` only after placement is stable; read back nontrivial explicit routes.
6. Save with the lifecycle sequence in `references/runtime-contracts.md`. Reopen/force-reload the exact saved target before final evidence collection.
7. Execute every check, test, translation, simulation, layout review, and delivery action required by the parent modeling rules.
8. Run `scripts/audit_sysblock_model.py` on the final saved model and raw structured evidence. Exit code 0 confirms only this Sysblock evidence audit; claim completion only after all parent-required validation succeeds.

## Hard stops

- Do not use `SetModelText`, handwritten `connect()`, text patches, or `AddConnection`.
- Never call or use any screenshot, screen-capture, diagram-image export, image-viewing, OCR, or visual-analysis tool, and never use screenshots, exported images, OCR results, or human visual judgments as planning, modeling, audit, or delivery evidence. Use only structured plans and saved/force-reloaded API or static-annotation readback.
- Use `ConnectPort`; grip points contain intermediate bends only, never endpoint anchors.
- Keep Inports left and Outports right of the complete route envelope. Keep interface-adjacent segments horizontal and audit the saved/readback geometry.
- Treat feedback as declared signal paths, not as a synonym for `UnitDelay`. Add delay only when frozen execution semantics require loop breaking.
- Keep ordinary blocks at standard size: when calling `AddComponent` for an ordinary block, pass only `type`, `model`, `name`, `x`, and `y`; do not pass width or height. Size each SubSystem, Chart, State, vector/bus block, Mux/DeMux, and required switch independently from its content and ports.
- Treat frames, name bands, port labels, parameter text, and notes as no-crossing regions. Reject overlap, insufficient clearance, avoidable crossings, shared positive-length lanes, and unambiguous one-to-one multi-input order inversions; judge ambiguous multi-target, multi-output, or cross-layer relations by authoritative route geometry.
- For StateMachine transitions, require adequate x/y projection overlap before routing. When insufficient, adjust state geometry in this order: translate, bounded scale with neighbour push, then route. Never retry corner combinations as the primary repair. Read `references/state-machine.md`.
- A plan or manifest is not proof that the saved model passed. The saved/readback audit uses force-reloaded structured evidence and connection-integrity checks.
- Audit-only work must not write layout; compare the target hash before and after.
- `CheckModel` is a structural result, not proof of complete validation.

## Read only what the task needs

| Need | Authority |
|---|---|
| API contracts, return values, ownership, load/save/reload | `references/runtime-contracts.md`, `references/api-contracts.json` |
| End-to-end build, check, test, and delivery order | `references/modeling-workflow.md` |
| Geometry-free planning, routing, sizing, readback audit | `references/layout-workflow.md` |
| Chart semantics, API, transitions, labels, O'Clock | `references/state-machine.md` |
| Block selection and parameters | `references/block-reference.md`; load `references/sysblock-parameters.json` only for unresolved parameter names |
| Symptom-directed recovery | `references/troubleshooting.md` |
| Explicit skill-revision effectiveness evaluation only | `references/layout-evaluation.md` |

## Production tools

- `scripts/api_contract_resolver.py`: read-only exact-contract resolver; not a mandatory stage when no ModelingPy API is needed.
- `scripts/layout_input_tool.py`: `prepare` and `audit` coordinate-free inputs.
- `scripts/layout_plan_tool.py`: `block` and `statechart` planning. The StateMachine planner supports cyclic graphs and records geometry adjustments.
- `scripts/audit_sysblock_model.py`: one read-only structured-evidence audit from the saved model and raw evidence.

Development evaluation tools and tests live under `tests/` and must not run during ordinary model construction, repair, audit, or delivery.

## Delivery

Report the model path and hash, task/change scope, check/test/simulation results required by scope, audit report path, failure codes if any, and remaining risks. Never replace required validation with a cached hash or a local audit result.
