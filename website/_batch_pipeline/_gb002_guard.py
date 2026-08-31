#!/usr/bin/env python3
"""Guardrail verification for gbatch_002 edits (no baseline diff available)."""
import re, os, sys, html
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUGS = [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/gap_batches/gbatch_002.txt'),
                                 encoding='utf-8') if l.strip()]
LANGS = [("en", "blog/articles"), ("zh-cn", "zh-cn/blog/articles"), ("zh-tw", "zh-tw/blog/articles")]

problems = []
note = []


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


for slug in SLUGS:
    for lang, rel in LANGS:
        p = os.path.join(ROOT, rel, slug + '.html')
        f = '%s/%s' % (lang, slug)
        raw = open(p, encoding='utf-8').read()
        he = raw.find('</head>')
        head = raw[:he]

        # 1. versioned asset links intact
        for asset in ('/css/article.css?v=20260826', '/js/article.js?v=20260826'):
            if asset not in raw:
                problems.append('%s: MISSING versioned asset %s' % (f, asset))
        if re.search(r'href="/css/article\.css(?!\?v=20260826)', raw):
            problems.append('%s: unversioned css link' % f)
        if re.search(r'src="/js/article\.js(?!\?v=20260826)', raw):
            problems.append('%s: unversioned js link' % f)

        # 2. FAQPage JSON-LD must NOT have been added to head
        if '"FAQPage"' in head:
            note.append('%s: FAQPage LD in head (pre-existing, untouched)' % f)

        # 3. share buttons / footer present and intact
        for token in ('sidebar-share', 'article-share-btn', 'share-linkedin', 'share-x', 'share-copy'):
            if token not in raw:
                problems.append('%s: share token missing: %s' % (f, token))
        if raw.count('article-share-btn') != 3:
            problems.append('%s: expected 3 share buttons, found %d' % (f, raw.count('article-share-btn')))
        if '<footer' not in raw or '</footer>' not in raw:
            problems.append('%s: footer block missing' % f)

        # 4. recommended cards root-relative + language prefixed
        for m in re.finditer(r'<a class="recommended-card"[^>]*href="([^"]+)"', raw):
            href = m.group(1)
            want = '/blog/articles/' if lang == 'en' else '/%s/blog/articles/' % lang
            if not href.startswith(want):
                problems.append('%s: recommended-card href not language-prefixed: %s' % (f, href))
        for m in re.finditer(r'<a class="recommended-card"[^>]*>(.*?)</a>', raw, re.S):
            if 'recommended-card-excerpt' in m.group(1):
                ex = re.search(r'class="recommended-card-excerpt"[^>]*>(.*?)</', m.group(1), re.S)
                if ex and len(re.sub(r'<[^>]+>', '', ex.group(1)).strip()) < 20:
                    problems.append('%s: empty recommended-card-excerpt' % f)

        # 5. root-relative link sanity
        for m in re.finditer(r'href="(/[^"#]*)"', raw):
            h = m.group(1)
            if h.startswith(('/blog/', '/zh-cn/', '/zh-tw/', '/css/', '/js/', '/assets/')):
                if ' ' in h or h.endswith('/') is False and h.count('//') > 0:
                    problems.append('%s: malformed internal link %s' % (f, h))

        # 6. tag balance inside <article>
        a = raw.find('<article')
        e = raw.rfind('</article>')
        seg = raw[a:e]
        for tag in ('div', 'section', 'h2', 'h3', 'p', 'ul', 'ol', 'li', 'table', 'button', 'script'):
            o = len(re.findall(r'<%s[\s>]' % tag, seg))
            c = len(re.findall(r'</%s>' % tag, seg))
            if o != c:
                problems.append('%s: unbalanced <%s> open=%d close=%d' % (f, tag, o, c))

        # 7. no placeholder text
        low = raw.lower()
        for bad in ('lorem ipsum', 'todo', 'placeholder text', 'xxx xxx', 'coming soon'):
            if bad in low:
                problems.append('%s: placeholder text "%s"' % (f, bad))

        # 8. CTA
        phrase = {'en': 'Book a Demo', 'zh-cn': '预约演示', 'zh-tw': '預約示範'}[lang]
        if 'article-cta-btn' not in raw or phrase not in raw:
            problems.append('%s: CTA missing' % f)

        # 9. FAQ structure: >=3 items, h3 per question, LD right after FAQ close
        if 'faq-section' not in raw:
            problems.append('%s: no faq-section' % f)
            continue
        fs = re.search(r'<section[^>]*class="faq-section"[^>]*>', raw)
        depth, i = 1, fs.end()
        for mm in re.finditer(r'</?section\b', raw[i:], re.I):
            depth += -1 if raw[i + mm.start():].startswith('</') else 1
            if depth == 0:
                i = i + mm.start()
                break
        close = raw.find('>', i) + 1
        items = raw[fs.start():close].count('class="faq-item"')
        if items < 3:
            problems.append('%s: only %d FAQ items' % (f, items))
        after = raw[close:close + 400]
        if '"FAQPage"' not in after:
            problems.append('%s: FAQPage JSON-LD not immediately after FAQ section' % f)

print('GUARDRAIL REPORT — %d files checked' % (len(SLUGS) * 3))
if problems:
    print('\nPROBLEMS (%d):' % len(problems))
    for x in problems:
        print('  !', x)
else:
    print('\nAll guardrail checks passed.')
if note:
    print('\nNOTES (%d):' % len(note))
    for x in Counter(note).items():
        print('  -', x[0], 'x%d' % x[1])
sys.exit(1 if problems else 0)
