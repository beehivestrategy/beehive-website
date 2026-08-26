#!/usr/bin/env python3
"""
gen_zhtw.py — generate zh-TW article files from zh-CN via OpenCC, applying the
attribute-aware head transforms (canonical, og:url, cover path, og:locale,
lang switcher active state, lang label). Updates manifests with wordCount/
readingTime. No LLM needed.

Usage: python3 _batch_pipeline/gen_zhtw.py
Reads /tmp/ready_slugs.json (list of slugs already EN+zh-CN complete).
"""
import json, re, os, sys
import opencc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cc = opencc.OpenCC('s2t')

def transform(h):
    # lang attr
    h = re.sub(r'<html dir="ltr" lang="zh-CN">', '<html dir="ltr" lang="zh-TW">', h, count=1)
    # OpenCC body+head text (s2t)
    h = cc.convert(h)
    # canonical -> zh-tw
    h = re.sub(r'(<link href="https://www\.beehivestrategy\.com/)zh-cn/([^"]*?)" rel="canonical"',
               r'\1zh-tw/\2" rel="canonical"', h)
    # og:url -> zh-tw
    h = re.sub(r'(<meta content="https://www\.beehivestrategy\.com/)zh-cn/([^"]*?)" property="og:url"',
               r'\1zh-tw/\2" property="og:url"', h)
    # cover image path
    h = h.replace('assets/blog/covers/zh-cn/', 'assets/blog/covers/zh-tw/')
    # og:locale zh_CN -> zh_TW
    if 'og:locale' not in h:
        h = h.replace('</head>', '<meta content="zh_TW" property="og:locale"/>\n</head>', 1)
    else:
        h = re.sub(r'content="zh_CN"', 'content="zh_TW"', h)
    # lang switcher active state: remove active from zh-cn, add to zh-tw
    h = h.replace('class="active" data-lang="zh-cn"', 'data-lang="zh-cn"')
    h = re.sub(r'(data-lang="zh-tw")', r'class="active" \1', h)
    # lang label 简 -> 繁
    h = h.replace('<span id="current-lang-label">简</span>', '<span id="current-lang-label">繁</span>')
    return h

def main():
    slugs = json.load(open('/tmp/ready_slugs.json'))
    made = []
    for s in slugs:
        src = os.path.join(ROOT, 'zh-cn', 'blog', 'articles', s + '.html')
        dst = os.path.join(ROOT, 'zh-tw', 'blog', 'articles', s + '.html')
        if not os.path.exists(src):
            print(f"SKIP (no zh-cn): {s}")
            continue
        h = open(src, encoding='utf-8').read()
        out = transform(h)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'w', encoding='utf-8').write(out)
        made.append(s)
    print(f"zh-TW generated: {len(made)}")
    # update manifests wordCount/readingTime for ready slugs (EN + zh-CN + zh-TW)
    for lang, sub in [('en','blog/articles'),('zh-cn','zh-cn/blog/articles'),('zh-tw','zh-tw/blog/articles')]:
        mpath = os.path.join(ROOT, sub, 'manifest.json')
        m = json.load(open(mpath, encoding='utf-8'))
        by_slug = {a['slug']: a for a in m['articles']}
        updated = 0
        for s in slugs:
            if s not in by_slug: continue
            fpath = os.path.join(ROOT, sub, s + '.html')
            h = open(fpath, encoding='utf-8').read()
            a = h.find('<article class="article">')
            if a == -1: a = h.find('<div class="article-content">')
            e = h.rfind('</article>'); body = h[a:e] if e>a else h
            if lang == 'en':
                t = re.sub(r'<[^>]+>',' ',body); t=re.sub(r'&[a-z]+;',' ',t); t=re.sub(r'\s+',' ',t)
                wc = len(t.split())
            else:
                wc = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', body))
            by_slug[s]['wordCount'] = wc
            by_slug[s]['readingTime'] = max(1, round(wc/200)) if lang=='en' else max(1, round(wc/350))
            updated += 1
        json.dump(m, open(mpath,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
        print(f"manifest {lang}: updated {updated}")
    print("DONE")

if __name__ == "__main__":
    main()
