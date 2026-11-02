# -*- coding: utf-8 -*-
"""Register the 2026-11-02 batch into index.html, all-tools.html and sitemap.xml."""
import io, re

NEW = [
    ("sha512-hash-generator.html", "\U0001F510", "SHA-512 Hash Generator", "512-bit SHA-2 digest computed locally"),
    ("html-minifier.html", "\U0001F4C4", "HTML Minifier", "Compress HTML: drop comments and whitespace"),
    ("png-to-jpg.html", "\U0001F5BC\uFE0F", "PNG to JPG Converter", "Convert PNG to JPEG with quality slider"),
]

# ---------- index.html ----------
s = io.open("index.html", encoding="utf-8").read()
add = ""
for slug, icon, title, desc in NEW:
    if 'href="%s"' % slug in s:
        continue
    add += ('        <a class="home-card" href="%s"><div class="hc-icon">%s</div>'
            '<div class="hc-title">%s</div><div class="hc-desc">%s</div></a>\n' % (slug, icon, title, desc))
if add:
    anchor = '        <a class="home-card" href="fahrenheit-to-celsius.html">'
    i = s.find(anchor)
    assert i > 0
    s = s[:i] + add + s[i:]
    s = s.replace('<meta name="description" content="Free online toolbox: ',
                  '<meta name="description" content="Free online toolbox: ', 1)
    io.open("index.html", "w", encoding="utf-8").write(s)
    print("index.html cards+%d" % add.count("home-card"))

# ---------- all-tools.html ----------
try:
    a = io.open("all-tools.html", encoding="utf-8").read()
    adda = ""
    for slug, icon, title, desc in NEW:
        if slug in a:
            continue
        adda += '<li><a href="%s">%s</a> - %s</li>\n' % (slug, title, desc)
    if adda:
        j = a.rfind("</ul>")
        a = a[:j] + adda + a[j:]
        if "</ul>" not in a:
            a = a.replace("</body>", adda + "</body>")
        io.open("all-tools.html", "w", encoding="utf-8").write(a)
        print("all-tools updated")
    else:
        print("all-tools already has entries")
except IOError:
    print("no all-tools.html")

# ---------- sitemap.xml ----------
sm = io.open("sitemap.xml", encoding="utf-8").read()
base = "https://maniu2475-glitch.github.io/tools-en/"
news = ""
for slug, icon, title, desc in NEW:
    url = base + slug
    if url in sm:
        continue
    news += ("  <url><loc>%s</loc><lastmod>2026-11-02</lastmod>"
             "<changefreq>monthly</changefreq><priority>0.8</priority></url>\n" % url)
if news:
    k = sm.rfind("</urlset>")
    sm = sm[:k] + news + sm[k:]
    io.open("sitemap.xml", "w", encoding="utf-8").write(sm)
print("sitemap locs:", sm.count("<loc>"))

# ---------- verification ----------
for slug, _, _, _ in NEW:
    p = io.open(slug, encoding="utf-8").read()
    print(slug, len(p), "h1=%d" % p.count("<h1>"), "canon=%d" % p.count('rel="canonical"'))
