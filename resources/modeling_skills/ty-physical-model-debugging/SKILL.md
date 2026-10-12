---
name: ty-physical-model-debugging
description: >-
  Independently diagnose or repair failures in existing Sysplorer Modelica physical models,
  including checks, translation, generated-solvers, initialization, state
  selection, index reduction, nonlinear systems, events, runtime numerics, and
  external C functions. Use when a concrete failure or abnormal result exists;
  do not use for ordinary model construction, domain design, or API lookup.
metadata:
  short-description: Debug existing Modelica physical models
  version: 1.1.0
  managed-by: sysplorer-mcp
---

# Physical Model Debugging

Use evidence to diagnose, or repair one verified task-owned copy. Record source
and working identities separately; preserve package/resource references, public C
signatures and experiment settings. Before physical-model edits or delivery,
load applicable `ty-sysplorer-modeling-rules` constraints, including Gate 6 for
changed graphical targets. Pure log diagnosis does not load its full workflow.

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

For a simple single-file or single-package fault, keep the workflow near 12
external calls when practical.

1. Read the staged source and SHA-256 once. Do not scan Git, unrelated
   directories, helper source, or large generated artifacts.
2. Extract every functional acceptance invariant supplied by the user, including
   values, signs, units, ranges, stop time, and KPIs.
3. Confirm the target through Sysplorer MCP before first live access: use
   `session_manager(action="probe")` when available, then `health`. Reuse valid
   same-session evidence; recheck after a switch, disconnection or infrastructure
   symptom. Offline artifact inspection needs no session call. Resolve unknown
   API contracts before calling; do not enumerate all APIs.
4. Reproduce once through the first failed stage:
   `check -> translate -> initialize/simulate`. Stop at the first failure.
5. Form one falsifiable hypothesis, make one minimal reversible patch in the work
   copy, and read back the exact change.
6. Rerun the affected stage and the requested terminal chain after its cheaper
   prerequisites pass. Static-only acceptance does not require simulation.
7. Verify original hashes and temporary-settings restoration. Verify end time
   for required runtime acceptance and KPIs only when requested or necessary to
   resolve the reported abnormal result; otherwise mark them `not_required`.

Stop after the same infrastructure failure occurs twice. Do not compensate for a
model defect by changing the solver, tolerance, step size, assertions, event
semantics, or generated code without direct causal evidence.

If the observed baseline fails at an earlier stage than the reported or
manifested fault, and the diagnostic does not attribute that earlier failure to
the model, stop with `verification_required`. Report the environment mismatch;
do not patch source merely because static inspection suggests a plausible bug.

## Stage Gates

1. **Check failure:** capture the first blocking diagnostic and source location.
   Rerun `check_model` only; do not translate.
2. **Translation or generated-solver failure:** after check passes, capture the
   first diagnostic attributable to this translation/build. Rerun check and
   translation only; do not simulate.
3. **Initialization failure:** inspect assertions, domains, missing or illegal
   start values, selected states, nonlinear iteration variables, and initial
   residual evidence for the failed system only.
4. **Runtime failure:** record the first failure time, stage, variable/system,
   nearest prior event or accepted step, and the smallest window that crosses the
   original failure time.
5. **External C:** correlate the Modelica declaration, resource mapping, public
   signature, first compile/link/runtime evidence, and user-provided `.c/.h`.
   Before the first source edit, derive the complete reachable input domain from
   declarations, initialization/default values, events, and probe calls. One
   patch must remove the evidenced defect for that domain, not only for the
   sampled failing value.

Use the check/translate wrapper diagnostic as the primary evidence. If runtime or
build output is truncated, use at most one immediate bounded retrieval that keeps
the target command and message capture attributable to the same run. Never claim
that a complete structured first error is available when the MCP cannot prove it.

## Help Escalation

Reuse known current API contracts. Resolve unknown names, parameters and return
types with targeted `get_api_document` before calling. For empty/failed docs, use
the exact-name MCP Help/signature fallback in the main skill's
`references/shared-standards.md`; do not guess a write or treat empty docs as absence.

