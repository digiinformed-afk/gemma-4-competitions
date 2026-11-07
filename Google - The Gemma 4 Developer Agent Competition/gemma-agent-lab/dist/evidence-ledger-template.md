# Task-local evidence ledger — proposed template

Use only through the competition's supported tool/skill path. Keep task state out of the submitted patch, using an allowed scratch location if available. Confirm persistence and cleanup with the current harness. Do not place secrets, gold patches or evaluator-only tests here. Reset between tasks.

## Identity and freshness
- Task ID:
- Repository / base commit:
- Current diff hash or edited-file hashes:
- Last updated at tool-call / phase:
- Observed remaining budget:

## Contract
- Reported failure:
- Required behavior:
- Relevant boundary conditions:

## Observations (not guesses)
| Fact | Path / symbol / source revision | Tool observation | Fresh after edits? |
|---|---|---|---|
| | | | |

## Hypotheses
- Active hypothesis and supporting evidence:
- Rejected hypothesis, disconfirming observation and reason not to retry:
- Remaining uncertainty:

## Changes and tests
- Changed files and purpose:
- Last reproducer command, exit status and observed failure:
- Last targeted/regression command, exit status and observed result:
- Infrastructure failure, if any (separate from defect):
- Strongest validated candidate / recovery reference:

## Next action and stopping rule
- Next grounded action:
- Evidence that would change the hypothesis:
- Finalization reserve / stop trigger:
- Patch submission status:

Proposed working-state target: about 1,000 tokens using the actual tokenizer. Compress decisions and evidence pointers; retain raw outputs separately when allowed. On resume, consult the ledger, reread edited source and reconcile stale facts before acting. A failed or truncated test is not a passing test. No source snapshot or unverified model claim is ground truth.
