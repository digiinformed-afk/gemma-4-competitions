# PatchQuestions overnight research ledger — 2026-11-12 (Pakistan)

## Study 1: correct candidate absent (EXECUTED)

- **Code:** [scripts/paper_open_set.py](../scripts/paper_open_set.py)
- **Execution:** [GitHub Actions run 43091180332](https://github.com/digiinformed-afk/gemma-4-competitions/actions/runs/43091180332) — success, CPython 3.12.16 on Ubuntu.
- **Artifact:** `patchquestions-open-set-43091180332` in the run's Artifacts area; retention 30 days.
- **Frozen dataset SHA256:** `a60edcc4b000353aaa40b86e8b2380ccd6555d99af8b149f995c22c7d289f70f`.
- **Recorded evaluation rows:** 13,500 = 750 target/split conditions × 2 candidate-presence states × 3 policies × 3 budgets (1,2,3).
- **Result:** for a 3-question budget, family-macro absent-target contradiction detection was **34.79%** for fixed sequential queries, **31.46%** for entropy with early stopping, and **43.15%** for entropy with verification queries. At budgets 1 and 2, detection respectively was fixed 12.19/22.50%, entropy-stop 23.70/31.46%, and entropy-verify 23.70/36.67%.
- **Mechanism under test:** selectors use only the visible candidate query-output matrix and answers acquired to date. If every remaining candidate agrees, a standard entropy selector stops; a verification selector continues by choosing an unused question based on its *initial candidate-pool* entropy. This can expose a mismatch even after a singleton survives.
- **Do not overstate:** this is an artificial candidate-deletion, **perfect-oracle** simulation on eight manually curated Python API families with five overlapping split universes, not a measured model improvement, not real software-repair evidence, and not a prospective sample. The 13,500 rows are *not* independent real-world cases. The missing-candidate outcome is never given to the policy; held-out matrix is used only in analysis.
- **Scientific interpretation:** Selecting questions solely to partition plausible candidates can miss *falsification/verification* value. The verification rule improves failure detection in this finite setting. Larger independent suites and noisy-oracle comparisons are needed to assess generalization.

## Evidence priority and experiment queue

1. **SUBMISSION CRITICAL:** Preserve canonical PatchQuestions manuscript and existing 18,000-row evidence; verify <3,000 words, title/subtitle, citations, public links, unpublished status. **Kaggle Writeup must be actually submitted** by Nov 12 2026 23:59 UTC / Nov 13 2026 04:59 Pakistan. Draft-only is not sufficient.
2. **Next CPU robustness:** trusted-label noise injection (0%, 5%, 15%) with matched seeds and a no-noise control, compare hard elimination with appropriately specified noisy Bayesian filtering. Report accuracy plus contradiction/abstention, do not conflate.
3. **Validation:** independent targeted checks of candidate-deletion experiment, including leakage audit, per-family stratification, counterexamples and sensitivity to tie-breaking/query ordering.
4. **Cost comparison:** report query count AND UTF-8 character/token or human-response effort for high-information compound questions; note differing information capacity.
5. **Model-in-the-loop only when compute is accessible:** fixed Gemma 4 checkpoint, 16 balanced pairs, matched prompt/seed/hardware/budgets, actual logged model actions and error rates. Do not infer model effect from simulated questions.
6. **Research claim audit:** document relative novelty against InPaFer, LEARN2FIX, xTestCluster, generalized binary search, CodeMonkeys and clarification works. Keep limitations candid.

## State of submission

At time of this entry, no new Kaggle Writeup submission is confirmed. GitHub Actions execution is *not* a Kaggle submission. Paper modifications should incorporate only independently verified, correctly scoped claims and remain under the official word limit.

## Reproduction

```bash
python scripts/paper_open_set.py --self-test
python scripts/paper_open_set.py --output paper-results/open-set.json
```
