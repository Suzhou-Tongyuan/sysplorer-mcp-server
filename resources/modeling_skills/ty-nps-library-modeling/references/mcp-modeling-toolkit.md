# MCP Modeling Toolkit

Use this file when tool choice is unclear during NPSLibrary work.

## Tool Boundary

- Use Sysplorer MCP for graphical modeling, model creation, component insertion, wiring, parameter placement, `check_model`, `translate_model`, `simulate_model`, result inspection, and model-file lifecycle.
- Use Syslab MCP for script execution, algorithm validation, data processing, and Julia/Python/M-language style computation only when the task explicitly needs those activities.
- Do not route ordinary Sysplorer graphical modeling through Syslab MCP.
- Do not copy Syslab-style error recovery into Sysplorer API work. Repair the Sysplorer call path itself.

## 1. Session And Library

| Task | Preferred Tool |
|------|----------------|
| Ensure Sysplorer is ready | `session_manager(action="ensure")` |
| Inspect health | `session_manager(action="health")` |
| Load `NPSLibrary` | `load_library(library_name="NPSLibrary")` |

## 2. Model Lifecycle

| Task | Preferred Tool |
|------|----------------|
| Create a new model | `model_manager(action="new")` |
| Load a `.mo` file | `model_manager(action="load_file")` |
| Open a model | `model_manager(action="open")` |
| Save a model | `model_manager(action="save")` |
| Read components, ports, or model text | `model_manager(action="get_components" / "get_component_ports" / "get_model_text")` |

## 3. Modeling And Layout

Preferred order:

1. Use official Sysplorer MCP tools first when they can complete the work directly.
2. Use `call_code(mode="run_sysplorer_api")` only for batch or custom Sysplorer scripting that cannot be completed cleanly with the dedicated MCP tools.
3. Use `smart_layout` only when diagram placement or wire layout needs automatic cleanup.

Important rules:

- In `run_sysplorer_api`, always start with `import mworks.sysplorer as ModelingPy`.
- Never assume `ModelingPy` exists implicitly in the script namespace.
- Prefer `call_code(mode="run_sysplorer_api", payload={"python_source": "...", "capture_stdout": true, "capture_stderr": true})`.
- `payload.python_source` must not be empty unless a valid `payload.script_path` is provided.
- If you see `python_source is empty`, payload-shape errors, or JSON encoding errors, fix the `call_code` invocation itself before attempting any modeling fallback.
- For graphical modeling, if `call_code` fails, continue repairing Sysplorer-side modeling calls such as `AddComponent` or `ConnectPort`; do not jump directly to full-text rewrite.
- Do not switch to `SetModelText`, `SetModelCode`, or ad hoc `.mo` text patching until the minimal `run_sysplorer_api` path is proven healthy.

Minimal valid example:

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

## 4. API Usage Rules

- For normal model creation, keep `NewModel` on the default `restriction="model"` path; do not casually switch to `block`, `package`, or other restrictions.
- For `AddComponent`, pass the component class path, instance name, and placement/location arguments required by the API. Do not pass `annotation` as an API argument.
- Prefer injecting component parameters directly into the `.mo` declaration when parameter structure is known.

```modelica
NPSLibrary.xxx.Component comp1(parameterA = 1, parameterB = 2)
  annotation(Placement(transformation(origin={0,0}, extent={{-10,-10},{10,10}})));
```

- For complex `annotation`, `Diagram`, `Icon`, `Placement`, or parameter-panel content, prefer generating or editing the `.mo` file instead of repeatedly calling parameter-setting APIs.

## 5. Check, Translate, Simulate

| Step | Preferred Tool | Typical Purpose |
|------|----------------|-----------------|
| Check | `check_model` | Structure, parameters, and electrical consistency |
| Translate | `translate_model` | Build the mathematical/simulation form |
| Simulate | `simulate_model` | Run the case |
| Result readback | `result_manager` | Read variables, values, and timeseries |
| Plot | `plot_manager` | Plot curves or create animation |

## 6. Search Strategy

1. Read `references/nps_component_quick_index.md` before traversing NPSLibrary directories.
2. Read `references/component_fallback_strategy.md` immediately when `Ground`, `Reference`, `ElectricalReference`, `Neutral`, or `Terminal` primitives are missing.
3. Check `Sysplorer 2026a\Docs\EleLib\Samples\NPSLibrary` first when the user wants an existing example, an official sample, or a model based on a reference case.
4. Use `get_lib_model_document` only when the quick index and samples path do not resolve the specific class.
5. Batch similar component lookups and deduplicate semantically overlapping results.
6. Do not repeat `get_lib_model_document` for the same path in a single modeling task unless new evidence justifies it.

## 7. Recommended Flow

```text
session_manager ensure
-> load_library(NPSLibrary)
-> model_manager new/open/load
-> quick index or sample lookup
-> modeling / wiring / parameter injection
-> check_model
-> translate_model
-> simulate_model
-> result_manager / plot_manager
```

## 8. When To Enter Repair Loop

- `check_model` fails
- `translate_model` fails
- `simulate_model` fails or yields abnormal results
- result verification fails
- `LoadFlowBus` or `Powergui` initialization is inconsistent
- `PLL`, `PWM`, sampling-period, or switching-frequency choices produce unreasonable behavior
