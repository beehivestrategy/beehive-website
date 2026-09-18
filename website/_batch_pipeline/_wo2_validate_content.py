# -*- coding: utf-8 -*-
import json, re, sys, os
sys.path.insert(0, "_batch_pipeline")
from _wo2_faq import FAQ, HEADS, CARDS

scan = json.load(open("_batch_pipeline/_wo2_scan.json", encoding="utf-8"))
CJK = re.compile(r"[\u4e00-\u9fff]")
err = 0

print("== FAQ 校验 ==")
for fn, qas in FAQ.items():
    key = "zh-cn/blog/articles/" + fn
    v = scan[key]
    h2 = {h["txt"] for h in v["h"] if h["tag"] == "h2"}
    if len(qas) != 4:
        print(f"  [ERR] {fn} 不是 4 组"); err += 1
    qs = set()
    for i, (q, a) in enumerate(qas, 1):
        n = len(CJK.findall(a))
        if not (60 <= n <= 110):
            print(f"  [ERR] {fn} A{i} 汉字数={n} 超出 60-110"); err += 1
        if q in qs:
            print(f"  [ERR] {fn} Q{i} 重复"); err += 1
        qs.add(q)
        if q in h2:
            print(f"  [ERR] {fn} Q{i} 与 H2 重名: {q}"); err += 1
        if len(q) > 34:
            print(f"  [WARN] {fn} Q{i} 偏长({len(q)}字)")
    # 数字核查：答案中出现的百分数必须原文存在
    s = open(key, encoding="utf-8").read()
    body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", s, flags=re.S)))
    for i, (q, a) in enumerate(qas, 1):
        for p in set(re.findall(r"\d+(?:\.\d+)?%", a)):
            if p not in body:
                print(f"  [ERR] {fn} A{i} 引用了原文不存在的百分数 {p}"); err += 1
        for m in re.findall(r"\d+(?:\.\d+)?(?:倍|个月)", a):
            if m not in body:
                print(f"  [ERR] {fn} A{i} 引用了原文不存在的数据 {m}"); err += 1

print("\n== 标题译文校验 ==")
for fn, items in HEADS.items():
    key = "zh-cn/blog/articles/" + fn
    v = scan[key]
    txts = {h["txt"] for h in v["h"]}
    new = set()
    for en, zh, hid in items:
        if len(zh) > 20:
            print(f"  [ERR] {fn} 译文超 20 字({len(zh)}): {zh}"); err += 1
        if not CJK.search(zh):
            print(f"  [ERR] {fn} 译文无中文: {zh}"); err += 1
        if zh in txts and zh != en:
            print(f"  [ERR] {fn} 译文与文件内已有标题冲突: {zh}"); err += 1
        if zh in new:
            print(f"  [ERR] {fn} 译文组内重复: {zh}"); err += 1
        new.add(zh)
        # 确认英文标题确实存在且带该 id
        if not re.search(r'<h2[^>]*id="' + re.escape(hid) + r'"[^>]*>' + re.escape(en) + r'</h2>', open(key, encoding="utf-8").read()):
            print(f"  [ERR] {fn} 未找到匹配的 h2: id={hid} 原文={en}"); err += 1

for en, zh in CARDS:
    if len(zh) > 20:
        print(f"  [ERR] 卡片译文超 20 字: {zh}"); err += 1

print(f"\n错误数: {err}")
