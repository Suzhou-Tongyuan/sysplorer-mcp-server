---
name: ty-design-opt-psa-modeling
description: >-
  Use this skill for Sysplorer DesignOptPsa sensitivity analysis Python API
  tasks: initializing the PSA toolbox, creating parameter sets, configuring
  parameter sampling distributions or explicit sampling data, creating
  requirements and variable sets, evaluating parameter samples, running
  quantified sensitivity analysis, and reading PSA result data. Do not use this
  skill for DesignOptMpe parameter estimation or DesignOptMro response
  optimization.
metadata:
  short-description: DesignOptPsa sensitivity analysis Python API guidance
  version: 1.0.0
  managed-by: sysplorer-mcp
---

# DesignOptPsa Sensitivity Analysis

## Scope

- **In scope**: Sysplorer DesignOptPsa / PSA / sensitivity analysis scripts, parameter sets, sample distributions, explicit sampling data, requirements, variable sets, evaluation, quantified analysis, sessions, and result extraction.
- **Out of scope**: DesignOptMpe parameter estimation, DesignOptMro response optimization, batch simulation, model experiment APIs, unrelated ModelingPy APIs, and pure Modelica / Sysblock modeling.

## Hard Rules

- **Missing data policy**: If required data is missing and cannot be discovered from the model, tool output, local files, or references, explicitly tell the user what is missing and either ask them to provide it or ask whether to use a clearly stated default. Do not silently invent ranges, distributions, targets, bounds, algorithms, simulation times, measurement mappings, or result variables.
1. **Session first**: call `session_manager(action="health" | "ensure")` before any `run_sysplorer_api` that touches Sysplorer.
2. **Never** call `ClearAll` or `ChangeDirectory` from generated scripts. Close PSA with `psa.CloseApp()`; unload models via `model_manager(action="unload")` when cleanup is needed.
3. DesignOptPsa is an independent toolbox module. Do not query it via main ModelingPy `get_api_document`; use explicit import plus `ListFunctions()` / `help()` and this skill's `references/`.
4. In `run_sysplorer_api`, import the toolbox explicitly:

```python
import mworks.sysplorer.DesignOptPsa as psa
```

Do not assume PSA functions are available through the main `mworks.sysplorer` namespace.

## Standalone Sysplorer launch mode

When generating a standalone `.py` script outside MCP, start Sysplorer in quiet/headless mode by default for DesignOptPsa. If the default `-q` launch or connection fails, retry with `-gui` before declaring the workflow blocked. Use the installed version's supported `StartSysplorer` form, for example:

```python
import mworks.sysplorer as eng
import mworks.sysplorer.DesignOptPsa as psa

eng.StartSysplorer("-q", processPath=r"C:\path\to\mworks.exe")
eng.SetCompileSolver64(1)
eng.LoadLibrary("Modelica")
eng.OpenModelFile(model_path)
# Only for nested models or when explicitly opening a submodel class:
# eng.OpenModel(model_name)
```

For single-level models, `OpenModelFile(model_path)` is sufficient. Call `OpenModel(model_name)` only for nested models or when the workflow explicitly needs to open a submodel class after loading the `.mo` file.

Use `-gui` when the user explicitly needs to interact with the Sysplorer UI, or as the fallback after `-q` fails. Model-experiment workflows are handled by the DesignOptExpGui skill and must use `-gui`.

## Tool Map

| Need | Tool / action |
|---|---|
| Sysplorer readiness | `session_manager` |
| Run PSA script | `call_code` (`mode="run_sysplorer_api"`) |
| Model open / save / unload | `model_manager` |
| Check / translate / simulate affected models | `check_model`, `translate_model`, `simulate_model` |
| Detailed local docs | `references/敏感度分析使用说明.md`, `references/DesignOptPsa.md`, `references/敏感度分析demo说明.md` |

## Cross-skill Composition

The five DesignOpt skills can be combined when sampling, simulation, and analysis are split across tools:

- Use `DesignOptExpGui` to generate experiment-design matrices or Monte Carlo sample arrays.
- Use `DesignOptExp` to run large parameter sets through batch simulation.
- Use `DesignOptPsa` to quantify which parameters most affect requirements or variables.
- Use `DesignOptMro` for optimization after screening, or `DesignOptMpe` for parameter estimation/calibration tasks.

## Execution Loop

1. **Clarify analysis target**: variable matching, variable property, step response, linear bound, or tracking requirement.
2. **Choose sampling path**:
   - Use `SetSampleOption` + `SetParamSampleDistribution` + `StartSampling()` for toolbox-generated samples.
   - Use `NormalSampling` / `UniformSampling` / other sampling helpers plus `SetParamSamplingData(...)` for explicit sample arrays.
3. **Minimal script**: open model, `InitialApp(...)`, create one parameter set, provide sample data, create one requirement and variable set or matching requirement, then `StartEvaluate()`.
4. **Quantify**: select an evaluate result, set quantified method/type, then `StartQuantifiedAnalysis()`.
   If the user asks for quantified analysis / correlation analysis but does not specify methods or types, default to all supported methods and types enabled:
   `psa.SetQuantifiedMethod(correlation=True, standardizedRegression=True, partialCorrelation=True)` and
   `psa.SetQuantifiedType(linear=True, ranked=True, kendall=True)`. Only narrow these booleans when the user explicitly names the desired method(s) or type(s).
