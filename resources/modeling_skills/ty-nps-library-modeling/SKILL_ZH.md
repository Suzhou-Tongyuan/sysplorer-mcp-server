# TY NPSLibrary 建模

本文件是 `SKILL.md` 的中文阅读版。本 skill 只能作为 `ty-sysplorer-modeling-rules` 之后的领域薄补丁使用；父级 skill 负责分流、七门闸、布局时机、修复闭环和交付证据。

## 最小读取

本文与对应 `SKILL.md` 中所有 `references/...`、`workflows/...` 路径均相对于**本 skill 目录**（包含 `SKILL.md` 的文件夹），不是工作区根目录，也不是上层 `skills/` 目录。

| 需求 | 读取 |
|---|---|
| 输入/契约 | `references/standard-input-checklist.md`, `references/input-output-contract.md` |
| 领域规则 | `references/nps-domain-rules.md` |
| 组件映射 | `references/component-mapping.md` |
| 典型场景 | `references/nps-typical-scenarios.md` |
| 修复 | `references/error-repair-playbook.md`，再读 `references/nps-common-errors.md` |
| 验收 | `references/acceptance-checklist.md` |
| 工具映射 | 工具选择不清时读 `references/mcp-modeling-toolkit.md` |
| 手册查询 | 仅在精简参考不足时读取 `references/manual-index.md` |

## 专项流程

- 场景建模：`workflows/build-from-scenario.md`
- 样例/环境验证：`workflows/verify-example.md`
- 修复已有失败模型：`workflows/repair-existing-model.md`

## 领域增量

- 默认保持在 `NPSLibrary` 内。
- 保留用户指定的拓扑和关键组件，除非已证明不兼容且得到用户认可。
- 先映射主功率路径，再映射控制链；按需补充 `Ground / Reference / Powergui / Sensors / Boundary / Result probes`。
- 潮流任务需检查 `LoadFlowBus`、平衡/PV/PQ 母线定义和 `Powergui` 潮流初始化。
- 图形化建模需保持组件摆放和连线可在 GUI 中编辑、审阅；若 GUI 侧 `call_code` 失败，先修复调用路径。
- 开关/PWM/PLL 主导模型默认优先离散基线，场景另有要求除外；无更强规则时使用 `step <= T/10`。
- 验证功能正确性、趋势合理性、数值可接受性和工程/参考预期。

## 修复优先级

优先沿最短阻塞链排查：

`GUI/call_code invocation -> grounding/reference -> connection completeness -> interface compatibility -> Powergui/load-flow -> initialization -> parameters -> translation -> simulation -> result interpretation`

不得为了通过翻译而删除传感器、电源、变换器、接地或用户要求的子系统。

## 交付增量

在父级交付证据基础上补充：

- 模型结构、组件映射、参数摘要、关键假设、图面审阅、仿真设置、已验证变量和限制。
- 默认只保存一个最终模型文件；只有用户明确要求时才生成打包报告。
