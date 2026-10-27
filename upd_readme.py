# -*- coding: utf-8 -*-
import io
s = io.open("README.md", encoding="utf-8").read()
assert "batch 2" not in s
s = s.replace("115 free online tools", "120 free online tools", 1)
s = s.replace("Newly added tools (2026-10-26 batch):",
              "Newly added tools (2026-10-26, batch 1):", 1)
add = """Newly added tools (2026-10-26, batch 2):

- [Tally Counter](https://maniu2475-glitch.github.io/tools-en/tally-counter.html) — click/space counting with step, undo and localStorage
- [Hex to ASCII Converter](https://maniu2475-glitch.github.io/tools-en/hex-to-ascii.html) — hex bytes to text and back, 0x/spaces tolerated
- [CSV to TSV Converter](https://maniu2475-glitch.github.io/tools-en/csv-to-tsv.html) — proper quoted-field CSV parsing, bidirectional
- [Word to Number Converter](https://maniu2475-glitch.github.io/tools-en/word-to-number.html) — English number words to digits, up to trillions
- [Decimal to Fraction Converter](https://maniu2475-glitch.github.io/tools-en/decimal-to-fraction.html) — fully simplified fractions via GCD

"""
s = s.replace("Newly added tools (2026-10-26, batch 1):",
              add + "Newly added tools (2026-10-26, batch 1):", 1)
io.open("README.md", "w", encoding="utf-8").write(s)
print("README updated OK")
