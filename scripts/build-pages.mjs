import fs from 'node:fs';
import path from 'node:path';
const root=process.cwd(), site=path.join(root,'site');
const main='Google - The Gemma 4 Developer Agent Competition/gemma-agent-lab';
const paper='Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local';
fs.mkdirSync(site,{recursive:true});
fs.cpSync('web',site,{recursive:true});
fs.cpSync(path.join(main,'dist'),path.join(site,'agent'),{recursive:true});
fs.cpSync(path.join(paper,'public'),path.join(site,'paper'),{recursive:true,filter:src=>!src.includes('__pycache__')});
fs.cpSync('exports',path.join(site,'downloads'),{recursive:true});
fs.mkdirSync(path.join(site,'downloads/agent'),{recursive:true});
for(const f of ['submission.zip','main-track-pilot.ipynb','scripted-smoke.json']) fs.copyFileSync(path.join(main,'artifacts',f),path.join(site,'downloads/agent',f));
const seed=JSON.parse(fs.readFileSync(path.join(paper,'server/seed.json'),'utf8'));
seed.manuscript=fs.readFileSync(path.join(paper,'public/project/PatchQuestions_Writeup.md'),'utf8');
seed.gates={...seed.gates,baseline:true,archive:true,draft:true,novelty:true,cost:true,reproduce:true,submitted:false};
for(const task of seed.tasks){
 if(['replicate','novelty','write'].includes(task.id))task.status='done';
 if(['freeze','gemma','blind','generalize','cost'].includes(task.id)){
  task.title='Optional follow-up: '+task.title;
  task.priority='low';
 }
 if(task.id==='replicate'){task.title='Reproduce the frozen baseline locally';task.detail='Completed: all 18,000 rows reproduced under Windows CPython 3.12.14; see paper-revision/STATUS.md.';}
 if(task.id==='novelty')task.detail='Completed: closest-work comparison and bounded resource contribution documented in the revised manuscript and revision evidence.';
 if(task.id==='write')task.detail='Completed: canonical manuscript revised around reproduced CPU evidence, explicit assumptions and limitations.';
 if(task.id==='release'){task.title='Review final Kaggle rendering and optional notebook access';task.detail='All 16 notebook code cells executed locally. Check the Writeup rendering and word count on Kaggle and any optional notebook Project Link.';task.depends=['write'];}
 if(task.id==='submit')task.depends=['release'];
}
seed.notes.unshift({id:'github-checkpoint-20261107',title:'Current checkpoint — 7 November 2026',text:'The canonical manuscript is revised and reproduced on CPython 3.12.14. All 16 notebook code cells completed. The strict optional model supervisor has 12 passing regression tests. No real Gemma run or Kaggle submission is claimed. Older planned experiments below remain planning history. See the hub and paper-revision/STATUS.md for the current next steps.',created:'2026-11-07'});
fs.writeFileSync(path.join(site,'paper/seed.json'),JSON.stringify(seed));
let app=fs.readFileSync(path.join(site,'paper/app.js'),'utf8');
const begin=app.indexOf('async function api(path, options = {}) {');
const end=app.indexOf('\nfunction toast(',begin);
if(begin<0||end<0)throw new Error('Paper API boundary changed. Review static adapter.');
const adapter=fs.readFileSync('web/paper-api.txt','utf8');
app=app.slice(0,begin)+adapter+app.slice(end);
app=app.replace(/((?:href|src)=["'])\//g,'$1./');
app=app.replace('Kaggle draft prepared','Manuscript draft prepared').replace('Question cost measured','Question cost proxies measured');
fs.writeFileSync(path.join(site,'paper/app.js'),app);
let html=fs.readFileSync(path.join(site,'paper/index.html'),'utf8').replaceAll('href="/','href="./').replaceAll('src="/','src="./');
html=html.replace('<body>','<body><div style="padding:10px 20px;background:#132b27;color:#d4f5df;font:13px system-ui;position:relative;z-index:100"><a style="color:inherit" href="../">← Competition hub</a> · Browser edition: local saves only. Use Export backup / Restore backup to move edits. Use GitHub Issues for shared progress and Codespaces for AI and uploads.</div>');
fs.writeFileSync(path.join(site,'paper/index.html'),html);
let agentHtml=fs.readFileSync(path.join(site,'agent/index.html'),'utf8');
agentHtml=agentHtml.replace('<header>','<header><a href="../" style="font-size:12px">← Hub & current checkpoint</a>');
fs.writeFileSync(path.join(site,'agent/index.html'),agentHtml);
for(const [name,from] of [['MAIN-TRACK-STATUS.md',main+'/MAIN-TRACK-STATUS.md'],['PAPER-STATUS.md',paper+'/paper-revision/STATUS.md'],['PROGRAM-PLAN.md','shared/PROGRAM-PLAN.md']])fs.copyFileSync(from,path.join(site,'downloads',name));
fs.writeFileSync(path.join(site,'.nojekyll'),'');
console.log('Built hub, both dashboards, current paper seed, and downloadable artifacts.');
