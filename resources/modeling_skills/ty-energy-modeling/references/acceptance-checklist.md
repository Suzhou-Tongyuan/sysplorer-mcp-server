# Acceptance Checklist

Use only the items applicable to the requested terminal stage. Parent `../../ty-sysplorer-modeling-rules/workflows/seven-gates-validation.md` owns completion status and Gate 6. Nonrequired runtime/results/plots/animation/formal-report items are `not_required`; they do not block completion of a requested check, translation, or successful simulation.

## Required Gates

- Energy-subsystem library scope respected; parent-selected standard and support-domain components retained
- No unresolved structural errors remain
- No required ports are left unconnected
- `CheckModel` passes when runtime check is in scope; read-only/source-only boundaries are preserved
- `TranslateModel` succeeds when translation is in scope
- Simulation runs when simulation is part of the request
- Required result variables are verified only when result review is in scope; no automatic proxy variables or default verification signal
- Final response includes relevant assumptions, evidence and limitations; a formal report is created only when requested

## Result Judgment

Only required when the request includes result criteria. Otherwise record `not_required` and report simulation status separately. Verify fresh result provenance and preserve interpolation/endpoint warning.

- Functional behavior matches the requested purpose
- Trends are physically reasonable
- Key values or states are numerically acceptable
- Unmet criteria are stated explicitly

## Evidence Quality

- State whether the conclusion is based on check only, translate only, successful simulation, or simulation plus variable review.
- If the result is partial, say so directly instead of claiming completion.
