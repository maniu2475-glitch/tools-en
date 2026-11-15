# -*- coding: utf-8 -*-
"""Generate 3 new English tool pages (2026-11-15): image-resizer, exif-viewer, json-escape."""
import os

BASE = "https://maniu2475-glitch.github.io/tools-en/"
FAVICON = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAn0lEQVR4nO3asQ2AMBCF"
           "0S9SAdqAsxVwJGACZjAUIAd8a7S0L/1/1r/HPn1vAmAAGIAJRWYAfwFVAdAA0ADQANAA0ADQAKAH+pwAFcBDwADwAHgAPADegAY"
           "AvQAXgBHYA7gAroAPwFegCnAAGIAGIAMYAL4BF9oD3T941acAAAAASUVORK5CYII=")

NAV = """<header class="site-header">
  <div class="container header-inner">
    <button class="menu-toggle" id="menuToggle" aria-label="menu">&#9776;</button>
    <a class="logo" href="index.html#home"><span class="logo-icon">&#129520;</span><span class="logo-text">Online Toolbox</span></a>
    <nav class="main-nav" id="mainNav">
      <a href="index.html#tool-json">JSON</a><a href="index.html#tool-base64">Base64</a>
      <a href="index.html#tool-url">URL</a><a href="index.html#tool-qrcode">QR Code</a>
      <a href="index.html#tool-hash">Hash</a><a href="all-tools.html">All Tools</a>
    </nav>
  </div>
</header>"""

FOOTER = """<footer class="site-footer"><div class="container">
<p>&copy; 2026 Online Toolbox &middot; <a href="index.html">Home</a> &middot; <a href="all-tools.html">All Tools</a> &middot; <a href="sitemap.xml">Sitemap</a></p>
<p>All tools run 100% in your browser. No uploads, no signup, no tracking of your content.</p>
</div></footer>"""

RELATED_ALL = [("image-compressor.html", "Image Compressor"), ("png-to-jpg.html", "PNG to JPG"),
               ("json-formatter.html", "JSON Formatter"), ("base64.html", "Base64 Encoder"),
               ("html-entities.html", "HTML Entities"), ("url-encode-decode.html", "URL Encoder"),
               ("word-counter.html", "Word Counter"), ("text-diff.html", "Text Diff")]

TPL = u"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#4f6ef7">
<link rel="canonical" href="{canon}">
<link rel="sitemap" type="application/xml" href="sitemap.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="en_US">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="{favicon}">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"{h1}","url":"{canon}","applicationCategory":"UtilitiesApplication","operatingSystem":"Any","offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
</head>
<body>
{nav}
<main class="container" style="max-width:960px;margin:0 auto;padding:24px 16px">
<h1>{h1}</h1>
<p>{intro}</p>
<div class="tool-card" style="background:#fff;border:1px solid #e6e9f0;border-radius:12px;padding:20px;margin:20px 0">
{body}
</div>
<h2>About this tool</h2>
{about}
<h3>Frequently asked questions</h3>
<div style="line-height:1.9">{faq}</div>
{rel}
</main>
{footer}
<script>
document.addEventListener('DOMContentLoaded',function(){{var m=document.getElementById('menuToggle');if(m){{m.addEventListener('click',function(){{var n=document.getElementById('mainNav');if(n)n.classList.toggle('open');}});}}}});
{js}
</script>
</body>
</html>
"""

def build(slug, title, desc, keywords, h1, intro, body, js, about, faq, extra_rel):
    items = extra_rel + [r for r in RELATED_ALL if r[0] not in [e[0] for e in extra_rel]]
    li = "".join('<li><a href="%s">%s</a></li>' % (s, t) for s, t in items[:10])
    rel = '<h3>Related tools</h3><ul class="related-list" style="columns:2;line-height:1.9">%s</ul>' % li
    html = TPL.format(title=title, desc=desc, keywords=keywords, canon=BASE + slug, favicon=FAVICON,
                      h1=h1, intro=intro, body=body, about=about, faq=faq, rel=rel,
                      nav=NAV, footer=FOOTER, js=js)
    with open(slug, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", slug, len(html), "bytes")

# ============ 1. Image Resizer ============
build(
 "image-resizer.html",
 "Image Resizer Online - Resize Images Free in Your Browser",
 "Free online image resizer: resize JPG, PNG, WebP and GIF images to any width or height, keep aspect ratio and download instantly. 100% browser-side, no upload.",
 "image resizer,resize image online,resize jpg,resize png,image dimensions,scale image,browser image resize",
 "Image Resizer - Resize Images Online for Free",
 "Resize any image to an exact pixel size without uploading it to a server. This resizer runs entirely inside your browser using the HTML5 canvas API, so your pictures never leave your computer.",
 """<h2 style="margin-top:0">Resize an image</h2>
