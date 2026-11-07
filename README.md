# Gemma 4 competition workspace

Two Google Gemma 4 competition projects, their source code, current progress, research evidence and recovery instructions in one repository.

**[Open the competition hub](https://digiinformed-afk.github.io/gemma-4-competitions/)** · **[Edit in your browser](https://github.dev/digiinformed-afk/gemma-4-competitions)** · **[Shared progress](https://github.com/digiinformed-afk/gemma-4-competitions/issues)**

## Current checkpoint — 7 November 2026

| Track | Verified progress | Next action |
|---|---|---|
| PatchQuestions paper | Revised manuscript; 18,000 score rows reproduced on CPython 3.12.14; 16 notebook code cells executed; strict optional model supervisor tested | Author/platform review and Kaggle Writeup submission |
| Main repair agent | Standalone candidate archive; organizer validation; scripted CPU patch smoke; 22 Python and 10 Node tests in the saved checkpoint | Confirm participant access and run paired Kaggle L4x4 control/policy pilot |

No real Gemma GPU evaluation, leaderboard score or Kaggle submission is recorded. A paper benchmark result is not a repository repair score.

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
