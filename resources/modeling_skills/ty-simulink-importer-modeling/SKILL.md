---
name: ty-simulink-importer-modeling
description: >-
  Use this skill for Sysplorer SimulinkImporter Python API tasks: opening the
  importer toolbox, importing Simulink (.slx) models into Sysplorer as Sysblock
  models, configuring export paths, Link subsystem libraries, and data files.
  Do not use this skill for general Modelica/Sysblock modeling, DesignOpt
  toolboxes, or CAD toolbox tasks.
metadata:
  short-description: SimulinkImporter model import Python API guidance
  version: 1.0.0
  managed-by: sysplorer-mcp
---

# SimulinkImporter

## Scope

- **In scope**: Sysplorer SimulinkImporter toolbox scripting: `OpenSimulinkImporter`, `CloseSimulinkImporter`, `ImportSimulinkModel` for importing `.slx` files (R2017b–R2024b) into Sysplorer as Sysblock models.
- **Out of scope**: General Modelica/Sysblock modeling, DesignOpt batch simulation/optimization/sensitivity, CAD toolbox operations.
- **Routing priority**: When the user wants to import a Simulink model, use the `SimulinkImporter` interfaces in this skill first.

## Hard Rules

1. **Session first**: call `session_manager(action="health" | "ensure")` before any `run_sysplorer_api` that touches Sysplorer.
2. SimulinkImporter is an independent toolbox module. Do not query it via main ModelingPy `get_api_document`; use explicit import plus `ListFunctions()` / `help()` and this skill's `references/`:

```python
import mworks.sysplorer.SimulinkImporter as slxImporter
print(slxImporter.ListFunctions())
help(slxImporter.ImportSimulinkModel)
```

3. **Always** call `OpenSimulinkImporter()` before `ImportSimulinkModel()`. Call `CloseSimulinkImporter()` after all imports are complete to release resources.

## Tool Map

| Need | Tool / action |
|---|---|
| Sysplorer readiness | `session_manager` |
| Run importer script | `call_code` (`mode="run_sysplorer_api"`) |
| Model open / save / unload | `model_manager` |
| Detailed local docs | `references/SimulinkImporter.md`, `references/批量导入使用说明.md`, `references/批量导入demo说明.md` |

## Canonical Workflow

1. Ensure Sysplorer is ready.
2. Load the Sysblock library:

```python
import mworks.sysplorer as eng
eng.LoadLibrary("SysplorerEmbeddedCoder")
```

3. Open the importer toolbox:

```python
import mworks.sysplorer.SimulinkImporter as slxImporter
slxImporter.OpenSimulinkImporter()
```

4. **Check for data files** in the same directory as the `.slx` model. If a `.slxdata` or other data file is found in the model's path, ask the user whether to import it before proceeding.

5. Import referenced models (with Link subsystem libraries) **first**. Skip this step if there are no referenced/sub-models:

```python
slxImporter.ImportSimulinkModel(
    SimulinkFilePath="H:/svpwm_section.slx",
    LibraryPath="H:/custom_libs",
    OpenReport=False,
)
```

6. Import the main model (with data file) **second**:

```python
slxImporter.ImportSimulinkModel(
    SimulinkFilePath="H:/SVPWM.slx",
    ExportPath="H:/output/",
    LibraryPath="H:/custom_libs",
    DataFilePath="H:/SimulinkImport_SVPWM_Data.slxdata",
    ClearBaseWorkSpace=True,
    OpenReport=False,
)
```

7. Close the importer:

```python
slxImporter.CloseSimulinkImporter()
```

## API Summary

| Function | Description |
|---|---|
| `OpenSimulinkImporter()` | Start the importer, validate license, initialize telemetry |
| `CloseSimulinkImporter()` | Close the importer, finalize telemetry |
| `ImportSimulinkModel(...)` | Import a `.slx` model into Sysplorer |
| `ListFunctions()` | List all available functions |

## ImportSimulinkModel Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `SimulinkFilePath` | `str` | (required) | Absolute path to `.slx` file |
| `ExportPath` | `str` | `""` | Output path for generated Sysblock model; defaults to Sysplorer workspace |
| `LibraryPath` | `str` | `""` | Semicolon-separated paths to Link subsystem library folders |
| `DataFilePath` | `str` | `""` | Absolute path to `.slxdata` file |
| `ClearBaseWorkSpace` | `bool` | `True` | Clear base workspace before import |
| `OpenReport` | `bool` | `True` | Auto-open report after import |

## Debugging Checklist

- All path parameters must be **absolute paths**.
- Call `OpenSimulinkImporter()` before `ImportSimulinkModel()`.
- **Import order matters**: import referenced/link models **before** the main model that references them. Skip if models have no dependencies; if a specific order is required, import in that order.
- Load `SysplorerEmbeddedCoder` library before importing to ensure Sysblock components are available.
- Verify the `.slx` file exists and is from a supported version (R2017b–R2024b).
- Before importing, check the `.slx` model's directory for `.slxdata` or other data files; if found, ask the user whether to include them via `DataFilePath`.
- `LibraryPath` uses semicolons (`;`) as separators between multiple folders.
- `DataFilePath` must be a `.slxdata` file. If the user provides a file in another format, prompt them to generate the correct `.slxdata` file per the tool documentation.
- The generated model is automatically loaded in Sysplorer after successful import.
- After import, a report file is generated in the model's output path, containing error and warning details.
- Call `CloseSimulinkImporter()` after all imports to release resources.