<input type="file" id="imgFile" accept="image/*" style="margin:8px 0">
<div style="display:flex;gap:16px;flex-wrap:wrap;margin:12px 0;align-items:flex-end">
  <label>Width (px)<br><input type="number" id="rw" min="1" style="width:110px"></label>
  <label>Height (px)<br><input type="number" id="rh" min="1" style="width:110px"></label>
  <label><input type="checkbox" id="keepRatio" checked> Keep aspect ratio</label>
  <label>Format<br><select id="fmt"><option value="image/png">PNG</option><option value="image/jpeg">JPEG</option><option value="image/webp">WebP</option></select></label>
</div>
<div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end">
  <label>Quality <span id="qval">0.92</span><br><input type="range" id="quality" min="0.1" max="1" step="0.01" value="0.92" style="width:160px"></label>
  <button id="btnResize" style="padding:8px 18px;background:#4f6ef7;color:#fff;border:none;border-radius:8px;cursor:pointer">Resize</button>
  <button id="btnDl" style="padding:8px 18px;background:#20b26b;color:#fff;border:none;border-radius:8px;cursor:pointer" disabled>Download</button>
</div>
<p id="info" style="color:#666;margin-top:12px">Choose an image to begin.</p>
<canvas id="cv" style="max-width:100%;border:1px solid #e6e9f0;border-radius:8px;margin-top:12px;display:none"></canvas>""",
 """(function(){
var $=function(i){return document.getElementById(i)};
var img=null,outUrl=null,origW=0,origH=0;
var file=$('imgFile'),rw=$('rw'),rh=$('rh'),keep=$('keepRatio'),cv=$('cv'),info=$('info'),dl=$('btnDl');
$('quality').addEventListener('input',function(){$('qval').textContent=this.value});
file.addEventListener('change',function(){
  var f=file.files[0];if(!f)return;
  var r=new FileReader();
  r.onload=function(e){var im=new Image();im.onload=function(){
    img=im;origW=im.naturalWidth;origH=im.naturalHeight;
    rw.value=origW;rh.value=origH;
    info.textContent='Original: '+origW+'x'+origH+' px, '+(f.size/1024).toFixed(1)+' KB ('+f.type+')';
  };im.src=e.target.result;};
  r.readAsDataURL(f);
});
rw.addEventListener('input',function(){if(keep.checked&&img){rh.value=Math.round(rw.value*origH/origW);}});
rh.addEventListener('input',function(){if(keep.checked&&img){rw.value=Math.round(rh.value*origW/origH);}});
function doResize(){
  if(!img){alert('Please choose an image first.');return;}
  var w=Math.max(1,parseInt(rw.value,10)||origW),h=Math.max(1,parseInt(rh.value,10)||origH);
  cv.width=w;cv.height=h;cv.style.display='block';
  var ctx=cv.getContext('2d');ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';
  ctx.clearRect(0,0,w,h);
  var fmt=$('fmt').value;
  if(fmt==='image/jpeg'){ctx.fillStyle='#fff';ctx.fillRect(0,0,w,h);}
  ctx.drawImage(img,0,0,w,h);
  outUrl=cv.toDataURL(fmt,parseFloat($('quality').value));
  dl.disabled=false;
  var bytes=Math.round((outUrl.length-outUrl.indexOf(',')-1)*3/4);
  info.textContent='Resized to '+w+'x'+h+' px, about '+(bytes/1024).toFixed(1)+' KB';
}
$('btnResize').addEventListener('click',doResize);
dl.addEventListener('click',function(){
  if(!outUrl)return;var a=document.createElement('a');
  var ext=$('fmt').value.split('/')[1].replace('jpeg','jpg');
  a.href=outUrl;a.download='resized-'+cv.width+'x'+cv.height+'.'+ext;
  document.body.appendChild(a);a.click();document.body.removeChild(a);
});
})();""",
 """<p>Resizing images is one of the most common everyday tasks: shrinking a photo before emailing it, fitting a picture into a website header, meeting an upload limit on a job portal, or preparing an avatar for a social network. Most people reach for desktop software or upload private photos to an unknown website, which is slow and often a privacy risk.</p>
