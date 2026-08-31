import os, re
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT,"_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]
report = []
for slug in slugs:
    p = os.path.join(ROOT, "zh-tw/blog/articles", slug + ".html")
    if not os.path.exists(p):
        report.append(f"[MISSING] {slug}")
        continue
    html = open(p, encoding="utf-8").read()
    # fix CTA button text specifically
    new = re.sub(r'(<a [^>]*class="article-cta-btn">)(?:预约演示|預約演示)(</a>)', r'\1預約示範\2', html)
    # also catch any leftover anywhere (CTA only)
    new = new.replace('預約演示', '預約示範').replace('预约演示', '預約示範')
    if new != html:
        open(p, "w", encoding="utf-8").write(new)
    ok = ('預約示範' in new) and ('预约演示' not in new)
    report.append(f"{slug}: cta_fixed={new!=html} cta_ok={ok}")
for r in report:
    print(r)
