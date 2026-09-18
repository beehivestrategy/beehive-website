# -*- coding: utf-8 -*-
import re, os, json, sys

CJK = re.compile(r"[\u4e00-\u9fff]")
def strip(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()

def variant(s):
    if re.search(r'<h3 class="faq-question-text"><span class="faq-number">', s): return "V5"
    if re.search(r'<span class="faq-question-text"><span class="faq-number">\d+</span><span>', s): return "V1"
    if re.search(r'<h3 class="faq-question-text"[^>]*>', s): return "V2"
    if re.search(r'<span class="faq-question-text"><span class="faq-number">\d+</span><h3 class="faq-q"', s): return "V3"
    if re.search(r'<span class="faq-question-text"><span class="faq-number">\d+</span>', s): return "V4"
    return "?"

def questions(s, v):
    if v == "V1":
        return [strip(x) for x in re.findall(r'<span class="faq-question-text"><span class="faq-number">\d+</span><span>(.*?)</span>\s*</span>', s, re.S)]
    if v == "V2":
        return [strip(x) for x in re.findall(r'<h3 class="faq-question-text"[^>]*>(.*?)</h3>', s, re.S)]
    if v == "V3":
        return [strip(x) for x in re.findall(r'<span class="faq-question-text"><span class="faq-number">\d+</span><h3 class="faq-q"[^>]*>(.*?)</h3>', s, re.S)]
    if v == "V4":
        return [strip(x) for x in re.findall(r'<span class="faq-question-text"><span class="faq-number">\d+</span>(.*?)</span>', s, re.S)]
    if v == "V5":
        return [strip(x) for x in re.findall(r'<h3 class="faq-question-text"><span class="faq-number">\d+</span><span>(.*?)</span>\s*</h3>', s, re.S)]
    return []

files = [l.strip() for l in open("_batch_pipeline/wo_faq_2.txt", encoding="utf-8") if l.strip()]
fails = 0
print(f"{'file':46} {'Q':>2}{'A':>2}{'LD':>3} 检查")
for rel in files:
    fn = os.path.basename(rel)
    s = open(rel, encoding="utf-8").read()
    old = open("_batch_pipeline/_bak_wo2/" + fn, encoding="utf-8").read()
    probs = []

    # ① 无 undefined 可见文本
    # 剔除 script/style 后检查
    vis = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    vis = re.sub(r"<style.*?</style>", "", vis, flags=re.S)
    if "undefined" in vis:
        probs.append("①残留undefined(可见)")
    if "undefined" in s:
        probs.append("①残留undefined(含脚本)")

    # ② 无纯英文 h2/h3
    for m in re.finditer(r"<(h2|h3)([^>]*)>(.*?)</\1>", s, re.S):
        t = strip(m.group(3))
        cls = re.search(r'class="([^"]*)"', m.group(2))
        if cls and "faq" in cls.group(1): continue
        if t and not CJK.search(t):
            probs.append(f"②纯英文{m.group(1)}:{t[:28]}")

    # ③ FAQ 问题数 == JSON-LD 数 == 答案数
    v = variant(s)
    q = questions(s, v)
    a = re.findall(r'<div class="faq-answer-inner">(.*?)</div>', s, re.S)
    ld = []
    for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: j = json.loads(mm.group(1).strip())
        except Exception: probs.append("③JSON-LD解析失败"); continue
        for o in (j if isinstance(j, list) else [j]):
            if isinstance(o, dict) and o.get("@type") == "FAQPage":
                for it in o.get("mainEntity", []):
                    ld.append((it.get("name"), (it.get("acceptedAnswer") or {}).get("text")))
    if not (len(q) == len(a) == len(ld)):
        probs.append(f"③数量不一致 Q{len(q)}/A{len(a)}/LD{len(ld)}")
    else:
        for i, (lq, la) in enumerate(ld):
            if lq != q[i]: probs.append(f"③LD[{i}]问题与可见不一致")
            if la != a[i].strip(): probs.append(f"③LD[{i}]答案与可见不一致")
        for i, x in enumerate(q):
            if not x or x == "undefined": probs.append(f"③Q{i+1}为空")
            if len(set(q)) != len(q): probs.append("③问题重复"); break

    # ④ div 开闭差额一致
    d0 = len(re.findall(r"<div\b", old)) - len(re.findall(r"</div>", old))
    d1 = len(re.findall(r"<div\b", s)) - len(re.findall(r"</div>", s))
    if d0 != d1: probs.append(f"④div差额 {d0}->{d1}")

    # 附加：id/href 未被改动
    id0 = re.findall(r'id="([^"]+)"', old); id1 = re.findall(r'id="([^"]+)"', s)
    h0 = re.findall(r'href="([^"]+)"', old); h1 = re.findall(r'href="([^"]+)"', s)
    if id0 != id1: probs.append("⑤id集合变化")
    if h0 != h1: probs.append("⑤href集合变化")

    if probs:
        fails += 1
        print(f"{fn[:44]:46} {len(q):2}{len(a):2}{len(ld):3} ✗ " + "; ".join(probs[:4]))
    else:
        print(f"{fn[:44]:46} {len(q):2}{len(a):2}{len(ld):3} ✓")

print(f"\n未通过文件数: {fails}/{len(files)}")
