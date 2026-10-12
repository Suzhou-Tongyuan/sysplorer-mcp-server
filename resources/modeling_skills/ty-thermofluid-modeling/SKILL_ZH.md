# TY 热流体建模

本文件是 `SKILL.md` 的中文阅读版。本 skill 只能作为 `ty-sysplorer-modeling-rules` 之后的领域薄补丁使用；父级 skill 负责分流、七门闸、布局时机、修复闭环和交付证据。

## 父规则与 MCP 0.4

会话复用、工具分类、错误解析及重试统一引用 `../ty-sysplorer-modeling-rules/references/shared-standards.md`；验证深度、Gate 6 与完成状态引用 `../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md`。离线/源码任务不调用会话。已有具体故障由父规则规定的独立调试入口主导，本领域只提供定向证据，不重启完整建模；新建中的失败保留原任务。

执行到用户要求的终端阶段即停止。结果变量、KPI、曲线、动画和正式文档仅在用户要求或约定验收标准确需时执行，否则标记 `not_required`；不得为填表自动推定 proxy 指标。仿真成功与物理结果达标分别表述。

MCP 0.4 的类、组件、端口与文本查询使用 `model_inspect`，比较使用 `compare_model`，生命周期操作使用 `model_manager`。`call_code` 仅接受 `run_sysplorer_api` 或兼容别名 `run_script`，必须传对象 `payload` 并显式导入 ModelingPy。检查/翻译/仿真即使未传 `reload_mo_path`，也可能对已加载用户文件自动布局写回，不能作为无写入的只读评审工具；遵守父级授权边界，并把实际图形改动纳入 Gate 6。

## 最小读取

本文与对应 `SKILL.md` 中所有 `references/...`、`workflows/...` 路径均相对于**本 skill 目录**（包含 `SKILL.md` 的文件夹），不是工作区根目录，也不是上层 `skills/` 目录。

| 需求 | 读取 |
|---|---|
| 需求分类 | `references/requirement-map.md` |
| 库/组件映射 | `references/library-selection.md`, `references/component-map.md` |
| 介质 | `references/media-selection.md` |
| 参数/建模规则 | `references/parameter-rules.md`, `references/modeling-rules.md` |
| 验证 | `references/validation-rules.md` |
| 修复 | `references/common-errors.md` |
| 验收 | `references/acceptance-checklist.md`, `references/output-contract.md` |
| 手册查询 | 仅在精简参考不足时读取 `references/manual-index.md` |

## 专项流程

- 从场景建模：`workflows/build-from-scenario.md`
- 修复现有模型：`workflows/repair-existing-model.md`
- 验证样例或现有模型：`workflows/verify-example.md`

## 领域增量

- 商业库路径（含标准库＋商业库组合）固定使用 `Modelica 4.0.0.TY.1`。用户/工程版本冲突时报告依赖约束不一致，不静默改写；父规则单独使用时的版本覆盖例外不适用于此。热流体库范围只约束负责的子系统，保留父规则已选标准库和支持领域组件。
- 用户指定或父规则/有效上下文已选热流体商业组件时使用本领域；未指定库先由父规则评估标准库能力，不足时组合补足。先判断新建、修复、样例验证或结果复核；运行预检仅针对已选库且不超过请求深度，离线/只读任务不追加运行。
- 提交拓扑前先确定介质和相态假设。
- 先搭最小能量/流体路径，再添加控制、传感器和次级回路。
- 对需要图形交付的模型，每个实例化组件都必须显式带有 `annotation(Placement(...))`，确保图形层能显示图标，不能依赖工具自动布局。
- 实例化和布置组件时，优先保持组件默认图标尺寸与宽高比例不变；优先通过移动位置完成排布，不要仅为对齐而拉长、压缩或变形组件。
- 每个必要的 `connect(...)` 都必须通过显式 `annotation(Line(...))` 在图形层可见；仅有语义连接而没有可视走线不能作为交付。当两个数组接口是一一对应连接时，使用单条数组连接，例如 `connect(a[:], b[:])`，避免展开为冗余的逐个连线。
- 顶层交付模型至少要包含基础的 `Icon(...)` 与 `Diagram(...)` 坐标系注释，除非父级流程后续会用 smart layout 结果覆盖。
- 明确实际使用的库和介质。
- 按任务验证压力、温度、流量、湿度、焓、换热率、压缩机功率、COP 或用户指定指标。
- 在本次适用验证范围内，介质错误、边界/参考缺失、不可能的压力/温度、发散或必需变量未验证视为失败；结果核验不在范围时标记 `not_required`，仅要求仿真成功的任务可据实完成。
- 图解任务仍由父级 Gate 6 控制布局时机与复检要求。布局验收以模型结构和工具可读证据为基础，检查 `Placement`、`Line`、坐标系、连接器端点以及可用的布局工具诊断信息。
- 图片按父 Gate 6 的用户需求及可用能力选用；能力不可用时停止反复尝试并报告原因。用户明确要求图片时，图片交付仍须单列未完成，不与功能/结构化验收混同；未查看图片不得声称目视确认遮挡等视觉项。

## 修复优先级

以下为诊断定位顺序，只执行到请求终态，不要求运行全部后续阶段：

`medium selection -> boundary/reference -> topology -> parameters -> discretization/resistance organization -> initialization -> translation -> simulation -> result interpretation`

保留已有有效结构，修复后回到失败的父级 Step/Gate。

## 交付增量

在父级交付证据基础上补充：

- 临时假设、介质假设、剩余风险、未解决项和下一步建议。
- 必要的过程、热与控制连接是否都有 `annotation(Line(...))` 等图形层证据，而不只是语义连接。
- 实际采用的布局审核方式：结构/代码检查、布局工具诊断以及可选的导出图片检查。仅在请求过或实际尝试过导图时报告导出路径与状态；缺少图片能力本身不表示结构化布局验收未闭环。
- 若交付库，说明顶层包和绑定依赖。
