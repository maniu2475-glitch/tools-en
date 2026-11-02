# -*- coding: utf-8 -*-
"""2026-11-02 batch: generate 3 high-volume English tool pages.
Tools: sha512-generator, url-parser (exists? no -> skip), unix-timestamp-now...
Chosen (verified not in repo): sha512-hash-generator, html-minifier, jpg-to-png.
"""
import io, re, os

BASE = "https://maniu2475-glitch.github.io/tools-en/"
TODAY = "2026-11-02"

FAVICON = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAn0lEQVR4nO3asQ2AMBCF"
           "0S9SAdqAsxVwJGACZjAUIAd8a7S0L/1/1r/HPn1vAmAAGIAJRWYAfwFVAdAA0ADQANAA0ADQAKAH+pwAFcBDwADwAHgAPADegAY"
           "AvQAXgBHYA7gAroAPwFegCnAAGIAGIAMYAL4BF9oD3T941acAAAAASUVORK5CYII=")

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
      <a href="index.html#tool-hash">Hash</a>
      <a href="all-tools.html">All Tools</a>
    </nav>
  </div>
</header>"""

FAQ = """<h3>Frequently asked questions</h3>
      <div style="line-height:1.9">
        <details><summary><strong>Is this tool really free?</strong></summary><p>Yes - free, no signup, no login, no usage limit.</p></details>
        <details><summary><strong>Is my data uploaded anywhere?</strong></summary><p>No. All processing happens locally in your browser using JavaScript. Nothing is sent to a server.</p></details>
        <details><summary><strong>Does it work offline?</strong></summary><p>Once the page has loaded you can usually keep using it without a connection.</p></details>
      </div>"""

TEMPLATE = """<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="ToolBox">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#4f6ef7">
<link rel="canonical" href="{canonical}">
<link rel="sitemap" type="application/xml" href="sitemap.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="en_US">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="{FAVICON}">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "WebApplication", "name": "{og_title}", "url": "{canonical}", "description": "{desc}", "applicationCategory": "UtilityApplication", "operatingSystem": "Any", "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}, "browserRequirements": "Requires JavaScript"}}</script>
</head>
<body>
{NAV}
<main class="content" id="content">
  <section class="tool-panel active" id="tool-{tid}">
      <h1>{h1}</h1>
{body}
      <hr>
      <h2>About this tool</h2>
{about}
      <h3>Related tools</h3>
      <div class="btn-group" style="flex-wrap:wrap">
{rel}
      </div>
      {FAQ}
  </section>
</main>
<footer class="site-footer"><div class="container"><p>&copy; 2025 Online Toolbox</p><p class="footer-links"><a href="index.html#home">Online Toolbox</a></p></div></footer>
<script src="app.js"></script>
<script src="extra.js"></script>
<script>{script}</script>
</body>
</html>
"""

TOOLS = []

# ---------------- 1. SHA-512 ----------------
TOOLS.append(dict(
    slug="sha512-hash-generator.html", tid="sha512",
    title="SHA-512 Hash Generator - Free Online SHA2-512 Calculator",
    og_title="SHA-512 Hash Generator",
    desc="Free online SHA-512 hash generator. Compute the 512-bit SHA-2 digest of any text instantly in your browser - no upload, no signup, no tracking.",
    keywords="sha512,sha-512 generator,sha512 hash,hashing tool,sha2-512,checksum generator",
    h1="SHA-512 Hash Generator",
    body="""      <div class="form-row">
        <label for="in">Text to hash</label>
        <textarea id="in" rows="6" placeholder="Type or paste any text here..."></textarea>
      </div>
      <div class="btn-group">
        <button class="btn" onclick="doHash()">Generate SHA-512</button>
        <button class="btn btn-outline" onclick="document.getElementById('in').value='';document.getElementById('out').textContent='';document.getElementById('bits').textContent='';">Clear</button>
        <button class="btn btn-outline" onclick="copyOut()">Copy hash</button>
      </div>
      <div class="form-row">
        <label>SHA-512 digest (hex)</label>
        <pre id="out" class="output" style="word-break:break-all">-</pre>
      </div>
      <p id="bits" class="hint"></p>""",
    about="""      <p style="line-height:1.9">SHA-512 is a cryptographic hash function from the SHA-2 family, defined in FIPS PUB 180-4 and published by NIST in 2001. It takes any amount of input data - a single character or a multi-gigabyte file - and produces a fixed 512-bit (64-byte) digest, normally written as 128 hexadecimal characters. Unlike encryption, hashing is a one-way operation: there is no key and no way to reverse a digest back into the original message.</p>
      <p style="line-height:1.9">This page computes SHA-512 entirely with the Web Crypto API built into your browser (<code>crypto.subtle.digest</code>). Your text never leaves your device and there is no server-side logging, which makes the tool safe for hashing API keys, license strings, tokens or any other sensitive value you only want a fingerprint of. The same input always yields the same digest, so you can compare hashes computed here with hashes produced by <code>sha512sum</code> on Linux, <code>shasum -a 512</code> on macOS or <code>Get-FileHash -Algorithm SHA512</code> in PowerShell - the hex strings will match exactly.</p>
      <p style="line-height:1.9">SHA-512 is used for integrity checks, digital signature schemes, password-derived keys (as part of HMAC and PBKDF2), blockchain address derivation and TLS certificate fingerprints. It is faster than SHA-256 on 64-bit CPUs because its internal word size matches the register width, while still offering a much larger output space. For new password storage you should still use a memory-hard KDF such as Argon2id or bcrypt rather than a bare hash, but for checksums and content addressing SHA-512 remains an excellent choice.</p>
      <p style="line-height:1.9">Input is hashed as UTF-8 text, so accented characters and emoji are converted to their multi-byte form before hashing - this is exactly what most server-side libraries do, meaning your digest will match theirs. If you need the shorter 256-bit variant, use the <a href="sha256-hash-generator.html">SHA-256 generator</a>; for the legacy MD5 algorithm see the <a href="md5-generator.html">MD5 generator</a>.</p>""",
    rel=[("sha256-hash-generator.html","SHA-256 Generator"),("md5-generator.html","MD5 Generator"),
         ("base64.html","Base64 Encode"),("password-generator.html","Password Generator"),
         ("uuid-generator.html","UUID Generator"),("hmac" and "jwt-decoder.html","JWT Decoder"),
         ("base32.html","Base32 Encoder"),("bcrypt" and "password-strength.html","Password Strength")],
    script=r"""
