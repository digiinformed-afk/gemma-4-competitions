# PatchQuestions: adversarial research review

**Review date:** 7 November 2026. **Project:** Gemma 4 Paper Track.

This review distinguishes **observed** executions, **deductions** from the specified model, and **proposed** experiments. References to `paper/` and `context/` identify unchanged files in the attached package; `reviewer_checks/` contains new review evidence. No model pilot, human study, repository-repair evaluation or submission was performed.

## 1. Verdict

**Recommend submitting a carefully bounded resource paper after the claim and reporting edits below. Do not position it as a new general repair algorithm.**

The defensible contribution is a small executable resource for studying adaptive question selection when candidate behaviors are already known, labels are perfect, and a correct configuration is present. Exhaustive target rotation, exact randomized baselines, frozen matrices and an auditable reference solver make this component unusually inspectable. I reproduced its reference results under CPython 3.12.14 and independently checked the central calculations.

The strongest rejection argument is scientific scope: familiar active identification is instantiated on eight curated API families, while patch generation, oracle construction, real repairs and learned-agent behavior are unevaluated. Its most striking intervention also increases the information carried by each answer.

The strongest empirical story is **a reproducible diagnostic resource with a strong simple baseline**. My crossed check finds that entropy also reaches 86.25% on the compound regex pool at three questions. Tree search adds little at that budget. A bounded Gemma pilot could improve relevance, but its absence does not by itself invalidate the resource or establish formal ineligibility.

## 2. Evidence audit

**Files inspected.** `START_HERE.md`; `FILE_MANIFEST.json`; the manuscript, README, notebook source and stored outputs; all seven Python modules (`benchmark`, `analyze`, `intervention`, `verify`, `replay`, `export_cases`, `cognitive_probe`); reference scores and JSON results; frozen matrices; the historical 3.13.5 summary and bundled 3.15.2 audit; `RESEARCH-REVIEW.md`, `EXPERIMENT-PROTOCOL.md`, `REQUIREMENTS-COVERAGE.md`; the cognitive-study and research-evidence notes; relevant research-library records and program-plan passages. The promotional PNG was not needed to establish the research claims.

All **38 payload hashes and byte counts** match the manifest. Input ZIP SHA-256: `6f2e3a897fa154177446f1c791c3cc20922b22c97d294ddd3a39c0a234e39e49`.

**Actual execution.** Fresh directory: `/workspace/scratch/90877478f44e/review_work/run_cpython_3_12_14`. Runtime: CPython **3.12.14**, Linux x86_64, Clang 22.1.3. `python` below resolves to `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python`.

```sh
python -B benchmark.py > summary.json
python -B analyze.py > audit.json
python -B intervention.py > intervention.json
python -B verify.py > verify.txt
python -B export_cases.py
# After preserving the new export and placing the original frozen archive beside the runner:
python -B cognitive_probe.py --check
```

All exited successfully. Wall times were respectively **4.906, 1.205, 2.774, 0.994, 0.274 and 0.216 seconds**. Exact argument vectors and stderr files are retained in `review_execution_log.json`.

- `scores.csv`—all **18,000 rows**—and `summary.json`, `audit.json`, `intervention.json` match reference bytes exactly.
- All **40 freshly exported matrix records** match the decompressed reference JSON. Gzip container bytes need not match because headers contain time/name metadata.
- The 750 paired entropy masking checks pass. This is an algorithmic invariance control, not a Gemma result.
- All **six** notebook-embedded modules match standalone files. The notebook was inspected; it was **not executed in a Jupyter kernel**. Its standalone computational equivalents were executed.

Additional commands, run from `/workspace/scratch/90877478f44e/review_work`:

```sh
python -B reviewer_audit.py > reviewer_audit.stdout.txt 2> reviewer_audit.stderr.txt
python -B protocol_audit.py > protocol_audit.stdout.txt 2> protocol_audit.stderr.txt
```

These produced: 24,000 independently checked random-policy metrics; exhaustive tree checks on 4,096 binary matrices at four budgets; minimal objective counterexamples; policy × probe-pool results; descriptive sensitivity and redundancy analyses; matched pilot baselines; timing diagnostics; and a protocol scoring-boundary example. `reviewer_audit.py` took **26.010 seconds**. Reference files were not modified.

**Runtime separation.** This review supplies a fresh same-version 3.12.14 reproduction. The package's 3.13.5 results remain historical, and its 3.15.2 results remain someone else's separate rerun. I did not execute either runtime. At budget three, their random-policy summaries differ from the 3.12.14 reference by approximately −0.251 and −0.197 percentage points, respectively; the stored deterministic entropy/tree aggregates match. These results must retain their runtime labels.

**Competition verification.** I read the live official overview and complete paper rules on 7 November, in addition to indexed official sources. The deadline remains **12 November 2026, 23:59 UTC / 13 November, 04:59 PKT**. The report limit is **3,000 words**; five criteria are equally weighted: Novelty, Quality, Relevance, Verifiability and Clarity. Related unpublished research and resource entries are allowed; main-track participation is optional. Fine-tuning and graph/embedding use are not universal paper requirements. A Writeup must actually be submitted. The live account page shows a draft ready for submission. I made no submission or account changes. [Official overview](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview); [official rules](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/rules).

**Unverified/access boundaries.** The full official HARNESS_README, actual sample submission, exact model terms, active compute balance, model availability, personal eligibility and publication/ownership status were not verified. The historical 200 Colab units are not a current balance. The literature review below is targeted primary-source verification, not an exhaustive novelty search or independent reproduction of other papers.

## 3. Answers to all 28 questions

### A. Contribution and positioning

**1. What remains new?**

**Verdict:** The resource and its controlled decomposition may be useful; interactive filtering, behavioral grouping, active querying and decision-tree identification are established. The narrow claim is: *an executable finite API-contract resource with exhaustive target rotation, exact policy expectations, frozen runtime-specific behavior and separate policy/probe-pool interventions*. Do not claim the first clarification benchmark or a new repair algorithm.

**Evidence:** Manuscript Related work and `benchmark.evaluate`; InPaFer Section 2, LEARN2FIX's active oracle learning, xTestCluster Sections 2.2–2.3, CodeMonkeys Section 2.3, and the clarification benchmarks compared in Section 5 below.

**Strongest counterargument:** Packaging well-known identification into small standard-library configuration tables might be a teaching exercise without a research question that changes practice. That is a stronger rejection than alleging the code is wrong.

**Smallest decisive check:** Add the direct overlap table and demonstrate one useful diagnosis a user could not obtain from an aggregate repair score—here, pool insufficiency and the crossed regex result. A frozen model pilot would establish usability, not unique novelty.

**Severity:** Material novelty weakness; a submission blocker only for claims of algorithmic or interactive-filtering invention.

**2. Does the visible behavior matrix measure a meaningful bottleneck?**

