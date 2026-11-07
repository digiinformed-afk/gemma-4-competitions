# Bounded paper experiment and shared evidence protocol

**Revision on 7 November 2026.** The paper revision is complete on reproduced CPU evidence. No real model session or checkpoint-specific sample has been frozen. The executable `pilot.py` supervisor and its README in the paper project supersede the proposed model scoring and sampling details below. Primary model success requires valid completion, consistency with acquired answers and held-out agreement; the historical held-out-only metric is retained separately. The new plan samples two targets per family across configuration-index halves, independently shuffles paired row orders and randomly renames masked labels. It permits no retries within a run. Confirm exact model/tokenizer/server settings on development cases before freezing. The earlier targets-0/1 schedule below remains historical planning. See the [current paper status](<../Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local/paper-revision/STATUS.md>).

Proposed 7 November 2026. No Gemma session has been executed in this review. Freeze the model, protocol and sample manifest before the first scored session. This specification refines the existing `cognitive-core-study.md` into a component-level feasibility experiment.

## Question and limits

Can one fixed Gemma checkpoint select useful questions and choose a consistent candidate from a finite behavior matrix? Does hiding input/output semantics change its performance?

This is a test of displayed evidence selection. It is not a repair benchmark, a test of model internals, a human-time study or a comparison of model sizes. Named and masked views contain the same equality partitions, but they differ in readability and tokenization. Equal accuracy could mean both views are solved or both fail; always report absolute scores.

## Freeze before inference

| Item | Locked choice / required record |
|---|---|
| Data | Existing `frozen_cases.jsonl.gz`, with SHA-256. Do not regenerate it under a different Python before the paired comparison. |
| Sample | Existing study's split **19**, targets **0 and 1** for each of the eight families: **16 paired episodes / 32 model sessions**. This convenience sample supports feasibility only. |
| Base model | One available Gemma 4 checkpoint, no adapter. Prefer an organizer-permitted E4B artifact if it can be served reliably; log exact model path/revision, tokenizer, quantization and serving stack. Do not silently replace it mid-run. |
| Conditions | `named` and `masked`, using `cognitive_probe.py`. Candidate row order is matched between the pair; masking changes equality-preserving labels within columns. |
| Interaction | JSON action only: `{"ask": column}` or `{"pick": row}`. Zero-based indices, no repeated query, at most three questions, early pick allowed. |
| Sampling | Freeze temperature, top-p/top-k, output-token cap and seed behavior after development smoke sessions. Record unsupported/non-deterministic seed behavior explicitly. |
| Context | Fresh context per session; same instructions. Measure token count before inference; no silent truncation. |
| Order | Alternate which view runs first across episode IDs. Record the actual order. |
| Cost | At most the program's **20-unit total profiling/paper allowance**, including setup. Stop earlier if measured runtime threatens the paper freeze. No paid API or additional model is required by this protocol. |

Use split 43, a different development target, and at most four sessions for plumbing/prompt debugging. Keep these outside scored results. Any context-size adaptation, shorter JSON serialization or output cap must be selected on development episodes and frozen for both scored views. A restart after a bug fix gets a new run ID; retain the failed run.

The 16-pair sample deliberately follows the existing executable study for speed. It is not a representative random sample of bugs or all 750 conditions. A larger balanced run is future work. Do not expand after seeing promising scored outcomes merely to obtain a favorable result.

## Blinding and execution

The supervisor selects the family, target and split and launches the process. The model receives only the protocol's initial message and subsequent answers. Give it no execution tools, filesystem access, launch command, target index, source/frozen archive or final grading response. Keep private outputs in a separate supervisor process or environment. The frozen archive contains grading information and is safe for public reproducibility only when the agent cannot read it during evaluation.

For each episode, log the complete initial message and every model action and answer. Validate action keys, integer types, range, repeats and budget before passing an action. Reject malformed actions as protocol failures without an unlogged repair attempt. A model-protocol failure counts as unsuccessful in the end-to-end denominator; retain partial transcripts. Hardware/service failures also remain in the denominator, with a separate category. Permit at most one infrastructure retry under the same predeclared rule for every condition; preserve both attempts and report sensitivity to counting the first attempt only.

