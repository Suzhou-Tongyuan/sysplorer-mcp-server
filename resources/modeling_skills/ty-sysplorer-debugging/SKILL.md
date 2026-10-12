---
name: ty-sysplorer-debugging
description: >-
  Independently route diagnosis or repair of existing Sysplorer model failures
  when the fault domain is unknown, mixed, or product-wide. Confirmed Modelica
  faults use ty-physical-model-debugging directly; confirmed Sysblock or CCaller
  faults use ty-sysblock-model-debugging directly. Exclude ordinary construction,
  editing, layout, tuning, and pure API help.
metadata:
  short-description: Route Sysplorer debugging by fault domain
  version: 1.1.0
  managed-by: sysplorer-mcp
---

# Sysplorer Debugging Router

This is an independent entrypoint, not a mandatory child of the modeling skill.
Known domains can enter either specialist directly without this router. Identify
the fault domain and coordinate specialists; do not repeat their repair loops.

## Task Mode and Handoff

1. Identify `diagnose_only` or `repair` from the user's request. A request only to
   explain or locate a fault does not authorize edits. Reproduce only when the
   request authorizes execution; explicit offline review uses supplied artifacts.
2. Record the requested terminal stage and acceptance conditions. Reuse available
   model identity, session evidence, first attributable diagnostic, baseline,
   settings and work-copy/checkpoint. Unknown fields stay unknown; do not query
   unrelated data merely to fill a report.
3. Use the smallest evidence needed to choose a specialist. Hand off the existing
   context once. Do not recreate the workspace, replan, or reproduce a baseline
   already attributable to the current model/settings.
4. Summarize the specialist's evidence and scope-qualified status. For mixed
   faults, coordinate another layer only when current evidence requires it.

## Routing

| Evidence | Route |
|---|---|
| Modelica equations, initialization, runtime, external function, or build produced by Modelica translation | `ty-physical-model-debugging` |
| Confirmed Sysblock restriction, ports/blocks, CCaller, or build produced by Sysblock code generation | `ty-sysblock-model-debugging` |
| Generated solver without a known origin | Identify restriction and generating pipeline before choosing a specialist |
| Mixed model | Follow the implicated layer; reuse valid child evidence and verify interfaces when the fault crosses the boundary |

Do not preload both specialists or all references. A known top-level fault does
not require rerunning every child. Ordinary diagram work uses
`ty-sysblock-diagram-modeling`; domain construction uses its existing modeling
skill. Construction-stage failures retain the original task owner and working
model, invoke scoped debugging, then resume construction.

## Shared Execution Boundaries

- Offline artifact inspection needs no session call. Before first live access,
  confirm the target through Sysplorer MCP: `session_manager(action="probe")`
  when available, then `health`. Reuse valid same-session evidence; recheck after
  a switch, disconnection, or infrastructure symptom. Never reset the user's GUI.
- Reuse known current API contracts. Resolve unknown names, parameters and return
  types before calling; use targeted documentation/fallback, never guessed writes
  or full API enumeration. Read `references/current-mcp-recipes.md` when needed.
- For physical edits/delivery, load applicable `ty-sysplorer-modeling-rules`
  constraints; for ordinary Sysblock, use diagram/signal constraints. Return to
  the current debug step without rerouting. Read-only diagnosis does not trigger
  layout; actual model changes retain applicable save/reload and delivery checks.
- Never call `ClearAll`, `ChangeDirectory`, or `Exit`. Preserve original model/C
  source and unsaved GUI state; edit only a verified task-owned working copy.
  Do not use `extends Original` as a copy, text edits for Sysblock topology,
  generated-code patches, or protected commercial-library source inspection.
- Keep user semantics and acceptance intact. Do not hide defects with removed
  assertions or parameter/solver sweeps. Existing authorization remains valid;
  seek judgment only for a new material design/scope choice.
- Two rounds without repeatable improvement stop the current hypothesis, not all
  useful work. Continue authorized targeted evidence/minimal-case isolation.
  Stop retrying the same infrastructure operation after two failures and report
  the missing capability; do not invent a static patch for an environment mismatch.

## Bounded Help and Evidence

Read `references/help-doc-index.md` for unexplained product diagnostics and query
`scripts/query_sysplorer_help.py` against the active installation. Match FAQ
number and category; compiler/process exit codes are a different namespace.
Report conflicting messages rather than applying a same-number FAQ explanation.
Use `get_lib_model_document` for public component semantics; fall back to
`resources_retrieval` when installed help is unavailable or has no match.
Messages may truncate or be overwritten: claim only evidence attributable to the
current operation. Use `scripts/extract_debug_evidence.py` for anchored excerpts;
`references/external-c-debugging.md` only for a relevant external-C fault.

## Result Contract

Use `references/report-contract.md` for scoped statuses and structured reports.
`diagnosis_complete` means the requested diagnosis is supported without claiming
a repair. `verified_solved` requires only the requested terminal stages and
acceptance, plus original protection and restoration of temporary changes.
Static-only fixes do not require simulation/stop time; result/KPI evidence is
`not_required` unless requested or needed to resolve the reported abnormal result.
Missing required evidence is `verification_required`; repeatable but incomplete
repair is `partially_improved`; an unresolved stop boundary is
`automatic_debugging_stopped`. Do not mistake an untested KPI for a passed KPI.
