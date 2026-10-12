---
name: ty-design-opt-mpe-modeling
description: >-
  在 Sysplorer 内通过 DesignOptMpe 做参数设计、MPE 参数估计、优化与标定脚本、`run_sysplorer_api` 实验循环。
  覆盖原生 MPE 流程、多边界与稳态估计、统一残差设计、批量仿真驱动的自定义算法与外置算法适配器。
  不要用于与 DesignOptMpe 无关的 ModelingPy 通用 API 查询（请用 `get_api_document`），也不要用于纯 Modelica / Sysblock 建模范式任务（请先用 `ty-sysplorer-modeling-rules` 再进入领域技能）。
metadata:
  short-description: DesignOptMpe parameter estimation and custom optimization guidance
  version: 1.4.1
  managed-by: sysplorer-mcp
---

# DesignOptMpe — parameter design, estimation, and optimization

## Scope

- **In scope**: DesignOpt / MPE / parameter estimation / optimization tasks that require the **DesignOptMpe** Python module inside Sysplorer, experiment loops, multi-boundary and steady-state estimation, residual design, custom external optimizers, batch-simulation-backed objective evaluation, and integration with Sysplorer models.
- **Out of scope**: Unrelated ModelingPy surface APIs (use `get_api_document`), pure Modelica / Sysblock modeling execution (use domain skills + `modeling_path_router`), and response optimization tasks that belong to `ty-design-opt-mro-modeling`.

## Hard rules

1. **Session first**: `session_manager(action="health" | "ensure")` before any `run_sysplorer_api` that touches Sysplorer.
2. **Never** call **`ClearAll`** or **`ChangeDirectory`** from scripts or tools; unload with `model_manager(action="unload")` when needed.
3. DesignOptMpe is **not** documented via the main `Help()` namespace—use **`import` + `ListFunctions()` / `help()`** in `run_sysplorer_api`, plus corpus text in `references/` and **`resources_retrieval`** on corpus `design_opt_mpe_api`.
4. Import the toolboxes explicitly:

```python
import mworks.sysplorer.DesignOptMpe as mpe
import mworks.sysplorer.DesignOptExp as exp
```

5. **Missing data policy**: do not invent parameter names, bounds, variable mappings, time windows, boundary values, or measurement columns. If they are not discoverable, ask for them or state the default you are about to use.
6. **Custom optimizer path**: when the user asks for a custom algorithm, a high-performance external algorithm, a hybrid strategy, or the built-in MPE algorithms are too limiting, switch to the custom batch-optimization path in this skill.
7. **Batch simulation path**: for custom optimizers that evaluate many candidates, prefer `DesignOptExp.InitialBatchSimulate(...)` and `DesignOptExp.BatchSimulate(...)` instead of repeated single-run estimation calls.
8. **Failure penalty**: if one candidate causes any required boundary simulation to fail, assign the candidate objective directly to `1e300`.
9. **Model dependency policy**: when the user provides a model file, ask whether it depends on libraries beyond `Modelica`. If the user provides library names, include them in the run configuration and load them before model open/check/optimization. If the user does not provide them or is unsure, infer dependencies from the model text and installed library folders, then use the inferred libraries internally.
10. **Preflight dependency order**: dependency inference and loading must happen before `CheckModel`, `TranslateModel`, `InitialBatchSimulate`, or short simulation checks. `CheckModel` and `TranslateModel` can block on missing libraries, so do not rely on them as the first missing-library detector.
11. **Algorithm adapter policy**: if the user names a custom algorithm that is not built in, first research whether it can optimize an expensive black-box scalar objective over numeric parameter vectors. If feasible, connect it through an optimizer adapter instead of changing the residual or batch-simulation core. If infeasible or too evaluation-hungry for Sysplorer simulation, explain the blocker and suggest a feasible alternative.
12. **User-facing algorithm wording**: when listing supported algorithms to users, list native algorithms, built-in custom algorithms, and "external optimizer adapters". Do not expose internal adapter runner names, config field names, callback names, or implementation classes unless the user asks for implementation details or a config/script artifact.

All `references/...` paths in this skill are relative to **this skill directory** (the folder that contains this `SKILL.md`), not the workspace root or any parent `skills/` directory.

## Tool map

| Need | Tool / action |
|------|----------------|
| Sysplorer readiness | `session_manager` |
| Run estimation / optimization code | `call_code` (`mode="run_sysplorer_api"`) |
| Long docs, FAQs, API tables | `resources_retrieval` with `sources` including **`design_opt_mpe_api`** |
| Model open / save / unload | `model_manager` |
| Check / translate / simulate affected models | `check_model`, `translate_model`, `simulate_model` |
| Batch simulation execution | `DesignOptExp.InitialBatchSimulate(...)`, `DesignOptExp.BatchSimulate(...)` |

