# PatchQuestions: An Executable Benchmark for Budgeted API-Contract Disambiguation

**A finite resource for separating probe vocabulary, adaptive selection and trusted-label cost**

## Abstract

Selecting a useful clarification requires separating available candidate behaviors from the policy used to acquire trusted labels. PatchQuestions is an executable API-contract disambiguation resource with 150 configurations across eight Python standard-library families. Policies inspect candidate outputs on a fixed query pool and receive the intended output only for selected inputs. Five splits and exhaustive target rotation produce 750 target–split conditions. At a maximum of three questions, random-informative selection achieves 76.32% full held-out agreement, entropy 85.27%, and an identity-optimal frugal tree 85.48%. Mean question counts are 1.88 for entropy, 1.86 for frugal and 2.27 for ordinary tree search. In an exploratory regex intervention, compound probes increase three-question agreement from 30% to 86.25% for both entropy and frugal selection, while increasing answer capacity. We provide exact randomized baselines, frozen behavior matrices and reproducible CPU evaluation. The resource isolates selection under correct-candidate and perfect-oracle assumptions. Human-time savings and repository-repair gains remain unevaluated. An exploratory candidate-deletion stress test suggests verification questions can detect absent targets after identity uncertainty disappears.

## Introduction

Two CSV-importer patches can agree on an ordinary field and disagree on an escaped comma. Another ordinary field cannot resolve that ambiguity. A discriminating input helps only when a trustworthy source supplies its intended output. Candidate agreement alone cannot establish the contract.

PatchQuestions supports researchers developing question selectors or evaluating a model's use of displayed evidence. It fixes candidate behavior and exposes a finite query pool, allowing policy changes to be evaluated independently of candidate generation and oracle learning. A practical diagnostic is whether disappointing selection accuracy comes from the policy or from indistinguishable candidate rows. In our regex family, asking every available input still yields only 30% held-out agreement. Increasing the question budget within that pool cannot resolve the missing distinctions; revising the probes can.

The contribution is this inspectable component resource, its exact comparisons and diagnostic decomposition. Adaptive identification, behavioral clustering and interactive patch filtering are established ideas. We do not introduce a general repair algorithm. The main empirical lesson is that a strong simple selector nearly matches exact search here, while the available probe vocabulary can impose a much larger limitation.

## Resource and experimental design

Each family wraps a Python standard-library operation. Candidate configurations vary documented options, including quoting safety, parsing strictness, separators and regex flags. A concealed configuration defines the intended behavior. Every candidate agrees on an ordinary smoke input, and the correct configuration is always present.

| Family | Configuration identities | Non-smoke inputs |
|---|---:|---:|
| URL quoting | 20 | 42 |
| Query parsing | 16 | 35 |
| CSV reading | 24 | 48 |
| Text wrapping | 16 | 48 |
| JSON serialization | 16 | 31 |
| Regex matching | 16 | 56 |
| Base64 decoding | 6 | 56 |
| Hex formatting | 36 | 44 |

For seeds 19, 43, 73, 101 and 137, the generator shuffles sorted unique non-smoke inputs. Up to 16, and at most half, become query inputs; the rest are held out. Every configuration is rotated through the target role in each split. The resulting 750 conditions reuse eight curated families and five overlapping input universes. They are not independent software bugs.

Policies see all candidate outputs on the query pool. Asking reveals the target output and removes inconsistent candidates. They never use held-out outputs to choose a question. Returns are JSON-serialized structured values, with list order preserved; exceptions expose their class. JSON wire formatting and regex match-span lists are the observable contracts. This finite observation schema does not establish general program equivalence.

Targets are uniform over configuration identities within a family. Hex has 36 identities but only 30 distinct joint query/held-out behaviors. The other families are joint-distinct on their finite suites. Multiplicity therefore affects the prior; joint or held-out deduplication would change the experiment and must remain evaluator-only. The resource supplies class counts to make that choice visible.

## Methods and endpoints

