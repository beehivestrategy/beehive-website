#!/usr/bin/env python3
"""Generate merged SEO+GEO audit & env-sync HTML report (2026-09-02)."""
import json, os, html, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "seo-geo-audit-sync-2026-09-02.html")

def load(name):
    p = os.path.join(BASE, name)
    with open(p, encoding="utf-8") as f:
        return json.load(f)

gaps = load("gaps_audit.json")
deep = load("deep_audit.json")

# ---------- staging missing slugs (41, batch 08-18 ~ 09-02) ----------
STAGING_MISSING = sorted("""
ai-analytics-commercial-real-estate-2026
ai-budget-planning-fy2027-cfo-playbook
ai-credit-risk-modeling-banks-2026
ai-demand-forecasting-retail-q4-2026
ai-knowledge-management-professional-services
ai-pilot-to-production-benchmarks-2026
ai-regulation-q3-2026-global-update
ai-supply-chain-control-tower-2026
ai-underwriting-claims-insurance-2026
ai-vendor-risk-assessment-framework
analytics-engineer-role-ai-era
analytics-team-playbook-conversational-bi
build-vs-buy-conversational-bi-2026
ceo-guide-enterprise-ai-2027
chief-data-officer-roadmap-2027
china-enterprise-ai-adoption-september-2026
cio-framework-choosing-ai-analytics-platform
conversational-analytics-energy-sector
conversational-bi-roi-business-case
conversational-bi-vs-dashboards-compared
coo-guide-ai-operations-excellence
data-pipeline-orchestration-tools-compared-2026
data-warehouse-vs-lakehouse-2026
enterprise-ai-funding-ma-q3-2026
enterprise-ai-trends-september-2026-month-ahead
enterprise-ai-vendor-landscape-q4-2026
enterprise-data-ai-outlook-october-2026
excel-vs-conversational-bi-finance-teams
finance-controllers-ai-month-end-close
fintech-ai-compliance-automation-2026
hong-kong-ai-adoption-index-september-2026
hong-kong-gba-ai-policy-september-2026
im-native-bi-vs-portal-wechat-dingtalk-feishu
manufacturing-demand-sensing-real-time-ai
markdown-optimization-ai-retail-q4
mcp-ecosystem-september-2026-update
mcp-vs-custom-integrations-2026
predictive-maintenance-roi-manufacturing-2026
rag-vs-fine-tuning-enterprise-choice
self-service-analytics-governance-balance
text-to-sql-accuracy-benchmark-2026
""".split())
assert len(STAGING_MISSING) == 41, len(STAGING_MISSING)

# ---------- gaps ----------
agg = gaps.get("agg", {})
not_ok = gaps.get("not_ok", [])

# ---------- deep audit summary ----------
summ = deep.get("summary", {})
per_lang = summ.get("per_lang", {})
sev = summ.get("severity_counts", {})

LANGS = [("en", "EN"), ("cn", "zh-CN"), ("tw", "zh-TW")]

def sev_rows(lang_key):
    rows = ""
    d = sev.get(lang_key, {})
    for k in sorted(d, key=lambda x: -d[x]):
        n = d[k]
        badge = "b-ok" if n == 0 else ("b-warn" if n <= 30 else "b-bad")
        rows += f'<tr><td>{html.escape(k)}</td><td><span class="badge {badge}">{n}</span></td></tr>'
    return rows

gap_rows = ""
for s in not_ok:
    r = gaps["results"].get(s, {})
    parts = []
    for lk, lab in LANGS:
        item = r.get(lk, {})
        if item.get("ok"):
            parts.append(f'<span class="badge b-ok">{lab} ✅</span>')
        else:
            fails = []
            if not item.get("len_ok"): fails.append("len")
            if not item.get("faq"): fails.append("faq")
            if not item.get("jsonld"): fails.append("jsonld")
            if not item.get("cta"): fails.append("cta")
            detail = ",".join(fails) or "ok"
            extra = ""
            if "words" in item: extra = f' ({item["words"]}w)'
            if "cjk" in item: extra = f' ({item["cjk"]}cjk)'
            parts.append(f'<span class="badge b-bad">{lab} ❌ {detail}{extra}</span>')
    gap_rows += f"<tr><td><code>{html.escape(s)}</code></td><td>{' '.join(parts)}</td></tr>"
if not gap_rows:
    gap_rows = '<tr><td colspan="2">无缺口</td></tr>'

staging_rows = "".join(
    f'<tr><td>{i+1}</td><td><code>{html.escape(s)}</code></td>'
    f'<td><a href="https://beehive-strategy-v2.pages.dev/blog/articles/{s}/" target="_blank">EN</a></td>'
    f'<td><a href="https://beehive-strategy-v2.pages.dev/zh-cn/blog/articles/{s}/" target="_blank">zh-CN</a></td>'
    f'<td><a href="https://beehive-strategy-v2.pages.dev/zh-tw/blog/articles/{s}/" target="_blank">zh-TW</a></td></tr>'
    for i, s in enumerate(STAGING_MISSING))

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M HKT")

