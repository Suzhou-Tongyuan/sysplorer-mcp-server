# 工作流总览

## 用途

本文件用于给主 skill 提供轻量化工作流入口。
它只维护引用顺序、职责分工与最小流程，不重复展开模板、契约、检查点和排障细节。

## 引用顺序

路径约定：同 skill 内文件相对本 skill 的 `references/`；父 skill 文件相对其自身目录 `ty-sysplorer-modeling-rules/`（含 `SKILL.md`），不是工作区根目录，也不是 `modeling_skills/` 打包前缀。

1. `modeling_rules`（父 skill 语料：`ty-sysplorer-modeling-rules/references/`）
2. `ty-sysplorer-modeling-rules/references/sysblock_style_guide.md`
3. `workflow-overview.md`
4. `template-selector.md`
5. `modeling-methods.md`
6. `playbooks.md`
7. `parameter-contracts.md`
8. `execution-checkpoints.md`
9. `troubleshooting-and-fallback.md`
10. `sysblock_model_library`

## 职责分工

- `template-selector.md`
  负责任务归类、模板映射与层级入口
- `modeling-methods.md`
  负责通用建模骨架、能力分层与四层说明
- `playbooks.md`
  负责已选模板的 A/B/C/D/F0/F1 细化
- `parameter-contracts.md`
  负责参数契约与可观测性
- `execution-checkpoints.md`
  负责检查点、门禁、证据打包与 KPI 口径
- `troubleshooting-and-fallback.md`
  负责失败分类、排障顺序与回退

## 最小流程

1. 先判定是否属于 Sysblock 路径
2. 若进入程序化建模，先服从 `sysblock_style_guide.md`（mcp 工具中的文件）
3. 先用 `template-selector.md` 完成任务归类、模板选择与层级选择
4. 再用 `playbooks.md` 展开已选模板
5. 组织四层方案与通用骨架
6. 审核参数契约与可观测性
7. 推进 `check_model -> simulate_model -> result_manager`
8. 结合 `execution-checkpoints.md` 做 KPI / 证据判定
9. 若失败，进入排障与回退
