# CADToolbox API Reference

Mirror of `mworks.sysplorer.CADToolbox` (`import mworks.sysplorer.CADToolbox as cadtool`). Signatures and one-line summaries are grouped by purpose. For the authoritative installed version, run `cadtool.ListFunctions()` or `help(cadtool.<fn>)` via run_script (see `mcp-workflow.md`). All functions return `bool` success unless noted; coordinate triples are metres + Euler degrees.

## Contents

1. [Session & files](#1-session--files)
2. [Window & quick preview](#2-window--quick-preview)
3. [View & display](#3-view--display)
4. [Model browser](#4-model-browser)
5. [Workbench](#5-workbench)
6. [Check & generate](#6-check--generate)
7. [Grouping (multibody)](#7-grouping-multibody)
8. [Create — multibody elements](#8-create--multibody-elements)
9. [Modify — multibody elements](#9-modify--multibody-elements)
10. [Loop tools & geometry (multibody)](#10-loop-tools--geometry-multibody)
11. [Create / modify — fluid elements](#11-create--modify--fluid-elements)
12. [Iteration design](#12-iteration-design)
13. [Delete](#13-delete)
14. [Query (Get*)](#14-query-get)
15. [Enums](#15-enums)

---

## 1. Session & files

| Function | Summary |
|---|---|
| `OpenCadWindow()` | Launch the CAD toolbox window. |
| `ImportCad(path:str, do_save:bool=False)` | Import a CAD assembly. Formats: STEP/IGES/sldasm/CATProduct/ty3d. Path must be ASCII (no Chinese/special chars). Disabled during iteration design. |
| `OpenCadFile(path:str, do_save:bool=False)` | Open a saved `.sys3d` file. |
| `SaveCadFiles(package_name:str='', save_path:str='')` | Save CAD files. Empty package → a Sysplorer-assigned name (observed as `Default` in the bundled test cases; the API docstring example shows `default1` — do **not** assume the prefix, read it back). Empty path → Sysplorer working dir. Only the first save needs the args. |
| `CloseCadWindow(do_save:bool=False)` | Close the toolbox design window. |
| `UndoCad()` / `RedoCad()` | Undo / redo the last toolbox action. |

## 2. Window & quick preview

| Function | Summary |
|---|---|
| `OpenQuickPreview()` / `CloseQuickPreview()` | Open/close the quick-preview window (needs `EnableQuickPreview(True)`). |
| `EnableQuickPreview(is_enable:bool=True)` | Enable the quick-preview feature. |
| `LockQuickPreview(is_lock:bool=True)` | Pin / unpin the preview window. |
| `UpdateQuickPreview()` | Refresh preview to the currently open model. |
| `SetWindowPos(position_arr:list, win_type:int=WindowType.CadWindow)` | Set `[x, y, w, h]` of a window. |
| `GetWindowPos(win_type:int=WindowType.CadWindow)` | → dict `{x,y,width,height}`. |

## 3. View & display

| Function | Summary |
|---|---|
| `ZoomAll(win_type=WindowType.CadWindow)` | Fit all in view. |
| `ZoomToEntity(entity_name_arr:list, is_highlight=True, win_type=WindowType.CadWindow)` | Fit/zoom to named entities (parts, points, markers, joints, drivers, contacts, ports). |
| `SetViewDirection(view_dir=ViewDirection.ViewISOZXY, win_type=...)` | Six standard views + isometric. |
| `SetDisplayMode(view_dis_mode=ViewDisplayMode.DisShadedEdges, win_type=...)` | Wireframe / shaded / shaded-with-edges. |
| `SetProjection(view_proj_mode=ViewProjectionMode.ProjOrthogonal, win_type=...)` | Orthographic / perspective. |
| `SetDesignElemtsVisibility(is_visible=True, win_type=...)` | Show/hide all design elements. |
| `ShowViewCube(is_show=True)` / `ShowAxis(is_show=True)` | View cube / reference axes. |
| `SetIconsSize(icons_size:int)` | Icon size for all design elements. |
| `ShowGrid(is_xy=True, is_yz=True, is_zx=True)` / `SetGridSpacing(grid_spacing:float)` | Grid planes / spacing. |
| `SetBackgroundColor(top_color:list, bottom_color:list)` | RGB gradient background. |
| `SetInertiaMomentPrecision(precision:int)` | Decimal precision of inertia tensor display. |
| `SwitchGestureStyle(gesture_type=GestureStyle.Sysplorer)` | Mouse navigation style (SolidWorks/Catia/…). |

## 4. Model browser

| Function | Summary |
|---|---|
| `ShowModelDescription(is_show=True)` | Toggle the description panel. |
| `ExpandBrowser(is_expand=True)` | Expand/collapse the tree. |
| `ShowVisibleElemtsOnly(is_only=True)` | Filter to visible elements only. |
| `FilterBrowser(filter_type=OcafTreeFilter.Model)` | Filter tree by element category. |
| `SearchBrowser(search_content:str)` | Search the tree. |
| `HideEntities(entity_name_arr:list)` | Hide the named entities (names: multibody dotted `base.gear`, fluid bare). |
| `HideOtherEntities(entity_name_arr:list)` / `ShowAllEntities()` | Isolate the named entities (hide the rest — parts/groups/sub-bodies only; fluid: parts only) / show all. |

## 5. Workbench

| Function | Summary |
|---|---|
| `SwitchWorkbenchType(workbench_type:int)` | `CadWorkbenchType.MultiBody` / `.Fluid`. Set before building elements. |
| `GetWorkbenchType()` | → `0` (multibody) or `1` (fluid). |

## 6. Check & generate

| Function | Summary |
|---|---|
| `CheckDesign()` | Toolbox design sanity check (empty/ungrouped parts, marker w/o ref-marker, unknown joints, inertia rule, fluid checks). Run before generating. |
| `GenerateMoModel(package_name:str='', model_type:int=ModelicaModelType.ModelNone)` | Generate the Modelica model (layout + connections + joints included). `ModelNone` → use current workbench. Simulatable top model: `<package>.<cad_model>.<cad_model>_main` — **read the real name back** (`GetModels()` / `model_manager`), don't hardcode the prefix. In iteration accept/exit, `package_name`/`model_type` are ignored. |

## 7. Grouping (multibody)

| Function | Summary |
|---|---|
| `CreateGroup(body_arr:list, group_name:str, is_hide=False)` | Combine parts/groups into a new top-level group. |
| `MoveToGroup(body_arr:list, group_name:str='')` | Move parts/groups under a group (empty → top level). |
| `ClearGroups()` | Delete empty groups. |
| `Ungroup(group_name:str)` | Dissolve a group. |
| `CreateDefaultGroups()` | Auto-create default groups for ungrouped parts. |

## 8. Create — multibody elements

| Function | Summary |
|---|---|
| `CreateMarker(name:str, attached_part:str, coord:list, icon_size=0)` | Create a marker frame. `coord=[x,y,z,rx,ry,rz]` (omit position if attaching to a design point). |
| `CreateRefMarker(base_marker:str, target_part:str)` | Create a reference marker on another part. Base marker and ref must be in different top groups. |
| `CreateConnector(connector_type:int, connector_name:str, first_entity:str, second_entity:str, coord:list, is_show_animation=False, icon_size=0)` | Create a joint. `first_entity` may be a part / design point / another joint's marker (series). `second_entity` is a part (or `"Ground"`). `coord=[x,y,z,rx,ry,rz]`; universal adds `rx2,ry2,rz2`; series-add passes only `[rx,ry,rz]`. |
| `CreateJointMotion(motion_type:int, motion_name:str, attached_connector:str, icon_size=0)` | Add a driver onto a Revolute/Prismatic/Cylindrical joint. Rotational/Translational. |
| `CreateDesignPointByPick(point_name, attached_part, coord:list[x,y,z], icon_size=0)` | Design point by coordinates. |
| `CreateDesignPointByMidpoint(point_name, attached_part, first_coord, second_coord, icon_size=0)` | Design point at midpoint of two points. |
| `CreateDesignPointByOffset(point_name, attached_part, coord, direction[rx,ry,rz], offset:float, icon_size=0)` | Design point offset along a direction (metres). |
| `CreateContact(contact_type:int, contact_name, first_entity, first_face_id, second_entity, second_face_id, icon_size=0)` | Contact between two faces. Face ids from `GetGeometricElementIdsOfPart`. Types: SphereToSphere/Cylinder/Rectangle/Circle. |

## 9. Modify — multibody elements

Each takes `(name, attr_params:dict)` unless noted. Keys are type-specific — query with the matching `Get*Params` first (see `multibody-elements.md`). Marker / Connector / JointMotion / DesignPoint / Contact / material edits need the **MultiBody** workbench; `ModifyPartsParams` and `ModifyGravityParams` also work in **Fluid** (reduced key set).

| Function | Key fields |
|---|---|
| `ModifyPartsParams(body_arr:list, attr_params)` | `name, description, visibility, color[RGBA], is_translucent, material_name, density, mass, centroid[x,y,z], inertia_moment[9], mesh_precision`. (Fluid: only `name,visibility,color,is_translucent`.) `mass` cannot combine with `material_name`/`density`. |
| `ModifyMarkerParams(marker_name, attr_params)` | `name, visibility, icon_size, x,y,z, rx,ry,rz`. Ref-markers: only `visibility`. |
| `ModifyConnectorParams(joint_name, attr_params)` | common `name,visibility,icon_size,x,y,z`; per-type `rx/ry/rz`, `animation, stateSelect, phi_rel_fixed, phi_rel_0, om_rel_0, s_rel_0, v_rel_0, s_rel_1/2, v_rel_1/2`; universal `rx1.. rx2..`, `phi1/2_rel_0`; spherical `sequence_0, phi_rel_0, om_rel_0, enforceStates, useQuaternions, sequence_angleStates` (`"{a, b, c}"`); screw `s`. |
| `ModifyJointMotionParams(motion_name, attr_params)` | `name, visibility, icon_size, motion_type`; rotational `phi.start, w.start`; translational `s.start, v.start` (editable subset depends on `motion_type`). |
| `ModifyDesignPointParams(point_name, attr_params)` | `name, visibility, icon_size, x, y, z`. |
| `ModifyContactParams(contact_name, attr_params)` | `name, visibility, icon_size, ContactOut, k, d, n1, n2, p_max, mue_k, mue_s, mue_r, k_v, v_e1, v_e2`. |
| `ModifyGravityParams(attr_params)` | multibody `gravity_type, acceleration, direction("{0,0,-1}"), constant`; fluid `gravity_type, constant, is_table_on_file, extrapolation, time_scale, g_table, g_table_name, file_path`. |
| `ModifyUnknownConnector(joint_name, attr_params)` | `name, type(DesignElemtType.*), position[x,y,z], rotation[rx,ry,rz] (universal: 6)`. `type` accepts only the 8 real joints (Fixed/Revolute/Prismatic/Cylindrical/Spherical/Universal/Screw/Planar); for a spherical target `rotation` is ignored. |
| `AddNewMaterial(body_arr:list, material_name:str, material_density:float)` | New material (name: digits/letters/Chinese). |
| `RestoreDefaultMaterial(body_arr:list)` | Reset parts to default material. |
| `BatchModifyMaterial(name:str, density:float, body_arr:list, attr_params:{material_name,density})` | Batch material replace by node. |

## 10. Loop tools & geometry (multibody)

| Function | Summary |
|---|---|
| `PlanarLoopConstraint(base_connector:str, connector_arr:list, is_reversed:list=[], base_rotation:list=[])` | **平面环处理 — orientation unification, NOT a loop cut.** Aligns a planar loop's joint orientations onto `base_connector`'s so CAD assembly precision (~1e-6) meets the solver's (1e-10), preventing simulation-init failure. `connector_arr` = joints to adjust; `is_reversed` = per-joint Z-reverse bool list (same length); `base_rotation` = `[Rx,Ry,Rz]` (empty = base joint's current pose). Joints must be Revolute/Prismatic/Cylindrical/Screw/Planar. Multibody only; not in local iteration. The loop **cut** is separate (auto at `GenerateMoModel`, or `RevolutePlanarCut`). |
| `ThickenSurface(surface_name:str, offset:float=0.1)` | Thicken a surface part into a solid. |
| `ExplodedView(factor:int=50, body_arr:list=[], by_group=True)` / `ExitExplodedView()` | Enter/leave exploded view. |
| `Measure(geometry_names:list, circle_arc_measure_type:int, show_xyz_distance=False)` | Measure between geometry (edge/vertex/face names). → list. |
| `GetGeometricElementIdsOfPart(part_name:str, shape_type:int)` | → list of face/edge/vertex ids like `["gear_face <1>", ...]`. Source of face ids for contacts, wet surfaces, rib holes, ports. |

## 11. Create / modify — fluid elements

Switch to `CadWorkbenchType.Fluid` first. Parts are addressed by bare name (`"Tank1"`).

| Function | Summary |
|---|---|
| `CreateSimpleTankSlice(slice_name, tank_name, attr_params)` | Simple tank slice. `attr_params`: `ref_point_type, custom_point, step_type, slice_step, slice_num_per_attitude, yaw, roll`. **Blocking**, → result path. |
| `CreateTankSlice(slice_name, tank_name, attr_params)` | Full tank slice. Adds `posture_type` (FixedAttitude/MinMaxStep/FromFile + matching fields), `is_inertiatensor_checked, is_add_wet_surface, wet_surfaces[{wet_surface_name, wet_surface_indexes}]`. **Blocking**, → result path. |
| `CreateRibSlice(slice_name, rib_name, attr_params)` | Rib slice. Adds `rib_hole_faces:list`. Reference point must lie on the rib; holes within 10mm. **Blocking**, → result path. |
| `CreateFluidPort(port_name, port_type:int, icon_size:int, attr_params:str)` | Create a port on a planar face. `attr_params` is the **target face-id string**. `port_type` = FluidPortType.*. |
| `ModifyRibSliceParams(rib_slice_name, attr_params)` | `lambda_crit, cqmax, cq_gas`. |
| `ModifyFluidPortParams(fluid_port_name, attr_params)` | `name, visibility, icon_size, port_type, area, x,y,z, lambda_crit, cqmax, cq_gas, sigmin, sigmax`. Note: **input** key is `cq_gas`; `GetFluidPortParams` returns it as `cq_Gas`. |
| `ModifyMediumParams(medium_type:int, attr_params)` | Gas → `gas_type(FluidGasMedium.*), gas_medium(GasMedium.*)`; Liquid → `liquid_type(FluidLiqMedium.*)`. |
| `SetSliceChecked(slice_name, check_state=True)` / `IsSliceChecked(slice_name)` | Check state (Fluid workbench only). Per part: ≤1 tank slice, multiple rib slices. |

## 12. Iteration design

Multibody-only (fluid not supported yet).

| Function | Summary |
|---|---|
| `OpenModelInCadBrowser(model_name:str, component_name:str='')` | Re-enter the toolbox on a generated model. Empty `component_name` → whole-model iteration; a top group/sub-body name → local iteration. Model name like `Default1.PickAndPlace.step`. |
| `SetComponentIcon()` | During local iteration, set current view as the component icon. |
| `DeleteModelInCadBrowser(model_name:str)` | Lighten the generated `.mo` and detach it from the toolbox. |

## 13. Delete

| Function | Summary |
|---|---|
| `DeleteEntity(name:str)` | Delete an element. Multibody: groups/parts/sub-bodies/design points/markers/ref-markers/joints (incl. unknown)/drivers. Fluid: parts/contacts/slices/ports. Must match active workbench. |

## 14. Query (Get*)

Most queries are **workbench-scoped**: multibody-oriented (`GetMarkers, GetConnectors, GetUnknownConnectors, GetJointMotions, GetDesignPoints, GetMaterials` + their `*Params`) need the **MultiBody** workbench; fluid queries (`GetSlices, GetFluidPorts, GetFluidPortParams, GetSliceParams, GetMediumParams`) need **Fluid**. Called in the wrong workbench they return a **hint string, not data** (no exception) — check `GetWorkbenchType()` first.

| Function | Returns |
|---|---|
| `GetParts(group_name='')` | child parts/groups/sub-bodies (short names) at that level. Fluid: only the no-arg form (a non-empty `group_name` returns a hint message). |
| `GetMarkers(part_name='')` | markers + ref-markers under a group/sub-body/Ground (multibody). |
| `GetConnectors()` / `GetUnknownConnectors()` | all joints / only unknown joints (multibody). |
| `GetJointMotions()` | all drivers (multibody). |
| `GetDesignPoints(part_name='')` | design points on a part (multibody). |
| `GetSlices(part_name='')` / `GetFluidPorts(part_name='')` | slice / port names on a part (fluid). |
| `GetPartParams(part_name)` | part attributes. Multibody: mass/centroid/inertia/material/… ; fluid: only name/type/visibility/color/is_translucent. |
| `GetMarkerParams / GetConnectorParams / GetJointMotionParams / GetDesignPointParams / GetContactParams` | element attribute dicts (use to learn real keys before Modify*). |
| `GetFluidPortParams(name) / GetSliceParams(name)` | fluid port / slice attributes (fluid). |
| `GetMediumParams(medium_type:int)` | medium attributes; pass `FluidMediumType.Gas` / `.Liquid` (fluid). |
| `GetGravityParams()` | gravity attributes — works in **both** workbenches; dict shape differs (multibody: gravity_type/acceleration/direction/constant; fluid: acceleration/table/file/extrapolation). |
| `GetMaterials()` | all materials (multibody). |
| `GetModels()` | CAD-browser model ids (for `OpenModelInCadBrowser`); **not** the `_main` simulate target. |
| `GetModelBrowserItems(parent_item='')` | child nodes under a tree node. |
| `GetSettings()` | current toolbox settings. |
| `GetWorkbenchType()` | 0 / 1. |
| `ListFunctions()` | every function + one-line description. |

## 15. Enums

```text
DesignElemtType:  ElemtNone=0, BodyPart=1, BodyGroup=2, BodyDesignPoint=3, BodyPointMass=4,
                  BodyMarker=5, BodyRefMarker=6, BodyGround=7,
                  ConnectorFixed=8, ConnectorRevolute=9, ConnectorPrismatic=10,
                  ConnectorCylindrical=11, ConnectorSpherical=12, ConnectorConstantVelocity=13(未开发),
                  ConnectorUniversal=14, ConnectorScrew=15, ConnectorPlanar=16,
                  ConnectorInLine=17, ConnectorInPlane=18, ConnectorOrientation=19,
                  ConnectorParallelAxes=20, ConnectorPerpendicular=21,
                  MotionTranslational=22, MotionRotational=23,
                  ForceSingleComponentForce=24, ForceSingleComponentTorque=25,
                  ForceVectorForce=26, ForceVectorTorque=27, ForceGeneralForce=28, ForceGravity=29,
                  BodySubBody=30, ConnectorUnknown=31, FluidPort=32,
                  SliceSimpleTank=33, SliceTank=34, SliceRib=35, FluidMediumGas=36, FluidMediumLiq=37,
                  ContactSphereToSphere=38, ContactSphereToCylinder=39,
                  ContactSphereToRectangle=40, ContactSphereToCircle=41
CadWorkbenchType:    MultiBody=0, Fluid=1
ModelicaModelType:   ModelNone=-1, ModelMultiBody=0, ModelFluid=1
JointMotionType:     Displacement=0, Velocity=1, Acceleration=2
StateSelectType:     Prefer=0, Never=1, Avoid=2, Default=3, Always=4
GravityType:         NoGravity=0, UniformGravity=1, PointGravity=2
FluidGravityType:    Constant=0, TableData=1
MeshPrecision:       PrecisionHigh=0, PrecisionMiddle=1, PrecisionLow=2
ShapeType:           Face=0, Edge=1, Vertex=2
ReferencePointType:  Origin=0, GravityCenter=1, CustomPoint=2
StepType:            FixedStep=0, SlicesPerAttitude=1
PostureType:         FixedAttitude=0, MinMaxStep=1, FromFile=2
FluidPortType:       VarGasTankOrigice=0, VarLiqankOrigice=1, VarFileankOrigice=2
FluidMediumType:     Gas=0, Liquid=1
ViewDirection:       ViewFront/Back/Top/Bottom/Left/Right=0..5, ViewISOZXY=6
ViewDisplayMode:     DisWireFrame=0, DisShaded=1, DisShadedEdges=2 (preview不支持2)
ViewProjectionMode:  ProjOrthogonal=0, ProjPerspective=1
Extrapolation:       HoldLastPoint=0, LastTwoPoints=1, Periodic=2, NoExtrapolation=3
GestureStyle:        Sysplorer=0, SolidWorks=1, Catia=2, ProEngineer=3, Unigraphics=4
WindowType:          CadWindow=0, QuickPreview=1
CircleArcMeasureType: CircleCenter=0, MinDistance=1
OcafTreeFilter:      Model=0, Body=1, UngroupPart=2, Marker=3, DesignPoint=4, Connector=5,
                     JointMotion=6, Force=7, Material=8, Slice=9, Port=10, Medium=11
GasMedium:           GasMediumNone=-1, GasMediumPerfect=0, GasMediumSemiPerfect=1
FluidGasMedium:      GasNone=-1, GasAir=0, GasStoichio=1, GasH2=2, GasO2=3, GasN2=4, GasCO2=11 ... (see CADToolbox.py)
FluidLiqMedium:      LiqMediumNone=-1, ThermalOil=0, LiqWater=53, LiqGlycol=54 ... (see CADToolbox.py)
```

Reference enums by attribute (`cadtool.DesignElemtType.ConnectorRevolute`), not raw integers, so the code survives version changes.
