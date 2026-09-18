import re, sys, os, html

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()

def dump(rel, per=420):
    src = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    # cut article body
    body = src
    print('=' * 70)
    print('FILE:', rel)
    m = re.search(r'<h1[^>]*>(.*?)</h1>', src, re.S)
    print('H1:', strip_tags(m.group(1)))
    m = re.search(r'<p class="article-lead"[^>]*>(.*?)</p>', src, re.S)
    print('LEAD:', (strip_tags(m.group(1))[:600]) if m else None)
    # split by h2/h3
    for m in re.finditer(r'<(h[23])[^>]*>(.*?)</\1>', src, re.S):
        tag = m.group(1)
        title = strip_tags(m.group(2))
        if title in ('常見問題', '推薦文章') or '準備好改變' in title:
            continue
        nxt = src[m.end():]
        paras = re.findall(r'<p[^>]*>(.*?)</p>', nxt[:6000], re.S)
        txt = ' '.join(strip_tags(p) for p in paras[:3])[:per]
        lis = re.findall(r'<li[^>]*>(.*?)</li>', nxt[:4000], re.S)
        print('  [%s] %s' % (tag, title))
        print('      ', txt)
        for li in lis[:4]:
            print('       -', strip_tags(li)[:160])

if __name__ == '__main__':
    files = [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/wo_faq_3.txt')) if l.strip()]
    for f in files[int(sys.argv[1]):int(sys.argv[2])]:
        dump(f)
