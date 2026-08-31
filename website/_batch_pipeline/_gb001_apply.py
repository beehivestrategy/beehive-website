#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply a standardisation spec to one slug across en / zh-CN / zh-TW.

spec = {
  "renames": {h2_id: new_title_text},          # optional
  "sections": [(h2_id, h2_title, inner_html)],# optional
  "faq": [(q, a), ...],                        # required
  "excerpts": ["...", "..."],                  # optional
}
"""
import sys, os, re
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb001_lib as L


def apply(slug, lang, spec, do_sections=True, do_faq=True):
    h = L.read(slug, lang)
    before = L.metric(h, lang)
    notes = []

    if spec.get("lead"):
        h = L.replace_lead(h, spec["lead"])
        notes.append("lead")

    if spec.get("replace"):
        h = L.replace_section_bodies(h, spec["replace"])
        notes.append(f"replaced:{len(spec['replace'])}")

    for hid, new in spec.get("renames", {}).items():
        h, n = L.retitle_h2(h, hid, new)
        if n:
            notes.append(f"renamed:{hid}")

    if do_sections and spec.get("sections"):
        h = L.insert_sections(h, spec["sections"])
        notes.append(f"+{len(spec['sections'])}sections")

    if do_faq and spec.get("faq"):
        h, added = L.replace_or_add_faq(h, spec["faq"], lang)
        notes.append("faq_added" if added else "faq_replaced")
        h = L.put_jsonld_after_faq(h, spec["faq"])
        notes.append("ld")

    if spec.get("excerpts"):
        h = L.fill_excerpts(h, spec["excerpts"])

    h, nrec = L.fix_recommended(h, lang)
    if nrec:
        notes.append(f"rechref:{nrec}")

    h, ncta = L.ensure_cta(h, lang)
    if ncta:
        notes.append("cta_phrase")

    L.write(slug, lang, h)
    after = L.metric(h, lang)
    return before, after, notes


def report(slug, en, zhcn, zhtw):
    out = [slug]
    for lang, spec in (("en", en), ("zh-CN", zhcn), ("zh-TW", zhtw)):
        b, a, notes = apply(slug, lang, spec,
                            do_sections=bool(spec.get("sections")),
                            do_faq=bool(spec.get("faq")))
        out.append(f"  {lang}: {b}->{a}  [{', '.join(notes)}]")
    print("\n".join(out))
