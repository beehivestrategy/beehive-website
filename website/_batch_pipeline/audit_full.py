#!/usr/bin/env python3
"""Full audit of all blog articles against the GEO/SEO standard.
Measures per-language length, FAQ section, FAQPage JSON-LD, question-style H2,
blank zh bodies, and empty recommended excerpts. Produces a per-slug gap map,
a summary, and batch files for sub-agents."""
import re, json, os, glob

BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = [
    ("blog/articles", "en", 2500),
    ("zh-cn/blog/articles", "zh-cn", 3500),
    ("zh-tw/blog/articles", "zh-tw", 3500),
]

def ext(h):
    if not h: return ""
    h = re.sub(r"<script[\s\S]*?</script>", " ", h, flags=re.I)
    h = re.sub(r"<style[\s\S]*?</style>", " ", h, flags=re.I)
    m = re.search(r'id="article-content"[\s\S]*?</article>', h, flags=re.I)
    if m: return m.group(0)
    m = re.search(r"<article\b[\s\S]*?</article>", h, flags=re.I)
    if m: return m.group(0)
    return h

def plain(a):
    t = re.sub(r"<[^>]+>", " ", a); t = re.sub(r"&[a-z]+;", " ", t)
    return t

def wc_en(t):
    return len(re.findall(r"[A-Za-z0-9]+(?:['\-][A-Za-z0-9]+)*", t))

def cjk(t):
    return len(re.findall(r"[一-鿿]", t))

def has_faq(art):
    return bool(re.search(r'class="[^"]*faq', art, flags=re.I)) or 'id="faq"' in art.lower()

def has_jsonld(h):
    return '"@type":"faqpage"' in h.lower()

def q_h2_zh(art):
    h2s = re.findall(r"<h2\b[^>]*>([\s\S]*?)</h2>", art, flags=re.I)
    txt = [re.sub(r"<[^>]+>", "", x).strip() for x in h2s]
    for t in txt:
        if not t: continue
        if t.endswith("?") or t.endswith("？"): return True
        if re.match(r"(如何|什么是|为什么|怎么|是否|怎样|哪种|什么|为何|在哪|哪里|多少)", t): return True
    return False

def read(p):
    try: return open(p, encoding="utf-8").read()
    except: return None

# Load slug master
status = json.load(open(os.path.join(BASE, "_batch_pipeline/status.json")))
slugs = list(status["slugs"].keys())
print("Master slug count:", len(slugs))

summary = {"total": len(slugs)}
per = {}
for s in slugs:
    per[s] = {}
    for sub, lang, floor in LANGS:
        h = read(os.path.join(BASE, sub, s + ".html"))
        if h is None:
            per[s][lang] = {"missing": True}; continue
        a = ext(h); t = plain(a)
        if lang == "en":
            w = wc_en(t); below = w < floor
        else:
            w = cjk(t); below = w < floor
        blank = (lang != "en") and (w < 50)
        faq = has_faq(a)
        jld = has_jsonld(h)
        qh2 = q_h2_zh(a) if lang != "en" else True
        # recommended excerpt empty?
        empty_excerpt = bool(re.search(r'class="recommended-card-excerpt"></p>', a))
        per[s][lang] = {
            "words": w, "below": below, "blank": blank,
            "faq": faq, "jsonld": jld, "qh2": qh2, "empty_excerpt": empty_excerpt,
        }

# Aggregate
agg = {l: {"below":0,"blank":0,"no_faq":0,"no_jsonld":0,"no_qh2":0,"empty_excerpt":0,"ok_len":0} for _,l,_ in LANGS}
for s in slugs:
    for _,l,_ in LANGS:
        d = per[s].get(l, {})
        if d.get("missing"): continue
        if d["below"]: agg[l]["below"] += 1
        else: agg[l]["ok_len"] += 1
        if d["blank"]: agg[l]["blank"] += 1
        if not d["faq"]: agg[l]["no_faq"] += 1
        if not d["jsonld"]: agg[l]["no_jsonld"] += 1
        if not d["qh2"]: agg[l]["no_qh2"] += 1
        if d["empty_excerpt"]: agg[l]["empty_excerpt"] += 1

print("\n=== AGGREGATE (per language) ===")
for l in ["en","zh-cn","zh-tw"]:
    a = agg[l]
    print(f"{l}: below_floor={a['below']} ok_len={a['ok_len']} blank={a['blank']} no_faq={a['no_faq']} no_jsonld={a['no_jsonld']} no_qh2={a['no_qh2']} empty_excerpt={a['empty_excerpt']}")

# Articles needing JSON-LD backfill (faq exists but no jsonld) - scriptable
jsonld_backfill = [s for s in slugs if per[s]["en"].get("faq") and not per[s]["en"].get("jsonld")]
print("\nJSON-LD backfill candidates (EN faq present, no jsonld):", len(jsonld_backfill))

# Blank zh slugs
blank_zh = [s for s in slugs if per[s]["zh-cn"].get("blank") or per[s]["zh-tw"].get("blank")]
print("Blank zh slugs:", blank_zh)

# Save gap map + summary
out = {"summary": agg, "per": per,
       "jsonld_backfill": jsonld_backfill, "blank_zh": blank_zh}
json.dump(out, open(os.path.join(BASE, "_batch_pipeline/audit.json"), "w"), ensure_ascii=False)

# Build batch files (~18 slugs each) for sub-agents: full standard
BATCH = 18
batches = [slugs[i:i+BATCH] for i in range(0, len(slugs), BATCH)]
bd = os.path.join(BASE, "_batch_pipeline/batches")
os.makedirs(bd, exist_ok=True)
for i, b in enumerate(batches, 1):
    with open(os.path.join(bd, f"batch_{i:03d}.txt"), "w") as f:
        f.write("\n".join(b))
print(f"\nWrote {len(batches)} batch files to {bd} ({BATCH} slugs each)")
print("Total slugs:", len(slugs))
