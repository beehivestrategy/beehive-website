import re, os
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT,'_batch_pipeline/gap_batches/gbatch_003.txt')) if l.strip()]
paths = {'EN':'blog/articles/%s.html','zh-CN':'zh-cn/blog/articles/%s.html','zh-TW':'zh-tw/blog/articles/%s.html'}
BF = re.compile(r'<h2 id="([^"]*)">(常见问题|常見問題|Frequently asked questions|Frequently Asked Questions)</h2>\s*((?:<p><strong>.*?</strong>.*?</p>\s*)+)', re.S)
PHRASE = {'EN':'Book a Demo','zh-CN':'预约演示','zh-TW':'預約示範'}
for s in slugs:
    out=[]
    for lang,tpl in paths.items():
        p=os.path.join(ROOT,tpl%s)
        h=open(p,encoding='utf-8').read()
        m=BF.search(h)
        # css/js version
        v_ok = '/css/article.css?v=20260826' in h and '/js/article.js?v=20260826' in h
        rel_hrefs = re.findall(r'href="(?!https?://|/|#)([^"]+)"', h)
        rel_hrefs = [x for x in rel_hrefs if 'blog/articles' in x or x in ('contact','solution','services','pricing','about','case-studies','industries')]
        nfaq_btn = h.count('class="faq-question"')
        out.append(f"{lang}: bodyfaq={'Y' if m else 'N'} faqitems={nfaq_btn} phrase={'Y' if PHRASE[lang] in h else 'N'} v={v_ok} rel={sorted(set(rel_hrefs))[:2]} nrel={len(rel_hrefs)}")
    print(s,'|',' || '.join(out))
