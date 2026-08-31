import os, re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/batches/batch_005.txt")) if l.strip()]

langs = [("EN","blog/articles","Book a Demo"),
         ("zh-CN","zh-cn/blog/articles","预约演示"),
         ("zh-TW","zh-tw/blog/articles","預約示範")]

def read_lead(slug, sub):
    p=os.path.join(ROOT, sub, slug+".html")
    if not os.path.exists(p): return ""
    h=open(p,encoding="utf-8").read()
    m=re.search(r'id="article-content">(.*?)</article>', h, re.S)
    ac=m.group(1) if m else h
    lead=None
    lead=re.search(r'<p class="article-lead">(.*?)</p>', ac, re.S)
    if not lead:
        lead=re.search(r'<p[^>]*>(.*?)</p>', ac, re.S)
    if not lead: return ""
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',lead.group(1))).strip()

def first_sentence(t, maxlen=160):
    s=re.split(r'(?<=[.!?。！？])\s', t)
    first=s[0] if s else t
    if len(first)>maxlen:
        first=first[:maxlen-3].rsplit(' ',1)[0]+'…'
    return first.strip()

def fill_excerpts(html, sub):
    out=[]
    last=0
    pat=re.compile(r'<a href="([^"]*)" class="recommended-card"')
    for m in pat.finditer(html):
        start=m.start()
        end=html.find('</a>', m.end())
        if end<0:
            out.append(html[last:]); last=len(html); break
        card=html[start:end+4]
        href=m.group(1)
        if re.search(r'<p class="recommended-card-excerpt">\s*</p>', card):
            mslug=href.rstrip('/').split('/')[-1].replace('.html','')
            lead=read_lead(mslug, sub)
            if lead:
                card=re.sub(r'(<p class="recommended-card-excerpt">)\s*(</p>)',
                            lambda x: x.group(1)+first_sentence(lead)+x.group(2), card, count=1)
        out.append(html[last:start])
        out.append(card)
        last=end+4
    out.append(html[last:])
    return ''.join(out)

def fix_cta(html, phrase):
    if phrase in html:
        return html, False
    m=re.search(r'<a href="/contact" class="article-cta-btn">.*?</a>', html, re.S)
    if m:
        new='<a href="/contact" class="article-cta-btn">'+phrase+'</a>'
        html=html[:m.start()]+new+html[m.end():]
        return html, True
    return html, False

changed=[]
for slug in slugs:
    for lang, sub, phrase in langs:
        p=os.path.join(ROOT, sub, slug+".html")
        if not os.path.exists(p): continue
        h=open(p,encoding="utf-8").read()
        h2=fill_excerpts(h, sub)
        h2,ctad=fix_cta(h2, phrase)
        if h2!=h:
            open(p,"w",encoding="utf-8").write(h2)
            changed.append((slug,lang,"CTA" if ctad else "EXC"))
print("Changed:",len(changed))
for c in changed: print(c)
