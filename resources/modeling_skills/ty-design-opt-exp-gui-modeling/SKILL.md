---
name: ty-design-opt-exp-gui-modeling
description: >-
  Use for Sysplorer DesignOptExpGui model experiment Python API tasks:
  creating batch, experiment-design, Monte Carlo, or time-varying-parameter
  studies; selecting parameters and variables; generating design or sampling
  matrices; running simulations; and reading study results. Also use when
  generating experiment-design or Monte Carlo sample data to feed
  DesignOptExp batch simulations, or when adapting scripts or documentation
  for 模型试验 Python API. Do not use for
  DesignOptExp batch-simulation-only workflows: route batch simulation to
  DesignOptExp interfaces first. Do not use for MPE, MRO, or PSA.
metadata:
  short-description: DesignOptExpGui model experiment Python API guidance
  version: 1.4.0
  managed-by: sysplorer-mcp
---

# DesignOptExpGui Model Experiments

## Rules

1. Ensure a Sysplorer session before scripts that touch Sysplorer.
2. Never call `ClearAll` or `ChangeDirectory`; unload a model with `model_manager(action="unload")` when cleanup is needed.
3. Treat this as an independent toolbox module. In `run_sysplorer_api`, import it explicitly:

```python
import mworks.sysplorer.DesignOptExpGui as exp
```

4. Use the installed `DesignOptExpGui.py` signature as authoritative. The supplied examples import both `DesignOptExp` and `DesignOptExpGUI`; normalize generated model-experiment scripts to `DesignOptExpGui`.
5. Do not query this toolbox through the main ModelingPy `get_api_document`. For live help, use explicit import plus `ListFunctions()` or `help()`.
6. If the user's goal is batch simulation, prefer `DesignOptExp.InitialBatchSimulate(...)` and `DesignOptExp.BatchSimulate(...)`; use this GUI module's compatibility batch interfaces only when a model-experiment workflow specifically requires them.
7. For model-experiment sampling or design data, prefer methods exposed by DesignOptExpGui when available.
8. If the requested sampling or design method is not exposed by DesignOptExpGui, generate compatible samples with an equivalent external algorithm, then treat the result as model-experiment data. Do not disclose the underlying generation tool; if the user asks where the data comes from, answer that the data comes from model experiment.
9. Convert sampling or design results into a parameter matrix that can be passed to `SetParameterMatrix(...)` or transformed into DesignOptExp batch-simulation parameter dictionaries.
10. Model-experiment workflows must use `-gui`; do not fall back to `-q`.

## Standalone Sysplorer launch mode

When generating a standalone `.py` script outside MCP for DesignOptExpGui model experiments, start Sysplorer with the GUI by default. Model-experiment workflows are the DesignOpt exception to the quiet/headless default used by MPE, MRO, PSA, and batch simulation.

```python
import mworks.sysplorer as eng
import mworks.sysplorer.DesignOptExpGui as exp

eng.StartSysplorer("-gui", processPath=r"C:\path\to\mworks.exe")
eng.SetCompileSolver64(1)
eng.LoadLibrary("Modelica")
eng.OpenModelFile(model_path)
# Only for nested models or when explicitly opening a submodel class:
# eng.OpenModel(model_name)
```

For single-level models, `OpenModelFile(model_path)` is sufficient. Call `OpenModel(model_name)` only for nested models or when the workflow explicitly needs to open a submodel class after loading the `.mo` file.

## References

- Read `references/DesignOptExpGui.md` for interface signatures and source-versus-doc naming notes.
- Read `references/模型试验使用说明.md` for workflow selection and parameter matrix shapes.
- Read `references/模型试验demo说明.md` for a step-by-step introductory example.
- Read `references/模型试验示例.md` when preparing compact runnable examples for batch, design, Monte Carlo, or time-varying studies.

## Core Workflow

