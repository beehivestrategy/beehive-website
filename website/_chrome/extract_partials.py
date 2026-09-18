#!/usr/bin/env python3
"""
extract_partials.py — 从三语 fde 模板抽取 chrome 块到 _chrome/_partials/，
作为 build_chrome.py 的单一事实源。仅在模板设计变更时运行。

输出:
  _chrome/_partials/{en,zh-cn,zh-tw}/{header,footer,mobile}.html
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "_partials")
TEMPLATES = {"en": "fde.html", "zh-cn": "zh-cn/fde.html", "zh-tw": "zh-tw/fde.html"}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def blk(s, tag):
    m = re.search(r"<%s[\s\S]*?</%s>" % (tag, tag), s)
    return m.group(0) if m else None


def find_div_span(raw, start):
    depth = 0
    for m in re.finditer(r"<div\b|</div>", raw[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return start + m.end()
    raise ValueError("unbalanced div at %d" % start)


def mobile_block(s):
    i = s.find('<div class="mobile-menu" id="mobile-menu"')
    return s[i:find_div_span(s, i)]


def main():
    for lang, rel in TEMPLATES.items():
        raw = read(os.path.join(ROOT, rel))
        header = blk(raw, "header")
        footer = blk(raw, "footer")
        mobile = mobile_block(raw)
        d = os.path.join(OUT, lang)
        os.makedirs(d, exist_ok=True)
        for name, content in (("header.html", header),
                              ("footer.html", footer),
                              ("mobile.html", mobile)):
            open(os.path.join(d, name), "w", encoding="utf-8").write(content)
        print("extracted %-6s header=%d footer=%d mobile=%d" % (
            lang, len(header), len(footer), len(mobile)))


if __name__ == "__main__":
    main()
