# Sysblock StateMachine Chart Editing

This file is the authoritative source for concrete StateMachine API, condition
subsystem, geometry, and layout-audit rules. MBD workflow documents may link
here but must not duplicate or override these rules.

Use this reference only when a Sysblock model or subsystem actually contains a StateMachine `Chart`. A StateMachine Chart implements explicit discrete mode logic inside a Sysblock block diagram. External interfaces, condition logic, timing, action handling, layout around the Chart, simulation, and verification remain ordinary Sysblock modeling concerns.

Use `layout-workflow.md` as the authority for the cross-level layout order and geometry-free input. This file remains authoritative for Chart semantics, StateMachine API details, transition rules, and Chart-internal audit evidence.

Never directly edit saved `.mo` text for StateMachine creation, topology, state geometry, transition geometry, or label placement. Use Sysplorer StateMachine APIs.

## Contents

- Entry And Scope
- Capability Coverage
- Minimum Workflow
- States
- Parallel States
- Nested States
- Subchart States
- Junctions
- Chart Data And Ports
- Chart Events
- Transitions
- External Conditions, Timing, And Actions
- Chart Layout Planning
- Transition Geometry
- Labels
- Priority
- Layout Audit
- API Pattern
- Common Pitfalls

## Entry And Scope

Create a Chart inside an existing or in-progress Sysblock model/subsystem with `AddComponent` so its outer size is set at creation time:

```python
M.AddComponent(
    "SysplorerEmbeddedCoder.StateMachine.Chart",
    "Controller",
    "chart",
    0, 0, 260, 220
)
chart = M.GetBlockHandle("Controller", "chart")
```

Rules:

- Do not default to `CreateChart(model, "")` for a top-level Chart. It usually creates a small default frame, and the current API cannot reliably resize it afterward through `SetComponentInfo`.
- Prefer `AddComponent("SysplorerEmbeddedCoder.StateMachine.Chart", model, "chart", x, y, w, h)`.
- Size the Chart by port count and port-name length.
- After creation, call `GetBlockHandle(model, "chart")`, then use `CreateState`, `CreateChartData`, `CreateChartEvent`, and `CreateTransition`.
- If the Chart is inside a subsystem, still prefer `AddComponent` in that subsystem context and read back the handle.

Valid StateMachine API parents:

- `CreateState(parent_id)` accepts a Chart handle or a State handle.
- `CreateTransition(parent_id)` usually uses the Chart handle for top-level transitions.
- `CreateChartData(chart_id)` creates Chart data. Create states before Chart data so input/output data stays in Chart scope rather than being captured into the currently active state.
- `CreateChartEvent(chart_id)` creates Chart events.
- `CreateJunction(chart_id)` is available, but use it only when junction semantics are required.

Common readback APIs:

```python
M.GetChartElementInfos(element_id)
M.GetChartElementInfo(element_id, "LabelString")
M.GetBlockHandle(model_name, "chart")
M.GetChildren(chart_id, "State")
M.GetChildren(chart_id, "Transition")
M.GetComponentPorts(model_name, "chart", 0)
```

## Capability Coverage

| Capability | API pattern |
|---|---|
| State | `CreateState(chart_id)` |
| Child state | `CreateState(parent_state_id)` |
| Subchart state | `SetChartElementInfo(state_id, "IsSubchart", "true")` |
| Junction | `CreateJunction(chart_id)` |
| Transition | `CreateTransition(chart_id)` |
| Data | `CreateChartData(chart_id)` |
| Event | `CreateChartEvent(chart_id)` |

Treat this table as a strict allowlist for Chart-internal element kinds: `State` (including child, nested, parallel, and subchart states), `Transition` (including default transitions), `Data`, `Event`, and business-semantic `Junction`. Create and retain only these element kinds inside a Chart. At the containing Sysblock level, the StateMachine block allowlist contains only `SysplorerEmbeddedCoder.StateMachine.Chart`. Include the complete actual element-kind inventory from saved/force-reloaded StateMachine API readback in final Chart evidence; the evidence audit rejects every kind outside this allowlist.

## Minimum Workflow

