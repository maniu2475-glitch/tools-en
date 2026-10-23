/* ===== 在线工具箱 app.js ===== */
"use strict";

/* ---------- 导航与面板切换 ---------- */
function initNav() {
  const toggle = document.getElementById('menuToggle');
  const nav = document.getElementById('mainNav');
  toggle.addEventListener('click', () => nav.classList.toggle('open'));

  nav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => nav.classList.remove('open'));
  });

  window.addEventListener('hashchange', showPanel);
  showPanel();
}

function showPanel() {
  let id = location.hash.replace('#', '') || 'home';
  const panels = document.querySelectorAll('.tool-panel');
  const target = document.getElementById('tool-' + id);
  if (!target) id = 'home';
  panels.forEach(p => p.classList.toggle('active', p.id === 'tool-' + id));
  // 高亮导航
  document.querySelectorAll('.main-nav a').forEach(a =>
    a.classList.toggle('active', a.dataset.tool === id));
  // 预填时间戳
  if (id === 'timestamp') startClock();
  window.scrollTo(0, 0);
}

/* ---------- JSON ---------- */
function getJsonInput() { return document.getElementById('json-input').value; }
function setJsonOutput(text) { document.getElementById('json-output').textContent = text; }

function jsonFormat() {
  try {
    const obj = JSON.parse(getJsonInput());
    setJsonOutput(JSON.stringify(obj, null, 2));
  } catch (e) { setJsonOutput('❌ JSON error: ' + e.message); }
}
function jsonMinify() {
  try {
    const obj = JSON.parse(getJsonInput());
    setJsonOutput(JSON.stringify(obj));
  } catch (e) { setJsonOutput('❌ JSON error: ' + e.message); }
}
function jsonValidate() {
  try {
    JSON.parse(getJsonInput());
    setJsonOutput('✅ Valid JSON');
  } catch (e) { setJsonOutput('❌ JSON error: ' + e.message); }
}
function jsonCopy() {
  const text = document.getElementById('json-output').textContent;
  navigator.clipboard.writeText(text).then(() => alert('Copied to clipboard'));
}

/* ---------- Base64 / URL ---------- */
function utf8ToB64(str) { return btoa(unescape(encodeURIComponent(str))); }
function b64ToUtf8(b64) { return decodeURIComponent(escape(atob(b64))); }
function b64Encode() {
  try { document.getElementById('b64-output').value = utf8ToB64(document.getElementById('b64-input').value); }
  catch (e) { document.getElementById('b64-output').value = '❌ 编码失败：' + e.message; }
}
function b64Decode() {
  try { document.getElementById('b64-output').value = b64ToUtf8(document.getElementById('b64-input').value.trim()); }
  catch (e) { document.getElementById('b64-output').value = '❌ Not valid Base64'; }
}
function urlEncode() { document.getElementById('url-output').value = encodeURIComponent(document.getElementById('url-input').value); }
function urlDecode() {
  try { document.getElementById('url-output').value = decodeURIComponent(document.getElementById('url-input').value); }
  catch (e) { document.getElementById('url-output').value = '❌ Decode failed: ' + e.message; }
}
function swapText(aId, bId) {
  const a = document.getElementById(aId), b = document.getElementById(bId);
  [a.value, b.value] = [b.value, a.value];
}

/* ---------- 二维码 ---------- */
let qrSize = 200;
document.addEventListener('DOMContentLoaded', () => {
  const sizeEl = document.getElementById('qr-size');
  if (sizeEl) {
    sizeEl.addEventListener('input', () => {
      qrSize = +sizeEl.value;
      document.getElementById('qr-size-val').textContent = qrSize;
    });
  }
});
function qrGenerate() {
  const text = document.getElementById('qr-input').value.trim();
  const box = document.getElementById('qr-output');
  box.innerHTML = '';
  if (!text) { box.innerHTML = '<p style="color:#9aa1ad">请输入内容后再生成</p>'; return; }
  if (typeof QRCode === 'undefined') { box.innerHTML = '<p style="color:#d93025">二维码库加载失败，请检查网络</p>'; return; }
  new QRCode(box, { text, width: qrSize, height: qrSize, correctLevel: QRCode.CorrectLevel.M });
}
function qrDownload() {
  const img = document.querySelector('#qr-output img');
  if (!img) { alert('Generate a QR code first'); return; }
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = qrSize;
  canvas.getContext('2d').drawImage(img, 0, 0, qrSize, qrSize);
  const a = document.createElement('a');
  a.href = canvas.toDataURL('image/png');
  a.download = 'qrcode.png';
  a.click();
}

