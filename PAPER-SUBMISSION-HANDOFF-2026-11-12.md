# PatchQuestions — submission handoff (12 November 2026, Pakistan)

## Submission is the critical path

**Deadline:** 12 November 2026, 23:59 UTC = 13 November 2026, 04:59 PKT. Official overview: https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview ; rules: https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/rules . The earlier source review is recorded in `Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local/paper-revision/SUBMISSION-CHECKLIST.md`.

**Canonical submission source:** [PatchQuestions_Writeup.md](Google%20-%20The%20Gemma%204%20Developer%20Agent%20Paper%20Track/PatchQuestions_Local/public/project/PatchQuestions_Writeup.md) on `main`. At this audit: 2,483 whitespace-delimited words (including title, subtitle, tables and references); 7 numbered references; all abstract/introduction/methods/results/related-work sections present. This is a local count, not Kaggle's rendered counter. Do not replace with the older release/checkpoint manuscript.

**Title:** PatchQuestions: An Executable Benchmark for Budgeted API-Contract Disambiguation

**Subtitle:** A finite resource for separating probe vocabulary, adaptive selection and trusted-label cost

**Actual status:** No authenticated Kaggle submission receipt or public submitted Writeup URL has been verified. GitHub commits, passing CI, a draft, or a public notebook do not constitute submission.

## Author-side gate (must be completed on Kaggle)

1. Sign in to the eligible author's Kaggle account, accept the applicable competition terms, and open the Paper Track Writeup submission interface.
2. Paste the canonical title, subtitle and complete manuscript; check the rendered content, table formatting, reference links and the platform's word count (maximum 3,000).
3. If attaching a notebook or project link, publish it as required and test the public link in a signed-out window. An optional artifact must not delay the required Writeup.
4. Personally verify originality/unpublished status, authorship, permissions, eligibility, licensing and any declarations. These cannot be inferred from repository contents.
5. Press the **final Submit** action before the deadline; retain the submitted Writeup URL, timestamp and receipt/status screenshot. Do not rely on Save Draft.

## Claim firewall

- **Established finite benchmark:** 150 configurations, eight curated Python standard-library families, five overlapping splits, 750 target–split conditions, 18,000 policy/budget rows. At three trusted questions: random-informative 76.32%, entropy 85.27%, frugal tree 85.48% family-macro full held-out agreement. This is not 750 independent real bugs.
- **Exploratory regex intervention:** compound probes improve three-label agreement from 30.00% to 86.25% on constructed regex cases, with higher answer capacity; not a controlled equal-human-effort result.
- **Exploratory candidate-deletion stress test:** entropy-plus-verification detects absent targets in 43.15% of frozen family-macro cases at three labels versus 31.46% for entropy-stop, under a perfect oracle; not real repair evidence.
- **Toy noise audit:** exhaustive binary 3×3 matrices; verification false-rejection with present target is 0%, 10.92%, 29.54% at 0%, 5%, 15% answer-flip rates. This is a separate toy setting, not an eight-family result.
- **Not established:** real Gemma 4 performance, model-generated patch quality, repository-repair improvement, human-time savings, prospective generalization or Kaggle award/rank.

## Reproduction receipts

- Frozen open-set CPU experiment: https://github.com/digiinformed-afk/gemma-4-competitions/actions/runs/43091180332
- Python exhaustive/noisy-oracle CI cross-check: https://github.com/digiinformed-afk/gemma-4-competitions/actions/runs/43116822447
- Research ledger: [PAPER-OVERNIGHT-LEDGER.md](PAPER-OVERNIGHT-LEDGER.md)

**Execution record for this handoff:** Canonical GitHub manuscript and earlier submission checklist were fetched and inspected; local count and section/reference presence were independently checked against the fetched UTF-8 text. No Kaggle authentication, rendered preview or final submission was performed. No new experiment was run and no new empirical finding is claimed.
