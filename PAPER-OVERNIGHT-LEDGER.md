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

## Study 1g: independent manuscript-to-artifact numerical consistency audit (2026-11-12 08:xx PKT)

- **Executed:** fetched the canonical manuscript, `summary.json`, `intervention.json`, and `cross_version_summary.json` directly from current GitHub `main`. Independently recalculated the manuscript's headline three-question results from the baseline machine-readable artifact: ordinary random **56.8313%**, random informative **76.3189%**, entropy **85.2708%**, frugal **85.4792%**, frugal-minus-entropy **0.208333 percentage points**. These round to the numbers in the paper.
- **Regex intervention check:** the separate intervention artifact reports original three-label **30.00%** and compound three-label **86.25%**, matching the manuscript. Configuration-family counts sum to **150**. The fetched manuscript contains **2,483 whitespace-delimited words** and **seven numbered references**; its open-set section and real-Gemma-performance disclaimer remain present.
- **Version-control caveat:** `cross_version_summary.json` differs from `summary.json` for some random-policy values (e.g. ordinary random at three questions **56.5805%** vs canonical **56.8313%**). The manuscript correctly uses `summary.json` values. Do **not** silently mix cross-version numbers or interpret their differences as a new intervention effect; they are separately labeled historical runtime results.
- **Status:** this is an independent arithmetic/source-consistency check, **not** a new CPU benchmark execution, prospective validation, Gemma model test, or Kaggle submission. No empirical manuscript claims were changed.
- **Blocker:** connected browser returned “Browser access requires the originating browser context”; authenticated Kaggle submission status, eligibility declarations, platform word counter and final receipt remain unavailable. **Submit the already prepared Writeup before 2026-11-12 23:59 UTC**; this has higher priority than additional experiments.

## Study 1h: submission-critical integrity gate (2026-11-12 08:58 PKT)

- **Executed:** independently fetched current canonical manuscript, summary and regex intervention artifacts from GitHub `main`; recomputed 150 configurations, 18,000 expected score records, 2,483 manuscript whitespace words, seven references, baseline rates, frugal–entropy gap and compound-regex delta. All inspected anchors agree with the manuscript's rounded figures.
- **Committed:** [PAPER-SUBMISSION-INTEGRITY-GATE-2026-11-12.md](PAPER-SUBMISSION-INTEGRITY-GATE-2026-11-12.md), a concise reproducible source-consistency record. This is **not** a new benchmark execution or model experiment; existing research data and manuscript were preserved.
- **Blocker:** authenticated Kaggle browser context unavailable, so final Writeup submission remains unverified. **Next:** final Submit before Nov 12 23:59 UTC and retain receipt. No additional experiment should displace this deadline.

## Submission access recheck — 2026-11-12 10:04 PKT

- **Executed:** fetched the canonical `main` repository index, submission handoff, ledger and canonical `PatchQuestions_Writeup.md` through the connected GitHub repository. Independently counted **2,483 whitespace-separated words** in the fetched manuscript. The canonical title/subtitle and explicit limits on simulated versus real-agent claims remain in place.
- **Kaggle rules:** attempted to read the official [Paper Track rules](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/rules) directly; the public page returned no machine-readable rules text in this environment. The previously recorded 3,000-word limit and deadline were not independently revalidated from rendered Kaggle rules in this run.
- **Submission attempt blocker:** attempted to inspect connected browser tabs, but the browser connector returned `Browser access requires the originating browser context`. No authenticated Kaggle account, submission form, receipt, or submitted Writeup status was accessible. **No submission was made or verified.**
- **Experiment status:** no new experiment run; previous toy simulation and frozen benchmark evidence unchanged. No GPU or Kaggle compute used.
- **Next action (critical):** obtain an authenticated Kaggle session in the originating connected browser context, verify official form/rules and rendered word count, perform final Writeup submission before 2026-11-12 23:59 UTC, and retain its confirmation URL/timestamp. Avoid additional experiments until this is done.

## Submission gate recheck — 2026-11-12 10:56 PKT

- **Reviewed current canonical sources:** fetched the manuscript, submission handoff and ledger from GitHub `main`. The manuscript continues to distinguish finite eight-family benchmark outcomes, separate binary toy-noise findings, and *no measured Gemma-agent improvement*.
- **Public rules access:** official Kaggle Paper Track rules URL was opened, but its page yielded no machine-readable lines; platform-specific eligibility, formatting and live submission status therefore remain unverified in this run.
- **Authenticated access attempted:** connected browser tab listing returned `Browser access requires the originating browser context`. The GitHub repository code search for `kaggle.com/writeups` returned zero matches with `incomplete_results=true`; this is **not proof** that no Writeup exists.
- **Execution:** source review and access checks only. No new CPU experiment, GPU/Kaggle compute, model evaluation or submission occurred. Existing baseline files and manuscript were not modified.
- **Critical next action:** author must open the authenticated Kaggle Paper Track Writeup form, verify live rules and rendered word count, press final Submit by **2026-11-12 23:59 UTC**, and preserve the submitted URL/receipt. Until then status is **unconfirmed**.

## Official Kaggle overview requirements independently verified — 2026-11-12 12:02 PKT

