#!/usr/bin/env python3
"""Detect articles whose BODY content does not match their slug/title topic.

Cause: a rewrite sub-agent pasted the wrong article's content into a file,
leaving the correct <title>/<h1> but an unrelated body.

Signal: distinctive tokens from the slug should appear in the EN body.
An article about "from-sql-to-natural-language" whose body never says
"sql" or "natural language" is mismatched.

EN is authoritative for detection (zh files are translations of the EN body,
so an EN mismatch implies zh mismatch for the same slug).

Run: python3 detect_topic_mismatch.py
Writes: topic_mismatch.json
"""
import os, re, json, glob

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
EN = os.path.join(ROOT, "blog/articles")

# Generic words that carry no topical signal
STOP = set("""a an the of for to in on and or with without vs versus is are be
part guide update how what why when which who where playbook checklist framework
your you our we it its at from into by as that this these those not no
2024 2025 2026 2027 i ii iii new best top real full deep complete practical
enterprise business company companies use using used make made get getting
do does done more most less least can could should would will
""".split())


def body_text(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S | re.I)
    seg = m.group(1) if m else html
    seg = re.sub(r"<script.*?</script>", " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<style.*?</style>", " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<[^>]+>", " ", seg)
    return " ".join(seg.split()).lower()


def slug_tokens(slug):
    toks = [t for t in slug.split("-") if t and t not in STOP and not t.isdigit()]
    # keep tokens of length >= 2
    return [t for t in toks if len(t) >= 2]


def main():
    rows = []
    for p in sorted(glob.glob(os.path.join(EN, "*.html"))):
        slug = os.path.basename(p)[:-5]
        try:
            h = open(p, encoding="utf-8").read()
        except Exception:
            continue
        body = body_text(h)
        if len(body) < 200:
            continue
        toks = slug_tokens(slug)
        if not toks:
            continue
        hits = [t for t in toks if t in body]
        cov = len(hits) / len(toks)
        # distinctive = the rarest-looking tokens (longest 3)
        distinct = sorted(toks, key=len, reverse=True)[:3]
        dhits = [t for t in distinct if t in body]
        rows.append({
            "slug": slug,
            "coverage": round(cov, 3),
            "tokens": toks,
            "missing": [t for t in toks if t not in body],
            "distinct_hit": len(dhits),
            "distinct": distinct,
        })

    rows.sort(key=lambda r: (r["coverage"], r["distinct_hit"]))

    # Mismatch heuristic: low overall coverage AND none/one of the distinctive tokens present
    suspect = [r for r in rows if r["coverage"] < 0.5 and r["distinct_hit"] <= 1]
    hard = [r for r in rows if r["coverage"] < 0.34 and r["distinct_hit"] == 0]

    print(f"Scanned {len(rows)} EN articles")
    print(f"SUSPECT (coverage<0.5 and <=1 distinctive token): {len(suspect)}")
    print(f"HARD MISMATCH (coverage<0.34 and 0 distinctive tokens): {len(hard)}")
    print("\n=== worst 30 ===")
    for r in rows[:30]:
        print(f"  cov={r['coverage']:.2f} dh={r['distinct_hit']} {r['slug']}")
        print(f"      missing: {', '.join(r['missing'][:8])}")

    out = {
        "scanned": len(rows),
        "suspect": [r["slug"] for r in suspect],
        "hard": [r["slug"] for r in hard],
        "rows": rows,
    }
    with open(os.path.join(os.path.dirname(__file__), "topic_mismatch.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"\nWrote topic_mismatch.json (suspect={len(suspect)}, hard={len(hard)})")


if __name__ == "__main__":
    main()
