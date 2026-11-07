# PatchQuestions

The paper is in PatchQuestions_Writeup.md. Open PatchQuestions.ipynb on Kaggle or Jupyter and run all cells in a writable directory. No model, network, GPU or pip install is needed. Use CPython 3.12.14 to reproduce the reference measurements. The notebook materializes its five small Python modules in a dedicated subdirectory and writes scores there.

## Command-line reproduction
Run in this directory:
```sh
python benchmark.py > summary.json
python analyze.py > audit.json
python intervention.py > intervention.json
python verify.py
python export_cases.py
```
scores.csv contains one row per family, split, target configuration, policy and budget. The heldout_exact and probe_exact columns are probabilities over final candidate choice and randomized query paths. survivors and queries_used are expected counts. summary.json contains family-macro averages. audit.json adds the all-probe reference. frozen_cases.jsonl.gz stores the complete CPython 3.12.14 matrices in 40 JSON records, including private grading outputs. cross_version_summary.json is a separate CPython 3.13.5 run.

## Connecting a coding agent
Launch the evaluator as a separate process. Read one JSON object from standard output. Its rows are anonymized candidates and its columns are probe inputs. Send one JSON action per line, e.g. `{"ask":2}`. The reply gives the expected output on that chosen input; discard rows that disagree. After at most three questions, send e.g. `{"pick":0}`. The final reply gives exact held-out agreement and query count. The example below starts one episode:
```sh
python replay.py csv_fields 19 7 --shuffle 824
```
For blind comparisons, let the *evaluator* pick the target and shuffle seed. Expose only standard input/output to the agent. Keep the launching command, private files, target identifier and grading data out of agent context. This protocol is an evaluation interface, not a security sandbox for untrusted code. Use a separate process/container if evaluating an agent with execution tools.

## Kaggle Writeup
Use the H1 as the title, the bold line below it as subtitle, and the text from Abstract onward as the report. If attaching code, import the self-contained notebook and supply its public notebook URL in Project Links. Review author attribution, eligibility, and publication settings before submitting. The package contains no private competition data or account credentials.