**Verdict:** It isolates **which trusted observation to buy next**, conditional on having candidate implementations and executing them successfully. It is a legitimate component task, but it measures neither autonomous debugging nor discovering that clarification is necessary.

**Evidence:** `benchmark.py:50–64` precomputes query and hidden matrices; `score_state` selects from the former. `replay.play` exposes the entire query matrix. Correct targets come from the candidate configurations.

**Strongest counterargument:** Matrix construction and trustworthy expected-output acquisition may dominate real repair cost. Giving both away could isolate a component whose optimization scarcely affects the full system.

**Smallest decisive check:** Explicitly diagram or state the boundary in the manuscript, and record matrix construction, selection and label-acquisition costs separately. A small real-patch pool would test whether the same matrix ambiguity occurs naturally.

**Severity:** Weakens external relevance; reasonable scope for a resource if stated plainly. It blocks claims of measured end-to-end repair benefit.

**3. Can it compete without a Gemma or repository experiment?**

**Verdict:** Distinguish three issues. **Formal scope:** the live overview permits related unpublished research and resources; it does not universally require those experiments. **Scientific strength:** the resource can be internally sound without them. **Award competitiveness:** its model and software-engineering relevance is materially less demonstrated. No award probability follows from this review.

**Evidence:** Official overview's Description, Submission Topics and Best New Resource sections; manuscript Reproduction and limitations; `EXPERIMENT-PROTOCOL.md` identifies the pilot as proposed.

**Strongest counterargument:** Eligibility is a low bar; a resource with no demonstrated user, model or repair application may be weak on both Quality and Relevance.

**Smallest decisive check:** Complete one checkpoint's frozen 32-session feasibility pilot with matched baselines and failure-inclusive scoring, if access is already practical. Real-repository repairs would be stronger evidence but carry substantially greater setup risk.

**Severity:** Competitive weakness, not an automatic eligibility failure. Personal eligibility and rights remain separate checks.

**4. Is the coding-agent title supported?**

**Verdict:** It is defensible as motivation but invites an interpretation the experiments do not support. Prefer **“PatchQuestions: An Executable Benchmark for Budgeted API-Contract Disambiguation.”**

**Evidence:** Manuscript title and abstract contrast with its explicit statement that no Gemma or repository evaluation has occurred; `replay.py` is an interface, not an evaluated agent.

**Strongest counterargument:** A research title can ask a question about a future application without asserting completed integration. The present title is not itself a fabricated result.

**Smallest decisive check:** Revise the title and first abstract sentence to name the measured object: fixed candidate configurations, a visible behavior matrix and a trusted label budget. Keep coding-agent relevance in the motivation.

**Severity:** Clarity and expectation-setting issue; easy pre-submission edit.

### B. Mathematics and implementation

**5. Derive the leaf-count objective, including its actual failure conditions.**

**Verdict/deduction:** For (N) uniformly likely targets and a deterministic query tree, let terminal leaf (S) contain (k) consistent candidates. Uniform final selection contributes

\[
P(T\in S)P(\widehat T=T\mid T\in S)=\frac{k}{N}\frac{1}{k}=\frac1N.
\]

Thus (L) nonempty leaves give identity recovery (L/N).

Two premises in the question need refinement. **Duplicate behaviors do not break this identity proof:** they create identities the allowed queries cannot separate. **Nonuniform final picking does not necessarily break it either:** for any target-blind distribution (r_S(i)) supported on (S), the contribution is \(\sum_{i\in S}r_S(i)/N=1/N\). Uniform picking is sufficient, not necessary.

With nonuniform prior (p_i), contribution becomes \(\sum_{i\in S}p_i r_S(i)\): uniform picking gives (p(S)/|S|), while a best identity pick gives \(\max_{i\in S}p_i\). Leaf count alone no longer determines the objective. Missing targets, mistaken labels, choosing outside the consistent leaf, or additional target-revealing information also invalidate the stated argument. Behavioral agreement is a different reward even when the identity proof holds.

**Evidence:** `benchmark.tree`, `score_state` terminal rule, and manuscript Methods.

**Strongest counterargument:** Uniform configuration weights are convenient rather than estimated repair priors.

**Smallest decisive check:** State the exact assumptions and add one unequal-prior example; use prior-weighted utilities if making claims under different priors.

**Severity:** Current identity derivation is sound. Broader optimality claims require narrowing.

**6. Smallest explicit identity/behavior mismatch.**

**Verdict:** Three candidates, two query columns, one held-out input and budget one suffice when the identity objective ties:

| Candidate | Query A | Query B | Held-out output |
|---|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 2 | 0 | 1 | 1 |

Both queries create two leaves, hence **2/3 identity recovery**. Query A yields **2/3 held-out agreement**; Query B yields **1** because each leaf is behaviorally homogeneous. With A first, the implementation chooses A. Two candidates cannot produce this failure: an informative query identifies the target, and all uninformative queries leave the same survivor set.

For a **strict objective conflict**, use four candidates with (A=(0,1,0,2)), (B=(0,0,1,1)), and held-out outputs (H=(0,0,1,1)). A creates three leaves and scores **3/4** behaviorally; B creates two and scores **1**. More identity leaves can strictly hurt the endpoint.

**Evidence:** Both examples were executed through the original `evaluate`; see `objective_counterexamples.json`. The manuscript already explicitly distinguishes the objectives in Methods.

**Strongest counterargument:** This is not evidence of incorrect implementation or concealed metric mismatch. The draft discloses it, and the observed tree results remain valid.

**Smallest decisive check:** Add the three-row example or a short explanatory sentence; call the solver *identity-optimal under the stated model*, never held-out-optimal. Hidden behavioral classes may be used only in evaluator diagnostics.

**Severity:** Blocks an optimal-held-out-accuracy claim; otherwise a disclosed limitation requiring clear terminology.

**7. Does frugal tree minimize questions among identity-optimal trees?**

**Verdict:** Yes, under this deterministic, uniform-target, unit-question-cost model. At depth zero, the pair is ((L,C)=(1,0)). An informative query with children (S_a) has

\[
L=\sum_a L(S_a,d-1),\qquad C=|S|+\sum_a C(S_a,d-1).
\]

Choose the largest (L), then the smallest (C). Induction over depth establishes the lexicographic optimum; expected questions at the root are (C/N). Children independently maximizing leaves is valid because their leaf counts add, and minimizing child costs among those optima minimizes the parent cost.

**Evidence:** `benchmark.py:70–83`; base case `(1,0,None)`; exact integer leaf/cost comparisons; first-pool-order residual ties; cached state `(ids, depth, frugal)`. Previously asked queries are constant on every descendant survivor set, so searching all columns cannot reuse them informatively. `score_state` removes asked columns for other policies.

My independent explicit enumeration passed **all 4,096 binary 4×3 matrices at budgets 0–3**, including early stopping and tied objectives. The bundled verifier additionally checks real-family depth-two leaf optima.

