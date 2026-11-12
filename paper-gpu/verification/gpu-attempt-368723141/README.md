# Verified Kaggle GPU pilot — version 3 / 368723141

This directory preserves the actual scored run, including the original zero-question failures. The source here predates the prospective prompt clarification in the canonical evaluator.

- Kaggle: https://www.kaggle.com/code/digiinformed/patchquestions-gpu-pilot-python-3-12?scriptVersionId=368723141
- Run ID: `patchquestions-20261112-083802`; plan frozen at 2026-11-12 08:43:23 UTC.
- Kaggle reported successful completion in 710.6 seconds, on four NVIDIA L4 GPUs.
- `Kaggle_Output.zip` is the complete, unmodified Download output artifact, SHA-256 `05d5ae6fac7da03e7a4c080ab2a226c353c6a1168682ad2d3514e759f58bd6e3`.
- The nested evidence archive SHA-256 is `6885caed94e7b94fe5182776724a3f9378ffee94ab2a50ba88c414774432a481`; its supplied checksum agrees.
- Actual evaluator SHA-256: `1077b414d63c927f06e9748aa41af5138fba503ee95831af731ad0f56bdf04a3`.
- Frozen data SHA-256: `a60edcc4b000353aaa40b86e8b2380ccd6555d99af8b149f995c22c7d289f70f`.

## Independent local verification

Run from any working directory with Python 3.12 or later:

```sh
python paper-gpu/verification/gpu-attempt-368723141/audit_gpu.py
```

The audit safely extracts the retained archive into temporary storage, checks source/data/plan hashes, reruns the original replay, independently recomputes all 64 matched baseline records, and grades raw legal actions using a separate implementation. It verifies the saved summaries and compares every scored request's logged local token count with actual server usage. This is a CPU regrade of retained GPU evidence; it does not rerun Gemma or independently retokenize prompts.

| Arm | Scheduled/recorded | Strict successes | Completed | Protocol failures |
|---|---:|---:|---:|---:|
| Free named | 16/16 | 3 | 16 | 0 |
| Free masked | 16/16 | 4 | 16 | 0 |
| Entropy-assisted final pick | 16/16 | 8 | 16 | 0 |
| Zero-question named | 16/16 | 0 | 0 | 16 |

All 116 scored requests have equal logged local/server prompt counts. Maximum single-request prompt length was 11,100 tokens. Opening, multi-turn and long-matrix calibration passed with a learned one-token offset (the first calibration was used to determine the offset; the other two checked it). No missing or interrupted sessions occurred. All 48 completed-session grades agree with the separate raw-action regrade. Paired outcomes are named wins 2, masked wins 3, ties 11. Consistent final picks: named 14/16, masked 15/16, assisted 10/16.

The matched CPU uniform-survivor expectations are entropy 87.50% and random-informative 77.7427%; these are expectations on this pilot's targets, not new full-benchmark averages. Mean questions were 1.625 across the free arms and 1.875 for entropy assistance. The assisted interaction supplies CPU-generated question/answer history and asks the model for one final pick, so it differs from free selection.

## Zero-question failure diagnosis and prospective fix

Every zero-question raw response is a Markdown-fenced JSON object. `parse_action` correctly rejects the entire string as `malformed_json`; there is no retry or post-hoc fence stripping in the reported grades. The zero prompt lacks the free prompt's explicit `{"pick": row}` example and no-prose instruction. Thus 0/16 is strict protocol success, not interpretable zero-question selection accuracy. For example, a retained reply is:

````text
```json
{"pick": 1}
```
````

The canonical future-run evaluator now specifies the literal pick schema, zero-based indexing, and no Markdown fences/prose. Two regression tests check that contract and the one-token accounting offset. All 20 supervisor tests passed locally. The rebuilt notebook contains this prospective change; **it has not been rerun on GPU**. It must not be represented as the exact source that produced this version's results. This directory and archive retain the original source unchanged.

No significance, population generalization, human-time saving, cognitive-core validation or repository-repair gain follows from this small convenience pilot. The richer regex probes were not used here. No model weights, organizer wheel binaries, credentials or browser state are included.
