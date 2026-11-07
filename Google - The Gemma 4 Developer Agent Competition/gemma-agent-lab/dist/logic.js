export function budget({tasks,setup,reserve}){if(!Number.isInteger(tasks)||tasks<1||!Number.isFinite(setup)||!Number.isFinite(reserve)||setup<0||reserve<0||setup+reserve>=720)return null;return (720-setup-reserve)/tasks;}
export function wilson(success,total){if(!Number.isInteger(success)||!Number.isInteger(total)||total<1||success<0||success>total)throw Error('Invalid success count');const z=1.959963984540054,p=success/total,d=1+z*z/total,c=(p+z*z/(2*total))/d,h=z*Math.sqrt(p*(1-p)/total+z*z/(4*total*total))/d;return [Math.max(0,c-h),Math.min(1,c+h)];}
export function validateState(s){
 const obj=v=>v&&typeof v==='object'&&!Array.isArray(v);
 const str=(v,max=10000)=>typeof v==='string'&&v.length<=max;
 if(!obj(s)||s.version!==1)throw Error('Unsupported workspace format.');
 for(const k of ['done','read','saved','notes']){if(!obj(s[k])||Object.keys(s[k]).length>10000)throw Error('Invalid '+k);for(const [id,v] of Object.entries(s[k]))if(['__proto__','constructor','prototype'].includes(id)||!str(id,500)||(k==='notes'?!str(v,100000):typeof v!=='boolean'))throw Error('Invalid '+k+' entry');}
 if(!obj(s.budget)||!Number.isInteger(s.budget.tasks)||s.budget.tasks<1||s.budget.tasks>10000||!['setup','reserve'].every(k=>Number.isFinite(s.budget[k])&&s.budget[k]>=0&&s.budget[k]<=720))throw Error('Invalid planner inputs');
 if(!Array.isArray(s.runs)||s.runs.length>10000||!Array.isArray(s.custom)||s.custom.length>1000)throw Error('Invalid collection');
 for(const r of s.runs)if(!obj(r)||typeof r.id!=='string'||!/^[a-zA-Z0-9-]{1,100}$/.test(r.id))throw Error('Invalid evaluation identifier');
 const ids=new Set();for(const r of s.runs){if(!obj(r)||!['id','name','model','split','revision','date','notes'].every(k=>str(r[k]))||!r.name.trim()||!r.split.trim()||!r.revision.trim()||!['31B','12B','E4B','E2B'].includes(r.model)||!/^\d{4}-\d{2}-\d{2}$/.test(r.date)||!Number.isFinite(Date.parse(r.date))||!['total','resolved','timeouts'].every(k=>Number.isInteger(r[k]))||r.total<1||r.total>1e6||r.resolved<0||r.timeouts<0||r.resolved+r.timeouts>r.total||!Number.isFinite(r.minutes)||r.minutes<=0||r.minutes>1e6||ids.has(r.id))throw Error('Invalid evaluation record');ids.add(r.id);}
 for(const r of s.custom){if(!obj(r)||!['id','title','url','author','year','type','priority','summary','action'].every(k=>str(r[k],10000))||!/^user-[a-zA-Z0-9-]+$/.test(r.id)||ids.has(r.id)||!['Official','Paper','Article','Documentation','Dataset'].includes(r.type)||!['Essential','Useful','Later'].includes(r.priority))throw Error('Invalid resource');let u;try{u=new URL(r.url);}catch{throw Error('Invalid source URL');}if(!['https:','http:'].includes(u.protocol)||u.username||u.password)throw Error('Use an HTTP or HTTPS source URL without credentials.');ids.add(r.id);}
 return true;
}
