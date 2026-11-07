import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
test('local app persistence, validation, files, and request isolation',async()=>{
 const temp=await fs.mkdtemp(path.join(os.tmpdir(),'patchquestions-test-'));
 for(const name of ['server','public','server.mjs','package.json']) await fs.cp(path.join(root,name),path.join(temp,name),{recursive:true});
 const port=19000+Math.floor(Math.random()*10000),base=`http://127.0.0.1:${port}`;
 let child;
 const start=async()=>{child=spawn(process.execPath,['server.mjs'],{cwd:temp,env:{...process.env,PORT:String(port)},stdio:['ignore','pipe','pipe']});await new Promise((ok,no)=>{child.stdout.once('data',ok);child.once('error',no);child.once('exit',code=>no(new Error('Server exited '+code)));});};
 const stop=async()=>{const done=once(child,'exit');child.kill();await done;child=null;};
 try {
  await start();
  const html=await fetch(base);assert.match(await html.text(),/PatchQuestions/);
  const sources=await (await fetch(base+'/project/research-library.json')).json();assert.equal(sources.length,34);
  for(const f of ['/app.js','/style.css','/research-utils.js','/baseline.json','/cases.json','/project/scores.csv','/project/PatchQuestions.ipynb'])assert.equal((await fetch(base+f)).status,200,f);
  const first=await (await fetch(base+'/api/workspace')).json();assert.equal(first.revision,0);
  first.workspace.notes.push({id:'local-smoke',title:'Test persistence',text:'Saved locally.',created:new Date().toISOString()});
  const put=(body)=>fetch(base+'/api/workspace',{method:'PUT',headers:{'content-type':'application/json'},body:JSON.stringify(body)});
  assert.equal((await put(first)).status,200);assert.equal((await put(first)).status,409);
  assert.equal((await put({workspace:{},revision:1})).status,400);
  assert.equal((await fetch(base+'/api/workspace',{method:'POST',body:JSON.stringify(first.workspace)})).status,200);
  assert.equal((await fetch(base+'/api/workspace',{method:'POST',body:'broken'})).status,400);
  const form=new FormData();form.set('file',new File(['a,b\n1,2\n'],'proof.csv'));
  const uploaded=await (await fetch(base+'/api/files',{method:'POST',body:form})).json();assert.ok(uploaded.id);
  assert.equal(await (await fetch(base+'/api/files?id='+uploaded.id)).text(),'a,b\n1,2\n');
  assert.equal((await (await fetch(base+'/api/files')).json()).files.length,1);
  assert.equal((await fetch(base+'/api/files?id=../../server.mjs')).status,404);
  assert.equal((await fetch(base+'/server.mjs')).status,404);
  assert.equal((await fetch(base+'/api/workspace',{headers:{origin:'https://untrusted.example'}})).status,403);
  assert.equal((await fetch(base+'/api/ai',{method:'POST',body:'{}'})).status,400);
  await stop();await start();
  const saved=await (await fetch(base+'/api/workspace')).json();assert.equal(saved.revision,1);assert.ok(saved.workspace.notes.find(n=>n.id==='local-smoke'));
  assert.equal(await (await fetch(base+'/api/files?id='+uploaded.id)).text(),'a,b\n1,2\n');
  assert.ok(JSON.parse(await fs.readFile(path.join(temp,'data/workspace.json.bak'),'utf8')));
 } finally {if(child)await stop();await fs.rm(temp,{recursive:true,force:true});}
});
test('AI adapters use selected provider and parse simulated answers',async()=>{
 const {POST}=await import('../server/ai.mjs');const original=globalThis.fetch;
 const key='test-key-not-a-real-credential';
 try {for(const provider of ['openai','gemini','anthropic','groq','openrouter']) {
  globalThis.fetch=async(url,options)=>{assert.ok(url.startsWith('https://'));assert.ok(JSON.stringify(options.headers).includes(key));return Response.json({output:[{content:[{type:'output_text',text:'OpenAI answer'}]}],candidates:[{content:{parts:[{text:'Gemini answer'}]}}],content:[{type:'text',text:'Anthropic answer'}],choices:[{message:{content:'Chat answer'}}]});};
  const response=await POST(new Request('http://127.0.0.1/api/ai',{method:'POST',body:JSON.stringify({action:'generate',provider,apiKey:key,model:'test-model',prompt:'Next step?'})}));
  assert.equal(response.status,200,provider);assert.match((await response.json()).answer,/answer/);
  globalThis.fetch=async()=>Response.json({data:[{id:'test-model'}],models:[{name:'models/test-model',supportedGenerationMethods:['generateContent']}]});
  const models=await POST(new Request('http://127.0.0.1/api/ai',{method:'POST',body:JSON.stringify({action:'models',provider,apiKey:key})}));assert.equal((await models.json()).models[0].id,'test-model');
 }
 globalThis.fetch=async()=>Response.json({error:{message:'Invalid '+key}},{status:401});
 const redacted=await POST(new Request('http://127.0.0.1/api/ai',{method:'POST',body:JSON.stringify({action:'models',provider:'openai',apiKey:key})}));assert.ok(!(await redacted.text()).includes(key));
 }finally{globalThis.fetch=original;}
});
