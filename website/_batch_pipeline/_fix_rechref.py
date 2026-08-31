import re, os

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = open(os.path.join(ROOT, "_batch_pipeline/batches/batch_007.txt"), encoding="utf-8").read().split()

files = {}
for slug in slugs:
    files[("en", slug)]   = os.path.join(ROOT, f"blog/articles/{slug}.html")
    files[("zh-cn", slug)]= os.path.join(ROOT, f"zh-cn/blog/articles/{slug}.html")
    files[("zh-tw", slug)]= os.path.join(ROOT, f"zh-tw/blog/articles/{slug}.html")

# for each (lang, slug) the recommended prefix
prefix = {"en":"/blog/articles/", "zh-cn":"/zh-cn/blog/articles/", "zh-tw":"/zh-tw/blog/articles/"}

def fix(path, lang):
    h = open(path, encoding="utf-8").read()
    new = h
    # match each recommended-card anchor and rewrite its href
    def repl(m):
        full = m.group(0)
        hrefm = re.search(r'href="([^"]*)"', full)
        old = hrefm.group(1)
        seg = old.rstrip("/").split("/")[-1]
        # only rewrite if it looks like an article slug path
        newhref = prefix[lang] + seg
        return full[:hrefm.start()] + f'href="{newhref}"' + full[hrefm.end():]
    new, n = re.subn(r'<a[^>]*class="recommended-card"[^>]*>', repl, new)
    # also handle order href before class
    if n == 0:
        new, n = re.subn(r'<a[^>]*href="[^"]*"[^>]*class="recommended-card"[^>]*>', repl, new)
    if n:
        open(path, "w", encoding="utf-8").write(new)
    return n

total = 0
for (lang, slug), p in files.items():
    if os.path.exists(p):
        n = fix(p, lang)
        if n:
            total += n
            print(f"{lang} {slug}: fixed {n} rec hrefs")
print("TOTAL rec href fixes:", total)
