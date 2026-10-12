# Bounded Deep Debugging

## Entry Conditions

Enter when lightweight evidence is insufficient and a bounded anchor can resolve
the current question. State the scope and byte budget; authorized inspection of
user-owned artifacts needs no separate approval. New scope or unavailable access
requires user input. Never inspect protected commercial implementations through
RMF/Flat/generated C. Diagnose-only remains non-mutating.

## Pair Every Artifact to One Run

Use model FQN, work-copy hash, settings fingerprint, translation/simulation time,
and solver-directory identity to prove that logs and artifacts belong to the
same run. Unpaired artifacts cannot justify an edit.

## Anchored Search Order

Start with an existing variable, system/equation ID, runtime code, assertion, or
source text, and read bounded excerpts in this order:

1. `Variables.xml`: IDs, variable names, and aliases.
2. RMF: system, residual, and equation mapping.
3. `*_Flat.mo`: declarations, bindings, initial equations, and component paths.
4. RuntimeDebug `momodel.c` / `momodel_func.c`: annotated system functions and residuals.

Build only the shortest chain needed for the current decision:

```text
reported variable/system -> residual/equation -> actual state or iteration variable -> editable source variable/parameter
```

When the chain breaks, report the confirmed layer and the missing evidence.

## Permitted Deep Changes

The completed mapping may support a physically justified `start/nominal`, a
report-supported state candidate in the same derivative relation, correction of
a hidden initialization conflict, or a parameter/modifier/equation that directly
causes an unsatisfied or illegal-domain system. Component removal/addition,
topology, boundary, or degree-of-freedom changes require judgment only when they
exceed the existing authorized design. Read-only diagnosis never applies patches.

## Nonlinear Variable Reselection

Test `MNonLinearVariables` only after mapping a failed hybrid block through its
discrete decision/continuous constraint to source variables. It changes
tearing/elimination and is not an ordinary initial-value adjustment.

Choose at most one candidate per layer: continuous operands of guards/zero
crossings, values closing the same residual loop, interface compatibility or
conservation quantities, then adjacent states/derivatives that govern those
constraints. Never select generated names such as `R_[n]` or `mwAux.*`.

After each round, verify that the candidate was retained, the partition changed
as predicted, the original settings pass the failure point, and conservation and
physical KPIs remain valid. Remove an ignored, ineffective, or non-repeatable annotation.

## Stop

After two rounds without improvement, stop the current hypothesis. Use a new
targeted source of evidence or a minimal case when authorized and useful; do not
repeat complete-model guesses. A still-broken mapping, unsupported capability or
protected-source dependency blocks that operation; report the remaining evidence
gap and a bounded next step instead of declaring the whole task solved.

