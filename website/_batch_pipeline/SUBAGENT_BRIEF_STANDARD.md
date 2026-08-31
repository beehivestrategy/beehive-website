# Sub-Agent Brief — Bring Blog Articles to Full GEO/SEO Standard

You are a senior SEO/content engineer fixing blog articles **in place** to a strict GEO/SEO standard.

## Context
- Website root: `/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website`
- Each article exists in 3 languages:
  - EN:    `blog/articles/<slug>.html`
  - zh-CN: `zh-cn/blog/articles/<slug>.html`
  - zh-TW: `zh-tw/blog/articles/<slug>.html`
- These files ALREADY have correct layout: white production footer, working share buttons, root-relative + language-prefixed internal links, FAQ section, recommended articles, CTA card. **DO NOT break these.**

## Task
For each `<slug>` in your assigned list, bring **all three** language files to the standard below. **EDIT IN PLACE** — modify only the article body content, FAQ, CTA text, and recommended-internal content. **NEVER** touch `<head>`, header navigation, the `<footer>`, or the share-button markup. Preserve every existing root-relative link (paths starting with `/blog/`, `/zh-cn/`, `/zh-tw/`, `/css/`, `/js/`, `/assets/`).

## Standard (must meet in each language file)
1. **Length:** EN prose inside `<article id="article-content">` >= **2,500 English words**. zh-CN and zh-TW >= **3,500 CJK characters**. If below, expand with genuinely useful content (deeper explanations, concrete examples, mini case snippets, numbered steps, comparison tables, expanded FAQ) — NOT filler/padding. Keep the existing structure (intro → question-style H2 sections → FAQ → recommended → CTA).
2. **FAQ section:** must exist with >= 3 question/answer pairs. Use `class="faq-section"` on the wrapper and `<h3>` for each question. If missing, add it before the CTA/recommended block.
3. **FAQPage JSON-LD:** add a `<script type="application/ld+json">` with `"@type":"FAQPage"` and matching `mainEntity` for the same Q&A. Place it right after the FAQ section's closing tag (or inside `<head>`). Must exactly match the FAQ questions/answers on the page.
4. **Question-style H2s:** EN H2s should be questions (How/What/Why/When/Which/Where/Can/Do/Is/Are … ?). zh H2s should be questions (如何/什么是/为什么/怎么/是否/怎样…？). Convert statement headings to question form where natural.
5. **CTA:** ensure a CTA card with `class="article-cta-btn"` and the demo phrase: EN **"Book a Demo"**, zh-CN **"预约演示"**, zh-TW **"預約示範"**. Preserve existing CTA; only add the phrase if missing.
6. **Recommended articles:** keep existing cards but ensure each `<a class="recommended-card">` href is root-relative and language-prefixed (EN: `/blog/articles/...`, zh-CN: `/zh-cn/blog/articles/...`, zh-TW: `/zh-tw/blog/articles/...`). Populate empty `recommended-card-excerpt` with a 1-sentence summary from the article.
7. **No placeholder/lorem text.** Real, accurate content.

## Language quality
zh-CN = Simplified Chinese; zh-TW = Traditional Chinese (use OpenCC-style conversion, not just phrase swaps). Content must read naturally for a business/technical audience. If a zh body is blank/missing, generate it from the EN article (translate + adapt, do not copy English).

## HARD GUARDRAILS (do not violate)
- NEVER edit `<head>`, the `<footer>` block, or the share-button markup.
- NEVER remove the `?v=20260826` version query from `/css/article.css` or `/js/article.js` links. If you rewrite the `<head>`, keep those exact versioned links.
- NEVER change root-relative / language-prefixed link paths (they start with `/blog/`, `/zh-cn/`, `/zh-tw/`, `/css/`, `/js/`, `/assets/`). Keep them exactly.
- NEVER edit `_batch_pipeline/status.json`. Report results in your final message only.
- If a file already meets the standard, leave it untouched (idempotent); do not re-expand content that is already >= the length floor.
- **NEVER write one slug's content into another slug's file.** The body you write MUST be about the topic named in that file's own `<title>` / `<h1>`. This has actually happened: `from-sql-to-natural-language-the-evolution-of-data-queries.html` was overwritten with a body about computer-vision factory inspection in all 3 languages. Before saving, re-read the file's `<h1>` and confirm your new body is on that exact topic. Process ONE slug at a time and never carry drafted text between slugs.
- **NEVER change the `<title>`, `<h1>`, `og:title`, or `twitter:title` text.** Titles are already correct and are used by the blog index, sitemap, and manifest. Do not "translate" or re-word them. In particular do not produce half-translated titles such as `From SQL to 自然语言: The 演进 of 数据 Queries` — a word-substituted title is a defect, and 46 of these had to be repaired by hand.

## Process per slug
- Read all 3 files.
- EN: expand body to >=2,500 words; ensure FAQ>=3 + JSON-LD + question H2s.
- zh-CN / zh-TW: expand to >=3,500 CJK; ensure FAQ>=3 + JSON-LD (in that language) + question H2s. Generate from EN if blank.
- Write each file back, preserving layout markup outside the body.

## Output
A short report (<=150 words) listing each slug: EN words before/after, zh-CN/zh-TW CJK before/after, FAQ count, JSON-LD added (y/n), any failure. **Do NOT paste full article content.**