<p>This tool solves that by doing all of the work locally. When you select a file it is read with the browser's built-in <code>FileReader</code> API and drawn onto a canvas element at the size you specify. The canvas is exported back to PNG, JPEG or WebP using <code>toDataURL</code>. Nothing is transmitted over the network, so there is no upload wait, no server-imposed file-size limit, and no chance of your image being logged or reused by a third party.</p>
<p>Key features: exact width and height inputs, an optional aspect-ratio lock so pictures never look stretched, a quality slider that matters for JPEG and WebP output, and a format selector so you can convert as you resize (a large PNG screenshot can come out as a compact WebP). The canvas preview updates in place and the download button saves the result with a descriptive file name that includes the new dimensions.</p>
<p>Typical uses include reducing 4000-pixel camera photos down to 1200 pixels for the web, generating thumbnails, preparing images for Markdown documents, and fitting pictures into a strict pixel budget. Because scaling happens in the browser with high-quality smoothing enabled, results look clean for both upscaling and downscaling. If you need to shrink file size rather than pixel dimensions, try the <a href="image-compressor.html">image compressor</a>; for format conversion without resizing, see <a href="png-to-jpg.html">PNG to JPG</a>.</p>""",
 """<details><summary><strong>Are my images uploaded anywhere?</strong></summary><p>No. All decoding, resizing and encoding happens in your browser. You can disconnect from the internet after the page loads and the tool still works.</p></details>
<details><summary><strong>What is the maximum image size?</strong></summary><p>It depends on your browser's memory, but images up to roughly 50 megapixels usually work. Very large panoramas may be slow on older phones.</p></details>
<details><summary><strong>Does resizing reduce file size?</strong></summary><p>Usually yes, especially with JPEG or WebP output. Lowering the quality slider also lowers file size; WebP at about 0.8 quality gives the smallest files.</p></details>
<details><summary><strong>Can I resize to exact dimensions such as 1920x1080?</strong></summary><p>Yes. Type the width and height you need, uncheck "keep aspect ratio" if the target ratio differs, then press Resize.</p></details>""",
 [("image-compressor.html", "Image Compressor"), ("png-to-jpg.html", "PNG to JPG")])

# ============ 2. EXIF Viewer ============
build(
 "exif-viewer.html",
 "EXIF Viewer Online - View Image Metadata & Photo EXIF Data Free",
 "Free online EXIF viewer: read camera model, lens, ISO, shutter speed, aperture, date taken, GPS location and more from your JPG photos. No upload, runs in your browser.",
 "exif viewer,image metadata,photo exif,view exif data,camera metadata,gps location photo,exif reader",
 "EXIF Viewer - Read Image Metadata Online",
 "Inspect the hidden metadata inside your photos: camera make and model, lens, exposure settings, ISO, orientation, capture time, and GPS coordinates. Everything is parsed locally in your browser.",
 """<h2 style="margin-top:0">View EXIF data</h2>
