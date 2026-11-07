# Revision decisions and changes

Revised locally on 7 November 2026 after the user reassigned the external review follow-up to this chat. Originals remain in the dated original review export and received-review archive.

| Change | Reason and evidence |
|---|---|
| Resource title and contribution | Current measurements isolate finite API-contract disambiguation; no autonomous repair experiment exists. |
| Crossed entropy/frugal table | Reviewer checks and local rerun show both reach 86.25% with compound regex probes at budget three. Budget two retains a 6.25-point frugal margin. |
| Comparator-specific question savings | Recalculated 17.705747% against ordinary tree, 0.929872% against entropy, with absolute question differences. |
| Explicit identity objective and counterexample | Independent reviewer enumeration rerun locally; identity-optimal querying can be weaker for behavioral agreement. |
| Class counts and family sensitivity | Hex has 36 configurations/30 joint behaviors. Dropping CSV removes the budget-three entropy/frugal accuracy gap. |
| Selected-transcript costs | New descriptive reanalysis of existing arms; 2,880 target/policy/pool/budget/scoring-suite rows, each traced against the unchanged evaluator. Includes selected input/answer lengths and conditional information. |
| Direct prior-work table | Existing identification/filtering/clustering mechanisms acknowledged; primary source links and reading depth recorded. |
| Strict model-pilot supervisor | Adds query-consistency success, strict actions, sample/row/label randomization, private plan, model-input whitelist, raw logs and failure-inclusive recovery. Historical replay and score definitions remain available. |
| Nine-module notebook | Rebuilds original results and new analysis, preserves embedded reference matrices, includes deterministic scoring-boundary fixture. Execution status is in notebook verification. |
| Separate original and runtime outputs | Avoids combining historical 3.13.5/3.15.2 records with the fresh 3.12.14 reproduction. |

## Decisions on new experiments

No new API family is added. Designing, freezing and interpreting a prospective output-capacity control would create a new empirical claim with moderate development risk. The current resource's usefulness is demonstrated by the all-query regex diagnosis and crossed simple-baseline comparison. Reanalysis strengthens those existing claims directly.

No Gemma inference session is started. This paper has no demonstrated serving endpoint, verified model artifact or active compute balance. Main-track packaging and scripted smoke tests do not establish paper-model feasibility. This is a current readiness decision; the 8 November 18:00 PKT access gate remains a proposed future cutoff, rather than a completed historical gate. The complete paper does not depend on that gate succeeding.

If working access becomes available before that gate, perform only development smoke/context checks before a checkpoint-specific frozen 16-pair feasibility plan. The new supervisor samples across configuration halves and uses family/pair-specific row and label permutations. This supersedes the older, unrun targets-0/1 sample. No scored outcome has been inspected and no real-checkpoint sample has been frozen. Save any eventual negative or failed run. A model result could demonstrate interface use and representation sensitivity on this sample; it could not establish semantic isolation, model internals, human savings or repair gains.

## Reproduction and portability record

Fresh local runtime is Windows CPython 3.12.14, a different build/platform from the external AI's Linux CPython 3.12.14. All original 18,000 CSV rows match byte for byte. Summary, audit and intervention JSON match after parsing. Windows stdout CRLF explains their byte differences.

Two earlier local reviewer-audit attempts are preserved. The first timing variant decoded UTF-8 Python source with the Windows system encoding, changing non-ASCII literals and failing its reference assertion. The second made reading UTF-8 explicit and exposed a corresponding source-write encoding error. The completed third run specifies UTF-8 for both operations. The original reviewer source is preserved separately; no benchmark scoring logic was changed.

The completed run repeats all 24,000 exact random-policy metric comparisons and 16,384 exhaustive tree-objective checks on 4,096 binary matrices. It also repeats the 750 displayed/native entropy checks and contradictory-pick example. Timings are diagnostic and not a speed ranking.

The first notebook verifier stalled before starting a kernel under restricted Windows process/temp access. It was stopped and restarted with workspace-local temporary files and a permitted kernel process. The notebook execution record reports the completed attempt; the initial stall supplies no notebook result.

The first extracted-release smoke run reproduced the scores and summaries but exposed a reporting bug in the command-line wrapper: it labeled raw decompressed JSONL byte equality as matrix-record equality. Windows text-mode CRLF made the bytes differ while the 40 parsed records were identical. The wrapper now reports parsed-record equality and decompressed-byte equality separately. The initial archive and smoke outputs are preserved; the final package includes the corrected wrapper.