1. Freeze the business states, guards, actions, transition priorities, and required behavior.
2. Derive the complete directed transition topology, including default, reciprocal, exceptional, and cross-level transitions.
3. Run `scripts/layout_plan_tool.py statechart`. Cyclic topology is allowed; it does not by itself require hierarchy redesign. The command audits the generated Chart geometry before emitting the plan.
4. For every ordinary transition, require sufficient source/target x- or y-projection before choosing endpoints. When overlap is insufficient, translate a state first, then use bounded scale and deterministic neighbour push. Record every adjustment. Do not enumerate corners.
5. Use nested states, subcharts, or semantic junctions only when the bounded geometry planner fails or the business hierarchy independently requires them; never change business semantics merely to simplify the drawing.
6. Accept the static Chart plan only when the planning command returns successfully. It rejects non-orthogonal or multi-point transitions, crossings, collinear overlaps, shared endpoints, and state overlaps before any Chart creation API.
7. Decide the Chart position, size, and interface in the Sysblock model/subsystem.
8. Create the Chart with `AddComponent("SysplorerEmbeddedCoder.StateMachine.Chart", ...)` and read back its handle with `GetBlockHandle`.
9. Create states with `CreateState`; set names, actions, font sizes, and approved positions with `SetChartElementInfo`.
10. Create Chart-level data after states; create events only when event triggering is needed.
11. Expose and wire same-level Chart ports, external conditions, and actions.
12. Create default and ordinary transitions from the approved topology and geometry; set endpoints/OClock, labels, label positions, and execution order.
13. Read back every state and transition geometry. Rerun the Sysblock and internal Chart audits; actual geometry must satisfy the pre-modeling constraints.

For every StateMachine API call in this workflow, check its returned status or identifier before issuing any dependent call. `AddComponent` and all `Create*` calls must succeed and, when documented, return a valid handle/identifier; every `SetChartElementInfo` call must return success. On failure, stop the dependent Chart edits and diagnose the returned error. This return-value check does not add any property-readback requirement; retain only the readbacks already required elsewhere in this reference.

## States

Example:

```python
idle = M.CreateState(chart)
M.SetChartElementInfo(idle, "Name", "Idle")
M.SetChartElementInfo(idle, "FontSize", "10")
M.SetChartElementInfo(idle, "Position", "{-80, 18, -30, -18}")
M.SetChartElementInfo(idle, "LabelString", "du: sm_y := 0;")

active = M.CreateState(chart)
M.SetChartElementInfo(active, "Name", "Active")
M.SetChartElementInfo(active, "FontSize", "10")
M.SetChartElementInfo(active, "Position", "{30, 18, 85, -18}")
M.SetChartElementInfo(active, "LabelString", "du: sm_y := 1;")
```

Rules:

- `LabelString` is action text, not the state name. Set the state name with `Name`.
- Statements inside a StateMachine use Modelica syntax. Assign with `:=` and end statements with semicolons, for example `du: sm_y := 0;`.
- Supported action keywords include `en:`, `du:`, and `ex:`.
- Sysplorer may normalize `y = 0;` into `y := 0;`, but write `:=` intentionally.
- Saved readback may split an action across escaped newlines and indentation. Compare its semantics after removing only backslashes and whitespace; identifiers, operators, and literals must still match (for example, `du: mode := 10;` matches `du:\\n  mode := 10;\\n`).
- Do not assume variables or built-ins from other state-machine tools exist. For example, writing `time` directly in a state action can fail because `time` is not a Chart variable.
- Before adding a same-level second state, move or size the first state so the insertion point is not geometrically inside it; otherwise the second state may become nested.

## Parallel States

Chart-level parallel decomposition is supported. Set the Chart decomposition to `PARALLEL_AND`; sibling states then read back as `Type=AND`.

```python
M.AddComponent("SysplorerEmbeddedCoder.StateMachine.Chart", "ParallelDemo", "chart", 0, 0, 260, 220)
chart = M.GetBlockHandle("ParallelDemo", "chart")
M.SetChartElementInfo(chart, "Decomposition", "PARALLEL_AND")

region_a = M.CreateState(chart)
M.SetChartElementInfo(region_a, "Name", "RegionA")
M.SetChartElementInfo(region_a, "Position", "{-120, 70, -20, 20}")

region_b = M.CreateState(chart)
M.SetChartElementInfo(region_b, "Name", "RegionB")
M.SetChartElementInfo(region_b, "Position", "{20, 70, 120, 20}")
```

