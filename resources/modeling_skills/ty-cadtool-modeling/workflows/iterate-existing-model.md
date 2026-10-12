# Workflow — Iterate / re-enter an existing model

Use when a model was already generated and the user wants to change geometry, joints, or parameters and regenerate. **Multibody only** (fluid has no iteration design).

## Default reading

- Required: `references/mcp-workflow.md`, `references/multibody-elements.md`

## Two iteration scopes

- **Whole-model iteration**: re-enter the toolbox on the entire model.
  ```python
  model_name = cadtool.GetModels()[-1]            # e.g. "Default1.PickAndPlace.step"
  cadtool.OpenModelInCadBrowser(model_name)
  ```
- **Local iteration**: re-enter on a single top group / sub-body; some calls (create group/joint/driver/contact, slicing, planar loop) are disabled in local scope.
  ```python
  cadtool.OpenModelInCadBrowser(model_name, "base")   # component_name = a top group/sub-body
  cadtool.SetComponentIcon()                          # optionally set the current view as the icon
  ```

## Steps

1. Find the model: `model_name = cadtool.GetModels()[-1]` (or pick by name).
2. Re-enter: `OpenModelInCadBrowser(model_name[, component_name])`.
3. Edit: add/delete/modify design elements as in `build-multibody-from-cad.md`. Note `ImportCad` is **disabled** during iteration.
4. Accept-exit: `GenerateMoModel()` — in iteration the package/type args are ignored; it regenerates in place.
5. Re-validate via MCP: `check_model` → `translate_model` → `simulate_model` → `result_manager` / `plot_manager`.

## Lightening a delivered model

To ship a lighter `.mo` that no longer carries the toolbox link (geometry detached):

```python
cadtool.DeleteModelInCadBrowser(model_name)
```

After this the model can still simulate but can no longer be re-entered for iteration.

## Notes

- Local iteration restrictions: no new groups/joints/drivers/contacts, no slicing, no planar-loop tool inside a local scope — do those in whole-model scope.
- For pure parameter tweaks (no geometry/topology change), you usually don't need to re-enter the toolbox at all — set parameters on the generated model via MCP (`run_with_ready set_model_param` / run_script `SetParamValue`) and re-simulate.
