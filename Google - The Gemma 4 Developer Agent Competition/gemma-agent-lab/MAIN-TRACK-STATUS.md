# Main-track checkpoint — 9 November 2026

## Current: V11 reconstructed; GPU evaluation pending

The earlier matched Kaggle comparison completed on four L4 GPUs: control, generic
policy and Hikmah each resolved **2/3**. Requests and Rich passed; FastAPI remained
unresolved. No repair-rate gain is established, and no leaderboard score or final
Kaggle submission is recorded.

[Version 11 source, notebook and next steps](v11/README.md) supersede the older
resume instructions below. V11 reconstructs the documented Canvas plan on the
saved repaired runtime-v2.2 notebook; the original Canvas export was unavailable.
It adds batched call-chain discovery, public API prechecks, larger local budgets,
shorter decoding and separate agent/result archives. Three local CPU checks pass;
**V11 has not run on GPU**. The recovered prior-pilot summary is in
[v11/prior-pilot-summary.json](v11/prior-pilot-summary.json).

Next: run V11 Hikmah on the same three tasks, then matched V11 controls, then a
larger frozen public development set and untouched HTTPX confirmation. Keep this
small tuned pilot distinct from the final hidden-task evaluation.

## Historical checkpoint — 7 November 2026


Updated 7 November 2026. The paper review is with the other AI. Work in this folder can proceed independently.

## Saved

- Confirmed the organizer's Version 3 starter uses the `swegemma` evaluator and the `adk_submission` validator. Its default notebook cell converts the sample to 12B. The distributed sample uses 31B and includes demonstration adapters.
- Checked the workspace, likely files in Downloads, local Kaggle CLI and credential-file presence. No participant bundle or configured CLI was found. The in-app Kaggle data page asks for sign-in and acceptance of the rules. No GPU run has started.
- Saved a standalone 31B single-agent candidate under `candidate/`. Its six tools, instruction include, and generation settings use the schema in the organizer's public `adk_submission` 0.2.13 wheel. The four-minute time cap and 16 charged calls are initial settings for measurement.
- Obtained organizer evaluator 0.2.11 and compiler 0.2.13 from the public wheelhouse. Confirmed the expected transition from patch capture to a text-only final answer in the evaluator source. The manifest comparator and its initial regression tests have been saved.
- Built [submission.zip](artifacts/submission.zip). SHA-256 is `13dfe5ed9d6295b89fbaf9e9ea2e5158e7a52e44bc67e6eb66fdfc4c1803da80`. The organizer's directory validator passed with the competition's own limits. The archive matches the three source files byte for byte.
- The archived agent compiled with Google ADK 1.36.1 and the organizer's real tool registry. A scripted model made six calls, four charged, through a local disposable Git fixture. The captured 202-byte patch applied to another fresh checkout. The failing regression turned green and two tests passed. See the [CPU smoke report](artifacts/scripted-smoke.json).
- **22 Python and 10 Node project tests passed.** The [Kaggle pilot notebook](artifacts/main-track-pilot.ipynb) embeds the scripts and configuration. CPU preflight matched all three task identities in all three arms on synthetic inputs. The embedded source was checked against disk. Private runtime inputs include the pinned notebook and four public organizer wheels in `private-data/organizer/`.
- The GPU runner writes one atomic row per finished task. Its recovery command reads committed rows even if the process dies before the final manifest. The paired comparator rejects changes to the frozen task order, model, relevant environment or wall-time budget.

## Resume

**Next experiment.** Use the private Kaggle pilot on L4×4 with the competition data, 31B QAT model v2 and organizer wheelhouse attached. Run `sample-control` first and `sample-policy` second in fresh sessions. Use the same frozen development schedule and 1,800-second limit for each. Keep HTTPX for a later holdout. Run `standalone` to exercise the separate candidate archive configuration. The [lab README](README.md) includes the comparison and interrupted-run commands.

**Access.** The in-app data viewer requires a signed-in participant who has accepted the rules. Access through the desktop Chrome window could not be verified. The full restricted guide and sample still need review, and Gemma has not run against a competition task. A GPU run and real repair outcome remain pending. [Official data page](https://www.kaggle.com/competitions/gemma-4-developer-agent/data)

**Local reproduction.** On this Windows workspace the Python interpreter and the project-only packages used for the exact archived-agent smoke can be selected in PowerShell:

```powershell
$labPython = "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe"
$env:PYTHONPATH = (Resolve-Path 'private-data/organizer-runtime').Path + ';' + (Resolve-Path 'private-data/validator-env').Path
$env:OTEL_SDK_DISABLED = 'true'
$env:LITELLM_LOCAL_MODEL_COST_MAP = 'True'
& $labPython -B scripts/smoke-agent.py --archive artifacts/submission.zip --report artifacts/scripted-smoke.json
```

From the lab folder, run `python scripts/save-checkpoint.py` after each milestone. It verifies every member and saves a separate content-addressed ZIP under `artifacts/checkpoints/` whenever the source, notebook, archive or reports change. Each ZIP includes this status file, code, tests, candidate and exported artifacts. Private datasets and the installed runtime stay on this machine.

The main-track source is under this folder. Keep account data, competition inputs, evaluator outputs and archives outside the hosted `dist/` folder.
