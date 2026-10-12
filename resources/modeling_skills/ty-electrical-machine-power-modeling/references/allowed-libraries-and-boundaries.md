# Allowed Libraries And Boundaries

## Runtime Boundary

- Final deliverables may instantiate only `TYMotor`, `TYElectricPower`, `TYElectrical`, and minimal `Modelica 4.0.0.TY.1` glue.
- `Modelica 4.0.0.TY.1` is the default standard-library version unless the user explicitly specifies another version.
- `NPSLibrary` and unpublished local NPS packages are reference-only. They may be studied for packaging, comments, testing style, and documentation workflow, but may not appear as instantiated dependencies in final models.

## Library Priority

1. `TYMotor`
2. `TYElectricPower`
3. `TYElectrical`
4. `Modelica 4.0.0.TY.1` only when the TY libraries do not cover the role

## Domain Roles

- `TYMotor`
  - First choice for motor systems, machines, drive chains, converters, motor-side sensors, motor-side controllers, and electromechanical assemblies.
- `TYElectricPower`
  - First choice for power-system, power-flow, network, bus, transformer, line, source, load, and electromechanical-transient structure.
- `TYElectrical`
  - First choice for digital circuits, basic analog circuits, teaching circuits, elementary devices, and limited foundational power-electronics elements.
- `Modelica 4.0.0.TY.1`
  - Fallback glue only.
  - Typical acceptable uses: signal sources, small helper logic, simple control glue, limited sensor/source adapters.
  - Whenever it is used, state why the TY libraries did not provide a practical block for that exact role.

## Forbidden In Final Deliverables

- Instantiating `NPSLibrary`
- Instantiating unpublished `NPS_New` components
- Instantiating any unauthorized commercial library
- Letting `Modelica` dominate the final topology when a TY-library path exists

## Allowed Reuse From NPS References

Only the method may be reused, not the dependency:

- package organization
- parameter-panel grouping
- Chinese comment style
- `Tests` / `Examples` / `Resources` layout
- verification workflow
- help-document workflow

## Required Boundary Evidence

Every delivery must be able to answer:

1. Which instantiated components come from which allowed libraries.
2. Whether any non-allowed library instance appears in the final topology.
3. Which parts were only informed by `NPSLibrary.mol` or `NPS_New` as reference samples.

If the boundary cannot be proven clearly, the delivery is not accepted.
