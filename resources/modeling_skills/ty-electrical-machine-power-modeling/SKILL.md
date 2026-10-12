---
name: ty-electrical-machine-power-modeling
description: Sysplorer electrical, motor-drive, and power-system modeling with TYMotor, TYElectricPower, TYElectrical, and minimal Modelica glue. Use when building, fixing, or validating Sysplorer models for average-value inverters, PMSM DTC systems, transmission transients, distribution feeders, generators, transformers, lines, breakers, buses, static loads, sensors, grounding, or official TY electrical examples; includes case-derived fixes for executable models and mandatory reload/check/translate/simulate/inspect validation.
metadata:
  short-description: TY electrical, motor-drive, and power-system modeling guidance
  version: 0.2.0
  managed-by: sysplorer-mcp
---

# TY Electrical Machine Power Modeling

## Core Rules

- Instantiate only `TYMotor`, `TYElectricPower`, `TYElectrical`, and minimal `Modelica 4.0.0.TY.1` glue in final models.
- Never instantiate `NPSLibrary` or unpublished local commercial packages in final deliverables.
- Prefer official TY examples and component documentation before drafting topology.
- Deliver standalone user cases as one `.mo` file unless the user explicitly asks for a package.
- After every disk edit, force reload the edited `.mo`, then run `check -> translate -> simulate -> inspect`.
- Inspect key result variables immediately after the simulation that produced them.
- If no Simulink reference data exists, report `Sysplorer structure validation passed` and `Simulink parity pending reference data`.

## Library Priority

1. Use `TYMotor` for motor systems, PMSM drives, motor controllers, inverters, torque/speed sources, and motor-side sensors.
2. Use `TYElectricPower` for generators, transformers, buses, lines, breakers, power sensors, static loads, distribution feeders, transmission lines, and grounding in power-system topologies.
3. Use `TYElectrical` for basic electrical and foundational power-electronics examples, including average-value three-phase inverter demos.
4. Use `Modelica 4.0.0.TY.1` only for glue such as `Blocks.Sources`, `BooleanExpression`, `Electrical.MultiPhase.Basic.Star`, `Electrical.Analog.Basic.Ground`, and unit types when no practical TY block covers that role.

## Validation Gate

For every model:

1. Load required libraries with `load_library`.
2. Reload the edited file with `reload_mo_path`.
3. Run `check_model`.
4. Run `translate_model`.
5. Run `simulate_model` with at least one requested result variable.
6. Read representative values with `result_manager`.
7. Plot requested variables with `plot_manager` when waveform output is requested.
8. Record solver, step size or variable-step setting, stop time, key variables, and any unresolved compatibility findings.

## Case-Derived Patterns

### TYElectrical Average-Value Three-Phase Inverter

Use this pattern for a DC-link ramp feeding `TYElectrical.PowerConverters.AverageValueThreePhaseInverter`.

- Component: `TYElectrical.PowerConverters.AverageValueThreePhaseInverter(v_ratio=sqrt(6)/Modelica.Constants.pi)`.
- If the DC input must fall below the default `v_off=75 V`, explicitly set `v_on=0, v_off=0`; otherwise the inverter output turns off when the ramp reaches 50 V.
- Use `TYElectrical.BasicComponents.IdealElectricSource.ControlledVoltageSource` with `Modelica.Blocks.Sources.Ramp`.
- Keep the DC negative terminal referenced to electrical ground when the converter requires a DC reference.
- Do not short the AC load star point directly to the DC negative node if the requested output is pure three-phase AC load voltage; that introduces common-mode bias.
- For a user-facing `resistor.v[1..3]` output using TYElectrical one-phase resistors, wrap the three resistors and expose common-mode removed phase voltages if necessary.
- Use `experiment(StartTime=0, StopTime=3, Interval=0.001 or 0.0001, Tolerance=1e-6, Algorithm="Dassl")` or `__MWorks(Solver="Dassl")` according to local style.

Expected sanity checks:

- `VoltageSource.v` follows the ramp from 200 V to 50 V.
- Three-phase AC output remains balanced and scales with DC input.
- At `t=2s` and `t=3s`, output must not collapse to all zeros unless inverter undervoltage shutdown is intentionally being tested.

### TYElectricPower Transformer With Power Sensor

Use this wrapper when the user requests paths like `transformer.powerSensor1.plug_p.pin[i].v`.

```modelica
model TransformerWithPowerSensor
  parameter Real n = 10000/400 "变压器变比：一次侧/二次侧";
  parameter Modelica.Units.SI.Voltage V1 = 10000 "一次侧额定电压";
  parameter Modelica.Units.SI.Voltage V2 = 400 "二次侧额定电压";
  TYElectricPower.Interfaces.Electrical.PositivePlug positivePlug(final m=3) "变压器输入端";
  TYElectricPower.Interfaces.Electrical.NegativePlug negativePlug(final m=3) "变压器输出电流端";
  TYElectricPower.Interfaces.Electrical.NegativePlug voltageRef(final m=3) "功率传感器电压参考端";
  TYElectricPower.Primary.Transformer winding(n=n, V1=V1, V2=V2) "三相变压器本体";
  TYElectricPower.Secondary.PowerSensor powerSensor1 "三相功率/电压传感器";
equation
  connect(positivePlug, winding.positivePlug);
  connect(winding.positivePlug1, powerSensor1.plug_p);
  connect(powerSensor1.plug_ni, negativePlug);
  connect(powerSensor1.plug_nv, voltageRef);
end TransformerWithPowerSensor;
```

