# Library Selection

Use this as the light entry point for TY hydraulic, thermal-hydraulic, pneumatic, gas-media, and thermal-support library selection. For concrete component names, continue to `component-map.md`; for installed library scope, check `sysplorer26a-builtins.md`.

## Priority

| Task signal | Preferred library |
|---|---|
| Hydraulic system, pump/valve/cylinder/oil circuit | `TYHydraulics` |
| Temperature, enthalpy flow, heat boundary, heat exchange in a hydraulic loop | `TYThermalHydraulics` |
| Pneumatic circuit, gas actuator, compressor, gas volume, exhaust boundary | `TYPneumatics` |
| Hydraulic component design or low-level component extension | `TYHydraulicComponents` |
| Thermal-hydraulic component design | `TYThermalHydraulicComponents` |
| Pneumatic component design | `TYPneumaticComponents` |
| Oil medium selection | `TYOilMedia` |
| Gas medium selection | `TYGasMedia` |
| Standalone thermal network support | `TYThermals` |

## Rules

- Prefer system libraries before component-design libraries for system assembly.
- If a temperature or heat-transfer requirement appears, do not silently stay in plain `TYHydraulics`; decide whether `TYThermalHydraulics` is required.
- If the medium is unclear and pressure/gas/temperature behavior matters, mark it as `to confirm` before validation claims.
- Do not pass off file-system/private copies as official TY components. This library list governs only selected fluid-domain commercial components; preserve standard-library components and other domains confirmed by the parent. When no library is selected, the parent uses sufficient standard components and commercial additions only for evidenced gaps, not documentation/tool failure. Commercial paths fix `Modelica 4.0.0.TY.1`.
