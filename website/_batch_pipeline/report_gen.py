#!/usr/bin/env python3
"""Generate deep_audit_report.html from deep_audit.json."""
import json, os, datetime

HERE = os.path.dirname(__file__)
data = json.load(open(os.path.join(HERE, "deep_audit.json"), encoding="utf-8"))
summary = data["summary"]
records = data["records"]
LANGS = {"en": "English", "cn": "简体中文", "tw": "繁體中文"}

# example slugs per issue code
examples = {}
for slug, rec in records.items():
    for lang in ("en","cn","tw"):
        r = rec.get(lang, {})
        if "err" in r: continue
        for code in r.get("issues", []):
            base = code.split(":")[0]
            examples.setdefault(base, set())
            if len(examples[base]) < 8:
                examples[base].add(slug)

# Issue metadata: (label, priority, impact)
META = {
 "canonical_wrong": ("Canonical URL 错误", "P0", "规范链接指向错误地址，导致搜索引擎收录错乱/重复"),
 "h1_missing": ("缺少 H1 标题", "P0", "每页必须有且仅有一个 H1，否则主题信号缺失"),
 "title_untranslated": ("标题未翻译（中文页含英文标题）", "P0", "中文页 title 仍是英文，用户体验与排名受损"),
 "title_known_broken": ("标题为已知损坏（半翻译/混排）", "P0", "来自 broken_titles.json 的 35 个损坏标题"),
 "faqpage_jsonld_missing": ("缺少 FAQPage JSON-LD", "P1", "GEO 关键：AI Overview 难以引用无结构化的 FAQ"),
 "faqpage_jsonld_multiple": ("FAQPage JSON-LD 重复", "P1", "同页多个 FAQPage schema 属违规"),
 "faqpage_jsonld_mismatch": ("FAQPage 与正文 FAQ 数量不符", "P1", "结构化数据与页面不一致，可能被判定为作弊"),
 "faq_missing": ("缺少 FAQ 区块", "P1", "GEO 转化必备模块缺失"),
 "faq_lt3": ("FAQ 少于 3 组问答", "P1", "GEO 标准要求 >=3 组 Q/A"),
 "og_missing": ("OpenGraph 标签缺失", "P1", "社交分享/富媒体预览失效，点击率受损"),
 "tw_missing": ("Twitter Card 标签缺失", "P1", "X/Twitter 分享卡片失效"),
 "broken_internal_links": ("站内死链", "P1", "指向不存在的文章，损耗权重与爬虫"),
 "anchor_broken": ("页内锚点失效", "P2", "目录/TOC 跳转指向不存在的 id"),
 "img_no_alt": ("图片缺少 alt", "P2", "可访问性 + 图片 SEO 缺失"),
 "desc_missing": ("缺少 meta description", "P2", "SERP 摘要失控，CTR 下降"),
 "desc_short": ("meta description 过短", "P2", "摘要信息不足"),
 "desc_long": ("meta description 过长", "P2", "被截断，信息丢失"),
 "title_long": ("title 过长", "P3", "搜索结果被截断（软指标）"),
 "no_h2": ("无 H2 小节", "P2", "结构扁平，可读性/GEO 信号弱"),
 "h3_before_h2": ("H3 出现在 H2 之前", "P2", "标题层级错乱"),
 "len_short": ("正文偏短（接近下限）", "P3", "严格词数口径下低于 2500/3500（与通过门禁的宽松口径存在定义差）"),
 "jsonld_invalid": ("JSON-LD 解析失败", "P1", "结构化数据损坏"),
 "title_missing": ("缺少 title", "P0", "致命：无页面标题"),
 "title_empty": ("title 为空", "P0", "致命"),
 "canonical_missing": ("缺少 canonical", "P1", "重复内容风险"),
 "hreflang_missing": ("hreflang 缺失", "P1", "多语言版本互相引用信号缺失"),
}

PRI_ORDER = {"P0":0,"P1":1,"P2":2,"P3":3}

def bar(n, total):
    pct = (n/total*100) if total else 0
    color = "#d9534f" if pct>20 else ("#f0ad4e" if pct>5 else "#5cb85c")
    return f'<div class="bar"><span style="width:{min(pct,100)}%;background:{color}"></span></div><span class="bval">{n} ({pct:.1f}%)</span>'

