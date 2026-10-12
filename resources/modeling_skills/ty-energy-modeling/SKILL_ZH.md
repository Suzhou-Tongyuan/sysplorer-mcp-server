# TY 能源系统建模

本文件是 `SKILL.md` 的中文阅读版。本 skill 只能作为 `ty-sysplorer-modeling-rules` 之后的领域薄补丁使用；父级 skill 负责分流、关卡纪律、布局时机、修复闭环和交付证据。

## 父规则与 MCP 0.4

会话复用、工具分类、错误解析及重试统一引用 `../ty-sysplorer-modeling-rules/references/shared-standards.md`；验证深度、Gate 6 与完成状态引用 `../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md`。离线/源码任务不调用会话。已有具体故障由父规则规定的独立调试入口主导，本领域只提供定向证据，不重启完整建模；新建中的失败保留原任务。

执行到用户要求的终端阶段即停止。结果变量、KPI、曲线、动画和正式文档仅在用户要求或约定验收标准确需时执行，否则标记 `not_required`；不得为填表自动推定 proxy 指标。仿真成功与物理结果达标分别表述。

MCP 0.4 的类、组件、端口与文本查询使用 `model_inspect`，比较使用 `compare_model`，生命周期操作使用 `model_manager`。`call_code` 仅接受 `run_sysplorer_api` 或兼容别名 `run_script`，必须传对象 `payload` 并显式导入 ModelingPy。检查/翻译/仿真即使未传 `reload_mo_path`，也可能对已加载用户文件自动布局写回，不能作为无写入的只读评审工具；遵守父级授权边界，并把实际图形改动纳入 Gate 6。

## 最小读取

本文与对应 `SKILL.md` 中所有 `references/...`、`workflows/...` 路径均相对于**本 skill 目录**（包含 `SKILL.md` 的文件夹），不是工作区根目录，也不是上层 `skills/` 目录。

| 需求 | 读取 |
|---|---|
| 输入/契约 | `references/standard-input-checklist.md`、`references/input-output-contract.md` |
| 领域规则 | `references/energy-domain-rules.md` |
| 组件选型 | `references/component-mapping.md` |
| 典型场景 | `references/energy-typical-scenarios.md` |
| 修复 | `references/error-repair-playbook.md` |
| 验收 | `references/acceptance-checklist.md` |
| 工具映射 | 工具选择不清时读 `references/mcp-modeling-toolkit.md` |
| 资源导航 | `references/resource-map.md` |
| 手册查询 | 仅在精简参考不足时读取 `references/manual-index.md` |

## 专项流程

- 场景建模：`workflows/build-from-scenario.md`
- 修复已有失败模型：`workflows/repair-existing-model.md`
- 手册/样例核验：`workflows/verify-example.md`

## 领域增量

用户明确指定或父规则/有效上下文已选能源商业组件后使用本领域；未指定库先评估标准库能力，满足则标准库，不足则保留可用标准库并补充商业组件。场景词本身不决定商业选型。

- 能源子系统使用光伏发电库、风力发电库、电池库、综合能源系统库及 `Modelica 4.0.0.TY.1`；该白名单不约束整个交付物，保留父规则已选标准库与支持领域组件。商业路径固定 Modelica 为 `4.0.0.TY.1`，工程版本冲突时报告，不静默改写。
- 保留用户指定的拓扑、关键组件和明确参数目标，除非已证明不兼容且得到用户认可。
- 先映射主能量路径，再映射控制链，最后补经济性、调度或辅助子系统。
- 保留父规则已选、能力满足的标准库组件；仅针对已确认的能源功能缺口选择接口兼容的 TY 领域类，不因有商业示例而整体替换标准库。
- 图形化建模需保持组件摆放和连线可在 Sysplorer GUI 中编辑、审阅；可行时优先用 Sysplorer 原生方式生成连接与图面。
- 先用保守的仿真设置完成 bring-up，再逐步扩展时长、求解器激进程度或优化范围。
- 验证功能正确性、趋势合理性、数值可接受性以及与用户目标的一致性。
- 需要查手册时，先读精简 references，再按需打开已复制的能源库手册原文。

## 修复优先级

以下为诊断定位顺序，仅在本次请求终态内使用，不要求运行全部后续阶段：

`session/tool readiness -> allowed-library/class scope -> boundary/source completeness -> connection topology -> interface compatibility -> parameter/unit consistency -> CheckModel -> TranslateModel -> simulation stability -> result interpretation`

不得为了通过检查或翻译而跳出父级确认的能源子系统库范围，且必须保留其他已选子系统库；不得仅为消除报错而删除必需的能源源端、储能、变换器、负载、边界条件或观测量。

## 交付增量

在父级交付证据基础上补充：

- 模型结构、组件映射、库使用记录、参数摘要、关键假设、图面审阅、仿真设置、已验证变量、验收判定和限制。
- 默认只保存一个最终模型或明确一个最终模型名/路径；只有用户明确要求时才生成额外打包报告。
