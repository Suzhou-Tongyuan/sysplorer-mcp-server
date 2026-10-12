---
name: ty-cadtool-modeling
description: 当用户已有一个三维 CAD 几何文件（STEP / IGES / sldasm / CATProduct / ty3d，或已保存的 sys3d 设计；亦含口语的"装配体 / 三维模型 / 几何模型"）并想在 Sysplorer 里把它变成**可仿真的 Modelica 模型**时使用——同元 CAD 工具（CADToolbox / CAD 工具 Python API，经 Sysplorer MCP 的 call_code run_sysplorer_api 驱动）的几何驱动建模：质量/惯量来自实体、拓扑来自在真实零件上放置的运动副，自动生成已布局连线的 .mo 并仿真。两条路径——①多体：分组→转动副/平移副/圆柱副/球副+驱动+接触+闭环平面环→生成→仿真，产出功能样机/动画/曲线；②流体：油箱/贮箱切片+肋板+流体端口+介质+重力→生成→仿真燃油高度/气体体积。典型触发：把 step/装配体"转成"多体或流体模型、几何模型转多体、生成功能样机、几何转 Modelica 并仿真、油箱切片/肋板切片/流体端口建模（中英文均适用）。**不要用于**：没有任何几何文件、仅凭文字需求从零手写 TYMultibody/TYMechanics 等库组件——改用 `ty-mechanical-modeling`；也不用于有限元/网格/应力分析、纯 CAD 零件编辑（不涉及 Sysplorer）、或只是查看 STEP 的零件数/体积。
metadata:
  short-description: CAD-to-Modelica multibody and fluid modeling guidance
  version: 1.3.0
  managed-by: sysplorer-mcp
---

# TY CADToolbox Modeling (geometry-driven)

Convert a real CAD assembly into a Sysplorer Modelica model with the **CADToolbox Python API**, driven through the Sysplorer MCP. Unlike `ty-mechanical-modeling` (which hand-authors TY library components from a text scenario), this skill is **geometry-first**: mass, inertia and centroid come from the solid, and the topology comes from joints you place on real parts. `GenerateMoModel` then emits a laid-out `.mo` automatically.

Use this only when there is (or will be) a geometry file to import. If the user only describes a mechanism in words with no CAD file, switch to `ty-mechanical-modeling`.

## The mental model: replicate the official UI process, blind

The CADToolbox help docs (新手入门 + 应用案例) drive **every** model through the same **five named stages**; only stages ②–③ differ by domain. The GUI user picks geometry features and the tool *infers* positions and axes (闪电模式 + 特征拾取智能推理). You instead drive it **blind through MCP**, so your job at each stage is to **reproduce what that UI step does** with the API — e.g. where the user picks a circular face and the tool snaps the joint to its axis, you `Measure` that circle's centre + axis and pass the numbers. Keeping the official stage names in mind lets you map cleanly to the docs and to what the user sees.

After `GenerateMoModel`, the model is an ordinary Modelica physical model, so the downstream discipline of `ty-sysplorer-modeling-rules` applies: `check_model` → translate → simulate → result; paths only via Agent CWD / `GetDirectory`; and the hard bans (`ClearAll`, `ChangeDirectory`, `Exit`) still hold. **Layout is produced by `GenerateMoModel`** (its own engine lays out components, connections, joints), so manual `smart_layout` writeback is normally unnecessary — only fall back to it if the generated diagram is unusable.

## Minimal Reading

| Need | Read |
|---|---|
| How to drive CADToolbox through MCP (the bridge) | `references/mcp-workflow.md` |
| Full API surface (every function, grouped) | `references/api-reference.md` |
| Multibody element rules (joints, markers, contacts, naming, coords, closed loops) | `references/multibody-elements.md` |
| **Get a joint's exact position & axis from geometry (replicate 闪电模式智能推理 while blind)** | `references/joint-placement.md` |
| Fluid element rules (tank/rib slicing, ports, media) | `references/fluid-elements.md` |
| Failures and repair | `references/common-errors.md` |
| New multibody model (5-stage walkthrough) | `workflows/build-multibody-from-cad.md` |
| New fluid (tank) model (5-stage walkthrough) | `workflows/build-fluid-from-cad.md` |
| Iterate / re-enter the toolbox on an existing model | `workflows/iterate-existing-model.md` |
| Ready-to-edit run_sysplorer_api templates | `templates/run-script-skeleton.md` |

