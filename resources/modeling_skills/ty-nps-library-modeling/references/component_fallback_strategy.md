# Component Fallback Strategy

Use this file when common reference-point primitives are missing from NPSLibrary or when interface compatibility becomes the main blocker.

## Applies To

- `Ground`
- `Reference`
- `ElectricalReference`
- `Neutral`
- `Terminal`
- other common reference-point primitives

## Primary Rules

1. If `Ground` is not found inside NPSLibrary, do not keep re-searching for it.
2. For single-phase or DC systems, prefer:

```modelica
Modelica.Electrical.Analog.Basic.Ground
```

3. For three-phase systems that need a neutral grounding point, prefer:

```modelica
Modelica.Electrical.Polyphase.Basic.Star
```

Connect the three phases to `Star` first, then connect the star point to `Ground`.

## Interface Compatibility

If an NPS interface is not directly compatible with a Modelica Standard Library connector, do not force the connection.

Follow this order:

1. Look for an equivalent reference-point component inside NPSLibrary.
2. Look for an adapter component within the same library family.
3. If no safe adapter path exists, stop and request manual confirmation of the intended interface adaptation.

## Search Limit

- Search common primitives such as `Ground`, `Reference`, `ElectricalReference`, `Neutral`, and `Terminal` at most two times.
- If they are still unresolved after two attempts, trigger the fallback path instead of continuing deep library traversal.

## Operational Guidance

- Prefer this fallback document over repeated root-to-leaf library browsing when a common primitive is missing.
- Keep the topology reviewable: use explicit fallback components and explain why they were chosen.
- Record any adapter or manual-confirmation requirement in the delivery notes.