Rules:

- Set `Decomposition=PARALLEL_AND` on the Chart, not separately on each child state.
- Declare parallel Chart layout input with `decomposition=parallel` and `default_state=null`; it has no top-level default transition. An omitted declaration means `exclusive`, so a missing exclusive default still fails.
- Actions in parallel states still use Modelica syntax.
- If regions share data, define Chart-level data scope clearly and avoid simultaneous writes to the same output.

## Nested States

Nested states are supported. Create children under the parent state and use hierarchical paths such as `Parent.ChildA`.

```python
M.AddComponent("SysplorerEmbeddedCoder.StateMachine.Chart", "NestedDemo", "chart", 0, 0, 300, 240)
chart = M.GetBlockHandle("NestedDemo", "chart")

parent = M.CreateState(chart)
M.SetChartElementInfo(parent, "Name", "Parent")
M.SetChartElementInfo(parent, "Position", "{-130, 90, 130, -90}")
M.SetChartElementInfo(parent, "Decomposition", "EXECLUSIVE_OR")

child_a = M.CreateState(parent)
M.SetChartElementInfo(child_a, "Name", "ChildA")
M.SetChartElementInfo(child_a, "Position", "{-100, 45, -20, 5}")

child_b = M.CreateState(parent)
M.SetChartElementInfo(child_b, "Name", "ChildB")
M.SetChartElementInfo(child_b, "Position", "{20, 45, 100, 5}")

t_parent = M.CreateTransition(chart)
M.SetChartElementInfo(t_parent, "Destination", "Parent")

t_default_child = M.CreateTransition(chart)
M.SetChartElementInfo(t_default_child, "Destination", "Parent.ChildA")

t_ab = M.CreateTransition(chart)
M.SetChartElementInfo(t_ab, "Source", "Parent.ChildA")
M.SetChartElementInfo(t_ab, "Destination", "Parent.ChildB")
M.SetChartElementInfo(t_ab, "LabelString", "[T_ab]")
```

Nested-state rules:

- Use `CreateState(parent_state_id)` to create a child state.
- If the parent state is mutually exclusive (`EXECLUSIVE_OR`), it needs an internal default transition.
- A mutually exclusive top-level Chart also needs a default transition to the top-level default state, such as `Parent`.
- Every nested exclusive submachine must satisfy the default-transition rule. A top-level transition should enter the parent; the parent's default transition selects the default child.
- Ordinary transitions should connect same-level states. Do not create a cross-level transition from one state directly into the child of another same-level state. Enter the parent and let its default transition choose the child.
- A transition from a child state to an upper-level state is allowed when it represents leaving the nested mode, for example `Parent.ChildA -> Fault` or `Parent.ChildA -> Parent`.
- In current experiments, `CreateTransition(parent_state_id)` reports that transitions may only be inserted to chart or subchart. Therefore create nested transitions with the Chart handle and hierarchical endpoint paths.
- Nested-state actions still use Modelica syntax.

## Subchart States

Convert a normal state to a subchart by setting:

```python
parent = M.CreateState(chart)
M.SetChartElementInfo(parent, "Name", "Parent")
M.SetChartElementInfo(parent, "IsSubchart", "true")
```

Rules:

- `IsSubchart` is writable. `Type` is read-only; do not use `Type=SUBCHART` for conversion.
- Create subchart children with `CreateState(parent_state_id)`.
- Prefer `CreateTransition(chart_id)` for subchart transitions and use hierarchical paths, for example `Parent.ChildA`.
- External transitions should target the subchart state itself, not an internal child. The subchart's internal default transition selects the child.

## Junctions

Create a junction only when the design has clear branch, merge, or conditional-path reuse semantics:

```python
j = M.CreateJunction(chart)
M.SetChartElementInfo(j, "Position", "{0, 0, 6, 6}")
```

Rules:

- `CreateJunction(chart_id)` creates a StateMachine junction; it is not an ordinary Sysblock block.
- Do not add junctions only to improve layout, bend or orthogonalize transitions, separate or extend lines, reroute lines, or move labels. Change state placement or hierarchy instead of changing state-machine topology for layout.
- After creating a junction, connect real control flow through transitions and confirm structure legality.

## Chart Data And Ports

