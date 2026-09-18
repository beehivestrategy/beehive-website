#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pre-flight: check the 78 proposed new titles for collisions against
(a) each other, (b) all existing titles in zh-cn + zh-tw (audit norm rules).
Read-only.
"""
import json, os, re, glob, unicodedata, io

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(BASE)

def clean(t):
    t = re.sub(r"\s*\|\s*Beehive.*$", "", t)
    t = re.sub(r"原创$", "", t.strip())
    return t.strip()

def norm(t):
    t = unicodedata.normalize("NFKC", t).lower()
    return re.sub(r"[\s\W_]+", "", t, flags=re.UNICODE)

# existing normalized titles per lang
def scan(lang_dir):
    out = {}
    for f in glob.glob(os.path.join(SITE, lang_dir, "blog", "articles", "*.html")):
        with io.open(f, encoding="utf-8", errors="ignore") as fh:
            m = re.search(r"<title>(.*?)</title>", fh.read(4000), re.S)
        if m:
            out[os.path.basename(f)[:-5]] = norm(clean(m.group(1)))
    return out

existing = {"cn": scan("zh-cn"), "tw": scan("zh-tw")}

with open(os.path.join(BASE, "title_fixes_proposal.json"), encoding="utf-8") as f:
    prop = json.load(f)

problems = []
for lang, key in (("cn", "new_cn"), ("tw", "new_tw")):
    # (a) self-collision among proposals
    seen = {}
    for e in prop:
        n = norm(e[key])
        if n in seen:
            problems.append("SELF-DUP [%s] %s <-> %s : %s" % (lang, seen[n], e["slug"], e[key]))
        else:
            seen[n] = e["slug"]
    # (b) collision vs existing pages NOT being fixed
    fixed_slugs = {e["slug"] for e in prop}
    existing_norm = {}
    for slug, n in existing[lang].items():
        if slug not in fixed_slugs:
            existing_norm.setdefault(n, []).append(slug)
    for e in prop:
        n = norm(e[key])
        if n in existing_norm:
            problems.append("COLLIDE [%s] %s -> '%s' == existing: %s" % (
                lang, e["slug"], e[key], ", ".join(existing_norm[n][:3])))

# (c) length check (zh titles: soft warn > 40 chars incl. suffix)
warns = []
for e in prop:
    L = len(e["new_cn"])
    if L > 40:
        warns.append("LONG cn (%d) %s : %s" % (L, e["slug"], e["new_cn"]))

print("proposals checked: %d" % len(prop))
print("collisions: %d" % len(problems))
for p in problems[:20]:
    print("  " + p)
print("length warns: %d" % len(warns))
for w in warns[:10]:
    print("  " + w)
