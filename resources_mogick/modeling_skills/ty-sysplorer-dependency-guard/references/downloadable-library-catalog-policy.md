# Downloadable Library Catalog Policy

The authoritative downloadable-library catalog is:

```text
resources/library_download_catalog.json
```

The server also has an internal default list in `DEFAULT_DOWNLOADABLE_LIBRARY_NAMES`. The resolver merges the built-in list with the external JSON catalog and keeps the built-in standard spelling when normalized names collide.

## Required Behavior

- Never use raw user input to build a download URL.
- Never invent a downloadable library name outside the catalog.
- Always inspect `library_name_resolution` when present.
- Use only `resolved_name` for latest lookup, download URL generation, archive file names, staging, and install records.

## Match Results

Allowed to continue automatically:

| `matched_by` | Meaning |
|---|---|
| `exact` | Input exactly matches the catalog spelling. |
| `case_insensitive` | Only letter case differs. |
| `normalized` | Input matches after removing spaces, `-`, `_`, and `.` and lowercasing. |
| `fuzzy` | A single high-confidence fuzzy match passed the server threshold. |

Must stop and report:

| Status | Behavior |
|---|---|
| `ambiguous_library_name` | Do not download. Return candidates and require a concrete choice. |
| `unknown_library_name` | Do not download. Report that the library is not in the downloadable catalog. |
| `invalid_library_name` | Do not download. Require a non-empty library name. |

## Examples

Allowed automatic corrections:

```text
TYMultiBody -> TYMultibody
TY MultiBody -> TYMultibody
TY-MultiBody -> TYMultibody
TY_MultiBody -> TYMultibody
tymultibody -> TYMultibody
```

Blocked examples:

```text
TYBody -> ambiguous or unknown; do not pick a candidate automatically
UnknownLib -> unknown_library_name
```

## Current Catalog Families

The catalog currently covers downloadable Modelica/Sysplorer library families such as:

```text
Modelica, ModelicaReference, NPSLibrary, SysplorerEmbeddedCoder,
TAEconomy, TADynamics, TAThermalSystem, TAEngine, TABattery, TAElectronic,
TYBase, TYMultibody, TYMechanics, TYHydraulics, TYPneumatics,
TYThermoFluidSys, TYMedia, TYElectrical, TYMotor, TYDSPSystem,
TYPhotovoltaicPower, TYWindPower, TYIntegratedEnergySys, and related TY/TA libraries.
```

This paragraph is only an orientation snapshot. The JSON catalog and internal resolver are authoritative.
