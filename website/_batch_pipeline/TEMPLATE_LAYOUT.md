# Article Layout — Canonical Template (post-2026-08-26 fix)

These are the site-wide conventions every rewritten blog article MUST follow so it matches
production (www.beehivestrategy.com) and all links actually work.

## 1. Footer — MUST equal production white footer
- Use the white footer from `css/styles.css` (`.footer { background: rgba(255,255,255,0.97) ... }`).
- article.css already contains the matching footer CSS (appended 2026-08-26).
- Structure: `.footer-brand` (logo + `<p>` desc + `.social` LinkedIn + Email), then
  `.footer-col` ×3 (Product / Industries / Company), then `.footer-bottom`
  (copyright `© 2024–2026 Beehive Strategy Limited` + `.footer-legal` /privacy /terms /cookies + "Built in Shenzhen, China").
- Do NOT use the old dark harness footer (`.footer-brand-desc`, `.footer-social`, `.footer-col-heading`,
  `.footer-col-links`, `.footer-bottom-links` are obsolete).

## 2. Links MUST be root-relative (never page-relative)
On article pages the file lives at `/blog/articles/<slug>.html`, so a page-relative link like
`href="blog/articles/x"` resolves to `/blog/articles/blog/articles/x` → 404.

| Location | Correct | Wrong |
|---|---|---|
| Header "Book a Demo" | `/contact` | `contact` |
| Mobile menu CTA | `/contact` | `contact` |
| CTA buttons | `/contact`, `/solution` | `contact`, `solution` |
| Related (sidebar) | `/<lang>/blog/articles/<slug>` | `blog/articles/<slug>` |
| Recommended (grid) | `/<lang>/blog/articles/<slug>` | `blog/articles/<slug>` |
| Footer nav | `/solution`, `/industries`, `/about`, `/contact`, `/privacy`, `/terms`, `/cookies`, `/security` | `solution`, etc. |

Language prefix for Related/Recommended:
- EN:          `/blog/articles/<slug>`
- zh-CN:       `/zh-cn/blog/articles/<slug>`
- zh-TW:       `/zh-tw/blog/articles/<slug>`
(the slug is language-neutral; the prefix selects the language version)

## 3. Share buttons
- Markup (sidebar): buttons `id="share-linkedin"`, `id="share-x"`, `id="share-copy"`.
  No WeChat button in markup (JS guards for it).
- JS (`/js/article.js`) uses `window.__ARTICLE_TITLE__` (set per article) for the share title —
  do NOT hardcode a single title for all articles.
- Share handlers are null-guarded so a missing button never breaks the others.

## 4. Recommended card excerpts
- `.recommended-card-excerpt` is currently empty in many articles (cosmetic blank space).
  Populate from the article meta description when available; otherwise leave the tag empty.

## Batch-fix script
`_batch_pipeline/fix_layout.py` swaps the live footer in and fixes all links for the
`verified` (deepseek-harness) set across EN/zh-CN/zh-TW. Re-run after any future
harness rewrite that regresses layout.
