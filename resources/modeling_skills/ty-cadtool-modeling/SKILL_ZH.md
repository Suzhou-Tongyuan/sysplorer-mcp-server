> 本文件仅用于中文审核参考，实际任务执行请调用 SKILL.md。

# TY CAD 工具建模（几何驱动）

用同元 **CAD 工具（CADToolbox Python API）**，经 Sysplorer MCP 把真实 CAD 装配转换为 Sysplorer 的 Modelica 模型。与 `ty-mechanical-modeling`（凭文字需求手写 TY 库组件）不同，本 skill 是**几何优先**的：质量、惯量、质心来自实体，拓扑来自你在真实零件上放置的运动副；随后 `GenerateMoModel` 自动产出带布局的 `.mo`。

仅当有（或将有）几何文件可导入时使用。若用户只用文字描述机构、没有 CAD 文件，改用 `ty-mechanical-modeling`。

## 心智模型：盲态复刻官方 UI 流程

CAD 工具帮助文档（新手入门 + 应用案例）对**每一个**模型都走**同一套五个命名阶段**，仅②③阶段因领域而异。GUI 用户拾取几何特征、工具自动**推理**位置与姿态（闪电模式 + 特征拾取智能推理）；你则**经 MCP 盲操作**，故每个阶段的本质是**用 API 复刻该 UI 步骤所做的事**——例如用户拾取圆柱面、工具把运动副吸附到其轴线处，你就 `Measure` 出该圆的圆心+轴并把数字传进去。牢记官方阶段名，便于对照文档与界面。

`GenerateMoModel` 之后即是普通 Modelica 物理模型，因此沿用 `ty-sysplorer-modeling-rules` 的下游纪律：`check_model` → 翻译 → 仿真 → 读结果；路径只用 Agent CWD / `GetDirectory`；硬禁项（`ClearAll`、`ChangeDirectory`、`Exit`）依旧。**图面布局由 `GenerateMoModel` 自动完成**（自带引擎排布组件、连线与运动副），一般无需手动 `smart_layout` 回写；仅当生成图面不可用时才回退。

## 最小阅读表

| 需要 | 阅读 |
|---|---|
| 经 MCP 驱动 CADToolbox 的桥接方式 | `references/mcp-workflow.md` |
| 完整 API 清单（分类） | `references/api-reference.md` |
| 多体元素规则（运动副/标架/接触/命名/坐标/闭环） | `references/multibody-elements.md` |
| **从几何精确获取运动副位置与轴（盲态复刻闪电模式智能推理）** | `references/joint-placement.md` |
| 流体元素规则（油箱/肋板切片、端口、介质） | `references/fluid-elements.md` |
| 失败与修复 | `references/common-errors.md` |
| 新建多体模型（5 阶段分步） | `workflows/build-multibody-from-cad.md` |
| 新建流体（油箱）模型（5 阶段分步） | `workflows/build-fluid-from-cad.md` |
| 在已有模型上迭代/重进工具 | `workflows/iterate-existing-model.md` |
| 可直接套用的 run_sysplorer_api 模板 | `templates/run-script-skeleton.md` |

## 管线——五个命名阶段

每个 `cadtool.*` 动作都在一次 `call_code(mode="run_sysplorer_api")` 内完成；校验尾段（⑤）用专用 MCP 工具——run_sysplorer_api 头部与工具映射见 `references/mcp-workflow.md`。

**阶段 0（一次）**：`session_manager(action="ensure")`；确认工作目录（Agent CWD / `GetDirectory`），禁止写到 MCP 程序目录。

### 多体——导入 → 分组 → 连接和驱动 → 生成 → 仿真

