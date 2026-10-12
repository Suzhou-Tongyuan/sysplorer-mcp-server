# MCP Workflow — driving CADToolbox through Sysplorer MCP

The CADToolbox is a **separate Sysplorer toolbox package**, not part of the main ModelingPy command set. The MCP reaches it through `call_code(mode="run_sysplorer_api")`, which runs Python in-process where you `import mworks.sysplorer.CADToolbox`. Everything else (check / translate / simulate / read results) uses the dedicated MCP tools.

## 1. The run_script bridge

Drive every `cadtool.*` action with:

```
call_code(mode="run_sysplorer_api", payload={
  "python_source": "<your script>",
  "capture_stdout": true,
  "capture_stderr": true
})
```

Inside `python_source`:

- **Always import explicitly** — the script namespace has no implicit `cadtool` / `ModelingPy`:
  ```python
  import mworks.sysplorer.CADToolbox as cadtool      # CAD toolbox API
  import mworks.sysplorer as ModelingPy              # only if you need core API (e.g. SetComponentInfo)
  ```
- To return a value to the MCP JSON, assign it to `RUN_SCRIPT_RESULT`:
  ```python
  RUN_SCRIPT_RESULT = cadtool.GetParts()
  ```
  Read it back from the response field `run_script_result`.
- You can batch a whole build (import → group → joints → check → save → generate) in **one** `python_source` for speed, or split into steps when you need to inspect intermediate query results before deciding the next call. Splitting is preferred while the part/joint names are still unknown.

## 2. Discovering the API (do NOT use get_api_document for CADToolbox)

`get_api_document` only documents the main ModelingPy session and returns empty/garbage for toolbox functions. For CADToolbox, use run_script + introspection:

```python
import io, sys
import mworks.sysplorer.CADToolbox as cadtool
RUN_SCRIPT_RESULT = cadtool.ListFunctions()          # list every function + one-line description
```

```python
import io, sys
import mworks.sysplorer.CADToolbox as cadtool
buf = io.StringIO(); sys.stdout = buf
help(cadtool.CreateConnector)                         # full docstring for one function
sys.stdout = sys.__stdout__
RUN_SCRIPT_RESULT = buf.getvalue()
```

`references/api-reference.md` already mirrors `ListFunctions()`; use live `help()` only to confirm a signature against the installed version.

## 3. Tool mapping (test scripts use `sysplorer_api.*`; via MCP prefer the dedicated tools)

The bundled `test_use_case` scripts call `sysplorer_api.*` directly. When driving through MCP, map them as follows:

| Intent | In a test script | Through MCP |
|---|---|---|
| Make sure Sysplorer is up | `start_sysplorer.ConnectSysplorer()` | `session_manager(action="ensure")` |
| Session health / workspace root | — | `session_manager(action="health")` |
| Load a library | — | `load_library` |
| CAD import / build / save / generate | `cad.ImportCad(...)` etc. | `call_code(mode="run_sysplorer_api")` with `import mworks.sysplorer.CADToolbox` |
| New / open / save / query a model | `sysplorer_api.*` | `model_manager(action="new"/"open"/"save"/"get_components"/"get_model_text")` |
| Swap a component's type (e.g. cut joint) | `sysplorer_api.SetComponentInfo(...)` | `call_code(run_sysplorer_api)` → `ModelingPy.SetComponentInfo(...)`, or `run_with_ready(action="set_model_param")` |
| Set a parameter value | `sysplorer_api.SetParamValue(...)` | `run_with_ready(action="set_model_param")` or run_script `ModelingPy.SetParamValue(...)` |
| Check | `sysplorer_api.CheckModel(...)` | `check_model` |
| Translate | — | `translate_model` |
| Simulate | `sysplorer_api.SimulateModel(name, stopTime=...)` | `simulate_model` |
| Read results | — | `result_manager` |
| Plot / animation | `sysplorer_api.CreateAnimation()` / `RunAnimation()` | `plot_manager` (+ run_script for animation calls if needed) |
| Auto-layout writeback | — | `smart_layout` (rarely needed; `GenerateMoModel` already lays out) |

`cadtool.CheckDesign()` (design-element sanity inside the toolbox) is **different** from MCP `check_model` (Modelica model check). Run `CheckDesign()` before `GenerateMoModel`, and `check_model` after.

## 4. Generated model naming

`SaveCadFiles()` with an empty package name uses a **Sysplorer-assigned** package name. The official docs (生成 Modelica 模型 / 保存模型) confirm the default is **`Default` + a numeric suffix** (e.g. `Default1`); the bundled test cases happened to show `Default`. Either way, **don't assume the exact prefix — read it back** (saving is optional anyway — `GenerateMoModel` can run without a prior save). `GenerateMoModel(package, type)` produces the package and a **simulatable** top model named:

```
<package>.<cad_model_name>.<cad_model_name>_main
```

e.g. `Default.crank_rocker_mechanism.crank_rocker_mechanism_main` (verified across the bundled test cases). The `<cad_model_name>` derives from the imported file.

Caveat on `GetModels()`: it returns the **CAD-browser model identifiers** that `OpenModelInCadBrowser` consumes (e.g. `Default.<cad_model>...`), which are **not** the `_main` simulation target. To get the exact simulatable name, inspect the generated package with `model_manager(action="get_components"/"get_model_text")` (or rely on the verified `_main` convention) before passing it to `simulate_model` / `SetComponentInfo`.

The on-disk results land under `<work_dir>/<package>/<cad_model>/Mbs/<cad_model>.csv` for multibody.

## 5. Paths and hard bans (inherit from the parent rules)

- **Paths**: use the Agent CWD or `GetDirectory()` for the working directory. Never read/write user models under the MCP server program tree. `ImportCad` needs an absolute, ASCII-only path.
- **Never** call `ClearAll` (wipes loaded libraries / translation cache / results) or `ChangeDirectory` (conflicts with MCP workspace rules) from run_script. For teardown use `model_manager(action="unload")`.
- If the MCP server attached to an existing GUI (`SYSPLORER_API_PORT`), **never** call `Exit()` from run_script and do not use `session_manager(shutdown|force_restart|restart(full_reset))` — it would close the user's window.

## 6. Recommended cadence

```
session_manager ensure
-> run_script: import CADToolbox; ImportCad; SwitchWorkbenchType; (query tree)
-> run_script: build elements (groups/joints/drivers/markers/contacts | slices/ports/media)
-> run_script: CheckDesign  -> fix loop
-> run_script: SaveCadFiles; GenerateMoModel; RUN_SCRIPT_RESULT = GetModels()
-> check_model -> translate_model -> simulate_model -> result_manager / plot_manager
```

Enter the repair loop whenever `CheckDesign`, `check_model`, `translate_model`, `simulate_model`, or result verification fails. See `common-errors.md`.
