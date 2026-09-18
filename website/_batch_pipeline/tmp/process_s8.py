# -*- coding: utf-8 -*-
"""Slug 8: cross-border-ai-compliance-strategy — EN H2 interrogative + FAQ rebuild; zh full rewrite."""
import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/tmp")
from common import (load, save, rep1, re_dl, build_faq_list, build_jsonld,
                    body_h1, fill_excerpts, integrity, FAQ_RX, JSONLD_RX)

W = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/"
EN = W + "blog/articles/cross-border-ai-compliance-strategy.html"
ZHCN = W + "zh-cn/blog/articles/cross-border-ai-compliance-strategy.html"
ZHTW = W + "zh-tw/blog/articles/cross-border-ai-compliance-strategy.html"

# ---------------- EN ----------------
EN_FAQ = [
    ("Which AI rules apply to a multinational enterprise in 2026?",
     "At minimum three regimes: the EU AI Act, whose prohibitions on unacceptable-risk systems have applied since February 2025, whose general-purpose AI transparency obligations arrived in August 2025, and whose bulk of obligations applies from August 2026; China's stack of PIPL, the Data Security Law (amended 2025), and the generative AI labeling measures; and the US sectoral and state-law patchwork, with the NIST AI RMF as the voluntary reference. Which specific obligations attach to a given system depends on where it is developed, deployed, trained, and used — the points of contact, not the headquarters."),
    ("How severe are the penalties for non-compliance?",
     "The EU AI Act backs its prohibitions with fines up to €35 million or 7% of worldwide annual turnover, whichever is higher. China has demonstrated headline enforcement: the CAC's 2022 fine of ¥8.026 billion — roughly US$1.2 billion — against Didi for data-law violations remains the benchmark. Sectoral regulators in finance, health, and employment add their own penalties on top. The scale of exposure is why compliance strategy is now a board-level topic rather than a legal-team task."),
    ("Should we build separate compliance programs for each market?",
     "No — harmonization is cheaper than duplication by an order of magnitude. A company that treats GDPR, PIPL, and the EU AI Act as three separate projects maintains three documentation systems that drift apart; a company that treats them as three requirement sets over one control framework keeps a single source of truth. Build one set of controls — model documentation, risk assessment, data governance, human oversight, transparency and labeling — and map each regime's requirements onto them so one evidence artifact serves multiple regulators."),
    ("How should an enterprise start building cross-border AI compliance?",
     "Start with the AI system inventory: every system in production or development, with its jurisdictions, data flows, and risk tier under the strictest applicable regime — you cannot manage compliance for systems you have not enumerated. Then define one control framework aligned to ISO/IEC 42001 and the NIST AI RMF, map each regime's requirements onto the controls, and automate the evidence collection so compliance status is queryable at any moment. Run the first cycle on a bounded portfolio in about 90 days, then expand."),
]

EN_TOC = [
    ("understanding-the-current-landscape", "What Does the Cross-Border AI Compliance Landscape Look Like in 2026?"),
    ("key-principles-and-strategic-framework", "Which Principles Guide a Cross-Border AI Compliance Strategy?"),
    ("which-rules-actually-apply-to-your-ai-systems", "Which Rules Actually Apply to Your AI Systems?"),
    ("implementation-approach-and-best-practices", "How Do You Implement Cross-Border AI Compliance?"),
    ("how-do-you-keep-one-operating-model-across-many-regimes", "How Do You Keep One Operating Model Across Many Regimes?"),
    ("measuring-success-and-demonstrating-roi", "How Do You Measure Success and Demonstrate ROI?"),
    ("common-pitfalls-and-how-to-avoid-them", "What Are the Common Pitfalls and How Do You Avoid Them?"),
    ("key-takeaways", "What Are the Key Takeaways for Global Enterprises?"),
    ("conclusion", "Why Is Harmonization the Only Cross-Border AI Compliance Strategy That Scales?"),
]

