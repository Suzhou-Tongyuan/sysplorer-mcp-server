---
name: ty-design-opt-exp-modeling
description: >-
  Use this skill for Sysplorer DesignOptExp batch simulation Python API tasks:
  initializing a batch simulation pool, preparing or auto-generating solver
  directories, running many simulations with parameter dictionaries, requesting
  result variables, and reading batch result time series. Also use when
  DesignOptExpGui provides experiment-design or Monte Carlo sample data that
  should be executed by DesignOptExp batch simulation. Do not use this skill
  for DesignOptMpe parameter estimation, DesignOptMro response optimization, or
  DesignOptPsa sensitivity analysis.
metadata:
  short-description: DesignOptExp batch simulation Python API guidance
  version: 1.1.0
  managed-by: sysplorer-mcp
---

# DesignOptExp Batch Simulation

## Scope

- **In scope**: Sysplorer DesignOptExp / batch simulation scripting, solver directory preparation, model loading, `InitialBatchSimulate`, `BatchSimulate`, parameter sweeps, and result extraction.
- **Out of scope**: DesignOptMpe parameter estimation, DesignOptMro response optimization, DesignOptPsa sensitivity analysis, and general Modelica/Sysblock modeling.
- **Routing priority**: When the user wants batch simulation, use the `DesignOptExp` interfaces in this skill first. Do not default to compatibility batch interfaces exposed by `DesignOptExpGui`.

## Hard Rules

- **Missing data policy**: If required data is missing and cannot be discovered from the model, tool output, local files, or references, explicitly tell the user what is missing and either ask them to provide it or ask whether to use a clearly stated default. Do not silently invent ranges, distributions, targets, bounds, algorithms, simulation times, measurement mappings, or result variables.
- **Quiet by default**: For actual batch simulation execution, prefer a standalone Python script that starts Sysplorer with `StartSysplorer("-q", ...)`. Do not call MCP `session_manager` merely to run a batch job when the user expects quiet/headless execution, because MCP startup may attach to or launch a visible GUI.
- **Input confirmation gate**: Before running `BatchSimulate`, confirm the batch parameters, each parameter's values, result variables, and simulation options. If multiple parameters are provided and the user does not specify a parameter-combination mode, default to row-wise combination. Use full-factorial only when the user explicitly asks for all combinations / Cartesian product. If required parameters, values, or result variables are missing, inspect the model and present candidates instead of choosing them yourself.
- **No demo-as-result**: Example matrices such as `PI1.k=[1, 1.2]` are allowed only in documentation or when explicitly labeled as a dry-run/example. Never execute or report them as the user's batch simulation unless the user approved those exact values.
- **Parameter matrix intake**: Accept sampling or experiment-design results as a parameter matrix, including compatible matrices generated when a requested method is not exposed by DesignOptExpGui. Convert each row into `list[dict[paramName, value]]` for `BatchSimulate`. If the user asks where sampling/design data comes from, answer that the data comes from model experiment.
- **MCP session first only for MCP execution**: call `session_manager(action="health" | "ensure")` before any MCP `run_sysplorer_api` that touches Sysplorer. If quiet execution is required, use the standalone `-q` path instead of MCP `run_sysplorer_api`.
- **Never** call `ClearAll` or `ChangeDirectory` from generated scripts. Use `model_manager(action="unload")` for cleanup when needed.
- **DesignOptExp module docs**: DesignOptExp is an independent toolbox module. Do not query it via main ModelingPy `get_api_document`; use explicit import plus `ListFunctions()` / `help()` and this skill's `references/`.
- **Explicit import**: In scripts, import the toolbox explicitly:

```python
import mworks.sysplorer.DesignOptExp as exp
```

- **Preferred API**: Prefer `DesignOptExp.InitialBatchSimulate(...)` and `DesignOptExp.BatchSimulate(...)` for batch simulation requests; use `DesignOptExpGui` compatibility interfaces only when a model-experiment workflow specifically requires that module.

## Standalone Sysplorer launch mode

When generating a standalone `.py` script outside MCP for DesignOptExp batch simulation, start Sysplorer in quiet/headless mode by default. If the default `-q` launch or connection fails, retry with `-gui` before declaring the batch run blocked. Use the installed version's supported `StartSysplorer` form, for example:

```python
import mworks.sysplorer as eng
import mworks.sysplorer.DesignOptExp as exp

eng.StartSysplorer("-q", processPath=r"C:\path\to\mworks.exe")
eng.SetCompileSolver64(1)
eng.LoadLibrary("Modelica")
eng.OpenModelFile(model_path)
# Only for nested models or when explicitly opening a submodel class:
# eng.OpenModel(model_name)
```

