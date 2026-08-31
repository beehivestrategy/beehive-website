#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply a content batch (zh-CN derived by t2s, zh-TW term-fixed)."""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb002r_lib as L

TW_FIX = [("上下文視窗", "上下文窗口"), ("視窗", "窗口"), ("匯入", "導入"),
          ("儀錶板", "儀表板"), ("資料庫", "資料庫")]


def twfix(s):
    if not s:
        return s
    for a, b in TW_FIX:
        s = s.replace(a, b)
    return s


def to_cn(s):
    import opencc
    return opencc.OpenCC('t2s').convert(s)


def run(DATA):
    for slug, d in DATA.items():
        trad_faq = d.get("ZH_FAQ_TRAD")
        trad_add = d.get("ZH_ADD_TRAD")
        cn, tw = d.get("zh-CN", {}), d.get("zh-TW", {})
        data = {"EN": d["EN"]}
        if trad_faq or cn:
            faq = trad_faq or cn.get("faq")
            h2 = cn.get("h2")
            add = to_cn(trad_add) if trad_add else cn.get("add")
            data["zh-CN"] = {"h2": h2,
                             "add": add,
                             "faq": [(to_cn(q), to_cn(a)) for q, a in faq] if faq else None}
        if trad_faq or tw:
            faq = trad_faq or tw.get("faq")
            h2 = tw.get("h2")
            data["zh-TW"] = {"h2": [(o, twfix(n)) for o, n in h2] if h2 else None,
                             "add": twfix(trad_add) if trad_add else tw.get("add"),
                             "faq": [(twfix(q), twfix(a)) for q, a in faq] if faq else None}
        log = L.apply_slug(slug, data)
        print(slug, log)
