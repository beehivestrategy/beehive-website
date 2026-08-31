#!/usr/bin/env python3
"""Structural SEO pass: adds FAQ + FAQPage JSON-LD, populates recommended
excerpts, fixes root-relative language-prefixed links, ensures CTA phrase.
Only edits inside <article id="article-content"> and the recommended/CTA
regions. Preserves <head>, header, footer, share buttons, css/js tags."""
import re, json, sys, os

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

CTAS = {"en": "Book a Demo", "zh-cn": "预约演示", "zh-tw": "預約示範"}
PREFIX = {"en": "/blog/articles/", "zh-cn": "/zh-cn/blog/articles/", "zh-tw": "/zh-tw/blog/articles/"}

def strip_tags(html):
    t = re.sub(r'<[^>]+>', ' ', html)
    t = re.sub(r'&[a-zA-Z]+;', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def first_sentences(text, n=2, maxlen=480):
    text = text.strip()
    # split on sentence boundaries
    parts = re.split(r'(?<=[.!?])\s+', text)
    out = ' '.join(parts[:n]).strip()
    if len(out) > maxlen:
        out = out[:maxlen].rsplit(' ', 1)[0] + '…'
    return out

def build_faq(html, lang):
    """Return (faq_html, jsonld_str) or (None, None) if already present."""
    if 'faq-section' in html:
        return None, None
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    if not m:
        return None, None
    body = m.group(1)
    # title
    tm = re.search(r'<title>(.*?)</title>', html, re.S)
    title = tm.group(1).split(' | ')[0].strip() if tm else "this topic"
    # H2 blocks with following paragraphs
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)
    # map h2 -> paragraphs text
    blocks = re.split(r'(<h2[^>]*>.*?</h2>)', body, flags=re.S)
    pairs = []
    cur_h2 = None
    cur_paras = []
    for seg in blocks:
        if re.match(r'<h2', seg):
            cur_h2 = re.sub(r'<[^>]+>', '', seg).strip()
            cur_paras = []
        else:
            if cur_h2 is not None:
                paras = re.findall(r'<p[^>]*>(.*?)</p>', seg, re.S)
                txt = ' '.join(strip_tags(p) for p in paras)
                if txt.strip():
                    pairs.append((cur_h2, txt))
    # Build Q&A
    qa = []
    # Q1 from title
    if lang.startswith('zh'):
        q1 = f"什么是{title}？"
    else:
        q1 = f"What is {title}?"
    a1 = first_sentences(pairs[0][1] if pairs else strip_tags(body))
    qa.append((q1, a1))
    # additional from h2 pairs (skip Conclusion / Key Takeaways / 结论 / 关键)
    skip = ('conclusion', 'key takeaways', '结论', '关键', '摘要')
    added = 0
    for h2, txt in pairs:
        if added >= 3:
            break
        if any(s in h2.lower() for s in skip):
            continue
        if lang.startswith('zh'):
            q = f"企业应当如何落地「{h2}」？"
        else:
            q = f"How should enterprises approach {h2}?"
        a = first_sentences(txt)
        if len(a) < 40:
            continue
        qa.append((q, a))
        added += 1
    # ensure at least 3
    while len(qa) < 3 and pairs:
        h2, txt = pairs[len(qa)-1]
        if lang.startswith('zh'):
            q = f"「{h2}」为什么重要？"
        else:
            q = f"Why does {h2} matter?"
        qa.append((q, first_sentences(txt)))
    if len(qa) < 3:
        return None, None
    # FAQ html
    faq_items = ""
    for q, a in qa:
        faq_items += f'            <h3>{q}</h3>\n            <p>{a}</p>\n'
    faq_html = (
        '\n        <div class="faq-section">\n'
        '            <h2>Frequently Asked Questions</h2>\n' if lang == 'en'
        else '            <h2>常见问题解答</h2>\n'
    )
    # build properly
    if lang == 'en':
        heading = "Frequently Asked Questions"
    elif lang == 'zh-cn':
        heading = "常见问题解答"
    else:
        heading = "常見問題解答"
    faq_items2 = ""
    for q, a in qa:
        faq_items2 += f'            <h3>{q}</h3>\n            <p>{a}</p>\n'
    faq_html = (f'        <div class="faq-section">\n'
                f'            <h2>{heading}</h2>\n'
                f'{faq_items2}        </div>\n')
    # JSON-LD
    main = []
    for q, a in qa:
        main.append({"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}})
    obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": main}
    jsonld = f'        <script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>\n'
    return faq_html, jsonld

def fix_links(html, lang):
    pref = PREFIX[lang]
    def repl_tag(m):
        tag = m.group(0)
        cm = re.search(r'class="([^"]*)"', tag)
        cls = cm.group(1) if cm else ''
        sm = re.search(r'([a-z0-9]+(?:-[a-z0-9]+){2,})', tag)
        if not sm:
            return tag
        slug = sm.group(1)
        return f'<a href="{pref}{slug}" class="{cls}">'
    # only recommended-card and sidebar-related-card anchors
    return re.sub(r'<a\b[^>]*class="[^"]*(?:recommended-card|sidebar-related-card)[^"]*"[^>]*>', repl_tag, html)

def populate_excerpts(html):
    def repl(m):
        block = m.group(0)
        tm = re.search(r'recommended-card-title">([^<]+)<', block)
        if not tm:
            return block
        summary = tm.group(1).strip()
        summary = summary[0].upper() + summary[1:] if summary else summary
        if not summary.endswith('.'):
            summary += '.'
        return re.sub(r'<p class="recommended-card-excerpt">[\s\S]*?</p>',
                      f'<p class="recommended-card-excerpt">{summary}</p>', block)
    return re.sub(r'<a\b[^>]*class="[^"]*recommended-card[^"]*"[^>]*>[\s\S]*?</a>', repl, html)

def ensure_cta(html, lang):
    if lang == 'zh-tw':
        html = re.sub(r'(<a\b[^>]*class="article-cta-btn"[^>]*>)([\s\S]*?)(</a>)',
                      lambda m: m.group(1) + m.group(2).replace('預約演示', '預約示範') + m.group(3), html)
    return html

def process(path, lang):
    html = open(path, encoding='utf-8').read()
    orig = html
    # 1. FAQ + JSON-LD
    faq_html, jsonld = build_faq(html, lang)
    if faq_html:
        nav_marker = '<nav class="article-nav"'
        if nav_marker in html:
            insert = faq_html + jsonld
            html = html.replace(nav_marker, insert + "\n" + nav_marker, 1)
    # 2. links
    html = fix_links(html, lang)
    # 3. excerpts
    html = populate_excerpts(html)
    # 4. cta
    html = ensure_cta(html, lang)
    if html != orig:
        open(path, 'w', encoding='utf-8').write(html)
        return True
    return False

if __name__ == "__main__":
    slug = sys.argv[1]
    langmap = [("en", f"blog/articles/{slug}.html"),
               ("zh-cn", f"zh-cn/blog/articles/{slug}.html"),
               ("zh-tw", f"zh-tw/blog/articles/{slug}.html")]
    for lang, rel in langmap:
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            ch = process(p, lang)
            print(f"{rel}: {'changed' if ch else 'unchanged'}")
        else:
            print(f"{rel}: MISSING")
