# -*- coding: utf-8 -*-
import io, re

NEW = [("tally-counter.html", "Tally Counter"),
       ("hex-to-ascii.html", "Hex to ASCII Converter"),
       ("csv-to-tsv.html", "CSV to TSV Converter"),
       ("word-to-number.html", "Word to Number Converter"),
       ("decimal-to-fraction.html", "Decimal to Fraction Converter")]
BASE = "https://maniu2475-glitch.github.io/tools-en/"

# --- index.html: append to footer-links line ---
p = "index.html"
s = io.open(p, encoding="utf-8").read()
add = "".join(' · <a href="%s">%s</a>' % (f, n) for f, n in NEW)
lines = s.split("\n")
done = False
for i, l in enumerate(lines):
    if "footer-links" in l and "json-formatter.html" in l:
        assert "tally-counter" not in l, "already added"
        # insert before </p> at end of that line
        j = l.rfind("</p>")
        lines[i] = l[:j] + add + l[j:]
        done = True
        break
assert done, "footer line not found"
io.open(p, "w", encoding="utf-8").write("\n".join(lines))
print("index.html updated")

# --- all-tools.html ---
p = "all-tools.html"
s = io.open(p, encoding="utf-8").read()
if "tally-counter" not in s:
    m = re.search(r'</ol>\s*</body>', s)
    if not m:
        m = re.search(r'</ul>\s*</body>', s)
    items = "".join('<li><a href="%s">%s</a></li>\n' % (f, n) for f, n in NEW)
    if m:
        s = s[:m.start()] + items + s[m.start():]
    else:
        # fallback: append before </main>
        j = s.rfind("</main>")
        s = s[:j] + "<ul>" + items + "</ul>\n" + s[j:]
    io.open(p, "w", encoding="utf-8").write(s)
    print("all-tools.html updated")
else:
    print("all-tools.html already had them")

# --- sitemap.xml ---
p = "sitemap.xml"
s = io.open(p, encoding="utf-8").read()
if "tally-counter" not in s:
    add_xml = "".join(
        '  <url>\n    <loc>%s%s</loc>\n    <lastmod>2026-10-26</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n' % (BASE, f)
        for f, _ in NEW)
    j = s.rfind("</urlset>")
    s = s[:j] + add_xml + s[j:]
    io.open(p, "w", encoding="utf-8").write(s)
    print("sitemap.xml updated")
else:
    print("sitemap already updated")
