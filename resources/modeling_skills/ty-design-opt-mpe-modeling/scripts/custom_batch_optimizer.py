from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import random
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple


SUPPORTED_RESIDUALS = (
    "Mean Error",
    "Mean Absolute Error",
    "Mean Percentage Error",
    "Mean Absolute Percentage Error",
    "Mean Squared Error",
)
DEFAULT_RESIDUAL = "Mean Absolute Percentage Error"
FAIL_PENALTY = 1e300
LSHADE_DEFAULT_MAX_GENERATIONS = 100
LIBRARY_PREFIX_RE = re.compile(r"(?<![A-Za-z0-9_])([A-Z][A-Za-z0-9_]*)\s*\.")
LIBRARY_VERSION_SUFFIX_RE = re.compile(r"\s+\d+(?:\.\d+)*(?:\.[A-Za-z]+\.\d+)?$")


def _mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("mean() requires at least one value")
    return sum(values) / len(values)


def _clip(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, float(value)))


def _safe_denominator(measure: float) -> float:
    return measure if abs(measure) > 1e-12 else 1.0


def _dedupe(items: Sequence[str]) -> Tuple[str, ...]:
    seen = set()
    result: List[str] = []
    for item in items:
        name = str(item).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        result.append(name)
    return tuple(result)


def _path_exists(path: Path) -> bool:
    """Return False for malformed or inaccessible Windows paths instead of leaking OSError."""
    try:
        return path.exists()
    except (OSError, ValueError):
        return False


def _path_is_file(path: Path) -> bool:
    try:
        return path.is_file()
    except (OSError, ValueError):
        return False


def _library_root_from_mworks(mworks_exe: str) -> Optional[Path]:
    exe_path = Path(mworks_exe)
    if not _path_exists(exe_path):
        return None
    candidate = exe_path.parent.parent / "Library"
    return candidate if _path_exists(candidate) else None


def _installed_library_names(mworks_exe: str) -> Set[str]:
    library_root = _library_root_from_mworks(mworks_exe)
    if library_root is None:
        return set()
    names: Set[str] = set()
    for child in library_root.iterdir():
        if child.is_dir():
            names.add(child.name)
            names.add(LIBRARY_VERSION_SUFFIX_RE.sub("", child.name))
        elif child.suffix.lower() in {".mo", ".mol"}:
            names.add(child.stem)
            names.add(LIBRARY_VERSION_SUFFIX_RE.sub("", child.stem))
    return names


def infer_extra_libraries(model_path: str, mworks_exe: str) -> Tuple[str, ...]:
    path = Path(model_path)
    if not path.exists():
        return ()
    installed = _installed_library_names(mworks_exe)
    if not installed:
        return ()
    model_text = path.read_text(encoding="utf-8", errors="ignore")
    prefixes = set(LIBRARY_PREFIX_RE.findall(model_text))
    return tuple(sorted((prefixes & installed) - {"Modelica"}))


def _interp_series(times: Sequence[float], values: Sequence[float], target_time: float) -> float:
    if not times or not values:
        raise ValueError("Cannot interpolate an empty series")
    if len(times) != len(values):
        raise ValueError(f"Time/value length mismatch: {len(times)} vs {len(values)}")
    if target_time <= float(times[0]):
        return float(values[0])
    if target_time >= float(times[-1]):
        return float(values[-1])
    for idx in range(1, len(times)):
        t0 = float(times[idx - 1])
        t1 = float(times[idx])
        if t0 <= target_time <= t1:
            y0 = float(values[idx - 1])
            y1 = float(values[idx])
            if t1 == t0:
                return y0
            ratio = (target_time - t0) / (t1 - t0)
            return y0 + ratio * (y1 - y0)
    return float(values[-1])


def _series_window(
    times: Sequence[float],
    values: Sequence[float],
    start_time: float,
    end_time: float,
) -> Tuple[List[float], List[float]]:
    selected_times: List[float] = []
    selected_values: List[float] = []
    for t, y in zip(times, values):
        tf = float(t)
        if start_time <= tf <= end_time:
            selected_times.append(tf)
            selected_values.append(float(y))
    return selected_times, selected_values


def _residual_from_points(residual_func: str, sim_values: Sequence[float], measure_values: Sequence[float]) -> float:
    if residual_func not in SUPPORTED_RESIDUALS:
        raise ValueError(f"Unsupported residual function: {residual_func}")
    if len(sim_values) != len(measure_values):
        raise ValueError(f"Residual input length mismatch: {len(sim_values)} vs {len(measure_values)}")
    if not sim_values:
        raise ValueError("Residual requires at least one sample")
    errors = [float(sim) - float(measure) for sim, measure in zip(sim_values, measure_values)]
    if residual_func == "Mean Error":
        return _mean(errors)
    if residual_func == "Mean Absolute Error":
        return _mean([abs(e) for e in errors])
    if residual_func == "Mean Percentage Error":
        return _mean([e / _safe_denominator(float(measure)) for e, measure in zip(errors, measure_values)])
    if residual_func == "Mean Absolute Percentage Error":
        return _mean([abs(e / _safe_denominator(float(measure))) for e, measure in zip(errors, measure_values)])
    if residual_func == "Mean Squared Error":
        return _mean([e * e for e in errors])
    raise AssertionError("Unreachable residual branch")


@dataclass(frozen=True)
class ParameterSpec:
    name: str
    lower: float
    upper: float
    initial: float


@dataclass(frozen=True)
class VariableTarget:
    sim_var: str
    measure_key: str
    weight: float = 1.0


@dataclass(frozen=True)
class BoundaryCase:
    name: str
    params: Dict[str, float]
    variables: List[VariableTarget]


