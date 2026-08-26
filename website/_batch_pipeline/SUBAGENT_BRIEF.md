# Blog Batch Rewrite — Sub-Agent Brief (GEO Standard)

You are rewriting ONE Beehive Strategy blog article (EN + zh-CN) to meet the
site's GEO/SEO design standard. The orchestrator will later regenerate zh-TW
and reconcile the verifier — **you must NOT run `gen_zhtw_one.py`,
`update_manifest`, or touch `status.json`. You must NOT run git restore/checkout.**

## Paths
- ROOT = `/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website`
- EN file:    `ROOT/blog/articles/<slug>.html`
- zh-CN file: `ROOT/zh-cn/blog/articles/<slug>.html`
- Python (managed): `/Users/kennethkwok/.workbuddy/binaries/python/versions/3.13.12/bin/python3`
- Helpers: `ROOT/_batch_pipeline/rewrite_lib.py` (has `splice(real_path, new_inner)`)
- Verifier: `ROOT/_batch_pipeline/verify_article.py <path> [en|zh-cn]`

## Hard requirements (the verifier checks ALL of these)
1. **Length floor** — EN ≥ 2,500 words; zh-CN ≥ 3,500 CJK characters. Aim 2,600–3,400 EN / 3,700–5,000 CJK for headroom.
2. **FAQ HTML block** inside `<article>`: a wrapper `<div class="faq-section">` containing `<h2>Frequently Asked Questions</h2>` and ≥3 `<div>` Q&A items (microdata `itemscope itemtype="https://schema.org/FAQPage"` with `itemprop="mainEntity"` / `name` / `acceptedAnswer` / `text`). **The verifier searches for the substring `faq-section`** — do NOT use `article-faq`.
3. **FAQPage JSON-LD** — a `<script type="application/ld+json">` containing `"@type":"FAQPage"` with `mainEntity` array of ≥3 items. Place it INSIDE `<article>` (as the last child, after the container `</div>`, before the file's own `</article>`). Valid JSON (no trailing commas). This is the ONLY FAQPage JSON-LD in the file.
4. **CTA block** inside `<article>`: `<div class="cta article-cta">…</div>` — the verifier checks the substring `class="cta` (must be FIRST class). EN CTA text must include **"Book a Demo"**; zh-CN CTA text must include **"预约演示"**.
5. **Balanced `<div>`** tags inside the body (equal open/close).
6. **hreflang** ×4 (en / zh-CN / zh-TW / x-default) and **canonical** are in the `<head>` — **preserve them; do not touch**. `splice()` keeps the head untouched.
7. **og:locale** — EN head is fine. For **zh-CN** the existing head has REVERSED attribute order `<meta content="zh_CN" property="og:locale"/>` which FAILS the verifier (its regex is `og:locale"[^>]*content="zh_CN"`). After splicing, fix it in the zh-CN file: replace with `<meta property="og:locale" content="zh_CN"/>`.
8. **No placeholder text** (Lorem / TODO / TBD / 占位 / 待补充 / "coming soon").
9. Include ≥1 question-style `<h2>` (good GEO practice; not a hard verifier gate but include it).

## Procedure (per slug)
1. Read the existing EN and zh-CN files to capture: exact `<title>`, `category` (label), `date` (ISO + human), `tags`, and the thin existing body to expand from (same topic/angle).
2. Write the new **inner body** (NO `<article>` tag, NO trailing `</article>`) to a temp file `_gen_<slug>_en.html` and `_gen_<slug>_zh.html`. Use the skeleton below, expanded to the length floor with substantive, original, expert-level prose (not fluff). EN and zh-CN must cover the same sections/topics.
3. Splice each:
   ```
   import sys
   sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline")
   from rewrite_lib import splice
   splice("/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/blog/articles/<slug>.html", open("_gen_<slug>_en.html",encoding="utf-8").read())
   splice("/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/zh-cn/blog/articles/<slug>.html", open("_gen_<slug>_zh.html",encoding="utf-8").read())
   ```
4. Fix zh-CN `og:locale` order (see req 7).
5. Update the head `BlogPosting` JSON-LD `"wordCount"` and the `<span>N min read</span>` to the new counts (EN: rt = round(wc/200); zh: rt = round(cjk/350)). Only one `"wordCount"` exists per file.
6. Verify BOTH langs:
   ```
   PY=/Users/kennethkwok/.workbuddy/binaries/python/versions/3.13.12/bin/python3
   $PY "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/verify_article.py" "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/blog/articles/<slug>.html" en
   $PY "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/verify_article.py" "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/zh-cn/blog/articles/<slug>.html" zh-cn
   ```
   Both must print `PASS`. If FAIL, fix and re-verify. Do NOT proceed until both PASS.
7. Clean up your two `_gen_*.html` temp files.

## Inner-body skeleton (fill CATEGORY/TITLE/DATEISO/DATEHUMAN/TAGS; expand prose)
```
<div class="container">
<header class="article-header">
<span class="label">CATEGORY</span>
<h1>TITLE</h1>
<div class="article-meta">
<span class="article-author">By Beehive Strategy</span>
<span aria-hidden="true">·</span>
<time datetime="DATEISO">DATEHUMAN</time>
<span aria-hidden="true">·</span>
<span>RT min read</span>
</div>
</header>
<div class="article-content">
<p class="article-lead">LEAD 1–2 sentences.</p>

<h2>Why TOPIC matters for ENTERPRISE</h2>
<p>…250–350 words…</p>

<h2>The business cost of getting it wrong</h2>
<p>…</p>

<h2>How Beehive Strategy approaches it</h2>
<p>…</p>
<ul><li>…</li><li>…</li></ul>

<h2>A practical implementation roadmap</h2>
<p>…</p>
<ol><li>…</li><li>…</li></ol>

<h2>Measuring success: the metrics that matter</h2>
<p>…</p>

<h2>Common pitfalls and how to avoid them</h2>
<p>…</p>

<h2>What should enterprises do first?</h2>
<p>…question-style H2…</p>

<div class="faq-section">
<h2>Frequently Asked Questions</h2>
<div itemscope itemtype="https://schema.org/FAQPage">
<div itemprop="mainEntity" itemscope itemtype="https://schema.org/Question">
<h3 itemprop="name">Q1?</h3>
<div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer"><div itemprop="text"><p>A1</p></div></div>
</div>
<div itemprop="mainEntity" itemscope itemtype="https://schema.org/Question">
<h3 itemprop="name">Q2?</h3>
<div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer"><div itemprop="text"><p>A2</p></div></div>
</div>
<div itemprop="mainEntity" itemscope itemtype="https://schema.org/Question">
<h3 itemprop="name">Q3?</h3>
<div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer"><div itemprop="text"><p>A3</p></div></div>
</div>
<div itemprop="mainEntity" itemscope itemtype="https://schema.org/Question">
<h3 itemprop="name">Q4?</h3>
<div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer"><div itemprop="text"><p>A4</p></div></div>
</div>
</div>
</div>

<div class="cta article-cta">
<p>Ready to turn TOPIC into measurable outcomes? <a href="/contact">Book a Demo</a> with Beehive Strategy and see how our MCP-driven conversational BI platform delivers governed answers in natural language across your enterprise.</p>
</div>
</div>
<footer class="article-footer">
<div class="article-tags"><span class="article-tag">tag1</span><span class="article-tag">tag2</span></div>
<div class="article-share">
<a class="btn btn-secondary" href="https://www.linkedin.com/sharing/share-offsite/?url=https://www.beehivestrategy.com/blog/articles/SLUG" rel="noopener noreferrer" target="_blank">LinkedIn</a>
<a class="btn btn-secondary" href="https://twitter.com/intent/tweet?url=https://www.beehivestrategy.com/blog/articles/SLUG" rel="noopener noreferrer" target="_blank">X</a>
</div>
</footer>
<nav aria-label="Article navigation" class="article-nav"></nav>
</div>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type":"Question","name":"Q1?","acceptedAnswer":{"@type":"Answer","text":"A1"}},
    {"@type":"Question","name":"Q2?","acceptedAnswer":{"@type":"Answer","text":"A2"}},
    {"@type":"Question","name":"Q3?","acceptedAnswer":{"@type":"Answer","text":"A3"}},
    {"@type":"Question","name":"Q4?","acceptedAnswer":{"@type":"Answer","text":"A4"}}
  ]
}
</script>
```
The FAQ HTML Q&A text and the FAQPage JSON-LD `name`/`text` must match (same 4 questions/answers). Keep them consistent between the HTML block and the JSON-LD.

## Reporting
End your turn with a short report: slug, EN word count, zh-CN CJK count, and the
verify result (EN PASS/FAIL, zh-CN PASS/FAIL). If any lang FAILED after fixes,
state the remaining error verbatim.
