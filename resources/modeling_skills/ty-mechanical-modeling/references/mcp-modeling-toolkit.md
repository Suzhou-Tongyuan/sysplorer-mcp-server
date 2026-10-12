# MCP Modeling Toolkit

本文件仅补充机械查询节奏。MCP 0.4 分类、会话、错误和重试以 `../../ty-sysplorer-modeling-rules/references/shared-standards.md` 为权威；验证范围与 Gate 6 以父级 `workflows/seven-gates-validation.md` 为准。

---

## 1. 会话与库

| Task | Preferred Tool |
|------|----------------|
| 会话前置条件 | 按父级规则复用有效证据，首次确认及必要恢复使用 `session_manager`；离线任务不调用 |
| 查看状态 | 按父级规则使用 `session_manager(action="health")`；`starting` 时不追加 ensure/restart |
| 加载库 | `load_library` |

库加载纪律：

- 只加载当前分流需要的 TY 子库；不要为了“保险”一次加载所有机械商业库。
- 若只是信息查询，先列出目标库/子包范围，再查询必要文档；不要对同一库反复做重叠 search。
- 只读取任务允许范围内的 Skill 与证据文件；无法读取时记录缺口，不以其他目录副本静默替代。

---

## 2. 模型生命周期

| Task | Preferred Tool |
|------|----------------|
| 新建物理模型 | 按父级写 `.mo` 文本，再用 `model_manager(action="load_file")` 加载 |
| 加载 `.mo` 文件 | `model_manager(action="load_file")` |
| 打开模型 | `model_manager(action="open")` |
| 保存模型 | `model_manager(action="save")` 原位保存；另存用 `save_as`，核对 `saved_path` |
| 获取组件/端口/文本 | `model_inspect(action="get_components" / "get_component_ports" / "get_model_text", model_name=...)`，按动作核对必要参数 |

组件和文档查询节奏（用户模型可查文本；商业受保护类仅用公开内省与文档，不读取受保护源码）：

1. 顶层已加载列表使用 `session_manager(action="get_loaded_models")`；明确包/子包使用 `model_inspect(action="get_classes", model_name=...)`，不依赖空根查询。
2. 用 `get_lib_model_document(full_class_names=[...])` 批量查询当前候选类；只有工具不支持批量时才逐个查询。
3. 用 `model_inspect(action="get_component_ports", model_name=..., component_name=...)` 或真实文档确认端口域和方向；按当前 schema 填写动作所需字段。
4. 组件名单稳定后再查参数，避免为被淘汰组件消耗大量文档 token。
5. 在工作记录中缓存已查过的类名、端口和参数；同一组件不要重复查询。

---

## 3. 建模与布局

优先顺序：

1. 能用官方 MCP 工具直接完成的，先用 MCP 工具
2. Modelica 结构按父级写 `.mo` 文本；未封装官方 API 先查 `get_api_document`，再用 `call_code(mode="run_sysplorer_api", payload={"python_source":"..."})`，脚本字段不能放在 payload 外
3. 图面布局需要自动整理时，使用 `smart_layout`

注意：

- `run_sysplorer_api` 内必须先显式 `import mworks.sysplorer as ModelingPy`
- 不要假定脚本环境中天然存在 `ModelingPy`

---

## 4. 检查、翻译、仿真

| Step | Preferred Tool | Typical Purpose |
|------|----------------|-----------------|
| Check | `check_model` | 结构、参数、物理一致性检查 |
| Translate | `translate_model` | 翻译数学模型 |
| Simulate | `simulate_model` | 运行仿真 |
| Result Readback | `result_manager` | 读变量、时序、时刻值 |
| Plot | `plot_manager` | 绘图与动画 |

调用纪律：

- 调用 MCP 工具前以当前工具 schema 为准，不要向工具传未声明字段。仿真终止时间、结果文件路径和验证变量尤其要核对参数名与类型。
- 请求检查/仿真时先完成适用静态预检：连接、世界/参考、方程/自由度和参数；仅要求结果核验时提供预期变量名。
- 仅请求结果核验时读取结果，优先批量接口；simulate-only 不指定 `verify_result_var`。失败仿真不得靠残留旧结果判成功；时间插值/区间外端点回退保留 warning，不充当原始采样。
- 重试按父级错误分类执行，先判断后端是否仍在运行及错误的可恢复性；不把每个失败都处理为会话故障，也不执行原样无限重试。

---

## 5. 推荐调用节奏

```text
按父级确认/复用会话（仅需要真实平台动作时）
-> load_library
-> model_inspect(get_classes) / get_lib_model_document only for candidate scope
-> 按父级写 Modelica 文本并用 model_manager load_file/open
-> 建模/连线/参数写入
-> static preflight: library boundary, ports, world/reference, DOF/equation intuition
-> check_model（按请求范围）
-> translate_model（按请求范围及运行前提）
-> simulate_model（仅按请求）
-> result_manager / plot_manager（仅按请求）
```

---

## 6. MCP 0.4 副作用与图面

- check/translate/simulate 不再接受旧布局参数；显式布局使用 `smart_layout`。未传 `reload_mo_path` 也可能按缓存路径自动写回缺 Placement 的用户 `.mo`，只读诊断先采用获授权副本或说明能力限制。
- 自动布局或官方布线成功不等于 Gate 6 通过；记录实际图形改动、写盘和会话保存状态。纯视觉问题不阻止检查、翻译或仿真。
- 结构化图面证据为基础；按需导图先用 `get_api_document(api_function_name="ExportDiagram")` 核对官方签名，再通过必填 payload 的 `call_code` 调用；不使用旧 manager 导图动作。

## 7. 什么时候进入修复闭环

- `check_model` 返回不通过
- `translate_model` 失败
- `simulate_model` 失败或结果异常
- `result verify` 结论不通过
