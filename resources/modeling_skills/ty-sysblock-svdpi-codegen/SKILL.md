---
name: ty-sysblock-svdpi-codegen
description: 用于在已有 Sysplorer Sysblock codegen 目录之上生成、刷新、检查或验证 SV-DPI wrapper，尤其适用于用户提到 dpi.h、dpi.c、dpi_pkg.sv、dpi.sv、tb.sv、simulate.do、wave.do、motrace.json、testpoint getter、ModelSim 或 Questa 的场景。只在可用 codegen 目录已经存在时接管；本技能不负责 Sysplorer 建模或 codegen 本体。
metadata:
  short-description: Generate and verify SV-DPI wrapper for Sysblock code generation results
  version: 1.0.0
  managed-by: sysplorer-mcp
---

# Sysblock SV-DPI Codegen

> Orchestration layer for generating and verifying SV-DPI wrapper files on top of existing Sysplorer Sysblock codegen directories. This skill wraps around the bundled script `scripts/render_svdpi.py`; prefer the script over hand-editing generated wrapper files unless the user explicitly asks for a manual patch.

**Core closed loop**: `Boundary check -> Codegen directory inspection -> Run generator -> Metadata review -> Testpoint handling -> Optional simulation -> Delivery`

> [!CAUTION]
> ## Global Execution Discipline (Mandatory)
>
> 1. **Boundary first**: Must confirm a usable codegen directory exists before any wrapper generation; if codegen does not exist yet, stop and route back to Sysplorer codegen.
> 2. **Codegen directory as fact source**: Must NOT infer ports, step functions, or testpoints from memory; always read the codegen directory directly.
> 3. **Script first**: Default to running `scripts/render_svdpi.py` over manual wrapper editing; only switch to manual patching when user explicitly requests.
> 4. **Metadata review required**: Do not claim success from file generation alone if `_svdpi_metadata.json` shows unresolved testpoints or structural warnings that matter to the user's goal.
> 5. **Heuristics must be disclosed**: Natural-language testpoint matching is heuristic; must explain this before presenting results.
> 6. **Delivery must be verifiable**: Final output must describe actual completed actions, generated files, metadata review, and any warnings or unresolved items.

> [!IMPORTANT]
> ## Trigger and Language Rules
>
> - Response language should match user input language unless user explicitly specifies otherwise.
> - This skill applies only after a usable Sysplorer codegen directory exists.
> - When user asks to "generate model code" or "export code from the model", first complete Sysplorer codegen, then use this skill.
> - Do NOT use this skill for generic SystemVerilog DPI theory without Sysplorer wrapper generation work.

## Scope of Application

- Generate or refresh SV-DPI wrapper files (dpi.h, dpi.c, dpi_pkg.sv, dpi.sv, tb.sv) from existing codegen directory
- List or select scalar testpoint candidates from `motrace.json`
- Generate `GetTestpoint_*` accessors on request
- Produce `simulate.do` and `wave.do` for simulation helpers
- Optionally run ModelSim or Questa smoke test on generated wrapper

**Out of scope:**
- Sysplorer modeling or codegen itself
- Editing the generated model C implementation as a substitute for wrapper generation
- Debugging arbitrary simulator environment issues beyond basic smoke-test triage

## Key Constraints

- Minimum usable input: one Sysplorer-generated codegen directory containing `<model>.h`, `<model>_private.h`, `<model>.c`
- For testpoint enumeration or getter generation, codegen directory should also contain `motrace.json`
- Must treat codegen directory as the source of truth
- Must NOT infer ports, step functions, or testpoints without reading the codegen directory
- Must report metadata review results including model stem, inputs/outputs, testpoints, and warnings
- Natural-language testpoint matching (`--testpoint-nl`) is heuristic; must explain before use

## Tools and Boundaries

### Primary Script
| Script | Purpose |
|--------|---------|
| `scripts/render_svdpi.py` | Generate SV-DPI wrapper files from codegen directory |

### Common Commands
| Command | Purpose |
|---------|---------|
| `python render_svdpi.py --codegen-dir <dir> --api-prefix model --force` | Generate wrapper in place |
| `python render_svdpi.py --codegen-dir <dir> --list-testpoints` | List testpoint candidates |
| `python render_svdpi.py --codegen-dir <dir> --testpoint-nl "<desc>" --force` | Generate testpoints from natural language |
| `vsim -c -do "do ./simulate.do"` | Run smoke validation |
| `vsim -view waves.wlf` | Open waveform output |

### External Tools
| Tool | Purpose |
|------|---------|
| ModelSim / Questa | Smoke test and waveform inspection |
| Python | Script execution for wrapper generation |