@dataclass(frozen=True)
class ScenarioConfig:
    model_path: str
    model_name: str
    mworks_exe: str
    simulate_start: float
    simulate_end: float
    estimate_start: float
    estimate_end: float
    step_number: int = 500
    steady_state_time: Optional[float] = None
    residual_func: str = DEFAULT_RESIDUAL
    failure_penalty: float = FAIL_PENALTY
    output_step: Optional[float] = None
    save_event: bool = False
    algorithm: str = "lshade"
    population_size: Optional[int] = None
    max_generations: Optional[int] = None
    seed: int = 20260630
    tolerance: float = 1e-6
    solver_algorithm: str = "Dassl"
    extra_libraries: Tuple[str, ...] = ()
    auto_infer_libraries: bool = True
    algorithm_settings: Dict[str, Any] = field(default_factory=dict)
    adapter_module_path: Optional[str] = None
    adapter_callable: str = "run_optimizer"

    @property
    def is_steady_state(self) -> bool:
        return self.steady_state_time is not None

    @property
    def target_time(self) -> float:
        return self.steady_state_time if self.steady_state_time is not None else self.estimate_end

    @property
    def resolved_extra_libraries(self) -> Tuple[str, ...]:
        inferred = infer_extra_libraries(self.model_path, self.mworks_exe) if self.auto_infer_libraries else ()
        return _dedupe([*self.extra_libraries, *inferred])


@dataclass
class TimeSeriesMeasurements:
    time_column: str
    times: List[float]
    columns: Dict[str, List[float]]


@dataclass
class MeasurementBundle:
    steady_values: Dict[str, float] = field(default_factory=dict)
    time_series: Optional[TimeSeriesMeasurements] = None


@dataclass
class BatchRuntimeConfig:
    solver_path: str
    store_path: str
    inst_num: int


@dataclass
class CandidateEvaluation:
    params: Dict[str, float]
    total_residual: float
    boundary_details: List[Dict[str, Any]]
    failed: bool


class ProgressLogger:
    def __init__(self, path: Optional[str] = None):
        self.path = Path(path) if path else None
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("", encoding="utf-8")

    def emit(self, entry: Dict[str, Any]) -> None:
        if self.path:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
        boundary_parts = []
        for detail in entry.get("boundary_details", []):
            boundary_parts.append(f"{detail.get('boundary_name')}={detail.get('boundary_residual')}")
        suffix = "" if not boundary_parts else " | boundaries: " + ", ".join(boundary_parts)
        print(
            f"[progress] {entry.get('stage')} best_residual={entry.get('best_residual')} "
            f"failed={entry.get('failed')}{suffix}",
            flush=True,
        )


