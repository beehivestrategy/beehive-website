#!/usr/bin/env python3
"""
build_chrome.py — Beehive 站点 chrome 的「真·include 引擎」（自包含，无外部依赖）

单一事实源 = website/_chrome/_partials/{en,zh-cn,zh-tw}/{header,footer,mobile}.html
（由 extract_partials.py 从三语 fde 模板抽取，已是首页同设计 + zh 已对齐首页）。

每页 chrome 在构建时由其 partial + 每页派生数据重新生成：
  - 语言：路径前缀 (en / zh-cn / zh-tw)
  - 三语锚点 URL：derive_urls(rel) 从路径推导
  - active nav：沿用该页当前 active（old_active_href）—— active 是每页固有属性，
    不是 chrome 编辑项，故从页面自身继承而非写死在 partial

>>> 这才是 "include"：改 chrome = 改 1 个 partial 文件 + 跑本脚本，
    全站 3,200+ 页一次性更新。不再手改单页，不再页页补丁。

幂等性：partials == 当前 chrome 时，本脚本重建 0 页（git diff website/ 应为 0）。
传播性已验证：改 1 个 partial -> ~1085 en 页同步；还原 partial -> 0 残留。

用法:
  python3 website/_chrome/build_chrome.py            # 构建全站（仅写有变化页）
  python3 website/_chrome/build_chrome.py --dry      # 只报告，不写
门禁: 构建后必须 `python3 website/_chrome/chrome_audit.py` → GREEN 才可部署。

部署流程（不变）:
  改 _chrome/_partials/*  →  python3 website/_chrome/build_chrome.py  →
  python3 website/_chrome/chrome_audit.py (GREEN)  →  wrangler pages deploy website
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # website/
PARTIAL_DIR = os.path.join(HERE, "_partials")
EXCLUDE_DIRS = ("_batch_pipeline", "node_modules", ".git", "beehive-homepage-draft",
                "beehive-homepage", "seo-audit-report", "seo-audit-summary",
                "templates", "_chrome")
KNOWN_PREFIXES = ("wechat-preview", "wechat-draft-preview",
                  "wechat-article-draft-preview", "training/opc/")
KNOWN_PAGES = {"zh-cn.html", "zh-tw.html"}


# ---------- helpers (self-contained; no import from gitignored dirs) ----------
def find_div_span(raw, start):
    depth = 0
    for m in re.finditer(r"<div\b|</div>", raw[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return start + m.end()
    raise ValueError("unbalanced div at %d" % start)


def blk(s, tag):
    m = re.search(r"<%s[\s\S]*?</%s>" % (tag, tag), s)
    return m.group(0) if m else None


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


def self_url(rel):
    base = rel[:-len(".html")]
    if base == "index":
        return "/"
    if base.endswith("/index"):
        return "/" + base[:-len("/index")] + "/"
    return "/" + base


def derive_urls(rel):
    s = self_url(rel)
    if s.startswith("/zh-cn"):
        en = s[len("/zh-cn"):] or "/"
        return {"en": en, "zh-cn": s, "zh-tw": "/zh-tw" + (en if en != "/" else "/")}
    if s.startswith("/zh-tw"):
        en = s[len("/zh-tw"):] or "/"
        return {"en": en, "zh-cn": "/zh-cn" + (en if en != "/" else "/"), "zh-tw": s}
    tail = s if s != "/" else "/"
    return {"en": s, "zh-cn": "/zh-cn" + tail, "zh-tw": "/zh-tw" + tail}


def extract_lang_urls(old_header, relpath, lang):
    cand = None
    anchors = re.findall(r'<a\s[^>]*?href="([^"]+)"[^>]*?data-lang="(en|zh-cn|zh-tw)"', old_header)
    if len(anchors) >= 3:
        d = {l: u for u, l in anchors[:3]}
        if len(d) == 3:
            cand = d
    if cand is None:
        m = re.search(r'<div class="lang-dropdown">(.*?)</div>', old_header, re.S)
        if m:
            hrefs = re.findall(r'<a href="([^"]+)"', m.group(1))
            if len(hrefs) == 3:
                cand = {"en": hrefs[0], "zh-cn": hrefs[1], "zh-tw": hrefs[2]}
    self_u = self_url(relpath)
    if cand and cand.get(lang) == self_u and len(set(cand.values())) == 3:
        return cand
    return derive_urls(relpath)


def old_active_href(old_header):
    m = re.search(r'<a href="([^"]+)" class="nav-link[^"]*?active', old_header)
    return m.group(1) if m else None


def apply_active(header, href, lang="en"):
    if not href:
        return header, None

    def try_mark(u):
        pat = '<a href="%s" class="nav-link"' % u
        if pat in header:
            return header.replace(pat, '<a href="%s" class="nav-link active"' % u, 1)
        return None

    variants = [href]
    m = re.match(r"^/(zh-cn|zh-tw)(/.*)$", href)
    if m:
        tail = m.group(2)
        variants += [tail, "/zh-cn" + tail, "/zh-tw" + tail]
    elif href.startswith("/"):
        variants += ["/zh-cn" + href, "/zh-tw" + href]
    if lang == "zh-cn":
        variants.sort(key=lambda u: not u.startswith("/zh-cn"))
    elif lang == "zh-tw":
        variants.sort(key=lambda u: not u.startswith("/zh-tw"))
    for u in variants:
        out = try_mark(u)
        if out is not None:
            return out, None
    return header, "WARN-active-not-found:" + href


def rewrite_lang_urls(html, urls):
    def repl(m):
        return m.group(1) + urls[m.group(3)] + m.group(2)
    return re.sub(r'(<a\s[^>]*?href=")[^"]*("[^>]*?data-lang="(en|zh-cn|zh-tw)")', repl, html)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def load_partials(lang):
    d = os.path.join(PARTIAL_DIR, lang)
    return (read(os.path.join(d, "header.html")),
            read(os.path.join(d, "mobile.html")),
            read(os.path.join(d, "footer.html")))


def main():
    dry = "--dry" in sys.argv
    partials = {l: load_partials(l) for l in ("en", "zh-cn", "zh-tw")}

    targets = []
    for dp, dn, fn in os.walk(ROOT):
        rel_dir = os.path.relpath(dp, ROOT).replace(os.sep, "/")
        if rel_dir == ".":
            rel_dir = ""
        dn[:] = [d for d in dn if d not in EXCLUDE_DIRS]
        for f in fn:
            if not f.endswith(".html"):
                continue
            rel = (rel_dir + "/" + f).lstrip("/")
            if any(rel.startswith(k) for k in KNOWN_PREFIXES) or rel in KNOWN_PAGES:
                continue
            targets.append(rel)

    fixed = 0
    for rel in sorted(targets):
        path = os.path.join(ROOT, rel)
        raw = read(path)
        lang = lang_of(rel)
        old_header = blk(raw, "header")
        if not old_header:
            continue
        tpl_header, tpl_mobile, tpl_footer = partials[lang]

        urls = extract_lang_urls(old_header, rel, lang)
        active = old_active_href(old_header)

        new_header = rewrite_lang_urls(tpl_header, urls)
        new_header, warn = apply_active(new_header, active, lang)
        new_mobile = rewrite_lang_urls(tpl_mobile, urls)
        new_footer = tpl_footer

        out = raw
        changed = False
        m = re.search(r"<header[\s\S]*?</header>", out)
        if m and norm(m.group(0)) != norm(tpl_header):
            out = out[:m.start()] + new_header + out[m.end():]
            changed = True
        i = out.find('<div class="mobile-menu"')
        if i != -1:
            cur = out[i:find_div_span(out, i)]
            if norm(cur) != norm(tpl_mobile):
                out = out[:i] + new_mobile + out[find_div_span(out, i):]
                changed = True
        m = re.search(r"<footer[\s\S]*?</footer>", out)
        if m and norm(m.group(0)) != norm(tpl_footer):
            out = out[:m.start()] + new_footer + out[m.end():]
            changed = True

        if changed:
            fixed += 1
            print("BUILD %-8s %s%s" % (lang, rel, (" " + warn if warn else "")))
            if not dry:
                open(path, "w", encoding="utf-8").write(out)

    print("\n%s: %d pages rebuilt" % ("DRY-RUN" if dry else "DONE", fixed))


if __name__ == "__main__":
    main()
