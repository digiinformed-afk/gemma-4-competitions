# Continue from any device

- **Published hub:** https://digiinformed-afk.github.io/gemma-4-competitions/
- **Code, checkpoints and shared plans:** https://github.com/digiinformed-afk/gemma-4-competitions
- **Browser editor:** https://github.dev/digiinformed-afk/gemma-4-competitions
- **Shared progress:** use the repository's Issues tab. Open the Progress update template to record completed work, evidence, next action and blockers. Issues are available on all devices when signed in.

## Run the full applications in a Codespace

Open Code → Codespaces on the repository and choose an existing Codespace, or create one if your GitHub allowance permits. Creating compute may consume your GitHub allowance; no paid compute is started by the published hub.

The development container installs Node 22 and Python 3.12.14. Open a terminal at the repository root and run:

```sh
npm run dev
```

Open the **Ports** panel:

| Port | Application |
|---|---|
| 8080 | Combined static competition hub |
| 3000 | Full PatchQuestions Node app, with server storage, uploads and optional AI |
| 4173 | Gemma Agent Lab |

Keep port visibility **Private**. Do not expose the paper server through a public tunnel. Existing localhost origin checks remain; the deployment copy additionally allows the exact private Codespaces forwarding hostname for its configured port.

The source editor does not run Node or Python; use Codespaces or a local checkout for execution. Kaggle L4x4 and the restricted competition inputs remain separate requirements for the real agent pilot. The included pilot notebook and checkpoint explain those inputs.

## Save and resume

Code and documentation: commit and push changes. GitHub Actions rebuilds and publishes Pages on pushes to `main`.

Shared task updates: use GitHub Issues. The hub loads open issues through GitHub's public API, falling back to the saved next actions when unavailable or rate limited.

The two dashboard workspaces are browser-local in the Pages edition. Use their **Export workspace / Export backup** and **Import backup / Restore backup** controls to transfer edits. They do not synchronize automatically. The full Node paper app saves to its Codespace's ignored `data/` folder; export backups and download uploaded evidence before deleting a Codespace. Workspace JSON does not include uploaded file bytes.

Do not commit API keys, personal backups containing sensitive data, restricted competition datasets, model weights or organizer inputs. Provider keys are needed only for optional features in the full Node app. The Pages edition does not call providers.

## Evidence and current status

The original folder names and contents are preserved, except for the narrow Codespaces hostname allowance in the deployment copy. `SOURCE-MANIFEST.json` records the original imported bytes; a source check permits only that reviewed server change. See the track status files for measurement and submission boundaries. The paper has reproduced CPU evidence and an executed notebook; the main agent has packaging and scripted validation but no real Gemma GPU score. No Kaggle entry is submitted by this repository.

The paper manuscript is canonical in the paper app's `public/project/PatchQuestions_Writeup.md`. The build inserts it into a fresh browser-edition seed, so a first visit starts from the revised manuscript. Existing browser saves are preserved and can be updated with backup/import.

The full Pages artifact includes the published manuscript, benchmark data, supporting packages and candidate agent archive. These are project artifacts; `submission.zip` is not evidence of a scored competition submission.