**Strongest counterargument:** This minimizes labels, not human effort, execution cost or behavior loss. Larger instances may make exact search impractical.

**Smallest decisive check:** Retain the proof and independent fixtures; no repair to this recurrence is indicated by the evidence.

**Severity:** No demonstrated implementation defect within scope.

**8. Is all-available-queries an upper bound?**

**Verdict:** The answer is conditional, and the archive supports a stronger statement than a generic warning suggests.

For uniform targets and uniform selection within a terminal set (S), its behavioral contribution is

\[
\frac1N\frac{\sum_g n_{S,g}^2}{|S|},
\]

where (n_{S,g}) counts a held-out behavior class. Revealing more queries refines the partition; convexity of squared class probabilities makes the target-averaged score nondecreasing. The all-query score therefore bounds policies with that final-selection rule and information model.

It is **not universally optimal across selectors**. Three candidates indistinguishable on every query, with held-out labels A,A,B, give uniform selection **5/9**. Always picking the first A gives **2/3**, without accessing the hidden target. Knowing which class is largest would require legitimate side information or an evaluator-only diagnostic.

For the **actual 40 frozen matrices**, I also computed the evaluator-only optimum \(N^{-1}\sum_S\max_g n_{S,g}\). It equals the uniform all-query result in every case. Thus here the reference is also an optimal bound under a uniform target prior and no target information beyond the query transcript. This coincidence need not survive new pools, priors or families.

**Evidence:** `analyze.audit`, `effects_redundancy_sensitivity.json`; manuscript's cautious “reference” wording is appropriate. The code's `ceiling` key is underspecified.

**Strongest counterargument:** A selector with a different valid target prior or additional task requirements operates under a different information model.

**Smallest decisive check:** Publish both formulas/diagnostics and use **“all-query uniform-selection reference”** in general descriptions.

**Severity:** Terminology/generalization issue, not a falsified bound for these frozen conditions.

**9. Are the random expectations exact?**

**Verdict:** Yes, up to floating-point representation. `random` chooses uniformly from unused columns and spends the full budget even after ambiguity disappears. `random_split` chooses uniformly among currently informative unused columns and stops when none remain. Its branch probabilities depend on the accumulated answers; simply averaging all terminating paths equally would be wrong, but the implementation does not do that.

**Evidence:** `score_state` lines 89–117 averages children at each conditional choice, scores each target separately, then macro-averages families. My independent checker used uniform unordered subsets for ordinary random and explicit weighted paths with `Fraction` arithmetic for random-informative. Across **6,000 episode/policy/budget cases and 24,000 metric comparisons**, the maximum discrepancy was **1.78×10⁻¹⁵**. It enumerated 1,015,896 terminal subsets/paths.

**Strongest counterargument:** Exact expectations eliminate sampling error in these policies, not uncertainty about representativeness or oracle realism.

**Smallest decisive check:** Already performed; retain the independent checker and document the different stopping rules.

**Severity:** No demonstrated error. Do not describe these exact finite expectations as evidence of population-level certainty.

**10. Do redundant configurations distort difficulty?**

**Verdict:** They can change the effective prior and therefore entropy, random selection, identity recovery and behavioral agreement. I found **36 hex configurations but 30 joint query/held-out behavior classes**. Every other family is joint-distinct on its combined finite suite. This is an actual multiplicity issue, not proof of distorted conclusions.

**Evidence:** `families()['hex_format']`; `effects_redundancy_sensitivity.json`. Query-only class counts can be much smaller: regex has 2–8 classes across splits despite 16 configurations.

**Strongest counterargument:** Multiplicity is legitimate if configuration frequency is the intended prior; real generators can also emit behaviorally duplicate patches.

**Smallest decisive check:** Report class counts and one prespecified sensitivity analysis. Query-only deduplication loses distinctions that held-out inputs can expose and may remove the correct behavior; treating a query class as one equally likely target changes the problem. Held-out-only deduplication merges query-distinct rows and leaks grading structure if used by the policy. Joint deduplication removes finite-suite redundancy but also uses held-out data, so label it evaluator-only. Alternatively, keep multiplicity weights when compressing rows to preserve the original prior.

**Severity:** Prior/parameterization sensitivity; not fatal if the configuration-uniform experiment is explicit.

### C. Results and interpretation

**11. Does the 0.21-point tree margin justify search?**

**Verdict:** It does not establish a practically important accuracy advantage. At three questions, entropy gives **85.270833%**, frugal **85.479167%**: **0.208333 percentage points**, entirely from CSV. Dropping CSV makes the margin zero. The useful story is the resource, a strong simple baseline and diagnosing inadequate probe pools.

**Evidence:** Reference scores, `effects_redundancy_sensitivity.json`, manuscript Results. The new crossed probe check also gives entropy the full 86.25% regex result at budget three.

**Strongest counterargument:** Exact search is tiny on this resource, so simplicity does not automatically imply a meaningful measured CPU saving. At budget two, the original aggregate tree advantage is larger, and compound regex shows a 6.25-point tree advantage.

**Smallest decisive check:** Retain budget-specific comparisons and report cost. My whole-sweep timing diagnostics do not demonstrate a material tree penalty at the current scale; a larger-candidate scaling claim would need separate measurements.

**Severity:** Weakens a tree-breakthrough narrative, strengthens a baseline/resource narrative. It does not invalidate the numerical result.

**12. Recompute question savings and costs.**

**Observed, family-macro means at maximum budget three:**

| Policy | Full held-out agreement | Mean questions |
|---|---:|---:|
| Random | 56.831288% | 3.000000 |
| Random informative | 76.318877% | 2.299580 |
| Most outcomes | 84.812500% | 1.877708 |
| Entropy | 85.270833% | 1.881979 |
| Ordinary tree | 85.479167% | 2.265625 |
| Frugal tree | 85.479167% | 1.864479 |

Random-informative improves over ordinary random by **19.487590 points**. Frugal improves over random-informative by **9.160289 points**, and over entropy by **0.208333 points**.

The claimed saving is \((2.265625-1.864479)/2.265625=17.705747\%\), or **0.401146 questions per episode**. Relative to entropy it is only \((1.881979-1.864479)/1.881979=0.929872\%\), or **0.017500 questions**. The denominator must remain attached to the 17.7% statement.

**Evidence:** `effects_redundancy_sensitivity.json`. Three timing trials of the actual code restricted to budget three gave median **0.226 s entropy, 0.252 s ordinary tree, 0.225 s frugal** for the entire 750-target sweep, including generating 40 matrices. Trials varied and order was not randomized; these are coarse reproduction costs, not isolated policy timing or a stable speed ranking.

**Strongest counterargument:** The manuscript already mentions entropy's similar question usage; its body is not hiding that comparison. The abstract emphasizes the weaker tree comparator more strongly.

**Smallest decisive check:** Add entropy's question usage to the abstract or remove the standalone saving percentage. Treat labels, answer size, CPU, model tokens and human minutes separately.

