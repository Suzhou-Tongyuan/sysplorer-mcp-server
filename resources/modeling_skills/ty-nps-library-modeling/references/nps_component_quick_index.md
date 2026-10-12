# NPS Component Quick Index

Use this file before traversing NPSLibrary manuals or repeatedly querying library documents.

## Ground And Reference Primitives

Prefer Modelica Standard Library grounding primitives when NPSLibrary does not expose a suitable `Ground` component.

Single-phase or DC reference:

```modelica
Modelica.Electrical.Analog.Basic.Ground
```

Three-phase neutral collection before grounding:

```modelica
Modelica.Electrical.Polyphase.Basic.Star
```

Rules:

- If `Ground` is not found inside NPSLibrary, do not keep re-searching for it.
- For single-phase or DC reference points, prefer `Modelica.Electrical.Analog.Basic.Ground`.
- For three-phase systems that need a neutral point, use `Modelica.Electrical.Polyphase.Basic.Star` first and then connect the star point to ground.
- If the interface is incompatible, do not force the connection. Look for an adapter or request manual confirmation.

## High-Frequency Component Paths

| Component Category | Recommended Search Path | Notes |
|---|---|---|
| Interfaces | `NPSLibrary.Interfaces` | Look for `PositivePlug`, `NegativePlug`, and three-phase electrical connectors. |
| Sensors | `NPSLibrary.Sensors` | Voltage, current, power, RMS, and similar measurement blocks. |
| Sources | `NPSLibrary.Sources` | Ideal sources, three-phase voltage sources, and controlled sources. |
| Lines | `NPSLibrary.PowerSystem.TransmissionAndDistribution.Line` | Three-phase lines, pi-section lines, RL lines. |
| Loads / RLC branches | `NPSLibrary.PowerSystem.Load` | Basic loads and RLC load structures. |
| Dynamic loads | `NPSLibrary.PowerSystem.Load.DynamicLoad` | Dynamic load models. |
| Constant-power loads | `NPSLibrary.PowerSystem.Load.ConstantPowerLoad` | Constant-power load models. |
| Transformers | `NPSLibrary.PowerSystem.TransmissionAndDistribution.Transformer` | Two-winding, three-winding, and wiring-group variants. |
| Power electronics / converters / generators | `NPSLibrary.PowerElectronics` | Switches, rectifiers, inverters, PWM, pulse generation. |
| Reference-frame transforms | `NPSLibrary.Utilities.Reference_System_Transformation` | `abc/dq`, `dq/abc`, Clarke, Park, and related transforms. |
| Control / integrator / filter | `NPSLibrary.Utilities.Control` | PI, integrator, filter, and controller blocks. |
| Breakers | `NPSLibrary.PowerSystem.TransmissionAndDistribution.Breaker` | Three-phase breakers, switches, and fault switching components. |
| Renewable energy / PV / battery / supercapacitor | `NPSLibrary.PowerSystem.RenewableEnergy` | PV, battery, storage, and supercapacitor models. |
| Motors / synchronous / asynchronous / wind | `NPSLibrary.Motors` | Motor and wind-generation families. |

## Example Search Path

When the request mentions reusing an existing example, an official sample, or building from a reference case, search this path before deep library traversal:

```text
Sysplorer 2026a\Docs\EleLib\Samples\NPSLibrary
```

Use scenario keywords first:

- `Line`, `Transmission`, `Distribution`
- `Transformer`
- `Load`, `RLC`, `ConstantPowerLoad`
- `PowerElectronics`, `Rectifier`, `Inverter`, `PWM`
- `RenewableEnergy`, `PV`, `Battery`
- `Motors`, `Synchronous`, `Asynchronous`, `Wind`

When a suitable sample is found, reuse its component paths, parameter-writing style, connection style, and annotation style before searching from scratch.

## Usage Rules

1. Check this file first for high-frequency components.
2. If a quick-index path already resolves the category, do not traverse from the NPSLibrary root.
3. Use `get_lib_model_document` only when the quick-index path is still too broad to identify the exact class.
4. Batch queries by category instead of making repeated single-point lookups.
5. Merge semantically similar search results such as `voltage source`, `three-phase voltage source`, and `AC voltage source`.
6. Do not repeat `get_lib_model_document` for the same path.
7. Limit deep traversal and repeated document queries unless the task truly needs them.
