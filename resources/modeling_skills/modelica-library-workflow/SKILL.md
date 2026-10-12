---
name: modelica-library-workflow
description: 处理 Modelica 模型库的包结构、公共接口、Examples/Tests、库级本地化及治理；适用于建库、库扩展、库评审和库级图面修复。普通单模型的建模、修复、评审或导图不触发本技能。仅作为 ty-sysplorer-modeling-rules 的库工作流附加层，验证与文档范围继承用户请求。
metadata:
  short-description: Modelica library structure, interfaces, and scoped validation
  version: 1.1.2
  managed-by: sysplorer-mcp
---

# Modelica Library Workflow

Use this only as a thin add-on to `ty-sysplorer-modeling-rules`. The parent skill owns routing, seven gates, layout timing, repair loop, and delivery evidence. This skill adds library/package workflow details.

## When To Use

- Use only when the deliverable concerns a Modelica library: package structure, public interfaces, Examples/Tests, library localization, or library governance.
- Use templates and library-wide diagram/localization workflows only inside that library-level scope. Ordinary single-model creation, repair, review, and diagram export remain with the parent and domain skills.
- Do not use for pure theory, pure API lookup, or broad discussion without a concrete artifact objective.
- Existing concrete failures stay under the parent-designated debugging entry; provide library support only when structure/public interfaces are implicated. Failures during new construction remain in that task.

## Minimal Reading

All `references/...` and `workflows/...` paths in this skill are relative to **this skill directory** (the folder that contains this `SKILL.md`), not the workspace root or any parent `skills/` directory.

Read `references/shared-standards.md` once for the parent contract, then select one workflow and only the needed reference sections. `references/reference-role-map.md` explains the ownership of each rule:

| Need | Read |
|---|---|
| Task classification | `references/requirement-mapper.md` |
| Template/top package design | `references/template-package-scheme.md` |
| Cross-domain package names | `references/cross-domain-business-package-strategy.md` |
| Requested terminal stage / execution | `references/executor-base.md` |
| Static checklist / common mistakes | `references/workflow-checklist.md`, `references/common-errors.md` |
| Acceptance / delivery | `references/acceptance-checklist.md`, `references/input-output-contract.md` |

## Specialized Workflows

Prefer these when they match exactly:

| Workflow | Path |
|---|---|
| Build from template | `workflows/build-from-template.md` |
| Build library with example validation | `workflows/build-library-with-example-validation.md` |
| Extend existing library | `workflows/extend-existing-library.md` |
| Review existing library | `workflows/review-existing-library.md` |
| Normalize structure | `workflows/normalize-library-structure.md` |
| Chinese localization | `workflows/chinese-localization.md` |
| Repair diagram annotations | `workflows/repair-diagram-annotations.md` |

## Domain Additions

- Keep `package.mo` and `package.order` synchronized.
- Route the task to exactly one primary mode before expanding work: `plan/review`, `structure build`, `library extension`, `localization`, `diagram repair`, or `library + example/test validation`.
- Match the first increment to the requested terminal stage. A skeleton/file task ends with files and applicable static checks; a runnable-library request needs real evidence for the agreed first Examples/Tests. Do not turn first-pass creation into mandatory simulation.
- When the task mixes library workflow with domain-model construction or multi-condition simulation, keep this skill responsible for package structure, `Examples` / `Tests`, and delivery status only; hand physical modeling and deep simulation loops back to the parent skill or the active domain skill.
- Template-specific fixed layers, local interface wrappers, names, and ordering belong to `references/template-package-scheme.md` and apply only when that template is adopted. Preserve compatible native interfaces and existing structure in other projects.
- Keep `Examples` and `Tests` separate: examples show usage, tests verify behavior.
- Do not use official examples as renamed deliverables; use them as reference or validation baselines.
- Reuse the parent classified retry policy. Stop an unchanged hypothesis without new evidence; distinguish infrastructure retries from model repairs and overall progress.
- Use `references/acceptance-checklist.md` for the four completion levels. A missing unrequested run does not invalidate completed files; requested runnable claims need real simulation evidence.
- For diagram-related work, parent Gate 6 still decides layout timing and re-check requirements.

## Delivery Additions

In addition to parent delivery evidence, state:

- Completion level: `plan-complete`, `files-modified`, `structure-level-verified`, or `run-level-verified`.
- Package-structure decisions, common-layer decisions, localization scope, diagram status, validation depth, and remaining risks.
- The requested terminal stage and each applicable validation fact. Use parent statuses: `not_required` for out-of-scope stages, `blocked` with the reason for required but unexecuted stages, and `passed` / `failed` for executed stages. Do not present a planned endpoint as a failed gate.
- Use report/document templates only when explicitly requested; code/package skeletons remain available for authorized file generation. Results, KPIs, curves, animations, and formal documentation are conditional on the request.
