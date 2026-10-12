---
name: ty-design-opt-mro-modeling
description: >-
  Use this skill for Sysplorer DesignOptMro response optimization Python API
  tasks: initializing the MRO toolbox, selecting tuner/fixed parameters,
  creating response requirements and variable sets, configuring optimization
  algorithms, running evaluation/optimization, reading result data, and writing
  safe MCP run_sysplorer_api examples. Do not use this skill for DesignOptMpe
  parameter estimation.
metadata:
  short-description: DesignOptMro response optimization Python API guidance
  version: 1.1.0
  managed-by: sysplorer-mcp
---

# DesignOptMro Response Optimization

## Scope

- **In scope**: Sysplorer DesignOptMro / MRO / response optimization scripting, including tuner parameters, fixed parameters, requirements, variable sets, algorithm options, evaluation, optimization, session save/load, and result extraction.
- **Out of scope**: DesignOptMpe parameter estimation, sensitivity analysis, unrelated ModelingPy API lookup, and pure Modelica / Sysblock modeling.

## Hard Rules

- **Missing data policy**: If required data is missing and cannot be discovered from the model, tool output, local files, or references, explicitly tell the user what is missing and either ask them to provide it or ask whether to use a clearly stated default. Do not silently invent ranges, distributions, targets, bounds, algorithms, simulation times, measurement mappings, or result variables.
1. Call `session_manager(action="health" | "ensure")` before `run_sysplorer_api` code that touches Sysplorer.
2. Never call `ClearAll` or `ChangeDirectory` in generated scripts. Use `mro.CloseApp()` and `pyapi.Exit()` when the script owns the Sysplorer process; use `model_manager(action="unload")` for model cleanup in MCP workflows.
3. DesignOptMro is an independent toolbox module. Do not query it with main ModelingPy `get_api_document`; use:

```python
import mworks.sysplorer.DesignOptMro as mro
print(mro.ListFunctions())
help(mro.ConfigVariablePropertyRequirement)
```

4. In `run_sysplorer_api`, import the toolbox explicitly:

```python
import mworks.sysplorer as pyapi
import mworks.sysplorer.DesignOptMro as mro
```

## Standalone Sysplorer launch mode

When generating a standalone `.py` script outside MCP, start Sysplorer in quiet/headless mode by default for DesignOptMro. If the default `-q` launch or connection fails, retry with `-gui` before declaring the workflow blocked. Use the installed version's supported `StartSysplorer` form, for example:

```python
import mworks.sysplorer as eng
import mworks.sysplorer.DesignOptMro as mro

eng.StartSysplorer("-q", processPath=r"C:\path\to\mworks.exe")
eng.SetCompileSolver64(1)
eng.LoadLibrary("Modelica")
eng.OpenModelFile(model_path)
# Only for nested models or when explicitly opening a submodel class:
# eng.OpenModel(model_name)
```

For single-level models, `OpenModelFile(model_path)` is sufficient. Call `OpenModel(model_name)` only for nested models or when the workflow explicitly needs to open a submodel class after loading the `.mo` file.

Use `-gui` when the user explicitly needs to interact with the Sysplorer UI, or as the fallback after `-q` fails. Model-experiment workflows are handled by the DesignOptExpGui skill and must use `-gui`.

## Reference Map

| Need | Local reference |
|---|---|
| API signatures and return shapes | `references/DesignOptMro.md` |
| End-to-end MRO workflow | `references/响应优化使用说明.md` |
| Rectangle-area example | `references/响应优化demo说明.md` |

Primary upstream references used to maintain this skill:

- `<Sysplorer 安装目录>/sys/python/win64/Lib/site-packages/mworks/sysplorer/DesignOptMro/DesignOptMro.py`
- `<Sysplorer 安装目录>/sys/python/win64/Lib/site-packages/mworks/sysplorer/矩形面积example.py`
- `《响应优化 Python API 2024b 说明》文档（随产品文档分发）`

## Cross-skill Composition

The five DesignOpt skills can be combined when needed:

- Use `DesignOptExpGui` to generate experiment-design matrices or Monte Carlo samples.
- Use `DesignOptExp` to run those parameter sets as batch simulations.
- Use `DesignOptMro` when the user wants to turn response requirements into an optimization problem.
- Use `DesignOptPsa` to screen influential parameters before optimization, or `DesignOptMpe` when measured-data calibration is required.

## Canonical Workflow

