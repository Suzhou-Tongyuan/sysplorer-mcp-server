# External C Debugging

## Route by Integration Type

| Integration | Inspect first |
|---|---|
| Modelica `external "C"` | declaration, input/output order and types, dimensions, `Include`, `IncludeDirectory`, `Library`, `LibraryDirectory`, resource URI |
| Sysblock CCaller | `HeaderFile`, `FunctionName`, `Arguments`, `IOType`, `DataType`, `Dimension`, `ArrayLayout`, sample time |

Follow the actually failed integration stage and requested terminal acceptance.
Diagnose-only tasks inspect evidence without patches. Known static/link faults
do not require an external runtime call; inspect generated wrappers only when
an existing diagnostic anchor needs them. All ModelingPy snippets execute via MCP.

## Fast Evidence Order

1. Current check/translation result or first compiler/linker diagnostic.
2. One immediate primary message channel for that same operation.
3. Current external declaration or complete CCaller configuration.
4. Target function and direct callees in user-provided `.c/.h` files.
5. Compiler source line or function-call stack, when available.
6. A bounded generated-wrapper excerpt only around an existing anchor.

User-provided C source is eligible for targeted fast-path inspection. Do not
read an entire external project without a function, symbol, source line, or
stack anchor.

Before the first edit, derive the complete reachable input domain from the
Modelica/CCaller declaration, initialization and default/probe calls, event
values, dimensions, and user acceptance constraints. A bounds fix must cover
that domain in one patch, not merely the observed failing sample.

## Generated-Solver Failures

Classify the first error before editing:

| Stage | Inspect |
|---|---|
| Preprocess | include path, macro, conditional compilation, encoding, generated include |
| Compile | prototype, const/pointer level, return value, array decay, type width, calling convention |
| Link | spelling, C/C++ name mangling, static/dynamic library, architecture, duplicate symbol, search path |
| Code generation | unsupported CCaller configuration, target limitations, array layout or dimension flattening |

When a compiler points into a generated wrapper, read only the anchored excerpt
and map its function and arguments back to the integration configuration and
user source. Never patch the wrapper; fix configuration or user source and
regenerate. Code-generation success is not compile/link success.

## CCaller Configuration

`GetModelParamValues` returns an `ExternalCFunctionConfig` DataClass, not
necessarily a dictionary:

```python
cfg = ModelingPy.GetModelParamValues(model, block)
```

Relevant fields are `HeaderFile`, `AvailableFunctions`, `FunctionName`,
`Arguments`, and `ArrayLayout`. Each argument carries `CName`, `MoName`,
`IOType`, `DataType`, `Dimension`, and `Value`. Read and write the complete
DataClass, then read back targeted fields. Do not change `AvailableFunctions` or
unrelated `CName` values.

For an empty configuration, assign a valid `HeaderFile` and complete
`FunctionName` in the same DataClass before one `SetModelParamValues` call.
Normalize Windows paths to forward slashes before they enter JSON/DataClass
values. `ArrayLayout` is only `""`, `columnMajor`, or `rowMajor`.

Header selection and compilation resources are separate. `HeaderFile` enables
function discovery; compiling user `.c` may also require the model's complete
`CFile` resource list. `SetExternalResources` replaces that list, so snapshot,
merge, write, and read it back as a whole value.

## Runtime Structured Exceptions

Enable only the needed pair first:

```python
{
    "optimizationRuntimeCheck": True,
    "debugIncludeFunctionCallInErrorMessages": True,
}
```

Add `debugLoggingUserDefinedMsg=true` only when user C already emits useful
diagnostics. Extract the first failure time/stage, exception category, calling
Modelica function or CCaller, call stack, target C function, bounded argument
summary, and source line or smallest defensible candidate region.

Typical mappings:

| Symptom | Inspect in source |
|---|---|
| Access violation | null/dangling pointer, bounds, dimension/stride, write to read-only storage |
| Stack corruption | prototype/calling-convention mismatch, buffer overwrite, bad variadic call |
| Divide by zero | denominator provenance, reachable input domain, initialization call |
| Invalid argument | type conversion, output buffer, length argument |
| Wrong result without crash | row/column order, units/scale, directions, state lifetime |

An exception code alone is not an exact root cause. Report the candidate region
and missing evidence unless a stack/compiler line anchors the claim.

## Automatic Edit Boundary

In a verified user-owned work copy, automatically repair only a directly
evidenced signature/type/order/direction/dimension/layout/include mismatch, or a
compiler/stack-anchored bounds, null, length, or deterministic resource-lifetime
defect. Preserve the public ABI and intended function semantics.

Respect existing authorization. Seek user judgment only when a new change to
formulas, control/state logic, numerical approximation, public ABI, third-party
code or invalid-input behavior exceeds the agreed design/scope. Never invent a constant, remove an unresolved dependency, or
mask an invalid input solely to make a test pass.

Recheck and rebuild the requested terminal target. Runtime/function recovery
uses baseline settings and verifies fault-dependent results/resource behavior;
link-only acceptance does not require unrequested simulation or result reads.

## Current Stop Points

Stop at bounded diagnosis for binary-only code without symbols, absent call
stacks, unrecoverable process corruption, dump/PDB symbolization needs, or a
hung external call that cannot be cancelled. These require upgraded MCP support
for isolated workers, SEH/timeout capture, dumps, symbolization, and wrapper/source maps.

