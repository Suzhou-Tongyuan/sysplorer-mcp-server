# Multibody Elements

Rules for building a multibody model on imported geometry. Switch to `cadtool.SwitchWorkbenchType(CadWorkbenchType.MultiBody)` before any of this.

## Entity naming (address everything by exact name)

Names are **hierarchical, dot-joined from the top node down**. After import, a part typically appears as `Group.Part_n`:

- Part / group / sub-body: `"base.Base_1"`, `"grip.fingertips_1"` (top group `grip` → part `fingertips_1`).
- Marker: lives in a top group → `"base.Marker1"`.
- Reference marker: addressed like a marker.
- Design point: on a part → `"upperarm.Point1"`.
- Connector / driver / contact: **bare name**, e.g. `"Revolute1"`, `"Rotational1"`, `"Contact1"`.
- World anchor: the special entity literal **`"Ground"`** (only valid as a `second_entity` for a fixed/joint to the world).

Never invent names. Query first: `GetParts()`, `GetParts("grip")`, `GetMarkers("base")`, `GetConnectors()`, `GetDesignPoints("upperarm.upperarm_1")`, `GetGeometricElementIdsOfPart("base.gear", ShapeType.Face)`.

## Coordinates

`coord = [x, y, z, rx, ry, rz]` — position in **metres** in the assembly's **world frame** (stored verbatim, no part-local transform), orientation as **extrinsic-XYZ Euler angles in degrees**. The orientation's job is to point the joint's **functional axis** (the joint frame's local **+Z** — rotation axis for Revolute/Cylindrical, slide direction for Prismatic) along the real axis of motion; for those joints the in-plane X/Y spin is kinematically irrelevant. Universal joints append a second orientation triple: `[x, y, z, rx1, ry1, rz1, rx2, ry2, rz2]`. When **series-adding** a joint onto an existing marker (passing a marker as `first_entity`), pass only the rotation part `[rx, ry, rz]`; position is inherited.

**Do not invent these numbers.** You are blind through the MCP — read the position and axis out of the geometry with `Measure` (single circular edge → `Center Position`; vertex → `Vertex Position`; two features → `Coaxial`/`Parallel`/`Angle` to verify). The full recipe, the axis→Euler helper, and a worked example live in **`references/joint-placement.md`** — use it for every joint whose location you don't already know.

## Grouping — one rigid body = one group (the invariant)

The imported tree is usually flat parts. Each **group becomes exactly one rigid body** in the generated model, so the grouping *is* the body topology. The rule that prevents the most damage:

> **Parts that don't move relative to each other go into ONE group. They are never tied together with a `ConnectorFixed`.** A Fixed joint between two real parts is a modelling smell — merge them into a group instead.

```python
cadtool.MoveToGroup(["Pin_2.Pin_3"], "crank")          # one moving link = one group
cadtool.CreateGroup(["Base.Base_1", "Base_2.Base_3"], "base")  # several rigidly-fixed parts -> ONE body
cadtool.ClearGroups()                                   # drop leftover empty groups
# cadtool.CreateDefaultGroups()                         # auto-group everything still ungrouped
```

**Why this matters (not just tidiness).** At generation the toolbox **auto-detects planar closed loops and auto-inserts the cut joint** — but the detector walks a graph whose **nodes are groups** and whose edges are the joints between them. If you split one rigid body into several groups wired by Fixed joints, you inject extra nodes and edges that **pollute that graph**: the clean kinematic loop (where all revolute axes are parallel) is no longer the loop the search finds, so it fails to recognise the planar loop, skips the cut, and the model comes out over-constrained (translate/simulate fails with redundant equations). Merge the rigid parts and the loop becomes clean again. This is why `ball_four_link` merges its two base parts into one `base` group rather than fixing them together.

Reserve `ConnectorFixed` for exactly one use: anchoring **one** body to `"Ground"` (next section). A healthy multibody model has **exactly one Fixed joint, and its `second_entity` is `"Ground"`.** If you've written a second Fixed joint, or a Fixed joint between two parts, stop and group those parts instead.

## Joints (`CreateConnector`)

`CreateConnector(type, name, first_entity, second_entity, coord)`. The two entities are the bodies (or part/design-point/marker) the joint couples.

