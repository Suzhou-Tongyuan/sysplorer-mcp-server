---
name: ty-sysplorer-modeling-rules
description: >-
  Sysplorer 建模总规则。用户要新建、搭建、修复、仿真或交付模型，或需要在 Modelica 物理、Sysblock 框图、Modelica+Sysblock 混合建模之间分流时使用。强制执行：Modelica 物理写 `.mo` 文本（默认 Modelica 4.0.0.TY.1），Sysblock 只用官方 API，混合模型按 Sysblock 子模型 + Modelica 物理顶层分层处理；路径只用 Agent CWD 或 `GetDirectory`；`check_model` / `check` 后、翻译、长仿真或交付前，对所有新建或修改的系统、子系统和组件图形模型完成 Gate 6 布局与图面验收。
---

# Sysplorer modeling rules (mandatory)

## Mandatory Operating Rules

- **Route first**: before construction, choose exactly one path. Use the **Decision flow** below for quick triage and **`references/modeling_path_router.md`** as the authoritative tie-breaker; after routing, load only the path-specific references.
- **Use the required modality**: Modelica physical models are authored as plain-text `.mo`; Sysblock diagrams are built and wired only through official APIs; hybrid models keep Sysblock internals in the Sysblock path and the physical wrapper/top level in the Modelica path.
- **Decide commercial-library use first**: in the Modelica physical portion of a task, first determine whether a TY/TA commercial-library component is needed and suitable. If not, record why and use the requested/appropriate Modelica standard-library or self-authored implementation. If selected, treat every commercial-library class as protected and use documentation, registered commercial-library corpora, and public introspection rather than source inspection.
- **Apply dependency guard before treating library work as complete (modelica_lite)**: this mogick pack runs as **`modelica_lite` / `mols`** and typically **does not preinstall** full Modelica / TY `.mol` packs. Always **`load_library(action="load")` first**; `dependency_download_enabled=false` does not mean libraries are absent. When `load_library` returns `ok: false` / `LoadLibrary returned False` (including silent False), apply `ty-sysplorer-dependency-guard`: **plan** via `load_library(action="plan")`, then real `prepare` (`dry_run=false`, `download_missing=true`) when the `--user-workspace` gate is open, before retrying the original workflow point.
- **`run_sysplorer_api` on modelica_lite**: always uses the original **in-process** path (no separate `python.exe` lookup). Do not try to point `SYSPLORER_PYTHON` at a missing `External\\python64`.
- **Close Gate 6 before deep execution or delivery**: after `check_model` / `check` succeeds and before `translate`, first long `simulate`, or delivery, finish path-specific layout and diagram acceptance for every created or modified graphical model, including reusable component models. Modelica physical and hybrid `.mo` files must have usable connector `Placement` / `iconTransformation`, key-instance `Placement`, and visible-connection `Line` annotations for their actual scope; bare topology is not deliverable. Use `smart_layout(mode="writeback_mo", model_name="<FQ name>", model_output_path="<path to .mo>", auto_layout=true)` when needed, and re-check if `.mo` changed. Sysblock uses block-diagram APIs / Sysblock rules, not Modelica `.mo` writeback. A strictly code-only Modelica class may mark Gate 6 as `not_applicable(code-only)` when it neither inherits another component/model structure nor contains component instances.
- **Require an explicit Gate 6 completion checkpoint**: do not mark layout complete from `check_model` success alone. Before translation, simulation, or delivery, record `layout.applicability`, `layout.scope`, `layout.annotations_checked`, `layout.diagram_reviewed`, `layout.rechecked_after_writeback`, and `layout.ok`. Component-level delivery may not use `skipped(component-level)`; inspect external connector anchors, icon-layer placement, internal instances, and every connection intended to be visible. For `not_applicable(code-only)`, record source inspection evidence proving there is no inherited component/model structure and no component instance. If completion or exemption evidence is unavailable, set `layout.ok=false` and block delivery.
- **Treat all commercial-library classes as documentation-only dependencies**: after commercial-library selection, do not decrypt, decompile, unpack or inspect commercial-library source, and do not call `model_manager(action="get_model_text")` for those classes. Determine the fully qualified class name from metadata/quick references, load the library, and use `get_lib_model_document` plus commercial-library documentation search. If documentation is insufficient, use component/port introspection and a minimal black-box validation model; never fall back to source inspection. Read `references/modeling_path_router.md` §0.4.
- **Never** call `ClearAll` or `ChangeDirectory`, and never use `SetModelText` / text editing for Sysblock topology.

