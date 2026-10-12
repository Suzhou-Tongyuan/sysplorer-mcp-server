# Energy Domain Rules

## Allowed Scope

- Apply this library set to the energy subsystem assigned by the parent, not the complete cross-domain delivery. Preserve parent-selected standard components and approved support domains:
  - 光伏发电库
  - 风力发电库
  - 电池库
  - 综合能源系统库
  - `Modelica 4.0.0.TY.1`
- If a required behavior lacks a supported component, report the gap to the parent project library selection; do not delete sufficient standard components or already-selected support domains. Mere lookup/load failure is not proof of a capability gap. This commercial path fixes Modelica at `4.0.0.TY.1`; report conflicting engineering versions without silent rewrites.

## Selection Priority

These priorities apply only after the parent has selected the commercial supplement. With no established library boundary, evaluate standard-library capability first; retain sufficient standard parts and use TY classes only to fill documented gaps.

- For photovoltaic generation behavior, prefer direct PV-domain classes first.
- For wind-power generation behavior, prefer direct wind-domain classes first.
- For storage behavior, prefer battery-domain classes first.
- For multi-energy coupling, dispatch, thermal-hydrogen integration, or cross-domain auxiliaries, prefer the integrated-energy library first.
- For generic boundaries, math, signals, adapters, and standard physical interfaces, prefer semantically suitable classes from `Modelica 4.0.0.TY.1`.

## Modeling Order

1. Main energy conversion path
2. Boundary and source completion
3. Control and supervisory logic
4. Measurement and result probes
5. Economic or scheduling auxiliaries if required

## Layout Rules

- Keep the main energy flow left to right whenever feasible.
- Separate control logic from the main physical chain.
- Avoid overlapping components and unreadable connections.
- Re-run or refine layout after structure changes affecting readability.

## Parameter Rules

- Respect declared units and avoid mixed unit systems in one inferred parameter set.
- Prefer user targets first, documented manual values second, conservative engineering defaults third.
- Change one parameter group at a time during debugging or tuning.

## Simulation Rules

- Use a short bring-up horizon first.
- Prefer conservative solver and tolerance settings before structural simplification.
- Set `verify_result_var` only when result verification belongs to the agreed scope; otherwise omit it and mark result review `not_required`.

## Result Rules

Apply only when requested or needed for the agreed acceptance criterion. A successful simulation and accepted physical results are separate outcomes. Verify current-run/explicit-file provenance, and retain MCP warning for interpolation or endpoint fallback; never treat stale values or interpolation as fresh raw samples.

- Judge against explicit user targets when available.
- When result review is requested but a criterion is incomplete, explain the needed criterion or a clearly marked assumption that is necessary for that request. Do not infer proxy observables merely to fill an acceptance form or expand a simulation-only task.
- Evaluate steady-state value, overshoot, rise time, and trend consistency when applicable.
