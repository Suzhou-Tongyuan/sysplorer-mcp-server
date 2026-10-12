---
description: 扩展现有 Modelica 模型库的业务包、组件族、样例或测试入口
---

# 扩展已有模型库

## 适用场景

用户已经有一个模型库，但希望继续补组件族、细分子包、增加 `Examples`、增加 `Tests`，或把临时结构扩成可持续维护的正式结构。

## 步骤

1. 复用 `references/shared-standards.md`，按 `references/executor-base.md` 确定新增对象和终端阶段。
2. 检查现有分层、接口、引用及可扩展位置；只有实际采用模板时才读 `references/template-package-scheme.md`。
3. 确定新增业务包、子包或组件的归位，保留现有兼容接口；跨域包设计有需要时再读角色映射资料。
4. 按影响范围同步必要 `package.order`、引用及已请求的 Examples / Tests；维护必要类说明，不自动生成正式文档。
5. 用 `references/workflow-checklist.md` 的相关章节静态自检；真实验证按请求执行到终点。
6. 按 `references/acceptance-checklist.md` 和 `references/input-output-contract.md` 交付真实完成层级。

## 模板优先级

优先级从高到低：

1. 现有库中已验证的同类业务包结构
2. 模板包结构方案
3. 通用 business package 骨架模板

## 输出重点

1. 新增内容应该放在哪一层
2. 是否需要新增 `Basics`、`Examples`、`Tests`
3. 是否需要同步整理 `Interfaces`、`Utilities` 或 `package.order`
4. 扩展后对现有结构的影响
