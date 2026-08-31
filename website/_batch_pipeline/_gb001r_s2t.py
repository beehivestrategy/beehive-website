#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simplified -> Traditional (Taiwan) conversion (OpenCC s2twp + site post-map)."""
import opencc

_CC = opencc.OpenCC('s2twp')

POST = [
    ("智慧體", "智慧體"),
    ("引數", "參數"),
    ("投資回報率", "投資報酬率"),
    ("回報率", "報酬率"),
    ("投資回報", "投資報酬"),
    ("文檔", "文件"),
    ("調度", "排程"),
    ("審計", "稽核"),
    ("算法", "演算法"),
    ("缺省", "預設"),
    ("信息", "資訊"),
    ("性能", "效能"),
    ("矢量", "向量"),
    ("服務器", "伺服器"),
    ("視頻", "影片"),
    ("內存", "記憶體"),
    ("芯片", "晶片"),
    ("項目", "專案"),
    ("運營", "營運"),
    ("網絡", "網路"),
    ("操作系統", "作業系統"),
    ("自定義", "自訂"),
    ("隊列", "佇列"),
    ("通過", "透過"),
    ("軟件", "軟體"),
    ("硬件", "硬體"),
    ("數據", "資料"),
    ("界面", "介面"),
    ("數字化", "數位化"),
    ("數字轉型", "數位轉型"),
    ("數字", "數位"),
    ("在哪裏", "在哪裡"),
    ("哪裏", "哪裡"),
]


def s2tw(s):
    out = _CC.convert(s)
    for a, b in POST:
        out = out.replace(a, b)
    return out


def spec_s2tw(spec):
    """Convert a zh-CN spec dict into a zh-TW spec dict."""
    out = {}
    if "replace" in spec:
        out["replace"] = [(s2tw(a), s2tw(b)) for a, b in spec["replace"]]
    if "h2fix" in spec:
        out["h2fix"] = {k: s2tw(v) for k, v in spec["h2fix"].items()}
    if "sections" in spec:
        out["sections"] = [(s[0], s2tw(s[1]), s2tw(s[2])) + tuple(s2tw(x) for x in s[3:])
                           for s in spec["sections"]]
    if "faq" in spec:
        out["faq"] = [(s2tw(q), s2tw(a)) for q, a in spec["faq"]]
    if "excerpts" in spec:
        out["excerpts"] = [s2tw(x) for x in spec["excerpts"]]
    return out
