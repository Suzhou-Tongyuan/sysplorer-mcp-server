# Acceptance Checklist

Use this checklist before claiming the task is complete.

## Grade Definitions

### Complete Pass

All of the following are true:

- Requirement target is implemented.
- Parent closed-loop validation has passed for the required depth.
- Key user-facing variables have been verified.
- Diagram has been reviewed and is readable.
- The latest model text contains `Algorithm=InlineImplicitEuler` in the model-level experiment annotation.
- Solver, step size, and sampling choices are recorded.
- Final delivery package contains evidence and known limitations.

### Partial Pass

Use this when:

- The minimum closed loop is runnable and verified for core behavior,
- but some advanced details, scenarios, or refinements are still incomplete.

This grade still requires:

- A runnable model
- At least one successful verification round
- Diagram review evidence
- Explicit list of missing scope

### Plan Only

Use this when:

- The scenario, mapping, and parameter strategy are clear,
- but the model is not yet fully built or verified.

This grade requires:

- Structured requirement understanding
- Component mapping
- Parameter assumptions
- Clear next actions and blockers

### Not Complete

Use this when:

- The model cannot pass the current gate,
- or the evidence is too weak to support any stronger grade.

## Mandatory Evidence Checklist

- Requirement understanding exists.
- Component mapping exists.
- Parameter table and assumptions exist.
- Successful tool actions are recorded.
- Diagram review result is recorded.
- Solver, step size, and sampling information are recorded when simulation is involved, including `Algorithm=InlineImplicitEuler`, `InlineIntegrator`, `Interval`, and `IntegratorStep`.
- Key result variables are recorded when verification is involved.
- Repair history is recorded if failures occurred.
- Known limitations and next steps are recorded.

## Hard Stop Conditions

Do not grade the task above `Plan Only` if any of the following are missing:

- No runnable model
- No diagram review evidence
- No solver or step-size evidence for simulated models
- The latest simulated NPSLibrary model lacks model-level `Algorithm=InlineImplicitEuler` experiment evidence
- The simulated model is left on Dassl or an unspecified default solver
- No key variables for claimed verification
- No explicit statement of unresolved blockers
