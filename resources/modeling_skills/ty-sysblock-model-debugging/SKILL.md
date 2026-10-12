---
name: ty-sysblock-model-debugging
description: >-
  Independently diagnose or repair failures in existing Sysplorer Sysblock diagrams,
  including components, ports, connections, parameters, sample times,
  simulation, code generation, generated solvers, and CCaller source/configuration.
  Use for a concrete failure or abnormal result; do not use for new diagram
  construction, routine layout, controller tuning, or pure API lookup.
metadata:
  short-description: Debug existing Sysblock models and CCaller
  version: 1.1.0
  managed-by: sysplorer-mcp
---

# Sysblock Model Debugging

Use official structured APIs for topology and parameters in one verified
task-owned copy. Record source/working identities and preserve target settings.
For ordinary Sysblock edits/delivery, reuse `ty-sysblock-diagram-modeling` API,
layout, save/reload and audit constraints; add signal-skill constraints only for
relevant signal tasks. Only physical-top-level changes need the physical modeling
skill. Loading constraints never reroutes or restarts this debug workflow.
Ordinary construction, editing, layout and tuning remain with their existing skills.

## Task Mode and Applicable Constraints

Enter directly from a concrete fault; neither the modeling router nor the debug
router is a prerequisite. Select `diagnose_only` or `repair` from the request.
In diagnose-only mode, inspect and, only if authorized, reproduce the needed
stage; report the cause or evidence gap and stop without a patch. Offline review
does not authorize execution. Repairs follow the workflow below.

Record the requested terminal stage and user acceptance before execution. Reuse
the existing attributable baseline, valid session, and task-owned working copy;
do not reroute, replan, or recreate them when loading another skill's constraints.
Construction-stage debugging returns to the original construction task.

## Fast Path

For a simple single-model or anchored CCaller fault, keep the workflow near 12
external calls when practical.

1. Read the staged model identity, structured state, source files, and hashes
   once. Do not scan Git, unrelated directories, helper source, or all API docs.
2. Extract every user acceptance invariant, including expected values, signs,
   units, ranges, sample times, stop time, and KPIs.
3. Confirm the target through Sysplorer MCP before first live access: use
   `session_manager(action="probe")` when available, then `health`. Reuse valid
   same-session evidence; recheck after a switch, disconnection or infrastructure
   symptom. Offline artifact inspection needs no session call. Resolve unknown
   API contracts before calling; do not enumerate all APIs.
4. Read only the failed block, direct neighbors, relevant ports/connections,
   parameters, and target configuration.
5. Form one falsifiable hypothesis. Apply one minimal structured model change or
   one user-source patch, then read back the changed value/source and hash.
6. Rerun the affected stage and final functional acceptance. Build or simulation
   success alone is insufficient when the KPI is wrong.

Stop after the same infrastructure failure occurs twice, when the old value is
unreadable, when rollback cannot be verified, or before a new material control-design
change outside existing authorization. Do not re-request already granted approval.

If the observed baseline does not reach the reported or manifested fault stage,
and no current diagnostic attributes the earlier failure to the model, stop with
`verification_required`. Do not infer success from code generation when the
required terminal stage is generated-solver compile/link.

## Stage Gates

1. **Open/check:** verify model FQN, `restriction="Sysblock"`, component names,
   ports, connections, and the first available blocking diagnostic. Do not
   proceed while check fails.
2. **Simulation:** inspect parameters, sample times, algebraic loops, illegal
   operations, events, and the minimum signal neighborhood needed by the KPI.
3. **Code generation:** distinguish unsupported blocks/data types/continuous
   states, sample-time constraints, target configuration, and structural errors.
4. **Generated solver:** code generation success is not link success. Use the
   first attributable preprocess, compile, or link diagnostic as the anchor.
5. **CCaller:** correlate the complete structured CCaller configuration, external
   C resources, public function signature, argument mapping, user source, and the
   actual failed terminal stage.

Do not assume that `simulate_model`, `GenerateModelCode`, or another command is
the universal generated-solver path. Start from the stage that actually fails in
the user's workflow and verify the same terminal stage after the patch.

## Help Escalation

- For a product diagnostic candidate, read `references/help-doc-index.md` and use
  `scripts/query_sysplorer_help.py` against the current installation with the
  exact `--error-code` and category. Keywords are optional context checks. A
  compiler/linker/process `error code: n` is a different namespace: diagnose its
  first specific nested message and never substitute a conflicting FAQ entry.
  Return at most five matches and 12,000 characters.
- Reuse known current contracts. For an unknown API use the diagram skill's
  `scripts/api_contract_resolver.py` and `references/runtime-contracts.md` before
  calling; query exact documentation and use its empty-document fallback. Do not
  probe a write on the target or enumerate all APIs. Use `get_lib_model_document`
  for public block semantics.
- Fall back to `resources_retrieval` only when installed help is unavailable or
  has no match. Report an evidence gap when all sources fail.
- Current message APIs may truncate or overwrite diagnostics. Report only the
  first blocking evidence attributable to the current operation.

## Structured and Reversible Editing

Read `references/current-mcp-recipes.md` before creating a work copy or editing
structured state. Read `references/sysblock-diagnostics.md` only when the first
error and immediate topology/configuration evidence do not identify the defect.

- Never use `SetModelText`, handwritten Modelica, `connect()`, or generated-file
  edits for Sysblock topology.
- Snapshot components, ports, connections, scalar parameters, complete parameter
  DataClasses, external-resource lists, and target settings that the change may
  affect.
- Treat complex parameter objects and external-resource lists as whole values:
  merge the intended field, write once, and read back the relevant fields.
- Each write requires an executable inverse operation. If the old value cannot be
  read or restored, do not write automatically.
- Do not edit wrappers, generated C, project files, solver directories, or
  protected third-party source.
- For topology/layout changes use the diagram skill's planning and structured
  geometry readback. Save and reopen/force-reload changed models before final
  structural audit; a simulation pass is not saved-model evidence. Pure user-C
  changes do not trigger layout edits. Read-only diagnosis does not mutate a model.

## CCaller and User C Source

Read `references/external-c-debugging.md` only after structured CCaller evidence
and the first build/runtime diagnostic are insufficient.

1. Preserve the declared public signature, argument order, directions, types,
   dimensions, array layout, sample time, resource registration, and user KPIs.
2. Patch only a verified user-owned work copy of `.c/.h` source.
3. Fix only defects supported by direct evidence, such as signature mismatch,
   missing resource registration, unresolved implementation symbols, null or
   bounds errors, or incorrect argument mapping.
4. Never invent a constant or remove an external dependency merely because a
   test value is known. An unresolved symbol requires its intended definition,
   correct linkage, or an explicit user-approved design change.
5. Rebuild and verify the requested terminal stage. Validate actual function
   results/downstream KPIs when the request requires functional recovery or an
   abnormal result; a link-only fix does not automatically require simulation.

## Acceptance

Read `references/report-contract.md`. Diagnose-only completion reports the cause
and supporting evidence without claiming a repair. A verified repair requires
changed topology/configuration readback, applicable saved-model audit, required
check and terminal simulation/codegen/build stages, original protection and
temporary-settings restoration. Codegen success is not compile/link success.
Only runtime acceptance requires the agreed stop time; only requested or
fault-dependent result acceptance requires KPIs. Mark other result checks
`not_required`; missing required evidence is `verification_required`.

Two rounds without repeatable improvement stop the current hypothesis. Continue
authorized targeted evidence/minimal-case isolation rather than repeating guesses
or discarding the remaining task. Keep infrastructure and model failures separate.
