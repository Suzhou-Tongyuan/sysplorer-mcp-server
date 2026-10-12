# Resource Map

Use this file when you need to decide quickly which reference to read next.

## By Stage

| Stage | Read first | Read next |
|-------|------------|-----------|
| Requirement understanding | `standard-input-checklist.md` | `input-output-contract.md`, `phase-output-templates.md` |
| Tool choice / MCP routing | `mcp-modeling-toolkit.md` | `sysplorer_api_usage.md` |
| High-frequency component lookup | `nps_component_quick_index.md` | `component-mapping.md`, `nps-typical-scenarios.md` |
| Ground / reference fallback | `component_fallback_strategy.md` | `nps-domain-rules.md`, `nps-common-errors.md` |
| Sample model reuse | `Sysplorer 2026a\Docs\EleLib\Samples\NPSLibrary` | `nps-typical-scenarios.md`, `component-mapping.md` |
| Parameter completion | `sysplorer_api_usage.md` | `nps-domain-rules.md`, `phase-output-templates.md` |
| Model construction | `nps-domain-rules.md` | `component-mapping.md`, `templates/modelica/minimal-nps-model.mo.tpl` |
| Check | `nps-domain-rules.md` | `phase-output-templates.md` |
| Translate | `nps-common-errors.md` | `error-repair-playbook.md` |
| Simulate | `nps-domain-rules.md` | `phase-output-templates.md`, `acceptance-checklist.md` |
| Result verify | `acceptance-checklist.md` | `nps-domain-rules.md`, `phase-output-templates.md` |
| Delivery | `input-output-contract.md` | `acceptance-checklist.md`, `templates/acceptance-report-template.md` |

## By Problem Type

| Problem | Read first |
|---------|------------|
| Sysplorer vs Syslab uncertainty | `mcp-modeling-toolkit.md`, `sysplorer_api_usage.md` |
| Class name or library uncertainty | `nps_component_quick_index.md`, then `manual-text/NPSlibrary模型清单.md` if still unresolved |
| Grounding or isolated-side issue | `component_fallback_strategy.md`, `nps-domain-rules.md` |
| Step size or solver uncertainty | `nps-domain-rules.md`, `nps-common-errors.md` |
| Port mismatch or interface conversion | `component-mapping.md`, `component_fallback_strategy.md`, `nps-common-errors.md` |
| Need a ready-made scenario scaffold | `templates/scenarios/scenario_index.json` |
| Need an official or reusable NPS example | `Sysplorer 2026a\Docs\EleLib\Samples\NPSLibrary` |

## Search Discipline

- Prefer `nps_component_quick_index.md` for repeated, high-frequency component categories.
- Prefer the samples path for example-oriented requests instead of deep library-document traversal.
- Use `get_lib_model_document` only after the quick index, samples path, and concise references are not enough.
- Batch similar lookups and deduplicate overlapping search results.
- Avoid reopening the same manual or querying the same library path multiple times in one task unless new evidence requires it.
