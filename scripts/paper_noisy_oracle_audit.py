#!/usr/bin/env python3
"""Exact noisy-oracle stress test on all 3x3 binary behavior matrices.

This is a finite toy protocol audit, NOT a Gemma experiment or a realistic
estimate of annotation noise. Every target and every possible oracle flip
pattern is enumerated; no random seed or Monte Carlo variance is involved.
"""
from collections import Counter
from itertools import product
from math import log2

POLICIES = ("fixed", "entropy_stop", "entropy_verify")
RATES = (0.0, 0.05, 0.15)

def entropy(values):
    c = Counter(values)
    n = len(values)
    return -sum((v/n)*log2(v/n) for v in c.values()) if n else 0.0

def run(grid, target, available, policy, budget, flips):
    survivors, used = list(available), []
    for _ in range(budget):
        if not survivors:
            break
        remaining = [j for j in range(3) if j not in used]
        if not remaining:
            break
        if policy == "fixed":
            j = remaining[0]
        else:
            gains = [entropy([grid[i][k] for i in survivors]) for k in remaining]
            top = max(gains)
            if top > 1e-12:
                j = remaining[gains.index(top)]
            elif policy == "entropy_stop":
                break
            else:
                j = max(remaining, key=lambda k: entropy([grid[i][k] for i in available]))
        used.append(j)
        # Flip schedule is indexed by QUERY POSITION, not by query column.
        observed = grid[target][j] ^ flips[len(used)-1]
        survivors = [i for i in survivors if grid[i][j] == observed]
    return {"contradiction": not survivors, "questions": len(used),
            "target_survives": target in survivors}

def main():
    import json
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("paper-results/noisy-oracle-toy.json"))
    args = parser.parse_args()
    totals = {}
    for noise in RATES:
        for absent in (False, True):
            for policy in POLICIES:
                for budget in (1, 2, 3):
                    weight = contradiction = questions = retained = 0.0
                    for bits in product((0, 1), repeat=9):
                        grid = [bits[i*3:(i+1)*3] for i in range(3)]
                        for target in range(3):
                            available = [i for i in range(3) if not(absent and i == target)]
                            for flips in product((0, 1), repeat=budget):
                                prob = 1.0
                                for flip in flips:
                                    prob *= noise if flip else (1.0-noise)
                                if prob == 0:
                                    continue
                                r = run(grid,target,available,policy,budget,flips)
                                weight += prob
                                contradiction += prob*r["contradiction"]
                                questions += prob*r["questions"]
                                retained += prob*r["target_survives"]
                    key = f"noise={noise}|absent={absent}|policy={policy}|budget={budget}"
                    totals[key] = dict(conditions=1536, contradiction_rate=contradiction/weight,
                        mean_questions=questions/weight, target_survival_rate=retained/weight)
    assert all(totals[f"noise=0.0|absent=False|policy={p}|budget={b}"]["contradiction_rate"] == 0
               for p in POLICIES for b in (1,2,3))
    result = {"protocol":"exhaustive_binary_toy_noisy_oracle_v1",
              "matrices":512, "target_conditions":1536, "noise_rates":RATES,
              "flip_model":"independent Bernoulli bit flip on each acquired binary oracle answer",
              "method":"exact weighted enumeration, including all query-order noise sequences",
              "limitations":["Toy 3x3 binary matrices; not real software tasks",
                "Noise is independent, symmetric, and known only to evaluator",
                "Hard elimination only; no Bayesian noisy-label policy",
                "Absence detection under noise is not trustworthy without false-positive accounting",
                "No Gemma or human study"],"results":totals}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\\n",encoding="utf-8")
    for noise in RATES:
        for absent in (False, True):
            for policy in POLICIES:
                k=f"noise={noise}|absent={absent}|policy={policy}|budget=3"
                print(k, f"contradiction={totals[k]['contradiction_rate']:.6f}",
                      f"questions={totals[k]['mean_questions']:.4f}")
    print("Wrote", args.output)

if __name__ == "__main__":
    main()
