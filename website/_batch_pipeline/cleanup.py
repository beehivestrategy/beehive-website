import re, os

base = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = """retail-ai-dynamic-pricing-competitive-intelligence
enterprise-ai-adoption-trends-2026-what-data-reveals
computer-vision-quality-assurance
annual-data-governance-review-2025-dec
nlg-automated-insight-reports-executive
enterprise-ai-adoption-roi-measurement-jan2025
responsible-ai-operationalizing-ethics
data-marketplace-trends-enterprise-data
what-is-conversational-bi-chatbi-explained
enterprise-software-q4-2025-update-cycle
mcp-connectors-enterprise-ecosystem-q3-2025
embedding-analytics-in-collaboration-tools-a-2026-update
vector-search-patterns-for-enterprise-knowledge-bases-a-2026-update
natural-language-to-sql-how-modern-bi-engines-work-a-2026-update
enterprise-ai-budget-planning-2026-preparation""".strip().splitlines()

def dedupe(html):
    if html.count('</body>') <= 1:
        return html, False
    i = html.index('</body>')
    return html[:i] + '</body>\n</html>\n', True

report = []
for slug in slugs:
    for pre in ["zh-tw/blog/articles/"]:  # only tw needs dedupe per measure
        p = os.path.join(base, pre+slug+".html")
        h = open(p, encoding='utf-8').read()
        h, deduped = dedupe(h)
        # CTA fix for zh-TW
        cta_fixed = False
        if 'class="article-cta-btn">預約演示</a>' in h:
            h = h.replace('class="article-cta-btn">預約演示</a>', 'class="article-cta-btn">預約示範</a>')
            cta_fixed = True
        # also header/mobile 預約演示 left as-is (out of scope)
        if deduped or cta_fixed:
            open(p, 'w', encoding='utf-8').write(h)
        ver = '?v=20260826' in h
        report.append((slug, pre, deduped, cta_fixed, ver, h.count('</body>')))
    # cn CTA check (should be 预约演示)
    cp = os.path.join(base, "zh-cn/blog/articles/"+slug+".html")
    ch = open(cp, encoding='utf-8').read()
    cncta = ('class="article-cta-btn">预约演示</a>' in ch)
    report.append((slug, "zh-cn/blog/articles/", None, cncta, '?v=20260826' in ch, None))

for r in report:
    print(r)