| Joint | `DesignElemtType` | DOF freed | Can carry a driver? |
|---|---|---|---|
| Fixed | `ConnectorFixed` | 0 (rigid) | no |
| Revolute | `ConnectorRevolute` | 1 rot | **yes** (rotational) |
| Prismatic | `ConnectorPrismatic` | 1 trans | **yes** (translational) |
| Cylindrical | `ConnectorCylindrical` | 1 rot + 1 trans | **yes** |
| Spherical | `ConnectorSpherical` | 3 rot | no |
| Universal | `ConnectorUniversal` | 2 rot | no |
| Screw | `ConnectorScrew` | coupled rot/trans | no |
| Planar | `ConnectorPlanar` | 2 trans + 1 rot | no |

(`ConstantVelocity`, `InLine`, `InPlane`, `Orientation`, `ParallelAxes`, `Perpendicular` exist in the enum; `ConstantVelocity` is marked 未开发/not implemented.)

**World anchor** — every mechanism needs exactly one tie to ground, or the model is under-determined:

```python
cadtool.CreateConnector(cadtool.DesignElemtType.ConnectorFixed, "Fixed1",
                        "frame.frame_1", "Ground",
                        [-0.515, -0.007, 0.05, 0, 0, 0])
```

A typical revolute (from `crank_rocker_mechanism`):

```python
cadtool.CreateConnector(cadtool.DesignElemtType.ConnectorRevolute, "Revolute2",
                        "frame.frame_1", "crank.crank_1", [0, 0, 0.05, 0, 0, -90])
```

## Drivers (`CreateJointMotion`)

A driver prescribes motion on a Revolute / Prismatic / Cylindrical joint:

```python
cadtool.CreateJointMotion(cadtool.DesignElemtType.MotionRotational, "Rotational1", "Revolute3")
```

Driver kind (`JointMotionType` via `ModifyJointMotionParams`): `Displacement` (no start values editable), `Velocity` (`phi.start`/`s.start` editable), `Acceleration` (all start values editable).

## Markers and reference markers

A marker is a frame on a part; a reference marker links it to a second body and is how the generated model wires `frame_a`/`frame_b` when you connect via markers (see `double_pendulm`):

```python
cadtool.CreateMarker("Marker1", "upper_arm.upper_arm_1", [0, 0, 0, 0, 0, 0])
cadtool.CreateMarker("Marker2", "upper_arm.upper_arm_1", [1, 0, 0, 0, 0, 0])
cadtool.CreateRefMarker("upper_arm.Marker2", "lower_arm.lower_arm_1")
```

Rule: a base marker and its reference marker (and multiple refs of the same base) **must not share a top-level group**.

## Design points

Three constructors — use the one matching the geometry you can pick reliably:

```python
cadtool.CreateDesignPointByPick("Point1", "upperarm.upperarm_1", [0.087, 0.158, 0])
cadtool.CreateDesignPointByMidpoint("P2", "upperarm.upperarm_1", [-0.045,0.162,0.024], [0.020,0.162,-0.024])
cadtool.CreateDesignPointByOffset("P3", "upperarm.upperarm_1", [-0.013,0.162,0], [0,0,90], 0.05)
```

Design points are handy as `first_entity` of a joint (lets you place the joint precisely without typing a coord).

## Contacts

Contacts need **face ids**, obtained from `GetGeometricElementIdsOfPart`:

```python
faces = cadtool.GetGeometricElementIdsOfPart("upperarm_1.upperarm", cadtool.ShapeType.Face)
# faces is like ["upperarm_face <1>", "upperarm_face <27>", ...] — pick the contacting face id
# (the <N> in the string is the geometry id, NOT the list index)
cadtool.CreateContact(cadtool.DesignElemtType.ContactSphereToSphere, "Contact1",
                      "upperarm_1.upperarm", "upperarm_face <27>",
                      "forearm_1.forearm", "forearm_face <53>")
```

Type ↔ required faces: `ContactSphereToSphere` (two spheres), `…ToCylinder` (sphere+cylinder), `…ToRectangle` (sphere+rectangle), `…ToCircle` (sphere+circle); for the asymmetric types the two faces may be given in either order. Tune with `ModifyContactParams` (`k, d, n1, n2, p_max, mue_k, mue_s, mue_r, k_v, v_e1, v_e2`).

## Gravity

```python
cadtool.ModifyGravityParams({"gravity_type": cadtool.GravityType.UniformGravity,
                             "acceleration": 9.81, "direction": "{0, 0, -1}"})
```

