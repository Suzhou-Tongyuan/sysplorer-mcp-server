# Sysplorer 建模总规则

本文件是 `SKILL.md` 的中文阅读与审核镜像。`SKILL.md` 是唯一运行时权威；本文件不增加独立强制规则，修改运行规则后必须同步更新。

本副本随 **modelica-lite / mols** 覆盖层发布：不含 `sysplorer-mds-docs`；模型库缺失走 `ty-sysplorer-dependency-guard`。

## 使用范围

- 用于具体的 Modelica 物理模型、商业库模型、Modelica 库和 Modelica+Sysblock 混合模型的规划、评审、搭建、修改、仿真、验证与交付。
- 用户明确要求时，为 Modelica 模型、Example/Demo 或测试对象新建或同步更新 `annotation(Documentation(info=...))` 帮助信息。
- 物理 Modelica 顶层与 Sysblock 子模型协同时，负责边界分层、验证阶段和交付证据协调。
- 不用于普通 Sysblock 框图或 StateMachine、Sysblock 信号/通信、纯 API 查询、纯结果读取或无具体制品目标的泛讨论。
- 纯帮助问答走本地 `resources_retrieval`、类文档与 API 文档；本包无 MDS 帮助中心 Skill。
- 第一阶段不为 Sysblock 生成本文档体系；普通建模不得自动触发、询问或推荐文档生成。

## 意图与分流

| 意图 | 处理方式 |
|---|---|
| 计划 | 输出范围、路径、证据和验收条件；新系统未获明确执行指令前不创建、检查、翻译或仿真。 |
| 评审 | 只检查用户指定材料，不擅自修改、建模或仿真。 |
| 修改/搭建、执行/验证、交付 | 按选定路径执行，并以用户要求的交付深度完成相应验证。 |

| 请求类型 | 责任 Skill 或工具 |
|---|---|
| 普通 Sysblock 图或 StateMachine | `ty-sysblock-diagram-modeling` |
| Sysblock 信号或通信 | `ty-sysblock-signal-modeling` |
| 明确要求为 Modelica 模型/案例/测试对象生成或同步帮助信息 | 本 Skill 的 Documentation 路径；第一阶段不适用于 Sysblock |
| Modelica 物理、商业领域、模型库或物理顶层混合模型 | `ty-sysplorer-modeling-rules` |
| 模型库包结构、示例、测试、本地化或库评审 | 在本 Skill 分流后附加 `modelica-library-workflow` |
| `load_library` 失败 / 模型库未安装 | 附加 `ty-sysplorer-dependency-guard` |

## 最小读取

所有 `references/...` 与 `workflows/...` 路径相对于本 Skill 目录。

| 需求 | 读取 |
|---|---|
| 工具、会话、路径、商业库证据和验证范围 | `references/shared-standards.md` |
| 帮助问答与文档降级 | `references/documentation-routing.md` |
| 显式 Modelica Documentation 任务 | `references/modelica-documentation-rules.md`、`workflows/modelica-documentation.md`，再按场景只读取 `templates/documentation/model-help-template.md`、`case-help-template.md` 或 `test-case-template.md` 中选中的一个 |
| 物理/混合/领域歧义 | `references/modeling-path-router.md` |
| Modelica 文本与图形语义 | `references/modelica-style-guide.md`、`references/modelica-diagram-connect-semantics.md` |
| Modelica 工作流、混合边界、七门闸 | `workflows/modelica-modeling.md`、`workflows/hybrid-modeling.md`、`workflows/seven-gates-validation.md` |

## 核心约束

- Modelica 物理模型使用 `.mo` 文本；Sysblock 子模型使用官方 API；混合模型保持 Sysblock 子模型与 Modelica 物理顶层分层。
- 使用 Agent CWD 管理项目产物；禁止 `ClearAll` 和 `ChangeDirectory`。附着用户 GUI 前先 `probe`（若可用）再 `health`，不得关闭或重启该 GUI 会话。
- 商业库一律按受保护依赖处理，只使用类文档、登记语料、公开内省和最小黑盒验证，不检查源码。
- modelica_lite 上 `run_sysplorer_api` 固定进程内执行，不查找 `External\python64`。
- `load_library` 返回 `ok: false` / 静默 False 时先 `plan` 再（门控打开时）真实 `prepare`。
- 图形交付对象在成功检查后、翻译/长仿真/交付前完成适用的 Gate 6。记录 `layout.applicability`、`layout.scope`、`layout.annotations_checked`、`layout.diagram_reviewed`、`layout.rechecked_after_writeback`、`layout.ok` 和证据。
- 未指定版本时，Modelica 标准库依赖使用 `Modelica(version = "4.0.0.TY.1")`。

## Documentation 隔离规则

- 只有用户明确要求生成、编写、更新或同步 Modelica 帮助信息时才进入 Documentation 路径。
- 开发 + 文档组合任务先完成原建模流程及所需验证，再串行执行 `workflows/modelica-documentation.md`；文档步骤不插入或改变原开发流程。
- 独立文档任务只读取当前 `.mo`，并只修改 `Documentation(info=...)`；仅在用户明确要求时另行导出 Markdown。
- 不为使说明成立而修改模型行为，不执行测试，不生成测试报告，不推断 PASS/FAIL。
- 文档或图片失败只影响文档状态，不否定已经成功的建模结果。
- 三套内置默认模板均采用 `modelica-documentation-v1` 统一格式并标记为 `ready`；只读取当前场景对应的一份模板，并仅从其输出区间生成成品。