## Entry Checklist

1. **Route**: Modelica physical, Sysblock, hybrid Modelica + Sysblock, or one clarifying question if genuinely unclear.
2. **Load refs**: read only the references required for that path.
3. **Confirm paths**: use only Agent CWD or Sysplorer `GetDirectory`; never use the MCP server program tree as the project root.
4. **Build by modality**: `.mo` text for Modelica physical, official APIs for Sysblock, layered handling for hybrid.
5. **Validate**: `check_model` / `check` -> Gate 6 layout acceptance -> translate / simulate / KPI / delivery evidence per `seven_gates_workflow.md`.

## Decision Flow

1. **Hybrid Modelica + Sysblock**: signals include 混合建模 / 混合仿真, physical plant + Sysblock controller, or a physical top model embedding a Sysblock model. Read `references/hybrid_modeling_workflow.md` and `modeling_path_router.md` §4. Build/check the Sysblock child first, then embed it as a Sysplorer-recognized SEC instance in a Modelica `.mo` top level; ordinary same-layer `AddComponent` failure is an insertion-path limit, not proof that hybrid models are unsupported.
2. **Sysblock**: signals include Sysblock, block diagram, Embedded Coder, `NewModel(..., restriction="Sysblock")`, or programmatic block wiring, with no physical top-level integration. Read `references/sysblock_style_guide.md` and `modeling_path_router.md` §3. Skip physical-library §0 and do not author physical `connect()` hydraulic/mechanical graphs.
3. **Modelica physical**: run library/domain mapping in `references/modeling_path_router.md` §0, then use `references/modelica_style_guide.md`, `references/modelica_diagram_connect_semantics.md`, and `references/seven_gates_workflow.md`. Unless the user specifies another version, declare/load **`Modelica(version = "4.0.0.TY.1")`**.

## Work Paths

| Priority | Source | Use |
|----------|--------|-----|
| 1 | Agent current working directory | Default base for relative paths, new files, and current project outputs. |
| 2 | `GetDirectory` | Use only when Sysplorer/tool-chain aligned paths are required. |
| Forbidden | MCP program / entry path | Do not read/write user models under the MCP server source, install, `main.py`, or launch tree. |

## Reference Map

| Need | Read / use |
|------|------------|
| Path routing | `references/modeling_path_router.md` |
| Full gates and workflow | `references/seven_gates_workflow.md` |
| Modelica style and diagram syntax | `references/modelica_style_guide.md`; `references/modelica_diagram_connect_semantics.md` |
| Sysblock API modeling | `references/sysblock_style_guide.md`; Sysblock block manuals via `resources_retrieval` + `sysblock_model_library` |
| Hybrid workflow | `references/hybrid_modeling_workflow.md` |
| Installed class docs | `get_lib_model_document` |
| Encrypted `.moc` / `.mol` commercial classes | `references/modeling_path_router.md` §0.4; use class documentation and black-box validation, never protected source inspection |
| Large corpora | `resources_retrieval` |

Authoritative copies live under `references/`. RAG `corpus_id=modeling_rules` points at this directory; if workspace copies under `resources/` differ, use `resources_retrieval` for search but keep behavior consistent with this skill.

Audit-only Chinese review text lives at `references/skill_zh_audit.md`; use it only for human review or translation checks. `SKILL.md` remains the sole execution authority.
