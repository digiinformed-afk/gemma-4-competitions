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


## Study 1a: independent exhaustive selector audit (2026-11-12 01:xx PKT)

- **Code committed:** [scripts/paper_open_set_exhaustive_audit.py](scripts/paper_open_set_exhaustive_audit.py), commit `15277bc461222db25445d1b81c581d5f9f37508e`.
- **Executed cross-check:** independent JavaScript enumeration of all 512 binary 3-candidate × 3-query matrices, all 3 target identities (1,536 target conditions), both presence states, all three query budgets, and the fixed/entropy-stop/entropy-verify policy rules. This is a *toy exhaustive correctness check*, not a new software benchmark or model experiment.
- **Observed invariants:** 0 false absent-target detections when the correct candidate is present; 0 cases where entropy-stop detects absence but entropy-verify fails; 2,088 absent-target/budget conditions where verification detects and entropy-stop does not; 360 target conditions with a remaining candidate identical on every query, and 0 detections in those indistinguishable cases across all three policies at budget three.
- **Reproduction status:** independent JavaScript audit **executed**. Python audit source **committed but not yet executed in GitHub Actions**; no Python pass is claimed. Run `python scripts/paper_open_set_exhaustive_audit.py` in a checked-out repository to cross-validate the expected counts. This small-grid check does not independently replicate the 13,500-row real frozen-matrix study.
- **Interpretation:** zero false positives and the monotonicity of verification versus early stopping follow from the perfect-oracle, exact-match protocol. They should **not** be presented as empirical robustness to noisy labels. Detection is impossible when a missing target has a query-identical available candidate.
- **Next priority:** run the Python audit in CI, then add a matched noisy-oracle study; do not change the manuscript's central result based on toy enumeration alone.


## Study 1b: noisy-oracle protocol prepared (2026-11-12 02:xx PKT)

- **New script:** [scripts/paper_noisy_oracle_audit.py](scripts/paper_noisy_oracle_audit.py), committed and newline corrected in commit `a89976afdd9813b0f35e15538f6642b62f378049`.
- **Design:** exact enumeration of all 512 binary 3-candidate × 3-query matrices, all three target identities, present/absent correct-candidate conditions, three budgets, three policies, and independent Bernoulli answer flips at 0%, 5%, and 15%. Noise schedules are indexed by the order questions are asked, avoiding a policy-dependent column-flip confound. Reports contradiction rate, question usage, and target survival with matched finite cases.
- **Status:** SOURCE COMMITTED, **NOT YET EXECUTED**. No numerical noise findings are claimed. This is a toy correctness/stress test, not a Gemma experiment or a prospective benchmark. Run `python scripts/paper_noisy_oracle_audit.py --output paper-results/noisy-oracle-toy.json` and independently check the resulting JSON before citing any result.
- **Additional validation this run:** an independent JavaScript enumeration rechecked the earlier 512-matrix perfect-oracle invariants: 0 present false detections, 0 verification regressions, 2,088 verification-only detections across budgets, 360 indistinguishable absent target conditions, 0 impossible detections. This **does not** constitute execution of the committed Python exhaustive-audit script.
- **Caution:** under label noise, hard elimination may falsely reject an actually present target. Any claimed open-set benefit must be reported alongside false-rejection rate; do not add noisy-oracle conclusions to the manuscript until execution.


## Study 1c: independent noisy-oracle enumeration (2026-11-12, executed)

- **Result report committed:** [PAPER-NOISY-ORACLE-TOY-RESULTS-2026-11-12.md](PAPER-NOISY-ORACLE-TOY-RESULTS-2026-11-12.md), commit `9eaf5b20e723926bc0e26d106fb9e646c32425b0`.
- **Execution:** independent JavaScript exact weighted enumeration executed in ChatGPT tool runtime. Local Python/container execution failed to start; **neither committed Python audit has been run here**, and no CI pass is claimed.
- **Budget 3:** target-present false-rejection for verification: 0% (no noise), 10.92% (5% flips), 29.54% (15% flips); absent-target detection 76.56% in this exhaustive symmetric 3×3 binary toy. Entropy-stop has zero contradiction detection in this toy setup, not generally.
- **Interpretation:** hard-elimination verification is vulnerable to noisy labels. This is a toy protocol result, **not Gemma performance** or real bug-repair evidence; keep separate from frozen 750-condition benchmark. The report contains matched controls, question counts and limitations.
- **Next:** run Python audits in CI and compare all 54 result cells, then focus on the actual Kaggle Writeup submission and claim audit.