1. **导入 CAD 模型**——`ImportCad(绝对ASCII路径)`（多体为默认工作台，可显式 `SwitchWorkbenchType(MultiBody)`）。路径须绝对、ASCII、Modelica 合法。曲面/破损实体导入为**红色**且质量为 0 → `ThickenSurface` 或手填质量。商用格式（sldasm/CATProduct）会自动求解运动副，可能留下**未知运动副**（在③处理）。随后**探查+测量**：查模型树（`GetParts`…），并**在分组前测量好每个运动副特征**、把世界坐标存成数字——分组改变零件**路径**但不改世界坐标（`references/joint-placement.md`）。
2. **为零件分组**——`CreateGroup` / `MoveToGroup` / `ClearGroups` / `CreateDefaultGroups`。**一个刚体=一个组**；互固定零件合并进同一组，**绝不**用固定副互连。分组即刚体拓扑。
3. **添加连接和驱动**（+接触/标架/设计点/材料/重力）——`CreateConnector`（运动副，坐标用测量值），`CreateJointMotion`（驱动，仅转动/平移/圆柱副；设 `驱动类型`），`CreateContact`（UI 在 力→点点接触），`CreateMarker`+`CreateRefMarker`，`CreateDesignPoint*`，重力/材料。用**唯一一个对 `"Ground"` 的 `ConnectorFixed`** 锚定。修正/删除**未知运动副**（`GetUnknownConnectors`→`ModifyUnknownConnector`）。闭环见下文。
4. **生成 Modelica 模型**——`CheckDesign()`（=检查）→ `SaveCadFiles()`（可选）→ `GenerateMoModel("", ModelicaModelType.ModelMultiBody)`（=接受并退出+导出设置；**即使跳过 CheckDesign 也会自动执行必要检查**）。默认包名 `Default`+数字（如 `Default1`）；可仿真顶模型 `<包>.<CAD>.<CAD>_main`；每个分组各一个 `[group].mo`；**每个驱动默认配一个 `Modelica.Blocks.Sources.RealExpression`=1 的源**。`GetModels()` 返回的是 CAD 浏览器标识，**非** `_main` 目标——需确认真实名。
5. **仿真及结果查看**——`check_model` → `translate_model` → `simulate_model(<…>_main, stopTime=…)` → `result_manager`/`plot_manager`+动画。真实运动需把驱动默认 `RealExpression`=1 换成 `TimeTable` 等并设 `驱动类型`。判断动画（闭环、位姿、关节运动、干涉、跳变）；趋势不对则回到最早可疑阶段（轴向、切割、质量、初值）。

### 流体——导入(切流体台) → 切片 → 端口/介质/重力 → 生成 → 仿真

1. **导入 CAD 模型**——**先切流体台**：`SwitchWorkbenchType(Fluid)` 再 `ImportCad(...)`。流体按**裸名**寻址零件（`"Tank1"`）。曲面零件 → 先 `ThickenSurface`。
2. **油箱切片**——`CreateSimpleTankSlice`/`CreateTankSlice`/`CreateRibSlice`（切片菜单）。**阻塞**（返回结果路径；切片中勿发其他调用）。每零件至多勾选 1 个油箱切片、可多个肋板切片（`SetSliceChecked`）。肋板孔须与参考点共面。
3. **端口/介质/重力**——`CreateFluidPort`+`ModifyFluidPortParams`（设计→端口；**仅平面**；可变油箱 液体/气体/填充 孔口），`ModifyMediumParams`（气/液），`ModifyGravityParams`。
4. **生成 Modelica 模型**——`CheckDesign()` → `GenerateMoModel("", ModelicaModelType.ModelFluid)`（生成类型默认流体）。
5. **仿真及结果查看**——常需先把 `<tank>.mo` 的 `NumGauge` 设为 0（`run_with_ready set_model_param` / run_sysplorer_api `SetParamValue`），再 `check_model`→`translate_model`→`simulate_model`→`result_manager`（燃油高度/气体体积）。多油箱需手动连接（设 `tankPortDemux` 的 N、加 `TankPort` 接口、在顶模型连 `RibSliceN`）。**流体不支持迭代设计**——改设计需重开 `.sys3d`（`OpenCadFile`）重新生成。

### 官方术语 ↔ 菜单 ↔ MCP/API

| 官方术语 (UI) | 菜单 / 位置 | MCP / API |
|---|---|---|
| 打开 CAD 工具 / 导入 | 工具→CAD 工具→导入 | `OpenCadWindow` / `ImportCad` |
| 工作台 (多体 / 流体) | 左上工作台切换 | `SwitchWorkbenchType(MultiBody \| Fluid)` |
| 组合 / 移动至 / 清理 / 默认分组 | 菜单·右键 | `CreateGroup` / `MoveToGroup` / `ClearGroups` / `CreateDefaultGroups` |
| 固定/转动/平移/圆柱/球/平面/万向/螺旋副 | 连接 | `CreateConnector(ConnectorFixed/Revolute/…)` |
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
| 接受并退出 + 导出设置 | 接受并退出 | `SaveCadFiles` + `GenerateMoModel(pkg, type)`（自动检查） |
| 迭代设计 (整体/局部) | CAD 浏览器 双击/打开 | `OpenModelInCadBrowser`（仅多体） |

## 多体关键不变量

