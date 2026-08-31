#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove duplicated <h2 id="..."> blocks (and their content) added by repeat runs."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gb001r_lib as L

IDS = set("""why-keyword-search-fails how-embeddings-represent-meaning hybrid-search-default
evaluate-search-quality what-is-a-cross-border-transfer data-residency-vs-data-localization
operationalizing-transfer-mechanisms proving-compliance-to-regulators why-no-single-federal-law
state-laws-setting-the-bar what-regulators-actually-ask-for building-a-compliance-cadence""".split())

def dedupe(html):
    # map id -> list of h2 start offsets
    occ = {}
    for m in re.finditer(r'<h2 id="([^"]+)"', html):
        if m.group(1) in IDS:
            occ.setdefault(m.group(1), []).append(m.start())
    cuts = []
    for hid, starts in occ.items():
        for st in starts[1:]:
            nxt = html.find("<h2", st + 10)
            if nxt < 0: nxt = len(html)
            cuts.append((st, nxt))
    if not cuts: return html, 0
    for st, en in sorted(cuts, reverse=True):
        html = html[:st] + html[en:]
    return html, len(cuts)

def run():
    total = 0
    for s in [l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
              "gap_batches/gbatch_001.txt")) if l.strip()]:
        for sub, lang, floor in L.LANGS:
            before = L.read(sub, s)
            after, n = dedupe(before)
            if not n: continue
            errs = L.guard(before, after, sub, s)
            if errs:
                print("GUARD", s, lang, errs); continue
            L.write(sub, s, after)
            total += n
            print(f"{s[:44]:44} {lang:6} removed {n}")
    print("total removed:", total)

if __name__ == "__main__":
    run()
