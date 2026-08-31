import os, re
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_003.txt")) if l.strip()]
def body_of(t):
    m = re.search(r'<article id="article-content">(.*)', t, re.S)
    return m.group(1) if m else t
for slug in slugs:
    print("==== ", slug)
    for lang, pref in [("EN","blog/articles"),("zh-CN","zh-cn/blog/articles"),("zh-TW","zh-tw/blog/articles")]:
        fp = os.path.join(ROOT, pref, slug+".html")
        t = open(fp, encoding="utf-8").read()
        hs = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_of(t), re.S)
        print("  --", lang)
        for i,x in hs:
            print("    %s || %s" % (i, re.sub(r'<[^>]+>','',x).strip()))
