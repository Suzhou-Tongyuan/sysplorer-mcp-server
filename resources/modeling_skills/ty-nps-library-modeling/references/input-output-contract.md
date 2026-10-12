# Input and Output Contract

This file defines the minimum information needed to start and the minimum evidence required to finish.

## Minimum Input Expectation

At least identify or explicitly mark as unknown:

- Topology or system family
- Modeling objective
- Library choice
- Main expected results
- Key ratings or operating conditions

If these are missing, Step 2 must surface them as gaps instead of guessing silently.

## Mandatory Delivery Output

The final delivery package should include:

- Model file path or model name
- Topology summary
- Component mapping summary
- Key parameters and assumption sources
- Solver, step size, switching period, sampling period, and control period when applicable
- Diagram review result
- Actual successful tool actions
- Key observed variables and why they matter
- Verification conclusion
- Acceptance grade
- Known limitations
- Recommended next step

## Reporting Rules

- Do not claim successful completion without stating the evidence level.
- Do not summarize only the final conclusion; include the path taken.
- If the work stopped early, state the last passed gate and the current blocker.
- If a parameter is assumed, state that it is assumed and why it is acceptable for the current stage.