**Severity:** Presentation fix, not arithmetic correction.

**13. What is the independent unit of evidence?**

**Verdict:** The closest unit for cross-task sensitivity is the **API family**, of which there are only eight curated examples—not a random sample of eight real bugs. Five splits reuse input universes, and exhaustive targets reuse the same matrices. There are 750 conditions and 18,000 score rows, not 750 independent bugs or 18,000 trials.

**Evidence:** `run`, `summarize`, manuscript Benchmark; the new leave-one-family-out analysis. Tree versus entropy ranges from **0 to 0.238095 points** after dropping one family. Tree versus random-informative remains **5.434686–10.468902 points**.

**Strongest counterargument:** The finite resource is fully enumerated, so its exact average needs no sampling confidence interval. It is a useful descriptive result even without population inference.

**Smallest decisive check:** Present per-family and per-split results plus leave-one-family-out sensitivity. If bootstrapping families, label the result a descriptive resampling exercise whose external interpretation assumes exchangeable families; eight handpicked families do not justify that assumption automatically.

**Severity:** Blocks pseudoreplicated significance or real-bug generalization claims; the draft already avoids the most serious version of this error.

**14. Which sensitivity checks could overturn the conclusion?**

**Verdict:** The broad resource contribution survives many parameter changes; universal policy ranking and probe-design generality have not been established.

| Priority | Check | What it could overturn | Effort |
|---|---|---|---|
| 1 | Fresh families; matched answer capacity | General usefulness of the probe-design result | Moderate |
| 2 | Candidate multiplicity and nonuniform target priors | Leaf-count optimality assumptions and rankings | Low–moderate |
| 3 | Query-pool sizes 8, 16, full; frozen new splits | Apparent ceiling and entropy/tree gap | Low |
| 4 | Budgets beyond the existing 0–3; answer-cost budgets | Budget-specific policy claims | Low–moderate |
| 5 | Candidate subsets/counts, preserving the target | Difficulty and exact-search scaling | Low–moderate |
| 6 | Family weighting/leave-one-out | Aggregate headline robustness | Very low; partly completed |

**Evidence:** The crossed probe result changes regex far more than the original policy change. Simple target weighting instead of family weighting gives **87.6000% entropy versus 87.8667% tree**; it does not measure a real-world prior. Leaving out CSV removes the three-question advantage.

**Strongest counterargument:** A benchmark need not exhaust every sensitivity axis before release. Expanding all axes now risks replacing a coherent small paper with an underexplained grid.

**Smallest decisive check:** Freeze one sensitivity relevant to the retained main claim. Under unequal priors, distinguish reweighting the existing policy's outcomes from implementing a genuinely prior-aware policy.

**Severity:** Limits generalization; do not treat the full sensitivity grid as a pre-submission requirement.

**15. Are the equivalence criteria appropriate?**

**Verdict:** They are appropriate for the explicitly defined wrapper outputs, but not for general Python program equivalence. Ordered CSV fields, query-pair lists and wrapping results often legitimately require order. Comparing JSON wire strings makes whitespace and escaping distinctions intentional, even when decoded values agree. Regex span lists describe positions, not capture groups or the complete behavior of a regex API.

**Evidence:** `outcome` at `benchmark.py:12–16`, each wrapper in `families`, and frozen outputs. Exception class equality erases messages, error positions and other exception attributes. JSON serialization merges tuples with lists and canonicalizes dictionary order; unsupported values can fail serialization. A serialization `ValueError` is caught in the same block as a function error. These are general extension risks, not observed corruptions of the present supported wrappers.

**Strongest counterargument:** The benchmark defines a concrete observable contract; requiring richer equivalence without an application need would change that contract rather than repair a bug.

**Smallest decisive check:** Document the observation schema and use typed return/error envelopes before extending to arbitrary functions. Keep runtime-pinned regeneration and frozen replay distinct. The supplied cross-version Base64 changes demonstrate why the exact interpreter matters.

**Severity:** Limits semantic and cross-runtime claims; not a failure of current finite-suite scoring.

### D. Probe-design evidence

**16. Is 30% to 86.25% evidence of better query design or a richer channel?**

**Verdict:** Both. It demonstrates improved **information acquisition under a per-call label budget**, achieved in part by requesting richer answers. It does not demonstrate a comparable reduction in human work.

**Evidence:** `intervention.single`, `intervention.compound`; new `crossed_probe_results.json`. Across all 56 original regex inputs, a query has at most **two** candidate outcomes and at most **one bit** of initial answer entropy. Compound probes have up to **eight** outcomes and **2.548795 bits**. Average input lengths are about **6.02 characters** in the original universe, **5** for single-flag replacements and **19** for compound replacements. Mean serialized answers are about **16.60, 17 and 22.06 characters**, respectively; compound answers reach 57. These compare vocabularies, not the distributions of selected transcripts, and are character counts rather than tokenizer measurements.

**Strongest counterargument:** Designing a question that reveals several facts is a legitimate benefit when the oracle can answer it cheaply. Richer answers do not make the experiment invalid.

**Smallest decisive check:** Report answer cardinality/entropy and selected-transcript input/output lengths next to question counts. A matched-output-capacity arm or timed annotations would address the human-effort claim; CPU execution time alone would not.

**Severity:** Blocks “saves human time” or equal-effort interpretations, not the measured label-count improvement.

**17. How post-hoc is the intervention and transfer suite?**

**Verdict:** Clearly exploratory. The replacement probes were designed after diagnosing the regex failure, and the transfer suite was fixed after that diagnostic analysis. Input disjointness establishes that exact strings do not overlap; it does not make the test prospectively independent or establish transfer across APIs.

**Evidence:** Manuscript follow-up section; `intervention.py` docstring and `transfer_suite` comment; `RESEARCH-REVIEW.md`. Assertions prevent replacement/original overlap and transfer/query overlap. The archive contains no development history sufficient to reconstruct how many discarded probe designs or scoring inspections preceded the final choice.

**Strongest counterargument:** Post-hoc mechanism discovery is legitimate, and the manuscript labels it exploratory. The separate suite is still useful against simple exact-input memorization.

**Smallest decisive check:** Freeze the design rule, query budget, output format and analysis before scoring one fresh family. For example, use a separately generated `str.split` configuration family; freeze both probe pools before generating a sealed scoring suite. Keep a timestamped manifest and report every prespecified arm. Matching answer capacity is necessary for an equal-effort interpretation.

**Severity:** Weakens confirmatory/general-transfer claims. It does not invalidate the reported constructed example.

**18. How does entropy perform on the improved pools?**

**Observed answer:** I ran the crossed comparison. At three questions, entropy matches frugal on **both** the original held-out and transfer suites:

| Regex pool | Entropy, budget 3 | Frugal, budget 3 | Mean questions, both |
|---|---:|---:|---:|
| Original | 30.00% | 30.00% | 2.1000 |
| Four single-flag replacements | 50.00% | 50.00% | 3.0000 |
| Four compound replacements | 86.25% | 86.25% | 2.0625 |