## The pipeline — five named stages

Every `cadtool.*` action runs inside one `call_code(mode="run_sysplorer_api")`; the validation tail (stage ⑤) uses dedicated MCP tools — see `references/mcp-workflow.md` for the run_sysplorer_api header and tool mapping.

**Stage 0 (once):** `session_manager(action="ensure")`; confirm the working dir (Agent CWD / `GetDirectory`) — never write under the MCP program tree.

### Multibody — 导入 → 分组 → 连接和驱动 → 生成 → 仿真

1. **导入 CAD 模型** — `ImportCad(abs_ascii_path)` (MultiBody is the default workbench; call `SwitchWorkbenchType(CadWorkbenchType.MultiBody)` to be explicit). Path must be absolute, ASCII, Modelica-legal. Surface / broken-solid parts import **red** with zero mass → `ThickenSurface` or set mass manually. Commercial formats (sldasm/CATProduct) auto-solve joints and may leave **unknown joints** (handle in ③). Then **survey + measure**: query the tree (`GetParts`…) and **measure every joint feature now, before grouping**, capturing numeric world coords — grouping changes part *paths* but not world coords (`references/joint-placement.md`).
2. **为零件分组** — `CreateGroup` / `MoveToGroup` / `ClearGroups` / `CreateDefaultGroups`. **One rigid body = one group**; merge mutually-fixed parts into a single group, never tie them with a Fixed joint. The grouping *is* the body topology.
3. **添加连接和驱动** (+ contacts / markers / design points / material / gravity) — `CreateConnector` (joints, placed from the measured coords), `CreateJointMotion` (drivers — Revolute/Prismatic/Cylindrical only; set `驱动类型`), `CreateContact` (the UI puts these under 力→点点接触), `CreateMarker`+`CreateRefMarker`, `CreateDesignPoint*`, gravity/material. Anchor with **exactly one `ConnectorFixed` to `"Ground"`**. Fix/delete any **unknown joints** (`GetUnknownConnectors`→`ModifyUnknownConnector`). Closed loops → see *Closed loops* below.
4. **生成 Modelica 模型** — `CheckDesign()` (= 检查) → `SaveCadFiles()` (optional) → `GenerateMoModel("", ModelicaModelType.ModelMultiBody)` (= 接受并退出 + 导出设置; **it auto-runs the necessary checks even if you skip `CheckDesign`**). Default package = `Default`+number (e.g. `Default1`); simulatable top = `<pkg>.<cad>.<cad>_main`; one `[group].mo` per group; **each driver gets a default `Modelica.Blocks.Sources.RealExpression` source = 1**. `GetModels()` returns CAD-browser ids, **not** the `_main` target — confirm the real name.
5. **仿真及结果查看** — `check_model` → `translate_model` → `simulate_model(<…>_main, stopTime=…)` → `result_manager` / `plot_manager` + animation. For real motion, replace a driver's default `RealExpression`=1 with a `TimeTable` (etc.) and set `驱动类型`. Judge the animation (loop closure, body pose, joint motion, interference, jumps); wrong trend → return to the earliest suspect stage (axis, cut, mass, init).

### Fluid — 导入(切流体台) → 切片 → 端口/介质/重力 → 生成 → 仿真

1. **导入 CAD 模型** — **switch to Fluid first**: `SwitchWorkbenchType(CadWorkbenchType.Fluid)` then `ImportCad(...)`. Fluid addresses parts by **bare name** (`"Tank1"`). Shell parts → `ThickenSurface` first.
2. **油箱切片** — `CreateSimpleTankSlice` / `CreateTankSlice` / `CreateRibSlice` (the 切片 menu). **Blocking** (returns a result path; issue no other call mid-slice). Per part ≤1 tank slice checked, multiple rib slices allowed (`SetSliceChecked`). Rib holes must be coplanar with the rib reference point.
3. **端口 / 介质 / 重力** — `CreateFluidPort`+`ModifyFluidPortParams` (设计→端口; **planar faces only**; 可变油箱 液体/气体/填充 孔口), `ModifyMediumParams` (gas/liquid), `ModifyGravityParams`.
4. **生成 Modelica 模型** — `CheckDesign()` → `GenerateMoModel("", ModelicaModelType.ModelFluid)` (生成类型默认流体).
5. **仿真及结果查看** — often set the gauge `NumGauge`=0 on `<tank>.mo` first (`run_with_ready set_model_param` / run_sysplorer_api `SetParamValue`), then `check_model` → `translate_model` → `simulate_model` → `result_manager` (燃油高度 / 气体体积). Multi-tank models need manual port wiring (set `tankPortDemux` N, add a `TankPort` interface, connect to `RibSliceN` in the top model). **Fluid has no iteration design** — to revise, reopen the `.sys3d` (`OpenCadFile`) and regenerate.