## Execution modes

This skill supports two execution paths. Pick the minimal path that matches the user's request.

### 1. Native DesignOptMpe path

Use the native toolbox path when the user wants normal parameter estimation with built-in MPE algorithms: `Bobyqa` (default), `Cobyla`, `GA`, `PSO`, `Praxis`.

Canonical sequence:

1. Load/open the model.
2. `mpe.InitialApp(modelName, instPath="")`.
3. Inspect names with `mpe.GetTunerParam()`, `mpe.GetVariable()`, and `mpe.GetMeasureVariable(expName)`.
4. `mpe.SelectTunerParam(...)` and `mpe.ConfigTunerParam(...)`.
5. Create/configure the experiment:
   - single file: `mpe.NewExpAttachPath(...)`
   - multi-boundary: `mpe.NewExp(...)` + `mpe.ConfigMultiBoundaryExp(...)`
   - steady-state: `mpe.NewExp(...)` + `mpe.ConfigSteadyStateExp(...)`
6. `mpe.SetEstimateExp(expName)`.
7. Only for non-multi-boundary estimation, if fixed parameters are needed:
   `mpe.SelectFixParam(...)` then `mpe.ConfigFixParam(...)`.
8. Configure mappings and time:
   `mpe.SetSimulateVariable(...)`, `mpe.SetSimulateOption(...)`, `mpe.SetEstimateOption(...)`.
9. Select and configure the native algorithm:
    `mpe.SelectAlgorithm("Bobyqa")` (default). Available built-in algorithms: `Bobyqa`, `Cobyla`, `GA`, `PSO`, `Praxis`.
    Use `mpe.ConfigPSOAlgorithm(...)` for PSO, `mpe.ConfigGAAlgorithm(...)` for GA. `Bobyqa`, `Cobyla`, and `Praxis` use internal defaults with no dedicated config function.
10. Prefer `mpe.StartEvaluate()` before `mpe.StartEstimate()`.
11. Read results after estimation finishes:
    `mpe.GetEstimateResult()`, `mpe.GetEstimateParamData(...)`, `mpe.GetEstimateReport()`, `mpe.GetEstimateResultData()`.

### 2. Custom batch-optimization path

Use this path when the user asks for:

- a custom algorithm
- high-performance external optimization
- hybrid optimization with algorithms beyond built-in MPE selection
- large multi-boundary / steady-state estimation that benefits from batch simulation
- an algorithm name that is not currently built in but can be adapted to black-box objective evaluation

Canonical sequence:

1. Normalize the scenario into:
   - tuner parameters
   - boundary list
   - variable mappings
   - measurement bundle
   - simulation / estimation time settings
2. Resolve model dependencies: use user-provided extra libraries when available; otherwise infer them from the model text and installed libraries.
3. Convert single-condition estimation into **one virtual boundary**. Do not branch the objective logic by "has boundary / has no boundary".
4. Run preflight validation before long optimization.
5. Prepare batch runtime with `DesignOptExp.InitialBatchSimulate(...)`.
6. Evaluate the configured parameter initial values once before optimizer search, and record that evaluation as the first history item.
7. Expand each candidate parameter vector across all boundaries.
8. Call `DesignOptExp.BatchSimulate(...)`.
9. Regroup flat run results back into `candidate -> boundary -> variable`.
10. Compute residuals with the unified hierarchy below.
11. Select or build an optimizer adapter:
    - built-in adapter: `lshade` or `basic-de`
    - external optimizer adapter: a local module that calls the shared batch-evaluation callback
    - new algorithm adapter: research the algorithm, confirm feasibility, then implement the adapter contract
12. Drive the search through the selected adapter.
13. Report:
    - best parameters
    - total residual
    - per-boundary diagnostics
    - failure flags
    - algorithm name and settings
    - iteration history, with the initial-parameter evaluation as the first item
    - live progress JSONL records, one record per iteration stage

Reusable script asset:

- [`scripts/custom_batch_optimizer.py`](scripts/custom_batch_optimizer.py)

## Residual policy

### Supported residual functions

When the user does not explicitly specify a residual function, use **`Mean Absolute Percentage Error`** as the default.

Supported residual functions:

- `Mean Error`
- `Mean Absolute Error`
- `Mean Percentage Error`
- `Mean Absolute Percentage Error`
- `Mean Squared Error`

Percentage residual denominator rule:

- use `measure` as the denominator when the measured value is nonzero
- use `1` when the measured value is zero

### Unified multi-boundary residual hierarchy

For custom optimization, including steady-state multi-boundary estimation, always compute residuals with this hierarchy:

1. **Point deviation**

   `e(b, v, k) = sim(b, v, k) - measure(b, v, k)`

2. **Single-variable residual**

   `R(b, v) = phi({e(b, v, k)})`

   `phi` is the selected residual function.

