# -*- coding: utf-8 -*-
"""Slug 5: bias-detection-in-training-data-tools-and-techniques-a-2026-update — EN expand, zh full rewrite."""
import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/tmp")
from common import (load, save, rep1, re_dl, build_faq_list, build_jsonld,
                    body_h1, fill_excerpts, integrity, FAQ_RX, JSONLD_RX)

W = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/"
EN = W + "blog/articles/bias-detection-in-training-data-tools-and-techniques-a-2026-update.html"
ZHCN = W + "zh-cn/blog/articles/bias-detection-in-training-data-tools-and-techniques-a-2026-update.html"
ZHTW = W + "zh-tw/blog/articles/bias-detection-in-training-data-tools-and-techniques-a-2026-update.html"

# ---------------- EN ----------------
EN_FAQ = [
    ("What is bias detection in training data, and why does it matter in 2026?",
     "Bias detection is the discipline of finding and fixing systematic performance gaps across customer segments, demographics, or regions, before and after a model ships. It matters now because regulators made it an obligation: the EU AI Act's high-risk obligations, applying from August 2026, explicitly require bias testing and documentation. The cost of detection is small; the cost of discovery — fines, brand damage, failed deployments — is not."),
    ("Which tools are commonly used for bias detection?",
     "The established open-source options are IBM's AI Fairness 360 (the broadest library of fairness metrics and mitigation algorithms), Microsoft's Fairlearn (assessment and reduction techniques), and Google's What-If Tool (interactive slicing without code). Data profiling engines catch distribution skew before training. The bigger determinant of success is process: pipeline-embedded scans, release gates, and versioned audit records."),
    ("What does the EU AI Act require for bias testing?",
     "From August 2026, high-risk systems — including those used in employment, credit, insurance, and essential services — must have bias examination and mitigation built into data governance, periodic testing against discriminatory outcomes, technical documentation, human oversight mechanisms, and a conformity assessment before deployment, with records reproducible on demand."),
    ("How often should models be re-evaluated for bias after deployment?",
     "At least quarterly for most models, monthly for the highest-risk ones. Populations drift and upstream data changes, so a model that was fair at launch can degrade within quarters. The standard design is scheduled recomputation of sliced metrics on fresh data, with automatic alerts when a fairness gap crosses its threshold."),
]

SEC_TOOLS = '''<h2 id="which-tools-should-you-use-for-bias-detection">Which Tools Should You Use for Bias Detection?</h2>
<p>The open-source ecosystem has matured to the point where no team needs to invent its own fairness mathematics. IBM's AI Fairness 360 offers the broadest library of fairness metrics and mitigation algorithms; Microsoft's Fairlearn focuses on assessment and reduction techniques with clean scikit-learn integration; Google's What-If Tool supports interactive slicing of model behaviour without writing evaluation code. Alongside these, data profiling engines in the Great Expectations family catch distribution skew before any model is trained. Most teams do not lack algorithms — they lack these tools wired into their delivery process.</p>
<p>The real gap is rarely the toolkit; it is the process around it. Tools produce numbers, and release gates are what turn numbers into decisions. The pattern that works: embed bias scans in the training pipeline so every retrain runs them automatically, and record sliced fairness metrics as versioned metadata in the model registry, sitting next to accuracy rather than in a separate spreadsheet. When evaluating vendor platforms, test four capabilities explicitly: sliced evaluation support, a fairness metric suite, segment-level drift monitoring in production, and audit-ready documentation export.</p>
<p>Where Beehive Strategy operates, these checks are embedded in the governed data and semantic layer built with clients: segment definitions stay consistent across systems, audits are reproducible on demand, and results reach business owners through the tools they already use. The logo on the toolkit matters less than whether the numbers it produces actually change a decision — that is the test of a bias detection stack.</p>'''

SEC_EU = '''<h2 id="what-will-the-eu-ai-act-require-from-august-2026">What Will the EU AI Act Require from August 2026?</h2>
<p>The EU AI Act's high-risk obligations apply from August 2026, and systems used in employment, credit, insurance, and essential services fall squarely in scope. The Act explicitly requires bias examination and mitigation within training-data governance, together with periodic testing to ensure that outputs are not discriminatory — the text turns what was best practice into a legal obligation with defined evidence requirements.</p>
<p>Compliance extends well beyond running tests once. Providers need technical documentation, automatic logging, human oversight mechanisms, and a conformity assessment before market placement, with records that must be reproducible on demand. Penalties for the most serious breaches reach into the tens of millions of euros or a meaningful percentage of global turnover — enough to move bias from a values conversation to a board agenda item.</p>
<p>Practical preparation comes down to three moves. First, inventory your models and map each against the Act's use-case categories, so scope is known before regulators ask. Second, begin bias audits now rather than in mid-2026; the documentation requirement alone takes quarters to satisfy properly. Third, merge the EU requirements into existing model risk management frameworks instead of running a parallel process — supervisory direction in Hong Kong and Singapore is converging on the same segment-level validation expectations, so one well-built evidence trail serves all of them.</p>'''

