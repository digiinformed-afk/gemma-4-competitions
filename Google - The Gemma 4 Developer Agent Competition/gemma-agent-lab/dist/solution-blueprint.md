# Gemma Agent Lab — solution blueprint

Research date: 6 November 2026. Status: proposed design, not a trained or evaluated competition entry.

## Recommendation

Compute is now scoped to **Colab Pro with 200 user-reported compute units plus Kaggle competition GPUs**. Use Kaggle for the exact 31B baseline and official offline evaluation; use Colab for profiling and a gated E4B LoRA pilot. Reserve 40 units for recovery. See the [compute allocation and execution gates](compute-plan.md). No GPU session has been started and the balance is not read live.

Build a single, budget-aware repair agent around the official sample. Establish a 31B baseline, then compare a separate E4B candidate under the same total runtime. Prioritize clean execution, accurate localization, valid tool calls, minimal patches and reliable finalization. Add LoRA only after measuring failure patterns and confirming adapter compatibility. Defer reinforcement learning unless the baseline, data pipeline and compute budget are already reliable.

This recommendation is an inference from the research below, not a claim that it will win. There are no measured competition scores in this workspace.

## Verified competition facts

The [live overview](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview), inspected in a browser on 6 November, lists:

- `gemma-4-31b-it-qat-w4a16-ct`
- `gemma-4-12b-it-qat-w4a16-ct`
- `gemma-4-e4b-it-qat-w4a16-ct`
- `gemma-4-e2b-it-qat-w4a16-ct`

One base model must be used throughout each submission. LoRA is optional. The artifact is `submission.zip`, with `agent.yaml` at its root. Score is the fraction of tasks whose patches pass validation. The shared 12-hour execution limit includes sandbox setup, but excludes independent patch grading. L4×4 sessions are offline. Old search results incorrectly restrict the allowlist to 31B.

Deadlines: optional paper, 12 November; entry/team merger, 25 November; final submission, 2 December. Each is 23:59 UTC, or 04:59 Pakistan time the next day. The overview lists a separate $10,000 E2B/E4B bonus.