def load_measurements_from_config(config: Dict[str, Any]) -> MeasurementBundle:
    measurement_mode = (config.get("measurement_mode") or "steady").strip().lower()
    if measurement_mode == "steady":
        steady_values = config.get("steady_measurements") or {}
        return MeasurementBundle(
            steady_values={str(k): float(v) for k, v in steady_values.items()},
            time_series=None,
        )
    if measurement_mode == "timeseries":
        csv_info = config.get("timeseries_csv") or {}
        csv_path = csv_info.get("path")
        if not csv_path:
            raise ValueError("timeseries measurement mode requires timeseries_csv.path")
        time_column = csv_info.get("time_column") or "time"
        with open(csv_path, newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        if not rows:
            raise ValueError(f"Measurement CSV is empty: {csv_path}")
        times = [float(row[time_column]) for row in rows]
        columns: Dict[str, List[float]] = {}
        for key in rows[0].keys():
            if not key or key == time_column:
                continue
            columns[key] = [float(row[key]) for row in rows]
        return MeasurementBundle(
            steady_values={},
            time_series=TimeSeriesMeasurements(time_column=time_column, times=times, columns=columns),
        )
    raise ValueError(f"Unsupported measurement_mode: {measurement_mode}")


def load_boundary_cases(boundary_items: Sequence[Dict[str, Any]], default_variable_targets: Sequence[Dict[str, Any]]) -> List[BoundaryCase]:
    if not boundary_items:
        return [
            BoundaryCase(
                name="boundary_1",
                params={},
                variables=[
                    VariableTarget(
                        sim_var=str(item["sim_var"]),
                        measure_key=str(item["measure_key"]),
                        weight=float(item.get("weight", 1.0)),
                    )
                    for item in default_variable_targets
                ],
            )
        ]
    cases: List[BoundaryCase] = []
    for idx, item in enumerate(boundary_items, start=1):
        variables = item.get("variables") or default_variable_targets
        cases.append(
            BoundaryCase(
                name=str(item.get("name") or f"boundary_{idx}"),
                params={str(k): float(v) for k, v in (item.get("params") or {}).items()},
                variables=[
                    VariableTarget(
                        sim_var=str(var["sim_var"]),
                        measure_key=str(var["measure_key"]),
                        weight=float(var.get("weight", 1.0)),
                    )
                    for var in variables
                ],
            )
        )
    return cases


def parse_config(config_path: str) -> Tuple[ScenarioConfig, List[ParameterSpec], List[BoundaryCase], MeasurementBundle, BatchRuntimeConfig]:
    with open(config_path, encoding="utf-8") as handle:
        config = json.load(handle)
    scenario_info = config["scenario"]
    scenario = ScenarioConfig(
        model_path=str(config["model_path"]),
        model_name=str(config["model_name"]),
        mworks_exe=str(config["mworks_exe"]),
        simulate_start=float(scenario_info["simulate_start"]),
        simulate_end=float(scenario_info["simulate_end"]),
        estimate_start=float(scenario_info["estimate_start"]),
        estimate_end=float(scenario_info["estimate_end"]),
        step_number=int(scenario_info.get("step_number", 500)),
        steady_state_time=(
            None
            if scenario_info.get("steady_state_time") is None
            else float(scenario_info["steady_state_time"])
        ),
        residual_func=str(scenario_info.get("residual_func", DEFAULT_RESIDUAL)),
        failure_penalty=float(scenario_info.get("failure_penalty", FAIL_PENALTY)),
        output_step=None if scenario_info.get("output_step") is None else float(scenario_info["output_step"]),
        save_event=bool(scenario_info.get("save_event", False)),
        algorithm=str(scenario_info.get("algorithm", "lshade")),
        population_size=(
            None if scenario_info.get("population_size") is None else int(scenario_info["population_size"])
        ),
        max_generations=(
            None if scenario_info.get("max_generations") is None else int(scenario_info["max_generations"])
        ),
        seed=int(scenario_info.get("seed", 20260630)),
        tolerance=float(scenario_info.get("tolerance", 1e-6)),
        solver_algorithm=str(scenario_info.get("solver_algorithm", "Dassl")),
        extra_libraries=tuple(str(item) for item in scenario_info.get("extra_libraries", [])),
        auto_infer_libraries=bool(scenario_info.get("auto_infer_libraries", True)),
        algorithm_settings=dict(scenario_info.get("algorithm_settings") or {}),
        adapter_module_path=(
            None
            if scenario_info.get("adapter_module_path") is None
            else str(scenario_info["adapter_module_path"])
        ),
        adapter_callable=str(scenario_info.get("adapter_callable", "run_optimizer")),
    )
    parameters = [
        ParameterSpec(
            name=str(item["name"]),
            lower=float(item["lower"]),
            upper=float(item["upper"]),
            initial=float(item["initial"]),
        )
        for item in config["parameters"]
    ]
    variable_targets = config.get("variable_targets") or []
    boundaries = load_boundary_cases(config.get("boundary_cases") or [], variable_targets)
    measurements = load_measurements_from_config(config)
    runtime = BatchRuntimeConfig(
        solver_path=str(config["batch_runtime"]["solver_path"]),
        store_path=str(config["batch_runtime"]["store_path"]),
        inst_num=int(config["batch_runtime"]["inst_num"]),
    )
    return scenario, parameters, boundaries, measurements, runtime


class DesignOptBatchBackend:
    def __init__(self, scenario: ScenarioConfig, runtime: BatchRuntimeConfig):
        self.scenario = scenario
        self.runtime = runtime
        self._prepared = False

    def prepare(self) -> None:
        if self._prepared:
            return
        import mworks.sysplorer as eng
        import mworks.sysplorer.DesignOptExp as exp

        self._eng = eng
        self._exp = exp
        Path(self.runtime.solver_path).mkdir(parents=True, exist_ok=True)
        Path(self.runtime.store_path).mkdir(parents=True, exist_ok=True)

        last_exc: Optional[Exception] = None
        for mode in ("-q", "-gui"):
            try:
                eng.StartSysplorer(mode, self.scenario.mworks_exe)
                version = eng.GetVersion()
                if version:
                    self.launch_mode = mode
                    self.sysplorer_version = version
                    break
            except Exception as exc:  # pragma: no cover - environment specific
                last_exc = exc
        else:
            raise last_exc or RuntimeError("Unable to connect to Sysplorer")

        eng.SetCompileSolver64(1)
        eng.LoadLibrary("Modelica")
        self.loaded_extra_libraries = self.scenario.resolved_extra_libraries
        for library_name in self.loaded_extra_libraries:
            eng.LoadLibrary(library_name)
        eng.OpenModelFile(self.scenario.model_path)
        try:
            eng.OpenModel(self.scenario.model_name)
        except Exception:
            pass

        options: Dict[str, Any] = {
            "startTime": self.scenario.simulate_start,
            "stopTime": self.scenario.simulate_end,
            "saveEvent": self.scenario.save_event,
            "algorithm": self.scenario.solver_algorithm,
            "tolerance": self.scenario.tolerance,
        }
        if self.scenario.output_step is not None:
            options["outputStep"] = self.scenario.output_step

        ok = exp.InitialBatchSimulate(
            modelName=self.scenario.model_name,
            solverPath=self.runtime.solver_path,
            storePath=self.runtime.store_path,
            instNum=self.runtime.inst_num,
            options=options,
        )
        if not ok:
            raise RuntimeError("InitialBatchSimulate failed")
        self._prepared = True

    def simulate_candidates(self, candidates: Sequence[Sequence[float]], parameters: Sequence[ParameterSpec], boundaries: Sequence[BoundaryCase]) -> List[List[Dict[str, Any]]]:
        self.prepare()
        unique_vars = sorted({var.sim_var for boundary in boundaries for var in boundary.variables})
        flat_params: List[Dict[str, float]] = []
        for candidate in candidates:
            tuner_values = {
                spec.name: float(value)
                for spec, value in zip(parameters, candidate)
            }
            for boundary in boundaries:
                row = dict(tuner_values)
                row.update(boundary.params)
                flat_params.append(row)
        raw_results = self._exp.BatchSimulate(flat_params, [unique_vars])
        if len(raw_results) != len(flat_params):
            raise RuntimeError(f"Unexpected batch result count: {len(raw_results)} vs {len(flat_params)}")

        grouped: List[List[Dict[str, Any]]] = []
        idx = 0
        for _ in candidates:
            grouped.append(raw_results[idx: idx + len(boundaries)])
            idx += len(boundaries)
        return grouped


class ResidualEngine:
    def __init__(self, scenario: ScenarioConfig, boundaries: Sequence[BoundaryCase], measurements: MeasurementBundle):
        self.scenario = scenario
        self.boundaries = list(boundaries)
        self.measurements = measurements

    def evaluate_candidate(
        self,
        parameters: Sequence[ParameterSpec],
        candidate_values: Sequence[float],
        boundary_results: Sequence[Dict[str, Any]],
    ) -> CandidateEvaluation:
        params = {spec.name: float(value) for spec, value in zip(parameters, candidate_values)}
        total_residual = 0.0
        boundary_details: List[Dict[str, Any]] = []
        any_failed = False

        for boundary, raw_result in zip(self.boundaries, boundary_results):
            variable_residuals: List[float] = []
            variable_details: List[Dict[str, Any]] = []
            boundary_failed = False
            for target in boundary.variables:
                try:
                    residual_value, sim_summary, measure_summary = self._evaluate_variable(raw_result, target)
                except Exception as exc:
                    boundary_failed = True
                    any_failed = True
                    residual_value = None
                    sim_summary = None
                    measure_summary = None
                    variable_details.append(
                        {
                            "simulate_variable": target.sim_var,
                            "measure_variable": target.measure_key,
                            "weight": target.weight,
                            "variable_residual": residual_value,
                            "failed": True,
                            "error": str(exc),
                            "sim_summary": sim_summary,
                            "measure_summary": measure_summary,
                        }
                    )
                    continue

                variable_residuals.append(residual_value)
                total_residual += abs(target.weight * residual_value)
                variable_details.append(
                    {
                        "simulate_variable": target.sim_var,
                        "measure_variable": target.measure_key,
                        "weight": target.weight,
                        "variable_residual": residual_value,
                        "failed": False,
                        "sim_summary": sim_summary,
                        "measure_summary": measure_summary,
                    }
                )

            boundary_residual = None if not variable_residuals else _mean(variable_residuals)
            boundary_details.append(
                {
                    "boundary_name": boundary.name,
                    "boundary_params": boundary.params,
                    "boundary_residual": boundary_residual,
                    "failed": boundary_failed,
                    "variables": variable_details,
                }
            )

        if any_failed:
            total_residual = self.scenario.failure_penalty

        return CandidateEvaluation(
            params=params,
            total_residual=total_residual,
            boundary_details=boundary_details,
            failed=any_failed,
        )

    def _evaluate_variable(self, raw_result: Dict[str, Any], target: VariableTarget) -> Tuple[float, Dict[str, Any], Dict[str, Any]]:
        if self.scenario.is_steady_state:
            sim_value = self._interpolate_sim_value(raw_result, target.sim_var, self.scenario.target_time)
            measure_value = float(self.measurements.steady_values[target.measure_key])
            residual = _residual_from_points(self.scenario.residual_func, [sim_value], [measure_value])
            return (
                residual,
                {"time": self.scenario.target_time, "value": sim_value},
                {"time": self.scenario.target_time, "value": measure_value},
            )

        if self.measurements.time_series is None:
            raise ValueError("Dynamic residuals require time_series measurements")
        time_series = self.measurements.time_series
        sim_times = [float(t) for t in (raw_result.get("time") or [])]
        sim_values = [float(v) for v in (raw_result.get(target.sim_var) or [])]
        if not sim_times or not sim_values:
            raise ValueError(f"Missing simulation series for {target.sim_var}")
        win_times, win_sim_values = _series_window(
            sim_times,
            sim_values,
            self.scenario.estimate_start,
            self.scenario.estimate_end,
        )
        if not win_times:
            raise ValueError(f"No simulation samples inside estimate window for {target.sim_var}")
        measure_values = time_series.columns.get(target.measure_key)
        if not measure_values:
            raise ValueError(f"Missing measurement series: {target.measure_key}")
        aligned_measure_values = [
            _interp_series(time_series.times, measure_values, current_time)
            for current_time in win_times
        ]
        residual = _residual_from_points(self.scenario.residual_func, win_sim_values, aligned_measure_values)
        return (
            residual,
            {
                "points": len(win_times),
                "time_start": win_times[0],
                "time_end": win_times[-1],
                "value_start": win_sim_values[0],
                "value_end": win_sim_values[-1],
            },
            {
                "points": len(aligned_measure_values),
                "time_start": win_times[0],
                "time_end": win_times[-1],
                "value_start": aligned_measure_values[0],
                "value_end": aligned_measure_values[-1],
            },
        )

    @staticmethod
    def _interpolate_sim_value(raw_result: Dict[str, Any], sim_var: str, target_time: float) -> float:
        values = raw_result.get(sim_var)
        if values is None:
            raise ValueError(f"Missing simulation variable: {sim_var}")
        if isinstance(values, (int, float)):
            return float(values)
        times = raw_result.get("time")
        if times is None:
            raise ValueError(f"Missing time series for: {sim_var}")
        return _interp_series([float(t) for t in times], [float(v) for v in values], target_time)


def latin_hypercube_population(parameters: Sequence[ParameterSpec], size: int, seed: int) -> List[List[float]]:
    rng = random.Random(seed)
    per_dimension: List[List[float]] = []
    for _ in parameters:
        values = [(i + rng.random()) / size for i in range(size)]
        rng.shuffle(values)
        per_dimension.append(values)
    population: List[List[float]] = []
    for member_idx in range(size):
        member: List[float] = []
        for dim_idx, spec in enumerate(parameters):
            normalized = per_dimension[dim_idx][member_idx]
            member.append(spec.lower + normalized * (spec.upper - spec.lower))
        population.append(member)
    if population:
        population[0] = [spec.initial for spec in parameters]
    return population


def clip_vector(values: Sequence[float], parameters: Sequence[ParameterSpec]) -> List[float]:
    if len(values) != len(parameters):
        raise ValueError(
            f"Candidate dimension mismatch: expected {len(parameters)}, got {len(values)}"
        )
    return [_clip(value, spec.lower, spec.upper) for value, spec in zip(values, parameters)]


def resolve_algorithm_name(name: str, dimension: int, adapter_module_path: Optional[str] = None) -> str:
    if adapter_module_path:
        return "python-module"
    normalized = (name or "lshade").strip().lower()
    if normalized in {"lshade", "l-shade"}:
        return "lshade"
    if normalized in {"de", "basic-de", "basic_de"}:
        return "basic-de"
    if normalized in {"python-module", "python_module", "external-python", "external_python"}:
        return "python-module"
    raise ValueError(
        f"Unsupported custom algorithm: {name}. "
        "Research the algorithm feasibility and provide an external optimizer adapter, "
        "or register a built-in adapter before running optimization."
    )


def display_algorithm_name(scenario: ScenarioConfig) -> str:
    normalized = (scenario.algorithm or "").strip().lower()
    if scenario.adapter_module_path or normalized in {
        "python-module",
        "python_module",
        "external-python",
        "external_python",
    }:
        return "external-optimizer-adapter"
    return scenario.algorithm


def evaluate_population(
    backend: DesignOptBatchBackend,
    residual_engine: ResidualEngine,
    parameters: Sequence[ParameterSpec],
    boundaries: Sequence[BoundaryCase],
    candidates: Sequence[Sequence[float]],
) -> List[CandidateEvaluation]:
    grouped_results = backend.simulate_candidates(candidates, parameters, boundaries)
    return [
        residual_engine.evaluate_candidate(parameters, candidate, boundary_results)
        for candidate, boundary_results in zip(candidates, grouped_results)
    ]


@dataclass
class OptimizerContext:
    backend: DesignOptBatchBackend
    residual_engine: ResidualEngine
    parameters: Sequence[ParameterSpec]
    boundaries: Sequence[BoundaryCase]
    scenario: ScenarioConfig
    progress: Optional[ProgressLogger] = None
    initial_evaluation: Optional[CandidateEvaluation] = None
    initial_history: Optional[Dict[str, Any]] = None

    @property
    def parameter_names(self) -> List[str]:
        return [spec.name for spec in self.parameters]

    @property
    def parameter_bounds(self) -> List[Tuple[float, float]]:
        return [(spec.lower, spec.upper) for spec in self.parameters]

    @property
    def initial_vector(self) -> List[float]:
        return initial_candidate_vector(self.parameters)

    def clip(self, values: Sequence[float]) -> List[float]:
        return clip_vector(values, self.parameters)

    def evaluate(self, candidates: Sequence[Sequence[float]]) -> List[CandidateEvaluation]:
        clipped = [self.clip(candidate) for candidate in candidates]
        return evaluate_population(self.backend, self.residual_engine, self.parameters, self.boundaries, clipped)

    def emit_progress(self, entry: Dict[str, Any]) -> None:
        if self.initial_history is not None and entry.get("stage") == "initial_parameter":
            return
        if self.progress:
            self.progress.emit(entry)


def initial_candidate_vector(parameters: Sequence[ParameterSpec]) -> List[float]:
    return [spec.initial for spec in parameters]


def initial_history_entry(evaluation: CandidateEvaluation) -> Dict[str, Any]:
    return {
        "stage": "initial_parameter",
        "iteration": 0,
        "best_residual": evaluation.total_residual,
        "best_params": evaluation.params,
        "failed": evaluation.failed,
        "boundary_details": evaluation.boundary_details,
    }


def best_history_entry(
    stage: str,
    best: CandidateEvaluation,
    population_size: Optional[int] = None,
    improved_members: Optional[int] = None,
) -> Dict[str, Any]:
    entry: Dict[str, Any] = {
        "stage": stage,
        "best_residual": best.total_residual,
        "best_params": best.params,
        "failed": best.failed,
        "boundary_details": best.boundary_details,
    }
    if population_size is not None:
        entry["population_size"] = population_size
    if improved_members is not None:
        entry["improved_members"] = improved_members
    return entry


def run_basic_de(
    backend: DesignOptBatchBackend,
    residual_engine: ResidualEngine,
    parameters: Sequence[ParameterSpec],
    boundaries: Sequence[BoundaryCase],
    scenario: ScenarioConfig,
    progress: Optional[ProgressLogger] = None,
) -> Dict[str, Any]:
    population_size = scenario.population_size or max(8, min(24, 6 * len(parameters)))
    max_generations = scenario.max_generations or 12
    rng = random.Random(scenario.seed)
    population = latin_hypercube_population(parameters, population_size, scenario.seed)
    initial_vector = initial_candidate_vector(parameters)
    initial_evaluation = evaluate_population(backend, residual_engine, parameters, boundaries, [initial_vector])[0]
    if population:
        population[0] = initial_vector
        evaluations = [initial_evaluation]
        if len(population) > 1:
            evaluations.extend(evaluate_population(backend, residual_engine, parameters, boundaries, population[1:]))
    else:
        evaluations = [initial_evaluation]
    scores = [item.total_residual for item in evaluations]
    best = min(evaluations, key=lambda item: item.total_residual)
    history = [
        initial_history_entry(initial_evaluation),
        best_history_entry("initial_population", best, population_size=population_size),
    ]
    if progress:
        progress.emit(history[0])
        progress.emit(history[1])

    for generation in range(1, max_generations + 1):
        trial_population: List[List[float]] = []
        for idx in range(population_size):
            choices = [i for i in range(population_size) if i != idx]
            a, b, c = rng.sample(choices, 3)
            mutant = [
                population[a][d] + 0.8 * (population[b][d] - population[c][d])
                for d in range(len(parameters))
            ]
            mutant = clip_vector(mutant, parameters)
            j_rand = rng.randrange(len(parameters))
            trial = [
                mutant[d] if rng.random() < 0.9 or d == j_rand else population[idx][d]
                for d in range(len(parameters))
            ]
            trial_population.append(clip_vector(trial, parameters))

        trial_evaluations = evaluate_population(backend, residual_engine, parameters, boundaries, trial_population)
        improved_members = 0
        for idx, trial_eval in enumerate(trial_evaluations):
            if trial_eval.total_residual <= scores[idx]:
                population[idx] = trial_population[idx]
                evaluations[idx] = trial_eval
                scores[idx] = trial_eval.total_residual
                improved_members += 1
        current_best = min(evaluations, key=lambda item: item.total_residual)
        if current_best.total_residual < best.total_residual:
            best = current_best
        history_entry = best_history_entry(
            f"generation_{generation}",
            best,
            population_size=population_size,
            improved_members=improved_members,
        )
        history.append(history_entry)
        if progress:
            progress.emit(history_entry)

    return {
        "algorithm": "basic-de",
        "population_size": population_size,
        "max_generations": max_generations,
        "best": {
            "params": best.params,
            "total_residual": best.total_residual,
            "failed": best.failed,
            "boundary_details": best.boundary_details,
        },
        "history": history,
    }


def _sample_cauchy(rng: random.Random, location: float, scale: float) -> float:
    value = location + scale * math.tan(math.pi * (rng.random() - 0.5))
    return value


def _sample_normal(rng: random.Random, mean: float, stddev: float) -> float:
    return rng.gauss(mean, stddev)


def _weighted_lehmer_mean(values: Sequence[float], weights: Sequence[float]) -> float:
    numerator = sum(w * v * v for v, w in zip(values, weights))
    denominator = sum(w * v for v, w in zip(values, weights))
    if abs(denominator) <= 1e-12:
        return _mean(values)
    return numerator / denominator


def run_lshade(
    backend: DesignOptBatchBackend,
    residual_engine: ResidualEngine,
    parameters: Sequence[ParameterSpec],
    boundaries: Sequence[BoundaryCase],
    scenario: ScenarioConfig,
    progress: Optional[ProgressLogger] = None,
) -> Dict[str, Any]:
    rng = random.Random(scenario.seed)
    dimension = len(parameters)
    initial_pop_size = scenario.population_size or max(18, min(60, 12 * dimension))
    min_pop_size = max(4, 4 * dimension)
    max_generations = scenario.max_generations or LSHADE_DEFAULT_MAX_GENERATIONS
    memory_size = 6
    memory_f = [0.5] * memory_size
    memory_cr = [0.5] * memory_size
    memory_index = 0
    archive: List[List[float]] = []

    population = latin_hypercube_population(parameters, initial_pop_size, scenario.seed)
    initial_vector = initial_candidate_vector(parameters)
    initial_evaluation = evaluate_population(backend, residual_engine, parameters, boundaries, [initial_vector])[0]
    if population:
        population[0] = initial_vector
        evaluations = [initial_evaluation]
        if len(population) > 1:
            evaluations.extend(evaluate_population(backend, residual_engine, parameters, boundaries, population[1:]))
    else:
        evaluations = [initial_evaluation]
    best = min(evaluations, key=lambda item: item.total_residual)
    history: List[Dict[str, Any]] = [
        initial_history_entry(initial_evaluation),
        best_history_entry("initial_population", best, population_size=len(population)),
    ]
    if progress:
        progress.emit(history[0])
        progress.emit(history[1])

    for generation in range(1, max_generations + 1):
        pop_size = len(population)
        ranked_indices = sorted(range(pop_size), key=lambda idx: evaluations[idx].total_residual)
        p_count = max(2, int(math.ceil(0.2 * pop_size)))
        trial_population: List[List[float]] = []
        trial_fs: List[float] = []
        trial_crs: List[float] = []

        for idx in range(pop_size):
            memory_slot = rng.randrange(memory_size)
            f = _sample_cauchy(rng, memory_f[memory_slot], 0.1)
            while f <= 0:
                f = _sample_cauchy(rng, memory_f[memory_slot], 0.1)
            f = min(f, 1.0)

            cr_center = memory_cr[memory_slot]
            if cr_center < 0:
                cr = 0.0
            else:
                cr = _sample_normal(rng, cr_center, 0.1)
            cr = min(1.0, max(0.0, cr))

            pbest_index = rng.choice(ranked_indices[:p_count])
            candidates_r1 = [j for j in range(pop_size) if j != idx]
            r1 = rng.choice(candidates_r1)
            population_and_archive = population + archive
            candidates_r2 = [
                j for j in range(len(population_and_archive))
                if j != idx and j != r1 and j != pbest_index
            ]
            r2 = rng.choice(candidates_r2)

            x = population[idx]
            xpbest = population[pbest_index]
            xr1 = population[r1]
            xr2 = population_and_archive[r2]
            mutant = [
                x[d] + f * (xpbest[d] - x[d]) + f * (xr1[d] - xr2[d])
                for d in range(dimension)
            ]
            mutant = clip_vector(mutant, parameters)
            j_rand = rng.randrange(dimension)
            trial = [
                mutant[d] if rng.random() < cr or d == j_rand else x[d]
                for d in range(dimension)
            ]
            trial_population.append(clip_vector(trial, parameters))
            trial_fs.append(f)
            trial_crs.append(cr)

        trial_evaluations = evaluate_population(backend, residual_engine, parameters, boundaries, trial_population)

        successful_f: List[float] = []
        successful_cr: List[float] = []
        successful_delta: List[float] = []
        improved_members = 0

        for idx, trial_eval in enumerate(trial_evaluations):
            delta = evaluations[idx].total_residual - trial_eval.total_residual
            if trial_eval.total_residual <= evaluations[idx].total_residual:
                archive.append(population[idx][:])
                population[idx] = trial_population[idx]
                evaluations[idx] = trial_eval
                improved_members += 1
                if delta > 0:
                    successful_f.append(trial_fs[idx])
                    successful_cr.append(trial_crs[idx])
                    successful_delta.append(delta)

        if successful_f:
            memory_f[memory_index] = _weighted_lehmer_mean(successful_f, successful_delta)
            memory_cr[memory_index] = _mean(successful_cr)
            memory_index = (memory_index + 1) % memory_size

        max_archive_size = max(1, len(population))
        if len(archive) > max_archive_size:
            rng.shuffle(archive)
            archive = archive[:max_archive_size]

        target_pop_size = int(
            round(initial_pop_size - (initial_pop_size - min_pop_size) * generation / max_generations)
        )
        target_pop_size = max(min_pop_size, target_pop_size)
        if len(population) > target_pop_size:
            ranked_pairs = sorted(
                zip(population, evaluations),
                key=lambda item: item[1].total_residual,
            )
            ranked_pairs = ranked_pairs[:target_pop_size]
            population = [member for member, _ in ranked_pairs]
            evaluations = [evaluation for _, evaluation in ranked_pairs]

        current_best = min(evaluations, key=lambda item: item.total_residual)
        if current_best.total_residual < best.total_residual:
            best = current_best

        history_entry = best_history_entry(
            f"generation_{generation}",
            best,
            population_size=len(population),
            improved_members=improved_members,
        )
        history.append(history_entry)
        if progress:
            progress.emit(history_entry)

    return {
        "algorithm": "lshade",
        "initial_population_size": initial_pop_size,
        "final_population_size": len(population),
        "max_generations": max_generations,
        "best": {
            "params": best.params,
            "total_residual": best.total_residual,
            "failed": best.failed,
            "boundary_details": best.boundary_details,
        },
        "history": history,
    }


def run_python_module_adapter(context: OptimizerContext) -> Dict[str, Any]:
    module_path = context.scenario.adapter_module_path
    if not module_path:
        raise ValueError("External optimizer adapter requires an adapter module path")
    path = Path(module_path)
    if not _path_is_file(path):
        raise ValueError(f"Optimizer adapter module does not exist: {module_path}")
    module_name = f"custom_optimizer_adapter_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load optimizer adapter module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    module_dir = str(path.parent)
    sys.path.insert(0, module_dir)
    try:
        spec.loader.exec_module(module)
    finally:
        if sys.path and sys.path[0] == module_dir:
            sys.path.pop(0)
    adapter = getattr(module, context.scenario.adapter_callable, None)
    if not callable(adapter):
        raise ValueError("Optimizer adapter module must define the configured entry function")
    result = adapter(context)
    if not isinstance(result, dict):
        raise ValueError("Optimizer adapter must return a result dictionary")
    best = result.get("best")
    history = result.get("history")
    if not isinstance(best, dict):
        raise ValueError("Optimizer adapter result must contain a best dictionary")
    if not isinstance(history, list):
        raise ValueError("Optimizer adapter result must contain a history list")
    best_params = best.get("params")
    if not isinstance(best_params, dict):
        raise ValueError("Optimizer adapter best result must contain a params dictionary")
    expected_names = set(context.parameter_names)
    if set(best_params) != expected_names:
        raise ValueError(
            "Optimizer adapter best parameter names do not match the configured tuner parameters"
        )
    for spec in context.parameters:
        value = best_params[spec.name]
        if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
            raise ValueError(f"Optimizer adapter returned a non-finite best parameter: {spec.name}")
        if not spec.lower <= float(value) <= spec.upper:
            raise ValueError(f"Optimizer adapter returned an out-of-bounds best parameter: {spec.name}")
    best_residual = best.get("total_residual")
    if not isinstance(best_residual, (int, float)) or not math.isfinite(float(best_residual)):
        raise ValueError("Optimizer adapter best result must contain a finite total_residual")
    if not isinstance(best.get("boundary_details"), list):
        raise ValueError("Optimizer adapter best result must contain boundary_details")
    if context.initial_history is None:
        raise RuntimeError("Initial parameter evaluation was not prepared before adapter execution")
    if history and isinstance(history[0], dict) and history[0].get("stage") == "initial_parameter":
        history[0] = context.initial_history
    else:
        history.insert(0, context.initial_history)
    required_history_keys = {"stage", "best_residual", "best_params", "boundary_details", "failed"}
    for entry in history:
        if not isinstance(entry, dict) or not required_history_keys.issubset(entry):
            raise ValueError(
                "Optimizer adapter history entries must contain stage, best_residual, "
                "best_params, boundary_details, and failed"
            )
    result.setdefault("algorithm", display_algorithm_name(context.scenario))
    return result


def run_custom_optimization(config_path: str, progress_log_path: Optional[str] = None) -> Dict[str, Any]:
    preflight = preflight_config(config_path)
    if not preflight["ok"]:
        messages = "; ".join(item["message"] for item in preflight["issues"] if item["level"] == "error")
        raise ValueError(f"Preflight validation failed: {messages}")
    scenario, parameters, boundaries, measurements, runtime = parse_config(config_path)
    backend = DesignOptBatchBackend(scenario, runtime)
    residual_engine = ResidualEngine(scenario, boundaries, measurements)
    algorithm = resolve_algorithm_name(scenario.algorithm, len(parameters), scenario.adapter_module_path)
    progress = ProgressLogger(progress_log_path) if progress_log_path else None
    context = OptimizerContext(
        backend=backend,
        residual_engine=residual_engine,
        parameters=parameters,
        boundaries=boundaries,
        scenario=scenario,
        progress=progress,
    )
    started_at = time.time()
    if algorithm == "lshade":
        result = run_lshade(backend, residual_engine, parameters, boundaries, scenario, progress=progress)
    elif algorithm == "basic-de":
        result = run_basic_de(backend, residual_engine, parameters, boundaries, scenario, progress=progress)
    elif algorithm == "python-module":
        initial_evaluation = context.evaluate([context.initial_vector])[0]
        context.initial_evaluation = initial_evaluation
        context.initial_history = initial_history_entry(initial_evaluation)
        context.emit_progress(context.initial_history)
        result = run_python_module_adapter(context)
    else:  # pragma: no cover - guarded by resolve_algorithm_name
        raise ValueError(f"Unexpected algorithm: {algorithm}")

    result["scenario"] = {
        "model_path": scenario.model_path,
        "model_name": scenario.model_name,
        "simulate_time": [scenario.simulate_start, scenario.simulate_end],
        "estimate_time": [scenario.estimate_start, scenario.estimate_end],
        "steady_state_time": scenario.steady_state_time,
        "residual_func": scenario.residual_func,
        "algorithm": display_algorithm_name(scenario),
        "failure_penalty": scenario.failure_penalty,
        "boundary_count": len(boundaries),
        "parameter_count": len(parameters),
    }
    result["parameters"] = [
        {
            "name": spec.name,
            "lower": spec.lower,
            "upper": spec.upper,
            "initial": spec.initial,
        }
        for spec in parameters
    ]
    result["boundaries"] = [
        {
            "name": boundary.name,
            "params": boundary.params,
            "variables": [
                {
                    "sim_var": var.sim_var,
                    "measure_key": var.measure_key,
                    "weight": var.weight,
                }
                for var in boundary.variables
            ],
        }
        for boundary in boundaries
    ]
    result["runtime"] = {
        "solver_path": runtime.solver_path,
        "store_path": runtime.store_path,
        "inst_num": runtime.inst_num,
        "launch_mode": getattr(backend, "launch_mode", None),
        "sysplorer_version": getattr(backend, "sysplorer_version", None),
        "elapsed_seconds": time.time() - started_at,
    }
    return result


def preflight_config(config_path: str) -> Dict[str, Any]:
    scenario, parameters, boundaries, measurements, runtime = parse_config(config_path)
    issues: List[Dict[str, str]] = []

    def issue(level: str, message: str) -> None:
        issues.append({"level": level, "message": message})

    model_path = Path(scenario.model_path)
    mworks_path = Path(scenario.mworks_exe)
    if not _path_is_file(model_path):
        issue("error", f"Model file does not exist: {scenario.model_path}")
        model_text = ""
    else:
        try:
            model_text = model_path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, ValueError) as exc:
            issue("error", f"Model file cannot be read: {exc}")
            model_text = ""
    if not _path_is_file(mworks_path):
        issue("error", f"Sysplorer executable does not exist: {scenario.mworks_exe}")
    if scenario.residual_func not in SUPPORTED_RESIDUALS:
        issue("error", f"Unsupported residual function: {scenario.residual_func}")
    try:
        resolved_algorithm = resolve_algorithm_name(scenario.algorithm, len(parameters), scenario.adapter_module_path)
    except Exception as exc:
        issue("error", str(exc))
        resolved_algorithm = scenario.algorithm
    if resolved_algorithm == "python-module":
        if not scenario.adapter_module_path:
            issue("error", "External optimizer adapter requires an adapter module path")
        elif not _path_is_file(Path(scenario.adapter_module_path)):
            issue("error", f"Optimizer adapter module does not exist: {scenario.adapter_module_path}")
    if not parameters:
        issue("error", "At least one tuner parameter is required")
    parameter_names = [spec.name for spec in parameters]
    if any(not name.strip() for name in parameter_names):
        issue("error", "Tuner parameter names must not be empty")
    if len(parameter_names) != len(set(parameter_names)):
        issue("error", "Tuner parameter names must be unique")
    if not boundaries:
        issue("error", "At least one boundary is required")
    for boundary in boundaries:
        if not boundary.variables:
            issue("error", f"Boundary has no variable mappings: {boundary.name}")
        for variable in boundary.variables:
            if not variable.sim_var.strip():
                issue("error", f"Simulation variable name is empty: {boundary.name}")
            if not variable.measure_key.strip():
                issue("error", f"Measurement variable name is empty: {boundary.name}")
    if scenario.simulate_end <= scenario.simulate_start:
        issue("error", "Simulation end time must be greater than start time")
    if scenario.estimate_end < scenario.estimate_start:
        issue("error", "Estimate end time must be greater than or equal to estimate start time")
    for label, value in (
        ("simulate_start", scenario.simulate_start),
        ("simulate_end", scenario.simulate_end),
        ("estimate_start", scenario.estimate_start),
        ("estimate_end", scenario.estimate_end),
    ):
        if not math.isfinite(value):
            issue("error", f"{label} must be finite")
    if scenario.steady_state_time is not None and not math.isfinite(scenario.steady_state_time):
        issue("error", "Steady-state time must be finite")
    if scenario.estimate_start < scenario.simulate_start or scenario.estimate_end > scenario.simulate_end:
        issue("error", "Estimate time window must be inside the simulation time range")
    if scenario.steady_state_time is not None and not (
        scenario.simulate_start <= scenario.steady_state_time <= scenario.simulate_end
    ):
        issue("error", "Steady-state time must be inside the simulation time range")
    if scenario.step_number <= 0:
        issue("error", "Simulation step number must be positive")
    if scenario.tolerance <= 0 or not math.isfinite(scenario.tolerance):
        issue("error", "Simulation tolerance must be a positive finite number")
    if scenario.failure_penalty < 0 or not math.isfinite(scenario.failure_penalty):
        issue("error", "Failure penalty must be a non-negative finite number")
    if runtime.inst_num <= 0:
        issue("error", "Batch simulation parallel instances must be positive")
    if scenario.population_size is not None and scenario.population_size < 4:
        issue("error", "Custom optimizer population size must be at least 4")
    if scenario.max_generations is not None and scenario.max_generations < 1:
        issue("error", "Custom optimizer max_generations must be at least 1")
    for spec in parameters:
        if not all(math.isfinite(value) for value in (spec.lower, spec.upper, spec.initial)):
            issue("error", f"Parameter bounds and initial value must be finite: {spec.name}")
        if spec.upper < spec.lower:
            issue("error", f"Parameter upper bound is lower than lower bound: {spec.name}")
        if not (spec.lower <= spec.initial <= spec.upper):
            issue("error", f"Parameter initial value is outside bounds: {spec.name}")
        if model_text and spec.name not in model_text:
            issue("warning", f"Parameter name was not found in model text: {spec.name}")
    if scenario.is_steady_state:
        required_measurements = {var.measure_key for boundary in boundaries for var in boundary.variables}
        missing = sorted(required_measurements - set(measurements.steady_values.keys()))
        for key in missing:
            issue("error", f"Missing steady measurement: {key}")
    elif measurements.time_series is None:
        issue("error", "Dynamic estimation requires time-series measurements")
    elif measurements.time_series is not None:
        time_series = measurements.time_series
        required_measurements = {var.measure_key for boundary in boundaries for var in boundary.variables}
        missing = sorted(required_measurements - set(time_series.columns))
        for key in missing:
            issue("error", f"Missing measurement column: {key}")
        if any(not math.isfinite(value) for value in time_series.times):
            issue("error", "Measurement time values must be finite")
        if any(time_series.times[idx] > time_series.times[idx + 1] for idx in range(len(time_series.times) - 1)):
            issue("error", "Measurement time values must be sorted in ascending order")
        if time_series.times:
            if scenario.estimate_start < time_series.times[0] or scenario.estimate_end > time_series.times[-1]:
                issue("error", "Measurement data does not cover the complete estimation time window")
    for boundary in boundaries:
        for name in boundary.params:
            if model_text and name not in model_text:
                issue("warning", f"Boundary parameter name was not found in model text: {name}")
            if not math.isfinite(boundary.params[name]):
                issue("error", f"Boundary parameter value must be finite: {boundary.name}/{name}")
        for var in boundary.variables:
            if model_text and var.sim_var not in model_text:
                issue("warning", f"Simulation variable name was not found in model text: {var.sim_var}")
            if not math.isfinite(var.weight) or var.weight < 0:
                issue("error", f"Variable weight must be non-negative: {boundary.name}/{var.measure_key}")
    return {
        "ok": not any(item["level"] == "error" for item in issues),
        "issues": issues,
        "summary": {
            "model_name": scenario.model_name,
            "parameter_count": len(parameters),
            "boundary_count": len(boundaries),
            "residual_func": scenario.residual_func,
            "algorithm": display_algorithm_name(scenario),
            "optimizer_path": "external-adapter" if resolved_algorithm == "python-module" else resolved_algorithm,
            "solver_path": runtime.solver_path,
            "store_path": runtime.store_path,
            "inst_num": runtime.inst_num,
        },
    }


def default_progress_log_path(output_path: Optional[str], config_path: str) -> str:
    if output_path:
        return str(Path(output_path).parent / "progress.jsonl")
    _, _, _, _, runtime = parse_config(config_path)
    return str(Path(runtime.store_path).parent / "progress.jsonl")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run custom high-performance parameter estimation with batch simulation and unified multi-boundary residuals."
    )
    parser.add_argument("--config", required=True, help="Path to the JSON config file.")
    parser.add_argument("--output", required=False, help="Optional JSON output path.")
    parser.add_argument("--progress-log", required=False, help="Optional JSONL progress output path.")
    parser.add_argument("--preflight", action="store_true", help="Validate the config and model references without running optimization.")
    args = parser.parse_args()

    if args.preflight:
        result = preflight_config(args.config)
    else:
        progress_log = args.progress_log or default_progress_log_path(args.output, args.config)
        result = run_custom_optimization(args.config, progress_log_path=progress_log)
        result.setdefault("runtime", {})["progress_log_path"] = progress_log
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
    print(output_json)


if __name__ == "__main__":
    main()
