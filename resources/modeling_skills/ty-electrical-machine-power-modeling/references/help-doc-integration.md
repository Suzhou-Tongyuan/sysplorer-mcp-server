# Help Doc Integration

Help-document work starts only after the component and its tests are already stable.

## Pre-Conditions

Before writing help content, confirm:

- all user-adjustable parameters are exposed in the parameter panel
- every parameter has a Chinese comment
- every external interface has a Chinese comment
- units and physical meaning are clear where needed
- the main equations, discrete logic, and initialization logic are stable
- at least `2` component tests are completed when the deliverable is a reusable component

## Tool Rule

- If `$sysplorer-help-doc-writer` is available, use it after the model and tests are stable.
- If `$sysplorer-help-doc-writer` is unavailable, generate a local Markdown help draft from the same inputs and report that formal help-document integration is blocked.

## Inputs To Prepare

At minimum prepare:

- component `.mo` file path
- component package path
- parameter list
- interface list
- principle summary
- test summary
- icon or annotation notes if relevant

## Expected Sections

Help content should normally cover:

- model path
- functional overview
- parameter description
- interface description
- typical use
- constraints and cautions
- principle summary
- test or example summary

## Important Rule

Do not generate formal help content before parameters and interfaces are annotated cleanly. That only pushes rework downstream.
