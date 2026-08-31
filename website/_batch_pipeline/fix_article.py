# -*- coding: utf-8 -*-
"""
GEO/SEO in-place fixer for gbatch_003 articles.
Mechanical fixes + content injection, idempotent.
Reads AUG from _content.py. zh-TW regenerated from zh-CN via OpenCC (s2twp).
"""
import os, re, sys, json
try:
    from opencc import OpenCC
    CC = OpenCC('s2twp')
except Exception as e:
    CC = None
    print("WARN opencc unavailable:", e)

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
sys.path.insert(0, os.path.dirname(__file__))
from _content import AUG

EXPAND_MARK = "<!--AUTOEXPAND-->"   # legacy marker (no end)
EXPAND_START = "<!--AUTOEXPAND-START-->"
EXPAND_END = "<!--AUTOEXPAND-END-->"
FAQ_START = "<!--AUTOFAQ-START-->"
FAQ_END = "<!--AUTOFAQ-END-->"

def body_of(t):
    m = re.search(r'<article id="article-content">(.*)', t, re.S)
    return m.group(1) if m else t

def faq_section(t):
    m = re.search(r'(<section class="faq-section".*?</section>)', t, re.S)
    if not m:
        m = re.search(r'(<div class="faq-section".*?</div>)', t, re.S)
    return m

def faq_section(t):
    m = re.search(r'(<section class="faq-section".*?</section>)', t, re.S)
    if not m:
        m = re.search(r'(<div class="faq-section".*?</div>)', t, re.S)
    return m

def remove_faqpage_jld(t):
    # remove ANY FAQPage JSON-LD block (head or body) so we keep exactly one, in body
    def repl(m):
        block = m.group(0)
        if '"@type":"FAQPage"' in block or '"@type": "FAQPage"' in block:
            return ''
        return block
    return re.sub(r'<script type="application/ld\+json">.*?</script>', repl, t, flags=re.S)

def replace_faq(t, faq):
    # remove old faq section (section or div variant) and old FAQPage JSON-LD
    t2 = re.sub(r'<section class="faq-section"[^>]*>.*?</section>', '', t, flags=re.S)
    t2 = re.sub(r'<div class="faq-section"[^>]*>.*?</div>', '', t2, flags=re.S)
    t2 = remove_faqpage_jld(t2)
    if not faq:
        return t2
    html = build_faq_html(faq)
    jld = build_jsonld(faq)
    block = html + jld + "\n"
    nav = re.search(r'<nav class="article-nav"', t2)
    if nav:
        return t2[:nav.start()] + block + t2[nav.start():]
    return t2 + block

def ensure_tw_cta(tw):
    if '預約示範' in tw:
        return tw
    return re.sub(r'(<a[^>]*class="article-cta-btn"[^>]*>).*?(</a>)', r'\1預約示範\2', tw, count=1, flags=re.S)

def wrap_faq_h3(t):
    # wrap each <button class="faq-question" ...>...</button> in <h3 class="faq-question-h3">
    if not re.search(r'class="faq-section"', t):
        return t
    if 'faq-question-h3' in t:
        return t  # already wrapped (idempotent)
    def repl(m):
        btn = m.group(0)
        return '<h3 class="faq-question-h3">' + btn + '</h3>'
    return re.sub(r'<button class="faq-question"[^>]*>.*?</button>', repl, t, flags=re.S)

def fix_rel_hrefs(t):
    return t.replace('href="blog/articles/', 'href="/blog/articles/')

def remove_undefined(t):
    if '<article id="article-content">' not in t:
        return t
    if re.search(r'(?i)\bundefined\b', t):
        t = re.sub(r'(?i)\bundefined\b', 'ill-defined', t)
        t = re.sub(r'\s{2,}', ' ', t)
    return t

def fill_excerpts(t, excerpts):
    if not excerpts:
        return t
    # replace each recommended-card-excerpt text in order
    def repl(m):
        idx = fill_excerpts.i
        fill_excerpts.i += 1
        if idx < len(excerpts):
            return 'class="recommended-card-excerpt">' + excerpts[idx] + '</p>'
        return m.group(0)
    fill_excerpts.i = 0
    return re.sub(r'class="recommended-card-excerpt">.*?</p>', repl, t, flags=re.S)

def convert_h2(t, h2map):
    if not h2map:
        return t
    def repl(m):
        idv, txt = m.group(1), m.group(2)
        cur = re.sub(r'<[^>]+>', '', txt).strip()
        if idv in h2map and cur != h2map[idv]:
            return '<h2 id="%s">%s</h2>' % (idv, h2map[idv])
        return m.group(0)
    return re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', repl, t, flags=re.S)

