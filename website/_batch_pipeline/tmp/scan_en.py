import re, sys, os, html

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
CJK = re.compile(r'[\u4e00-\u9fff]')

def clean(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()

# find elements (with class) whose text content is pure english
PAT = re.compile(r'<(h[1-6]|a|span|div|p|li|button|strong|em)\b([^>]*)>((?:(?!</?\1\b).)*?)</\1>', re.S)
SKIP_CLASS = ('lang-code', 'lang-switcher')

def scan(rel):
    src = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    res = []
    for m in PAT.finditer(src):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if any(s in attrs for s in SKIP_CLASS):
            continue
        txt = clean(inner)
        if not txt or CJK.search(txt):
            continue
        if len(txt) < 3:
            continue
        if not re.search(r'[A-Za-z]{3}', txt):
            continue
        cls = re.search(r'class="([^"]*)"', attrs)
        res.append((tag, cls.group(1) if cls else '', txt))
    return res

if __name__ == '__main__':
    files = [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/wo_faq_3.txt')) if l.strip()]
    for f in files[int(sys.argv[1]):int(sys.argv[2])]:
        print('=' * 60)
        print(f)
        seen = set()
        for tag, cls, txt in scan(f):
            k = (tag, cls, txt)
            if k in seen:
                continue
            seen.add(k)
            print('  <%s class="%s"> %s' % (tag, cls, txt))
