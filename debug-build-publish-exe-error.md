# Debug Session: build-publish-exe-error

Status: [OPEN]

## Symptom
`install/build_publish_exe.ps1` exits with an error when executed.

## Hypotheses
1. The newly added robocopy `/XD` argument form causes PowerShell parsing or argument-passing failure.
2. The script has a pre-existing PowerShell parser issue involving here-strings or special characters.
3. The failure is caused by build prerequisites such as Python, MWorks, or required files.
4. The failure occurs during resource staging or resource overlay copying.

## Evidence
- PowerShell 5.1 parser initially reported errors beginning at the two here-string blocks in `Wait-PublishScriptExit`/`Remove-TreeBestEffort` context and the prerequisite error block.
- The file had no UTF-8 BOM after the previous edit (`bytes=3C 23 ...`), while the original script used a BOM. Rewriting it as UTF-8 with BOM and replacing the two here-string throws with ordinary strings removed the parser errors.
- Final parser check: `build_publish_exe.ps1 syntax OK`.

## Root Cause
The script became invalid for the repository's Windows PowerShell 5.1 execution path after the edit/encoding change. The parser failure was not caused by Python, MWorks, or robocopy prerequisites.
