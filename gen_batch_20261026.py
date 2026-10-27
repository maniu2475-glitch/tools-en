# -*- coding: utf-8 -*-
import generate_tool_page as g
import io, re

TOOLS = {
"tally-counter.html": dict(
 title="Tally Counter Online - Click Counter (Clicker)",
 og_title="Tally counter",
 desc="Free online tally counter: click or press space to count people, laps, reps or inventory. Offline-friendly, no signup, runs entirely in your browser.",
 h1="Online Tally Counter",
 body="""<div class="opt-group"><input type="number" id="tc-step" value="1" min="-100" max="100" style="width:90px" title="step per click"><label style="margin-left:8px"> step (+/-)</label></div>
<div style="font-size:96px;font-weight:700;text-align:center;margin:24px 0;color:#4f6ef7" id="tc-display">0</div>
<div class="btn-group"><button class="btn" onclick="tcAdd(1)" style="font-size:22px;padding:16px 40px">+ Count</button>
<button class="btn btn-outline" onclick="tcAdd(-1)">Undo (−)</button>
<button class="btn btn-outline" onclick="tcReset()">Reset</button></div>
<p style="margin-top:16px;color:#6a737d">Tip: press <kbd>Space</kbd> or <kbd>Enter</kbd> to count, <kbd>Backspace</kbd> to undo. The value is saved in localStorage so it survives page reloads.</p>
<script>
var tcVal=parseInt(localStorage.getItem('tc-val')||'0',10)||0;
var tcStep=parseInt(localStorage.getItem('tc-step')||'1',10)||1;
function tcSave(){localStorage.setItem('tc-val',tcVal);localStorage.setItem('tc-step',tcStep);}
function tcRender(){document.getElementById('tc-display').textContent=tcVal;}
function tcAdd(d){tcVal+=tcStep*d;tcSave();tcRender();}
function tcReset(){if(confirm('Reset counter to 0?')){tcVal=0;tcSave();tcRender();}}
document.getElementById('tc-step').onchange=function(){tcStep=parseInt(this.value,10)||1;tcSave();};
document.addEventListener('keydown',function(e){if(e.target.tagName==='INPUT')return;if(e.code==='Space'||e.key==='Enter'){e.preventDefault();tcAdd(1);}else if(e.key==='Backspace'){e.preventDefault();tcAdd(-1);}});
tcRender();
</script>""",
 about="""A tally counter (also called a click counter or clicker) is one of the simplest and most useful counting tools. People use it to count people entering an event, tally scores in a game, count laps, reps at the gym, inventory items, or tally survey responses. This online version replaces the physical mechanical clicker: just click the big button or tap the space bar. You can set a custom step (useful when counting in dozens or boxes of 12), undo mistakes, and the value is stored in your browser's localStorage so an accidental page refresh won't wipe your count. Like every tool on this site it runs 100% client-side and works offline once loaded."""),

"hex-to-ascii.html": dict(
 title="Hex to ASCII Text Converter - Free Online",
 og_title="Hex to ASCII converter",
 desc="Convert hexadecimal (hex) bytes to ASCII text and back instantly. Supports 0x prefixes, spaces or plain hex, fully client-side.",
 h1="Hex ⇄ ASCII Text Converter",
 body="""<div class="opt-group"><label style="font-weight:600">Hex input</label></div>
<textarea id="hx-in" rows="4" style="width:100%;font-family:monospace" placeholder="48 65 6c 6c 6f or 0x48656c6c6f" oninput="hxConv()"></textarea>
<div class="btn-group"><button class="btn" onclick="hxConv()">Convert</button><button class="btn btn-outline" onclick="document.getElementById('hx-out').select();document.execCommand('copy')">Copy result</button></div>
<div class="opt-group"><label style="font-weight:600">ASCII text output</label></div>
<textarea id="hx-out" rows="4" readonly style="width:100%;font-family:monospace" oninput="hxBack()"></textarea>
<div class="btn-group"><button class="btn btn-outline" onclick="hxBack()">Convert text → hex</button>
<label style="margin-left:12px"><input type="checkbox" id="hx-sp" checked> separate bytes with spaces</label></div>
<script>
function cleanHex(s){var m=s.replace(/0[xX]/g,'').replace(/[^0-9a-fA-F]/g,'');if(m.length%2)m=m+'0';return m;}
function hxConv(){var m=cleanHex(document.getElementById('hx-in').value);var out='';for(var i=0;i<m.length;i+=2){var c=parseInt(m.substr(i,2),16);out+=(c>=32&&c<127)?String.fromCharCode(c):'.';}document.getElementById('hx-out').value=out;}
function hxBack(){var s=document.getElementById('hx-out').value,sp=document.getElementById('hx-sp').checked,h='';for(var i=0;i<s.length;i++){h+=s.charCodeAt(i).toString(16).padStart(2,'0');if(sp)h+=' ';}document.getElementById('hx-in').value=h.trim();}
</script>""",
 about="""Every character in a computer is stored as a number, and hexadecimal is the most common way humans write those numbers down. Hex-to-ASCII conversion is a daily task for anyone working with network packets, debugging file formats, reverse engineering, or reading memory dumps: 0x48 0x65 0x6c 0x6c 0x6f spells "Hello". This converter accepts hex with or without spaces, colons or 0x prefixes, shows a dot for non-printable bytes, and also converts in the reverse direction so you can check what your text looks like on the wire. Everything runs locally in your browser."""),

"csv-to-tsv.html": dict(
 title="CSV to TSV Converter Online - Tab-Separated Values",
 og_title="CSV to TSV converter",
 desc="Convert CSV (comma-separated) data to TSV (tab-separated) and back. Handles quoted fields with embedded commas, 100% in-browser.",
 h1="CSV ⇄ TSV Converter",
 body="""<div class="opt-group"><label style="font-weight:600">Input (CSV or TSV auto-detected)</label></div>
<textarea id="ct-in" rows="7" style="width:100%;font-family:monospace" placeholder='name,city&#10;"Doe, John","New York"' oninput="ctConv()"></textarea>
<div class="btn-group"><button class="btn" onclick="ctConv()">Convert</button>
<label style="margin-left:12px"><input type="radio" name="ctdir" value="2tsv" checked> CSV → TSV</label>
<label style="margin-left:8px"><input type="radio" name="ctdir" value="2csv"> TSV → CSV</label></div>
<div class="opt-group"><label style="font-weight:600">Output</label></div>
<textarea id="ct-out" rows="7" readonly style="width:100%;font-family:monospace"></textarea>
<script>
function parseCSV(text,delim){var rows=[],row=[],cur='',q=false;for(var i=0;i<text.length;i++){var c=text[i];if(q){if(c=='"'){if(text[i+1]=='"'){cur+='"';i++;}else q=false;}else cur+=c;}else{if(c=='"')q=true;else if(c==delim){row.push(cur);cur='';}else if(c=='\n'){row.push(cur);rows.push(row);row=[];cur='';}else if(c!='\r')cur+=c;}}if(cur!==''||row.length){row.push(cur);rows.push(row);}return rows;}
function ctConv(){var t=document.getElementById('ct-in').value.trim();if(!t)return;var dir=document.querySelector('input[name=ctdir]:checked').value;var src=dir=='2tsv'?',':'\t',dst=dir=='2tsv'?'\t':',';var rows=parseCSV(t,src);var out=rows.map(function(r){return r.map(function(f){if(dir=='2csv'&&(/[",\n]/.test(f)))return '"'+f.replace(/"/g,'""')+'"';return f;}).join(dst);}).join('\n');document.getElementById('ct-out').value=out;}
</script>""",
 about="""CSV (comma-separated values) and TSV (tab-separated values) are the two most common plain-text spreadsheet formats. TSV is preferred by Unix tools, databases like PostgreSQL's COPY, and bioinformatics pipelines because tabs almost never appear in data, so no quoting is needed; CSV is the default everywhere else. Converting between them is tricky when fields contain commas or quotes - a naive find-and-replace will corrupt your data. This converter properly parses quoted fields ("" escapes a quote inside a quoted field), handles multi-line quoted cells, and quotes fields as needed when going back to CSV. All parsing happens in your browser."""),

"word-to-number.html": dict(
 title="Word to Number Converter - Number Words to Digits",
 og_title="Word to number converter",
 desc="Convert English number words to digits: 'twenty-three thousand four hundred' → 23400, plus number to words.",
 h1="Word ⇄ Number Converter",
 body="""<div class="opt-group"><label style="font-weight:600">Words</label></div>
<input type="text" id="wn-in" style="width:100%" placeholder="two million forty-eight thousand one hundred seven" oninput="wnConv()">
<div class="btn-group"><button class="btn" onclick="wnConv()">Words → Number</button><button class="btn btn-outline" onclick="wnBack()">Number → Words</button></div>
<div class="opt-group"><label style="font-weight:600">Number</label></div>
<input type="text" id="wn-out" readonly style="width:100%;font-family:monospace">
<script>
var ONES=['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'];
var TENS=[,,,'','','','','','','','','','','','','','','','','',''];TENS[2]='twenty';TENS[3]='thirty';TENS[4]='forty';TENS[5]='fifty';TENS[6]='sixty';TENS[7]='seventy';TENS[8]='eighty';TENS[9]='ninety';
var SCALES={'hundred':100,'thousand':1000,'million':1000000,'billion':1000000000,'trillion':1000000000000};
function words2num(s){s=s.toLowerCase().replace(/[^a-z ]/g,'').replace(/\band\b/g,' ').replace(/-/g,' ').replace(/\s+/g,' ').trim();if(!s)return NaN;var parts=s.split(' ');var total=0,current=0;for(var i=0;i<parts.length;i++){var p=parts[i],v=ONES.indexOf(p);if(v>=0&&v<20){current+=v;}else if(TENS.indexOf(p)>0){current+=TENS.indexOf(p)*10;}else if(p=='hundred'){current=(current||1)*100;}else if(SCALES[p]){var sc=SCALES[p];if(sc==100){current*=100;}else{total+=(current||0)*sc;current=0;}}else if(p=='zero'&&parts.length==1){return 0;}else{return NaN;}}return total+current;}
function num2words(n){if(!isFinite(n)||n<0||Math.floor(n)!==n)return'';if(n<20)return ONES[n];if(n<100){return TENS[Math.floor(n/10)]+(n%10?'-'+ONES[n%10]:'');}if(n<1000){return ONES[Math.floor(n/100)]+' hundred'+(n%100?' and '+num2words(n%100):'');}var sc=[[1000000000,'billion'],[1000000,'million'],[1000,'thousand']];for(var k=0;k<sc.length;k++){if(n>=sc[k][0]){return num2words(Math.floor(n/sc[k][0]))+' '+sc[k][1]+(n%sc[k][0]?' '+num2words(n%sc[k][0]):'');}}return '';}
function wnConv(){var v=words2num(document.getElementById('wn-in').value);document.getElementById('wn-out').value=isNaN(v)?'Could not parse':v.toLocaleString();}
function wnBack(){var n=parseInt(document.getElementById('wn-out').value.replace(/,/g,''),10);document.getElementById('wn-in').value=isNaN(n)?'':num2words(n);}
</script>""",
 about="""Writing numbers as English words ("seventy-two thousand five hundred") appears on legal documents, cheques, invoices, song lyrics, subtitles, and NLP training data. Converting them back to digits is a classic interview question and a real-world chore: you must handle hyphens, "and", compound scales like "two hundred fifty thousand", and the short-scale words up to a trillion. This converter parses all of that and also works in reverse, turning 1,250,000 into "one million two hundred fifty thousand" using British-style "and" in the hundreds. It runs entirely in your browser and handles values from zero to the trillions."""),

"decimal-to-fraction.html": dict(
 title="Decimal to Fraction Calculator - Simplified",
 og_title="Decimal to fraction",
 desc="Convert any decimal to a simplified fraction: 0.75 → 3/4, 1.625 → 13/8. Also fraction to decimal. Free, instant, client-side.",
 h1="Decimal ⇄ Fraction Converter",
 body="""<div class="opt-group"><label style="font-weight:600">Decimal</label></div>
<input type="text" id="df-dec" style="width:100%;font-family:monospace" placeholder="0.375" oninput="dfDec()">
<div class="btn-group"><button class="btn" onclick="dfDec()">Decimal → Fraction</button></div>
<div class="opt-group"><label style="font-weight:600">Fraction (a/b)</label></div>
<input type="text" id="df-frac" style="width:100%;font-family:monospace" placeholder="7/8" oninput="dfFrac()">
<div class="btn-group"><button class="btn btn-outline" onclick="dfFrac()">Fraction → Decimal</button></div>
<div class="opt-group"><label style="font-weight:600">Result</label></div>
<div style="font-size:32px;font-weight:700;color:#4f6ef7" id="df-out">—</div>
<script>
function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){var t=b;b=a%b;a=t;}return a;}
function dfDec(){var s=document.getElementById('df-dec').value.trim().replace(/,/g,'');if(!/^-?\d*\.?\d+$/.test(s)){document.getElementById('df-out').textContent='Enter a decimal like 0.375';return;}var neg=s[0]=='-';if(neg)s=s.slice(1);var dot=s.indexOf('.');var den,parts;if(dot<0){den=1;}else{den=Math.pow(10,s.length-dot-1);parts=s.replace('.','');}var num=parseInt(dot<0?s:s.replace('.',''),10);var g=gcd(num,den);num/=g;den/=g;document.getElementById('df-out').textContent=(neg?'−':'')+num+' / '+den+(den===1?'':'  (≈ '+(neg?-num:num/den)+')');}
function dfFrac(){var s=document.getElementById('df-frac').value.trim();var m=s.match(/^(-?\d+)\s*\/\s*(\d+)$/);if(!m){document.getElementById('df-out').textContent='Enter a fraction like 7/8';return;}var a=parseInt(m[1],10),b=parseInt(m[2],10);if(!b){document.getElementById('df-out').textContent='Divide by zero';return;}var g=gcd(a,b);var out=(a/b);document.getElementById('df-out').textContent=(a/g)+' / '+(b/g)+' = '+(Math.round(out*1e10)/1e10);}
</script>""",
 about="""Decimals and fractions are two ways of writing the same numbers, and switching between them is constant homework in school math and a real need in carpentry, machining, cooking and finance: 0.375 inch is exactly 3/8", and drill charts are written in fractions. Converting a decimal to a fraction means multiplying by a power of ten and reducing by the greatest common divisor - this calculator does it instantly and always shows the fully simplified result, plus converts fractions back to decimals with full precision. Repeat decimals like 0.333... are shown rounded to 10 decimal places. Everything is computed locally in your browser."""),
}

if __name__ == "__main__":
    for slug, d in TOOLS.items():
        html = g.page(slug, d["title"], d["og_title"], d["desc"], d["h1"], d["body"], d["about"])
        io.open(slug, "w", encoding="utf-8").write(html)
        print("wrote", slug, len(html))
