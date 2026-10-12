# Workflow — Build a fluid (tank) model from CAD

Use when the user has tank/rib geometry and wants a Modelica fluid model via slicing.

This mirrors the **official five-stage process** (新手入门 简单油箱, 应用案例 带肋板油箱):

> **导入(切流体台) → 切片 → 端口/介质/重力 → 生成 → 仿真**

Run each `cadtool.*` step inside one `call_code(mode="run_sysplorer_api")`.

## Default reading

- Required: `references/mcp-workflow.md`, `references/fluid-elements.md`
- On demand: `references/common-errors.md`, `templates/run-script-skeleton.md`

## Stage 0 — Intent & ready

1. **Intent**: which tank/rib parts; reference point (origin/centroid/picked/custom); slice step (thickness or slices-per-attitude); attitude mode (fixed / min-max-step / from-file); medium (gas/liquid); ports needed; whether multiple tanks must be connected.
2. `session_manager(action="ensure")`; confirm the working dir.

## Stage ① 导入 CAD 模型 — switch to Fluid FIRST

`cadtool.SwitchWorkbenchType(CadWorkbenchType.Fluid)` **then** `cadtool.ImportCad(abs_ascii_path)`. (The SimpleTank tutorial切流体台 before 导入.) Fluid addresses parts by **bare name** (`GetParts()` → `"simple_tank_1"`, `"tank1_1"`…). Shell parts (volume 0, red) → `cadtool.ThickenSurface(part, offset)` first. For wet surfaces / rib holes / ports, get planar face ids with `GetGeometricElementIdsOfPart(part, ShapeType.Face)`.

## Stage ② 油箱切片 (Slice) — blocking, one at a time

Each slice call **blocks until done** and returns a result path; capture it. Do not issue other toolbox calls mid-slice. Choose the slicer per scenario:

- **简单油箱 (fixed attitude only)** — `CreateSimpleTankSlice(name, tank, {ref_point_type, step_type, slice_step, yaw, roll})`. `ref_point_type` = Origin / GravityCenter / CustomPoint(+`custom_point`); `step_type` = FixedStep(+`slice_step`, default 0.03m) / SlicesPerAttitude(+`slice_num_per_attitude`, default 20).
- **油箱 (fixed OR variable attitude)** — `CreateTankSlice(name, tank, {... posture_type, is_inertiatensor_checked, is_add_wet_surface, wet_surfaces})`. `posture_type` = FixedAttitude(yaw/roll) / MinMaxStep(min/max/step for yaw & roll) / FromFile(file_path). Pitch ∈ [-90,90], roll ∈ [-180,180] deg.
- **肋板 (ribs with holes)** — `CreateRibSlice(name, rib, {custom_point, step_type, slice_step, posture_type, yaw, roll, rib_hole_faces})`. The reference point and **all rib-hole faces must be coplanar**, or slicing errors.

For a multi-tank model (带肋板油箱 case): slice each tank, hide an occluding tank to pick another's features (`HideEntities`/`ShowAllEntities` ↔ UI 隐藏/显示所有实体), then slice the rib.

## Stage ②.5 — Check states

Per part: **at most one** simple/tank slice may be checked, **multiple** rib slices may be checked. `SetSliceChecked(slice, True)`; verify `IsSliceChecked`.

## Stage ③ 端口 / 介质 / 重力 (Ports / Medium / Gravity)

1. **Ports** — `CreateFluidPort(name, FluidPortType.*, icon_size, "<face_id>")` (UI 设计→端口; **planar faces only**). Types: `VarLiqankOrigice` (可变油箱液体孔口), `VarGasTankOrigice` (可变油箱气体孔口), `VarFileankOrigice` (可变油箱填充孔口). Tune with `ModifyFluidPortParams` (`area`, `cq_gas`/`lambda_crit`/`cqmax`, `sigmin`, `sigmax`).
2. **Medium** — `ModifyMediumParams(FluidMediumType.Gas|Liquid, {...})` (介质 node: 气体/液体介质).
3. **Gravity** — `ModifyGravityParams({gravity_type, constant})` (力→重力 node).

## Stage ④ 生成 Modelica 模型 (Generate)

`cadtool.CheckDesign()` (= 检查; flags multiple checked tank slices per part, port-only parts, etc.) → `cadtool.SaveCadFiles()` (optional) → `cadtool.GenerateMoModel("", ModelicaModelType.ModelFluid)` (= 接受并退出 + 导出设置, 生成类型默认流体; auto-checks). `RUN_SCRIPT_RESULT = cadtool.GetModels()`. Simulatable top = `<pkg>.<cad>.<cad>_main`.

## Stage ⑤ 仿真及结果查看 (Simulate & review)

1. **Gauge** — fluid models commonly need the measurement gauge disabled: set `NumGauge`=0 on the `<tank>_gauge` component of `<tank>.mo` (`run_with_ready set_model_param` / run_script `SetParamValue`). The SimpleTank & RibTank cases both do this before simulating.
2. **Multi-tank wiring** (RibTank case) — connect tanks manually: set `tankPortDemux` interface count `N`, add a `TankPort` interface (`TYAircraftFuelSys.Interfaces.TankInterfaces.TankPort`) on the secondary `tank.mo`, then connect it to `RibSliceN` in the top model.
3. `check_model` → `translate_model` → `simulate_model(<…>_main, stopTime=…)` → `result_manager` / `plot_manager` + animation. Review 油液运动 animation and curves (燃油高度, 气体体积).

## Notes

- Slicing blocks; never interleave other toolbox calls while a slice runs (the tool prompts to stop slicing if you try).
- Wet surfaces / rib holes / ports require **planar** faces; rib holes must be coplanar with the rib reference point.
- Slice result files default to the Sysplorer working directory.
- Fluid has **no iteration design** — to revise, reopen the `.sys3d` (`OpenCadFile`) and regenerate.

## Deliver

Sliced parts + result paths; which slice is checked per part; medium; ports + types; gravity; generated model name; gauge/`NumGauge` and any tank-tank wiring; simulate outcome; verified variables (燃油高度/气体体积); any assumed parameters.
