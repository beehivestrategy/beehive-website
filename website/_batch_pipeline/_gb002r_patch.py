#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch pass: CTA href/phrase fixes + H2 retitles for batches 2-3."""
import re
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb002r_lib as L
import _gb002r_d1 as D1
import _gb002r_d2 as D2
import _gb002r_d3 as D3
import _gb002r_apply as A

SLUGS = [l.strip() for l in open('/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/gap_batches/gbatch_002.txt') if l.strip()]

CTAHREF = {"EN": "/contact", "zh-CN": "/zh-cn/contact", "zh-TW": "/zh-tw/contact"}
CTATXT = {"EN": "Book a Demo", "zh-CN": "预约演示", "zh-TW": "預約示範"}

# ---- 1. CTA fixes -------------------------------------------------------
n = 0
for slug in SLUGS:
    for lang, pat in L.LANGS:
        rel = pat % slug
        h = L.read(rel)
        o = h
        def rep(m):
            return '<a href="%s" class="article-cta-btn">%s</a>' % (CTAHREF[lang], CTATXT[lang])
        h = re.sub(r'<a href="[^"]*" class="article-cta-btn">[^<]*</a>', rep, h)
        if h != o:
            L.guard(rel, o, h)
            L.write(rel, h)
            n += 1
print("cta fixed:", n)

# ---- 2. H2 retitles: zh-CN / zh-TW for batches 2-3 ----------------------
MAPS = {}
for D in (D1, D2, D3):
    for slug, d in D.DATA.items():
        if d.get("ZH_CN_H2"):
            MAPS.setdefault(slug, {})["zh-CN"] = d["ZH_CN_H2"]
        if d.get("ZH_TW_H2"):
            MAPS.setdefault(slug, {})["zh-TW"] = [(o, A.twfix(x)) for o, x in d["ZH_TW_H2"]]

# additional EN fixes for headings that remain non-question form
EXTRA_EN = {
    "retail-ai-personalization-early-2025": [
        ("From Recommendations to Conversations: What Changes?",
         "What Changes When Recommendations Become Conversations?"),
    ],
    "design-ai-augmented-dashboards": [
        ("Conversational Interaction and Proactive Insights",
         "How Should Conversational Interaction and Proactive Insights Work?"),
    ],
    "hidden-cost-dashboard-sprawl-enterprises": [
        ("The Hidden Costs: Conflicting Numbers and Eroded Trust",
         "What Are the Hidden Costs of Conflicting Numbers?"),
        ("The Migration Path from Dashboards to Conversational BI",
         "What Does the Migration Path Look Like?"),
    ],
    "anatomy-of-analytics-failure-metric-drift-and-trust-gaps": [
        ("Failure 1: What Is Metric Drift?", "What Is Metric Drift?"),
        ("Failure 2: How Does Definition Ambiguity Hurt?", "How Does Definition Ambiguity Hurt Analytics?"),
        ("Failure 3: How Does the Trust Gap Form?", "How Does the Trust Gap Form?"),
        ("What Is the Solution: Governed Metrics as Products?", "What Is the Solution: Governed Metrics as Products?"),
    ],
}
for slug, pairs in EXTRA_EN.items():
    MAPS.setdefault(slug, {})["EN"] = pairs

m = 0
missing = []
for slug, per in MAPS.items():
    for lang, pairs in per.items():
        rel = dict(L.LANGS)[lang] % slug
        h = L.read(rel)
        o = h
        live = []
        for old, new in pairs:
            if L._find_h2(h, old) is not None:
                live.append((old, new))
            elif old != new:
                missing.append("%s [%s] %r" % (slug, lang, old))
        if live:
            h = L.retitle_h2(h, live)
        if h != o:
            L.guard(rel, o, h)
            L.write(rel, h)
            m += 1
print("h2 retitled files:", m)
for x in missing:
    print("  already-applied or absent:", x)
