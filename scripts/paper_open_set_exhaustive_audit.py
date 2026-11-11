#!/usr/bin/env python3
"""Independent exhaustive tiny-matrix audit of open-set query selection.

Enumerates all 2^(3*3)=512 binary 3-candidate x 3-query matrices,
each of 3 targets, presence/absence, 3 budgets, and 3 policies.
This is a correctness/property audit, NOT a new empirical benchmark.
"""
import importlib.util
from itertools import product
from pathlib import Path

module_path = Path(__file__).with_name("paper_open_set.py")
spec = importlib.util.spec_from_file_location("paper_open_set", module_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def main():
    counts = dict(matrices=0, target_conditions=0, present_false_positives=0,
                  verification_regressions=0, verification_only_detections=0,
                  indistinguishable_absent_cases=0, impossible_detections=0)
    for bits in product((0, 1), repeat=9):
        grid = [list(bits[i*3:(i+1)*3]) for i in range(3)]
        hidden = [(i,) for i in range(3)]
        counts["matrices"] += 1
        for target in range(3):
            counts["target_conditions"] += 1
            available = [i for i in range(3) if i != target]
            same = any(grid[i] == grid[target] for i in available)
            if same:
                counts["indistinguishable_absent_cases"] += 1
            for budget in (1, 2, 3):
                for policy in mod.POLICIES:
                    present = mod.episode(grid, hidden, target, [0, 1, 2], policy, budget)
                    counts["present_false_positives"] += int(present["detected"])
                stop = mod.episode(grid, hidden, target, available, "entropy_stop", budget)
                verify = mod.episode(grid, hidden, target, available, "entropy_verify", budget)
                counts["verification_regressions"] += int(stop["detected"] and not verify["detected"])
                counts["verification_only_detections"] += int(verify["detected"] and not stop["detected"])
                if same and budget == 3:
                    for policy in mod.POLICIES:
                        result = mod.episode(grid, hidden, target, available, policy, budget)
                        counts["impossible_detections"] += int(result["detected"])
    assert counts == dict(matrices=512, target_conditions=1536,
                          present_false_positives=0, verification_regressions=0,
                          verification_only_detections=2088,
                          indistinguishable_absent_cases=360, impossible_detections=0), counts
    print(counts)
    print("Exhaustive small-matrix audit passed")

if __name__ == "__main__":
    main()
