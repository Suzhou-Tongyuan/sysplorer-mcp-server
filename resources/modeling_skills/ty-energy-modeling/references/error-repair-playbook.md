# Error Repair Playbook

Existing concrete failures are led by the independent debugging entry defined by the parent; new-build failures stay in the original task. Apply the smallest repair and rerun only the affected requested stages. `../../ty-sysplorer-modeling-rules/references/shared-standards.md` owns session/error/retry and automatic-layout writeback boundaries; this is domain diagnosis only.

## Repair Order

1. Session and tool readiness
2. Allowed-library and class existence
3. Boundary/source completeness
4. Connection topology
5. Interface compatibility
6. Parameter type, range, unit, or missing value
7. `CheckModel`
8. `TranslateModel`
9. Simulation stability
10. Result interpretation

## Common Rules

- If a connector is missing or incompatible, inspect ports and repair topology first.
- If a parameter is wrong, repair only the affected parameter set first.
- If a proposed class lies outside the energy-subsystem set, check the parent project library set and assigned support-domain responsibility before reporting a gap. Do not reject or remove already-selected standard/support components.
- If the model is underconstrained or overconstrained, add the minimum missing boundary condition or remove the minimum conflicting connection.
- If translation fails after `CheckModel` passes, repair the diagnosed element and re-run `check_model` before translating again.
- If simulation diverges, tune solver, step size, or tolerance before simplifying structure.

## Do Not

- Invent undocumented classes
- Delete required energy subsystems just to pass
- Override units casually
- Repeat the same failed repair loop without a new hypothesis
