# 执行职责摘要

本文件用于需要明确协作职责时的快速复核，不作为每个 workflow 的强制第二入口。

- 库任务分类与边界：`requirement-mapper.md`。
- 公共接口、包结构和模板约定：仅采用模板时读 `template-package-scheme.md`；其他工程保留兼容接口和原有分层。
- 执行顺序与验证终点：`executor-base.md`。
- 静态检查与问题定位：按问题读取 `workflow-checklist.md`、`common-errors.md`。
- 完成事实与证据表达：`acceptance-checklist.md`、`input-output-contract.md`。
- 通用会话、修复归属、分类重试、图面及 MCP 副作用：通过 `shared-standards.md` 引用父级规则。

必须做到：保护已确认的目标和依赖，区分 Examples 与 Tests，保持实际改动的引用及目录一致，只中文化要求范围，按真实证据声明完成层级。

不得做到：为模板外工程强制复制接口或增加空公共层；为骨架/文案任务启动运行验证；把静态修改写成可运行；为填表读取无关结果；未获授权修改技术标识符或生成成套文档。
