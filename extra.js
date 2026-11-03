/* ===== Extra tools (10 new) for EN site ===== */
"use strict";

/* ---------- Lorem Ipsum ---------- */
const LOREM_WORDS = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum").split(" ");
function randWords(n){let s=[];for(let i=0;i<n;i++){s.push(LOREM_WORDS[Math.floor(Math.random()*LOREM_WORDS.length)]);}return s;}
function cap(w){return w.charAt(0).toUpperCase()+w.slice(1);}
function loremGen(){
  const n=parseInt(document.getElementById('lorem-count').value)||3;
  const classic=document.getElementById('lorem-classic').checked;
  const out=[];
  for(let p=0;p<n;p++){
    let words=randWords(45+Math.floor(Math.random()*30));
    if(p===0&&classic){words=loremClassic().split(/\s+/).concat(words);words=words.slice(0,60);}
    let text=cap(words.join(" "))+".";
    text=text.replace(/ ([.])/g,"$1");
    out.push(text);
  }
  document.getElementById('lorem-output').value=out.join("\n\n");
}
function loremClassic(){return "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.";}
function loremCopy(){navigator.clipboard.writeText(document.getElementById('lorem-output').value).then(()=>alert('Copied!'));}

/* ---------- Cron parser ---------- */
const CRON_FIELDS=[{n:"minute",min:0,max:59},{n:"hour",min:0,max:23},{n:"day of month",min:1,max:31},{n:"month",min:1,max:12},{n:"day of week",min:0,max:7}];
const MONTHS=["January","February","March","April","May","June","July","August","September","October","November","December"];
const DOW=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
function cronNum(tok,f){
  if(!/^\d+$/.test(tok))throw new Error("bad");
  const v=+tok;
  if(v<f.min||v>f.max)throw new Error("bad");
  return v;
}
function parseCronField(expr,f){
  if(expr==="*")return "every "+f.n;
  const parts=[];
  expr.split(",").forEach(seg=>{
    if(seg.startsWith("*/")){
      const st=seg.slice(2);
      if(!/^\d+$/.test(st)||+st<=0||+st>f.max)throw new Error("bad");
      parts.push("every "+st+" "+f.n+"s");
    }
    else if(seg.includes("-")){
      const[a,b]=seg.split("-");cronNum(a,f);cronNum(b,f);
      let s=fieldWord(a,f),e=fieldWord(b,f);parts.push("from "+s+" to "+e);
    }
    else{cronNum(seg,f);parts.push("at "+fieldWord(seg,f));}
  });
  return parts.join(" and ");
}
function fieldWord(v,f){
  v=parseInt(v,10);
  if(isNaN(v))return "?";
  if(f.n==="month")return MONTHS[v-1]||("month "+v);
  if(f.n==="day of week")return DOW[v%7]||("day "+v);
  if(f.n==="hour")return v+":00";
  return String(v);
}
// 把单个 cron 字段转成可读短语；通配符返回 null 由调用方处理默认文案。
// 支持：通配、单值、范围 a-b、列表 a,b,c、步长。
function summarizeField(expr,f){
  if(expr==="*")return null;
  const segs=expr.split(",");
  const parts=segs.map(seg=>{
    if(seg.startsWith("*/"))return "every "+seg.slice(2)+" "+f.n+"s";
    if(seg.includes("-")){const[a,b]=seg.split("-");return fieldWord(a,f)+" to "+fieldWord(b,f);}
    return fieldWord(seg,f);
  });
  return parts.join(", ");
}
function cronExplain(){
  const raw=document.getElementById('cron-input').value.trim();
  const out=document.getElementById('cron-output');
  const f=raw.split(/\s+/);
  if(f.length!==5){out.textContent="❌ A standard cron expression has exactly 5 fields: minute hour day-of-month month day-of-week. Quartz (6 fields) is not supported yet.";return;}
  const lines=[];
  for(let i=0;i<5;i++){
    try{lines.push("• "+cap(CRON_FIELDS[i].n)+": "+parseCronField(f[i],CRON_FIELDS[i]));}
    catch(e){out.textContent="❌ Invalid field: "+CRON_FIELDS[i].n;return;}
  }
  let summary="In plain English: this job runs ";
  const mt=summarizeField(f[0],CRON_FIELDS[0]); if(mt)summary+=mt+" ";
  const ht=summarizeField(f[1],CRON_FIELDS[1]); if(ht)summary+=ht+" ";
  summary+="on days "+(summarizeField(f[2],CRON_FIELDS[2])||"of every month")+", ";
  summary+="in "+(summarizeField(f[3],CRON_FIELDS[3])||"every month")+", ";
  summary+="when it is "+(summarizeField(f[4],CRON_FIELDS[4])||"any day of the week")+".";
  out.textContent=lines.join("\n")+"\n\n"+summary+"\n\nCommon examples:\n*/5 * * * *  → every 5 minutes\n0 * * * *  → every hour\n0 0 * * *  → daily at midnight\n0 9 * * 1-5  → weekdays at 9 AM\n0 0 1 * *  → first day of every month";
}
function describeField(e,name){if(e.startsWith("*/"))return "every "+e.slice(2)+" minutes";if(e.includes("-"))return "at minutes "+e;return "at minute "+e;}
function cronFill(v){document.getElementById('cron-input').value=v;cronExplain();}
function cap(s){return s.charAt(0).toUpperCase()+s.slice(1);}