3. **Single-boundary residual**

   `B(b) = mean_v(R(b, v))`

   This is a diagnostic value only.

4. **Total residual**

   `J = sum_b sum_v abs(w(b, v) * R(b, v))`

   This is the optimizer objective.

Rules:

- Do **not** average again across boundaries.
- Do **not** add a second boundary-level weighting layer.
- If one boundary should count more, push that priority into the variable weights under that boundary.
- Default variable weight is `1.0`.

### Dynamic estimation rule

For dynamic estimation:

- keep simulation points inside `[estimateStart, estimateEnd]`
- interpolate measured data onto simulation timestamps when the grids differ
- compute `R(b, v)` from the whole time window with the selected residual function

### Steady-state estimation rule

For steady-state estimation:

- 稳态场景应提供稳态时间
- 若未提供，则默认使用参数估计结束时间作为稳态时间
- if the simulation output does not contain that exact time, interpolate the simulation value
- compare only the single steady-state value
- compute `R(b, v)` from that single point with the selected residual function

## Multi-boundary experiment notes

### Native MPE multi-boundary configuration

Use:

```python
mpe.NewExp("exp1")
mpe.ConfigMultiBoundaryExp(
    "exp1",
    path=r"C:\path\measure.csv",
    boundaryParameter=["CarBody.L", "gearBox.ratio"],
    boundaryParameterVal=[
        [4.7, 4.17],
        [4.7, 2.34],
        [3.8, 4.17],
        [3.8, 2.34],
    ],
    BoundaryVar=[{"CarBody.a": "acc"}],
)
```

Rules:

- `boundaryParameterVal` is row-oriented
- `BoundaryVar` maps simulation variable names to measured variable names
- do not call `SelectFixParam(...)` or `ConfigFixParam(...)` for multi-boundary experiments

### Native steady-state configuration

Use:

```python
mpe.NewExp("exp1")
mpe.ConfigSteadyStateExp(
    "exp1",
    r"C:\path\boundary.csv",
    r"C:\path\steady_state.csv",
    1000,
)
mpe.SetSimulateOption(0, 1000, 999, 1000, 500)
```

## Custom algorithm policy

### Directly supported custom algorithm names

- `lshade`
- `basic-de`
- external optimizer adapter, when a local adapter module has been prepared

### Selection rule

- If the user explicitly asks for `basic-de`, use `basic-de`.
- If the user explicitly asks for `lshade`, use `lshade`.
- If the user supplies an adapter module, run it through the external optimizer adapter path.
- If the user asks for a custom algorithm but does not pick one, use `lshade`.
- If the user names an unsupported algorithm, do not pretend it is available. Research the algorithm, decide whether it fits the adapter contract, then either implement/register an adapter or explain why it is not suitable.

### Algorithm adapter contract

Use adapters to standardize integration of new optimizers. An adapter must:

- optimize a scalar objective where lower is better
- generate numeric parameter vectors that match the configured tuner parameters
- respect finite lower/upper bounds, or apply a documented transform before evaluation
- evaluate candidates through the shared batch callback, never by running Sysplorer directly
- emit progress records with the same history shape used by built-in algorithms
- return a result dictionary containing at least `algorithm`, `best`, and `history`

The external optimizer adapter receives a context object with:

- parameter metadata, names, bounds, and initial values
- boundary definitions and scenario settings
- a candidate clipping helper
- a shared batch-evaluation callback that returns total residuals and boundary details
- a progress emitter

Before an external adapter is called, the framework runs preflight validation and evaluates the configured initial parameter vector once. That evaluation is inserted as the first history item; the adapter must preserve it and append its own iteration records.

Implementation note: the script has internal adapter configuration fields. Use them only when generating a machine-readable config or editing the script; do not include them in user-facing capability lists or ordinary status summaries.

Adapter feasibility guidance:

- Good fit: derivative-free, bounded, expensive black-box optimizers such as DE variants, CMA-ES variants with bounds/repair, Bayesian optimization with low evaluation budgets, simulated annealing, tabu-style numeric search, and particle-swarm variants.
- Needs care: algorithms that are naturally unconstrained, require integer/discrete variables, or assume cheap objectives. Add transforms, repairs, or budget guards before using them.
- Poor fit by default: algorithms that require analytic gradients, Hessians, direct access to equations, millions of evaluations, or differentiability of the simulator.

### Current defaults

- default custom optimizer: `lshade`
- compatibility baseline: `basic-de`
- default residual: `Mean Absolute Percentage Error`
- failure penalty: `1e300`
- recommended `lshade` production run: population size `20`, max generations `100`
  (population size is a recommendation; when not configured explicitly the script derives it from the parameter dimension, while `max generations` defaults to `100`)