### Official term ↔ menu ↔ MCP/API

| 官方术语 (UI) | 菜单 / 位置 | MCP / API |
|---|---|---|
| 打开 CAD 工具 / 导入 | 工具→CAD 工具→导入 | `OpenCadWindow` / `ImportCad` |
| 工作台 (多体 / 流体) | 左上工作台切换 | `SwitchWorkbenchType(MultiBody \| Fluid)` |
| 组合 / 移动至 / 清理 / 默认分组 | 菜单·右键 | `CreateGroup` / `MoveToGroup` / `ClearGroups` / `CreateDefaultGroups` |
| 固定/转动/平移/圆柱/球/平面/万向/螺旋副 | 连接 | `CreateConnector(ConnectorFixed/Revolute/Prismatic/…)` |
| 转动驱动 / 平移驱动 (+驱动类型) | 驱动 | `CreateJointMotion(MotionRotational/Translational)` + `ModifyJointMotionParams` |
| 点点接触 (球球/球-圆柱/球-矩形/球-圆) | 力→点点接触 | `CreateContact(ContactSphereTo…)` |
| 标架 / 参考标架 | 标架 | `CreateMarker` / `CreateRefMarker` |
| 设计点 (拾取/中点/偏移/交点) | 设计点 | `CreateDesignPointByPick` / `…ByMidpoint` / `…ByOffset` |
| 平面环处理 (姿态统一) | 工具→平面环处理 | `PlanarLoopConstraint(base, [others], is_reversed, base_rotation)` — **姿态统一，非切割** |
| 修改未知类型运动副 | 双击红色未知副 | `GetUnknownConnectors` / `ModifyUnknownConnector` |
| 测量 | 工具→测量 | `Measure` / `GetGeometricElementIdsOfPart` |
| 曲面加厚 | 工具→曲面加厚 | `ThickenSurface` |
| 切片 (简单油箱/油箱/肋板) | 切片 | `CreateSimpleTankSlice` / `CreateTankSlice` / `CreateRibSlice` |
| 端口 / 介质 / 重力 | 设计→端口 · 介质 · 力→重力 | `CreateFluidPort` / `ModifyMediumParams` / `ModifyGravityParams` |
| 检查 | 检查 | `CheckDesign()` |
| 接受并退出 + 导出设置 | 接受并退出 | `SaveCadFiles` + `GenerateMoModel(pkg, type)` (auto-checks) |
| 迭代设计 (整体/局部) | CAD 浏览器 双击/打开 | `OpenModelInCadBrowser` (multibody only) |

## Multibody — key invariants

