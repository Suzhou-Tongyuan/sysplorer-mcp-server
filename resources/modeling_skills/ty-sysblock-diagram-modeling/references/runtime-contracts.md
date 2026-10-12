# Sysplorer Runtime and API Contracts

This file is the sole authority in this skill for API discovery, return-value handling, object ownership, and model lifecycle. Layout and Chart algorithms belong in their own references.

## API resolution

Resolve only exact API names needed by the task:

1. Prefer an available high-level MCP operation.
2. Read `api-contracts.json` through `scripts/api_contract_resolver.py`.
3. If missing or version-mismatched, query exact API documentation once.
4. If `get_api_document` returns `ok=true` with empty `help_text`, do not treat the API as absent or resolved. In one targeted `call_code(mode="run_sysplorer_api")` lookup, explicitly import `mworks.sysplorer`, resolve only the already-requested name with `getattr`, capture `Help(name)` stdout, and read `inspect.signature` plus `inspect.getdoc`. Do not call `ListFunctions()` for this fallback.
5. If exact documentation still cannot establish behavior, test that one uncertainty once in a disposable task-owned model.
6. Add verified findings to a contract candidate; do not repeat the query in the same task.

Sysplorer 2026b implements `Help(name)` by calling Python `help()`: the documentation is printed to stdout and the direct return is `None`. An MCP wrapper that reads only the return value can therefore report an empty `help_text` even when the function and its documentation exist. Use this exact-name fallback:

```python
import contextlib
import inspect
import io
import mworks.sysplorer as ModelingPy

name = "ExactApiName"
fn = getattr(ModelingPy, name, None)
if not callable(fn):
    raise RuntimeError(f"API not found: {name}")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    ModelingPy.Help(name)
help_text = buf.getvalue()
signature = str(inspect.signature(fn))
doc = inspect.getdoc(fn) or ""
if not help_text and not doc:
    raise RuntimeError(f"API documentation empty: {name}")
```

This is a documentation lookup, not a behavior probe. Preserve the exact name, signature, captured help/doc, runtime version, and lookup count in the resolution evidence. A task may batch only its frozen exact-name set in one script; namespace enumeration remains forbidden by default.

Do not run full `ListFunctions()` exploration by default. Allow one namespace-limited enumeration only after the expected exact name is confirmed absent and no documented fallback exists.

Limits per API/version/uncertainty:

- known contract: zero probes;
- unknown signature: one exact documentation lookup;
- unknown behavior: one disposable probe;
- target-model probes: forbidden;
- blind retries: forbidden.

`api_contract_resolver.py` is read-only. It classifies `known`, `needs_exact_doc`, `needs_behavior_probe`, and `unsupported`; it never creates or edits a model.

## Return-value check

For every API returning a Boolean status, handle, identifier, object, or query result:

- require `true` for Boolean success;
- require a nonempty value of the documented type for creation/query results;
- on false, empty/invalid result, or exception, stop dependent calls;
- preserve the direct return and exception, then call `GetLastErrors()` when available;
- fix the first failure before continuing.

This rule does not require unrelated property readback after every successful setter.

## Sysblock boundary Outport

For `SysplorerEmbeddedCoder.Port.Outport` in Sysplorer 2026b, `GetComponentPorts(model, outport, 0)` may validly return `[]`. Connect an incoming signal with the Outport component name itself, for example `ConnectPort(model, "chart.mode", "mode_out")`, not a synthetic `mode_out.u` endpoint. Keep logical `u` in layout data when useful, but normalize it to the direct component name only at the API/readback boundary. Do not generalize an empty port query to ordinary components.

For connection geometry readback, call `GetConnectionInfo(model, (source, target), "Points")`; Sysplorer 2026b requires a tuple and returns a brace-form string such as `{{x1,y1},{x2,y2}}`. Parse its numeric pairs into a finite point list before checking bends, orthogonality, or overlap; do not test the raw string as a list.

## Three-scope lifecycle preflight

Before create/open/save/load operations, distinguish:

1. the absolute project target file;
2. any loaded same-name class;
3. any same-name file under Sysplorer `GetDirectory()`.

Record ownership for each. Automatically unload, replace, rename, erase, or delete only assets created by the current task. Never infer that a loaded same-name class owns the requested file.

## Save modes

- New target: use `SaveModelAs(model, existing_absolute_directory, new_simple_model_name)` once only when that directory does not already contain `<new_simple_model_name>.mo`; verify the resulting absolute file.
- Existing confirmed target: use `SaveModel` in place.
- Never use `SaveModelAs` as an overwrite operation or universal explicit save.
- After save, verify the absolute file exists and hash it.

## Final reload/readback

For final evidence, load the exact absolute target with `model_manager(action="load_file", force_reload=true)` and then run `check_model(model_name)` without asking `check_model` to reload another path. A successful top-level load is not invalidated solely by failed `auto_loaded_libs` fragments such as unqualified `Port`, enum, or internal StateMachine symbols; require the intended top-level library/model and use the structural check to decide whether a named dependency is truly missing.

Accepted final readback sources are `force_reloaded_api` and `saved_static_annotation`. A plan, screenshot, handwritten summary, or project-authored `passed` field is not readback evidence.

For a force-reloaded Sysblock level, use `GetComponents` plus `GetComponentInfo(model, component, "Type")` for actual inventory/type and `GetConnectionInfo` for actual connection geometry. `GetComponentInfo` does not document `Position`; obtain component frames from the same saved, hash-bound `.mo` `Placement` annotations and record that field source as `saved_static_annotation`. Do not call an invented `model_manager.get_component_info` action.

## Version-sensitive values

Parameter enums, StateMachine data-type tokens, Chart info-type tokens, and serialized geometry are runtime contracts. Use the 2026b values already documented in this skill. If the installed version differs, route the exact affected API/token through the resolution chain; do not rediscover unrelated APIs.

## Audit-only mode

For audit-only tasks, forbid writeback. Hash the target before and after all reads. Any hash change is an audit failure and must be reported.
