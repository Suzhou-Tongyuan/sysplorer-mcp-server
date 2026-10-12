# SYSPLORER_API_MOLS Startup Design

## Background

The current MCP server has an existing attach mode controlled by `SYSPLORER_API_PORT`.
When this environment variable is a positive integer, the server attaches to an
already running Sysplorer instance with `ConnectSysplorer(port=...)`.

This behavior must stay unchanged.

The new requirement is to add `SYSPLORER_API_MOLS`, defaulting to `False`, to
select the `StartSysplorer` launch mode:

- `False`: start Sysplorer with `-gui`
- `True`: start Sysplorer with `-q`

All existing launch parameters, especially `processPath`, must remain unchanged.

## Required Behavior

Startup priority:

1. If `SYSPLORER_API_PORT` is a positive integer, use the existing attach path:

   ```text
   ConnectSysplorer(port=SYSPLORER_API_PORT)
   ```

   In this case, `SYSPLORER_API_MOLS` is ignored.

2. If `SYSPLORER_API_PORT` is absent, empty, zero, negative, or invalid, use
   `StartSysplorer`.

3. When starting Sysplorer, `SYSPLORER_API_MOLS` selects only the mode argument:

   ```text
   SYSPLORER_API_MOLS=False -> StartSysplorer("-gui", processPath=<existing processPath>)
   SYSPLORER_API_MOLS=True  -> StartSysplorer("-q",   processPath=<existing processPath>)
   ```

4. `processPath` must continue to use the current resolved value from
   `_resolve_sysplorer_process_path(self.bin64_path)`.

## Environment Variable Parsing

`SYSPLORER_API_MOLS` defaults to `False`.

Recommended truthy values:

```text
1, true, yes, on
```

Recommended false values:

```text
unset, empty, 0, false, no, off, any other value
```

This keeps accidental or malformed values conservative and preserves current
startup behavior.

## Implementation Shape

The decision should stay in `core/stack_health.py`, because that file already
owns the choice between `ConnectSysplorer` and `StartSysplorer`.

Suggested helper:

```python
def _sysplorer_api_mols_from_env() -> bool:
    raw = os.environ.get("SYSPLORER_API_MOLS", "").strip().lower()
    return raw in ("1", "true", "yes", "on")
```

In `_start_fresh()`, keep the existing `SYSPLORER_API_PORT` branch first:

```python
attach_port = None if force_launch else _sysplorer_api_port_from_env()
if attach_port is not None:
    # Existing ConnectSysplorer behavior. Do not change this branch.
    ...
```

Only after the attach branch is skipped should the new variable affect startup:

```python
start_mode = "-q" if _sysplorer_api_mols_from_env() else "-gui"
MWorksDriver(force_start=True, start_mode=start_mode)
```

`mworks_driver.py` should accept and forward `start_mode` without reading the
environment variable directly:

```python
MWorksDriver(..., force_start=True, start_mode="-gui")
```

The actual `StartSysplorer` wrapper should preserve `processPath`:

```python
start_fn(start_mode, processPath=process_path)
```

Do not replace this with `start_fn(start_mode)` because that would drop the
existing `processPath` behavior.

## Non-Goals

- Do not add a CLI flag for this requirement.
- Do not change `SYSPLORER_API_PORT` parsing or attach behavior.
- Do not change how `processPath` is resolved.
- Do not start `mworks.exe` directly via subprocess or shell commands.
- Do not change shutdown, restart, or run-script safety policy except where the
  existing start path naturally calls `StartSysplorer` again.

## Test Cases

Minimum cases to cover:

1. `SYSPLORER_API_PORT=9001`, `SYSPLORER_API_MOLS=True`

   Expected: `ConnectSysplorer(port=9001)`, no `StartSysplorer`.

2. `SYSPLORER_API_PORT=9001`, `SYSPLORER_API_MOLS=False`

   Expected: existing `ConnectSysplorer(port=9001)` behavior.

3. `SYSPLORER_API_PORT` unset, `SYSPLORER_API_MOLS` unset

   Expected: `StartSysplorer("-gui", processPath=<existing processPath>)`.

4. `SYSPLORER_API_PORT` unset, `SYSPLORER_API_MOLS=False`

   Expected: `StartSysplorer("-gui", processPath=<existing processPath>)`.

5. `SYSPLORER_API_PORT` unset, `SYSPLORER_API_MOLS=True`

   Expected: `StartSysplorer("-q", processPath=<existing processPath>)`.

6. `SYSPLORER_API_PORT=invalid`, `SYSPLORER_API_MOLS=True`

   Expected: current invalid-port fallback behavior, then
   `StartSysplorer("-q", processPath=<existing processPath>)`.