1. Open or load the target model.
2. Initialize the toolbox with `mro.InitialApp(modelName, instPath="")`.
3. Inspect available names with `mro.GetTunerParam()`, `mro.GetFixParam()`, and `mro.GetVariable()`.
4. Select and configure tuner parameters:
   `mro.SelectTunerParam((...))`, then `mro.ConfigTunerParam(paramName, minVal, maxVal, initialVal)`.
5. Optionally select fixed parameters with `mro.SelectFixParam((...))`, then `mro.ConfigFixParam(paramName, initialVal)`.
6. Create requirements with one of:
   `NewVariablePropertyRequirement`, `NewStepResponseRequirement`, `NewVariableLinearBoundRequirement`, `NewVariableTrackingRequirement`.
7. Configure each requirement with the matching `Config...Requirement(...)` API.
8. Create variable sets with `mro.NewVariableSet(setName, (...))`.
9. Bind requirements to variable sets with `mro.SetRequirementVariableSet(reqName, (...))`.
10. Optionally choose requirements with `mro.SelectRequirement((...))`; if not called, created requirements are selected by default.
11. Configure simulation and optimization options:
    `mro.SetSimulationOption(startTime, endTime, stepNumber=500)` and `mro.SetOptimizeOption(continueOptimize=True, parallelNum=...)`.
12. Select/configure the algorithm with `mro.SelectAlgorithm("PSO" | "GA" | "Cobyla" | "Auglag")`; for PSO/GA call `ConfigPSOAlgorithm(...)` or `ConfigGAAlgorithm(...)`.
13. Run `mro.StartEvaluate()` before `mro.StartOptimize()` when validating new scripts.
14. Read results with `mro.GetOptimizeData()`, `mro.GetOptimizeResult()`, `mro.GetOptimizeParamData(resultName)`, `mro.GetOptimizeParamIterData(paramName)`, `mro.GetOptimizeReqTimeData(reqName)`, or `mro.GetOptimizeReqIterData(reqName)`.
15. Close the toolbox with `mro.CloseApp()`.

## Requirement Types

- **Variable property**: scalar properties such as `"Final Value"`, `"Maximum"`, `"Minimum"`, `"Average"`, `"Variance"`. Configure with `ConfigVariablePropertyRequirement(reqName, varProperty, varType, value=0.0)`.
- **Step response**: initial/final value, rise time, settling time, overshoot, undershoot. Configure with `ConfigStepResponseRequirement(...)`.
- **Variable linear bound**: time-domain upper/lower linear bounds. In current Python code the function names are `NewVariableLinearBoundRequirement` and `ConfigVariableLinearBoundRequirement`, even though the 2024b docx also mentions older `NewLinearBoundRequirement` / `ConfigLinearBoundRequirement` names.
- **Variable tracking**: a variable tracks a time/value sequence. Configure with `ConfigVariableTrackingRequirement(reqName, time, value, method)`.

Always create a variable set and attach it to the requirement. A requirement without a variable set is incomplete.

## Rectangle-Area Minimal Example

```python
import mworks.sysplorer as pyapi
import mworks.sysplorer.DesignOptMro as mro

pyapi.LoadLibrary("Modelica", "4.0.0")
pyapi.OpenModelFile(r"C:\path\to\rectangle_area.mo")

mro.InitialApp("rectangle_area")
mro.SelectTunerParam(("length",))
mro.ConfigTunerParam("length", minVal=0.001, maxVal=199.99, initialVal=10.0)

mro.NewVariablePropertyRequirement("Req_1")
mro.ConfigVariablePropertyRequirement("Req_1", "Final Value", "Maximization")

mro.NewVariableSet("Set_1", ("area",))
mro.SetRequirementVariableSet("Req_1", ("Set_1",))

mro.StartEvaluate()
mro.StartOptimize()
data = mro.GetOptimizeData()
print(data["params"])
print(data["reqs"])

mro.CloseApp()
```

## Debugging Checklist

- Names are case-sensitive; discover parameter, variable, requirement, variable-set, and result names from MRO output.
- Tuner/fixed parameters must be selected before they are configured.
- Tuner parameters and fixed parameters are mutually exclusive.
- Requirement APIs are paired: `New...Requirement` first, then `Config...Requirement`.
- Variable set APIs are separate: `NewVariableSet(...)`, then `SetRequirementVariableSet(...)`.
- If optimization fails, run `StartEvaluate()` and inspect `GetEvaluateResultData(reqName)`.
- `GetOptimizeStatus()` returns `0` for successful completion, `-1` for not-started/running, and other values for optimization errors.
- If parameters converge to bounds, revisit parameter bounds before increasing population size or iteration limits.

