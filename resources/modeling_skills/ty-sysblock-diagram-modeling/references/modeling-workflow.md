# Sysblock Modeling Workflow

This file defines only the end-to-end stage order and delivery evidence. API contracts belong in `runtime-contracts.md`; geometry algorithms belong in `layout-workflow.md`; Chart details belong in `state-machine.md`.

When used by `ty-sysblock-model-debugging`, inherit its established task mode,
terminal stage, baseline and working model. Apply only the relevant edit/save/
audit constraints below, then return to the debugger without routing again.
Diagnose-only inspection does not start this mutation workflow; pure C-source
changes do not create model-layout work. Here parent-required means the current
request and applicable modeling constraints, not an automatic full physical workflow.

## 1. Route and freeze

Confirm that the task is concrete Sysblock work. Freeze model boundary, inputs/outputs, names, types, dimensions, units, sample time, behavior, priorities, solver intent, verification cases, and affected hierarchy. If architecture or requirements are still undecided, return to the upstream MBD contract before editing.

Classify the change:

- parameter-only;
- topology;
- layout;
- StateMachine;
- repair;
- audit-only;
- delivery/reverification.

Topology/layout builds require pre-layout evidence. Parameter-only and audit-only work do not invent it retroactively.

## 2. Resolve the minimum API set

List exact APIs the task will call. Use `api_contract_resolver.py`; known contracts proceed with zero probes. Apply the bounded fallback from `runtime-contracts.md` only to unresolved entries.

## 3. Plan structure and layout

For topology/layout changes:

1. create and audit a geometry-free layout input;
2. plan every affected level and Chart;
3. audit plans and bind them to the canonical input hash;
4. preserve the complete hierarchy list for final coverage comparison.

Use the layout tools and rules in `layout-workflow.md`.

### Single-core Chart side-port half-step formula

For an unrotated Chart centered at `(cx, cy)` with planned size `W x H`, compute each side independently for `N` ports ordered top-to-bottom, using zero-based index `i`:

```text
step = H / N
y_i = cy + H / 2 - (i + 0.5) * step
input_x = cx - W / 2
output_x = cx + W / 2
```

Larger `y` is higher. Treat these as planned anchors and verify them against force-reloaded frame or accepted static-annotation geometry.

## 4. Build through official APIs

Create/open the correct task-owned model, add full-path `SysplorerEmbeddedCoder` components, set parameters, refresh variable ports, and connect with `ConnectPort`. Check each API return before making a dependent call.

Build the minimum runnable signal chain before adding optional complexity. For repairs, fix the shortest failure chain needed to reach the next failed validation. Keep semantic loop breaking separate from visual feedback routing.

## 5. Check and verify

Execute the validation required by the parent modeling workflow. At minimum:

- structural check after relevant changes;
- applicable translation/simulation;
- behavior tests at all required boundaries;
- clean warnings only when clean-delivery scope requires it;
- saved/readback layout audit and required diagram review before long simulation or delivery;
- required delivery evidence and handoff.

For discrete timing, test cold start, threshold-minus-one, exact threshold, threshold-plus-one, and release behavior. Do not label a one-sample shift a defect without an integer-tick execution table.

## 6. Save, reload, and collect final evidence

Use the save mode and safe reload sequence from `runtime-contracts.md`. Recursively enumerate the final hierarchy root-to-leaf. Collect structured evidence for:

- model file and current hash;
- change scope and affected levels/Charts;
- layout input and hash when required;
- pre-layout plan results when required;
- structural check and warnings;
- final hierarchy coverage;
- final level manifests and Chart layouts from accepted readback sources;
- connection integrity;
- parent-required translation, simulation, and testing status.

Do not persist separate preconnect/readback manifests by default. They may remain temporary while composing the raw evidence object.

## 7. Audit saved/readback evidence

Run:

```text
python scripts/audit_sysblock_model.py \
  --model-file <absolute-model.mo> \
  --evidence <raw-evidence.json> \
  --output <final-report.json>
```

Exit code 0 confirms that the local structured-evidence audit found no failure. The auditor recomputes canonical layout checks and stale-evidence checks; it does not trust project-authored pass flags and does not replace parent-required diagram review, translation, simulation, or testing.

## Delivery record

Report:

- model name, absolute path, and final hash;
- task/change scope and `SysplorerEmbeddedCoder` scope;
- solver/simulation parameters when applicable;
- structural check, warning, translation, simulation, and test results required by scope;
- audit report path and status;
- failure codes and the first actionable failure if incomplete;
- unresolved risks.

Never claim completion when hierarchy coverage, final readback, connection integrity, evidence freshness, or required tests are missing.