function hex(buf){return Array.from(new Uint8Array(buf)).map(function(b){return b.toString(16).padStart(2,'0')}).join('');}
function doHash(){
  var t=document.getElementById('in').value;
  crypto.subtle.digest('SHA-512', new TextEncoder().encode(t)).then(function(d){
    document.getElementById('out').textContent=hex(d);
    document.getElementById('bits').textContent='Input length: '+t.length+' chars, digest: 512 bits / 128 hex chars / '+t.length+' -> '+hex(d).length;
  }).catch(function(e){document.getElementById('out').textContent='Error: '+e.message;});
}
function copyOut(){
  var s=document.getElementById('out').textContent;
  if(navigator.clipboard){navigator.clipboard.writeText(s);}
}
document.addEventListener('DOMContentLoaded',function(){
  var el=document.getElementById('in');
  if(el){el.addEventListener('input',doHash);}
});
"""))

# ---------------- 2. HTML Minifier ----------------
TOOLS.append(dict(
    slug="html-minifier.html", tid="htmlmin",
    title="HTML Minifier - Compress & Minify HTML Online Free",
    og_title="HTML Minifier",
    desc="Free online HTML minifier: remove comments, collapse whitespace and shrink your HTML source in one click. 100% browser-side, works offline.",
    keywords="html minifier,minify html,compress html,html compressor,html optimizer,reduce html size",
    h1="HTML Minifier / Compressor",
    body="""      <div class="form-row">
        <label for="in">HTML source</label>
        <textarea id="in" rows="10" placeholder="&lt;!DOCTYPE html&gt;&#10;&lt;html&gt; ... paste your HTML here"></textarea>
      </div>
      <div class="btn-group" style="flex-wrap:wrap">
        <label style="display:inline-flex;gap:6px;align-items:center"><input type="checkbox" id="opt-comments" checked> Remove comments</label>
        <label style="display:inline-flex;gap:6px;align-items:center"><input type="checkbox" id="opt-space" checked> Collapse whitespace</label>
        <label style="display:inline-flex;gap:6px;align-items:center"><input type="checkbox" id="opt-quote"> Remove optional quotes</label>
      </div>
      <div class="btn-group">
        <button class="btn" onclick="minify()">Minify HTML</button>
        <button class="btn btn-outline" onclick="copyOut()">Copy result</button>
        <button class="btn btn-outline" onclick="document.getElementById('in').value='';document.getElementById('out').textContent='';document.getElementById('stats').textContent=''">Clear</button>
      </div>
      <div class="form-row">
        <label>Minified output</label>
        <pre id="out" class="output" style="white-space:pre-wrap;word-break:break-all">-</pre>
      </div>
      <p id="stats" class="hint"></p>""",
    about="""      <p style="line-height:1.9">An HTML minifier removes everything a browser does not need: HTML comments, indentation, repeated spaces and newlines between tags. These characters are invisible to visitors but they are still transferred over the network and parsed by the browser, so trimming them reduces page weight and can shave tens of milliseconds off time-to-first-byte on slow mobile connections. A typical hand-written page shrinks by 10% to 35% depending on how heavily it is indented and commented.</p>
      <p style="line-height:1.9">This tool runs entirely in your browser with no upload step, so you can safely minify internal templates, email HTML or customer pages that you cannot paste into a third-party service. It applies three independent passes: comment removal (with <code>&lt;!-- --&gt;</code> blocks and conditional-comment safety), whitespace collapsing between tags while preserving the contents of <code>&lt;pre&gt;</code>, <code>&lt;textarea&gt;</code> and <code>&lt;script&gt;</code>, and an optional pass that drops quotes around single-token attribute values where HTML5 allows it.</p>
      <p style="line-height:1.9">Before deploying, always confirm the minified page renders identically. Whitespace inside inline elements such as a <code>&lt;span&gt;</code> followed by another <code>&lt;span&gt;</code> is significant (it produces a visible space), so aggressive collapsing can occasionally join two words together. If that happens, disable the whitespace checkbox or keep a space inside the first inline element. Minification is lossless for structure but not always lossless for typography.</p>
      <p style="line-height:1.9">For best production results, combine this tool with gzip or Brotli on your web server - minifying first and compressing second always beats compressing the original source. CSS and JavaScript files should be minified separately with the <a href="css-minifier.html">CSS minifier</a> and <a href="js-minifier.html">JS minifier</a>.</p>""",
    rel=[("css-minifier.html","CSS Minifier"),("js-minifier.html","JS Minifier"),
         ("html-entities.html","HTML Entities"),("html-table-generator.html","HTML Table Generator"),
         ("xml-formatter.html","XML Formatter"),("json-formatter.html","JSON Formatter"),
         ("slug-generator.html","Slug Generator"),("text-diff.html","Text Diff")],
    script=r"""
