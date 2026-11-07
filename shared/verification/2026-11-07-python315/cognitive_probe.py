"""Replay frozen evidence with semantic labels visible or masked. Python standard library."""
import argparse
from collections import Counter
import gzip
import json
import math
from pathlib import Path
import random


def mask(grid):
    result = [[] for row in grid]
    for column in zip(*grid):
        labels = {}
        for row, value in enumerate(column):
            result[row].append(labels.setdefault(value, f"v{len(labels)}"))
    return result


def choose(grid, survivors, remaining):
    def entropy(j):
        counts = Counter(grid[i][j] for i in survivors)
        return -sum((n / len(survivors)) * math.log2(n / len(survivors)) for n in counts.values())
    best = max(remaining, key=entropy)
    return best if entropy(best) > 0 else None


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--family', default='csv_fields')
    parser.add_argument('--split', type=int, default=19)
    parser.add_argument('--target', type=int, default=0)
    parser.add_argument('--view', choices=['named', 'masked'], default='masked')
    args = parser.parse_args()
    with gzip.open(Path(__file__).with_name('frozen_cases.jsonl.gz'), 'rt') as f:
        cases = [json.loads(line) for line in f]
    count = 0
    for case in cases:
        if not args.check and (case['family'], case['split']) != (args.family, args.split):
            continue
        order = list(range(len(case['configs'])))
        random.Random(2026 + case['split']).shuffle(order)
        named = [[json.dumps(v) for v in case['query_outputs'][i]] for i in order]
        masked = mask(named)
        for target in range(len(order)) if args.check else [args.target]:
            key = order.index(target)
            if args.check:
                survivors = list(range(len(order)))
                remaining = list(range(len(named[0])))
                for _ in range(3):
                    j = choose(named, survivors, remaining)
                    assert j == choose(masked, survivors, remaining)
                    if j is None:
                        break
                    remaining.remove(j)
                    survivors = [i for i in survivors if named[i][j] == named[key][j]]
                    assert survivors == [i for i in range(len(order)) if all(masked[i][q] == masked[key][q] for q in set(range(len(named[0]))) - set(remaining))]
                count += 1
                continue
            grid = named if args.view == 'named' else masked
            print(json.dumps(dict(inputs=case['query_inputs'] if args.view=='named' else list(range(len(grid[0]))), outputs=grid, budget=3, instructions='Send {"ask": column} or {"pick": row}. Indices start at zero.')), flush=True)
            asked = set()
            while True:
                action = json.loads(input())
                if set(action)=={'pick'} and type(action['pick']) is int and 0<=action['pick']<len(order):
                    print(json.dumps(dict(heldout_exact=case['heldout_outputs'][order[action['pick']]]==case['heldout_outputs'][target], questions=len(asked))))
                    return
                j = action.get('ask')
                if set(action)!={'ask'} or type(j) is not int or j in asked or len(asked)>=3 or not 0<=j<len(grid[0]):
                    raise ValueError('Invalid action')
                asked.add(j)
                print(json.dumps(dict(answer=grid[key][j])), flush=True)
    if args.check:
        print(f'{count} target-split episodes passed the paired entropy decision and survivor checks.')
    else:
        parser.error('Unknown family or split')


if __name__ == '__main__':
    run()
