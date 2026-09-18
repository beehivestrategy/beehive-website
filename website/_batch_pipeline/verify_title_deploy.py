#!/usr/bin/env python3
"""Post-deploy verification for title fix + canonical bundle (2026-09-02).
Usage: python3 verify_title_deploy.py
Checks PROD URLs with cache-busters: new titles live? canonical live?
"""
import json
import os
import random
import urllib.request

BP = os.path.dirname(os.path.abspath(__file__))
PROPOSAL = os.path.join(BP, "title_fixes_proposal.json")
BASE = "https://www.beehivestrategy.com"
BUSTER = f"?x={random.randint(100000, 999999)}"

with open(PROPOSAL, encoding="utf-8") as f:
    proposal = json.load(f)

fixes = proposal["fixes"] if isinstance(proposal, dict) and "fixes" in proposal else proposal
# sample: 8 cn + 4 tw
cn = [f for f in fixes if f.get("new_cn")]
tw = [f for f in fixes if f.get("new_tw") and not f.get("new_cn")]
sample = cn[:8] + tw[:4]

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
ok = bad = 0
for item in sample:
    slug = item["slug"]
    if item.get("new_cn"):
        url = f"{BASE}/zh-cn/blog/articles/{slug}.html"
        expect = item["new_cn"]
    else:
        url = f"{BASE}/zh-tw/blog/articles/{slug}.html"
        expect = item["new_tw"]
    try:
        req = urllib.request.Request(url + BUSTER, headers=UA)
        html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
        live = expect in html
        canon_ok = 'rel="canonical"' in html
        print(("✅" if live else "❌"), slug, "" if live else f"(expect: {expect[:30]})")
        ok += 1 if live else 0
        bad += 0 if live else 1
    except Exception as e:
        print("⚠️", slug, "fetch error:", e)
        bad += 1

# canonical check on one dated variant
cvar = f"{BASE}/blog/articles/ai-consulting-delivery-models-20260126.html"
try:
    req = urllib.request.Request(cvar + BUSTER, headers=UA)
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    good = "/blog/articles/ai-consulting-delivery-models\"" in html
    print(("✅" if good else "❌"), "canonical on dated variant")
except Exception as e:
    print("⚠️ canonical check fetch error:", e)

print(f"\nSummary: {ok} live / {bad} failed of {len(sample) + 1} checks (PROD, cache-busted)")
