# Hikmah Version 11 — GPU test pending

Prepared **9 November 2026**. This is an executable reconstruction of the documented
Version 11 plan on the saved repaired runtime-v2.2 notebook. The original
`hikmah_v11_upgrade_cells.py` Canvas export was not accessible in this session;
these files must not be described as a byte-identical recovery of it.

- [Ready-to-run notebook](hikmah-main-track-pilot-v11.ipynb)
- [Reconstruction script](hikmah_v11_upgrade_cells.py)
- [CPU checks](test_v11.py)
- [Earlier result summary](prior-pilot-summary.json)

## What changed

| Setting | Saved repaired pilot | Version 11 |
|---|---:|---:|
| Task time | 6 minutes | 10 minutes |
| Tool calls | 40 | 65 |
| Turns | 70 | 95 |
| Command timeout | 60 seconds | 90 seconds |
| Public verification timeout | 300 seconds | 300 seconds |
| Temperature / top-p | 0.20 / 0.95 | 0.15 / 0.90 |
| Output token cap | 8,192 | 2,560 |
| Thinking allowance | 4,096 | 1,024 |
| Cold run cap | 2,700 seconds | 4,200 seconds |

The 1,024-token thinking allowance and 4,200-second cold cap are implementation
choices made in this reconstruction: thinking must fit inside the output cap,
and cold startup plus three longer tasks and verification need headroom.
Budget and sampling changes apply equally to all three arms. These are **local
evaluation settings**, not established final competition limits.

Hikmah's added policy batches symbol searches, traces public-to-internal API wiring,
and checks imports/signatures before pytest. It reserves four status checks and
the last 60 seconds for finishing. These are prompt instructions, not hard
enforcement or extra harness allowances. No FastAPI solution is hardcoded.

## Run next on Kaggle

1. Import the V11 notebook into a fresh **private** session. Select original
   Python 3.12, **L4 ×4**, and Internet off.
2. Attach competition data, the organizer wheelhouse, official **31B IT QAT
   W4A16 CT model v2**, and the private Hikmah Runtime Wheelhouse.
   The earlier attached wheelhouse supplies **Pygments only**. Also attach the
   other five wheels from `Hikmah_Runtime_Repair_v2.zip/source/extra-wheels/`
   (asttokens, dirty_equals, executing, inline_snapshot and starlette), or extend
   your private wheelhouse to include all six. All six filenames/digests are
   embedded; wheel bytes are not. The notebook fails if its required inputs or frozen task identities differ.
3. Run the default `sample-hikmah` arm on `requests_7309`, `rich_3130`, and
   `fastapi_14262`. Inspect the actual traces, test outcomes and patch capture.
   **3/3 is the debugging target**, not a promised result.
4. Run the export cell and download both the private result ZIP and
   `/kaggle/working/submission.zip`. The submission ZIP has `agent.yaml` at its
   root, excludes local `eval_config` and logs, and is copied into `RUN_DIR`.
   Packaging does not submit anything to Kaggle. Before final upload, run the
   official validator in the competition environment and verify the allowed
   settings, structure and inference constraints.
5. Rerun `sample-control` and `sample-policy` in fresh sessions with identical
   V11 settings. Preserve manifests, prompts, task results, failures, wall time,
   tool counts and exact agent archives. Compare these matched V11 runs; the
   old smaller-budget run is a historical reference, not a fair policy ablation.

The previous saved matched comparison resolved **2/3 in every arm**. Requests and
Rich passed; FastAPI remained unresolved after partial API wiring and timeout.
Hikmah's successful patches were cleaner, but no success-rate improvement was shown.
Prior conversation reports also describe Versions 8–10 as 2/3; the recovered
evidence labels itself runtime-v2.2 and is not relabeled as a V11 result.

## Way forward after the smoke test

- If FastAPI still fails, classify the actual failure as discovery, incomplete
  call-chain wiring, API/import failure, test failure, or budget exhaustion.
  Fix the general workflow implicated by that evidence and repeat the smoke test.
- Once stable, freeze a larger development set from the **129 public problems**,
  stratified across repositories. Keep HTTPX untouched for confirmation. Repeated
  tuning on the three pilot tasks does not establish performance on unseen bugs.
- Run matched control/generic/Hikmah comparisons with multiple repeats where
  affordable. Report paired outcomes, variance, wall time and tool usage. Separate
  the effects of the policy, sampling and extra budget through follow-up ablations.
- Freeze the chosen agent, validate it under the official final settings, then
  package and submit for hidden-task evaluation. A public pilot score is not a
  leaderboard score. Use the best measured configuration, including the baseline
  if Hikmah fails to improve broader results.
- For the paper, retain the bounded evidence claim: the recorded comparison shows
  no repair-rate gain. New V11 findings belong in the paper only after execution
  and verification; do not delay its final review for an open-ended agent campaign.

## Local verification and reproduction

The three CPU tests cover all arms' preparation with equal settings, clean notebook
source without embedded wheels, and separating private evidence from agent ZIPs.
Task selection and command invocation are mocked in preparation checks. They do
not test model loading, the real evaluator, GPU inference or repair quality.

```sh
python3 -m unittest discover -s v11 -p test_v11.py -v
python3 v11/hikmah_v11_upgrade_cells.py \
  --baseline /path/to/hikmah-main-track-pilot-v2.ipynb \
  --output /path/to/new-v11.ipynb
```

Use the repaired notebook from `Hikmah_Runtime_Repair_v2.zip`, version 5, as baseline.
The reconstruction clears execution outputs and retains the repaired worker,
checkout-first imports, pinned organizer setup and runtime preflight. The public
starter cells retain their bundled Apache 2.0 license. Competition inputs, weights,
private traces and third-party wheel binaries are excluded from this update.
