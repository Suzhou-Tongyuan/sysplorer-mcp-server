# Modelica 库工作流

本文件是 `SKILL.md` 的中文阅读版。使用本 skill 前必须先应用 `ty-sysplorer-modeling-rules`；父级 skill 负责分流、七门闸、布局时机、修复闭环和交付证据。本 skill 只补充 Modelica 库/包级工作流规则。

## 使用范围

- 仅用于 Modelica 库的包结构、公共接口、Examples / Tests、库级本地化和治理；普通单模型建模、修复、评审和导图由父级与领域 Skill 负责。
- 在上述库级目标内按需采用模板、已有骨架、库级图面或本地化工作流。已有具体故障由父级调试入口主导；新建中的失败保留原任务。
- 不用于纯理论讨论、纯 API 查询，或没有具体制品目标的宽泛讨论。

## 最小读取

先读取 `references/shared-standards.md` 的父级衔接，再选择一个工作流及所需章节；不顺序加载全部资料。资料权威与按需读取见 `references/reference-role-map.md`。

本文与对应 `SKILL.md` 中所有 `references/...`、`workflows/...` 路径均相对于**本 skill 目录**（包含 `SKILL.md` 的文件夹），不是工作区根目录，也不是上层 `skills/` 目录。

| 需求 | 读取 |
|---|---|
| 任务分类 | `references/requirement-mapper.md` |
| 模板/顶层包设计 | `references/template-package-scheme.md` |
| 跨领域业务包命名 | `references/cross-domain-business-package-strategy.md` |
| 请求终端阶段与执行 | `references/executor-base.md` |
| 静态检查/常见错误 | `references/workflow-checklist.md`, `references/common-errors.md` |
| 验收/交付 | `references/acceptance-checklist.md`, `references/input-output-contract.md` |

## 专项流程

| 流程 | 路径 |
|---|---|
| 基于模板建库 | `workflows/build-from-template.md` |
| 库与已请求示例验证 | `workflows/build-library-with-example-validation.md` |
| 扩展已有库 | `workflows/extend-existing-library.md` |
| 评审已有库 | `workflows/review-existing-library.md` |
| 规范化库结构 | `workflows/normalize-library-structure.md` |
| 中文本地化 | `workflows/chinese-localization.md` |
| 修复图解注解 | `workflows/repair-diagram-annotations.md` |

## 领域增量

- 保持 `package.mo` 与 `package.order` 同步。
- 固定公共层、接口本地包装、命名和排序仅在实际采用模板时按 `references/template-package-scheme.md` 执行；其他工程保留兼容原生接口和既有结构。
- 区分 `Examples` 和 `Tests`：示例展示用法，测试验证行为。
- 不把官方示例改名后直接作为交付物；只能作为参考或验证基线。
- 图解相关任务仍由父级 Gate 6 决定触发、证据和复检要求；MCP 检查可能自动布局写回，不能当作纯读取。
- 骨架/文件任务做到请求的静态终点，不默认加载或仿真；要求可运行时才收集真实运行证据，结果分析按请求执行。
- 会话、分类重试和 MCP 0.4 调用契约引用父级权威资料，不另定固定重试次数。

## 交付增量

在父级交付证据基础上补充：

- 完成层级：`plan-complete`、`files-modified`、`structure-level-verified` 或 `run-level-verified`。
- 包结构决策、公共层决策、本地化范围、图面状态、验证深度和剩余风险。
- 完成判定统一见 `references/acceptance-checklist.md`。报告模板仅在用户请求时生成成套文档；package 骨架仍可用于已授权建库。验证项复用父级状态：范围外为 `not_required`，已要求但未执行为 `blocked` 并说明原因，已执行按 `passed` / `failed` 记录。