For single-level models, `OpenModelFile(model_path)` is sufficient. Call `OpenModel(model_name)` only for nested models or when the workflow explicitly needs to open a submodel class after loading the `.mo` file.

Use the DesignOptExpGui skill and `-gui` only for model-experiment workflows that require the GUI module.

## Tool Map

| Need | Tool / action |
|---|---|
| Inspect model text without launching Sysplorer | local file read / parser first |
| Candidate discovery from loaded model | quiet standalone introspection script, or MCP only when GUI/attached session is acceptable |
| Sysplorer readiness for MCP-only work | `session_manager` |
| Run batch simulation script | standalone `python` with `StartSysplorer("-q", ...)` by default; `call_code(mode="run_sysplorer_api")` only when MCP execution is acceptable |
| Model open / save / unload | `model_manager` |
| Check / translate / simulate affected models | `check_model`, `translate_model`, `simulate_model` |
| Detailed local docs | `references/批量仿真使用说明.md`, `references/DesignOptExp.md`, `references/批量仿真demo说明.md` |

## Cross-skill Composition

The five DesignOpt skills can be combined in one workflow. A common pattern is:

1. Use `ty-design-opt-exp-gui-modeling` / `DesignOptExpGui` to generate experiment-design matrices or Monte Carlo samples, such as `FullFactorialDesign`, `LatinHypercubeDesign`, `DOptimalDesign`, `UniformSampling`, or `NormalSampling`.
2. Convert each generated sample row into the `DesignOptExp.BatchSimulate` input shape: `list[dict[paramName, value]]`.
3. Use this skill's `DesignOptExp.InitialBatchSimulate(...)` and `DesignOptExp.BatchSimulate(...)` for the actual batch simulations and result collection.
4. Feed resulting data into `DesignOptPsa` for sensitivity analysis, `DesignOptMro` for response optimization, or `DesignOptMpe` for parameter estimation when the user asks for those follow-up analyses.

## Canonical Workflow

1. Read the model file first when possible. Extract and present candidate parameter paths and result-variable paths, including explicit component parameters such as `gain.k`, source settings such as `step.height`, and public outputs such as `y`.
2. Ask the user to choose the batch parameters, value list for each parameter, result variables, and simulation options. If there are multiple parameters and the user does not specify the combination mode, use row-wise combination by default. Use `full-factorial` only when the user explicitly asks for all combinations / Cartesian product. Do not proceed with invented parameter values or result variables unless the user approves them.

### Input packet examples

When explaining the minimum required inputs to the user, explicitly label any concrete values as examples, not defaults. Prefer showing both a single-parameter example and a multi-parameter example.

Single-parameter example:

```text
示例：单参数批量仿真
模型：C:\path\rectangle_area.mo
模型名：rectangle_area
批量参数：length = [20, 40, 75, 100]
组合方式：单参数，无需组合
结果变量：area
仿真时间：startTime = 0, stopTime = 1, outputStep = 0.01
结果要求：终点值，或完整时序数据
```

Multi-parameter row-wise example, where each row is one simulation:

```text
示例：多参数逐行组合
模型：C:\path\WaterTank.mo
模型名：WaterTank
批量参数：
  PI1.k = [0.5, 1.0, 2.0]
  PI1.T = [5.0, 10.0, 20.0]
组合方式：逐行组合
实际仿真组：
  Run1: PI1.k = 0.5, PI1.T = 5.0
  Run2: PI1.k = 1.0, PI1.T = 10.0
  Run3: PI1.k = 2.0, PI1.T = 20.0
结果变量：y
仿真时间：startTime = 0, stopTime = 40, outputStep = 0.02
```

Multi-parameter full-factorial example, where every value of each parameter is crossed:

```text
示例：多参数全组合
模型：C:\path\WaterTank.mo
模型名：WaterTank
批量参数：
  PI1.k = [0.5, 1.0, 2.0]
  PI1.T = [5.0, 10.0]
组合方式：全组合
实际仿真组数：3 * 2 = 6
结果变量：y
仿真时间：startTime = 0, stopTime = 40, outputStep = 0.02
```

If the user provides multiple parameters and multiple data rows without naming a combination mode, default to row-wise. If the user says "all combinations", "full-factorial", or "Cartesian product", use full-factorial.

3. Build `param` from the confirmed design:

```python
# Row-wise example after user confirmation:
param = [
    {"paramA": value_a1, "paramB": value_b1},
    {"paramA": value_a2, "paramB": value_b2},
]

# Full-factorial example after user confirmation:
param = [
    {"paramA": a, "paramB": b}
    for a in paramA_values
    for b in paramB_values
]
```

4. Build simulation options from user input or clearly approved defaults, for example:

