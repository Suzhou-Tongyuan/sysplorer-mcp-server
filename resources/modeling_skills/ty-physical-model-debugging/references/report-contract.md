# Debug Report Contract

Select `task_mode: diagnose_only|repair` and `terminal_stage` from the user request.
For each check, translation, codegen, build, simulation, result/KPI and layout item,
record `required: true|false`, `status: passed|failed|not_required|not_run`, and
evidence when applicable. Do not treat `not_required` as a missing check.

## Per-Round Evidence

Record the hypothesis, current model/source identity, working identity, first
attributable diagnostic, counter-evidence, exact patch and checkpoint (repair
only), temporary settings, performed stages and keep/rollback/escalate decision.
Reuse existing evidence; unknown fields do not justify unrelated tool calls.
An apparent pass from stale logs, changed error wording, disabled protection or
a different unrequested solver is not a fix. Incomplete settings limit only
claims that depend on them; static diagnosis needs no full runtime fingerprint.

## Final Status

- `diagnosis_complete`: the requested diagnosis has supporting evidence; state
  whether the root cause is confirmed or a remaining hypothesis. No repair is
  claimed. Missing evidence needed for the diagnosis uses `verification_required`.
- `verified_solved`: requested repair stages and acceptance pass, exact patch
  readback/source ownership is established, originals remain protected, and
  temporary settings are restored. Static-only fixes need no simulation/stop time.
- `partially_improved`: repeatable improvement exists but required repair
  acceptance is incomplete; identify the outstanding stage/condition.
- `verification_required`: missing/invalid required tool, environment or behavior
  evidence prevents the requested conclusion, even if execution itself succeeds.
- `automatic_debugging_stopped`: an unresolved scope/authorization boundary or
  unavailable capability prevents further useful automatic work.

The requested terminal stage is the validation limit. Runtime acceptance requires
the agreed original end time and baseline settings. Results/KPIs are required only
when requested or necessary to resolve abnormal behavior; otherwise they are
`not_required` and must not be read speculatively. Actual changed graphical
targets retain their applicable modeling delivery requirements.

Report originals/work-copy paths and hashes when relevant to performed edits,
settings changes and restoration, checkpoint retention, and remaining risks.
Diagnose-only offline work need not invent a copy or runtime evidence. Any failed
compensation must name affected files and blocks a verified repair claim.
