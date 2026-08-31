#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply a per-slug spec to all three language files, in place."""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001x_lib import (read, write, rename_h2, rename_h2_text, remove_h2_section,
                         replace_faq, ensure_faq_section, regen_ld, section_html,
                         insert_prose, add_toc_before, add_toc_entries, fill_excerpts,
                         guard_ok, metrics, extract_faq, s2tw, LANGS, prose_anchor_id)


def _blocks(bs):
    return bs if isinstance(bs, list) else [bs]


def apply_spec(slug, specs, verbose=True):
    """specs: {'EN': {...}, 'zh-CN': {...}, 'zh-TW': {...}}"""
    report = {}
    for lang, d in LANGS:
        sp = specs.get(lang)
        if not sp:
            continue
        before = read(slug, d)
        raw = before
        notes = []

        for hid in sp.get("drop", []):
            raw, ok = remove_h2_section(raw, hid)
            if ok:
                notes.append("drop:" + hid)

        for hid, t in sp.get("rename", {}).items():
            raw, ok = rename_h2(raw, hid, t)
            notes.append(("ren:" + hid + "=" + ("ok" if ok else "MISS")))

        for old, new in sp.get("rename_text", {}).items():
            raw, ok = rename_h2_text(raw, old, new)
            notes.append(("renT:" + old[:14] + "=" + ("ok" if ok else "MISS")))

        for item in sp.get("new", []):
            hid, title, blocks = item[0], item[1], item[2]
            if re.search(r'<h2 id="' + re.escape(hid) + r'"', raw):
                notes.append("skip:" + hid)
                continue
            before_hid = item[3] if len(item) > 3 else None
            html = section_html(hid, title, _blocks(blocks))
            anchor = before_hid or prose_anchor_id(raw)
            raw = insert_prose(raw, html, before_hid)
            if anchor:
                raw = add_toc_before(raw, hid, title, anchor)
            else:
                raw = add_toc_entries(raw, hid, title)
            notes.append("new:" + hid)

        if "faq" in sp:
            raw, ok = ensure_faq_section(raw, sp["faq"], lang)
            if not ok:
                raw, ok = replace_faq(raw, sp["faq"])
            notes.append("faq=" + str(ok))

        if "excerpts" in sp:
            raw, n = fill_excerpts(raw, sp["excerpts"])
            notes.append("exc=%d" % n)

        raw, ld = regen_ld(raw, lang)

        probs = guard_ok(raw, before)
        if probs:
            report[lang] = ("GUARD-FAIL", probs)
            continue
        if raw != before:
            write(slug, d, raw)
        m = metrics(raw, lang)
        report[lang] = (m, ld, notes)
        if verbose:
            print("  [%s] words=%d cjk=%d ld=%s %s"
                  % (lang, m["words"], m["cjk"], ld, " ".join(notes)))
    return report


def zh_from_cn(cn_spec):
    """Derive a zh-TW spec from a zh-CN spec (headings + prose + FAQ)."""
    out = {}
    for k, v in cn_spec.items():
        if k == "rename":
            out[k] = {i: s2tw(t) for i, t in v.items()}
        elif k == "rename_text":
            out[k] = {s2tw(o): s2tw(t) for o, t in v.items()}
        elif k == "new":
            out[k] = [(i, s2tw(t), [s2tw(b) for b in _blocks(bs)]) + tuple(vv[3:])
                      for (i, t, bs, *vv) in v]
        elif k == "faq":
            out[k] = [(s2tw(q), s2tw(a)) for q, a in v]
        elif k == "excerpts":
            out[k] = [s2tw(x) for x in v]
        else:
            out[k] = v
    return out
