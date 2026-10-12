# 组件映射 / Component Map

用于在父级已选 TY 机械商业部分中完成“需求特征 -> 优先子库 -> 子包入口 -> 候选组件”的收敛。先继承有效上下文及标准库＋商业库组合；下表仅限制商业组件首轮搜索，不删除已选标准库和其他领域组件。观测、曲线和动画条目只在用户验收范围内执行。

## 选型总顺序

1. 先判断运动空间与系统层级。
2. 再判断功能角色。
3. 再判断物理对象或特殊机理。
4. 收敛候选组件后，再查询真实参数名并进入建模。

## 文档查询收敛策略

三轮评测中反复出现的问题是：为了找组件而重复读取大段文档，或者在未确认接口前先写模型再反复修。按以下顺序收敛：

1. 先用任务特征命中下方子库映射表，只选 1-2 个优先子库。
2. 用 `model_inspect(action="get_classes", model_name=...)` 获取明确包/子包列表；顶层已加载列表用 `session_manager(action="get_loaded_models")`。受保护模型的公开组件列表为空时改查 `get_lib_model_document`，不读取受保护源码。
3. 用 `get_lib_model_document(full_class_names=[...])` 批量查询候选子包，不逐个扫全库。
4. 对最终候选组件确认三件事：完整类名、连接器类型、关键参数名。没有确认接口前不要写跨库连接。
5. 信息查询任务只深挖与用户分类直接相关的子包；最终说明查询范围和未展开的旁支，不追求无边界“全库百科”。

## 子库优先映射

| 任务特征 | 优先子库 | 一级入口 | 典型关键词 | 强制检查项 |
|---|---|---|---|---|
| 一维基础机械 | `TYMechanics` | `Translational.*`、`Rotational.*` | 质量、惯量、弹簧、阻尼、摩擦、力源、扭矩源、基础传感器 | 明确平动或转动接口 |
| 一维传动系统 | `TYDriveline` | `Mechanisms`、`PowerSource`、`Gears`、`CouplingElements`、`Brake`、`Actuators` | 变速箱、曲柄滑块、发动机、离合器、刹车、联轴器、绳索传动 | 明确动力链方向与输入输出轴 |
| 二维平面机构 | `TYMechanics2D` | `World2D`、`Parts`、`Joints`、`Sensors`、`Sources` | 平面机构、二维机械臂、平面悬架、平面运动副 | 显式放置 `World2D` 或等价环境组件 |
| 三维多体骨架 | `TYMultibody` | `World`、`Bodies`、`FlexibleBeam`、`Joints`、`Forces`、`Constraints`、`Sensors` | 多体、三维刚体、梁、关节、姿态、约束 | 显式放置 `TYMultibody.World` 或等价世界组件 |
| 三维传动细节 | `TYDriveline3D` | `RopeDrive3D`、`ChainDrive`、`GearsDrive`、`Bearing`、`Mechanisms` | 绳索、链条、啮合、轴承、空间传动、滑轮、绞盘 | 同步检查与 `TYMultibody` 参考系的一致性 |
| 接触与碰撞 | `TYContact` | `PlaneContact`、`PointContact`、`LineContact`、`SurfaceContact`、`Sensors` | 接触、碰撞、法向力、摩擦力、点线面接触 | 明确接触对象、接触类型和观测量 |
| 柔性与刚柔耦合 | `TYFlexBody` | `ModalBeam`、`ModalBody`、`Utilities` | 柔性体、模态、MNF、刚柔耦合、柔性机械臂 | 明确柔性体来源和模态文件约束 |

## 需求到 TY 子库快速分流表

用于在用户自然语言需求较短时，快速得到首轮 TY 子库、建模路径和最小闭环。该表只用于首轮分流；最终组件路径、端口和参数仍必须通过 Sysplorer 查询确认。

| 用户需求说法 | 推荐子库 | 首选建模路径 | 首轮最小闭环 | 关联模板或骨架 |
|---|---|---|---|---|
| 搭一个转轴弹簧阻尼模型、转动惯量模型、扭振模型 | `TYMechanics.Rotational` | 一维转动机械 | 转动惯量 + 弹簧阻尼 + 力矩源 + 角位移/角速度传感器 | `templates/model-skeletons/mechanical-system-base.example.mo` |
| 搭一个直线运动质量块、滑块弹簧阻尼模型 | `TYMechanics.Translational` | 一维平动机械 | 质量 + 弹簧阻尼 + 力源 + 位移/速度传感器 | `templates/model-skeletons/mechanical-system-base.example.mo` |
| 搭一个齿轮传动、联轴器传动、传动链 | `TYDriveline` | 一维传动系统 | 动力源 + 齿轮/联轴器 + 负载 + 转速/力矩观测 | `templates/scenarios/mechanical-system-min-loop.example.json` |
| 搭一个曲柄滑块、曲柄连杆、平面四杆机构 | `TYMechanics2D` 或任务指定 TY 平面/多体子库 | 二维平面闭环机构 | `World2D` + 杆件 + 关节 + 驱动 + 切割铰 + 角度/位置观测 | `templates/scenarios/user-input-minimum-form.md` |
| 搭一个三维机械臂、空间连杆、多体摆臂 | `TYMultibody` | 三维多体系统 | `World` + 刚体 + 关节 + 驱动 + 位姿/关节变量观测及多体动画（仅按请求） | `templates/model-skeletons/mechanical-system-base.example.mo` |
| 做一个碰撞接触模型、接触力模型、摩擦接触模型 | `TYContact` | 接触系统 | 接触对象 + 接触模型 + 相对运动边界 + 接触力/穿透量观测 | `templates/scenarios/mechanical-system-min-loop.example.json` |
| 做刚柔耦合、柔性梁、模态体模型 | `TYFlexBody` | 柔性体系统 | 刚体/关节 + 柔性体 + 模态文件或柔性参数 + 变形/模态响应观测 | `templates/scenarios/user-input-minimum-form.md` |

