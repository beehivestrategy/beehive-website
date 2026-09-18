# -*- coding: utf-8 -*-
"""Shared helpers for per-slug processing scripts."""
import re, io, json

FAQ_RX = r'<div class="faq-list">.*?</div>\s*</section>'
# tempered: never crosses a </script> boundary
JSONLD_RX = r'<script type="application/ld\+json">(?:(?!</script>).)*?"@type":\s*"FAQPage"(?:(?!</script>).)*?</script>'
SVG_CHEV = '<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>'

def load(p):
    with io.open(p, encoding="utf-8") as f: return f.read()

def save(p, s):
    with io.open(p, "w", encoding="utf-8") as f: f.write(s)

def rep1(s, old, new, label):
    n = s.count(old)
    assert n == 1, f"[{label}] expected 1 occurrence, got {n}"
    return s.replace(old, new)

def re_dl(s, pattern, repl, label, expected=1, flags=re.S):
    rx = re.compile(pattern, flags)
    matches = rx.findall(s)
    assert len(matches) == expected, f"[{label}] expected {expected} matches, got {len(matches)}"
    return rx.sub(repl, s)

def build_faq_list(faq):
    items = []
    for i, (q, a) in enumerate(faq, 1):
        items.append(f'''                    <div class="faq-item">
                        <h3 style="margin:0;">
                            <button class="faq-question" aria-expanded="false">
                                <span class="faq-question-text"><span class="faq-number">{i}</span><span>{q}</span></span>
                                {SVG_CHEV}
                            </button>
                        </h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{a}</div></div>
                    </div>''')
    return "\n".join(items)

def build_jsonld(faq):
    ents = []
    for q, a in faq:
        ents.append('    {\n      "@type": "Question",\n      "name": %s,\n      "acceptedAnswer": {\n        "@type": "Answer",\n        "text": %s\n      }\n    }'
                    % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False)))
    return '<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [\n' + ",\n".join(ents) + '\n  ]\n}\n</script>'

def body_h1(s):
    m = re.search(r'<h1 class="article-h1">(.*?)</h1>', s, re.S)
    assert m, "no h1 found"
    return m.group(1)

def fill_excerpts(s, excerpts, label="excerpt"):
    for ex in excerpts:
        assert '<p class="recommended-card-excerpt"></p>' in s, f"[{label}] no empty excerpt left but one expected"
        s = s.replace('<p class="recommended-card-excerpt"></p>',
                      f'<p class="recommended-card-excerpt">{ex}</p>', 1)
    return s

def integrity(s, must_contain, min_h2, label):
    for needle in must_contain:
        assert needle in s, f"[{label}] integrity: missing {needle[:60]!r}"
    assert s.count("<h2 ") >= min_h2, f"[{label}] integrity: h2 count {s.count('<h2 ')} < {min_h2}"
