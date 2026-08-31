# -*- coding: utf-8 -*-
"""Phase 4: fix broken 'undefined' FAQs (rag cn/tw, ai-success cn/tw) and add
matching JSON-LD to ai-success en. Replaces faq-section + adds correct body LD."""
import re, os, html as _html, json
from opencc import OpenCC
BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
cc = OpenCC('s2t')

CHEV = '<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>'
FAQ_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
FAQ_TITLE = {"en":"Frequently Asked Questions","cn":"常见问题","tw":"常見問題"}

# proper Simplified-Chinese FAQ content
CN = {
"rag-architecture-patterns-enterprise-2025": [
 ("企业级 RAG 架构应优先考虑哪些模式？",
  "检索增强生成在企业落地的关键，不在于模型本身，而在于分块、嵌入与重排的策略。对结构化指标优先采用 SQL 检索，对非结构化文档使用混合检索，并用重排模型过滤噪声，能显著提升答案的可信度与稳定性。"),
 ("如何控制 RAG 系统中的幻觉与数据泄露？",
  "应设置检索白名单与租户隔离，确保每次生成只引用被授权的语料；同时对低置信结果显式标注来源缺失，并在合规场景加入人工确认。把可追溯的来源引用作为默认输出，是从根本上降低幻觉风险的手段。"),
 ("RAG 与语义层应当如何配合？",
  "语义层负责指标口径的统一，RAG 负责文档与知识的检索，两者结合可让模型同时理解数值与叙述。建议把语义层作为受治理的事实源，RAG 仅补充上下文，避免模型在口径上自由发挥。"),
],
"ai-success-metrics-beyond-accuracy": [
 ("企业应如何衡量人工智能投资的真实回报？",
  "仅看模型准确率会误导决策。更有价值的指标是决策周期缩短、返工率下降与业务结果改善，例如收入提升或成本节约。建议建立以业务指标为锚的投资组合视图，区分基础设施、用例与试验三类投入，并按三年回报评估。"),
 ("人工智能规模化落地的最大障碍是什么？",
  "试点成功到生产部署的最后一公里缺口是主要障碍。许多试点因运营流程不足、测试覆盖不够、开发与运维脱节而无法复现效果。解决之道是从项目制转向产品制，为模型设立持续监控与迭代机制。"),
 ("企业应如何构建有效的人工智能人才策略？",
  "有效策略是定向引进关键专才与大规模在岗培养并重。建立人工智能卓越中心、清晰职业路径，并提供具备竞争力的薪酬与跨职能协作环境，才能让数据科学、工程与业务真正形成合力。"),
],
}

def build_faq(items, lang, json_ld=None):
    title = FAQ_TITLE[lang]
    inner=""
    for i,(q,a) in enumerate(items,1):
        qe=_html.escape(q, quote=True); ae=_html.escape(a, quote=True)
        inner += (f'                    <div class="faq-item">\n'
                  f'                        <button class="faq-question" aria-expanded="false">\n'
                  f'                            <span class="faq-question-text"><span class="faq-number">{i}</span><span>{qe}</span></span>\n'
                  f'                            {CHEV}\n'
                  f'                        </button>\n'
                  f'                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{ae}</div></div>\n'
                  f'                    </div>\n')
    sec = (f'            <section class="faq-section" id="faq" aria-label="Frequently Asked Questions">\n'
           f'                <h2 class="faq-section-title">\n                    {FAQ_SVG}\n                    {title}\n                </h2>\n'
           f'                <div class="faq-list">\n{inner}                </div>\n'
           f'            </section>\n')
    if json_ld:
        return sec + json_ld + "\n"
    return sec

def build_json_ld(items):
    out = '<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [\n'
    for i,(q,a) in enumerate(items,1):
        out += ('    {\n      "@type": "Question",\n      "name": '+json.dumps(q)+
                ',\n      "acceptedAnswer": {\n        "@type": "Answer",\n        "text": '+
                json.dumps(a)+'\n      }\n    }' + (',' if i<len(items) else '') + '\n')
    out += '  ]\n}\n</script>'
    return out

def extract_onpage(html):
    out=[]
    for chunk in re.findall(r'<div class="faq-item">(.*?)(?=<div class="faq-item">|</div>\s*</section>)', html, re.S):
        qm=re.search(r'<span class="faq-number">.*?</span>\s*<span>(.*?)</span>', chunk, re.S)
        am=re.search(r'<div class="faq-answer-inner">(.*?)</div>', chunk, re.S)
        if qm and am:
            out.append((_html.unescape(re.sub(r'^\d+\s*','',qm.group(1))).strip(), _html.unescape(am.group(1)).strip()))
    return out

# files to fix
TARGETS = {
 "rag-architecture-patterns-enterprise-2025": ["cn","tw"],
 "ai-success-metrics-beyond-accuracy": ["cn","tw","en"],
}

for slug, langs in TARGETS.items():
    for lang in langs:
        sub = "blog/articles" if lang=="en" else f"{'zh-cn' if lang=='cn' else 'zh-tw'}/blog/articles"
        fn = os.path.join(BASE, sub, slug+".html")
        raw = open(fn, encoding="utf-8").read()
        head0 = raw[:raw.index("<body")]
        # strip any body-level FAQPage scripts
        body_region = re.sub(r'<script type="application/ld\+json">(.*?)</script>',
                             lambda m: '' if 'FAQPage' in m.group(1) else m.group(0),
                             raw[raw.index("<body"):], flags=re.S)
        html = head0 + body_region
        # items
        if lang=="en":
            items = extract_onpage(html)
        else:
            cn = CN[slug]
            if lang=="tw":
                items = [(cc.convert(h2), ''.join(cc.convert(p) for p in ps)) for h2,ps in cn]
            else:
                items = [(h2, ''.join(ps)) for h2,ps in cn]
        json_ld = build_json_ld(items)
        faq_html = build_faq(items, lang, json_ld)
        # replace existing faq-section (or insert if missing - none missing here)
        if '<section class="faq-section"' in html:
            html = re.sub(r'<section class="faq-section"[^>]*>.*?</section>', lambda m: faq_html, html, count=1, flags=re.S)
        else:
            idx = html.index('<nav class="article-nav"')
            html = html[:idx] + faq_html + "\n" + html[idx:]
        assert html[:html.index("<body")] == head0, "HEAD CHANGED "+slug+" "+lang
        assert "?v=20260826" in html
        open(fn,"w",encoding="utf-8").write(html)
        print(f"FIXED {slug} [{lang}] faq items={len(items)}")
print("DONE phase4")
