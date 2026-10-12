# Placing a joint where the geometry actually is

A joint placed at a guessed `coord` is the single biggest source of wrong models: the mechanism imports fine, `CheckDesign` passes, but the animation has parts flying apart, the loop won't close, or the solver fails on a bad axis. You are working **blind** through the MCP — you can't eyeball the 3D view — so you must **read the position and axis out of the geometry instead of inventing numbers.** The toolbox already carries every coordinate you need; this file is the recipe to extract it.

This is the missing half of `multibody-elements.md` → *Coordinates*. Read it before adding any joint whose location you don't already know from the user.

**Why measuring *is* the right move (not a workaround).** In the GUI the user never types coordinates: in 闪电模式 with 特征拾取智能推理 (on by default) they pick a feature and the tool infers the joint pose — pick a **circular edge / cylinder face** → it snaps to the **centre** and aligns the joint's local **+Z** to the **circle normal / cylinder axis**; pick a **line** → midpoint, along the line; pick a **vertex** → keeps the prior orientation. You are blind, so you reproduce that exact inference with `Measure`: read the circle's centre (origin) and bore axis (orientation). Measuring is literally "闪电模式智能推理, done by hand."

## Order of operations — measure BEFORE you group (critical)

Grouping silently breaks measurement if you do it first, and the reason is a naming subtlety worth understanding so you don't fight it:

- `GetGeometricElementIdsOfPart(part_name, …)` resolves `part_name` by **path** — it walks the part's *current* owner chain (`GetEntityByNamePath`). Grouping re-parents the part, so its dotted path changes (`Pin_6.Pin_7` → `rocker.Pin_7`). Calling it afterwards with the **old** path fails with `The part "..." does not exist!` — that is the error you hit when "measuring after grouping."
- Grouping does **not** rename a part's leaf and does **not** move geometry. `MoveToGroup`/`CreateGroup` only re-parent nodes; a part's world transform (its OCAF path id) and therefore its **world coordinates are invariant**. (`Measure` itself resolves its ids by the *leaf* name, flat, so an id measured earlier still resolves — but the path-based enumerator above is the trap.)

So the robust sequence is: **measure first, capture the numbers, then group, then build joints from the captured numbers.**

```
import → SwitchWorkbenchType(MultiBody)
  → survey tree (GetParts)                         # original paths
  → enumerate + Measure features, CAPTURE numeric world coords + axes   # ← here, before grouping
  → group into rigid bodies (CreateGroup/MoveToGroup/ClearGroups)
  → survey tree again (GetParts)                    # discover the NEW paths
  → CreateConnector(... captured coords ...)        # entities use the new paths
  → CheckDesign → generate → validate
```

If you genuinely must measure *after* grouping (e.g. you discover a missing joint later), do **not** reuse or guess a path (it is `G.<leaf>`, never `G.G_1`): call `GetParts("<group>")` to read the part's real current children, then `GetGeometricElementIdsOfPart` with that fresh path. Captured world coordinates from before grouping never need re-measuring.

## What `coord` means (so you know what to extract)

`CreateConnector(type, name, first, second, coord)` with `coord = [x, y, z, rx, ry, rz]`:

- `x, y, z` — the joint **origin**, in **metres**, in the **world frame** of the assembly. It is stored verbatim (no part-local transform), so a world coordinate measured off the geometry drops straight in.
- `rx, ry, rz` — the joint **orientation**, **extrinsic-XYZ Euler angles in degrees**. Their only kinematic job is to point the joint's **functional axis**, which is the joint frame's **local +Z**, along the real axis of motion:
  - Revolute / Cylindrical → +Z is the **rotation axis**.
  - Prismatic → +Z is the **translation direction**.
  - For these three, the in-plane X/Y spin is irrelevant — only where +Z points matters. So you only ever need to solve "rotate (0,0,1) onto the real axis direction."

That is the whole problem: **find a point on the axis (origin) and the axis direction (orientation).** Both come from `Measure`.

## The one tool that returns coordinates: `Measure`

