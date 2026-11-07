# PatchQuestions: external AI review bundle

Prepared 7 November 2026. This is a review package, not a Kaggle submission.

## Use

Upload the ZIP to the reviewing AI and paste REVIEW_PROMPT.md. It asks 28 difficult research questions and requires answers, evidence, counterexamples and practical improvements.

## Reading order

1. REVIEW_PROMPT.md: complete review assignment.
2. paper/PatchQuestions_Writeup.md: current manuscript.
3. paper/README.md, Python modules and PatchQuestions.ipynb: implementation and reproduction.
4. paper/scores.csv, summary.json, audit.json, intervention.json: original reference results.
5. context/RESEARCH-REVIEW.md: closest prior art and novelty risks.
6. context/EXPERIMENT-PROTOCOL.md: proposed Gemma pilot.
7. context/REQUIREMENTS-COVERAGE.md: official source review and access gaps.
8. verification/python-3.15.2/: separate cross-runtime rerun and audit.

The newer cognitive_probe.py, cognitive-core-study.md and research notes are included, unlike the older research ZIP. Embedded paths in historical notes may reflect the original workspace; use this reading map instead. This package grants no new license and does not publish the work.

## Evidence boundaries

The draft attributes reference measurements to CPython 3.12.14. paper/cross_version_summary.json records historical 3.13.5 results. The separate 3.15.2 rerun reproduced entropy/tree aggregates but has small random-policy differences. Keep runtimes separate; do not claim a fresh 3.12.14 reproduction.

The 18,000 reference rows represent 750 target/split conditions on eight families, six policies and four budgets. These are not 750 independent bugs. The benchmark assumes a correct candidate and perfect labels; candidate execution costs and human time are separate from question count.

No Gemma pilot, human-time study, real-repository repair evaluation or leaderboard submission has been completed. The proposed 32-session pilot is a feasibility study. The entropy masking check is a control, not a model result.

## Competition context

Recorded paper deadline: 12 November 2026 23:59 UTC / 13 November 04:59 PKT. Report maximum: 3,000 words. Original unpublished research and an explicitly submitted Kaggle Writeup are required. Five equally weighted dimensions: Novelty, Quality, Relevance, Verifiability and Clarity. Recheck current sources rather than assuming the schedule remains unchanged.

- https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview
- https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/rules
- https://www.kaggle.com/competitions/gemma-4-developer-agent/overview
- https://www.kaggle.com/competitions/gemma-4-developer-agent/rules

Full HARNESS_README, actual official sample files and exact model terms are not included or claimed reviewed. Source summaries are included, not downloaded copies of all papers or rules. Report source-access limitations honestly.

## Reproduction and integrity

Copy the Python modules into a fresh writable run directory and execute the documented commands there. Do not replace reference results. Put frozen_cases.jsonl.gz beside cognitive_probe.py for its --check control. The frozen archive contains grading outputs: never expose it to an evaluated model with filesystem access.

FILE_MANIFEST.json lists SHA-256 hashes and byte counts of every payload except itself. Original paper files are unchanged copies. Local user/workspace paths in verification copies were replaced with placeholders. No dashboard databases, API keys, account credentials, private uploads or restricted Kaggle datasets are bundled.
