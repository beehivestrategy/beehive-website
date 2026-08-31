# -*- coding: utf-8 -*-
import re, os, json, opencc
cc = opencc.OpenCC('s2twp')
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = "omnichannel-retail-analytics-unifying-online-and-offline-data"

en_extra = '''
<h2 id="how-do-you-measure-the-roi-of-omnichannel-analytics">How Do You Measure the ROI of Omnichannel Analytics?</h2>
<p>The ROI of unification shows up in three places, and a credible business case tracks all three. The first is marketing efficiency: once attribution reflects true cross-channel contribution, budget shifts away from the last click toward the channels that actually create demand, and customer acquisition cost falls. The second is conversion: real-time inventory visibility and a unified profile let staff and customers complete more journeys, lifting revenue per visit. The third is retention: cross-channel customers are worth roughly 30 percent more over their lifetime, so even a small improvement in repeat-purchase rate compounds. The mistake is to report only one of these; the programme looks under-funded or over-claimed depending on which is chosen.</p>
<p>We recommend a holdout-based measurement from the first phase: compare a test group reached by unified analytics against a control group still managed with siloed reporting, and quantify the lift in repeat purchase and basket size. Holding out a group feels wasteful, but it is the only way to prove the unification — not seasonality or a promotion — drove the result. Retailers that instrument this early report the multi-channel uplift within two quarters and use it to fund the next phase.</p>
<h2 id="what-are-the-most-common-omnichannel-analytics-failures">What Are the Most Common Omnichannel Analytics Failures?</h2>
<p>Most failures are sequencing failures, not technology failures. The first is building the full customer-360 platform before proving a single unified answer, which buries the value under a multi-year programme nobody can see. The second is treating identity resolution as a one-time batch job rather than a continuous process, so the profile drifts as new identifiers arrive. The third is neglecting privacy architecture until launch, which forces a rebuild when consent rules block the unified profile. The fourth is measuring on opinions: teams keep reconciling spreadsheets because no agreed semantic layer exists, so the "true" number is whatever the loudest stakeholder claims.</p>
<p>The antidote is the same sequence we apply elsewhere: identity first, unified metrics second, attribution third, real-time inventory fourth — each phase producing a visible result the business can act on. Retailers that follow this order ship value while competitors are still integrating; the platform arrives as a consequence of proven wins, not as a prerequisite for them.</p>
<h2 id="how-does-conversational-bi-change-omnichannel-analytics">How Does Conversational BI Change Omnichannel Analytics?</h2>
<p>Traditional omnichannel dashboards still require someone to know which report to open. Conversational BI removes that gate: a store manager can ask, in plain language, "which items are stocked near this customer's store but not in it?" and get a grounded answer from the same unified model. The semantic layer that defines customer, product, and inventory once becomes the single source of truth every channel queries, so the question "how did the omni campaign lift repeat purchases?" is answered consistently whether asked by a category lead in a meeting or a regional manager in a chat window.</p>
<p>This is where unification pays a second dividend. Because the model is defined once and governed, the natural-language answers inherit the same identity resolution, attribution logic, and access controls as the dashboards — no parallel spreadsheet of truth. Deployed as a managed service in about two weeks, conversational BI turns the unified model from a reporting asset into an operating habit across the retail organisation.</p>
'''

en_faq = [
 ("What is omnichannel retail analytics?",
  "Omnichannel retail analytics is the practice of unifying online and offline customer, product, and inventory data so a retailer can see one customer relationship across every touchpoint. It replaces siloed channel reports with a single model that supports identity resolution, cross-channel attribution, and real-time inventory visibility."),
 ("Why is identity resolution the hard part of omnichannel analytics?",
  "Customers interact through many identifiers — email, phone, loyalty, device — and not all joins are certain. Deterministic matches must come first, with probabilistic matching held to confidence thresholds, and the resolution must run continuously rather than as a one-off batch, or the unified profile drifts as new data arrives."),
 ("How does attribution change once data is unified?",
  "Algorithmic attribution on unified data typically shifts 20 to 40 percent of credit away from the last click toward the channels that actually create demand. That reshapes budget decisions and is only trustworthy when the underlying identity and consent architecture are sound."),
 ("What privacy rules apply to omnichannel customer data?",
  "Under PIPL in China and GDPR in Europe, cross-channel unification must be built with consent, purpose limitation, and data minimisation. The unified profile should respect the most restrictive consent across channels, hold only data that serves the analytics purpose, and be accessible under the same audit rules as each source system."),
]