`Measure(geometry_names, circle_arc_measure_type, show_xyz_distance=False)` returns a **list of `"<Label> : <value>"` strings** — the rows of the measure panel. The `circle_arc_measure_type` argument only matters when measuring *two* circles; for single-feature extraction it is ignored. Feed it geometry ids from `GetGeometricElementIdsOfPart(part, ShapeType.Edge|Vertex|Face)`.

What you get back depends on **how many** features and **what type**:

| Input | Rows you can parse | Use it for |
|---|---|---|
| one **vertex** | `Vertex Position : X: ..m, Y: ..m, Z: ..m` | an exact point (pin end, corner) |
| one **circular edge** (a hole/shaft rim) | `Center Position : X: ..m, Y: ..m, Z: ..m`, `Radius : ..m`, `Arc Length`/`Arc Angle` | the **axis point** of a revolute/cylindrical joint |
| one **cylinder/cone/sphere face** | `Radius : ..m`, `Perimeter` (no centre row) | confirm a face is round; not a coordinate source — use its rim edges instead |
| two features | `Distance`, `dx/dy/dz` (if `show_xyz_distance=True`), `Angle`, and relationships `Coaxial` / `Concentric` / `Parallel` / `Vertical` / `Coincide` / `Center Distance:..m` | **verify** axis/position guesses |

All positions are already in **metres** (world frame), the same units `coord` wants. No scaling.

> `Measure` runs only after a CAD file is imported and **not** while in design/edit state, in the active workbench. Edge ids look like `"crank_1_edge <418>"` — the `<N>` is the geometry id, not a list index.

## Finding the right feature to measure (you are blind)

There is **no** screenshot/image API, **no** "circular edges only" filter, and **no** "give me this face's axis" call — `GetGeometricElementIdsOfPart` just returns *every* edge (or face/vertex) by index, and a single cylindrical *face* measure returns only `Radius`/`Perimeter` (no centre, no axis). So you cannot eyeball or filter your way to the hole; you have to **enumerate edges, measure them, and keep the circular ones**, then cluster. This is the floor — there is no faster programmatic path. Mitigate the cost by (a) reusing one axis across a planar mechanism, and (b) using user-supplied coordinates when the user can read them off their CAD drawing.

Bundle this discovery helper into your run_script (it turns the blind enumeration into one structured result):

```python
import re
import mworks.sysplorer.CADToolbox as cadtool
MT = cadtool.CircleArcMeasureType
ST = cadtool.ShapeType

def _row(rows, label):
    for r in rows:
        if r.startswith(label):
            return r.split(":", 1)[1]
    return None

def _xyz(rows, label):
    s = _row(rows, label)
    if not s: return None
    n = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", s)
    return [float(n[0]), float(n[1]), float(n[2])]

def _num(rows, label):
    s = _row(rows, label)
    if not s: return None
    n = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", s)
    return float(n[0]) if n else None

def circular_edges(part_path):
    """Every circular edge of a part as {id, center[x,y,z], radius} (world coords, metres).
    part_path is the CURRENT dotted path (measure BEFORE grouping to keep it simple)."""
    out = []
    for eid in cadtool.GetGeometricElementIdsOfPart(part_path, ST.Edge) or []:
        rows = cadtool.Measure([eid], MT.CircleCenter)
        c = _xyz(rows, "Center Position")
        if c is not None:                       # a "Center Position" row ⇒ this edge is circular
            out.append({"id": eid, "center": c, "radius": _num(rows, "Radius")})
    return out

def bore_axis(edges, tol=1e-4):
    """Pair the two rims of one through-bore: equal radius, distinct centres.
    Returns (c1, c2) — two points on the axis — so you can call axis_to_euler(c1, c2)."""
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            a, b = edges[i], edges[j]
            if a["radius"] and b["radius"] and abs(a["radius"] - b["radius"]) < tol:
                d = sum((a["center"][k] - b["center"][k]) ** 2 for k in range(3)) ** 0.5
                if d > tol:
                    return a["center"], b["center"]
    return None, None
```

