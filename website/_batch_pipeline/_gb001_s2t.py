#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simplified -> Traditional (Taiwan) conversion via OpenCC s2twp + site-specific post-map."""
import re
import opencc

_CC = opencc.OpenCC('s2twp')

POST = [
    ("智慧體", "智能體"),
    ("智慧代理", "智能代理"),
    ("引數", "參數"),
    ("投資回報率", "投資報酬率"),
    ("回報率", "報酬率"),
    ("投資回報", "投資報酬"),
    ("連線", "連接"),
    ("文檔", "文件"),
    ("調度", "排程"),
    ("審計", "稽核"),
    ("算法", "演算法"),
    ("缺省", "預設"),
    ("缺省值", "預設值"),
    ("信息", "資訊"),
    ("性能", "效能"),
    ("矢量", "向量"),
    ("空間向量", "空間向量"),
    ("標籤體系", "標籤體系"),
    ("服務器", "伺服器"),
    ("視頻", "影片"),
    ("內存", "記憶體"),
    ("芯片", "晶片"),
    ("項目", "專案"),
    ("運營", "營運"),
    ("網絡", "網路"),
    ("操作系統", "作業系統"),
    ("自定義", "自訂"),
    ("缺省", "預設"),
    ("消息隊列", "訊息佇列"),
    ("隊列", "佇列"),
    ("前端", "前端"),
    ("缺省配置", "預設配置"),
    ("通過", "透過"),
    ("軟件", "軟體"),
    ("硬件", "硬體"),
    ("數據", "資料"),
    ("用戶界面", "使用者介面"),
    ("界面", "介面"),
    ("標註數據", "標註資料"),
    ("大數據", "大數據"),
    ("數字化", "數位化"),
    ("數字轉型", "數位轉型"),
    ("數字", "數位"),
]

def s2tw(s):
    out = _CC.convert(s)
    for a, b in POST:
        out = out.replace(a, b)
    return out


def spec_s2tw(spec):
    """Convert a zh-CN spec dict into a zh-TW spec dict."""
    out = {}
    if "lead" in spec:
        out["lead"] = s2tw(spec["lead"])
    if "replace" in spec:
        out["replace"] = {k: (s2tw(t), s2tw(b)) for k, (t, b) in spec["replace"].items()}
    if "sections" in spec:
        out["sections"] = [(hid, s2tw(t), s2tw(b)) for hid, t, b in spec["sections"]]
    if "faq" in spec:
        out["faq"] = [(s2tw(q), s2tw(a)) for q, a in spec["faq"]]
    if "renames" in spec:
        out["renames"] = {k: s2tw(v) for k, v in spec["renames"].items()}
    if "excerpts" in spec:
        out["excerpts"] = [s2tw(x) for x in spec["excerpts"]]
    return out


def audit_s2tw(spec):
    """Report simplified-only characters / stray ASCII words in a zh-TW spec."""
    import re as _re
    txt = []
    for _, t, b in spec.get("sections", []):
        txt += [t, b]
    for q, a in spec.get("faq", []):
        txt += [q, a]
    txt += [v for v in spec.get("renames", {}).values()]
    txt += spec.get("excerpts", [])
    blob = "\n".join(txt)
    # strip tags/attrs
    plain = _re.sub(r'<[^>]+>', ' ', blob)
    bad = {}
    for ch in plain:
        if '\u4e00' <= ch <= '\u9fff':
            if _CC.convert(ch) != ch:
                bad[ch] = bad.get(ch, 0) + 1
    words = sorted(set(_re.findall(r'[A-Za-z]{3,}', plain)))
    return bad, words
