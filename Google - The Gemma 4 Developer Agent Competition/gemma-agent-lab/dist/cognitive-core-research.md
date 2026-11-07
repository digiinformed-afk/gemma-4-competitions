# Cognitive core: research update and competition adaptation

Reviewed 6 November 2026. Status: sourced design hypothesis; no new GPU experiment, training or benchmark run has been performed.

## Attribution and source quality

Karpathy discusses separating problem-solving ability from extensive memorized knowledge in the [original Dwarkesh interview](https://www.dwarkesh.com/p/andrej-karpathy), 17 October 2025, around 12:42–13:50. The transcript also discusses continual learning around 22:07. This is a research proposal rather than a demonstrated training recipe.

The interview links to his [earlier cognitive-core post](https://x.com/karpathy/status/1938626382248149433). Direct retrieval from X returned 403 in this research session. We use the verified interview for attribution; the post is provided as an original reference, not as independently retrieved evidence. Do not substitute third-party summaries or fabricated quotations for the source.

## Our design inference

For the fixed-model competition, a useful operational hypothesis is that repair improves when repository facts are retrieved from the current checkout, working state is concise and explicit, and learned behavior emphasizes tool use, hypothesis revision and verification. These implementation choices are ours; Karpathy did not propose this specific competition agent or these experimental thresholds.

We cannot extract a new model architecture or remove encyclopedic knowledge merely by changing a prompt or training a LoRA. Keep the organizer-approved Gemma checkpoint intact. Do not claim a cognitive-core model has been built. Small parameter count alone is not evidence of superior generalization.

## Related research

| Work | Relevant observation | Limitation for this competition |
|---|---|---|
| [Lost in the Middle](https://arxiv.org/abs/2307.03172), Liu et al., 2023 | Context position affects performance on retrieval-oriented tasks. | Does not prove shorter context improves repository repair. |
| [MemGPT](https://arxiv.org/abs/2310.08560), Packer et al., 2023/2024 | Explicit context movement between memory tiers is a viable design. | Memory writes and reads add cost; use requires reliable delivery. |
| [Reflexion](https://arxiv.org/abs/2303.11366), Shinn et al., 2023 | Textual feedback can influence subsequent attempts without weight updates. | Self-generated reflection can preserve an incorrect diagnosis. |
| [Recursive Language Models](https://arxiv.org/abs/2512.24601), Zhang et al., 2025/2026 | Programs can inspect and decompose external context. | Frontier/other-model results do not establish Gemma repair gains; recursive calls can exhaust budget. |
| [How Do Small Coding Agents Use Code Graphs and Embeddings?](https://arxiv.org/abs/2610.33958), Bellam, 2026 | Tool benefits vary across model and localization characteristics. | Must evaluate final patches, not only localization. |

This is an abstract/documentation-level synthesis, not an independent replication. Do not transplant paper scores into competition predictions.

## Proposed architecture

**Fixed reasoning policy:** one allowed Gemma base model for all inference. Begin with the 31B no-adapter Kaggle baseline, then a separate E4B comparison. Use the same model for any optional reviewer. Internet-backed oracles cannot be used in offline scoring.

**External repository evidence:** lexical search, semantic seeds when useful, bounded graph expansion, narrow source reads and test execution. Tag observations with path, symbol and source revision. After edits, invalidate affected cached facts and inspect current code. A graph edge is not a behavioral guarantee.

**Task-local working state:** use the downloadable evidence-ledger template. Start with an approximately 1,000-token cap measured with the real tokenizer. Keep raw logs separate if supported. Record observed facts, alternatives rejected by tests, modified files, commands, exit statuses and the next action. Always distinguish setup failures from product failures.

**Delivery after compaction:** first inspect the actual HARNESS_README. Use native supported resume/compaction hooks only if available. Otherwise instruct the agent to consult its ledger using allowed tools at phase boundaries. Do not assume a saved file will automatically enter model context. If no reliable task-local persistent storage exists, test a structured in-context summary instead and label the variant accurately.

**No task contamination:** reset ledger state between tasks. Do not use hidden test data, reference patches or later issue histories. Do not persist evaluation task solutions as future-task memory. Keep scratch notes outside the captured repository diff where the sandbox supports it; audit the submitted patch.

**Behavioral adaptation:** consider verified traces that demonstrate exact tool arguments, grounding, error recovery and stopping. Train offline on development-only data. Keep adapters fixed during evaluation until current organizer rules and harness explicitly establish support for any online updates; online learning is not part of this plan.

## Controlled experiments

| ID | Control and treatment | Main failure to detect |
|---|---|---|
| C1 | Best simple baseline vs same agent plus bounded evidence ledger | Ledger maintenance costs more than rereads it saves |
| C2 | C1 vs C1 with explicit ledger recovery after supported compaction | Stale or missing state causes repeated wrong actions |
| C3 | Same scaffold without adapter vs verified behavioral SFT | Better tool syntax but worse held-out reasoning |
| C4 | Same scaffold vs one review on a predefined ambiguity trigger | Extra inference consumes time without correcting patches |

Keep model artifact, sampling, seeds, task IDs and global wall-clock limits identical within each comparison. Test 31B and E4B in separate runs. Use repository-disjoint folds and retain final confirmation data. Deduplicate issue families and base commits across training and evaluation.

Primary outcome: resolved / all scheduled tasks. Secondary measures: repeated source reads, repeated disconfirmed hypotheses, missing critical facts after compaction, invalid tool calls, tokens, empty patches, timeouts and total wall time. Count ledger tokens, I/O, review calls and failures in the cost. A small task set is a smoke check, not evidence of superiority. Report paired discordant outcomes and per-repository sensitivity.

Promotion requires useful repair/reliability evidence at equal budget. If context management improves latency but loses correct patches, keep it experimental. A same-model second review is correlated judgment; fresh execution of tests provides a different source of evidence.

## Compute and scheduling

Keep the existing 200-unit Colab plan. Research and trace preparation should use CPU. Run scaffold ablations before substantial SFT. Use the 20-unit profiling allowance to establish E4B feasibility, then verify a tiny exported adapter loads in Kaggle. Only then release the 80-unit SFT allocation. The 40-unit comparison allocation, 20-unit export/reload allocation and 40-unit reserve remain unchanged.

Kaggle's L4 ×4 provides 96 GB aggregate GPU memory, distributed across four devices. Do not treat it as one 96 GB GPU; model parallelism and runtime compatibility matter. Internet is disabled and quota consumption is elevated. See [official accelerator details](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview/upgraded-accelerators). Check actual account quota before scheduling full rehearsals.

## Recommended next action

After obtaining the official harness, establish B0/B1, then test C1 before adding training. Build a small regression set of source edits followed by compaction/resume to check that ledger facts are either refreshed or explicitly marked stale. If the ledger does not get reread, fix delivery rather than expanding storage. This provides a concrete way to investigate the proposal within the time and compute available.
