# Sysblock 框图建模（中文导览）

本文件是 `SKILL.md` 的中文导览，不复制详细算法。发生差异时以 `SKILL.md` 和其直接引用的权威文档为准。

## 核心流程

1. 普通 Sysblock 直接使用本 Skill；已有模型的具体故障由 `ty-sysblock-model-debugging` 主导，并复用本 Skill 的接口、布局、保存/重载和审计约束。作为约束加载时不再次分流或复现；新建过程中发生故障保留原任务上下文。
2. 冻结边界、语义、端口、类型、维度、采样时间和验证需求。
3. 用 `scripts/api_contract_resolver.py` 解析本次真正使用的准确 API 名称：已知契约零探针；未知签名只精确查询一次；文档仍不能确定行为时，才在一次性任务自有模型中探针一次。禁止在目标模型探针或默认全量枚举。
4. 拓扑/布局变更先生成无几何输入，再用 `layout_input_tool.py` 审计，之后用 `layout_plan_tool.py block|statechart` 规划。
5. 仅用官方 API 添加组件、设置参数和 `ConnectPort` 连线；检查每个有返回值的调用。
6. 保存并强制重载最终目标，执行总规则要求的检查、测试、布局复核和交付验证。
7. 用 `audit_sysblock_model.py` 审计保存模型及原始结构化证据；退出码为 0 只代表该审计通过，全部总规则验证成功后才能宣称完成。

## 状态机布局硬规则

普通转移必须为两点水平线或竖直线。布线前检查源、目标状态框的 x/y 投影重叠；重叠不足时必须按“平移 → 有界缩放 → 推移受影响邻居 → 重算”的顺序调整状态框，不能反复尝试角点连接。无法在边界内满足时返回结构性失败并重新考虑层级或业务拓扑。

## 权威资料

- API、返回值、生命周期：`references/runtime-contracts.md`
- 建模与交付顺序：`references/modeling-workflow.md`
- 布局算法和审计：`references/layout-workflow.md`
- StateMachine 语义和 API：`references/state-machine.md`
- 模块与参数：`references/block-reference.md`
- 故障索引：`references/troubleshooting.md`
- 仅在明确验证 skill 修订有效性时使用：`references/layout-evaluation.md`

详细英文规则只维护一份；本导览用于快速导航，避免中英文规则漂移。
