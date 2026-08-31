import re, sys
import opencc

cn = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/zh-cn/blog/articles/enterprise-ai-adoption-trends-2026-what-data-reveals.html"
tw = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/zh-tw/blog/articles/enterprise-ai-adoption-trends-2026-what-data-reveals.html"

cc = opencc.OpenCC('s2twp.json')

def extract_body(html):
    start = html.index('<article class="article-content" id="article-content">') + len('<article class="article-content" id="article-content">')
    end = html.rindex('</article>')
    return html[start:end]

cn_html = open(cn, encoding='utf-8').read()
tw_html = open(tw, encoding='utf-8').read()

cn_body = extract_body(cn_html)
tw_body_old = extract_body(tw_html)

# convert CJK in cn_body to Traditional
tw_body_new = cc.convert(cn_body)
# fix CTA phrase (zh-TW standard)
tw_body_new = tw_body_new.replace('預約演示', '預約示範')

new_tw = tw_html[:tw_html.index('<article class="article-content" id="article-content">') + len('<article class="article-content" id="article-content">')] + tw_body_new + tw_html[tw_html.rindex('</article>'):]

open(tw, 'w', encoding='utf-8').write(new_tw)

def cjk(s):
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', s))

before = cjk(tw_body_old)
after = cjk(tw_body_new)
faq = tw_body_new.count('faq-question-h3')
cta = ('預約示範' in tw_body_new)
print("zh-TW CJK before:", before, "after:", after)
print("faq H3 count:", faq, "CTA 預約示範 present:", cta)
print("contains 預約演示 leftover:", '預約演示' in tw_body_new)
