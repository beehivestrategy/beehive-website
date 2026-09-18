#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task #805 executor: apply title fixes from title_fixes_proposal.json.
DO NOT RUN without Kenneth's explicit approval (title rewrite = LOCKED class).

What it does:
  1. Backs up affected files to _batch_pipeline/title_fix_backups/<ts>/
  2. For each proposal entry:
     - zh-cn/blog/articles/<slug>.html : <title>, og:title, twitter:title, JSON-LD headline
     - zh-tw/blog/articles/<slug>.html : same (only where changed_tw)
  3. Updates zh-cn + zh-tw manifest.json title fields (preserves "| Beehive" suffix style).
Run:  python3 apply_title_fixes.py            # dry-run: show what would change
      python3 apply_title_fixes.py --apply   # real write
"""
import json, os, re, shutil, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(BASE)
PROP = os.path.join(BASE, "title_fixes_proposal.json")

def load():
    with open(PROP, encoding="utf-8") as f:
        return json.load(f)

def sub_title_tag(html, new, old_hint):
    def repl(m):
        old = m.group(1)
        suffix = " | Beehive Strategy" if old.rstrip().endswith(" | Beehive Strategy") else ""
        return "<title>%s%s</title>" % (esc(new), suffix)
    return re.sub(r"<title>((?:[^<]|<[^/])*?)</title>", repl, html, count=1)

def sub_meta(html, new, kind):
    pat = re.compile(r'(<meta\s+(?:property|name)="%s"\s+content=")((?:[^"\\]|\\.)*)(")' % re.escape(kind))
    def repl(m):
        old = m.group(2)
        suffix = " | Beehive" if old.rstrip().endswith(" | Beehive") else ""
        return m.group(1) + esc(new) + suffix + m.group(3)
    return pat.sub(repl, html, count=1)

def sub_headline(html, new):
    pat = re.compile(r'("headline"\s*:\s*")((?:[^"\\]|\\.)*)(")')
    def repl(m):
        return m.group(1) + esc(new) + m.group(3)
    return pat.sub(repl, html, count=1)

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

def patch_article(path, new_title):
    if not os.path.exists(path):
        return "MISSING-FILE"
    with open(path, encoding="utf-8") as f:
        html = f.read()
    orig = html
    html = sub_title_tag(html, new_title, None)
    html = sub_meta(html, new_title, "og:title")
    html = sub_meta(html, new_title, "twitter:title")
    html = sub_headline(html, new_title)
    if html == orig:
        return "NO-CHANGE"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return "OK"

def patch_manifests(entries):
    changed = []
    for lang, key in (("zh-cn", "new_cn"), ("zh-tw", "new_tw")):
        mp = os.path.join(SITE, lang, "blog", "articles", "manifest.json")
        with open(mp, encoding="utf-8") as f:
            m = json.load(f)
        idx = {a["slug"]: a for a in m["articles"]}
        n = 0
        for e in entries:
            if not e["changed_" + ("cn" if lang == "zh-cn" else "tw")]:
                continue
            a = idx.get(e["slug"])
            if not a:
                continue
            old_t = a["title"]
            suffix = " | Beehive" if old_t.rstrip().endswith(" | Beehive") else ""
            a["title"] = e[key] + suffix
            n += 1
        with open(mp, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        changed.append("%s manifest: %d titles updated" % (lang, n))
    return changed

def main():
    apply = "--apply" in sys.argv
    entries = load()
    ts = time.strftime("%Y%m%d-%H%M%S")
    bdir = os.path.join(BASE, "title_fix_backups", ts)
    results = []
    files_touched = set()
    for e in entries:
        for lang, key, flag in (("zh-cn", "new_cn", "changed_cn"), ("zh-tw", "new_tw", "changed_tw")):
            if not e[flag]:
                continue
            p = os.path.join(SITE, lang, "blog", "articles", e["slug"] + ".html")
            if apply:
                if os.path.exists(p) and p not in files_touched:
                    os.makedirs(bdir, exist_ok=True)
                    rel = os.path.relpath(p, SITE)
                    dst = os.path.join(bdir, rel.replace(os.sep, "__"))
                    shutil.copy2(p, dst)
                    files_touched.add(p)
                r = patch_article(p, e[key])
            else:
                r = "DRY:" + ("exists" if os.path.exists(p) else "MISSING-FILE")
            results.append((e["slug"], lang, r))

    ok = sum(1 for _, _, r in results if r in ("OK",))
    print("entries processed: %d | patched: %d" % (len(results), ok))
    bad = [(s, l, r) for s, l, r in results if r not in ("OK", "DRY:exists")]
    if bad:
        print("ATTENTION:")
        for s, l, r in bad[:20]:
            print("  %s [%s] -> %s" % (s, l, r))
    if apply:
        msgs = patch_manifests(entries)
        for mmsg in msgs:
            print(mmsg)
        print("backup dir: %s" % bdir)
    else:
        print("(dry-run; rerun with --apply to write)")

if __name__ == "__main__":
    main()
