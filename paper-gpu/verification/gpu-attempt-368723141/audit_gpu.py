from pathlib import Path
import sys,json,hashlib,collections,statistics,zipfile
import tempfile
ROOT=Path(__file__).resolve().parent
work=tempfile.TemporaryDirectory(prefix='patchquestions-replay-')
assert hashlib.sha256((ROOT/'Kaggle_Output.zip').read_bytes()).hexdigest()=='05d5ae6fac7da03e7a4c080ab2a226c353c6a1168682ad2d3514e759f58bd6e3'
with zipfile.ZipFile(ROOT/'Kaggle_Output.zip') as z:
 for name in z.namelist():
  assert (Path(work.name)/name).resolve().is_relative_to(Path(work.name).resolve())
 z.extractall(work.name)
CODE=Path(work.name)/'patchquestions-code'
RUN=Path(work.name)/'patchquestions-20261112-083802'
assert hashlib.sha256((CODE/'pilot.py').read_bytes()).hexdigest()=='1077b414d63c927f06e9748aa41af5138fba503ee95831af731ad0f56bdf04a3'
sys.path.insert(0,str(CODE))
import pilot
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
archive=RUN.with_suffix('.zip')
assert sha(archive)==Path(str(archive)+'.sha256').read_text().strip()
plan=json.loads((RUN/'plan.json').read_text())
assert sha(CODE/'pilot.py')==plan['source_sha256']
assert sha(CODE/'frozen_cases.jsonl.gz')==plan['data_sha256']
assert sha(RUN/'plan.json')==(RUN/'PLAN.sha256').read_text().strip()
assert (RUN/'plan.json').read_bytes()==(RUN/'sessions/plan.json').read_bytes()
replay=pilot.replay(RUN/'sessions',CODE/'frozen_cases.jsonl.gz')
assert replay==json.loads((RUN/'REPLAY.json').read_text())
summary=json.loads((RUN/'sessions/SUMMARY.json').read_text())
assert all(replay[k]==v for k,v in summary.items())
cases=pilot.load_cases(CODE/'frozen_cases.jsonl.gz')
baseline=json.loads((RUN/'BASELINES.json').read_text())
for spec,b in zip(plan['schedule'],baseline):
 assert spec['session_id']==b['session_id']
 for policy in ('entropy','random_split'):
  assert pilot.baseline(pilot.new_session(cases,spec),policy)==b[policy]
errors=collections.Counter();zero_raw=[];tokens=[];mismatches=[];counts=collections.Counter()
for spec in plan['schedule']:
 sid=spec['session_id']; events=[json.loads(s) for s in (RUN/'sessions'/(sid+'.events.jsonl')).read_text().splitlines()]
 result=json.loads((RUN/'sessions'/(sid+'.result.json')).read_text())
 counts[result['status']]+=1
 if result.get('error'): errors[result['error']]+=1
 requests=[e for e in events if 'request' in e]
 responses=[e for e in events if 'raw_response' in e]
 assert len(requests)==len(responses)
 for req,resp in zip(requests,responses):
  raw=json.loads(resp['raw_response']);actual=raw['usage']['prompt_tokens']; local=req['prompt_tokens_preflight']
  tokens.append(actual)
  if actual!=local:mismatches.append([sid,req['turn'],local,actual])
 if spec.get('arm')=='zero':zero_raw.append(json.loads(responses[0]['raw_response'])['choices'][0]['message']['content'])
assert not mismatches
assert len(tokens)==116
assert len(zero_raw)==16 and all(s.startswith('```json\n') and s.endswith('```') for s in zero_raw)
report={'archive_sha256':sha(archive),'supervisor_sha256':sha(CODE/'pilot.py'),'data_sha256':plan['data_sha256'],'replay_matches_saved':True,'matched_baselines_recomputed':64,'summary':summary,'statuses':dict(counts),'errors':dict(errors),'request_count':len(tokens),'prompt_token_mismatches':mismatches,'max_prompt_tokens':max(tokens),'zero_response_examples':zero_raw[:3], 'zero_all_fenced':True,'model_info':plan['model_info']}
# Separate implementation of raw action/answer replay and exact final grading.
fresh_counts=collections.Counter();consistent_counts=collections.Counter();diagnostics=[]
for spec in plan['schedule']:
 sid=spec['session_id']; case=cases[spec['family'],spec['split']]
 order=spec['order']; hidden=order.index(spec['target']); survivors=set(range(len(order)));asked=[];pick=None
 events=[json.loads(s) for s in (RUN/'sessions'/(sid+'.events.jsonl')).read_text().splitlines()]
 result=json.loads((RUN/'sessions'/(sid+'.result.json')).read_text())
 raw_actions=[]; logged_actions=[]
 validation=pilot.new_session(cases,spec)
 messages=pilot.initial_messages(validation); last_text=None; assisted_final=False
 for e in events:
  if 'request' in e:
   if spec.get('arm')=='entropy_pick' and not assisted_final:
    messages.append({'role':'user','content':'Select a consistent row now. Send only a JSON pick object.'})
    assisted_final=True
   assert e['request']==pilot.model_request(messages,plan['model_info']), 'request history mismatch: '+sid
  if 'raw_response' in e:
   text=json.loads(e['raw_response'])['choices'][0]['message']['content']
   last_text=text
   try:a=json.loads(text)
   except json.JSONDecodeError: a=None
   raw_actions.append(a)
  if 'action' in e:
   a=e['action'];logged_actions.append(a) if e.get('source')=='model' else None
   if e.get('source')=='entropy':assert a=={'ask':pilot.entropy_question(validation)}
   answer,_=validation.step(a);assert answer==e['answer'], 'answer mismatch: '+sid
   if answer is not None:
    messages.extend([{'role':'assistant','content':pilot.encode(a) if e.get('source')=='entropy' else last_text}, {'role':'user','content':pilot.encode(answer)}])
   if 'ask' in a:
    j=a['ask'];assert 0<=j<len(case['query_inputs']) and j not in asked and len(asked)<3
    asked.append(j)
    true=case['query_outputs'][spec['target']][j]
    survivors={i for i in survivors if case['query_outputs'][order[i]][j]==true}
   else:pick=a['pick']; assert 0<=pick<len(order)
 if result['status']=='completed':
  assert raw_actions==logged_actions
  assert pick is not None
  success=pick in survivors and case['heldout_outputs'][order[pick]]==case['heldout_outputs'][spec['target']]
  assert success==result['success']
  assert (pick in survivors)==result['query_consistent']
  arm=spec.get('arm','free');fresh_counts[spec['view'] if arm=='free' else arm]+=success
  consistent_counts[spec['view'] if arm=='free' else arm]+=pick in survivors
 diagnostics.append({'session_id':sid,'questions':len(asked),'survivors':len(survivors),'pick_consistent':pick in survivors if pick is not None else None})
report['independent_raw_regrade_successes']=dict(fresh_counts)
report['independent_consistent_picks']=dict(consistent_counts)
report['matched_core_baselines']={p:statistics.mean(b[p]['success'] for spec,b in zip(plan['schedule'],baseline) if spec.get('arm','free')=='free') for p in ('entropy','random_split')}
report['questions_by_arm']={arm:statistics.mean(d['questions'] for s,d in zip(plan['schedule'],diagnostics) if s.get('arm','free')==arm) for arm in ('free','zero','entropy_pick')}
(ROOT/'GPU_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