/* ---------- 密码生成 ---------- */
function pwdGenerate() {
  const len = +document.getElementById('pwd-length').value;
  let chars = '';
  if (document.getElementById('pwd-upper').checked) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  if (document.getElementById('pwd-lower').checked) chars += 'abcdefghijklmnopqrstuvwxyz';
  if (document.getElementById('pwd-digit').checked) chars += '0123456789';
  if (document.getElementById('pwd-symbol').checked) chars += '!@#$%^&*()-_=+[]{};:,.<>?';
  if (!chars) { document.getElementById('pwd-output').textContent = 'Select at least one character type'; return; }
  const noDup = document.getElementById('pwd-nodup').checked;
  let pwd = '';
  const rand = new Uint32Array(len * 4);
  crypto.getRandomValues(rand);
  for (let i = 0; i < rand.length && pwd.length < len; i++) {
    const c = chars[rand[i] % chars.length];
    if (noDup && pwd.includes(c)) continue;
    pwd += c;
  }
  if (noDup && pwd.length < len && chars.length < len) {
    document.getElementById('pwd-output').textContent = '⚠️ Charset too small for a unique ' + len + '-char password';
    return;
  }
  document.getElementById('pwd-output').textContent = pwd;
  updateStrength(pwd, chars.length);
}
function pwdCopy() {
  navigator.clipboard.writeText(document.getElementById('pwd-output').textContent)
    .then(() => alert('Copied to clipboard'));
}
function updateStrength(pwd, pool) {
  const bits = pwd.length * Math.log2(pool || 2);
  const bar = document.getElementById('pwd-strength');
  const txt = document.getElementById('pwd-strength-text');
  let pct, label, color;
  if (bits < 40) { pct = 25; label = 'Weak'; color = '#d93025'; }
  else if (bits < 60) { pct = 50; label = 'Fair'; color = '#f9ab00'; }
  else if (bits < 100) { pct = 75; label = 'Strong'; color = '#1e8e3e'; }
  else { pct = 100; label = 'Very strong'; color = '#0d652d'; }
  bar.style.width = pct + '%';
  bar.style.background = color;
  txt.textContent = 'Strength: ' + label + '（约 ' + Math.round(bits) + ' 位熵）';
}

/* ---------- 时间戳 ---------- */
let clockTimer = null;
function startClock() {
  if (clockTimer) return;
  const tick = () => {
    const now = Date.now();
    const el = document.getElementById('ts-now');
    if (el) el.textContent = Math.floor(now / 1000) + ' s / ' + now + ' ms';
  };
  tick();
  clockTimer = setInterval(tick, 1000);
}
function tsToDate() {
  let ts = document.getElementById('ts-input').value.trim();
  const out = document.getElementById('ts-date-out');
  if (!/^\d{10,13}$/.test(ts)) { out.textContent = '❌ Enter a 10-digit (sec) or 13-digit (ms) timestamp'; return; }
  if (ts.length === 10) ts = +ts * 1000;
  const d = new Date(+ts);
  out.textContent = 'Local: ' + d.toLocaleString('en-US', { hour12: false })
    + '\nUTC：' + d.toISOString();
  out.style.whiteSpace = 'pre-wrap';
}
function dateToTs() {
  const v = document.getElementById('date-input').value;
  const out = document.getElementById('ts-out2');
  if (!v) { out.textContent = '❌ Pick a date & time'; return; }
  const d = new Date(v);
  out.textContent = 'Seconds: ' + Math.floor(d.getTime() / 1000)
    + '\n毫秒级：' + d.getTime()
    + '\nISO：' + d.toISOString();
  out.style.whiteSpace = 'pre-wrap';
}