## Study 1d: Python CI cross-validation completed (2026-11-12 04:xx PKT)

- **Commit:** `bc92b29fd9739b0a7f8fc7293df024dd410b6803` extended `.github/workflows/paper-experiments.yml` to run both previously unexecuted Python audits on CPython 3.12, in addition to preserving the original frozen-matrix experiment.
- **Verified GitHub Actions execution:** [run 43116822447](https://github.com/digiinformed-afk/gemma-4-competitions/actions/runs/43116822447) completed successfully. Both `open-set` and `independent-toy-audits` jobs have GitHub-reported `success` conclusions.
- **Independent Python audit:** `scripts/paper_open_set_exhaustive_audit.py` executed with its built-in exact count assertions. This validates the 512-matrix invariants previously obtained through independent JavaScript enumeration.
- **Noisy-oracle Python audit:** `scripts/paper_noisy_oracle_audit.py` executed, wrote `paper-results/noisy-oracle-toy.json`, and passed independently specified anchor assertions for budget-three 0%, 5%, and 15% noise cells. The CI job uploaded machine-readable JSON and audit logs using `actions/upload-artifact@v4`.
- **Scope:** The Python/JavaScript agreement is a *toy protocol correctness cross-check*, not an independent prospective software-task sample, not a Gemma evaluation, and not evidence of end-to-end repair improvement. The CI assertions check anchor cells, not all 54 result cells against a separate implementation.
- **Submission remains unconfirmed:** a successful GitHub Actions run is not a Kaggle Writeup submission. Author-side Kaggle sign-in, final rendered word count, declarations and explicit Submit action remain necessary before **2026-11-12 23:59 UTC**.
- **Next:** perform a final manuscript claim/word-count audit and prioritize Kaggle submission. Further experiments should not delay submission.

## Study 1e: final manuscript claim audit (2026-11-12 05:xx PKT)

- **Executed:** fetched canonical `public/project/PatchQuestions_Writeup.md` from `main` and checked required sections, references, research claims and whitespace word count. Updated the limitations paragraph in commit `c7a2fa2ac38cebcce58c859f0f87a11ef4d7b34c`.
- **Word count:** 2,483 whitespace-delimited words including title, subtitle, tables and references, below the competition's 3,000-word limit. Kaggle's rendered counter remains unverified.
- **Correction:** replaced misleading broad claim that noisy labels were entirely unevaluated with a tightly scoped description of the independently cross-validated **binary toy** noise audit, including false-rejection tradeoff. It is explicitly separated from the eight-family benchmark and real Gemma/repository repair.
- **Evidence:** [successful Python audit CI](https://github.com/digiinformed-afk/gemma-4-competitions/actions/runs/43116822447); [original frozen-matrix/open-set CI](https://github.com/digiinformed-afk/gemma-4-competitions/actions/runs/43091180332). Neither is a Kaggle submission.
- **Submission blocker:** authenticated Kaggle Writeup creation, eligibility declarations, rendered preview and explicit final Submit remain unverified. No new model experiments should displace submission priority.
- **Next:** confirm actual Kaggle submission status through an authenticated session; if absent, submit the updated 2,483-word manuscript before 2026-11-12 23:59 UTC. Do not claim submitted without a platform receipt.

## Study 1f: submission handoff and source integrity recheck (2026-11-12 05:55 PKT)

- **Executed:** independently fetched the current canonical manuscript, source submission checklist, claim-evidence record and prior ledger from GitHub `main`. Counted **2,483 whitespace-delimited words**, verified required abstract/introduction/methods/results/related-work sections and seven numbered references; manuscript retains explicit no-Gemma-session and no-real-repair caveats. This is a source-text audit, not Kaggle's rendered count.
- **Committed handoff:** [PAPER-SUBMISSION-HANDOFF-2026-11-12.md](PAPER-SUBMISSION-HANDOFF-2026-11-12.md), commit `b2afedfd9e7048231bc8d24e5de072dbd0b12493`. It supplies exact title/subtitle, current manuscript location, required author-side submission steps, evidence boundaries and verified CI links. Existing benchmarks and manuscript are unchanged.
- **Blocked:** Browser/account access was unavailable in this execution; no authenticated Kaggle Writeup status or submission receipt was obtained. **Do not claim submitted.** Deadline is 2026-11-12 23:59 UTC / 2026-11-13 04:59 PKT.
- **Next:** Prioritize actual Kaggle Writeup creation and final Submit under the author's authenticated account; preserve receipt/URL. No additional CPU experiment should delay the submission.
