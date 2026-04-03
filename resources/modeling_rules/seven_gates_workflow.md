# MWorks 建模全局规则与执行闭环

> 与仓库根目录 `AGENTS.md` / `CLAUDE.md` 中「全局工程规则」「AI 自主执行闭环」等章节保持一致，供 MCP 服务端初始化时注入 instructions。若与仓库文件有出入，以仓库最新版为准。

## 全局工程规则（7 Gates）

> 所有 Gate 均为硬性约束，不可跳过。违反即为流程错误，不允许以"疏忽"为由。

**Gate 0: 规范优先** — 创建/修改 `.mo` 前需了解代码风格和库结构。豁免：已记录的类型、会话已读过、仅改参数。必须读：新库结构时读 `.claude/modelica_style_guide.md`。禁止从 `src/` 现有代码推断风格。

**⛔ Gate 1: Library First（每次建模前必检查）** — 写任何 `.mo` 组件代码前，先确认是否有 TY/TA 私有库版本。查询顺序：① `private_lib_quickref.md` → ② 在 Sysplorer 侧确认类可用：`mworks_sysplorer_load_library`（尚未加载时）+ `mworks_sysplorer_get_lib_model_document(full_class_name=...)` 拉取**当前已解析库**的说明/参数/端口等导出文档 → ③ 才考虑 MSL。私有库有则**必须用**；端口名未知时用上述文档与（必要时）`mworks_sysplorer_model_manager`（如 `action=get_component_ports`）等探测后再建模。豁免：quickref 已覆盖或任务明确要求自建。

**Gate 2: 零幻觉连线** — `connect(a, b)` 前确认两侧端口类型一致。豁免：会话上下文已明确。必须读：未覆盖的连接器类型查 quickref。绝不编造不存在的类名或端口名。

**Gate 3: 编译驱动** — 新建/修改 `.mo` 后**必须立即** `mworks_sysplorer_check_model`。失败自修复最多 3 次，之后求助用户。严禁运行有编译错误的模型。

**Gate 4: Testbench Required** — 变更后**必须**在 `tests/` 添加/更新测试台并 `mworks_sysplorer_simulate_model`（仅实例化不算完成）。

**Gate 5: 物理 KPI 验证** — 仿真后**必须**通过 `mworks_sysplorer_result_manager`（`action=get_var_values` 等）验证。变量名三级决策：① quickref §8 直接填 → ② 推断后猜测，报错再 `action=get_result_variables` → ③ 黑盒组件用 `get_result_variables` 取列表。硬性约束：p > 0, T > 0；冷却稳态温度 ≥ 冷却介质入口温度。

**⛔ Gate 6: Auto-Layout Required（系统级，每次建模前必检查）** — 系统级 `.mo` **唯一推荐写入路径**为 `mworks_sysplorer_smart_layout`，`mode=writeback_mo`（别名 `writeback` / `generate`），`auto_layout=true`，**禁止**先用 Write 写 `.mo` 再手工补 layout。须配合 `modelica_code` + `graph_json`（或 `graph_json_path`）及 `model_output_path` 等；`graph_json.children` 含 `world` 节点（如有 inner World），否则无 Placement。交付含布局状态。

**Gate 7: Delivery Evidence** — 最终回复输出证据（系统级 `layout` 必填）：
```json
{"lib_document":{"queried_classes":[],"ok":true},"mapping":{"used":[],"rejected":{}},"check":{"ok":true,"errors":[]},"sim":{"ok":true},"kpi":{"var":"value"},"layout":"ok | skipped(component-level)"}
```

## AI 自主执行闭环

**Step 0 — 健康检查**：`mworks_sysplorer_session_manager(action="health")` → `ok` 则预热；否则 `action="restart"` 或 `action="ensure"` 直至驱动可用。

**并行预热**：`mworks_sysplorer_load_library(<domain_libs>)`（域→库见 quickref §1）+ 按需读 quickref / style guide

**顺序执行**：
1. 解析需求 / 读文档 / PDF
2. Gate 1：quickref 未覆盖时，对已选类名 `mworks_sysplorer_load_library`（若需）+ `mworks_sysplorer_get_lib_model_document`；旁置语料用 `mworks_sysplorer_resources_retrieval`（`action=search` 等），**不**再使用已移除的元数据索引类 tool
3. 编写 `.mo`（对照 quickref §4 核验连接器）
4. **系统级任务**（Gate 6）→ `mworks_sysplorer_smart_layout`（`mode=writeback_mo`，`auto_layout=true`，`modelica_code` + `graph_json` + `model_output_path` 等），并按返回结果做 `mworks_sysplorer_check_model` 等后续校验
5. **一次性验证+展示**（Gate 3/4/5 合并）：`mworks_sysplorer_call_code(mode="fast_workflow", payload={...})`（字段与原 fast_workflow 一致，参数详见 quickref §1 Step 3）
6. check 失败 → 修复 + 强制重载重试（最多 3 次）
7. 新增 `.mo` 后在父目录 `package.order` 追加类名
8. 报告 Delivery Evidence（Gate 7）

> **调用次数目标**：系统级建模全流程（生成→检查→仿真→KPI→绘图→动画）≤ 2 次 MCP 调用。

## 建模加速规则

**规则 A: 跳过踏脚石模型** — 建模前必读 quickref，直接构建目标系统模型。仅在 quickref 未覆盖且 `mworks_sysplorer_get_lib_model_document` / 端口探测仍不足以确定连接器、或需最小化复现编译错误时才用踏脚石。

**规则 B: 预热 .mol 库** — TY/TA 私有库首次加载 10-30s，写代码前并行 `mworks_sysplorer_load_library`。`LoadLibrary` 返回 False 不等于失败，用 `mworks_sysplorer_check_model` 验证。

## 关键技术要点

- **MSL 版本**：`4.0.0.TY.1`。`uses()` 必须写 `Modelica(version = "4.0.0.TY.1")`，写 `"4.0.0"` 会加载失败
- **`when` 块**：同一 discrete 变量用 `when ... elsewhen ...` 单块，避免多块冲突
- **simMode**：`0`=自动（默认）、`1`=独立、`2`=实时
- **仿真结果**：`Result.msr`，路径 `C:\Users\<用户>\Documents\MWORKS\Simulation\<模型名>\Result.msr`

## 速查指针

→ `.claude/private_lib_quickref.md`：§1 域→库映射、§2 inner 声明、§3 参数差异、§4 连接器类型、§5 典型拓扑、§8 KPI 变量名

→ **Sysplorer 实时文档（非 RAG）**：已加载库类说明 / 端口 / 参数用 `mworks_sysplorer_get_lib_model_document`；Python 建模 API（`mworks_sysplorer_call_code` 的 `run_script` 模式 / ModelingPy）用 `mworks_sysplorer_get_api_document`。
