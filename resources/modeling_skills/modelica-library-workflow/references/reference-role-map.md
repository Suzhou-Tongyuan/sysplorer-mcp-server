# 参考资料角色映射

## 单一维护位置

| 资料 | 权威职责 | 何时读取 |
| --- | --- | --- |
| 父级 `references/shared-standards.md` | 会话、MCP 分类、错误、分类重试、项目边界 | 首次需要相应规则时，复用已有证据 |
| 父级 `workflows/seven-gates-validation.md` | 验证范围、Gate 6 与通用交付状态 | 验证/图面规则适用时 |
| 本地 `shared-standards.md` | 与父级衔接、模板边界和本地共用约定 | 库级任务首次使用 |
| `requirement-mapper.md` | 库级任务分类与工作流选择 | 任务类型不明确时 |
| `template-package-scheme.md` | TY 模板的骨架、接口本地化、命名和展示顺序 | 实际采用该模板或同类方案时 |
| `cross-domain-business-package-strategy.md` | 组件角色到业务包的映射 | 需要新业务包或跨域分层时 |
| `executor-base.md` | 终端阶段与执行顺序 | 建库/扩展及验证任务 |
| `workflow-checklist.md` | 受影响对象的静态自检项目 | 只读取相关章节 |
| `common-errors.md` | 高频结构、接口、图面问题索引 | 出现匹配的问题时 |
| `acceptance-checklist.md` | 四类完成事实和最低证据 | 收口时 |
| `input-output-contract.md` | 证据与结论表达 | 收口时 |
| `ai-execution-spec.md` | 执行职责摘要 | 需要职责复核时 |
| `phase-output-templates.md` | 可选阶段记录字段 | 用户要求结构化记录时 |
| `promotion-checklist.md` | Skill 发布资料一致性 | 准备发布 Skill 时 |

父级路径从本目录解析为 `../../ty-sysplorer-modeling-rules/...`；本地文件路径相对当前 `references/`。workflow 中 `references/...` 按 Skill 根目录解释。

## 按需读取原则

1. 入口先判断库级目标，选择一个匹配工作流；不要先顺序读取全部参考资料。
2. 本地化任务只读语言、标识符与输出范围；图面任务只读图面问题和父级 Gate 6；评审只读被评审章节。
3. 模板细则只在 `template-package-scheme.md` 维护，清单保留检查提示；公共工具/验证政策由父级维护，本地只说明衔接。
4. package 骨架是建库素材，可用于已授权文件生成；报告模板不自动变成独立交付物。
5. 保留可达文件与专业知识，不为了对齐目录模板重命名、迁移或批量删除资料。
