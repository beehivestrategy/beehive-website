#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F
import g3_s07 as S  # reuse EN_NEW / CN_BODY / FAQ / CHROME / make_zh

SLUG = S.SLUG

EN_EXTRA = """
<h2 id="what-does-conversational-analytics-cost-in-an-energy-deployment">What Does Conversational Analytics Cost in an Energy Deployment?</h2>
<p>Cost questions in this sector are usually asked too late, and the answer that matters is not the licence line. Three components make up the real number, and their proportions surprise most first-time buyers.</p>
<p><strong>Platform cost</strong> is the visible component — per-user or per-query pricing, plus any infrastructure charges if the platform runs in your own environment. It is the smallest of the three in a well-run deployment and the easiest to compare across vendors, which is why it attracts disproportionate attention in procurement.</p>
<p><strong>Integration and semantic layer work</strong> is the largest component and the one most often omitted from business cases. It covers connecting SCADA, historians, ERP and IoT sources, resolving entities, agreeing metric definitions, and standing up governance. Budgeting this honestly at the assessment stage is the single best predictor of whether the programme lands on time. Under-budgeting it is how a twelve-week roadmap becomes a nine-month project.</p>
<p><strong>Operating cost</strong> is the component that persists: semantic layer maintenance as new assets and metrics appear, model tuning as users ask questions nobody anticipated, and the governance overhead of reviewing new data sources. Most enterprises find this settles at a fraction of one full-time analyst, which is modest — but only if someone is explicitly assigned to it. Programmes that treat the semantic layer as a one-off build accumulate definitional drift until users stop trusting the answers.</p>
<p>Set against these, the return side is unusually well documented in this sector: up to 40 percent of analytical time recovered from data reconciliation, query resolution roughly 78 percent faster, and first-year ROI around 3x. The honest way to present it is a range with the assumptions stated, not a single number. Executives in this industry discount confident point estimates, and they are right to.</p>
"""

CN_EXTRA = """
<h2 id="what-does-conversational-analytics-cost-in-an-energy-deployment">在能源行业部署对话式分析，成本构成是怎样的？</h2>
<p>在这个行业，成本问题往往问得太晚，而真正重要的答案并不在许可证那一行。真实数字由三部分构成，它们的比例会让多数首次采购者感到意外。</p>
<p><strong>平台成本</strong>是看得见的部分——按用户或按查询计费，若平台运行在自有环境中还有基础设施费用。在运行良好的部署中它是三者中最小的，也最容易在厂商之间横向比较，正因如此它在采购环节吸引了不成比例的注意力。</p>
<p><strong>集成与语义层工作</strong>是最大的一块，也是最常被商业论证遗漏的一块。它包括接入SCADA、历史库、ERP和物联网数据源，解析实体，就指标定义达成一致，以及建立治理机制。在评估阶段诚实地为它编列预算，是项目能否按时落地的唯一最佳预测指标。低估它，正是"十二周路线图"变成"九个月项目"的原因。</p>
<p><strong>运营成本</strong>则是持续存在的部分：随着新资产和新指标出现而维护语义层，随着用户提出没人预料到的问题而调优模型，以及评审新数据源所带来的治理开销。多数企业发现这部分最终稳定在不到一名全职分析师的工作量，规模不大——但前提是明确有人负责。把语义层当成一次性建设的项目，会不断累积定义漂移，直到用户不再信任答案。</p>
<p>与之相对，收益端在这个行业有着异常充分的记录：从数据核对中回收高达40%的分析时间，查询解决时间加快约78%，首年投资回报约为3倍。呈现它的诚实方式是一个附带假设条件的区间，而不是一个孤零零的数字。这个行业的管理者会对自信的点估计打折扣，而他们这样做是对的。</p>
"""