At **budget two** on compound probes, entropy reaches **68.75% using 1.625 questions**, versus frugal **75.00% using 1.750**. Policy choice can therefore matter at another budget.

**Evidence:** `crossed_probe_results.json` and all 11,520 intervention score rows in `crossed_probe_rows.csv`; produced using the unchanged `evaluate` function. The original `intervention.study` computed all policies but reported only frugal.

**Strongest counterargument:** The crossed table removes the policy/pool reporting ambiguity, but it does not remove richer-answer, post-hoc or single-family confounds.

**Smallest decisive check:** Completed. Add this table and retain the budget-two result to avoid claiming probe vocabulary always dominates search.

**Severity:** Important missing comparison now resolved by review execution. Stronger support for the resource/simple-baseline story.

**19. What happens with no correct candidate, noise or abstention?**

**Verdict:** Exact elimination is brittle outside the declared realizable, perfect-oracle setting. One wrong but plausible answer can remove the target while leaving a convincing wrong singleton. An impossible answer can eliminate every candidate. A missing correct behavior can remain undetected if available queries fail to expose it. Abstention has no defined outcome in the current protocol.

**Evidence:** `score_state` follows the partition containing the known target; the interactive runners return only exact target outputs. There is no noisy-answer model, empty-survivor policy or abstention action.

**Strongest counterargument:** This is an acknowledged scope choice, not a discovered failure of a robustness claim the manuscript makes.

**Smallest decisive experiment:** On frozen episodes with an informative first query, replace that answer with each other available outcome in turn, weighting alternatives by a frozen rule. Keep the three-question budget. Report target elimination, empty survivors, wrong singletons, final agreement and failure/abstention rate; do not drop contradictory episodes. This permits a narrow statement about sensitivity to **one label error**, not real-world noise tolerance. A later missing-candidate check must remove every behaviorally correct candidate, not just a duplicate identity.

**Severity:** Future work for the bounded resource; a blocker for robust-deployment claims. This experiment is not needed to demonstrate that perfect labels are an assumption.

### E. Proposed model pilot

**20. Is the 16-pair pilot adequate?**

**Verdict:** Adequate for feasibility, protocol/error analysis and descriptive named/masked comparisons only. Targets 0 and 1 are the first two Cartesian-product configurations: they vary the final axis while earlier axes stay at their first settings. They are not a representative sample of all contracts.

**Evidence:** `EXPERIMENT-PROTOCOL.md:13–27`, `families`, `cognitive_probe.py:42–47`, `matched_pilot_baselines.json`. All five 16-candidate families place those targets in displayed rows **13 and 9** under the shared split-19 permutation. My matched entropy/frugal baseline is **87.5%**, above the full-benchmark average, confirming that aggregate baselines cannot be substituted.

**Strongest counterargument:** Matching row order within a pair is good experimental control. Reused row positions do not themselves reveal a target to a model with fresh context and no sample-manifest access.

**Smallest decisive check:** Retain feasibility wording and conceal the manifest. If no scored session has begun, freeze family-specific secret row permutations and a balanced random target selection before inference; otherwise do not quietly change the sample after outcomes. Report the old sample as a convenience sample if retained.

**Severity:** Limits inferential scope; not a reason to reject a clearly labeled feasibility pilot.

**21. Does masking isolate semantic knowledge?**

**Verdict:** No. It preserves within-column equality partitions while changing input identity, output semantics, token count, escaping, readability and context length. It also erases cross-column value equality and other semantic relations. The invariance check proves equivalence for equality-based entropy, not equal difficulty for a language model.

**Evidence:** `mask` assigns `v0`, `v1`, etc. by first appearance **within each column**; `run` replaces named inputs with indices and emits serialized outputs as strings. This makes the first row all `v0`, a presentation convention that can attract positional bias. Row count and partition structure can still fingerprint a family.

**Strongest counterargument:** Equality-preserving masking remains useful for testing whether a model can operate on abstract partitions; removing every presentation difference would defeat that intervention.

**Smallest decisive check:** Log actual tokenizer counts, truncation and failures; use fresh sessions and a frozen random label renaming/row-permutation diagnostic if time allows. A named advantage supports sensitivity to the representation bundle, not specifically semantic knowledge. A successful tie supports task-specific invariance; a failing tie establishes no useful reasoning ability. Neither identifies a “cognitive core.”

**Severity:** Blocks causal claims about semantics alone or model internals; acceptable descriptive comparison with these caveats.

**22. Is target and held-out secrecy enforced?**

**Verdict:** The documented text-only supervisor boundary can be adequate. A separate process alone is **not a security sandbox** if the evaluated agent has filesystem, shell or process access under the same permissions.

**Evidence:** `replay.py` takes the target in process arguments; `cognitive_probe.py` loads the full frozen archive containing grading outputs; both print final grades. The README warns that the protocol is not a sandbox. `EXPERIMENT-PROTOCOL.md:29–35` correctly denies the model tools/files/arguments/final feedback and requires fresh context.

**Strongest counterargument:** No tools are proposed for the small model pilot. A pure completion model receiving only supervisor-approved JSON does not need a whole container merely to hide its launch arguments.

**Smallest decisive check:** Inspect the **actual model request and granted tool set**, not just source intentions. Record a whitelist of fields sent to the model; demonstrate that initial messages/transcripts omit target indices, frozen paths, sample manifests and grades; reset context between views. If tools are added, isolate mounts, permissions and process visibility. Never let grades or the paired session's answers persist into another scored session.

**Severity:** No demonstrated leak in a completed model run—none exists. This is a hard gate before claiming a blinded model result.

**23. Which baselines and failure denominators are required?**

**Verdict:** Recompute **random-informative and entropy** on the same frozen targets, pool order, budget and uniform-survivor final rule; frugal, no-question and all-query references are useful additions. I independently verified the random expectations and confirmed displayed `cognitive_probe.choose` agrees with native entropy across all 750 three-question episodes. For the planned 16-episode sample:

| Baseline | Held-out agreement | Mean questions |
|---|---:|---:|
| Random informative | 79.910099% | 2.199487 |
| Entropy | 87.500000% | 1.812500 |
| Frugal | 87.500000% | 1.750000 |

**Evidence:** `matched_pilot_baselines.json`, `protocol_validation.json`, protocol Baselines and metrics section.

There is also a concrete scoring boundary: `replay.py wrap 43 10 --shuffle 2026`, followed by `{"ask":9}` and `{"pick":4}`, returns `heldout_exact:true` even though that pick contradicts the received answer. Target 10 returns `["abcdefgh-z"]` for the queried input; picked original candidate 14 returns `["abcdefgh-","z"]`. They happen to agree on the held-out suite. This follows the declared endpoint and does **not** affect classical policies, which pick survivors.

