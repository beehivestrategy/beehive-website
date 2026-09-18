#!/usr/bin/env python3
"""
fix_relative_links.py — site-wide broken relative link fixer.

Finds href/src attributes whose value is a relative path (no leading /,
no scheme) that does NOT resolve to an existing file relative to the
current page — even after appending .html (Cloudflare Pages pretty URLs).
Only GENUINELY broken links are rewritten to the site convention:
root-relative, extensionless for .html pages, extension kept for assets.
Working relative links (valid on CF pretty URLs) are left untouched.

Genuinely-missing targets (no file anywhere) are reported, not touched.

Usage:
  python3 fix_relative_links.py --dry     # report only
  python3 fix_relative_links.py --apply   # rewrite files
"""
import re, os, sys, posixpath, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {"node_modules", ".git", "_chrome", "_batch_pipeline", "_bgtest"}
ATTR_PAT = re.compile(r'''(href|src)="(?!#|/|https?:|mailto:|tel:|javascript:|data:|//)([^"]+)"''')

def exists_any(p):
    """File exists on disk, optionally with .html appended (pretty URL)."""
    return os.path.isfile(p) or os.path.isfile(p + ".html")

def candidate_fix(dirpath, raw):
    """Return (new_value, rule) or (None, None) if valid or no on-disk target."""
    path_part = raw.split("#")[0].split("?")[0]
    if not path_part or path_part.startswith("{{"):
        return None, None
    # 1) valid relative to current dir (incl. pretty-URL .html) -> leave alone
    if exists_any(posixpath.normpath(os.path.join(dirpath, path_part))):
        return None, None
    clean = path_part
    while clean.startswith("./"):
        clean = clean[2:]
    if not clean or clean.startswith("../") or clean.startswith("/"):
        return None, None
    # 2) root-relative interpretation
    if clean.endswith(".html"):
        if os.path.isfile(os.path.join(ROOT, clean)):
            base = clean[: -len(".html")]
            return ("/" if base == "index" else "/" + base), "html-page"
    else:
        if os.path.isfile(os.path.join(ROOT, clean)):
            return "/" + clean, "asset"
        if os.path.isfile(os.path.join(ROOT, clean + ".html")):
            return "/" + clean, "slug-page"
    return None, None

def main():
    apply = "--apply" in sys.argv
    fixes = collections.defaultdict(list)   # rule -> list of (file, old, new)
    missing = collections.defaultdict(list) # norm-target -> list of (file, raw)
    files_changed = set()

    for dirpath, dirs, fns in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in fns:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT)
            try:
                t = open(p, encoding="utf-8").read()
            except Exception:
                continue
            orig = t
            out = []
            last = 0
            for m in ATTR_PAT.finditer(t):
                attr, raw = m.group(1), m.group(2)
                new, rule = candidate_fix(dirpath, raw)
                if new is None:
                    path_part = raw.split("#")[0].split("?")[0]
                    if path_part and not path_part.startswith("{{"):
                        resolved = posixpath.normpath(os.path.join(dirpath, path_part))
                        if not exists_any(resolved):
                            norm = posixpath.relpath(resolved, ROOT)
                            missing[norm].append((rel, raw))
                    continue
                fixes[rule].append((rel, raw, new))
                out.append(t[last:m.start(2)])
                out.append(new)
                last = m.end(2)
            out.append(t[last:])
            t2 = "".join(out)
            if t2 != orig:
                files_changed.add(rel)
                if apply:
                    open(p, "w", encoding="utf-8").write(t2)

    mode = "APPLIED" if apply else "DRY-RUN"
    total = sum(len(v) for v in fixes.values())
    print(f"[{mode}] fixable broken links: {total} in {len(files_changed)} files")
    for rule, items in sorted(fixes.items()):
        print(f"  {rule}: {len(items)}  e.g. {items[0][0]}: {items[0][1]} -> {items[0][2]}")
    mt = sum(len(v) for v in missing.values())
    print(f"[{mode}] genuinely-missing targets: {mt} links, {len(missing)} unique paths")
    for k, v in sorted(missing.items(), key=lambda x: -len(x[1]))[:50]:
        print(f"  MISSING {k}: {len(v)}  e.g. {v[0][0]} href=\"{v[0][1]}\"")
    if apply:
        print(f"[{mode}] files rewritten: {len(files_changed)}")

if __name__ == "__main__":
    main()
