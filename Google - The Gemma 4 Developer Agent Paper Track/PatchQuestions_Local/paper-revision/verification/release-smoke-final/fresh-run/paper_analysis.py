"""Rebuild revision tables and selected-transcript costs from the benchmark.

CPU only. Run beside scores.csv. Original benchmark methods are unchanged.
Costs count Unicode code points in selected input and serialized outcome strings,
excluding protocol wrappers, JSON actions, repeated prompt context and thinking.
"""
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
import random
import statistics
import sys

from benchmark import evaluate, families, outcome
from intervention import compound, single, transfer_suite


def trajectory(query, target, policy, budget):
    @lru_cache(None)
    def parts(ids, j):
        groups = defaultdict(list)
        for i in ids:
            groups[query[i][j]].append(i)
        return tuple(tuple(g) for g in groups.values())

    @lru_cache(None)
    def tree(ids, depth):
        best = (1, 0, None)
        if depth:
            for j in range(len(query[0])):
                groups = parts(ids, j)
                if len(groups) < 2:
                    continue
                children = [tree(g, depth - 1) for g in groups]
                leaves = sum(x[0] for x in children)
                cost = len(ids) + sum(x[1] for x in children)
                if leaves > best[0] or leaves == best[0] and cost < best[1]:
                    best = (leaves, cost, j)
        return best

    ids = tuple(range(len(query)))
    remaining = list(range(len(query[0])))
    asked, information = [], []
    for depth in range(budget, 0, -1):
        choices = [j for j in remaining if len(parts(ids, j)) > 1]
        if not choices:
            break
        j = tree(ids, depth)[2] if policy == 'frugal' else max(choices, key=lambda j: -sum(len(g) * math.log2(len(g)) for g in parts(ids, j)))
        information.append(-sum((len(g) / len(ids)) * math.log2(len(g) / len(ids)) for g in parts(ids, j)))
        asked.append(j)
        remaining.remove(j)
        ids = next(g for g in parts(ids, j) if target in g)
    return ids, asked, information


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(Path('scores.csv').open(encoding='utf-8', newline='')))
    policies = ['random', 'random_split', 'diversity', 'entropy', 'lookahead', 'frugal']
    means, by_family = {}, {}
    for p in policies:
        means[p] = {}
        for b in range(4):
            groups = {f: [r for r in rows if r['family'] == f and r['policy'] == p and int(r['budget']) == b] for f in families()}
            means[p][b] = {k: statistics.fmean(statistics.fmean(float(r[k]) for r in group) for group in groups.values()) for k in ['heldout_exact', 'queries_used']}
            if b == 3:
                by_family[p] = {f: statistics.fmean(float(r['heldout_exact']) for r in group) for f, group in groups.items()}
    sensitivity = []
    for f in families():
        difference = statistics.fmean(by_family['frugal'][g] - by_family['entropy'][g] for g in families() if g != f)
        sensitivity.append({'excluded_family': f, 'frugal_minus_entropy_pp': 100 * difference})
    classes = []
    import gzip
    for line in gzip.open(Path(__file__).with_name('frozen_cases.jsonl.gz'), 'rt', encoding='utf-8'):
        c = json.loads(line)
        q = [json.dumps(v, sort_keys=True) for v in c['query_outputs']]
        h = [json.dumps(v, sort_keys=True) for v in c['heldout_outputs']]
        groups = defaultdict(list)
        for i, signature in enumerate(q):
            groups[signature].append(i)
        uniform = sum(sum(n * n for n in Counter(h[i] for i in group).values()) / len(group) for group in groups.values()) / len(q)
        optimal = sum(max(Counter(h[i] for i in group).values()) for group in groups.values()) / len(q)
        classes.append({'family': c['family'], 'split': c['split'], 'configurations': len(q), 'query_classes': len(groups), 'joint_classes': len(set(zip(q, h))), 'all_query_uniform': uniform, 'evaluator_only_majority': optimal})

    config, smoke, universe, impl = families()['regex_search']
    raw, crossed = [], []
    capacities = []
    for pool, replacement in [('original', []), ('single', single), ('compound', compound)]:
        for split in [19, 43, 73, 101, 137]:
            xs = sorted(set(universe) - {smoke})
            random.Random(split).shuffle(xs)
            cut = min(16, len(xs) // 2)
            probes, held = xs[:cut], xs[cut:]
            if replacement:
                probes = probes[:-len(replacement)] + replacement
            query = [tuple(outcome(impl, c, x) for x in probes) for c in config]
            capacities.extend({'pool': pool, 'split': split, 'column': j, 'outcomes': len(Counter(row[j] for row in query)), 'initial_answer_entropy_bits': -sum((n / len(config)) * math.log2(n / len(config)) for n in Counter(row[j] for row in query).values())} for j in range(len(probes)))
            for suite, inputs in [('original_holdout', held), ('transfer', transfer_suite())]:
                hidden = [tuple(outcome(impl, c, x) for x in inputs) for c in config]
                reference = evaluate('regex_search', families()['regex_search'], split, replacement, inputs)
                keyed = {(r[2], r[3], r[4]): r for r in reference}
                for policy in ['entropy', 'frugal']:
                    for budget in [1, 2, 3]:
                        for target in range(len(config)):
                            ids, asked, information = trajectory(query, target, policy, budget)
                            success = sum(hidden[i] == hidden[target] for i in ids) / len(ids)
                            expected = keyed[target, policy, budget]
                            assert abs(success - expected[5]) < 1e-12 and len(asked) == expected[8]
                            raw.append({'suite': suite, 'pool': pool, 'split': split, 'target': target, 'policy': policy, 'budget': budget, 'heldout_exact': success, 'questions': len(asked), 'input_characters': sum(len(probes[j]) for j in asked), 'answer_characters': sum(len(query[target][j]) for j in asked), 'conditional_information_bits': sum(information), 'asked': asked})
        for suite in ['original_holdout', 'transfer']:
            for p in ['entropy', 'frugal']:
                for b in [1, 2, 3]:
                    rs = [r for r in raw if (r['suite'], r['pool'], r['policy'], r['budget']) == (suite, pool, p, b)]
                    crossed.append({'suite': suite, 'pool': pool, 'policy': p, 'budget': b, 'episodes': len(rs), **{k: statistics.fmean(r[k] for r in rs) for k in ['heldout_exact', 'questions', 'input_characters', 'answer_characters', 'conditional_information_bits']}})
    result = {'runtime': sys.version, 'scope': 'Descriptive analysis of existing benchmark and exploratory intervention. No new family or model experiment.', 'score_rows': len(rows), 'score_sha256': hashlib.sha256(Path('scores.csv').read_bytes()).hexdigest(), 'baseline': means, 'per_family_budget3': by_family, 'leave_one_family_out': sensitivity, 'behavior_classes': classes, 'crossed': crossed, 'pool_capacity': capacities, 'cost_definition': __doc__}
    (output / 'revision-results.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    with (output / 'selected-transcripts.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(raw[0]))
        writer.writeheader()
        writer.writerows({**r, 'asked': json.dumps(r['asked'])} for r in raw)
    table = ['# Generated revision tables', '', '| Regex pool / policy | Agreement (%) | Questions | Input characters | Answer characters |', '|---|---:|---:|---:|---:|']
    for r in crossed:
        if r['suite'] == 'original_holdout' and r['budget'] == 3:
            table.append(f"| {r['pool']} / {r['policy']} | {100*r['heldout_exact']:.2f} | {r['questions']:.4f} | {r['input_characters']:.3f} | {r['answer_characters']:.3f} |")
    (output / 'TABLES.md').write_text('\n'.join(table) + '\n', encoding='utf-8')
    print('\n'.join(table))
    return result


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('revision-results'))
    build(parser.parse_args().output)
