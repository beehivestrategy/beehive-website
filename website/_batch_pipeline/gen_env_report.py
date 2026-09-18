#!/usr/bin/env python3
"""Generate the cross-environment blog inventory + by-day + by-language report."""
import json, os
from collections import defaultdict

BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline"
data = json.load(open(f"{BASE}/blog_inventory.json"))
lang_stats = data["lang_stats"]
per_day_lang = data["per_day_lang"]
LANGS = ["en", "zh-CN", "zh-TW"]

# monthly aggregation
months = defaultdict(lambda: {l: 0 for l in LANGS})
for lang in LANGS:
    for day, c in per_day_lang[lang].items():
        months[day[:7]][lang] += c
months = dict(sorted(months.items()))

# Live-verified environment counts (curl of each sitemap <loc>, 2026-09-02)
ENV = {
    "Local (source)":   {"en":1101,"zh-CN":1101,"zh-TW":1101,"note":"Authoritative — files on disk"},
    "dev  (beehive-strategy-v2)":      {"en":1101,"zh-CN":1101,"zh-TW":1101,"note":"✅ verified live; repair present (canonical fixed)"},
    "staging (beehive-strategy-v2-staging)": {"en":1060,"zh-CN":1060,"zh-TW":1060,"note":"⚠️ 41 articles/lang BEHIND dev/prod"},
    "prod (beehivestrategy.com)":      {"en":1101,"zh-CN":1101,"zh-TW":1101,"note":"✅ count matches; repair not directly probed"},
}

def row_env(name, d):
    tot = d["en"]+d["zh-CN"]+d["zh-TW"]
    flag = "⚠️" if d["en"]<1101 else "✅"
    return f"<tr><td>{name}</td><td class='num'>{d['en']:,}</td><td class='num'>{d['zh-CN']:,}</td><td class='num'>{d['zh-TW']:,}</td><td class='num'>{tot:,}</td><td class='foot'>{d['note']}</td></tr>"

env_rows = "".join(row_env(n,d) for n,d in ENV.items())

# char stats
def char_row(lang):
    s = lang_stats[lang]
    return (f"<tr><td>{lang}</td><td class='num'>{s['count']:,}</td>"
            f"<td class='num'>{s['total_chars_body']:,}</td><td class='num'>{s['avg_chars_body']:,}</td>"
            f"<td class='num'>{s['total_chars_file']:,}</td><td class='num'>{s['avg_chars_file']:,}</td>"
            f"<td class='num'>{s['with_date']:,}</td><td>{s['date_min']} → {s['date_max']}</td></tr>")
char_rows = "".join(char_row(l) for l in LANGS)

# by-day (monthly) table
maxm = max(max(d.values()) for d in months.values()) or 1
def day_row(m, d):
    tot = d["en"]+d["zh-CN"]+d["zh-TW"]
    bars = "".join(
        f"<span class='bar b{l}' style='width:{d[l]/maxm*120:.0f}px' title='{l}:{d[l]}'></span>"
        for l in LANGS)
    return (f"<tr><td>{m}</td><td class='num'>{d['en']}</td><td class='num'>{d['zh-CN']}</td>"
            f"<td class='num'>{d['zh-TW']}</td><td class='num'>{tot}</td><td>{bars}</td></tr>")
