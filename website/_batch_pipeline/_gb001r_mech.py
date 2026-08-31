#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mechanical pass: FAQ <h3> wrapping, body FAQPage JSON-LD, CTA demo phrase.
Touches only the article body. Verifies hard guardrails before writing."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gb001r_lib as L

SLUGS = [l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
         "gap_batches/gbatch_001.txt")) if l.strip()]
SKIP = {"how-to-build-a-data-first-culture-in-traditional-enterprises"}  # already compliant

report = []
for s in SLUGS:
    if s in SKIP:
        report.append((s, "SKIPPED compliant")); continue
    for sub, lang, floor in L.LANGS:
        before = L.read(sub, s)
        h = before
        # 1. normalise FAQ markup to the canonical <h3>-question pattern
        fb = L.FAQ_RE.search(h)
        items = L.faq_items(fb.group(0)) if fb else []
        if len(items) >= 3:
            nh = L.replace_faq(h, items, lang)
            if nh: h = nh; faqst = "normalised"
            else: faqst = "faq-replace-failed"
        else:
            h, n = L.ensure_faq_h3(h)
            faqst = f"wrapped({len(items)})"
        h, ldst = L.sync_jsonld(h, lang)
        h, ctast = L.ensure_cta(h, lang)
        errs = L.guard(before, h, sub, s)
        if errs:
            report.append((s, f"{lang} GUARD FAIL {errs}")); continue
        if h != before:
            L.write(sub, s, h)
        report.append((s, f"{lang} faq={faqst} ld={ldst} cta={ctast}"))

for s, r in report:
    print(f"{s[:48]:48} {r}")
