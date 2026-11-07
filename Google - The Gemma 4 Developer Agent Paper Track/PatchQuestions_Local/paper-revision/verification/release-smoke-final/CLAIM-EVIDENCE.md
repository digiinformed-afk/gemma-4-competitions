# Claim-to-evidence map

Paths below refer to the final release root. Source originals and failed attempts remain in the private recovery checkpoints.

| Retained claim | Reproduction / evidence | Boundary |
|---|---|---|
| 150 identities, eight families, five splits, 750 conditions | `paper/benchmark.py:families`, `paper/frozen_cases.jsonl.gz`, `paper/scores.csv` | Curated finite resource; conditions reuse families and inputs. |
| Reference policy scores and question means | `paper/summary.json`, `paper/audit.json`, `evidence/revision-analysis/revision-results.json`; `tools/reproduce_paper.py` | Family-macro expectations under configuration-uniform targets and uniform survivor choice. |
| Exact random expectations | `reviewer/reviewer_audit.py:check_random`, `evidence/local-cpython312-final/reviewer_checks/random_path_validation.json` | 24,000 metric comparisons, 1,015,896 terminal subsets/paths, max absolute error 1.776e-15. |
| Identity/frugal objective | `reviewer/reviewer_audit.py:check_trees`, `evidence/local-cpython312-final/reviewer_checks/tree_enumeration_validation.json` | 4,096 binary 4×3 matrices and four budgets; lexicographic identity/question objective. |
| Behavioral mismatch counterexamples | `evidence/local-cpython312-final/reviewer_checks/objective_counterexamples.json` | Evaluator demonstration; hidden classes never supplied to question policies. |
| Crossed regex results | `reviewer/reviewer_audit.py:crossed_probes`, `evidence/local-cpython312-final/reviewer_checks/crossed_probe_rows.csv`; independent traces in `paper/paper_analysis.py` | Original and constructed scoring suites; exploratory single-family evidence. |
| Answer capacity and selected-transcript costs | `paper/paper_analysis.py`, `evidence/revision-analysis/selected-transcripts.csv`, `revision-results.json` | Initial capacity differs from conditional transcript entropy. Unicode input/serialized-outcome code points exclude protocol/context and human time. |
| Hex duplicates and family sensitivity | `revision-results.json:behavior_classes/leave_one_family_out` | Joint classes use hidden data only for evaluator diagnostics. No real-world target prior inferred. |
| Local same-version reproduction | `evidence/local-cpython312-final/EXECUTION-RECORD.json` | Windows CPython 3.12.14; CSV byte equality, JSON parsed equality. Two failed encoding attempts retained in recovery checkpoints. |
| Jupyter execution | `evidence/notebook/EXECUTION.json`, `paper/PatchQuestions.ipynb` | Fresh kernel execution status, executed cell count and error count recorded. |
| Strict pilot scoring and input secrecy | `paper/pilot.py`, `tests/test_pilot.py`, `evidence/pilot-tests.txt` | 12 deterministic regression checks; mocked transport, no Gemma or endpoint validation. |
| Historical runtime differences | `paper/cross_version_summary.json`, original external-review reference verification | Historical 3.13.5 and separate 3.15.2 remain separate from this run. |

## Conclusions excluded from this release

No model-session outcome, cognitive-mechanism finding, human-time saving, broad task-generalization result, repository-repair benefit or leaderboard score is reported. The resources and executable supervisor can support future studies after their access, sampling and serving controls are met.