<input type="file" id="exifFile" accept="image/jpeg,image/jpg,image/tiff,image/png" style="margin:8px 0">
<p style="color:#666">JPEG files carry the most metadata. Pick a photo straight from your camera or phone for the richest results.</p>
<div id="exifOut" style="margin-top:14px"></div>""",
 """(function(){
var $=function(i){return document.getElementById(i)};
var TAGS={0x010F:'Make',0x0110:'Model',0x0112:'Orientation',0x011A:'XResolution',0x011B:'YResolution',
0x0132:'DateTime',0x8769:'ExifIFDPointer',0x8825:'GPSInfoIFDPointer',0x829A:'ExposureTime',0x829D:'FNumber',
0x8827:'ISOSpeedRatings',0x9003:'DateTimeOriginal',0x920A:'FocalLength',0x9209:'Flash',0xA002:'PixelXDimension',
0xA003:'PixelYDimension',0xA434:'LensModel',0xA433:'LensMake',0x0100:'ImageWidth',0x0101:'ImageLength',
0x9207:'MeteringMode',0x9208:'LightSource',0x9290:'SubSecTime',0x9291:'SubSecTimeOriginal',0xA001:'ColorSpace'};
var GPS={0:'GPSVersionID',1:'GPSLatitudeRef',2:'GPSLatitude',3:'GPSLongitudeRef',4:'GPSLongitude',
5:'GPSAltitudeRef',6:'GPSAltitude',7:'GPSTimeStamp',29:'GPSDateStamp'};
function rd(dv,o,l,le){var v=0,i;for(i=0;i<l;i++){v|=dv.getUint8(o+(le?l-1-i:i))<<(8*i);}return v;}
function readIFD(dv,off,tiff,le,sink){
  if(off+2>dv.byteLength)return;
  var n=dv.getUint16(off,le);
  for(var i=0;i<n&&i<200;i++){
    var e=off+2+i*12;if(e+12>dv.byteLength)break;
    var tag=dv.getUint16(e,le),typ=dv.getUint16(e+2,le),cnt=rd(dv,e+4,4,le),valOff=e+8;
    var sizes={1:1,2:1,3:2,4:4,5:8,7:1,9:4,10:8};var sz=(sizes[typ]||1)*cnt;
    var po=(sz>4)?tiff+rd(dv,e+8,4,le):valOff;
    if(po+sz>dv.byteLength)continue;
    var val='';
    if(typ===2){val='';for(var k=0;k<cnt;k++){var c=dv.getUint8(po+k);if(c===0)break;val+=String.fromCharCode(c);}val=val.trim();}
    else if(typ===3){val=dv.getUint16(po,le);if(cnt>1){val='';for(var k2=0;k2<cnt;k2++){val+=(k2?', ':'')+dv.getUint16(po+k2*2,le);}}}
    else if(typ===4){val=rd(dv,po,4,le);}
    else if(typ===5&&cnt===1){var a=rd(dv,po,4,le),b=rd(dv,po+4,4,le);val=b?(a/b).toFixed(4):'0';}
    else if(typ===1&&cnt===1){val=dv.getUint8(po);}
    else continue;
    sink(tag,val,typ,po,cnt,le);
  }
}
function parse(buf){
  var dv=new DataView(buf),len=dv.byteLength;
  if(dv.getUint16(0,false)!==0xFFD8){return {err:'Not a JPEG file (no SOI marker).'};}
  var p=2,exif=null;
  while(p<len-1){
    if(dv.getUint8(p)!==0xFF){p++;continue;}
    var mk=dv.getUint8(p+1);
    if(mk===0xE1){var segLen=dv.getUint16(p+2,false);
      if(dv.getUint32(p+4,false)===0x45786966){exif=p+10;break;}
      p+=2+segLen;continue;}
    if(mk===0xDA||mk===0xD9)break;
    p+=2+dv.getUint16(p+2,false);
  }
  if(exif===null)return {err:'No EXIF segment found. This image has no metadata (screenshots and edited exports usually have none).'};
  var le=dv.getUint16(exif,false)===0x4949;
  if(rd(dv,exif,2,le)!==42)return {err:'Malformed TIFF header.'};
  var ifd0=exif+rd(dv,exif+4,4,le);
  var out={},exifPtr=null,gpsPtr=null;
  readIFD(dv,ifd0,exif,le,function(tag,val){out[TAGS[tag]||('Tag0x'+tag.toString(16))]=val;
    if(tag===0x8769)exifPtr=exif+val; if(tag===0x8825)gpsPtr=exif+val;});
  if(exifPtr)readIFD(dv,exifPtr,exif,le,function(tag,val){out[TAGS[tag]||('Exif0x'+tag.toString(16))]=val;});
  if(gpsPtr){var g={};readIFD(dv,gpsPtr,exif,le,function(tag,val,typ,po,cnt){
    if(tag===2||tag===4){var d=[];for(var i=0;i<3;i++){var a=rd(dv,po+i*8,4,le),b=rd(dv,po+i*8+4,4,le);d.push(b?a/b:0);}val=d.map(function(x){return x.toFixed(4)+String.fromCharCode(176);}).join(' ');}
    g[GPS[tag]||('0x'+tag.toString(16))]=val;});out.GPS=g;}
  return out;
}
function render(res){
  var el=$('exifOut');
  if(res.err){el.innerHTML='<p style="color:#c0392b">'+res.err+'</p>';return;}
  var keys=Object.keys(res);if(!keys.length){el.innerHTML='<p>No readable metadata.</p>';return;}
  var rows='';
  keys.forEach(function(k){
    var v=res[k];
    if(typeof v==='object'){rows+='<tr><td style="padding:6px 10px;font-weight:600;vertical-align:top">'+k+'</td><td style="padding:6px 10px"><pre style="margin:0;white-space:pre-wrap">'+JSON.stringify(v,null,1)+'</pre></td></tr>';}
    else{rows+='<tr><td style="padding:6px 10px;font-weight:600">'+k+'</td><td style="padding:6px 10px">'+String(v).replace(/</g,'&lt;')+'</td></tr>';}
  });
  el.innerHTML='<table style="border-collapse:collapse;width:100%;font-size:14px"><tbody>'+rows+'</tbody></table>'+
   '<p style="color:#666;margin-top:10px">'+keys.length+' metadata fields found. Values are read directly from the file and never sent anywhere.</p>';
}
$('exifFile').addEventListener('change',function(){
  var f=this.files[0];if(!f)return;
  var r=new FileReader();
  r.onload=function(e){try{$('exifOut').innerHTML='<p>Parsing...</p>';render(parse(e.target.result));}
    catch(err){$('exifOut').innerHTML='<p style="color:#c0392b">Could not parse this file: '+err.message+'</p>';}};
  r.readAsArrayBuffer(f);
});
})();""",
 """<p>Most digital photos contain more than pixels. Cameras and phones embed an EXIF block (Exchangeable Image File Format) that records how the picture was taken: the camera manufacturer and model, the lens, the focal length, exposure time, aperture, ISO sensitivity, metering mode, the exact date and time, the orientation of the sensor, and - if you allowed location tagging - the GPS latitude and longitude where the shutter fired.</p>