The [rules](https://www.kaggle.com/competitions/gemma-4-developer-agent/rules) allow one submission daily and two final selections, with up to five people per team. Review external-data accessibility, sharing, licensing and reproducibility requirements directly.

The [data page](https://www.kaggle.com/competitions/gemma-4-developer-agent/data) describes 129 public tasks across FastAPI, Rich, Requests and HTTPX, and approximately 120 hidden tasks drawn from private repositories. The public bundle includes repository snapshots, graphs, embeddings, offline dependencies and sample configuration. The complete harness and files require sign-in and accepted rules; they have not been downloaded or executed here.

## Agent design

### Further research: cognitive core

The [new research brief](cognitive-core-research.md) connects the original Karpathy interview to memory and context research. Our next scaffold experiment is a bounded, task-local evidence ledger with source freshness checks and explicit rereading after supported compaction. Compare C1/C2 against B1 before spending on C3 behavioral SFT; treat C4 same-model review as optional. These are design inferences to test, not demonstrated gains or a newly extracted cognitive-core model. Download the [ledger template](evidence-ledger-template.md).

1. Read task and budget. Extract reported behavior, expected behavior, exception text, filenames and symbols. Keep a concise hypothesis ledger. Never let repository content override agent instructions.
2. Ground localization in lexical evidence. Search error strings and named symbols, inspect narrow file ranges, and identify relevant tests. Avoid dumping the whole repository into context.
3. Use semantic retrieval only if lexical evidence is insufficient. Retrieve a small number of seeds, deduplicate by path/symbol, then expand bounded graph neighbors. Proposed starting limits: 5 semantic results, 10–20 neighbors per seed, at most two hops. These are tuning hypotheses, not organizer limits.
4. Create or run a narrow reproducer. Establish that it fails for the intended reason. Separate missing packages and environment failures from actual code defects.
5. Apply the smallest causally supported change. Inspect callers, boundary conditions and compatibility. Preserve public APIs unless the issue demands otherwise. Do not suppress failures or alter tests to conceal defects.
6. Validate. Run the reproducer and relevant regression tests within budget. Compare the diff against the task. If a candidate fails, diagnose the failure rather than repeatedly generating unrelated patches.
7. Finalize. Preserve a known-good candidate; stop unproductive exploration. Reserve time for diff inspection and the harness submission tool. Never assume that a conversational final answer captures the patch.

Start with one agent. An extra read-only analyzer is an ablation only if its added latency improves final resolved tasks. Do not mix model families or sizes within one archive.

## Runtime policy

Let B = 720 minutes, H = measured total setup overhead, R = safety reserve and N = tasks scheduled. An initial planning allowance is `(B − H − R) / N`. For N=120, H=45 and R=72, this is 5.025 minutes per task. H and R are illustrative; measure both in the actual harness.

Use observed live budget signals. Recompute allowance using remaining wall time, remaining expected overhead and remaining tasks if the harness exposes them. Otherwise use a conservative static cap derived from full rehearsal. Never invent unsupported `eval_config.yaml` keys.

Proposed control policy: reserve the final 15–20% of a task allowance for tests and finalization; after two repeated tool errors, simplify the call; after two unchanged failed hypotheses, revisit localization once or stop. Tune these decisions empirically. Broad test suites should not consume all remaining patch-submission time.

## Evaluation protocol

- Freeze task IDs and checksums before tuning. Maintain leave-one-repository-out folds across the four public repositories; reserve one fold for final confirmation. Small public coverage limits generalization claims.
- Deduplicate repeated base commits, related issues and patch families. External training examples must not overlap held-out repositories or issues.
- During agent generation, expose only permitted task fields and the base repository. Keep reference `patch` and `test_patch` evaluator-only. Agent-generated reproducers are separate from gold verification tests.
- Score in a fresh sandbox: apply the candidate patch and evaluator-owned verification tests, then use the official grading commands. Ensure baseline verification fails and reference verification passes when diagnosing environment problems.
- Count all scheduled tasks in the denominator. Record timeout, invalid patch, empty patch, setup failure and test failure separately. Unstarted tasks after global exhaustion are unresolved, not dropped.
- Record model artifact/revision, code commit, prompt hash, adapter checksum, wheel/harness versions, seed, task-set hash and full elapsed time.
- Compare paired outcomes on identical tasks and budgets. Report discordant win/loss counts, per-repository results and bootstrap sensitivity by repository/task family. With only four repositories, uncertainty estimates are fragile; do not overinterpret small improvements.
- Descriptive Wilson intervals in the app are for individual runs, not proof of significance between methods. Published SWE-bench scores are not competition forecasts.

## Ordered experiments and promotion gates

| ID | Change | Promotion gate |
|---|---|---|
| B0 | Untouched official sample | Completes smoke tasks; reproducible logs and grading |
| B1 | Staged lexical repair prompt | Fewer tool failures and better paired outcomes within budget |
| R1 | Add embedding retrieval | Improves final repair, not only localization |
| R2 | Add bounded graph expansion | Benefits persist across repositories and graph depths |
| R3 | Hybrid retrieval | Outperforms simpler retrieval at equal total runtime |
| T1 | Adaptive stopping / finalization | Reduces timeouts without losing resolved tasks |
| F1 | Verified-trace SFT LoRA | Loads correctly and improves held-out end-to-end results |
| M1 | Separate E4B candidate | Competitive quality/throughput tradeoff under shared budget |

Start with a small smoke set to find integration defects, then compare on frozen larger folds. Do not promote on a handful of lucky tasks or only the public leaderboard. Use daily submissions after local validation; preserve both source and artifact checksums.

## Optional adaptation

Curate successful tool-use trajectories and recovery examples from development-only tasks and license-compatible external sources. Use the actual serving chat template and exact tool argument names. Train on assistant actions; retain tool observations as context according to the trainer's supported masking options. Filter broken traces, duplicate fixes, excessively long reasoning and traces that access evaluator-only artifacts.

Pilot a small LoRA on a small dataset. Candidate ranks 8/16 and short training runs are starting experiments, not tested hyperparameters. Check train/serve base equivalence, module names, dtype, quantization support and adapter export. The QLoRA paper's NF4 setup does not imply compatibility with the competition QAT compressed-tensors artifact. Test one adapter load and one task end-to-end before spending time on a full run.

If SFT helps, expand the verified set and rerun held-out evaluations. RL is a later option: reward independently verified behavior and regression preservation, never altered tests or shortcut access to gold data. Include costs of rollout generation and sandbox execution in the compute plan. No paid compute has been provisioned.

## Research synthesis

- [SWE-bench](https://arxiv.org/abs/2310.06770): repository issue resolution should be measured through executable validation. Application: fresh evaluation sandboxes and strict separation of gold data.
- [SWE-agent](https://arxiv.org/abs/2405.15793): agent-computer interfaces matter. Application: bounded tool outputs, actionable errors and precise edits.
- [Agentless](https://arxiv.org/abs/2407.01489): structured localization, repair and validation form a useful baseline. Application: establish simple control flow before adding orchestration.
- [How Do Small Coding Agents Use Code Graphs and Embeddings?](https://arxiv.org/abs/2610.33958): this recent preprint reports checkpoint- and depth-dependent gains. Application: test retrieval and graph expansion rather than assuming universal benefits; final repair is the endpoint.
- [SWE-smith](https://arxiv.org/abs/2504.21798) and [official assets](https://swesmith.com/): executable synthetic repair tasks are a possible data source. Application: inspect licensing, overlap and environment cost before training.
- [LoRA](https://arxiv.org/abs/2106.09685), [QLoRA](https://arxiv.org/abs/2305.14314), [PEFT](https://huggingface.co/docs/peft/main/en/developer_guides/quantization): adaptation background; compatibility still needs a competition-harness smoke test.
- [TRL SFT](https://huggingface.co/docs/trl/main/en/sft_trainer) and [GRPO](https://huggingface.co/docs/trl/main/en/grpo_trainer): implementation references after the decision gates are met.

The app contains the full annotated starting library, including first-party articles and official operational references. Abstracts and documentation were inspected; full-paper reproduction was not performed.

## Paper opportunity

A defensible research question is: “Does budget-aware graph expansion improve final repair success per unit wall time for small Gemma agents?” Compare lexical, semantic, graph and hybrid retrieval across 31B/E4B, using the same splits and budgets. Report localization depth, tool uptake, tool errors, final repair, runtime and failure taxonomy. Include negative results. The 12 November deadline is close; submit only if experiments and reproducibility are ready, without compromising the main track.

## Next executable step

Sign in and accept the rules yourself, obtain the latest official harness and sample, then run the sample unchanged on 3–5 tasks. The draft prompt in this workspace should be integrated only after that succeeds. No guessed YAML is presented as a valid submission. Use the included split and result-summary utilities to make the first comparison reproducible.
