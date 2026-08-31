#!/usr/bin/env python3
"""gbatch_002 mechanical fixes:
 1. Wrap FAQ question buttons in <h3 class="faq-question-title"> (brief requires <h3> questions)
 2. Strip duplicated leading number inside question text ("1 What ..." -> "What ...")
 3. Normalise recommended-card hrefs to root-relative / language-prefixed
 4. Normalise CTA hrefs and CTA demo phrase per language
 5. Populate empty recommended-card-excerpt (EN only)
"""
import re
import os

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
SLUGS = [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/gap_batches/gbatch_002.txt')) if l.strip()]

EXCERPTS = {
    'women-in-data-building-inclusive-ai-teams':
        'How gender-diverse data and AI teams make measurably better model and governance decisions, and the hiring practices that close the gap.',
    'why-data-strategy-needs-ai-agent-layer-2026':
        'Why an agent layer above the consumption layer turns a static data stack into one that answers questions and acts on them.',
    'vector-databases-enterprise-search-2026-practical-guide':
        'A practical guide to selecting, sizing and operating vector databases for enterprise-scale semantic search.',
}

CTA_TEXT = {'en': 'Book a Demo', 'zh-cn': '预约演示', 'zh-tw': '預約示範'}


def fix_faq_h3(doc):
    if '<h3 class="faq-question-title"' in doc:
        return doc, 0
    n = 0

    def repl(m):
        nonlocal n
        n += 1
        indent, attrs, inner = m.group(1), m.group(2), m.group(3)
        return f'{indent}<h3 class="faq-question-title" style="margin:0"><button class="faq-question"{attrs}>{inner}</button></h3>'

    doc = re.sub(r'(\s*)<button class="faq-question"([^>]*)>(.*?)</button>',
                 repl, doc, flags=re.S)
    return doc, n


def dedupe_faq_numbers(doc):
    before = doc
    doc = re.sub(r'(<span class="faq-number">\s*\d+\s*</span>\s*<span>)\s*\d+\s+', r'\1', doc)
    return doc, 1 if doc != before else 0


def fix_hrefs(doc, lang):
    """lang: 'en' | 'zh-cn' | 'zh-tw'"""
    changed = 0
    prefix = {'en': '/blog/articles/', 'zh-cn': 'zh-cn/blog/articles/', 'zh-tw': 'zh-tw/blog/articles/'}[lang]

    def rec_repl(m):
        nonlocal changed
        href = m.group(1)
        slug = href.split('/')[-1]
        new = prefix + slug
        if new != href:
            changed += 1
        return f'<a href="{new}" class="recommended-card"'

    doc = re.sub(r'<a href="([^"]*)" class="recommended-card"', rec_repl, doc)

    # CTA button href
    cta_href = {'en': '/contact', 'zh-cn': 'zh-cn/contact', 'zh-tw': 'zh-tw/contact'}[lang]
    def cta_repl(m):
        nonlocal changed
        if m.group(1) != cta_href:
            changed += 1
        return f'<a href="{cta_href}" class="article-cta-btn"'
    doc = re.sub(r'<a href="([^"]*)" class="article-cta-btn"', cta_repl, doc)

    sec_href = {'en': '/solution', 'zh-cn': 'zh-cn/solution', 'zh-tw': 'zh-tw/solution'}[lang]
    def sec_repl(m):
        nonlocal changed
        if m.group(1) != sec_href:
            changed += 1
        return f'<a href="{sec_href}" class="article-cta-secondary"'
    doc = re.sub(r'<a href="([^"]*)" class="article-cta-secondary"', sec_repl, doc)

    # covers image prefix
    img_pfx = {'en': '/assets/blog/covers/en/', 'zh-cn': '/assets/blog/covers/zh-cn/',
               'zh-tw': '/assets/blog/covers/zh-tw/'}[lang]
    def img_repl(m):
        nonlocal changed
        slug = m.group(1).split('/')[-1]
        new = img_pfx + slug
        if new != m.group(1):
            changed += 1
        return f'src="{new}"'
    doc = re.sub(r'src="((?:zh-(?:cn|tw)/)?assets/blog/covers/[a-z\-]+/[^"]+)"', img_repl, doc)
    return doc, changed


def fix_cta_text(doc, lang):
    want = CTA_TEXT[lang]
    wrong = {'zh-tw': ['預約演示', '预约演示', '预约示範']}.get(lang, ['Book A Demo', 'book a demo'])
    m = re.search(r'(<a href="[^"]*" class="article-cta-btn"[^>]*>)([^<]*)(<)', doc)
    if not m:
        return doc, 0
    if m.group(2).strip() == want:
        return doc, 0
    return doc[:m.start(2)] + want + doc[m.end(2):], 1


def fix_excerpts(doc, lang):
    if lang != 'en':
        return doc, 0
    n = 0
    cards = list(re.finditer(r'<a href="/blog/articles/([^"]+)" class="recommended-card">', doc))
    for m in cards:
        slug = m.group(1)
        exc = EXCERPTS.get(slug)
        if not exc:
            continue
        seg_end = doc.find('</a>', m.end())
        seg = doc[m.end():seg_end]
        new_seg, cnt = re.subn(r'(<p class="recommended-card-excerpt">)\s*(</p>)',
                               lambda mm: mm.group(1) + exc + mm.group(2), seg)
        if cnt:
            doc = doc[:m.end()] + new_seg + doc[seg_end:]
            n += cnt
    return doc, n


def main():
    for slug in SLUGS:
        for lang, pfx in (('en', ''), ('zh-cn', 'zh-cn/'), ('zh-tw', 'zh-tw/')):
            p = os.path.join(ROOT, pfx, 'blog/articles', slug + '.html')
            doc = open(p, encoding='utf-8').read()
            orig = doc
            doc, a = fix_faq_h3(doc)
            doc, b = dedupe_faq_numbers(doc)
            doc, c = fix_hrefs(doc, lang)
            doc, d = fix_cta_text(doc, lang)
            doc, e = fix_excerpts(doc, lang)
            if doc != orig:
                open(p, 'w', encoding='utf-8').write(doc)
            print(f"{slug:55s} {lang:6s} h3={a} num={b} href={c} cta={d} exc={e}")


if __name__ == '__main__':
    main()