# group issues by priority
grouped = {"P0":[], "P1":[], "P2":[], "P3":[]}
for lang in ("en","cn","tw"):
    for code, cnt in summary["severity_counts"].get(lang, {}).items():
        if code in META:
            grouped[META[code][1]].append((code, lang, cnt))
# dedupe by code keeping max
seen = {}
for pri in grouped:
    agg = {}
    for code, lang, cnt in grouped[pri]:
        agg[code] = max(agg.get(code,0), cnt)
    grouped[pri] = sorted(agg.items(), key=lambda x:-x[1])

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def issue_block(items):
    rows = ""
    for code, cnt in items:
        label, pri, impact = META.get(code, (code, "P2", ""))
        ex = ", ".join(sorted(examples.get(code, []))[:6]) or "—"
        rows += f"""<tr><td><span class="tag {pri}">{pri}</span></td><td><b>{label}</b><br><small>{code}</small></td>
        <td class="cnt">{cnt}</td><td>{impact}</td><td><code>{ex}</code></td></tr>"""
    return rows or "<tr><td colspan=5>无</td></tr>"

# per-language health table
health_rows = ""
for lang in ("en","cn","tw"):
    a = summary["per_lang"].get(lang, {})
    total = a.get("total",0); clean = a.get("clean",0)
    pct = clean/total*100 if total else 0
    health_rows += f"<tr><td>{LANGS[lang]} ({lang})</td><td>{total}</td><td>{clean}</td><td>{pct:.1f}%</td><td>{bar(total-clean,total)}</td></tr>"

# duplicate tables
def duptable(d, field):
    rows = ""
    for k, slugs in list(d.items())[:15]:
        rows += f"<tr><td><code>{k[:90]}</code></td><td>{', '.join(slugs[:6])}{'…' if len(slugs)>6 else ''}</td><td>{len(slugs)}</td></tr>"
    return rows or "<tr><td colspan=3>无</td></tr>"

dup_h1 = data.get("dup_h1_examples", {})
dup_title = data.get("dup_title_examples", {})

