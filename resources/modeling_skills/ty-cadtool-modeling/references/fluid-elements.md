# Fluid Elements (tank / rib slicing)

The fluid workbench turns tank/rib geometry into a Modelica fluid model by **slicing** the solid into level-dependent volume/area tables and wiring **fluid ports** with a chosen **medium**. Switch first: `cadtool.SwitchWorkbenchType(cadtool.CadWorkbenchType.Fluid)`.

## Naming differs from multibody

Fluid addresses parts by **bare name** (`"Tank1"`, `"AFT_tank_1"`), not the dotted multibody hierarchy. `GetParts()` (with no argument) returns all fluid part names. Face/plane ids still come from `GetGeometricElementIdsOfPart(part, ShapeType.Face)`.

## Slicing is blocking

`CreateSimpleTankSlice` / `CreateTankSlice` / `CreateRibSlice` start the slice computation immediately and **return only after it finishes** (the return value is the result path, a `str`). Do not issue other toolbox calls mid-slice. Wet surfaces, rib holes and ports may only use **planar** faces of the part.

### Simple tank slice

Fastest path; fixed attitude only.

```python
path = cadtool.CreateSimpleTankSlice("SimpleSlice1", "AFT_tank_1", {
    "ref_point_type": cadtool.ReferencePointType.GravityCenter,  # Origin / GravityCenter / CustomPoint
    "step_type": cadtool.StepType.FixedStep,                     # FixedStep / SlicesPerAttitude
    "slice_step": 0.03,                                          # used when FixedStep
    "yaw": 0.0, "roll": 0.0,
})
```

`CustomPoint` needs `"custom_point": [x, y, z]`; `SlicesPerAttitude` needs `"slice_num_per_attitude": N`.

### Full tank slice

Adds attitude sweeping and wet surfaces / inertia tensor.

```python
cadtool.CreateTankSlice("TankSlice1", "AFT_tank_1", {
    "ref_point_type": cadtool.ReferencePointType.GravityCenter,
    "step_type": cadtool.StepType.FixedStep, "slice_step": 0.03,
    "posture_type": cadtool.PostureType.FixedAttitude,           # FixedAttitude / MinMaxStep / FromFile
    "yaw": 0.0, "roll": 0.0,
    "is_inertiatensor_checked": False,
    "is_add_wet_surface": False,
    # "wet_surfaces": [{"wet_surface_name": "...", "wet_surface_indexes": [...]}],
})
```

Posture modes:
- `FixedAttitude` → `yaw`, `roll`.
- `MinMaxStep` → `min_yaw, max_yaw, yaw_step, min_roll, max_roll, roll_step`.
- `FromFile` → `file_path`.

### Rib slice

```python
cadtool.CreateRibSlice("RibSlice1", "AFT_tank_1", {
    "custom_point": [4.77253, -1.08, 0.3],          # must lie on the rib
    "step_type": cadtool.StepType.FixedStep, "slice_step": 0.03,
    "posture_type": cadtool.PostureType.FixedAttitude, "yaw": 0.0, "roll": 0.0,
    "rib_hole_faces": ["AFT_tank_1_face <20>"],     # holes within 10mm of the ref point
})
cadtool.ModifyRibSliceParams("RibSlice1", {"lambda_crit": 1, "cqmax": 0.8, "cq_gas": 0.6})
```

## Check state

Per part, **at most one tank slice** may be checked, but **multiple rib slices** may be checked:

```python
slice_name = cadtool.GetSlices("AFT_tank_1")[0]
cadtool.SetSliceChecked(slice_name, True)
checked = cadtool.IsSliceChecked(slice_name)
```

## Fluid ports

A port sits on a planar face; `attr_params` is the **face-id string** (not a dict here):

```python
faces = cadtool.GetGeometricElementIdsOfPart("AFT_tank_1", cadtool.ShapeType.Face)
cadtool.CreateFluidPort("Port1", cadtool.FluidPortType.VarGasTankOrigice, 22, "AFT_tank_1_face <20>")
cadtool.ModifyFluidPortParams("Port1", {"area": 0.001, "cq_gas": 0.6, "sigmin": 0.0, "sigmax": 1.0})
```

Port types: `VarGasTankOrigice` (gas orifice, uses `cq_gas`), `VarLiqankOrigice` (liquid orifice, uses `lambda_crit`/`cqmax`), `VarFileankOrigice` (fill orifice, uses all). Note: the **input** key is `cq_gas`; `GetFluidPortParams` reads it back as `cq_Gas`.

## Medium and gravity

```python
cadtool.ModifyMediumParams(cadtool.FluidMediumType.Gas,
                           {"gas_type": cadtool.FluidGasMedium.GasAir,
                            "gas_medium": cadtool.GasMedium.GasMediumPerfect})
cadtool.ModifyMediumParams(cadtool.FluidMediumType.Liquid,
                           {"liquid_type": cadtool.FluidLiqMedium.LiqWater})
cadtool.ModifyGravityParams({"gravity_type": cadtool.FluidGravityType.Constant, "constant": 9.81})
```

Fluid gravity also supports table data (`FluidGravityType.TableData` with `g_table` / `file_path` / `extrapolation` / `time_scale`).

## Generate

```python
cadtool.CheckDesign()           # fluid checks: multiple slices per part, port-only parts, etc.
cadtool.SaveCadFiles()
cadtool.GenerateMoModel("fuel_system_api", cadtool.ModelicaModelType.ModelFluid)
RUN_SCRIPT_RESULT = cadtool.GetModels()
```

Then validate via MCP `check_model` → `translate_model` → `simulate_model` → `result_manager` / `plot_manager`.

## Generated fluid model — simulate-time notes

- **Gauge `NumGauge`.** Generated tanks carry a measurement-gauge component `<tank>_gauge`. The SimpleTank and RibTank tutorials both set its `NumGauge` to **0** before simulating (`run_with_ready set_model_param` / run_script `SetParamValue` on `<tank>.mo`). If a fresh fluid model behaves oddly or won't run, check this first.
- **Multi-tank wiring** (RibTank case). Connecting a secondary tank to the main model is manual: set the `tankPortDemux` interface count `N`, add a `TankPort` interface (`TYAircraftFuelSys.Interfaces.TankInterfaces.TankPort`) on the secondary `tank.mo`, then connect it to `RibSliceN` in the top model.

## Shell parts (volume 0) — thicken first

A part imported as a surface/shell (or a broken solid) has **zero volume/mass** and shows **red**; it cannot be sliced meaningfully. Solidify it with `ThickenSurface(part, offset)` (UI 工具→曲面加厚; supports 普通平面/普通曲面/带孔曲面, not 离散/组合/封闭曲面) before slicing.

## Limitation

Iterative re-entry (`OpenModelInCadBrowser`, `SetComponentIcon`) is **not supported for fluid**. To revise a fluid model, rebuild from the saved `.sys3d` (`OpenCadFile`) and regenerate.
