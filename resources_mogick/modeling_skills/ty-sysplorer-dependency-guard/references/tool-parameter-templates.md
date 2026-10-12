# Tool Parameter Templates

> Scope: **modelica_lite / mols (mogick)**. Prefer **plan first** after any load failure,
> then real `prepare` when the download gate is open.

Use these templates exactly unless the user explicitly asks for analysis-only behavior or a different install location.

## After `load_library` Failure (modelica_lite default)

Silent `LoadLibrary returned False` is enough — do not wait for 「模型库未安装」 text.

```text
load_library(
  action="plan",
  library_name="<library>"
)
```

If the plan contains `action="install_if_missing"` and the download gate is open, continue with real prepare (next section). If `dependency_download_gate.enabled=false`, report the gate and keep the plan output.

## Explicit Library Name (real install)

Use when the user names a library such as `TYMultibody`, `TYMedia`, `TYThermoFluidSys`, `NPSLibrary`, `TAEconomy`, or `SysplorerEmbeddedCoder`, and installation is allowed.

```text
load_library(
  action="prepare",
  library_name="<library>",
  dry_run=false,
  download_missing=true,
  load_after_download=true,
  refresh_after_download=true
)
```

## Loaded Model Name

Use when the model is already loaded or a full model name is known.

```text
load_library(
  action="prepare",
  model_name="<Full.Model.Name>",
  dry_run=false,
  download_missing=true,
  load_after_download=true,
  refresh_after_download=true
)
```

## Existing `.mo` File

Prefer this for model files on disk. It loads the file and prepares dependencies when the server was started with `--user-workspace`.

```text
model_manager(
  action="load_file",
  file_path="<path>",
  prepare_dependencies=true,
  dependency_dry_run=false,
  download_missing_deps=true,
  refresh_libraries_after_download=true,
  load_dependencies_after_download=true
)
```

## Analysis Only

Use when inspecting the plan without changing the local environment (always the first step after load failure on modelica_lite).

```text
load_library(
  action="plan",
  library_name="<library>"
)
```

If the plan contains `action="install_if_missing"`, analysis is not completion. Continue with real `prepare` unless the user asked for plan-only behavior.

## What Not To Do

Do not treat a plain load as a download attempt:

```text
load_library(action="load", library_name="<library>")
```

`action="load"` only loads libraries that are already installed. On modelica_lite, looping load after `ok: false` is incorrect — call `load_library(action="plan")` then `prepare` instead.