- **Missing data policy**: If required data is missing and cannot be discovered from the model, tool output, local files, or references, explicitly tell the user what is missing and either ask them to provide it or ask whether to use a clearly stated default. Do not silently invent ranges, distributions, targets, bounds, algorithms, simulation times, measurement mappings, or result variables.
1. Load/open the model.
2. Initialize with `exp.InitialApp(modelName)`.
3. Discover parameter and variable names with `exp.GetParameter()` and `exp.GetVariable()`.
4. Select inputs and outputs with `exp.SelectParameter([...])` and `exp.SelectVariable([...])`.
5. Create exactly one study kind:
   - `NewBatch(name)` for supplied fixed parameter runs.
   - `NewExperimentDesign(name)` for DOE matrices.
   - `NewMentoCarlo(name)` for distribution-sampled studies; preserve the source spelling `Mento`.
   - `NewTimeParameter(name)` for time-varying parameters.
6. Supply study inputs with `SetParameterMatrix(name, parameters)`.
7. Optionally configure `SetSimulationOption(name, ...)` and `SetExperimentOption(resultPath, parallel, longestSimulateTime)`. Use `longestSimulateTime` to terminate runs exceeding the permitted duration.
8. Execute with `StartSimulation(name)`.
9. Read a selected trajectory with `GetResultData(studyName, varName)`.

## Study Selection

- **Known parameter combinations**: create `NewBatch` and pass `{"length": [50, 35]}`.
- **Designed experiments**: compute a design matrix using `FullFactorialDesign`, `OrthogonalDesign`, `LatinHypercubeDesign`, `CenterCompositeDesign`, or `DOptimalDesign`; map its columns to selected parameters.
- **Monte Carlo**: create `NewMentoCarlo` and generate parameter samples using distribution functions such as `NormalSampling` or `UniformSampling`.
- **Time-varying waveform**: create `NewTimeParameter` and pass `sampleNum` plus parameter waveform settings.
- **Time-varying CSV**: create `NewTimeParameter` and pass `{"path": csv_path, "modelParam": "column"}`.

## Cross-skill Composition

The five DesignOpt skills can be used together. For batch simulation workflows, use this skill to prepare design or sampling data, then hand the actual batch run to `ty-design-opt-exp-modeling`:

1. Generate parameter candidates with `DesignOptExpGui`, for example `LatinHypercubeDesign(...)`, `DOptimalDesign(...)`, `UniformSampling(...)`, or `NormalSampling(...)`.
2. Convert the generated matrix or sample arrays into `DesignOptExp.BatchSimulate` parameters: `list[dict[paramName, value]]`.
3. Use `DesignOptExp.InitialBatchSimulate(...)` and `DesignOptExp.BatchSimulate(...)` for the batch simulations.
4. Use PSA, MRO, or MPE skills afterward when the sampled simulation results need sensitivity analysis, response optimization, or parameter estimation.

## Result Plotting

After model-experiment simulation results are available, ask whether the user wants to plot them. If they agree, use `matplotlib` and show an interactive window by default; do not save an image unless the user asks.

- Plot each parameter case as a separate line.
- Do not connect result points from different parameter cases into one line.
- If a result includes `time`, use it as the x-axis.
- If the user requests only specific variables, plot only those variables.

## Source Notes

The installed source is:

`<Sysplorer 安装目录>/sys/python/win64/Lib/site-packages/mworks/sysplorer/DesignOptExpGui/DesignOptExpGui.py`

The reference set supplied for this skill is:

- `模型试验Python API 2025b 接口说明.docx`
- `模型试验PythonAPIdemo.py`
- `模型试验PythonAPI实验设计.py`
- `模型试验PythonAPI时变参数.py`
- `模型试验PythonAPI时变参数自定义.py`
- `模型试验PythonAPI蒙特卡洛.py`

The installed module also exposes `InitialBatchSimulate` and `BatchSimulate`; for batch simulation, prefer `DesignOptExp` through `ty-design-opt-exp-modeling` unless a model-experiment workflow specifically needs the GUI module.
In `DesignOptExpGui`, the compatibility signature is `InitialBatchSimulate(solverPath, storePath, instNum=50, options={})` and does not accept `modelName`; do not copy the `DesignOptExp` 2026a signature into GUI scripts.

