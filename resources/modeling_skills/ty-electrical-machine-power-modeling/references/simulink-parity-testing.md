# Simulink Parity Testing

## Objective

The goal is not merely "it runs". The goal is controlled comparison against Simulink behavior when reference data exists.

## Preferred Test Sources

Priority order:

1. Simulink official `openExample`
2. Official example model or help-document case
3. User-specified case
4. Self-built minimal comparable scenario

## Minimum Test Count

- Reusable component packages require at least `2` comparison tests.
- Standalone cases are scenario files and do not need a `Tests` package, but each scenario still needs explicit purpose and experiment settings.

## What To Compare

At minimum compare:

- one key output
- one key internal state or intermediate signal when practical
- startup behavior
- step, switching, disturbance, or boundary behavior

## Error Rule

Default parity acceptance:

- maximum relative error `< 1%`

Also record when available:

- maximum absolute error
- mean relative error
- worst timestamp
- signal names and units

## Comparison Procedure

1. Align input source, initial values, sample interval, stop time, and measurement point.
2. Export Simulink curves.
3. Export Sysplorer curves.
4. Use `scripts/compare_series.py`.
5. Record the error report using `assets/parity-report-template.md`.
6. If parity fails, return to modeling or solver review before claiming delivery.

## Typical Failure Causes

- inconsistent initial values
- different discrete update ordering
- different hold or delay logic
- saturation, limit, or dead-zone behavior mismatch
- torque, source, or sensor sign convention mismatch
- unit or per-unit conversion error
- sample alignment error
- switching event landing on different time points

## Scope Rule

- If Simulink reference data is available, parity is mandatory.
- If Simulink reference data is not available, do not claim parity complete.
- In the no-reference case, report only `Sysplorer structure validation passed`.

## Reload Rule

- After any local `.mo` edit, reload the root `package.mo` before re-running translation or simulation.
- Do not assume on-disk edits are active in an already-loaded stale class tree.

## Solver Reference

- Read `references/solver-and-parity-policy.md` before freezing the final solver.
- Do not treat "discrete solve" as a universal requirement for these TY libraries.
