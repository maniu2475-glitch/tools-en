# -*- coding: utf-8 -*-
import io
p = "gen_batch_20261026.py"
s = io.open(p, encoding="utf-8").read()
# fix JS \n escapes that Python interpreted as real newlines inside single-quoted JS strings
fixes = [
    ("else if(c=='\n')", "else if(c=='\\\\n')"),
    ("}else if(c!='\r')", "}else if(c!='\\\\r')"),
    (").join(dst);}).join('\n');", ").join(dst);}).join('\\\\n');"),
]
for a, b in fixes:
    if a in s:
        s = s.replace(a, b)
        print("fixed:", a[:30])
io.open(p, "w", encoding="utf-8").write(s)
