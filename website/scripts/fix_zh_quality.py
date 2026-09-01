#!/usr/bin/env python3
"""Fix zh article content-quality defects (2026-09-01 deep-dive review).

SAFE, deterministic fixes only:
  1. Remove exact-duplicate <p> within <article> (keep FIRST occurrence).
  2. Prose-FAQ heading de-duplication:
     - plain <h2>常见问题</h2> when the canonical faq-section widget also
       exists in the file  -> rename to 要点问答 / 重點問答 (keeps content,
       kills the double-「常见问题」heading confusion).
     - <h2>Frequently Asked Questions</h2> -> 要点问答 / 重點問答 (widget
       present) or 常见问题 / 常見問題 (no widget — pure translation fix).
     The faq-section widget's own <h2 class="faq-section-title"> is untouched.
  3. Hand-curated paragraph translations (2 files, exact-match replacement).

NOT auto-fixed (editorial follow-up, listed in the report):
  - same-title sections with DIFFERENT content (mislabeled h2)
  - fully-English content sections (need real translation)
  - franken articles (English TOC/lead)

Usage: python3 scripts/fix_zh_quality.py [--apply]   (default = dry run)
"""
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
APPLY = "--apply" in sys.argv

P_RE = re.compile(r"<p[^>]*>.*?</p>", re.S)
TAG_RE = re.compile(r"<[^>]+>")


def norm_text(fragment: str) -> str:
    s = re.sub(r"&nbsp;|&amp;|&lt;|&gt;|&quot;", " ", fragment)
    s = TAG_RE.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


def vis_text(fragment: str) -> str:
    """visible text excluding svg/button internals"""
    s = re.sub(r"<svg.*?</svg>", "", fragment, flags=re.S)
    return norm_text(s)


# hand-curated translations (exact full-<p> replacement)
HAND_FIX = {
    "bias-detection-in-training-data-tools-and-techniques.html": {
        "zh-cn": (
            "The practical takeaway is that bias detection is not a one-time audit but a standing capability.",
            "<p>实践层面的结论是：偏见检测不是一次性的审计动作，而是一项需要长期在岗的能力。把它当作一个正式控制项来对待——可度量、有门禁、持续监控——的团队，能把声誉风险转化为竞争优势，因为利益相关方只会信任他们看得见正在被检查的系统。每个训练周期都跑子群体评估的成本，远远低于部署之后才发现模型悄悄损害了某个受保护群体的代价。</p>",
        ),
        "zh-tw": (
            "The practical takeaway is that bias detection is not a one-time audit but a standing capability.",
            "<p>實務層面的結論是：偏見檢測不是一次性的稽核動作，而是一項需要長期在崗的能力。把它當作一個正式控制項來對待——可度量、有門檻、持續監控——的團隊，能把聲譽風險轉化為競爭優勢，因為利益相關方只會信任他們看得見正在被檢查的系統。每個訓練週期都跑子群體評估的成本，遠低於部署之後才發現模型悄悄損害了某個受保護群體的代價。</p>",
        ),
    },
    "real-time-data-streaming-for-ai-powered-decisions.html": {
        "zh-cn": (
            "The load-bearing points are worth isolating from the detail.",
            "<p>值得把最关键的支撑点从细节中单独拎出来看。</p>",
        ),
        "zh-tw": (
            "The load-bearing points are worth isolating from the detail.",
            "<p>值得把最關鍵的支撐點從細節中單獨拎出來看。</p>",
        ),
    },
}

# follow-up lists (editorial)
FOLLOWUP = {"dup_sections": [], "en_sections": [], "franken": []}