To lock onto the **shared joint hole** between two parts, confirm coaxiality with a two-feature measure: pick a circular edge from each part and check the result contains `Coaxial` (or `Concentric`):

```python
rows = cadtool.Measure([edgeA_id, edgeB_id], MT.CircleCenter)   # look for a "Coaxial"/"Concentric" row
```

## Position — exact, directly returned

- **Revolute / Cylindrical**: the joint origin is the **centre of the hole** the two parts share. Measure that part's circular rim edge:
  ```python
  rows = cadtool.Measure(["crank_1_edge <12>"], cadtool.CircleArcMeasureType.CircleCenter)
  # -> ["Arc Length : ...m", "Center Position : X: 0.155m, Y: 0.126m, Z: 0.05m", "Radius : 0.02m"]
  ```
  Parse the `Center Position` → `[0.155, 0.126, 0.05]`.
- **A precise point** (pin tip, slot end, prismatic reference): measure a **vertex** → `Vertex Position`.
- **Don't know which edge is the hole?** Enumerate `GetGeometricElementIdsOfPart(part, ShapeType.Edge)`, measure candidates, and keep the ones that return a `Radius` row (those are circular). The joint hole is the circular edge whose centre/axis is **shared with the mating part** — confirm with the two-feature `Coaxial`/`Concentric` check below.

You may also turn a measured point into a **design point** and hand that to the joint instead of retyping the position — `CreateDesignPointByPick(name, part, [x,y,z])`, or `CreateDesignPointByMidpoint(name, part, p1, p2)` for a point centred between two picks. When a design point is the joint's `first_entity`, the position is inherited and you pass **only** `[rx, ry, rz]`. Design points carry **position only**, never orientation — so you still derive the axis below.

## Axis / orientation — derive from two points on the axis

The measure panel computes the circle's axis internally but does **not** return it as a string. Recover the axis direction from **two points that lie on it**, then convert to Euler:

1. Take the **two rim edges of the same bore** (both ends of a through-hole on one part) — same `Radius`, different `Center Position`. Their two centres `c1`, `c2` define the axis. (For a blind hole, pair the single rim centre with any other coaxial feature, or use the planar shortcut below.)
2. `axis = normalize(c2 - c1)`.
3. Convert to extrinsic-XYZ Euler degrees with the helper — this rotates the joint's local +Z onto `axis`:

```python
import math
def axis_to_euler(p_from, p_to):
    """Euler [rx,ry,rz] (extrinsic XYZ, degrees) that points local +Z from p_from toward p_to.
    Matches the toolbox convention (functional axis = local +Z). In-plane spin is left at 0,
    which is fine for Revolute/Prismatic/Cylindrical (only the axis matters)."""
    dx, dy, dz = (p_to[0]-p_from[0], p_to[1]-p_from[1], p_to[2]-p_from[2])
    n = math.sqrt(dx*dx + dy*dy + dz*dz)
    if n < 1e-12:
        return [0.0, 0.0, 0.0]
    dx, dy, dz = dx/n, dy/n, dz/n
    rx = math.degrees(math.asin(max(-1.0, min(1.0, -dy))))
    ry = math.degrees(math.atan2(dx, dz))
    return [rx, ry, 0.0]
```

Sanity checks of the convention: axis `(0,0,1)` → `[0,0,0]`; axis `(1,0,0)` → `[0,90,0]`; axis `(0,1,0)` → `[-90,0,0]`. The **sign** of the axis (which rim you call `c1` vs `c2`) doesn't matter for Revolute/Prismatic/Cylindrical — the axis is a line, so e.g. axis `(0,0,-1)` → `[0,180,0]` is equivalent to `[0,0,0]`.

**Planar-mechanism shortcut.** In a planar mechanism (crank-rocker, four-bar, slider-crank) every revolute axis is parallel to one global direction — usually world **Z**, i.e. `coord` orientation `[0,0,0]` (or any `[0,0,rz]`; the `rz` is cosmetic in-plane spin). Confirm the plane once (measure two of the holes → `Coaxial`/`Parallel`), then reuse the same orientation for every joint and only vary the position. This is exactly what the bundled `crank_rocker_mechanism` test does (`[…, 0, 0, -90]` on all four revolutes — axis = Z, the −90 is in-plane only).