- recommended batch simulation parallel instances for stable long runs: `10`

`lshade` is the preferred default because it is more robust than the baseline DE path for bounded black-box search and usually needs fewer wasted evaluations on slow simulation problems.

Separate optimizer settings from simulation settings:

- Optimizer settings: algorithm, population size, max generations, and random seed.
- Simulation settings: solver algorithm, numerical tolerance, simulation time range, output options, and batch parallel instances.
- The random seed only makes stochastic initialization and evolution reproducible; it is not a required algorithm constant.
- Numerical tolerance is passed to the model solver during each batch simulation; it is not the `lshade` stopping tolerance.
- Solver algorithm is needed because every custom-optimizer candidate must be evaluated by running the Sysplorer model.

## Batch simulation policy

For custom optimization:

1. Candidate count = `N`
2. Boundary count = `B`
3. Flat batch run count = `N * B`

Pipeline:

1. repeat each candidate across every boundary
2. append boundary parameter values into the batch input rows
3. call `BatchSimulate(...)`
4. regroup the flat results back into one block per candidate
5. compute residuals and objective per candidate

This is the standard path for high-volume candidate evaluation in this skill.

## Script entry point

The reusable script in this skill is an internal execution asset. **The JSON
config it consumes is built by this skill from the user's optimization data; it
is not something the user is expected to author or submit.**

Who provides what:

- **User provides**: model file, tuner-parameter names and bounds, boundary
  conditions, measurement data, and any extra library dependencies.
- **This skill builds**: the JSON config (parameter list, boundary list,
  variable mappings, residual settings, algorithm settings, batch runtime) and
  writes it to a working file, then runs the script.

Workflow:

1. Collect the user's optimization data and confirm anything missing.
2. Build the config from that data, following the config structure in
   [`references/自定义批量参数估计说明.md`](references/自定义批量参数估计说明.md) §10.
3. Run preflight to validate the generated config; fix the config, not the user's
   data, when validation reports a problem.
4. Run the optimization and report results.

```bash
python scripts/custom_batch_optimizer.py --config <generated_config>.json --preflight --output preflight.json
python scripts/custom_batch_optimizer.py --config <generated_config>.json --output result.json
```

Live progress behavior:

- During optimization, write `progress.jsonl` next to the result JSON by default.
- Use `--progress-log path\\to\\progress.jsonl` to override the progress path.
- Each progress record includes the current stage, best residual, best parameters, failure flag, and per-boundary residual details.
- The first progress record is the configured initial-parameter evaluation.

Full config structure with all fields: see §10 of
[`references/自定义批量参数估计说明.md`](references/自定义批量参数估计说明.md).
Treat the config as an internal artifact: do not ask the user to author or submit it.

## Execution loop

1. **Clarify goal**: estimation vs design exploration vs optimization; inputs (measurements, parameters bounds).
2. **Pull references**: skim `references/参数估计使用说明.md` for operational flow; `references/DesignOptMpe.md` for API ordering; `references/自定义批量参数估计说明.md` for the custom path; demo notes under `references/` for runnable examples.
3. **Minimal script**: import module, reproduce smallest failing case, print structured status.
4. **Iterate** with `call_code` stdout/stderr; only then widen scope.

## Debugging checklist

- Run `--preflight` before long custom optimization.
- For user-provided models, ask for extra dependency libraries first. If none are provided, let the script infer and load dependencies before any model check, translation, or batch initialization.
- Inspect `progress.jsonl` while optimization is running; do not wait for the final JSON to diagnose a stalled run.
- Parameter names, variable names, experiment names, and measurement columns are case-sensitive and model-specific.
- For native multi-boundary MPE, never mix `ConfigMultiBoundaryExp(...)` with fixed-parameter APIs.
- For custom optimization, verify the batch runtime first:
  - model can open
  - required extra libraries are loaded
  - `InitialBatchSimulate(...)` returns `True`
  - requested simulation variables exist
  - candidate result count matches flat batch input count
- If the best point lands on bounds, tighten or revise bounds and rerun.
- If a custom run is too slow, first reduce population size or generations, then consider narrower bounds or fewer active variables.

## References

User-facing API and workflow references:

- [`references/DesignOptMpe.md`](references/DesignOptMpe.md)
- [`references/参数估计使用说明.md`](references/参数估计使用说明.md)
- [`references/参数估计demo说明.md`](references/参数估计demo说明.md)

Internal implementation reference (read to implement the custom path correctly;
do not surface its field names, script entry points, or config structure to users):

- [`references/自定义批量参数估计说明.md`](references/自定义批量参数估计说明.md)

## RAG hint

Call `resources_retrieval(action="corpora")` to confirm `design_opt_mpe_api` paths when manifest is deployed; use returned index paths for `action="search"` when you need full-text lookup beyond this skill.
