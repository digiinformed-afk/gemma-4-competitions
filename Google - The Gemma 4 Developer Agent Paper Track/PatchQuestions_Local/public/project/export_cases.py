"""Export exact query/held-out matrices for replay across Python versions."""
import gzip,json,random
from benchmark import families,outcome
def export(path):
    with gzip.open(path,'wt',encoding='utf8') as dst:
        for f,(configs,smoke,universe,impl) in families().items():
            for seed in [19,43,73,101,137]:
                xs=sorted(set(universe)-{smoke})
                random.Random(seed).shuffle(xs)
                cut=min(16,len(xs)//2)
                def matrix(inputs):
                    return [[json.loads(outcome(impl,c,x)) for x in inputs] for c in configs]
                record=dict(family=f,split=seed,smoke=smoke,configs=[list(map(repr,c)) for c in configs],
                            query_inputs=xs[:cut],query_outputs=matrix(xs[:cut]),
                            heldout_inputs=xs[cut:],heldout_outputs=matrix(xs[cut:]))
                dst.write(json.dumps(record,ensure_ascii=True)+'\n')
if __name__=='__main__': export('frozen_cases.jsonl.gz')
