# -*- coding: utf-8 -*-
import re, os, json, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from faq_data import FAQ, HEADING_MAP, CATEGORY_MAP, TAG_MAP

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
WO = os.path.join(ROOT, "_batch_pipeline/wo_faq_4.txt")
BACKUP = os.path.join(ROOT, "_batch_pipeline/tmp_faq4/backup")
os.makedirs(BACKUP, exist_ok=True)
paths = [l.strip() for l in open(WO, encoding="utf-8") if l.strip()]

CJK = re.compile(r'[\u4e00-\u9fff]')
ITEM_RE = re.compile(r'<div class="faq-item">.*?</div>\s*</div>\s*</div>', re.S)
# 页面存在三种 FAQ 标记变体，逐个尝试
Q_RES = [
    re.compile(r'(<span class="faq-question-text"><span class="faq-number">\d+</span><span>)undefined(</span>)'),
    re.compile(r'(<h3 class="faq-question-text"[^>]*>)undefined(</h3>)'),
    re.compile(r'(<h3 class="faq-question"><span class="faq-question-text"><span class="faq-number">\d+</span><span>)undefined(</span>)'),
]
A_RE = re.compile(r'(<div class="faq-answer-inner">)undefined(</div>)')
LD_RE = re.compile(
    r'(<script type="application/ld\+json">)'
    r'(\s*\{(?:(?!</script>).)*?"@type"\s*:\s*"FAQPage"(?:(?!</script>).)*?)'
    r'(\s*</script>)', re.S)

report = []

for rel in paths:
    fp = os.path.join(ROOT, rel)
    base = os.path.basename(rel)
    src = open(fp, encoding="utf-8").read()
    orig_div = len(re.findall(r'<div\b', src)) - len(re.findall(r'</div>', src))
    qa = FAQ.get(base)
    if qa is None:
        report.append((base, "SKIP-NO-DATA", 0, 0)); continue
    assert len(qa) == 4, base

    # ---------- 任务 A：重建 FAQ ----------
    items = list(ITEM_RE.finditer(src))
    need_rebuild = 'faq-answer-inner">undefined</div>' in src
    faq_rebuilt = 0
    if need_rebuild:
        if len(items) == 3:
            last = items[-1]
            new_item = last.group(0).replace(
                '<span class="faq-number">%d</span>' % len(items),
                '<span class="faq-number">4</span>')
            if new_item == last.group(0):  # 兼容编号不符的情况
                new_item = re.sub(r'(<span class="faq-number">)\d+(</span>)', r'\g<1>4\g<2>', last.group(0))
            src = src[:last.end()] + "\n                    " + new_item + src[last.end():]
        nq = 0
        for Q_RE in Q_RES:
            it = [0]
            def rq(m):
                v = qa[it[0]][0]; it[0] += 1
                return m.group(1) + v + m.group(2)
            src, nq = Q_RE.subn(rq, src)
            if nq == 4:
                break
            assert nq == 0, (base, "partial question match", nq)
        it2 = [0]
        def ra(m):
            v = qa[it2[0]][1]; it2[0] += 1
            return m.group(1) + v + m.group(2)
        src, na = A_RE.subn(ra, src)
        assert (nq, na) == (4, 4), (base, nq, na)
        faq_rebuilt = 1

        # JSON-LD FAQPage
        m = LD_RE.search(src)
        assert m, base + " no FAQPage ld+json"
        try:
            obj = json.loads(m.group(2))
        except Exception as e:
            raise SystemExit("LD parse fail %s: %s" % (base, e))
        def rebuild(o):
            if isinstance(o, list):
                for x in o: rebuild(x)
            elif isinstance(o, dict):
                if o.get("@type") == "FAQPage":
                    o["mainEntity"] = [
                        {"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]
                for v in o.values(): rebuild(v)
        rebuild(obj)
        newjson = json.dumps(obj, ensure_ascii=False, indent=2)
        src = src[:m.start(2)] + "\n" + newjson + "\n" + src[m.end(2):]

    # ---------- 任务 B：英文小标题 / 推荐卡片标题 ----------
    hcount = 0
    for en, zh in HEADING_MAP.items():
        pat = re.compile(r'(<h([23])\b[^>]*>)' + re.escape(en) + r'(</h\2>)')
        src, n = pat.subn(lambda m: m.group(1) + zh + m.group(3), src)
        hcount += n
        assert en not in src, (base, en)  # 确保没有藏在 href/id/JSON-LD 里的残留
    for en, zh in CATEGORY_MAP.items():
        pat = re.compile(r'(<span class="recommended-card-cat">)' + re.escape(en) + r'(</span>)')
        src, n = pat.subn(lambda m: m.group(1) + zh + m.group(2), src)
        hcount += n

    # ---------- 任务 C：英文标签 ----------
    tcount = 0
    for en, zh in TAG_MAP.items():
        pat = re.compile(r'(<span class="article-tag-pill">)' + re.escape(en) + r'(</span>)')
        src, n = pat.subn(lambda m: m.group(1) + zh + m.group(2), src)
        tcount += n

    # ---------- 备份 + 写入 ----------
    bp = os.path.join(BACKUP, base)
    if not os.path.exists(bp):
        shutil.copy2(fp, bp)
    open(fp, "w", encoding="utf-8").write(src)
    report.append((base, "OK", faq_rebuilt, hcount + tcount))

print("done", len(report))
for r in report:
    print(r)
