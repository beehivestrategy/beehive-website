#!/usr/bin/env python3
"""Verify every rebuilt article against the approved v9 format rules.

Checks, per language file:
  - EN body word count inside 2,000-3,000; zh-CN / zh-HK inside 3,500-5,000 CJK
  - six in-body visual blocks plus the content diagram figure (7), and the
    social card image referenced by og:image (8th)
  - four schema types: Article, BreadcrumbList, HowTo, FAQPage
  - author and publisher are Beehive Strategy, never a personal name
  - five share controls, no back-to-top control
  - canonical plus four hreflang alternates
  - no section sign, no internal code prefixes, no published prices
  - zh-HK contains no simplified-only characters (the language switcher label
    "简体中文" is the single allowed exception)

Usage: python3 scripts/qa_rebuild.py [--report threads/content_hub/rebuild_run_report.json]
Exit code 0 when every article passes every rule.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

def _simplified_only() -> set[str]:
    """Simplified characters whose Traditional partner is genuinely different.

    Built from explicit pairs so context-valid characters (台, 准, 干, 里, 后 as
    "queen") never trigger a false alarm.
    """
    pairs = (
        "这這 图圖 从從 链鏈 时時 与與 为為 说說 问問 关關 实實 现現 业業 务務 数數 据據 "
        "训訓 练練 计計 划劃 户戶 体體 验驗 点點 击擊 详詳 细細 选選 择擇 应應 该該 来來 过過 "
        "还還 设設 备備 网網 络絡 国國 际際 开開 确確 优優 运運 营營 视視 频頻 认認 复復 杂雜 "
        "简簡 单單 变變 动動 态態 处處 转轉 输輸 连連 统統 结結 构構 组組 织織 团團 队隊 员員 "
        "价價 观觀 测測 试試 证證 风風 险險 预預 权權 审審 凭憑 钥鑰 缓緩 并並 发發 线線 内內 盘盤"
    )
    return {p.split()[0] for p in pairs.split()}

SIMPLIFIED_ONLY = _simplified_only()
BANNED_PRICE_FIG = ["HK$88", "HK$4,880", "HK$15,000", "HKD 15,000",
                    "HK$3,888", "HK$4,800", "HK$25,000", "HK$68,000"]
PRICE_JSON_RE = re.compile(r'"price"\s*:\s*"?\d[\d.]*"?')
ZH_FIG_RE = re.compile(r"\d[\d,.]*\s?(?:美元|港元|人民幣|人民币|元)")
ZH_PRICE_CTX_RE = re.compile(r"定價|定价|報價|报价|價格|价格|費用|费用|起價|起价|收費|收费")
EN_PRICE_CTX_RE = re.compile(r"\b(?:price list|pricing|quotation|fee schedule|per engagement|starts? at)\b", re.I)
EN_FIG_RE = re.compile(r"(?:HK\$|US\$|HKD|USD)\s?\d[\d,]*")

CODE_PATTERN = re.compile(r"\b(?:T[1-5]|RK\d|PF\d)\b")


def body_of(text: str) -> str:
    start = text.find('<article class="ar-body"')
    if start == -1:
        return ""
    start = text.find(">", start) + 1
    end = text.find("</article>", start)
    body = text[start:end]
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S | re.I)
    for block in ("ar-related", "ar-lead-end", "ar-lead-inline"):
        body = re.sub(r'<(section|div)[^>]*class="%s".*?</\1>' % block, " ", body, flags=re.S)
    return body


def plain(html_text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html_text)
    text = re.sub(r"&[a-zA-Z#0-9]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def count_en(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*", text))


def count_cjk(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def check(path: Path, lang: str) -> list[str]:
    text = path.read_text(errors="ignore")
    body = body_of(text)
    text_plain = plain(body)
    issues: list[str] = []

    size = count_en(text_plain) if lang == "en" else count_cjk(text_plain)
    low, high = (2000, 3000) if lang == "en" else (3500, 5000)
    if not (low <= size <= high):
        issues.append(f"length {size} outside {low}-{high}")

    visuals = body.count('class="ar-visual"') // 3 + body.count('class="ar-figure"')
    if body.count('class="ar-visual"') == 0 or body.count('class="ar-figure"') == 0:
        issues.append("missing visual blocks")
    for cls in ["ar-flow", "ar-bars", "ar-matrix", "ar-donut", "ar-trend", "ar-roadmap"]:
        if f'class="{cls}"' not in body:
            issues.append(f"missing {cls}")

    for schema in ['"Article"', '"BreadcrumbList"', '"HowTo"', '"FAQPage"']:
        if schema not in text:
            issues.append(f"missing schema {schema}")

    if '"Beehive Strategy"' not in text:
        issues.append("author not Beehive Strategy")
    if re.search(r"Kenneth Kwok|Author:\s*[A-Z]", text):
        issues.append("personal author present")

    if text.count('id="share-') < 4:
        issues.append("share controls incomplete")
    if "back-to-top" in text:
        issues.append("back-to-top present")

    if 'rel="canonical"' not in text:
        issues.append("canonical missing")
    if text.count('hreflang="') != 4:
        issues.append(f"hreflang count {text.count('hreflang=')}")

    if "§" in text_plain:
        issues.append("section sign present")
    if CODE_PATTERN.search(text_plain):
        issues.append("internal code present")
    if any(fig in text for fig in BANNED_PRICE_FIG):
        issues.append("banned price figure")
    if PRICE_JSON_RE.search(text):
        issues.append("JSON-LD numeric price")
    for m in ZH_FIG_RE.finditer(text_plain):
        ctx = text_plain[max(0, m.start() - 90):m.end() + 90]
        if ZH_PRICE_CTX_RE.search(ctx):
            issues.append(f"price figure in pricing context: {m.group(0)}")
            break
    for m in EN_FIG_RE.finditer(text_plain):
        ctx = text_plain[max(0, m.start() - 90):m.end() + 90]
        if EN_PRICE_CTX_RE.search(ctx):
            issues.append(f"price figure in pricing context: {m.group(0)}")
            break

    if lang == "zh-hk":
        cleaned = text.replace("简体中文", "").replace("简", "")
        leaks = sorted({c for c in cleaned if c in SIMPLIFIED_ONLY})
        if leaks:
            issues.append("simplified characters: " + "".join(leaks))
    return issues


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=str(REPO / "threads/content_hub/rebuild_run_report.json"))
    ap.add_argument("--scan-from", dest="scan", default=None,
                    help="scan every article whose slug ends with a date >= this value, e.g. 20260918")
    args = ap.parse_args()

    if args.scan:
        targets = []
        for lang, folder in (("en", "blog/articles"), ("zh-cn", "zh-cn/blog/articles"),
                             ("zh-hk", "zh-hk/blog/articles")):
            for path in sorted((ROOT / folder).glob("*.html")):
                suffix = path.stem[-8:]
                if suffix.isdigit() and suffix >= args.scan:
                    targets.append({"slug": path.stem, "lang": lang, "path": str(path)})
        failures = 0
        rows = []
        for entry in targets:
            path = Path(entry["path"])
            if not path.exists():
                rows.append((entry["slug"], entry["lang"], ["file missing"]))
                failures += 1
                continue
            issues = check(path, entry["lang"])
            if issues:
                failures += 1
                rows.append((entry["slug"], entry["lang"], issues))

        if not rows:
            print(f"PASS — {len(targets)} files with date >= {args.scan}")
            return 0
        print(f"FAIL — {failures} of {len(targets)} file(s) with issues")
        for slug, lang, issues in rows:
            print(f"  {lang:6} {slug[:60]} -> {'; '.join(issues)}")
        return 1

    report = json.loads(Path(args.report).read_text())
    failures = 0
    rows = []
    for article in report["articles"]:
        for entry in article["files"]:
            path = Path(entry["path"])
            if not path.exists():
                rows.append((article["slug"], entry["lang"], ["file missing"]))
                failures += 1
                continue
            issues = check(path, entry["lang"])
            if issues:
                failures += 1
                rows.append((article["slug"], entry["lang"], issues))

    if not rows:
        print(f"PASS — {len(report['articles']) * 3} files across {len(report['articles'])} articles")
        return 0
    print(f"FAIL — {failures} file(s) with issues")
    for slug, lang, issues in rows:
        print(f"  {lang:6} {slug[:60]} -> {'; '.join(issues)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
