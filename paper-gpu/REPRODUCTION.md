# Reproduction and evidence index

Run from a clean repository checkout. The historical benchmark sources and published scores are unchanged. Use CPython 3.12.14 for CPU reference measurements. `P` below means `Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local`.

| Manuscript result | Input | Exact command | Output / evidence | Runtime |
|---|---|---|---|---|
| Six policies, budgets 0–3; 18,000 rows | Executable stdlib API families | In a fresh source copy: `python -B benchmark.py > summary.json` | `scores.csv`, `summary.json` | CPython 3.12.14, CPU |
| All-query reference | Same API families | `python -B analyze.py > audit.json` | `audit.json` | CPython 3.12.14, CPU |
| Regex probe design and costs | Original, single and compound probes | `python -B intervention.py > intervention.json`; `python -B paper_analysis.py` | `intervention.json`, `revision-results/TABLES.md`, selected transcripts | CPython 3.12.14, CPU |
| Correct candidate removed | Frozen CPython 3.12 matrices | From repository root: `python -B scripts/paper_open_set.py --output paper-results/open-set.json` | `paper-results/open-set.json`; historical CI 43091180332 | CPython, CPU |
| Noisy binary answers | All 512 binary 3×3 matrices | From repository root: `python -B scripts/paper_noisy_oracle_audit.py --output paper-results/noisy.json` | `paper-results/noisy.json`; historical CI 43116822447 | CPython, CPU |
| Strict model protocol and all four arms | Scripted local transport | `python -m unittest discover -v -s "$P/paper-revision/tests"` | 18 passing tests, GitHub Actions supervisor checks | CPython 3.12, CPU |
| Complete CPU notebook | All embedded modules and frozen matrices | Execute every code cell of `$P/public/project/PatchQuestions.ipynb` in one fresh process/kernel | `paper-gpu/verification/PatchQuestions_CPU_executed.ipynb`, `CPU_VALIDATION.json` | CPython 3.12.14; 14.6 seconds on implementation host |
| Gemma named/masked and controls | Frozen matrices and private matched schedule | Run every cell of `paper-gpu/PatchQuestions_GPU_Pilot.ipynb` in the pinned Python 3.12 GPU environment | Actual attempt recorded in `STATUS.md`; performance pending verified output | Gemma 4 31B QAT w4a16, 4 L4, offline |

For one-command CPU reproduction with captured stdout/stderr, run `python -B "$P/paper-revision/reproduce_paper.py" --output /absolute/new-directory`. The output directory must not exist. For GPU packaging, run `python paper-gpu/build_notebook.py`. For an exported GPU session directory, run `python "$P/public/project/pilot.py" replay /absolute/session-directory > replay.json`. This verifies the frozen-data hash and recomputes every recorded completed grade and aggregate denominator; diagnostics include survivor ambiguity, question entropy and token usage.

The current canonical CPU notebook has cleared outputs. The executed verification copy retains its independently captured outputs. Earlier executed snapshots remain in `paper-revision/verification`. A scripted transport exercise verifies software behavior; only retained real-server transcripts support a Gemma performance claim. An active run keeps the source originally embedded when it started; later replay diagnostics do not silently change that run's model inputs.
