# Repair Existing Model

## Scope

Use this workflow when the user provides or identifies an existing model and asks to repair connections, parameters, medium selection, check/translate/simulate failures, result behavior, diagram visibility, red dashed wires, dangling endpoints, chaotic routing, or stretched symbols.

## Required Inputs

- Model path, model name, or currently loaded model object.
- Current error, symptom, diagram export, result anomaly, or desired repair target.
- Whether preserving the current topology is required.
- Any known previous working version or benchmark result.

## Execution

1. Existing fault diagnosis follows the parent's debugging route; this domain workflow supplies hydraulic/pneumatic evidence without restarting construction. A failure in a new-build workflow returns to that originating stage after repair.
2. **Gate 1 — scope:** retain the concrete model target, fault, permitted edits, requested endpoint and existing library boundary. Distinguish offline file work, read-only diagnosis and authorized live repair; available tools do not authorize software startup or model changes. Before authorized live checks, read-only diagnosis must account for MCP 0.4 automatic layout writeback; use an authorized copy or state the limitation.
3. **Gate 2 — evidence:** read `references/error-repair-playbook.md`, then `references/common-errors.md` for the observed symptom only. Offline tasks use authorized source files and existing indexes/documents without MCP probing or software startup. For authorized live evidence, use `model_inspect` for model/components/ports, class docs for medium and parameter evidence, and the parent shared standards for session/error handling.
4. Classify the fault: source/input, library/dependency, mapping, medium, topology, capacitor/resistive topology, parameter, initialization, translation, simulation, result variable or graphical annotation. Isolate the shortest failure chain.
5. **Gate 3 — minimal repair:** within authorized edits, change only the responsible fluid subsystem or confirmed interface; preserve selected standard and cross-domain components. Read-only diagnosis produces findings and repair suggestions without applying patches. For graphical symptoms inspect `Placement`, `Line`, `Diagram`, connector anchors and extents before changing physical topology.
6. Apply `references/capacitor-resistive-check.md` when the affected `TYHydraulics` / `TYHydraulicComponents` topology or symptom requires it, retaining the offline/read-only/authorized live mode selected at Gate 1.
7. **Gate 4 — check:** rerun the earliest affected required check after repair. Offline file work repeats static review only; authorized live work records any automatic annotation writeback. Model check failures block dependent runtime actions without granting repair permission, while visual layout findings wait for applicable Gate 6.
8. **Gate 5 — validation design:** rerun only affected translation/simulation stages through the requested endpoint. Read results only when behavior/result acceptance requires them; other result, plot and animation steps are `not_required`.
9. **Gate 6 — diagram acceptance:** changed graphical targets use structured evidence; images are added according to request and capability. Unchanged targets and read-only work use `not_required`; image unavailability does not justify claiming visual inspection or ignoring an explicit request.
10. **Gate 7 — delivery:** record minimal repair, rerun evidence and remaining gaps. Formal reports/templates are optional unless requested; do not force result and diagram work beyond their applicability.

## Failure Handling

- Do not skip from failed `check` to `simulate`.
- Do not treat "model tree has components" as completion when the diagram is invisible.
- Do not perform broad unrelated cleanup before repairing the active failure chain.
- If a required model artifact is missing or inaccessible, stop and state the blocker.

## Delivery Focus

Report only applicable requested evidence, with unrequested stages as `not_required`; formal reports are not required for an ordinary repair.

- Failed gate and symptom.
- Root-cause judgment and repair action.
- MCP actions rerun after repair and their results.
- Result variable verification when behavior was part of the request.
- Diagram review conclusion when graphical repair was part of the request.
- Remaining blockers and next executable action if not fully closed.