We compare six policies. **Random** chooses uniformly among unused queries and spends its budget even after uncertainty disappears. **Random informative** chooses uniformly among unused queries that separate survivors and stops when none remain. **Most outcomes** maximizes the number of resulting groups. **Entropy** maximizes output entropy under a uniform survivor prior. **Tree** maximizes attainable answer leaves within the remaining depth. **Frugal tree** maximizes leaves and then minimizes questions summed over possible targets. Residual ties follow seeded pool order. All informative policies stop when no available query separates survivors.

For a nonempty survivor set S at depth zero, leaf count L is one and cost C is zero. An informative query partitions S into answer groups. Its recurrence sums child leaf counts and sets cost to |S| plus summed child costs. Frugal selects the largest leaf count, then the smallest cost. Memoization uses survivor set and remaining depth; previously asked queries are constant on descendants. Expected question usage is C/N at the root.

With N uniformly likely targets, a terminal leaf of k consistent candidates contributes (k/N)(1/k) = 1/N to configuration recovery under uniform final selection. Thus L/N is identity recovery. Duplicate behaviors do not invalidate this identity argument. Nonuniform target priors require a different objective.

Our endpoint is the probability that a uniform survivor choice agrees with the target on **every held-out input**. Identity-optimality does not imply optimality for that endpoint. For example, query columns (0,1,0) and (0,0,1), with held-out labels (0,0,1), both create two identity leaves. Their expected held-out agreement is respectively 2/3 and 1. The first-column tie rule can choose the weaker behavioral partition. We provide executable counterexamples.

Both random policies are evaluated over all possible conditional query choices, rather than Monte Carlo samples. We average targets and splits within each family, then weight families equally. The 18,000 score rows cover six policies and budgets zero through three. Exact finite expectations remove policy-sampling noise; they do not establish population generality. Costs count trusted labels. Candidate generation, matrix construction, oracle acquisition and human effort are outside that budget.

## Results

**Family-macro probability of full held-out agreement (%)**

| Policy | 1 question | 2 questions | 3 questions |
|---|---:|---:|---:|
| Random | 30.72 | 46.35 | 56.83 |
| Random informative | 34.24 | 59.21 | 76.32 |
| Most outcomes | 52.09 | 72.79 | 84.81 |
| Entropy | 51.64 | 72.89 | 85.27 |
| Tree | 52.09 | 74.43 | 85.48 |
| Frugal tree | 52.09 | 74.43 | 85.48 |

The no-question baseline is 7.05%. At three questions, informative random choice gains 19.49 percentage points over ordinary random. Frugal gains another 9.16 points over random informative, but only 0.2083 points over entropy, entirely from CSV. Excluding CSV removes that margin. Other leave-one-family-out margins are 0.2381 points. These are descriptive sensitivity checks across curated families.

Ordinary tree, entropy and frugal use respectively 2.265625, 1.881979 and 1.864479 questions per episode. Frugal saves 0.401146 questions, or 17.71%, relative to ordinary tree. Relative to entropy, the saving is 0.0175 questions, or 0.93%. These results support entropy as a strong baseline. Coarse CPU timing checks at this scale establish no stable search-cost ranking.

| Family | Random informative | Entropy | Frugal | All-query uniform reference |
|---|---:|---:|---:|---:|
| URL quoting | 62.8 | 98.0 | 98.0 | 100.0 |
| Query parsing | 86.7 | 95.0 | 95.0 | 95.0 |
| CSV reading | 62.2 | 83.3 | 85.0 | 85.0 |
| Text wrapping | 86.2 | 92.5 | 92.5 | 92.5 |
| JSON serialization | 99.9 | 100.0 | 100.0 | 100.0 |
| Regex matching | 30.0 | 30.0 | 30.0 | 30.0 |
| Base64 decoding | 83.3 | 83.3 | 83.3 | 83.3 |
| Hex formatting | 99.5 | 100.0 | 100.0 | 100.0 |

