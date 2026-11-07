# Research review and implications

Reviewed 7 November 2026. This is a targeted primary-source review for the immediate competition decision, not a systematic literature review or proof of novelty. The recommendations combine published evidence with the actual local artifacts. Published benchmark percentages are not forecasts for this team's competition entry.

## Why these competitions belong in one program

The paper track explicitly welcomes unpublished related research, including resources, without requiring a main-track entry. The main track evaluates executable repair agents. This supports one evidence-selection research program with two deliverables and distinct validation protocols. [Paper overview](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview), [Main overview](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview)

The existing work has three possible directions. PatchQuestions has code, frozen data, results and a manuscript, making it the best deadline fit. Graph retrieval has clear competition relevance but would require substantial new evaluations. The cognitive-core idea has a small controlled presentation experiment ready, but no evidence about a new model architecture. Use that experiment as a model-facing benchmark probe, without making architectural claims.

## Closest prior work and concrete consequences

| Primary source and reading depth | What is already established | Consequence for this paper |
|---|---|---|
| [InPaFer: Interactive Patch Filtering as Debugging Aid](https://arxiv.org/html/2004.08746v2), 2020. Abstract and approach/interaction passages inspected. | Developer questions about static/dynamic program properties can filter plausible patches. Its evaluation includes a developer study. | Do not claim interactive patch filtering is new. Explain the difference between program-property questions and this resource's finite input/output matrix. |
| [LEARN2FIX: Human-In-The-Loop Automatic Program Repair](https://arxiv.org/html/1912.07758v1), 2019 preprint / ICST 2020. Abstract and oracle-learning procedure inspected. | A limited human-label budget can train a bug oracle before repair. | State that PatchQuestions assumes perfect labels and a fixed candidate pool; it does not learn a general bug oracle. Add this missing related-work citation. |
| [xTestCluster: Test-based Patch Clustering](https://arxiv.org/html/2207.11082v2), 2024 journal version. Abstract and generation/execution/clustering passages inspected. | Generated tests can group plausible patches by their dynamic behavior, reducing review work. | Behavioral grouping is prior art. Contrast review-set reduction with adaptive label selection and finite-suite agreement. Add this missing citation. |
| [Automated Patch Assessment for Program Repair at Scale](https://doi.org/10.1007/s10664-020-09920-w), 2021. Publisher abstract/introduction inspected. | Reference behavior can support assessment of test-passing patches; passing existing tests does not establish correctness. | Keep scoring references evaluator-only. Say finite held-out agreement, not program equivalence. |
| [CodeMonkeys](https://arxiv.org/html/2501.14723v2), 2025. Abstract and candidate-selection/cost passages inspected. | Generated tests and a selection trajectory can help choose among multiple candidate edits; candidate coverage differs from selected-patch success. | Report candidate availability separately from selection accuracy in future repair experiments. Its large compute regime and imperfect generated tests differ from free executions and perfect labels here. |
| [Ambig-SWE](https://arxiv.org/abs/2502.13069), current 2026 revision. Abstract/metadata inspected. | Detecting missing information, asking questions and using answers are distinct agent capabilities. | PatchQuestions starts after ambiguity is exposed; describe it as a controlled component evaluation. |
| [Ask or Assume?](https://aclanthology.org/2026.findings-emnlp.15/), EMNLP Findings 2026. Official abstract/metadata inspected. | Selective clarification and uncertainty-aware agent scaffolds have already been studied on repository tasks. | Permit an early pick and measure questions used. Do not claim to introduce the ask-versus-proceed decision. |
| [SWE-Clar](https://arxiv.org/abs/2610.31854), October 2026 preprint. Abstract/metadata inspected. | Clarification quality and implementation can be evaluated separately in greenfield work. | Keep transcripts, information acquisition and final choice as separate outcomes. Its task scope differs from API configurations. |
| [Agentless](https://arxiv.org/abs/2407.01489), 2024. Abstract/metadata inspected. | A simple localization/repair/validation pipeline is an important baseline. | Start the main track with a simple reproducible agent before adding orchestration. |
| [How Do Small Coding Agents Use Code Graphs and Embeddings?](https://arxiv.org/abs/2610.33958), October 2026 preprint. Abstract/metadata inspected. | Reported tool gains vary by checkpoint, size and graph depth; localization improvements need not become successful repairs. | Graph retrieval is not an unexplored idea. Evaluate it against lexical search at equal end-to-end budget after the paper deadline. Do not transplant the paper's gains to this competition. |

Most works above were not independently reproduced. Three closest method families and CodeMonkeys received targeted method reading, rather than relying entirely on abstracts. The existing manuscript cites only InPaFer, the patch-assessment study and CodeMonkeys; the bibliography should now cover LEARN2FIX, xTestCluster and the most relevant clarification benchmarks as space permits.

## Assessment of the local evidence

The current results support a resource and diagnostic paper. They give little reason to sell depth-limited tree search as an accuracy breakthrough: at budget three its margin over entropy is about 0.21 points. Frugal search uses nearly the same mean questions as entropy. This is an argument for including a strong cheap baseline and reporting negative results.

The regex intervention is more striking, but deliberately exploratory. Four compound inputs can reveal several flags in one answer. Counting one long structured answer as one label does not make it one equally easy human interaction. Its transfer suite was also designed after the initial diagnosis, so describe it as a separate constructed check, not untouched external replication.

The benchmark rotates 150 configurations through five splits: 750 target/split conditions on only eight families. Candidate executions are available in advance and the correct candidate is always included. Exact expectations remove Monte Carlo noise from those policy comparisons; they do not remove dataset-selection bias or create 750 independently sampled bugs.

The tree objective maximizes configuration-identification leaves, while the reported endpoint is agreement on a finite scoring suite. These are different objectives. The all-probes score is a reference for the stated uniform-survivor rule, not proof that no conceivable selector or richer probe pool can do better. Preserve that distinction in captions and claims.

The named/masked entropy agreement is a mathematical invariance control. It is not evidence that Gemma reasons abstractly, has learned a cognitive core, or generalizes to unseen APIs. A model pilot can test behavior on the displayed task, with presentation and tokenization confounds acknowledged.

## What transfers to the main agent

Transfer **candidate comparison, useful-test selection, observed-evidence logging and stopping rules**. Do not transfer the perfect oracle assumption. In autonomous repair, model-written expected outputs and candidate voting are hypotheses; use requirements and legitimate executable checks to establish support.

The official starter documents public tasks containing reference patches and tests for development. Keep those evaluator-only at generation time. A public discussion contains community environment failures and a Kaggle staff response about training-task fixes and hidden-test validation; it does not establish that an old community score remains current. Version the evaluator and run baseline/gold controls before model comparisons. [Official starter inputs](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent/input), [staff response in discussion](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/747248)

## Recommended reading and work order

1. Read the approach sections of InPaFer, LEARN2FIX and xTestCluster and write a short direct comparison before revising the contribution claim.
2. Use Ambig-SWE and one current clarification benchmark to explain what the new resource isolates. Use CodeMonkeys to motivate patch selection while acknowledging the oracle difference.
3. Finish the fixed Gemma pilot only if infrastructure is ready. Keep any result, including a negative result, subject to the declared feasibility scope.
4. After submission, read the exact current harness and implement a simple baseline. Graph retrieval and adaptation remain gated experiments.

All deadlines and model constraints were checked against rendered official Kaggle pages on 7 November; indexed search still contains stale 31B-only rules. Check live pages again before the actual release, particularly if the organizer changes the schedule or harness.
