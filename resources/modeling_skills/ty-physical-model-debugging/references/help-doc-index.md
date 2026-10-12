# Installed Help Query

Treat help shipped with the active Sysplorer installation as the authority. The
Skill contains query logic, not a versioned copy of the product manual.

## Help Corpora

The query helper selects the corpus by operation:

| Operation | Installed index |
|---|---|
| Exact product diagnostic lookup | `Docs/FAQ/pageData/page-data-list.json` |
| Topic and debugging-option search | `Docs/DevelopingModels/pageData/page-data-list.json` |

Pass the current `GetInstallationDirectory()` result with `--root` when it is
already available. The helper accepts an installation root, a `Docs` directory,
or a direct corpus root. It refuses to guess when multiple installations exist.
A missing requested corpus is an unavailable-help error, not `not_documented`;
it must not silently substitute DevelopingModels for FAQ.

## Diagnostic Lookup

Product diagnostic pages use category-specific paths:

- error: `ErrorsReference/Error/Error{code}.html`
- warning: `ErrorsReference/Warning/Warning{code}.html`
- message: `ErrorsReference/Message/Message{code}.html`

Codes contain one to eight digits. Keywords are optional and measure whether
the official entry agrees with the observed context; they do not hide the exact
candidate.

```powershell
python scripts/query_sysplorer_help.py --error-code 4 --kind error --root "<install>"
python scripts/query_sysplorer_help.py stateSelect --error-code 6170 --kind error --root "<install>"
```

`--kind auto` may return same-number candidates from multiple categories. A
missing page returns `status=not_documented`. A documented entry whose text does
not contain the supplied context returns `context_conflict=true`.

## Namespace Rule

A number is not a globally unique diagnosis.

- `Error(n)`, `Warning(n)`, and their Chinese equivalents are product-help
  candidates, subject to message and stage agreement.
- `error code: n` or its localized colon form in compiler, linker, process, or generated-solver
  output is normally a toolchain return code. Diagnose the first specific nested
  message instead of mapping it to `Error(n)`.
- An API validation error must be interpreted with the API name, field, and full
  message. Do not map it to a model diagnostic solely because the number matches.
- Even a product-form candidate is not conclusive when its help text conflicts
  with the observed message or stage. Report the namespace conflict and keep the
  direct runtime evidence primary.

For example, FAQ `Error(4)` concerns state-machine action expressions. A GCC
link log ending with `error code: 4` and `undefined reference` is a linker
failure, not FAQ `Error(4)`.

## Topic Query

Use ordinary terms without `--error-code` for bounded searches of modeling and
simulation documentation:

```powershell
python scripts/query_sysplorer_help.py runtime check --root "<install>" --max-records 5
```

Relevant topics include model debugging, external-function environments,
simulation debugging settings, solver-version differences, and external
resources. Use `resources_retrieval` only when installed help is unavailable or
has no relevant topic. Never infer an explanation from a similar number.
