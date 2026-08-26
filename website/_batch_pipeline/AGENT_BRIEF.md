# Blog Article Rewrite — Agent Brief

You are rewriting Beehive Strategy blog articles to meet the content-length and
design standard. You will be given a BATCH of EN article slugs. For EACH slug
you must produce TWO files: the rewritten EN article and its zh-CN translation.

## Hard rules (do not violate)

1. **Only rewrite the inner article content.** Open the existing file
   `website/blog/articles/<slug>.html`. Preserve the ENTIRE `<head>` (all meta,
   hreflang, og:*, JSON-LD @graph, lang switcher) and the outer page chrome
   (header nav, sidebar, footer, `<article class="article">` open tag). You may
   ONLY replace the HTML between `<div class="article-content">` and its
   closing structure up to `</article>` — i.e. the article body (lead, TLD;,
   sections, FAQ, CTA, tags, article-nav). Do NOT touch the head or footer.

2. **Length standard (EN):** article-content body must be **2,500–3,500 words**
   (target 3,200). Do not pad with fluff; expand with substantive sections,
   examples, tables, numbered steps, and practitioner insight.

3. **Required H2 structure (EN)** — include all of these in order:
   - What is <topic>? — A Concise Definition
   - How Does <topic> Work?
   - Key Components of <topic>
   - Why <topic> Matters for Enterprises
   - Common Use Cases (cover retail/ecom, finance, manufacturing, supply chain,
     real estate, professional services where relevant)
   - How <topic> Fits into Beehive Strategy's Approach (MCP-driven conversational
     BI, 2-week enterprise deploy, IM channels: WeCom/DingTalk/Feishu/WhatsApp/
     Telegram/Teams/WeChat)
   - Getting Started with <topic> (first 3 steps)
   - <topic> vs Alternatives (comparison table or prose)
   - Core Architecture Components
   - <topic> for Mid-Market and Resource-Constrained Teams
   - How <topic> Grounds AI and Large Language Models
   - A Phased 90-Day Implementation Roadmap (30/60/90)
   - Frequently Asked Questions
   Adapt section titles to the topic; do not use literal "<topic>".

4. **FAQ section REQUIRED** with 4–6 Q&A items, each wrapped:
   `<div class="faq-item reveal"><h3>Q?</h3><p>A.</p></div>` inside
   `<div class="faq-section">`. ALSO add a `FAQPage` JSON-LD block — a separate
   `<script type="application/ld+json">` containing
   `{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[...]}` with
   `Question`/`Answer` pairs matching the FAQ items. (Keep the existing BlogPosting
   @graph in the head intact; add this as an additional script block before
   `</body>` if no FAQPage exists, or merge if one exists.)

5. **CTA block REQUIRED** inside the body: a section with
   `class="cta-content reveal"` and a primary button
   `<a class="btn btn-primary btn-lg" href="/contact">Book a Demo</a>`. The
   existing file already has a CTA — keep/expand it, do not remove.

6. **zh-CN translation:** produce `website/zh-cn/blog/articles/<slug>.html`.
   Translate the FULL rewritten EN body to natural, professional Simplified
   Chinese (3,500–5,000 CJK chars). Preserve the EXACT same `<head>` structure as
   the existing zh-cn file (canonical /zh-cn/, hreflang alternates en/zh-CN/zh-TW/
   x-default, og:locale zh_CN, og:url /zh-cn/, lang="zh-CN"). Only replace the
   body. Keep FAQ JSON-LD with `"inLanguage":"zh-CN"`.

7. **Do NOT create zh-TW files** (a separate script generates them via OpenCC).

8. **No placeholder text** (no "Lorem", "TODO", "coming soon", "待补充").

9. **Balanced HTML** — every `<div>` opened in the body must be closed.

10. Keep existing internal "Related Articles" links if present; otherwise you
    may omit. Do not invent broken links.

## Deliverable check
After writing both files for a slug, run:
`python3 website/_batch_pipeline/verify_article.py website/blog/articles/<slug>.html en`
`python3 website/_batch_pipeline/verify_article.py website/zh-cn/blog/articles/<slug>.html zh-cn`
Fix until both PASS (the EN word-floor check is the gate; 2,500 minimum).

Report a short summary: per-slug EN word count + zh-CN CJK count + PASS/FAIL.
