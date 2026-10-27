# -*- coding: utf-8 -*-
import io
p = "csv-to-tsv.html"
h = io.open(p, encoding="utf-8").read()
h = h.replace("else if(c=='\n')", "else if(c=='\\n')")
h = h.replace("else if(c!='\n')cur+=c", "else if(c!='\\r')cur+=c")
h = h.replace("/[\",\n]/", '/[",\\n]/')
h = h.replace("}).join('\n');", "}).join('\\n');")
io.open(p, "w", encoding="utf-8").write(h)
print("patched")