SEC_MON = '''<h2 id="how-should-you-monitor-bias-after-deployment">How Should You Monitor Bias After Deployment?</h2>
<p>Bias is not a static property. Populations shift, upstream data sources change, and model outputs feed back into future training data — so a model that was fair at launch can degrade within quarters. Organizations without post-launch monitoring are betting fairness on a snapshot taken the day the model shipped, which is precisely when their evidence is strongest and least representative of what follows.</p>
<p>An operable monitoring design has four elements: sliced metrics recomputed on fresh data on a fixed schedule; automatic alerts when a fairness gap crosses its threshold; a named owner and response time for every alert; and an incident-style handling loop — investigate the cause, remediate through reweighting or retraining, document what was done. Quarterly cadence suits most organizations; monthly is appropriate for the highest-risk models in credit, hiring, and health.</p>
<p>Monitor the monitoring, too. Which segments were tested, what thresholds were set, and who approved any exception belong inside the audit record, reviewed with the same seriousness as model performance itself. The organizations that defend their models successfully are the ones whose evidence trail shows sustained attention — not a compliance exercise performed once and forgotten.</p>'''

PARA_P = '''<p>Ownership deserves its own line in the plan. Bias audits fail most often because everyone is accountable and no one is responsible: name an owner for every high-risk model, give that person the authority to block a release when thresholds are breached, and put the model portfolio on a quarterly review agenda. Governance structure, more than any single technique, is what makes bias detection durable once the initial audit is finished.</p>'''

PARA_D2 = '''<p>Document the detection itself. Record which segments were tested, the metrics and thresholds applied, and the exact model version audited, so any result can be reproduced months later when a regulator, customer, or auditor asks. An audit that cannot be re-run is an opinion; an audit that can be re-run is evidence.</p>'''

def process_en():
    s = load(EN)
    h1 = body_h1(s)
    assert "Bias" in h1, "wrong file? h1=" + h1
    if 'which-tools-should-you-use-for-bias-detection' in s:
        print("EN already processed, skip")
        return
    # 1) H2 question-form conversions (keep ids)
    s = rep1(s, '<h2 id="the-current-landscape">The Current Landscape</h2>',
             '<h2 id="the-current-landscape">Why Has Bias Detection Become an Operational Priority in 2026?</h2>', 'h2-1')
    s = rep1(s, '<h2 id="key-implementation-challenges">Key Implementation Challenges</h2>',
             '<h2 id="key-implementation-challenges">What Makes Bias Detection So Hard to Implement?</h2>', 'h2-2')
    s = rep1(s, '<h2 id="practical-approaches-that-work">Practical Approaches That Work</h2>',
             '<h2 id="practical-approaches-that-work">How Do You Operationalize Bias Detection?</h2>', 'h2-3')
    s = rep1(s, '<h2 id="key-takeaways">Key Takeaways</h2>',
             '<h2 id="key-takeaways">What Are the Key Takeaways for 2026?</h2>', 'h2-4')
    s = rep1(s, '<h2 id="conclusion">Conclusion</h2>',
             '<h2 id="conclusion">Why Will Bias Detection Decide Who Gets to Deploy AI at Scale?</h2>', 'h2-5')
    # 2) extra paragraphs
    s = rep1(s, 'reviewing high-impact models.</p>',
             'reviewing high-impact models.</p>\n' + PARA_D2, 'paraD2')
    s = rep1(s, 'learn from its own track record.</p>',
             'learn from its own track record.</p>\n' + PARA_P, 'paraP')
    # 3) new sections: tools after detect section; EU + monitoring before takeaways
    s = rep1(s, '<h2 id="practical-approaches-that-work">', SEC_TOOLS + '\n<h2 id="practical-approaches-that-work">', 'sec-tools')
    s = rep1(s, '<h2 id="key-takeaways">', SEC_EU + '\n' + SEC_MON + '\n<h2 id="key-takeaways">', 'sec-eu-mon')
    # 4) FAQ block + JSON-LD before article-nav
    faq_sec = ('            <section class="faq-section" id="faq" aria-label="Frequently Asked Questions">\n'
               '                <h2 class="faq-section-title">\n'
               '                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>\n'
               '                    Frequently Asked Questions\n'
               '                </h2>\n'
               '<div class="faq-list">\n' + build_faq_list(EN_FAQ) + '\n                </div>\n            </section>')
    nav_line = '            <nav class="article-nav" aria-label="Article navigation">'
    assert s.count(nav_line) == 1
    s = s.replace(nav_line, faq_sec + '\n' + build_jsonld(EN_FAQ) + '\n\n' + nav_line)
    # 5) TOC sync
    toc_entries = [
        ("the-current-landscape", "Why Has Bias Detection Become an Operational Priority in 2026?"),
        ("key-implementation-challenges", "What Makes Bias Detection So Hard to Implement?"),
        ("how-do-you-detect-bias-you-cannot-see", "How Do You Detect Bias You Cannot See?"),
        ("which-tools-should-you-use-for-bias-detection", "Which Tools Should You Use for Bias Detection?"),
        ("practical-approaches-that-work", "How Do You Operationalize Bias Detection?"),
        ("what-will-the-eu-ai-act-require-from-august-2026", "What Will the EU AI Act Require from August 2026?"),
        ("how-should-you-monitor-bias-after-deployment", "How Should You Monitor Bias After Deployment?"),
        ("key-takeaways", "What Are the Key Takeaways for 2026?"),
        ("conclusion", "Why Will Bias Detection Decide Who Gets to Deploy AI at Scale?"),
    ]
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in toc_entries)
    s = re_dl(s, r'<div class="toc-mobile-links">.*?</div>', '<div class="toc-mobile-links">\n' + mob + '\n                </div>', 'toc-mobile')
    # 6) excerpts
    s = fill_excerpts(s, [
        "How inclusive data teams produce fairer models — and the practices that make inclusion stick.",
        "Where the AI agent layer fits in a modern data strategy, and what to build first.",
        "How vector databases power enterprise semantic search, with a 2026 implementation guide.",
    ], "EN-excerpt")
    integrity(s, [
        '?v=20260901', '"@type": "BlogPosting"', '"@type": "BreadcrumbList"',
        'id="which-tools-should-you-use-for-bias-detection"',
        'id="what-will-the-eu-ai-act-require-from-august-2026"',
        'id="how-should-you-monitor-bias-after-deployment"',
        '"@type": "FAQPage"', 'Book a Demo',
        '<h1 class="article-h1">',
    ], 9, "EN")
    assert 'Bias' in body_h1(s), "EN h1 changed!"
    save(EN, s)
    print("EN done")