EXTRA_CHROME = [
  ("Discover how energy operators use conversational analytics to reduce reporting cycles, improve sustainability metrics, and accelerate operational decisions.",
   "了解能源运营商如何用对话式分析缩短报表周期、改进可持续指标，并加快运营决策。"),
  ("Observability-driven data quality automation that frees analysts from manual cleanup.",
   "以可观测性驱动的数据质量自动化，把分析师从手工清洗中解放出来。"),
  ("Beehive Strategy Blog", "蜂启咨询博客"),
  ("Book a personalised demo", "预约个性化演示"),
  ("AI-powered conversational intelligence that transforms how enterprises query, analyze, and act on their data.",
   "AI驱动的对话式智能，改变企业查询、分析和运用数据的方式。"),
  ("Adoption in 6 months", "6个月内采用率"),
  ("Data connectors", "数据连接器"),
  ("All rights reserved.", "保留所有权利。"),
  ("API Reference", "API 文档"),
  ("Integrations", "集成"),
  ("Changelog", "更新日志"),
  ("Partners", "合作伙伴"),
  ("Careers", "招聘"),
  ("Support", "支持"),
  ("Product", "产品"),
  ("Status", "状态"),
  ("Legal", "法律"),
]

def build_faq_ld_zh(qas):
    ent = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent},
                      ensure_ascii=False, indent=2)

def make_zh(en_html, lang, faq_qas):
    s = en_html
    pre = "zh-cn" if lang == "zh-CN" else "zh-tw"
    s = s.replace('lang="en"', 'lang="%s"' % pre)
    s = s.replace('content="en_US"', 'content="%s"' % ("zh_CN" if lang == "zh-CN" else "zh_TW"))
    s = s.replace('https://www.beehivestrategy.com/blog', 'https://www.beehivestrategy.com/%s/blog' % pre)
    s = s.replace('href="/blog', 'href="/%s/blog' % pre)
    for p in ('solution', 'contact', 'about', 'services', 'industries', 'case-studies', 'pricing'):
        s = s.replace('href="/%s"' % p, 'href="/%s/%s"' % (pre, p))
    s = s.replace('href="/"', 'href="/%s/"' % pre)
    s = S.READ_RE.sub(lambda m: "%s 分钟阅读" % m.group(1), s)
    # article body
    b = F.get_body(s)
    newb = re.sub(r'</div>\s*<html><body>.*?</body></html>', lambda m: '</div>' + S.CN_BODY + CN_EXTRA, b, flags=re.S)
    assert newb != b
    s = F.set_body(s, newb)
    # translate the head FAQPage JSON-LD block
    s = re.sub(r'(<script type="application/ld\+json">\s*\{.*?"@type":\s*"FAQPage".*?)\s*</script>',
               lambda m: '<script type="application/ld+json">\n' + build_faq_ld_zh(faq_qas) + '\n</script>',
               s, count=1, flags=re.S)
    chrome = sorted(S.CHROME + EXTRA_CHROME, key=lambda x: -len(x[0]))
    for a, bb in chrome:
        s = s.replace(a, bb)
    s = s.replace('Beehive Strategy <span aria-hidden="true" class="article-meta-dot">',
                  '蜂启咨询 <span aria-hidden="true" class="article-meta-dot">')
    return s

def main():
    # EN top-up
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    if 'what-does-conversational-analytics-cost-in-an-energy-deployment' not in b:
        anchor = '<h2 id="measuring-roi">'
        b = b.replace(anchor, EN_EXTRA.strip() + "\n" + anchor, 1)
        F.save(SLUG, "EN", F.set_body(s, b))

    faq = dict(S.FAQ)
    faq["zh-TW"] = [(F.S2TWP.convert(q), F.S2TWP.convert(a)) for q, a in S.FAQ["zh-CN"]]

    en = F.load(SLUG, "EN")
    cn = make_zh(en, "zh-CN", faq["zh-CN"])
    with open(F.path(SLUG, "zh-CN"), "w", encoding="utf-8") as f:
        f.write(cn)
    tw = F.s2twp_text(cn)
    tw = tw.replace('lang="zh-cn"', 'lang="zh-tw"').replace('content="zh_CN"', 'content="zh_TW"')
    tw = re.sub(r'(https://www\.beehivestrategy\.com/)zh-cn/', r'\1zh-tw/', tw)
    tw = re.sub(r'(href=")/zh-cn/', r'\1/zh-tw/', tw)
    tw = re.sub(r'(src=")/zh-cn/', r'\1/zh-tw/', tw)
    tw = tw.replace('/assets/blog/covers/zh-cn/', '/assets/blog/covers/zh-tw/')
    with open(F.path(SLUG, "zh-TW"), "w", encoding="utf-8") as f:
        f.write(tw)

    before, after = F.process(SLUG, faq=faq,
                              faq_titles={"EN": "Frequently Asked Questions",
                                          "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, before[lang], "->", after[lang])

main()
