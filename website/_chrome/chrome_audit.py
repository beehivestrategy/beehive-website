#!/usr/bin/env python3
"""
chrome_audit.py — Beehive 站点 chrome 一致性门禁（部署前必跑，自包含）

Source of truth = 三语 fde 模板（与首页 index.html 同一设计）。
对每页的 <header> / <footer> / mobile-menu 与语言模板比对，
归一化三类合法差异（不算 drift）：
  1. active 状态（nav-link active / 语言锚点 class="active"）
  2. data-lang 锚点 href（每页指向自己的对应语言版本）
  3. Cloudflare email-protection 哈希（每页盐不同，解码结果相同）

用法:
  python3 website/_chrome/chrome_audit.py            # 全站审计，exit 0=绿 1=有 drift
  python3 website/_chrome/chrome_audit.py blog/     # 只审计子路径
KNOWN 白名单：结构性特殊页（wechat 预览、training/opc）+ 已报备观察项
（zh-cn.html / zh-tw.html hub 未本地化）——打印为 KNOWN，不影响 exit code。
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEMPLATES = {"en": "fde.html", "zh-cn": "zh-cn/fde.html", "zh-tw": "zh-tw/fde.html"}
EXCLUDE_DIRS = ("_batch_pipeline", "node_modules", ".git", "beehive-homepage-draft",
                "beehive-homepage", "seo-audit-report", "seo-audit-summary",
                "templates", "_chrome")
KNOWN_PREFIXES = ("wechat-preview", "wechat-draft-preview",
                  "wechat-article-draft-preview", "training/opc/")
KNOWN_PAGES = {"zh-cn.html": "hub header 未本地化（EN 链接）— 观察项",
               "zh-tw.html": "hub header 未本地化 — 观察项"}


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


def mobile_menu(s):
    i = s.find('<div class="mobile-menu" id="mobile-menu"')
    if i == -1:
        return None
    return s[i:find_div_span(s, i)]


def norm(x):
    if x is None:
        return None
    x = re.sub(r'(<a\s[^>]*?href=")[^"]*("[^>]*?data-lang="(?:en|zh-cn|zh-tw)")',
               r"\1X\2", x)
    x = x.replace('class="nav-link active"', 'class="nav-link"')
    x = re.sub(r"/cdn-cgi/l/email-protection#[0-9a-f]+", "EMAILPROT", x)
    x = re.sub(r"\s+", " ", x)
    return x.strip()


def lang_of(rel):
    if rel.startswith("zh-cn/"):
        return "zh-cn"
    if rel.startswith("zh-tw/"):
        return "zh-tw"
    return "en"


def main():
    sub = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else ""
    tmpl = {}
    for l, f in TEMPLATES.items():
        raw = read(os.path.join(ROOT, f))
        tmpl[l] = {"header": norm(blk(raw, "header")),
                   "footer": norm(blk(raw, "footer")),
                   "mobile": norm(mobile_menu(raw))}

    drift, known, missing = [], [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
        if rel_dir == ".":
            rel_dir = ""
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            rel = (rel_dir + "/" + fn).lstrip("/")
            if sub and not rel.startswith(sub):
                continue
            if any(rel.startswith(k) for k in KNOWN_PREFIXES) or rel in KNOWN_PAGES:
                known.append(rel)
                continue
            s = read(os.path.join(dirpath, fn))
            t = tmpl[lang_of(rel)]
            checks = (("header", norm(blk(s, "header"))),
                      ("footer", norm(blk(s, "footer"))),
                      ("mobile", norm(mobile_menu(s))))
            for part, got in checks:
                if got is None:
                    if part != "mobile":
                        missing.append((rel, part))
                    continue
                if got != t[part]:
                    drift.append((rel, part))

    for rel, part in missing:
        print("MISSING  %-8s %s" % (part, rel))
    for rel, part in drift:
        print("DRIFT    %-8s %s" % (part, rel))
    print("\nKNOWN (%d, 白名单): %s" % (len(known), ", ".join(sorted(known)[:8]) +
          (" ..." if len(known) > 8 else "")))
    print("\nRESULT: %d drift, %d missing, %d known → %s" % (
        len(drift), len(missing), len(known),
        "GREEN ✅" if not drift and not missing else "RED ❌"))
    sys.exit(0 if not drift and not missing else 1)


if __name__ == "__main__":
    main()