Create states first, then Chart-level data:

```python
du = M.CreateChartData(chart)
M.SetChartElementInfo(du, "Name", "sm_u")
M.SetChartElementInfo(du, "Scope", "Input")

dy = M.CreateChartData(chart)
M.SetChartElementInfo(dy, "Name", "sm_y")
M.SetChartElementInfo(dy, "Scope", "Output")
M.SetChartElementInfo(dy, "Port", "1")
```

Set every required data type explicitly with the case-sensitive tokens verified in `runtime-contracts.md`. For Sysplorer 2026b, use `boolean` for Boolean data and `int32` for a 32-bit signed integer; do not use Modelica names such as `Boolean` or `Integer`, or aliases such as `bool`.

Rules:

- Chart data names become Chart port instance names.
- A Chart data name must not conflict with another component instance name at the same model level.
- External condition/action subsystems must not share names with Chart inputs/outputs. Prefer `G_`, `Cond_`, or `Act_` prefixes for subsystems while Chart ports keep semantic condition/action names such as `T_start_permitted`.
- After each `SetChartElementInfo(data, "Name", name)`, check the return value. If it returns `false`, rename immediately and do not continue with default names such as `data` or `data1`.
- After creating or changing Chart ports, size the Chart frame by port count and port-name length.
- Before wiring external Sysblock `Inport` / `Outport` blocks to a Chart, calculate the Chart side-port y-centers from the actual Chart height with the single-core half-step formula in `modeling-workflow.md`, then place the external ports at those y values. `GetComponentPorts` confirms port names/order but does not provide the rendered y-coordinate.
- If the Chart is inside a subsystem, adjust the parent `SubSystem` frame as needed.
- If `GetChartElementInfos(data_id)["Path"]` becomes `Idle.sm_u`, the data was created inside a state instead of Chart scope. Recreate in the correct order.

## Chart Events

Create events with `CreateChartEvent(chart)`:

```python
ev = M.CreateChartEvent(chart)
M.SetChartElementInfo(ev, "Name", "ev_tick")
M.SetChartElementInfo(ev, "Scope", "Input")
M.SetChartElementInfo(ev, "Port", "1")
M.SetChartElementInfo(ev, "Trigger", "rising")
```

Rules:

- Use `Scope=Local` for internal Chart events or `Scope=Input` to expose an input event.
- After creating input events, read back `GetComponentPorts(model, "chart", 0)` and wire by actual port name.
- Transition labels can use event names directly, for example `ev_tick[T_ready]`.
- Events express discrete triggers. Complex judgments still belong in external Sysblock condition logic.

## Transitions

Create a default transition:

```python
t0 = M.CreateTransition(chart)
M.SetChartElementInfo(t0, "Destination", "Idle")
```

Create ordinary transitions:

```python
t1 = M.CreateTransition(chart)
M.SetChartElementInfo(t1, "Source", "Idle")
M.SetChartElementInfo(t1, "Destination", "Active")
M.SetChartElementInfo(t1, "LabelString", "[T_to_active]")
```

Label syntax:

```text
event[condition]{conditionAction}/transitionAction
```

Examples:

```text
[T_call]
[u > 0.5]
[fault]{faultCount := faultCount + 1;}/sm_y := 0;
```

Important 2026b runtime observations:

- `Condition`, `ConditionAction`, and `TransitionAction` are read-only. Set `LabelString` directly.
- In Sysplorer 2026b, an omitted or explicitly empty default-transition `LabelString` reads back as `[true]`. Treat it as the same semantic empty label only when the transition has no source object and its read-back `Condition` is `true`; ordinary transition labels remain exact.
- Prefer boolean Chart inputs such as `[T_call]`. Do not write boolean conditions as `[T_call > 0.5]`.
- Connect conditions with no judgment logic directly. For every transition condition with combinational logic, compute it outside the Chart in its own `Cond_<condition>` SubSystem and name the output after the condition; do not combine multiple Chart conditions in one subsystem or hide them inside an opaque composite block that cannot be traced one-to-one to named Chart conditions.
- Write an OClock only when that endpoint has an object. A default transition has no source object: keep `source_oclock=null` in its plan, write its free `SourceEndPoint`, and write `DestinationOClock` for the target; never write `Source` or `SourceOClock`. Read back the actual points.
- For serialized geometry strings in Sysplorer 2026b, use brace forms such as `"{x1,y1,x2,y2}"` for state `Position` and `"{x,y}"` for endpoints or `LabelPosition`. Never pass a bracket-shaped string such as `"[x,y]"`; see `runtime-contracts.md`.
- Do not directly edit `.mo` annotation text to move transition lines or labels. If the API cannot satisfy a layout request, state the API limitation rather than patching saved text.