After the third question, the model must still issue a final pick. Record a timeout or missing pick as failure. At pick time, compare against held-out behaviors in the supervisor; do not send the score back into another scored session. Pair sessions by their frozen sample ID.

The existing control `python -B cognitive_probe.py --check` passed all 750 frozen target/split checks in this review. This verifies entropy's decisions and survivors under masking; it does not validate a future Gemma runner or remove the need for separate leakage checks.

## Baselines and metrics

Run **random informative and entropy on exactly the same 16 targets, frozen matrices, row ordering and three-question limit**. Compute exact expected random outcomes rather than one favorable random seed. Use uniform final choice among consistent candidates for the classical references. Optionally include the existing frugal-tree reference if calculated from the same frozen data. Do not copy the full-benchmark published average into this small-sample comparison.

The required primary table has one row per family and a macro average, with named Gemma, masked Gemma, matched entropy and matched random-informative outcomes. All 16 episodes per condition stay in the denominator.

Record these secondary outcomes: questions used; uninformative asks; repeated or invalid actions; final picks inconsistent with acquired answers; survivor count; input/output tokens; model/tool wall time; and missing sessions. Separate behavior agreement from exact configuration identity. Record answer size and input length; they are cost proxies, not human annotation time.

For named versus masked, report paired wins/losses/ties and the absolute success counts. Inspect errors by family. With 16 pairs on eight curated families, a small difference is descriptive. Do not report episode-level confidence as though all repeated configurations are independent real software tasks. Any repeated presentation run is a robustness diagnostic, not independent new bug evidence.

## Minimal record schema

Use one immutable JSONL record per completed or failed session, plus separate raw transcript files:

```json
{
  "run_id": "paper-gemma-YYYYMMDD-a",
  "sample_id": "csv_fields/19/0",
  "condition": "masked",
  "model_revision": "record exact artifact",
  "data_sha256": "record frozen archive hash",
  "prompt_sha256": "record initial instruction hash",
  "settings": {"temperature": 0, "seed": 2026, "max_output_tokens": 256},
  "status": "planned",
  "questions": null,
  "heldout_exact": null,
  "invalid_actions": null,
  "input_tokens": null,
  "output_tokens": null,
  "elapsed_seconds": null,
  "transcript_path": "relative path within run artifacts"
}
```

The settings above illustrate the schema; they are **not measured or final hyperparameters**. Freeze supported values after development checks. Never convert null planned outcomes into zeros or successes; report planned/unstarted counts separately and include unstarted sessions as unsuccessful in the end-to-end result.

## Optional diagnostic and stop rule

Only after the 32 sessions and matched baselines are complete, and before **10 November 18:00 PKT**, repeat the same sample with one predeclared row permutation and masked-label renaming. Preserve target correspondence. This tests presentation sensitivity and must be reported separately. Skip it if any core run, reproduction or manuscript task remains incomplete.

If Gemma access is unresolved by **8 November 18:00 PKT**, take the resource-only paper path. If a run fails from leakage or an evaluator defect, invalidate it and rerun only if the deadline buffer remains. Do not replace missing measurements with adviser-generated results.

## Later transfer experiment for the repair agent

After the paper submission, compare the simple official-harness baseline with a policy that spends a bounded amount of time on one distinguishing check when two supported candidate patches remain. Record candidate generation cost, test execution and selection in the same total budget. Expected behavior must come from legitimate task evidence; otherwise the probe reveals disagreement only.

Compare final resolved tasks on frozen repository-disjoint folds, including every scheduled task. Keep reference patches/tests evaluator-only, reset state between tasks, and record harness/model/prompt/data hashes. Promote only on useful final-repair evidence at equal budget. This later experiment is a hypothesis about transfer; the paper pilot cannot establish the result in advance.
