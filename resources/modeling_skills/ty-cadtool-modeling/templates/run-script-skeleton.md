# run_sysplorer_api Skeletons

Paste a block into `call_code(mode="run_sysplorer_api", payload={"python_source": "...", "capture_stdout": true, "capture_stderr": true})`. Adapt names/coords to the real model (query them first). Read return values from the response field `run_script_result`.

> Do **not** include `ClearAll`, `ChangeDirectory`, or `Exit()`. The MCP manages the session and working directory — see `references/mcp-workflow.md`.

## A. Survey (run this first, decide names before building)

```python
import mworks.sysplorer.CADToolbox as cadtool
cadtool.ImportCad(r"C:\work\my_assembly.step")       # absolute, ASCII-only path
cadtool.SwitchWorkbenchType(cadtool.CadWorkbenchType.MultiBody)
RUN_SCRIPT_RESULT = {
    "top": cadtool.GetParts(),                       # top-level parts/groups
    "workbench": cadtool.GetWorkbenchType(),         # 0 multibody / 1 fluid
}
```

## B1. Measure joint coords from geometry — run this FIRST, before grouping

`GetGeometricElementIdsOfPart` addresses a part by its CURRENT path, which grouping changes — so measure now (original paths) and capture the numeric world coords; they stay valid after grouping. See `references/joint-placement.md`.

```python
import math, re
import mworks.sysplorer.CADToolbox as cadtool
MT, ST = cadtool.CircleArcMeasureType, cadtool.ShapeType

def _xyz(rows, label):
    for r in rows:
        if r.startswith(label):
            n = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", r.split(":", 1)[1]); return [float(n[0]), float(n[1]), float(n[2])]
    return None
def _num(rows, label):
    for r in rows:
        if r.startswith(label):
            n = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", r.split(":", 1)[1]); return float(n[0]) if n else None
    return None
def circular_edges(part_path):                    # every circular edge as {id, center, radius} (world m)
    out = []
    for eid in cadtool.GetGeometricElementIdsOfPart(part_path, ST.Edge) or []:
        rows = cadtool.Measure([eid], MT.CircleCenter); c = _xyz(rows, "Center Position")
        if c is not None: out.append({"id": eid, "center": c, "radius": _num(rows, "Radius")})
    return out
def bore_axis(edges, tol=1e-4):                   # two rims of one bore -> (c1, c2); axis = c2-c1
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            a, b = edges[i], edges[j]
            if a["radius"] and b["radius"] and abs(a["radius"] - b["radius"]) < tol:
                if sum((a["center"][k]-b["center"][k])**2 for k in range(3))**0.5 > tol: return a["center"], b["center"]
    return None, None
def axis_to_euler(p, q):                          # point local +Z from p toward q -> extrinsic-XYZ degrees
    dx, dy, dz = q[0]-p[0], q[1]-p[1], q[2]-p[2]; n = math.sqrt(dx*dx+dy*dy+dz*dz) or 1.0; dx, dy, dz = dx/n, dy/n, dz/n
    return [math.degrees(math.asin(max(-1.0, min(1.0, -dy)))), math.degrees(math.atan2(dx, dz)), 0.0]

e = circular_edges("Pin_2.Pin_3")                 # ORIGINAL pre-group path
c1, c2 = bore_axis(e)
RUN_SCRIPT_RESULT = {"crank_coord": (c1 + axis_to_euler(c1, c2)) if c1 else None, "edges": e}
# capture the coord; feed it into CreateConnector in B (after grouping)
```

## B. Group, then build the mechanism from captured coords + generate

```python
import mworks.sysplorer.CADToolbox as cadtool
D = cadtool.DesignElemtType

# 1) group parts into rigid bodies — ONE body per group; merge mutually-fixed parts,
#    do NOT join them with Fixed joints. (Coords were captured in B1, before this.)
cadtool.MoveToGroup(["Pin_2.Pin_3"], "crank")
cadtool.MoveToGroup(["Pin_4.Pin_5"], "frame")
cadtool.CreateGroup(["Base.Base_1", "Base_2.Base_3"], "base")  # 2+ rigidly-fixed parts -> one body
cadtool.ClearGroups()
# re-survey to learn the NEW dotted paths the entities now have:
# RUN_SCRIPT_RESULT = {"top": cadtool.GetParts(), "crank": cadtool.GetParts("crank")}

# 2) anchor to world + joints  (coord = [x,y,z, rx,ry,rz] metres/degrees, world frame, from B1)
#    EXACTLY ONE Fixed joint, and it goes to "Ground".
cadtool.CreateConnector(D.ConnectorFixed,    "Fixed1",    "frame.frame_1", "Ground",                  [-0.515, -0.007, 0.05, 0, 0, 0])
cadtool.CreateConnector(D.ConnectorRevolute, "Revolute1", "crank.crank_1", "frame.frame_1",            [0, 0, 0.05, 0, 0, -90])
cadtool.CreateConnector(D.ConnectorRevolute, "Revolute2", "crank.crank_1", "connecting_rod.connecting_rod_1", [0.155, 0.126, 0.05, 0, 0, -90])

# 3) driver on a revolute/prismatic/cylindrical joint
cadtool.CreateJointMotion(D.MotionRotational, "Rotational1", "Revolute1")

# 4) sanity check, save, generate
cadtool.CheckDesign()
cadtool.SaveCadFiles()                                # empty -> package "Default"
cadtool.GenerateMoModel("", cadtool.ModelicaModelType.ModelMultiBody)
RUN_SCRIPT_RESULT = cadtool.GetModels()               # returns CAD-browser ids (e.g. "Default.crank_rocker_mechanism.step")
# The simulatable target is "<pkg>.<cad_model>.<cad_model>_main" — construct from package + model name, NOT from GetModels()
```

