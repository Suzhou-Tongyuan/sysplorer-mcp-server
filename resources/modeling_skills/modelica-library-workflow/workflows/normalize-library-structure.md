---
description: 整理 Modelica 模型库的 package 分层、归位规则和业务包命名
---

# 整理模型库结构

## 适用场景

用户希望把已有库从“能用但混乱”整理成“结构清晰、可扩展、可交付”的状态。

## 步骤

1. 复用 `references/shared-standards.md`，确定允许调整的结构、兼容边界和请求终点。
2. 先保留现有有效顶层结构和接口；仅明确采用模板时读 `references/template-package-scheme.md` 并应用其固定层次。
3. 修复实际存在的包归位、路径引用及 `package.order` 一致性，不为对齐模板迁移所有原生接口或增建空包。
4. 本轮需要时同步受影响的 Examples / Tests 与既有说明链接；未请求不额外生成文档或示例。
5. 对照 `references/workflow-checklist.md` 相关章节做静态检查；工具验证按 `references/executor-base.md` 的请求终点执行。
6. 按验收清单报告文件/结构证据，明确未运行与范围外事项。

## 模板优先级

优先级从高到低：

1. 现有顶层结构中可保留的部分
2. 模板包结构方案
3. 通用 package 骨架模板

## 输出重点

1. 哪些内容被迁移或归位
2. 哪些包名被正式化
3. 哪些 `package.order` 被补齐或需要补齐
4. 结构整理后还缺什么