/* ---------- Text diff (LCS line diff) ---------- */
function diffLines(a,b){
  const A=a.split("\n"),B=b.split("\n"),n=A.length,m=B.length;
  const dp=Array.from({length:n+1},()=>new Array(m+1).fill(0));
  for(let i=n-1;i>=0;i--)for(let j=m-1;j>=0;j--)
    dp[i][j]=A[i]===B[j]?dp[i+1][j+1]+1:Math.max(dp[i+1][j],dp[i][j+1]);
  const out=[];let i=0,j=0;
  while(i<n&&j<m){
    if(A[i]===B[j]){out.push({t:" ",s:A[i]});i++;j++;}
    else if(dp[i+1][j]>=dp[i][j+1]){out.push({t:"-",s:A[i]});i++;}
    else{out.push({t:"+",s:B[j]});j++;}
  }
  while(i<n){out.push({t:"-",s:A[i++]});}
  while(j<m){out.push({t:"+",s:B[j++]});}
  return out;
}
function diffRun(){
  const r=diffLines(document.getElementById('diff-a').value,document.getElementById('diff-b').value);
  let same=0,add=0,del=0;
  r.forEach(l=>{if(l.t===" ")same++;else if(l.t==="+")add++;else del++;});
  const pre=document.getElementById('diff-output');
  pre.textContent="";
  r.forEach(l=>{
    const span=document.createElement('div');
    span.textContent=l.t+" "+l.s;
    span.className=l.t==="+"?"diff-add":(l.t==="-"?"diff-del":"diff-same");
    pre.appendChild(span);
  });
  document.getElementById('diff-stats').textContent="Summary: "+same+" unchanged, "+add+" added (+), "+del+" removed (-)";
}

/* ---------- HTML entities ---------- */
function entitiesEncode(){
  const ta=document.createElement('textarea');
  ta.textContent=document.getElementById('entities-input').value;
  document.getElementById('entities-output').value=ta.innerHTML;
}
function entitiesDecode(){
  const ta=document.createElement('textarea');
  ta.innerHTML=document.getElementById('entities-input').value;
  document.getElementById('entities-output').value=ta.value;
}

/* ---------- Slug generator ---------- */
function slugify(){
  let s=document.getElementById('slug-input').value;
  if(document.getElementById('slug-lower').checked)s=s.toLowerCase();
  s=s.normalize("NFKD").replace(/[\u0300-\u036f]/g,"");
  s=s.replace(/[^a-zA-Z0-9]+/g,"-").replace(/^-+|-+$/g,"");
  document.getElementById('slug-output').value=s;
}
function slugCopy(){navigator.clipboard.writeText(document.getElementById('slug-output').value).then(()=>alert('Copied!'));}

