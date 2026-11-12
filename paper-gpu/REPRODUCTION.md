# Evidence map

| Manuscript result | Input | Entry point | Evidence |
|---|---|---|---|
| Six policies, budgets 0–3 | Executable stdlib families | public/project/benchmark.py | scores.csv, summary.json, audit.json |
| Regex probe design and costs | Original/single/compound probes | public/project/intervention.py and paper_analysis.py | intervention.json and generated tables |
| Correct candidate removed | Frozen CPython 3.12 matrices | scripts/paper_open_set.py | CI run 43091180332 |
| Noisy binary answers | All 512 binary 3×3 matrices | scripts/paper_noisy_oracle_audit.py | CI run 43116822447 |
| Gemma named/masked and controls | Same frozen matrices, privately sampled targets | paper-gpu/PatchQuestions_GPU_Pilot.ipynb | Pending actual GPU execution |

The public/project paths are under Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local. The updated CPU notebook has cleared outputs pending a fresh execution. Earlier executed snapshots remain in paper-revision/verification. Pilot changes do not alter benchmark.py, the frozen matrices or historical scores.