Ground `voltageRef` through a `Modelica.Electrical.MultiPhase.Basic.Star` and `Modelica.Electrical.Analog.Basic.Ground` unless a TY-specific reference is already proven for the topology.

### TYElectricPower Distribution System

Use these components:

- `TYElectricPower.Primary.Generator` for the source.
- `TransformerWithPowerSensor` for main and branch transformers when voltage/power observation is needed.
- `TYElectricPower.Primary.TransLine` for line and branch equivalent impedances.
- `TYElectricPower.Primary.Bus` for three-phase main and secondary buses.
- `TYElectricPower.Load.StLoad` for static loads.
- `Modelica.Electrical.MultiPhase.Basic.Star` plus `Modelica.Electrical.Analog.Basic.Ground` for reference grounding.

Important wiring rule:

- Do not connect the energized load bus or branch end directly to the same star-ground plug used as a voltage reference; this clamps the load node to 0 V and falsely passes source-side voltage checks while loads are not actually supplied.
- Ground sensor/reference plugs, not the live load node, unless the scenario explicitly models a grounded neutral/load return.

Useful checks:

- Read `transformer.powerSensor1.plug_p.pin[1].v`, `[2].v`, `[3].v` at multiple points in one 50 Hz cycle.
- Read at least one load terminal voltage from each branch to confirm both branches receive nonzero voltage.
- Plot the requested transformer-side three-phase voltage signals.

### TYElectricPower Transmission Transient

For generator-transformer-breaker-line examples:

- Use `TYElectricPower.Primary.Generator`, `TYElectricPower.Primary.Transformer`, `TYElectricPower.Primary.Breaker3ph`, and `TYElectricPower.Primary.TransLine`.
- Wrap `Breaker3ph` when the user asks for `CB.ib`; expose `ib = negativePlug.pin.i`.
- Drive breaker close/open/reclose with `Modelica.Blocks.Sources.BooleanExpression[3]`.
- For a breaker initially closed, open at `0.5s`, reclose at `0.8s`:

```modelica
Modelica.Blocks.Sources.BooleanExpression closeCmd[3](
  each y = not (time >= 0.5 and time < 0.8));
```

- Use `__MWorks(Solver="ImplicitEuler", FixedStep=0.001)` or the user-requested fixed step.
- Inspect both current and power variables immediately after simulation.

### TYMotor PMSM DTC

When an official TYMotor example already exists, prefer extending it instead of manually wiring every drive component.

Pattern:

```modelica
model TYMotorPMSM_DTC_DirectTorqueControl
  extends TYMotor.Examples.PMSMSystem_DTC(
    V=60,
    p=4,
    Rs=3,
    Lssigma=0.0028,
    Lmd=0.0085,
    Lmq=0.0085,
    V0=26,
    J_Rotor=0.0008,
    fsNominal=50,
    sine(amplitude=10, offset=100),
    torquestep(stepTorque=0),
    PMSM_DTC(p=4, Ld=0.0085, Lq=0.0085),
    PMSM1(p=4, Rs=3, Lssigma=0.0028, Lmd=0.0085, Lmq=0.0085, V0=26, J_Rotor=0.0008, fsNominal=50));
end TYMotorPMSM_DTC_DirectTorqueControl;
```

Expose aliases for user-requested plots, such as:

```modelica
Real speedRef = sine.y "参考转速信号";
Real speedActual = angularVelecitySensor.w "电机实际机械角速度";
```

Use `__MWorks(Solver="Dassl")` and simulate for the requested stop time.

## Common Failure Modes To Check

- `CheckModel` passes but `TranslateModel` fails: inspect grounding, floating DC references, or duplicated ideal constraints.
- Simulation passes but load voltages are zero: check whether a bus or branch end was accidentally shorted to star ground.
- Requested result variable is missing: rename wrappers and internal sensors to match the exact requested path before final validation.
- Three-phase values contain an unexpected offset: check whether AC neutral and DC negative/reference were tied together.
- Output vanishes at low DC voltage: check default converter `v_on/v_off` thresholds.
- Result values are inspected after another model ran: rerun the target simulation and inspect immediately.

## Final Response Requirements

Report:

- Absolute path to the `.mo` model.
- Components and libraries instantiated.
- Solver, step size, stop time, and requested plotted variables.
- Gate results: check, translate, simulate, inspect.
- A short physical explanation of power flow and observed behavior.
- `Sysplorer structure validation passed`.
- `Simulink parity pending reference data` when no reference data is provided.
