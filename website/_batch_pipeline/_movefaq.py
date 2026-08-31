#!/usr/bin/env python3
"""Move the FAQ section + its adjacent FAQPage JSON-LD to the end of the
<article id="article-content"> body, so page order is
content -> FAQ -> FAQPage JSON-LD (JSON-LD stays immediately after the FAQ
section's closing tag). Idempotent: does nothing if already last.

Usage: _movefaq.py <file> [<file> ...]
"""
import re, io, sys

ART = re.compile(r'(<article\b[^>]*id="article-content"[^>]*>)(.*?)(</article>)', re.S)
BLK = re.compile(
    r'\s*<section\b[^>]*class="[^"]*faq-section[^"]*"[^>]*>.*?</section>'
    r'\s*<script[^>]*application/ld\+json[^>]*>\s*\{.*?"FAQPage".*?</script>',
    re.S,
)

for p in sys.argv[1:]:
    s = io.open(p, encoding="utf-8").read()
    m = ART.search(s)
    if not m:
        print(f"NOART {p}")
        continue
    body = m.group(2)
    b = BLK.search(body)
    if not b:
        print(f"NOBLOCK {p}")
        continue
    if not body[b.end():].strip():
        print(f"SKIP (already last) {p}")
        continue
    rest = body[: b.start()] + body[b.end():]
    newbody = rest.rstrip() + "\n" + b.group(0).strip() + "\n"
    io.open(p, "w", encoding="utf-8").write(s[: m.start(2)] + newbody + s[m.end(2):])
    print(f"MOVED {p}")
