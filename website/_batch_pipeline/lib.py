import os, re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def read(slug, sub):
    return open(os.path.join(ROOT, sub, slug+".html"), encoding="utf-8").read()

def write(slug, sub, html):
    open(os.path.join(ROOT, sub, slug+".html"), "w", encoding="utf-8").write(html)

def extract_h2s(block):
    out=[]
    for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', block, re.S):
        out.append((m.group(1), re.sub(r'<[^>]+>','',m.group(2)).strip()))
    return out

def inject_expansion(html, expansion):
    """Insert expansion before faq-section if present, else before recommended-section.
       Also insert matching TOC links into .toc-links and .toc-mobile-links."""
    h2s = extract_h2s(expansion)
    # find insertion anchor
    faq = re.search(r'<section class="faq-section"', html)
    if faq:
        anchor = faq.start()
        pre = html[:anchor]
        post = html[anchor:]
    else:
        # no faq-section: insert INSIDE article-content, before its closing tag
        rec = re.search(r'</article>', html)
        anchor = rec.start()
        pre = html[:anchor]
        post = html[anchor:]
    new_html = pre + "\n" + expansion + "\n" + post
    # TOC updates
    for hid, htext in h2s:
        link = f'<a href="#{hid}" class="toc-link">{htext}</a>'
        mlink = f'<a href="#{hid}" class="toc-mobile-link">{htext}</a>'
        # toc-links nav (sidebar)
        toc = re.search(r'(<nav class="toc-links">)(.*?)(</nav>)', new_html, re.S)
        if toc and link not in toc.group(2):
            new_html = new_html[:toc.start(2)] + toc.group(2) + "                    " + link + "\n" + new_html[toc.end(2):]
        # toc-mobile-links
        tm = re.search(r'(<div class="toc-mobile-links">)(.*?)(</div>)', new_html, re.S)
        if tm and mlink not in tm.group(2):
            new_html = new_html[:tm.start(2)] + tm.group(2) + "                    " + mlink + "\n" + new_html[tm.end(2):]
    return new_html

def add_faq_section(html, faq_html):
    """Insert FAQ section (with .faq-section) INSIDE article-content if not present."""
    if re.search(r'class="faq-section"', html):
        return html, False
    # insert before article-content closing </article> (after the conclusion)
    art = re.search(r'</article>', html)
    if not art:
        return html, False
    anchor = art.start()
    return html[:anchor] + "\n" + faq_html + "\n" + html[anchor:], True

def inject_jsonld_in_head(html, jsonld):
    """Add a FAQPage JSON-LD script into <head> if not already present (match by @type FAQPage)."""
    if re.search(r'"@type"\s*:\s*"FAQPage"', html):
        return html, False
    # insert before </head>
    idx = html.rfind("</head>")
    if idx<0: idx = html.rfind("</body>")
    script = '<script type="application/ld+json">'+jsonld+'</script>\n'
    return html[:idx] + script + html[idx:], True

def count_words(s):
    s=re.sub(r'<[^>]+>',' ',s); s=re.sub(r'&[a-z]+;',' ',s); s=re.sub(r'&#\d+;',' ',s)
    return len(s.split())

def cjk_count(s):
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', s))

def article_metric(html, lang):
    m=re.search(r'<article class="article-content" id="article-content">(.*?)</article>', html, re.S)
    body=m.group(1) if m else html
    return count_words(body) if lang=="EN" else cjk_count(body)