```python
options = {
    "startTime": 0,
    "stopTime": 1,
    "outputStep": 0.02,
    "saveEvent": False,
}
```

5. Start Sysplorer quietly for standalone execution, load required libraries, open the model, and initialize batch simulation:

```python
eng.StartSysplorer("-q", processPath=r"C:\path\to\mworks.exe")
eng.SetCompileSolver64(1)
eng.LoadLibrary("Modelica")
eng.OpenModelFile(model_path)

exp.InitialBatchSimulate(
    modelName=model_name,
    solverPath=solver_path,
    storePath=store_path,
    instNum=min(max(len(param), 1), requested_instance_count),
    options=options,
)
```

6. Run batch simulation with the confirmed parameter dictionaries and result-variable lists:

```python
results = exp.BatchSimulate(param, [result_variables])
```

7. Read result values from the returned list and save summaries:

```python
first_y = results[0]["y"]
first_time = results[0]["time"]
```

8. After batch simulation completes, actively ask the user whether to plot results. If they agree, plot with `matplotlib` according to the **Result Plotting** rules below.

## Result Plotting

After batch simulation finishes, **proactively ask** the user: *"批量仿真已完成，是否需要绘制结果图？"* (or in English: *"Batch simulation completed. Would you like to plot the results?"*). Do not skip this prompt.

When the user agrees to plot:

- **Use `matplotlib`** (`import matplotlib.pyplot as plt`) for plotting.
- **Display interactively** with `plt.show()` — the plot window pops up directly. Do **not** save images to disk unless the user explicitly asks for it.
- **One variable per figure**: Each result variable gets its own figure window.
- **All batches on one plot**: For a given variable, overlay all batch cases as separate lines in a single axes, so the user can compare them side-by-side.
- **X-axis = simulation time** (`results[i]["time"]`), **Y-axis = variable values** (`results[i]["var_name"]`).
- **Legend**: Label each line with the corresponding parameter values to identify which batch it belongs to.

Example plotting script for MCP `run_sysplorer_api`:

```python
import matplotlib
matplotlib.use("TkAgg")  # or "Qt5Agg"
import matplotlib.pyplot as plt

var_names = ["area"]      # result variables requested by user
params = [{"length": 10}, {"length": 12}, {"length": 50}, {"length": 99}]

for var in var_names:
    plt.figure()
    for i, r in enumerate(results):
        label = ", ".join(f"{k}={v}" for k, v in params[i].items())
        if "time" in r:
            plt.plot(r["time"], r[var], label=label)
        else:
            plt.plot(r[var], label=label)
    plt.xlabel("time")
    plt.ylabel(var)
    plt.title(f"Batch Simulation: {var}")
    plt.legend()
    plt.grid(True)
    plt.show()
```

**Rules**:
- Do not connect result points from different parameter cases into one continuous line.
- If the user requests only specific variables (e.g., `["area"]`), plot only those variables.
- If `time` data is missing from results, use sample indices as the x-axis.

## 2026a Notes

- `InitialBatchSimulate` includes `modelName`; pass the full loaded model name.
- `solverPath` is a solver directory. In 2026a, if the directory has no usable solver, Sysplorer can generate one automatically from `modelName`.
- Manual solver preparation from older workflows is still supported; pass that prepared directory as `solverPath`.
- Load libraries and open the target model before calling `InitialBatchSimulate`.
- `options` is optional; only include key/value pairs you need (e.g. you can omit `algorithm` and `tolerance` and rely on defaults).
- `InitialBatchSimulate` returns `bool` - `True` on success; always check the return value.
- `resultName` usually has the same length as `param`. If `resultName` has length 1, the API auto-expands that one result-variable list for every parameter set.

## Debugging Checklist

- Parameter names and result variable names are case-sensitive and model-specific.
- `param` must be `list[dict[str, number]]`.
- `resultName` must be `list[list[str]]`.
- If `resultName` length is neither `1` nor equal to `param` length, normalize it before calling `BatchSimulate`.
- Ensure `solverPath` and `storePath` are writable absolute paths.
- Include `"time"` only if needed; result dictionaries usually include time data for requested trajectories.
- If initialization fails, verify that the model is loaded and `modelName` matches the loaded class name. Capture `InitialBatchSimulate`'s `bool` return value and check it.

## Source Notes

References used to maintain this skill:

- `<Sysplorer 安装目录>/sys/python/win64/Lib/site-packages/mworks/sysplorer/DesignOptExp/DesignOptExp.py`
- `<Sysplorer 安装目录>/sys/python/win64/Lib/site-packages/mworks/sysplorer/bs_demo.py`
- `《批量仿真 Python API 2026a 接口说明》文档（随产品文档分发）`
