# Workflow — Build a multibody model from CAD

Use when the user has a CAD assembly and wants a working Modelica multibody model + simulation.

This mirrors the **official five-stage process** (新手入门 曲柄滑块/牛顿摆, 应用案例 PickAndPlace/Bulldozer/RobotGrabBall/DoubleSlider/SolidWorks):

> **导入 → 分组 → 连接和驱动 → 生成 → 仿真**

You drive it **blind through MCP**, so each stage = reproduce what the GUI step does (where the user picks a feature and the tool infers the joint, you `Measure` and pass numbers). Run each `cadtool.*` step inside one `call_code(mode="run_sysplorer_api")`.

## Default reading

- Required: `references/mcp-workflow.md`, `references/multibody-elements.md`, `references/joint-placement.md`
- On demand: `references/common-errors.md` (any failure), `templates/run-script-skeleton.md`

## Minimal closed loop first

Build the smallest checkable mechanism (bodies + joints + one world anchor + one driver), get it to simulate, **then** add contacts, extra drivers, losses, monitoring. Don't front-load detail.

## Stage 0 — Intent & ready

1. **Extract the intent**: which assembly file & format, the mechanism type and motion dimension, the driven joint(s), the joints between bodies, and the result variables to verify. If a blocking field is missing, ask one targeted question. (The official cases start from a *机构解析* table — the part-to-part joint list; build yours first.)
2. `session_manager(action="ensure")`; confirm the working dir.

## Stage ① 导入 CAD 模型 (Import)

- `cadtool.ImportCad(abs_ascii_path)` → `cadtool.SwitchWorkbenchType(CadWorkbenchType.MultiBody)` (MultiBody is default; be explicit). Path absolute, ASCII, Modelica-legal.
- **Commercial formats** (sldasm/CATProduct): import opens the CAD software, auto-solves assembly constraints into joints, and may produce **unknown joints (红色)** + default groups. Note any unknown joints to fix in ③.
- **Surface / broken-solid parts** import red with zero mass → `cadtool.ThickenSurface(part, offset)` or set mass later.
- **Survey the tree** (run_script, return values): `GetParts()` top level, drill with `GetParts("<group>")`. Learn the exact original names and decide the rigid-body grouping. Do not skip.

## Stage ①.5 — Measure joint features NOW (before grouping) and capture the numbers

This is the blind equivalent of the UI's 闪电模式特征拾取智能推理 (pick a circular face → tool snaps to its centre/axis). For each kinematic pair, enumerate the part's edges (`GetGeometricElementIdsOfPart(part, ShapeType.Edge)`), `Measure` the circular rims → `Center Position` (origin) and two coaxial rim centres → axis → Euler (helpers `circular_edges`/`bore_axis`/`axis_to_euler` in `references/joint-placement.md`). **Store the numeric world coords.**

Do this *before* grouping because `GetGeometricElementIdsOfPart` addresses a part by its *current* dotted path, which grouping changes — while world coords are grouping-invariant, so captured numbers stay valid. You are blind (no screenshot/filter): find holes by enumerate → measure → keep circular. If the user can read coords off their CAD drawing, use those directly.

## Stage ② 为零件分组 (Group)

**One rigid body per group.** `MoveToGroup` / `CreateGroup` / `CreateDefaultGroups`, then `ClearGroups()`. Merge **all** mutually-fixed parts of a body into one group (e.g. `CreateGroup(["Base.Base_1","Base_2.Base_3"], "base")`); do **not** join them with Fixed joints — clean grouping is what lets the generator auto-recognise loops later. For commercial imports, default groups already exist (零件名_数字) — merge/move as needed. Re-survey with `GetParts` to learn the new dotted paths.

## Stage ③ 添加连接和驱动 (Connections & drivers)

