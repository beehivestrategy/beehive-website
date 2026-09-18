#!/usr/bin/env python3
"""清点全部低质量 zh 标题：无信息机翻 / 半翻译（EN 占比高）/ 超短"""
import os, re, json, unicodedata

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
DIRS = {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)

def clean(t):
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s*\|\s*Beehive.*$", "", t)
    t = re.sub(r"\s*原创\s*$", "", t)
    return t

def cjk_ratio(t):
    if not t: return 0
    cjk = sum(1 for c in t if '\u4e00' <= c <= '\u9fff')
    return cjk / len(t.replace(" ", ""))

bad = []
for slug_file in sorted(os.listdir(os.path.join(ROOT, DIRS["cn"]))):
    if not slug_file.endswith(".html"): continue
    slug = slug_file[:-5]
    row = {"slug": slug}
    for lang, d in DIRS.items():
        p = os.path.join(ROOT, d, slug_file)
        if not os.path.exists(p):
            row[lang] = None; continue
        m = TITLE_RE.search(open(p, encoding="utf-8", errors="ignore").read())
        row[lang] = clean(m.group(1)) if m else ""
    tcn = row.get("cn") or ""
    # 低信息模式
    junk_pat = re.match(r"^(什么|什麼)是？?$", tcn) or re.match(r"^[\w\s]{0,6}(实践指南|實踐指南|指南)$", tcn) or "框架指南" in tcn
    # 半翻译：CJK 占比低且含字母
    half = len(tcn) > 8 and cjk_ratio(tcn) < 0.5 and re.search(r"[A-Za-z]{4}", tcn)
    # 超短
    tiny = 0 < len(tcn.replace(" ", "")) < 6
    if junk_pat or half or tiny:
        row["reason"] = ("junk" if junk_pat else "") + ("+half" if half else "") + ("+tiny" if tiny else "")
        bad.append(row)

print("低质量标题总数:", len(bad))
for x in bad:
    print("\nslug:", x["slug"], "|", x["reason"])
    print("  en:", (x.get("en") or "")[:65])
    print("  cn:", (x.get("cn") or "")[:55])
    print("  tw:", (x.get("tw") or "")[:55])

json.dump(bad, open("/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/title_bad_list.json", "w"), ensure_ascii=False, indent=1)
