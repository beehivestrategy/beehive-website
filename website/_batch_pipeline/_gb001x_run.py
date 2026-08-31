#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Driver: apply a spec module's SPECS to every slug it covers, then sync zh-TW."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001x_lib import read, write, metrics, sync_zh_tw, guard_ok, LANGS
from _gb001x_apply import apply_spec


def run(SPECS, slugs=None, do_tw=True):
    for slug, spec in SPECS.items():
        if slugs and slug not in slugs:
            continue
        print("=" * 12, slug)
        print("  BEFORE:", {l: metrics(read(slug, d), l) for l, d in LANGS})
        sp = {k: v for k, v in spec.items() if k != "zh-TW"}
        res = apply_spec(slug, sp)
        for lang, r in res.items():
            if r and r[0] == "GUARD-FAIL":
                print("  !! GUARD FAIL", lang, r[1])
                continue
        if do_tw:
            tw = sync_zh_tw(slug)
            if tw:
                old = read(slug, LANGS[2][1])
                probs = guard_ok(tw, old)
                if probs:
                    print("  !! zh-TW GUARD FAIL", probs)
                else:
                    write(slug, LANGS[2][1], tw)
        print("  AFTER :", {l: metrics(read(slug, d), l) for l, d in LANGS})


if __name__ == "__main__":
    mod = __import__(sys.argv[1])
    slugs = sys.argv[2:] or None
    run(mod.SPECS, slugs)