## External Conditions, Timing, And Actions

- Place external `Cond_*` condition subsystems, the Chart, and external `Act_*` action subsystems in the Chart's immediate parent Sysblock as sibling components. Use `Cond_* -> Chart -> Act_*` as the default left-to-right data flow; raw inputs may also feed `Cond_*` or `Act_*` directly when required by their contracts.
- If a state action drives multiple external signals or contains complex calculation, selection, limiting, holding, or output-coordination logic, keep the Chart responsible only for business-mode selection and expose the minimum mode value or mode flags needed by `Act_*`. Classify timing separately by its purpose; do not assign it to `Act_*` automatically.
- Partition external action logic by functional cohesion rather than by a fixed output count. Keep outputs in one `Act_<action>` subsystem when they share substantial intermediate calculations or must be coordinated atomically; the subsystem may expose multiple Outports.
- Splitting by output is allowed. Use separate `Act_<output>` subsystems when outputs have independent calculations, enabling conditions, timing/sample behavior, safety handling, reuse, or reasons to change. Do not create single-output subsystems that only pass through or rename a mode value without adding a meaningful boundary.
- Encapsulate every business timer/counter and its reset/restart and threshold-comparison logic inside a named subsystem; never lay that timing chain out as ordinary blocks beside the Chart. Put transition-driving timing inside the corresponding `Cond_*` subsystem, and put output phase, cadence, or waveform timing inside the corresponding `Act_*` subsystem. When one timebase serves several conditions or actions, use one shared `Timing_*` sibling and branch its outputs instead of duplicating counters.
- In the parent-level preconnect manifest, mark every component or subsystem participating in business timing with `business_timing=true`. At a level that contains a Chart, each marked item must be a `SubSystem`; audit the interior of that subsystem at its own level instead of exposing its timing blocks beside the Chart.
- `UnitDelay` used to break state/mode feedback may remain beside the Chart, but the timer/counter and timing-threshold logic it feeds must be inside `Cond_*`, `Act_*`, or shared `Timing_*`. Never implement business counters or timers in Chart state actions.
- Boolean judgments inside transition-condition/action subsystems follow normal Sysblock boolean modeling rules.
- Do not use Chart-internal `after(...)` for business timing. Generate boolean transition conditions outside the Chart with state output feedback, `UnitDelay`, and timing blocks.
- Implement transition-driving business timing with this explicit pattern: `Chart mode/state -> UnitDelay -> active-state/reset-or-restart logic -> timer/counter -> CompareToConstant -> named boolean condition -> Chart`. Freeze whether timing starts on entry or the next tick, whether reset is level- or edge-driven, whether interruption resets/pauses/continues, the exact-threshold tick, and simultaneous safety-event priority before selecting blocks.
- Use only `UnitDelay` to break a state/mode feedback path that feeds transition-condition or timing logic.
- Reuse the same `UnitDelay` state-feedback chain when several timing/condition paths need the same state.
- Do not add `UnitDelay` to action outputs just because they are action outputs.
- Do not create an undelayed `Act_* -> Cond_* -> Chart -> Act_*` feedback loop. When a transition condition depends on the current mode, feed the Chart mode output through the required `UnitDelay` before `Cond_*`.
- Before generation, mark the `state output -> UnitDelay -> condition/timing subsystem` path and confirm there is no undelayed state-feedback loop.

## Chart Layout Planning

Start from the audited geometry-free Chart inventory in `sysblock-layout-input/v1`. It contains state/transition semantics and priorities but no state rectangles, rows, anchors, OClock values, label positions, or transition points. Generate those only in the hash-bound plan. Tighten State content before the Chart frame, prefer translation before resizing, and feed the final Chart frame upward before parent routing.