**Strongest counterargument:** Reporting held-out agreement and query consistency separately is scientifically legitimate. The problem arises if held-out success is advertised as correct use of all evidence.

**Smallest decisive check:** Freeze a model success definition requiring valid completion, query-consistent selection and held-out agreement; also report the original held-out-only metric for comparability. Count malformed JSON, repeated/out-of-range asks, missing picks and truncation as failures with categories. Keep every scheduled episode in each condition's denominator. Permit at most the predeclared infrastructure retry, retain both attempts and report first-attempt sensitivity; never retry reasoning failures selectively. Report incomplete pairs rather than silently analyzing only complete sessions.

**Severity:** Mandatory scoring/protocol decision before the pilot; no correction required to existing classical score tables.

### F. Connection to autonomous repair

**24. Where do trustworthy expected outputs come from offline?**

**Verdict:** From legitimate task requirements, existing trusted tests/contracts, a permitted reference implementation, or independently justified properties. A metamorphic relation can reject some behaviors without supplying a complete expected output. Ambiguous requirements may supply no trusted answer at all.

**Evidence:** The package uses a hidden configuration as a perfect oracle; manuscript Introduction explicitly states that candidate agreement cannot supply the contract. `RESEARCH-REVIEW.md` and `EXPERIMENT-PROTOCOL.md` keep reference patches/tests evaluator-only. The RGT paper explicitly assumes a human-written reference patch; CodeMonkeys instead works with model-generated, imperfect tests.

**Strongest counterargument:** In some repair tasks, specifications and existing tests are sufficient to create new trustworthy checks, so this component can transfer without a live maintainer.

**Smallest decisive check:** For each proposed repair probe, record its expected-behavior source and whether it is trusted, hypothetical or unavailable. Treat model votes as evidence of agreement, not correctness. Without a justified oracle, a probe identifies disagreement; elimination based on a model-written answer remains a heuristic.

**Severity:** Blocks direct transfer of perfect-oracle performance to offline autonomous repair. Candidate comparison, stopping and evidence logging can still transfer.

**25. What minimum end-to-end experiment could establish repair benefit?**

**Verdict/proposal:** Freeze a small set of public repair tasks across at least two repositories, one checkpoint and a total per-task compute cap. Use a prespecified baseline agent and a version that spends a bounded share of that same cap on candidate-distinguishing checks. Ten to twenty tasks could demonstrate feasibility and expose regressions; they would not establish broad superiority.

**Evidence required:** Every scheduled task, generated candidate, test, execution, model call, timeout and final patch; evaluator-only candidate coverage; independent final repair grading. Charge candidate generation, probe creation, executions and selection to both arms. A baseline must be allowed to use any saved selection budget for its normal work. Alternatively, holding candidate/test workloads identical cleanly isolates selection, but that is a matched-workload component result rather than evidence of optimal end-to-end compute allocation.

**Strongest counterargument:** Realistically grounded labels and reproducible repository setup may cost more time than the entire remaining paper window. A token pilot with cherry-picked successful tasks would add little.

**Smallest decisive check:** Run paired full-task trials with trusted checks available from permitted task information, and include tasks lacking any correct candidate. Report final resolved-task differences, costs and failures, with repository-level sensitivity. Hidden patches/tests must never generate selection evidence.

**Severity:** Required for claiming demonstrated repair benefit; appropriate later work for the current resource. CPU matrix accuracy cannot establish it.

### G. Submission decision

**26. How does the evidence map to the five criteria?**

These are **my provisional assessments of the current resource draft**, not official scores or predictions of judging.

| Criterion | Provisional 0–5 | Strongest supported evidence | Weakest unresolved point |
|---|---:|---|---|
| Novelty | 2 | Controlled resource, exact baselines, inspectable interventions | Established querying/filtering; uncertain incremental user value |
| Quality | 2 | Correct finite calculations and explicit limitations | Eight curated families; post-hoc richer-channel intervention |
| Relevance | 2 | Concrete question-selection interface and repair motivation | No Gemma or repository-repair demonstration |
| Verifiability | 4 | Same-runtime reproduction, frozen matrices, manifest, independent checks | No actual model runner/run to audit; notebook not separately rerun in Jupyter here |
| Clarity | 4 | Concise manuscript already discloses major limitations | Title expectations, objective terminology and abstract comparator emphasis |

**Evidence:** The manuscript, reference and new execution artifacts; verified official rubric.

**Strongest counterargument:** Resource awards can value simplicity and reproducibility more than this assessment anticipates; the field impact of a small diagnostic can exceed its size.

**Smallest decisive check:** Have a reader unfamiliar with the conversation identify the measured task, prior, oracle, endpoint and contribution from the abstract and methods alone. Add the crossed table and closest-work comparison.

**Severity:** A reasonable resource submission is supportable; a competitive award claim is not established by these scores.

**27. Which missing experiment has highest information value?**

**Verdict:** First incorporate the already-completed crossed comparison and reproducibility evidence. Among genuinely new experiments, the best choice depends on access and the claim being defended:

| Option | Information gained | Cost/risk | Recommendation |
|---|---|---|---|
| Bounded Gemma pilot | Can a relevant model use the interface; what fails? | Serving, context and leakage setup; weak causal inference | Highest relevance value if inference is ready by the access cutoff |
| Fresh-family prospective probe test | Does the design principle extend beyond diagnosed regex? | Moderate design cost; answer-capacity controls essential | Highest resource-generalization value; CPU-capable |
| One-label-error robustness check | How badly exact elimination fails under one controlled violation | Low cost; likely confirms an expected limitation | Useful later or as a replacement, not a third pre-deadline study |
| No new experiment | More reliable claims, artifacts and submission | Leaves external relevance unresolved | Credible fallback; preferable to a rushed, leaky or selectively reported pilot |

**Evidence:** Completed CPU audit; proposed protocol; no verified live GPU balance or model setup.

**Strongest counterargument:** A small Gemma pilot could show mostly formatting/context failures and do little for scientific novelty. A strong resource can be more coherent without a rushed model appendix.

**Smallest decisive check:** One development-only serving smoke test and prompt-size check, then a firm go/no-go. Keep at most the two bounded experiment slots in the action plan.

**Severity:** Prioritization decision, not an obligation to perform all listed experiments.

**28. What findings change the recommendation?**

**Verdict:** **Submit after narrowing** is the current recommendation: the arithmetic, code and same-runtime results survive scrutiny, while the broader application claims remain unestablished.

**Evidence:** Exact reproduction; independent random/tree checks; matched entropy/probe result; published prior-art overlap; explicitly missing model/repair studies.

**Strongest counterargument:** If the only contribution accepted by the authors is a novel repair algorithm or a demonstrated cognitive mechanism, the current evidence cannot sustain their intended paper. Merely changing the title would not fix that mismatch.

