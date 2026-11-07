"""Independent review diagnostics. Never writes into reference/.

Run: python -B reviewer_audit.py
Uses the provided CPython 3.12.14 frozen matrices and original scores.
"""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
import csv, gzip, hashlib, json, math, random, statistics, sys, time

ROOT = Path(__file__).resolve().parent
REF = ROOT / 'reference' / 'paper'
OUT = ROOT / 'reviewer_checks'
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / 'run_cpython_3_12_14'))
import benchmark
import intervention

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2))
    print(name, flush=True)

def canon(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=True)

CASES = [json.loads(s) for s in gzip.open(REF / 'frozen_cases.jsonl.gz', 'rt')]
ROWS = list(csv.DictReader((REF / 'scores.csv').open()))
KEYED = {(r['family'], int(r['split']), int(r['target']), r['policy'], int(r['budget'])):
         tuple(float(r[k]) for k in ['heldout_exact','probe_exact','survivors','queries_used']) for r in ROWS}

def grids(case):
    return tuple(tuple(map(canon,r)) for r in case['query_outputs']), tuple(tuple(map(canon,r)) for r in case['heldout_outputs'])

def brute_paths(case, target, budget, informative):
    """No DP: uniform unordered subsets for random, explicit weighted paths otherwise."""
    q,h = grids(case)
    n,m = len(q),len(q[0])
    full = (1 << n)-1
    same_q = sum(1 << i for i in range(n) if q[i] == q[target])
    same_h = sum(1 << i for i in range(n) if h[i] == h[target])
    target_answers = [sum(1 << i for i in range(n) if q[i][j] == q[target][j]) for j in range(m)]
    total = [Fraction(0) for _ in range(4)]
    terminals = 0
    # Terminal states can repeat across paths; aggregate weights only after enumerating paths.
    terminal_weights = defaultdict(Fraction)
    if not informative:
        d = min(budget,m)
        for js in combinations(range(m),d):
            mask = full
            for j in js: mask &= target_answers[j]
            terminal_weights[mask,d] += Fraction(1,math.comb(m,d))
            terminals += 1
    else:
        stack = [(full,tuple(range(m)),budget,Fraction(1),0)]
        while stack:
            mask,available,left,weight,used = stack.pop()
            choices = [j for j in available if mask & target_answers[j] != mask] if left else []
            if not choices:
                terminal_weights[mask,used] += weight
                terminals += 1
                continue
            for j in choices:
                stack.append((mask & target_answers[j],tuple(k for k in available if k!=j),left-1,weight/len(choices),used+1))
    assert sum(terminal_weights.values()) == 1
    for (mask,used),weight in terminal_weights.items():
        size = mask.bit_count()
        values = [Fraction((mask & same_h).bit_count(),size),Fraction((mask & same_q).bit_count(),size),Fraction(size),Fraction(used)]
        for k,v in enumerate(values):total[k] += weight*v
    return total,terminals

def check_random():
    started=time.perf_counter(); comparisons=terminals=0;maximum=0.0
    for case in CASES:
        for target in range(len(case['configs'])):
            for method,informative in [('random',False),('random_split',True)]:
                for budget in range(4):
                    values,count=brute_paths(case,target,budget,informative)
                    expected=KEYED[case['family'],case['split'],target,method,budget]
                    for actual,want in zip(values,expected):
                        error=abs(float(actual)-want);maximum=max(maximum,error)
                        assert error<1e-12,(case['family'],case['split'],target,method,budget,actual,want)
                        comparisons+=1
                    terminals+=count
        print('random paths verified',case['family'],case['split'],flush=True)
    save('random_path_validation.json',dict(metric_comparisons=comparisons,terminal_subsets_or_paths=terminals,max_absolute_error=maximum,wall_seconds=time.perf_counter()-started))

def explicit_trees(q, ids, remaining, depth, used=0):
    """Enumerate full terminal leaf/depth lists, including early stopping. No memoization."""
    yield ((ids,used),)
    if not depth:return
    for j in remaining:
        groups=defaultdict(list)
        for i in ids:groups[q[i][j]].append(i)
        if len(groups)<2:continue
        children=[list(explicit_trees(q,tuple(g),tuple(k for k in remaining if k!=j),depth-1,used+1)) for g in groups.values()]
        for alternative in product(*children):
            yield tuple(leaf for child in alternative for leaf in child)

def synthetic_spec(q,h):
    # evaluate() splits 2*m inputs into m query and m hidden columns.
    m=len(q[0]);xs=[f'x{j}' for j in range(2*m)];random.Random(19).shuffle(xs)
    table={x:tuple(q[i][j] for i in range(len(q))) for j,x in enumerate(xs[:m])}
    for j,x in enumerate(xs[m:]):table[x]=tuple(h[i][j%len(h[0])] for i in range(len(q)))
    def impl(i,x):return 'same smoke' if x=='smoke' else table[x][i]
    return (list(range(len(q))),'smoke',xs,impl)