HTML = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Beehive Strategy — 全站博客深度 SEO/GEO 审计报告</title>
<style>
:root{{--bg:#0f1115;--card:#171a21;--fg:#e8eaed;--mut:#9aa0a6;--teal:#2B9E8B;--gold:#d4a843;--line:#262b33;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg);line-height:1.6;padding:32px}}
.wrap{{max-width:1100px;margin:0 auto}}
h1{{font-size:28px;margin:0 0 4px}}
h2{{font-size:20px;margin:34px 0 12px;border-left:4px solid var(--teal);padding-left:10px}}
.sub{{color:var(--mut);font-size:14px;margin-bottom:8px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:14px 0}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{color:var(--mut);font-weight:600}}
code{{background:#0c0e12;padding:1px 6px;border-radius:5px;font-size:12px;color:var(--gold)}}
.tag{{display:inline-block;padding:1px 8px;border-radius:6px;font-size:11px;font-weight:700}}
.P0{{background:#5a1d1d;color:#ff8a8a}} .P1{{background:#5a4a1d;color:#ffd98a}} .P2{{background:#1d3f5a;color:#8ad0ff}} .P3{{background:#2a2f38;color:#c5ccd6}}
.bar{{display:inline-block;width:160px;height:10px;background:#0c0e12;border-radius:5px;overflow:hidden;vertical-align:middle;margin-right:8px}}
.bar span{{display:block;height:100%}} .bval{{font-size:12px;color:var(--mut)}}
.kpi{{display:flex;gap:14px;flex-wrap:wrap}}
.kpi .box{{flex:1;min-width:150px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}}
.kpi .n{{font-size:30px;font-weight:800;color:var(--teal)}}
.kpi .l{{color:var(--mut);font-size:13px}}
.note{{font-size:13px;color:var(--mut);border-left:3px solid var(--gold);padding-left:10px;margin:10px 0}}
</style></head><body><div class="wrap">
<h1>Beehive Strategy · 全站博客深度 SEO/GEO 审计报告</h1>
<div class="sub">生成时间 {now} · 覆盖范围：1,061 slug × 3 语言 = 3,183 个 HTML 文件 · 多维度审计</div>

<div class="kpi">
  <div class="box"><div class="n">1,061</div><div class="l">slug 总数（EN/zh-CN/zh-TW 各 1,061）</div></div>
  <div class="box"><div class="n">100%</div><div class="l">GEO 基础门禁达标率（长度+FAQ+JSON-LD+CTA）</div></div>
  <div class="box"><div class="n">{summary['per_lang']['en']['clean']+summary['per_lang']['cn']['clean']+summary['per_lang']['tw']['clean']}</div><div class="l">三语言零问题文件数合计</div></div>
  <div class="box"><div class="n">{len(META)}</div><div class="l">审计维度</div></div>
</div>

<div class="note">基础门禁已于本次会话前 100% 通过（1,061/1,061）。本深度审计聚焦门禁之外的 <b>技术性 SEO / GEO 健康度</b>，用于驱动下一轮修复与「新博客生产」的质量基线。</div>

<h2>一、各语言健康度</h2>
<div class="card"><table>
<tr><th>语言</th><th>文件数</th><th>零问题</th><th>零问题率</th><th>有问题文件占比</th></tr>
{health_rows}
</table></div>

<h2>二、P0 — 致命 / 高优先级（必须修）</h2>
<div class="card"><table><tr><th>优先级</th><th>问题</th><th>数量</th><th>影响</th><th>示例 slug</th></tr>
{issue_block(grouped["P0"])}</table></div>

<h2>三、P1 — 重要（GEO / 社交 / 链接）</h2>
<div class="card"><table><tr><th>优先级</th><th>问题</th><th>数量</th><th>影响</th><th>示例 slug</th></tr>
{issue_block(grouped["P1"])}</table></div>

<h2>四、P2 / P3 — 优化项</h2>
<div class="card"><table><tr><th>优先级</th><th>问题</th><th>数量</th><th>影响</th><th>示例 slug</th></tr>
{issue_block(grouped["P2"]+grouped["P3"])}</table></div>

<h2>五、全站级重复内容（跨 slug 完全相同）</h2>
<div class="note">重复 H1 / Title / Description 会被搜索引擎判定为低质重复，压低整站排名。需改写为唯一值。</div>
<div class="card"><h3>重复 H1（{summary['dup_h1']['en']+summary['dup_h1']['cn']+summary['dup_h1']['tw']} 组）</h3>
<table><tr><th>H1 文本</th><th>出现 slug</th><th>次数</th></tr>{duptable(dup_h1.get('en',{}),'h1')}</table></div>
<div class="card"><h3>重复 Title（{summary['dup_title']['en']+summary['dup_title']['cn']+summary['dup_title']['tw']} 组）</h3>
<table><tr><th>Title 文本</th><th>出现 slug</th><th>次数</th></tr>{duptable(dup_title.get('en',{}),'title')}</table></div>

<h2>六、方法论与修复路线</h2>
<div class="card">
<ol>
<li><b>P0 立即修</b>：32 个 zh-TW canonical 错误、7 个缺失 H1、4 个未翻译标题 + broken_titles.json 中 35 个损坏标题（半翻译/混排）。</li>
<li><b>P1 批量修</b>：47/43/43 个 FAQPage JSON-LD 与正文不符 → 重新生成匹配 schema；39/41/40 个 FAQ <3 组 → 补足；166/7/7 个 OG + 165/6/6 个 Twitter 卡片缺失 → 补齐 meta；21/21/16 个站内死链 → 修复或 301。</li>
<li><b>P2 优化</b>：页内锚点、图片 alt、meta description 长度、标题层级。</li>
<li><b>防回归</b>：将本审计脚本接入 CI / 发布前门禁，任何新文章必须 0 问题才允许上线。</li>
</ol>
</div>

<div class="note">原始数据见 <code>_batch_pipeline/deep_audit.json</code>。修复脚本与「新博客生产流水线」标准已沉淀至 Obsidian Vault（见 23-GEO-SEO-内容标准与审计 / 24-新博客生产流水线）。</div>
</div></body></html>"""

out = os.path.join(HERE, "deep_audit_report.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("Wrote", out, len(HTML), "bytes")