def faq_section(items):
    out = ['<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">',
           '    <h2 class="faq-section-title">',
           '        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
           '        Frequently Asked Questions',
           '    </h2>',
           '    <div class="faq-list">']
    for i,(q,a) in enumerate(items, 1):
        out.append('        <div class="faq-item">')
        out.append('            <button class="faq-question" aria-expanded="false">')
        out.append('                <span class="faq-question-text"><span class="faq-number">%d</span><span>%d %s</span></span>' % (i, i, q))
        out.append('                <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>')
        out.append('            </button>')
        out.append('            <div class="faq-answer" role="region"><div class="faq-answer-inner">%s</div></div>' % a)
        out.append('        </div>')
    out.append('    </div>')
    out.append('</section>')
    return "\n".join(out)

def faq_jsonld(items):
    ent = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":ent}, ensure_ascii=False, indent=2)

en_faq_html = faq_section(en_faq)
en_jsonld = faq_jsonld(en_faq)

# EN inject
en_path = os.path.join(ROOT, "blog/articles/%s.html"%slug)
h = open(en_path, encoding='utf-8').read()
m = re.search(r'(<p class="article-lead">.*?)(<nav class="article-nav")', h, re.S)
new_inner = m.group(1) + en_extra + en_faq_html + "\n" + en_jsonld + "\n"
h = h[:m.start(1)] + new_inner + h[m.end(1):]
open(en_path,'w',encoding='utf-8').write(h)
print("EN written")

# Chinese extra + faq
cn_extra = '''
<h2 id="how-to-measure-omnichannel-roi">如何衡量全渠道分析的投资回报？</h2>
<p>统一的回报体现在三个地方，一个可信的商业论证会同时追踪这三者。第一是营销效率：一旦归因反映真实跨渠道贡献，预算就会从"最后一次点击"转向真正创造需求的渠道，获客成本随之下降。第二是转化：实时库存可见与统一客户档案让店员和顾客都能完成更多旅程，提升每次访问的营收。第三是留存：跨渠道客户的终身价值约高出 30%，因此复购率哪怕小幅改善也会复利放大。常见的错误是只汇报其中一项——项目会因所选指标不同，看起来要么投入不足，要么夸大其词。</p>
<p>我们建议从第一阶段就采用对照（holdout）测量：把接受统一分析的实验组，与仍用孤岛报告管理的对照组比较，量化复购与客单的提升。保留对照组看似浪费，却是证明"是统一、而非季节或促销"驱动结果的唯一方法。及早埋点的零售商，能在两个季度内报出多渠道增量，并以此来资助下一阶段。</p>
<h2 id="common-omnichannel-failures">全渠道分析最常见的失败模式是什么？</h2>
<p>多数失败是顺序失败，而非技术失败。第一，在证明任何一个统一答案之前就搭建完整的客户 360 平台，让价值淹没在多年看不到成果的项目里。第二，把身份解析当成一次性批处理，而非持续过程，于是新标识到来时档案就漂移。第三，直到上线才补隐私架构，结果合规拦截统一档案时被迫返工。第四，靠"观点"而非"模型"度量：没有公认语义层，团队不断对账表格，"真实数字"成了嗓门最大者说了算。</p>
<p>解药就是我们一贯的顺序：先身份、再统一指标、再归因、最后实时库存——每一阶段都产出业务可见的结果。遵循此顺序的零售商在交付价值，竞争对手还在集成；平台是已被证明的胜果带来的结果，而非其前提。</p>
<h2 id="conversational-bi-and-omnichannel">对话式 BI 如何改变全渠道分析？</h2>
<p>传统全渠道仪表盘仍要求有人知道该打开哪份报告。对话式 BI 去掉这道门槛：店长可以用自然语言问"这家门店附近有哪些货、本店却没有"，并从同一个统一模型得到 grounded 的答案。把客户、商品、库存定义一次的语义层，成为每个渠道查询的唯一真相源，于是"全渠道活动提升了多少复购"这个问题，无论品类负责人在会上问，还是区域经理在聊天窗里问，都得到一致回答。</p>
<p>这正是统一带来的第二重红利。因为模型定义一次且受治理，自然语言答案继承了与仪表盘相同的身份解析、归因逻辑与访问控制——没有平行的"真相表格"。作为托管服务约两周即可部署，对话式 BI 把统一模型从报告资产变成零售组织日常的操作习惯。</p>
<h2 id="roadmap-from-pilot-to-enterprise">从试点到企业级落地的路线图是什么？</h2>
<p>不要一开始就建大平台。先选一个最高价值的连接——通常是电商与门店 POS 之间跨购物最多的客户身份——在一个用例上证明统一档案，比如复购测量或活动留存测试。第一阶段的目标，是用一个可信答案回答一个重要问题，而不是完美的客户 360。随后依次是统一指标、归因、实时库存；每一阶段都依赖前一阶段，也都产出业务可见的结果。遵循此顺序的零售商通常两个季度内就展现出多渠道价值提升，而先建完整平台的仍在建设中。</p>
'''
cn_faq = [
 ("什么是全渠道零售分析？",
  "全渠道零售分析是把线上与线下的客户、商品、库存数据统一起来的实践，让零售商在每个触点上看到同一个客户关系。它用单一模型取代孤岛式的渠道报告，支撑身份解析、跨渠道归因与实时库存可见。"),
 ("为什么身份解析是全渠道分析最难的部分？",
  "客户通过多种标识——邮箱、手机号、会员、设备——互动，且并非所有关联都确定。必须先把确定性匹配做好，概率匹配要设置信阈值，且解析要持续运行而非一次性批处理，否则新数据到来时统一档案就会漂移。"),
 ("数据统一后归因会发生什么变化？",
  "在统一数据上做算法归因，通常会把 20% 到 40% 的功劳从「最后一次点击」转移到真正创造需求的渠道。这会重塑预算决策，且只有在身份与同意架构健全时才可信。"),
 ("全渠道客户数据适用哪些隐私规则？",
  "在中国《个人信息保护法》与欧洲 GDPR 下，跨渠道统一必须以同意、目的限制与数据最小化为前提构建。统一档案应遵从各渠道中最严格的同意，只保留服务分析目的的数据，并在与各源系统相同的审计规则下可供访问。"),
]
cn_faq_html = faq_section(cn_faq)
cn_jsonld = faq_jsonld(cn_faq)
cn_inner = cn_extra + "\n" + cn_faq_html + "\n" + cn_jsonld + "\n"
tw_inner = cc.convert(cn_inner)

