# Phase Output Templates

Use only the section that matches the current workflow stage. Keep the structure, but replace placeholders with task-specific content.

## Requirement Understanding

```md
### Requirement Understanding
- Modeling target:
- System type:
- Modeling objective:
- Main power path:
- Control strategy:
- Operating conditions:
- Input signals:
- Expected output observations:
- Key constraints:
- Library choice:
- Success criteria:
- Current information gaps:
```

## Component Mapping

```md
### Component Mapping
| Function or subsystem | Selected class or block | Source sub-library | Same-name or equivalent | Reason |
|-----------------------|-------------------------|--------------------|-------------------------|--------|
|                       |                         |                    |                         |        |

### Mandatory Supporting Blocks
- Ground or reference:
- Powergui or equivalent:
- Boundary conditions:
- Sensors and probes:
- Interface conversion blocks:
```

## Parameter Table

```md
### Parameter Table
| Parameter | Value | Unit | Source category | Evidence or rationale |
|-----------|-------|------|-----------------|-----------------------|
|           |       |      |                 |                       |
```

## Key Assumptions

```md
### Key Assumptions
- Assumption:
  Value:
  Impact:
```

## Model Construction

```md
### Model Construction Status
- Main power path implemented:
- Control path implemented:
- Supporting blocks added:
- Outstanding advanced details:
- Diagram reviewability status:
- Diagram export or layout action taken:
```

## Check Result

```md
### Check Result
- Model name:
- Check tool used:
- Check status:
- Key structural findings:
- Port-domain findings:
- Missing or corrected support blocks:
- Diagram review result:
- Next action:
```

## Translate Result

```md
### Translate Result
- Model name:
- Translation tool used:
- Translation status:
- Initialization findings:
- Structural findings:
- Sampling or discrete-control findings:
- Repair actions taken:
- Next action:
```

## Simulate Result

```md
### Simulate Result
- Model name:
- Simulation status:
- Solver / Algorithm:
- InlineIntegrator:
- InlineStepSize:
- Step size / IntegratorStep:
- Output interval:
- Switching period:
- Sampling period:
- Control period:
- Relationship among solver, step, and sampling:
- Key variables extracted:
- Actual successful tool actions:
- Result file or result context:
- Next action:
```

## Result Verify

```md
### Result Verify
- Functional correctness judgment:
- Trend reasonableness judgment:
- Numerical acceptability judgment:
- Comparison with target or reference:
- Diagram reviewability judgment:
- Acceptance grade:
- Residual risks:
- Next action:
```

## Delivery Summary

```md
### Delivery Summary
- Model files:
- Topology summary:
- Key parameters:
- Solver and simulation setup, including `Algorithm=InlineImplicitEuler` evidence:
- Diagram review result:
- Key observed variables:
- Actual successful tool actions:
- Acceptance grade:
- Known limitations:
- Recommended next step:
```
