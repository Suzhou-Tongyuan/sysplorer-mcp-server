# Error Repair Playbook

Use as domain evidence under the parent debugging route for existing faults; do not restart model construction. During new construction, repair and return to its originating failed stage. Parent shared standards own MCP session, error parsing and retry limits; read-only diagnosis must account for automatic layout writeback.

## Repair Loop

1. Name the failed step: source, requirement, mapping, parameter, construction, check, translate, simulate, result verification, diagram review, or delivery.
2. Capture the concrete symptom: MCP error, failed variable lookup, NaN/divergence, zero flow, reversed motion, missing temperature response, missing wire, invisible instance, red dashed endpoint, or stretched symbol.
3. Classify the fault.
4. Identify the shortest active failure chain.
5. Apply the smallest meaningful repair only within permitted edits. For read-only diagnosis, provide findings and proposed fixes without changing the model; a failed check does not authorize a patch.
6. Return to the affected required step using the original offline or authorized live mode. Offline file work repeats static review and does not start Sysplorer or acquire live checks. Query/post-processing corrections reuse valid existing results and repeat only affected queries/verification; missing or invalid results are a blocker unless new simulation is within scope.
7. Resume affected required stages up to the user's endpoint. Visual Gate 6 findings do not block physical check/translation/simulation; complete them before full graphical delivery. Unrequested result and report steps remain not_required.

## Fault Classes

| Class | Typical Signal | First Repair Target |
|---|---|---|
| Source/input | Missing model path, ambiguous system target, no success criteria | Return to requirement extraction and mark `to confirm`. |
| Library/dependency | Class missing, wrong TY family, missing medium package | Load or switch to the correct TY system and medium libraries. |
| Component mapping | Wrong component family, system task built from component-design library | Remap through `references/component-map.md`. |
| Medium | Oil/gas package missing or incompatible | Select `TYOilMedia` or `TYGasMedia` and propagate medium consistently. |
| Topology | Unconnected ports, wrong P/T/A/B, missing return or exhaust | Repair the topology table and then `connect(...)`. |
| Capacitor/resistive topology | Direct resistive-resistive or capacitive-capacitive fluid connection, wrong `UseVolume*` side, unsupported nested check item | Select offline review, read-only diagnosis, or authorized live repair through `references/capacitor-resistive-check.md`; rerun only affected required checks in that mode. |
| Parameter | Missing source, illegal value, unit mismatch, wrong initial condition | Repair only the active parameter blocker and record assumptions. |
| Initialization | Conflicting starts, impossible initial state | Relax or align initial states with physical boundaries. |
| Translation | Equation/variable mismatch, unsupported component combination | Remove the smallest incompatible combination or set required switches. |
| Simulation | NaN, divergence, tiny steps, no motion, pressure explosion | Check boundaries, relief/exhaust path, stiffness, input timing, and load direction. |
| Result variable | Target variable missing or wrong path | Query component ports/result info and adjust variable names. |
| Graphical annotation | Invisible instance, missing wires, red dashed lines, stretched symbols | Repair `Placement`, `Line`, `Diagram`, connector anchors, and extents. |

## Domain-Specific Shortcuts

- No motion: check medium, source, return/exhaust, valve state, then load direction.
- Zero flow under commanded actuation: check real `connect(...)`, valve opening state, boundary pressure/flow, and source drive.
- High pressure: check blocked return/exhaust, missing relief path, wrong valve port semantics, and load direction.
- Capacitor-resistive check failure: evaluate adding or enabling one needed volume/capacitive element between resistive elements, inserting resistance between capacitive elements, or repairing nested subsystem topology. These are repair candidates; apply them only within authorized edits and keep read-only diagnosis as findings/suggestions.
- Reversed displacement: check actuator chamber connections, load sign, and command polarity.
- No thermal response: check `TYThermalHydraulics`, heat boundary, `useHeatPort`, and temperature variables.
- Pneumatic instability: check gas source, exhaust boundary, `TYGasMedia`, chamber volume, and valve state.
- Diagram not visible: check `Placement` first, then `Diagram`, then export/review.
- Diagram has components but no wires: check whether plain `connect(...)` equations lack `annotation(Line(points=...))`, then repair route points and rerun diagram review.

## Repair Output

For each repair iteration, keep internal notes with:

- failed step
- symptom
- fault class
- root-cause hypothesis
- repair action
- rerun result

Only include these details in the final response when they are useful to the user or when a blocker remains.