The first three columns permit three labels. The last reveals every available query and applies uniform final selection. It is a reference for that information model and selection rule. Frugal reaches it in seven families. The regex result diagnoses a pool limitation that aggregate accuracy alone would conceal.

### Exploratory probe intervention

After diagnosing regex, we replaced the final four queries in every split. Single-flag probes separately exercise case, anchors, dot/newline matching and Unicode classes. Compound probes combine flag-sensitive cases within multiline inputs and return match-span lists. Replacements are disjoint from original inputs, and each arm uses the same original scoring suite.

| Regex pool | Entropy, 2 labels | Frugal, 2 labels | Entropy, 3 labels | Frugal, 3 labels |
|---|---:|---:|---:|---:|
| Original | 22.50% | 22.50% | 30.00% | 30.00% |
| Single-flag replacements | 25.00% | 25.00% | 50.00% | 50.00% |
| Compound replacements | 68.75% | 75.00% | 86.25% | 86.25% |

A separate 48-input constructed suite gives the same three-label percentages. Both replacement probes and that suite were designed after the original diagnosis. Disjoint strings therefore supply an exploratory check, without prospective or cross-family validation. No complete history of discarded designs is available. At two labels, compound probes retain a 6.25-point frugal advantage; probe vocabulary does not eliminate every policy effect.

Original queries have at most two distinct candidate answers and one bit of initial answer entropy. Compound queries allow up to eight answers and 2.549 bits. They buy more information per call. Across all 80 regex target–split conditions, both selectors at budget three yield the following selected-transcript means.

| Pool | Questions | Input characters | Serialized-answer characters |
|---|---:|---:|---:|
| Original | 2.1000 | 13.400 | 37.100 |
| Compound | 2.0625 | 30.5875 | 38.6125 |

Character costs sum only selected inputs and returned serialized outcomes, excluding actions, protocol wrappers and repeated context. They are Unicode code-point counts, rather than tokenizer or human-time measurements. Initial answer entropy uses the full candidate prior; transcript information diagnostics also condition on current survivors. We provide target-level trajectories and capacity statistics. The result establishes label-count efficiency from richer probes. Equal-effort improvement remains untested.

## Open-set stress test: verification after uncertainty disappears

The main benchmark assumes a correct candidate is present. We also ran an **exploratory candidate-deletion stress test**: for each frozen target–split condition, remove that target configuration from the visible pool while retaining its trusted answers. This models a failure of candidate generation, not a real-world repair evaluation. We compare a fixed query order, entropy with standard early stopping, and entropy that spends remaining questions on verification even if all surviving candidates already agree. Verification queries are selected using the original *visible* candidate pool, without access to target identity or held-out outputs.

