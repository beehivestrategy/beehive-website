#!/usr/bin/env python3
"""Populate empty recommended-card-excerpt values (single pass, offset safe)."""
import os
import re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
SLUGS = [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/gap_batches/gbatch_002.txt')) if l.strip()]

EX = {
    ('en', 'women-in-data-building-inclusive-ai-teams'):
        'How gender-diverse data and AI teams make measurably better model and governance decisions, and the hiring practices that close the gap.',
    ('en', 'why-data-strategy-needs-ai-agent-layer-2026'):
        'Why an agent layer above the consumption layer turns a static data stack into one that answers questions and acts on them.',
    ('en', 'vector-databases-enterprise-search-2026-practical-guide'):
        'A practical guide to selecting, sizing and operating vector databases for enterprise-scale semantic search.',
    ('zh-cn', 'data-quality-automation-from-reactive-to-proactive-part-2'):
        '把数据质量从事后补救转向事前预防的自动化机制与落地路径。',
    ('zh-tw', 'data-quality-automation-from-reactive-to-proactive-part-2'):
        '把數據質量從事後補救轉向事前預防的自動化機制與落地路徑。',
    ('zh-tw', 'cfo-guide-ai-budget-allocation'):
        'CFO如何为AI预算分配建立可审计的资本配置与回报追踪机制。',
}


def fill(doc, lang):
    def repl(m):
        href = m.group(1)
        slug = href.split('/')[-1]
        exc = EX.get((lang, slug))
        if not exc:
            return m.group(0)
        body, cnt = re.subn(r'(<p class="recommended-card-excerpt">)\s*(</p>)',
                            lambda mm: mm.group(1) + exc + mm.group(2), m.group(0))
        return body
    return re.sub(r'<a href="([^"]*)" class="recommended-card">.*?</a>', repl, doc, flags=re.S)


for slug in SLUGS:
    for lang, pfx in (('en', ''), ('zh-cn', 'zh-cn/'), ('zh-tw', 'zh-tw/')):
        p = os.path.join(ROOT, pfx, 'blog/articles', slug + '.html')
        d = open(p, encoding='utf-8').read()
        nd = fill(d, lang)
        if nd != d:
            open(p, 'w', encoding='utf-8').write(nd)
            print('filled', lang, slug)
