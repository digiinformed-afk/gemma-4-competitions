"""Independent decision-tree and blind-grader checks."""
import csv, json, subprocess, sys
from fractions import Fraction
from itertools import combinations
from benchmark import families, evaluate
from replay import episode
from intervention import study

def check():
    # Exhaustive two-query search using explicit leaf lists, independently of the DP.
    for name in families():
        ids,xs,held,grid,key,c,impl=episode(name,19,0,99)
        assert len(ids)==len(c)
        best=0
        for j in range(len(xs)):
            groups={}
            for i,row in enumerate(grid):
                groups.setdefault(row[j],[]).append(i)
            leaves=sum(max(len({grid[i][k] for i in group}) for k in range(len(xs))) for group in groups.values())
            best=max(best,leaves)
        # Uniform selection in each leaf scores exactly one correct identity per leaf.
        out=evaluate(name,families()[name],19)
        from math import isclose
        vals=[1/r[7] for r in out if r[3]=='frugal' and r[4]==2]
        assert isclose(sum(vals),best),name
        for b in (1,2,3):
            a=[r for r in out if r[3]=='lookahead' and r[4]==b]
            z=[r for r in out if r[3]=='frugal' and r[4]==b]
            assert isclose(sum(1/r[7] for r in a),sum(1/r[7] for r in z))
            assert sum(r[8] for r in z)<=sum(r[8] for r in a)+1e-9
    ids,_,_,_,key,_,_=episode('csv_fields',19,7,2026)
    cmd=[sys.executable,'replay.py','csv_fields','19','7']
    result=subprocess.run(cmd,input='{"ask":0}\n'+json.dumps({'pick':key})+'\n',capture_output=True,text=True,check=True)
    assert json.loads(result.stdout.splitlines()[-1])=={'heldout_exact':True,'queries':1}
    print('Eight independent optimality checks and blind protocol check passed.')

if __name__=='__main__':check()