def check_trees():
    started=time.perf_counter();fixtures=0
    for bits in product(range(2),repeat=12):
        q=tuple(tuple(bits[i*3:(i+1)*3]) for i in range(4));h=tuple((i,) for i in range(4))
        rows=benchmark.evaluate('synthetic',synthetic_spec(q,h),19)
        for budget in range(4):
            alternatives=list(explicit_trees(q,tuple(range(4)),tuple(range(3)),budget))
            leaves=max(map(len,alternatives))
            cost=min(sum(len(ids)*depth for ids,depth in t) for t in alternatives if len(t)==leaves)
            frugal=[r for r in rows if r[3]=='frugal' and r[4]==budget]
            regular=[r for r in rows if r[3]=='lookahead' and r[4]==budget]
            assert abs(sum(r[5] for r in frugal)-leaves)<1e-12
            assert sum(r[8] for r in frugal)==cost
            assert abs(sum(r[5] for r in regular)-leaves)<1e-12
        fixtures+=1
    save('tree_enumeration_validation.json',dict(binary_4_by_3_matrices=fixtures,budgets=[0,1,2,3],tree_objective_checks=fixtures*4,wall_seconds=time.perf_counter()-started))

def metrics_and_redundancy():
    out={};duplicates=[]
    for policy in ['random','random_split','diversity','entropy','lookahead','frugal']:
        selected=[r for r in ROWS if r['policy']==policy and int(r['budget'])==3]
        by=defaultdict(list)
        for r in selected:by[r['family']].append(r)
        out[policy]={k:statistics.fmean(statistics.fmean(float(r[k]) for r in rs) for rs in by.values()) for k in ['heldout_exact','queries_used','survivors','probe_exact']}
        out[policy]['target_weighted_heldout']=statistics.fmean(float(r['heldout_exact']) for r in selected)
    regular=out['lookahead']['queries_used'];frugal=out['frugal']['queries_used'];entropy=out['entropy']['queries_used']
    effects={'tree_vs_entropy_pp':100*(out['frugal']['heldout_exact']-out['entropy']['heldout_exact']),
             'tree_vs_random_informative_pp':100*(out['frugal']['heldout_exact']-out['random_split']['heldout_exact']),
             'random_informative_vs_random_pp':100*(out['random_split']['heldout_exact']-out['random']['heldout_exact']),
             'frugal_vs_tree_questions_absolute':regular-frugal,'frugal_vs_tree_questions_relative':(regular-frugal)/regular,
             'frugal_vs_entropy_questions_absolute':entropy-frugal,'frugal_vs_entropy_questions_relative':(entropy-frugal)/entropy}
    fams=list(benchmark.families())
    leave=[]
    for drop in fams:
        vals={}
        for policy in ['frugal','entropy','random_split']:
            vals[policy]=statistics.fmean(statistics.fmean(float(r['heldout_exact']) for r in ROWS if r['family']==f and r['policy']==policy and int(r['budget'])==3) for f in fams if f!=drop)
        leave.append(dict(dropped_family=drop,tree_entropy_pp=100*(vals['frugal']-vals['entropy']),tree_random_informative_pp=100*(vals['frugal']-vals['random_split'])))
    for c in CASES:
        q,h=grids(c);n=len(q);bins=defaultdict(list)
        for i,row in enumerate(q):bins[row].append(i)
        uniform=sum(sum(z*z for z in Counter(h[i] for i in ids).values())/len(ids) for ids in bins.values())/n
        majority=sum(max(Counter(h[i] for i in ids).values()) for ids in bins.values())/n
        duplicates.append(dict(family=c['family'],split=c['split'],N=n,query_classes=len(bins),heldout_classes=len(set(h)),joint_classes=len(set(zip(q,h))),all_queries_uniform=uniform,evaluator_only_hidden_majority=majority))
    save('effects_redundancy_sensitivity.json',dict(budget3=out,effects=effects,leave_one_family_out=leave,classes=duplicates))

