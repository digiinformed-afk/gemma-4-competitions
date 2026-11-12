import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
test('published local links resolve under a GitHub project path',()=>{
 for(const file of ['site/index.html','site/paper/index.html','site/agent/index.html']){
  const html=fs.readFileSync(file,'utf8');
  for(const [,link]of html.matchAll(/(?:href|src)="([^"#][^"]*)"/g)){
   if(/^(https?:|data:)/.test(link))continue;
   assert(!link.startsWith('/'),'Must be project relative: '+link);
   const target=path.resolve(path.dirname(file),link.split(/[?#]/)[0]);assert(fs.existsSync(target),file+': '+link);
  }
 }
 const data=JSON.parse(fs.readFileSync('site/paper/seed.json'));
 assert.equal(data.manuscript,fs.readFileSync('Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local/public/project/PatchQuestions_Writeup.md','utf8'));
 assert.equal(data.gates.submitted,false);
 assert.equal(data.tasks.find(t=>t.id==='replicate').status,'done');
 assert(!/(?:href|src)=["']\//.test(fs.readFileSync('site/paper/app.js','utf8')),'Dynamic links must be project relative');
 assert(!/["']\/project\//.test(fs.readFileSync('site/paper/app.js','utf8')),'Helper resource links must be project relative');
});
test('Pages paper adapter persists edits and rejects stale revisions and server features',async()=>{
 const values=new Map();let requested=[];
 const seed=JSON.parse(fs.readFileSync('site/paper/seed.json','utf8'));
 const context=vm.createContext({localStorage:{getItem:k=>values.get(k)||null,setItem:(k,v)=>values.set(k,v)},AbortSignal,fetch:async url=>{requested.push(url);return {ok:true,json:async()=>seed}}});
 vm.runInContext(fs.readFileSync('web/paper-api.txt','utf8')+'\nthis.api=api;',context);
 const state=await context.api('/api/workspace');assert.equal(state.revision,0);
 const updated={...state.workspace,manuscript:'Saved revised text'};
 const saved=await context.api('/api/workspace',{method:'PUT',body:JSON.stringify({workspace:updated,revision:0})});assert.equal(saved.revision,1);
 assert.equal((await context.api('/api/workspace')).workspace.manuscript,'Saved revised text');
 await assert.rejects(context.api('/api/workspace',{method:'PUT',body:JSON.stringify({workspace:updated,revision:0})}),e=>e.status===409);
 await assert.rejects(context.api('/api/ai',{method:'POST'}),/full Node app/);
 await context.api('/baseline.json');assert.equal(requested.at(-1),'./baseline.json');
});
test('imported artifacts match original bytes or explicit reviewed revisions',()=>{
 const manifest=JSON.parse(fs.readFileSync('docs/SOURCE-MANIFEST.json'));
 const revised=new Map((manifest.reviewed_revisions||[]).map(f=>[f.path,f]));
 for(const f of manifest.files){
  if(f.path==='README.md'||f.path==='Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local/server.mjs')continue;
  const revision=revised.get(f.path);
  if(revision){assert.equal(revision.original_sha256,f.sha256);assert(revision.reason);}
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(f.path)).digest('hex'),revision?.sha256||f.sha256,f.path);
 }
});
