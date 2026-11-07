# Official requirements review: coverage and remaining access

Reviewed 7 November 2026. This records the source coverage behind the phase visualization. Proposed work dates come from PROGRAM-PLAN.md; official deadlines come from the competition overview pages.

| Official source | Review coverage |
|---|---|
| [Paper overview](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview) | Full rendered page: description, timeline, five judging criteria, required report sections, optional links, 3,000-word scope, non-archival status, awards and final submission requirement. |
| [Paper rules](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/rules) | Complete competition-specific terms/rules and all 18 foundational sections. |
| [Main overview](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview) | Full rendered page: scoring, archive structure, timeline, prizes/bonus, all four permitted models, adapter/tool/skill rules and accelerator restrictions. |
| [Main rules](https://www.kaggle.com/competitions/gemma-4-developer-agent/rules) | Complete competition-specific rules read. Foundational wording compared with paper rules: identical through all substantive sections; difference appears in the trailing navigation/prize labels. |
| [Main data](https://www.kaggle.com/competitions/gemma-4-developer-agent/data) | Complete public description: task fields, snapshots, graphs, embeddings, wheels, sandbox setup, sample directory, harness guide and two-phase verification. The file viewer explicitly blocks full HARNESS_README pending rule acceptance/sign-in. |
| [Official starter notebook](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent) | Version 3: all six code cells read, including offline setup, model configuration, graph tools, vLLM startup, inference/verification and archive validation. Notebook outputs inspected. This is documentation review, not execution. |
| [Winner documentation guidelines](https://www.kaggle.com/WinningModelDocumentationGuidelines) | Full page: model summary, reproducible submission archive, README/environment, pinned dependencies, configuration, saved model, entry commands and presentation. These are winner handoff guidelines, not extra initial paper-submission sections. |

## Confirmed interpretation

The paper deliverable is a submitted Writeup reporting original unpublished research, with the stated required sections. A notebook and a publicly accessible PDF alternative are optional. Main-track participation is not required for the paper. All five judging dimensions have equal weight. Our CPU benchmark and optional Gemma feasibility run are a proposed approach, not mandatory competition experiments.

The main deliverable is an agent archive with root agent.yaml. The evaluator runs inference to collect patches and separately grades them. The generated submission.parquet is an evaluator output; it is not a replacement for the requested archive. The official starter's small smoke run is not a full-budget submission rehearsal. Its successful notebook execution can still contain unresolved tasks/NO_PATCH, as the displayed outputs demonstrate.

Current permitted base variants are 31B, 12B, E4B and E2B in the exact QAT W4A16 CT formats named in the overview. Use one base across all agents in an archive. LoRA is optional. The starter validates symlinks, allowed extensions and total uncompressed member size against a 3 GiB limit; consult the actual current validator before release.

The rules cover eligibility and account/team limits; entry/submission deadlines; competition data security; external resources and licensing; no private sharing outside teams; winner selection, notification and disqualification; prize documentation and tax obligations; privacy/publicity; warranties, governing law and other legal terms. The phase map summarizes actionable gates and does not replace these rules. No account eligibility determination was made.

## Not yet reviewed: explicit technical gate

The full HARNESS_README.md (55.94 kB), actual sample_submission directory, bundled evaluator/configuration source and exact model license/terms have not been read in this workspace. The complete competition bundle is not present locally, and the data viewer requires a signed-in account that has accepted the rules. Public notebook code does not substitute for those files.

To finish that review, obtain HARNESS_README.md and sample_submission from the official data page after sign-in/rule acceptance and place them in a private workspace folder. Then verify exact supported YAML keys, limits, compaction behavior, permitted file extensions, lifecycle and final submission process against the current bundle before implementing the agent.

This is not a claim to have read every forum post, third-party article, linked framework manual, model agreement or evaluator implementation. No rules were accepted and no signed-in competition status or GPU quota was verified during this review.
