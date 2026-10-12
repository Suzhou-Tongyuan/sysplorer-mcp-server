---
name: ty-sysplorer-modeling-rules
description: 为 Sysplorer 中具体的 Modelica 物理模型、商业库模型、Modelica+Sysblock 混合模型及 Modelica 库工作提供规划、评审、搭建、修改、仿真、分阶段验证和交付规则；也在用户明确要求时，为 Modelica 模型、Example/Demo 或测试对象新建或同步更新 annotation(Documentation(info=...)) 帮助信息。普通 Sysblock 框图或信号任务、纯 API 或结果查询不使用本 Skill；第一阶段不为 Sysblock 生成本文档体系，普通建模不得自动触发文档生成。纯帮助问答仅在 sysplorer-mds-docs 无法完成时进入文档检索、降级与总结路径。已有模型的具体故障诊断或修复优先由独立的专业调试 Skill 主导，故障域未知时使用 ty-sysplorer-debugging；本 Skill 仅按需提供物理或混合顶层修改与交付约束。
metadata:
  short-description: Sysplorer Modelica and hybrid modeling rules
  version: 1.9.2
  managed-by: sysplorer-mcp
---

# Sysplorer Modelica and Hybrid Modeling Rules

## Intent and routing

| Intent | Action |
|---|---|
| Plan | Define scope, route, evidence, and acceptance. Stop after the plan only for a plan-only request; an explicit request to build, execute, check, translate, or simulate already authorizes those in-scope actions. |
| Review | Inspect only the requested artifacts; do not modify, build, or simulate unless requested. |
| Modify/build, execute/verify, deliver | Follow the selected route; run only validation required by the requested outcome; never report an unmet objective as complete. |

| Request | Owner |
|---|---|
| Official-help Q&A | `sysplorer-mds-docs`; use this skill's fallback only if it cannot complete the request. |
| Pure API or results query | Live discovery then `get_api_document`, or `result_manager`; do not construct a model. |
| Ordinary Sysblock diagram/StateMachine | `ty-sysblock-diagram-modeling` directly. |
| Sysblock signal/communication | `ty-sysblock-signal-modeling` directly. |
| Explicit Modelica model/example/test-case Documentation authoring or synchronization | This skill's Documentation route; do not use it for Sysblock in phase one. |
| Modelica physical, commercial Modelica, Modelica library, or physical-top-level hybrid | This skill. |

Author Modelica physical work as `.mo` text. In a hybrid, keep the Sysblock controller/algorithm as a child and the physical wrapper/top level as Modelica text. Never substitute a Modelica `connect()` graph for Sysblock topology or use `SetModelText` for Sysblock topology.

## Independent debugging entrypoints

For an existing model's concrete failure or abnormal result, directly use
`ty-physical-model-debugging` for Modelica, `ty-sysblock-model-debugging` for
Sysblock, or `ty-sysplorer-debugging` when the fault domain is unknown/mixed.
None requires prior routing through this skill. When a debugger reads this skill
for applicable physical-model edit or delivery constraints, stay in the current
debugging step: do not reroute, replan, recreate the workspace, or reproduce twice.
Ordinary Sysblock edits use the diagram/signal skill's constraints directly.

A construction task retains its owner when an intermediate stage fails: reuse
its evidence and task-owned working model for scoped debugging, then resume the
original task. A failure keyword alone does not turn construction into a new
debugging assignment. Read-only diagnosis does not trigger graphical delivery;
actual changed graphical targets still require the applicable Gate 6.

## Invariants

- Use Agent CWD for project artifacts; query a live Sysplorer directory only when required. Never call `ClearAll` or `ChangeDirectory`.
- MCP 0.4 routing, startup states, errors and side effects follow `references/shared-standards.md`. Check/translate/simulate may write layout annotations; do not treat them as read-only diagnostic calls.
- Offline model/log inspection needs no session call. Before first live access, confirm the target through Sysplorer MCP: use `session_manager(action="probe")` when available, then `health`. Reuse valid evidence for the same session; recheck after session changes, disconnection, or infrastructure symptoms. Never close or restart a user-attached GUI session.
- Treat commercial-library classes as protected: never decrypt, decompile, unpack, or inspect source.
- Run full Gate 6 on every newly created or modified graphical target before final graphical delivery, but do not make visual-layout defects block translation or simulation. Only annotation syntax or structural errors surfaced by model checking block execution.
- Vehicle and commercial-library paths bind `Modelica(version = "4.0.0.TY.1")`. Only when using this parent alone, without vehicle/commercial paths, may explicit user or valid project version information override the default. Do not silently rewrite conflicting dependencies; see `references/domain-routing-and-library-versions.md`.
- Treat the user's acceptance contract as the maximum validation depth. If the requested terminal stage is only check + translate + simulate, stop the execution/result chain after all three succeed. Complete only any outstanding applicable Gate 6, necessary graphical re-check and delivery evidence; do not add results, variables, KPI, plots or animation.
- Mark result/KPI verification as `not_required` when the user did not request result evidence and no stated acceptance condition depends on it. A successful simulation may satisfy a simulation-only acceptance contract, but never implies an unrequested KPI was checked.

