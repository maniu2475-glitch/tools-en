# -*- coding: utf-8 -*-
"""Batch: 5 new tool pages + update index.html / all-tools.html / sitemap.xml (2026-10-27)."""
import io, re, sys
sys.path.insert(0, '.')
from generate_tool_page import page

TODAY = "2026-10-27"
NEW = [
 dict(slug="data-storage-converter.html", title="Data Storage Converter - Bytes, KB, MB, GB, TB",
   og="Data storage converter", kw="data storage converter,bytes to kb,kb to mb,mb to gb,gb to tb,binary prefixes,kibibyte",
   h1="Data Storage Converter (Bytes / KB / MB / GB / TB / KiB / MiB)",
   body='''<div class="opt-group"><select id="ds-from" class="wide"></select><label> to </label><select id="ds-to" class="wide"></select></div>
<div class="opt-group"><input type="number" id="ds-input" value="1" step="any" style="width:100%" placeholder="Enter value"></div>
<div class="btn-group"><button class="btn" onclick="dsConv()">Convert</button></div>
<div class="result" id="ds-out">Result appears here</div>
<script>
var dsUnits=[["bit",1/8],["Byte",1],["KB (1000)",1e3],["MB (1000²)",1e6],["GB (1000³)",1e9],["TB (1000⁴)",1e12],
["KiB (1024)",1024],["MiB (1024²)",1048576],["GiB (1024³)",1073741824],["TiB (1024⁴)",1099511627776]];
function dsFill(){var f=document.getElementById('ds-from'),t=document.getElementById('ds-to');dsUnits.forEach(function(u,i){f.add(new Option(u[0],i));t.add(new Option(u[0],i));});f.value=3;t.value=1;}
function dsConv(){var v=parseFloat(document.getElementById('ds-input').value);if(isNaN(v)){document.getElementById('ds-out').textContent='Please enter a valid number';return;}
var fi=+document.getElementById('ds-from').value,ti=+document.getElementById('ds-to').value;
var bytes=v*dsUnits[fi][1], r=bytes/dsUnits[ti][1];
document.getElementById('ds-out').innerHTML='<strong>'+dsNum(v)+' '+dsUnits[fi][0]+' = '+dsNum(r)+' '+dsUnits[ti][0]+'</strong><br>'+dsNum(bytes)+' bytes';}
function dsNum(x){if(x===0)return '0';if(Math.abs(x)>=1e15||Math.abs(x)<1e-6)return x.toExponential(6);return (+x.toPrecision(12)).toString();}
dsFill();dsConv();
</script>''',
   about='''A data storage converter translates between the many units used to measure digital information: bits, bytes, kilobytes, megabytes, gigabytes, terabytes, and the binary prefixed kibibytes (KiB), mebibytes (MiB), gibibytes (GiB) and tebibytes (TiB). The classic source of confusion is that hard-drive and network marketers use decimal units where 1 KB = 1000 bytes, while operating systems often report sizes using binary units where 1 KiB = 1024 bytes. That is why a "500 GB" drive shows as roughly 465 GiB in Windows. This converter supports both families side by side so you can check the real numbers yourself. It handles scientific input, formats large and small results cleanly, and shows the intermediate byte count. Whether you are comparing cloud storage plans, sizing a database export, estimating how many photos fit on a memory card, or decoding an ISP data cap, this free browser-side tool gives instant answers with zero signup and no data uploaded anywhere.'''),
 dict(slug="speed-converter.html", title="Speed Converter - km/h, mph, m/s, knots, ft/s",
   og="Speed converter", kw="speed converter,kmh to mph,mph to kmh,m/s to km/h,knots to mph,feet per second,speed units",
   h1="Speed Converter (km/h · mph · m/s · knots · ft/s)",
   body='''<div class="opt-group"><select id="sp-from" class="wide"></select><label> to </label><select id="sp-to" class="wide"></select></div>
<div class="opt-group"><input type="number" id="sp-input" value="100" step="any" style="width:100%" placeholder="Enter speed"></div>
<div class="btn-group"><button class="btn" onclick="spConv()">Convert</button></div>
<div class="result" id="sp-out">Result appears here</div>
<script>
var spUnits=[["km/h",1],["mph",1.609344],["m/s",3.6],["knots",1.852],["ft/s",1.09728],["cm/s",0.036]];
function spFill(){var f=document.getElementById('sp-from'),t=document.getElementById('sp-to');spUnits.forEach(function(u,i){f.add(new Option(u[0],i));t.add(new Option(u[0],i));});f.value=0;t.value=1;}
function spConv(){var v=parseFloat(document.getElementById('sp-input').value);if(isNaN(v)){document.getElementById('sp-out').textContent='Please enter a valid number';return;}
var fi=+document.getElementById('sp-from').value,ti=+document.getElementById('sp-to').value;
var base=v*spUnits[fi][1], r=base/spUnits[ti][1];
document.getElementById('sp-out').innerHTML='<strong>'+v+' '+spUnits[fi][0]+' = '+(+r.toFixed(6))+' '+spUnits[ti][0]+'</strong>';}
spFill();spConv();
</script>''',
   about='''This speed converter instantly translates between the six most common velocity units: kilometres per hour (km/h), miles per hour (mph), metres per second (m/s), knots (kn), feet per second (ft/s) and centimetres per second. Each field uses exact conversion factors, so 100 km/h becomes 62.137119 mph and 60 mph becomes exactly 96.56064 km/h. The tool is handy for drivers comparing speed limits between countries, runners checking treadmill paces, sailors and pilots working with knots, physics students converting to SI units, and engineers reading fan or airflow specifications. Type any number, pick the two units, and the answer appears immediately - there is no server round trip, because all math runs locally in your browser. That makes it safe, fast and available offline once loaded. Common reference points: highway speeds are around 100-130 km/h, a marathon runner averages roughly 12 km/h, and the speed of sound is about 1,235 km/h or 767 mph.'''),
 dict(slug="volume-converter.html", title="Volume Converter - Liters, Gallons, Cups, ml, oz",
   og="Volume converter", kw="volume converter,liters to gallons,gallons to liters,ml to cups,cups to ml,fl oz to ml,quarts,pints",
   h1="Volume Converter (liters · gallons · cups · ml · fl oz · quarts · pints)",
   body='''<div class="opt-group"><select id="vol-from" class="wide"></select><label> to </label><select id="vol-to" class="wide"></select></div>
<div class="opt-group"><input type="number" id="vol-input" value="1" step="any" style="width:100%" placeholder="Enter volume"></div>
<div class="btn-group"><button class="btn" onclick="volConv()">Convert</button></div>
<div class="result" id="vol-out">Result appears here</div>
<script>
var volUnits=[["milliliters (ml)",1],["liters (L)",1000],["US teaspoons",4.92892159375],["US tablespoons",14.78676478125],
["US fluid ounces",29.5735295625],["US cups",236.5882365],["US pints",473.176473],["US quarts",946.352946],
["US gallons",3785.411784],["imperial fluid ounces",28.4130625],["imperial pints",568.26125],["imperial gallons",4546.09],
["cubic meters",1e6],["cubic feet",28316.846592],["cubic inches",16.387064]];
function volFill(){var f=document.getElementById('vol-from'),t=document.getElementById('vol-to');volUnits.forEach(function(u,i){f.add(new Option(u[0],i));t.add(new Option(u[0],i));});f.value=8;t.value=1;}
function volConv(){var v=parseFloat(document.getElementById('vol-input').value);if(isNaN(v)){document.getElementById('vol-out').textContent='Please enter a valid number';return;}
var fi=+document.getElementById('vol-from').value,ti=+document.getElementById('vol-to').value;
var base=v*volUnits[fi][1], r=base/volUnits[ti][1];
document.getElementById('vol-out').innerHTML='<strong>'+v+' '+volUnits[fi][0]+' = '+(+r.toFixed(6))+' '+volUnits[ti][0]+'</strong>';}
volFill();volConv();
</script>''',
   about='''Cooking recipes, chemistry labs, aquariums and fuel economy all measure volume, but they use wildly different units. This converter covers metric units (millilitres, litres, cubic metres), US customary units (teaspoons, tablespoons, fluid ounces, cups, pints, quarts, gallons), imperial units (imperial fluid ounces, pints, gallons) and cubic feet / cubic inches. All factors are exact legal definitions: 1 US gallon = 3.785411784 litres, 1 imperial gallon = 4.54609 litres, 1 US cup = 236.5882365 ml. Note that US and imperial cups, pints and gallons differ - a US gallon is about 0.83 imperial gallons - which is why British and American recipes never quite match. Use this tool to scale a recipe, convert a car's fuel tank size, check a drink label, or convert lab quantities. Everything is calculated in your browser with no signup, no ads inside the tool, and your input never leaves your device.'''),
 dict(slug="angle-converter.html", title="Angle Converter - Degrees, Radians, Gradians, Turns",
   og="Angle converter", kw="angle converter,degrees to radians,radians to degrees,gradian,turn,arcminute,arcsecond,revolution",
   h1="Angle Converter (degrees · radians · gradians · turns · arcminutes)",
   body='''<div class="opt-group"><select id="ag-from" class="wide"></select><label> to </label><select id="ag-to" class="wide"></select></div>
<div class="opt-group"><input type="number" id="ag-input" value="180" step="any" style="width:100%" placeholder="Enter angle"></div>
<div class="btn-group"><button class="btn" onclick="agConv()">Convert</button></div>
<div class="result" id="ag-out">Result appears here</div>
<script>
var agUnits=[["degrees",1],["radians",57.29577951308232],["gradians",0.9],["turns",360],["arcminutes",1/60],["arcseconds",1/3600],["milliradians",0.05729577951]];
function agFill(){var f=document.getElementById('ag-from'),t=document.getElementById('ag-to');agUnits.forEach(function(u,i){f.add(new Option(u[0],i));t.add(new Option(u[0],i));});f.value=0;t.value=1;}
function agConv(){var v=parseFloat(document.getElementById('ag-input').value);if(isNaN(v)){document.getElementById('ag-out').textContent='Please enter a valid number';return;}
var fi=+document.getElementById('ag-from').value,ti=+document.getElementById('ag-to').value;
var base=v*agUnits[fi][1], r=base/agUnits[ti][1];
document.getElementById('ag-out').innerHTML='<strong>'+v+' '+agUnits[fi][0]+' = '+(+r.toFixed(10))+' '+agUnits[ti][0]+'</strong>';}
agFill();agConv();
</script>''',
   about='''Angles appear in trigonometry homework, CAD drawings, astronomy coordinates, satellite pointing, game development and machining. The four main systems each divide a full circle differently: 360 degrees, 2π radians, 400 gradians, or 1 turn. Radians are the natural unit of mathematics because sin, cos and tan in calculus assume them; degrees dominate everyday navigation and engineering drawings; gradians (also called gons) survive in European surveying where a right angle is exactly 100 gon; and the mil (milliradian) is used for artillery and rifle scopes, where 1 mil ≈ 1 metre at 1000 metres. This converter also handles arcminutes and arcseconds, the 1/60 and 1/3600 subdivisions used in astronomy and GPS coordinates. Conversions use the exact factor 180/π per radian. Enter any value including decimals or numbers beyond a full turn, and the result is computed instantly in your browser - no login, no limits, nothing sent to a server.'''),
 dict(slug="download-time-calculator.html", title="Download Time Calculator - How Long to Download",
   og="Download time calculator", kw="download time calculator,how long to download,file size bandwidth,mbps to mb/s,transfer time estimator",
   h1="Download Time Calculator",
   body='''<div class="opt-group"><label>File size:</label><input type="number" id="dt-size" value="10" min="0" step="any" style="width:110px"><select id="dt-unit" style="width:110px"><option value="1">MB</option><option value="1024">GB</option><option value="0.001">KB</option></select></div>
<div class="opt-group"><label>Connection speed:</label><input type="number" id="dt-speed" value="100" min="0" step="any" style="width:110px"><select id="dt-sunit" style="width:140px"><option value="1000000">Mbps</option><option value="125000">MB/s</option><option value="1000000000">Gbps</option><option value="1250">KB/s</option></select></div>
<div class="opt-group"><label>Realistic overhead/efficiency: <input type="number" id="dt-eff" value="90" min="1" max="100" step="1" style="width:70px">%</label></div>
<div class="btn-group"><button class="btn" onclick="dtCalc()">Calculate download time</button></div>
<div class="result" id="dt-out">Result appears here</div>
<script>
function dtCalc(){var s=parseFloat(document.getElementById('dt-size').value)*parseFloat(document.getElementById('dt-unit').value);
var sp=parseFloat(document.getElementById('dt-speed').value)*parseFloat(document.getElementById('dt-sunit').value);
var eff=parseFloat(document.getElementById('dt-eff').value)/100;
if(isNaN(s)||isNaN(sp)||s<=0||sp<=0){document.getElementById('dt-out').textContent='Please enter positive numbers';return;}
var sec=s/(sp*eff);
var h=Math.floor(sec/3600),m=Math.floor(sec%3600/60),ss=Math.round(sec%60);
var str=(h>0?h+' h ':'')+(m>0?m+' min ':'')+ss+' s';
document.getElementById('dt-out').innerHTML='<strong>Download time: '+str+'</strong><br>'+(+sec.toFixed(1))+' seconds at '+(+((sp*eff)/125000).toFixed(2))+' MB/s effective';}
dtCalc();
</script>''',
   about='''This calculator answers the classic question "how long will this download take?" by combining file size, connection speed and real-world efficiency. The key insight it encodes is the difference between megabits (Mb) and megabytes (MB): internet plans are sold in Mbps but files are measured in MB, and 8 megabits equal 1 megabyte, so a 100 Mbps line moves at most 12.5 MB/s. On top of that, protocol overhead, Wi-Fi loss, disk speed and server limits typically reduce throughput to around 80-95 percent of the theoretical rate - adjustable with the efficiency field. Enter a 70 GB game on a 300 Mbps fibre line and you will see roughly 35 minutes; a 4 GB movie on 25 Mbps ADSL needs about 25 minutes. The tool supports file sizes in KB/MB/GB and speeds in Mbps, MB/s, Gbps or KB/s, then formats the result in seconds, minutes or hours automatically. All calculations run locally in your browser, so it works offline and your inputs are never transmitted anywhere.'''),
]

