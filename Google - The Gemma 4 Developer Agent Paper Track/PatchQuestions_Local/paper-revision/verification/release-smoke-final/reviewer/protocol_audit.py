"""Check displayed entropy and demonstrate scoring boundary with actual protocol."""
from pathlib import Path
import gzip,json,random,subprocess,sys,statistics
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'run_cpython_3_12_14'))
import cognitive_probe
import replay
from reviewer_audit import CASES,KEYED,grids,save

differences=[];pilot=[]
for c in CASES:
    order=list(range(len(c['configs'])));random.Random(2026+c['split']).shuffle(order)
    grid=[[json.dumps(v) for v in c['query_outputs'][i]] for i in order]
    for target in range(len(order)):
        key=order.index(target);ids=list(range(len(order)));remaining=list(range(len(grid[0])));used=0
        for _ in range(3):
            j=cognitive_probe.choose(grid,ids,remaining)
            if j is None:break
            used+=1;remaining.remove(j);ids=[i for i in ids if grid[i][j]==grid[key][j]]
        held=sum(c['heldout_outputs'][order[i]]==c['heldout_outputs'][target] for i in ids)/len(ids)
        expected=KEYED[c['family'],c['split'],target,'entropy',3]
        if abs(held-expected[0])>1e-12 or used!=expected[3]:differences.append(dict(family=c['family'],split=c['split'],target=target,actual=[held,used],expected=[expected[0],expected[3]]))
        if c['split']==19 and target in [0,1]:pilot.append(dict(family=c['family'],target=target,heldout_exact=held,questions=used))

fixture=None
for c in CASES:
    q,h=grids(c)
    for t in range(len(q)):
        for pick in range(len(q)):
            if h[t]==h[pick] and q[t]!=q[pick]:
                j=next(j for j in range(len(q[t])) if q[t][j]!=q[pick][j])
                fixture=(c,t,pick,j);break
        if fixture:break
    if fixture:break
c,t,pick,j=fixture
launch=[sys.executable,'-B','replay.py',c['family'],str(c['split']),str(t),'--shuffle','2026']
ids,*_=replay.episode(c['family'],c['split'],t,2026)
actions=[{'ask':j},{'pick':ids.index(pick)}]
r=subprocess.run(launch,cwd=ROOT/'run_cpython_3_12_14',input=''.join(json.dumps(x)+'\n' for x in actions),capture_output=True,text=True)
assert r.returncode==0,r.stderr
final=json.loads(r.stdout.splitlines()[-1]);assert final['heldout_exact'] is True
out=dict(entropy_frozen_episodes_checked=750,native_vs_displayed_differences=differences,pilot_entropy=pilot,pilot_entropy_mean=statistics.fmean(x['heldout_exact'] for x in pilot),inconsistent_pick_fixture=dict(family=c['family'],split=c['split'],target=t,picked_original_candidate=pick,query=j,input=c['query_inputs'][j],target_answer=c['query_outputs'][t][j],picked_candidate_answer=c['query_outputs'][pick][j],argv=launch,actions=actions,final_result=final,note='This is allowed by the explicitly held-out-only endpoint. It does not affect classical policies, which always pick survivors. It needs a separate consistency metric/gate for model evaluations.'))
save('protocol_validation.json',out)
(ROOT/'reviewer_checks'/'inconsistent_pick_transcript.txt').write_text(r.stdout)
print(json.dumps(out,indent=2))