/* ---------- Password strength ---------- */
function pwStrength(){
  const p=document.getElementById('pw-input').value;
  const checks=[
    ["At least 12 characters",p.length>=12],
    ["Contains lowercase letters",/[a-z]/.test(p)],
    ["Contains uppercase letters",/[A-Z]/.test(p)],
    ["Contains digits",/[0-9]/.test(p)],
    ["Contains symbols",/[^a-zA-Z0-9]/.test(p)],
    ["No repeated character 3+ times in a row",!/(.)\1\1/.test(p)]
  ];
  let pool=0;
  if(/[a-z]/.test(p))pool+=26;if(/[A-Z]/.test(p))pool+=26;if(/[0-9]/.test(p))pool+=10;if(/[^a-zA-Z0-9]/.test(p))pool+=33;
  const bits=p.length*Math.log2(pool||1);
  const guesses=Math.pow(2,bits);
  const seconds=guesses/1e10; // 10 billion guesses/sec offline attacker
  const fmt=s=>{if(s<1)return "instantly";if(s<3600)return Math.round(s)+" seconds";if(s<86400*365)return Math.round(s/86400)+" days";const y=s/(86400*365);if(y<1e6)return Math.round(y).toLocaleString()+" years";if(y<1e9)return Math.round(y/1e6)+" million years";return "billions of years";};
  const score=checks.filter(c=>c[1]).length;
  const label=bits<40?"Very weak":bits<60?"Weak":bits<80?"Moderate":bits<100?"Strong":"Very strong";
  const bar=document.getElementById('pw-bar');
  bar.style.width=Math.min(100,bits)+"%";
  bar.className="pw-bar-fill "+(bits<60?"pw-bad":bits<80?"pw-mid":"pw-good");
  document.getElementById('pw-label').textContent="Strength: "+label+" ("+Math.round(bits)+" bits of entropy, offline crack time: "+fmt(seconds)+")";
  const ul=document.getElementById('pw-checks');
  ul.innerHTML="";
  checks.forEach(c=>{const li=document.createElement('li');li.textContent=(c[1]?"✅ ":"❌ ")+c[0];ul.appendChild(li);});
}

/* ---------- Image to Base64 ---------- */
function imgToB64(input){
  const f=input.files[0];
  if(!f)return;
  const r=new FileReader();
  r.onload=e=>{
    const d=e.target.result;
    document.getElementById('img-output').value=d;
    const pv=document.getElementById('img-preview');
    pv.src=d;
    pv.style.display='block';
    document.getElementById('img-info').textContent=f.name+" — "+(f.size/1024).toFixed(1)+" KB — Base64 size: "+(d.length/1024).toFixed(1)+" KB";
  };
  r.readAsDataURL(f);
}
function imgB64Copy(){navigator.clipboard.writeText(document.getElementById('img-output').value).then(()=>alert('Copied!'));}

/* ---------- URL parser ---------- */
function urlParse(){
  try{
    const u=new URL(document.getElementById('urlp-input').value.trim());
    let out="Protocol: "+u.protocol+"\nHost: "+u.hostname+(u.port?("\nPort: "+u.port):"")+"\nPath: "+u.pathname;
    if(u.hash)out+="\nHash: "+u.hash;
    if(u.search){
      out+="\n\nQuery parameters:";
      u.searchParams.forEach((v,k)=>{out+="\n  "+k+" = "+v;});
    }
    document.getElementById('urlp-output').textContent=out;
  }catch(e){document.getElementById('urlp-output').textContent="❌ Invalid URL. Include the protocol, e.g. https://example.com/path?q=1";}
}

/* ---------- Color picker（复用 app.js 的统一 colorUpdate，避免同名覆盖） ---------- */
function cpFromHex(){const v=document.getElementById('cp-hex').value.trim();if(v)colorUpdate(v);}
function cpCopy(id){navigator.clipboard.writeText(document.getElementById(id).value).then(()=>alert('Copied!'));}

/* ---------- Text ↔ Binary ---------- */
function textToBinary(){
  const t=document.getElementById('bin-input').value;
  const out=[];
  for(const ch of new TextEncoder().encode(t)){out.push(ch.toString(2).padStart(8,"0"));}
  document.getElementById('bin-output').value=out.join(" ");
}
function binaryToText(){
  const parts=document.getElementById('bin-input').value.trim().split(/\s+/).filter(Boolean);
  try{
    const bytes=parts.map(p=>parseInt(p,2));
    if(bytes.some(b=>isNaN(b)||b<0||b>255))throw new Error("not valid binary bytes");
    document.getElementById('bin-output').value=new TextDecoder().decode(new Uint8Array(bytes));
  }catch(e){document.getElementById('bin-output').value="❌ Invalid input: use sequences of 8-bit binary numbers separated by spaces (e.g. 01001000 01101001).";}
}
