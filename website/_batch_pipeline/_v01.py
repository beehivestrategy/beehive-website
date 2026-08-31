import re, sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from _lib01 import ROOT, path, load, body, strip_tags, en_words, cjk, h2s

CTA_PHRASE = {"EN": "Book a Demo", "CN": "预约演示", "TW": "預約示範"}
QUESTION_EN = re.compile(r'^(How|What|Why|When|Which|Where|Who|Can|Do|Does|Is|Are|Should|Will|Did)\b')
QUESTION_ZH = re.compile(r'[？?]\s*$')


def faq_block(h):
    m = re.search(r'class="faq-section".*?</section>', body(h), re.S)
    return m.group(0) if m else ""


def check(slug, lang):
    p = path(slug, lang)
    h = open(p, encoding="utf-8").read()
    r = {}
    r["w"] = en_words(h)
    r["cjk"] = cjk(h)
    fb = faq_block(h)
    r["faq_h3"] = len(re.findall(r'<h3 class="faq-question-title"', fb))
    r["faq_items"] = len(re.findall(r'class="faq-item"', fb))
    r["ld_faq"] = len(re.findall(r'"@type"\s*:\s*"FAQPage"', h))
    r["cta_ok"] = 1 if re.search(r'class="article-cta-btn"[^>]*>\s*%s' % CTA_PHRASE[lang], h) else 0
    recs = re.findall(r'<a href="([^"]*)"[^>]*class="recommended-card"', h)
    r["rec"] = len(recs)
    r["rec_bad"] = [x for x in recs if not x.startswith("/blog/articles/")
                    and not x.startswith("/zh-cn/blog/articles/")
                    and not x.startswith("/zh-tw/blog/articles/")]
    hs = h2s(h)
    r["h2"] = len(hs)
    if lang == "EN":
        r["h2_nonq"] = [t for i, t in hs if not t.rstrip().endswith("?")]
    else:
        r["h2_nonq"] = [t for i, t in hs if not QUESTION_ZH.search(t)]
    # guardrails
    r["cssver"] = 1 if '/css/article.css?v=20260826' in h else 0
    r["jsver"] = 1 if '/js/article.js?v=20260826' in h else 0
    r["footer"] = 1 if '<footer' in h else 0
    r["share"] = h.count('article-share-btn')
    r["h1"] = (re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S) or [None, ""])[1]
    r["h1"] = strip_tags(r["h1"]).strip() if isinstance(r["h1"], str) else ""
    r["title"] = (re.search(r'<title>(.*?)</title>', h, re.S) or [None, ""])[1]
    r["title"] = strip_tags(r["title"]).strip()
    r["tables"] = body(h).count("<table")
    return r


if __name__ == "__main__":
    slugs = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    ok_all = True
    for slug in slugs:
        row = {"slug": slug}
        for lang in ("EN", "CN", "TW"):
            row[lang] = check(slug, lang)
        # verdict
        probs = []
        e = row["EN"]
        if e["w"] < 2500: probs.append("EN words %d" % e["w"])
        for lang in ("CN", "TW"):
            v = row[lang]
            if v["cjk"] < 3500: probs.append("%s cjk %d" % (lang, v["cjk"]))
        for lang in ("EN", "CN", "TW"):
            v = row[lang]
            if v["faq_h3"] < 3: probs.append("%s faq %d" % (lang, v["faq_h3"]))
            if v["ld_faq"] != 1: probs.append("%s ld %d" % (lang, v["ld_faq"]))
            if not v["cta_ok"]: probs.append("%s cta" % lang)
            if v["rec_bad"]: probs.append("%s recbad" % lang)
            if v["h2_nonq"]: probs.append("%s h2nonq %s" % (lang, v["h2_nonq"][:2]))
            if not v["cssver"] or not v["jsver"]: probs.append("%s version" % lang)
            if not v["footer"]: probs.append("%s footer" % lang)
            if not v["share"]: probs.append("%s share" % lang)
        print(("FAIL " if probs else "PASS ") + slug, "|", "; ".join(probs))
        if probs: ok_all = False
        print("    EN w=%d faq=%d ld=%d h2=%d tbl=%d | CN cjk=%d faq=%d h2=%d | TW cjk=%d faq=%d h2=%d" % (
            e["w"], e["faq_h3"], e["ld_faq"], e["h2"], e["tables"],
            row["CN"]["cjk"], row["CN"]["faq_h3"], row["CN"]["h2"],
            row["TW"]["cjk"], row["TW"]["faq_h3"], row["TW"]["h2"]))
    print("ALL OK" if ok_all else "SOME FAILURES")