快速分流执行要求：

- 能直接命中表格时，先输出分流依据、推荐子库、首轮最小闭环和仍需查询确认的组件。
- 不能直接命中时，先列出不确定点，再回到 `templates/scenarios/user-input-minimum-form.md` 补齐必须字段。
- 分流后不得立即猜参数名；必须查询真实组件路径、端口和参数。
- 若用户指定 TY 子库与快速分流表冲突，优先尊重用户指定，并说明冲突和风险。

## 按功能角色收敛

| 功能角色 | 优先子包 |
|---|---|
| 环境与世界 | `World`、`World2D` |
| 本体与零部件 | `Bodies`、`Parts`、`Components`、`FlexibleBeam`、`ModalBeam`、`ModalBody` |
| 连接与运动副 | `Joints`、`Mechanisms`、`Constraints`、`CouplingElements` |
| 传动件 | `Gears`、`GearsDrive`、`RopeDrives`、`RopeDrive3D`、`ChainDrive`、`Bearing` |
| 激励与动力源 | `Sources`、`PowerSource`、`Actuators` |
| 接触效应 | `PlaneContact`、`PointContact`、`LineContact`、`SurfaceContact` |
| 传感与观测 | `Sensors` |
| 可视化与辅助 | `Visualizers`、`Visualize`、`Utilities` |

## 高频拓扑预检

| 拓扑 | 建模前必须确认 | 常见失败 |
|---|---|---|
| 一维转动传动链：转速源 -> 齿轮 -> 弹簧/阻尼 -> 惯量 | 源、齿轮、弹簧阻尼、惯量的端口均为同一转动域；只有必要的固定支座；负载惯量保留可运动自由度；传动比方向与预期转速关系一致 | 负载或中间轴两端同时接地导致过约束；传动比符号/方向解释错误；传感器串接方式改变物理链 |
| 一维平动质量-弹簧-阻尼 | 固定端只用于边界或弹簧参考；质量块不能被两个刚性边界锁死；驱动力/速度源与运动方向一致 | 方程过约束、位移恒为零、初始冲击过大 |
| `TYDriveline3D` 齿轮/绳索/链条与多体框架 | `flange`、`frame`、信号端口不能混连；确认是否需要 `TYMultibody.World`、支撑框架或轴承参考 | 跨库接口不兼容、inner/outer world 缺失、动画无有效运动 |
| 电梯/提升/按钮状态场景 | 先分清物理提升机构与控制状态机；物理子模型先做最小升降闭环，控制按钮可用简化信号驱动；每个自定义组件先做方程/变量平衡 | 直接写大系统导致方程不足、控制变量无方程、机械部分未闭合 |
| 多体摆杆/弹性支撑 | 世界、固定端、关节、刚体、支撑力元和传感器的连接器域一致；受控阻尼与自由摆动可作为两个工况或参数化模式 | 缺世界、支撑力方向错误、仿真前后变量选择不一致 |

## 特殊机理二次分流

- 出现 `柔性/MNF/刚柔耦合` 时，优先转向 `TYFlexBody`。
- 出现 `接触/碰撞/接触力` 时，优先转向 `TYContact`。
- 出现 `平面机构/x-y/绕 z 转动` 时，优先转向 `TYMechanics2D`。
- 出现 `三维刚体/姿态/世界坐标/空间机构` 时，优先转向 `TYMultibody`。
- 出现 `三维绳索/链条/轴承/齿轮啮合` 时，优先转向 `TYDriveline3D`。

## 平面闭环多体机构规则

当用户需求包含曲柄滑块、曲柄连杆、四杆机构、平面闭环机构、带环多体机构等特征时，必须先判断是否存在运动闭环。

| 场景 | 必须动作 | 说明 |
|---|---|---|
| 曲柄滑块 | 将闭环中的一个转动副替换为 TY 切割铰 | 避免闭环约束过强或方程冗余 |
| 曲柄连杆 | 将闭环中的一个转动副替换为 TY 切割铰 | 替换位置应记录在组件映射和交付说明中 |
| 平面四杆或其他闭环机构 | 选择一个合适转动副作为切割位置 | 优先选择对驱动、输出和观测语义影响最小的位置 |

执行要求：

- 使用切割铰前，必须通过 Sysplorer 查询 TY 库中真实的切割铰组件路径、端口和参数。
- 不得用普通转动副完整闭合所有环路后直接交付。
- 不得用非 TY 库组件替代 TY 切割铰。
- 组件映射输出中必须写明：闭环位置、被替换转动副、采用的切割铰组件、替换原因。
- 若当前 TY 库版本中切割铰名称或路径不确定，先检索 TY 帮助或库文档，再建模。

## 候选组件收敛后的强制动作

- 先输出准备采用的 TY 子库与候选组件列表，再进入建模。
- 对最终候选组件逐个使用 Sysplorer 参数查询接口获取真实参数名。
- 参数赋值、参数修改和 `redeclare` 只允许基于已查询到的真实参数名。
- 若初步判断无合适组件，先扫描 TY 帮助文档或库文档，再决定是否告知缺件。
