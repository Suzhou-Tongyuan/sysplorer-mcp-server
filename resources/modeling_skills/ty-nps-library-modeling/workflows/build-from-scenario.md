# Workflow: Build from Scenario

Use this workflow when the user gives a typical electrical scenario, a topology name, or only partial requirements such as "build a grid-tied inverter" or "set up a three-phase supply network."

## Inputs

- User requirement text, notes, or source files
- Optional scenario JSON from `templates/scenarios/scenario_index.json`
- Optional existing model fragments

## Step 1: Pick or Normalize the Scenario

- Identify whether the task matches a known family such as three-phase supply network, Boost converter, grid-tied inverter, motor drive, or load-flow network.
- If a matching JSON template exists under `templates/scenarios/`, use it as the minimum requirement scaffold.
- If there is no exact template, normalize the user request into the same fields used by the scenario templates.

## Step 2: Freeze the Minimum Closed Loop

- Define the main power path first.
- Define the minimum control path required to make the topology meaningful.
- List mandatory support blocks such as `Ground`, `Powergui`, sensors, and boundaries.
- Write the `Requirement Understanding` and `Component Mapping` outputs before building.

## Step 3: Complete Critical Parameters

- Fill only the parameters required for a first runnable model.
- Record whether each value is user-specified, document-derived, case-based, or assumed.
- For electrical cases, make voltage type, frequency, switching frequency, sampling period, control period, and selected simulation step explicit.
- For every simulated NPSLibrary case, choose the step for the mandatory inline implicit Euler experiment annotation before building proceeds to gates.

## Step 4: Build the Skeleton Model

- Start with the main power path.
- Add the minimum sensing and control chain.
- Keep the diagram reviewable from the first pass.
- Prefer the minimal model skeleton under `templates/modelica/minimal-nps-model.mo.tpl` when starting from scratch.
- Keep the model-level `annotation(experiment(...))` present and set to `Algorithm=InlineImplicitEuler` in the skeleton or generated `.mo` text.

## Step 5: Make the Diagram Reviewable

- Add or repair `Placement(...)`, `Line(points=...)`, and `Diagram(coordinateSystem(...))`.
- Keep power, sensing, and control lines visually distinguishable.
- Export the diagram or use `smart_layout` plus export once.

## Step 6: Run Check and Translate

- Before `check_model`, inspect the latest model text and confirm that the model-level experiment annotation contains `Algorithm=InlineImplicitEuler`, `InlineIntegrator=true`, and matching `Interval` / `IntegratorStep` values.
- If the model is still on Dassl or has no explicit experiment annotation, repair the `.mo` annotation before proceeding.
- Run `check_model` first.
- If `check` fails, enter the repair loop before translation.
- After `check` passes, run translation and solve structural or initialization issues before simulation.

## Step 7: Run the First Simulation

- Start from the mandatory NPS simulation baseline: inline implicit Euler with `Algorithm=InlineImplicitEuler` in the model-level experiment annotation.
- Record solver, `InlineIntegrator`, `Interval`, `IntegratorStep`, and the relationship among switching period, sampling period, and control period.
- If simulation results are abnormal, first verify that the latest model text is not using Dassl and that the required experiment annotation was actually applied.
- Extract the minimum key observables for the chosen scenario family.

## Step 8: Verify Against the Scenario Goal

- Compare functional behavior against the scenario objective.
- Grade the result using `references/acceptance-checklist.md`.
- If only the minimum closed loop passes, mark it accordingly instead of over-claiming completion.

## Step 9: Package Delivery

- Use `templates/acceptance-report-template.md` for acceptance evidence.
- Use `templates/delivery-template.md` for the final delivery summary.
- Record topology, parameter baselines, diagram review result, successful tool actions, and known limitations.
