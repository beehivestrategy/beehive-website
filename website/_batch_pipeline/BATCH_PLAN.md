# Blog Content Batch Rewrite Plan — model-limit-resilient

> Source of truth for the full-corpus content rewrite. Mirror: `04 - Projects/Blog Batch Rewrite Plan.md` (Obsidian vault).
> Last updated: 2026-08-25.

## 1. Current state (audit, 2026-08-25)
- Corpus: **1,067 articles × 3 langs = 3,201 files**.
- **21 slugs fully done** (EN + zh-CN + zh-TW verified, manifests updated). 5 completed this session:
  `ai-knowledge-management-assistant-2026` (full rewrite, 2,510w EN / 4,573 CJK zh-CN, clean tail),
  `customer-journey-analytics-ai`, `industry-llm-deployment-strategy-2026`,
  `future-of-business-intelligence-2027`, `automated-data-lineage-ai-2026` (near-threshold topups).
- **status.json (2026-08-25 eve):** `verified=21`, `wave0_pending=20`, `pending=1026` (sum 1,067). Pipeline proven end-to-end (splice → gen_zhtw_one → verify → checkpoint).
- At canonical floor: EN **2%** (22/1,067, avg 1,028w); zh-CN **51%** (546); zh-TW **50%** (543).
- Layout strong: H2≥4 ~99% all langs; CTA 100% (zh uses 预约演示).
- GEO gaps: ~30% lack an FAQ section; ~20–29% lack FAQPage JSON-LD; only ~28% of zh articles use question-style H2s.
- **Blockers observed:**
  1. `402 INSUFFICIENT_BALANCE` — appeared **only** when the pipeline spawned **sub-agents** (parallel mode); a generic quota/billing error from the model gateway. **Does NOT affect the inline (main-agent) path** — proven: 5 full articles hand-written this session with zero 402s. Root billing system is **unverified** (no "TokenHub" reference exists anywhere in the environment; that was a prior-session guess in this doc). Likely the model gateway's own quota.
  2. Agent-tool infra fault — `Cannot read properties of undefined (reading 'history')`; sub-agent spawning fully broken even for trivial calls.

## 2. Goal
Bring **every** article to the canonical floor and GEO baseline:
- **EN:** 2,500–3,500 words (floor 2,500; absolute min 1,200).
- **zh-CN / zh-TW:** 3,500–5,000 CJK (floor 3,500; absolute min 1,800).
- **GEO backfill (all langs):** FAQ section + FAQPage JSON-LD + ≥1 question-style H2.

## 3. Resilience principles (built for model limits)
1. **Fixed small batches (8 slugs).** A failure loses ≤1 batch, never the run.
2. **Status manifest = source of truth.** `status.json` records per-slug state:
   `pending → en_done → zhcn_done → zhtw_done → verified → deployed`.
   Resume = process only non-final states. No double work.
3. **Per-batch verify gate.** Run `verify_article.py` after each batch; advance only slugs that pass
   (word/CJK floor, balanced divs, CTA, FAQ section, FAQPage JSON-LD, hreflang, canonical, og:locale).
   Failed slugs stay `pending` for retry (max 3 tries → `failed_slugs.json` for manual review).
4. **Probe before spend.** Tiny model probe at each wave start; on `402`, **STOP + notify** — never loop-retry into a dead balance.
5. **Dual execution mode:**
   - *Agent mode (preferred, when Agent tool healthy):* N=5 background agents, disjoint batches of 8; bounded concurrency to avoid throttle.
   - *Inline fallback (Agent tool broken):* main loop processes 1–2 slugs/turn, writes file, verifies; small batches keep context under limit. Checkpoint every slug. Same end result, just slower.
6. **Wave-based, impact-ordered.** Never one giant pass.
7. **Deploy gated + explicit.** Regenerate index/sitemap + `wrangler deploy` only after a full wave passes verification, and only with explicit user confirmation (postpaid/billing + irreversible).

## 4. Wave plan
- **Wave 0 — Finish incomplete (26 slugs).** 4 partial (agentic-etl-pipelines-2026, customer-journey-analytics-ai, industry-llm-deployment-strategy-2026, real-time-decisioning-ai-operations-2026) + 22 untouched from Wave 1. Lowest cost; completes what's started.
- **Wave A — Aug-2026 thin batch (~198 slugs).** Worst SEO damage (all <800w). Highest priority.
- **Wave B — 2026 Jan–Jul zh degradation.** zh fell to ~1,831 CJK; expand zh-CN to floor, regenerate zh-TW via OpenCC.
- **Wave C — Remaining EN-to-pillar depth.** Bring EN to 2,500–3,500w; add FAQ + JSON-LD + question H2s across all.
- **Wave D — GEO backfill sweep.** For articles already at length but missing FAQ section / FAQPage JSON-LD / question H2s, add them (cheap, no full rewrite).

## 5. Tooling (already in `website/_batch_pipeline/`)
- `template_spec.py` — canonical design (H2 structure, CTA, FAQ + JSON-LD).
- `verify_article.py` — gate (region-capture fix + case-insensitive CTA check).
- `gen_zhtw.py` — OpenCC s2t transform + head fixes + manifest updates.
- `AGENT_BRIEF.md` — rules brief for rewrite agents.
- `audit_report.html` — corpus-wide word/layout/GEO audit.

## 6. Per-slug rewrite procedure
1. Read EN source (or thin EN body) from `website/blog/articles/<slug>.html`.
2. **Expand EN** to 2,500–3,500w: H2 structure (≥4 H2s, ≥1 question-style), answer-first, ≥3 stats, ≥1 table/list, internal links, FAQ section (8+ Q&A), FAQPage JSON-LD, "Book a Demo" CTA, dateModified refresh.
3. **Translate to zh-CN** (3,500–5,000 CJK), same structure, CTA = 预约演示.
4. **Generate zh-TW** mechanically via `gen_zhtw.py` (OpenCC s2t + head fixes).
5. **Verify** all three with `verify_article.py`; update `status.json`.
6. After wave passes: regen index (`generate_blog_index_all.py`, `generate_blog_shadows.py`) + sitemap + deploy (user-confirmed).

## 7. Resume / recover procedure
- On interruption (model 402, Agent fault, crash): re-run the wave launcher → reads `status.json`, skips done slugs, reprocesses `pending`/`failed`.
- No double work. Max 3 retries/slug, then quarantine.

## 8. Production deploy (explicit only)
From `website/`:
`npx wrangler pages deploy . --project-name=beehive-strategy --commit-dirty`
Preceded by `generate_blog_index_all.py` + `generate_blog_shadows.py` + `generate_sitemap_full.py`.
**NOT auto-run** — waits for explicit user go-ahead.

## 9. Open risks
- **Billing:** the `402` was a sub-agent-only quota error; the **inline path needs no billing** and is fully working. Parallel/volume mode additionally needs the Agent-tool infra fault fixed (separate issue).
- **Agent tool:** infra fault must be resolved (reload WorkBuddy / check outage) to use parallel mode; otherwise inline fallback (slower, same result).
- **Trae pipeline:** confirmed **inactive** — no new content from it; do not wait for it. Remediation is this batch program.