## Documentation isolation

Enter the Documentation route only when the user explicitly requests help/documentation creation or synchronization for a Modelica object. Do not auto-generate, auto-update, offer, or ask about documentation after ordinary modeling. For a combined build-and-document request, finish the existing modeling workflow and its requested validation first, then run `workflows/modelica-documentation.md` as a serial, optional step.

A Documentation-only task reads the current `.mo` object and may change only its `Documentation(info=...)` content, plus an independent Markdown export when explicitly requested. Do not change model behavior to make prose true. Do not execute a designed test, generate a test report, or infer PASS/FAIL. Documentation failure does not invalidate an already successful modeling result.

## Commercial and library route

Respect the effective user/project library boundary. When unspecified, use the standard library if sufficient; otherwise retain its usable parts and add publicly evidenced commercial components for functional gaps. Failed queries or missing documents are not proof of functional gaps. This combination remains Modelica, not automatically a hybrid. Choose a primary commercial domain skill only after that commercial boundary has been selected. Explicit library/package names and user-selected boundaries override scene words; scene words alone never authorize an arbitrary commercial-library default. Use `references/domain-routing-and-library-versions.md` as the authoritative cross-domain and alias/version table. TY hydraulic/pneumatic routes to `ty-hydraulic-pneumatic-modeling`; TY mechanics to `ty-mechanical-modeling`; TY thermal-fluid/HVAC to `ty-thermofluid-modeling`; explicit NPSLibrary to `ty-nps-library-modeling`; TY electrical/machine to `ty-electrical-machine-power-modeling`; TY energy to `ty-energy-modeling`; TA vehicle to `ta-vehicle-modeling`. A pure Modelica Standard Library or self-authored mechanical/multibody task stays in this parent skill and must not load a TY commercial domain skill. Add a supporting domain skill only for a real selected component boundary. Record the project library set and domain-owned subsystems; a domain whitelist cannot reject already selected standard-library or supporting-domain components. Preserve existing vehicle coverage/entry paths and electrical/NPS-specific routing. Add `modelica-library-workflow` only for library-level structure, public interfaces, Examples/Tests organization, localization, extension or governance. A single model or one-off testbench does not by itself trigger the library workflow.

## Minimal loading map

All paths are relative to this skill directory and are directly linked here.

| Need | Read/invoke |
|---|---|
| Tools, paths, commercial evidence, validation scope | `references/shared-standards.md` |
| Help-query/MDS fallback | `references/documentation-routing.md` |
| Cross-domain routing, library aliases, and versions | `references/domain-routing-and-library-versions.md` |
| Explicit Modelica Documentation task | `references/modelica-documentation-rules.md`; `workflows/modelica-documentation.md`; then only one selected template: `templates/documentation/model-help-template.md`, `templates/documentation/case-help-template.md`, or `templates/documentation/test-case-template.md` |
| Ambiguous physical/hybrid/domain route | `references/modeling-path-router.md` |
| Modelica text/diagram | `references/modelica-style-guide.md`; `references/modelica-diagram-connect-semantics.md` |
| Modelica work / hybrid / gates | `workflows/modelica-modeling.md`; `workflows/hybrid-modeling.md`; `workflows/seven-gates-validation.md` |
| Class/API/corpus documentation | `get_lib_model_document`; live discovery then `get_api_document`; `resources_retrieval` |

For Gate 6, record only `layout.status`, `layout.level`, changed `layout.targets`, performed `layout.checks`, and evidence. Use `not_required` only when the task creates or changes no graphical target, such as Documentation-only, code-only, or read-only work with no graphical modification. Layout repair belongs in the shared `repairs` record.
