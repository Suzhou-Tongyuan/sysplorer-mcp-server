> 中文阅读与审核镜像；`SKILL.md` 是唯一执行入口。本文件不增加独立规则。

# Sysplorer 调试总入口

只在已有模型故障域未知、混合或产品级故障需要协调时触发；普通新建、编辑、布局、整定和纯 API 帮助不触发。本入口负责最小识别、上下文交接和结论汇总，专业 Skill 执行修复循环，不重复执行完整诊断修复链。

| 证据 | 目标 |
|---|---|
| Modelica 方程、初始化、运行、外部函数或 Modelica 翻译后的构建故障 | `ty-physical-model-debugging` |
| 已确认 Sysblock、块/端口、CCaller 或 Sysblock 代码生成后的构建故障 | `ty-sysblock-model-debugging` |
| 只知道生成求解器失败 | 先确认 restriction 与产生求解器的流水线，不仅凭名称分流 |
| 混合模型 | 跟随证据指向的层级，复用有效子模型证据，跨边界时再验证接口 |

不预加载两个专业 Skill 的全部资料；顶层已定位的故障不要求重跑全部子模型。交接任务模式、模型身份、可用会话、首错、终端验收、基线、工作副本与检查点，未知项保持未知。

物理修改/交付按需引用主 Skill；普通 Sysblock 修改引用框图/信号 Skill；只读诊断不触发布局。错误帮助使用 `references/help-doc-index.md` 和 `scripts/query_sysplorer_help.py`，区分产品诊断号与编译器退出码。公开组件语义使用 `get_lib_model_document`，本地帮助不可用或无匹配后回退 `resources_retrieval`。日志仅报告可归属本轮操作的证据，不承诺未获得的完整首错。

具体调用需要时读 `references/current-mcp-recipes.md`；外部 C 故障按需读 `references/external-c-debugging.md`；有锚点的大文件证据使用 `scripts/extract_debug_evidence.py`。

## 任务模式与共用边界

- 入口独立触发，不要求先经过建模主入口或调试总入口。明确领域时直接使用专业调试 Skill。
- 根据请求区分 `diagnose_only` 与 `repair`。只解释/定位问题不授权补丁；仅在请求允许时复现，明确离线审查不执行模型。证据不足如实报告，不将假设称为已解决。
- 记录用户要求的终端阶段及验收条件，复用可归属当前模型和设置的基线、会话、工作副本与检查点。引用其他 Skill 的约束后返回当前步骤，不再次分流、重规划或重复复现。新建过程中的故障处理完后继续原建模任务。
- 离线模型/日志读取不调用会话工具。首次实时访问经 Sysplorer MCP 确认目标，支持时先 `probe` 再 `health`；同一有效会话可复用，切换、断连或基础设施异常后重查。所有 ModelingPy 调用只经 MCP，本地辅助脚本只处理文件。
- 当前已知 API 契约直接复用；未知名称、参数和返回类型在调用前定向确认，文档为空按准确名称查询 Help/签名或对应工具箱文档。不得猜测写入、在目标模型试探未知写接口或全量枚举 API。
- 保护原模型、原 C 源码和未保存 GUI 状态，修复只写已核验的任务自有副本。不用 `extends Original` 冒充副本，不修改生成代码或受保护商业库源码，不以删除断言或扫求解参数掩盖缺陷。
- 现有明确授权继续有效；新增实质性设计或范围变化才请求用户判断。同一假设两轮无改善后停止该策略，转入有用的定向证据或最小案例；相同基础设施操作失败两次后停止重复重试，报告缺口，不为凑次数继续猜测。

## 按范围验收与报告

详细状态见 `references/report-contract.md`。只诊断有充分证据时用 `diagnosis_complete`，说明根因已确认还是仍为假设，不宣称修复。证据不足用 `verification_required`。

修复必须有补丁读回、所需静态及终端阶段通过、原件保护和临时设置恢复。静态/链接验收不自动要求仿真或 stopTime；运行验收达到约定原终点；只有用户要求或异常结果所必需时才读取结果和核验 KPI，否则标记 `not_required`。实际变更图形对象仍完成对应建模交付检查。范围内验证通过用 `verified_solved`；有可重复改善但未完成用 `partially_improved`；必要证据缺失用 `verification_required`；无可继续的授权/能力路径用 `automatic_debugging_stopped`。