for lang, inner in (("zh-cn", cn_inner), ("zh-tw", tw_inner)):
    p = os.path.join(ROOT, "%s/blog/articles/%s.html"%(lang, slug))
    hh = open(p, encoding='utf-8').read()
    mm = re.search(r'(<p class="article-lead">.*?)(<nav class="article-nav")', hh, re.S)
    hh = hh[:mm.start(1)] + inner + hh[mm.end(1):]
    # fix tw CTA phrase
    if lang == "zh-tw":
        hh = hh.replace('article-cta-btn">預約演示', 'article-cta-btn">預約示範')
    open(p,'w',encoding='utf-8').write(hh)
    print(lang, "written")

# verify
for lang, pat in (("en","blog/articles/%s.html"),("zh-cn","zh-cn/blog/articles/%s.html"),("zh-tw","zh-tw/blog/articles/%s.html")):
    p = os.path.join(ROOT, pat%slug)
    hh = open(p, encoding='utf-8').read()
    b = re.search(r'<article class="article-content" id="article-content">(.*?)</article>', hh, re.S).group(1)
    if lang=="en":
        print(lang,"words=",len(re.findall(r"[A-Za-z0-9']+", b)),"faq=",b.count('faq-item'),"jsonld=", 'FAQPage' in hh,"css=",hh.count('article.css?v=20260826'),"js=",hh.count('article.js?v=20260826'),"footer=",hh.count('footer class="footer"'))
    else:
        print(lang,"cjk=",len(re.findall(r'[\u4e00-\u9fff]', b)),"faq=",b.count('faq-item'),"jsonld=", 'FAQPage' in hh,"css=",hh.count('article.css?v=20260826'),"footer=",hh.count('footer class="footer"'),"cta=", ('預約示範' in hh if lang=='zh-tw' else '预约演示' in hh))