# ---------------- zh-CN ----------------
CN_FAQ = [
    ("什么是训练数据偏见检测？为什么它在2026年如此重要？",
     "偏见检测是在模型部署前后系统性发现并修复跨客群、人口属性或地区性能差距的纪律。它在当下重要，是因为监管已将其变为义务：欧盟AI法案的高风险义务自2026年8月起适用，明确要求偏见测试与文档。检测的成本很小，而发现的代价——罚款、品牌损害、部署失败——很大。"),
    ("有哪些常用的偏见检测工具？",
     "成熟的开源选项包括IBM的AI Fairness 360（最全面的公平性指标与缓解算法库）、微软的Fairlearn（评估与减少技术）和谷歌的What-If Tool（免代码交互式切片）。数据剖析引擎在训练前捕捉分布偏移。决定成败的更大因素是流程：管道内扫描、发布门禁和可版本化的审计记录。"),
    ("欧盟AI法案对偏见测试有什么要求？",
     "自2026年8月起，雇用、信贷、保险和基本公共服务等高风险系统必须在数据治理中内置偏见检查与缓解、进行防止歧视性输出的定期测试，并具备技术文档、人工监督机制和部署前的合格评定，记录须可按需复现。"),
    ("模型上线后应该多久重新评估一次偏见？",
     "大多数模型至少每季度一次，最高风险模型（信贷、招聘、健康）每月一次。群体漂移和上游数据变化会让上线时公平的模型在几个季度内退化。标准做法是在新鲜数据上定期重算切片指标，公平性缺口超过阈值时自动告警。"),
]

