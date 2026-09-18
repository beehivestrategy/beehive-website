# -*- coding: utf-8 -*-
import re, os, json, sys, html
sys.path.insert(0, "_batch_pipeline")
from _wo2_faq import FAQ, HEADS, CARDS, CATS

ROOT = "."
ART = "zh-cn/blog/articles"

def match_div(s, i):
    """i 指向 '<div'，返回该 div 匹配 '</div>' 的结束下标"""
    depth = 0
    for m in re.finditer(r"<div\b|</div>", s[i:]):
        if m.group(0) == "</div>":
            depth -= 1
            if depth == 0:
                return i + m.end()
        else:
            depth += 1
    return -1

def faq_items(s):
    """返回 [(start, end)] 覆盖所有 <div class="faq-item"> 块"""
    out = []
    for m in re.finditer(r'<div class="faq-item"[ >]', s):
        e = match_div(s, m.start())
        if e != -1:
            out.append((m.start(), e))
    return out

Q_RE = re.compile(r'(<span class="faq-number">)(\d+)(</span><span>)(.*?)(</span>)', re.S)
A_RE = re.compile(r'(<div class="faq-answer-inner">)(.*?)(</div>)', re.S)

def rebuild_faq(s, qas):
    """把现有 faq-item 的 Q/A 依次替换为 qas；数量不足则克隆最后一块补齐"""
    blocks = faq_items(s)
    if not blocks:
        raise RuntimeError("no faq-item found")
    # 从后往前替换，避免下标偏移
    for idx in range(len(blocks) - 1, -1, -1):
        st, en = blocks[idx]
        blk = s[st:en]
        if idx < len(qas):
            q, a = qas[idx]
            blk, n1 = Q_RE.subn(lambda m: m.group(1) + m.group(2) + m.group(3) + q + m.group(5), blk, count=1)
            blk, n2 = A_RE.subn(lambda m: m.group(1) + a + m.group(3), blk, count=1)
            if n1 != 1 or n2 != 1:
                raise RuntimeError(f"item{idx} 替换失败 q={n1} a={n2}")
            s = s[:st] + blk + s[en:]
    # 补齐缺失项：克隆最后一块（替换已改变字符串长度，必须重算下标）
    blocks = faq_items(s)
    while len(blocks) < len(qas):
        st, en = blocks[-1]
        last = s[st:en]
        idx = len(blocks)
        q, a = qas[idx]
        new = re.sub(r'(<span class="faq-number">)\d+', lambda m: m.group(1) + str(idx + 1), last, count=1)
        new, n1 = Q_RE.subn(lambda m: m.group(1) + m.group(2) + m.group(3) + q + m.group(5), new, count=1)
        new, n2 = A_RE.subn(lambda m: m.group(1) + a + m.group(3), new, count=1)
        if n1 != 1 or n2 != 1:
            raise RuntimeError(f"新增 item{idx} 替换失败 q={n1} a={n2}")
        s = s[:en] + "\n" + new + s[en:]
        blocks = faq_items(s)
    return s

def rebuild_ld(s, qas):
    """重写 FAQPage JSON-LD 的 mainEntity"""
    def repl(m):
        raw = m.group(1)
        try:
            obj = json.loads(raw)
        except Exception:
            return m.group(0)
        lead, trail = "", ""
        if raw.startswith("\n"): lead = "\n"
        if raw.endswith("\n"): trail = "\n"
        ent = [{"@type": "Question", "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]
        def fix(o):
            if isinstance(o, dict):
                if o.get("@type") == "FAQPage":
                    o["mainEntity"] = ent
                for v in o.values(): fix(v)
            elif isinstance(o, list):
                for v in o: fix(v)
        fix(obj)
        return ('<script type="application/ld+json">' + lead
                + json.dumps(obj, ensure_ascii=False, indent=2) + trail
                + "</script>")
    s2, n = re.subn(r'<script type="application/ld\+json">(.*?)</script>',
                    lambda m: repl(m) if "FAQPage" in m.group(1) else m.group(0), s, flags=re.S)
    if n == 0:
        raise RuntimeError("未找到 FAQPage JSON-LD")
    return s2

def translate_heads(s, items, fn):
    """翻译 h2（保留 id/属性）、TOC 链接文本（保留锚点）"""
    n = 0
    for en, zh, hid in items:
        pat_h = re.compile(r'(<h2\b[^>]*\bid="' + re.escape(hid) + r'"[^>]*>)' +
                           re.escape(en) + r'(</h2>)')
        s, c = pat_h.subn(lambda m: m.group(1) + zh + m.group(2), s)
        n += c
        pat_a = re.compile(r'(<a\b[^>]*href="#' + re.escape(hid) + r'"[^>]*>)' +
                           re.escape(en) + r'(</a>)')
        s, c = pat_a.subn(lambda m: m.group(1) + zh + m.group(2), s)
        n += c
    return s, n

def translate_cards(s):
    n = 0
    for en, zh in CARDS:
        pat = re.compile(r'(<h3 class="recommended-card-title">)' + re.escape(en) + r'(</h3>)')
        s, c = pat.subn(lambda m: m.group(1) + zh + m.group(2), s)
        n += c
        pat2 = re.compile(r'(aria-label=")' + re.escape(en) + r'(")')
        s, c = pat2.subn(lambda m: m.group(1) + zh + m.group(2), s)
        n += c
    for en, zh in CATS:
        pat = re.compile(r'(<span class="recommended-card-cat">)' + re.escape(en) + r'(</span>)')
        s, c = pat.subn(lambda m: m.group(1) + zh + m.group(2), s)
        n += c
    return s, n

def main():
    files = [l.strip() for l in open("_batch_pipeline/wo_faq_2.txt", encoding="utf-8") if l.strip()]
    stats = {"faq": 0, "head": 0, "card": 0}
    for rel in files:
        fn = os.path.basename(rel)
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        d0 = len(re.findall(r"<div\b", s)) - len(re.findall(r"</div>", s))

        if fn in FAQ:
            s = rebuild_faq(s, FAQ[fn])
            s = rebuild_ld(s, FAQ[fn])
            stats["faq"] += 1

        s, nh = translate_heads(s, HEADS.get(fn, []), fn)
        s, nc = translate_cards(s)
        stats["head"] += nh
        stats["card"] += nc

        d1 = len(re.findall(r"<div\b", s)) - len(re.findall(r"</div>", s))
        if d0 != d1:
            print(f"  [FAIL] {fn} div 差额变化 {d0}->{d1}，跳过写回")
            continue
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
    print("处理:", json.dumps(stats, ensure_ascii=False))

if __name__ == "__main__":
    main()