5. **Iterate** using `call_code` stdout/stderr and result dictionaries.

## Canonical PSA Workflow

Use this order for a standard sensitivity analysis:

1. Load/open the model with Sysplorer APIs or `model_manager`.
2. `psa.InitialApp(modelName, instPath="")`.
3. Inspect available names with `psa.GetTunerParam()` and `psa.GetVariable()`.
4. Create a parameter set:
   `psa.NewParameterSetAttachParam(setName, (...))`, or `psa.NewParameterSet(setName)` then `psa.ConfigParameterSet(setName, {...})`.
5. Set it current with `psa.SetCurrentParameterSet(setName)`.
6. Configure sampling:
   `psa.SetSampleOption(number, "Random", overWrite=True)` and `psa.SetParamSampleDistribution(paramName, distribute, array)`, then `psa.StartSampling()`.
7. Alternatively, generate samples directly:
   `psa.NormalSampling(...)`, `psa.UniformSampling(...)`, etc., then `psa.SetParamSamplingData(paramName, values)`.
8. Create requirements:
   `NewVariableMatchingRequirement`, `NewVariablePropertyRequirement`, `NewStepResponseRequirement`, `NewLinearBoundRequirement`, or `NewVariableTrackingRequirement`.
9. Configure each requirement with the matching `Config...Requirement(...)` API.
10. For non-matching requirements, create variable sets with `psa.NewVariableSet(...)` and bind them with `psa.SetRequirementVariableSet(...)`.
11. Select requirements with `psa.SelectRequirement((...))`.
12. Set simulation and evaluation options:
    `psa.SetSimulateOption(startTime, endTime, stepNumber=500)` and `psa.SetEvaluateOption(continueEvaluate=True, saveEvaluate=True, parallelNum=...)`.
13. Run `psa.StartEvaluate()` and read `psa.GetEvaluateResult()` / `psa.GetEvaluateResultData(resultName)`.
14. Select an evaluate result for quantified analysis with `psa.SelectEvaluateResult(resultName)`.
15. Set methods/types. Unless the user explicitly specifies a subset, enable every method and type:
    `psa.SetQuantifiedMethod(correlation=True, standardizedRegression=True, partialCorrelation=True)` and `psa.SetQuantifiedType(linear=True, ranked=True, kendall=True)`.
16. Run `psa.StartQuantifiedAnalysis()` and read `psa.GetQuantifiedResult()` / `psa.GetQuantifiedResultData(resultName)`. `GetQuantifiedResultData` returns `[quantifiedType, requirementName, {parameterName: correlationValue}]`.
17. Close the toolbox with `psa.CloseApp()`.

## Requirement Selection

- **Variable matching**: compare simulation variables against CSV measurement columns. Use `NewVariableMatchingRequirement` and `ConfigVariableMatchingRequirement(reqName, csvPath, {"simVar": "measuredColumn"}, fix={})`.
- **Variable property**: scalar properties such as final value, max/min, average, variance. Use `NewVariablePropertyRequirement` and `ConfigVariablePropertyRequirement`.
- **Step response**: rise time, settling time, overshoot, undershoot style metrics. Use `NewStepResponseRequirement` and `ConfigStepResponseRequirement`.
- **Linear bound**: time-domain linear upper/lower bound. PSA source uses `NewLinearBoundRequirement` for creation and `ConfigVariableLinearBoundRequirement` for configuration.
- **Variable tracking**: track a target time/value curve. Use `NewVariableTrackingRequirement` and `ConfigVariableTrackingRequirement`.

Always bind a variable set for property, step-response, linear-bound, and tracking requirements. Variable matching requirements configure the variable mapping directly in `ConfigVariableMatchingRequirement`.

## Debugging Checklist

- Names must come from PSA output: parameter names, variable names, requirement names, variable-set names, evaluate result names, and quantified result names are case-sensitive.
- `SetCurrentParameterSet(...)` matters; distribution APIs apply to the current parameter set.
- Explicit sample lists should have the same length for every sampled parameter.
- If `SetSampleOption(number=...)` is used, explicit `SetParamSamplingData(...)` lists should match `number`.
- `ConfigVariableMatchingRequirement` maps simulation variable names to CSV column names, e.g. `{"y": "eyedata"}`.
- `StartQuantifiedAnalysis()` needs a selected evaluate result from `SelectEvaluateResult(...)`.
- For quantified analysis / correlation analysis, if the user does not specify methods or types, default to all booleans `True` for both `SetQuantifiedMethod(...)` and `SetQuantifiedType(...)`. If the user specifies a subset, follow the user's subset exactly.
- Choose at least one method and one type, otherwise no useful result is produced.

## Source Notes

References used to maintain this skill:

- `<Sysplorer 安装目录>/sys/python/win64/Lib/site-packages/mworks/sysplorer/DesignOptPsa/DesignOptPsa.py`
- `<Sysplorer 安装目录>/sys/python/win64/Lib/site-packages/mworks/sysplorer/DesignOptPsa/psa_demo.py`
- `《敏感度分析 Python API 2025b 说明》文档（随产品文档分发）`

The user-provided source path `.../DesignOptMro/DesignOptPsa.py` does not exist in this installation; the actual module path is `.../DesignOptPsa/DesignOptPsa.py`.