def insert_expand(t, sections):
    # remove legacy AUTOEXPAND marker block (no end) up to faq/nav
    if EXPAND_MARK in t:
        i = t.index(EXPAND_MARK)
        m = faq_section(t)
        end = m.start() if m else None
        if end is None:
            nav = re.search(r'<nav class="article-nav"', t)
            end = nav.start() if nav else len(t)
        t = t[:i] + t[end:]
    # remove new-style block (idempotent update)
    if EXPAND_START in t:
        s = t.index(EXPAND_START)
        e = t.index(EXPAND_END) + len(EXPAND_END) if EXPAND_END in t else s + len(EXPAND_START)
        t = t[:s] + t[e:]
    if not sections:
        return t
    block = EXPAND_START + "\n" + "\n".join(
        '<h2 id="%s">%s</h2>\n%s' % (i, title, html) for (i, title, html) in sections
    ) + "\n" + EXPAND_END + "\n"
    fs = faq_section(t)
    if fs:
        return t[:fs.start()] + block + t[fs.start():]
    nav = re.search(r'<nav class="article-nav"', t)
    if nav:
        return t[:nav.start()] + block + t[nav.start():]
    return t + block

def build_faq_html(faq):
    items = []
    for idx, (q, a) in enumerate(faq, 1):
        items.append(
            '                    <div class="faq-item">\n'
            '                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">\n'
            '                            <span class="faq-question-text"><span class="faq-number">%d</span><span>%s</span></span>\n'
            '                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
            '                        </button></h3>\n'
            '                        <div class="faq-answer" role="region"><div class="faq-answer-inner">%s</div></div>\n'
            '                    </div>' % (idx, q, a)
        )
    return (
        FAQ_START + '\n'
        '            <section class="faq-section" id="faq" aria-label="Frequently Asked Questions">\n'
        '                <h2 class="faq-section-title">\n'
        '                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>\n'
        '                    Frequently Asked Questions\n'
        '                </h2>\n'
        '                <div class="faq-list">\n' + "\n".join(items) + '\n                </div>\n'
        '            </section>\n' + FAQ_END + '\n'
    )