`direction` is the `"{x, y, z}"` string format. `PointGravity` uses `constant` instead; `NoGravity` disables both.

## Material / mass

Mass and inertia are computed from the solid + material density. Override with `ModifyPartsParams` (`material_name` / `density` / `mass` — not together), or manage the material library with `AddNewMaterial` / `BatchModifyMaterial` / `RestoreDefaultMaterial`. For non-solid (surface) parts you may set `mass`, `centroid`, `inertia_moment[9]` directly.

## Closed loops (handle, or it over-constrains)

A closed loop (four-bar, crank-rocker, crank-slider, coulisse) is kinematically over-constrained — translate/simulate fails with redundant-equation / DAE-index errors — and, separately, a planar loop can also **fail to initialize** because the CAD joint orientations are imprecise. These are **two different problems with two different tools** — do not conflate them.

### Problem A — over-constraint → a **cut joint** is needed

**First: let the toolbox do it.** For a **planar** loop with **parallel revolute axes**, `GenerateMoModel` **auto-detects the loop and auto-inserts the cut joint** — *provided the grouping is clean* (one rigid body per group; see Grouping). You usually do **nothing**: the bundled `crank_rocker_mechanism` has a 4-revolute loop and no manual cut anywhere. So before reaching for a manual cut, get the grouping right and try generating — most planar over-constraint reports are really "this rigid body was split by Fixed joints," not "I forgot to cut."

**When auto-detection won't fire** — the loop is **spatial** (revolute axes not parallel, e.g. a ball/3-D four-bar), mixes joint types the detector rejects, or the geometric test otherwise misses — cut one joint yourself, **post-generation**, by swapping one loop Revolute to a cut joint via the core API (used by `ball_four_link`, a spatial loop):

```python
import mworks.sysplorer as ModelingPy
ModelingPy.SetComponentInfo("Default.ball_four_link.ball_four_link_main",
                            "Revolute3", "Type", "TYMultibody.Joints.RevolutePlanarCut")
```

Cut a joint that carries **no driver** and least affects the output variables. There is **no standalone cut API** in CADToolbox — the cut is either automatic at generation or this post-gen `RevolutePlanarCut` swap.

### Problem B — planar-loop init failure (precision) → **orientation unification** with `PlanarLoopConstraint`

A model assembled in CAD carries ~`1e-6` precision; Sysplorer's solver wants `1e-10`. For a **planar** loop, the slightly-off auto-derived joint orientations make the generated model **fail to initialize in simulation** even though it isn't over-constrained. The **平面环处理** tool fixes this by **unifying all loop-joint orientations** onto a base orientation (optionally Z-reversing individual joints) — it is **NOT a cut**, and it runs **pre-generation** (this is exactly what the `double_slider` CATIA case does, then generates with no manual cut):

```python
# base_connector = reference joint; connector_arr = joints to align onto it;
# is_reversed = per-joint Z-reverse bools (same length); base_rotation = [Rx,Ry,Rz] (empty = base's current pose)
cadtool.PlanarLoopConstraint("Revolute1", ["Revolute2", "Revolute3", "Revolute4"],
                             [False, False, True], [0, 0, -90])
```

### Recommended order

clean grouping → (planar loop with init/precision trouble) `PlanarLoopConstraint` to unify orientations → `GenerateMoModel` (auto-cut for parallel-axis planar loops) → if still over-constrained, post-gen `RevolutePlanarCut`. **Always record** which tools you used (orientation unify / auto-cut / manual cut), which joint, and why, in the delivery notes.

## End-to-end shape (multibody)

```python
import mworks.sysplorer.CADToolbox as cadtool
cadtool.ImportCad(r"C:\work\crank_rocker_mechanism.step")
cadtool.SwitchWorkbenchType(cadtool.CadWorkbenchType.MultiBody)
# group into bodies ...
# CreateConnector x N (one Fixed to "Ground") ...
# CreateJointMotion on the driven joint ...
cadtool.CheckDesign()
cadtool.SaveCadFiles()
cadtool.GenerateMoModel()
RUN_SCRIPT_RESULT = cadtool.GetModels()   # returns CAD-browser ids (e.g. "Default.ball_four_link.step") — NOT the _main sim target
# Simulatable top model: "<pkg>.<cad_model>.<cad_model>_main" — construct from package + model name
```

Then validate via MCP `check_model` → `translate_model` → `simulate_model` → `result_manager`/`plot_manager` + animation.
