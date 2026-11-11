#!/usr/bin/env python3
"""Open-set robustness of PatchQuestions on its frozen CPython 3.12 matrices.

Research question: if the intended API configuration is absent from the
candidate pool, can a limited-budget selector detect that the observed trusted
oracle answers contradict ALL candidates?

This is a synthetic, perfect-oracle, candidate-deletion intervention.
It is NOT a Gemma result, repository repair result, or prospective validation.
Every query choice depends only on the candidate query matrix and earlier
oracle answers. The held-out matrix is used exclusively for evaluation.
"""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import math
from pathlib import Path
import statistics

DATA = Path(__file__).resolve().parents[1] / (
    "Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local/"
    "public/project/frozen_cases.jsonl.gz"
)
POLICIES = ("fixed", "entropy_stop", "entropy_verify")
BUDGETS = (1, 2, 3)


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def entropy(values):
    counts = Counter(values)
    n = len(values)
    return -sum((k / n) * math.log2(k / n) for k in counts.values()) if n else 0.0


def choose(policy, grid, survivors, initial, used):
    remaining = [j for j in range(len(grid[0])) if j not in used]
    if not remaining:
        return None
    if policy == "fixed":
        return remaining[0]
    rank = lambda j: entropy(grid[i][j] for i in survivors)
    best = max(rank(j) for j in remaining)
    if best > 1e-12:
        return next(j for j in remaining if abs(rank(j) - best) < 1e-12)
    if policy == "entropy_stop":
        return None
    # A singleton still needs validation! Choose the most informative
    # remaining column measured on the initially available pool. This is
    # chosen without seeing the hidden target or any held-out outcomes.
    return max(remaining, key=lambda j: entropy(grid[i][j] for i in initial))


def episode(grid, hidden, target, available, policy, budget):
    survivors = list(available)
    used = []
    for _ in range(budget):
        if not survivors:
            break
        j = choose(policy, grid, survivors, available, used)
        if j is None:
            break
        used.append(j)
        answer = grid[target][j]
        survivors = [i for i in survivors if grid[i][j] == answer]
    exact = (sum(hidden[i] == hidden[target] for i in survivors) / len(survivors)) if survivors else 0.0
    return dict(detected=not survivors, questions=len(used),
                heldout_uniform=exact, survivors=len(survivors))


def evaluate(cases):
    records = []
    for case in cases:
        grid = [[canon(x) for x in row] for row in case["query_outputs"]]
        hidden = [tuple(canon(x) for x in row) for row in case["heldout_outputs"]]
        n = len(grid)
        assert len(hidden) == n and len(grid[0]) == len(case["query_inputs"])
        for target in range(n):
            for absent in (False, True):
                available = tuple(i for i in range(n) if not(absent and i == target))
                # Full-pool observational distinguishability is a diagnostic
                # ceiling, NOT information supplied to the query selector.
                indistinguishable = absent and any(grid[i] == grid[target] for i in available)
                for policy in POLICIES:
                    for budget in BUDGETS:
                        result = episode(grid, hidden, target, available, policy, budget)
                        records.append(dict(family=case["family"], split=case["split"],
                            target=target, absent=absent, policy=policy, budget=budget,
                            full_pool_indistinguishable=bool(indistinguishable), **result))
    summary = []
    for policy in POLICIES:
        for budget in BUDGETS:
            for absent in (False, True):
                family_rates = []
                family_details = {}
                for family in sorted({r["family"] for r in records}):
                    rows = [r for r in records if (r["policy"],r["budget"],r["absent"],r["family"])
                        == (policy,budget,absent,family)]
                    stats = dict(
                        episodes=len(rows),
                        detection_rate=statistics.fmean(r["detected"] for r in rows),
                        questions=statistics.fmean(r["questions"] for r in rows),
                        heldout_uniform=statistics.fmean(r["heldout_uniform"] for r in rows),
                        full_pool_detection_ceiling=statistics.fmean(
                            not r["full_pool_indistinguishable"] for r in rows) if absent else None)
                    family_details[family] = stats
                    family_rates.append(stats["detection_rate"])
                summary.append(dict(policy=policy,budget=budget,absent=absent,
                    family_macro_detection=statistics.fmean(family_rates),
                    family_details=family_details))
    return records, summary


def self_test():
    grid = [["0","A","same"],["1","A","same"],["1","B","same"]]
    hidden = [("H0",),("H1",),("H2",)]
    r = episode(grid, hidden, 0, [1,2], "fixed", 3)
    assert r["detected"] and r["questions"] == 1
    r = episode(grid, hidden, 0, [0,1,2], "entropy_stop", 3)
    assert not r["detected"]
    # Absent singleton: a pure information-gain policy stops, verification
    # policy continues and can reject when a later column disagrees.
    grid2 = [["a","different"],["a","same"]]
    stopped = episode(grid2, [("0",),("1",)], 0, [1], "entropy_stop", 2)
    verified = episode(grid2, [("0",),("1",)], 0, [1], "entropy_verify", 2)
    assert not stopped["detected"] and verified["detected"]
    assert verified["questions"] == 2
    print("self-tests passed")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data", type=Path, default=DATA)
    p.add_argument("--output", type=Path, default=Path("paper-results/open-set.json"))
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    self_test()
    if args.self_test:
        return
    raw = args.data.read_bytes()
    cases = [json.loads(line) for line in gzip.decompress(raw).decode("utf-8").splitlines()]
    assert len(cases) == 40, "expected eight families times five splits"
    records, summary = evaluate(cases)
    artifact = dict(
        protocol="open_set_candidate_deletion_v1",
        source="PatchQuestions frozen CPython 3.12 matrix",
        data_sha256=hashlib.sha256(raw).hexdigest(),
        cases=len(cases), target_conditions=sum(len(c["configs"]) for c in cases),
        observation="perfect trusted answers, up to 3 queries; absent state removes target",
        no_leakage="heldout outputs never used for choosing a query",
        limitations=["Artificial removal of correct candidate",
                     "No missing-case prior or abstention utility estimation",
                     "Overlapping curated families and split universes",
                     "No Gemma-model or real repository repair evaluation"],
        row_count=len(records), summary=summary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    for s in summary:
        if s["absent"]:
            print(f"{s['policy']:14} budget={s['budget']} absent_detection_macro="
                  f"{100*s['family_macro_detection']:.2f}%")
    print(f"wrote {args.output} ({len(records)} episodes), data SHA256 {artifact['data_sha256']}")


if __name__ == "__main__":
    main()
