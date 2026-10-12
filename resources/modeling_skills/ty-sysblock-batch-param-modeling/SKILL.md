---
name: ty-sysblock-batch-param-modeling
description: >-
  Use this skill for Sysplorer Python API tasks that read or write complete
  Sysblock component parameter objects through GetModelParamValues and
  SetModelParamValues, and for tasks that generate or update per-module
  parameter-reference notes from dialog screenshots and JSON parameter samples.
  Use it when the task needs whole-object parameter retrieval, batch-style
  configuration updates, dict or dataclass handling, complex block parameter
  mapping such as CCaller, or reusable module-parameter note generation rules.
  Do not use this skill for general topology editing, DesignOpt toolboxes, or
  direct access to internal normalization helpers.
metadata:
  short-description: Sysblock batch parameter object and module-note guidance
  version: 1.5.0
  managed-by: sysplorer-mcp
---

# Sysblock Batch Parameter Objects

## Scope

- **In scope**: `GetModelParamValues`, `SetModelParamValues`, full component parameter-object retrieval, partial field reads, dict / dataclass payload handling, standard single-parameter coordination around `GetModelParamValue` / `SetModelParamValue`, and generation of per-module parameter-reference notes from screenshots plus JSON samples.
- **Out of scope**: Sysblock topology construction, DesignOpt toolboxes, Modelica physical modeling, and direct external use of `Utils/param_normalize.py`.
- **Routing priority**: When a task is about reading or updating many fields of one component at once, or about documenting a module's parameter-object mapping, prefer this skill over repeated single-field `SetModelParamValue(...)` calls or ad hoc note writing.

## Hard Rules

1. Call `session_manager(action="health" | "ensure")` before any `call_code(mode="run_sysplorer_api")` script that touches Sysplorer.
2. Never call `ClearAll` or `ChangeDirectory` from generated scripts.
3. Use the public Python APIs `GetModelParamValues` and `SetModelParamValues` as the documented batch parameter entry points.
4. Treat `Utils/param_normalize.py` as an internal implementation detail, not a user-facing API.
5. If only one or two scalar fields need to change, `SetModelParamValue` is still valid. If a whole configuration object is needed, use `GetModelParamValues` first and then write back with `SetModelParamValues`.
6. When generating module parameter notes, distinguish three field classes explicitly:
   - main writable fields
   - reference fields
   - internally handled fields that should not appear in the note
7. Do not generate a new module note from guesses alone. If the user has not provided the module's parameter-dialog screenshot and JSON sample, ask for them first, or ask for other reliable reference materials.
8. In the final module note, output conclusions only. Do not mention source-material traces such as "according to screenshot", "according to JSON", or similar wording.

## Tool Map

| Need | Tool / action |
|---|---|
| Sysplorer readiness | `session_manager` |
| Run Python API script | `call_code` (`mode="run_sysplorer_api"`) |
| Open / load model | `model_manager` |
| Validate changed model | `check_model`, `simulate_model`, `translate_model` |
| Batch parameter interface reference | `references/批量参数配置接口说明.md` |
| Batch object mapping overview | `references/模块参数对象映射说明.md` |
| Single-parameter coordination | `references/与单参数接口协同流程.md` |
| Module-note generation workflow | `references/模块参数专项说明编写流程.md` |
| Per-module notes | `references/模块参数专项说明/` |

## Canonical Workflow

1. Ensure Sysplorer is ready and the target model is loaded.
2. In `run_sysplorer_api`, import the public package entry:

```python
import mworks.sysplorer as ModelingPy
```

3. Read the current component configuration:

```python
cfg = ModelingPy.GetModelParamValues("model1", "Gain1")
```

4. For standard blocks, update the returned `dict` and submit it back:

```python
cfg["Gain"] = "10"
ok = ModelingPy.SetModelParamValues("model1", "Gain1", cfg)
```

5. For complex blocks such as `CCaller`, update the returned dataclass object and submit it back:

```python
cfg = ModelingPy.GetModelParamValues("model1", "CCaller1")
cfg.FunctionName = "calc_sum_diff"
cfg.SampleTime = "0.01"
ok = ModelingPy.SetModelParamValues("model1", "CCaller1", cfg)
```

6. When only specific fields are needed, use `fields` to read a filtered `dict`:

```python
partial_cfg = ModelingPy.GetModelParamValues(
    "model1",
    "CCaller1",
    fields=["FunctionName", "SampleTime"],
)
```

## Return-Shape Rules

- `GetModelParamValues(modelName, component)` returns a full configuration object.
- Only block types whose dataclass structures are defined in `block_params.py` and registered in `BLOCK_PARAM_CLASS_MAP` can be auto-converted to dataclass objects.
- All other block types return `dict`.
- If `fields` is provided, the return value is always the filtered `dict` built from those fields.
- `SetModelParamValues(modelName, component, params)` accepts `dict`, dataclass objects, or JSON strings.

