# Independent noisy-oracle toy enumeration — 2026-11-12

**Execution status:** EXECUTED in JavaScript in the ChatGPT tool runtime on 2026-11-12; the committed Python implementation `scripts/paper_noisy_oracle_audit.py` was inspected but **has not been executed** in this run (local Python/container execution unavailable). This is an independently implemented cross-language check, not a Python CI pass.

## Protocol

All 512 binary 3-candidate × 3-query matrices, 3 target identities, present/absent target, three policies (fixed, entropy-stop, entropy-verify), budgets 1–3, and all possible answer-flip schedules were exhaustively enumerated. Every flip has independent probability p in {0, 0.05, 0.15}. Results below use budget 3 and exact weighted expectations, rounded to 4 decimal places.

| Flip probability | Target present: false rejection, fixed | Target present: false rejection, entropy-stop | Target present: false rejection, entropy-verify | Target absent: detection, fixed | Target absent: detection, entropy-stop | Target absent: detection, entropy-verify |
|---|---:|---:|---:|---:|---:|---:|
| 0% | 0.0000 | 0.0000 | 0.0000 | 0.7656 | 0.0000 | 0.7656 |
| 5% | 0.1092 | 0.0000 | 0.1092 | 0.7656 | 0.0000 | 0.7656 |
| 15% | 0.2954 | 0.0000 | 0.2954 | 0.7656 | 0.0000 | 0.7656 |

Mean question counts (target present): fixed 3.0000/2.9327/2.8064, entropy-stop 1.4219/1.4109/1.3891, entropy-verify 3.0000/2.9501/2.8604 for p=0/0.05/0.15 respectively.

**Key interpretation:** Under this *specific symmetric exhaustive toy distribution*, verification can detect 76.56% of missing-target conditions, but at 5% oracle noise it falsely rejects 10.92% of present-target conditions, rising to 29.54% at 15% noise. Entropy-stop makes no contradiction detections in this 3-candidate setup because it stops as soon as survivors become query-indistinguishable; this is an artifact of the small toy design, not a general guarantee. Missing-target detection happens to be noise-invariant here due to symmetry over all possible matrices; do not extrapolate that property.

**Critical limitations:** toy binary matrices, independent symmetric flips, hard elimination, no Bayesian noise handling, no Gemma, no real software repair, no human annotation study. The apparent verification benefit is not cost-adjusted. These are not competition leaderboard results.

**Reproduction:** Run `python scripts/paper_noisy_oracle_audit.py --output paper-results/noisy-oracle-toy.json` in CI, compare all 54 combinations against the independent JavaScript calculation, and preserve machine-readable artifacts. Run `python scripts/paper_open_set_exhaustive_audit.py` in the same job. Only then consider citing the toy stress test in the paper.

**Next priority:** Execute both Python scripts in GitHub Actions, audit the manuscript against submission rules, and confirm actual Kaggle Writeup submission before 2026-11-12 23:59 UTC.