- For a product diagnostic candidate, read `references/help-doc-index.md` and run
  `scripts/query_sysplorer_help.py` against the current installation with the
  exact `--error-code` and category. Keywords are optional context checks. Do not
  map compiler/process `error code: n`, API return codes, or a conflicting
  same-number FAQ page to a model error; use the first specific nested diagnostic.
  Return at most five matches and 12,000 characters.
- Re-query a known API only when its current contract is no longer valid.
- Use `get_lib_model_document` for public component semantics.
- Fall back to `resources_retrieval` only after installed help is unavailable or
  has no match. If all sources fail, report the evidence gap instead of inferring
  an explanation from a similar code.

## Reversible Changes

Read `references/current-mcp-recipes.md` before creating a model copy, projecting
settings, editing model text, or coordinating a multi-file C workspace. Every
write must have a captured old value and an executable inverse operation.

Directly evidenced automatic changes may include:

- syntax, type, dimension, reference, resource URI, or external declaration
  errors;
- illegal or missing `start` values, and `nominal` values supported by scale
  evidence;
- `StateSelect.prefer/avoid` changes supported by state-selection evidence;
- parameters that directly violate a documented component domain or user
  constraint;
- user-owned `.c/.h` signature, resource, bounds, null-handling, or symbol defects
  anchored by compiler, stack, or minimal-reproduction evidence.

Honor existing authorization for an evidenced edit. Seek user judgment when a
new change to equations, degrees of freedom, topology, boundaries, algorithms,
public ABI or third-party source changes the agreed design or scope. Do not ask
again merely because an already requested correction involves equations. Never
modify protected library source.

## Initialization and Runtime Numerics

Use this order and read `references/initialization-and-runtime.md` only when the
simple evidence is insufficient:

1. Illegal/missing starts, domains, and physical operating point.
2. State selection, index reduction, and derivative relationships.
3. Nonlinear iteration variables, scale, residuals, and post-event constraints.
4. Clearly illegal physical parameters.
5. One mechanism-based algorithm/event/step comparison only as a sensitivity
   experiment, followed by final verification with the original settings.

Use a bounded nonlinear-solution summary before high-frequency iteration logs.
Enable event, dynamic-state, singular-system, or user-C diagnostics only when the
current hypothesis needs that evidence.

## Deep Evidence

Do not open RMF, Flat Model, Variables.xml, RuntimeDebug C, generated C, dumps, or
large logs on the fast path. If lightweight evidence cannot map the failing
variable/system to editable source, state the anchors and byte budget and read
`references/deep-debugging.md` for authorized bounded inspection. Reading user-owned
evidence within the existing task needs no separate approval. Do not inspect
protected commercial implementation, including through generated artifacts.

Search in this order: Variables.xml -> RMF -> Flat Model -> RuntimeDebug C. Use
`scripts/extract_debug_evidence.py` and return only bounded excerpts around an
error code, variable, system, function, or source-line anchor. Evidence that
cannot be paired with the current model, settings, and run must not support a
conclusion.

## Acceptance

Read `references/report-contract.md` for reporting and status semantics.
For `diagnose_only`, report `diagnosis_complete` only when the requested diagnosis
has supporting evidence, without claiming a repair; otherwise report the gap.
For repair, require the changed value/source to be read back, required static and
terminal stages to pass using the patch, originals to remain unchanged, and
temporary settings to be restored. A static-only fix needs no runtime stop time.
Runtime acceptance reaches the agreed original stop time with baseline settings.
Verify physical behavior/KPIs when requested or needed to resolve abnormal results;
otherwise mark them `not_required`. Missing required evidence is
`verification_required`, not `verified_solved`.

Two rounds without reproducible improvement stop the current hypothesis; continue
authorized targeted evidence or minimal-case isolation when useful. Distinguish
this from repeated infrastructure failure and do not retry merely to meet a count.
