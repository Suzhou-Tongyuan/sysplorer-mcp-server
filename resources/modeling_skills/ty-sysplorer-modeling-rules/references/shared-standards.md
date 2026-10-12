# 共用标准与受保护商业库证据

本文件承接工具、会话、路径、建模形式、商业库证据和通用验证边界。七门闸的通过条件、Gate 6 记录和交付状态以 `workflows/seven-gates-validation.md` 为唯一权威。

## 1. 工具、会话与路径

1. 首次依赖工具时核对当前目录、版本和参数；当前任务确认的契约可复用。以下以 MCP 0.4 分类为目标，旧服务缺少新工具时记录能力不匹配，不尝试未知写操作，也不绕过 MCP 直连 Sysplorer。
2. 离线模型/日志检查不调用会话工具。首次 live access 先 `session_manager(action="probe")`（若支持）确认目标，再 `health`；同一有效会话复用证据，切换/断连/基础设施异常后重查。`version` 仅查询 MCP 版本，不连接软件。
3. `health` 返回 `starting:true` 时按启动进度有界查询 health；不要调用 ensure/restart 或重载 MCP 重复拉起 GUI。没有进展或明确错误时转入环境取证，停止原样轮询；不得关闭、重启用户附着 GUI。`ensure` 不是每个工作流的固定前置步骤。
4. 项目产物使用 Agent CWD 与显式路径。需要时分别用 `session_manager(action="get_directory")` / `get_sim_result_directory` 查询软件工作目录/结果目录，它们不等于 MCP workspace。禁止 `ClearAll`、`ChangeDirectory`、`ChangeSimResultDirectory`，不得硬编码旧结果路径。

### 1.1 MCP 0.4 分类调用

| 任务 | 入口与关键契约 |
|---|---|
| 新建/打开/载入/卸载/保存模型 | `model_manager`：new/open/load_file/unload/save/save_as；open 接已加载全名，load_file 接文件；save 原位保存，save_as 另存并核对 saved_path；restriction 默认 model |
| 类、组件、端口、文本、描述、错误 | `model_inspect`：get_classes/get_components/get_component_ports/get_component_type_name/get_model_text/get_model_description/get_component_description/lookup_component/get_last_errors；文本查询仅用于有权读取的用户源码，商业实现禁止提取 |
| 已加载模型快照 | `session_manager(action="get_loaded_models")`；深入子包时给 model_inspect 明确全名，不依赖空根查询 |
| 对比 | `compare_model(model_name, model_name_b, is_file, open_model_first)`；区分类名与文件路径 |
| 本地已装库 | `load_library(action="installed" / "load", library_name, library_version, use_cache)` |
| 缺失库准备 | 仅实际暴露时使用 `library_prepare`（lite/mols）；先 plan/dry_run，只有安装/下载属于授权范围才执行，保留所选版本，不默认追 latest |
| 检查/翻译/仿真 | `check_model` / `translate_model` / `simulate_model`；保留 reload_mo_path，但不再传旧 smart_layout_* 参数或 auto_generate_graph |
| 布局 | `smart_layout` 的 layout_only/finalize_generation/writeback_mo；writeback 明确目标类和文件，区分文件写回、重载及官方 RouteLine 保存状态 |
| 图片导出 | 用户需要时先 `get_api_document("ExportDiagram")`，再用 call_code 的 API 脚本；不是 model_manager/model_inspect/plot_manager 的导图动作 |
| 结果及绘图/动画 | `result_manager` / `plot_manager`，仅验收需要时执行；读取实际结果上下文并保留来源及 warning |
| 公开文档与语料 | `get_lib_model_document`、`get_api_document`、`resources_retrieval`；多类文档优先 full_class_names，部分失败保留成功项并核对 failed_class_names |
| 未封装 API / 工具箱脚本 | `call_code(mode="run_sysplorer_api", payload={"python_source": "..."})`，或 payload.script_path；payload 必填对象，脚本显式 import mworks.sysplorer as ModelingPy；只用于官方 API，不当通用 Python 解释器 |

旧 model_manager 查询/比较/导图动作会返回 moved_to，须改入口而非重试。call_code 仅保留 run_sysplorer_api（兼容 run_script）；submit_job/get_job_result/run_with_ready/dispatch/ready/fast_workflow 已退役。改参未封装为独立工具，先查 `SetModelParamValue` 文档再用 API 脚本。已有专用工具时优先使用，不能为规避其行为而绕道脚本。

### 1.2 失败、重试与工具副作用

- 同时识别 MCP `isError`、业务 `ok:false`、错误对象及 `_meta` 的 `sysplorer/error` / `cc.tongyuan.mogick/toolFailure`；不能假定第一个 text 始终为 JSON。保留 code、failure_stage、reasonCode、retry.mode、hint、官方 upstreamCode 和部分成功项。
- invalid_arguments/class_not_found：修正参数或定向类证据后再试；library_not_installed：查已装清单，不靠等待安装库；library_load_failed/not_ready：先确认安装/会话事实再有界恢复；forbidden：停止该动作；timeout：执行状态未知，先核对状态和已有结果，尤其不原样重复写操作。retry 提示不授权无限重试、重启 GUI 或扩大任务。
- `check_model` / `translate_model` / `simulate_model` 可从 reload_mo_path 或加载缓存找到无 Placement 的用户文件并自动布局、写回、重载；不传路径也不保证无副作用。只读评审/诊断不直接对原件调用它们；验证需用授权副本或报告缺少无写回能力，不能偷偷扩为修复。不要将描述中的“库不改写”扩展为所有商业/自定义库的保证。
- 自动布局失败可记录并继续官方检查，但检查失败仍阻断后续执行。实际图形写回按 Gate 6 纳入目标和 repairs。smart_layout 的 disk_changed、official_route.persisted、layout_writeback_ok、session_persist_ok 分别取证；自动布局不等于图面验收通过，多模型首项预检也不等于全层级已验收。
- 仿真仅需成功时 verify_result_var 留空；要求结果时再给变量，SimulateModel 失败不能用旧结果翻成成功。加载文件/仿真可关闭当前结果集（RemoveResult，必要时 RemoveResults 回退）；它不表示删除磁盘结果文件。数值时刻可能返回插值或端点回退值，需保留 warning 并说明来源。
- readonly 工具提示不等于零会话/文件/UI 副作用：文档可加载库、导出临时 HTML，检索可写索引，绘图可改变窗口。按具体动作与用户授权判断范围。

