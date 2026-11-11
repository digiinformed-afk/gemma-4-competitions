"use strict";
const KEY="hikmah-command-v1",SNAPKEY="hikmah-command-snapshots-v1";
const nowISO=()=>new Date().toISOString();
const uid=()=>Math.random().toString(36).slice(2,10);
const seed={
schema:1,updated:"2026-11-11T17:30:00Z",
actions:[
{id:"a1",track:"paper",title:"Complete author review and submit the Kaggle Writeup",priority:1,status:"blocked",why:"Paper deadline 12 Nov 23:59 UTC; no submitted Writeup confirmed",next:"Verify authorship, rights, rendering, word count, optional notebook link; submit and preserve submission ID"},
{id:"a2",track:"main",title:"Audit V12/V14 raw runs and exact controls",priority:2,status:"tentative",why:"Later reports are not a matched, fully audited ledger",next:"Collect manifests, model hashes, prompts, wall time, archive hashes, task traces and evaluator version"},
{id:"a3",track:"main",title:"Fix FastAPI cross-file propagation and tool-call recovery",priority:3,status:"blocked",why:"Repeated edit argument omissions, incomplete lifecycle wiring and timeout",next:"Implement persistent progress checklist; enforce required edit fields; test imports/signatures before pytest"},
{id:"a4",track:"main",title:"Freeze new untouched multi-repo benchmark tasks",priority:4,status:"tentative",why:"Requests/Rich/FastAPI and HTTPX are already exposed",next:"Stratify public tasks by repo, bug category and complexity; pre-register run order and baselines"},
{id:"a5",track:"main",title:"Run matched control/policy/Hikmah under identical budgets",priority:5,status:"tentative",why:"No demonstrated general repair-rate advantage",next:"Freeze model, prompt, evaluator, time/tool budgets; report paired resolved counts, costs and failures"},
{id:"a6",track:"main",title:"Official submission archive validation and Kaggle upload",priority:6,status:"blocked",why:"Local structural pass does not prove accepted final entry",next:"Inspect root agent.yaml, disallowed content, official validator, exact model constraints; preserve receipt"}
],
versions:[
{version:"V8",status:"verified",score:"2/3",detail:"Older three-task pilot: Requests + Rich resolved; FastAPI not resolved",gate:"Reproduce if needed"},
{version:"V9",status:"verified",score:"2/3",detail:"Reported and historically tracked three-task pilot; source provenance older",gate:"Match raw config"},
{version:"V10",status:"verified",score:"2/3",detail:"Faster solved cases; unresolved FastAPI. Prior GCS signature issue was repaired",gate:"Trace audit"},
{version:"V11",status:"completed",score:"Not run",detail:"Documented reconstruction, CPU checks passed. Not a byte-identical recovered original",gate:"GPU run / manifests"},
{version:"V12",status:"verified",score:"2/3",detail:"Notebook review: Requests 3m30/24 calls; Rich 10m02/65; FastAPI 10m05/46",gate:"New tasks + controlled ablation"},
{version:"V14",status:"tentative",score:"2/3 reported",detail:"Later session summary reports slower V14; raw conditions not audited",gate:"Raw trace/hash verification"}
],
benchmarks:[
{id:"requests_7309",name:"Requests",outcome:"verified",text:"Resolved",calls:"24/65",time:"3m 30s",scope:"Known, repeatedly tuned"},
{id:"rich_3130",name:"Rich",outcome:"verified",text:"Resolved",calls:"65/65",time:"10m 02s",scope:"Known; early probe passed"},
{id:"fastapi_14262",name:"FastAPI",outcome:"blocked",text:"Timeout",calls:"46/65",time:"10m 05s",scope:"Known; incomplete call chain"},
{id:"httpx_holdout",name:"HTTPX",outcome:"tentative",text:"1 pass each reported",calls:"31 Hikmah / 34 control",time:"603s / 583s",scope:"Exposed in later runs; raw audit pending"}
],
experiments:[
{id:"pilot-control",version:"Prior",track:"main",condition:"Control",status:"verified",resolved:2,total:3,time:null,calls:null,gpu:"4× L4",notes:"Historical saved matched pilot; 2/3. Not comparable to new budget without alignment.",hash:""},
{id:"pilot-policy",version:"Prior",track:"main",condition:"Generic policy",status:"verified",resolved:2,total:3,time:null,calls:null,gpu:"4× L4",notes:"Historical matched arm; 2/3.",hash:""},
{id:"pilot-hikmah",version:"Prior",track:"main",condition:"Hikmah",status:"verified",resolved:2,total:3,time:null,calls:null,gpu:"4× L4",notes:"Historical matched arm; 2/3, no established repair-rate gain.",hash:""},
{id:"v11-prep",version:"V11",track:"main",condition:"Hikmah reconstructed",status:"completed",resolved:null,total:3,time:null,calls:null,gpu:"L4×4 planned",notes:"CPU checks pass; no GPU result. 10m/65 calls/95 turns are experimental settings.",hash:""},
{id:"v12-hikmah",version:"V12",track:"main",condition:"Hikmah",status:"verified",resolved:2,total:3,time:1417,calls:135,gpu:"Kaggle GPU (exact manifest pending)",notes:"Summed task wall times include evaluator overhead; 24+65+46 calls. No final submission.",hash:""},
{id:"v14-hikmah",version:"V14",track:"main",condition:"Hikmah",status:"tentative",resolved:2,total:3,time:null,calls:null,gpu:"Not verified",notes:"Session summary only; slower V14. Raw manifest/trace audit pending.",hash:""},
{id:"httpx-hikmah",version:"HTTPX",track:"main",condition:"Hikmah",status:"tentative",resolved:1,total:1,time:603,calls:31,gpu:"Not verified",notes:"Reported one pass, exposed holdout, raw conditions pending.",hash:""},
{id:"httpx-control",version:"HTTPX",track:"main",condition:"Control",status:"tentative",resolved:1,total:1,time:583,calls:34,gpu:"Not verified",notes:"Reported one pass, raw matched conditions pending.",hash:""}
],
gates:[
{id:"import",track:"main",label:"Import smoke",description:"Import changed files from fresh checkout",status:"blocked"},
{id:"signature",track:"main",label:"Public API signatures",description:"Validate full lifecycle call chain and compatibility",status:"blocked"},
{id:"pytest",track:"main",label:"Relevant pytest",description:"Pass focused tests before broader suite",status:"blocked"},
{id:"trace",track:"main",label:"Raw run manifest",description:"Task trace + prompt + hashes + settings captured",status:"tentative"},
{id:"zip",track:"main",label:"Official ZIP validator",description:"Older archived candidate passed official structural check; newest ZIP not verified",status:"tentative"},
{id:"receipt",track:"main",label:"Final submission receipt",description:"Actual Kaggle submission and leaderboard entry",status:"blocked"},
{id:"paper-reproduce",track:"paper",label:"18,000 reference score rows",description:"Reproduced byte-for-byte on CPython 3.12.14",status:"verified"},
{id:"paper-notebook",track:"paper",label:"Notebook execution",description:"16/16 code cells executed, zero error outputs",status:"verified"},
{id:"paper-author",track:"paper",label:"Authorship, rights and attribution",description:"Human eligibility and rights review",status:"blocked"},
{id:"paper-render",track:"paper",label:"Kaggle Writeup rendering",description:"Rendered manuscript, word count, optional Project Link",status:"blocked"},
{id:"paper-submit",track:"paper",label:"Official Writeup submission",description:"Save submission ID, timestamp, screenshot/receipt",status:"blocked"}
],
failures:[
{id:"f1",track:"main",version:"V12",title:"FastAPI dependency lifecycle fix incomplete",category:"cross-file implementation",status:"blocked",detail:"Multi-file API wiring not completed before 10-minute timeout; no passing evaluator result.",cause:"General tool policy and call-chain search did not yield complete repair."},
{id:"f2",track:"main",version:"V12",title:"Malformed tool calls",category:"tool discipline",status:"verified",detail:"FastAPI repeatedly omitted mandatory old_string in edit calls.",cause:"Add schema-aware retry with required argument checks; test against controls."},
{id:"f3",track:"main",version:"V12",title:"Repeated investigation after useful progress",category:"memory/context",status:"tentative",detail:"Rich early probe passed around 191s but continued exploring until tool budget exhaustion.",cause:"Context compaction is one hypothesis, not proven cause."},
{id:"f4",track:"main",version:"V12",title:"Narrative not equal to applied patch",category:"evidence trust",status:"verified",detail:"Final Rich explanation described a failed edit operation.",cause:"Trust checkout diff and evaluator over final natural-language summary."}
],
compute:[
{id:"c1",run:"V12 · Requests",hardware:"Kaggle GPU; exact GPU manifest pending",seconds:210,calls:"24/65",tokens:"Not recorded",cost:"Not recorded",status:"verified"},
{id:"c2",run:"V12 · Rich",hardware:"Kaggle GPU; exact GPU manifest pending",seconds:602,calls:"65/65",tokens:"Not recorded",cost:"Not recorded",status:"verified"},
{id:"c3",run:"V12 · FastAPI",hardware:"Kaggle GPU; exact GPU manifest pending",seconds:605,calls:"46/65",tokens:"Not recorded",cost:"Not recorded",status:"verified"},
{id:"c4",run:"HTTPX · Hikmah",hardware:"Unverified",seconds:603,calls:"31",tokens:"Not recorded",cost:"Not recorded",status:"tentative"},
{id:"c5",run:"HTTPX · Control",hardware:"Unverified",seconds:583,calls:"34",tokens:"Not recorded",cost:"Not recorded",status:"tentative"}
],
submissions:[
{id:"s1",track:"main",title:"Historical candidate archive packaged",date:"2026-11-07",status:"verified",detail:"Archive hash 13dfe5ed9d6295b89fbaf9e9ea2e5158e7a52e44bc67e6eb66fdfc4c1803da80; structural validator passed. Not uploaded to Kaggle."},
{id:"s2",track:"paper",title:"Paper release ZIP prepared",date:"2026-11-07",status:"completed",detail:"Supporting package prepared with adjacent SHA256 and reproduction checks. Writeup submission is separate."}
],
settings:[
{label:"Base model",value:"Gemma 4 31B IT QAT W4A16 CT v2 (documented pilot target)"},
{label:"V11 task budget",value:"600 seconds"},
{label:"V11 tool calls",value:"65"},
{label:"V11 turns",value:"95"},
{label:"V11 tool timeout",value:"90 seconds"},
{label:"V11 temperature / top_p",value:"0.15 / 0.90"},
{label:"V11 max output tokens",value:"2,560"},
{label:"V11 thinking allowance",value:"1,024"},
{label:"V11 cold-run cap",value:"4,200 seconds"},
{label:"GPU / inference",value:"4× L4 planned for matched V11 sessions"},
{label:"Tools",value:"6-tool repository repair agent"},
{label:"V12 exact settings",value:"Audit required (do not infer identical to V11)"}
],
methods:[
{id:"m1",title:"Persistent progress ledger",status:"tentative",idea:"Keep compact list of verified edits, remaining call chain, and checks after context compaction.",test:"A/B against baseline on unfamiliar multi-file tasks with same tokens and time.",source:"V12 trace review"},
{id:"m2",title:"Schema-validating tool wrapper",status:"tentative",idea:"Validate required edit fields before issuing tool calls, and recover from malformed calls explicitly.",test:"Count malformed/retried calls and final resolved issues at equal budget.",source:"V12 FastAPI"},
{id:"m3",title:"Cross-file symbol graph",status:"tentative",idea:"Batch lexical search of public entrypoints, internal call sites, imports and compatibility checks.",test:"Compare lexical baseline versus graph-assisted discovery on fresh multi-file fixes.",source:"Saved V11 plan"},
{id:"m4",title:"Stop-on-green & verification reserve",status:"tentative",idea:"Stop exploration on trustworthy pass and reserve remaining budget for a final diff/import check.",test:"Measure wasted calls and regression failures while preserving resolved rates.",source:"V12 Rich trace"},
{id:"m5",title:"Agentless localization baseline",status:"tentative",idea:"Simple locate → edit → validate baseline before adding orchestration.",test:"Matched control, generic policy and Hikmah, same model/hardware/tasks.",source:"https://arxiv.org/abs/2407.01489"},
{id:"m6",title:"Discriminating tests / patch comparison",status:"tentative",idea:"Adapt PatchQuestions' information selection to real repository uncertainty without assuming a perfect oracle.",test:"Compare end-to-end repair and test costs on frozen new tasks; exclude hidden evaluator references.",source:"Saved Paper Track + CodeMonkeys"}
]
};
const clone=x=>JSON.parse(JSON.stringify(x));
let state;
try{const stored=JSON.parse(localStorage.getItem(KEY));state=stored&&stored.schema===1&&Array.isArray(stored.actions)?stored:clone(seed)}catch{state=clone(seed)}
let snapshots;
try{snapshots=JSON.parse(localStorage.getItem(SNAPKEY))||[]}catch{snapshots=[]}
const $=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const pill=s=>'<span class="pill '+esc(s)+'">'+esc(s)+'</span>';
const toast=t=>{const el=$("toast");el.textContent=t;el.style.display="block";clearTimeout(window.toastTimeout);window.toastTimeout=setTimeout(()=>el.style.display="none",3500)};
function persist(){state.updated=nowISO();try{localStorage.setItem(KEY,JSON.stringify(state));$("save-state").textContent="Saved · "+new Date().toLocaleTimeString()}catch(e){$("save-state").textContent="Autosave failed — export now";toast("Storage unavailable: export a backup")}}
function formatTime(s){if(!Number.isFinite(Number(s)))return"—";return Math.floor(s/60)+"m "+Math.round(s%60)+"s"}
function idSort(a,b){return a.priority-b.priority}
function kpi(label,value,sub,symbol,cls=""){return '<div class="kpi"><div class="kpi-top">'+esc(label)+'<span class="kpi-symbol">'+symbol+'</span></div><div class="kpi-value '+cls+'">'+esc(value)+'</div><div class="kpi-sub">'+esc(sub)+'</div></div>'}
function set(id,html){const el=$(id);if(el)el.innerHTML=html}
function renderOverview(){
set("overview-kpis",[
kpi("MAIN TRACK PILOT","2 / 3","V12 · 3 familiar tasks","⌘"),
kpi("PAPER REPRODUCTION","18,000","Rows reproduced · source-evidence","▤","mint"),
kpi("FASTAPI RESOLUTION","0 / 1","Unresolved in reviewed pilot","!","amber"),
kpi("FINAL SUBMISSIONS","0 verified","No official receipt recorded","◈")
].join(""));
set("overview-actions",state.actions.slice().sort(idSort).filter(a=>a.status!=="completed").slice(0,5).map((a,i)=>'<div class="action-row"><span class="sequence">0'+(i+1)+'</span><div class="main-col"><b>'+esc(a.title)+'</b><p>'+esc(a.why)+'</p><span class="meta">'+esc(a.track.toUpperCase())+' · P'+esc(a.priority)+'</span></div>'+pill(a.status)+'<button data-edit="actions" data-id="'+esc(a.id)+'">EDIT</button></div>').join("")||'<p class="empty">No open actions.</p>');
set("milestone-list",[
["◉","Paper manuscript reproduced","18,000 rows · 16 notebook cells", "verified"],
["◉","Historical archive validator","Older candidate only", "verified"],
["◌","Raw latest-run controls","V14 / HTTPX require manifest audit", "tentative"],
["×","FastAPI repair","No passing result in V12", "blocked"],
["×","Competition entry","No confirmed main or paper receipt", "blocked"]
].map(x=>'<div class="milestone-row"><span class="mark">'+x[0]+'</span><div class="main-col"><b>'+esc(x[1])+'</b><p>'+esc(x[2])+'</p></div>'+pill(x[3])+'</div>').join(""));
const deadlines=[["Paper Writeup","2026-11-12T23:59:00Z","13 Nov 04:59 PKT"],["Main team merger","2026-11-25T23:59:00Z","26 Nov 04:59 PKT"],["Main final submission","2026-12-02T23:59:00Z","03 Dec 04:59 PKT"]];
set("deadline-cards",deadlines.map(([n,d,local])=>{const ms=new Date(d)-Date.now();return '<div class="deadline-row"><div><b>'+n+'</b><small>'+local+' · verify with Kaggle</small></div><div class="deadline-time">'+(ms>0?Math.ceil(ms/86400000)+"d left":"Passed")+'</div></div>'}).join(""));
drawChart("overview-trend",state.experiments.filter(e=>["pilot-control","pilot-policy","pilot-hikmah","v12-hikmah","v14-hikmah"].includes(e.id)),"resolved");
}
function drawChart(where,arr,what){const finite=arr.filter(x=>Number.isFinite(x[what]));const max=Math.max(3,...finite.map(x=>x[what]));set(where,'<div class="chart">'+arr.map(x=>{const val=Number.isFinite(x[what])?x[what]:null;return '<div class="chart-col"><span class="chart-num">'+(val===null?"?":val)+'</span><div class="chart-bar" style="height:'+(val===null?3:Math.max(3,100*val/max))+'%"></div><small>'+esc(x.version+" "+x.condition)+'</small></div>'}).join("")+'</div><p class="quiet">Different cohorts/settings and tentative results are not a single comparable trajectory. Unknown measurements are “?”.</p>')}
function renderMain(){
set("version-rows",state.versions.map(v=>'<tr><td><b>'+esc(v.version)+'</b></td><td>'+pill(v.status)+'</td><td>'+esc(v.score)+'</td><td>'+esc(v.detail)+'</td><td>'+esc(v.gate)+'</td></tr>').join(""));
set("benchmark-rows",state.benchmarks.map(t=>'<tr><td><b>'+esc(t.name)+'</b><br><small class="muted mono">'+esc(t.id)+'</small></td><td>'+pill(t.outcome)+'<br>'+esc(t.text)+'</td><td class="mono">'+esc(t.calls)+'</td><td class="mono">'+esc(t.time)+'</td><td>'+esc(t.scope)+'</td></tr>').join(""));
set("fastapi-checklist",[
["Batch search all lifecycle symbol references","Before first implementation edit"],
["Patch full call chain, imports and compatibility","No partial wiring"],
["Run import/signature smoke before pytest","Cheap failure detection"],
["Use edit schema validation (old_string required)","Prevent malformed tool calls"],
["Reserve 60 seconds to verify and finalize","Avoid uncommitted progress"]
].map(([label,desc],i)=>'<div class="gate"><span class="pill tentative">'+(i+1)+'</span><label>'+esc(label)+'<small>'+esc(desc)+'</small></label></div>').join(""));
set("settings-list",state.settings.map(s=>'<div class="setting"><small>'+esc(s.label)+'</small><strong>'+esc(s.value)+'</strong></div>').join(""));
renderGates("main-gates","main")
}
function renderGates(id,track){set(id,state.gates.filter(g=>g.track===track).map(g=>'<div class="gate"><label>'+esc(g.label)+'<small>'+esc(g.description)+'</small></label><select data-gate="'+esc(g.id)+'">'+["tentative","verified","blocked","completed"].map(s=>'<option value="'+s+'"'+(s===g.status?" selected":"")+'>'+s+'</option>').join("")+'</select></div>').join(""))}
function renderPaper(){
set("paper-kpis",[
kpi("REFERENCE ROWS","18,000","Byte-for-byte reproduction","✓","mint"),
kpi("NOTEBOOK CELLS","16 / 16","Executed without error","✓","mint"),
kpi("SUPERVISOR TESTS","12","Passed on local regression suite","✓","mint"),
kpi("WRITEUP SUBMISSION","Unverified","Human action required","!","amber")
].join(""));
renderGates("paper-gates","paper");
set("paper-evidence",[
["Verified reproduction","18,000 score rows byte-for-byte; 24,000 random-check metrics; 4,096 binary matrices; 2,880 transcript rows."],
["Notebook and release","16/16 code cells ran; manuscript revised and supporting research ZIP prepared with hash verification."],
["Paper claim boundaries","Finite behavior matrices, resource contribution; no Gemma inference, human study, or production repair benefit proven."]
].map(([title,desc])=>'<div><b>'+esc(title)+'</b><p>'+esc(desc)+'</p></div>').join(""))}
function renderExperiments(){
const opts=state.experiments.map(e=>'<option value="'+esc(e.id)+'">'+esc(e.version+' · '+e.condition+' ('+e.status+')')+'</option>').join("");
const a=$("compare-a"),b=$("compare-b");const av=a.value||"pilot-control",bv=b.value||"pilot-hikmah";a.innerHTML=opts;b.innerHTML=opts;a.value=state.experiments.some(e=>e.id===av)?av:state.experiments[0]?.id;b.value=state.experiments.some(e=>e.id===bv)?bv:state.experiments[1]?.id;compare();
const filtered=state.experiments.filter(e=>$("experiment-filter").value==="all"||e.status===$("experiment-filter").value);
set("experiment-rows",filtered.map(e=>'<tr><td><b>'+esc(e.id)+'</b><br><small>'+esc(e.version)+'</small></td><td>'+esc(e.track)+'</td><td>'+esc(e.condition)+'</td><td class="mono">'+(e.resolved===null?"Not run":esc(e.resolved+"/"+e.total))+'</td><td>'+esc(e.calls===null?"?":e.calls)+' calls · '+esc(e.time===null?"?":formatTime(e.time))+'</td><td>'+pill(e.status)+' <button class="tiny-link" data-edit="experiments" data-id="'+esc(e.id)+'">Edit</button></td></tr>').join(""));
const trend=state.experiments.filter(e=>["pilot-control","pilot-policy","pilot-hikmah","v12-hikmah","v14-hikmah"].includes(e.id));
drawChart("resolution-chart",trend,"resolved");drawChart("cost-chart",state.experiments.filter(e=>["v12-hikmah","httpx-hikmah","httpx-control"].includes(e.id)),"calls")
}
function compare(){
const a=state.experiments.find(x=>x.id===$("compare-a").value),b=state.experiments.find(x=>x.id===$("compare-b").value);
if(!a||!b)return;
const card=e=>'<div class="compare-card"><strong>'+esc(e.version+' · '+e.condition)+'</strong><p>'+pill(e.status)+' · '+esc(e.gpu)+'</p><div class="compare-value">'+(e.resolved===null?"Not run":esc(e.resolved+"/"+e.total))+'</div><p>Wall time: '+(e.time===null?"unknown":formatTime(e.time))+' · Tool calls: '+(e.calls===null?"unknown":e.calls)+'</p><p>'+esc(e.notes)+'</p></div>';
const matched=a.version===b.version&&a.total===b.total&&Number.isFinite(a.resolved)&&Number.isFinite(b.resolved)&&a.version==="Prior";
set("comparison-result",'<div class="comparison-grid">'+card(a)+card(b)+'</div><div class="warning-line">'+(matched?"These are described as historical matched arms; verify their exact input order, prompts and hashes for causal interpretation.":"NOT a verified matched causal comparison: task exposure, settings, compute, evaluation period or source verification differ/are not fully documented.")+'</div>')
}
function renderEvidence(){
set("verification-matrix",state.gates.map(g=>'<div class="gate"><label>'+esc(g.track.toUpperCase()+' · '+g.label)+'<small>'+esc(g.description)+'</small></label>'+pill(g.status)+'</div>').join(""));
set("failure-list",state.failures.map(f=>'<div class="failure"><div class="failure-top"><b>'+esc(f.version+' · '+f.title)+'</b>'+pill(f.status)+'</div><p>'+esc(f.detail)+'</p><p class="cause">Hypothesis / action: '+esc(f.cause)+'</p><small class="status-note">'+esc(f.category)+'</small> <button class="tiny-link" data-edit="failures" data-id="'+esc(f.id)+'">Edit</button></div>').join(""));
set("compute-rows",state.compute.map(c=>'<tr><td><b>'+esc(c.run)+'</b></td><td>'+esc(c.hardware)+'</td><td class="mono">'+formatTime(c.seconds)+'</td><td class="mono">'+esc(c.calls)+'</td><td>'+esc(c.tokens)+'</td><td>'+pill(c.status)+'<br><small>'+esc(c.cost)+'</small></td></tr>').join(""));
set("submission-list",state.submissions.map(s=>'<div class="list-row"><div class="main-col"><b>'+esc(s.title)+'</b><p>'+esc(s.date+' · '+s.track+' · '+s.detail)+'</p></div>'+pill(s.status)+'</div>').join(""))}
function renderResearch(){set("method-grid",state.methods.map(m=>'<article class="method-card">'+pill(m.status)+'<h3>'+esc(m.title)+'</h3><p>'+esc(m.idea)+'</p><p class="rule"><b>Experiment:</b> '+esc(m.test)+'</p><small>Source: '+(m.source.startsWith("https://")?'<a target="_blank" rel="noopener" href="'+esc(m.source)+'">Primary source ↗</a>':esc(m.source))+'</small></article>').join(""))}
function renderRecovery(){
set("checkpoint-list",snapshots.length?snapshots.slice().reverse().slice(0,18).map((s,i)=>'<div class="list-row"><div class="main-col"><b>'+esc(s.name)+'</b><p>'+esc(new Date(s.at).toLocaleString())+' · SHA-256 '+esc(s.hash.slice(0,18))+'…</p></div><button class="tiny-link" data-restore="'+esc(s.id)+'">Restore</button><button class="tiny-link" data-snapshot-download="'+esc(s.id)+'">Export</button></div>').join(""):'<p class="empty">No snapshots created on this browser yet.</p>');
$("checkpoint-count").textContent=snapshots.length+" saved";
}
function renderAll(){renderOverview();renderMain();renderPaper();renderExperiments();renderEvidence();renderResearch();renderRecovery()}
function save(){persist();renderAll()}
function navigate(view){document.querySelectorAll(".view").forEach(v=>v.classList.toggle("active",v.id==="view-"+view));document.querySelectorAll(".nav").forEach(b=>b.classList.toggle("active",b.dataset.view===view));$("view-crumb").textContent=view.toUpperCase();document.body.classList.remove("active-mobile");history.replaceState(null,"","#"+view);window.scrollTo({top:0,behavior:"instant"})}
const statusOpts=["tentative","verified","blocked","completed"];
const field=(name,label,type="text",value="",options=[])=>'<div class="field"><label for="field-'+name+'">'+esc(label)+'</label>'+(type==="select"?'<select id="field-'+name+'" name="'+name+'">'+options.map(o=>'<option value="'+esc(o)+'"'+(value===o?" selected":"")+'>'+esc(o)+'</option>').join("")+'</select>':type==="textarea"?'<textarea id="field-'+name+'" name="'+name+'">'+esc(value)+'</textarea>':'<input id="field-'+name+'" name="'+name+'" type="'+type+'" value="'+esc(value??"")+'">')+'</div>';
const definitions={
actions:[["title","Action"],["track","Track","select",["main","paper"]],["priority","Priority (1 = most urgent)","number"],["status","Status","select",statusOpts],["why","Why this matters","textarea"],["next","Exact next step","textarea"]],
versions:[["version","Version ID"],["status","Status","select",statusOpts],["score","Resolved count / status"],["detail","Evidence & changes","textarea"],["gate","Next verification gate"]],
benchmarks:[["id","Task ID"],["name","Repository / task"],["outcome","Status","select",statusOpts],["text","Result"],["calls","Tool calls"],["time","Duration"],["scope","Task exposure"]],
experiments:[["id","Run ID"],["version","Version"],["track","Track","select",["main","paper"]],["condition","Arm / policy"],["status","Evidence status","select",statusOpts],["resolved","Resolved (blank = unknown)","number"],["total","Total scheduled","number"],["time","Wall seconds (blank = unknown)","number"],["calls","Tool calls (blank = unknown)","number"],["gpu","Compute / hardware"],["hash","Artifact SHA-256"],["notes","Evidence & caveats","textarea"]],
failures:[["version","Version"],["track","Track","select",["main","paper"]],["title","Failure"],["category","Category"],["status","Status","select",statusOpts],["detail","Observed behavior","textarea"],["cause","Root cause hypothesis / next action","textarea"]],
compute:[["run","Run ID"],["hardware","Hardware"],["seconds","Elapsed seconds","number"],["calls","Tool calls"],["tokens","Tokens (or Not recorded)"],["cost","Compute cost"],["status","Status","select",statusOpts]],
submissions:[["title","Event"],["track","Track","select",["main","paper"]],["date","Date"],["status","Status","select",statusOpts],["detail","Receipt / artifact hash / notes","textarea"]],
methods:[["title","Method"],["status","Status","select",statusOpts],["idea","Summary","textarea"],["test","Falsifiable matched test","textarea"],["source","Source"]],
gates:[["track","Track","select",["main","paper"]],["label","Gate"],["description","Evidence required","textarea"],["status","Status","select",statusOpts]],
settings:[["label","Setting name"],["value","Value / revision"]]
};
let modalContext={};
function openEditor(type,id=null,pre={}){const item=id?state[type].find(x=>x.id===id):null;modalContext={type,id};$("modal-eyebrow").textContent=id?"EDIT RECORD":"NEW RECORD";$("modal-title").textContent=type.replace(/s$/,"").toUpperCase();$("modal-fields").innerHTML=definitions[type].map(([name,label,t="text",options=[]])=>field(name,label,t,(item||pre)[name]??(name==="status"?"tentative":""),options)).join("");$("editor-dialog").showModal()}
function formSave(ev){ev.preventDefault();const {type,id}=modalContext;const val={};for(const [name,label,t] of definitions[type]){const el=$("field-"+name);let value=el.value.trim();if(t==="number")value=value===""?null:Number(value);val[name]=value}if(type==="actions"&&(!Number.isFinite(val.priority)||val.priority<1)){toast("Priority must be a positive number");return}if(type==="experiments"&&val.resolved!==null&&val.total!==null&&val.resolved>val.total){toast("Resolved count exceeds scheduled tasks");return}if(id){const idx=state[type].findIndex(x=>x.id===id);if(idx<0)return;state[type][idx]={...state[type][idx],...val}}else{if(!val.id)val.id=uid();if(state[type].some(x=>x.id===val.id)){toast("ID already exists");return}state[type].push(val)}$("editor-dialog").close();save();toast("Record saved locally")}
function stableStringify(obj){if(Array.isArray(obj))return"["+obj.map(stableStringify).join(",")+"]";if(obj&&typeof obj==="object")return"{"+Object.keys(obj).sort().map(k=>JSON.stringify(k)+":"+stableStringify(obj[k])).join(",")+"}";return JSON.stringify(obj)}
async function sha256(bytes){if(!crypto?.subtle)throw Error("Secure browser origin required for SHA-256");return [...new Uint8Array(await crypto.subtle.digest("SHA-256",bytes))].map(n=>n.toString(16).padStart(2,"0")).join("")}
const encoded=x=>new TextEncoder().encode(x);
async function fingerprint(x=state){return sha256(encoded(stableStringify(x)))}
function download(name,data,type="application/json"){const url=URL.createObjectURL(new Blob([data],{type}));const a=document.createElement("a");a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),5000)}
async function checkpoint(name="Manual checkpoint"){const hash=await fingerprint();const snap={id:uid(),name,at:nowISO(),hash,state:clone(state)};snapshots.push(snap);if(snapshots.length>25)snapshots=snapshots.slice(-25);try{localStorage.setItem(SNAPKEY,JSON.stringify(snapshots))}catch{toast("Checkpoint storage full; export backup immediately")}renderRecovery();$("fingerprint").textContent=hash;toast("Checkpoint created: "+hash.slice(0,12));return snap}
function backup(){download("hikmah-command-backup-"+new Date().toISOString().slice(0,10)+".json",JSON.stringify({format:"hikmah-control-center",schema:1,exported:nowISO(),state,snapshots},null,2));toast("Exported portable JSON backup")}
async function importBackup(file){if(!file)return;try{const x=JSON.parse(await file.text());if(x.format!=="hikmah-control-center"||x.schema!==1||!x.state||!Array.isArray(x.state.actions)||!Array.isArray(x.state.gates)||!Array.isArray(x.state.experiments))throw Error("Unsupported or invalid backup format");await checkpoint("Before import");state=x.state;const imported=Array.isArray(x.snapshots)?x.snapshots.filter(s=>s&&s.state&&typeof s.hash==="string"):[];snapshots=[...snapshots,...imported].slice(-25);localStorage.setItem(SNAPKEY,JSON.stringify(snapshots));save();toast("Backup restored. Previous state saved as checkpoint.")}catch(e){toast("Restore failed: "+e.message)}$("import-state").value=""}
function brief(){const actions=state.actions.slice().filter(a=>a.status!=="completed").sort(idSort).slice(0,8);return"# Hikmah / Gemma 4 resume brief\n\nSaved: "+nowISO()+"\n\nMain: V12 2/3 (Requests, Rich pass; FastAPI unresolved). V14 and HTTPX reports need raw-log auditing. No leaderboard score confirmed.\nPaper: 18,000 score rows reproduced; Writeup submission unverified. Deadline Nov 12 23:59 UTC.\n\nNext actions:\n"+actions.map(a=>"- P"+a.priority+" ["+a.status+"] "+a.title+" — "+a.next).join("\n")+"\n\nOpen gates:\n"+state.gates.filter(g=>!["verified","completed"].includes(g.status)).map(g=>"- ["+g.status+"] "+g.track+": "+g.label).join("\n")+"\n\nBrowser state is local; use exported backup or GitHub Issues to share. Always verify actual Kaggle run logs and receipts."}
async function copyBrief(){try{await navigator.clipboard.writeText(brief());toast("Resume brief copied")}catch{download("hikmah-resume.md",brief(),"text/markdown");toast("Clipboard unavailable; downloaded resume brief")}}
function githubIssue(){const title="Gemma 4 research checkpoint "+new Date().toISOString().slice(0,10);const url="https://github.com/digiinformed-afk/gemma-4-competitions/issues/new?title="+encodeURIComponent(title)+"&body="+encodeURIComponent(brief().slice(0,6000));window.open(url,"_blank","noopener,noreferrer");toast("Review the issue before submitting; not posted automatically")}
function wire(){
document.addEventListener("click",e=>{const target=e.target.closest("[data-view-target],[data-edit],[data-restore],[data-snapshot-download]");if(!target)return;if(target.dataset.viewTarget){navigate(target.dataset.viewTarget)}else if(target.dataset.edit){openEditor(target.dataset.edit,target.dataset.id)}else if(target.dataset.restore){const snap=snapshots.find(x=>x.id===target.dataset.restore);if(snap&&confirm("Restore checkpoint? The current state will be snapshotted first.")){checkpoint("Before checkpoint restore").then(()=>{state=clone(snap.state);save();toast("Checkpoint restored")}).catch(x=>toast(x.message))}}else if(target.dataset.snapshotDownload){const snap=snapshots.find(x=>x.id===target.dataset.snapshotDownload);if(snap)download("hikmah-snapshot-"+snap.at.slice(0,10)+".json",JSON.stringify({format:"hikmah-control-center",schema:1,exported:nowISO(),state:snap.state,snapshots:[]},null,2))}});
document.querySelectorAll("#nav button").forEach(b=>b.addEventListener("click",()=>navigate(b.dataset.view)));
$("mobile-menu").onclick=()=>document.body.classList.toggle("active-mobile");
$("new-action").onclick=()=>openEditor("actions",null,{track:"main",priority:7});
$("add-version").onclick=()=>openEditor("versions");
$("add-benchmark").onclick=()=>openEditor("benchmarks");
$("new-fastapi-experiment").onclick=()=>{navigate("experiments");openEditor("experiments",null,{version:"V15",track:"main",condition:"Hikmah + cross-file repair",status:"tentative",total:3})};
$("edit-settings").onclick=()=>{const options=state.settings.map((s,i)=>i+": "+s.label).join("\n");const i=prompt("Select setting index to edit:\n"+options);if(i===null)return;const obj=state.settings[Number(i)];if(!obj){toast("Invalid setting");return}const v=prompt(obj.label,obj.value);if(v!==null){obj.value=v;save()}};
$("add-paper-gate").onclick=()=>openEditor("gates",null,{track:"paper"});
$("add-experiment").onclick=()=>openEditor("experiments",null,{track:"main",status:"tentative"});
$("add-failure").onclick=$("add-failure-inline").onclick=()=>openEditor("failures",null,{track:"main",status:"tentative"});
$("add-compute").onclick=()=>openEditor("compute");
$("add-submission").onclick=()=>openEditor("submissions");
$("add-method").onclick=()=>openEditor("methods");
$("editor-form").onsubmit=formSave;
$("close-dialog").onclick=$("cancel-dialog").onclick=()=>$("editor-dialog").close();
$("compare-a").onchange=$("compare-b").onchange=compare;
$("experiment-filter").onchange=renderExperiments;
document.addEventListener("change",e=>{if(e.target.matches("[data-gate]")){const g=state.gates.find(x=>x.id===e.target.dataset.gate);if(g){g.status=e.target.value;save();toast("Gate updated — attach evidence in a checkpoint")}}});
for(const id of ["quick-backup","export-state"])$(id).onclick=backup;
for(const id of ["make-checkpoint","recovery-snapshot"])$(id).onclick=()=>checkpoint().catch(e=>toast(e.message));
$("import-state").onchange=e=>importBackup(e.target.files[0]);
$("recovery-copy").onclick=copyBrief;$("recovery-issue").onclick=githubIssue;
$("recalc-hash").onclick=()=>fingerprint().then(h=>$("fingerprint").textContent=h).catch(e=>toast(e.message));
$("zip-file").onchange=e=>inspectZip(e.target.files[0]);$("yaml-file").onchange=e=>inspectYaml(e.target.files[0]);
}
async function inspectYaml(file){if(!file)return;const txt=await file.text();let lines=['Local YAML preview: '+file.name];for(const term of ["name:","model:","tools:","instruction:","generation_config:","sub_agents:"]){lines.push(term+" "+(txt.includes(term)?"found":"not found"))}lines.push("This is a textual heuristic, not official YAML schema validation.");$("archive-results").innerHTML=lines.map(x=>'<div class="result-row">'+esc(x)+'</div>').join("")}
async function inspectZip(file){
if(!file)return;try{const bytes=new Uint8Array(await file.arrayBuffer());const view=new DataView(bytes.buffer);let eocd=-1;for(let i=bytes.length-22;i>=Math.max(0,bytes.length-65557);i--)if(view.getUint32(i,true)===0x06054b50){eocd=i;break}if(eocd<0)throw Error("End-of-central-directory record not found");const disk=view.getUint16(eocd+4,true),entries=view.getUint16(eocd+10,true),total=view.getUint16(eocd+8,true),cdOffset=view.getUint32(eocd+16,true),cdSize=view.getUint32(eocd+12,true);if(disk!==0||entries!==total||cdOffset===0xffffffff||cdSize===0xffffffff)throw Error("Multi-disk or ZIP64 archive not supported by browser inspector");if(cdOffset+cdSize>bytes.length)throw Error("Invalid central directory boundaries");let cursor=cdOffset;const names=[];let unsafe=[];const dec=new TextDecoder();for(let i=0;i<entries;i++){if(cursor+46>bytes.length||view.getUint32(cursor,true)!==0x02014b50)throw Error("Invalid central directory member");const size=view.getUint16(cursor+28,true),extra=view.getUint16(cursor+30,true),comment=view.getUint16(cursor+32,true);const name=dec.decode(bytes.slice(cursor+46,cursor+46+size));names.push(name);if(name.startsWith("/")||name.includes("\\")||name.split("/").includes(".."))unsafe.push(name);cursor+=46+size+extra+comment;if(cursor>bytes.length)throw Error("Corrupt central directory")};const hash=await sha256(bytes);const required=names.includes("agent.yaml");const suspicious=names.filter(n=>/(^|\/)(eval_config|\.env|__pycache__|private-data|\.git|secret|token)(\/|$)/i.test(n));const rows=[["SHA-256",hash],["Entries",names.length],["Root agent.yaml",required?"Present":"MISSING"],["Unsafe paths",unsafe.length?unsafe.join(", "):"None observed"],["Potentially private / evaluator data",suspicious.length?suspicious.join(", "):"None observed"],["Root entries",names.filter(n=>!n.includes("/")).join(", ")||"None"],["Official Kaggle validator","NOT RUN — cannot confirm submission acceptance"]];set("archive-results",rows.map(([k,v])=>'<div class="result-row"><b>'+esc(k)+':</b> '+esc(v)+'</div>').join(""));toast("ZIP central directory inspected; no organizer checks executed")}catch(e){set("archive-results",'<div class="warning-line">'+esc("Inspection failed: "+e.message)+'</div>')}}
wire();renderAll();navigate(["overview","main","paper","experiments","evidence","research","recovery"].includes(location.hash.slice(1))?location.hash.slice(1):"overview");
$("current-clock").textContent=new Date().toLocaleDateString("en-GB",{day:"2-digit",month:"short",year:"numeric",timeZone:"Asia/Karachi"})+" · PKT";
fingerprint().then(h=>$("fingerprint").textContent=h).catch(()=>{$("fingerprint").textContent="SHA-256 unavailable on insecure origin"});
window.addEventListener("hashchange",()=>{const v=location.hash.slice(1);if(document.getElementById("view-"+v))navigate(v)});
