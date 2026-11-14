# GEO Citation Baseline & Tracking Protocol
> Beehive Strategy · Established 2026-10-05 (Day 0)
> Companion to `seo-geo-strategy.html` (six-layer SEO/AEO/GEO/GAO/GMO/GDO research)

## 0. Why this document exists
The prior strategy doc defined *what* GEO is and *how* to optimise for it. It did **not** establish *how we measure whether AI engines actually cite us*. This document is the Day-0 baseline + the recurring measurement protocol. Without a baseline, "we improved GEO" is unprovable.

Status before this doc: **zero measurement** of AI citations. Every future comparison is measured against the numbers captured here.

---

## 1. Engines tracked (and why)
| Engine | Role in GEO | How it surfaces Beehive | Probe method |
|---|---|---|---|
| **ChatGPT** (OpenAI) | Highest consumer reach | Web-browsing answers, GPTs | Manual prompt / API (paid) — auth-gated |
| **Perplexity** | Citation-first; most transparent | Always shows source links | Perplexity API (paid key) or manual |
| **Claude** (Anthropic) | Long-form, enterprise | Web fetch in answers | Manual / API (paid) — auth-gated |
| **Gemini** (Google) | Tied to Search index | AI Overviews + direct answers | Manual / Vertex — tied to Google index |
| **Google AI Overviews** | Gatekeeper of traditional search | Surfaces before organic | GSC + manual query |

We treat **Bing index coverage** as a proxy signal because Bing is a primary crawl source for several LLMs and is programmatically checkable (unlike the chat UIs).

---

## 2. Day-0 GEO Readiness Baseline (measured 2026-10-05)
These are facts we can verify today — the "are we even eligible to be cited" layer.

| Asset | State | Evidence | Action |
|---|---|---|---|
| `llms.txt` present | ✅ Yes | 7.3 KB, lists Home/Solution/Services/Industries/Case Studies/Pricing/About/Contact/**Credentials**/Blog + 1,140 EN articles | Keep maintained; refresh on content drops |
| `robots.txt` allows AI crawlers + `llms.txt` | ✅ Yes | `Allow: /` for GPTBot, ChatGPT-User, ClaudeBot, Claude-Web, PerplexityBot, Google-Extended, CCBot, Bytespider | No change needed; broad allow covers `llms.txt` |
| JSON-LD on articles | ✅ Yes | Sampled 3 articles → 3 ld+json blocks each (Article + Breadcrumb + Org) | Extend to all static pages |
| Entity anchoring (Layer 1) | ✅ Partial | Organization schema present | Add sameAs to authoritative profiles |
| `credentials.html` (honest capability page) | ✅ New | Added this cycle (fills 404) | Submit to index |
| Case-study honesty disclaimers | ✅ New | 33 articles + 3 indexes flagged "Illustrative scenario" | N/A — done |
| Broken meta descriptions | ✅ Fixed | 403 → 0 across EN/zh-cn/zh-hk | N/A — done |
| Contact trust signals | ✅ New | 3-card bar on all 3 languages | N/A — done |

**Critical Day-0 gap:** `llms.txt` advertises pages (`/solution`, `/services`, `/industries`, `/pricing`, `/about`) — verify each resolves 200, not 404. A 404 in `llms.txt` actively *harms* GEO trust. (Flagged for verification in #826.)

---

## 3. Seed Query Set (probe these every cycle)
Grouped by the topic clusters Beehive owns. Use the **exact** phrasing; record the engine, whether Beehive was cited, the cited URL, and the rank/snippet.

**Cluster A — Conversational BI / NL Analytics**
1. "What is conversational business intelligence?"
2. "How do you build a natural-language analytics layer for non-technical teams?"
3. "Best MCP-driven BI platform for mid-market companies"

**Cluster B — MCP / Agentic AI**
4. "What is the Model Context Protocol and why does it matter for enterprises?"
5. "How to deploy agentic AI inside WeChat Work, DingTalk or Feishu?"
6. "Model Context Protocol use cases in finance and retail"

**Cluster C — Data governance / semantic layer**
7. "How to build a semantic layer without a data warehouse team?"
8. "PIPL compliance for AI systems in Hong Kong and China"

**Cluster D — Industry (retail / manufacturing / finance)**
9. "AI strategy for cross-border retail in Greater Bay Area"
10. "How manufacturers can start with AI-ready data"

**Cluster E — Buying / vendor**
11. "Forward-deployed AI partner vs traditional consulting"
12. "Two-week enterprise AI deployment — realistic?"

Run each on ChatGPT, Perplexity, Claude, Gemini. Target ≥ 1 citation across engines per cluster within 90 days.

---

## 4. Measurement Protocol (monthly, 1st business day)
1. Run the 12 seed queries on all 4 engines (manual or via Perplexity API if key obtained).
2. Log every citation: engine, query, cited URL, snippet, rank.
3. Compute **Citation Rate** = (queries where Beehive cited) / (total queries × engines).
4. Track **Entity Recall** = does the engine name "Beehive Strategy" / "蜂启咨询" unprompted in category answers?
5. Compare vs. prior month; trend line in the tracker sheet.

**Tooling options (when ready to automate):**
- *Otterly.ai* — dedicated LLM visibility tracking (ChatGPT/Perplexity/Gemini).
- *LLMrefs* — AI search rank tracking.
- *Goodie / Brandwatch* — enterprise social + AI mention monitoring.
- *Perplexity API* — cheapest programmatic probe for citation-first answers.
- *Bing Indexing API + site: query* — free proxy for crawl eligibility.

---

## 5. Tracking Template
See `geo_citation_tracking.csv` — pre-filled with the 12 seed queries and empty result columns for Month 1. Copy the sheet each month; the baseline is Month 0 (this doc, §2 readiness only — no live citations captured yet because automated probing requires authenticated sessions/paid keys).

---

## 6. Immediate action items coming out of Day-0
- [x] `robots.txt` already allows AI crawlers + `llms.txt` (broad `Allow: /`) — no change needed.
- [x] Verified all `llms.txt`-advertised pages (solution/services/industries/pricing/about/case-studies/contact) return 200 — no 404 risk.
- [x] Registered new `credentials.html` in `llms.txt` Main Pages (GEO eligibility for honest capability page).
- [ ] Obtain a Perplexity API key (or Otterly trial) to enable Month-1 automated probing.
- [ ] Submit `credentials.html` + updated `case-studies.html` to index (part of #826 deploy).
- [ ] Refresh `llms.txt` blog count after each content batch (currently states 1,140 EN; verify live count).

---
*This is a living baseline. Update §2 only when a structural GEO asset changes; append monthly citation results to the tracker, never overwrite prior months.*
