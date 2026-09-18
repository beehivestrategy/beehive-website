# -*- coding: utf-8 -*-
"""Second pass: mobile TOC links, toggle/view-all text nodes, breadcrumb."""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch

P_MOBILE = re.compile(r'(<a\b[^>]*class="[^"]*toc-mobile-link[^"]*"[^>]*>)((?:(?!</a>).)*?)(</a>)', re.S)
P_TOGGLE = re.compile(r'(<button class="toc-mobile-toggle"[^>]*>)([^<]*?)(\s*<svg)', re.S)
P_VIEWALL = re.compile(r'(<a\b[^>]*class="[^"]*recommended-view-all[^"]*"[^>]*>)([^<]*?)(\s*<svg)', re.S)
P_CRUMB = re.compile(r'(<a href="https://www\.beehivestrategy\.com/(?:blog)?">)([^<]*)(</a>)')

def apply(src, pattern, mapping, counter, label, group=2):
    def rep(m):
        t = re.sub(r'\s+', ' ', m.group(group)).strip()
        if t in mapping:
            counter[label] += 1
            return m.group(1) + mapping[t] + m.group(3)
        return m.group(0)
    return pattern.sub(rep, src)

def process(rel, dry=False):
    p = os.path.join(patch.ROOT, rel)
    src = open(p, encoding='utf-8').read()
    d0 = len(re.findall(r'<div\b', src)) - len(re.findall(r'</div>', src))
    counter = {'mobile': 0, 'ui': 0}

    tw = rel.startswith('zh-tw')
    common = patch.COMMON_TW if tw else patch.COMMON_CN
    cfg = patch.TW_FILES.get(rel) if tw else patch.CN.get(rel)
    hmap = dict(common)
    hmap.update(cfg['h'] if cfg else {})
    tocmap = dict(hmap)
    tocmap.update(cfg['toc'] if cfg else {})

    src = apply(src, P_MOBILE, tocmap, counter, 'mobile')
    extra = {'Table of Contents': ('目录' if not tw else '目錄'),
             'View all': ('查看全部' if not tw else '查看全部')}
    src = apply(src, P_TOGGLE, extra, counter, 'ui')
    src = apply(src, P_VIEWALL, extra, counter, 'ui')

    if rel.endswith('omnichannel-retail-analytics-unifying-online-and-offline-data.html'):
        src = apply(src, P_CRUMB, {'Home': '首页', 'Blog': '博客'}, counter, 'ui')

    d1 = len(re.findall(r'<div\b', src)) - len(re.findall(r'</div>', src))
    if d0 != d1:
        print('!! DIV DELTA CHANGED', rel)
        return None
    if not dry:
        open(p, 'w', encoding='utf-8').write(src)
    return counter

if __name__ == '__main__':
    files = [l.strip() for l in open(os.path.join(patch.ROOT, '_batch_pipeline/wo_faq_3.txt')) if l.strip()]
    dry = '--dry' in sys.argv
    tot = {'mobile': 0, 'ui': 0}
    for f in files:
        c = process(f, dry)
        if c is None:
            continue
        tot['mobile'] += c['mobile']; tot['ui'] += c['ui']
        if c['mobile'] or c['ui']:
            print('%-70s mobile=%d ui=%d' % (os.path.basename(f), c['mobile'], c['ui']))
    print('TOTAL', tot, 'DRY' if dry else 'WRITTEN')
