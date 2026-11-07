# Which question should a coding agent ask before choosing a patch?

**PatchQuestions, an offline benchmark for recovering API behavior under a three-question budget**

## Abstract

A coding agent can produce several edits that pass a smoke test but disagree on edge cases. If a maintainer will clarify only three expected outputs, which three inputs should the agent show them? We introduce PatchQuestions, an executable benchmark with 150 candidate Python API configurations across eight families. Every configuration serves in turn as the intended contract. Policies observe candidate executions and receive a trusted label only for the input they select. With a budget of three, random informative queries achieved 76.32% exact agreement on all held-out inputs, greedy entropy achieved 85.27%, and a depth-limited decision tree achieved 85.48%. Breaking ties between trees by their expected question count reduced mean usage from 2.27 to 1.86 at the same observed accuracy. A follow-up regex experiment found a larger effect from redesigning the inputs themselves. This resource isolates a decision that can be evaluated before integrating a model into a repository repair loop.

## Introduction

Consider two patches for a CSV importer. Both read a file containing one ordinary field. One treats a backslash before a comma as an escape, while the other treats it as ordinary text followed by a field separator. Another ordinary field tells the maintainer nothing about this difference. Asking what should happen on an escaped comma can decide between the patches. The outcome still has to come from someone or something that knows the contract. Candidate agreement alone cannot supply it.

We study the cost of obtaining that information. The resource separates three choices that are easy to conflate in a full coding-agent run: which candidate behaviors are available, which inputs the agent may ask about, and how it spends its questions.

## Benchmark

Each family is a short wrapper around a Python standard-library operation. Candidate edits change documented settings, such as decoding strictness, separator choice or regex flags. The intended behavior is defined by a concealed configuration. This models uncertainty about a specification after multiple implementations pass the same test. It does not sample the patch distribution of a trained model.

| API family | Candidate configurations | Non-smoke inputs |
|---|---:|---:|
| URL quoting | 20 | 42 |
| Query-string parsing | 16 | 35 |
| CSV reading | 24 | 48 |
| Text wrapping | 16 | 48 |
| JSON serialization | 16 | 31 |
| Regex matching | 16 | 56 |
| Base64 decoding | 6 | 56 |
| Hex formatting | 36 | 44 |

The generator takes explicit products of options and input fragments, removes duplicate inputs and excludes one ordinary smoke input per family. All candidates agree on that smoke input. For each of five seeds (19, 43, 73, 101, 137), we shuffle the sorted inputs, allocate up to 16 and at most half to the query pool, and reserve the rest for scoring. Each configuration acts once as the target in each split, giving 750 target–split episodes. These are repeated conditions on eight API families. They should not be interpreted as 750 independent software bugs.

The policy can inspect each candidate's output on every query input. Asking for an input reveals its target output and eliminates inconsistent candidates. Outputs preserve structured values and list order. Exceptions are represented by class name. Regex outcomes are lists of match spans, which can convey several pieces of information in one answer. Policies never consult the held-out output matrix to select a question.

## Methods

We compare six policies. **Random** samples unused inputs without replacement. **Random informative** samples only inputs that separate surviving candidates. **Most outcomes** chooses the input with the greatest number of distinct outcomes. **Entropy** chooses the split with maximum outcome entropy under a uniform prior on the survivors. **Tree** chooses an input that maximizes the number of attainable answer leaves within the remaining budget. **Frugal tree** breaks ties by minimizing the total number of questions summed over possible targets. Remaining ties use the seeded pool order. Informative policies stop when the pool contains no further distinction.

The tree calculation is small enough to audit. At zero remaining questions any nonempty candidate set yields one leaf. For each informative input, partition survivors by output and sum the best child leaf counts with one fewer question. Keep the maximum. For the frugal variant, querying at a node costs one question for each target in that node, plus the costs of its children. Memoization reuses repeated candidate sets. Previously asked inputs need no separate history in this recursion because they cannot split a surviving set.

Why maximize leaves? Under a uniform target prior and uniform final selection among survivors, a leaf containing k candidates contributes k/N × 1/k = 1/N to exact configuration recovery. More leaves therefore optimize identity recovery. **The reported metric is deliberately different.** A selected candidate succeeds if it agrees with the target on *every* held-out input, including exception classes. Different configurations may be interchangeable on that suite. We assign a leaf the exact success probability of a uniform draw and average targets and splits within each family, then weight the eight families equally. Both random policies are averaged over their possible query paths exactly. All reported budgets count trusted labels. Candidate executions and the thinking time required to supply a label are separate costs.

## Results

**Mean probability of full held-out agreement (%)**

| Policy | 1 question | 2 questions | 3 questions |
|---|---:|---:|---:|
| Random | 30.72 | 46.35 | 56.83 |
| Random informative | 34.24 | 59.21 | 76.32 |
| Most outcomes | 52.09 | 72.79 | 84.81 |
| Entropy | 51.64 | 72.89 | 85.27 |
| Tree | 52.09 | 74.43 | 85.48 |
| Frugal tree | 52.09 | 74.43 | 85.48 |