**Decision thresholds:** Submit a resource paper when the solver, data provenance, bibliography, scoped claims and final artifacts are reviewable. Narrow claims when benefits depend on one family, richer answers or a convenience sample. Substantially revise if a model pilot exposes leakage, scoring inconsistencies are hidden, or an algorithmic-novelty claim proves necessary to the thesis. Postpone if a central result cannot be reproduced, a required rights/eligibility issue remains unresolved, or no honest contribution can be stated before the freeze. A negative but valid model pilot can be reported; it is not automatically a reason to postpone.

**Smallest decisive check:** Apply that checklist to the actual final manuscript and run manifest, not planned experiments. Distinguish a valid submitted entry from a paper likely to persuade judges.

**Severity:** No demonstrated technical reason to postpone the bounded resource. No evidence supports a winning probability.

## 4. Top five threats and cheapest decisive responses

These are ranked by their ability to undermine the **research contribution or an expanded claim**, not by pretending the reproduced score table is invalid. Several are already disclosed limitations.

| Rank | Threat and evidence status | Claim at risk | Cheapest decisive response |
|---|---|---|---|
| 1 | Incremental value over established active identification and interactive patch filtering; unresolved research judgment | A defensible novel research contribution | Direct overlap table plus a concrete resource use case; avoid algorithmic novelty |
| 2 | Perfect labels, present correct candidate and free matrix construction; observed design assumptions | Transfer to offline repair agents | State the conditional task and oracle provenance; reserve repair-benefit claims for an actual end-to-end trial |
| 3 | Post-hoc, richer-channel regex probes; observed design and measured answer-cardinality change | General or human-effort probe-design improvement | Add crossed entropy results and information/length accounting now; prospective matched-capacity test if pursued |
| 4 | Eight curated families, configuration-uniform priors and duplicate behaviors; observed | Universal ranking or statistically broad gains | Publish class counts, per-family effects and leave-one-family-out results; label alternative priors as sensitivity cases |
| 5 | Identity objective differs from endpoint; held-out-only grader can reward an inconsistent pick; demonstrated | Held-out optimality and valid future model success | Include the counterexample; require a prespecified consistency metric/gate and an audited model secrecy boundary |

## 5. Literature comparison

The overlap claims below were checked against primary sources. “Remaining contribution” describes a possible distinction for PatchQuestions, not proof that no other resource has that feature. None of these papers' performance numbers are evidence for this project.

