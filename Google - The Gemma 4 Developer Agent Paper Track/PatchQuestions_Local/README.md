# PatchQuestions Research Lab — local edition

**First priority in the shared Gemma program:** follow the [combined execution plan](../../shared/PROGRAM-PLAN.md), [research review](../../shared/RESEARCH-REVIEW.md) and [bounded Gemma pilot protocol](../../shared/EXPERIMENT-PROTOCOL.md). The paper is due 13 November 2026 at 04:59 PKT. Existing benchmark results remain reference artifacts; planned model experiments are not completed results.

## Start on Windows

1. Install **Node.js 22 or newer** from https://nodejs.org/ if it is not already installed.
2. Extract this entire ZIP to a normal writable folder, for example Documents\PatchQuestions_Local. Do not run it from inside the ZIP.
3. Double-click **Start_Windows.bat**. Keep its terminal window open.
4. Open **http://127.0.0.1:3000** in your browser.

There is no npm install, build step, ChatGPT sign-in or cloud hosting requirement. All application dependencies are included. Node.js itself is not included.

macOS/Linux: run `sh start.sh` from the extracted folder. Alternatively, on any platform run `node server.mjs` or `npm start`.

Stop with Ctrl+C in the terminal. Restart using the same launcher and folder to resume your saved work. Run only one server per data folder. If port 3000 is busy, close its other server, or set PORT before starting (Windows Command Prompt: `set PORT=3001`, then `node server.mjs`).

## Included

- The original dashboard, 34 curated research sources, source notes and reading lists.
- Sprint planner, experiment tracker, baseline analysis and CSV imports.
- Interactive question-selection sandbox, paper workspace, readiness gates and backup/restore.
- AI adviser and model discovery for Gemini, OpenAI, Anthropic, Groq and OpenRouter.
- Crossref paper discovery and original research files, notebook, benchmark code and frozen results under `public/project/`.

The research library contains summaries and links; it does not contain downloaded copies of every linked paper or video. Internet is needed for external sources, paper discovery and API requests. The dashboard, bundled resources, editing, imports and analysis work locally without internet.

## Activate the AI adviser

Open **Model & workspace settings**. Choose a provider, paste your own API key, fetch available models, then select or enter a supported text model ID. Ask a question in the adviser. Provider API usage is billed by your provider. The key stays in page memory and is sent to your local server and chosen provider; it is not saved in workspace files or backups. Re-enter it after reloading. No live provider response has been verified with your key.

## Move your work from the hosted app

The included starting state is the original project seed, not a live copy of your private hosted database. To bring over later edits:

1. In the hosted app, go to settings and **Export backup**.
2. In this local app, go to settings and **Restore backup**, then select that JSON file.
3. Wait for **All changes saved**.
4. Download any separately uploaded evidence from the hosted app and upload it again locally. Workspace JSON does not include uploaded file bytes, and old file download IDs do not transfer.

Local changes and hosted changes are independent. Nothing automatically submits to Kaggle or synchronizes with the hosted app.

## Data and backups

The server creates a `data/` folder beside `server.mjs` on first launch:

- `workspace.json`: saved tasks, notes, experiments, manuscript, reading progress and conversations.
- `workspace.json.bak`: the previous successful workspace version.
- `files.json` and `uploads/`: uploaded evidence index and file bytes.

Use **Export backup** for workspace-only backups. For a complete backup, stop the server and copy the whole `data/` folder. Keep it with the app when moving computers. Wait for **All changes saved** before closing the page. Do not edit data files while the app is running.

The app binds to **127.0.0.1 only**. It is intended for your own computer, has no local login, and must not be exposed through a public tunnel or network proxy. Anyone using the same computer account can access its local data.

## Verification and maintenance

Run `npm test` to check workspace loading/saving, restart persistence, revision conflicts, backups, uploads/downloads, static files, request protection and AI adapter request/response handling with simulated provider responses. Tests use a temporary folder and do not touch your research data.

The UI and original measurements were retained from the deployed app. Local packaging changes replace hosted storage with atomic local file writes and a localhost server. The deadline and curated sources retain their original project dates; consult Kaggle for current competition status.

`server/` contains the local backend and bundled Zod 3.25.76 validation library with its MIT license. `public/` contains the app and project resources. No API credentials or hosting credentials are included.