def process_en():
    s = load(EN)
    h1 = body_h1(s)
    assert "Compliance" in h1, "wrong file? h1=" + h1
    if 'Which AI rules apply to a multinational enterprise in 2026?' in s:
        print("EN already processed, skip")
        return
    # 1) H2 interrogative conversions (keep ids)
    s = rep1(s, '<h2 id="understanding-the-current-landscape">Understanding the Current Landscape</h2>',
             '<h2 id="understanding-the-current-landscape">What Does the Cross-Border AI Compliance Landscape Look Like in 2026?</h2>', 'h2-1')
    s = rep1(s, '<h2 id="key-principles-and-strategic-framework">Key Principles and Strategic Framework</h2>',
             '<h2 id="key-principles-and-strategic-framework">Which Principles Guide a Cross-Border AI Compliance Strategy?</h2>', 'h2-2')
    s = rep1(s, '<h2 id="implementation-approach-and-best-practices">Implementation Approach and Best Practices</h2>',
             '<h2 id="implementation-approach-and-best-practices">How Do You Implement Cross-Border AI Compliance?</h2>', 'h2-3')
    s = rep1(s, '<h2 id="measuring-success-and-demonstrating-roi">Measuring Success and Demonstrating ROI</h2>',
             '<h2 id="measuring-success-and-demonstrating-roi">How Do You Measure Success and Demonstrate ROI?</h2>', 'h2-4')
    s = rep1(s, '<h2 id="common-pitfalls-and-how-to-avoid-them">Common Pitfalls and How to Avoid Them</h2>',
             '<h2 id="common-pitfalls-and-how-to-avoid-them">What Are the Common Pitfalls and How Do You Avoid Them?</h2>', 'h2-5')
    s = rep1(s, '<h2 id="key-takeaways">Key Takeaways</h2>',
             '<h2 id="key-takeaways">What Are the Key Takeaways for Global Enterprises?</h2>', 'h2-6')
    s = rep1(s, '<h2 id="conclusion">Conclusion</h2>',
             '<h2 id="conclusion">Why Is Harmonization the Only Cross-Border AI Compliance Strategy That Scales?</h2>', 'h2-7')
    # 2) remove head FAQPage
    s = re_dl(s, JSONLD_RX, '', 'head-faqpage-remove')
    # 3) rebuild FAQ list (h3-wrapped, topical)
    new_faq = '<div class="faq-list">\n' + build_faq_list(EN_FAQ) + '\n                </div>\n            </section>'
    s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'faq-list')
    old_nav = '</section>\n\n            <nav class="article-nav"'
    assert s.count(old_nav) == 1
    s = s.replace(old_nav, '</section>\n' + build_jsonld(EN_FAQ) + '\n\n            <nav class="article-nav"')
    # 4) TOC sync
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in EN_TOC)
    s = re_dl(s, r'<div class="toc-mobile-links">.*?</div>', '<div class="toc-mobile-links">\n' + mob + '\n                </div>', 'toc-mobile')
    # 5) excerpts
    s = fill_excerpts(s, [
        "How inclusive data teams catch the blind spots homogeneous hiring misses.",
        "Where the AI agent layer fits in a modern data strategy — and what to build first.",
        "A practical 2026 guide to vector databases and enterprise semantic search.",
    ], "EN-excerpt")
    integrity(s, [
        '?v=20260901', '"@type": "BlogPosting"', '"@type": "BreadcrumbList"',
        'id="which-rules-actually-apply-to-your-ai-systems"',
        'id="how-do-you-keep-one-operating-model-across-many-regimes"',
        'What Are the Key Takeaways for Global Enterprises?',
        '"@type": "FAQPage"', 'Book a Demo',
    ], 9, "EN")
    assert "Compliance" in body_h1(s)
    assert s[:s.index('</head>')].count('FAQPage') == 0
    save(EN, s)
    print("EN done")

# ---------------- zh-CN ----------------
CN_FAQ = [
    ("跨国企业在2026年需要遵守哪些AI规则？",
     "至少三个法域：欧盟AI法案——对不可接受风险系统的禁令自2025年2月适用，通用AI透明度义务于2025年8月到来，大部分义务自2026年8月适用；中国的PIPL、《数据安全法》（2025年修订）与生成式AI标识办法的组合；美国行业性与州级规则的拼图，以NIST AI RMF为自愿参照。具体义务取决于系统在哪里开发、部署、训练和使用——是接触点而非总部所在地决定适用规则。"),
    ("不合规的处罚有多严重？",
     "欧盟AI法案对禁止行为设定的罚款最高可达3500万欧元或全球年营业额的7%，取较高者。中国已展示过标志性执法：网信办2022年对滴滴处以80.26亿元罚款（约12亿美元），至今仍是数据法违规的标杆案例。金融、健康和雇佣领域的行业监管者还会在此之上叠加各自的处罚。风险敞口的量级，正是合规战略如今成为董事会级议题而非法务团队任务的原因。"),
    ("应该为每个市场分别建设合规项目吗？",
     "不应该——协调统一比重复建设便宜一个数量级。把GDPR、PIPL和欧盟AI法案当作三个独立项目的公司，维护着三套彼此漂移的文档系统；把它们当作同一控制框架上三组需求的公司，保持单一事实来源。正确做法是构建一套控制——模型文档、风险评估、数据治理、人工监督、透明度与标识——并把每个法域的要求映射上去，让一份证据材料服务多个监管者。"),
    ("企业应该如何启动跨境AI合规建设？",
     "从AI系统清单开始：盘点每一个生产中或开发中的系统，记录其法域、数据流和在最严格适用法域下的风险等级——没有枚举的系统无法管理合规。然后定义一个对齐ISO/IEC 42001和NIST AI RMF的控制框架，把各法域要求映射到控制上，并自动化证据收集，让合规状态随时可查询。在约90天内对有边界的组合跑完第一个循环，然后再扩展。"),
]