CN_BODY = '''<p class="article-lead">训练数据中的偏见是2026年企业AI最隐蔽的破坏者。模型在总体指标上可能表现优异，却在特定客群、地区或员工群体上系统性失效——代价体现为监管罚款、品牌损害和错失的收入。偏见检测已经从研究课题成长为运营纪律，本文系统梳理实际有效的工具与技术，以及欧盟AI法案生效前企业必须完成的准备。</p>
<div class="article-tldr"><p><strong>核心要点：</strong>NIST评估发现部分人脸识别算法对特定人群的错误率高出10-100倍；Gartner警告到2027年多数AI模型将因偏见产生错误结果。欧盟AI法案高风险义务自2026年8月起明确要求偏见测试与文档。正确次序是：先审数据、按群体评估模型、部署后持续监控，并把偏见审计设为发布门禁。</p></div>
<h2 id="理解当前格局">为什么偏见检测在2026年成为企业AI的当务之急？</h2>
<p>偏见真实存在且可以测量。NIST对人脸识别算法的评估发现，某些人口群体的错误率比其他群体高出10-100倍，类似模式同样出现在信贷评分、招聘和医疗分析中。监管已经回应：欧盟AI法案的高风险义务自2026年8月起适用，明确要求对做出重大决策的系统进行偏见测试和文档记录。</p>
<p>Gartner警告，到2027年绝大多数AI模型将因偏见产生错误结果——除非组织投入认真的治理。而多数企业至今没有正式的偏见检测流程：模型验证中没有分群体评估，上线后没有子群体表现监控，也没有经得起监管审视的文档。总体准确率与分群体公平性之间的差距，正是偏见藏身之处。在金融、医疗、招聘等受监管行业，风险最为具体：有偏见的信贷或定价模型不只是公平性问题，而是有监管后果的行为风险，香港和新加坡的模型风险管理指引已经指向分群体验证方向。</p>
<h2 id="关键原则与战略框架">偏见检测实施的主要挑战有哪些？</h2>
<p>第一个挑战是偏见通常存在于数据而非模型。企业评估显示约70%的企业数据需要大幅准备才能支撑AI负载，代表性是准备工作的核心。历史数据内嵌历史决策：过去的信贷或招聘决策有偏见，数据标签就带有偏见，模型会忠实地复现它们。检测必须在模型存在之前开始——检查年龄、性别、地区等敏感属性上的分布，以及各群体内部的标签质量。</p>
<p>第二个挑战是选择公平的定义。人口均等、机会均等和校准各自编码了不同的公平定义，且可能相互冲突；选择取决于监管与业务语境，必须记录在案，因为它本质上是价值判断。第三个挑战是运营层面：偏见测试需要法务、数据科学和产品的跨职能协作，而上线后的偏见监控是最常被遗漏的一环——群体漂移和市场变化会让上线时公平的模型在几个季度内变得有偏见，没有定期重评估，组织只会从投诉而不是仪表板那里发现问题。</p>
<h2 id="实施方法与最佳实践">如何检测看不见的偏见？</h2>
<p>先看数据，再看模型。跨群体分布分析揭示代表性不足——如果某客群占目标市场20%却只占训练数据的2%，模型就不可能学好它。标签质量审计捕捉真相中的历史偏见；代理变量分析捕捉更隐蔽的情况：邮编、设备类型等看似中性的字段可能安静地编码了受保护群体的身份。</p>
<p>然后按群体测试模型。切片评估对每个群体分别计算准确率、精确率和假阳性率，而不是只看总体；人口均等、机会均等等公平性指标量化群体间差距；反事实测试检验模型对仅敏感属性不同的两个人是否会做出不同决定。更进一步是因果与反事实审计——这位申请人换一个受保护属性还会被批准吗？这位患者还会被标记吗？这些问题比基于相关性的检查更诚实地穿透代理变量和历史锁定，也越来越被成熟的监管机构所期待。</p>
<p>最后，把检测本身记录在案：记录测试了哪些群体、使用了哪些指标和阈值、审计的是哪个版本的模型，这样几个月后监管者、客户或审计师提问时，任何结果都可以复现。无法重跑的审计只是观点，可以重跑的审计才是证据。</p>
<h2 id="常用偏见检测工具">有哪些常用的偏见检测工具？</h2>
<p>开源公平性生态已经成熟到没有团队需要自己发明公平性数学。IBM的AI Fairness 360提供最全面的公平性指标与缓解算法库；微软的Fairlearn专注于评估与减少技术，并与scikit-learn良好集成；谷歌的What-If Tool支持无需编写评估代码的交互式切片检查。配合这些，Great Expectations一类的数据剖析引擎在模型训练之前捕捉分布偏移。多数团队不缺算法，缺的是把这些工具接进交付流程。</p>
<p>真正的缺口很少在工具箱，而在流程。工具产出数字，发布门禁才把数字变成决策。有效的模式是：把偏见扫描嵌入训练流水线，每次重训自动运行；把切片公平性指标作为版本化元数据记录进模型注册表，与准确率并列。评估供应商平台时，明确测试四项能力：分群体评估支持、公平性指标套件、生产环境的群体级漂移监控、以及可审计的文档导出。Beehive Strategy的方法把这些检查嵌入与客户共建的受治理数据层和语义层，使群体定义跨系统一致、审计可按需复现、结果通过业务团队已在用的工具送达。工具箱上的标志不如它产出的数字能否改变某个决策重要。</p>
<h2 id="衡量成功与展示投资回报率">如何让偏见检测真正落地？</h2>
<p>从最高风险用例开始：信贷、招聘、定价、保险，以及一切触及健康或身份的场景。在部署前运行结构化偏见审计——数据分布审查、标签审计、切片评估、公平性指标、文档记录——并把审计设为发布门禁而非可选项。对低风险的内部用途，轻量清单也能保留这个习惯。</p>
<p>能自动化的自动化：偏见扫描在数据管道内运行，新数据到达时标记群体级偏移；切片指标仪表板让子群体表现在生产中持续可见；重采样、重加权和约束优化等缓解技术处理发现的问题。责任归属需要在计划中单列一行——偏见审计失败最常见的原因是人人负责等于无人负责：为每个高风险模型指定责任人，赋予其在阈值被突破时叫停发布的权限，并按季度复审模型组合。同时保持人在回路、定期审查边缘群体、记录一切：选定的指标、设定的阈值、审查的证据和最终结论。文档不是官僚主义，它是满足监管、抗辩质疑、让组织从自身记录中学习的资产。</p>
<h2 id="欧盟AI法案的要求">欧盟AI法案对偏见测试有什么要求？</h2>
<p>欧盟AI法案的高风险义务自2026年8月起适用，雇用、信贷、保险和基本公共服务中使用的系统都在明确范围内。法案要求在训练数据治理中内置偏见检查与缓解，并进行定期测试以确保输出不具有歧视性——这把过去的最佳实践变成了有明确证据要求的法律义务。</p>
<p>合规远不止跑一次测试。提供商需要技术文档、自动日志、人工监督机制和投放市场前的合格评定，记录必须可按需复现。最严重违规的罚款可达数千万欧元或全球营业额的可观比例——足以把偏见从价值观讨论提升为董事会议程。实际准备归结为三步：盘点模型并对照法案用例类别确定范围，在监管者提问之前搞清边界；现在就开始偏见审计而不是等到2026年中，仅文档要求就需要数个季度才能妥善满足；把欧盟要求并入现有模型风险管理框架而不是另起炉灶——香港和新加坡的监管指引正指向同样的分群体验证预期，一套构建良好的证据链可以同时满足所有这些要求。</p>
<h2 id="常见陷阱及规避方法">部署后如何持续监控模型偏见？</h2>
<p>偏见不是静态属性。群体构成漂移、上游数据源变化、模型输出反馈进入未来的训练数据——上线时公平的模型可能在几个季度内退化。没有部署后监控的组织，等于把公平性押注在模型发布当天拍摄的快照上，而那恰恰是证据最强、却最不能代表此后情况的时刻。</p>
<p>可运营的监控设计有四个要素：按固定时间表在新鲜数据上重算切片指标；公平性缺口越过阈值时自动告警；每条告警有明确的责任人和响应时限；以事件方式处理——调查原因、通过重加权或重训缓解、记录处理过程。季度节奏适合多数组织；信贷、招聘、健康等最高风险模型宜按月。还要监控监控本身：测试了哪些群体、设定了什么阈值、谁批准了任何例外，这些都应纳入审计记录并与模型表现同样认真地复审。能成功为自己的模型辩护的组织，是那些证据链显示持续关注的组织，而不是做一次性合规表演的组织。</p>
<h2 id="关键要点">2026年的关键要点是什么？</h2>
<ul>
<li>先审数据再审模型——代表性和标签质量是第一道防线</li>
<li>按群体评估模型而非只看总体；公平性指标量化群体间差距</li>
<li>选择并记录公平性定义——这是有监管分量的价值判断</li>
<li>把偏见检查设为发布门禁，上线后持续监控子群体表现</li>
<li>把自动扫描嵌入数据管道，让检测随模型规模扩展</li>
<li>在2026年8月欧盟AI法案高风险义务生效前完成准备</li>
</ul>
<h2 id="结论">为什么偏见检测决定谁能规模化部署AI？</h2>
<p>2026年的偏见检测是一门工具成熟、方法清晰的纪律，采纳它的组织才被允许规模化部署AI——被监管者允许、被客户允许、也被自己的风险职能允许。检测的成本很小，发现的代价很大。</p>
<p>今天就把偏见检查建进数据管道、模型验证和监控体系的组织，明天就能更快交付AI，因为信任正是解锁部署的东西。另一种结局——从报纸头版得知模型伤害了某个弱势群体——没有组织需要学第二次。</p>
<section class="faq-section" id="faq" aria-label="常见问题">
    <h2 class="faq-section-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        常见问题
    </h2>
<div class="faq-list">
{FAQ_LIST}
</div>
</section>
{JSONLD}'''

