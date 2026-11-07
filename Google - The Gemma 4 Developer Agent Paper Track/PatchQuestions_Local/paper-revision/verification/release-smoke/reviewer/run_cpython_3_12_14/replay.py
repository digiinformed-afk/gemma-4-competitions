"""Blinded JSON protocol for one episode: python replay.py csv_fields 19 7."""
import argparse
import json
import random
from benchmark import families, outcome

def episode(family, split, target, seed):
    configs, smoke, universe, impl=families()[family]
    if not 0<=target<len(configs):
        raise ValueError('target outside family')
    xs=sorted(set(universe)-{smoke})
    random.Random(split).shuffle(xs)
    cut=min(16,len(xs)//2)
    probes,holdout=xs[:cut],xs[cut:]
    value=outcome(impl,configs[target],smoke)
    ids=[i for i,c in enumerate(configs) if outcome(impl,c,smoke)==value]
    random.Random(seed).shuffle(ids)
    grid=[[outcome(impl,configs[i],x) for x in probes] for i in ids]
    target_row=ids.index(target)
    return ids,probes,holdout,grid,target_row,configs,impl

def play(family, split, target, seed):
    ids,xs,held,grid,key,configs,impl=episode(family,split,target,seed)
    print(json.dumps(dict(family=family,inputs=xs,outputs=[[json.loads(o) for o in row] for row in grid],
                          budget=3,instructions='Send {"ask": column} or {"pick": row}; indices start at zero.')),flush=True)
    seen=set()
    for _ in range(4):
        action=json.loads(input())
        if set(action)=={'pick'}:
            row=action['pick']
            if type(row)!=int or not 0<=row<len(ids): raise ValueError('invalid row')
            correct=all(outcome(impl,configs[ids[row]],x)==outcome(impl,configs[target],x) for x in held)
            print(json.dumps(dict(heldout_exact=correct,queries=len(seen))),flush=True)
            return
        j=action.get('ask')
        if set(action)!={'ask'} or type(j)!=int or not 0<=j<len(xs) or j in seen or len(seen)>=3:
            raise ValueError('invalid or repeated query, or budget exceeded')
        seen.add(j)
        print(json.dumps(dict(answer=json.loads(grid[key][j]))),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('family',choices=sorted(families()));p.add_argument('split',type=int)
    p.add_argument('target',type=int);p.add_argument('--shuffle',type=int,default=2026)
    a=p.parse_args();play(a.family,a.split,a.target,a.shuffle)