## C. Closed loops — two distinct tools (don't conflate)

**C1. Orientation unification (平面环处理) — pre-generation, for planar loops that fail to *initialize* (CAD precision ~1e-6 < solver 1e-10). This is NOT a cut.**
```python
# base_connector, [joints to align], per-joint Z-reverse bools (same length), base orientation [Rx,Ry,Rz]
cadtool.PlanarLoopConstraint("Revolute1", ["Revolute2", "Revolute3", "Revolute4"],
                             [False, False, True], [0, 0, -90])
```

**C2. Loop cut — for over-constraint.** Prefer the auto-cut at `GenerateMoModel` (clean grouping + parallel-axis planar loop → nothing to do). Only for spatial loops / auto-miss, swap one loop Revolute to a cut joint **post-generation** via the core API:
```python
import mworks.sysplorer as ModelingPy
ModelingPy.SetComponentInfo("Default.ball_four_link.ball_four_link_main",
                            "Revolute3", "Type", "TYMultibody.Joints.RevolutePlanarCut")
```

## D. Build a fluid (tank) model + generate

```python
import mworks.sysplorer.CADToolbox as cadtool
cadtool.ImportCad(r"C:\work\fuel_system.step")
cadtool.SwitchWorkbenchType(cadtool.CadWorkbenchType.Fluid)

# slicing is blocking; returns a result path
path = cadtool.CreateSimpleTankSlice("Slice1", "AFT_tank_1", {
    "ref_point_type": cadtool.ReferencePointType.GravityCenter,
    "step_type": cadtool.StepType.FixedStep, "slice_step": 0.03,
    "yaw": 0.0, "roll": 0.0,
})
cadtool.SetSliceChecked("Slice1", True)

# port on a planar face (attr_params is the face-id string)
cadtool.CreateFluidPort("Port1", cadtool.FluidPortType.VarGasTankOrigice, 22, "AFT_tank_1_face <20>")

# medium + gravity
cadtool.ModifyMediumParams(cadtool.FluidMediumType.Gas,
                           {"gas_type": cadtool.FluidGasMedium.GasAir,
                            "gas_medium": cadtool.GasMedium.GasMediumPerfect})
cadtool.ModifyGravityParams({"gravity_type": cadtool.FluidGravityType.Constant, "constant": 9.81})

cadtool.CheckDesign()
cadtool.SaveCadFiles()
cadtool.GenerateMoModel("", cadtool.ModelicaModelType.ModelFluid)
RUN_SCRIPT_RESULT = {"slice_path": path, "models": cadtool.GetModels()}
```

## E. Query an element's real parameter keys before modifying

```python
import mworks.sysplorer.CADToolbox as cadtool
RUN_SCRIPT_RESULT = {
    "connector": cadtool.GetConnectorParams("Revolute1"),
    "part": cadtool.GetPartParams("crank.crank_1"),
    "faces": cadtool.GetGeometricElementIdsOfPart("crank.crank_1", cadtool.ShapeType.Face),
}
```

## F. Live API help (when unsure of a signature)

```python
import io, sys
import mworks.sysplorer.CADToolbox as cadtool
buf = io.StringIO(); sys.stdout = buf
help(cadtool.CreateConnector)
sys.stdout = sys.__stdout__
RUN_SCRIPT_RESULT = buf.getvalue()
```

## Validation tail (use MCP tools, not run_sysplorer_api)

```
check_model(<model>_main)
translate_model(<model>_main)
simulate_model(<model>_main, stopTime=10)
result_manager(... read target variables ...)
plot_manager(... / animation ...)
```
