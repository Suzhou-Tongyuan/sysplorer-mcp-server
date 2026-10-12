# Workflow: Verify Example First

Use this workflow when the environment, library capability, solver baseline, or expected result style is still uncertain.

## Goal

Confirm that Sysplorer, NPSLibrary, and the chosen model family can run a known-good example before building or repairing a larger task.

## Step 1: Choose the Closest Available Example

- Prefer an example from the same family as the target task.
- If no exact family match exists, choose the nearest topology and document the gap.

## Step 2: Record the Example Baseline

- Example name or path
- Expected key variables
- Expected solver or initialization style
- Any known library-specific setup such as `Powergui` or `LoadFlowBus`

## Step 3: Run the Example Through the Standard Gates

- Check
- Translate
- Simulate
- Result review

## Step 4: Capture the Usable Baseline

Record:

- Which tools succeeded
- Which solver and step settings worked
- Which result variables were actually readable
- Any environment-specific warnings or restrictions

## Step 5: Apply the Baseline to the Real Task

- Reuse only the verified aspects from the example.
- Do not copy example assumptions blindly if topology or ratings differ.
- State which parts of the upcoming model are now lower risk because the example passed.

## Deliverable

Produce a short baseline note that can be referenced by the later build or repair workflow.
