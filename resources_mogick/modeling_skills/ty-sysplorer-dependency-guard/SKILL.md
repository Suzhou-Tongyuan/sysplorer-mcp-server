---
name: ty-sysplorer-dependency-guard
description: >-
  Mandatory model-library dependency guard for modelica_lite / mols (mogick). Use whenever a
  task loads, opens, checks, translates, simulates, or builds models with Modelica, TY, TA,
  NPSLibrary, SysplorerEmbeddedCoder, or any model-library dependency; when load_library returns
  ok:false / LoadLibrary returned False (including silent False with no diagnostics); when tool
  output contains "模型库未安装", "library not installed", "not installed", or load_library
  plan entries with action="install_if_missing". Enforces plan-first analysis, downloadable
  catalog resolution, real prepare/download when the user-workspace gate is open, library refresh,
  LoadLibrary verification, and clear blocked-state reporting.
---

# Sysplorer Dependency Guard (modelica_lite / mogick)

Use this as a thin add-on to `ty-sysplorer-modeling-rules` and any active domain skill.
**Platform**: `SYSPLORER_PLATFORM_LABEL=modelica_lite` / `mols` (mogick app). This pack does
**not** preinstall full Modelica / TY commercial `.mol` files — treat missing libs as normal.

The domain skill chooses the modeling library and components; this skill ensures required
libraries are analyzed, downloadable, installed (when gate allows), refreshed, loaded, and
re-verified before work continues.

## Hard Rules (modelica_lite)

- **Load locally first.** Call `load_library(action="load")` before any plan/download.
  `session_manager` `paths.dependency_download_enabled=false` only gates remote install;
  it does **not** mean TA/Modelica/TY libraries are absent.
- **Do not assume libraries are present after a failed load.** `Modelica`, `TYMedia`,
  `TYThermoFluidSys`, and other TY/TA packs are often missing until `load_library` installs
  them (or the host preinstalls).
- **Silent `LoadLibrary returned False` counts as missing.** On modelica_lite there may be no
  「模型库未安装」 text. Any `load_library` / `LoadLibrary` `ok: false` must enter this guard.
- **Plan first, then prepare.** After a load failure:
  1. `load_library(action="plan", library_name=...)` (or `model_name=...`)
  2. If `install_if_missing` and gate open → `prepare` / `download` with `dry_run=false`,
     `download_missing=true`, prefer `load_after_download=true`
- Treat missing model libraries as actionable, not as a user handoff. Do not only report and stop.
- Do not treat `load_library(action="load")` as a downloader. Do not retry `action="load"` in a loop.
- Do not treat `load_library(action="plan")` or any call with `dry_run=true` as installation.
- Before any download/prepare decision, respect the downloadable catalog resolver. Only the
  resolver's `resolved_name` may be used for download, latest lookup, and package naming.
- If `library_name_resolution.status` is `ambiguous_library_name` or `unknown_library_name`,
  do not download. Return the candidates or the not-downloadable status.
- If `dependency_download_gate.enabled=false`, report that real download/install requires the MCP
  server to be started with `--user-workspace`. Keep the plan output; do not claim install succeeded.
- After prepare/download succeeds, return to the original operation (`load_library`, `load_file`,
  `check_model`, etc.) and re-verify once.

## Minimal Reading

Read only the reference needed for the current issue:

| Need | Read |
|---|---|
| Exact tool arguments | `references/tool-parameter-templates.md` |
| Downloadable catalog behavior | `references/downloadable-library-catalog-policy.md` |
| Failure signal handling | `references/failure-signals.md` |

## Guard Workflow

1. **Detect dependency work**: apply when the task mentions Modelica, TY, TA, `NPSLibrary`,
   `SysplorerEmbeddedCoder`, library loading, opening `.mo` files, checking, translating,
   simulating, **or** any `load_library` `ok: false` / silent False on modelica_lite.
2. **Resolve against the catalog**: inspect `library_name_resolution`. Continue automatically
   only for `exact`, `case_insensitive`, `normalized`, or high-confidence `fuzzy` matches.
3. **Choose the entry point**:
   - Load failure / named library: `load_library(action="plan", library_name=...)` then `prepare`.
   - Existing `.mo` file: prefer `model_manager(action="load_file")` with dependency preparation enabled.
   - Already loaded model name: `load_library(action="prepare", model_name=...)`.
4. **Install for real when missing**: use `dry_run=false` and `download_missing=true`. Prefer
   `load_after_download=true` and keep `refresh_after_download=true`.
5. **Handle the gate**: if `dependency_download_gate.enabled=false`, stop installation and report
   the startup requirement (still show plan). If Windows elevation is needed, follow the structured
   `needs_elevation` / helper result.
6. **Verify and resume**: check `refresh`, `load`, and the original model operation.

## Allowed Auto-Corrections

Allow automatic library-name correction only when the resolver returns `ok=true`.

Examples:

```text
TYMultiBody -> TYMultibody
TY MultiBody -> TYMultibody
TY-MultiBody -> TYMultibody
tymultibody -> TYMultibody
TYmultibbody -> TYMultibody, only when matched_by="fuzzy" and high-confidence
```

Do not auto-download on examples like:

```text
TYBody -> ambiguous candidates; require a choice
UnknownLib -> unknown; not in the downloadable catalog
```

## Delivery Evidence

When this skill affects a task, include concise evidence in the final task status:

- Platform note: modelica_lite / mols; whether libs were assumed missing due to silent False.
- Required libraries and whether each was already installed, planned, downloaded, skipped, or blocked.
- Any name correction, with `input_name`, `resolved_name`, and `matched_by` when available.
- Whether `UpdateLibrary` / post-prepare `LoadLibrary` ran.
- Whether the original operation was retried and its result.
- If blocked, name the blocking gate: catalog ambiguity, unknown library, missing `--user-workspace`,
  download failure, checksum failure, extract failure, install/UAC/helper failure, `UpdateLibrary`
  failure, or post-prepare `LoadLibrary` failure.