## Auxiliary Scripts

| Script | Purpose |
|--------|---------|
| `scripts/render_svdpi.py` | Core generator for SV-DPI wrapper files from codegen directory |

## Reference Navigation

This skill is script-driven; no separate `references/` files are maintained. All execution guidance is embedded in this `SKILL.md` and the script's own help.

## Task Entry Points

This skill has no independent workflow files; all tasks follow the core workflow below, driven by `scripts/render_svdpi.py`.

## Templates and Assets

- Bundled example model: `model/McpComplexMixer.mo` (for reproduction demos only; not a codegen directory)

## Workflow

### Phase 1: Confirm The Boundary

**GATE**: User has requested SV-DPI wrapper generation, testpoint handling, or simulation validation.

1. Confirm that the task is wrapper generation on top of an existing codegen directory.
2. If codegen does not exist yet, stop and route back to Sysplorer codegen first.
3. If codegen exists, treat that directory as the source of truth.

**Checkpoint**: Codegen directory existence is confirmed; task boundary is clear.

### Phase 2: Inspect The Codegen Directory

**GATE**: Codegen directory is confirmed.

Before generation, confirm the presence of required files:
- `<model>.h`
- `<model>_private.h`
- `<model>.c`

When testpoints are requested, also check:
- `motrace.json`

Do NOT infer ports, step functions, or testpoints from memory when the codegen directory can be read directly.

**Checkpoint**: Required files are present; codegen directory is readable.

### Phase 3: Run The Bundled Generator

**GATE**: Codegen directory inspection is complete.

Default to running the bundled script in place:
```powershell
python <path-to-skill>\scripts\render_svdpi.py `
  --codegen-dir <generated-code-dir> `
  --api-prefix model `
  --force
```

Only switch to `--output-dir` when the user explicitly asks for a separate wrapper directory.

**Checkpoint**: Wrapper generation script has been executed.

### Phase 4: Review Metadata

**GATE**: Generation has completed.

After generation, inspect `_svdpi_metadata.json` and report at least:
- Inferred model stem
- Discovered inputs and outputs
- Whether CSV compare mode is supported
- Selected testpoints
- Warnings

Do NOT claim success from file generation alone if `_svdpi_metadata.json` shows unresolved testpoints or structural warnings that matter to the user's goal.

**Checkpoint**: Metadata review is complete; any warnings or unresolved items are documented.

### Phase 5: Handle Testpoints

**GATE**: Metadata has been reviewed.

When the user asks for testpoints:
- First prefer exact `--testpoint` ids.
- If the user gives natural language, run `--testpoint-nl` only after explaining it is heuristic.
- If natural-language matching resolves candidates, report the matched `motrace` ids before presenting the final result.

List candidates with:
```powershell
python <path-to-skill>\scripts\render_svdpi.py `
  --codegen-dir <generated-code-dir> `
  --list-testpoints
```

**Checkpoint**: Testpoint handling is complete; all heuristics and warnings are disclosed.

### Phase 6: Execute Simulation and Deliver

**GATE**: Wrapper, testpoints, and optional simulation are complete.

1. **Optional simulation**: When the user asks for validation, run `vsim -c -do "do ./simulate.do"`; treat as smoke test unless stronger criteria are requested.
2. **Review generated files**: Confirm presence of standard artifacts (dpi.h, dpi.c, dpi_pkg.sv, dpi.sv, tb.sv, _svdpi_metadata.json; plus simulate.do and wave.do if enabled).
3. **Deliver**: Organize delivery following standard output format (Boundary Check -> Detected Codegen Facts -> Generation Command -> Generated Files -> Metadata Review -> Validation Result -> Risks Or Next Actions).

**Checkpoint**: Complete delivery with documented execution actions, generated files, metadata review, and any risks or next actions.

## Result Requirements

- Must describe boundary check results and codegen directory facts.
- Must describe generation command and generated files.
- Must describe metadata review including model stem, inputs/outputs, testpoints, and warnings.
- Must describe validation results if simulation was run.
- Must describe risks, unresolved testpoints, heuristics, and next actions.

## Current Limits

- Testpoint getter generation currently supports only scalar candidates that can be mapped stably from `motrace.json`.
- Natural-language matching is heuristic and should not be treated as authoritative without review.
- `tb.sv` enters CSV compare mode only when all root inputs are scalar.
- Simulator layout assumptions in `simulate.do` match the common Sysplorer codegen layout and may need manual adjustment in custom environments.
- Julia-related artifacts are only passed through and are not built by this skill.