- **一个刚体=一个组**。彼此不动的零件放进同一组，**绝不**用 `ConnectorFixed` 互连。每个组生成一个体，平面环自动识别器走的是**"组"图**——把一个刚体拆成多个固定副相连的组会污染该图、破坏环识别（`references/multibody-elements.md` → 分组）。
- **世界锚定**：有且仅有一个固定副，且其 `second_entity` 为 `"Ground"`。出现第二个固定副、或两零件之间的固定副，说明本应分组。
- **运动副坐标不要猜，要测量，且在分组之前**。这是 UI 闪电模式智能推理的盲态等价：拾取圆边 → 圆心是轴上点、孔轴即运动副轴。`coord=[x,y,z,rx,ry,rz]`=世界系米 + 外旋 XYZ 度，使局部 **+Z** 指向运动轴。`GetGeometricElementIdsOfPart` 按零件**当前点分路径**解析（分组会改路径），故导入后立刻枚举/测量并存数字（坐标对分组不变）。完整配方与助手：`references/joint-placement.md`。
- **驱动**（`CreateJointMotion`）只能挂转动/平移/圆柱副。用 `ModifyJointMotionParams` 设 `驱动类型`（位移/速度/加速度；案例都显式设置）。生成时每个驱动都被配上默认 `RealExpression`=1 源——做规定运动需替换（如 `TimeTable`）。
- **未知运动副**（常见于商用 CAD 导入）显示**红色**且**阻断生成**。`GetUnknownConnectors()` → `ModifyUnknownConnector(name, {"type": …, "position":[…], "rotation":[…]})`，或删除重建。
- **闭环——两个不同概念（切勿混淆）：**
  1. **姿态统一 = `PlanarLoopConstraint(base_connector, connector_arr, is_reversed, base_rotation)` = 平面环处理工具**。当 CAD 装配精度（~1e-6）低于求解精度（1e-10）时，自动求得的运动副姿态有误差，导致平面环模型**仿真初始化失败**。该工具把环内所有运动副姿态**统一**到基准姿态（可对个别副 Z 轴反向）。它**不是切割**，且**在生成之前**做（双滑块 CATIA 案例即如此，随后直接生成）。`base_connector`=基准副，`connector_arr`=待调整副，`is_reversed`=各副 Z 轴反向 bool 列表（等长），`base_rotation`=`[Rx,Ry,Rz]`。
  2. **闭环切割（cut joint）** 消除冗余约束。**优先自动**：分组干净时 `GenerateMoModel` 对平行轴平面环自动插入切割（`crank_rocker_mechanism` 无手动切割）。**兜底**（空间环/非平行轴/自动失效）：生成后把某 Revolute 改为 `TYMultibody.Joints.RevolutePlanarCut`（`SetComponentInfo`）。CADToolbox **无**独立切割 API。
  - 顺序：分组干净 →（平面环精度/姿态问题）`PlanarLoopConstraint` → 生成（自动切割）→ 若仍过约束再 `RevolutePlanarCut`。
- **赋值前先查参数**。`Modify*Params` 键随类型而异（转动副 `phi_rel_0`/`om_rel_0`；平移副 `s_rel_0`/`v_rel_0`；球副/重力方向用 `"{a, b, c}"` 字符串）。先用对应 `Get*Params` 取真实键。

## 流体关键不变量

- **导入前先切到 `CadWorkbenchType.Fluid`**（简单油箱教程是切流体台再导入）。流体用裸名寻址（`"Tank1"`），非多体点分路径。
- 切片（`CreateSimpleTankSlice`/`CreateTankSlice`/`CreateRibSlice`）**阻塞至完成**并返回结果路径；切片中勿发其他调用。每零件至多勾选 1 个油箱切片、可多个肋板切片。湿面/肋板孔/端口的面 ID 来自 `GetGeometricElementIdsOfPart(part, ShapeType.Face)` 且须为**平面**；肋板孔须与参考点共面。
- 介质 `ModifyMediumParams(Gas|Liquid, {...})`；端口 `CreateFluidPort`/`ModifyFluidPortParams`；重力 `ModifyGravityParams`。流体树根节点：物体/力/介质。
- **曲面零件**（体积 0、红色）须先 `ThickenSurface` 实体化再切片。
- 仿真时流体模型常需把 `NumGauge` 设为 0；多油箱需手动连接端口。流体**无**迭代设计。

## 校验与交付

除父规范证据外，还需说明：

- 源 CAD 文件与格式、所选工作台、生成模型全名、`simulate_model` 结果。
- 多体：分组方案；世界锚定是否存在；闭环处理（用了 `PlanarLoopConstraint` 姿态统一？切割是自动还是 `RevolutePlanarCut`？为什么）；驱动类型是否设置；未知运动副是否修正；动画判断。
- 流体：勾选了哪个切片、介质、端口、切片结果路径、gauge/NumGauge 与油箱间连线。
- 凡是臆测而非查询得到的参数值，以及任何元素替换及其预期影响。

## 修复优先级

走最短阻塞链：

`导入(路径/格式/红色曲面) -> 工作台匹配 -> 未知运动副 -> 世界/Ground 锚定 -> 实体名 -> 运动副拓扑/平面环姿态/闭环切割 -> 参数 -> CheckDesign -> GenerateMoModel -> 翻译 -> 求解/初值 -> 结果解读`

保留已建的有效结构，修最早的阻塞点，再回到失败阶段。具体失败特征与修法见 `references/common-errors.md`。
