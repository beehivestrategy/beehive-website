import os, re, subprocess, json
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT,"_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]

def opencc_convert(text):
    p = subprocess.run(["opencc","-c","s2twp"], input=text.encode("utf-8"),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode())
    return p.stdout.decode("utf-8")

def count_cjk(s):
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', s))

report = []
for slug in slugs:
    src = os.path.join(ROOT, "zh-cn/blog/articles", slug + ".html")
    dst = os.path.join(ROOT, "zh-tw/blog/articles", slug + ".html")
    if not os.path.exists(src):
        report.append(f"[MISSING SRC] {slug}")
        continue
    html = open(src, encoding="utf-8").read()
    tw = opencc_convert(html)
    # fix recommended-card hrefs to /zh-tw/blog/articles/
    def repl(m):
        tag = m.group(0)
        hm = re.search(r'href="([^"]*)"', tag)
        if not hm: return tag
        href = hm.group(1)
        new = href
        if href.startswith("/zh-cn/blog/articles/"):
            new = "/zh-tw/blog/articles/" + href[len("/zh-cn/blog/articles/"):]
        elif href.startswith("/blog/articles/"):
            new = "/zh-tw/blog/articles/" + href[len("/blog/articles/"):]
        return tag.replace('href="%s"' % href, 'href="%s"' % new, 1)
    tw = re.sub(r'<a class="recommended-card"[^>]*>', repl, tw)
    # set faq aria-label to traditional
    tw = tw.replace('<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">',
                    '<section class="faq-section" id="faq" aria-label="常見問題">')
    open(dst, "w", encoding="utf-8").write(tw)
    # verify
    faq_items = len(re.findall(r'<h3>', tw))
    faq_ld = '"FAQPage"' in tw or '"@type":"FAQPage"' in tw
    cjk = count_cjk(tw)
    cta_ok = ("預約示範" in tw) and ("预约演示" not in tw)
    s_cjk = count_cjk(html)
    report.append(f"{slug}: zhTW cjk={cjk} (zhCN={s_cjk}) h3={faq_items} faq_ld={faq_ld} cta_ok={cta_ok}")

for r in report:
    print(r)
