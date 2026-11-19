# -*- coding: utf-8 -*-
"""Generate 3 new standalone English tool pages (2026-11-16 batch)."""
import io, sys

BASE = "https://maniu2475-glitch.github.io/tools-en/"
TODAY = "2026-11-16"

NAV = """<header class="site-header">
  <div class="container header-inner">
    <button class="menu-toggle" id="menuToggle" aria-label="menu">&#9776;</button>
    <a class="logo" href="index.html#home"><span class="logo-icon">&#129520;</span><span class="logo-text">Online Toolbox</span></a>
    <nav class="main-nav" id="mainNav">
      <a href="index.html#tool-json">JSON</a>
      <a href="index.html#tool-base64">Base64</a>
      <a href="index.html#tool-url">URL</a>
      <a href="index.html#tool-qrcode">QR Code</a>
      <a href="index.html#tool-password">Password</a>
      <a href="index.html#tool-timestamp">Timestamp</a>
      <a href="index.html#tool-color">Color</a>
      <a href="all-tools.html">All Tools</a>
    </nav>
  </div>
</header>"""

FOOT = """<footer class="site-footer">
  <div class="container">
    <p>&copy; 2026 Online Toolbox &middot; All tools run locally in your browser.</p>
    <p><a href="index.html">Home</a> &middot; <a href="all-tools.html">All Tools</a> &middot; <a href="privacy.html">Privacy</a></p>
  </div>
</footer>
<script src="app.js"></script>
</body>
</html>"""

TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{base}{slug}.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{base}{slug}.html">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
</head>
<body>
{nav}
<main class="container" id="home">
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
  <section class="tool-card">
{tool}
  </section>
  <section class="explain">
{explain}
  </section>
  <section class="related">
    <h2>Related tools</h2>
    <ul>
{related}
    </ul>
  </section>
{script}
</main>
{foot}"""

REL_POOL = [
    ("json-formatter.html", "JSON Formatter"), ("base64.html", "Base64 Encoder &amp; Decoder"),
    ("url-encode-decode.html", "URL Encoder &amp; Decoder"), ("qr-code-generator.html", "QR Code Generator"),
    ("password-generator.html", "Password Generator"), ("timestamp-converter.html", "Timestamp Converter"),
    ("md5-generator.html", "MD5 Hash Generator"), ("sha256-hash-generator.html", "SHA-256 Hash Generator"),
    ("jwt-decoder.html", "JWT Decoder"), ("regex-tester.html", "Regex Tester"),
    ("cron-generator.html", "Cron Expression Generator"), ("base32.html", "Base32 Encoder &amp; Decoder"),
    ("text-diff.html", "Text Diff Checker"), ("word-counter.html", "Word Counter"),
]

pages = {}

pages["user-agent-parser"] = dict(
    title="User Agent Parser - Decode Browser &amp; OS from UA String (Free)",
    desc="Free online user agent parser. Paste any User-Agent string to instantly see browser, version, operating system, device type and engine. Runs locally in your browser.",
    h1="User Agent Parser",
    lead="Paste a User-Agent string to decode the browser, version, operating system, rendering engine and device type behind it.",
    tool="""    <textarea id="uaInput" rows="4" spellcheck="false" placeholder="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"></textarea>
    <div class="btn-row">
      <button class="btn" id="uaParse">Parse</button>
      <button class="btn btn-ghost" id="uaMine">Use my current UA</button>
      <button class="btn btn-ghost" id="uaCopy">Copy JSON</button>
    </div>
    <table class="result-table" id="uaOut"><tbody><tr><td>Enter a User-Agent string and click Parse.</td></tr></tbody></table>
    <pre id="uaJson" class="output" hidden></pre>""",
    explain="""    <h2>What is a User-Agent string?</h2>
    <p>Every time a browser, app or bot requests a web page it sends a <strong>User-Agent</strong> (UA) header. That short line of text tells the server which browser is calling, which version it runs, which operating system and device it is on, and which rendering engine produced the page. The UA evolved in the mid-1990s alongside the first Netscape releases, when sites needed a cheap way to serve different markup to different browsers. Almost thirty years later the same header is still there, carrying a small amount of historical luggage: most strings begin with <code>Mozilla/5.0</code> even in Chrome, Edge or Safari, purely for backward compatibility with 1990s sniffing code.</p>
    <p>This parser breaks the string into its meaningful parts. It looks for the browser token and version (Chrome, Firefox, Safari, Edge, Opera, Samsung Internet, and the Chromium-based family), then detects the operating system from markers such as <code>Windows NT 10.0</code>, <code>Mac OS X 14_5</code>, <code>Android 14</code> or <code>iPhone OS 17_2</code>. It also recognises the two mainstream engines &mdash; Blink/WebKit, reported by the <code>AppleWebKit/537.36</code> token, and Gecko, reported by <code>Gecko/20100101</code> &mdash; and finally guesses whether the device is a desktop, tablet, phone, or an automated crawler.</p>
    <h2>Why you would decode a UA string</h2>
    <ul>
      <li><strong>Debugging reports.</strong> A user says "the layout breaks on my machine" &mdash; ask for the UA from <code>navigator.userAgent</code> and you immediately know their exact browser and OS build.</li>
      <li><strong>Reading access logs.</strong> Server logs store the raw string; this tool turns those cryptic tokens into a readable summary you can paste into a bug tracker.</li>
      <li><strong>Bot filtering.</strong> Crawlers, scrapers and SEO tools identify themselves in the UA. Spotting <code>Googlebot</code>, <code>bingbot</code> or <code>curl</code> tells you whether a hit is real traffic.</li>
      <li><strong>QA test matrices.</strong> Collect the UAs of the devices you actually care about, then use them to configure emulation in DevTools or Playwright.</li>
    </ul>
    <h2>Accuracy caveats you should know</h2>
    <p>A UA string is self-declared and freely spoofable, so treat the output as a strong hint rather than ground truth. Browsers have also deliberately frozen parts of the header: Chrome reduced the platform detail it exposes (User-Agent Reduction) and recommends feature detection with <code>navigator.userAgentData</code> instead. iOS Safari inside a third-party app often reports a WebView UA that omits the host app name. And some strings are genuinely ambiguous &mdash; Edge on macOS and Chrome on macOS differ only by a couple of tokens, so a heuristic parser occasionally guesses wrong. If you need certainty, prefer capability detection in the code you write and use the UA only for analytics and support triage.</p>
    <h2>Privacy</h2>
    <p>Everything here runs in JavaScript on your own machine. The string you paste is never uploaded to a server, which matters when the UA comes from a customer ticket or an internal log file. Close the tab and the data is gone. If you also need to decode tokens, try the <a href="jwt-decoder.html">JWT decoder</a>; for encoding strings into a URL safe form see the <a href="url-encode-decode.html">URL encoder</a>.</p>""",
    js="""(function(){
  function detect(ua){
    var r = {raw: ua, browser:'Unknown', version:'', os:'Unknown', engine:'Unknown', device:'Desktop'};
    if(!ua) return r;
    var m;
    if(/Googlebot/i.test(ua)) {r.browser='Googlebot'; r.device='Bot';}
    else if(/bingbot/i.test(ua)) {r.browser='Bingbot'; r.device='Bot';}
    else if(/curl\\//i.test(ua)) {r.browser='curl'; r.device='Bot';}
    else if((m=ua.match(/Edg\\/([\\d.]+)/))) {r.browser='Edge'; r.version=m[1];}
    else if((m=ua.match(/OPR\\/([\\d.]+)/))) {r.browser='Opera'; r.version=m[1];}
    else if((m=ua.match(/SamsungBrowser\\/([\\d.]+)/))) {r.browser='Samsung Internet'; r.version=m[1];}
    else if((m=ua.match(/Firefox\\/([\\d.]+)/))) {r.browser='Firefox'; r.version=m[1];}
    else if((m=ua.match(/Chrome\\/([\\d.]+)/))) {r.browser='Chrome'; r.version=m[1];}
    else if((m=ua.match(/Version\\/([\\d.]+).*Safari/))) {r.browser='Safari'; r.version=m[1];}
    if(/Windows NT 10/i.test(ua)) r.os='Windows 10/11';
    else if(/Windows NT 6\\.3/i.test(ua)) r.os='Windows 8.1';
    else if(/Windows NT 6\\.1/i.test(ua)) r.os='Windows 7';
    else if(/Windows/i.test(ua)) r.os='Windows';
    else if((m=ua.match(/Android ([\\d.]+)/i))) r.os='Android ' + m[1];
    else if((m=ua.match(/(?:iPhone|iPad|iPod).*?OS ([\\d_]+)/i))) r.os='iOS ' + m[1].replace(/_/g,'.');
    else if((m=ua.match(/Mac OS X ([\\d_]+)/i))) r.os='macOS ' + m[1].replace(/_/g,'.');
    else if(/CrOS/i.test(ua)) r.os='ChromeOS';
    else if(/Ubuntu/i.test(ua)) r.os='Ubuntu';
    else if(/Linux/i.test(ua)) r.os='Linux';
    else if(/FreeBSD/i.test(ua)) r.os='FreeBSD';
    if(/Gecko\\/20/.test(ua) && /Firefox/.test(ua)) r.engine='Gecko';
    else if(/AppleWebKit\\//.test(ua)) r.engine='Blink/WebKit';
    if(/iPad|Tablet/i.test(ua)) r.device='Tablet';
    else if(/Mobi|iPhone|Android.*Mobile/i.test(ua)) r.device='Phone';
    return r;
  }
  var input=document.getElementById('uaInput');
  var out=document.getElementById('uaOut');
  var json=document.getElementById('uaJson');
  var last=null;
  function run(u){
    last=detect(u);
    var rows=[['Browser',last.browser],['Version',last.version||'-'],['Operating system',last.os],['Rendering engine',last.engine],['Device type',last.device]];
    out.innerHTML='<tbody>'+rows.map(function(x){return '<tr><th>'+x[0]+'</th><td>'+String(x[1]).replace(/</g,'&lt;')+'</td></tr>';}).join('')+'</tbody>';
    json.hidden=false; json.textContent=JSON.stringify(last,null,2);
  }
  document.getElementById('uaParse').onclick=function(){run(input.value.trim());};
  document.getElementById('uaMine').onclick=function(){input.value=navigator.userAgent;run(input.value);};
  document.getElementById('uaCopy').onclick=function(){if(!last)return;if(navigator.clipboard)navigator.clipboard.writeText(JSON.stringify(last,null,2));};
  input.addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();run(input.value.trim());}});
})();""",
    rel=["jwt-decoder.html", "url-encode-decode.html", "json-formatter.html", "regex-tester.html"],
)

pages["curl-to-code"] = dict(
    title="cURL to JavaScript fetch Converter - Online &amp; Free",
    desc="Convert cURL commands into JavaScript fetch or async/await code instantly. Paste a curl line from DevTools and get runnable JS in your browser. No data leaves your machine.",
    h1="cURL to JavaScript Converter",
    lead="Paste a cURL command copied from your browser DevTools or API docs and get ready-to-run JavaScript fetch code.",
    tool="""    <textarea id="curlIn" rows="7" spellcheck="false" placeholder="curl 'https://api.example.com/v1/items' -H 'Authorization: Bearer TOKEN' -H 'Content-Type: application/json' --data-raw '{"q":"hello"}'"></textarea>
    <div class="btn-row">
      <label class="lbl">Output style
        <select id="curlStyle">
          <option value="await">async / await</option>
          <option value="then">.then() chain</option>
          <option value="node">Node.js fetch</option>
        </select>
      </label>
      <button class="btn" id="curlGo">Convert</button>
      <button class="btn btn-ghost" id="curlCopy">Copy code</button>
    </div>
    <pre id="curlOut" class="output" style="min-height:120px">Your JavaScript will appear here.</pre>
    <div id="curlErr" class="err"></div>""",
    explain="""    <h2>Why convert cURL to fetch?</h2>
    <p>cURL is the universal language for describing an HTTP request, and almost every API documentation page ships a copy-paste <code>curl</code> example. That is convenient for the terminal, but the moment you want to reproduce the same call in a browser front-end or a Node script you have to translate flags into a JavaScript object by hand: <code>-H</code> becomes a <code>headers</code> map, <code>-X POST</code> becomes <code>method</code>, and <code>--data-raw</code> becomes <code>body</code> with the right content type. Doing that manually for a long request with cookies, auth headers and JSON payloads is slow and easy to get wrong &mdash; a single quoting slip produces a runtime error that can take minutes to trace.</p>
    <p>This converter reads the command the same way a shell would: it tokenises respecting single quotes, double quotes and backslash escapes, then maps the well-known flags. <code>-H</code> or <code>--header</code> collects headers, <code>-X</code> or <code>--request</code> sets the method, <code>-d</code>, <code>--data</code>, <code>--data-raw</code>, <code>--data-binary</code> and <code>--json</code> build the body, <code>-u</code> becomes a Basic auth header, and <code>-b</code> or <code>--cookie</code> becomes a <code>Cookie</code> header. If the data looks like JSON, the output is embedded as a JSON string literal so the generated code is immediately valid.</p>
    <h2>Reading the generated code</h2>
    <p>Three styles are offered. The <strong>async / await</strong> form is the one most people want in modern code: it produces an immediately-invoked async function with a <code>try/catch</code> so you can run it straight from the console. The <strong>.then() chain</strong> style suits older codebases or scripts that keep everything flat. The <strong>Node.js</strong> style adds an explicit <code>response.ok</code> check and prints the status, which is handy when debugging a backend integration.</p>
    <p>Two habits worth keeping: first, treat every generated snippet as a starting point and move secrets into environment variables rather than leaving a bearer token in a committed file. Second, remember that browsers enforce CORS, so a request that works in your terminal may still be blocked in a page &mdash; that is a server policy issue, not a bug in the code. If you are reversing the other direction, compare payloads with the <a href="json-formatter.html">JSON formatter</a>, and decode tokens with the <a href="jwt-decoder.html">JWT decoder</a>.</p>""",
    js="""(function(){
  function tokenize(s){
    var out=[], cur='', q=null, i=0;
    while(i<s.length){
      var c=s[i];
      if(q){
        if(c==='\\\\' && q==='"' && i+1<s.length){ cur+=s[i+1]; i+=2; continue; }
        if(c===q){ q=null; i++; continue; }
        cur+=c; i++; continue;
      }
      if(c==='"'||c==="'"){ q=c; i++; continue; }
      if(/\\s/.test(c)){ if(cur){out.push(cur);cur='';} i++; continue; }
      if(c==='\\\\' && i+1<s.length){ cur+=s[i+1]; i+=2; continue; }
      cur+=c; i++;
    }
    if(cur) out.push(cur);
    return out;
  }
  function parse(cmd){
    var t=tokenize(cmd.trim());
    if(t[0]==='curl') t.shift();
    var r={url:'', method:'', headers:{}, body:null};
    var noVal={'-L':1,'--location':1,'-s':1,'--silent':1,'-k':1,'--insecure':1,'-v':1,'--verbose':1,'-i':1,'-g':1,'--compressed':1};
    for(var i=0;i<t.length;i++){
      var a=t[i], v=t[i+1];
      if(a==='-H'||a==='--header'){ var p=v||''; var k=p.indexOf(':'); if(k>0) r.headers[p.slice(0,k).trim()]=p.slice(k+1).trim(); i++; }
      else if(a==='-X'||a==='--request'){ r.method=(v||'').toUpperCase(); i++; }
      else if(a==='-d'||a==='--data'||a==='--data-raw'||a==='--data-binary'||a==='--data-ascii'){ r.body=v||''; if(!r.method) r.method='POST'; i++; }
      else if(a==='--json'){ r.body=v||''; if(!r.headers['Content-Type']) r.headers['Content-Type']='application/json'; if(!r.method) r.method='POST'; i++; }
      else if(a==='-u'||a==='--user'){ try{ r.headers['Authorization']='Basic '+btoa(v||''); }catch(e){} i++; }
      else if(a==='-b'||a==='--cookie'){ r.headers['Cookie']=v||''; i++; }
      else if(a==='-A'||a==='--user-agent'){ r.headers['User-Agent']=v||''; i++; }
      else if(a==='-e'||a==='--referer'){ r.headers['Referer']=v||''; i++; }
      else if(noVal[a]){ continue; }
      else if(a.charAt(0)!=='-' && !r.url){ r.url=a; }
    }
    return r;
  }
  function jsq(s){ return JSON.stringify(String(s)); }
  function build(r, style){
    if(!r.url) throw new Error('No URL found in the command.');
    var hs=Object.keys(r.headers);
    var hdr = hs.length ? '{\\n' + hs.map(function(k){ return "      " + JSON.stringify(k) + ': ' + jsq(r.headers[k]); }).join(',\\n') + '\\n    }' : null;
    var opts = [];
    if(r.method && r.method!=='GET') opts.push('method: ' + jsq(r.method));
    if(hdr) opts.push('headers: ' + hdr);
    if(r.body!==null) opts.push('body: ' + jsq(r.body));
    var optStr = opts.length ? '{\\n    ' + opts.join(',\\n    ') + '\\n  }' : '{}';
    var url = jsq(r.url);
    if(style==='then'){
      return 'fetch(' + url + ', ' + optStr + ')\\n  .then(function (res) {\\n    if (!res.ok) throw new Error("HTTP " + res.status);\\n    return res.json();\\n  })\\n  .then(function (data) {\\n    console.log(data);\\n  })\\n  .catch(function (err) {\\n    console.error(err);\\n  });';
    }
    var body = style==='node'
      ? 'const res = await fetch(' + url + ', ' + optStr + ');\\n    console.log(res.status);\\n    const data = await res.json();\\n    console.log(data);'
      : 'const res = await fetch(' + url + ', ' + optStr + ');\\n    if (!res.ok) throw new Error("HTTP " + res.status);\\n    const data = await res.json();\\n    console.log(data);';
    return '(async () => {\\n  try {\\n    ' + body + '\\n  } catch (err) {\\n    console.error(err);\\n  }\\n})();';
  }
  var out=document.getElementById('curlOut'), err=document.getElementById('curlErr');
  function go(){
    err.textContent='';
    try{
      var r=parse(document.getElementById('curlIn').value);
      out.textContent=build(r, document.getElementById('curlStyle').value);
    }catch(e){ out.textContent=''; err.textContent=e.message; }
  }
  document.getElementById('curlGo').onclick=go;
  document.getElementById('curlCopy').onclick=function(){ if(navigator.clipboard) navigator.clipboard.writeText(out.textContent); };
})();""",
    rel=["json-formatter.html", "url-encode-decode.html", "jwt-decoder.html", "regex-tester.html"],
)

pages["ascii-table"] = dict(
    title="ASCII Table - Character Codes, Hex, Binary &amp; Decimal Chart",
    desc="Searchable ASCII and extended Latin-1 character table with decimal, hex, binary, octal and HTML entity values. Copy any code instantly. Free, offline, in-browser.",
    h1="ASCII Table &amp; Character Code Lookup",
    lead="Search any ASCII or Latin-1 character and read its decimal, hexadecimal, octal, binary and HTML entity values side by side.",
    tool="""    <input type="text" id="asciiSearch" placeholder="Type a character, a name, or a code (e.g. 65, A, space)" />
    <div class="btn-row">
      <label class="lbl"><input type="checkbox" id="asciiExt" checked> Include extended (128-255)</label>
      <label class="lbl"><input type="checkbox" id="asciiCtrl"> Show control characters</label>
    </div>
    <div style="max-height:420px;overflow:auto">
      <table class="result-table" id="asciiTable">
        <thead><tr><th>Dec</th><th>Hex</th><th>Oct</th><th>Binary</th><th>Char</th><th>HTML</th><th>Name</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>
    <p class="hint" id="asciiCount"></p>""",
    explain="""    <h2>The ASCII table in one paragraph</h2>
    <p>ASCII &mdash; the American Standard Code for Information Interchange &mdash; was published in 1963 as a seven-bit character encoding and it remains the substrate under nearly every text format used today. Codes 0 to 31 plus 127 are non-printing control characters inherited from teletype machines: <code>0x0A</code> is line feed, <code>0x0D</code> is carriage return, <code>0x09</code> is tab, and the notorious <code>0x07</code> rings an actual bell on old terminals. Codes 32 to 126 are the printable set that starts with space, runs through digits and punctuation, and ends with the tilde at 126. The ordering is not arbitrary: uppercase letters occupy 65 to 90 and lowercase occupy 97 to 122, a gap of exactly 32, so flipping bit 5 of a letter toggles its case &mdash; a trick still used in fast text algorithms.</p>
    <h2>Why hexadecimal and binary matter</h2>
    <p>Developers meet ASCII in three different costumes. Protocols and file formats usually speak hex, so a space shows up as <code>0x20</code> and a newline as <code>0x0A</code>; that is what you will see in a packet capture or a hex editor. Decimal codes appear in HTML numeric entities such as <code>&amp;#65;</code> and in programming-language escapes. Binary is where bit-level codecs like Base64 and compression live &mdash; Base64 exists precisely because it maps every six bits onto an ASCII-safe subset of 64 printable characters. Being able to move between the three representations without guessing is the fastest way to debug mojibake, mismatched line endings and stray non-breaking spaces.</p>
    <h2>Extended characters and the road to Unicode</h2>
    <p>ASCII stops at 127. Codes 128 to 255 belong to the extended ranges: ISO-8859-1 (Latin-1) assigns Western European accented letters, while the CP437 and Windows-1252 variants reuse the same slots for box-drawing symbols and smart quotes. This ambiguity is exactly why "smart quotes" from a word processor break JSON: they are byte 0x92 in Windows-1252, not an ASCII apostrophe. Modern text is Unicode, and UTF-8 deliberately keeps the first 128 code points identical to ASCII, which is why a plain English file is byte-for-byte valid UTF-8. When you need to move between these representations, pair this table with the <a href="hex-to-ascii.html">hex to ASCII converter</a>, the <a href="base64.html">Base64 encoder</a> and the <a href="binary-to-text.html">binary to text tool</a>.</p>
    <h2>Handy landmarks to memorise</h2>
    <ul>
      <li><code>48&ndash;57</code> digits 0&ndash;9 &mdash; subtract 48 to get the integer value</li>
      <li><code>65&ndash;90</code> uppercase, <code>97&ndash;122</code> lowercase &mdash; difference 32</li>
      <li><code>32</code> space, <code>9</code> tab, <code>10</code> LF, <code>13</code> CR</li>
      <li><code>64</code> at sign, <code>91</code> left bracket, <code>96</code> backtick, <code>123</code> curly brace</li>
    </ul>""",
    js="""(function(){
  var names={};
  var known={32:'Space',33:'Exclamation mark',34:'Quotation mark',35:'Number sign',36:'Dollar sign',37:'Percent sign',38:'Ampersand',39:'Apostrophe',40:'Left parenthesis',41:'Right parenthesis',42:'Asterisk',43:'Plus sign',44:'Comma',45:'Hyphen-minus',46:'Full stop',47:'Slash',58:'Colon',59:'Semicolon',60:'Less-than sign',61:'Equals sign',62:'Greater-than sign',63:'Question mark',64:'At sign',91:'Left square bracket',92:'Backslash',93:'Right square bracket',94:'Caret',95:'Underscore',96:'Grave accent',123:'Left curly bracket',124:'Vertical bar',125:'Right curly bracket',126:'Tilde',127:'Delete'};
  for(var k in known) names[parseInt(k,10)]=known[k];
  for(var d=48;d<=57;d++) names[d]='Digit '+(d-48);
  for(var u=65;u<=90;u++) names[u]='Uppercase ' + String.fromCharCode(u);
  for(var l=97;l<=122;l++) names[l]='Lowercase ' + String.fromCharCode(l);
  var cf={0:'NUL',7:'BEL',8:'BS',9:'HT (tab)',10:'LF (newline)',11:'VT',12:'FF',13:'CR (carriage return)',27:'ESC',127:'DEL'};
  function pad(n,w){ var s=n.toString(2); while(s.length<w) s='0'+s; return s; }
  function esc(c){ if(c==='<') return '&lt;'; if(c==='>') return '&gt;'; if(c==='&') return '&amp;'; return c; }
  function render(){
    var q=(document.getElementById('asciiSearch').value||'').toLowerCase().trim();
    var ext=document.getElementById('asciiExt').checked;
    var showCtrl=document.getElementById('asciiCtrl').checked;
    var max=ext?256:128, rows=[], n=0;
    for(var i=0;i<max;i++){
      var isCtrl = i<32 || i===127;
      if(isCtrl && !showCtrl) continue;
      var ch=String.fromCharCode(i);
      var nm=names[i]||cf[i]||('Extended char '+i);
      var dec=String(i), hex='U+'+('000'+i.toString(16).toUpperCase()).slice(-4);
      var bin=pad(i,8), oct=i.toString(8);
      if(q){
        var hay=(dec+' '+i.toString(16)+' '+bin+' '+oct+' '+nm+' '+ch).toLowerCase();
        if(hay.indexOf(q)===-1) continue;
      }
      rows.push('<tr><td>'+dec+'</td><td>'+hex+'</td><td>'+oct+'</td><td><code>'+bin+'</code></td><td><code>'+(isCtrl?'&middot;':esc(ch))+'</code></td><td><code>&amp;#'+i+';</code></td><td>'+nm+'</td></tr>');
      n++;
      if(n>600) break;
    }
    document.querySelector('#asciiTable tbody').innerHTML=rows.join('')||'<tr><td colspan="7">No match.</td></tr>';
    document.getElementById('asciiCount').textContent=rows.length+' characters shown.';
  }
  document.getElementById('asciiSearch').addEventListener('input',render);
  document.getElementById('asciiExt').addEventListener('change',render);
  document.getElementById('asciiCtrl').addEventListener('change',render);
  render();
})();""",
    rel=["base64.html", "hex-to-ascii.html", "binary-to-text.html", "html-entities.html"],
)


def build(slug, cfg):
    rel_html = []
    pool = {s: n for s, n in REL_POOL}
    for s in cfg["rel"]:
        label = pool.get(s, s.replace('.html', '').replace('-', ' ').title())
        rel_html.append('      <li><a href="%s">%s</a></li>' % (s, label))
    script = "<script>\n" + cfg["js"] + "\n</script>"
    return TPL.format(title=cfg["title"], desc=cfg["desc"], base=BASE, slug=slug,
                      h1=cfg["h1"], lead=cfg["lead"], nav=NAV, foot=FOOT,
                      tool=cfg["tool"], explain=cfg["explain"],
                      related="\n".join(rel_html), script=script)


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    for slug, cfg in pages.items():
        path = outdir + "/" + slug + ".html"
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(build(slug, cfg))
        print("wrote", path)
