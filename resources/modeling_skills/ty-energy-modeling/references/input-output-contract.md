# Input and Output Contract

This file defines the minimum information needed to start and the minimum evidence required to finish.

## Minimum Input Expectation

At least identify or explicitly mark as unknown:

- System family or topology
- Modeling objective
- Allowed-library scope
- Requested terminal stage and result criterion when in scope
- Key ratings, operating conditions, or boundary conditions

If these are missing, the requirement-understanding step must surface them as gaps instead of guessing silently.

## Mandatory Delivery Output

In the final response, include applicable fields only; use `not_required` for out-of-scope result, layout or runtime stages. Formal documents are generated only when requested. Include:

- Model file path or model name
- Topology and subsystem summary
- Library usage summary
- Component mapping summary
- Key parameters and assumption sources
- Solver, step size, stop time, and control or sampling periods when applicable
- Diagram review result
- Actual successful tool actions
- Key observed variables and provenance/warning only when result review is in scope; otherwise `not_required`
- Verification conclusion
- Acceptance grade
- Known limitations
- Recommended next step

## Reporting Rules

- Do not claim successful completion without stating the evidence level.
- Do not summarize only the final conclusion; include the path taken.
- If the work stopped early, state the last passed gate and the current blocker.
- If a parameter is assumed, state that it is assumed and why it is acceptable for the current stage.
