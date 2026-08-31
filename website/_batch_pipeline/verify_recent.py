import os, re, glob, sys
from datetime import datetime, timedelta

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
dirs = ["blog/articles", "zh-cn/blog/articles", "zh-tw/blog/articles"]
cutoff = datetime.now() - timedelta(minutes=120)

def cjk_count(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))

def word_count(s):
    return len(re.findall(r"[A-Za-z0-9]+", s))

results = []
for d in dirs:
    base = os.path.join(ROOT, d)
    for fp in glob.glob(os.path.join(base, "*.html")):
        try:
            mt = datetime.fromtimestamp(os.path.getmtime(fp))
        except:
            continue
        if mt < cutoff:
            continue
        with open(fp, encoding="utf-8") as f:
            html = f.read()
        m = re.search(r'<article id="article-content">(.*?)</article>', html, re.S)
        body = m.group(1) if m else html
        text = re.sub(r"<[^>]+>", "", body)
        if d.startswith("zh"):
            n = cjk_count(text)
            metric = f"CJK={n} (need>=3500)"
            ok = n >= 3500
        else:
            n = word_count(text)
            metric = f"words={n} (need>=2500)"
            ok = n >= 2500
        faq = len(re.findall(r'class="faq-question"', html)) or len(re.findall(r'faq-item', html))
        jld = '"FAQPage"' in html or '"@type": "FAQPage"' in html or '"@type":"FAQPage"' in html
        cta = "article-cta-btn" in html
        ver = "?v=20260826" in html
        status = "OK" if (ok and faq >= 3 and jld and cta and ver) else "GAP"
        results.append((fp.replace(ROOT+"/",""), status, metric, f"faq={faq}", "jld" if jld else "NO-JLD", "cta" if cta else "NO-CTA", "ver" if ver else "NO-VER"))

print(f"Checked {len(results)} recently-modified files\n")
gaps = [r for r in results if r[1] == "GAP"]
print(f"PASS={len(results)-len(gaps)}  GAP={len(gaps)}\n")
if gaps:
    print("=== GAPS ===")
    for r in gaps:
        print(" | ".join(r))
# show a few EN/zh samples
print("\n=== sample (first 8) ===")
for r in results[:8]:
    print(" | ".join(r))