<p>An EXIF viewer is useful in several situations. Photographers inspect the metadata after a shoot to remember which settings produced a good result. Buyers checking a used camera can confirm a file really came from that model. Content creators strip or verify GPS data before posting images publicly, because a photo can reveal exactly where someone lives. Researchers and journalists verify the provenance and capture time of an image.</p>
<p>This tool reads the file with <code>ArrayBuffer</code> and parses the TIFF header, the IFD0 directory, the Exif sub-IFD and the GPS IFD directly in the browser. It handles both little-endian and big-endian files and decodes ASCII, SHORT, LONG and RATIONAL values. GPS coordinates made of three rationals (degrees, minutes and seconds) are converted into readable decimal degrees. Nothing is uploaded, so the metadata of your private photos stays private.</p>
<p>Limitations to be aware of: PNG and WebP files usually carry no EXIF, so results will be empty for screenshots. Images that passed through social networks, messaging apps or editors are often re-encoded and lose their metadata - that is a feature of those platforms' privacy filtering, not a fault of the viewer. If you need to see how much a photo would shrink in size, the <a href="image-compressor.html">image compressor</a> can help; to resize without losing quality, use the <a href="image-resizer.html">image resizer</a>.</p>""",
 """<details><summary><strong>What exactly is EXIF data?</strong></summary><p>EXIF is a metadata standard embedded in image files. It stores camera settings, timestamps, device information and optional GPS coordinates so software can display and organise photos.</p></details>
<details><summary><strong>Does every photo have EXIF data?</strong></summary><p>No. Screenshots, downloaded images and pictures edited by many apps have their metadata removed. Photos straight from a camera or phone usually include it.</p></details>
<details><summary><strong>Can this tool see the GPS location of a photo?</strong></summary><p>Yes, if the file contains a GPS IFD. The latitude and longitude are shown in decimal degrees, convertible to a map URL.</p></details>
<details><summary><strong>Is my photo uploaded?</strong></summary><p>Never. The file is read into memory in your browser and discarded when you close the page.</p></details>""",
 [("image-resizer.html", "Image Resizer"), ("image-compressor.html", "Image Compressor")])