/* ---------- 颜色 ---------- */
function hexToRgb(hex) {
  hex = hex.replace('#', '');
  if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
  if (!/^[0-9a-fA-F]{6}$/.test(hex)) return null;
  return [parseInt(hex.slice(0,2),16), parseInt(hex.slice(2,4),16), parseInt(hex.slice(4,6),16)];
}
function rgbToHsl(r, g, b) {
  r/=255; g/=255; b/=255;
  const max = Math.max(r,g,b), min = Math.min(r,g,b);
  let h=0, s=0, l=(max+min)/2;
  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d/(2-max-min) : d/(max+min);
    if (max===r) h = ((g-b)/d + (g<b?6:0));
    else if (max===g) h = ((b-r)/d + 2);
    else h = ((r-g)/d + 4);
    h /= 6;
  }
  return [Math.round(h*360), Math.round(s*100), Math.round(l*100)];
}
function hslToHex(h, s, l) {
  s/=100; l/=100;
  const f = n => {
    const k = (n + h/30) % 12;
    const a = s * Math.min(l, 1-l);
    const c = l - a * Math.min(-1, Math.min(k-3, Math.min(9-k, 1)));
    return Math.round(255*c).toString(16).padStart(2,'0');
  };
  return '#' + f(0)+f(8)+f(4);
}
function colorUpdate(fromHex) {
  const hex = document.getElementById('color-hex').value.trim();
  const rgb = hexToRgb(hex);
  if (!rgb) return;
  document.getElementById('color-picker').value = '#' + hex.replace('#','').toLowerCase();
  renderColor(rgb, hex.startsWith('#') ? hex.toLowerCase() : ('#' + hex.toLowerCase()));
}
function colorFromHex() { colorUpdate(); }
function renderColor(rgb, hex) {
  const [h, s, l] = rgbToHsl(...rgb);
  document.getElementById('color-info').textContent =
    'HEX: ' + hex + '   RGB: rgb(' + rgb.join(', ') + ')   HSL: hsl(' + h + ', ' + s + '%, ' + l + '%)';
  // 配色方案
  const schemes = {
    '互补色': [hslToHex((h+180)%360, s, l)],
    '类似色': [hslToHex((h+30)%360, s, l), hslToHex((h-30+360)%360, s, l)],
    '三角': [hslToHex((h+120)%360, s, l), hslToHex((h+240)%360, s, l)],
    '明暗': [hslToHex(h, s, Math.min(l+20,95)), hslToHex(h, s, Math.max(l-20,5))],
  };
  const out = document.getElementById('palette-out');
  out.innerHTML = '';
  const items = [['主色', hex]].concat(Object.entries(schemes).flatMap(([k, arr]) => arr.map(c => [k, c])));
  items.forEach(([name, c]) => {
    const div = document.createElement('div');
    div.className = 'palette-item';
    div.innerHTML = '<div class="palette-swatch" style="background:' + c + '"></div><div class="palette-label">' + name + '<br>' + c + '</div>';
    div.title = '点击复制 ' + c;
    div.style.cursor = 'pointer';
    div.onclick = () => navigator.clipboard.writeText(c).then(() => div.title = '已复制!');
    out.appendChild(div);
  });
}
// 取色器变化
document.addEventListener('DOMContentLoaded', () => {
  const picker = document.getElementById('color-picker');
  if (picker) picker.addEventListener('input', () => {
    document.getElementById('color-hex').value = picker.value.toUpperCase();
    colorUpdate();
  });
  colorUpdate();
});

/* ---------- Markdown ---------- */
function mdRender() {
  const input = document.getElementById('md-input');
  const out = document.getElementById('md-output');
  if (!input || !out || typeof marked === 'undefined') return;
  marked.setOptions({ breaks: true, gfm: true });
  out.innerHTML = marked.parse(input.value);
}
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('md-input');
  if (input) {
    input.addEventListener('input', mdRender);
    mdRender();
  }
  startClock();
});