## Verify — because you can't see the result

After placing a joint, cross-check with two-feature measurements before trusting it:

- Two holes that should share an axis → `Measure([edgeA, edgeB], CircleArcMeasureType.CircleCenter)` should report **`Coaxial`** (or `Concentric` if centres coincide). If it doesn't, your axis is wrong.
- Two faces that should be parallel/perpendicular → the `Parallel` / `Vertical` / `Angle` row confirms it.
- Finally, judge the **animation** (loop closes, bodies stay assembled, no jumps). A guessed axis usually shows up as parts swinging out of plane.

## Worked example — measure first, then group, then build

Two run_script passes. Pass 1 (right after import, **before grouping**) discovers and captures the numbers. Pass 2 (**after grouping**) builds the joint from those numbers — no re-measuring.

**Pass 1 — capture (uses the `circular_edges`/`bore_axis`/`axis_to_euler` helpers above):**

```python
import math
import mworks.sysplorer.CADToolbox as cadtool
# paste _row / _xyz / _num / circular_edges / bore_axis from the helper block above

def axis_to_euler(p, q):
    dx, dy, dz = q[0]-p[0], q[1]-p[1], q[2]-p[2]
    n = math.sqrt(dx*dx+dy*dy+dz*dz) or 1.0
    dx, dy, dz = dx/n, dy/n, dz/n
    return [math.degrees(math.asin(max(-1.0, min(1.0, -dy)))), math.degrees(math.atan2(dx, dz)), 0.0]

edges = circular_edges("Pin_2.Pin_3")          # ORIGINAL path, before grouping
c1, c2 = bore_axis(edges)                       # the crank bore's two rims
coord = c1 + axis_to_euler(c1, c2)              # origin on the axis + axis orientation
RUN_SCRIPT_RESULT = {"crank_bore": edges, "coord": coord}   # capture the numbers
```

**Pass 2 — group, then build with the captured `coord`:**

```python
import mworks.sysplorer.CADToolbox as cadtool
D = cadtool.DesignElemtType
cadtool.MoveToGroup(["Pin_2.Pin_3"], "crank")   # now the path is crank.<leaf>, but coord is unchanged
cadtool.MoveToGroup(["Pin_4.Pin_5"], "frame")
cadtool.ClearGroups()
# coord captured in pass 1 is still correct (world coords are grouping-invariant)
cadtool.CreateConnector(D.ConnectorRevolute, "Revolute2", "frame.frame_1", "crank.crank_1",
                        [0.155, 0.126, 0.05, 0.0, 0.0, 0.0])   # <- the captured coord
# verify the two parts really share the axis (fresh ids on the CURRENT paths):
fa = cadtool.GetGeometricElementIdsOfPart("crank.crank_1", cadtool.ShapeType.Edge)
fb = cadtool.GetGeometricElementIdsOfPart("frame.frame_1", cadtool.ShapeType.Edge)
RUN_SCRIPT_RESULT = cadtool.Measure([fa[0], fb[0]], cadtool.CircleArcMeasureType.CircleCenter)
# expect a "Coaxial"/"Concentric" row when fa[0]/fb[0] are the mating rims
```

## Prefer user-supplied coordinates when available

Measuring is the fallback for when you *only* have the geometry. If the user can read joint coordinates off their CAD drawing/tool (this is exactly how the bundled test cases were authored — they hardcode the numbers), **use those directly** — it is faster and more reliable than blind enumeration. Ask for them when the mechanism has many joints or organic surfaces. Either way the numbers are world-frame metres + extrinsic-XYZ degrees and drop straight into `coord`.

## When measurement can't reach it

If the axis can't be pinned from geometry (no clean rim, organic surface, user-specified motion not tied to a feature), say so and fall back deliberately: reuse a confirmed parallel axis (planar case), ask the user for the axis, or place a provisional joint and lean hard on the animation check — and record in the delivery notes that the value was assumed, not measured.
