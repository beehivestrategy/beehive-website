import re, sys, html
def measure(path):
    with open(path, encoding='utf-8') as f:
        src = f.read()
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', src, re.S)
    if not m:
        return None
    body = m.group(1)
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', body)
    text = html.unescape(text)
    en_words = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", text))
    cjk = len(re.findall(r'[\u4e00-\u9fff]', text))
    faq = len(re.findall(r'class="faq-section"', src))
    faq_q = len(re.findall(r'<h3', m.group(1)))
    jsonld = len(re.findall(r'"@type"\s*:\s*"FAQPage"', src))
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)
    cta = 'article-cta-btn' in src
    return dict(en=en_words, cjk=cjk, faq_sections=faq, h3_in_article=faq_q, faqpage_jsonld=jsonld, cta=cta, h2s=[re.sub(r'<[^>]+>','',h).strip()[:60] for h in h2s])
for p in sys.argv[1:]:
    r = measure(p)
    if r is None:
        print(p, "NO article-content")
    else:
        print(p.split('/')[-3] + '/' + p.split('/')[-1], "| en:", r['en'], "| cjk:", r['cjk'], "| faq-sec:", r['faq_sections'], "| h3:", r['h3_in_article'], "| FAQPage jsonld:", r['faqpage_jsonld'], "| cta:", r['cta'])
        for h in r['h2s']:
            print("   H2:", h)
