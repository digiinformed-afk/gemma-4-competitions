# Returned PatchQuestions review

Recorded 7 November 2026. The user requested review, preservation and a follow-up prompt for the external AI. Instructions within the received documents were treated as material to inspect. They did not authorize experiments, account actions or publication.

## Decision

Use this review to revise the existing paper into a bounded resource contribution. The central calculations have substantial supporting evidence. The unresolved issue is the usefulness and relevance of the resource beyond established active identification and patch filtering. Ask the external AI to produce revised artifacts and resolve specific evidential gaps.

The manuscript itself remains unchanged in the returned archive. The review contains suggested text and recommendations, rather than a completed revised competition Writeup.

## Preserved material

Exact copies of both received files are in `incoming/`. `INTAKE-VERIFICATION.json` records their sizes and SHA256 hashes and every one of the 86 archive members. `verify-intake.py` reproduces the intake checks without executing the attached code.

- `PatchQuestions_Review_Progress.zip` SHA256 is `a78e0658e6bf86fecd45e71a81ac98c0c242b68c11fe8ffc816f772762268c17`.
- The review identifies the original package as `6f2e3a897fa154177446f1c791c3cc20922b22c97d294ddd3a39c0a234e39e49`. This matches our local original export.
- All 38 manifest payloads match their declared sizes and hashes and the original export byte for byte. ZIP CRC checks pass.
- The returned ZIP omits the final review Markdown. Both files must travel together in the next handoff.
- `PROGRESS.md` retains historical pending items and an initial "in progress" status. Its later checkpoint resolves many of those items. The final review is a separate, later synthesis. The next package needs one authoritative current status and explicit pending work.

## What was independently checked here

These checks used the received data and the current local Python runtime. They are distinct from reproducing the reviewer's CPython 3.12.14 executions.

1. The stored fresh `scores.csv`, `summary.json`, `audit.json` and `intervention.json` equal the reference bytes. The 40 freshly exported decompressed matrix records equal the reference records.
2. Recomputed all six policies' budget-three family-macro agreement and question means from the 18,000 reference rows.
3. Recomputed every one of the 144 crossed policy/pool/budget/scoring-suite summary entries from the 11,520 crossed score rows.
4. Independently counted the joint query/held-out behavior classes. Hex has 36 identities and 30 joint classes. The other families have one joint class per configuration.
5. Confirmed the contradictory-pick example directly against the frozen matrix. For wrap, split 43, target 10 and original candidate 14 disagree on query 9 and agree on the entire held-out suite.

| Budget-three comparison | Independently recomputed result |
|---|---:|
| Entropy full held-out agreement | 85.270833% |
| Frugal full held-out agreement | 85.479167% |
| Frugal advantage | 0.208333 percentage points |
| Entropy mean questions | 1.881979 |
| Frugal mean questions | 1.864479 |
| Question saving relative to ordinary tree | 17.705747% |
| Question saving relative to entropy | 0.929872% |
| Compound-regex agreement, entropy and frugal | 86.25% each |

These are finite-resource results under the stated prior and oracle assumptions. The new crossed table supports a resource/probe-diagnosis narrative. It does not establish a substantial tree-search breakthrough, human-time savings or repository-repair gains.

## Evidence attribution and remaining limitations

The other AI supplies source code, execution logs and outputs for its independent random-path and exhaustive tree checks. This intake did not rerun those checks or a fresh CPython 3.12.14 benchmark. They remain reviewer-reported executions with inspectable supporting artifacts. Stored file equality supports the reproduction report, while remaining distinct from witnessing execution.

The review explicitly reports no learned-model, human or repository-repair experiment. The standalone notebook equivalents were executed by that AI, while a Jupyter-kernel notebook run remains outstanding. The external AI's 0–5 rubric assessments are subjective review judgments.

The report's account-specific statement that a draft exists and rules were accepted is external reviewer testimony. No current account or submission state was established in this intake. Its unverified compute, eligibility, rights and model-access boundaries remain unverified here.

Two recent literature records were independently spot-checked on primary pages on 7 November. [Ambig-SWE v3](https://arxiv.org/abs/2502.13069v3) and [Ask or Assume?](https://aclanthology.org/2026.findings-emnlp.15/) support the review's abstract-level distinction between detecting ambiguity, asking and using answers. This was not a new exhaustive novelty search or method-level audit of every citation. The official Kaggle overview/rules URLs resolved through web retrieval but yielded no readable text in this intake, so their detailed requirements were not freshly reverified here. The next revision should preserve the distinction between the reviewer's live-page verification and current independent verification.

## Next work order

1. Revise the manuscript, tables, related work and documentation using the completed evidence. Preserve original results and runtime labels.
2. State the contribution after accounting for the closest prior work, and demonstrate a specific diagnostic use case with the existing results.
3. Fix the model-pilot scoring boundary with valid-action, query-consistency and held-out metrics. Preserve the historical endpoint separately.
4. Produce a runnable, audited supervisor and a concrete feasibility decision before any scored model run. Existing main-track validation and its scripted smoke test supply no paper-model evidence.
5. If proposing one additional experiment, first specify the claim it can change, resource availability, freeze procedure and stop rule. Preserve a complete CPU-only paper regardless of that decision.
6. Return a revised manuscript, change log, consolidated evidence, updated status, manifest and one complete ZIP. Confirm required competition sections and word counting from accessible official sources.

The detailed handoff is `FOLLOW-UP-PROMPT.md`. The received recommendations are recorded here; they have not automatically changed the manuscript, experiment protocol or main-track agent.