At three questions, family-macro rates of detecting that no candidate matches the answers were **34.79% fixed, 31.46% entropy-stop, and 43.15% entropy-plus-verification**. At one question, the corresponding rates were 12.19%, 23.70%, and 23.70%; at two, 22.50%, 31.46%, and 36.67%. The controlled sweep includes 750 target–split conditions, two presence states, three policies and three budgets (13,500 evaluation records). Runs use frozen CPython 3.12 matrices; code, tests and machine logs are [reproducible in GitHub Actions](https://github.com/digiinformed-afk/gemma-4-competitions/actions/runs/43091180332).

The result highlights a distinction: **a question may stop helping identify the best surviving candidate while still helping falsify the entire candidate set**. This intervention shares the same eight curated families and overlapping split universes, assumes a perfect oracle, and does not evaluate Gemma or repository repair. It motivates open-set verification as a future research target, not a general performance claim.

## Related work

| Prior work | Established overlap | Scope isolated here |
|---|---|---|
| InPaFer [1] | Developer answers filter candidate patches | Fixed input/output matrices and exact budgeted policy comparisons |
| LEARN2FIX [2] | Active human labeling learns a bug oracle before repair | Oracle assumed correct; selection among fixed candidates |
| xTestCluster [3] | Cross-execution clusters dynamically similar patches | Adaptive acquisition of trusted target outputs |
| Generalized binary search [4] | Strategic queries identify finite hypotheses | Executable API contracts with multi-outcome answers and behavioral scoring |
| CodeMonkeys [5] | Generated tests and trajectories select candidate edits | Exhaustive small-instance evaluation with perfect labels |
| Ambig-SWE [6]; Ask or Assume? [7] | Detecting underspecification, asking and using answers | Begins with ambiguity exposed and a visible finite behavior matrix |

These connections motivate the resource and bound its novelty. It permits inspectable policy/pool diagnoses, rather than demonstrating a new ask-versus-act mechanism or end-to-end repair benefit. The current clarification papers are compared at abstract/metadata depth; the filtering, oracle-learning, clustering and CodeMonkeys selection mechanisms received targeted method reading.

## Reproduction and limitations

The CPU notebook rebuilds the benchmark, crossed comparison and transcript costs without network or model access. It embeds nine source modules. Frozen CPython 3.12.14 matrices permit replay. A fresh Windows CPython 3.12.14 run reproduces all 18,000 score rows byte for byte and the JSON results numerically. Independent random-path checks cover 24,000 metrics; explicit tree enumeration covers 4,096 binary 4×3 matrices at budgets zero through three. The reviewer timing helper required explicit UTF-8 source reads/writes on Windows; failed attempts and the portability patch are retained. Historical 3.13.5 and separate 3.15.2 results remain separately labeled because Base64 behavior and random-policy averages differ.

The trusted oracle, present target, uniform configuration prior and precomputed candidate behavior are restrictive assumptions. A separate exhaustive **toy** audit of all 512 binary 3-candidate × 3-query matrices examines independent answer flips, not realistic annotation noise. With three questions, hard-elimination verification falsely rejects a present target in 0%, 10.92%, and 29.54% of conditions at 0%, 5%, and 15% oracle-error rates, respectively; its absent-target contradiction rate is 76.56% in that symmetric toy setting. [Python CI cross-validation](https://github.com/digiinformed-afk/gemma-4-competitions/actions/runs/43116822447) passed anchor assertions. These figures are not from the eight-family benchmark and are not evidence of noise-tolerant repair. Real-world missing-candidate detection, arbitrary Python outputs and human annotation costs remain unevaluated. Real repair may be dominated by generating candidates or obtaining justified expected behavior. Model-written expectations and candidate votes cannot substitute for a trusted contract.

We include a tested supervisor for future text-only model comparisons. Its primary success requires valid completion, consistency with acquired answers and held-out agreement; historical held-out-only scoring remains available separately. This prevents a candidate from being counted as successful evidence use merely because it matches the held-out suite while contradicting an answer. The supervisor keeps targets and grading outputs outside model requests. Its local serving adapter requires model-specific validation before use. No learned-model session, human study or repository repair is reported.

## References

1. Liang et al. (2020). [Interactive Patch Filtering as Debugging Aid, v2](https://arxiv.org/abs/2004.08746v2).
2. Böhme, Geethal and Pham (2019 preprint). [Human-In-The-Loop Automatic Program Repair](https://arxiv.org/abs/1912.07758v1).
3. Martinez et al. (2024 revision). [Test-based Patch Clustering for Automatically-Generated Patches Assessment](https://arxiv.org/abs/2207.11082v2).
4. Nowak. [The Geometry of Generalized Binary Search](https://nowak.ece.wisc.edu/GBS_arxiv_v4.pdf).
5. Ehrlich et al. (2025). [CodeMonkeys: Scaling Test-Time Compute for Software Engineering, v2](https://arxiv.org/abs/2501.14723v2).
6. Vijayvargiya et al. (2026 revision). [Ambig-SWE, v3](https://arxiv.org/abs/2502.13069v3).
7. Edwards and Schuster (2026). [Ask or Assume? Uncertainty-Aware Clarification-Seeking in Coding Agents](https://aclanthology.org/2026.findings-emnlp.15/).