- Start from business semantics, then lay out by transition topology. Preserve state meaning, guards, actions, and priority; do not choose positions from semantic convention alone.
- Build the directed adjacency matrix before placing states. Record each state's degree, reciprocal state pairs, default entry, high-priority transitions, and legal hierarchy boundaries.
- Required priority: reduce top-level states before optimizing lines. If several states are internal stages, submodes, or local strategies of the same business mode, use nested states or subcharts first.
- Keep top-level states for system modes such as off, active, fault, hazard, reset, or monitor.
- Plan state positions and transition lanes before creating the Chart.
- In Sysplorer Chart coordinates, larger y renders higher; for `Position={x1, y1, x2, y2}`, the visual top is `max(y1, y2)`. Place the default state in the highest feasible row and enter its top edge vertically from a source whose y is greater than that visual top; do not use a lower row when an all-orthogonal higher layout exists.
- If a higher default-state placement is geometrically impossible, record the attempted higher layouts and the blocking crossings/overlaps before accepting a lower row; absence of this evidence fails pre-modeling planning.
- Place normal flow horizontally or vertically.
- Put fault, hazard, protection, emergency, inspection, or monitor states at a side or edge, not in the main-flow center.
- Keep symmetric behavior symmetric only when the transition topology can still provide an orthogonal lane for every transition.
- Do not accept a conventional semantic arrangement such as default state in the center, exceptional state above, and symmetric modes below until the complete transition graph proves that every edge has a valid orthogonal lane.
- Finish a static layout plan before API modeling: text-fit state sizes, final state rectangles, default-transition source points, every ordinary-transition axis and lane, uniform anchors, label positions, and expected non-orthogonal/crossing/overlap/shared-endpoint counts.
- The pre-modeling validation requires all expected issue counts to be zero. If the flat graph fails, redesign the state hierarchy or use junctions only for real business branching, merging, or dispatch semantics, then repeat planning.
- Use only supported state properties:

```python
M.SetChartElementInfo(state_id, "Position", "{x1, y1, x2, y2}")
M.SetChartElementInfo(state_id, "FontSize", "10")
```

- Size states from visible text first: state name, action lines, font size, and minimal padding. Use the smallest readable rectangle as the baseline.
- Enlarge a state only for concrete routing needs such as separating multiple anchors, preserving straight lanes, or avoiding label/line overlap. Record the reason when width or height exceeds the text-fit baseline.
- Do not shrink states so much that straight routes become impossible.
- A state with many transitions may be wider or taller. If there is no competing state horizontally, widen it; if there is no competing state vertically, heighten it.
- For a state with three or more incident transitions, calculate the independent anchors needed on each edge before choosing its final size. Enlarge only enough to separate those anchors and transition lanes, then tighten after the readback audit passes.
- Use state resizing or spacing adjustments to create straight transition lanes. Never accept diagonal ordinary transitions.
- After routing lanes pass, tighten oversized states again. A state with large blank area not justified by text fit or anchor-lane separation fails layout planning.
- Chart size is controlled at creation time with `AddComponent(..., x, y, w, h)`.
- Multi-port Charts need height for port count and width for the longest port name; do not place 10 inputs on a compact small Chart.
- After ports, labels, and route lanes are readable, tighten the Chart frame.
- Leave dedicated routing lanes around the Chart so condition/action lines do not hug edges, cross the Chart, or overlap labels.

## Transition Geometry

