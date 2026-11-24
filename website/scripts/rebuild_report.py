#!/usr/bin/env python3
"""Summarise the rebuilt window for the handover report.

Reads the live file tree (not the run log) so the numbers reflect what is
actually on disk: article counts per language, length distribution, visual and
schema coverage, and Traditional Chinese leakage.

Usage: python3 scripts/rebuild_report.py [--from 20260918] [--json out.json]
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = [("en", "blog/articles"), ("zh-cn", "zh-cn/blog/articles"), ("zh-hk", "zh-hk/blog/articles")]
SIMPLE_PAIRS = (
    "这這 图圖 从從 链鏈 时時 与與 为為 说說 问問 关關 实實 现現 业業 务務 数數 据據 训訓 练練 "
    "计計 划劃 户戶 体體 验驗 点點 击擊 详詳 细細 选選 择擇 应應 该該 来來 过過 还還 设設 备備 "
    "网網 络絡 国國 际際 开開 确確 优優 运運 营營 视視 频頻 认認 复復 杂雜 简簡 单單 变變 动動 "
    "态態 处處 转轉 输輸 连連 统統 结結 构構 组組 织織 团團 队隊 员員 价價 观觀 测測 试試 证證 "
    "风風 险險 预預 权權 审審 凭憑 钥鑰 缓緩 并並 发發 线線 内內 盘盤"
)
SIMP = {p.split()[0] for p in SIMPLE_PAIRS.split()}


def body(text: str) -> str:
    m = re.search(r'<article class="ar-body".*?</article>', text, re.S)
    if not m:
        return ""
    chunk = m.group()
    for block in ("ar-related", "ar-lead-end", "ar-lead-inline"):
        chunk = re.sub(r'<(section|div)[^>]*class="%s".*?</\1>' % block, " ", chunk, flags=re.S)
    return re.sub(r"<[^>]+>", " ", chunk)


def measure(path: Path, lang: str) -> dict:
    text = path.read_text(errors="ignore")
    plain = re.sub(r"&[a-zA-Z#0-9]+;", " ", body(text))
    size = (len(re.findall(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*", plain)) if lang == "en"
            else len(re.findall(r"[\u4e00-\u9fff]", plain)))
    return {
        "slug": path.stem,
        "size": size,
        "flow": 'class="ar-flow"' in text,
        "bars": 'class="ar-bars"' in text,
        "matrix": 'class="ar-matrix"' in text,
        "donut": 'class="ar-donut"' in text,
        "trend": 'class="ar-trend"' in text,
        "roadmap": 'class="ar-roadmap"' in text,
        "figure": 'class="ar-figure"' in text,
        "schemas": sum(1 for s in ('"Article"', '"BreadcrumbList"', '"HowTo"', '"FAQPage"') if s in text),
        "share": text.count('id="share-'),
        "backtotop": "back-to-top" in text,
        "section_sign": "§" in plain,
        "hk_leak": "".join(sorted({c for c in text.replace("简体中文", "") if c in SIMP})) if lang == "zh-hk" else "",
        "has_card": (ROOT / f"assets/blog/social/{lang}/{path.stem}.jpg").exists(),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="20260918")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    summary, rows = {}, []
    for lang, folder in LANGS:
        files = [p for p in sorted((ROOT / folder).glob("*.html"))
                 if p.stem[-8:].isdigit() and p.stem[-8:] >= args.start]
        data = [measure(p, lang) for p in files]
        rows.extend({"lang": lang, **d} for d in data)
        sizes = [d["size"] for d in data]
        low, high = (2000, 3000) if lang == "en" else (3500, 5000)
        summary[lang] = {
            "articles": len(data),
            "size_min": min(sizes) if sizes else 0,
            "size_median": sorted(sizes)[len(sizes) // 2] if sizes else 0,
            "size_max": max(sizes) if sizes else 0,
            "in_band": sum(1 for s in sizes if low <= s <= high),
            "six_blocks": sum(1 for d in data if all(d[k] for k in ("flow", "bars", "matrix", "donut", "trend", "roadmap"))),
            "figure": sum(1 for d in data if d["figure"]),
            "four_schema": sum(1 for d in data if d["schemas"] == 4),
            "five_share": sum(1 for d in data if d["share"] == 5),
            "no_backtotop": sum(1 for d in data if not d["backtotop"]),
            "cards": sum(1 for d in data if d["has_card"]),
            "section_sign": sum(1 for d in data if d["section_sign"]),
            "hk_leak": sum(1 for d in data if d["hk_leak"]),
        }

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if args.json:
        Path(args.json).write_text(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
