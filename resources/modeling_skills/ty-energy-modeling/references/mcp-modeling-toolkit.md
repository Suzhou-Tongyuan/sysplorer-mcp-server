# MCP Modeling Toolkit

Use this compact mapping when needed; exact MCP 0.4 contract, session/error/retry rules and layout writeback boundaries are authoritative in `../../ty-sysplorer-modeling-rules/references/shared-standards.md`. The optional `library_prepare` tool is lite/mols-only; it does not change fixed-version policy.

| Need | Preferred tool |
|---|---|
| Session health, attach, restart decision | `session_manager` |
| Load TY libraries | `load_library` |
| Create, open, load, save/save_as | `model_manager` |
| Classes, components, ports, text, descriptions, errors | `model_inspect` |
| Compare models | `compare_model` |
| Read class documentation | `get_lib_model_document` |
| Read Sysplorer API help | `get_api_document` |
| Local corpus or reference retrieval | `resources_retrieval` |
| Layout generation or writeback | `smart_layout` |
| Structural check | `check_model` |
| Translation | `translate_model` |
| Simulation | `simulate_model` |
| Result variables and values | `result_manager` |
| Plots | `plot_manager` |
| Narrow official API action / ExportDiagram | `get_api_document` then `call_code(mode="run_sysplorer_api", payload={...})` |

## Notes

- Prefer official higher-level tools over `call_code`.
- In `run_sysplorer_api`, explicitly import `mworks.sysplorer` before using Sysplorer APIs.
- Treat `CheckModel` as the minimum validation gate before simulation.
