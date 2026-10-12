# Diagram Line Annotation Rules

Use this file for newly created or actually modified graphical targets under parent Gate 6. It exists because a model can contain valid semantic `connect(...)` equations while Sysplorer still shows no visible wires when `annotation(Line(...))` is missing or unusable.

## Hard Rule

For model-creation tasks, every planned visible connection must be emitted in this form:

```modelica
connect(componentA.portX, componentB.portY)
  annotation(Line(points={{x1,y1},{xm,y1},{xm,y2},{x2,y2}}, color={0,0,255}));
```

Do not rely on plain `connect(componentA.portX, componentB.portY);` for graphical delivery.

## Required Generation Order

1. Create a diagram coordinate system, normally `Diagram(coordinateSystem(extent={{-140,-100},{140,100}}))`.
2. Create a layout table with one center coordinate for every key instance.
3. Add every key instance with `annotation(Placement(transformation(origin={x,y}, extent={{-w,-h},{w,h}})))`.
4. Create a route table for every planned connection.
5. Emit every `connect(...)` with `annotation(Line(points=...))`.
6. Save or write the `.mo` file.
7. Run `scripts/check_modelica_line_annotations.ps1 <model.mo> -TargetClass <FQClass> -Json`.
8. Record script findings and repair applicable visible-line issues before full graphical delivery. Visual defects do not block check, translation or simulation; annotation syntax/structure errors are handled by model check.
9. Review wire visibility from structured line annotations, route tables, coordinate ranges, connector anchors and script output as the common basis. Add images by request and capability; unmet explicit image requests remain gaps, and structured evidence is not claimed as visual inspection.
10. If visible wires are missing or structured evidence shows zero-length, cropped, hidden, or unplanned routes, repair `Line(points=...)` and rerun diagram review before delivery.

## Layout Table Minimum Fields

| instance | role | center | extent | rotation | notes |
|---|---|---|---|---|---|
| `pSrc` | pressure/gas source | `{-110,40}` | `{{-10,-10},{10,10}}` | `0` | left side |
| `dcv` | main valve | `{0,20}` | `{{-12,-12},{12,12}}` | `0` | center |
| `act` | actuator/load | `{90,20}` | `{{-18,-10},{18,10}}` | `0` | right side |
| `tank` | return/exhaust | `{0,-60}` | `{{-12,-12},{12,12}}` | `0` | bottom return layer |

## Route Table Minimum Fields

| connection | semantic pair | line points | layer |
|---|---|---|---|
| `L1` | `pSrc.port -> dcv.P` | `{{-100,40},{-50,40},{-50,20},{-12,20}}` | pressure/supply |
| `L2` | `dcv.A -> act.A` | `{{12,26},{45,26},{45,30},{72,30}}` | working line A |
| `L3` | `dcv.B -> act.B` | `{{12,14},{45,14},{45,10},{72,10}}` | working line B |
| `L4` | `dcv.T -> tank.port` | `{{0,8},{0,-25},{0,-48}}` | return/exhaust |

Adapt coordinates to the actual component ports. The important property is not the exact numbers; it is that every planned connection has explicit, visible, nonzero-length route points.

Select each changed class explicitly. Counts cover only its direct `connect(...)` statements; nested/short class bodies and inherited connections are excluded, and loop iterations are not expanded. A zero-connection pass only describes an empty local scan and must still be reconciled with the plan. Multi-class ambiguity and unsupported expressions return `undetermined` (`passed: null`, exit 2); keep this status and obtain applicable supplemental evidence rather than treating it as a pass or an instruction to repair other classes. See `scripts/README.md`.

## Validation Checklist

- `connect_count == planned_connection_count`
- every `connect(...)` has `annotation(Line(points=...))`
- every `Line(points=...)` has at least two distinct points
- `scripts/check_modelica_line_annotations.ps1 <model.mo> -TargetClass <FQClass> -Json` supplies evidence for applicable Gate 6; unresolved visual findings block complete graphical delivery, not check/translation/simulation
- route points are inside the diagram coordinate system
- wires are not fully hidden under component icons or labels
- pressure/supply, working, return/exhaust, thermal, and control lines are visually separated
- diagram export/direct review or documented structured evidence confirms visible key wires

## Common Failure Patterns

- Plain `connect(...)` equations exist, but no `Line` annotations: semantic model may compile, diagram may show no wires.
- `Line(points={{0,0},{0,0}})`: zero-length wire may be invisible.
- Route points outside `Diagram(coordinateSystem(...))`: exported diagram can appear empty or cropped.
- Missing `Placement`: line endpoints may not align with visible component symbols.
- Long instance labels cover ports or wires: shorten names or move route points.
