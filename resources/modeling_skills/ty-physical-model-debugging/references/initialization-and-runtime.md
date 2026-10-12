# Initialization and Runtime Numeric Debugging

Use these changes only in repair mode with evidence and existing authorization.
Diagnose-only mode reads the relevant evidence without applying adjustments.
Runtime/result observations below apply when required by the reported fault or
user acceptance; static-only work does not acquire unrequested KPI data.

## Build a Bounded Hypothesis

For the reported variable/system, identify its editable source declaration, its
physical domain and operating point, its current role (state, nonlinear
iteration variable, derivative, or index-reduction candidate), its
`start/fixed/nominal` and initialization equations, and directly connected
boundary conditions. Proceed only when current diagnostics, source, and a
current report form a falsifiable hypothesis.

## Priority 1: Illegal or Missing Initial Values

Strong evidence includes an initialization assertion at a function domain,
default-zero state/iteration variables, a residual dominated by a remote start,
or a stable adjacent operating point. A typical non-binding start is:

```modelica
x(start = physicalValue, fixed = false, nominal = physicalScale)
```

- `start` is a solver seed; it does not add a constraint by itself.
- `fixed=true` on a state can add an initialization constraint. Use it only when
  model semantics require a fixed initial value and degrees of freedom remain correct.
- Do not set algebraic variables `fixed=true` merely to force convergence.
- Add `nominal` only with scale evidence and use a representative nonzero magnitude.
- After an instance modifier, prove that the report uses the modified value.

## Priority 2: State Selection and Derivatives

Change state preference only when the failing chain, current state/index report,
physically interpretable alternative, and unchanged equations/degrees of freedom
all support it. Prefer soft annotations first:

```modelica
candidate(stateSelect = StateSelect.prefer)
current(stateSelect = StateSelect.avoid)
```

Reserve `always/never` for established state semantics. Retranslate and verify
the selected state set, derivatives, and system partition. Roll back when the
annotation is ignored or creates an earlier failure. A dynamic-state switch is
not itself evidence that state selection is wrong; correlate its time and old/new
states with the failure.

## Priority 3: Nonlinear Iteration Variables

For only the failed system, inspect iteration-variable paths/starts, domains,
scales/nominals, initial residual and direction, and event-driven constraint
changes. Source initial values in this order: parameter binding -> boundary
condition -> initialization equation -> physical balance point -> adjacent
successful operating point.

Change one variable, or one directly coupled minimal group, per round. Use
`debugNonlinearSolution` for bounded summaries; enable high-volume
`debugNonlinearIteration` for one round only if the summary is insufficient.

## Priority 4: Clearly Illegal Physical Parameters

Automatically correct only a value that directly explains the failure and
violates a documented/user constraint, such as nonpositive absolute temperature,
mass, capacitance, or inertia; a zero denominator; an out-of-domain medium or
geometry value; or a sampling/physical-time contradiction. Do not normalize an
extreme but intentional operating condition.

## Initialization Equation Boundary

Fast-path diagnosis may inspect and report initialization equations but must not
add/remove initial equations, change fixed degrees of freedom or boundaries, or
rewrite core equilibrium equations outside the authorized design without user
judgment. Do not ask again for an explicitly requested correction. Ordinary
syntax, type, dimension, and reference faults remain fast-path fixes.

## One Mechanism-Based Setting Comparison

Use no more than one comparison supported by a mechanism:

| Mechanism | Allowed comparison | Observe |
|---|---|---|
| Suspected stiffness | one suitable stiff solver | rejected steps, Jacobian/iterations, failure time, accuracy |
| Event resolution | one event-related setting | before/after values, event count, same root cause |
| Initial-step sensitivity | `fixedOrInitStepSize` only | first-step failure, minimum step, residual |
| Scaling | improve `nominal` before tolerance | residual/iteration change under same solver |

Never sweep algorithms, tolerances, or step sizes. A comparison that passes while
the original settings still fail proves numerical sensitivity, not a repaired model.

## Events and Hybrid Systems

With bounded event logging, correlate guards, zero crossings, discrete updates,
and repeat counts at one time. Check use of `pre()`, mode chatter, clear discrete
semantics, domain violations after an event, and changed residuals within the
same hybrid block. Do not add `noEvent()`, hysteresis, or delays automatically;
they change semantics.

## Per-Round Comparison

Keep model/settings fingerprints, first failure time and stage, diagnostic
anchor, selected states, target nonlinear variables/starts, residual/iteration
summary, minimum step, event summary, key physical KPIs, and the reason to keep
or roll back the patch.

