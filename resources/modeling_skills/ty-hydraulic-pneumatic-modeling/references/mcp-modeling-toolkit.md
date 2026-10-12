# MCP Modeling Toolkit

Use MCP / Sysplorer official capabilities for platform actions. Use this skill for domain decisions.

MCP 0.4 classifications, session evidence, `starting`, failure parsing and retries are owned by `../../ty-sysplorer-modeling-rules/references/shared-standards.md`. Read the parent contract before platform actions; an offline or documentation-only task does not start Sysplorer.

| Stage | Preferred MCP Tool | Notes |
|---|---|---|
| Session and version | `session_manager` | Reuse valid parent evidence; first confirmation and justified recovery follow the parent policy. A `starting` response is not a reason to ensure/restart. |
| Library loading | `load_library` | Load only required components and dependencies. Commercial paths and standard/commercial combinations fix `Modelica 4.0.0.TY.1`. |
| Lifecycle | `model_manager` | New/load/open/save; `save` saves in place, `save_as` is explicit copy/save-as. Check `saved_path`. |
| Inspection | `model_inspect` | Classes, components, ports, model text and last errors use this tool; top-level loaded models use `session_manager(action="get_loaded_models")`. |
| API/class help | `get_api_document`, `get_lib_model_document` | Query actual public API/class details; distinguish missing class/library, load failure and partial document failure. |
| Unwrapped official APIs | `call_code(mode="run_sysplorer_api", payload={"python_source":"..."})` | Query API help first; script must explicitly import `mworks.sysplorer as ModelingPy`. Modelica construction remains text-first per parent. |
| Smart layout | `smart_layout` | Only when parent Gate 6 requires explicit repair. Record disk change, official routing and persistence separately. |
| Layout/line evidence | Both local `check_modelica_*.ps1` scripts with `-TargetClass <FQClass>` | Inspect only each changed class's direct annotations/connections; no nested or inherited layers. Preserve passed / failed / undetermined and diagnostics (see `scripts/README.md`). Visual findings do not block model check, translation or simulation. |
| Check/translation/simulation | `check_model`, `translate_model`, `simulate_model` | Execute only requested depth and required runtime prerequisites. These tools can automatically write layout; no old layout-parameter overrides. |
| Results | `result_manager` | Only when results are requested; simulate-only leaves `verify_result_var` unset. Preserve interpolation/endpoint warnings and reject stale-result success. |
| Plot/animation | `plot_manager` | Only requested visual result artifacts; it does not replace model-diagram export. |
| Diagram export | `get_api_document(api_function_name="ExportDiagram")` then `call_code` | Use the returned official signature with required payload; no retired manager export action. |
| Local reference search | `resources_retrieval` | Search authorized evidence only; concise references precede large manual text. |

## Safety Rules

- Do not use Sysplorer `ClearAll` or `ChangeDirectory`.
- Do not claim downstream stages after MCP session failure.
- Do not infer success from source text alone; use the relevant MCP result.
- When a generated model is written to disk, reload or check the exact file/model that will be delivered.

## Stage-to-Tool Pattern

Use the parent gate sequence with domain additions in the selected workflow; do not equate tool categories with gates.

- Check, translation and simulation can automatically layout/reload a user `.mo` found through file cache even when `reload_mo_path` is omitted. Read-only diagnostics require an authorized copy or a documented limitation; do not bypass the dedicated tools through scripts.
- Record changed graphical targets, `preflight_steps`, file writeback and session persistence. An automatic layout success does not satisfy Gate 6, and `smart_layout_skipped_continue` does not prove the official model check failed.
- Structured diagram evidence is the common basis. Images are supplemental by request and capability; an explicit image request that cannot be fulfilled remains a visible gap.
- Use required `payload` for API scripts. Legacy async/ready/dispatch/fast-workflow modes are retired; explicit dedicated actions provide stage evidence.