The no-question baseline was 7.05%. At three questions, restricting random choice to informative inputs accounts for 19.49 percentage points. Frugal tree gained a further 9.16 points over this stronger baseline. Its advantage over entropy was only 0.21 points, entirely attributable to CSV reading at this budget. Across families, the tree tie-break reduced average questions by 17.7% relative to the ordinary tree. Entropy used 1.88 questions, close to the frugal tree's 1.86. These finite-suite averages give little reason to prefer an expensive search over entropy on accuracy alone.

| Family | Random informative | Entropy | Frugal tree | All available queries |
|---|---:|---:|---:|---:|
| URL quoting | 62.8 | 98.0 | 98.0 | 100.0 |
| Query parsing | 86.7 | 95.0 | 95.0 | 95.0 |
| CSV reading | 62.2 | 83.3 | 85.0 | 85.0 |
| Text wrapping | 86.2 | 92.5 | 92.5 | 92.5 |
| JSON serialization | 99.9 | 100.0 | 100.0 | 100.0 |
| Regex matching | 30.0 | 30.0 | 30.0 | 30.0 |
| Base64 decoding | 83.3 | 83.3 | 83.3 | 83.3 |
| Hex formatting | 99.5 | 100.0 | 100.0 | 100.0 |

The first three columns use a three-question budget. The last asks every available query and applies the same uniform-survivor rule. In seven families the frugal policy already reaches that reference. The regex failure was particularly informative: extra questions from the same pool could not expose the missing behavioral differences.

### Follow-up experiment on probe design

After inspecting the regex result, we replaced the last four query inputs in every split while holding the original scoring suite fixed. One replacement set probes case, multiline anchors, dot/newline matching and Unicode character classes separately. The other uses four short multiline strings and an anchored pattern that can exercise several flags in one run. For example, the pattern begins with an anchored lowercase q, followed by a dot and a word character. Different lines begin with q or Q and include newlines or non-ASCII letters at discriminating positions. The observable is the list of matching spans. The replacement inputs are disjoint from the original inputs.

| Regex probe pool | 1 question | 2 questions | 3 questions |
|---|---:|---:|---:|
| Original | 15.0% | 22.5% | 30.0% |
| Four single-flag probes | 15.0% | 25.0% | 50.0% |
| Four compound probes | 51.0% | 75.0% | 86.25% |

On a separate 48-input transfer suite using different patterns and strings, the three-question results were again 30%, 50% and 86.25%. This was an exploratory intervention on one family. The inputs were engineered with knowledge of the flag space, and a human may take longer to supply a list of spans for a compound example. It shows what a better probe vocabulary can buy under a label-count budget. It does not establish a saving in human minutes.

## Related work

*Interactive Patch Filtering as Debugging Aid* studies using developer questions to filter candidate patches [1]. *Automated Patch Assessment for Program Repair at Scale* uses reference behavior for generated tests to assess patch correctness [2]. *CodeMonkeys* combines generated tests and a model-based selection trajectory to choose among multiple edits [3]. We build on those ideas. Our contribution is an offline finite resource with exhaustive target rotation, exact random-policy expectations, an auditable depth-limited reference, and a comparison between changing the query policy and changing the available inputs.

## Reproduction and limitations

Run the companion notebook from top to bottom on CPU without network access. It rebuilds the scores, per-family analysis and regex intervention. The separate interactive runner exposes a JSON interface for an agent to select a probe or a final candidate. The evaluator should launch the runner separately and give the agent only protocol messages. The target must stay outside the agent's prompt and tool access.

Reported results use CPython 3.12.14. A separate CPython 3.13.5 run reproduced the frugal-tree aggregate accuracy at all three budgets, but some Base64 outcomes and random-policy results differed. For example, decoding AA==x with the default alphabet and validation disabled returned a zero byte in our first runtime and raised an error in the second. We include frozen baseline data so such differences can be inspected.

The eight families are curated Python configuration tasks with deterministic behavior and a correct candidate in the pool. Equal target weighting, perfect oracle answers, free candidate executions and uniform tie selection are experimental choices. The finite held-out suites approximate behavioral agreement. They cannot prove program equivalence. We have not evaluated Gemma 4, developer response times, repository-scale repairs or a leaderboard submission. A direct extension is to collect candidate patches from a fixed Gemma run, execute them on sandboxed probes, and compare policy gains against both random informative selection and entropy with the same available inputs and label budget.

## References

1. [Interactive Patch Filtering as Debugging Aid](https://arxiv.org/abs/2004.08746).
2. [Automated Patch Assessment for Program Repair at Scale](https://doi.org/10.1007/s10664-020-09920-w).
3. [CodeMonkeys: Scaling Test-Time Compute for Software Engineering](https://arxiv.org/abs/2501.14723).
