# Sysblock 信号与通信建模

本文件是 `SKILL.md` 的中文阅读版。只有当 `ty-sysplorer-modeling-rules` 将任务分流到 Sysblock 路径后，才使用本 skill。父级 skill 负责会话健康、分流、七门闸、布局时机、修复闭环和交付证据。

## 范围

- 信号处理：滤波、频谱检查、多速率处理、特征提取。
- 通信链路：基带链路、BER、QPSK/QAM、同步、DSSS。
- 相关库：`TYDSPSystem`、`TYCommunication`、`TYMixedSignal`、`SysplorerEmbeddedCoder`。

不用于 Modelica 物理模型、纯 API 查询，或不需要信号领域工作流指导的孤立块参数/端口核对。

## Sysblock 硬规则

- 建模前必须先执行父级分流，不得覆盖父级判断。
- 通过 `call_code(mode="run_sysplorer_api")` 使用官方 Sysplorer API。
- 禁止 `SetModelText`、手写 `.mo` 或文本补丁构建 Sysblock 拓扑。
- 不得把 Modelica 物理库混入 Sysblock 信号路径。
- 先加载 `SysplorerEmbeddedCoder`；只有明确源块类别后才查询具体源块。

## 最小读取

本文与对应 `SKILL.md` 中所有 `references/...` 路径均相对于**本 skill 目录**（包含 `SKILL.md` 的文件夹），不是工作区根目录，也不是上层 `skills/` 目录。

| 需求 | 读取 |
|---|---|
| 总览/读取顺序 | `references/workflow-overview.md` |
| 模板与层级选择 | `references/template-selector.md` |
| 建模方法 | `references/modeling-methods.md` |
| 选定 playbook | `references/playbooks.md` |
| 参数/可观测性 | `references/parameter-contracts.md` |
| 检查点/证据 | `references/execution-checkpoints.md` |
| 排障/降级 | `references/troubleshooting-and-fallback.md` |
| 具体块文档 | 通过 MCP 读取 `sysblock_model_library` |

## 领域增量

- 设计前先分类任务：滤波、频谱、多速率、特征提取、通信链路、BER、同步或混合信号。
- 先构建最小可运行信号链，再扩展场景。
- 提前定义可观测性：所需输出变量、频谱、BER、同步状态或时序指标。
- `run_sysplorer_api` 成功只表示脚本执行成功；模型有效性仍以父级 `check_model` 为准。
- 若最小闭环能运行但用户指标未满足，回到父级优化循环。

## 交付增量

在父级交付证据基础上补充：

- 任务类别、使用的模板/playbook、库范围、关键参数、观测变量、验证结论和未解决风险。
