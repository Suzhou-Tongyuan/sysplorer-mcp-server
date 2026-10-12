# Diagram Layout Rules

Use this file only for newly created or actually modified graphical targets under parent Gate 6. Valid `Placement` annotations can still produce an unreadable diagram when components are crowded, overlapped, randomly placed, or routed without functional layers.

## Hard Rule

For model-creation tasks, layout must be generated as a functional diagram, not as arbitrary coordinates.

Before writing component `Placement`, create a layout table that assigns each key instance to one of these zones:

| Zone | X Range | Y Range | Typical Components |
|---|---:|---:|---|
| source_zone | `-130..-80` | `20..80` | pressure source, gas source, pump, compressor |
| protection_zone | `-90..-35` | `-10..55` | relief valve, check valve, accumulator, filter |
| control_zone | `-30..35` | `5..70` | directional valve, throttle valve, controller interface |
| actuator_zone | `70..130` | `5..70` | hydraulic cylinder, pneumatic cylinder, motor, load |
| return_zone | `-60..60` | `-90..-45` | tank, exhaust, surroundings, return manifold |
| sensor_zone | `70..130` | `-35..10` | pressure, flow, displacement, temperature sensors |
| signal_zone | `-130..130` | `75..95` | command sources, gains, logic blocks |
| thermal_zone | `-130..130` | `-95..-65` | heat source, thermal boundary, heat exchanger support |

If a system has more components than fit these zones, expand the diagram coordinate system before crowding components.

## Minimum Spacing

- Key component centers must be at least `24` units apart unless they are intentionally compact non-visual helpers.
- Major fluid components should use extents near `{{-10,-10},{10,10}}` to `{{-18,-12},{18,12}}`; avoid stretched extents unless the library icon requires it.
- Do not place two key component bounding boxes so they overlap.
- Leave a margin inside `Diagram(coordinateSystem(...))`.
- Keep instance names short enough to avoid covering ports or wires.

## Directional Flow Policy

- Main supply or gas flow should run left-to-right.
- Return or exhaust should run downward and then along the lower return layer.
- Working lines from valves to actuators should be parallel and separated.
- Control and signal lines should stay above the physical fluid circuit.
- Thermal lines should stay below or in a separate thermal zone.
- Avoid diagonal wires for main fluid lines; use orthogonal routes with intermediate points.

## Required Generation Order

1. Classify every key component into a layout zone.
2. Produce a layout table with instance, role, zone, center, extent, and rotation.
3. Check centers and extents for overlap before writing Modelica.
4. Produce line routes that follow the zone/layer policy.
5. Write `Placement` and `Line(points=...)` annotations.
6. Save the `.mo` file.
7. Run `scripts/check_modelica_diagram_layout.ps1 <model.mo> -TargetClass <FQClass> -Json`.
8. Run `scripts/check_modelica_line_annotations.ps1 <model.mo> -TargetClass <FQClass> -Json`.
9. Record script findings and complete applicable parent Gate 6 before full graphical delivery. Visual layout findings do not block check, translation or simulation; annotation syntax/structure errors are handled by model check.
10. Review structured Placement/Diagram, script, coordinate, extent, anchor and route-table evidence as the common basis. Add images according to user request and capability; record unmet explicit image requests. Repair crowding, crossing or unreadable routes found by applicable evidence without claiming unperformed visual inspection.

Run each changed target separately; the scripts inspect only that class's direct annotations, excluding nested/short class declarations and inherited graphics. Multiple long classes without `-TargetClass` are `undetermined`. Numeric expressions or unsupported syntax also return `undetermined` (`passed: null`, exit 2), not a geometry failure or a pass. Preserve the diagnostic and supplement the parent Gate 6 evidence without expanding the repair scope. Rotated extents use corner-transformed axis-aligned bounds; overlaps are conservative preflight findings. Invocation and limitations: `scripts/README.md`.

## Validation Checklist

- diagram coordinate system exists
- every key instance has `Placement`
- no key component is outside the diagram coordinate system
- no key component overlaps another key component
- key component centers are not crowded into one point or one narrow column
- source, control, actuator, return/exhaust, sensor, signal, and thermal elements are separated by role
- line routes stay mostly orthogonal and inside the coordinate system
- diagram export/direct review or documented structured evidence confirms readable layout

## Common Failure Patterns

- All components use `{0,0}` or near-identical origins: diagram has components but layout is unreadable.
- Components have `Placement`, but no zone policy: source, valve, cylinder, and tank appear in arbitrary order.
- Return or exhaust path runs through the actuator/control zone: diagram technically has wires but is confusing.
- Diagram coordinate system is too small: components or line routes are cropped.
- `smart_layout` is skipped after manual coordinate generation fails: bad layout persists into delivery.
