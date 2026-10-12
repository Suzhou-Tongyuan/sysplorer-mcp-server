# Build From Scenario

Use this workflow for a new TA whole-vehicle model, subsystem model, or TA-based user model library.

## Read

0. `../references/preflight-checklist.md`
1. `../references/requirement-map.md`
2. `../references/library-selection.md`
3. One selected `../references/library-cards/<library>.md`
4. `../references/build-rules.md`
5. `../references/diagram-layout-rules.md` when source-level layout annotations are created or changed
6. `../references/package-design.md` when the task needs vehicle-specific business-layer design for a user library

For multi-library whole-vehicle models, add `../references/combination-rules.md` before reading support library cards.

## Do

- Identify task type, main analysis goal, vehicle architecture, target operating case, and required landing level.
- Select exactly one primary TA library before adding support libraries.
- Use official examples/classes as structural, parameter, result-variable, and diagram references only. Do not directly copy or `extends` a complete official example, complete vehicle architecture, or complete subsystem template as the new deliverable.
- Modeling difficulty, missing internal wiring, or failed repair attempts do not relax the previous rule. If blocked, reduce scope, hand-build visible topology, or report the blocker.
- Before writing model content, create a build contract with: primary goal, vehicle architecture, operating case, landing level, primary/support libraries, reference examples/classes, top-level components, exposed interfaces/buses, and expected result variables.
- Define topology, hierarchy, interfaces, and vehicle business-layer placement before writing model content. If these are not explicit, stop and finish the build contract first.
- For common requests, start from the selected library card quick-start entries instead of broad recursive library exploration: `TAEconomy` for acceleration/cycle/economy architectures, `TADynamics` for chassis/KC/six-wheel dynamics, and `TAThermalSystem` for cabin/HVAC/refrigerant loops.
- Build the deliverable as explicit component instances and `connect(...)` statements. Use inheritance only for small interfaces, connectors, records, replaceable partial bases, or user-owned abstractions that do not hide the requested topology.
- Before `check_model`, run `../scripts/audit_modelica_source.py` when a `.mo` file path is available. For a packaged model, pass `--dependency-root` with the already authorized top-level package directory; only enclosing `package.mo` files up to that boundary are read. Without the option, only the target file is read; do not invent an authorization root or repeat dependencies in every child model. When no file is available, audit the authorized source evidence manually: standalone or top-level package dependency fixes Modelica at `4.0.0.TY.1`; no full-template/example `extends`; key components and connections are visible; no unsolicited parameter overrides; no support libraries beyond the build contract.
- Treat a failed source audit as a stop condition before `check_model`, translation, or simulation.
- Before simulation, verify the requested duration is set through the actual stop-time setting. Treat result probe times such as `target_time` as validation/readback times unless the active tool schema explicitly says otherwise.
- If construction is timing out, validate the smallest runnable skeleton or subsystem matching the build contract and report the unresolved interface/blocker.
- Keep whole-vehicle assemblies and reusable subsystems separated when a user vehicle library is created.
- Return to the parent `ty-sysplorer-modeling-rules` gates and stop at the requested terminal stage. Expected result-variable fields are `not_required` when no result criterion is agreed; do not create KPI, plots, animation, or formal reports merely to complete a template.

## Report

- Before final delivery, read `../references/output-contract.md` and answer `../references/acceptance-checklist.md`; do not report completion if any acceptance item fails.
- Build contract, primary library, support libraries, reference examples/classes, official/example usage status, vehicle scope, model entry point, source-audit result, layout-annotation status, and current validation level.
