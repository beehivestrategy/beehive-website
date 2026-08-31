#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardrail checker: head, footer, share markup, ?v=20260826 links, root-relative links."""
import sys, os, re
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb001_lib as L

ROOT = L.ROOT
BK = os.path.join(ROOT, "_batch_pipeline/_backup_gb001run")
SLUGS = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]
PREF = {"en": "blog_articles", "zh-CN": "zh-cn_blog_articles", "zh-TW": "zh-tw_blog_articles"}


def region(h, tag):
    if tag == "head":
        m = re.search(r'<head[^>]*>(.*?)</head>', h, re.S)
        return m.group(1) if m else ""
    if tag == "footer":
        i = h.rfind('<footer')
        return h[i:] if i >= 0 else ""
    return ""


def shares(h):
    return re.findall(r'<[^>]*(?:share-linkedin|share-x|share-copy|share-wechat|share-btn)[^>]*>', h)


def links(h):
    return sorted(set(re.findall(r'(?:href|src)="((?:/|https://www\.beehivestrategy\.com)[^"]*)"', h)))


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


bad = 0
for s in SLUGS:
    for lang in ("en", "zh-CN", "zh-TW"):
        cur = L.read(s, lang)
        old = open(os.path.join(BK, f"{PREF[lang]}__{s}.html"), encoding="utf-8").read()
        probs = []
        if norm(region(cur, "head")) != norm(region(old, "head")):
            probs.append("HEAD CHANGED")
        if norm(region(cur, "footer")) != norm(region(old, "footer")):
            probs.append("FOOTER CHANGED")
        if shares(cur) != shares(old):
            probs.append("SHARE MARKUP CHANGED")
        for f in (cur, old):
            if '?v=20260826' not in f:
                probs.append("MISSING v=20260826")
        ol, cl = links(old), links(cur)
        removed = [x for x in ol if x not in cl]
        if removed:
            probs.append("LINKS REMOVED: " + ",".join(removed[:4]))
        # div balance inside article
        b = L.body_of(cur)
        if len(re.findall(r'<div\b', b)) != len(re.findall(r'</div>', b)):
            probs.append("DIV UNBALANCED")
        if '<section class="faq-section"' not in cur:
            probs.append("NO FAQ SECTION")
        if probs:
            bad += 1
            print(f"FAIL {lang} {s}: " + " | ".join(probs))
print("GUARDRAIL ISSUES:", bad)
