#!/usr/bin/env python3
"""Insert an HTML fragment into an article body immediately BEFORE the FAQ
section (so the new prose counts toward both pre-FAQ and total measures).

Usage: _insert.py <html_file> <fragment_file>

Idempotent guard: refuses to insert if the fragment's first h2 id already
exists in the file.
"""
import re, io, sys

ART = re.compile(r'(<article\b[^>]*id="article-content"[^>]*>)(.*?)(</article>)', re.S)
FAQ = re.compile(r'<section\b[^>]*class="[^"]*faq-section[^"]*"[^>]*>', re.S)

path, frag_path = sys.argv[1], sys.argv[2]
frag = io.open(frag_path, encoding="utf-8").read().strip()
s = io.open(path, encoding="utf-8").read()

hid = re.search(r'<h2 id="([^"]+)"', frag)
if hid and f'id="{hid.group(1)}"' in s:
    print(f"SKIP (section exists) {path}")
    sys.exit(0)

m = ART.search(s)
if not m:
    print(f"NOART {path}")
    sys.exit(1)
body = m.group(2)
f = FAQ.search(body)
if f:
    newbody = body[: f.start()].rstrip() + "\n" + frag + "\n" + body[f.start():]
else:
    newbody = body.rstrip() + "\n" + frag + "\n"
io.open(path, "w", encoding="utf-8").write(s[: m.start(2)] + newbody + s[m.end(2):])
print(f"INSERTED {path}")
