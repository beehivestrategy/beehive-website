#!/usr/bin/env python3
"""
gen_zhtw_one.py — generate the zh-TW article for ONE slug from its zh-CN file
via OpenCC, applying the attribute-aware head transforms. Updates the zh-TW
manifest wordCount/readingTime. No LLM needed.

Usage: python3 gen_zhtw_one.py <slug>
"""
import re, os, sys, json
import opencc

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
cc = opencc.OpenCC('s2t')

def transform(h):
    h = re.sub(r'<html dir="ltr" lang="zh-CN">', '<html dir="ltr" lang="zh-TW">', h, count=1)
    h = cc.convert(h)
    h = re.sub(r'(<link href="https://www\.beehivestrategy\.com/)zh-cn/([^"]*?)" rel="canonical"',
               r'\1zh-tw/\2" rel="canonical"', h)
    h = re.sub(r'(<meta content="https://www\.beehivestrategy\.com/)zh-cn/([^"]*?)" property="og:url"',
               r'\1zh-tw/\2" property="og:url"', h)
    h = h.replace('assets/blog/covers/zh-cn/', 'assets/blog/covers/zh-tw/')
    if 'og:locale' not in h:
        h = h.replace('</head>', '<meta content="zh_TW" property="og:locale"/>\n</head>', 1)
    else:
        h = re.sub(r'content="zh_CN"', 'content="zh_TW"', h)
    h = h.replace('class="active" data-lang="zh-cn"', 'data-lang="zh-cn"')
    h = re.sub(r'(data-lang="zh-tw")', r'class="active" \1', h)
    h = h.replace('<span id="current-lang-label">简</span>', '<span id="current-lang-label">繁</span>')
    return h

def main():
    slug = sys.argv[1]
    src = os.path.join(ROOT, 'zh-cn', 'blog', 'articles', slug + '.html')
    dst = os.path.join(ROOT, 'zh-tw', 'blog', 'articles', slug + '.html')
    if not os.path.exists(src):
        print(f"SKIP (no zh-cn): {slug}")
        sys.exit(1)
    h = open(src, encoding='utf-8').read()
    out = transform(h)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(out)
    # update zh-tw manifest
    mpath = os.path.join(ROOT, 'zh-tw', 'blog', 'articles', 'manifest.json')
    m = json.load(open(mpath, encoding='utf-8'))
    by_slug = {a['slug']: a for a in m['articles']}
    if slug in by_slug:
        a = out.find('<article class="article">')
        if a == -1:
            a = out.find('<div class="article-content">')
        e = out.rfind('</article>')
        body = out[a:e] if e > a else 0
        cjk = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', body)) if e > 0 else 0
        by_slug[slug]['wordCount'] = cjk
        by_slug[slug]['readingTime'] = max(1, round(cjk/350))
        json.dump(m, open(mpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"zh-TW generated: {slug} (CJK {by_slug[slug]['wordCount'] if slug in by_slug else 'n/a'})")

if __name__ == "__main__":
    main()
