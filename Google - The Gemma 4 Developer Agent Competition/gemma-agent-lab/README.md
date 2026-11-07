# Gemma Agent Lab

The paper review is proceeding separately. Main-track code, recovery instructions and the latest measured result are recorded in the [checkpoint](MAIN-TRACK-STATUS.md). The [shared program plan](../../shared/PROGRAM-PLAN.md) covers both competitions.

A buildless research and progress web app for the Google Gemma 4 Developer Agent competition. Research reviewed 6 November 2026.

Compute plan: Colab Pro (200 user-reported compute units) plus Kaggle competition GPUs. See `dist/compute-plan.md` and the compute cards in the blueprint and experiment pages. Allocations are proposed limits, not measured spending or a live balance.

## Repair agent

The [standalone candidate](candidate/agent.yaml) uses one 31B QAT model, six organizer tools and a 4-minute task limit. At 120 tasks this would allocate up to 480 minutes of agent time. Model loading, sandbox setup and operational overhead still need measurement. The four-minute limit, 16 charged calls and decoding parameters are pilot choices.

The [competition-format archive](artifacts/submission.zip) contains the root config, task limits and repair instructions. The local smoke test compiles the contents with the organizer compiler and competition limits. A scripted CPU model drives the real organizer tools on a disposable Git repository through a small local transport. The test reapplies the captured patch to a second checkout and reruns its regression tests. The [result](artifacts/scripted-smoke.json) records the archive hash and runtime versions.

To rebuild and verify in a Python 3.12 environment with the organizer libraries installed, run:

```sh
python scripts/build-submission.py --sample candidate --baseline --require-official-validation --output artifacts/submission.zip
python scripts/smoke-agent.py --archive artifacts/submission.zip --report artifacts/scripted-smoke.json
```

Here `--baseline` preserves the contents of the selected source directory byte for byte. With `candidate` as input this packages our standalone agent. With `sample_submission` as input it packages the organizer control.

## First Kaggle run

Open the [self-contained pilot notebook](artifacts/main-track-pilot.ipynb) as a private Kaggle notebook. Attach the competition data, the public organizer wheelhouse and version 2 of the 31B QAT model. Select L4×4 and turn Internet off. The settings cell defaults to `sample-control`. Save its outputs, then run `sample-policy` in a fresh session with the same inputs. The notebook embeds the scripts and checks the two organizer setup cells before execution. [Organizer starter](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent)

These two arms isolate the effect of appending our repair instructions to the same sample. Each gets 1,800 seconds for setup, inference, verification and teardown across the same three public development tasks. The HTTPX repository is held out. The `standalone` setting runs the packaged candidate's configuration as a separate engineering check. It changes tools, adapters and limits, so it cannot establish the effect of the prompt alone.

After extracting the two result bundles locally, compare the manifests:

```sh
node scripts/compare-runs.mjs sample-control/manifest.json sample-policy/manifest.json
```

The report gives the task IDs gained and lost by the candidate and the resolution counts for each repository. Every scheduled task remains in the denominator. A three-task pilot establishes whether the workflow runs and helps locate failures. Use fresh tasks for later performance conclusions.

Each timed run writes its schedule and commits one result file per completed task. If interrupted, keep the private run directory, including `prepared.json` and `rows/`, and inspect it locally:

```sh
python scripts/run-kaggle.py --recover path/to/interrupted-run --remaining pending.json
```

A fresh diagnostic run can use the pending IDs. Keep its wall time and manifest separate from the interrupted run. Kaggle working files persist according to the notebook session lifecycle. Save the notebook outputs before that session ends.

## Research dashboard

Requires Node.js 18 or newer; no npm dependencies or model API keys.

```powershell
node server.mjs
```

Open http://127.0.0.1:4173. The server exposes only `dist/`. The published private site uses the same static files. Browser-local progress is specific to each origin/device; export and import a JSON backup to move it. No server-side sync, live Kaggle integration or background updates are implemented. External fonts are optional; system fallbacks keep the app usable without them.

## Features

- Competition facts checked against the live page, UTC/PKT deadlines and freshness notes.
- Solution blueprint and draft repair prompt; both explicitly unvalidated in the competition harness.
- 28 annotated resources, search/type/priority filters, bookmarks, reading status and custom resources.
- Cognitive core research page: verified Karpathy interview, related memory/context papers, architecture diagram, four ablations, downloadable brief and task-local evidence-ledger template.
- Manual evaluation logging and editing, honest empty state, descriptive uncertainty and runtime calculator.
- Checkable roadmap, submission checklist, saved notes and validated backup import/export.
- Keyboard navigation, semantic controls and responsive layout.

## Checks

```powershell
node --test tests/core.test.mjs tests/evaluation.test.mjs
python -B -m unittest discover -s tests -p "test_*.py"
node --check dist/app.js
```

## Research utilities

After downloading the official dataset into a private local folder, generate IDs-only repository folds:

```powershell
node scripts/make-folds.mjs 'private-data/tasks.jsonl' 'private-data/folds.json'
```

The output is created only if it does not already exist. Select a fold once, then store its `validation_ids` array in a separate `scheduled-ids.json`. Keep gold patches/test patches outside agent-visible inputs and outside `dist/`.

Log one result row per task using the schema in `dist/experiment-template.jsonl`, replacing the example ID. Summarize against all scheduled IDs:

```powershell
node scripts/summarize.mjs 'private-data/results.jsonl' 'private-data/scheduled-ids.json'
```

Missing tasks count as unstarted and unresolved. This is a result accounting utility, not the Kaggle evaluation harness. Total wall time must be measured independently; task times may omit overhead or overlap. The web app accepts manual aggregate results and separate workspace backups, not raw harness logs.

## Remaining competition validation

The organizer's public wheels and starter are available locally. Validation against the restricted task bundle, the current sample, the full harness guide and a real Gemma GPU run remains open. The signed-out session displays a sign-in and rule-acceptance gate. This candidate has no public-task or leaderboard score. [Competition data](https://www.kaggle.com/competitions/gemma-4-developer-agent/data)

The site is registered as owner-private. Hosting identity is tracked in `.openai/hosting.json`. Keep competition datasets and credentials out of the hosted source repository.
