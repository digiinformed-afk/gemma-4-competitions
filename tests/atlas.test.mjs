import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const html=fs.readFileSync('web/atlas.html','utf8');
const dataText=html.match(/<script type="application\/json" id="atlas-data">([\s\S]*?)<\/script>/)?.[1];
const script=html.match(/<script id="atlas-app">([\s\S]*?)<\/script>/)?.[1];
const D=JSON.parse(dataText);
function boot(){
 const nodes=new Map(),listeners={};
 const get=id=>{if(!nodes.has(id))nodes.set(id,{textContent:id==='atlas-data'?dataText:'',innerHTML:'',value:'',hidden:true,classList:{add(){},remove(){},toggle(){return true}},setAttribute(){},addEventListener(){},focus(){},click(){},remove(){}});return nodes.get(id)};
 const document={getElementById:get,addEventListener:(name,cb)=>listeners[name]=cb,querySelectorAll:()=>[],activeElement:{tagName:'BODY'},body:{appendChild(){}},documentElement:{outerHTML:html},createElement:()=>({click(){},remove(){}})};
 const window={addEventListener(){},scrollTo(){}};
 const context={document,window,location:{hash:''},localStorage:{getItem:()=>null,setItem(){}},setInterval(){},setTimeout(){},clearTimeout(){},URL:{createObjectURL:()=>'',revokeObjectURL(){}},Blob:class{},console};
 vm.runInNewContext(script,context,{timeout:3000});
 return {a:window.Atlas,nodes,listeners};
}
test('atlas data has valid evidence links and distinct reported results',()=>{
 assert.ok(D.sources.length>=25);assert.equal(D.concepts.length,55);
 const ids=new Set(D.sources.map(x=>x.id));assert.equal(ids.size,D.sources.length);
 for(const collection of [D.timeline,D.community,D.bottlenecks,D.plan])for(const item of collection)assert.ok(ids.has(item.source),item.title||item.name);
 for(const s of D.sources){assert.ok(new URL(s.url).protocol==='https:');assert.notEqual(new URL(s.url).hostname,'chatgpt.com','Public atlas must not link private files');}
 assert.equal(D.sources.find(x=>x.id==='latest').kind,'Reported');
 assert.ok(D.timeline.filter(x=>/HTTPX|V12|Larger-memory/.test(x.title)).every(x=>x.status==='Reported'));
});
test('all pages render in both depth modes without unresolved values',()=>{
 const {a}=boot();
 assert.equal(Object.keys(a.views).length,11);
 for(const depth of ['simple','technical']){a.state.depth=depth;for(const [name,view]of Object.entries(a.views)){
  const out=view();assert.ok(out.length>500,name);assert.ok(out.includes('page-title'),name);
  assert.doesNotMatch(out,/\bundefined\b|\bNaN\b/,name);
 }}
});
test('candidate demo can distinguish informative and redundant questions',()=>{
 const {a}=boot();assert.equal(a.survivors([]).length,4);assert.equal(a.survivors(['smoke']).length,4);
 assert.equal(a.survivors(['space']).length,2);assert.equal(a.survivors(['slash']).length,2);
 assert.equal(a.survivors(['space','slash']).map(x=>x.id).join(','),'C');
 assert.equal(a.survivors(['slash','space']).map(x=>x.id).join(','),'C');
});
test('budget planner exposes a ten-minute-per-task overrun',()=>{
 const {a}=boot();const r=a.budgetStats({setup:45,reserve:72,tasks:120,perTask:10});
 assert.equal(r.available,603);assert.equal(r.total,1317);assert.equal(r.over,597);assert.equal(r.avg,5.025);
 const fit=a.budgetStats({setup:45,reserve:72,tasks:120,perTask:5});assert.equal(fit.over,0);
});
test('filters and search preserve evidence coverage',()=>{
 const {a}=boot();for(const type of ['Retrieval','Training','Evaluation','Recovery','Workflow']){a.state.communityFilter=type;assert.ok(a.views.community().includes('What is actually recorded'))}
 a.state.learnCategory='Paper';a.state.learnLevel='Foundation';assert.ok(a.views.learn().includes('No concepts match'));
 for(const query of ['FastAPI','LoRA','HTTPX','entropy','31B'])assert.ok(a.searchItems().some(x=>(x.title+' '+x.text).toLowerCase().includes(query.toLowerCase())),query);
});
test('progress import rejects wrong format and strips unknown state',()=>{
 const {a}=boot();assert.throws(()=>a.validateBackup({}),/backup/);
 const x=a.validateBackup({format:'gemma-atlas-progress',version:1,notes:'<script>text</script>',checks:{entry:true,unknown:true},learned:{c0:true,c1000:true},answers:{'0':1,'1':99}});
 assert.equal(x.notes,'<script>text</script>');assert.equal(Object.keys(x.checks).join(','),'entry');
 assert.equal(Object.keys(x.learned).join(','),'c0');assert.equal(Object.keys(x.answers).join(','),'0');
 assert.throws(()=>a.validateBackup({format:'gemma-atlas-progress',version:1,notes:'',checks:null,learned:{},answers:{}}));
});
test('delegated navigation, quiz, model and depth controls execute',()=>{
 const {a,listeners}=boot();const click=dataset=>listeners.click({target:{closest:()=>({dataset})}});
 click({nav:'models'});assert.equal(a.state.page,'models');click({model:'2'});assert.equal(a.state.model,2);
 click({step:'3'});assert.equal(a.state.step,3);click({action:'next-step'});assert.equal(a.state.step,4);
 click({nav:'quiz'});click({answer:'1'});assert.equal(a.state.answers[0],1);click({action:'quiz-next'});assert.equal(a.state.quiz,1);
 listeners.change({target:{id:'depth',value:'technical',dataset:{}}});assert.equal(a.state.depth,'technical');
 listeners.input({target:{id:'search',value:'FastAPI',dataset:{}}});assert.equal(a.state.search,'FastAPI');
});
test('script and data parse as shipped; standalone content has no external dependencies',()=>{
 new vm.Script(script);
 assert.doesNotMatch(html,/<script[^>]+src=/);
 assert.ok(html.includes('prefers-reduced-motion'));assert.ok(html.includes('max-width:760px'));
 assert.ok(html.includes('aria-label="Search all included knowledge"'));
});
