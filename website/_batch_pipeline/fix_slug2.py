import re, os

base = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = "enterprise-ai-adoption-trends-2026-what-data-reveals"
files = {
    "en": f"blog/articles/{slug}.html",
    "cn": f"zh-cn/blog/articles/{slug}.html",
    "tw": f"zh-tw/blog/articles/{slug}.html",
}

def dedupe(html):
    # Keep only up to the first </body>, re-add proper closing
    cnt = html.count('</body>')
    if cnt <= 1:
        return html, cnt
    i = html.index('</body>')
    return html[:i] + '</body>\n</html>\n', cnt

for lang, rel in files.items():
    p = os.path.join(base, rel)
    h = open(p, encoding='utf-8').read()
    h2, cnt = dedupe(h)
    changed = (h2 != h)
    if changed:
        open(p, 'w', encoding='utf-8').write(h2)
    # zh-TW CTA phrase fix (target article-cta-btn only)
    if lang == 'tw':
        if 'class="article-cta-btn">預約演示</a>' in h2:
            h2 = h2.replace('class="article-cta-btn">預約演示</a>', 'class="article-cta-btn">預約示範</a>')
            open(p, 'w', encoding='utf-8').write(h2)
            print("zh-TW CTA fixed to 預約示範")
    # report
    cjk = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', h2))
    faq = h2.count('faq-question-h3')
    faqld = h2.count('FAQPage')
    head_v = ('?v=20260826' in h2)
    print(f"{lang}: </body> count={cnt} (deduped={changed}), CJK={cjk}, faqH3={faq}, FAQPage={faqld}, cssVerOK={head_v}")
