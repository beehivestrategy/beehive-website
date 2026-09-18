#!/usr/bin/env python3
"""三语言标题审计：重复 / 未翻译 / 未转繁体 / 高度相似"""
import os, re, json, unicodedata
from collections import defaultdict

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
DIRS = {
    "en": os.path.join(ROOT, "blog", "articles"),
    "cn": os.path.join(ROOT, "zh-cn", "blog", "articles"),
    "tw": os.path.join(ROOT, "zh-tw", "blog", "articles"),
}
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)

def clean(t: str) -> str:
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s*\|\s*Beehive.*$", "", t)          # 站点后缀
    t = re.sub(r"\s*原创\s*$", "", t)                  # 原创 后缀
    return t

def norm(t: str) -> str:
    """归一化：去空白/标点/大小写/全半角，用于相似检测"""
    t = unicodedata.normalize("NFKC", t).lower()
    t = re.sub(r"[\s\-—–_·•:：,，。.、;；!！?？'\"“”‘’()\[\]{}（）【】|/\\]", "", t)
    return t

data = {k: {} for k in DIRS}
for lang, d in DIRS.items():
    for f in sorted(os.listdir(d)):
        if not f.endswith(".html"):
            continue
        slug = f[:-5]
        try:
            html = open(os.path.join(d, f), encoding="utf-8", errors="ignore").read()
        except Exception as e:
            data[lang][slug] = {"title": "", "error": str(e)}
            continue
        m = TITLE_RE.search(html)
        raw = m.group(1) if m else ""
        data[lang][slug] = {"title": clean(raw), "raw": raw.strip()}

report = {"per_lang_count": {}, "exact_dup": {}, "norm_dup": {}, "prefix_dup": {},
          "cn_eq_tw": [], "zh_uses_en": [], "cross_notes": []}

# 1) 同语言内重复
for lang in DIRS:
    titles = {s: v["title"] for s, v in data[lang].items()}
    report["per_lang_count"][lang] = len(titles)
    # 精确重复
    seen = defaultdict(list)
    for s, t in titles.items():
        if t:
            seen[t].append(s)
    report["exact_dup"][lang] = [{"title": t, "slugs": ss} for t, ss in seen.items() if len(ss) > 1]
    # 归一化重复（近似重复的主要来源）
    seen2 = defaultdict(list)
    for s, t in titles.items():
        n = norm(t)
        if n:
            seen2[n].append(s)
    report["norm_dup"][lang] = [{"titles": [{"slug": x, "title": titles[x]} for x in ss]}
                                 for n, ss in seen2.items() if len(ss) > 1]
    # 前缀重复（一个标题是另一个的前缀）
    entries = sorted([(s, t) for s, t in titles.items() if t], key=lambda x: x[1])
    prefixes = []
    for i in range(len(entries) - 1):
        s1, t1 = entries[i]
        for j in range(i + 1, len(entries)):
            s2, t2 = entries[j]
            if t2.startswith(t1) and t2 != t1 and len(t2) - len(t1) <= 30:
                prefixes.append({"base": {"slug": s1, "title": t1},
                                 "ext": {"slug": s2, "title": t2}})
            if not t2.startswith(t1):
                break
    report["prefix_dup"][lang] = prefixes

# 2) zh-CN == zh-TW（未转繁体嫌疑）
for slug in data["cn"]:
    tcn = data["cn"].get(slug, {}).get("title", "")
    ttw = data["tw"].get(slug, {}).get("title", "")
    if tcn and ttw and tcn == ttw:
        report["cn_eq_tw"].append({"slug": slug, "title": tcn})

# 3) zh 沿用 EN（未翻译嫌疑）：zh 标题与 EN 标题一致 或 zh 标题基本是 ASCII
for slug in data["en"]:
    ten = data["en"].get(slug, {}).get("title", "")
    for lang in ("cn", "tw"):
        tz = data[lang].get(slug, {}).get("title", "")
        if not tz:
            continue
        if ten and norm(tz) == norm(ten):
            report["zh_uses_en"].append({"slug": slug, "lang": lang, "title": tz})
        else:
            ascii_ratio = sum(1 for c in tz if ord(c) < 128) / max(len(tz), 1)
            if ascii_ratio > 0.9 and len(tz) > 10:
                report["zh_uses_en"].append({"slug": slug, "lang": lang, "title": tz, "reason": "mostly-ascii"})

# 汇总
report["summary"] = {
    "exact_dup": {k: len(v) for k, v in report["exact_dup"].items()},
    "norm_dup": {k: len(v) for k, v in report["norm_dup"].items()},
    "prefix_dup": {k: len(v) for k, v in report["prefix_dup"].items()},
    "cn_eq_tw": len(report["cn_eq_tw"]),
    "zh_uses_en": len(report["zh_uses_en"]),
}

out = os.path.join(ROOT, "_batch_pipeline", "title_audit.json")
json.dump(report, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps(report["summary"], ensure_ascii=False, indent=1))
print("saved:", out)