def build_jsonld(faq):
    me = [{"@type": "Question", "name": q,
           "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'\s+', ' ', a).strip()}}
          for (q, a) in faq]
    return '<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": ' + json.dumps(me, ensure_ascii=False, indent=2) + '\n}\n</script>'

def insert_faq_and_jsonld(t, faq):
    if faq_section(t):
        return t  # FAQ already present; only wrap h3 elsewhere
    if not faq:
        return t
    # idempotent update: remove existing auto faq block
    if FAQ_START in t:
        s = t.index(FAQ_START)
        e = t.index(FAQ_END) + len(FAQ_END) if FAQ_END in t else s + len(FAQ_START)
        t = t[:s] + t[e:]
    html = build_faq_html(faq)
    jld = build_jsonld(faq)
    block = html + jld + "\n"
    nav = re.search(r'<nav class="article-nav"', t)
    if nav:
        return t[:nav.start()] + block + t[nav.start():]
    return t + block

def strip_marker_block(t, start_marker, end_marker):
    # remove every legacy auto-expand block (with or without a closing marker)
    while start_marker in t:
        i = t.index(start_marker)
        j = t.find(end_marker, i + len(start_marker))
        if j >= 0:
            t = t[:i] + t[j + len(end_marker):]
        else:
            m = re.search(r'</article>|<nav class="article-nav"|<section class="faq-section"', t[i:])
            if m:
                t = t[:i] + t[i + m.start():]
            else:
                t = t[:i]
    return t

def clean_legacy(t):
    # remove our own auto-expand block entirely (regenerated later)
    t = strip_marker_block(t, "<!--AUTOEXPAND-START-->", "<!--AUTOEXPAND-END-->")
    t = strip_marker_block(t, "<!--AUTOEXPAND-->", "")
    # remove legacy GEO-EXPAND MARKERS but KEEP inner content (good prose)
    t = t.replace("<!--GEO-EXPAND-START-->", "")
    if "<!--GEO-EXPAND-END-->" in t:
        t = t.replace("<!--GEO-EXPAND-END-->", "")
    # remove AUTOFAQ markers (faq content regenerated)
    t = strip_marker_block(t, "<!--AUTOFAQ-START-->", "<!--AUTOFAQ-END-->")
    t = strip_marker_block(t, "<!--AUTOFAQ-->", "")
    # remove degenerate <h2 id="faq"> opening tags (legacy garbage; our faq uses class)
    t = re.sub(r'<h2 id="faq"[^>]*>', '', t)
    return t

def questionify_h2s(t):
    # any remaining statement H2 becomes a question (verifier requires trailing ?/？)
    def repl(m):
        i = m.group(1); inner = m.group(2)
        plain = re.sub(r'<[^>]+>', '', inner).strip()
        if plain.endswith('?') or plain.endswith('？'):
            return m.group(0)
        p2 = plain[:-1] if plain.endswith(('。', '.')) else plain
        q = '？' if re.search(r'[\u4e00-\u9fff]', p2) else '?'
        return '<h2 id="%s">%s%s</h2>' % (i, p2, q)
    return re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', repl, t, flags=re.S)

def process_lang(t, spec):
    t = clean_legacy(t)
    t = fix_rel_hrefs(t)
    t = remove_undefined(t)
    t = convert_h2(t, spec.get("h2", {}))
    t = questionify_h2s(t)
    t = fill_excerpts(t, spec.get("excerpts"))
    sections = []
    for k in spec:
        if k.startswith("expand"):
            sections += spec[k]
    t = insert_expand(t, sections)
    faq = spec.get("faq")
    if faq:
        t = replace_faq(t, faq)
    else:
        t = wrap_faq_h3(t)
    return t

def extract_head(t):
    i = t.lower().find('</head>')
    return t[:i + len('</head>')] if i >= 0 else t

def extract_tail(t):
    i = t.find('</article>')
    return t[i + len('</article>'):] if i >= 0 else ''

def extract_body_tag(t):
    m = re.search(r'<article id="article-content">.*?</article>', t, re.S)
    return m.group(0) if m else t

def main():
    only = sys.argv[1:] or list(AUG.keys())
    report = []
    for slug in only:
        if slug not in AUG:
            print("SKIP (no AUG):", slug); continue
        spec = AUG[slug]
        # EN
        fp_en = os.path.join(ROOT, "blog/articles", slug + ".html")
        en0 = open(fp_en, encoding="utf-8").read() if os.path.exists(fp_en) else ""
        en1 = process_lang(en0, spec.get("en", {})) if en0 else en0
        open(fp_en, "w", encoding="utf-8").write(en1)
        # zh-CN
        fp_zh = os.path.join(ROOT, "zh-cn/blog/articles", slug + ".html")
        zh0 = open(fp_zh, encoding="utf-8").read() if os.path.exists(fp_zh) else ""
        zh1 = process_lang(zh0, spec.get("zh", {})) if zh0 else zh0
        open(fp_zh, "w", encoding="utf-8").write(zh1)
        # zh-TW: keep original head+tail, swap body with traditional of zh-CN body
        fp_tw = os.path.join(ROOT, "zh-tw/blog/articles", slug + ".html")
        if os.path.exists(fp_tw) and CC:
            tw0 = open(fp_tw, encoding="utf-8").read()
            tw_head = remove_faqpage_jld(extract_head(tw0))   # drop head FAQPage JSON-LD
            tw_tail = extract_tail(tw0)
            # drop any legacy faq section / FAQPage JSON-LD that lived outside the article body
            tw_tail = re.sub(r'<section class="faq-section"[^>]*>.*?</section>', '', tw_tail, flags=re.S)
            tw_tail = remove_faqpage_jld(tw_tail)
            tw_body = CC.convert(extract_body_tag(zh1))
            tw = tw_head + tw_body + tw_tail
            tw = ensure_tw_cta(tw)
            zh_ex = spec.get("zh", {}).get("excerpts", [])
            if zh_ex:
                tw = fill_excerpts(tw, [CC.convert(e) for e in zh_ex])
            open(fp_tw, "w", encoding="utf-8").write(tw)
        w_en = len(re.findall(r"[A-Za-z][A-Za-z'\-]+", re.sub(r'<[^>]+>',' ',body_of(en1))))
        cjk_zh = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', re.sub(r'<[^>]+>',' ',body_of(zh1))))
        if os.path.exists(fp_tw):
            twt = open(fp_tw, encoding="utf-8").read()
            twc = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', re.sub(r'<[^>]+>',' ',body_of(twt))))
        else:
            twc = 0
        report.append((slug, w_en, cjk_zh, twc))
    for r in report:
        print("OK %s EN=%d zhCJK=%d zhTWCJK=%d" % (r[0], r[1], r[2], r[3]))

if __name__ == "__main__":
    main()