| Closest work and direct primary source | Verified overlap | Remaining PatchQuestions distinction | Verification depth |
|---|---|---|---|
| [InPaFer: Interactive Patch Filtering as Debugging Aid](https://arxiv.org/abs/2004.08746), v2, 2020 | Developer answers to discriminating program attributes filter patches; includes a user study | Fixed input/output matrices, exact policy comparison and exhaustive target rotation | Abstract and PDF Section 2 |
| [Human-In-The-Loop Automatic Program Repair / LEARN2FIX](https://arxiv.org/html/1912.07758v1), 2019 preprint | Limited human labels and active oracle learning before repair | Assumes an already-correct oracle and fixed candidates; isolates selection rather than learning an oracle | Abstract and method/algorithm passages |
| [xTestCluster: Test-based Patch Clustering for Automatically-Generated Patches Assessment](https://arxiv.org/html/2207.11082v2), 2024 revision | Generates tests, cross-executes patches and clusters dynamic outcomes to support review | Adaptive trusted-label acquisition and finite-budget policy reference | Abstract; execution and clustering methods |
| [Automated patch assessment for program repair at scale](https://doi.org/10.1007/s10664-020-09920-w), 2021 | Uses human-written reference-patch behavior as an oracle for generated-test assessment | Hides the intended candidate and measures which queries reveal it | Publisher abstract and introduction |
| [CodeMonkeys](https://arxiv.org/html/2501.14723v2), 2025 | Candidate edits, generated tests, cross-execution and a selection trajectory | Small exact component evaluation with perfect labels and transparent costs/assumptions | Abstract and Section 2.3 |
| [Ambig-SWE](https://arxiv.org/abs/2502.13069v3), 2026 revision | Separates detecting underspecification, asking and using the answer in software tasks | Starts after ambiguity is exposed, with finite observable candidate behavior | Primary abstract and metadata |
| [Ask or Assume?](https://aclanthology.org/2026.findings-emnlp.15/), 2026 | Clarification seeking and uncertainty-aware scaffolding on underspecified repository tasks | Exact low-budget selection and stopping diagnostics, not a new ask-versus-act concept | Official ACL abstract and metadata |
| [SWE-Clar](https://arxiv.org/abs/2610.31854), October 2026 preprint | Separates clarification assessment from implementation in greenfield tasks | Compact executable contracts and algorithmic baselines | Primary abstract and metadata; not independently reproduced |
| [The Geometry of Generalized Binary Search](https://nowak.ece.wisc.edu/GBS_arxiv_v4.pdf), Robert Nowak | Finite hypotheses, strategic discriminating queries and decision-tree identification | A software-specific resource and multi-outcome observations; not invention of active identification | Primary author-hosted abstract and setup |
| [Active Learning Literature Survey](https://research.cs.wisc.edu/techreports/viewreport.php?report=1648), Burr Settles, 2009 | Label-budget query selection and different query settings | Distinguish fixed-pool selection from engineered query synthesis | University report record and abstract |

No citation in this table is marked “verified” solely because the package says so. Recent clarification sources were verified at abstract/metadata depth; they should not support detailed method comparisons beyond that coverage. The manuscript's three-item related-work section should add at least LEARN2FIX, xTestCluster, an active-identification foundation and the most relevant current clarification work. Approximately 250–350 focused words can state the differences without turning the paper into a literature survey.

## 6. Deadline-aware action plan

**Must-fix work, beginning now:**

1. Adopt the resource title and narrow contribution. Preserve the strong disclosures already present.
2. Add the crossed regex table, explicitly identify the tree's identity objective and keep entropy beside the question-saving claim.
3. Integrate the closest-work comparison. Add equivalence-class counts and a short per-family/sensitivity note.
4. Attach or include the same-runtime reproduction record, frozen-data hash and independent checks in the reproducibility materials. Explain that the notebook embeds six modules; its README currently says five.
5. Before any model session, freeze the real supervisor implementation, consistency success rule, invalid-action handling and secrecy boundary. A proposed protocol is not evidence that those controls exist in execution.
6. Keep the manuscript below the official limit; the current file has approximately **1,806 whitespace-separated words**, leaving room for targeted additions. This review is an analysis document, not a replacement competition Writeup.

**At most two bounded new experiment slots:**

| Slot | Fixed scope | Stop rule | Allowed conclusion |
|---|---|---|---|
| 1: Conditional Gemma feasibility | One available checkpoint; 16 paired episodes / 32 fresh sessions; matched exact baselines; development-only plumbing before freeze | If inference, context sizing or model-access terms are unresolved by **8 Nov, 18:00 PKT**, drop it. Use only confirmed resources, with a maximum of the already-proposed 20-unit profiling allowance if such units are actually available. No training or model sweep. | Demonstrated success/failure on the displayed component task; descriptive presentation sensitivity |
| 2: Prospective CPU probe check | One genuinely new API family; frozen atomic/compound design rule and matched output-capacity accounting; entropy and frugal at budgets 1–3; scoring suite generated only after probe freeze | Stop if a defensible freeze or channel-control design cannot be established in one focused work session. No redesign after the first scored result. Complete analysis before **10 Nov, 18:00 PKT**. | Limited prospective evidence for the design principle on one additional family |

The existing crossed comparison and mathematical validation are already complete; they do not require another research campaign. Drop the robustness extension rather than adding a third experiment. Also drop fine-tuning, graph/embedding integration, multi-model comparisons, large human studies and repository-scale repairs from this paper window.

**Schedule:** On 7–8 November, finish claim/bibliography/reproducibility edits and decide the model-access gate. On 9–10 November, complete only approved bounded experiments and retain negative outcomes. Freeze research scope on **10 November at 18:00 PKT**. Prepare a complete submission-ready Writeup by **11 November at 20:00 PKT** and perform the final content/status audit by **12 November at 18:00 PKT**. The author should leave the remaining time as a submission buffer before **13 November at 04:59 PKT**. This review does not authorize or perform publication or submission.

**Credible CPU-only fallback:** The reproduced resource, verified recurrence, independent random baselines, corrected terminology, expanded related work and crossed entropy/probe result form a coherent paper. State that learned-agent, human-cost and repository validation remain future work. Do not write a placeholder model section that makes planned results resemble completed evidence.

## 7. Claim edits

| Treatment | Claim | Suggested wording or action |
|---|---|---|
| Retain | 150 configurations, eight families, five splits, 750 conditions | Call them configuration identities and target/split conditions; disclose 30 joint behaviors among 36 hex configurations |
| Retain | Exact expectations for both random policies | Explain stopping and conditional path weighting; distinguish exact expectation from float rounding |
| Retain | Frugal's lexicographic identity/question optimum | State uniform targets, deterministic correct labels, present target and unit question cost |
| Retain | 76.32%, 85.27%, 85.48% reference results | Label family-macro full held-out agreement, maximum three questions and CPython 3.12.14 |
| Narrow | Coding-agent title and motivation | Describe API-contract disambiguation; an agent interface is not an evaluated agent |
| Narrow | 17.7% question saving | Name ordinary tree as denominator and report entropy's 1.882 versus frugal's 1.864 |
| Narrow | All-query “ceiling” | Use uniform-selection reference in generic wording; optionally include the independently verified bound for these matrices under the stated prior/information model |
| Narrow | Compound probes demonstrate better questioning | Say richer probes improve label-count efficiency in an exploratory single-family experiment; add the entropy result and answer capacity |
| Narrow | Transfer suite | “Separate constructed suite designed after diagnosis,” not external or prospective validation |
| Remove/prevent | Held-out-optimal algorithm; human-time savings; general repair gains | Unsupported by the current objective or experiments |
| Remove/prevent | Masking proves a cognitive core or removes only semantics | Neither follows from the control or the proposed pilot |
| Remove/prevent | 750 independent bugs; completed Gemma run; verified current Colab balance | These would be false descriptions of the evidence |

The final three rows are safeguards for revision; the current draft already avoids many of those claims. They are not accusations that the manuscript contains them.

**Proposed contribution paragraph**

PatchQuestions is an executable resource for studying question selection under uncertainty about a finite set of API contracts. It fixes candidate behavior and separates the available probe vocabulary, adaptive selection policy and trusted-label budget. Across eight Python API families, it supplies exhaustive target rotation, exact expectations for randomized baselines, frozen runtime-specific behavior matrices and an identity-optimal depth-limited reference with a question-cost tie-break. Its experiments show where simple entropy selection nearly matches that reference and where the available probes limit identification. An exploratory regex intervention, crossed with both entropy and tree selection, illustrates how richer probe outputs improve performance under a question-count budget. The resource does not measure human annotation time or end-to-end repair performance.

**Proposed abstract**

Selecting a useful clarification requires separating the information available in candidate behaviors from the policy used to acquire trusted labels. We introduce PatchQuestions, an executable API-contract disambiguation benchmark with 150 configurations across eight Python standard-library families. Policies inspect candidate outputs on a fixed query pool and receive the intended output only for selected inputs. Five splits and exhaustive target rotation produce 750 target–split conditions. At a maximum of three questions, random-informative selection achieves 76.32% full held-out agreement, entropy 85.27%, and an identity-optimal frugal tree 85.48%. Frugal tree uses 1.86 questions on average, compared with 1.88 for entropy and 2.27 for ordinary tree search. In an exploratory regex intervention, engineered compound probes increase three-question agreement from 30% to 86.25% for both entropy and frugal selection, while increasing the information available in individual answers. We provide exact randomized baselines, frozen behavior matrices and reproducible CPU evaluation. The benchmark isolates question selection under a correct-candidate, perfect-oracle assumption; it does not establish savings in human time or improved repository repair.

## 8. Author challenge

1. **What research use remains after subtracting InPaFer, LEARN2FIX, xTestCluster and active identification?** A satisfactory answer needs the closest-work comparison and a concrete diagnostic/resource use case, not merely more citations.
2. **Why should this component matter when candidate generation, execution and oracle acquisition are free?** Supply a clearly bounded intended use and, for stronger claims, a real workflow's cost breakdown.
3. **Exactly what is optimal, and under which prior?** Derive leaf-count identity recovery and the frugal cost recurrence; explain both counterexamples and why behavioral optimality does not follow.
4. **Why is a configuration the unit of probability?** Show redundancy counts, the intended target distribution and a sensitivity check that distinguishes reweighting from changing the task.
5. **How much of the regex improvement is additional answer bandwidth?** Provide the crossed policy table, answer cardinality/entropy, selected-transcript lengths and any truly matched-capacity comparison.
6. **What evidence makes the transfer result prospective?** Produce a dated freeze and an uninspected scoring protocol; otherwise defend its explicitly exploratory role and disclose the development history available.
7. **Why does the claimed saving matter when entropy uses nearly the same number of questions?** Supply comparator-specific denominators, absolute effects, practical costs and budget-dependent results.
8. **Can a proposed model result survive target secrecy, shared row patterns and presentation confounds?** Provide actual model requests, tool permissions, fresh-context logs, token counts and complete failed sessions.
9. **Can a model be counted successful after contradicting an oracle answer?** State the primary success rule before running; demonstrate the existing `wrap/43/10` example and show how consistency is reported or enforced.
10. **What exactly is established if all new experiments fail or are dropped?** Present the reproduced CPU resource, appropriately limited contribution, complete artifacts and a final Writeup whose claims do not depend on unexecuted work.


