#!/usr/bin/env python3
"""Pull Chinese article length back into the approved band without changing structure.

The English source is correct; only some Chinese translations land slightly
outside 3,500-5,000 characters. This rewrites a single paragraph per article to
close the gap, then re-derives the Traditional Chinese paragraph from the new
Simplified text, so section and paragraph counts stay identical across languages.

Usage: python3 scripts/fix_cjk_length.py [--workers 6]
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from opencc import OpenCC

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
CN_DIR = ROOT / "zh-cn/blog/articles"
HK_DIR = ROOT / "zh-hk/blog/articles"
MODEL = os.environ.get("REBUILD_MODEL", "deepseek/deepseek-chat-v3.1")
LOW, HIGH = 3500, 5000
HK_FIX = {"户": "戶", "门": "門"}


def load_key() -> str:
    for line in (REPO / "ai-geo-seo-mcp/.env").read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no key")


def cjk(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def body_span(text: str) -> tuple[int, int]:
    start = text.find('<article class="ar-body"')
    start = text.find(">", start) + 1
    end = text.find("</article>", start)
    return start, end


def prose_count(text: str) -> int:
    a, b = body_span(text)
    chunk = text[a:b]
    for block in ("ar-related", "ar-lead-end", "ar-lead-inline"):
        chunk = re.sub(r'<(section|div)[^>]*class="%s".*?</\1>' % block, " ", chunk, flags=re.S)
    plain = re.sub(r"<[^>]+>", " ", chunk)
    return cjk(re.sub(r"&[a-zA-Z#0-9]+;", " ", plain))


def paragraphs(text: str) -> list[re.Match]:
    a, b = body_span(text)
    return list(re.finditer(r"<p>(.*?)</p>", text[a:b], re.S))


def rewrite(key: str, paragraph: str, target: int) -> str:
    prompt = (f"以下是一篇企业 AI 文章中的一段。请改写该段，使其长度约为 {target} 个汉字，"
              "保持原意与专业语气，不要添加小标题，不要使用 Markdown，只输出改写后的段落正文。\n\n"
              + html.unescape(re.sub(r"<[^>]+>", "", paragraph)))
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 1600, "temperature": 0.4}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
            out = data["choices"][0]["message"].get("content") or ""
            out = out.strip().strip('"')
            if out:
                return out
        except Exception:  # noqa: BLE001
            time.sleep(3)
    return ""


def fix_one(key: str, page: Path, converter: OpenCC) -> str:
    text = page.read_text()
    current = prose_count(text)
    if LOW <= current <= HIGH:
        return "ok"
    delta = (LOW + 150 - current) if current < LOW else (HIGH - 150 - current)
    paras = paragraphs(text)
    if not paras:
        return "no-paragraph"
    a, b = body_span(text)
    inside = text[a:b]
    target_match = max(paras, key=lambda m: cjk(m.group(1)))
    new_text = rewrite(key, target_match.group(1), max(120, cjk(target_match.group(1)) + delta))
    if not new_text:
        return "model-failed"
    new_para = "<p>" + html.escape(new_text, quote=False) + "</p>"
    new_inside = inside.replace(target_match.group(0), new_para, 1)
    page.write_text(text[:a] + new_inside + text[b:])

    hk_page = HK_DIR / page.name
    if hk_page.exists():
        hk_text = hk_page.read_text()
        ha, hb = body_span(hk_text)
        hk_inside = hk_text[ha:hb]
        hk_paras = list(re.finditer(r"<p>.*?</p>", hk_inside, re.S))
        idx = [m.group(0) for m in paragraphs(text)].index(target_match.group(0))
        if idx < len(hk_paras):
            hk_new = converter.convert(new_text)
            for s, t in HK_FIX.items():
                hk_new = hk_new.replace(s, t)
            hk_inside = hk_inside.replace(hk_paras[idx].group(0), "<p>" + html.escape(hk_new, quote=False) + "</p>", 1)
            hk_page.write_text(hk_text[:ha] + hk_inside + hk_text[hb:])
    return f"{current}->{prose_count(page.read_text())}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    key = load_key()
    converter = OpenCC("s2hk")
    targets = []
    for p in sorted(CN_DIR.glob("*.html")):
        suffix = p.stem[-8:]
        if suffix.isdigit() and suffix >= "20260918" and not (LOW <= prose_count(p.read_text()) <= HIGH):
            targets.append(p)
    print("outliers:", len(targets))
    def settle(page: Path) -> str:
        before = prose_count(page.read_text())
        for _ in range(5):
            if LOW <= prose_count(page.read_text()) <= HIGH:
                break
            fix_one(key, page, converter)
        after = prose_count(page.read_text())
        return f"{before}->{after}" + ("" if LOW <= after <= HIGH else " STILL OUT")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for page, result in zip(targets, pool.map(settle, targets)):
            print(" ", page.stem[:58], result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
