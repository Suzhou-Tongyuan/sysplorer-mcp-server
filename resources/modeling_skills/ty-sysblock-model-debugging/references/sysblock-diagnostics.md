# Sysblock Diagnostic Reference

All API snippets run through Sysplorer MCP after confirming unknown contracts.
Use this reference without edits in diagnose-only mode. Repair actions retain
the diagram skill's applicable structured-edit and save/reload/audit requirements.

## Minimal Introspection Set

Call only the interfaces required by the current first error:

| Object | Read interface |
|---|---|
| Model existence/restriction | `ClassExist`, `GetRestriction` |
| Components | `GetComponents`, `GetComponentTypeName`, `GetComponentInfo` |
| Ports | `GetComponentPorts`, `GetSubsystemPortInfo` |
| Connections | `GetConnectionInfo` |
| Scalar parameters | `GetModelParamList`, `GetModelParamValue` |
| Complex parameters | `GetModelParamValues` |
| External C resources | `GetExternalResources` |
| Code generation | `ListCodeGenerationOptions`, `GetModelCodeGenerationOptions` |
| Experiment settings | `GetModelExperiment`, `ListSimulationOptions` |

Do not recursively expand every subsystem. Inspect the failed block, direct
neighbors, and shortest feedback loop first.

## Common First Errors

### Missing component or parameter

Verify the full model FQN, `restriction`, real component name/type, and parameter
name from `GetModelParamList` or component documentation. Do not infer API field
names from GUI labels.

### Missing or incompatible port

Read actual ports after the change and compare direction, type, dimension, and
variable-port count. Auto-reconnect only when design intent is unique; otherwise
return candidates for confirmation.

### Algebraic loop

Extract the smallest directed loop and distinguish a valid continuous algebraic
system, a missing control state/delay, a discrete state/mode feedback loop, and
an accidental self-connection. Adding UnitDelay/Memory changes dynamics and
requires a design decision if not already authorized.

### Simulation timeout or integration failure

Check whether the process is still running, current simulation time, sample
times, integrator state, saturation, zero crossings, and high-frequency events.
A wall-clock timeout alone does not prove numerical non-convergence.

### Lookup table

Check breakpoint monotonicity, table dimensions, extrapolation, input domain,
and row/column meaning. Change data only with user or documented evidence.

### Unsupported code generation

Report the target, first unsupported block, and reason. For continuous blocks on
an embedded discrete target, propose a semantically equivalent discrete design
for confirmation and revalidate dynamic KPIs after any replacement.

## CCaller

The full value is an `ExternalCFunctionConfig` DataClass:

```python
cfg = ModelingPy.GetModelParamValues(model, component)
```

It includes `HeaderFile`, `AvailableFunctions`, `FunctionName`, `SampleTime`,
`ArrayLayout`, and `Arguments`. Each argument includes `CName`, `MoName`,
`IOType`, `DataType`, `Dimension`, `Value`, and `Description`.

- `HeaderFile` must name a valid C/header file. Writing the whole object with an
  empty function name can fail.
- From an empty configuration, set valid `HeaderFile` and complete
  `FunctionName` on the same read DataClass, then call `SetModelParamValues` once.
- Normalize Windows paths to forward slashes before JSON/DataClass transport.
- Treat `AvailableFunctions` and `CName` as reference fields unless direct evidence requires otherwise.
- After changing `FunctionName`, verify argument order, direction, type, and dimension.
- `ArrayLayout` is only empty, `columnMajor`, or `rowMajor`.
- Read back only relevant fields after the whole-object write.

Header selection does not guarantee compilation. Snapshot
`GetExternalResources(model, "CFile")`; if user source must be compiled, merge
the source into the complete list passed to `SetExternalResources`, then read it
back. That setter replaces the whole list.

`GenerateModelCode=true` can occur before the implementation is linked. Only the
required generated-solver build or baseline simulation closes the compile/link
verification loop.

## Result Verification

Only use this section when requested or needed for abnormal-result/functional
recovery acceptance. Static/link-only tasks mark results `not_required`.

Preselect a small set of signals: failed block input/output, one immediate
upstream/downstream signal, state/integrator output, and user KPI. Compare values,
dimensions, sample transitions, saturation, and finiteness around the failure.
Do not substitute a `true` simulation return for control-behavior verification.

