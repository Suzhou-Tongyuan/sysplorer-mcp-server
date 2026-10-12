# Current Sysplorer 2026b MCP Recipes

These examples run only through the Sysplorer MCP script execution tool
(`call_code(mode="run_sysplorer_api")` when exposed). Local helper scripts only
process files; never run an independent ModelingPy client to connect to the GUI.
Resolve actual tool names/contracts in the current environment before use.

## Session and API Contracts

Offline model/log review needs no session. Before first live access confirm the
target via MCP, use `session_manager(action="probe")` when available, then
`health`. Reuse valid evidence for the same session; recheck after a switch,
disconnection or infrastructure symptoms. Never reset an attached user GUI.

Known current API contracts require no repeat query. Resolve unknown names,
parameters and return types with targeted `get_api_document`; empty/failed docs
require exact-name MCP `Help`, signature or docstring inspection. Toolbox APIs
use their own namespace. Sysblock tasks reuse the diagram skill's contract
resolver/runtime-contracts. Do not guess a write or enumerate all APIs. Missing
capabilities stop only the dependent operation; report the evidence gap.

## Project Experiment Settings

Only when the requested stage needs simulation settings and the current API
contracts confirm these return schemas, project fields shared by
`GetModelExperiment` and `ListSimulationOptions`, converting values to the
declared type:

```python
baseline = ModelingPy.GetModelExperiment(model)
supported = ModelingPy.ListSimulationOptions()
allowed = {
    "startTime", "stopTime", "interval", "algorithm", "tolerance",
    "fixedOrInitStepSize", "inlineIntegrator", "inlineStepSize", "storeEvent",
}
options = {key: baseline[key] for key in allowed if key in baseline and key in supported}
def parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    if isinstance(value, str) and value.strip().lower() in ("true", "false", "0", "1"):
        return value.strip().lower() in ("true", "1")
    raise ValueError(f"unsupported boolean: {value!r}")

for key, value in list(options.items()):
    kind = supported[key]
    options[key] = {"bool": parse_bool, "float": float, "int": int, "str": str}[kind](value)
```

Do not pass descriptive fields such as `isIntervalLength` or
`numberOfIntervals`. A missing field makes settings evidence `partial`; it does
not block static diagnosis, but limits claims that depend on that field. Do not
invent defaults or silently change interval semantics. A final runtime claim
requires evidence that the requested baseline settings were actually used.

## Stage Gates and Message Capture

- Check failure: use `check_model`; preserve its first diagnostic; do not translate.
- Translation failure: after check passes, use `translate_model`; do not simulate.
- Runtime failure: call `SimulateModelEx` only after static stages pass.
- Generated solver failure: build only after code generation; the first
  attributable compile/link diagnostic is the anchor.

After simulation, immediately capture the result before another command can
overwrite message state:

```python
# Add only hypothesis-required diagnostics temporarily; restore baseline options
# before final runtime acceptance. Capture messages before unrelated calls.
ok = ModelingPy.SimulateModelEx(model, options)
log = ModelingPy.MessageText()
exit_state = ModelingPy.GetSimulationExitState()
current_time = ModelingPy.GetCurrentSimTime()
```

`MessageText()` and `GetLastErrors()` may be overwritten by later commands.
Prefer the wrapper diagnostic for check/translation and `MessageText()` for the
immediate simulation/build call. Do not claim that sequential reads came from
the same target operation without ownership evidence. Required runtime success
needs the return value, terminal state and `currentTime >= stopTime - epsilon`
with a justified time tolerance. Static/link-only acceptance needs no stop time
or simulation. Read results/KPIs only when requested or fault-dependent.

## One Work Copy

Use one verified task-owned copy before edits, reusing a valid existing copy
from the original construction/debugging task. Diagnose-only work needs no patch
copy. Record source and working FQN/path separately:

- A disk-isolated package can preserve FQN only when loading it cannot replace
  unsaved source state. Preserve package layout and relative resources.
- A session copy has a distinct FQN. Confirm the current `CopyModel` contract,
  record the mapping and verify internal references, resources, experiment and
  target settings. Do not claim it preserves the source FQN or is automatically
  a complete resource copy. Use project naming rules (new classes default to
  ASCII letters/digits, at most 15 characters).
- If neither path protects original files and unsaved GUI state, stop dependent
  editing and report the limitation. Never substitute `extends Original`.

## Compensating Transactions

Modelica text:

1. Capture the complete old text and SHA-256.
2. Require the expected old fragment/hash to match.
3. Prefer minimal `EditModelText`; use `SetModelText` only for a necessary full replacement.
4. Read back the diff and new hash immediately.
5. Run the affected gate. On failure or no improvement, restore the old text and verify its hash.

Do not use text editing for Sysblock topology.

Disk files: use `scripts/debug_workspace.py start`, then `checkpoint` before a
repair round and `restore` on failure. `restore` preflights all paths/blobs before
any target write, captures current bytes, then verifies each same-volume atomic
replacement. On failure it compensates attempted files in reverse order and
returns `ok=false`, per-file compensation and a retained recovery directory.
Inspect that result; exit code 0 alone from another tool is not rollback evidence.
The retained `recovery.json` records pre-restore bytes for manual recovery; keep
it until the failure is resolved. This is not a crash-safe multi-file transaction.
Dry-run validates the complete plan without modifying targets.

Sysblock: snapshot components, connections, ports, scalar values, complete
parameter DataClasses, external-resource lists, and affected target settings.
Use only structured write APIs. Every write needs an executable inverse. Do not
write when the old value cannot be read and verified.

## Bounded Diagnostics

Use `debugNonlinearSolution` before the high-volume
`debugNonlinearIteration`. Enable event, dynamic-state, singular-system, and
user-C diagnostics one group at a time. Read RMF, Flat Model, Variables.xml,
dumps, or generated C only through an anchored bounded extractor.

## Prohibited Operations

- `ClearAll`, `ChangeDirectory`, or `Exit`.
- Editing the source model, unsaved GUI state, generated wrappers/C, or project files.
- Treating `SetModelExperiment` as temporary without verified restoration.
- Guessing run ownership from the newest solver directory.
- Sweeping algorithms, tolerances, or step sizes for an accidental pass.

