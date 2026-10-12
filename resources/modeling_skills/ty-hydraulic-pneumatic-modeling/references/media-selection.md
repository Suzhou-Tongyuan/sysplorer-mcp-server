# Media Selection

Use this as the light entry point for medium decisions. Medium selection is structural: it can change compatible ports, state variables, initialization, and result interpretation.

## Defaults

| System type | Preferred medium library | Notes |
|---|---|---|
| Hydraulic | `TYOilMedia` | Choose or confirm oil grade when pressure/flow response matters. |
| Thermal-hydraulic | `TYOilMedia` with `TYThermalHydraulics` | Confirm temperature range, heat boundary, and whether heat ports are active. |
| Pneumatic | `TYGasMedia` | Confirm gas type, source pressure, exhaust/surrounding boundary, and temperature assumptions. |
| Thermal support | `TYThermals` | Use only for thermal-network support, not as a fluid-system replacement. |

## Hard Checks

- Do not claim verification if the chosen medium is still implicit and affects the user objective.
- Re-check after changing medium package, because compatible connectors and initialization may change.
- Treat zero flow, impossible pressure, missing temperature response, or gas-state divergence as possible medium/boundary faults before tuning solver settings.