function minify(){
  var s=document.getElementById('in').value;
  var orig=s.length;
  if(document.getElementById('opt-comments').checked){
    s=s.replace(/<!--(?!\[if)[\s\S]*?-->/g,'');
  }
  if(document.getElementById('opt-space').checked){
    var keep=[];
    s=s.replace(/<(pre|textarea|script|style)\b[\s\S]*?<\/\1>/gi,function(m){keep.push(m);return '\u0000'+(keep.length-1)+'\u0000';});
    s=s.replace(/\s+/g,' ').replace(/>\s+</g,'><').replace(/\s+>/g,'>');
    s=s.replace(/\u0000(\d+)\u0000/g,function(m,i){return keep[+i];});
  }
  if(document.getElementById('opt-quote').checked){
    s=s.replace(/="([A-Za-z0-9_\-.:#%]+)"/g,'=$1');
  }
  document.getElementById('out').textContent=s.trim();
  var n=s.trim().length;
  var pct=orig?((1-n/orig)*100):0;
  document.getElementById('stats').textContent='Original '+orig+' bytes -> minified '+n+' bytes (saved '+(orig-n)+' bytes, '+pct.toFixed(1)+'%).';
}
function copyOut(){
  var s=document.getElementById('out').textContent;
  if(navigator.clipboard&&s&&s!=='-'){navigator.clipboard.writeText(s);}
}
"""))

# ---------------- 3. PNG to JPG ----------------
TOOLS.append(dict(
    slug="png-to-jpg.html", tid="pngtojpg",
    title="PNG to JPG Converter Online Free - No Upload, Instant",
    og_title="PNG to JPG Converter",
    desc="Convert PNG images to JPG in your browser with adjustable quality. Files never leave your device - private, free and unlimited.",
    keywords="png to jpg,png to jpeg,convert png to jpg online,image converter,free png converter,compress png",
    h1="PNG to JPG Converter",
    body="""      <div class="form-row">
        <label for="file">Choose a PNG image</label>
        <input type="file" id="file" accept="image/png,image/*">
      </div>
      <div class="form-row">
        <label for="q">JPEG quality: <span id="qv">92</span>%</label>
        <input type="range" id="q" min="30" max="100" value="92" oninput="document.getElementById('qv').textContent=this.value;convert()">
      </div>
      <div class="form-row">
        <label>Background for transparency (JPG has no alpha channel)</label>
        <input type="color" id="bg" value="#ffffff" oninput="convert()">
      </div>
      <div class="btn-group">
        <a id="dl" class="btn" download="converted.jpg" href="#" style="display:none">Download JPG</a>
      </div>
      <p id="info" class="hint"></p>
      <div class="form-row"><canvas id="cv" style="max-width:100%;border:1px solid #e2e6f0;border-radius:8px"></canvas></div>""",
    about="""      <p style="line-height:1.9">PNG is a lossless format that is ideal for screenshots, icons and graphics with sharp edges, but photographic images stored as PNG can easily be ten times larger than the equivalent JPEG. Converting to JPG lets you control the quality/size trade-off: at 90-95% quality most photos are visually indistinguishable from the source while occupying a fraction of the disk space, which is exactly what you need before uploading to a CMS, sending by email or embedding in a slide deck.</p>
      <p style="line-height:1.9">Because JPEG has no alpha channel, every transparent pixel must be flattened onto a solid colour. This converter draws your PNG onto a canvas filled with the colour you pick (white by default) before encoding, so logos with transparency come out clean instead of showing black background artifacts. Pick a colour that matches the destination page background for the best result.</p>
      <p style="line-height:1.9">Everything happens locally through the Canvas API and <code>canvas.toBlob('image/jpeg', quality)</code> - your images are never uploaded to any server, which matters if you are converting ID scans, medical images, unreleased product shots or client work under NDA. There are no file-size limits other than your device's memory, and no daily quota.</p>
      <p style="line-height:1.9">Tips for the smallest acceptable file: lower quality to around 80% for web thumbnails, resize large photos before converting (a 4000px photo displayed at 800px wastes bandwidth), and remember that repeated re-encoding degrades quality, so always convert from the original PNG rather than from an already compressed JPG. Need the opposite direction? Try the <a href="image-to-base64.html">image to Base64</a> encoder.</p>""",
    rel=[("image-to-base64.html","Image to Base64"),("qr-code-generator.html","QR Code Generator"),
         ("barcode-generator.html","Barcode Generator"),("color-picker.html","Color Picker"),
         ("hex-to-rgb.html","HEX to RGB"),("favicon" and "base64.html","Base64 Encode"),
         ("screen-resolution-checker.html","Screen Resolution Checker"),("text-diff.html","Text Diff")],
    script=r"""
var img=null, lastName='converted.jpg';
document.getElementById('file').addEventListener('change',function(e){
  var f=e.target.files[0]; if(!f) return;
  lastName=(f.name||'image').replace(/\.[^.]+$/,'')+'.jpg';
  var r=new FileReader();
  r.onload=function(){ var im=new Image(); im.onload=function(){ img=im; convert(); }; im.src=r.result; };
  r.readAsDataURL(f);
});
function convert(){
  if(!img) return;
  var cv=document.getElementById('cv');
  var max=2600, w=img.naturalWidth, h=img.naturalHeight;
  if(w>max){ h=Math.round(h*max/w); w=max; }
  cv.width=w; cv.height=h;
  var ctx=cv.getContext('2d');
  ctx.fillStyle=document.getElementById('bg').value;
  ctx.fillRect(0,0,w,h);
  ctx.drawImage(img,0,0,w,h);
  var q=parseInt(document.getElementById('q').value,10)/100;
  cv.toBlob(function(b){
    if(!b){document.getElementById('info').textContent='Conversion failed.';return;}
    var url=URL.createObjectURL(b);
    var a=document.getElementById('dl');
    a.href=url; a.download=lastName; a.style.display='inline-block';
    a.textContent='Download JPG ('+Math.round(b.size/1024)+' KB)';
    document.getElementById('info').textContent='Output size: '+Math.round(b.size/1024)+' KB at '+w+'x'+h+' px, quality '+Math.round(q*100)+'%.';
  },'image/jpeg',q);
}
"""))


def build(t):
    t = dict(t)
    t['FAVICON'] = FAVICON
    t['NAV'] = NAV
    t['FAQ'] = FAQ
    t['canonical'] = BASE + t['slug']
    rel = "\n".join('<a class="btn btn-outline" href="%s">%s</a>' % r for r in t['rel'])
    t['rel'] = rel
    return TEMPLATE.format(**t)


if __name__ == "__main__":
    for t in TOOLS:
        p = t['slug']
        if os.path.exists(p):
            print("SKIP exists", p)
            continue
        io.open(p, "w", encoding="utf-8").write(build(t))
        print("wrote", p)
