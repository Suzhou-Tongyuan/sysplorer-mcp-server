# Verify Example

## Scope

Use this workflow when the user asks to verify an official example, enterprise example, or existing reference model through real Sysplorer execution.

## Required Inputs

- Example class name, model name, or file path.
- Requested verification depth: check only, check plus translate, full simulation, result review, diagram review/export, or reuse assessment.
- Target variables, expected behavior, or acceptance criteria when available.
- Whether the user wants only verification or a follow-up user-owned model derived from the example.

## Execution

1. **Gate 1 — scope:** confirm example identity, requested check/translate/simulate/result/image depth and whether edits are allowed. Read-only verification must first consider MCP 0.4 automatic layout writeback; use an authorized copy or document the limitation.
2. **Gate 2 — evidence:** use `references/component-map.md` to identify system vs component-design library, medium and public interfaces. Read `references/manual-knowledge.md` only if concise evidence is insufficient; preserve the selected project library set and fixed `Modelica 4.0.0.TY.1` commercial dependency.
3. Session/tool confirmation is a prerequisite governed by the parent shared standards. Load only required TY and medium libraries when real execution needs them.
4. **Gate 3 — construction:** mark `not_required` for unchanged examples. If authorized edits are necessary, use the repair workflow for the minimal change rather than silently rebuilding the example.
5. **Gate 4 — check:** run the requested check against the exact target and retain actual results. Apply `references/capacitor-resistive-check.md` only when the affected library/topology or requested validation needs it, preserving the original offline/read-only/authorized live mode. Read-only findings do not trigger model patches; any repair requires authorization and affected rechecks.
6. **Gate 5 — validation design:** translate and simulate only as requested or required by the selected runtime path. Simulate-only stops without inventing result variables; read `result_manager` and apply result rules only when results/KPI/curves are in scope.
7. **Gate 6 — diagram acceptance:** unchanged/read-only examples use `not_required` for change acceptance. An explicit diagram review/export request still receives its requested evidence; structured evidence is the basis and images supplement it by request and capability. Actual graphical edits, including automatic layout writeback, enter full applicable Gate 6.
8. **Gate 7 — delivery evidence:** state actual requested actions, limits and any remaining explicit image request. If reuse was requested, distinguish reusable knowledge from a user model that must be built/changed separately; a formal report is generated only when requested.

## Failure Handling

- An example is not validated until the requested MCP actions actually succeed.
- Do not silently turn an example wrapper or `extends` chain into the final user model.
- If the example requires unavailable libraries or a broken session, state the exact blocker.
- If the example runs but results are physically implausible, enter the repair loop or report verification failure.

## Delivery Focus

Select only requested verification fields; other stages use `not_required`. This summary does not add result reads or image exports.

- Example target and actual library/dependency path.
- Actual Sysplorer version and TY libraries used.
- MCP actions executed and their success/failure.
- Key result variables and judgments only when requested; otherwise `not_required`.
- Diagram review status when applicable.
- Reuse scope, limitations, and next steps for converting the example into a user-owned model.
