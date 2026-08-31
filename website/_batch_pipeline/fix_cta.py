import os, re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/batches/batch_005.txt")) if l.strip()]
langs = [("EN","blog/articles","Book a Demo"),
         ("zh-CN","zh-cn/blog/articles","预约演示"),
         ("zh-TW","zh-tw/blog/articles","預約示範")]

changed=[]
for slug in slugs:
    for lang, sub, phrase in langs:
        p=os.path.join(ROOT, sub, slug+".html")
        if not os.path.exists(p): continue
        h=open(p,encoding="utf-8").read()
        def repl(m):
            text=m.group(1)
            if phrase in text:
                return m.group(0)
            return m.group(0).replace('>'+text+'<', '>'+phrase+'<')
        newh, n = re.subn(r'<a [^>]*class="article-cta-btn"[^>]*>(.*?)</a>', repl, h, flags=re.S)
        if n>0 and newh!=h:
            open(p,"w",encoding="utf-8").write(newh)
            changed.append((slug,lang))
print("CTA fixed:", len(changed))
for c in changed: print(c)
