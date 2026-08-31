# Operational Guardrails for Sub-Agents (EDIT-IN-PLACE)

Root: `/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website`

You are a senior SEO/content editor. First read `_batch_pipeline/SUBAGENT_BRIEF_STANDARD.md` and follow it. Then apply these precise guardrails.

## EDIT-IN-PLACE RULE (critical)
Use the Read tool, then the Edit tool. **NEVER rewrite an entire file with Write.** You may only modify these regions:
1. Article body inside `<article class="article-content" id="article-content">` (between that opening tag and `</article>`).
2. The FAQ `<section class="faq-section" ...>` (it lives inside the article).
3. Any `<script type="application/ld+json">` FAQPage block.
4. The CTA button `<a ... class="article-cta-btn">...</a>` text.
5. Internal article links (`.recommended-card` href, `.sidebar-related-card` href, and any related links).

## PRESERVE VERBATIM (do NOT touch)
- The entire `<head>...</head>` block.
- The `<header class="header"...>` through its `</header>`.
- The `<div class="mobile-menu"...>` block.
- The `<footer class="footer"...>` through its `</footer>`.
- The share-button markup: `.sidebar-share` containing `article-share-btn` buttons.
- The exact tags `<link href="/css/article.css?v=20260826" rel="stylesheet">` and `<script src="/js/article.js?v=20260826"></script>`.

## STANDARD TO APPLY
- **EN body >= 2500 English words.** Expand with genuinely useful content (deeper explanation, examples, mini case snippets, numbered steps, comparison tables). Keep existing intro → question-H2 → FAQ → recommended → CTA structure. EN H2s must be questions ending with `?`.
- **zh-CN / zh-TW:** if current CJK inside the article `< 3500`, expand to `>= 3500` CJK in the correct script (zh-CN = Simplified, zh-TW = Traditional — proper OpenCC-style conversion, not phrase swaps). zh H2s must be questions (如何/什么是/为什么/怎么/是否/怎样…？).
- **FAQ:** If a file already has a `faq-section` with `>=3` `faq-item` pairs AND a matching FAQPage JSON-LD in `<head>`, **do NOT modify the FAQ or its JSON-LD** — only expand the body. If a file lacks a FAQ section (faq count 0) or has `<3`, ADD/complete one before the `<nav class="article-nav">` block with `>=3` question/answer pairs, using the site's existing faq markup pattern (copy it from a sibling file that has it). Then ensure a matching FAQPage JSON-LD exists — add it immediately after the FAQ section's closing `</section>` if missing. The JSON-LD `mainEntity` `name` values must exactly match the FAQ questions.
- **CTA phrase:** EN file must contain `Book a Demo` in the `.article-cta-btn`; zh-CN `预约演示`; zh-TW `預約示範`. If missing, add the phrase into the CTA button text (preserve surrounding CTA markup).
- **Internal links:** all internal article links must be root-relative + language-prefixed: EN `/blog/articles/...`, zh-CN `/zh-cn/blog/articles/...`, zh-TW `/zh-tw/blog/articles/...`. Fix any `blog/articles/...` (no leading slash) or wrong-language prefixes. Populate any empty `<p class="recommended-card-excerpt"></p>` with a 1-sentence summary. Leave external `https://` links and `/css`, `/js`, `/assets` links untouched.

## VALIDATION (run via Bash python after edits)
- EN words inside article-content (`[A-Za-z0-9']+`) `>= 2500`.
- zh CJK inside article-content (`[\u4e00-\u9fff]`) `>= 3500` for files that were below (prefer all).
- `faq-item` count `>= 3`.
- FAQPage JSON-LD present and `json.loads` parses, with `mainEntity` names matching FAQ questions.
- `article.css?v=20260826` and `article.js?v=20260826` tags still present; footer/header/share markup unchanged (grep confirms presence).

## REPORT (<=200 words)
Covering your assigned slugs: for each slug list EN words before/after, zh-CN CJK before/after, zh-TW CJK before/after, FAQ count, JSON-LD added y/n, any failure. Do NOT paste article content. Read `_batch_pipeline/before_metrics.json` for the "before" numbers.

Work autonomously; do not ask questions. If a file is missing, report it as a failure.