def process_cn():
    s = load(ZHCN)
    h1 = body_h1(s)
    assert '偏见' in h1, "wrong file? h1=" + h1
    if 'id="常用偏见检测工具"' in s:
        print("CN already processed, skip")
        return
    body = CN_BODY.replace('{FAQ_LIST}', build_faq_list(CN_FAQ)).replace('{JSONLD}', build_jsonld(CN_FAQ))
    n = len(re.findall(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")', s, re.S))
    assert n == 1, f"cn body span: {n}"
    s = re.sub(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")',
               lambda m: body, s, count=1, flags=re.S)
    # TOC sync
    toc_entries = [
        ("理解当前格局", "为什么偏见检测在2026年成为企业AI的当务之急？"),
        ("关键原则与战略框架", "偏见检测实施的主要挑战有哪些？"),
        ("实施方法与最佳实践", "如何检测看不见的偏见？"),
        ("常用偏见检测工具", "有哪些常用的偏见检测工具？"),
        ("衡量成功与展示投资回报率", "如何让偏见检测真正落地？"),
        ("欧盟AI法案的要求", "欧盟AI法案对偏见测试有什么要求？"),
        ("常见陷阱及规避方法", "部署后如何持续监控模型偏见？"),
        ("关键要点", "2026年的关键要点是什么？"),
        ("结论", "为什么偏见检测决定谁能规模化部署AI？"),
    ]
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{t}</a>' for o, t in toc_entries)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
    assert s2 != s, "cn toc replace failed"
    s = s2
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "数据质量自动化让数据治理从被动补救转向主动预防。",
        ], "CN-excerpt")
    integrity(s, [
        '?v=20260901', '预约演示', '"@type": "FAQPage"',
        'id="常用偏见检测工具"', 'id="欧盟AI法案的要求"',
        '为什么偏见检测在2026年成为企业AI的当务之急', 'id="理解当前格局"', 'id="结论"',
    ], 9, "zh-CN")
    assert '偏见' in body_h1(s), "CN h1 changed!"
    save(ZHCN, s)
    print("zh-CN done")

