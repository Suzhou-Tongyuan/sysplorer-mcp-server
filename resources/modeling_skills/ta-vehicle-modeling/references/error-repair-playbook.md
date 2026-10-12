# Error Repair Playbook

Use this file when a TA vehicle model fails a parent gate, a result variable cannot be verified, or a vehicle behavior is physically implausible.

This file is a TA vehicle domain add-on, not a second task owner. Existing concrete faults are led by the independent debugging entry; new-build faults remain in the original task. Parent `../../ty-sysplorer-modeling-rules/references/shared-standards.md` owns session/error/retry policy, and its seven-gates workflow owns requested validation depth. Do not expand a check-only repair into simulation or result review.

## Repair Loop

1. Name the failed parent step: requirement, library selection, construction, layout annotation, check, translate, simulate, result verification, or delivery.
2. Capture the concrete symptom: MCP error, missing class, equation mismatch, initialization failure, NaN/divergence, no vehicle motion, missing bus field, missing result variable, missing or conflicting layout annotation, or wrong trend.
3. Classify the fault using the table below.
4. Identify the shortest active failure chain.
5. Apply the smallest meaningful repair.
6. Return to the failed parent step and rerun its gate.
7. Continue only after the gate passes or a real blocker is documented.

## Fault Classes

| Class | Typical Signal | First Repair Target |
|---|---|---|
| Source/input | Missing model path, unclear vehicle architecture, no target operating case, no success criteria | Return to requirement extraction and mark unknowns as `to confirm`. |
| Library/dependency | TA class missing, wrong library family, dependency not loaded, `TYBase` treated as the main answer | Load or switch to the correct TA primary library and record support libraries separately. |
| Primary library selection | Economy task built on dynamics skeleton, thermal task built from local heat sources only, battery detail treated as whole-vehicle thermal skeleton | Re-run `references/library-selection.md` and choose one primary library. |
| Vehicle architecture | Fuel / EV / hybrid / range-extender architecture unclear or mismatched with selected example | Confirm architecture and switch to the closest matching official example or template. |
| Model hierarchy/interface | Cross-layer variable writes, hidden reusable subsystem, missing boundary connector, direct inner-variable reference | Expose real interfaces, buses, or connectors; move reusable structures into proper subsystem classes. |
| Bus/signal mapping | Missing bus field, duplicate driver/control signal, inconsistent motor/wheel/battery index, multiple drivers for one signal | Repair bus definitions, adapters, numbering, and signal ownership. |
| Topology/connection | Driver, road, body, wheel, drive, brake, thermal loop, low-voltage bus, or boundary path not closed | Repair the smallest broken vehicle chain before touching solver settings. |
| Parameter/unit | Missing vehicle mass, tire parameter, gear ratio, pack series/parallel count, flow boundary, or unit mismatch | Repair active parameters using `references/parameter-rules.md` and record assumptions. |
| Initialization | Impossible initial speed/SOC/temperature, conflicting starts, state selection issue | Align starts with boundaries and operating case; add only necessary start/state hints. |
| Translation | Equation/variable mismatch, connector incompatibility, template redeclaration conflict, unsupported component combination | Remove the smallest incompatible combination or correct interface/redeclare choices. |
| Simulation | NaN, divergence, tiny step, no motion, pressure/temperature explosion, solver stalls | Check boundaries, control inputs, stiffness sources, discontinuities, and load direction. |
| Result variable | Target variable missing, wrong nested path, variable exists but does not match user goal | Query actual result variables and verify semantic match before reporting values. |
| Diagram annotation | Key assembly lacks `Placement`, connections lack `Line`, layout coordinates conflict, or a copied example layout is misleading | Repair vehicle-level `Placement`, `Line`, and subsystem grouping, then verify the source annotations. |

## TA Library Shortcuts

### `TAEconomy`

- No vehicle motion: check driver / drive cycle, power source, transmission, brake release, vehicle body, and road/load path.
- Wrong economy or range trend: check mass, rolling resistance, aero drag, SOC initialization, drive cycle, accessory load, and motor/engine efficiency maps.
- Equation mismatch: check motor count, axle mapping, drivetrain numbering, and bus index consistency.

### `TADynamics`

- Handling or ride response missing: check body, suspension, tire, steering, brake, road, and driver interfaces.
- Reversed or implausible motion: check coordinate conventions, wheel positions, steering sign, tire force direction, and brake/drive torque application points.
- Unstable dynamics: check tire parameters, suspension stiffness/damping, initial speed, road input, and solver stiffness before changing topology.
- Open-loop `ChassisBase` / `ChassisBase2` coast-down with no external brake or drive system:
  - If `CheckModel` passes but `TranslateModel` reports missing equations through wheel, suspension, or multibody torque paths, inspect the external `signalBus` torque fields before changing chassis class or adding physical flange torque sources.
  - These chassis models may require zero equations for `signalBus.brakeBus.brakeBus[i].tau_brake` and `signalBus.powertrainBus.emotorBus[i].tau_drive` for each wheel index, even when `driverBus.brakePedal = 0` and `driverBus.accPedal = 0`.
  - Repair by connecting visible `Modelica.Blocks.Sources.Constant(k=0)` sources to the four `tau_brake` fields and four `tau_drive` fields. Keep steering zero with `driverBus.SWAngle = 0` and hold zero steering with `driverBus.SWRelease = false` unless the intended case is released steering.
  - Do not treat the missing equations as proof that `ChassisBase2` is unusable or replace it with a simplified local vehicle model. Do not attach external physical wheel-flange torque components unless the requirement explicitly includes a physical driveline/brake boundary.

### `TAThermalSystem`

- No thermal response: check heat source, heat sink, pump/fan/compressor command, coolant/refrigerant/air loop closure, and temperature variables.
- Temperature or pressure explosion: check blocked loop, missing boundary, wrong valve state, pump direction, compressor command, and heat exchanger side connections.
- Mixed thermal task: decide whether the primary skeleton is whole-vehicle thermal (`TAThermalSystem`) or a local battery/engine/electronic refinement.

### `TAEngine`

- Engine does not produce expected torque: check speed boundary, throttle/fuel/ignition command, intake/exhaust boundary, and controller interface.
- Translation failure: check redeclarations, medium/boundary compatibility, turbocharger/fuel path connections, and engine-to-vehicle interface.
- Thermal refinement issue: check whether cooling is local engine cooling or whole-vehicle thermal management.

### `TABattery`

- Pack/module/cell mismatch: check `Module_N_series`, `Module_N_parall`, `Cell_N_series`, `Cell_N_parall`, and adapter parameters together.
- Duplicate or missing battery signal: check `iBattery` numbering, bus mapping, and pack/module adapter ownership.
- Thermal result missing: check thermal interface enablement, cooling boundary, cell/module/pack temperature variables, and whether `TAThermalSystem` support is needed.

### `TAElectronic`

- Low-voltage system inactive: check low-voltage bus, DCDC, source, load enable signals, and return/reference path.
- Accessory power implausible: check load schedule, domain grouping, bus mapping, and whether thermal-management actuators use the intended electrical version.
- Coupled thermal/electrical issue: check whether the actuator belongs in `TAElectronic` while its thermal loop remains under `TAThermalSystem`.

## Repair Output

For each repair iteration, keep internal notes with:

- failed parent step
- symptom
- fault class
- root-cause hypothesis
- repair action
- rerun result
- remaining blocker or next gate

Only include these details in the final response when they are useful to the user or when a blocker remains.
