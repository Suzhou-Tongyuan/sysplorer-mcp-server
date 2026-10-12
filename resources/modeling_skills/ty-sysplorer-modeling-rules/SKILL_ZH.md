# Sysplorer 建模总规则

本文件是 `SKILL.md` 的中文阅读与审核镜像。`SKILL.md` 是唯一运行时权威；本文件不增加独立强制规则，修改运行规则后必须同步更新。

## 使用范围

- 用于具体的 Modelica 物理模型、商业库模型、Modelica 库和 Modelica+Sysblock 混合模型的规划、评审、搭建、修改、仿真、验证与交付。
- 用户明确要求时，为 Modelica 模型、Example/Demo 或测试对象新建或同步更新 `annotation(Documentation(info=...))` 帮助信息。
- 物理 Modelica 顶层与 Sysblock 子模型协同时，负责边界分层、验证阶段和交付证据协调。
- 不用于普通 Sysblock 框图或 StateMachine、Sysblock 信号/通信、纯 API 查询、纯结果读取或无具体制品目标的泛讨论。
- 纯帮助问答优先由 `sysplorer-mds-docs` 完成；仅当其失败时进入文档检索、降级与总结路径。
- 第一阶段不为 Sysblock 生成本文档体系；普通建模不得自动触发、询问或推荐文档生成。

## 意图与分流

| 意图 | 处理方式 |
|---|---|
| 计划 | 输出范围、路径、证据和验收条件；仅计划型请求在计划后停止。用户已明确要求搭建、执行、检查、翻译或仿真时，视为已授权对应范围内的动作。 |
| 评审 | 只检查用户指定材料，不擅自修改、建模或仿真。 |
| 修改/搭建、执行/验证、交付 | 按选定路径执行，并以用户要求的交付深度完成相应验证。 |

| 请求类型 | 责任 Skill 或工具 |
|---|---|
| 普通 Sysblock 图或 StateMachine | `ty-sysblock-diagram-modeling` |
| Sysblock 信号或通信 | `ty-sysblock-signal-modeling` |
| 明确要求为 Modelica 模型/案例/测试对象生成或同步帮助信息 | 本 Skill 的 Documentation 路径；第一阶段不适用于 Sysblock |
| Modelica 物理、商业领域、模型库或物理顶层混合模型 | `ty-sysplorer-modeling-rules` |
| 库级包结构、公共接口、Examples/Tests 组织、本地化或库评审（单模型/单个测试台不自动追加） | 在本 Skill 分流后附加 `modelica-library-workflow` |

## 独立调试入口

已有模型的具体故障或异常结果由调试 Skill 主导：明确 Modelica 故障直接使用 `ty-physical-model-debugging`；明确 Sysblock 故障直接使用 `ty-sysblock-model-debugging`；未知或混合故障使用 `ty-sysplorer-debugging`。它们不必先经过本 Skill。

调试在物理模型修改或交付时按需引用本 Skill，读取后回到当前调试步骤，不再次分流、重新规划、重复创建副本或复现。普通 Sysblock 使用框图/信号 Skill 的约束。新建过程中发生故障时保留原任务及工作模型，按需诊断修复后继续；仅出现“失败”不改变原任务归属。只读诊断不触发图形交付，实际变更图形对象仍需适用 Gate 6。

## 最小读取

所有 `references/...` 与 `workflows/...` 路径相对于本 Skill 目录。

| 需求 | 读取 |
|---|---|
| 工具、会话、路径、商业库证据和验证范围 | `references/shared-standards.md` |
| 帮助问答与 MDS 失败降级 | `references/documentation-routing.md` |
| 跨领域分流、库名别名和版本信息 | `references/domain-routing-and-library-versions.md` |
| 显式 Modelica Documentation 任务 | `references/modelica-documentation-rules.md`、`workflows/modelica-documentation.md`，再按场景只读取 `templates/documentation/model-help-template.md`、`case-help-template.md` 或 `test-case-template.md` 中选中的一个 |
| 物理/混合/领域歧义 | `references/modeling-path-router.md` |
| Modelica 文本与图形语义 | `references/modelica-style-guide.md`、`references/modelica-diagram-connect-semantics.md` |
| Modelica 工作流、混合边界、七门闸 | `workflows/modelica-modeling.md`、`workflows/hybrid-modeling.md`、`workflows/seven-gates-validation.md` |

