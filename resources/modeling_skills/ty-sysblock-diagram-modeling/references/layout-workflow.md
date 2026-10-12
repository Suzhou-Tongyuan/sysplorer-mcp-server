# Sysblock Layout Workflow

This file is the sole authority for geometry-free input, layout planning, routing order, and saved/readback layout acceptance.

## Ordered workflow

1. Freeze semantics, topology, port metadata, signal directions, feedback paths, and affected hierarchy.
2. Project them into `sysblock-layout-input/v1`; remove all coordinates, sizes, layers, anchors, lanes, route points, O'Clock values, and label positions.
3. Run `layout_input_tool.py audit` and retain its canonical hash.
4. Run `layout_plan_tool.py block` or `statechart`; bind the plan to the input hash.
5. Audit the plan before changing the formal model.
6. Apply placement, configure variable ports, connect, then use `RouteLine` after placement stabilizes.
7. Adjust placement before adding explicit bends. Use explicit routes only for violations that remain.
8. Save, force-reload, extract structured final geometry, and rerun the canonical audits.
9. Run `audit_sysblock_model.py` on the saved/readback structured evidence; evaluate parent-required check/test evidence separately.

Do not reorder these stages. In particular, do not route first and try to rescue an infeasible state/component arrangement with corner enumeration.

## Coordinate-free input

Use `layout-input.schema.json` as the schema authority. Include complete levels, nodes, ports, edges, feedback paths, Charts, states, transitions, priorities, and policies. Declare each Chart as `exclusive` or `parallel`; `prepare` defaults an omitted declaration to `exclusive`. `layout_input_tool.py prepare` strips accidental geometry; `audit` rejects geometry, invalid topology, missing exclusive defaults, parallel top-level defaults, duplicate priorities, and noncanonical values.

## Sizing and placement

- Ordinary blocks retain standard size.
- Compute the minimum size of each resizable object independently from text, ports, pitch, inner content, and margins.
- Uniform subsystem sizes are optional only after independent minima are known.
- Compute row pitch independently per layer and center each occupied layer vertically; a tall node in another layer must not inflate ordinary-block spacing.
- Reserve name, port-label, parameter, note, feedback-return, and interface-clearance regions.
- Keep Inports left and Outports right of the full component-and-route envelope.
- For one core SubSystem/Chart, align boundary ports with the corresponding core ports where this preserves order and clearance.
- Order unambiguous same-layer, single-output fan-in sources by their target-port order. For multi-target, multi-output, or cross-layer relations, do not infer a vertical order; judge their authoritative route geometry instead.

## Routing

- Use straight `ConnectPort(model, source, target)` when possible.
- When `RouteLine` will run after connection, plan blocks with `--mode preconnect`; its ordinary route points are non-authoritative until routed and read back.
- Grip points contain bends only.
- Keep interface-adjacent segments horizontal; keep one-to-one interface paths horizontal whenever feasible.
- Treat feedback as declared directed paths. Reserve their return region before primary placement and mirror right-to-left members when semantics and port order remain correct.
- Fail distinct routes sharing a positive-length collinear segment.
- Fail crossings through unrelated frames or text/no-crossing regions.
- After any explicit route, read back saved points. Do not call `RouteLine` again unless intentionally accepting a complete reroute and re-audit.

## StateMachine geometry handoff

The StateMachine planner first checks source/target projection overlap. If it is below the profile minimum, it must adjust state rectangles before producing endpoints:

1. minimum collision-free translation;
2. bounded scale toward the other state;
3. deterministic neighbour push if added size consumes required clearance;
4. recompute all affected projections;
5. fail with `STATE_GEOMETRY_ADJUSTMENT_FAILED` if no bounded arrangement exists.

No corner enumeration is a fallback. See `state-machine.md` for transition semantics and labels.

## Saved/readback audit

Audit every affected level and Chart from the saved/force-reloaded model. Require:

- complete hierarchy coverage;
- valid endpoints and declared required connectivity;
- no overlap, avoidable crossing, shared lane, no-crossing-region hit, or interface-envelope violation;
- valid state/transition topology, labels, priorities, and geometry;
- final model and plan/input hashes matching the evidence;
- all checks and tests required by the parent workflow.

Missing levels, missing readback sources, or stale hashes fail closed. A successful static plan or saved/readback audit alone never proves complete validation.