## Stable Module Rules

- `CCaller` is the currently confirmed dataclass-return module.
- `BusCreator`, `BusSelector`, `SubSystem`, `LookupTable` family,  `CFunction` , `Goto`, `From`, `GotoTagVisibility`and ordinary wrapped blocks should be handled as `dict` unless a new dataclass mapping is explicitly added.
- Do not treat helper fields as writable by default.

Confirmed examples:

- `BusSelector.AvailableSignals`
  - reference field; candidate signal list; not a modification field
- `CCaller.AvailableFunctions`
  - reference field; list of selectable C functions in the current C file
- `CCaller.Arguments[].CName`
  - reference field; original C-side parameter name
- `BusCreator.OutDataTypeStr`
  - supports simplified input:
    - `auto` -> `"inherit: auto"`
    - `Bus1` -> bus type name shorthand
    - full strings such as `"inherit: auto"` and `"Bus: Bus1"` are also valid

- `CFunction.SymbolSpec`
  - array field; each element represents a variable (input/output/parameter)
  - submit as a complete array; the adapter rebuilds ports and parameters from the submitted array
  - `name` is required; `parameter` / `persistent` / `constant`  scopes must supply a non-empty `value`
  - each element contains: `name`, `scope`, `dataType`, `dimension`, `value`
- `Goto`
  - `GotoTag` and `TagVisibility` are writable; `TagVisibility` legal values: `Global`  /  `Local`  /  `Scoped`
  - submitting `GotoTag`  +  `TagVisibility`  together follows a fixed internal order (tag name first, then visibility)


- `From`
  - `GotoTag` is writable; `AvailableTags` is a read-only reference field, write attempts are rejected 
- `GotoTagVisibility`
  - `GotoTag` is writable; the component-scope prefix and `Scoped` visibility are internally handled and not exposed

Do not surface internally handled fields in generated module notes when they are intentionally hidden from callers.

Confirmed example:

- `BusCreator.BusTypeIsAuto`
- `BusCreator.BusTypeName`

These are internally handled and should not be exposed in the module note unless a future requirement explicitly changes that rule.

## Module Parameter Note Workflow

When the task is to add or update a module-specific parameter note:

1. Read `references/模块参数专项说明编写流程.md` first.
2. Check whether the module's dialog screenshot and JSON sample are available.
3. If they are missing, ask the user to provide them, or provide other reliable references such as help docs, parameter text descriptions, test materials, or API return samples.
4. Read the module's dialog screenshot and JSON sample.
5. Determine whether the module returns `dict` or dataclass on full read.
6. Split fields into:
   - main writable fields
   - reference fields
   - internal fields that should stay undocumented
7. If a field supports shorthand input, document the shorthand rule only when current evidence confirms it.
8. Write one dedicated note under `references/模块参数专项说明/`.
9. Update `references/模块参数对象映射说明.md` to include the new note.
10. If the module reveals a reusable rule, fold that rule back into this `SKILL.md`.

When writing the final note:

- Keep source materials as internal evidence only.
- Output the confirmed rules directly.
- Do not expose phrases like "based on the screenshot" or "according to the JSON sample" in the module note itself.

## Per-Module Note Output Structure

Use this structure for new module notes unless a section is clearly not needed:

1. Module name and purpose
2. Applicable scenarios
3. Confirmed dialog-to-key mapping
4. Reference-field notes
5. Simplified input rules
6. Recommended AI call pattern
7. Modification advice
8. Minimal verification example
9. Testing notes

Do not force every section into every note. Omit sections that are unsupported by current evidence.

## 2026a Notes

- `GetModelParamValues` serializes `fields` to JSON before passing them to the backend.
- Empty or omitted `fields` means full-object retrieval.
- Full-object retrieval attempts block-type detection through `GetComponentTypeName(...)`, then converts known block types to dataclasses.
- Dataclass return structures are defined only in `block_params.py`, which is deployed alongside `sysplorer_api.py`.
- The current mapping in `block_params.py` registers `CCaller` to `ExternalCFunctionConfig`.
- If a block type is not defined and registered there, treat the return value as `dict`.
- `SetModelParamValues` always normalizes the input to a JSON string before sending it to the backend.
- Internal helpers such as normalization and dict/dataclass conversion support this flow but are intentionally not documented as external APIs.

## Debugging Checklist

- Confirm the model is loaded and `modelName` / `component` names are exact.
- If `fields` is used, expect a `dict`, not a dataclass.
- If a complex block does not convert to a dataclass, check whether its type is registered in `BLOCK_PARAM_CLASS_MAP`.
- Keep writable values aligned with backend parameter names and casing.
- For JSON string input, make sure the JSON object keys match backend field names exactly.
- Before writing a module note, verify whether a suspicious field is actually writable, merely a helper field, or already internally handled.