## 核心约束

- Modelica 物理模型使用 `.mo` 文本；Sysblock 子模型使用官方 API；混合模型保持 Sysblock 子模型与 Modelica 物理顶层分层。
- 使用 Agent CWD 管理项目产物；禁止 `ClearAll` 和 `ChangeDirectory`。离线检查不调用会话工具；首次实时访问通过 Sysplorer MCP 确认目标，先 `probe`（若可用）再 `health`。复用同一有效会话证据，切换、断连或基础设施异常后重查，不得关闭或重启用户 GUI 会话。
- MCP 0.4 分类/参数、starting 状态、结构化错误、重试和副作用均引用 `references/shared-standards.md`。查询用 model_inspect，比较用 compare_model，导图用文档确认后的 API 脚本；不调用退役入口。检查/翻译/仿真可自动写布局，不能当纯读诊断。实际图形变更按 Gate 6 验收，结构化证据为基础，图片按用户需求和能力使用。
- 商业库一律按受保护依赖处理，只使用类文档、登记语料、公开内省和最小黑盒验证，不检查源码。
- 复用有效库边界；未指定时标准库满足则使用，不足时保留可用部分并补充有公开证据的商业组件。查询失败不是功能不足。领域白名单约束其子系统，不删除已选支持域/标准库组件；车辆入口/实现路径、电气/NPS 专项路由保持原样。
- 每个本次新建或修改的图形对象都执行完整 Gate 6，并在最终图形交付前完成。纯视觉布局问题不阻止翻译或仿真；只有模型检查发现的图形注解语法或结构错误才阻止执行。Gate 6 只记录 `layout.status`、`layout.level`、`layout.targets`、`layout.checks` 和证据，布局修复写入统一的 `repairs`。
- 车辆全部既有路径及商业库路径绑定 `Modelica 4.0.0.TY.1`；仅主规则单独使用且不涉及车辆/商业库时，默认该版本并允许用户/工程有效版本覆盖。冲突不静默改依赖。
- 用户验收是验证深度上限。验收仅要求 check + translate + simulate 时，三项成功后停止运行/结果链；只收完尚未完成的适用 Gate 6、必要图形复检与交付证据，不追加结果变量、曲线、KPI、绘图或动画。
- 用户未要求结果证据，且验收条件不依赖结果时，将结果/KPI 验证标记为 `not_required`。仿真成功可以满足“仅仿真成功”的验收合同，但不得声称检查了未要求的 KPI。
- 只有已选定 TY/同元商业机械库边界时才加载 `ty-mechanical-modeling`；纯 Modelica 标准库、自建或其他非 TY 机械/多体任务禁止加载该 skill。

## Documentation 隔离规则

- 只有用户明确要求生成、编写、更新或同步 Modelica 帮助信息时才进入 Documentation 路径。
- 开发 + 文档组合任务先完成原建模流程及所需验证，再串行执行 `workflows/modelica-documentation.md`；文档步骤不插入或改变原开发流程。
- 独立文档任务只读取当前 `.mo`，并只修改 `Documentation(info=...)`；仅在用户明确要求时另行导出 Markdown。
- 不为使说明成立而修改模型行为，不执行测试，不生成测试报告，不推断 PASS/FAIL。
- 文档或图片失败只影响文档状态，不否定已经成功的建模结果。
- 三套内置默认模板均采用 `modelica-documentation-v1` 统一格式并标记为 `ready`；只读取当前场景对应的一份模板，并仅从其输出区间生成成品。
