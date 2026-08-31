# Fleet Progress Tracker — Blog GEO/SEO Rewrite (1,061 slugs × 3 langs)

## Last updated: 2026-08-30 01:10 HKT

### True content-audit state (audit_content.py, fresh run)
- Per-language at standard: EN **446/1061**, zh-CN **697/1061**, zh-TW **697/1061**.
- **Slugs fully at standard (all 3 langs): 399/1061** (1061 − 662 gaps).
- **Slugs NOT fully at standard: 662** → split into **45 gap batches** (gbatch_001..045, 15 slugs each) in `gap_batches/`.
- Dominant gap: EN length (608 EN len_fail vs 364 zh).

### This session (2026-08-29 21:40 → 2026-08-30 01:10 HKT)
- Free re-audit: 345 → 395 fully standard (reasoning batches 001–003 + lite batches completed).
- **Regenerated 45 gap batches** from authoritative 666-slug audit.
- **lite model bypasses the wall** and handles 4-slug batches cleanly (single-slug and 4-slug both verified). Used for immediate progress while default/reasoning buckets are walled.
- **reasoning bucket walled until 2026-08-30 21:41 HKT** (its own per-model quota).
- **default bucket walled until 2026-08-30 02:52 HKT** (resets soon — the main engine).

### Free hardening DONE (no LLM quota)
- **zh-TW canonical fix: 178 files** had `<link rel="canonical">` + `og:url` pointing to `/zh-cn/` instead of `/zh-tw/` → all corrected to self-canonical `/zh-tw/` (hreflang alternates left intact). Verified 0 remaining mismatches across all 3 langs.
- **JSON-LD dedupe: 289 redundant blocks removed** — rewrite agents had been adding BODY copies on top of pre-existing HEAD copies (duplicate FAQPage JSON-LD). Now exactly ONE per file; 0 need manual review. NOTE: dedupe keeps the HEAD copy when both exist — head/boby placement is acceptable for SEO (JSON-LD valid anywhere), but FINALIZE's `backfill_jsonld.py` should be allowed to normalize to BODY if desired.
- `backfill_jsonld.py` (FINALIZE) regenerates all JSON-LD from on-page FAQ.

### Auto-resume automation (v2 — the driver)
- **automation-1788022239728** "Beehive Blog Fleet Resume + Deploy (v2)"
  - Recurring every 2h, **validFrom 2026-08-30T03:00**, validUntil 2026-10-15.
  - NOTE: the earlier v1 (automation-1787943560891) **vanished** (not found on list) — recreated as v2.
  - Each firing: DONE-guard (FLEET_DONE.flag) → audit → regenerate gap batches → launch ≤3 background agents (model: default, 15-slug batches) → 429-stop → loop. When `not_ok` empty → FINALIZE (dedupe → backfill → 3 root generators → wrangler deploy PROD → curl verify → write FLEET_DONE.flag → self-delete).
  - Fires at 03:00 right after the default-model quota reset (02:52), so the main engine resumes unattended.

### Rate-limit wall — per-model buckets (confirmed)
- 429 is **per-model**. `reasoning` and `lite` each have separate buckets; `default` is the main one (resets 02:52).
- Spawn ceiling: 1–2 background agents reliably; 3+ in one message → 499/“Agent not found”. `lite` viable for 1–4 slug batches only (small context; 15-slug → 400 input too long).
- `default` model (full context) is preferred for 15-slug batches once its bucket frees at 02:52.

### Key files
- `SUBAGENT_BRIEF_STANDARD.md` — agent instructions + guardrails (single source of truth).
- `audit_content.py` — compliance audit (source of truth).
- `dedupe_jsonld.py` / `backfill_jsonld.py` / `scan_dupe.py` — JSON-LD hygiene.
- `fix_zhtw_canonical.py` — canonical/og:url correction (already run, 178 files).
- `gap_batches/gbatch_NNN.txt` — current 666-gap batch list (regenerated 01:10).
- Root generators in `website/`: generate_blog_index_all.py, generate_blog_shadows.py, generate_sitemap_full.py.
- Deploy: `cd website && npx wrangler@4 pages deploy . --project-name beehive-strategy --commit-dirty`
