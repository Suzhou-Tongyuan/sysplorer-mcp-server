# NPS Domain Rules

## Contents

1. Sub-library priority
2. Common mapping rules
3. Diagram and connection rules
4. Grounding and electrical reference rules
5. Simulation setup baseline
6. Interface conversion rules
7. Parameter completion baseline
8. Result review and acceptance cues

## 1. Sub-library Priority

Use the following discovery order unless the scenario strongly suggests otherwise:

1. `NPSLibrary.Sources`
2. `NPSLibrary.PowerSystem`
3. `NPSLibrary.PowerElectronics`
4. `NPSLibrary.Motors`
5. `NPSLibrary.Sensors`
6. `NPSLibrary.Utilities`

Rules:

- Prefer same-name components first.
- If there is no same-name component, map by physical function.
- If the user explicitly names a topology or key component, continue searching inside `NPSLibrary` for other families, class paths, or conversion blocks before changing the requested structure.
- Do not pull in components from other power-system libraries unless the user explicitly requests or approves that library exception.
- Do not mix a high-level converter block with its internal detailed semiconductor reconstruction unless the task explicitly requires secondary development.
- Keep the minimum closed loop small before adding observers, protection, and controller refinements.

## 2. Common Mapping Rules

| Intent | Preferred sub-library or blocks | Mandatory supporting blocks | Typical observables |
|--------|---------------------------------|-----------------------------|---------------------|
| Three-phase source network | `Sources`, `PowerSystem`, transformer, line, load | `Ground` or reference, `Powergui`, measurement blocks | Node voltage, line current, P/Q, transformer variables |
| Grid-tied inverter | Converter bridge, filter, grid boundary, `PLL`, PWM, dq controller | `Powergui`, voltage/current measurement, P/Q measurement | Grid current, PCC voltage, DC bus voltage, modulation, PLL angle |
| Boost or Buck converter | Power-electronics switch stage, diode, inductor, capacitor, load | `Ground`, PWM, sensors | Output voltage, inductor current, duty ratio |
| Bidirectional DCDC | Bidirectional switch bridge, inductive branch, storage side, control | `Ground`, current and voltage sensors, PWM | Bus voltage, transfer current, charge/discharge direction |
| Motor drive | Inverter, motor, transforms, PI, speed loop | `Powergui`, current/speed/angle sensors | Speed, torque, dq current, controller output |
| Load-flow network | Source, transformer, line, load, `LoadFlowBus` | `Powergui`, P/Q constraint blocks | Voltage magnitude, phase angle, branch P/Q |

Load-flow reminder:

- Ask first whether load-flow initialization is desired; when it is, define bus roles explicitly and include `LoadFlowBus` plus `Powergui` load-flow initialization.
- Even outside dedicated load-flow studies, load-flow initialization can be a valid default aid for reaching steady state faster when the scenario fits.

## 3. Diagram and Connection Rules

These are hard reviewability rules, not optional styling suggestions.

- Every placed component should carry `annotation(Placement(...))`.
- Every connection that must be reviewable on the diagram should have visible `annotation(Line(points=...))` in addition to the real `connect(...)`.
- When a `connect(...)` is added or changed in text, repair the corresponding diagram `Line(points=...)` in the same edit round.
- A prior diagram review becomes stale as soon as later wiring edits change the connection set; rerun the review against the latest model state.
- For graphical wiring tasks, prefer GUI-side `ConnectPort`; do not use deprecated `AddConnection`.
- Do not treat direct text wiring as equivalent to GUI wiring when the requested deliverable is a GUI-reviewable diagram.
- For electrical-interface wiring, prefer explicit `color={0,0,255}` as the default visible convention unless the library already documents another standard.
- Keep `Diagram(coordinateSystem(...))` on the model so the layout remains exportable and stable.
- Route main power lines first, then sensing lines, then control lines.
- Avoid crossing power-path lines through dense control areas when a cleaner orthogonal route is available.
- Keep source -> conversion or network -> load as the dominant left-to-right or top-to-bottom visual chain.
- After major edits, export the diagram or use `smart_layout` plus diagram export once before claiming completion.
- Before `check`, confirm from the latest model text or latest exported diagram that the critical `connect(...)` set still maps to reviewable `annotation(Line(...))`.
- If an electrical line is rendered black, verify whether the black color comes from missing explicit color, overwritten annotation, or a valid library convention before accepting the diagram.
- If the model checks successfully but the diagram is unreadable, Step 5 and final acceptance are not complete.

