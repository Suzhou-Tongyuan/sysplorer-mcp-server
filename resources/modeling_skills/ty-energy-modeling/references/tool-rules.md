# Tool Rules

## Session

Session setup, reuse, `starting` handling, error-envelope parsing, and classified retry are owned by `../../ty-sysplorer-modeling-rules/references/shared-standards.md`. Offline/source-only tasks make no live calls. Do not ensure/restart before every action; do not interpret `starting:true` as permission to start another GUI. Distinguish invalid arguments, missing library/class, load failure, timeout, and partial success before retrying.

## Libraries

Load only the energy libraries and dependencies actually selected by the parent task; do not load all four families unconditionally. Preserve sufficient standard components and other approved subsystem libraries. The energy-subsystem whitelist includes photovoltaic, wind, battery, integrated energy, and `Modelica 4.0.0.TY.1`; it is not a whitelist for the complete cross-domain delivery.

Use `get_lib_model_document` for uncertain class/parameter semantics. Missing documentation, missing libraries, and load failures do not prove a standard-library capability gap. The fixed Modelica version is not overridden by an installed newer version or latest resolution. `library_prepare` exists only when exposed for lite/mols; do not assume it exists in desktop Sysplorer.

## Models

Use `model_manager(action="new", model_name=..., restriction="model")` to create a model, `action="open"` for a loaded fully qualified class name, and `action="load_file", file_path=...` for a model/package file. Package loading uses its top-level `package.mo` as required by the returned load target.

Use `model_manager(action="save", model_name=...)` for in-place SaveModel; use `action="save_as", folder=...` for a task-specific destination. Verify returned `saved_path` and actual artifact, not merely success text.

Use `model_inspect(action="get_components")` / `get_component_ports` / `lookup_component` / `get_model_text` with the required model/instance fields. Use `session_manager(action="get_loaded_models")` for top-level loaded inventory, and explicit package names for deeper `model_inspect(action="get_classes")` queries. Use the separate `compare_model` tool for comparisons. Do not send retired inspection/comparison actions to `model_manager`.

## Layout

Call `smart_layout(mode="layout_only")` to compute layout from graph JSON.

Call `smart_layout(mode="writeback_mo")` only when writing Placement or Line data back to `.mo` text is required.

## Validation

MCP 0.4 check/translate/simulate preflight may automatically write layout to a cached user file even without `reload_mo_path`. They are not guaranteed read-only. Follow parent authorization boundaries; record actual graphical writes under Gate 6. Pure visual defects do not block execution; annotation syntax/structure errors do. `smart_layout` success, file writeback, official routing, persistence, and final diagram acceptance are separate evidence.

Validation depth follows the requested terminal stage; source-only and read-only tasks do not gain runtime checks from this document.

Call `check_model` after every structural change.

Call `check_model` after every parameter repair that can affect typing, units, constraints, or equations.

Treat a failing `CheckModel` as a hard block on simulation.

## Translation

Call `translate_model` after `CheckModel` succeeds when translation diagnostics, generated code, or toolchain validation are required.

Treat translation failure as a repair loop input, not as a success signal.

## Simulation

Call `simulate_model` only after the model passes the required validation gate for the current loop.

Set `verify_result_var` only when the agreed result criterion requires that signal. Otherwise omit it; simulation success alone may satisfy the request, with result review `not_required`.

Bind the requested simulation horizon to the documented simulation stop-time setting. `target_time` is a result probe time, not a stop-time substitute. Use short bring-up only within the agreed simulation scope.

## Results

Enter this section only when result review is requested or required by the agreed acceptance criterion. Do not create proxy observations to fill a checklist. Verify fresh successful-run or explicit-file provenance; stale readable results cannot turn a failed simulation into success. Preserve warning and identify official samples, linear interpolation, and out-of-range endpoint fallback.

Call `result_manager(action="get_result_variables")` to discover available result signals when the expected variable name is uncertain.

Call `result_manager(action="get_var_values")` for trends.

Call `result_manager(action="get_var_value_at")` for point checks such as end value or peak-adjacent inspection.

Call `plot_manager(action="plot_variables")` only when a visual trace materially helps judgment or debugging.

## Fallback

Use `call_code(mode="run_sysplorer_api", payload={...})` (or the compatible `run_script` alias) only for a narrow uncovered official API action after consulting `get_api_document`. `payload` is a required object; do not use retired asynchronous/readiness/workflow modes. Diagram export uses official `ExportDiagram` through this path, not manager export actions.

In `run_script`, explicitly import `mworks.sysplorer` before using Sysplorer APIs.