# ---------------- zh-TW ----------------
TW_FAQ = [
    ("什麼是訓練資料偏見偵測？為什麼它在2026年如此重要？",
     "偏見偵測是在模型部署前後系統性發現並修復跨客群、人口屬性或地區效能差距的紀律。它在當下重要，是因為監管已將其變為義務：歐盟AI法案的高風險義務自2026年8月起適用，明確要求偏見測試與文件。偵測的成本很小，而發現的代價——罰款、品牌損害、部署失敗——很大。"),
    ("有哪些常用的偏見偵測工具？",
     "成熟的開源選項包括IBM的AI Fairness 360（最全面的公平性指標與緩解演算法庫）、微軟的Fairlearn（評估與減少技術）和谷歌的What-If Tool（免程式碼互動式切片）。資料剖析引擎在訓練前捕捉分布偏移。決定成敗的更大因素是流程：管線內掃描、發布門檻和可版本化的稽核記錄。"),
    ("歐盟AI法案對偏見測試有什麼要求？",
     "自2026年8月起，雇用、信貸、保險和基本公共服務等高風險系統必須在資料治理中內建偏見檢查與緩解、進行防止歧視性輸出的定期測試，並具備技術文件、人工監督機制和部署前的合格評定，記錄須可按需重現。"),
    ("模型上線後應該多久重新評估一次偏見？",
     "大多數模型至少每季度一次，最高風險模型（信貸、招聘、健康）每月一次。群體漂移和上游資料變化會讓上線時公平的模型在幾個季度內退化。標準做法是在新鮮資料上定期重算切片指標，公平性缺口超過門檻時自動警報。"),
]