def fix_file(path: Path, lang: str):
    html = path.read_text(encoding="utf-8")
    orig = html
    art_m = re.search(r"<article[^>]*>.*?</article>", html, re.S)
    if not art_m:
        return None
    stats = Counter()
    body = art_m.group(0)

    # ---- rule 1: exact-duplicate paragraphs (keep first) ----
    seen = set()

    def p_dedup(m):
        raw = m.group(0)
        t = norm_text(raw)
        if len(t) > 40:
            if t in seen:
                stats["dup_para_removed"] += 1
                return ""
            seen.add(t)
        return raw

    body = P_RE.sub(p_dedup, body)

    # ---- rule 2: FAQ heading de-duplication & translation ----
    has_widget = 'class="faq-section' in body
    faq_label = "重點問答" if lang == "zh-tw" else "要点问答"
    faq_std = "常見問題" if lang == "zh-tw" else "常见问题"
    en_faq = "frequently asked questions"

    # 2a. widget <h2 class="faq-section-title"> with ENGLISH text → translate
    #     (the 50-file "Frequently Asked Questions" widget-title leak)
    def widget_h2_fix(m):
        raw = m.group(0)
        if 'faq-section-title' not in raw:
            return raw
        t = vis_text(raw)
        if t.lower().rstrip("?").strip() == en_faq:
            stats["en_faq_renamed"] += 1
            fixed = re.sub(r"(<h2[^>]*>)(.*?)(</h2>)",
                           lambda mm: mm.group(1) + re.sub(r"<svg.*?</svg>", "", mm.group(2), flags=re.S).rstrip() + faq_std + mm.group(3),
                           raw, flags=re.S)
            return fixed
        return raw

    body = re.sub(r"<h2[^>]*>.*?</h2>", widget_h2_fix, body, flags=re.S)
    # widget section aria-label
    body = body.replace('aria-label="Frequently Asked Questions"', f'aria-label="{faq_std}"')

    # 2b. prose FAQ headings (no svg / no widget class) — rename until stable
    while True:
        pending = []
        for m in re.finditer(r"<h2[^>]*>.*?</h2>", body, re.S):
            raw = m.group(0)
            if 'faq-section-title' in raw or "<svg" in raw:
                continue
            t = vis_text(raw)
            is_en = t.lower().rstrip("?").strip() == en_faq
            if t == faq_std or is_en:
                pending.append((m.start(), m.end(), raw, is_en, t))
        if not pending:
            break
        s, e, raw, is_en, t = pending[0]
        prose_count = sum(1 for p in pending if not p[3] and p[4] == faq_std)
        en_count = sum(1 for p in pending if p[3])
        if has_widget:
            new_t = faq_label
            stats["en_faq_renamed" if is_en else "dup_faq_renamed"] += 1
        elif is_en and len(pending) == en_count and prose_count == 0:
            new_t = faq_std            # first (only EN) canonical heading
            stats["en_faq_renamed"] += 1
        elif not is_en and t == faq_std:
            # no widget: only rename if this is a DUPLICATE 常见问题
            others = [p for p in pending if p[4] == faq_std]
            if len(others) <= 1 and en_count == 0:
                break                   # single canonical prose FAQ — fine
            new_t = faq_label
            stats["dup_faq_renamed"] += 1
        else:
            new_t = faq_label
            stats["dup_faq_renamed"] += 1
        fixed = re.sub(r"(<h2[^>]*>).*(</h2>)", lambda mm: mm.group(1) + new_t + mm.group(2), raw, flags=re.S)
        body = body[:s] + fixed + body[e:]

    # ---- rule 3: hand-curated paragraph translations ----
    hf = HAND_FIX.get(path.name, {}).get(lang)
    if hf:
        marker, replacement = hf
        # find the <p> whose visible text starts with the marker
        for m in list(P_RE.finditer(body)):
            if norm_text(m.group(0)).startswith(marker[:60]):
                body = body[: m.start()] + replacement + body[m.end():]
                stats["hand_translated"] += 1
                break

    # ---- editorial follow-up detection (report only) ----
    h2s = [vis_text(h.group(0)) for h in re.finditer(r"<h2[^>]*>.*?</h2>", body, re.S)]
    hc = Counter(h2s)
    for t, n in hc.items():
        if n > 1 and len(t) > 3 and t != faq_std:
            FOLLOWUP["dup_sections"].append(f"{lang}/{path.name}: {t} x{n}")

    def latin_only(s):
        s = re.sub(r"[\s\d\W]", "", s)
        return len(s) >= 8 and all(ord(c) < 0x2E80 for c in s)

    en_h2 = [t for t in h2s if latin_only(t)]
    if en_h2:
        FOLLOWUP["en_sections"].append(f"{lang}/{path.name}: {en_h2[:4]}")
    if norm_text(body).startswith("Table of Contents") or "toc-mobile" in body and "The Data Silo Problem" in body:
        FOLLOWUP["franken"].append(f"{lang}/{path.name}")

    if body != art_m.group(0):
        html = html[: art_m.start()] + body + html[art_m.end():]
    if APPLY and html != orig:
        path.write_text(html, encoding="utf-8")
    return stats


def main():
    total = Counter()
    changed = 0
    for lang in ("zh-cn", "zh-tw"):
        for f in sorted((ROOT / lang / "blog" / "articles").glob("*.html")):
            st = fix_file(f, lang)
            if st:
                total.update(st)
                if sum(st.values()):
                    changed += 1
    mode = "APPLIED" if APPLY else "DRY RUN"
    print(f"=== {mode} === files changed: {changed}")
    print(f"dup paragraphs removed : {total['dup_para_removed']}")
    print(f"dup prose-FAQ renamed  : {total['dup_faq_renamed']}")
    print(f"EN FAQ heading renamed : {total['en_faq_renamed']}")
    print(f"hand translations      : {total['hand_translated']}")
    print(f"\neditorial follow-up: dup-sections={len(set(FOLLOWUP['dup_sections']))} "
          f"en-sections={len(set(FOLLOWUP['en_sections']))} franken={len(set(FOLLOWUP['franken']))}")
    rep = ROOT / "zh-quality-followup-2026-09-01.txt"
    with open(rep, "w", encoding="utf-8") as w:
        for k, items in FOLLOWUP.items():
            w.write(f"===== {k} ({len(set(items))}) =====\n")
            for it in sorted(set(items)):
                w.write(it + "\n")
            w.write("\n")
    print("follow-up list ->", rep)


if __name__ == "__main__":
    main()
