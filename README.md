# Gemma 4 competition workspace

Two Google Gemma 4 competition projects, their source code, current progress, research evidence and recovery instructions in one repository.

**[Open the resumable control center](https://digiinformed-afk.github.io/gemma-4-competitions/control-center.html)** · **[Open the interactive research atlas](https://digiinformed-afk.github.io/gemma-4-competitions/atlas.html)** · **[Open the competition hub](https://digiinformed-afk.github.io/gemma-4-competitions/)** · **[Edit in your browser](https://github.dev/digiinformed-afk/gemma-4-competitions)** · **[Shared progress](https://github.com/digiinformed-afk/gemma-4-competitions/issues)**

## Resumable control center

`web/control-center.html` is a static, dependency-free research operations dashboard published at `/control-center.html`. It supports separate Main/Paper Track views, version/task/experiment ledgers, comparison warnings, time/tool/compute logs, verification gates, failure triage, research proposals, submission history, local ZIP directory inspection, SHA-256 snapshots, browser autosave, resume briefs, and JSON export/import. All user edits are browser-local and do not update GitHub or Kaggle automatically. Share reviewed changes in GitHub Issues and export a backup between devices. The ZIP inspector is a heuristic browser preflight, not the official evaluator or schema validator. Seeded later V14/HTTPX outcomes are marked tentative until raw trace/hashes are audited.

## Current checkpoint — 12 November 2026

| Track | Verified progress | Next action |
|---|---|---|
| PatchQuestions paper | CPU benchmark reproduced; 64 real Gemma GPU sessions retained and independently regraded; named 3/16, masked 4/16, entropy-assisted 8/16; 20 supervisor tests pass | Revised Kaggle Writeup saved; final submission confirmation pending. See [GPU evidence](paper-gpu/verification/gpu-attempt-368723141/README.md). |
| Main repair agent | Saved matched L4×4 pilot: control, generic policy and Hikmah each resolved 2/3. Newer session reports: V12/control/V14 each 2/3; both Hikmah and control passed one HTTPX case. Raw newest-run audit pending. | Audit latest manifests/traces and exact import controls, then freeze broader matched evaluation with new confirmation tasks |

The earlier real Gemma GPU pilot resolved Requests and Rich; FastAPI remained unresolved. No leaderboard score or final Kaggle submission is recorded. V11 is a documented reconstruction, not a recovered copy of the inaccessible Canvas export; its historical README has no GPU result. Later session reports retain V12, describe slower V14 and a timed-out larger-memory diagnostic, with no clear Hikmah repair advantage. The HTTPX report records Hikmah 603s/31 calls and control 583s/34 calls; its exact raw conditions are pending audit and cannot be merged with the older three-task pilot. HTTPX has now been exposed, so future confirmation needs fresh tasks. [V11 notebook, source and way forward](<Google - The Gemma 4 Developer Agent Competition/gemma-agent-lab/v11/README.md>). A paper benchmark result is not a repository repair score.

Deadlines from the saved 7 November plan: paper **13 November 2026, 04:59 PKT**; main entry/team merger **26 November, 04:59 PKT**; main submission **3 December, 04:59 PKT**. Consult the official Kaggle pages for subsequent changes.

## Repository layout

- `Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local/`: full paper app, canonical manuscript, benchmark code, results, executed notebook and revision evidence.
- `Google - The Gemma 4 Developer Agent Competition/gemma-agent-lab/`: full agent dashboard, candidate, pilot notebook, scripts, tests and smoke evidence.
- `shared/`: coordinated plan, research review, experiment protocol and independent verification.
- `exports/`: supporting paper release packages, writeup and notebook.
- `web/` and `scripts/build-pages.mjs`: combined Pages hub and static adaptations of both apps.
- `docs/SOURCE-MANIFEST.json`: SHA-256 inventory of imported source artifacts.
- `.devcontainer/`: portable Node and Python environment for Codespaces.

## Run and publish

Node 22 or newer, no npm dependencies:

```sh
npm run build
npm test
npm run dev
```

Open `http://127.0.0.1:8080` for the hub, `:3000` for the full paper app and `:4173` for the agent lab. To continue online, follow **[Work from anywhere](docs/WORK-ANYWHERE.md)**. Pages deployment is handled by `.github/workflows/pages.yml`; select **GitHub Actions** under Settings → Pages.

Issues store shared progress across devices. Browser dashboard edits stay local to each origin/device; export/import a backup to move them. The full Node paper app supports its original server features. GitHub Pages provides static research dashboards and downloads; it does not run AI backends or GPU experiments.

Project-owned research artifacts are included. Restricted organizer inputs, installed runtimes, model weights, credentials and browser/runtime state are excluded. Third-party bundled Zod retains its MIT license. No blanket license is asserted over this research or third-party material.

The original workspace README is retained at [docs/ORIGINAL-WORKSPACE-README.md](docs/ORIGINAL-WORKSPACE-README.md). Current track status files supersede older planning statements.
