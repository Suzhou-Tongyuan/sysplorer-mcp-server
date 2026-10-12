# Failure Signals

> Scope: **modelica_lite / mols** (mogick app). This runtime typically does **not** ship
> full Modelica / TY commercial `.mol` packs. Treat library load failures as dependency
> work, not as “skip and keep coding”.

Use this file when deciding whether dependency preparation must continue or whether the task is blocked.

## Signals That Require Plan → Prepare/Download

If any of these appear, do **not** stop at reporting the problem and do **not** loop on `load_library`:

```text
ok: false from load_library / LoadLibrary
LoadLibrary returned False
(silent False / empty diagnostics — common on modelica_lite)
模型库未安装
library not installed
not installed
action="install_if_missing"
reason contains "模型库未安装"
```

Required next actions (in order):

```text
# 1) Analyze first (always on modelica_lite after load failure)
load_library(action="plan", library_name="<library>")
# or, once a model exists:
load_library(action="plan", model_name="<Full.Model.Name>")

# 2) Real install when plan shows install_if_missing and gate is open
load_library(
  action="prepare",
  library_name="<library>",   # or model_name=...
  dry_run=false,
  download_missing=true,
  load_after_download=true
)
```

On **modelica_lite**, never assume `Modelica` / `TYMedia` / `TYThermoFluidSys` / other TY packs
are preinstalled. A quiet `LoadLibrary returned False` is enough to enter this path.

## Blocking Signals

| Signal | Required response |
|---|---|
| `dependency_download_gate.enabled=false` | Report that the MCP server must be started with `--user-workspace` to enable real download/install. Still keep the `plan` output so missing libs are listed. |
| `ambiguous_library_name` | Return candidates and require a concrete library choice. |
| `unknown_library_name` | Report that the library is not in the downloadable catalog. |
| `latest` query failed and no version is available | Cannot download that dependency; report the failing library and latest URL/error if available. |
| `download_failed` | Report network/URL/download error; do not claim installation. |
| `sha256_mismatch` | Report checksum mismatch; do not use the archive. |
| `extract_failed` | Report extraction failure; do not continue to install a partial package. |
| `needs_elevation` | Report that the install root is not writable and Windows UAC/helper is required. |
| `helper_not_found` | Report missing install helper deployment or path configuration. |
| user cancelled elevation | Report cancellation; do not retry elevation without user intent. |
| `UpdateLibrary` failed | Verify with `LoadLibrary`; if still failing, report refresh failure. |
| post-prepare `LoadLibrary` failed | Return the real load error and do not loop on download. |

## Resume Rule

After any successful prepare/download, retry the original operation once at the same workflow point. Examples:

```text
load_library -> load_library plan -> prepare -> load_library
model_manager load_file -> load_library prepare -> model_manager load_file or reload_after_dependency_prepare
check_model -> load_library prepare -> check_model
```
