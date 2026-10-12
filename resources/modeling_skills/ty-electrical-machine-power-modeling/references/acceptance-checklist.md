# Acceptance Checklist

All applicable items below must be satisfied before delivery.

## Prerequisite

- `ty-sysplorer-modeling-rules` has already been applied.
- The modeling path, working directory, and tool-safety rules follow the prerequisite skill.
- Gate 6 layout acceptance has been completed when that gate applies.

## Scope

- Final topology instantiates only `TYMotor`, `TYElectricPower`, `TYElectrical`, and minimal `Modelica 4.0.0.TY.1` glue.
- No `NPSLibrary` or other unauthorized commercial library instance appears in the final topology.
- Any use of `Modelica 4.0.0.TY.1` is justified because the TY libraries did not cover the role practically.

## Deliverable Type

- Reusable component: correct package structure, `package.mo`, `package.order`, main model, `Tests`, `Examples`, and `Resources`.
- Standalone case: single `.mo` case file, not an artificial component package tree.

## Modeling Quality

- Topology is complete.
- All intended connections are present.
- No placeholder wiring remains.
- All user-adjustable parameters are exposed.
- Parameter comments are present in Chinese.
- External interfaces are commented in Chinese.
- Unit meaning is clear where needed.

## Execution Gate

- The edited root `package.mo` was force-reloaded after disk edits.
- `CheckModel` passed.
- `TranslateModel` passed.
- `SimulateModel` passed.
- Key variables from that same simulation were inspected immediately, without relying on ambiguous shared result context.

## Recording

- Solver name is recorded.
- Step size or variable-step setting is recorded.
- Stop time is recorded.
- Core variable names are recorded.
- Data source is recorded.
- Unresolved compatibility findings are recorded.

## Parity

- If Simulink reference data exists, at least one key signal comparison is complete.
- If the deliverable is a reusable component, at least `2` parity or validation tests exist.
- Maximum relative error is below `1%` when parity is claimed.
- If no Simulink reference exists, the report explicitly says `Sysplorer structure validation passed` and `Simulink parity pending reference data`.

## Documentation

- `Documentation(info=...)` or an equivalent component description exists when appropriate.
- Help-document work is completed or blocked status is reported explicitly.

## Delivery Evidence

- Component or case path is reported.
- Test path or scenario path is reported.
- Validation conclusion is reported.
- Error metrics are reported when parity is claimed.
- Known limitations are reported.
