"""Summarize exact expectations and compute the all-probes ceiling."""
import csv, statistics, json
from benchmark import families, outcome
from replay import episode

def audit():
    rows=list(csv.DictReader(open('scores.csv')))
    methods=list(dict.fromkeys(r['policy'] for r in rows))
    def family_mean(f,m,b,field):
        return statistics.fmean(float(r[field]) for r in rows if r['family']==f and r['policy']==m and int(r['budget'])==b)
    report={}
    for f,spec in families().items():
        vals=[]
        for seed in [19,43,73,101,137]:
            for t in range(len(spec[0])):
                ids,_,h,grid,key,c,impl=episode(f,seed,t,0)
                survivors=[i for i,row in zip(ids,grid) if row==grid[key]]
                vals.append(statistics.fmean(all(outcome(impl,c[i],x)==outcome(impl,c[t],x) for x in h) for i in survivors))
        report[f]={m:[family_mean(f,m,3,'heldout_exact'),family_mean(f,m,3,'queries_used')] for m in methods}
        report[f]['ceiling']=statistics.fmean(vals)
    return report

if __name__=='__main__':
    print(json.dumps(audit(),indent=2))