- **Source checked:** https://www.kaggle.com/competitions/gemma-4-developer-agent-paper (public official competition overview, retrieved this run). This is a stronger source than earlier inaccessible `/rules` page; do not represent it as authenticated account verification.
- **Official explicit requirements:** original, unpublished research; Kaggle **Writeup** containing title, subtitle, abstract, introduction, research methods/experiments, related work and citations; **3,000-word maximum**. Public notebook and public project link are **optional**. A public arXiv-ready PDF may alternatively be linked through Public Project Link. Main competition participation is not required for the Paper Track.
- **Submission action:** overview explicitly says create a New Writeup, save it, then click **Submit** in the upper right. Drafts/unsubmitted Writeups do **not** count. Deadline **2026-11-12 23:59 UTC / 2026-11-13 04:59 PKT**.
- **Repository review:** canonical `public/project/PatchQuestions_Writeup.md` and handoff fetched via connected GitHub; manuscript remains 2,483 words by prior independent source audit, with clear toy versus eight-family versus untested real-Gemma boundaries. This run did **not** execute an additional benchmark, and does not assert a new word-count measurement or authenticated Kaggle submission.
- **Open critical blocker:** No authenticated Kaggle Writeup submission confirmation/URL available to this run. Official public rules are now independently verified, but final account-side eligibility, rendered word count and Submit receipt remain unverified.
- **Priority:** immediately submit canonical Writeup, confirm public submitted status, save receipt. Do not delay for optional notebook, GPU, new experiments or cosmetic changes.


## Submission access and source preflight (2026-11-12 14:58 PKT)

- **EXECUTED:** Retrieved current canonical manuscript from GitHub default branch (blob `62dba99c6b7388b58464a51619fa2cf4cf534861`) and final submission gate (blob `315e7226c88bbb651c0ba77c8d7b524d300b067e`). Manuscript still explicitly separates finite simulated API-contract outcomes from actual Gemma-agent or repository-repair performance.
- **RULES ACCESS LIMITATION:** Reopened https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/rules ; public page returned no readable rules lines. Prior recorded requirements are not independently revalidated in this execution.
- **AUTHENTICATION BLOCKER:** Connected browser list-tabs failed with `Browser access requires the originating browser context`. Consequently **no Kaggle Writeup submission or receipt was observed or claimed**.
- **LOCAL COMPUTE BLOCKER:** Attempted shallow repository clone in the local container; DNS resolution of github.com failed. No new CPU experiment was executed; existing CI evidence remains the only verified execution for the prior experiments. No GPU or Kaggle compute was used.
- **CHANGE SCOPE:** Ledger-only operational update; no benchmark data, code, or manuscript altered. Next priority is authenticated final Submit and timestamped confirmation before 2026-11-12 23:59 UTC.


## Submission gate recheck — 2026-11-12 15:59 PKT

- **EXECUTED:** Fetched canonical manuscript from GitHub default branch (blob `62dba99c6b7388b58464a51619fa2cf4cf534861`); independently recomputed **2,483 whitespace-separated words**, 11 Markdown headings and nine external references/CI links. Required Abstract, Introduction, Methods, Results, Related work and References remain present. Explicit caveats continue to say no learned-model session, no real-world repair evaluation and no demonstrated noise-tolerant repair.
- **OFFICIAL PAGE:** Reopened https://www.kaggle.com/competitions/gemma-4-developer-agent-paper on 2026-11-12; public page returned no machine-readable lines. Previously documented competition requirements remain the working submission checklist, not newly verified live account-side requirements.
- **BLOCKED:** Authenticated browser tab listing again returned `Browser access requires the originating browser context`. Therefore no final Kaggle Writeup Submit action, submission URL, rendered word count or receipt could be verified. **Submission status remains UNCONFIRMED.**
- **NOT RUN:** No new CPU/GPU/Kaggle experiment, no real Gemma-agent test, and no new numerical research claim. Baselines and manuscript unchanged. The 85% benchmark results are controlled simulated API-contract findings, **not** real Gemma-agent accuracy.
- **NEXT (deadline-critical):** Finish authenticated Kaggle Writeup Submit before 2026-11-12 23:59 UTC (2026-11-13 04:59 PKT), and record submitted URL and timestamp. Do not delay for optional research work.

## Deadline cross-check and final submission blocker — 2026-11-12 21:56 PKT

- **EXECUTED:** Re-fetched canonical manuscript from GitHub default branch (blob `62dba99c6b7388b58464a51619fa2cf4cf534861`). No manuscript or benchmark data were modified.
- **Independent deadline corroboration:** The official parent competition's [prizes/timeline page](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview/prizes) explicitly identifies **2026-11-12** as the optional Research Paper deadline and says the paper prize submissions must be made by **November 12, 2026 at 11:59 PM UTC**. The [separate Paper Track public page](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview) exists, but its relative 'time to close' display is not an authenticated submission receipt and should not supersede the explicit date. Deadline remains **2026-11-13 04:59 PKT**.
- **Authentication attempt:** connected browser `list_tabs` failed: `Browser access requires the originating browser context`. No access to the account's Writeup draft, final Submit button or receipt. **Submission is unconfirmed.**
- **Execution classification:** GitHub source inspection and public-rule/deadline cross-check only. **No new CPU benchmark, no GPU/Kaggle compute, no model-in-the-loop run, and no real Gemma-agent performance result.** Prior frozen-matrix benchmark and noisy-oracle binary toy results retain their separate scopes.
- **Next priority:** Complete the Kaggle Writeup's final **Submit** action before the explicit deadline, capture the submitted Writeup URL and timestamp, and verify the platform status. Do not delay for further experiments.