TW_BODY = '''<p class="article-lead">訓練資料中的偏見是2026年企業AI最隱蔽的破壞者。模型在總體指標上可能表現優異，卻在特定客群、地區或員工群體上系統性失效——代價體現為監管罰款、品牌損害和錯失的收入。偏見偵測已經從研究課題成長為營運紀律，本文系統梳理實際有效的工具與技術，以及歐盟AI法案生效前企業必須完成的準備。</p>
<div class="article-tldr"><p><strong>核心要點：</strong>NIST評估發現部分人臉識別演算法對特定人群的錯誤率高出10-100倍；Gartner警告到2027年多數AI模型將因偏見產生錯誤結果。歐盟AI法案高風險義務自2026年8月起明確要求偏見測試與文件。正確次序是：先審資料、按群體評估模型、部署後持續監控，並把偏見稽核設為發布門檻。</p></div>
<h2 id="理解當前格局">為什麼偏見偵測在2026年成為企業AI的當務之急？</h2>
<p>偏見真實存在且可以測量。NIST對人臉識別演算法的評估發現，某些人口群體的錯誤率比其他群體高出10-100倍，類似模式同樣出現在信貸評分、招聘和醫療分析中。監管已經回應：歐盟AI法案的高風險義務自2026年8月起適用，明確要求對做出重大決策的系統進行偏見測試和文件記錄。</p>
<p>Gartner警告，到2027年絕大多數AI模型將因偏見產生錯誤結果——除非組織投入認真的治理。而多數企業至今沒有正式的偏見偵測流程：模型驗證中沒有分群體評估，上線後沒有子群體表現監控，也沒有經得起監管審視的文件。總體準確率與分群體公平性之間的差距，正是偏見藏身之處。在金融、醫療、招聘等受監管行業，風險最為具體：有偏見的信貸或定價模型不只是公平性問題，而是有監管後果的行為風險，香港和新加坡的模型風險管理指引已經指向分群體驗證方向。</p>
<h2 id="關鍵原則與策略框架">偏見偵測實施的主要挑戰有哪些？</h2>
<p>第一個挑戰是偏見通常存在於資料而非模型。企業評估顯示約70%的企業資料需要大幅準備才能支撐AI負載，代表性是準備工作的核心。歷史資料內嵌歷史決策：過去的信貸或招聘決策有偏見，資料標籤就帶有偏見，模型會忠實地複現它們。偵測必須在模型存在之前開始——檢查年齡、性別、地區等敏感屬性上的分布，以及各群體內部的標籤品質。</p>
<p>第二個挑戰是選擇公平的定義。人口均等、機會均等和校準各自編碼了不同的公平定義，且可能相互衝突；選擇取決於監管與業務語境，必須記錄在案，因為它本質上是價值判斷。第三個挑戰是營運層面：偏見測試需要法務、資料科學和產品的跨職能協作，而上線後的偏見監控是最常被遺漏的一環——群體漂移和市場變化會讓上線時公平的模型在幾個季度內變得有偏見，沒有定期重評估，組織只會從投訴而不是儀表板那裡發現問題。</p>
<h2 id="實施方法與最佳實踐">如何偵測看不見的偏見？</h2>
<p>先看資料，再看模型。跨群體分布分析揭示代表性不足——如果某客群占目標市場20%卻只占訓練資料的2%，模型就不可能學好它。標籤品質稽核捕捉真相中的歷史偏見；代理變數分析捕捉更隱蔽的情況：郵遞區號、設備類型等看似中性的欄位可能安靜地編碼了受保護群體的身分。</p>
<p>然後按群體測試模型。切片評估對每個群體分別計算準確率、精確率和假陽性率，而不是只看總體；人口均等、機會均等等公平性指標量化群體間差距；反事實測試檢驗模型對僅敏感屬性不同的兩個人是否會做出不同決定。更進一步是因果與反事實稽核——這位申請人換一個受保護屬性還會被批准嗎？這位患者還會被標記嗎？這些問題比基於相關性的檢查更誠實地穿透代理變數和歷史鎖定，也越來越被成熟的監管機構所期待。</p>
<p>最後，把偵測本身記錄在案：記錄測試了哪些群體、使用了哪些指標和門檻、稽核的是哪個版本的模型，這樣幾個月後監管者、客戶或稽核師提問時，任何結果都可以重現。無法重跑的稽核只是觀點，可以重跑的稽核才是證據。</p>
<h2 id="實用偏見檢測工具">有哪些常用的偏見偵測工具？</h2>
<p>開源公平性生態已經成熟到沒有團隊需要自己發明公平性數學。IBM的AI Fairness 360提供最全面的公平性指標與緩解演算法庫；微軟的Fairlearn專注於評估與減少技術，並與scikit-learn良好整合；谷歌的What-If Tool支援無需編寫評估程式碼的互動式切片檢查。配合這些，Great Expectations一類的資料剖析引擎在模型訓練之前捕捉分布偏移。多數團隊不缺演算法，缺的是把這些工具接進交付流程。</p>
<p>真正的缺口很少在工具箱，而在流程。工具產出數字，發布門檻才把數字變成決策。有效的模式是：把偏見掃描嵌入訓練管線，每次重訓自動執行；把切片公平性指標作為版本化中繼資料記錄進模型註冊表，與準確率並列。評估供應商平臺時，明確測試四項能力：分群體評估支援、公平性指標套件、生產環境的群體級漂移監控、以及可稽核的文件匯出。Beehive Strategy的方法把這些檢查嵌入與客戶共建的受治理資料層和語義層，使群體定義跨系統一致、稽核可按需重現、結果透過業務團隊已在用的工具送達。工具箱上的標誌不如它產出的數字能否改變某個決策重要。</p>
<h2 id="衡量成功與展示投資回報率">如何讓偏見偵測真正落地？</h2>
<p>從最高風險用例開始：信貸、招聘、定價、保險，以及一切觸及健康或身分的場景。在部署前執行結構化偏見稽核——資料分布審查、標籤稽核、切片評估、公平性指標、文件記錄——並把稽核設為發布門檻而非可選項。對低風險的內部用途，輕量清單也能保留這個習慣。</p>
<p>能自動化的自動化：偏見掃描在資料管線內執行，新資料到達時標記群體級偏移；切片指標儀表板讓子群體表現在生產中持續可見；重抽樣、重新加權和約束最佳化等緩解技術處理發現的問題。責任歸屬需要在計畫中單列一行——偏見稽核失敗最常見的原因是人人負責等於無人負責：為每個高風險模型指定責任人，賦予其在門檻被突破時叫停發布的權限，並按季度複審模型組合。同時保持人在回路、定期審查邊緣群體、記錄一切：選定的指標、設定的門檻、審查的證據和最終結論。文件不是官僚主義，它是滿足監管、抗辯質疑、讓組織從自身記錄中學習的資產。</p>
<h2 id="歐盟AI法案的要求">歐盟AI法案對偏見測試有什麼要求？</h2>
<p>歐盟AI法案的高風險義務自2026年8月起適用，雇用、信貸、保險和基本公共服務中使用的系統都在明確範圍內。法案要求在訓練資料治理中內建偏見檢查與緩解，並進行定期測試以確保輸出不具有歧視性——這把過去的最佳實踐變成了有明確證據要求的法律義務。</p>
<p>合規遠不止跑一次測試。提供商需要技術文件、自動日誌、人工監督機制和投放市場前的合格評定，記錄必須可按需重現。最嚴重違規的罰款可達數千萬歐元或全球營業額的可觀比例——足以把偏見從價值觀討論提升為董事會議程。實際準備歸結為三步：盤點模型並對照法案用例類別確定範圍，在監管者提問之前搞清邊界；現在就開始偏見稽核而不是等到2026年中，僅文件要求就需要數個季度才能妥善滿足；把歐盟要求併入現有模型風險管理框架而不是另起爐灶——香港和新加坡的監管指引正指向同樣的分群體驗證預期，一套構建良好的證據鏈可以同時滿足所有這些要求。</p>
<h2 id="常見陷阱及規避方法">部署後如何持續監控模型偏見？</h2>
<p>偏見不是靜態屬性。群體構成漂移、上游資料源變化、模型輸出回饋進入未來的訓練資料——上線時公平的模型可能在幾個季度內退化。沒有部署後監控的組織，等於把公平性押注在模型發布當天拍攝的快照上，而那恰恰是證據最強、卻最不能代表此後情況的時刻。</p>
<p>可營運的監控設計有四個要素：按固定時間表在新鮮資料上重算切片指標；公平性缺口越過門檻時自動警報；每條警報有明確的責任人和回應時限；以事件方式處理——調查原因、透過重新加權或重訓緩解、記錄處理過程。季度節奏適合多數組織；信貸、招聘、健康等最高風險模型宜按月。還要監控監控本身：測試了哪些群體、設定了什麼門檻、誰批准了任何例外，這些都應納入稽核記錄並與模型表現同樣認真地複審。能成功為自己的模型辯護的組織，是那些證據鏈顯示持續關注的組織，而不是做一次性合規表演的組織。</p>
<h2 id="關鍵要點">2026年的關鍵要點是什麼？</h2>
<ul>
<li>先審資料再審模型——代表性和標籤品質是第一道防線</li>
<li>按群體評估模型而非只看總體；公平性指標量化群體間差距</li>
<li>選擇並記錄公平性定義——這是有監管分量的價值判斷</li>
<li>把偏見檢查設為發布門檻，上線後持續監控子群體表現</li>
<li>把自動掃描嵌入資料管線，讓偵測隨模型規模擴展</li>
<li>在2026年8月歐盟AI法案高風險義務生效前完成準備</li>
</ul>
<h2 id="結論">為什麼偏見偵測決定誰能規模化部署AI？</h2>
<p>2026年的偏見偵測是一門工具成熟、方法清晰的紀律，採納它的組織才被允許規模化部署AI——被監管者允許、被客戶允許、也被自己的風險職能允許。偵測的成本很小，發現的代價很大。</p>
<p>今天就把偏見檢查建進資料管線、模型驗證和監控體系的組織，明天就能更快交付AI，因為信任正是解鎖部署的東西。另一種結局——從報紙頭版得知模型傷害了某個弱勢群體——沒有組織需要學第二次。</p>
<section class="faq-section" id="faq" aria-label="常見問題">
    <h2 class="faq-section-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        常見問題
    </h2>
<div class="faq-list">
{FAQ_LIST}
</div>
</section>
{JSONLD}'''