def per_lang_card(lk, lab):
    p = per_lang.get(lk, {})
    return f'''<div class="card"><h3>{lab}</h3>
<p>扫描 <b>{p.get('total','–')}</b> 页，完全干净 <b>{p.get('clean','–')}</b> 页</p></div>'''

pl_cards = "".join(per_lang_card(lk, lab) for lk, lab in LANGS)

def sev_block(lk, lab):
    return f'''<div class="card wide"><h3>{lab} 残留问题</h3>
<table><tr><th>问题类型</th><th>数量</th></tr>{sev_rows(lk)}</table></div>'''

sev_blocks = "".join(sev_block(lk, lab) for lk, lab in LANGS)

agg_rows = ""
for lk, lab in LANGS:
    a = agg.get(lk, {})
    ok = a.get("ok", 0); tot = a.get("total", 0)
    cls = "b-ok" if ok == tot else "b-warn"
    agg_rows += (f'<tr><td>{lab}</td><td>{ok} / {tot}</td>'
                 f'<td>{a.get("len_fail",0)}</td><td>{a.get("faq_fail",0)}</td>'
                 f'<td>{a.get("jsonld_fail",0)}</td><td>{a.get("cta_fail",0)}</td>'
                 f'<td><span class="badge {cls}">{"达标" if ok==tot else str(tot-ok)+" 缺口"}</span></td></tr>')

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SEO+GEO 全量审计 &amp; 三环境同步报告 — 2026-09-02</title>
<style>
:root{{--bg:#f7f9f8;--card:#fff;--ink:#1c2b28;--muted:#5a6b67;--teal:#2B9E8B;--gold:#d4a843;--bad:#c0392b;--warn:#b9770e;--line:#dde5e2}}
*{{box-sizing:border-box}}
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);margin:0;padding:32px 4vw;line-height:1.6}}
h1{{font-size:1.7rem;border-bottom:3px solid var(--teal);padding-bottom:10px}}
h2{{font-size:1.2rem;margin-top:40px;color:var(--teal)}}
h3{{margin:0 0 8px}}
.meta{{color:var(--muted);font-size:.9rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:16px 0}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px}}
.card.wide{{grid-column:1/-1}}
.verdict{{border-left:5px solid var(--teal);background:#eef7f5;padding:14px 18px;border-radius:0 10px 10px 0;margin:14px 0}}
.verdict.warn{{border-color:var(--gold);background:#fbf6ea}}
table{{border-collapse:collapse;width:100%;font-size:.9rem;margin:8px 0}}
th,td{{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}}
th{{background:#eef4f2}}
code{{background:#eef2f1;padding:1px 5px;border-radius:4px;font-size:.85em;word-break:break-all}}
.badge{{display:inline-block;padding:2px 9px;border-radius:20px;font-size:.8rem;font-weight:600}}
.b-ok{{background:#e2f3ee;color:#1c7a66}}
.b-warn{{background:#fdf3dd;color:#8a6410}}
.b-bad{{background:#fde8e5;color:#a53225}}
a{{color:var(--teal)}}
.small{{font-size:.85rem;color:var(--muted)}}
ol li{{margin:6px 0}}
</style></head><body>

<h1>SEO + GEO 全量审计 &amp; 三环境同步报告</h1>
<p class="meta">生成时间：{now} ｜ 审计范围：本地全量 1,061 slug × 3 语言 = 3,183 页 ｜ 工具：audit_content.py + deep_audit.py（修复后重跑）</p>

<div class="verdict">
<b>总体结论：</b>GEO 内容门禁 <b>满分达成</b> —— 三语言 1,061/1,061 slug 全部达标，0 缺口（EN 字数缺口已于本轮补齐：dingtalk-and-feishu 文 +~185 词，重跑确认达标）。
历史 P0（canonical 错误、OG 缺失、H1 缺失、FAQPage JSON-LD 缺失批量问题）已全部清零。
<b>三环境同步：dev = PROD（字节级一致）✅；staging 落后 41 slug × 3 语言 = 123 页 ⚠️</b>，待补部署。
</div>

<h2>1️⃣ GEO 内容门禁（gaps_audit 最新重跑）</h2>
<div class="grid">
<div class="card wide"><table>
<tr><th>语言</th><th>达标 slug</th><th>字数缺口</th><th>FAQ 缺口</th><th>JSON-LD 缺口</th><th>CTA 缺口</th><th>状态</th></tr>
{agg_rows}
</table>
<p class="small">门禁标准：EN ≥2,500 词 / zh ≥3,500 CJK；FAQ ≥3 组；正文末恰好 1 个 FAQPage JSON-LD；CTA（EN "Book a Demo" / zh "预约演示" / 繁 "預約示範"）。</p></div>
</div>

<h3>缺口明细（{len(not_ok)} 篇）</h3>
<table><tr><th>Slug</th><th>三语言状态</th></tr>{gap_rows}</table>
<div class="verdict"><b>✅ 已修复：</b>此前唯一缺口 <code>dingtalk-and-feishu-ai-ecosystem-enterprise-integration</code> EN 版（2,376 词）已于 2026-09-02 增补两段（+~185 词，含 modified_time 更新），重跑 audit_content.py 确认 EN 1,061/1,061 全达标。改动仅本地，尚未部署。</div>

<h2>2️⃣ 深度 SEO 审计（deep_audit 最新重跑）</h2>
<div class="grid">{pl_cards}</div>
<div class="grid">{sev_blocks}</div>
<p class="small">已清零项：canonical_wrong、og_missing、h1_missing（此前 33 canonical + 167 og 补齐修复全部生效）。</p>

<h2>3️⃣ 三环境同步状态</h2>
<div class="grid">
<div class="card"><h3>dev ✅</h3><p><b>beehive-strategy-v2.pages.dev</b><br>EN/zh-CN/zh-TW 各 1,101 篇<br>sitemap 与 PROD 字节级一致（diff IDENTICAL，2,776,580 B）</p></div>
<div class="card"><h3>PROD ✅</h3><p><b>www.beehivestrategy.com</b><br>EN/zh-CN/zh-TW 各 1,101 篇<br>含全部修复 + 08-18~09-02 新批次</p></div>
<div class="card" style="border-left:4px solid var(--gold)"><h3>staging ⚠️</h3><p><b>beehive-strategy-v2-staging.pages.dev</b><br>EN/zh-CN/zh-TW 各 1,060 篇<br><b>缺同一批 41 slug × 3 = 123 页</b>（08-18~09-02 批次未部署）</p></div>
</div>

<h3>线上抽检（dev + PROD 全绿）</h3>
<table><tr><th>样本</th><th>验证点</th><th>结果</th></tr>
<tr><td><code>what-is-conversational-bi-chatbi-explained</code> (zh-TW)</td><td>canonical 自指向修复</td><td><span class="badge b-ok">✅ 200 / canonical 正确</span></td></tr>
<tr><td><code>why-mcp-matters-enterprise-data-teams</code> (zh-TW)</td><td>FAQPage JSON-LD 重建（5 Q/A）</td><td><span class="badge b-ok">✅ 200 / JSON-LD×1 / H1×1</span></td></tr>
<tr><td><code>financial-services-ai-fraud-detection-real-time</code> (EN)</td><td>OG/Twitter 卡片补齐</td><td><span class="badge b-ok">✅ 200 / og:url 正确</span></td></tr>
<tr><td><code>text-to-sql-accuracy-benchmark-2026</code>（新文）</td><td>新批次上线</td><td><span class="badge b-ok">✅ dev+PROD 200</span> ／ staging 404（确认落后）</td></tr>
</table>

<h2>4️⃣ staging 缺失 123 页清单（41 slug × 3 语言）</h2>
<p class="small">以下链接均为 staging 环境（当前 404，部署后即恢复）：</p>
<table><tr><th>#</th><th>Slug</th><th colspan="3">三语言（staging）</th></tr>{staging_rows}</table>

<h2>5️⃣ 同步行动计画</h2>
<div class="card"><ol>
<li><b>① 补齐 staging（唯一环境差距）</b> — 本环境无 wrangler/CF 凭证，两个路径二选一：
  <ul><li>Kenneth 提供 <code>CF_API_TOKEN</code>（Pages 部署权限），我完成部署并验证 123 页 × 200；</li>
  <li>或在 Cloudflare dashboard → Pages → <code>beehive-strategy-v2-staging</code> 手动触发部署（source = 最新 main）。</li></ul></li>
<li><b>② EN 补字 ✅ 已完成</b> — dingtalk-and-feishu 文 EN 版 +~185 词，重跑 audit 确认 1,061/1,061（改动在本地，随下次部署上 dev/staging/prod）。</li>
<li><b>③ PROD 确认</b> — dev = PROD 已字节一致，staging 补齐后三环境对齐；后续部署仍遵循 PROD 逐字显式批准铁律。</li>
<li><b>④（可选，P1 类）</b> — 残留 faq_lt3（~40/语言）、broken_internal_links（~20）、title_long（EN 755）等优化项另行排期，不阻塞同步。</li>
</ol></div>

<p class="meta" style="margin-top:40px">Beehive Strategy · SEO/GEO Audit &amp; Sync Report · 2026-09-02</p>
</body></html>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("Wrote", OUT, os.path.getsize(OUT), "bytes")