- Before endpoint or OClock selection, calculate x/y projection overlap for every state pair. Require the layout-profile minimum. If neither projection is sufficient, execute `translate -> bounded scale -> neighbour push -> recompute`; only after it succeeds may routing begin. Return `STATE_GEOMETRY_ADJUSTMENT_FAILED` if bounded adjustment cannot satisfy the graph. Repeated corner-point attempts are forbidden.
- Complete the full state placement, state size, OClock lane, label, crossing, and endpoint-load calculation before writing model geometry. Apply the planned layout in one API pass and expect the first audit to pass.
- For orthogonal ordinary transitions, choose the smaller state rectangle on the dimension perpendicular to the transition line as the anchor-distribution reference. Distribute anchors evenly on that smaller rectangle, then project the same x/y coordinate to the larger rectangle so both endpoints share one horizontal or vertical coordinate.
- For N same-pair or reciprocal lanes, use fractions 1/(N+1), 2/(N+1), ... N/(N+1) on the smaller perpendicular dimension. A single lane uses the midpoint.
- Treat OClock as a clock-angle ray from the state center, not an edge percentage: for center `(cx, cy)` and planned boundary point `(px, py)`, compute `OClock = (atan2(px - cx, py - cy) * 6 / pi) mod 12` (0/12 up, 3 right, 6 down, 9 left) separately for each state, then verify endpoints by readback and refine locally only if API rounding misses the planned point.
- Ordinary transitions must be two-point horizontal or vertical. In the current API, a multi-point line is not accepted as an orthogonal substitute because saved annotations may retain Bezier smoothing.
- Default transitions should enter the target state from above and should be vertical straight lines.
- Any non-horizontal/non-vertical transition fails the pre-modeling and readback audits. Redesign placement, state hierarchy, or semantically valid transition topology instead of documenting an exception.
- A two-point diagonal transition saved with Bezier smoothing is both non-orthogonal and a curve-rendering risk; it always fails.
- Separate reciprocal transitions with different `SourceOClock` / `DestinationOClock` values so they are parallel, not overlapping.
- Use `SourceOClock` and `DestinationOClock` for object-to-object transition endpoints.
- For a default transition, write the planned free `SourceEndPoint` and the target `DestinationOClock`; do not write `SourceOClock`. For object-to-object transitions, use OClock and repair with state placement instead.
- Do not use transition `Position` multi-point arrays as an audit-passing routing fix. Current Sysplorer StateMachine transition annotations may keep Bezier smoothing; more than two nonduplicate points fail the audit.
- After editing or recreating a transition, read back geometry with `GetChartElementInfos` and confirm the line is two-point and axis-aligned when intended.
- Reject every non-horizontal/non-vertical transition. If source and destination cannot obtain a clear same-row or same-column lane, return to topology and hierarchy planning.
- If an old transition keeps unwanted curve control points, delete and recreate it through the StateMachine API.
- Multiple transitions on the same state edge must use separated source/destination anchors. Arrows, lines, and execution-order numbers must not share one point.
- Do not allow many transitions to converge through the Chart center.

## Labels

- Every recreated transition needs a new `LabelPosition` write. Recreated elements get new handles and do not keep old label geometry.
- Record a string `label` field and two-number `label_position` for every transition. An unlabelled default transition uses semantic `label=""` and does not create a label box; saved/readback `[true]` is canonicalized to empty only under the default-transition rule above. Ordinary transitions require a nonempty exact label.
- Select exactly one `LabelPosition` rule from read-back geometry after removing consecutive duplicate points. A two-point horizontal or vertical line uses a relative offset; every other non-orthogonal, curved, or intermediate-point route uses an absolute Chart coordinate. Do not mix the two rules.
- For a two-point horizontal or vertical line, use `[-0.55 * len(label), 0]` as the default relative offset from the midpoint label anchor. Require `abs(x - expected_x) <= max(2, 0.2 * len(label))` and `abs(y) <= 4` unless a tighter project rule applies.
- For a non-orthogonal, curved, or intermediate-point route, set the absolute `LabelPosition` near the midpoint of its longest visible segment. Audit this absolute position even when the route separately fails the transition-geometry audit.
- Include `label`, `condition`, `label_position`, and enough route points to select the rule on every transition in readback evidence; pre-modeling evidence need not invent a runtime `condition` field. Missing fields needed by the applicable rule, an empty ordinary-transition label, a position using the wrong rule, label boxes overlapping states or other labels, or labels intersecting unrelated transition lines fail the audit.
- Relative offsets may repeat on different transitions; uniqueness of raw `LabelPosition` values is not a validity criterion.
- Straight-transition labels must stay near their segment midpoint; routed/curved-transition labels must stay near the selected longest-segment midpoint.
- After setting `LabelPosition`, set `FontSize` again because label writes can disturb rendering.

## Priority

- Use `ExecutionOrder`, not `Priority`, and group it by source because only same-source transitions compete. Create all ordinary outgoing transitions from a source before assigning and reading back a contiguous `1..N` sequence; an order greater than the current outgoing count can be rejected while siblings are missing.
- Hazard, fault, emergency-stop, safety, and protection transitions should normally be first `ExecutionOrder` from the relevant source unless external logic guarantees mutual exclusion.
- Execution-order numbers must not cover state borders, labels, arrows, or other lines.

