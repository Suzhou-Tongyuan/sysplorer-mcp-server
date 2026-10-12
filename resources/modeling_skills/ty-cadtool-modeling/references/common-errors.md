# Common Errors & Repair Playbook

Ordered by where they bite in the pipeline. Always fix the **earliest** blocker, then re-run from that stage.

## Import stage

| Signature | Cause | Fix |
|---|---|---|
| `ImportCad` returns False / nothing loads | Path has Chinese or special characters, or is relative | Use an **absolute, ASCII-only** path. Copy the file to e.g. `C:\work\model.step` first. |
| "format not supported" | Unsupported extension | Only `STEP / IGES / sldasm / CATProduct / ty3d`. Re-export from the CAD tool to STEP. |
| `ImportCad` disabled | Called during iteration design | Exit iteration (regenerate / reopen) before importing a new file. |
| Geometry imports but parts are missing/merged | Source assembly issue | Re-export with the assembly structure preserved; verify with `GetParts()`. |

## Workbench / naming stage

| Signature | Cause | Fix |
|---|---|---|
| "operation not supported in current workbench" | Element call doesn't match active workbench | `SwitchWorkbenchType` to MultiBody (joints/markers/contacts) or Fluid (slices/ports) before the call; confirm with `GetWorkbenchType()`. |
| "entity not found" / call fails on a name | Guessed name or wrong hierarchy | Query the real name: `GetParts`, `GetParts("<group>")`, `GetMarkers`, `GetConnectors`, `GetGeometricElementIdsOfPart`. Multibody = dotted (`base.gear`); fluid = bare (`Tank1`). |
| `GetGeometricElementIdsOfPart` / `Measure` returns `The part "..." does not exist!` **after grouping** | Reused the pre-group dotted path — grouping re-parents the part so its path changed (`Pin_6.Pin_7` → `rocker.Pin_7`); `GetGeometricElementIdsOfPart` resolves by current path. (The leaf name is unchanged; only the path prefix moved.) | **Measure before grouping** and capture numeric world coords (they're grouping-invariant), then build joints from the numbers. If you must measure after grouping, re-query `GetParts("<group>")` for the part's real current path first — never guess `<group>_1`. See `references/joint-placement.md` → Order of operations. |
| RefMarker creation fails | Base marker and ref share a top group | Put the reference marker's target part in a **different** top-level group. |

## Build / CheckDesign stage

`CheckDesign()` flags: low OpenGL, no parts, empty groups, **ungrouped parts**, invalid parts, **markers without a reference marker**, **unknown joints**, inertia-rule violations; fluid: multiple slices per tank, port-only parts.

| Signature | Cause | Fix |
|---|---|---|
| Ungrouped parts reported | Parts not grouped into bodies | `CreateDefaultGroups()` or `MoveToGroup`/`CreateGroup`. |
| Too many Fixed joints / a Fixed joint between two real parts | Rigidly-connected parts modelled as separate bodies instead of merged | Merge those parts into **one group** (`CreateGroup`/`MoveToGroup`) and delete the Fixed joints. Keep exactly one Fixed joint, to `"Ground"`. Extra Fixed joints also break planar-loop auto-detection downstream. |
| Joint coords guessed (CheckDesign passes but you typed numbers you didn't measure) | Blind placement | Read position/axis from geometry with `Measure` and the axis→Euler helper — see `joint-placement.md`. |
| Unknown joints reported (often from `ty3d`) | Joint type couldn't be inferred | `GetUnknownConnectors()` then `ModifyUnknownConnector(name, {"type": DesignElemtType.ConnectorRevolute, "position":[...], "rotation":[...]})`, or delete and recreate with `CreateConnector`. |
| Marker without ref-marker | Dangling marker | Add `CreateRefMarker`, or delete the unused marker. |
| Model floats / "no fixation" | No world anchor | Add one `ConnectorFixed` against `"Ground"`. |

## Generate / translate stage

| Signature | Cause | Fix |
|---|---|---|
| Redundant equations / DAE index / over-constrained on a **planar** mechanism, **no auto cut joint appeared** | Auto-detection couldn't find a clean loop — usually because a rigid body was split into several groups wired by Fixed joints (pollutes the group graph the detector walks) | **Fix the grouping first**: merge mutually-fixed parts into one group, keep one Fixed joint to `"Ground"`, regenerate — the cut is then auto-inserted. See `multibody-elements.md` → Grouping. |
| Over-constrained on a **spatial** loop (non-parallel revolute axes), or auto-detection genuinely missed | Auto-cut only fires for planar loops with parallel axes | Cut one joint manually **post-generation**: swap one loop Revolute to `TYMultibody.Joints.RevolutePlanarCut` via `SetComponentInfo`. (Note: `PlanarLoopConstraint` is **not** a cut — see next row.) See `multibody-elements.md` → Problem A. |
| Planar loop **fails to initialize** in simulation (init error / residual not converging), but it is **not** reported over-constrained | CAD assembly precision (~1e-6) below solver precision (1e-10) → auto-derived loop-joint orientations are slightly off | Unify orientations **pre-generation** with the 平面环处理 tool: `PlanarLoopConstraint(base_connector, [others], is_reversed, base_rotation)` — aligns all loop-joint poses (the `double_slider` case), then regenerate. This is **orientation unification, NOT a cut**. See `multibody-elements.md` → Problem B. |
| Wrong simulate target | Assumed model name | The simulatable top model is `<package>.<cad_model>.<cad_model>_main` — construct it from the package name and the imported file's model name (e.g. `Default.crank_rocker_mechanism.crank_rocker_mechanism_main`). **`GetModels()` returns CAD-browser ids** (e.g. `Default.crank_rocker_mechanism.step`) used by `OpenModelInCadBrowser`, not the `_main` target. Confirm the exact name via `model_manager(action="get_components")` or rely on the verified `_main` convention. |
| Diagram unreadable | Layout edge case | `GenerateMoModel` normally lays out; only then fall back to `smart_layout(mode="writeback_mo", auto_layout=true)` and re-`check_model`. |

## Simulate / result stage

| Signature | Cause | Fix |
|---|---|---|
| Initialization fails | Inconsistent joint initial states | Query real keys with `GetConnectorParams`, set consistent `phi_rel_0`/`s_rel_0` etc. via `ModifyConnectorParams`; relax `stateSelect`. |
| Animation chaotic / parts fly apart | Wrong joint axis/pose (usually guessed coords), missing cut, bad mass | Re-derive the joint `coord` from geometry (`Measure` → centre + axis→Euler, `joint-placement.md`) and re-check with the `Coaxial`/`Parallel` two-feature measure; confirm loop cut; verify mass/inertia via `GetPartParams`. |
| Result differs from expectation | Driver type/units, gravity off | Check `ModifyJointMotionParams` motion_type & start values; `ModifyGravityParams`. Disable world animation noise: `SetParamValue("world.animateWorld","false")`. |

## Parameter discipline (prevents a whole class of failures)

`Modify*Params` keys are **type-specific**. Setting a Prismatic key on a Revolute, or passing a plain list where a `"{a, b, c}"` string is required (spherical, gravity direction), silently no-ops or errors. Always `Get*Params` the element first to learn the real keys, then modify.

## Hard bans (never do these from run_script)

- `ClearAll` — wipes loaded libraries, translation cache, results.
- `ChangeDirectory` — breaks MCP workspace rules.
- `Exit()` and `session_manager(shutdown/force_restart/restart(full_reset))` when attached to a user GUI — closes their window.
- `get_api_document` for CADToolbox functions — returns empty; use `help(cadtool.<fn>)` via run_script instead.
