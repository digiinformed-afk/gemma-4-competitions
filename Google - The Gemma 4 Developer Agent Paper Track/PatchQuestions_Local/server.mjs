import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';
import { json } from './server/helpers.mjs';
import { schema } from './server/validation.mjs';
import { POST as ai } from './server/ai.mjs';
import { GET as discover } from './server/discover.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const data=path.join(root,'data'), uploads=path.join(data,'uploads');
fs.mkdirSync(uploads,{recursive:true});
const stateFile=path.join(data,'workspace.json'), indexFile=path.join(data,'files.json');
function atomic(file,value) { const temp=file+'.tmp'; fs.writeFileSync(temp,JSON.stringify(value,null,2)); fs.renameSync(temp,file); }
if(!fs.existsSync(stateFile)) atomic(stateFile,{workspace:JSON.parse(fs.readFileSync(path.join(root,'server/seed.json'),'utf8')),revision:0});
if(!fs.existsSync(indexFile)) atomic(indexFile,[]);
const load=()=>JSON.parse(fs.readFileSync(stateFile,'utf8'));
if(!schema.safeParse(load().workspace).success) throw new Error('Saved workspace is invalid. Restore data/workspace.json from a backup before starting.');
const port=Number(process.env.PORT || 3000);
if(!Number.isInteger(port)||port<1024||port>65535) throw new Error('PORT must be an integer from 1024 to 65535.');
const mime={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.md':'text/markdown; charset=utf-8','.csv':'text/csv; charset=utf-8','.zip':'application/zip','.gz':'application/gzip','.py':'text/plain; charset=utf-8','.ipynb':'application/json'};
async function route(req) {
 const u=new URL(req.url);
 if(u.pathname==='/api/workspace') {
  if(req.method==='GET') return json(load());
  if(!['POST','PUT'].includes(req.method)) return json({error:'Method not allowed.'},405);
  const raw=await req.text(); if(raw.length>1000000) return json({error:'Workspace must be under 1 MB.'},413);
  let b; try {b=JSON.parse(raw);} catch { return json({error:'Invalid backup JSON.'},400); }
  const result=schema.safeParse(req.method==='POST'?b:b.workspace);
  if(!result.success) return json({error:'Invalid PatchQuestions workspace format.'},400);
  if(req.method==='POST') return json({valid:true});
  const old=load();
  if(!Number.isSafeInteger(b.revision)||b.revision!==old.revision) return json({error:'Another tab saved newer work. Export your changes, then reload.'},409);
  fs.copyFileSync(stateFile,stateFile+'.bak');
  atomic(stateFile,{workspace:result.data,revision:old.revision+1});
  return json({revision:old.revision+1});
 }
 if(u.pathname==='/api/files') {
  if(req.method==='GET') {
   const files=JSON.parse(fs.readFileSync(indexFile,'utf8')), id=u.searchParams.get('id');
   if(!id) return json({files:[...files].reverse()});
   const info=files.find(x=>x.id===id); if(!info) return json({error:'File not found.'},404);
   return new Response(fs.readFileSync(path.join(uploads,info.id)),{headers:{'Content-Type':'application/octet-stream','Content-Disposition':`attachment; filename="${info.name.replace(/[^a-zA-Z0-9._-]/g,'_')}"`}});
  }
  if(req.method!=='POST') return json({error:'Method not allowed.'},405);
  const form=await req.formData(), file=form.get('file');
  if(!(file instanceof File)||!file.size||file.size>5000000) return json({error:'Choose a nonempty file under 5 MB.'},400);
  const id=randomUUID(), bytes=Buffer.from(await file.arrayBuffer());
  const files=JSON.parse(fs.readFileSync(indexFile,'utf8'));
  fs.writeFileSync(path.join(uploads,id),bytes);
  files.push({id,name:file.name.slice(0,180),size:file.size,created_at:new Date().toISOString()});
  try {atomic(indexFile,files);} catch(e) {fs.unlinkSync(path.join(uploads,id));throw e;}
  return json({id});
 }
 if(u.pathname==='/api/ai') return req.method==='POST'?ai(req):json({error:'Method not allowed.'},405);
 if(u.pathname==='/api/discover') return req.method==='GET'?discover(req):json({error:'Method not allowed.'},405);
 if(u.pathname.startsWith('/api/')) return json({error:'Not found.'},404);
 if(!['GET','HEAD'].includes(req.method)) return json({error:'Method not allowed.'},405);
 let relative; try {relative=decodeURIComponent(u.pathname);} catch {return json({error:'Invalid URL.'},400);}
 const base=path.join(root,'public'), target=path.resolve(base,'.'+(relative==='/'?'/index.html':relative));
 if(!target.startsWith(base+path.sep)) return json({error:'Not found.'},404);
 try {if(!fs.statSync(target).isFile()) throw new Error();return new Response(req.method==='HEAD'?null:fs.readFileSync(target),{headers:{'Content-Type':mime[path.extname(target)]||'application/octet-stream'}});} catch {return json({error:'Not found.'},404);}
}
const server=http.createServer(async(incoming,out)=>{
 try {
  const allowed=[`127.0.0.1:${port}`,`localhost:${port}`];
  const codespacesHost=process.env.CODESPACES === 'true' && process.env.CODESPACE_NAME && process.env.GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN ? `${process.env.CODESPACE_NAME}-${port}.${process.env.GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}` : null;
  if(codespacesHost)allowed.push(codespacesHost);
  if(!allowed.includes(incoming.headers.host)) {out.writeHead(403);out.end('Invalid host');return;}
  const origin=`${codespacesHost && incoming.headers.host===codespacesHost?'https':'http'}://${incoming.headers.host}`;
  if(incoming.headers.origin && incoming.headers.origin!==origin) {out.writeHead(403);out.end('Cross-origin requests are not allowed');return;}
  if(incoming.headers['sec-fetch-site']==='cross-site') {out.writeHead(403);out.end('Cross-site requests are not allowed');return;}
  let length=0,chunks=[];
  for await(const chunk of incoming) {length+=chunk.length;if(length>6000000){out.writeHead(413);out.end('Request too large');return;}chunks.push(chunk);}
  const controller=new AbortController();out.on('close',()=>{if(!out.writableEnded)controller.abort();});
  const req=new Request(new URL(incoming.url,origin),{method:incoming.method,headers:incoming.headers,signal:controller.signal,...(!['GET','HEAD'].includes(incoming.method)?{body:Buffer.concat(chunks)}:{})});
  const res=await route(req);
  out.writeHead(res.status,{'X-Content-Type-Options':'nosniff','Cache-Control':'no-store','Referrer-Policy':'strict-origin-when-cross-origin',...Object.fromEntries(res.headers)});
  out.end(Buffer.from(await res.arrayBuffer()));
 }catch {if(!out.headersSent)out.writeHead(500,{'Content-Type':'application/json'});out.end(JSON.stringify({error:'Local request failed. Check that the data folder is writable.'}));}
});
server.on('error',err=>{console.error(err.code==='EADDRINUSE'?`Port ${port} is already in use. Close the other app or set PORT to a different number.`:err.message);process.exitCode=1;});
server.listen(port,'127.0.0.1',()=>console.log(`PatchQuestions Research Lab\nOpen http://127.0.0.1:${port}\nData: ${data}\nKeep this window open. Press Ctrl+C to stop.`));
