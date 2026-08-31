import os, re, json, sys

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/batches/batch_005.txt")) if l.strip()]

def inner_text_of(elem):
    # get text between <article ...> and </article> (or faq-section)
    return elem

def extract_block(html, tag_open, tag_close):
    # returns list of (start,end) for given tags (first level)
    out=[]
    i=0
    n=len(html)
    while True:
        s=html.find(tag_open, i)
        if s<0: break
        e=html.find(tag_close, s)
        if e<0: break
        out.append((s, e+len(tag_close)))
        i=e+len(tag_close)
    return out

def strip_tags(s):
    s=re.sub(r'<[^>]+>', ' ', s)
    s=re.sub(r'&[a-z]+;', ' ', s)
    s=re.sub(r'&#\d+;', ' ', s)
    return s

def cjk_count(s):
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', s))

results=[]
for slug in slugs:
    for lang, sub in [("EN","blog/articles"), ("zh-CN","zh-cn/blog/articles"), ("zh-TW","zh-tw/blog/articles")]:
        path=os.path.join(ROOT, sub, slug+".html")
        if not os.path.exists(path):
            results.append((slug,lang,"MISSING",0,0,0,False,False,False,0))
            continue
        html=open(path, encoding="utf-8").read()
        # article-content block
        m=re.search(r'<article class="article-content" id="article-content">(.*?)</article>', html, re.S)
        body = m.group(1) if m else html
        text = strip_tags(body)
        words = len(text.split())
        cjk = cjk_count(text)
        # FAQ items
        faq_items = len(re.findall(r'class="faq-item"', body))
        # CTA phrase
        cta_phrase = ("Book a Demo" if lang=="EN" else ("预约演示" if lang=="zh-CN" else "預約示範"))
        has_cta = cta_phrase in html
        # FAQPage JSON-LD present + valid + matches
        jsonlds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        faq_ld = None
        valid = False
        matches = False
        for j in jsonlds:
            try:
                d=json.loads(j)
            except Exception:
                continue
            if isinstance(d, dict) and d.get("@type")=="FAQPage":
                faq_ld=d
                valid=True
                # on-page questions
                page_qs=[strip_tags(x) for x in re.findall(r'class="faq-question-text"[^>]*>(.*?)</span>\s*</span>', body, re.S)]
                # simpler: extract faq question text spans
                break
        # recommended hrefs + empty excerpts
        rec_cards = re.findall(r'<a class="recommended-card" href="([^"]*)"', html)
        wrong_href=0
        for h in rec_cards:
            prefix = {"EN":"/blog/articles/","zh-CN":"/zh-cn/blog/articles/","zh-TW":"/zh-tw/blog/articles/"}[lang]
            if not h.startswith(prefix):
                wrong_href+=1
        empty_excerpt = len(re.findall(r'<p class="recommended-card-excerpt">\s*</p>', html))
        if lang=="EN":
            metric=words; target=2500; unit="words"
        else:
            metric=cjk; target=3500; unit="cjk"
        ok_len = metric>=target
        results.append((slug,lang,metric,target,unit,faq_items,valid,has_cta,wrong_href,empty_excerpt))

# print report
print(f"{'slug':52} {'lang':6} {'metric':>7} {'tgt':>5} {'FAQ':>3} {'LD':>3} {'CTA':>4} {'badH':>5} {'empE':>5}")
for r in results:
    slug,lang,metric,target,unit,faq,valid,cta,badh,empt = r
    if metric=="MISSING":
        print(f"{slug:52} {lang:6} MISSING")
        continue
    print(f"{slug:52} {lang:6} {metric:>7} {target:>5} {faq:>3} {('Y' if valid else 'N'):>3} {('Y' if cta else 'N'):>4} {badh:>5} {empt:>5}")