- **One rigid body = one group.** Parts that don't move relative to each other go into a single group, never tied with a `ConnectorFixed`. Each group becomes one body, and the planar-loop auto-detector walks the **group** graph — splitting a rigid body into Fixed-joined groups pollutes that graph and breaks loop auto-recognition (`references/multibody-elements.md` → Grouping).
- **World anchor:** exactly one Fixed joint, and its `second_entity` is `"Ground"`. A second Fixed joint, or one between two parts, means you should have grouped instead.
- **Don't guess joint coords — measure them, before grouping.** This is the blind equivalent of the UI's 闪电模式智能推理: pick a circular edge → its centre is the axis point and the bore axis is the joint axis. `coord = [x,y,z, rx,ry,rz]` = world-frame metres + extrinsic-XYZ degrees pointing local **+Z** along the axis. `GetGeometricElementIdsOfPart` resolves a part by its *current* dotted path (grouping changes it), so enumerate/measure right after import and capture the numeric world coords (grouping-invariant). Full recipe + helpers: `references/joint-placement.md`.
- **Drivers** (`CreateJointMotion`) attach only to Revolute / Prismatic / Cylindrical. Set `驱动类型` via `ModifyJointMotionParams` (位移/Displacement, 速度/Velocity, 加速度/Acceleration; the cases set it explicitly). The generator gives every driver a default `RealExpression`=1 source — replace it (e.g. with `TimeTable`) for prescribed motion.
- **Unknown joints** (常见于商用 CAD 导入) show **red** and **block generation**. `GetUnknownConnectors()` → `ModifyUnknownConnector(name, {"type": DesignElemtType.Connector…, "position":[…], "rotation":[…]})`, or delete and recreate.
- **Closed loops — two different concepts (do not conflate):**
  1. **Orientation unification = `PlanarLoopConstraint(base_connector, connector_arr, is_reversed, base_rotation)` = the 平面环处理 tool.** When CAD assembly precision (~1e-6) is below Sysplorer's solver precision (1e-10), auto-derived joint orientations are slightly off and the planar loop **fails to initialize in simulation**. This tool **unifies** all loop-joint orientations onto a base orientation (optionally Z-reversing individual joints). It is **NOT a cut** — it runs **before** generating (this is what the `double_slider` CATIA case does, then generates with no manual cut). `base_connector`=基准副, `connector_arr`=待调整副, `is_reversed`=per-joint Z-reverse bool list (same length), `base_rotation`=`[Rx,Ry,Rz]`.
  2. **Loop cut (cut joint)** removes the redundant constraint. **Prefer auto**: with clean grouping, `GenerateMoModel` auto-inserts the cut for planar loops with parallel axes (`crank_rocker_mechanism` has no manual cut). **Fallback** (spatial loop / non-parallel axes / auto-miss): post-gen swap one loop Revolute to `TYMultibody.Joints.RevolutePlanarCut` via `SetComponentInfo`. There is **no** standalone cut API in CADToolbox.
  - Order: clean grouping → (planar loop with precision/orientation trouble) `PlanarLoopConstraint` → generate (auto-cut) → if still over-constrained, `RevolutePlanarCut`.
- **Query parameters before assigning them.** `Modify*Params` keys are type-specific (Revolute exposes `phi_rel_0`/`om_rel_0`; Prismatic `s_rel_0`/`v_rel_0`; spherical/gravity/direction use `"{a, b, c}"` strings). Pull real keys with the matching `Get*Params` first.

## Fluid — key invariants

- **Switch to `CadWorkbenchType.Fluid` *before* import** (the SimpleTank tutorial切流体台 then 导入). Fluid addresses parts by bare name (`"Tank1"`), not the multibody dotted path.
- Slicing (`CreateSimpleTankSlice` / `CreateTankSlice` / `CreateRibSlice`) **blocks until done** and returns a result path; no other toolbox call mid-slice. Per part ≤1 tank slice checked, multiple rib slices allowed. Face/plane ids for wet surfaces, rib holes and ports come from `GetGeometricElementIdsOfPart(part, ShapeType.Face)` and must be **planar**; rib holes must be coplanar with the rib reference point.
- Set the medium with `ModifyMediumParams(FluidMediumType.Gas|Liquid, {...})`; ports with `CreateFluidPort` / `ModifyFluidPortParams`; gravity with `ModifyGravityParams`. The fluid tree roots are 物体 / 力 / 介质.
- **Shell parts** (volume 0, red) must be solidified with `ThickenSurface` before slicing.
- At simulate time, fluid models commonly need the gauge `NumGauge` set to 0; multi-tank models need manual port wiring. Fluid has **no** iteration design.

## Validation & delivery

State, in addition to the parent rules' evidence:

- Source CAD file & format, chosen workbench, generated model full name, and the `simulate_model` outcome.
- Multibody: body grouping; world anchor present; for closed loops, whether you used `PlanarLoopConstraint` (orientation unification) and/or a cut (auto vs `RevolutePlanarCut`) and why; driver type set; any unknown joints fixed; animation judgment.
- Fluid: which slice is checked, medium, ports, slice result paths, gauge/NumGauge and any tank-tank wiring.
- Any parameter whose value was assumed rather than queried, and any element substitution with its expected impact.

## Repair priority

Prefer the shortest blocking chain:

`import (path/format/红色曲面) -> workbench match -> unknown joints -> world/Ground anchor -> entity names -> joint topology / 平面环姿态 / closed-loop cut -> parameters -> CheckDesign -> GenerateMoModel -> translate -> solver/initialization -> result interpretation`

Preserve valid structure already built, fix the earliest blocker, then return to the failed stage. Read `references/common-errors.md` for concrete failure signatures and fixes.
