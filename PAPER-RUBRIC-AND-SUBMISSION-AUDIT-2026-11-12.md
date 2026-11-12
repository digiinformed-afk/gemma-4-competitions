# PatchQuestions — official rubric-to-manuscript audit (2026-11-12, 19:03 PKT)

## Source and scope
Official Paper Track overview (readable public page): https://www.kaggle.com/competitions/gemma-4-developer-agent-paper
Canonical manuscript: [PatchQuestions_Writeup.md](Google%20-%20The%20Gemma%204%20Developer%20Agent%20Paper%20Track/PatchQuestions_Local/public/project/PatchQuestions_Writeup.md).
This document is a **source-based submission audit**, not a Kaggle receipt or a new experiment. The official page states November 12 2026 23:59 UTC deadline, 3,000-word maximum, original unpublished work, required title/subtitle/abstract/introduction/methods/experiments/related work/citations, and an explicit final **Submit** action after saving. A public notebook is optional. An accessible PDF through Public Project Link is an alternative, not a requirement.

## Five equally weighted judging criteria — concrete manuscript evidence and remaining risks

| Criterion | Current manuscript support | Unresolved limitation / action |
|---|---|---|
| Novelty | Fixed executable API-contract matrix resource; diagnostic decomposition of probe vocabulary vs adaptive selector; open-set verification stress test | Prior interactive patch filtering, active learning and generalized binary search are acknowledged; avoid claiming invention of these ideas |
| Quality / generalization | Eight standard-library families, five overlapping input splits, leave-one-family-out sensitivity, exact randomized controls | Curated synthetic configurations, reused universes, perfect oracle; no independent repository repair task or real Gemma agent |
| Relevance | Trusted clarification questions and candidate falsification matter for coding-agent decision support | Demonstrated relevance is conceptual; no measured coding-agent productivity or bug-fix improvement |
| Verifiability | Frozen matrices, exact finite policy enumeration, reported split seeds, CPU CI records and reproducibility links | GitHub Actions success is not Kaggle submission; reviewer must be able to access source/results and reproduce commands |
| Clarity | Title, subtitle, abstract, methods, quantitative tables, related work and explicit limitations | Inspect Kaggle's rendered preview, word counter and links before final Submit |

## Submission critical path
1. In an **authenticated** Kaggle session, join the Paper Track and check eligibility and live rules.
2. Create/open a Writeup, use canonical manuscript verbatim, verify rendered length <= 3,000 words and functional citations/links. Source audit previously counted 2,483 whitespace-separated words, **not** a Kaggle editor count.
3. Save and then explicitly press **Submit**; confirm submitted status and record public Writeup URL and UTC timestamp.
4. Do not wait for new experiments. No Kaggle confirmation is available from this audit.

## Execution ledger
- **EXECUTED:** fetched canonical manuscript and submission gate via GitHub connector; read official Paper Track overview through public web search; mapped all five official judging criteria to manuscript evidence and limitations.
- **BLOCKED:** connected browser returned “Browser access requires the originating browser context”; authenticated Kaggle writeup submission cannot be verified or performed in this session.
- **NOT RUN:** new CPU/GPU experiment; no new measurements, no baseline modification.
- **SCIENTIFIC BOUNDARY:** the 750 target/split conditions and exploratory candidate-deletion stress test are **finite simulated API-contract benchmarks**; separate noisy-oracle checks are **binary toy enumerations**. Neither measures real Gemma-agent performance.
- **NEXT:** prioritize actual authenticated final Submit and receipt before 2026-11-12 23:59 UTC.
