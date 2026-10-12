# Sysplorer API Usage

Use this file when the task depends on correct Sysplorer API behavior rather than domain-specific component choice.

## Scope Boundary

- Use Sysplorer MCP for graphical modeling, model creation, component insertion, wiring, parameter placement, check, translate, simulate, and result readback.
- Use Syslab MCP only for script execution, algorithm validation, data processing, and Julia/Python/M-language style work that is explicitly part of the task.
- Do not mix Syslab MCP into ordinary Sysplorer graphical modeling tasks.
- Do not apply Syslab-style error handling to Sysplorer API modeling. Fix the Sysplorer invocation path itself.

## `NewModel`

- For a normal model, keep the default `restriction="model"` path.
- Do not casually switch to `block`, `package`, or other restrictions unless the request explicitly needs a different class type.
- When creating an NPSLibrary-based model, prefer a standard model shell first and add domain components afterward.

## `AddComponent`

- Pass the component class path, instance name, and any required position or placement arguments.
- Do not pass `annotation` as an API argument.
- Treat `AddComponent` as a topology construction step, not as a full source-text replacement step.

## Parameter Writing

Prefer writing known parameters directly in the component declaration inside the `.mo` model text:

```modelica
NPSLibrary.xxx.Component comp1(parameterA = 1, parameterB = 2)
  annotation(Placement(transformation(origin={0,0}, extent={{-10,-10},{10,10}})));
```

Use this pattern when:

- the class path is already known,
- the parameter names are already confirmed, and
- the goal is stable, reviewable model text.

## Complex Annotation And Diagram Data

Prefer generating or editing the `.mo` file for:

- `annotation(...)`
- `Placement(...)`
- `Diagram(...)`
- `Icon(...)`
- parameter-dialog or panel-level structures

Do not rely on repeated parameter-setting API calls for these complex structures.

## Script Invocation Discipline

- In `call_code(mode="run_sysplorer_api")`, always start with `import mworks.sysplorer as ModelingPy`.
- Do not assume `ModelingPy` exists implicitly.
- If `python_source is empty`, payload-shape validation fails, or JSON encoding breaks, repair the `call_code` invocation before attempting modeling fallback.
- For graphical modeling, repair the Sysplorer-side API path before jumping to full-text model replacement.

Minimal health-check example:

```text
call_code(
  mode="run_sysplorer_api",
  payload={
    "python_source": "import mworks.sysplorer as ModelingPy\nRUN_SCRIPT_RESULT = {'ok': True}",
    "capture_stdout": true,
    "capture_stderr": true
  }
)
```

## Recommended Order

1. Confirm Sysplorer session readiness.
2. Load `NPSLibrary`.
3. Resolve class paths from the quick index or samples path.
4. Create the model with `NewModel`.
5. Add components and wire them.
6. Inject stable parameters in `.mo` text when appropriate.
7. Run `check_model`, `translate_model`, and `simulate_model`.
