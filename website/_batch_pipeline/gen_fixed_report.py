import json, os, html, datetime

PIPE = os.path.dirname(os.path.abspath(__file__))

# Full universe = status.json slugs (1,061). Gaps = audit not_ok (771).
status = json.load(open(os.path.join(PIPE, "status.json")))
audit = json.load(open(os.path.join(PIPE, "gaps_audit.json")))

all_slugs = list(status["slugs"].keys())
not_ok = set(audit.get("not_ok", []))
ok = sorted([s for s in all_slugs if s not in not_ok])

BASE = "https://www.beehivestrategy.com"
rows = []
for s in ok:
    en = f"{BASE}/blog/articles/{s}.html"
    cn = f"{BASE}/zh-cn/blog/articles/{s}.html"
    tw = f"{BASE}/zh-tw/blog/articles/{s}.html"
    rows.append(
        f'<tr><td><code>{html.escape(s)}</code></td>'
        f'<td><a href="{en}" target="_blank" rel="noopener">EN</a></td>'
        f'<td><a href="{cn}" target="_blank" rel="noopener">简</a></td>'
        f'<td><a href="{tw}" target="_blank" rel="noopener">繁</a></td></tr>'
    )

n = len(ok)
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M HKT")
doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Beehive Blog — Fixed Articles ({n})</title>
<style>
body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:2rem;background:#0a0e0d;color:#f0f0f0}}
h1{{color:#3dd4b0}} table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid #1e7a6b;padding:6px 10px;text-align:left;vertical-align:top}}
a{{color:#3dd4b0;text-decoration:none}} a:hover{{text-decoration:underline}}
code{{color:#f0d78c;font-size:12px}} .meta{{color:#8a9e96;margin-bottom:1rem}}
</style></head>
<body><h1>Beehive Blog — Articles Brought to GEO Standard</h1>
<div class="meta">{n} of 1,061 slugs fully at standard (all 3 languages: EN / zh-CN / zh-TW) as of {now}.
Source: content audit (audit_content.py) minus {len(not_ok)} gap slugs. Click any link to open the live article.</div>
<table><thead><tr><th>Slug</th><th>EN</th><th>简体</th><th>繁體</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody></table></body></html>"""
out = os.path.join(PIPE, "fixed_articles_report.html")
open(out, "w").write(doc)
print("wrote", n, "fixed articles to", out)