for t in NEW:
    html = page(t['slug'], t['title'], t['og'], t['kw'], t['h1'], t['body'], t['about'])
    io.open(t['slug'], 'w', encoding='utf-8').write(html)
    print("wrote", t['slug'], len(html))

# ---- update index.html footer list ----
idx = io.open('index.html', encoding='utf-8').read()
old_tail = '<a href="decimal-to-fraction.html">Decimal to Fraction Converter</a></p>\n</main>'
new_tail = ('<a href="decimal-to-fraction.html">Decimal to Fraction Converter</a> · '
 + ' · '.join('<a href="%s">%s</a>' % (t['slug'], t['title'].split(' - ')[0].split(' (')[0].split(' Converter')[0] if ' Converter' in t['title'] else t['title']) for t in NEW)
 + '</p>\n</main>')
assert old_tail in idx, "index tail not found"
idx = idx.replace(old_tail, new_tail)
io.open('index.html', 'w', encoding='utf-8').write(idx)
print("index.html updated")

# ---- update all-tools.html list ----
at = io.open('all-tools.html', encoding='utf-8').read()
old_li = '<li><a href="decimal-to-fraction.html">Decimal to Fraction Converter</a></li>\n</ul>'
new_li = old_li.replace('</ul>', '\n'.join('<li><a href="%s">%s</a></li>' % (t['slug'], t['title'].split(' - ')[0].split(' (')[0]) for t in NEW) + '\n</ul>')
assert old_li in at, "all-tools tail not found"
at = at.replace(old_li, new_li)
io.open('all-tools.html', 'w', encoding='utf-8').write(at)
print("all-tools.html updated")

# ---- update sitemap.xml ----
sm = io.open('sitemap.xml', encoding='utf-8').read()
assert sm.rstrip().endswith('</urlset>')
add = ''.join('''  <url>
    <loc>https://maniu2475-glitch.github.io/tools-en/%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
''' % (t['slug'], TODAY) for t in NEW)
sm = sm.rstrip()[:-len('</urlset>')] + add + '</urlset>\n'
io.open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print("sitemap.xml updated")
print("DONE")
