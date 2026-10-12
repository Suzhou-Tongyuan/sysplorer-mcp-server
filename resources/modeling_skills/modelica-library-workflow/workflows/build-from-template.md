---
description: 基于模板或顶层骨架从 0 到 1 搭建 Modelica 模型库
---

# 从模板建库

## 适用场景

用户给了 `TYComponentsTemplate.mo`、同类模板、顶层骨架目录，或者明确要求“按流程建一个模型库”。

## 步骤

1. 复用 `references/shared-standards.md`，先确定本轮终点是方案、骨架/文件、结构还是可运行交付；分类不明时才读 `references/requirement-mapper.md`。
2. 仅对采用的模板读取 `references/template-package-scheme.md`；按 `references/executor-base.md` 选择适用步骤。
3. 固定顶层 package、正式库名与首批粒度，建立需要的公共层和业务包。
4. 骨架任务只生成约定结构和入口；请求可运行库时再建立首个 Examples / Tests 最小闭环。
5. 对照 `references/workflow-checklist.md` 的相关章节完成静态检查。
6. 明确要求真实示例/测试验证时转 `workflows/build-library-with-example-validation.md`，否则在本轮终点收口。
7. 按 `references/acceptance-checklist.md` 判断实际完成层级，用 `references/input-output-contract.md` 表达证据。

## 模板优先级

优先级从高到低：

1. 用户提供的模板 `.mo`
2. 已验证的顶层 package 骨架
3. 通用模板结构方案
4. 从零自由设计

## 停止条件

本轮实际需要的库名、目录/引用或接口设计未稳定时，先处理相应问题再扩展。骨架任务不以“首个示例未运行”作为失败；可运行交付才要求约定的示例/测试证据。已有故障归属与重试采用父级规则，不另设“两到三轮”的通用次数。

## 输出重点

1. 采用了哪种模板结构
2. 正式包名如何替换
3. 公用层如何归位
4. 第一阶段做到什么程度
5. 本轮要求的 Examples / Tests 入口及其证据；范围外的真实验证标为 `not_required`