## Layout Audit

Every Chart must pass this audit after creation or modification:

- Structure and hierarchy: states do not overlap and state text is readable. Top-level complexity is reduced by nesting when internal stages, submodes, or local strategies belong under the same business mode. Ordinary transitions prefer same-level states. Do not transition directly into another same-level state's child; enter the parent and let its default transition select the child. Child-to-upper-level transitions are allowed when they express leaving the nested mode. Every exclusive submachine has a valid default transition.
- Arrangement and size: normal flow is horizontal or vertical. Exceptional states are at a side or edge. State boxes are compact but readable. High-connectivity states may be widened or heightened to separate anchors and reduce bends/curves when that does not create meaningless blank area.
- Transition geometry: default transitions enter vertically from above. Every ordinary transition is a two-point horizontal or vertical line. Any diagonal or multi-point transition fails. Reciprocal transitions are non-overlapping. Same-axis segments with overlapping ranges fail even if both are straight. Shared or overloaded endpoints fail.
- Labels and priority: every transition records its label and geometry-matched `LabelPosition` in both plan and readback evidence; an unlabelled default records `label=""`, while ordinary labels are nonempty. Two-point horizontal/vertical lines pass the relative-offset bound; all other routes use an absolute coordinate near their longest visible segment midpoint. Estimated nonempty label boxes do not overlap states, other labels, or unrelated lines. Every deleted, recreated, or adjusted transition gets `LabelPosition` written and read back. Audit `ExecutionOrder` by source.
- Junctions and complex line nets: Junctions are allowed only for real control-flow branching, merging, or path reuse. Junctions added only for beauty, rerouting, or label movement fail. Center convergence, heavy crossings, label piles, shared anchors, slanted default transitions, forbidden cross-level transitions, and overlapping reciprocal lines fail.
- Audit evidence: use API-written/readback state and transition geometry plus saved-annotation static checks when needed. Explicitly list forbidden cross-level transitions, allowed child-to-upper-level exits, non-horizontal/non-vertical transitions, diagonal two-point Bezier risks, multi-point transitions, same-axis overlaps, and shared or overloaded endpoints. Every listed geometry issue must be empty.
- Pre-modeling layout evidence must include the business-semantic state set, default state and its upper-row decision, directed adjacency matrix, hierarchy decision, text-fit and final state sizes, resize reasons, every transition axis, smaller perpendicular reference state, lane index/count, projected anchor coordinate, computed OClock, label text, geometry-selected `LabelPosition` mode/value, and expected geometry/label issue counts. All expected counts must be zero before API modeling.

Final acceptance:

- Models without Charts: `CheckModel=true` plus Sysblock layout audit passed.
- Models with Charts: `CheckModel=true` plus Sysblock layout audit passed plus internal Chart layout audit passed.

## API Pattern

```python
chart = M.GetBlockHandle(model, "mode_chart")
state_ids = M.GetChildren(chart, "State")
transition_ids = M.GetChildren(chart, "Transition")
info = M.GetChartElementInfos(element_id)
```

Use `SetChartElementInfo(state_id, "Position", ...)` for states. For transitions, prefer OClock and label writes. Do not edit saved `.mo` text.

Reusable script references:

- `scripts/layout_plan_tool.py statechart` for cyclic/acyclic planning, projection repair, default transitions, OClock values, and pre-modeling Chart geometry audit.
- `scripts/audit_sysblock_model.py` for the final saved/readback structured-evidence audit. For StateMachine transition evidence, mark transition routes with `type`, `kind`, `route_type`, or `call` set to `transition`, and include `smooth` / `annotation_smooth` when saved annotation evidence is available.

## Common Pitfalls

- Never directly edit `.mo` text to build Sysblock topology or repair StateMachine layout.
- Recreating Chart elements invalidates old handles; after unload/reload, read handles back again.
- If Chart data is created before states, later data may be captured into a state; create states first, then Chart-level data.
- State names can conflict with top-level module names. Read back after creation.
- `Position` is valid for states. For transitions, treat it as readback/debug evidence only; do not rely on multi-point transition `Position` to pass the geometry audit.
- If a layout demand exceeds API support, report the limitation rather than editing saved `.mo` text.
