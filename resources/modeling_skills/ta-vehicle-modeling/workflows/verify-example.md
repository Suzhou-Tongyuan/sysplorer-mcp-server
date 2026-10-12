# Verify Example Or Results

Use this workflow for official examples, enterprise examples, result curves, or correctness review.

## Read

1. `../references/requirement-map.md`
2. `../references/validation-rules.md` only when result review is in scope
3. `../references/library-selection.md` when selecting an example by task goal
4. One selected `../references/library-cards/<library>.md`
5. `../templates/reports/result-summary-template.md` when writing a result summary

## Do

- First record the requested terminal stage. Finding/opening an example does not require checking, simulation, or result reads. When result review is required, confirm the model entry point, explicit result file, and fresh run provenance before reading variables.
- For "find/open an example" or "confirm whether an example exists", directly load the named or inferred TA library first, then explore candidate classes and class documents. Do not route this through `library-selection.md` except when the user did not name a TA library and the primary library must be inferred from the task goal.
- Use manuals/resources only as supporting evidence after the candidate library or class path is known, or when class exploration cannot disambiguate the result.
- Confirm result variable names before reading values or plotting curves.
- Validate only what was actually simulated or loaded from an explicit result file.
- For official examples, use them as reference, baseline, or comparison sources; do not treat them as user deliverables unless the task explicitly asks for adaptation.

## Report

- Before final delivery, read `../references/output-contract.md` and answer `../references/acceptance-checklist.md`; do not report completion if any acceptance item fails.
- Example/model entry, target variables, actual result source, verified values or trends, pass/fail/no-reference judgment, and unresolved items.
