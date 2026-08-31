#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run content modules: each module exposes SPECS = {slug: {'en':…, 'zh-cn':…}}."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gb001r_apply as A

for mod in (sys.argv[1:] or ["_gb001r_c01"]):
    m = __import__(mod)
    for slug, spec in m.SPECS.items():
        print("==", slug)
        A.report(slug, spec)
