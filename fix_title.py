# -*- coding: utf-8 -*-
import io
p = "gen_batch_20261026.py"
s = io.open(p, encoding="utf-8").read()
bad = 'title="Word to Number Converter - "One" '
if bad in s:
    s = s.replace(bad, 'title="Word to Number Converter - Number Words to Digits",')
    s = s.replace('\u2192 1 (English)",', '')
    io.open(p, "w", encoding="utf-8").write(s)
    print("fixed")
else:
    print("pattern not found; showing line")
    for line in s.split("\n"):
        if "Word to Number" in line:
            print(repr(line))
