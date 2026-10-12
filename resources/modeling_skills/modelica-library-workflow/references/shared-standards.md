# 库工作流共用约定

## 权威规则与读取边界

- 任务路由、会话、MCP 0.4 工具分类、错误与分类重试统一引用父级 [shared-standards.md](../../ty-sysplorer-modeling-rules/references/shared-standards.md)；不在本 Skill 复制第二套会话恢复或次数限制。
- 检查、翻译、仿真、结果和 Gate 6 的适用范围统一引用父级 [seven-gates-validation.md](../../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md)。本地步骤编号不是父级 Gate 编号。
- 本 Skill 只增补库结构、公共接口、Examples / Tests、本地化及库级治理。普通单模型不因“建模、修复、评审、图面”等词进入建库流程。
- 已有模型的具体故障由父级指定的独立调试入口主导，本 Skill 仅在故障确实涉及库结构或公共接口时提供支持；新建库过程中的失败留在原任务内修复。
- 离线方案、文件整理和静态评审不启动或探测 Sysplorer。仅在请求的验证阶段确实需要工具时读取父级工具契约并首次访问会话。

## 库级执行与模板边界

- 先明确本轮对象、改动范围和终端阶段，再进入对应 workflow；保留已有授权，不重复要求确认。
- `template-package-scheme.md` 是采用 `TYComponentsTemplate` 或明确选定同类模板时的结构约定权威来源。固定公共层、接口本地包装、展示顺序、中文显示名及 `Basics` 规则不自动施加给其他工程。
- 非模板任务优先保留既有兼容结构、公共接口及原生标准库/商业库接口；只修复实际请求范围内的引用、目录和 `package.order` 一致性。不为对齐模板迁移所有接口或增建空包。
- 完成层级与最低证据只由 `acceptance-checklist.md` 定义；执行顺序见 `executor-base.md`，结论表达见 `input-output-contract.md`。
- 只保留必要阶段记录。独立报告与成套文档按用户请求生成；代码骨架可用于已授权建库，不因禁止额外文档而禁止使用骨架。
- 已确认的项目总库集合由父级维护，库结构整理不删除其他已选域或标准库组件。

## 版本与 MCP 衔接

- 本附加 Skill 沿用 `Modelica 4.0.0.TY.1` 基线；用户/工程版本覆盖例外仅适用于单独使用主规则的任务，不自动扩展到本组合。已有工程版本不同则保留文件并报告不一致，不能静默改写 `uses` 或宣称兼容通过。
- 模型/组件/端口/文本查询使用 `model_inspect`；独立比较使用 `compare_model`；已加载顶层列表使用 `session_manager(action="get_loaded_models")`。查询子包时给出明确类名，不假定空根 `get_classes` 可用。
- `model_manager(action="save")` 原位保存，另存使用 `save_as`；按实际返回核对 `saved_path`，不把保存成功等同于检查或运行成功。
- MCP 0.4 的检查、翻译、仿真可对无 Placement 的用户文件自动布局并写回，即使不传 `reload_mo_path` 也可能触发。只读评审/诊断不得无条件调用这些操作；按父级处理获授权副本及未验证边界。
- 需要导出图片时先查 `get_api_document` 的 `ExportDiagram`，再用 `call_code(mode="run_sysplorer_api", payload={...})` 调用已查证的官方 API；`run_script` 仅为兼容别名，`payload` 对象必填。图片不是每项库任务的默认产物。
- 自动布局发生实际图形改动时纳入父级 Gate 6；结构化证据是基础，图片按请求和能力使用。视觉缺陷不阻断检查、翻译、仿真；注解语法/结构错误仍由检查阻断，完整图形交付前须完成适用验收。
- 这里只声明源码适配要求。目标部署、会话工具发现和真实运行回归必须另有证据，静态阅读不能代替。
