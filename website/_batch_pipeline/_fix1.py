import os, re, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT,"_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]

LANGS = [("en","blog/articles"),("zh-CN","zh-cn/blog/articles")]

def read(p): return open(p, encoding="utf-8").read()
def write(p, s): open(p,"w",encoding="utf-8").write(s)

def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&[a-zA-Z#0-9]+;", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def extract_faq_items_balanced(section_html):
    items = []
    start = section_html.find('<div class="faq-list">')
    if start < 0:
        return items
    rest = section_html[start:]
    pos = rest.find('<div class="faq-item">')
    while pos >= 0:
        depth = 0
        i = pos
        end = -1
        while i < len(rest):
            if rest.startswith('<div', i):
                depth += 1
                i += 4
            elif rest.startswith('</div>', i):
                depth -= 1
                i += 6
                if depth == 0:
                    end = i
                    break
            else:
                i += 1
        if end < 0:
            break
        block = rest[pos:end]
        # question
        q = None
        if '<h3>' in block:
            qm = re.search(r'<h3>(.*?)</h3>', block, re.S)
            q = strip_tags(qm.group(1)) if qm else None
        else:
            qtm = re.search(r'<span class="faq-question-text">(.*?)</button>', block, re.S)
            if qtm:
                inner = qtm.group(1)
                inner = re.sub(r'<span class="faq-number">.*?</span>', '', inner, flags=re.S)
                inner = re.sub(r'<svg.*?</svg>', '', inner, flags=re.S)
                spans = re.findall(r'<span>(.*?)</span>', inner, re.S)
                q = strip_tags(spans[-1]) if spans else strip_tags(inner)
        # strip leading "N " duplicated number
        if q:
            q = re.sub(r'^\s*\d+\s+', '', q).strip()
        # answer
        ans = None
        am = re.search(r'<div class="faq-answer[^"]*">(.*)', block, re.S)
        if am:
            ans = strip_tags(am.group(1))
        if q and ans:
            items.append((q, ans))
        pos = rest.find('<div class="faq-item">', end)
    return items

def rebuild_faq_section(section_html, items):
    title_m = re.search(r'(<h2 class="faq-section-title">.*?</h2>)', section_html, re.S)
    title = title_m.group(1) if title_m else '<h2 class="faq-section-title">Frequently Asked Questions</h2>'
    out = []
    out.append('<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">')
    out.append("                " + title)
    out.append('                <div class="faq-list">')
    for q, a in items:
        out.append('                    <div class="faq-item">')
        out.append(f'                        <h3>{q}</h3>')
        out.append(f'                        <div class="faq-answer"><div class="faq-answer-inner">{a}</div></div>')
        out.append('                    </div>')
    out.append('                </div>')
    out.append('            </section>')
    return "\n".join(out)

def build_faq_ld(items):
    ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ]
    }
    return json.dumps(ld, ensure_ascii=False, indent=2)

def replace_or_add_faq_ld(html, new_json, has_faq_section):
    scripts = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    for m in scripts:
        if 'FAQPage' in m.group(1):
            return html[:m.start()] + '<script type="application/ld+json">' + new_json + '</script>' + html[m.end():], True
    if has_faq_section:
        ins = '\n<script type="application/ld+json">\n' + new_json + '\n</script>\n'
        pos = html.find('</section>', html.find('class="faq-section"'))
        if pos >= 0:
            return html[:pos+len('</section>')] + ins + html[pos+len('</section>'):], True
    return html, False

def fix_recommended(html, lang):
    prefix = {'en':'', 'zh-CN':'zh-cn', 'zh-TW':'zh-tw'}[lang]
    base = ('/' + prefix + '/blog/articles/') if prefix else '/blog/articles/'
    def repl_href(m):
        tag = m.group(0)
        hm = re.search(r'href="([^"]*)"', tag)
        if not hm: return tag
        href = hm.group(1)
        new = href
        if lang == 'en':
            if href.startswith('/zh-cn/blog/articles/') or href.startswith('/zh-tw/blog/articles/'):
                new = base + href.split('/blog/articles/')[-1]
            elif href.startswith('/blog/articles/'):
                new = href
            elif not href.startswith('/'):
                new = base + href
        else:
            if href.startswith('/blog/articles/'):
                new = base + href[len('/blog/articles/'):]
            elif href.startswith(('/zh-cn/blog/articles/','/zh-tw/blog/articles/')):
                new = base + href.split('/blog/articles/')[-1]
            elif not href.startswith('/'):
                new = base + href
        return tag.replace('href="%s"' % href, 'href="%s"' % new, 1)
    html = re.sub(r'<a class="recommended-card"[^>]*>', repl_href, html)
    lead_m = re.search(r'<p class="article-lead">(.*?)</p>', html, re.S)
    summary = ""
    if lead_m:
        txt = strip_tags(lead_m.group(1))
        for sep in ['. ', '。', '! ', '！']:
            i = txt.find(sep)
            if i > 0:
                summary = txt[:i+1].strip()
                break
        if not summary:
            summary = txt[:200]
    else:
        p_m = re.search(r'<p>(.*?)</p>', html, re.S)
        if p_m:
            summary = strip_tags(p_m.group(1))[:200]
    if summary:
        def repl_ex(m):
            tag = m.group(0)
            inner = re.sub(r'<[^>]+>', '', tag)
            if inner.strip() == "" or len(inner.strip()) < 5:
                return f'<p class="recommended-card-excerpt">{summary}</p>'
            return tag
        html = re.sub(r'<p class="recommended-card-excerpt">.*?</p>', repl_ex, html, flags=re.S)
    return html

if __name__ == "__main__":
    report = []
    for slug in slugs:
        for lang, sub in LANGS:
            p = os.path.join(ROOT, sub, slug + ".html")
            if not os.path.exists(p):
                report.append(f"[MISSING] {slug} {lang}")
                continue
            html = read(p)
            faq_sec_pos = html.find('class="faq-section"')
            if faq_sec_pos < 0:
                html = fix_recommended(html, lang)
                write(p, html)
                report.append(f"[NO-FAQ] {slug} {lang}: recommended fixed only")
                continue
            sec_start = html.rfind('<section', 0, faq_sec_pos)
            sec_end = html.find('</section>', faq_sec_pos)
            sec_block = html[sec_start:sec_end+len('</section>')]
            items = extract_faq_items_balanced(sec_block)
            if not items:
                report.append(f"[WARN] {slug} {lang}: faq items not parsed")
                continue
            new_sec = rebuild_faq_section(sec_block, items)
            html = html[:sec_start] + new_sec + html[sec_end+len('</section>'):]
            new_json = build_faq_ld(items)
            html, added = replace_or_add_faq_ld(html, new_json, True)
            html = fix_recommended(html, lang)
            write(p, html)
            report.append(f"[OK] {slug} {lang}: faq={len(items)} h3, ld_added={added}")
    for r in report:
        print(r)