## 4. Grounding and Electrical Reference Rules

- Add the correct electrical reference for each isolated electrical island.
- For transformer-isolated primary and secondary sides, verify whether both sides need their own reference ground.
- If a subsystem already contains an internal reference or grounding mechanism, do not add a duplicate external ground blindly.
- When results look unstable, first re-check missing reference points before tuning controllers.
- For three-phase source or network cases, ensure phase sequence, polarity, and winding connection mode are consistent before simulation.
- During error diagnosis, check `Ground / Reference` as the first required item before deeper parameter or topology changes.
- Treat missing, duplicated, or wrongly sided grounding as a first-class root cause for `check`, `translate`, initialization, and abnormal-result failures.

## 5. Simulation Setup Baseline

Use the following mandatory baseline for every NPSLibrary modeling case that involves simulation:

- Force the model-level experiment setup to use inline implicit Euler: `Algorithm=InlineImplicitEuler`. Do not accept Dassl or an unspecified default solver for NPSLibrary simulation cases.
- Write the simulation setup in the final model annotation before `check`, `translate`, or `simulate`:

```modelica
annotation(
  experiment(
    Algorithm=InlineImplicitEuler,
    InlineIntegrator=true,
    InlineStepSize=false,
    Interval=<step>,
    StartTime=0,
    StopTime=2,
    Tolerance=0.0001,
    IntegratorStep=<step>,
    StoreEventValue=0),
  uses(NPSLibrary(version="*")));
```

- Use `5e-5` as the normal default for `<step>`. Use a smaller step such as `1e-5` when required by PWM frequency, the fastest physical sampling step, the control period, or observed numerical behavior.
- Keep `Interval` and `IntegratorStep` equal unless the case explicitly documents why they must differ.
- Record switching period, sampling period, control period, `Algorithm`, `InlineIntegrator`, `Interval`, and `IntegratorStep` together.
- Use `step <= T/10` as the practical default rule when `T` is the fastest relevant period and no stronger rule is available.
- Sampling period should equal the control period or stay in a stable integer-multiple relationship unless there is a clear reason otherwise.
- In load-flow scenarios, make the `Powergui` or `LoadFlowBus` initialization mode explicit while still keeping `Algorithm=InlineImplicitEuler` for simulation.
- Do not present simulation results without proving that the latest model text contains the required inline implicit Euler experiment annotation.

## 6. Interface Conversion Rules

- Do not directly force-connect mismatched single-phase and three-phase connectors.
- When converting among electrical connector forms, prefer official conversion blocks such as `PlugToPin_p` and `PlugToPins_p` when applicable.
- If the scenario uses vectorized or multi-phase interfaces, make the dimension and phase meaning explicit in the parameter record.
- When a port-domain mismatch appears during check or translate, solve the interface model first instead of patching downstream equations.
- Treat one-dimensional versus three-dimensional interfaces, scalar versus vector ports, and phase-count mismatch as hard compatibility checks, not optional cleanup.
- For interface mismatch, repair connection topology or add the right conversion block first; do not delete the connected component just to force translation to pass.

## 7. Parameter Completion Baseline

- Prefer user-provided values over all defaults.
- For three-phase systems, always state whether voltages are line voltages or phase voltages.
- For inverters and converters, explicitly record DC-side voltage, switching frequency, filter parameters, and key controller parameters.
- For transformers and lines, explicitly record connection mode, turns ratio or impedance model, and main network parameters.
- For motors, explicitly record rated power, rated voltage, pole pairs, inertia, load torque, and operating condition when available.
- For batteries or storage blocks, explicitly record rated voltage, capacity, initial SOC, and charge/discharge direction convention.
- If a parameter is assumed, state both its value and its source category: default, case-based, inferred, or user-specified.

## 8. Result Review and Acceptance Cues

- Grid-tied systems: focus on voltage-current phase alignment, dynamic response, steady-state error, ripple, and oscillation.
- DCDC systems: focus on direction, steady-state value, overshoot, ripple, and current sign.
- Motor drives: focus on speed tracking, torque response, current waveform quality, and controller stability.
- Three-phase supply networks: focus on voltage level, power transfer, line drop, transformer behavior, and load response.
- Load-flow analysis: focus on voltage magnitude, phase angle, and P/Q distribution consistency.
- A result cannot be accepted if key variables are missing, diagram review is missing, or the delivery package omits solver and step-size evidence.
- Final acceptance grading should follow `references/acceptance-checklist.md`.
