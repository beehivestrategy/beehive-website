# -*- coding: utf-8 -*-
import re, os, json
import opencc

base = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = "enterprise-ai-budget-planning-2026-preparation"
cc = opencc.OpenCC('s2twp.json')

def head_faq_items(path):
    h = open(path, encoding='utf-8').read()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        blk = m.group(1)
        if 'FAQPage' in blk:
            data = json.loads(blk)
            return [(q['name'], q['acceptedAnswer']['text']) for q in data['mainEntity']]
    raise SystemExit("no FAQPage in head of "+path)

def build_faq(items, title):
    out = ['<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">',
           '                <h2 class="faq-section-title">',
           '                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
           '                    ' + title,
           '                </h2>',
           '                <div class="faq-list">']
    for i, (q, a) in enumerate(items, 1):
        out.append('                    <div class="faq-item">')
        out.append('                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">')
        out.append('                            <span class="faq-question-text"><span class="faq-number">%d</span><span>%s</span></span>' % (i, q))
        out.append('                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>')
        out.append('                        </button></h3>')
        out.append('                        <div class="faq-answer" role="region"><div class="faq-answer-inner">%s</div></div>' % a)
        out.append('                    </div>')
    out.append('                </div>')
    out.append('            </section>')
    return "\n".join(out)

# EN expansion: new H2 + 2 paragraphs (~360 words)
EN_EXPAND = '''
<h2 id="what-does-a-realistic-2026-ai-budget-look-like">What Does a Realistic 2026 AI Budget Look Like in Practice?</h2>
<p>A useful rule of thumb is to ring-fence the 2026 budget into four buckets and weight them toward durability rather than novelty. Roughly 40% should go to data and platform foundations — the semantic layer, pipelines, and governance that every downstream use case depends on. About 25% should fund production deployments tied to a named business outcome, not experiments. Around 20% should cover adoption: training, change management, and the integration work that decides whether a tool is actually used. The remaining 15% can stay flexible for emerging models and opportunistic bets. Organizations that allocate this way avoid the common trap of funding impressive demos that never reach a P&amp;L line.</p>
<p>The second practical move is to budget for outcomes, not features. Tie each allocation to a metric the business already tracks — cost per resolved ticket, forecast accuracy, time-to-insight — and require a baseline before spend begins. When a line item cannot name its metric, it is a science project, and science projects are the first to be cut when the next review arrives. Done well, the 2026 budget reads less like a technology shopping list and more like a portfolio of bets, each with a defined return and a date by which it is measured.</p>'''

EN_TOC_MOBILE = '<a href="#what-does-a-realistic-2026-ai-budget-look-like" class="toc-mobile-link">What Does a Realistic 2026 AI Budget Look Like in Practice?</a>'
EN_TOC_SIDEBAR = '<a href="#what-does-a-realistic-2026-ai-budget-look-like" class="toc-link">What Does a Realistic 2026 AI Budget Look Like in Practice?</a>'

# EN
en_p = base + "/blog/articles/" + slug + ".html"
h = open(en_p, encoding='utf-8').read()
e = h.find('<nav class="article-nav"')
if 'faq-question-h3' not in h[:e]:
    h = h[:e] + EN_EXPAND + "\n" + build_faq(head_faq_items(en_p), "Frequently Asked Questions") + "\n" + h[e:]
    # TOC
    h = h.replace('class="toc-mobile-link">Implementation Roadmap and Key Success Factors</a>',
                  'class="toc-mobile-link">Implementation Roadmap and Key Success Factors</a>\n                    ' + EN_TOC_MOBILE, 1)
    h = h.replace('class="toc-link">Implementation Roadmap and Key Success Factors</a>',
                  'class="toc-link">Implementation Roadmap and Key Success Factors</a>\n                    ' + EN_TOC_SIDEBAR, 1)
    open(en_p, 'w', encoding='utf-8').write(h)
    print("EN: expanded + FAQ added")

# zh-CN
zh_p = base + "/zh-cn/blog/articles/" + slug + ".html"
h = open(zh_p, encoding='utf-8').read()
e = h.find('<nav class="article-nav"')
if 'faq-question-h3' not in h[:e]:
    h = h[:e] + "\n" + build_faq(head_faq_items(zh_p), "常见问题") + "\n" + h[e:]
    open(zh_p, 'w', encoding='utf-8').write(h)
    print("zh-CN: FAQ added")

# zh-TW
zhtw_p = base + "/zh-tw/blog/articles/" + slug + ".html"
h = open(zhtw_p, encoding='utf-8').read()
e = h.find('<nav class="article-nav"')
if 'faq-question-h3' not in h[:e]:
    h = h[:e] + "\n" + build_faq(head_faq_items(zhtw_p), "常見問題") + "\n" + h[e:]
    open(zhtw_p, 'w', encoding='utf-8').write(h)
    print("zh-TW: FAQ added")

print("slug15 done")
