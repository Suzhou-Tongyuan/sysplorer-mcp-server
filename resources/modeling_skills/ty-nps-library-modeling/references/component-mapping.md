# Component Mapping Quick Table

Use this file as a fast lookup table when the scenario is known but the exact class path is still uncertain.

| Intent | Typical blocks to search | Supporting blocks | Key observables | Common misuse to avoid |
|--------|--------------------------|-------------------|-----------------|------------------------|
| Three-phase source network | source, line, transformer, load, breaker | `Ground`, `Powergui`, voltage and current sensors | Node voltage, branch current, P/Q | Forgetting reference ground or phase-sequence review |
| Grid-tied inverter | converter bridge, filter, PCC, `PLL`, PWM, dq controller | `Powergui`, voltage/current sensors, P/Q measurement | Grid current, PCC voltage, DC bus voltage | Skipping `PLL`, mixing wrong voltage definition, unreadable diagram |
| Boost converter | switch, diode, inductor, capacitor, load | `Ground`, PWM, current and voltage sensors | Output voltage, inductor current | Using oversized step size or omitting duty-cycle evidence |
| Bidirectional DCDC | bidirectional switches, inductor, storage, bus capacitor | `Ground`, current sensor, voltage sensor, PWM | Bus current, charge/discharge direction, DC bus voltage | Ambiguous current sign convention |
| Motor drive | inverter, motor, transforms, PI, PWM, speed loop | `Powergui`, speed/current/angle sensors | Speed, torque, dq current | Missing coordinate transform or controller loop closure |
| Load-flow network | source, line, transformer, load, `LoadFlowBus` | `Powergui`, P/Q settings, slack or control node | Voltage magnitude, phase angle, branch P/Q | Missing load-flow initialization role definitions |

Load-flow initialization hint:

- Ask first whether the user wants load-flow initialization or faster steady-state entry.
- When the answer is yes, prioritize `LoadFlowBus`, bus-role definition, and load-flow initialization blocks before building only a plain time-domain source network.

## Interface Reminders

- Single-phase to three-phase transitions should use conversion blocks, not unsafe direct connections.
- If a component is vectorized, record the dimension and phase meaning before wiring it into the network.
- If the class path is still uncertain after quick lookup, fall back to `references/manual-text/NPSlibrary模型清单.md`.

## Search Priority For User-Specified Topology

- If the user explicitly requires a topology or key component, do not stop at the first failed candidate.
- Continue searching `NPSLibrary` for alternative class paths, sibling component families, interface adapters, or conversion blocks that preserve the requested topology intent.
- Only after the `NPSLibrary` search space has been exhausted should you discuss changing or downgrading the topology with the user.
