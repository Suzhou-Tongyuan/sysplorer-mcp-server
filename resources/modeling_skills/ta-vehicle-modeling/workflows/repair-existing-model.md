# Repair Existing Model

Use this workflow when an existing TA vehicle model fails check, translation, simulation, layout-annotation checks, or result validation.

## Task Ownership

Existing concrete failures are led by the independent debugging entry defined in `../../ty-sysplorer-modeling-rules/SKILL.md`. This workflow supplies domain checks only; it does not restart discovery or the complete build pipeline. A failure arising during a new build remains within that original task and returns to its affected gate after repair. Use `../../ty-sysplorer-modeling-rules/references/shared-standards.md` for session, error classification, and retry limits. Check/translate/simulate may write automatic layout to loaded files; preserve read-only boundaries. Retest only the requested, affected stages; result checks and formal reports outside scope are `not_required`.

## Read

1. `../references/requirement-map.md`
2. `../references/error-repair-playbook.md`
3. `../references/common-errors.md`
4. `../references/library-selection.md` and one matching library card when the primary library is unclear
5. `../references/diagram-layout-rules.md` when source-level diagram structure or layout annotations are involved

## Do

- Establish a baseline: model path, primary library, support libraries, and the earliest failed stage.
- Use `error-repair-playbook.md` to classify the fault, identify the shortest active failure chain, and apply TA-library-specific shortcuts.
- Repair along the shortest blocking chain from the skill: library boundary, dependencies, hierarchy/interfaces, topology, parameters, initialization, check/translate, simulation, result variables, diagram annotations.
- Preserve valid existing structure.
- Separate diagnostic edits from final deliverable edits.
- After repair, return evidence to the debugging owner; for a new-build failure, return to the failed parent Step/Gate. Rerun only affected validation within the requested terminal stage.

## Report

- Before final delivery, read `../references/output-contract.md` and answer `../references/acceptance-checklist.md`; do not report completion if any acceptance item fails.
- Baseline, failed stage, repair hypothesis, changed files/model classes, retest result, remaining blockers, and next action.
