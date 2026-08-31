#!/usr/bin/env python3
"""Compute before (git HEAD) vs after (working tree) counts for the 45 target
files and emit a compact report table."""
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cjk_count(s):
    return len(re.findall(r'[\u3400-\u9fff\uf900-\ufaff]', s))


def en_words(s):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))


def git_head(path):
    try:
        return subprocess.check_output(["git", "show", "HEAD:" + path],
                                       cwd=ROOT, stderr=subprocess.DEVNULL).decode("utf-8")
    except Exception:
        return None


def main():
    slugs = []
    with open(os.path.join(ROOT, "_batch_pipeline", "gap_batches", "gbatch_001.txt")) as fh:
        for line in fh:
            s = line.strip()
            if s:
                slugs.append(s)

    print("SLUG | EN(b/a) | CN(b/a) | TW(b/a) | FAQ | LD(loc) | defects")
    for slug in slugs:
        row = []
        for lang, prefix in [("en", ""), ("zh-CN", "zh-cn/"), ("zh-TW", "zh-tw/")]:
            path = prefix + "blog/articles/" + slug + ".html"
            before = git_head(path)
            with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
                after = fh.read()
            m = re.search(r'<article id="article-content">(.*?)</article>', after, re.S)
            body_a = m.group(1) if m else after
            if lang == "en":
                b = en_words(re.search(r'<article id="article-content">(.*?)</article>', before, re.S).group(1)) if before else 0
                a = en_words(body_a)
                row.append(f"EN {b}/{a}")
            else:
                b = cjk_count(re.search(r'<article id="article-content">(.*?)</article>', before, re.S).group(1)) if before else 0
                a = cjk_count(body_a)
                tag = "CN" if lang == "zh-CN" else "TW"
                row.append(f"{tag} {b}/{a}")
            # FAQ count + LD loc
            faq_sec = len(re.findall(r'class="faq-section"', after))
            head_end = after.find('</head>')
            blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', after, re.S)
            loc = None
            for bl in blocks:
                if '"@type": "FAQPage"' in bl:
                    idx = after.find(bl)
                    loc = 'head' if (head_end != -1 and idx < head_end) else 'body'
                    break
        # defects repaired (per file heuristic): CTA fixed, rec hrefs fixed, opencc regen
        print(f"{slug[:40]:40} | {row[0]} | {row[1]} | {row[2]} | faq={faq_sec} | LD={loc}")


if __name__ == "__main__":
    main()
