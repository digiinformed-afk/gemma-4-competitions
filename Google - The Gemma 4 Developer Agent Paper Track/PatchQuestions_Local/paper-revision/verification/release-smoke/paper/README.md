# PatchQuestions

The revised manuscript is `PatchQuestions_Writeup.md`. It describes an executable finite resource for API-contract disambiguation under a trusted-label budget. The original benchmark and historical score tables retain their definitions.

## Reproduce on CPU

Open `PatchQuestions.ipynb` in Kaggle or Jupyter and run every cell in a fresh kernel. It embeds **nine modules**, creates a fresh output directory and rebuilds the benchmark, crossed entropy/frugal comparison, selected-transcript costs, reference verification, frozen matrices and presentation control. The notebook's deterministic supervisor fixture is a software test. No model session is run. No network, GPU or package installation is needed inside the notebook.

Use **CPython 3.12.14** for the reference measurements. Other runtimes may change library behavior, particularly Base64. The embedded original frozen matrices are preserved separately from regenerated runtime matrices.

The release package includes `tools/reproduce_paper.py` for command-line reproduction in a fresh directory. From the release root, run:

```sh
python -B tools/reproduce_paper.py --paper paper --output my-fresh-run
```

The output directory must not already exist. The script copies sources, captures commands/stdout/stderr, compares reference results and leaves reference files unchanged. To run from the original workspace, use `paper-revision/reproduce_paper.py --output <new-directory>` instead.

Individual commands, after copying modules and frozen data into a new working directory, are:

```sh
python -B benchmark.py > summary.json
python -B analyze.py > audit.json
python -B intervention.py > intervention.json
python -B verify.py
python -B export_cases.py
python -B paper_analysis.py
python -B cognitive_probe.py --check
```

For cross-runtime presentation controls, restore the supplied reference `frozen_cases.jsonl.gz` after export. Keep the runtime-generated archive under a different name.

## Results and observation schema

`scores.csv` has 18,000 family/split/target/policy/budget rows. `heldout_exact` and `probe_exact` are probabilities over randomized query paths and uniform final survivor choice. `survivors` and `queries_used` are expected counts. `summary.json` weights the eight families equally. `audit.json` retains the historical key `ceiling`; read it as the **all-query uniform-selection reference**. The implementation key is preserved for compatibility.

`frozen_cases.jsonl.gz` contains 40 CPython 3.12.14 matrices, including target configurations and held-out outputs. It is public reproducibility material and evaluator-only during blinded evaluation. Outputs observe JSON-serialized wrapper returns or exception class. The resource measures finite-suite agreement, with a present correct candidate and perfect deterministic labels.

`paper_analysis.py` generates `revision-results/revision-results.json`, `selected-transcripts.csv` and `TABLES.md`. It crosses both selectors with all three regex pools at budgets 1–3 on both scoring suites. Costs sum selected input and serialized outcome Unicode code points. They exclude protocol/actions/repeated context, tokenizer measurements and human effort. Every traced result is checked against the original evaluator. Class counts and leave-one-family-out results are descriptive evaluator diagnostics.

## Model evaluation boundary

Historical `replay.py` and `cognitive_probe.py` implement held-out-only grading. A pick that contradicts an acquired answer can still match the held-out suite. They remain available to reproduce the historical interface; use **`pilot.py`** for a new learned-model pilot.

The new supervisor reports valid completion, query consistency, held-out agreement and identity separately. Primary success requires the first three. Strict JSON parsing rejects duplicate keys, Boolean/noninteger indices, repeated/out-of-range queries, over-budget actions and malformed responses. Model requests include only instructions, displayed matrix, previous actions and requested answers. Private grades are never fed back. No execution tools are supplied.

`pilot.py freeze` creates a private supervisor plan after development-only serving checks. It samples two targets per family across configuration-index halves, shuffles each pair's rows independently and uses randomly renamed masked labels. Named/masked row order is matched and starting view alternates. This differs from the older unrun targets-0/1 proposal; it remains a convenience feasibility sample. No scored plan has been frozen for a real checkpoint in this release.

The `--model-info` JSON must supply exactly these confirmed fields: `served_model`, `model_revision`, `tokenizer_revision`, `quantization`, `serving_stack`, `hardware`, `context_tokens`, `max_tokens`, `temperature`, `top_p`, `seed`, `timeout_seconds`. Values must be selected and recorded using development cases before freezing. The release supplies no pretend confirmed model configuration.

```sh
python -B pilot.py freeze --model-info confirmed-model-info.json --output private-plan.json
python -B pilot.py baselines --plan private-plan.json > matched-baselines.json
python -B pilot.py run --plan private-plan.json --endpoint http://127.0.0.1:8000 --tokenizer /local/exact-tokenizer --output new-run
python -B pilot.py summarize new-run
```

Live inference needs `transformers` for the exact local tokenizer and an already-running local server supporting `/v1/chat/completions`. The tokenizer loads locally with remote code disabled. Requests use server-side chat formatting, so verify that the local tokenizer/chat template matches the server on development requests. Preflight counts reserve output tokens; no prompt truncation is requested. The adapter is unit-tested using test doubles and has not been tested against a real Gemma endpoint. [Serving API reference](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/).

The plan hashes data, supervisor source and instruction. Keep it and the frozen archive outside evaluated-model access. A separate process alone does not sandbox a tool-enabled agent. Store all model/tokenizer/quantization hashes and server launch configuration with the confirmed revision metadata; the supervisor cannot independently certify weight identity.

Each request, raw response, usage and preflight token count is flushed to its session event log. Completed or failed results are individually flushed. Summarization includes every scheduled session, including interrupted/unstarted sessions. There are **no retries** in this revision. Infrastructure fixes require a new run ID and disclosure of the original attempt. Incomplete named/masked pairs are reported. This is recovery of evidence, rather than resuming model context after an interruption.

## Kaggle Writeup

Use the manuscript H1 as title, its bold line as subtitle and Abstract onward as report. The overview requires those fields, introduction, methods/experiments and related work/citations, with at most 3,000 words. Our local checks include title, tables and references and remain below the limit; confirm the final Kaggle rendering/count. The optional code link must be a publicly accessible notebook in Project Links. A saved draft still needs the platform's Submit action.

The release contains submission preparation instructions and local verification evidence. It does not establish personal eligibility, author/rights declarations, account acceptance or submission. The documented paper deadline is 12 November 2026, 23:59 UTC / 13 November, 04:59 PKT. [Official overview](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview), [official rules](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/rules).