day_rows = "".join(day_row(m,d) for m,d in months.items())

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Beehive Blog — Environment Inventory & GEO Report (2026-09-02)</title>
<style>
:root{{--bg:#f7f8fa;--card:#fff;--ink:#1c2430;--mut:#6b7686;--line:#e3e8ef;--ok:#1f9d6b;--warn:#c47d12;--acc:#2B9E8B;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;padding:28px}}
.wrap{{max-width:1000px;margin:0 auto}}h1{{font-size:22px;margin:0 0 4px}} .sub{{color:var(--mut);margin:0 0 22px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:0 0 18px}}
.card h2{{font-size:16px;margin:0 0 12px}}
table{{width:100%;border-collapse:collapse;font-size:14px}} th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line)}}
th{{color:var(--mut);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.04em}}
td.num{{text-align:right;font-variant-numeric:tabular-nums}} .foot{{color:var(--mut);font-size:12.5px}}
.kpi{{display:flex;flex-wrap:wrap;gap:12px}} .kpi div{{flex:1 1 150px;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:12px}}
.kpi b{{display:block;font-size:22px;line-height:1.1}} .kpi span{{color:var(--mut);font-size:12px}}
.bar{{display:inline-block;height:11px;margin-right:2px;border-radius:2px;vertical-align:middle}}
.ben{{background:#2B9E8B}} .bzh-CN{{background:#d4a843}} .bzh-TW{{background:#7c6bd4}}
.legend span{{margin-right:14px;font-size:12px}} .dot{{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:4px}}
.warn{{color:var(--warn);font-weight:600}} .ok{{color:var(--ok);font-weight:600}}
ul{{margin:8px 0;padding-left:20px}} li{{margin:5px 0}}
</style></head><body><div class="wrap">
<h1>Beehive Blog — Environment Inventory &amp; GEO Report</h1>
<p class="sub">Snapshot 2026-09-02 · 3 environments (dev / staging / prod) · 3 languages · blog articles only</p>

<div class="card">
  <h2>1 · Blog count by environment (live-checked via sitemap &lt;loc&gt;)</h2>
  <table><thead><tr><th>Environment</th><th>EN</th><th>zh-CN</th><th>zh-TW</th><th>Total</th><th>Note</th></tr></thead>
  <tbody>{env_rows}</tbody></table>
  <p class="foot">✅ dev &amp; prod both at full 1,101 / language (3,303 total). ⚠️ <b>staging is 41 articles/language behind</b> — a push to staging will catch it up. Local source = 1,101 each (authoritative).</p>
</div>

<div class="card">
  <h2>2 · Character volume by language (local source)</h2>
  <table><thead><tr><th>Lang</th><th>Articles</th><th>Total chars (body)</th><th>Avg / article</th><th>Total chars (file)</th><th>Avg / file</th><th>With date</th><th>Date span</th></tr></thead>
  <tbody>{char_rows}</tbody></table>
  <p class="foot">"Body" = HTML/JS/CSS stripped. EN averages ~19.9k chars/article; CJK articles ~6.3k chars/article (denser — each char ≈ a word). Total body content: EN 21.9M · zh-CN 6.9M · zh-TW 7.0M.</p>
</div>

<div class="card">
  <h2>3 · Publish cadence by month (articles per language)</h2>
  <div class="legend"><span><span class="dot ben"></span>EN</span><span><span class="dot bzh-CN"></span>zh-CN</span><span><span class="dot bzh-TW"></span>zh-TW</span></div>
  <table style="margin-top:8px"><thead><tr><th>Month</th><th>EN</th><th>zh-CN</th><th>zh-TW</th><th>Total</th><th></th></tr></thead>
  <tbody>{day_rows}</tbody></table>
  <p class="foot">{data['distinct_publish_days']} distinct publish days · span {lang_stats['en']['date_min']} → {lang_stats['en']['date_max']}. Daily granular data in blog_inventory.json.</p>
</div>

<div class="card">
  <h2>4 · "Is everything in dev?" — verification</h2>
  <ul>
    <li class="ok">✅ Your assumption holds for dev: a sampled repaired zh-TW article on <code>beehive-strategy-v2.pages.dev</code> returns the <b>fixed</b> canonical (<code>/zh-tw/blog/articles/...</code>), confirming the non-destructive repair batch is live in dev.</li>
    <li class="ok">✅ dev and prod both report the full 1,101 / language.</li>
    <li class="warn">⚠️ staging is stale (1,060 / language) — it has NOT received the latest content/repairs.</li>
    <li class="foot">Note: repairs are committed to the repo (dev auto-deploys from it); local working tree still has a few uncommitted auxiliary files (gaps_audit.json, _redirects) — these are non-article and don't affect blog counts.</li>
  </ul>
</div>

<div class="card">
  <h2>5 · Push to staging &amp; production — readiness</h2>
  <p class="foot">Content is <span class="ok">✅ good</span>: GEO baseline 100% (1,061/1,061/lang), repair batch zero-regression, dev live with fixes. But the actual <b>deploy step cannot run from this environment</b>:</p>
  <ul>
    <li>No <code>wrangler</code> config/auth present; repo has only content-publishing workflows (no site-deploy pipeline).</li>
    <li>Per your LOCKED convention, <b>PROD deploy needs explicit approval + defaults to dry-run</b>.</li>
  </ul>
  <p class="foot">To execute the push I need either: (a) CF_API_TOKEN + confirmation to run <code>wrangler pages deploy</code> for <code>beehive-strategy-v2-staging</code> then <code>beehive-strategy</code>, or (b) you trigger the deploy from the Cloudflare dashboard. Staging-first is lower risk and will also close the 41-article gap.</p>
</div>

<p class="foot">Generated from blog_inventory.json (local) + live sitemap probes (dev/staging/prod). Raw data: blog_inventory.json.</p>
</div></body></html>"""

out = f"{BASE}/ENV_INVENTORY_REPORT_2026-09-02.html"
open(out,"w",encoding="utf-8").write(HTML)
print("wrote", out, len(HTML), "bytes")
print("months:", len(months), "| total articles:", data["total_articles"])