def crossed_probes():
    results=[];raw=[];complexity=[]
    for transfer in [False,True]:
        for label,replacements in [('original',[]),('single',intervention.single),('compound',intervention.compound)]:
            rows=[r for seed in [19,43,73,101,137] for r in benchmark.evaluate('regex_search',benchmark.families()['regex_search'],seed,replacements,intervention.transfer_suite() if transfer else None)]
            for policy in ['random','random_split','diversity','entropy','lookahead','frugal']:
                for b in [0,1,2,3]:
                    rs=[r for r in rows if r[3]==policy and r[4]==b]
                    results.append(dict(scoring_suite='transfer' if transfer else 'original_holdout',pool=label,policy=policy,budget=b,heldout_exact=statistics.fmean(r[5] for r in rs),queries=statistics.fmean(r[8] for r in rs)))
            raw.extend([['transfer' if transfer else 'original_holdout',label]+r for r in rows])
    configs,smoke,universe,impl=benchmark.families()['regex_search']
    for label,probes in [('original_universe',sorted(set(universe)-{smoke})),('single',intervention.single),('compound',intervention.compound)]:
        for x in probes:
            vals=[benchmark.outcome(impl,c,x) for c in configs];freq=Counter(vals)
            complexity.append(dict(pool=label,input=x,input_characters=len(x),distinct_answers=len(freq),answer_entropy_bits=-sum((v/len(vals))*math.log2(v/len(vals)) for v in freq.values()),mean_serialized_answer_characters=statistics.fmean(map(len,vals)),max_serialized_answer_characters=max(map(len,vals))))
    with (OUT/'crossed_probe_rows.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['scoring_suite','pool','family','split','target','policy','budget','heldout_exact','probe_exact','survivors','queries_used']);w.writerows(raw)
    save('crossed_probe_results.json',dict(results=results,query_complexity=complexity))

def matched_pilot():
    selected=[r for r in ROWS if int(r['split'])==19 and int(r['target']) in [0,1] and int(r['budget'])==3]
    # Source queries have identical pool ordering/equality partitions to frozen cases verified by fresh export.
    report={}
    for family in benchmark.families():
        report[family]={method:dict(heldout_exact=statistics.fmean(float(r['heldout_exact']) for r in selected if r['family']==family and r['policy']==method),queries=statistics.fmean(float(r['queries_used']) for r in selected if r['family']==family and r['policy']==method)) for method in ['random','random_split','entropy','lookahead','frugal']}
    macro={method:{k:statistics.fmean(report[f][method][k] for f in report) for k in ['heldout_exact','queries']} for method in ['random','random_split','entropy','lookahead','frugal']}
    presentations=[]
    for c in CASES:
        if c['split']!=19:continue
        order=list(range(len(c['configs'])));random.Random(2026+c['split']).shuffle(order)
        presentations.append(dict(family=c['family'],N=len(order),target0_display_row=order.index(0),target1_display_row=order.index(1),configs0and1=c['configs'][:2]))
    save('matched_pilot_baselines.json',dict(per_family=report,macro=macro,presentation=presentations,warning='Classical exact expectations only; no model sessions. Same original query order, row permutation does not affect these tie rules or uniform final selection.'))

def counterexamples():
    out=[]
    for label,q,h in [('minimal_tie',[(0,0),(1,0),(0,1)],[(0,),(0,),(1,)]),('strict_conflict',[(0,0),(1,0),(0,1),(2,1)],[(0,),(0,),(1,),(1,)])]:
        rows=benchmark.evaluate(label,synthetic_spec(q,h),19)
        values=[]
        for j in range(2):
            bins=defaultdict(list)
            for i,row in enumerate(q):bins[row[j]].append(i)
            behavioral=sum(sum(z*z for z in Counter(h[i] for i in ids).values())/len(ids) for ids in bins.values())/len(q)
            values.append(dict(query=j,leaves=len(bins),identity=len(bins)/len(q),behavioral=behavioral))
        out.append(dict(label=label,query=q,heldout=h,query_metrics=values,package_frugal_1=statistics.fmean(r[5] for r in rows if r[3]=='frugal' and r[4]==1)))
    save('objective_counterexamples.json',out)

def time_deterministic_policies():
    # Compile the actual benchmark with ONLY method selection and budget list changed.
    # Measures complete CPU sweep including matrix construction; not model/human costs.
    source=(REF/'benchmark.py').read_text(encoding='utf-8');out={}
    old="methods=['random','random_split','diversity','entropy','lookahead','frugal']"
    assert old in source and 'for budget in [0,1,2,3]:' in source
    for method in ['entropy','lookahead','frugal']:
        modified=source.replace(old,'methods='+repr([method])).replace('for budget in [0,1,2,3]:','for budget in [3]:')
        ns={'__name__':'timing_variant'};exec(compile(modified,'<review_timing_variant>','exec'),ns)
        (OUT/f'timing_{method}.py').write_text(modified, encoding='utf-8')
        runs=[]
        for _ in range(3):
            t=time.perf_counter();rows=ns['run']();runs.append(time.perf_counter()-t)
            assert len(rows)==750
            for r in rows:
                assert all(abs(a-b)<1e-12 for a,b in zip(r[5:],KEYED[r[0],r[1],r[2],r[3],r[4]]))
        out[method]=dict(seconds=runs,median_seconds=statistics.median(runs),scope='750 targets, 40 freshly generated matrices, budget 3 only; per-matrix tree cache shared across targets; no random policies')
    save('deterministic_policy_timings.json',out)

if __name__=='__main__':
    started=time.perf_counter()
    metrics_and_redundancy();counterexamples();crossed_probes();matched_pilot();time_deterministic_policies()
    check_random();check_trees()
    save('run_metadata.json',dict(python=sys.version,executable=sys.executable,argv=sys.argv,wall_seconds=time.perf_counter()-started,frozen_sha256=hashlib.sha256((REF/'frozen_cases.jsonl.gz').read_bytes()).hexdigest()))