CN_TOC = [
    ("理解当前格局", "2026年跨境AI合规的监管格局是怎样的？"),
    ("关键原则与战略框架", "哪些原则指导跨境AI合规战略？"),
    ("哪些规则适用于你的ai系统", "哪些规则实际适用于你的AI系统？"),
    ("实施方法与最佳实践", "如何实施跨境AI合规战略？"),
    ("如何在多法域间保持统一运营模型", "如何在多法域间保持统一的运营模型？"),
    ("衡量成功与展示投资回报率", "如何衡量成功并展示投资回报？"),
    ("常见陷阱及规避方法", "常见陷阱有哪些，如何规避？"),
    ("关键要点", "跨国企业应记住哪些关键要点？"),
    ("结论", "为什么协调统一是唯一能规模化扩展的跨境AI合规战略？"),
]

CN_BODY = '''<p class="article-lead"><strong>跨境AI合规是让一套AI运营模型在多个法律法域之间运转的学科——2025年它变得刻不容缓：欧盟AI法案的禁令已开始适用，中国的标识与数据规则全面生效，而两个法域的罚款都以全球营业额的百分比计。</strong>制胜之道不是为每个市场分别建一套合规项目，而是把每个AI系统映射到触及它的规则、把控制协调为统一证据栈、并持续管理风险。本文讲解如何构建这一战略。</p>
<div class="article-tldr"><p><strong>核心要点：</strong>欧盟AI法案对禁止行为的罚款最高达3500万欧元或全球营业额的7%；网信办2022年对滴滴的80.26亿元罚款至今仍是中国数据执法的标杆。Gartner预计到2026年超过80%的企业将在生产中使用生成式AI API或模型——需要跨境合规管理的系统恰好在规则收紧之时大规模部署。协调统一的控制框架比逐法域重复建设便宜一个数量级。</p></div>
<h2 id="理解当前格局">2026年跨境AI合规的监管格局是怎样的？</h2>
<p>三个法域如今主导着全球AI合规议程，而每一家跨国企业都至少运转在其中两个之内。欧盟AI法案自2024年8月1日生效：对不可接受风险系统的禁令自2025年2月起适用，通用AI透明度义务于2025年8月到来，大部分义务自2026年8月适用——禁止行为的罚款最高可达3500万欧元或全球年营业额的7%。中国适用自己的规则栈：《个人信息保护法》（2021年11月1日生效）、《数据安全法》（2021年9月1日生效、2025年修订）、要求对AI生成内容进行标识的深度合成与生成式AI管理办法，以及2024年3月的跨境数据流动规定——网信办2022年7月对滴滴处以80.26亿元（约合12亿美元）罚款，展示了执法姿态。美国则叠加行业性法域——金融、健康、雇佣——和正在成形的州级规则拼图，背景是NIST于2023年1月发布的AI风险管理框架等自愿性框架。</p>
<p>部署语境让这一切刻不容缓。Gartner在2023年10月预测，到2026年将有超过80%的企业在生产中使用生成式AI API或模型，而2023年初这一比例还不到5%——这意味着现在需要跨境合规管理的系统，恰好在规则收紧的时刻被大规模部署。没有"观望"选项。</p>
<h2 id="关键原则与战略框架">哪些原则指导跨境AI合规战略？</h2>
<p>四条原则构成一个可辩护的跨境AI合规战略。第一条是<strong>先映射法域、再建设系统</strong>：对每个AI系统，识别触及它的法域——在哪里开发、在哪里部署、训练数据存放在哪里、用户在哪里——因为适用的义务跟随接触点，而不是总部。第二条是<strong>协调统一的控制</strong>：不为每个法域单独建一套控制，而是建一套控制——模型文档、风险评估、数据治理、人工监督、透明度与标识——把每个法域的要求映射上去，让一份证据材料服务多个监管者。第三条是<strong>按风险分级的深度</strong>：合规项目的深度应与系统在所适用的最严法域下的风险分级成比例，因为在一个市场属于高风险的系统，必须在所有市场达到同一标准。</p>
<p>第四条是<strong>持续的证据</strong>：跨境合规不是一次认证事件，而是一种必须随时可证明的状态，这意味着证据栈必须持续维护、持续可查询。战略洞察在于：协调统一比重复建设便宜一个数量级。把GDPR、PIPL和AI法案当作三个独立项目的公司，维护三套彼此漂移的文档系统；把它们当作同一控制框架上三组需求的公司，保持单一事实来源。</p>
<h2 id="哪些规则适用于你的ai系统">哪些规则实际适用于你的AI系统？</h2>
<p>应用规则需要映射纪律，下面的清单是任何跨边界系统的实际起点：</p>
<ul>
<li><strong>欧盟AI法案分级。</strong>系统是被禁止的（不可接受风险）、高风险、带透明度义务的有限风险，还是通用模型？分级决定附着哪些义务——罚款也随级别而变。</li>
<li><strong>中国的数据规则。</strong>系统是否处理中国境内个人的个人信息、是否跨境传输数据、是否生成合成内容？PIPL的合法性基础与同意规则、跨境传输机制（重要数据或超过一百万人的个人信息走安全评估，之下走标准合同）、以及2025年9月的标识办法，都适用于触达中国用户的AI系统。</li>
<li><strong>行业性法域。</strong>系统是否落在受监管行业——金融、健康、雇佣——美国、欧盟和中国在这些行业各自在通用法域之上叠加行业规则？</li>
<li><strong>透明度与标识。</strong>欧盟AI法案和中国的标识办法都要求告知用户正在与AI交互、并要求标识AI生成内容——两个法域、一种能力，只要在生成时一次性建好。</li>
<li><strong>标准对齐。</strong>ISO/IEC 42001——2023年12月发布的首个可认证AI管理体系标准——提供了同时满足大多数法域文档期望的控制结构。</li>
</ul>
<p>清单的意义在于：同一个系统很少只引出一个问题；它同时引出多个问题，而从一个受治理的清单出发回答它们，正是让战略可操作而非停留在纸面的关键。</p>
<h2 id="实施方法与最佳实践">如何实施跨境AI合规战略？</h2>
<p>分四步实施。第一，建立AI系统清单：每一个生产中或开发中的系统，记录其法域、数据流和在最严格适用法域下的风险等级——没有枚举的系统无法管理合规。第二，一次性定义控制框架，对齐ISO/IEC 42001和NIST AI RMF：文档、风险评估、数据治理、监督、透明度、事件响应。第三，把各法域的要求映射到控制上，生成一张显示哪些控制满足哪些法域哪些义务的矩阵——这张矩阵就是项目的操作手册。第四，给证据装上仪表：自动化收集模型文档、评估结果、标识记录和数据传输清单，并让全貌可查询，使合规状态随时可回答。</p>
<p>部署纪律与所有分析和合规项目的成功模式一致：从窄处起步、快速交付一个能用的能力、然后扩展。在你已运行的系统之上加一层托管对话层，可以实时回答跨法域合规问题——"我们哪些模型在向中国市场分发内容而没有按规定标识？"——在团队已在使用的聊天工具里，约两周上线第一个用例，并以托管服务方式维护。跨境合规由此不再是一场周期性的疲于奔命，而成为一种持续运转。</p>
<h2 id="如何在多法域间保持统一运营模型">如何在多法域间保持统一的运营模型？</h2>
<p>当三条纪律成立时，运营模型保持一致。第一，<strong>一份清单、一套控制框架</strong>：每个新系统进入同一份清单、通过同一套控制，无论开发它的是哪个市场——法域一旦催生平行流程，模型就会碎裂。第二，<strong>控制映射是活文档</strong>：控制与需求的矩阵必须随规则变化更新——欧盟AI法案到2026年的分阶段适用、2025年9月1日生效的中国《数据安全法》修订、新的行业规则——且更新必须流入自动化检查，而不只是流入一份演示文稿。第三，<strong>能回答问题的证据</strong>：项目健康度以它能否用当前数据回答监管者的问题来衡量——"给我看系统X的风险评估、这批资产的标识状态、这条数据流的传输机制"——通往这一能力的最快路径是在证据系统上加一层对话接口，让合规状态一次查询可得，而非一个项目可得。</p>
<h2 id="衡量成功与展示投资回报率">如何衡量成功并展示投资回报？</h2>
<p>在三个层级上衡量项目。运营层：清单中文档保持最新的AI系统占比、控制测试通过率、为监管者产出证据包的耗时、以及AI生成内容在各市场的标识覆盖率。业务层：协调框架在多个市场间摊薄后的单系统年合规成本、避免或快速整改的审计发现、以及新AI部署的速度——战略目标是合规放行系统的速度快于拦截速度。战略层：服务多个法域的控制占比（协调比率），以及进入新市场而无需新建合规项目的能力。基线是诚实的锚点：在项目启动前测量清单完整度、文档时效和证据组装耗时，然后每季度复测。以这种方式执行的组织会发现，前后对比的故事不是关于避免罚款——虽然那也重要——而是关于以没有协调框架的竞争对手无法企及的速度跨市场部署AI。</p>
<h2 id="常见陷阱及规避方法">常见陷阱有哪些，如何规避？</h2>
<p>最常见的失败是逐法域合规：三个法务团队、三套文档系统、一年三次审计——成本最高、漂移最大，清单永远对不上账。第二个是分级回避：因为欧盟AI法案风险分级和中国数据分级很难，就一直悬而不决，然后发现监管者最先问的恰恰是最难的问题。第三个是把证据栈当作文件柜：写一次就不再更新的文档不是证据，是负债。第四个是忽视AI内容层：当市场、客服和产品团队在跨市场生成AI内容时，标识与透明度是一种管道能力——把它们当作法务事后补录的公司，会同时倒在2025年9月的标识办法和AI法案的透明度义务上。第五个是只为最严法域建设：把每个系统都过度工程化到最高标准浪费资源，而按当地法域降低标准则会在更严法域同样适用的地方留下敞口。每个陷阱都由同一套架构规避：一份清单、一套协调的控制框架、持续的证据、按需的回答。</p>
<h2 id="关键要点">跨国企业应记住哪些关键要点？</h2>
<p>跨境AI合规的价值框架可以浓缩为五条要点：</p>
<ul>
<li>跨境AI合规意味着一套运营模型——法域映射、协调控制、风险分级深度、持续证据——应用于每个法域</li>
<li>风险已被量化：欧盟AI法案罚款最高3500万欧元或全球营业额的7%，滴滴80.26亿元罚单展示了中国的执法姿态</li>
<li>先建AI系统清单，再建一套对齐ISO/IEC 42001与NIST AI RMF的控制框架，然后把各法域要求映射上去</li>
<li>协调统一就是ROI：一份证据材料服务多个监管者，进入新市场变成一次映射练习而非一个新项目</li>
<li>让合规状态可查询——关于模型、标识和数据流的实时回答——让项目成为持续运转而非周期冲刺</li>
</ul>
<h2 id="结论">为什么协调统一是唯一能规模化扩展的跨境AI合规战略？</h2>
<p>把AI合规当作逐市场作业的时代结束了。欧盟AI法案、中国的数据与AI规则、美国的行业拼图，共同造就了一个同一系统要面对多个监管者、不同口径、不同处罚的世界——唯一能规模化扩展的战略是协调统一：一份清单、一套控制框架、一个证据栈，持续查询。运行它的技术今天已经存在：受治理的语义层、自动化的证据收集、以及实时回答合规问题的对话式接口——以托管服务方式在约两周内部署在你已运行的系统之上。采纳它的企业将把下一波监管当作一次配置变更；继续逐法域建设合规的企业会发现，法域之间的缝隙恰恰是风险和成本累积的地方。</p>
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
    assert '合规' in h1 or '合規' in h1, "wrong file? h1=" + h1
    if 'id="哪些规则适用于你的ai系统"' in s:
        print("CN already processed, skip")
        return
    body = CN_BODY.replace('{FAQ_LIST}', build_faq_list(CN_FAQ)).replace('{JSONLD}', build_jsonld(CN_FAQ))
    n = len(re.findall(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")', s, re.S))
    assert n == 1, f"CN body span: {n}"
    s = re.sub(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")',
               lambda m: body, s, count=1, flags=re.S)
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{t}</a>' for o, t in CN_TOC)
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
        'id="理解当前格局"', 'id="哪些规则适用于你的ai系统"', 'id="如何在多法域间保持统一运营模型"',
        '3500万欧元', '托管对话层',
    ], 9, "zh-CN")
    assert '合规' in body_h1(s) or '合規' in body_h1(s)
    save(ZHCN, s)
    print("CN done")

# ---------------- zh-TW ----------------
TW_FAQ = [
    ("跨國企業在2026年需要遵守哪些AI規則？",
     "至少三個法域：歐盟AI法案——對不可接受風險系統的禁令自2025年2月適用，通用AI透明度義務於2025年8月到來，大部分義務自2026年8月適用；中國的PIPL、《資料安全法》（2025年修訂）與生成式AI標識辦法的組合；美國行業性與州級規則的拼圖，以NIST AI RMF為自願參照。具體義務取決於系統在哪裡開發、部署、訓練和使用——是接觸點而非總部所在地決定適用規則。"),
    ("不合規的處罰有多嚴重？",
     "歐盟AI法案對禁止行為設定的罰款最高可達3500萬歐元或全球年營業額的7%，取較高者。中國已展示過標誌性執法：網信辦2022年對滴滴處以80.26億元罰款（約12億美元），至今仍是資料法違規的標杆案例。金融、健康和僱傭領域的行業監管者還會在此之上疊加各自的處罰。風險敞口的量級，正是合規戰略如今成為董事會級議題而非法務團隊任務的原因。"),
    ("應該為每個市場分別建設合規項目嗎？",
     "不應該——協調統一比重複建設便宜一個數量級。把GDPR、PIPL和歐盟AI法案當作三個獨立專案的公司，維護著三套彼此漂移的文檔系統；把它們當作同一控制框架上三組需求的公司，保持單一事實來源。正確做法是構建一套控制——模型文檔、風險評估、資料治理、人工監督、透明度與標識——並把每個法域的要求映射上去，讓一份證據材料服務多個監管者。"),
    ("企業應該如何啟動跨境AI合規建設？",
     "從AI系統清單開始：盤點每一個生產中或開發中的系統，記錄其法域、資料流和在最嚴格適用法域下的風險等級——沒有枚舉的系統無法管理合規。然後定義一個對齊ISO/IEC 42001和NIST AI RMF的控制框架，把各法域要求映射到控制上，並自動化證據收集，讓合規狀態隨時可查詢。在約90天內對有邊界的組合跑完第一個循環，然後再擴展。"),
]

TW_TOC = [
    ("理解當前格局", "2026年跨境AI合規的監管格局是怎樣的？"),
    ("關鍵原則與戰略框架", "哪些原則指導跨境AI合規戰略？"),
    ("哪些規則適用於你的ai系統", "哪些規則實際適用於你的AI系統？"),
    ("實施方法與最佳實踐", "如何實施跨境AI合規戰略？"),
    ("如何在多法域間保持統一營運模型", "如何在多法域間保持統一的營運模型？"),
    ("衡量成功與展示投資回報率", "如何衡量成功並展示投資回報？"),
    ("常見陷阱及規避方法", "常見陷阱有哪些，如何規避？"),
    ("關鍵要點", "跨國企業應記住哪些關鍵要點？"),
    ("結論", "為什麼協調統一是唯一能規模化擴展的跨境AI合規戰略？"),
]

TW_BODY = '''<p class="article-lead"><strong>跨境AI合規是讓一套AI營運模型在多個法律法域之間運轉的學科——2025年它變得刻不容緩：歐盟AI法案的禁令已開始適用，中國的標識與資料規則全面生效，而兩個法域的罰款都以全球營業額的百分比計。</strong>制勝之道不是為每個市場分別建一套合規項目，而是把每個AI系統映射到觸及它的規則、把控制協調為統一證據棧、並持續管理風險。本文講解如何構建這一戰略。</p>
<div class="article-tldr"><p><strong>核心要點：</strong>歐盟AI法案對禁止行為的罰款最高達3500萬歐元或全球營業額的7%；網信辦2022年對滴滴的80.26億元罰款至今仍是中國資料執法的標杆。Gartner預計到2026年超過80%的企業將在生產中使用生成式AI API或模型——需要跨境合規管理的系統恰好在規則收緊之時大規模部署。協調統一的控制框架比逐法域重複建設便宜一個數量級。</p></div>
<h2 id="理解當前格局">2026年跨境AI合規的監管格局是怎樣的？</h2>
<p>三個法域如今主導著全球AI合規議程，而每一家跨國企業都至少運轉在其中兩個之內。歐盟AI法案自2024年8月1日生效：對不可接受風險系統的禁令自2025年2月起適用，通用AI透明度義務於2025年8月到來，大部分義務自2026年8月適用——禁止行為的罰款最高可達3500萬歐元或全球年營業額的7%。中國適用自己的規則棧：《個人信息保護法》（2021年11月1日生效）、《資料安全法》（2021年9月1日生效、2025年修訂）、要求對AI生成內容進行標識的深度合成與生成式AI管理辦法，以及2024年3月的跨境資料流動規定——網信辦2022年7月對滴滴處以80.26億元（約合12億美元）罰款，展示了執法姿態。美國則疊加行業性法域——金融、健康、僱傭——和正在成形的州級規則拼圖，背景是NIST於2023年1月發布的AI風險管理框架等自願性框架。</p>
<p>部署語境讓這一切刻不容緩。Gartner在2023年10月預測，到2026年將有超過80%的企業在生產中使用生成式AI API或模型，而2023年初這一比例還不到5%——這意味著現在需要跨境合規管理的系統，恰好在規則收緊的時刻被大規模部署。沒有「觀望」選項。</p>
<h2 id="關鍵原則與戰略框架">哪些原則指導跨境AI合規戰略？</h2>
<p>四條原則構成一個可辯護的跨境AI合規戰略。第一條是<strong>先映射法域、再建設系統</strong>：對每個AI系統，識別觸及它的法域——在哪裡開發、在哪裡部署、訓練資料存放在哪裡、用戶在哪裡——因為適用的義務跟隨接觸點，而不是總部。第二條是<strong>協調統一的控制</strong>：不為每個法域單獨建一套控制，而是建一套控制——模型文檔、風險評估、資料治理、人工監督、透明度與標識——把每個法域的要求映射上去，讓一份證據材料服務多個監管者。第三條是<strong>按風險分級的深度</strong>：合規項目的深度應與系統在所適用的最嚴法域下的風險分級成比例，因為在一個市場屬於高風險的系統，必須在所有市場達到同一標準。</p>
<p>第四條是<strong>持續的證據</strong>：跨境合規不是一次認證事件，而是一種必須隨時可證明的狀態，這意味著證據棧必須持續維護、持續可查詢。戰略洞察在於：協調統一比重複建設便宜一個數量級。把GDPR、PIPL和AI法案當作三個獨立專案的公司，維護三套彼此漂移的文檔系統；把它們當作同一控制框架上三組需求的公司，保持單一事實來源。</p>
<h2 id="哪些規則適用於你的ai系統">哪些規則實際適用於你的AI系統？</h2>
<p>應用規則需要映射紀律，下面的清單是任何跨邊界系統的實際起點：</p>
<ul>
<li><strong>歐盟AI法案分級。</strong>系統是被禁止的（不可接受風險）、高風險、帶透明度義務的有限風險，還是通用模型？分級決定附著哪些義務——罰款也隨級別而變。</li>
<li><strong>中國的資料規則。</strong>系統是否處理中國境內個人的個人信息、是否跨境傳輸資料、是否生成合成內容？PIPL的合法性基礎與同意規則、跨境傳輸機制（重要資料或超過一百萬人的個人信息走安全評估，之下走標準合同）、以及2025年9月的標識辦法，都適用於觸達中國用戶的AI系統。</li>
<li><strong>行業性法域。</strong>系統是否落在受監管行業——金融、健康、僱傭——美國、歐盟和中國在這些行業各自在通用法域之上疊加行業規則？</li>
<li><strong>透明度與標識。</strong>歐盟AI法案和中國的標識辦法都要求告知用戶正在與AI交互、並要求標識AI生成內容——兩個法域、一種能力，只要在生成時一次性建好。</li>
<li><strong>標準對齊。</strong>ISO/IEC 42001——2023年12月發布的首個可認證AI管理體系標準——提供了同時滿足大多數法域文檔期望的控制結構。</li>
</ul>
<p>清單的意義在於：同一個系統很少只引出一個問題；它同時引出多個問題，而從一個受治理的清單出發回答它們，正是讓戰略可操作而非停留在紙面的關鍵。</p>
<h2 id="實施方法與最佳實踐">如何實施跨境AI合規戰略？</h2>
<p>分四步實施。第一，建立AI系統清單：每一個生產中或開發中的系統，記錄其法域、資料流和在最嚴格適用法域下的風險等級——沒有枚舉的系統無法管理合規。第二，一次性定義控制框架，對齊ISO/IEC 42001和NIST AI RMF：文檔、風險評估、資料治理、監督、透明度、事件響應。第三，把各法域的要求映射到控制上，生成一張顯示哪些控制滿足哪些法域哪些義務的矩陣——這張矩陣就是專案的營運手冊。第四，給證據裝上儀表：自動化收集模型文檔、評估結果、標識記錄和資料傳輸清單，並讓全貌可查詢，使合規狀態隨時可回答。</p>
<p>部署紀律與所有分析和合規專案的成功模式一致：從窄處起步、快速交付一個能用的能力、然後擴展。在你已運行的系統之上加一層託管對話層，可以即時回答跨法域合規問題——「我們哪些模型在向中國市場分發內容而沒有按規定標識？」——在團隊已在使用的聊天工具裡，約兩週上線第一個用例，並以託管服務方式維護。跨境合規由此不再是一場週期性的疲於奔命，而成為一種持續運轉。</p>
<h2 id="如何在多法域間保持統一營運模型">如何在多法域間保持統一的營運模型？</h2>
<p>當三條紀律成立時，營運模型保持一致。第一，<strong>一份清單、一套控制框架</strong>：每個新系統進入同一份清單、通過同一套控制，無論開發它的是哪個市場——法域一旦催生平行流程，模型就會碎裂。第二，<strong>控制映射是活文檔</strong>：控制與需求的矩陣必須隨規則變化更新——歐盟AI法案到2026年的分階段適用、2025年9月1日生效的中國《資料安全法》修訂、新的行業規則——且更新必須流入自動化檢查，而不只是流入一份簡報。第三，<strong>能回答問題的證據</strong>：專案健康度以它能否用當前資料回答監管者的問題來衡量——「給我看系統X的風險評估、這批資產的標識狀態、這條資料流的傳輸機制」——通往這一能力的最快路徑是在證據系統上加一層對話介面，讓合規狀態一次查詢可得，而非一個專案可得。</p>
<h2 id="衡量成功與展示投資回報率">如何衡量成功並展示投資回報？</h2>
<p>在三個層級上衡量專案。營運層：清單中文檔保持最新的AI系統佔比、控制測試通過率、為監管者產出證據包的耗時、以及AI生成內容在各市場的標識覆蓋率。業務層：協調框架在多個市場間攤薄後的單系統年合規成本、避免或快速整改的審計發現、以及新AI部署的速度——戰略目標是合規放行系統的速度快於攔截速度。戰略層：服務多個法域的控制佔比（協調比率），以及進入新市場而無需新建合規專案的能力。基線是誠實的錨點：在專案啟動前測量清單完整度、文檔時效和證據組裝耗時，然後每季度複測。以這種方式執行的組織會發現，前後對比的故事不是關於避免罰款——雖然那也重要——而是關於以沒有協調框架的競爭對手無法企及的速度跨市場部署AI。</p>
<h2 id="常見陷阱及規避方法">常見陷阱有哪些，如何規避？</h2>
<p>最常見的失敗是逐法域合規：三個法務團隊、三套文檔系統、一年三次審計——成本最高、漂移最大，清單永遠對不上帳。第二個是分級迴避：因為歐盟AI法案風險分級和中國資料分級很難，就一直懸而不決，然後發現監管者最先問的恰恰是最難的問題。第三個是把證據棧當作檔案櫃：寫一次就不再更新的文檔不是證據，是負債。第四個是忽視AI內容層：當市場、客服和產品團隊在跨市場生成AI內容時，標識與透明度是一種管道能力——把它們當作法務事後補錄的公司，會同時倒在2025年9月的標識辦法和AI法案的透明度義務上。第五個是只為最嚴法域建設：把每個系統都過度工程化到最高標準浪費資源，而按當地法域降低標準則會在更嚴法域同樣適用的地方留下敞口。每個陷阱都由同一套架構規避：一份清單、一套協調的控制框架、持續的證據、按需的回答。</p>
<h2 id="關鍵要點">跨國企業應記住哪些關鍵要點？</h2>
<p>跨境AI合規的價值框架可以濃縮為五條要點：</p>
<ul>
<li>跨境AI合規意味著一套營運模型——法域映射、協調控制、風險分級深度、持續證據——應用於每個法域</li>
<li>風險已被量化：歐盟AI法案罰款最高3500萬歐元或全球營業額的7%，滴滴80.26億元罰單展示了中國的執法姿態</li>
<li>先建AI系統清單，再建一套對齊ISO/IEC 42001與NIST AI RMF的控制框架，然後把各法域要求映射上去</li>
<li>協調統一就是ROI：一份證據材料服務多個監管者，進入新市場變成一次映射練習而非一個新專案</li>
<li>讓合規狀態可查詢——關於模型、標識和資料流的即時回答——讓專案成為持續運轉而非週期衝刺</li>
</ul>
<h2 id="結論">為什麼協調統一是唯一能規模化擴展的跨境AI合規戰略？</h2>
<p>把AI合規當作逐市場作業的時代結束了。歐盟AI法案、中國的資料與AI規則、美國的行業拼圖，共同造就了一個同一系統要面對多個監管者、不同口徑、不同處罰的世界——唯一能規模化擴展的戰略是協調統一：一份清單、一套控制框架、一個證據棧，持續查詢。運行它的技術今天已經存在：受治理的語義層、自動化的證據收集、以及即時回答合規問題的對話式介面——以託管服務方式在約兩週內部署在你已運行的系統之上。採納它的企業將把下一波監管當作一次配置變更；繼續逐法域建設合規的企業會發現，法域之間的縫隙恰恰是風險和成本累積的地方。</p>
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
    assert '合規' in h1, "wrong file? h1=" + h1
    if 'id="哪些規則適用於你的ai系統"' in s:
        print("TW already processed, skip")
        return
    body = TW_BODY.replace('{FAQ_LIST}', build_faq_list(TW_FAQ)).replace('{JSONLD}', build_jsonld(TW_FAQ))
    n = len(re.findall(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")', s, re.S))
    assert n == 1, f"TW body span: {n}"
    s = re.sub(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")',
               lambda m: body, s, count=1, flags=re.S)
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{t}</a>' for o, t in TW_TOC)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
    assert s2 != s, "tw toc replace failed"
    s = s2
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "資料品質自動化讓資料治理從被動補救轉向主動預防。",
        ], "TW-excerpt")
    integrity(s, [
        '?v=20260901', '預約示範', '"@type": "FAQPage"',
        'id="理解當前格局"', 'id="哪些規則適用於你的ai系統"', 'id="如何在多法域間保持統一營運模型"',
        '3500萬歐元', '託管對話層',
    ], 9, "zh-TW")
    assert '合規' in body_h1(s)
    save(ZHTW, s)
    print("TW done")

if __name__ == "__main__":
    process_en()
    process_cn()
    process_tw()
    print("ALL DONE")