# ============ 3. JSON Escape / Unescape ============
build(
 "json-escape.html",
 "JSON Escape / Unescape Online - Escape JSON Strings Free",
 "Free online JSON escape and unescape tool: convert text to escaped JSON string literals and decode escaped sequences back to plain text. Handles quotes, backslashes, unicode and newlines.",
 "json escape,json unescape,escape json string,json stringify,escape quotes,decode json string,json string literal",
 "JSON Escape / Unescape - Convert Text to JSON Strings",
 "Turn any text into a valid JSON string literal, or decode an escaped JSON string back into readable text. Handy when you need to embed JSON inside code, config files or another JSON document.",
 """<h2 style="margin-top:0">Input</h2>
<textarea id="in" rows="8" style="width:100%;box-sizing:border-box;font-family:ui-monospace,Consolas,monospace;padding:10px;border:1px solid #ccd;border-radius:8px" placeholder='Type or paste text here. Example: He said "hello" &amp; left.'></textarea>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin:12px 0">
  <button id="esc" style="padding:8px 18px;background:#4f6ef7;color:#fff;border:none;border-radius:8px;cursor:pointer">Escape &rarr; JSON</button>
  <button id="unesc" style="padding:8px 18px;background:#20b26b;color:#fff;border:none;border-radius:8px;cursor:pointer">&larr; Unescape</button>
  <button id="cp" style="padding:8px 18px;background:#eef1ff;color:#334;border:1px solid #ccd;border-radius:8px;cursor:pointer">Copy output</button>
  <button id="clr" style="padding:8px 18px;background:#f6f7fb;color:#334;border:1px solid #ccd;border-radius:8px;cursor:pointer">Clear</button>
</div>
<label><input type="checkbox" id="wrap" checked> Wrap output in double quotes (full JSON string literal)</label>
<h2>Output</h2>
<textarea id="out" rows="8" readonly style="width:100%;box-sizing:border-box;font-family:ui-monospace,Consolas,monospace;padding:10px;border:1px solid #ccd;border-radius:8px;background:#fafbff"></textarea>
<p id="stat" style="color:#666"></p>""",
 """(function(){
var $=function(i){return document.getElementById(i)};
function esc(s,wrap){
  var o=JSON.stringify(s);
  if(!wrap&&o.length>=2)o=o.slice(1,-1);
  return o;
}
function unesc(s){
  var t=s.trim();
  if(t.length>=2&&t[0]==='"'&&t[t.length-1]==='"'){try{return JSON.parse(t);}catch(e){}}
  t=t.replace(/^"+|"+$/g,'');
  try{return JSON.parse('"'+t.replace(/"/g,'\\\\"').replace(/\\\\"/g,'\\\\"')+'"');}
  catch(e){
    return t.replace(/\\\\u([0-9a-fA-F]{4})/g,function(m,h){return String.fromCharCode(parseInt(h,16));})
            .replace(/\\\\n/g,'\\n').replace(/\\\\t/g,'\\t').replace(/\\\\r/g,'\\r')
            .replace(/\\\\b/g,'\\b').replace(/\\\\f/g,'\\f')
            .replace(/\\\\"/g,'"').replace(/\\\\\\\\/g,'\\\\');
  }
}
function upd(){
  var v=$('out').value;$('stat').textContent='Output length: '+v.length+' characters';
}
$('esc').addEventListener('click',function(){$('out').value=esc($('in').value,$('wrap').checked);upd();});
$('unesc').addEventListener('click',function(){var src=$('in').value;$('out').value=unesc(src);upd();});
$('cp').addEventListener('click',function(){var o=$('out');o.select();
  var ok=false;try{ok=document.execCommand('copy');}catch(e){}
  if(navigator.clipboard&&!ok){navigator.clipboard.writeText(o.value);}
  $('stat').textContent='Copied to clipboard.';});
$('clr').addEventListener('click',function(){$('in').value='';$('out').value='';$('stat').textContent='';});
})();""",
 """<p>JSON string literals have strict escaping rules. A double quote inside the text must be written as <code>\\"</code>, a backslash as <code>\\\\</code>, and control characters must be encoded - a newline becomes <code>\\n</code>, a tab <code>\\t</code>, and any non-ASCII character may be written as a <code>\\uXXXX</code> escape. Whenever you need to place a piece of text inside a JSON document, a JavaScript string, a log format or a database column typed as JSON, you have to apply those rules correctly or the parser will reject the whole document.</p>
<p>This tool handles both directions. The Escape button takes whatever you paste and produces a valid JSON string literal, using the browser's native <code>JSON.stringify</code> so the output is guaranteed to be spec-compliant. The Unescape button takes an escaped string - with or without the surrounding quotes - and turns it back into readable text, decoding unicode escapes, newlines, tabs and escaped quotes.</p>
<p>Common real-world uses: preparing a snippet of HTML or SQL for embedding in a JSON config file, escaping a Windows file path (<code>C:\\Users\\name</code>) so it can live inside JSON, cleaning up API responses that arrive with escaped bodies, or reading a stack trace that has been double-encoded. Because the escaping is performed with the platform's own serialiser, characters such as emoji and accented letters produce identical results to what JavaScript, Python, Go and most other languages expect.</p>
<p>Note that escaping is not the same as minifying: to re-indent or validate a whole JSON document use the <a href="json-formatter.html">JSON formatter</a>; to turn JSON into query-friendly CSV use <a href="json-to-csv.html">JSON to CSV</a>.</p>""",
 """<details><summary><strong>What is the difference between escaping and encoding?</strong></summary><p>Escaping rewrites characters so they are legal inside a JSON string (quotes, backslashes, control characters). Encoding (such as Base64 or URL encoding) transforms the whole byte stream for a different transport.</p></details>
<details><summary><strong>Should I keep the surrounding double quotes?</strong></summary><p>Keep them if you are pasting the result into a JSON document as a string value. Remove them if you need just the inner content.</p></details>
<details><summary><strong>Does it handle unicode and emoji?</strong></summary><p>Yes. Escaping uses JSON.stringify, which outputs UTF-8 characters directly or \\uXXXX sequences depending on the character.</p></details>
<details><summary><strong>Is my data sent to a server?</strong></summary><p>No. The conversion runs entirely in JavaScript on this page.</p></details>""",
 [("json-formatter.html", "JSON Formatter"), ("json-to-csv.html", "JSON to CSV"), ("base64.html", "Base64 Encoder")])

print("done")
