# Solver And Parity Policy

## Default Position

- Do not assume `TYMotor`, `TYElectricPower`, or `TYElectrical` models must always use discrete solving.
- These libraries often model circuit-level, switching, drive-level, or electromechanical-coupled systems. Solver choice must match topology, stiffness, switching behavior, and the validation target.

## Parity Baseline For This Project

When the user requests the established Simulink parity baseline:

- Simulink: fixed-step `5e-5` with `backward Euler`
- Sysplorer baseline: step `5e-5` with `ImplicitEuler`

This is a parity baseline, not a universal solver mandate.

## Engineering Validation Cases

For non-parity engineering validation:

- fixed-step solvers are allowed
- variable-step solvers are allowed
- discrete solving is allowed only when the model structure or validation target truly requires it

Record why the chosen solver matches the case.

## Alternative-Solver Sanity Check

If the first solver choice produces suspicious behavior:

1. compare at least one alternative solver before changing topology
2. record both solver choices
3. state whether the issue looked numerical or structural

## InlineImplicitEuler Warning

- If a TY circuit, power-electronics, or motor-drive case shows zero speed, zero current, flat outputs, or stale switching under `InlineImplicitEuler`, retry with `ImplicitEuler` before declaring the model wrong.
- Record the observation explicitly in the validation report.

## Required Solver Record

Every delivery should record:

- solver name
- step size or variable-step setting
- stop time
- whether the case is parity validation or engineering validation
- any solver-dependent behavioral difference that remains relevant