def process_tw():
    s = load(ZHTW)
    h1 = body_h1(s)
    assert '偏見' in h1, "wrong file? h1=" + h1
    if 'id="實用偏見檢測工具"' in s:
        print("TW already processed, skip")
        return
    body = TW_BODY.replace('{FAQ_LIST}', build_faq_list(TW_FAQ)).replace('{JSONLD}', build_jsonld(TW_FAQ))
    n = len(re.findall(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")', s, re.S))
    assert n == 1, f"tw body span: {n}"
    s = re.sub(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")',
               lambda m: body, s, count=1, flags=re.S)
    toc_entries = [
        ("理解當前格局", "為什麼偏見偵測在2026年成為企業AI的當務之急？"),
        ("關鍵原則與策略框架", "偏見偵測實施的主要挑戰有哪些？"),
        ("實施方法與最佳實踐", "如何偵測看不見的偏見？"),
        ("實用偏見檢測工具", "有哪些常用的偏見偵測工具？"),
        ("衡量成功與展示投資回報率", "如何讓偏見偵測真正落地？"),
        ("歐盟AI法案的要求", "歐盟AI法案對偏見測試有什麼要求？"),
        ("常見陷阱及規避方法", "部署後如何持續監控模型偏見？"),
        ("關鍵要點", "2026年的關鍵要點是什麼？"),
        ("結論", "為什麼偏見偵測決定誰能規模化部署AI？"),
    ]
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{t}</a>' for o, t in toc_entries)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
    assert s2 != s, "tw toc replace failed"
    s = s2
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "資料質量自動化讓資料治理從被動補救轉向主動預防。",
        ], "TW-excerpt")
    integrity(s, [
        '?v=20260901', '預約示範', '"@type": "FAQPage"',
        'id="實用偏見檢測工具"', 'id="歐盟AI法案的要求"',
        '為什麼偏見偵測在2026年成為企業AI的當務之急', 'id="理解當前格局"', 'id="結論"',
    ], 9, "zh-TW")
    assert '偏見' in body_h1(s), "TW h1 changed!"
    save(ZHTW, s)
    print("zh-TW done")

if __name__ == "__main__":
    process_en()
    process_cn()
    process_tw()
    print("ALL DONE")
