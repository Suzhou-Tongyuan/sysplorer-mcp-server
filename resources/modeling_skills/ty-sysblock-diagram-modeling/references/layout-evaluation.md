# Repeatable Layout Evaluation

Use this reference only when the user explicitly asks to evaluate or improve this skill revision. Never load or run these tests during ordinary Sysblock model construction, repair, audit, or delivery. Production workflow entry points remain the four listed in `SKILL.md`; evaluation-only utilities belong under `tests/`.

## Improvement scorecard

| Dimension | Required result |
|---|---|
| API discovery | known task has `estimated_probe_count=0`; unknown API gets one exact lookup recommendation and no enumeration |
| StateMachine feasibility | a generated task-independent cyclic Chart input produces a plan instead of rejecting the cycle |
| Low-overlap repair | a low-projection transition records translate or scale/push before a two-point orthogonal route |
| Geometry quality | canonical Chart audit passes with zero diagonal, multipoint, overlap, crossing, shared-lane, and label issues |
| Regression safety | ordinary block planning and the saved/readback evidence audit still pass |
| Evidence complexity | one structured-evidence audit report replaces separately persisted per-level audit reports by default |
| Context complexity | workflow references have non-overlapping authority and lower combined line count |
| Scope integrity | SHA-256 inventory of `ty-sysplorer-modeling-rules` is unchanged |

Run `python tests/test_skill.py` for deterministic unit coverage. Then run representative live Sysplorer builds from user-provided requirements, save/reload them, and feed raw evidence to `audit_sysblock_model.py`. Unit tests prove planner/auditor behavior; live tests prove installed API and serialization compatibility. Both are required before publishing a version-sensitive contract update.

Use this mode to test or optimize the layout capability without carrying forward any previous layout result. It is part of this skill but independent from formal model construction.

## Artifacts

1. `input.json`: immutable `sysblock-layout-input/v1`; topology and semantics only.
2. `oracle.json`: `sysblock-layout-oracle/v1`; coordinate-free property assertions only.
3. `result.json`: generated layout result or readback evidence; always bound to the input hash.
4. `evaluation.json`: canonical audit report.

Never merge the oracle into the input. Never store a reference frame, coordinates, chosen rows/layers, anchors, lanes, or route points in either file. An oracle states properties such as zero crossings, preserved topology, horizontal one-to-one interfaces, allowed resize kinds, or orthogonal Chart transitions.

## Test loop

1. Run `layout_input_tool.py audit input.json`; stop on any forbidden geometry or topology defect.
2. Run the candidate planner/layout implementation from the unchanged input.
3. Save the candidate result with `layout_input_sha256` equal to the auditor's canonical hash.
4. Run `tests/tools/evaluate_layout_case.py input.json result.json --oracle oracle.json`.
5. For optimization, rerun from the same input and use `tests/tools/compare_layout_runs.py baseline.json candidate.json`. A candidate may improve compactness only when it does not regress any hard property.

## Coverage classes

Maintain cases for at least:

- primary `Cond -> Chart -> Act` flow plus a generic feedback-path block or SubSystem;
- nested SubSystem bottom-up tightening and independently calculated minimum frames;
- Mux/DeMux or bus fan-in/fan-out with fixed port order;
- StateMachine state tightening and orthogonal transitions, using a task-independent topology.

Do not package fixtures, user models, domain-specific examples, accepted layouts, or golden geometry with the skill. Construct minimal task-independent unit inputs in test code. Generate live cases from user-provided requirements in a temporary test directory and delete them after evaluation unless the user explicitly provides a separate regression repository.

## Required hard properties

- input schema and geometry-free audit pass;
- result input hash matches;
- node/state/edge/transition identity and endpoints match the input;
- only allowlisted object kinds change size;
- block-diagram and Chart canonical audits pass;
- saved/readback structured evidence is present and is not replaced by visual or screenshot evidence.

Compactness metrics are comparative signals, not a license to violate hard properties. Prefer smaller justified canvas/frame area, shorter total route length, and fewer bends only after all hard properties pass.