/* ---------- 字数统计 ---------- */
function countText() {
  const text = document.getElementById('count-input').value;
  const chars = text.length;
  const charsNoSpace = text.replace(/\s/g, '').length;
  const cjk = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  const words = (text.replace(/[\u4e00-\u9fa5]/g, ' ').match(/[A-Za-z0-9_'-]+/g) || []).length;
  const lines = text ? text.split('\n').length : 0;
  const paragraphs = text.trim() ? text.trim().split(/\n\s*\n/).length : 0;
  const bytes = new Blob([text]).size;
  const stats = [
    [chars, 'Characters'], [charsNoSpace, 'No spaces'], [cjk, 'CJK chars'],
    [words, 'Words'], [lines, 'Lines'], [paragraphs, 'Paragraphs'], [bytes, 'Bytes'],
  ];
  document.getElementById('count-output').innerHTML = stats.map(([n, l]) =>
    '<div class="stat-item"><div class="stat-num">' + n + '</div><div class="stat-label">' + l + '</div></div>').join('');
}

/* ---------- 初始化 ---------- */
document.addEventListener('DOMContentLoaded', initNav);

/* ===== v2 新增工具 ===== */

/* 哈希 */
async function hashCompute() {
  const text = document.getElementById('hash-input').value;
  const out = document.getElementById('hash-out');
  if (!text) { out.textContent = 'Enter some text'; return; }
  const enc = new TextEncoder().encode(text);
  const results = [];
  results.push('MD5     : ' + (window.md5 ? md5(text) : 'library not loaded'));
  for (const alg of ['SHA-1', 'SHA-256', 'SHA-512']) {
    const buf = await crypto.subtle.digest(alg, enc);
    const hex = [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
    results.push(alg.padEnd(8, ' ') + ': ' + hex);
  }
  out.textContent = results.join('\n');
  out.style.whiteSpace = 'pre-wrap';
}

/* IP 查询 */
async function ipLookup() {
  const out = document.getElementById('ip-out');
  out.textContent = 'Looking up…';
  try {
    const r = await fetch('https://ipapi.co/json/');
    const d = await r.json();
    out.textContent = 'Your IP: ' + d.ip + '\nLocation: ' + (d.country_name || '') + ' ' + (d.region || '') + ' ' + (d.city || '') +
      '\nOrg: ' + (d.org || '未知') + '\nTimezone: ' + (d.timezone || '未知');
  } catch (e) {
    try {
      const r2 = await fetch('https://ip.useragentinfo.com/json');
      const d2 = await r2.json();
      out.textContent = 'Your IP: ' + d2.ip + '\nLocation: ' + d2.province + ' ' + d2.city + ' ' + (d2.isp || '');
    } catch (e2) { out.textContent = '❌ Lookup failed, try again later'; }
  }
  out.style.whiteSpace = 'pre-wrap';
}

/* 进制转换 */
function radixConvert() {
  const from = +document.getElementById('radix-from').value;
  const val = document.getElementById('radix-input').value.trim();
  const out = document.getElementById('radix-out');
  if (!val) { out.textContent = ''; return; }
  const num = parseInt(val, from);
  if (isNaN(num)) { out.textContent = '❌ Not a valid base-' + from + ' number'; return; }
  out.textContent = 'Binary : ' + num.toString(2) + '\nOctal  : ' + num.toString(8) +
    '\nDecimal: ' + num.toString(10) + '\nHex    : ' + num.toString(16).toUpperCase();
  out.style.whiteSpace = 'pre-wrap';
}

/* 单位换算 */
const UNITS = {
  temp: [['摄氏度 (°C)', 1, 0], ['华氏度 (°F)', 5/9, -32], ['开尔文 (K)', 1, -273.15]],
  length: [['毫米 (mm)', 1], ['厘米 (cm)', 10], ['米 (m)', 1000], ['千米 (km)', 1e6], ['英寸 (in)', 25.4], ['英尺 (ft)', 304.8], ['英里 (mi)', 1.609e6]],
  weight: [['毫克 (mg)', 1], ['克 (g)', 1000], ['千克 (kg)', 1e6], ['吨 (t)', 1e9], ['盎司 (oz)', 28349.5], ['磅 (lb)', 453592]],
  area: [['平方厘米 (cm²)', 1], ['平方米 (m²)', 1e4], ['平方千米 (km²)', 1e10], ['公顷 (ha)', 1e8], ['英亩 (acre)', 4.047e7]]
};
function unitChangeCat() {
  const cat = document.getElementById('unit-cat').value;
  const list = UNITS[cat];
  const from = document.getElementById('unit-from');
  const to = document.getElementById('unit-to');
  from.innerHTML = list.map((u, i) => '<option value="' + i + '">' + u[0] + '</option>').join('');
  to.innerHTML = from.innerHTML;
  from.selectedIndex = 0; to.selectedIndex = Math.min(1, list.length - 1);
  unitConvert();
}
function unitConvert() {
  const cat = document.getElementById('unit-cat').value;
  const list = UNITS[cat];
  const v = parseFloat(document.getElementById('unit-val').value);
  const out = document.getElementById('unit-out');
  if (isNaN(v)) { out.textContent = ''; return; }
  const f = list[+document.getElementById('unit-from').value];
  const t = list[+document.getElementById('unit-to').value];
  if (cat === 'temp') {
    // 先换算回摄氏度再转到目标
    let c = f[2] === 0 ? v : (v + f[2]) * f[1];
    let result = t[2] === 0 ? c : c / t[1] - t[2];
    out.textContent = v + ' ' + f[0] + ' = ' + +result.toFixed(4) + ' ' + t[0];
  } else {
    const base = v * f[1];
    out.textContent = v + ' ' + f[0] + ' = ' + +(base / t[1]).toPrecision(8) + ' ' + t[0];
  }
}
document.addEventListener('DOMContentLoaded', unitChangeCat);

/* 大小写 */
function caseDo(mode) {
  const text = document.getElementById('case-input').value;
  let r = text;
  if (mode === 'upper') r = text.toUpperCase();
  else if (mode === 'lower') r = text.toLowerCase();
  else if (mode === 'cap') r = text.toLowerCase().replace(/(^|\s+)([a-z])/g, (m, a, b) => a + b.toUpperCase());
  else if (mode === 'camel') r = text.toLowerCase().replace(/[^a-zA-Z0-9]+(.)?/g, (m, c) => c ? c.toUpperCase() : '');
  else if (mode === 'snake') r = text.replace(/([a-z])([A-Z])/g, '$1_$2').replace(/[\s-]+/g, '_').toLowerCase();
  document.getElementById('case-output').value = r;
}

/* 文本排序 */
function tsort(mode) {
  const raw = document.getElementById('tsort-input').value;
  let lines = raw.split('\n');
  if (mode === 'dedup') lines = [...new Set(lines)];
  else if (mode === 'asc') lines.sort((a, b) => a.localeCompare(b, 'zh'));
  else if (mode === 'desc') lines.sort((a, b) => b.localeCompare(a, 'zh'));
  else if (mode === 'len') lines.sort((a, b) => a.length - b.length);
  else if (mode === 'trim') lines = lines.filter(l => l.trim());
  else if (mode === 'num') lines = lines.map((l, i) => (i + 1) + '. ' + l);
  else if (mode === 'rev') lines.reverse();
  document.getElementById('tsort-output').value = lines.join('\n');
}

/* CSV → JSON */
function csvToJson() {
  const text = document.getElementById('csv-input').value.trim();
  const sep = document.getElementById('csv-sep').value;
  const out = document.getElementById('csv-output');
  if (!text) { out.textContent = 'Enter CSV content'; return; }
  const lines = text.split(/\r?\n/).filter(l => l.trim());
  const parseLine = l => {
    const cells = [];
    let cur = '', inQ = false;
    for (const ch of l) {
      if (ch === '"' && (inQ || cur === '' || true)) { inQ = !inQ; continue; }
      if (ch === sep && !inQ) { cells.push(cur); cur = ''; } else cur += ch;
    }
    cells.push(cur);
    return cells.map(c => c.trim());
  };
  const header = parseLine(lines[0]);
  const data = lines.slice(1).map(l => {
    const cells = parseLine(l);
    const obj = {};
    header.forEach((h, i) => obj[h] = isNaN(+cells[i]) || cells[i] === '' ? cells[i] : +cells[i]);
    return obj;
  });
  out.textContent = JSON.stringify(data, null, 2);
}
function csvCopy() {
  navigator.clipboard.writeText(document.getElementById('csv-output').textContent).then(() => alert('已复制'));
}

/* UUID */
function uuidGen() {
  const n = Math.min(100, Math.max(1, +document.getElementById('uuid-count').value || 5));
  const upper = document.getElementById('uuid-upper').checked;
  const list = [];
  for (let i = 0; i < n; i++) {
    if (crypto.randomUUID) { list.push(crypto.randomUUID()); }
    else {
      const b = crypto.getRandomValues(new Uint8Array(16));
      b[6] = (b[6] & 15) | 64; b[8] = (b[8] & 63) | 128;
      const h = [...b].map(x => x.toString(16).padStart(2, '0')).join('');
      list.push(h.slice(0,8) + '-' + h.slice(8,12) + '-' + h.slice(12,16) + '-' + h.slice(16,20) + '-' + h.slice(20));
    }
  }
  document.getElementById('uuid-output').textContent = (upper ? list.map(u => u.toUpperCase()) : list).join('\n');
}
function uuidCopy() {
  navigator.clipboard.writeText(document.getElementById('uuid-output').textContent).then(() => alert('已复制'));
}

/* JWT 解码 */
function jwtDecode() {
  const token = document.getElementById('jwt-input').value.trim();
  const out = document.getElementById('jwt-output');
  const parts = token.split('.');
  if (parts.length < 2) { out.textContent = '❌ Invalid JWT (expected header.payload.signature)'; return; }
  const dec = s => {
    s = s.replace(/-/g, '+').replace(/_/g, '/');
    while (s.length % 4) s += '=';
    try { return JSON.parse(decodeURIComponent(escape(atob(s)))); } catch (e) { return '❌ Decode failed'; }
  };
  const header = dec(parts[0]), payload = dec(parts[1]);
  let html = 'Header:\n' + JSON.stringify(header, null, 2) + '\n\nPayload:\n' + JSON.stringify(payload, null, 2);
  if (payload && typeof payload.exp === 'number') {
    const exp = new Date(payload.exp * 1000);
    html += '\n\n过期时间：' + exp.toLocaleString('en-US', { hour12: false }) + (exp < new Date() ? ' (EXPIRED ⚠️)' : ' (valid ✅)');
  }
  out.textContent = html;
}
