# NPS Common Errors

## Contents

1. Parameter and syntax issues
2. Connection and interface issues
3. Translation and initialization issues
4. Simulation setup issues
5. Result readback and verification issues
6. Diagram and delivery issues

## 1. Parameter and Syntax Issues

### String parameters are written without quotes

Symptoms:

- Translation fails on record or text-like parameters.
- Parameter assignment looks visually correct but Sysplorer rejects it.

Checks:

- Confirm whether the target parameter is a string or enumeration-like text input.
- Add quotes exactly where the model expects text input.

### Repeated iteration happens without understanding the component first

Symptoms:

- The model is repeatedly rewired or retuned, but the root cause remains unverified.
- A component's pin mapping, rotation effect, internal structure, or parameter meaning is still unclear.
- Full-model iterations continue before any minimal local validation is done.

Checks:

- Stop further full-model edits until the uncertain component behavior is inspected.
- Read the component documentation, class description, and interface definition first.
- Build a minimal validation model for the uncertain component or local subcircuit before returning to the full system.

### Experiment or configuration keys use the wrong spelling or case

Symptoms:

- Simulation settings appear ignored.
- The model runs with unexpected defaults.

Checks:

- Verify exact parameter names and casing for experiment dictionaries or configuration records.
- Do not assume uppercase and lowercase are interchangeable.

### Non-editable parameters are assigned directly

Symptoms:

- Translation fails or the model rejects assignments.
- The parameter is visible in text but not meant to be edited externally.

Checks:

- Confirm whether the parameter is editable in the component definition.
- If not editable, change the correct exposed parameter or use a different component configuration path.

## 2. Connection and Interface Issues

### Single-phase and three-phase interfaces are connected incorrectly

Symptoms:

- Port-domain mismatch in check or translate.
- A model compiles only after unsafe edits to unrelated equations.

Checks:

- Verify connector type and phase count on both sides.
- Use official conversion blocks such as `PlugToPin_p` or `PlugToPins_p` when needed.
- Verify whether the ports are one-dimensional versus three-dimensional, or scalar versus vector interfaces.
- Do not work around this error by deleting the connected component or editing unrelated equations first.

### Ground or reference is missing or duplicated

Symptoms:

- Floating nodes, abnormal voltages, unstable currents, or failed initialization.

Checks:

- Ensure each isolated electrical island has a valid reference.
- For isolated transformer primary and secondary sides, verify whether both sides need their own reference.
- Do not add duplicate grounds if a subsystem already contains an internal reference.
- In electrical fault diagnosis, check this item first before deeper parameter tuning or topology replacement.

### The model is structurally connected but diagram review is impossible

Symptoms:

- `check` passes, but exported diagrams are unreadable.
- Important lines overlap or are invisible.
- A text-connected model cannot be reliably continued from the GUI workflow.
- A later text edit changes wiring after an earlier diagram review, so the review evidence is stale.
- Electrical interface lines appear black without a clear library-specific reason.
- The model reached `check` or later stages even though graphical construction was bypassed by direct full-model text injection.

Checks:

- Add or repair `Placement(...)` and `Line(points=...)` annotations.
- Confirm the model still contains `Diagram(coordinateSystem(...))`.
- Export the diagram once before accepting the build.
- If text `connect(...)` was added without a matching `Line(points=...)`, treat the diagram as incomplete even if check passes.
- If the task required graphical modeling, verify whether GUI-side placement and wiring were preserved instead of silently falling back to text-only edits.
- If wiring changed after the last review, redo the review from the latest model state instead of trusting the old evidence.
- For black electrical lines, check whether explicit `color={0,0,255}` is missing or overwritten; only keep black when the library convention is documented and intentional.
- If GUI construction was bypassed by `SetModelText`, `SetModelCode`, or direct full-model text injection, treat the current build as failed graphical modeling and return to the graphical repair path.

## 3. Translation and Initialization Issues

### Equation imbalance or structural singularity

Symptoms:

- Translation fails with underdetermined or overdetermined system messages.

Checks:

- Re-check missing support blocks such as `Powergui`, references, measurement reference points, or boundary conditions.
- Re-check `Ground / Reference` placement as the first required item, including duplicated grounds and wrong-side grounding on isolated sections.
- Re-check unconnected ports, duplicate connections, wrong connection direction, and interface dimension mismatch before touching topology.
- Remove duplicate or conflicting constraints only after connection and interface issues have been ruled out.

### Discrete control and continuous circuit initialization conflict

Symptoms:

- Translation or initialization fails around controller states, PWM, or sampled blocks.

Checks:

- Re-check the relationship among switching period, sampling period, and control period.
- Start from the default discrete baseline before introducing mixed-mode complexity.

### Load-flow initialization is incomplete

Symptoms:

- Load-flow models fail before time-domain simulation starts.

Checks:

- Confirm `Powergui`, `LoadFlowBus`, and slack or control node roles are present and consistent.
- Re-check P/Q settings, base voltage, and transformer connection mode.

## 4. Simulation Setup Issues

### Step size is too large for the fastest relevant period

Symptoms:

- Severe ripple distortion, aliasing, false oscillation, or unstable controller behavior.

Checks:

- Start from `step <= T/10`, where `T` is the fastest relevant switching or sampling period.
- If deviating from this rule, record the reason explicitly.

### Solver choice is inconsistent with the model family

Symptoms:

- Switching model results look non-physical or extremely noisy.

Checks:

- For switching, PWM, and PLL-heavy models, start from a discrete baseline with inline implicit Euler.
- Change solver only after documenting why the default baseline is insufficient.

## 5. Result Readback and Verification Issues

### Result variable is queried before confirming it exists

Symptoms:

- Result readback fails or returns empty data.

Checks:

- Confirm the exact variable name first.
- Probe availability before bulk result extraction.

### Verification conclusion is given without minimum evidence

Symptoms:

- The report says "correct" without key variables, settings, or figures.

Checks:

- Include solver, step size, key observables, and acceptance grade.
- Follow `references/acceptance-checklist.md` and `references/input-output-contract.md`.

## 6. Diagram and Delivery Issues

### Only technical success is reported, but no delivery evidence is packaged

Symptoms:

- The model runs, but there is no final report, no acceptance level, and no diagram review result.

Checks:

- Package the result with `templates/acceptance-report-template.md`.
- Include diagram review, successful tool actions, solver and step evidence, and known limitations.