## 2. 建模形式的不可替代边界

- Modelica 物理模型、物理连接和物理顶层必须使用 `.mo` 文本。
- 普通 Sysblock 拓扑、块图连线和状态机只能使用官方 API 与对应专业 Skill；不得用 `SetModelText` 或文本覆写替代。
- 混合模型先完成并检查 Sysblock 子模型，再通过已识别 SEC/混合边界将其置于 Modelica 物理顶层；不得在普通同层混放物理组件与 Sysblock 基础块。
- 不得以工具插入失败为由，把一个建模形式偷换为另一个建模形式。

## 3. 受保护商业库的证据流程

1. **识别候选类。** 从公开元数据、产品文档、已登记语料、领域 Skill 或已加载类说明中确定完全限定类名和预期功能。
2. **读取类文档。** 按需加载库后使用 `get_lib_model_document`，确认参数、端口、连接器、单位、默认值和限制条件。
3. **补充公开证据。** 使用 `resources_retrieval` 检索已登记语料；只通过公开可见的组件/端口内省补充文档缺口。
4. **最小黑盒验证。** 文档和公开内省仍不足以确认关键接口或行为，且用户授权的验证范围允许时，才建立最小验证模型或短时仿真。计划/只读/文档任务不因证据缺口自动进入建模仿真；说明未确认项。黑盒验证只回答已定义问题，不恢复内部实现。
5. **如实报告缺口。** 记录已确认内容、被拒绝候选、未确认端口/参数、验证范围和剩余风险。

任何商业类都不得解密、反编译、解包、解析源码，或使用模型文本提取获取受保护实现。文档不足不能成为读取源码的理由。

## 4. API 文档空结果回退

调用 `get_api_document` 后，若 `ok=false` 或 `help_text` 为空，不得把空结果解释为 API 不存在，也不得原样重复调用：

1. 已有专用 MCP 工具能完成任务时直接使用，不为查其封装 API 先运行 ListFunctions。仅对确需手写的主 ModelingPy 命令，已知准确名称时通过一次定向 `call_code(mode="run_sysplorer_api")` 显式导入 `mworks.sysplorer`，使用 `getattr`、`Help(name)`、`inspect.signature` 和 `inspect.getdoc` 核验；只有名称本身不确定时才调用 `ListFunctions()` 确认当前运行时的准确命令名。
2. 对 DesignOpt、CADToolbox、SimulinkImporter 等独立工具箱，显式导入对应模块，使用模块自己的 `ListFunctions()` 和 Python `help()`；不要继续用主 ModelingPy 的 `get_api_document` 查询工具箱函数。
3. 对已加载模型库类的参数、端口和说明，改用 `get_lib_model_document`。
4. 仍无文档时，记录已尝试的查询路径和缺口；不得虚构签名、参数或返回值。

## 5. 验证深度与修复边界

调试 Skill 独立触发。读取本文件仅继承与当前物理修改/交付相关的约束，不重新分流或启动完整建模流程；普通 Sysblock 修改遵守框图/信号 Skill。先区分只诊断与修复，再确定用户要求的终端阶段；只诊断不自动授权补丁，已有授权不重复询问。实际变更图形对象仍执行适用 Gate 6，纯日志诊断或纯 C 代码修改不自动触发布局任务。

验证深度、结果适用性和阶段状态只维护在 `workflows/seven-gates-validation.md` 的 Gate 5—7。本文件只补工具副作用与通用修复边界，不另设验证矩阵。

- `check_model`、布局、翻译、仿真和 KPI 是相互独立的事实；任何一个成功都不得推断其他步骤成功。
- 文本写回改变行为后，回到受影响的检查和后续 Gate。仅图形注解写回时重新检查；检查通过后不重复已经成功的翻译或仿真。
- 分开记录基础设施原样重试、同一模型修复假设的尝试和整体任务推进。基础设施按第 1.2 节处理，不消耗模型修复次数；同一假设两轮无新证据或改善时停止该策略，最迟同一局部修复连续三次失败时隔离最小案例并回到公开证据。不为凑次数继续尝试，也不因停止一个假设而结束仍可推进的授权任务。
- 用户验收是验证深度上限。仅要求 check + translate + simulate 时，三者成功后停止运行/结果链；仍需收完的适用 Gate 6、必要图形复检和交付记录按七门闸处理，不读取结果、生成曲线、播放动画或追加 KPI。
- 用户未明确要求结果、KPI、曲线或动画，且验收条件不依赖结果时，结果验证必须标记为 `not_required`，且不得调用结果读取工具。
- 不得为获得工具成功而删除用户要求的拓扑、组件或 KPI；实质性方案变化需要用户确认。