1. **World anchor** — exactly one `CreateConnector(ConnectorFixed, "Fixed1", "<frame_part>", "Ground", coord)`. This is the only Fixed joint you create. (UI: icon white→teal when 零件2=Ground.)
2. **Joints from the captured coords** — for each kinematic pair, `CreateConnector(type, name, "<groupA>.<leaf>", "<groupB>.<leaf>", coord)` using the world coords from ①.5 and the **new** post-group entity paths. Joint types: Fixed/Revolute/Prismatic/Cylindrical/Spherical/Universal/Screw/Planar. Verify with a two-feature `Coaxial`/`Parallel` measure on fresh ids.
3. **Unknown joints** (from commercial CAD, 红色) — `GetUnknownConnectors()` → `ModifyUnknownConnector(name, {"type": DesignElemtType.Connector…, "position":[…], "rotation":[…]})`, or delete + recreate. **They block generation if left.**
4. **Driver(s)** — `CreateJointMotion(MotionRotational|MotionTranslational, name, joint)` on a Revolute/Prismatic/Cylindrical. Set `驱动类型` with `ModifyJointMotionParams` (位移/Displacement, 速度, 加速度) — the cases set this explicitly (Bulldozer→位移, RobotGrabBall→角度).
5. **Optional** — contacts (`CreateContact`, UI 力→点点接触; set k/d), markers + ref-markers (`CreateMarker`+`CreateRefMarker`; ref target must be in a *different* top group), design points (`CreateDesignPoint*`), gravity, material.

## Stage ③.5 — Resolve closed loops (two distinct tools — don't conflate)

- **Planar loop, parallel axes, clean grouping → do nothing.** `GenerateMoModel` auto-detects and auto-inserts the cut (like `crank_rocker_mechanism`). If a planar mechanism reports over-constraint, suspect grouping (rigid body split by Fixed joints) first.
- **Planar loop that fails to *initialize* in simulation (precision)** → unify joint orientations with the **平面环处理** tool **before generating**: `cadtool.PlanarLoopConstraint(base_connector, [others], is_reversed, base_rotation)`. This aligns all loop-joint poses (CAD precision ~1e-6 < solver 1e-10) — it is **orientation unification, NOT a cut**. This is exactly what the `double_slider` CATIA case does, then it generates normally.
- **Spatial loop / non-parallel axes / auto-cut genuinely missed** → after generating, swap one loop Revolute to a cut joint: `ModelingPy.SetComponentInfo("<…>_main", "RevoluteN", "Type", "TYMultibody.Joints.RevolutePlanarCut")`. There is no standalone cut API.
- Record what you used (orientation unify? auto-cut? manual `RevolutePlanarCut`?), which joint, and why.

## Stage ④ 生成 Modelica 模型 (Generate)

1. `cadtool.CheckDesign()` (= 检查). Fix every flag (ungrouped parts, unknown joints, markers w/o ref, no anchor) before generating.
2. `cadtool.SaveCadFiles()` (optional) → `cadtool.GenerateMoModel("", ModelicaModelType.ModelMultiBody)` (= 接受并退出 + 导出设置; **auto-runs the needed checks even if you skipped CheckDesign**).
3. `RUN_SCRIPT_RESULT = cadtool.GetModels()` returns CAD-browser ids — **not** the sim target. The simulatable top is `<pkg>.<cad>.<cad>_main` (default pkg `Default`+number, e.g. `Default1`); confirm via `model_manager(action="get_components")`. Each driver gets a default `RealExpression`=1 source.

## Stage ⑤ 仿真及结果查看 (Simulate & review)

1. `check_model` → (apply `RevolutePlanarCut` if still over-constrained) → `translate_model` → `simulate_model(<…>_main, stopTime=…)` → `result_manager` for the target variables → `plot_manager` / animation.
2. **For real motion**: the default `RealExpression`=1 just holds a unit input. Replace it with a `TimeTable` (etc.) on the generated `.mo` and set the driver `驱动类型` (the Bulldozer/Robot cases do this).
3. **Judge the animation**: loop closure, body pose, joint motion, interference, abnormal jumps. If a body moves the wrong way, the joint axis is likely reversed — fix the joint's rotation vector (取反) or re-derive the axis. If the trend/KPI is wrong, return to the earliest suspect stage (axis, cut, mass, init).

## Deliver

Source file & format; 机构解析 (body grouping + joint list); world anchor; closed-loop handling (orientation unify via `PlanarLoopConstraint` and/or cut: auto vs `RevolutePlanarCut`, which joint + why); driver types set; any unknown joints fixed; generated model name; simulate outcome; verified variables; animation judgment; any assumed (unqueried) parameters or substitutions.
