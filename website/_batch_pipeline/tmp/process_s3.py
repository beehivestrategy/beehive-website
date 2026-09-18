# -*- coding: utf-8 -*-
"""Slug 3: human-in-the-loop-ai-when-automation-needs-oversight-a-2026-update
EN: expand + convert H2s + add FAQ/JSON-LD. zh: full body rewrite (template junk)."""
import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/tmp")
from common import (load, save, rep1, build_faq_list, build_jsonld,
                    body_h1, fill_excerpts, integrity)

W = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/"
EN = W + "blog/articles/human-in-the-loop-ai-when-automation-needs-oversight-a-2026-update.html"
ZHCN = W + "zh-cn/blog/articles/human-in-the-loop-ai-when-automation-needs-oversight-a-2026-update.html"
ZHTW = W + "zh-tw/blog/articles/human-in-the-loop-ai-when-automation-needs-oversight-a-2026-update.html"

FAQ_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'

def faq_block(faq, label):
    return f'''            <section class="faq-section" id="faq" aria-label="{label}">
                <h2 class="faq-section-title">
                    {FAQ_ICON}
                    {label}
                </h2>
                <div class="faq-list">
{build_faq_list(faq)}
                </div>
            </section>
{build_jsonld(faq)}
'''

# ================= EN =================
EN_FAQ = [
    ("What is human-in-the-loop AI?",
     "Human-in-the-loop AI is an architecture where a person approves, reviews, or overrides automated decisions at defined points in the workflow. In 2026 it matters because regulators — most prominently under the EU AI Act — now treat human oversight for high-risk systems as an auditable obligation, and because over-trusted automation has produced costly, predictable failures."),
    ("Where does human oversight add the most value?",
     "In four situations: when a wrong decision is costly, when the supporting data is thin or ambiguous, when the case is novel rather than routine, and when the decision carries regulatory or ethical accountability. Concentrating human attention on these cases — instead of blanket review — is what keeps oversight a control rather than a bottleneck."),
    ("How do you stop reviewers from rubber-stamping AI decisions?",
     "Three mechanisms work together: escalation design that routes cases by severity instead of raw alert volume; a reviewer experience that surfaces the case, the model's reasoning, and similar precedents in seconds; and instrumentation — override-rate trends and adversarial audits — that makes complacency visible before it becomes systemic."),
    ("Can any decisions safely run without human review?",
     "Yes, when four conditions hold: the decision is low-impact and reversible, volumes make review uneconomic, the model is well calibrated with drift monitoring in place, and there is a fast rollback path. Even then, unattended tiers need periodic sampling audits. High-risk decisions should always retain named human approval with documented reasoning."),
]

SEC1 = '''<h2 id="what-do-the-2026-regulations-actually-require">What Do the 2026 Regulations Actually Require?</h2>
<p>The EU AI Act is the anchor text. For high-risk systems, operators must implement effective oversight measures: the humans designated to supervise must have the competence to understand the model's capabilities and limitations, remain aware of automation bias, be able to intervene in or interrupt the system, and hold the actual authority to do so. These are no longer phrases in a policy document — they are line items that auditors check one by one.</p>
<p>In practical terms, auditors now expect four categories of evidence. First, decision-rights documentation: who approves, who reviews, and who escalates, by risk tier. Second, override logs with context — the reasoning behind every human intervention, not just the fact of it. Third, ongoing review-quality evidence: review rates, override-rate trends, and sampling results. Fourth, training records for the humans in the loop. Oversight without this evidence is, from a regulator's perspective, oversight that does not exist.</p>
<p>Asia-Pacific enterprises should also note the extraterritorial reach. Firms with EU customers or operations must meet EU-level obligations regardless of where their headquarters sit, while supervisors such as the Monetary Authority of Singapore have folded AI governance into existing conduct frameworks. The pragmatic approach is to design the oversight architecture to the strictest applicable standard, rather than assembling a patchwork of per-jurisdiction minimums.</p>'''

SEC2 = '''<h2 id="how-do-you-staff-and-train-the-humans-in-the-loop">How Do You Staff and Train the Humans in the Loop?</h2>
<p>Role design comes before headcount. An operable oversight system typically defines three roles: frontline reviewers who approve or reject individual decisions; escalation owners who take over contested or out-of-bound cases; and an oversight lead who owns the design and performance of the whole tiering system. Capacity follows from arithmetic — decisions per day, average review time, target review rates — not from intuition.</p>
<p>Training needs a curriculum, not apprenticeship by osmosis. The core modules are statistical literacy (confidence, calibration, base rates), common failure modes (automation bias, alarm fatigue, anchoring), and the domain's case law — past decisions that went wrong and why. Leading teams develop reviewers into domain experts who understand the model, rather than operators who watch logs, and they re-certify annually because both models and regulations drift.</p>
<p>Reviewer experience determines review quality. When a reviewer opens a case, they should see at a glance: the full case, the model's conclusion and its reasoning, how similar historical cases resolved, and a direct channel to query the evidence in natural language. Compressing evidence retrieval from tens of minutes to seconds is the single investment that most improves both oversight quality and throughput.</p>'''

SEC3 = '''<h2 id="when-should-automation-run-without-any-human-review">When Should Automation Run Without Any Human Review?</h2>
<p>Unattended operation is the right choice when four conditions hold simultaneously: the impact of a wrong decision is small and reversible; volumes are large enough that human review is uneconomic; the model is well calibrated on the relevant distribution with drift monitoring in place; and an automated backstop exists — the ability to roll back or degrade to a human process quickly when something goes wrong.</p>
<p>Even unattended tiers cannot skip audit. Leading teams run periodic sampling reviews of unattended decisions — with sampling rates scaled to risk — and preserve a one-switch degradation capability: when drift monitors trip a threshold, the system automatically reverts to exception-based review. Trust is not a setting in the system; it is a property that evidence continuously earns.</p>
<p>The maturity arc makes this concrete. Almost no enterprise starts with unattended high-risk decisions. They begin with full human supervision, use override rates and sampling audits to demonstrate the model deserves more autonomy, and then widen the tiers progressively. Autonomy is earned with evidence, not configured with a flag.</p>'''

def process_en():
    s = load(EN)
    assert "human-in-the-loop" in body_h1(s).lower(), "wrong file"
    if 'what-do-the-2026-regulations-actually-require' in s:
        print("EN already processed, skip"); return
    # H2 conversions
    s = rep1(s, '<h2 id="the-current-landscape">The Current Landscape</h2>',
             '<h2 id="the-current-landscape">What Does Human-in-the-Loop AI Look Like in 2026?</h2>', 'h2-1')
    s = rep1(s, '<h2 id="key-implementation-challenges">Key Implementation Challenges</h2>',
             '<h2 id="key-implementation-challenges">Why Is Human Oversight So Hard to Implement?</h2>', 'h2-2')
    s = rep1(s, '<h2 id="practical-approaches-that-work">Practical Approaches That Work</h2>',
             '<h2 id="practical-approaches-that-work">How Do You Design Oversight That Actually Works?</h2>', 'h2-3')
    s = rep1(s, '<h2 id="an-operating-model-for-oversight-that-scales">An Operating Model for Oversight That Scales</h2>',
             '<h2 id="an-operating-model-for-oversight-that-scales">What Does an Operating Model for Oversight That Scales Look Like?</h2>', 'h2-4')
    s = rep1(s, '<h2 id="key-takeaways">Key Takeaways</h2>',
             '<h2 id="key-takeaways">What Are the Key Takeaways for 2026?</h2>', 'h2-5')
    s = rep1(s, '<h2 id="conclusion">Conclusion</h2>',
             '<h2 id="conclusion">Why Does Oversight Remain the Deciding Factor?</h2>', 'h2-6')
    # new sections
    a1 = 'survive contact with auditors, boards, and dissatisfied customers.</p>'
    s = rep1(s, a1, a1 + "\n" + SEC1, 'sec1')
    a2 = 'quietly investing their next budget cycle.</p>'
    s = rep1(s, a2, a2 + "\n" + SEC2, 'sec2')
    a3 = 'but 100% unsupervised is still a liability.</p>'
    s = rep1(s, a3, a3 + "\n" + SEC3, 'sec3')
    # FAQ section + JSON-LD before article-nav
    old_nav = '\n\n            <nav class="article-nav" aria-label="Article navigation">'
    assert s.count(old_nav) == 1, "nav anchor not unique"
    s = s.replace(old_nav, '\n\n' + faq_block(EN_FAQ, "Frequently Asked Questions") + '\n            <nav class="article-nav" aria-label="Article navigation">')
    # TOC sync
    toc = [
        ("the-current-landscape", "What Does Human-in-the-Loop AI Look Like in 2026?"),
        ("what-do-the-2026-regulations-actually-require", "What Do the 2026 Regulations Actually Require?"),
        ("where-does-human-oversight-actually-add-value", "Where Does Human Oversight Actually Add Value?"),
        ("key-implementation-challenges", "Why Is Human Oversight So Hard to Implement?"),
        ("how-do-you-staff-and-train-the-humans-in-the-loop", "How Do You Staff and Train the Humans in the Loop?"),
        ("practical-approaches-that-work", "How Do You Design Oversight That Actually Works?"),
        ("when-should-automation-run-without-any-human-review", "When Should Automation Run Without Any Human Review?"),
        ("an-operating-model-for-oversight-that-scales", "What Does an Operating Model for Oversight That Scales Look Like?"),
        ("key-takeaways", "What Are the Key Takeaways for 2026?"),
        ("conclusion", "Why Does Oversight Remain the Deciding Factor?"),
    ]
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in toc)
    side = "\n".join(f'                    <a href="#{i}" class="toc-link">{t}</a>' for i, t in toc)
    s = re.sub(r'<div class="toc-mobile-links">.*?</div>', lambda m: '<div class="toc-mobile-links">\n' + mob + '\n                </div>', s, count=1, flags=re.S)
    s = re.sub(r'<nav class="toc-links">.*?</nav>', lambda m: '<nav class="toc-links">\n' + side + '\n                </nav>', s, count=1, flags=re.S)
    # excerpts
    s = fill_excerpts(s, [
        "How inclusive AI teams build fairer models — and why diversity is a data advantage.",
        "Why 2026 data strategies need an AI agent layer to stay governed and composable.",
        "How vector databases power enterprise semantic search — a practical 2026 guide.",
    ], "EN-excerpt")
    integrity(s, [
        '?v=20260901', '"@type": "BlogPosting"', '"@type": "BreadcrumbList"',
        '"@type": "FAQPage"', 'id="what-do-the-2026-regulations-actually-require"',
        'id="when-should-automation-run-without-any-human-review"', 'Book a Demo',
        'Human-in-the-Loop AI: When Automation Needs Oversight',
    ], 10, "EN")
    save(EN, s)
    print("EN done")

# ================= zh-CN =================
CN_FAQ = [
    ("什么是人在回路AI？它在2026年为什么重要？",
     "人在回路AI指在自动化流程的关键节点保留人类批准、复核或否决的架构。2026年它重要有两个原因：监管上，欧盟AI法案等已把高风险系统的人类监督从建议变为可审计的义务；运营上，过度信任自动化带来的错误决策代价陡增。"),
    ("人类监督在哪些环节最有价值？",
     "四种情形：错误代价高昂、支撑数据稀薄或模糊、决策属于新情况而非常规、以及涉及监管或伦理问责。把人力集中在这四类情形——而不是一刀切的全面复核——监督才能成为控制手段而不是瓶颈。"),
    ("如何避免审核者沦为橡皮图章？",
     "三个机制配合：用按严重程度分流的升级设计取代告警数量；为审核者提供秒级可得证据的审核体验——案例、模型推理、相似判例一屏呈现；以及用覆盖率趋势和对抗性审计让敷衍在变成系统性问题之前现形。"),
    ("高风险决策可以让AI全自动吗？",
     "通常不行。高风险决策应保留具名负责人的书面批准并记录理由。无人值守需要同时满足四个条件——影响小且可逆、量大到人工不经济、模型充分校准且有漂移监控、存在快速回滚机制——高风险决策一般不满足第一条。"),
]

CN_BODY = '''<p class="article-lead">人在回路AI——让一个人为重大决策承担最终责任的自动化——在2026年已从伦理脚注变为运营必需品。随着监管收紧、企业把AI推向核保、招聘、信贷和理赔等核心流程，设计问题已从"我们能自动化多少"转变为"人类究竟应该出现在回路的哪个位置"。本文剖析2026年格局，并给出一套可规模化的监督框架。</p>
<h2 id="理解当前格局">为什么人在回路AI在2026年成为董事会级优先事项？</h2>
<p>监管环境自2023年以来显著收紧。欧盟《人工智能法案》分阶段生效，到2026年，高风险系统的人类监督义务已在实践中产生约束力——包括服务欧盟客户的亚太企业。新加坡、日本、韩国和澳大利亚的监管机构也相继发布指引，部分已将AI系统纳入现有金融行为监管框架。方向已经明确：人类监督正从自愿的最佳实践转变为可审计的合规要求。</p>
<p>商业论证同步增强。艾伦·图灵研究所等机构的研究记录了过度信任自动化如何产生可预测的失败——从错误的信贷决策到因无人质疑而放行的供应链越权操作。行业调查显示，约70%的企业报告至少有一个AI系统在某种形式的人工审核下运行。我们在客户工作中看到的模式非常清晰：刻意设计监督机制的企业，其自动化项目才能经受住审计师、董事会和不满客户的检验。</p>
<h2 id="监管要求2026">2026年的监管要求对人类监督意味着什么？</h2>
<p>以欧盟AI法案为锚点：高风险系统的运营方必须落实有效监督措施——被指定监督的人需要具备理解模型能力与局限的素养、对自动化偏见保持警觉、能够在必要时介入或叫停系统，并真正拥有这样做的权限。这些不再是政策文件里的措辞，而是审计中逐项核对的证据要求。</p>
<p>落实到操作层面，审计师现在期待四类证据：按风险分层记录的决策权限文档——谁批准、谁复核、谁升级；带上下文的人工覆盖日志——不仅记录干预事实，还记录理由；持续的审核质量证据——复核率、覆盖率趋势和抽样结果；以及回路中人类的培训记录。没有这些证据的监督，在监管视角下等同于不存在。</p>
<p>亚太企业还需注意域外效力：只要服务欧盟客户或开展业务，无论总部在哪里都必须满足欧盟层面的义务；新加坡金管局等机构则已把AI治理并入现有行为监管框架。务实的做法是按最严格的适用标准设计监督架构，而不是按辖区逐套拼接最低标准。</p>
<h2 id="关键原则与战略框架">人类监督在哪些环节真正创造价值？</h2>
<p>值得把问题问得更直接，因为一刀切的监督与一刀切的自动化同样浪费。人在四种情形下创造价值：错误决策代价高昂时；支撑决策的数据稀薄或模糊时；决策是新情况而非常规时；以及决策涉及监管或伦理问责时。在高频、低风险、常规性的决策中，人类只会增加延迟和新错误；而在重大决策中移除人类，正是自动化悄然失败的方式。</p>
<p>2026年的新变化是这一判断正在被制度化。企业正在构建决策矩阵，把每个自动化决策按风险分层，并为每层指定监督模式——高风险需人工批准、中风险按异常人工复核、低风险无人值守运行。分层是把监督从瓶颈变成控制的关键。这一定类工作如今已成为我们客户设计工作坊的第一项议程，因为后续所有决策——人力配置、工具选型和审计证据——都由此派生。</p>
<h2 id="实施方法与最佳实践">为什么人类监督在实践中难以落地？</h2>
<p>第一个挑战是告警悖论。为标记不确定案例而设计的系统，要么告警太少——模型在出错时依然自信——要么告警太多，让审核者产生告警疲劳并机械式批准。行业经验表明，审核者对80%-90%的标记项目未经实质审查即予批准：人类沦为橡皮图章，审计轨迹形同虚设。</p>
<p>第二个挑战是问责架构。当没有人能回答三个问题时，人在回路就会失效：谁做决定、依据什么证据、人与系统不一致时怎么办。无法回答这些问题的企业会发现监督有名无实。明确决策权并记录每次覆盖的理由，是数据治理问题，不是法律形式。</p>
<p>第三个挑战是规模。人工审核队列每天处理几百个决策尚可，但现代自动化每天产生数千个。如果工具不能把正确的上下文呈现给审核者——案例本身、模型推理、相似历史案例与反事实信息——监督就会成为限制吞吐量的约束。这正是对话式界面的用武之地：我们看到企业用自然语言查询在几秒内调取被标记决策背后的证据，而不是让审核者从日志文件中手工重建。</p>
<p>第四个挑战是团队能力。回路中的审核者往往是领域专家，却被推入一个需要统计素养的新角色——理解置信区间、校准度，以及模型误差与流程差异的区别。提供结构化培训、决策支持和明确"什么是好的审核"的组织，监督质量显著更好；放任审核者自行摸索的组织，得到的就是橡皮图章。</p>
<h2 id="监督团队建设">如何组建并培训回路中的人类团队？</h2>
<p>角色设计先于人数。可运营的监督体系通常定义三类角色：一线审核者负责具体决策的批准或否决；升级负责人接手有争议或超限的案例；监督负责人对整个分层体系的设计与绩效负责。人力配置来自吞吐量测算——每天多少决策、平均审核时长、目标复核率——而不是直觉。</p>
<p>培训要有课程，不能靠传帮带。核心模块包括统计素养（置信度、校准、基率）、常见失效模式（自动化偏见、告警疲劳、锚定效应），以及本域的判例库——过去哪些案例审错了、为什么。领先团队把审核者培养成懂模型的业务专家，而不是看日志的操作员，并每年重新认证，因为模型和法规都会漂移。</p>
<p>审核体验决定审核质量。审核者打开一个案例时，应当一眼看到：案例全貌、模型的结论与理由、相似历史案例的走向，以及一条用自然语言直接查询证据的通道。把调取证据的时间从几十分钟压缩到几秒，是同时提升监督质量和吞吐量的最关键投资。</p>
<h2 id="常见陷阱及规避方法">哪些监督实践方法被证明有效？</h2>
<p>做得好的企业在部署之前、而不是事故之后设计监督。他们先按风险层级分类决策，并在模型上线前为每层定义监督模式、问责归属和升级路径。事前分类成本很低；事故之后追加监督，付出的则是金钱和信任的双重代价。</p>
<p>其次，他们为回路装上仪表。每次人工复核、覆盖和批准都连同上下文一起记录，使组织能衡量监督在创造价值还是流于形式。指标在这里至关重要：覆盖率应按趋势监控——持续下降的覆盖率既可能意味着模型在变好，也可能意味着审核者在敷衍。监管者越来越期待看到恰恰是这类证据。</p>
<p>第三，用升级设计取代告警数量。成熟方案不把每个边界案例都推给人类，而是按严重程度和上下文分流：常规异常自动处理并通知；模糊案例连同决策支持摘要交给审核者；高后果案例要求具名负责人的书面批准。2026年的前沿已经从"人在回路中"演进到"在正确的时刻处于回路之上"。</p>
<p>第四，像测试模型一样测试回路。对抗性测试——故意投喂边界案例，观察是否在正确的时间把正确的审核者拉进来——能暴露准确率指标掩盖的缺口。我们建议企业把监督设计纳入模型评估记分卡，因为准确率99%但100%无人监督的模型，仍然是负债。</p>
<h2 id="衡量成功与展示投资回报率">什么情况下自动化可以无需人工审核？</h2>
<p>四个条件同时满足时，无人值守是合理选择：错误决策的影响小且可逆；决策量大到人工复核不经济；模型在相关分布上经过充分校准并有漂移监控；存在自动化的兜底机制——出问题时能快速回滚或降级到人工流程。</p>
<p>即便无人值守，审计不能缺席。领先团队对无人值守决策做周期性抽样复核——抽样比例随风险水平调整——并保留一键降级能力：当漂移监控触发阈值时，系统自动切回异常复核模式。信任不是系统的一个开关设置，而是用证据持续赢取的属性。</p>
<p>成熟度路径也印证了这一点。几乎没有企业一开始就让高风险决策无人值守；他们从全面人工监督起步，用覆盖率和抽样审计的数据证明模型值得更大自主权，再逐层放宽。自主权是挣来的，不是配置出来的。</p>
<h2 id="规模化运营模型">可规模化的监督运营模型是什么样的？</h2>
<p>一套实用的运营模型可以归纳为少数几条规则：高风险决策需人工批准并记录理由；中风险决策按异常复核并附带决策支持摘要；低风险决策无人值守并做周期性抽样审计。每一层都被记录、度量，并按月向问责负责人汇报。运营模型清单如下：</p>
<ol>
<li>部署前按风险层级对每个自动化决策分类。</li>
<li>为每层指定具名问责负责人，并预先定义升级路径。</li>
<li>连同上下文和理由记录每次复核、覆盖与批准。</li>
<li>把覆盖率和审核时延作为一等运营指标监控。</li>
<li>用对抗性测试案例周期性审计回路，而不只看生产统计。</li>
</ol>
<h2 id="关键要点">2026年的关键要点是什么？</h2>
<ul>
<li>人类监督是2026年的监管与声誉要求，不是设计上的点缀。</li>
<li>人工审核只在明确的节点创造价值——高后果、薄数据、新情况与问责环节。</li>
<li>风险分层监督（批准、复核、无人值守）胜过一刀切的人工复核。</li>
<li>为回路装上仪表：记录决策、监控覆盖率趋势、用对抗性案例审计。</li>
<li>对话式分析工具让审核者秒级调取决策证据，使监督与吞吐量兼容。</li>
</ul>
<h2 id="结论">为什么监督仍是决定性因素？</h2>
<p>2026年的人在回路AI，与其说是对人类的哲学承诺，不如说是严谨的系统设计。胜出的企业将监督视为一等公民——像其他控制项一样被工程化、度量和审计。蜂启咨询帮助亚太地区的组织构建的正是这一点：有治理的对话式分析，在人们已经在用的工具里、在决策需要的那一刻，呈现人类需要的证据。自动化是引擎，监督是方向盘——两者都必须被设计，而且要一起设计。</p>
'''
CN_TOC = [
    ("理解当前格局", "为什么人在回路AI在2026年成为董事会级优先事项？"),
    ("监管要求2026", "2026年的监管要求对人类监督意味着什么？"),
    ("关键原则与战略框架", "人类监督在哪些环节真正创造价值？"),
    ("实施方法与最佳实践", "为什么人类监督在实践中难以落地？"),
    ("监督团队建设", "如何组建并培训回路中的人类团队？"),
    ("常见陷阱及规避方法", "哪些监督实践方法被证明有效？"),
    ("衡量成功与展示投资回报率", "什么情况下自动化可以无需人工审核？"),
    ("规模化运营模型", "可规模化的监督运营模型是什么样的？"),
    ("关键要点", "2026年的关键要点是什么？"),
    ("结论", "为什么监督仍是决定性因素？"),
]

def process_cn():
    s = load(ZHCN)
    assert '人在回路' in body_h1(s), "wrong file"
    if '为什么人在回路AI在2026年成为董事会级优先事项' in s:
        print("zh-CN already processed, skip"); return
    # full body replacement: from article-lead to just before article-nav
    m = re.search(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")', s, re.S)
    assert m, "cn body anchor not found"
    body = CN_BODY + faq_block(CN_FAQ, "常见问题")
    s = s[:m.start()] + body + s[m.end():]
    # TOC sync
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in CN_TOC)
    side = "\n".join(f'                    <a href="#{i}" class="toc-link">{t}</a>' for i, t in CN_TOC)
    s = re.sub(r'<div class="toc-mobile-links">.*?</div>', lambda m: '<div class="toc-mobile-links">\n' + mob + '\n                </div>', s, count=1, flags=re.S)
    s = re.sub(r'<nav class="toc-links">.*?</nav>', lambda m: '<nav class="toc-links">\n' + side + '\n                </nav>', s, count=1, flags=re.S)
    # excerpt (3rd card: 数据质量自动化第二部分)
    s = fill_excerpts(s, ["数据质量自动化让数据治理从被动补救转向主动预防。"], "CN-excerpt")
    integrity(s, [
        '?v=20260901', '预约演示', '"@type": "FAQPage"',
        '为什么人在回路AI在2026年成为董事会级优先事项',
        '可规模化的监督运营模型', '不把每个边界案例',
    ], 11, "zh-CN")
    assert s.count('class="faq-item"') == 4
    save(ZHCN, s)
    print("zh-CN done")

# ================= zh-TW =================
TW_FAQ = [
    ("什麼是人在迴路AI？它在2026年為什麼重要？",
     "人在迴路AI指在自動化流程的關鍵節點保留人類批准、審查或否決的架構。2026年它重要有兩個原因：監管上，歐盟AI法案等已把高風險系統的人類監督從建議變為可審計的義務；營運上，過度信任自動化帶來的錯誤決策代價陡增。"),
    ("人類監督在哪些環節最有價值？",
     "四種情形：錯誤代價高昂、支撐資料稀薄或模糊、決策屬於新情況而非常規、以及涉及監管或倫理問責。把人力集中在這四類情形——而不是一刀切的全面複核——監督才能成為控制手段而不是瓶頸。"),
    ("如何避免審核者淪為橡皮圖章？",
     "三個機制配合：用按嚴重程度分流的升級設計取代警示數量；為審核者提供秒級可得證據的審核體驗——案例、模型推理、相似判例一屏呈現；以及用覆蓋率趨勢和對抗性審計讓敷衍在變成系統性問題之前現形。"),
    ("高風險決策可以讓AI全自動嗎？",
     "通常不行。高風險決策應保留具名負責人的書面批准並記錄理由。無人值守需要同時滿足四個條件——影響小且可逆、量大到人工不經濟、模型充分校準且有漂移監控、存在快速回滾機制——高風險決策一般不滿足第一條。"),
]

TW_BODY = '''<p class="article-lead">人在迴路AI——讓一個人為重大決策承擔最終責任的自動化——在2026年已從倫理腳註變為營運必需品。隨著監管收緊、企業把AI推向核保、招聘、信貸和理賠等核心流程，設計問題已從「我們能自動化多少」轉變為「人類究竟應該出現在迴路的哪個位置」。本文剖析2026年格局，並給出一套可規模化的監督框架。</p>
<h2 id="理解當前格局">為什麼人在迴路AI在2026年成為董事會級優先事項？</h2>
<p>監管環境自2023年以來顯著收緊。歐盟《人工智慧法案》分階段生效，到2026年，高風險系統的人類監督義務已在實務中產生約束力——包括服務歐盟客戶的亞太企業。新加坡、日本、韓國和澳大利亞的監管機構也相繼發布指引，部分已將AI系統納入現有金融行為監管框架。方向已經明確：人類監督正從自願的最佳實踐轉變為可審計的合規要求。</p>
<p>商業論證同步增強。艾倫·圖靈研究所等機構的研究記錄了過度信任自動化如何產生可預測的失敗——從錯誤的信貸決策到因無人質疑而放行的供應鏈越權操作。產業調查顯示，約70%的企業報告至少有一個AI系統在某種形式的人工審查下運行。我們在客戶工作中看到的模式非常清晰：刻意設計監督機制的企業，其自動化專案才能經受住審計師、董事會和不滿客戶的檢驗。</p>
<h2 id="監管要求2026">2026年的監管要求對人類監督意味著什麼？</h2>
<p>以歐盟AI法案為錨點：高風險系統的營運方必須落實有效監督措施——被指定監督的人需要具備理解模型能力與局限的素養、對自動化偏見保持警覺、能夠在必要時介入或叫停系統，並真正擁有這樣做的權限。這些不再是政策文件裡的措辭，而是審計中逐項核對的證據要求。</p>
<p>落實到操作層面，審計師現在期待四類證據：按風險分層記錄的決策權限文件——誰批准、誰複核、誰升級；帶上下文的人工覆蓋日誌——不僅記錄干預事實，還記錄理由；持續的審查品質證據——複核率、覆蓋率趨勢和抽樣結果；以及迴路中人類的培訓記錄。沒有這些證據的監督，在監管視角下等同於不存在。</p>
<p>亞太企業還需注意域外效力：只要服務歐盟客戶或開展業務，無論總部在哪裡都必須滿足歐盟層面的義務；新加坡金管局等機構則已把AI治理併入現有行為監管框架。務實的做法是按最嚴格的適用標準設計監督架構，而不是按轄區逐套拼接最低標準。</p>
<h2 id="關鍵原則與策略框架">人類監督在哪些環節真正創造價值？</h2>
<p>值得把問題問得更直接，因為一刀切的監督與一刀切的自動化同樣浪費。人在四種情形下創造價值：錯誤決策代價高昂時；支撐決策的資料稀薄或模糊時；決策是新情況而非常規時；以及決策涉及監管或倫理問責時。在高頻、低風險、常規性的決策中，人類只會增加延遲和新錯誤；而在重大決策中移除人類，正是自動化悄然失敗的方式。</p>
<p>2026年的新變化是這一判斷正在被制度化。企業正在構建決策矩陣，把每個自動化決策按風險分層，並為每層指定監督模式——高風險需人工批准、中風險按異常人工複核、低風險無人值守運行。分層是把監督從瓶頸變成控制的關鍵。這一定類工作如今已成為我們客戶設計工作坊的第一項議程，因為後續所有決策——人力配置、工具選型和審計證據——都由此派生。</p>
<h2 id="實施方法與最佳實踐">為什麼人類監督在實務中難以落地？</h2>
<p>第一個挑戰是警示悖論。為標記不確定案例而設計的系統，要麼警示太少——模型在出錯時依然自信——要麼警示太多，讓審核者產生警示疲勞並機械式批准。產業經驗表明，審核者對80%-90%的標記項目未經實質審查即予批准：人類淪為橡皮圖章，審計軌跡形同虛設。</p>
<p>第二個挑戰是問責架構。當沒有人能回答三個問題時，人在迴路就會失效：誰做決定、依據什麼證據、人與系統不一致時怎麼辦。無法回答這些問題的企業會發現監督有名無實。明確決策權並記錄每次覆蓋的理由，是資料治理問題，不是法律形式。</p>
<p>第三個挑戰是規模。人工審查佇列每天處理幾百個決策尚可，但現代自動化每天產生數千個。如果工具不能把正確的上下文呈現給審核者——案例本身、模型推理、相似歷史案例與反事實資訊——監督就會成為限制吞吐量的約束。這正是對話式介面的用武之地：我們看到企業用自然語言查詢在幾秒內調取被標記決策背後的證據，而不是讓審核者從日誌檔案中手工重建。</p>
<p>第四個挑戰是團隊能力。迴路中的審核者往往是領域專家，卻被推入一個需要統計素養的新角色——理解信賴區間、校準度，以及模型誤差與流程差異的區別。提供結構化培訓、決策支援和明確「什麼是好的審查」的組織，監督品質顯著更好；放任審核者自行摸索的組織，得到的就是橡皮圖章。</p>
<h2 id="監督團隊建設">如何組建並培訓迴路中的人類團隊？</h2>
<p>角色設計先於人數。可營運的監督體系通常定義三類角色：一線審核者負責具體決策的批准或否決；升級負責人接手有爭議或超限的案例；監督負責人對整個分層體系的設計與績效負責。人力配置來自吞吐量測算——每天多少決策、平均審查時長、目標複核率——而不是直覺。</p>
<p>培訓要有課程，不能靠傳幫帶。核心模組包括統計素養（信賴度、校準、基率）、常見失效模式（自動化偏見、警示疲勞、定錨效應），以及本域的判例庫——過去哪些案例審錯了、為什麼。領先團隊把審核者培養成懂模型的業務專家，而不是看日誌的操作員，並每年重新認證，因為模型和法規都會漂移。</p>
<p>審核體驗決定審核品質。審核者打開一個案例時，應當一眼看到：案例全貌、模型的結論與理由、相似歷史案例的走向，以及一條用自然語言直接查詢證據的通道。把調取證據的時間從幾十分鐘壓縮到幾秒，是同時提升監督品質和吞吐量的最關鍵投資。</p>
<h2 id="常見陷阱及規避方法">哪些監督實踐方法被證明有效？</h2>
<p>做得好的企業在部署之前、而不是事故之後設計監督。他們先按風險層級分類決策，並在模型上線前為每層定義監督模式、問責歸屬和升級路徑。事前分類成本很低；事故之後追加監督，付出的則是金錢和信任的雙重代價。</p>
<p>其次，他們為迴路裝上儀表。每次人工複核、覆蓋和批准都連同上下文一起記錄，使組織能衡量監督在創造價值還是流於形式。指標在這裡至關重要：覆蓋率應按趨勢監控——持續下降的覆蓋率既可能意味著模型在變好，也可能意味著審核者在敷衍。監管者越來越期待看到恰恰是這類證據。</p>
<p>第三，用升級設計取代警示數量。成熟方案不把每個邊界案例都推給人類，而是按嚴重程度和上下文分流：常規異常自動處理並通知；模糊案例連同決策支援摘要交給審核者；高後果案例要求具名負責人的書面批准。2026年的前沿已經從「人在迴路中」演進到「在正確的時刻處於迴路之上」。</p>
<p>第四，像測試模型一樣測試迴路。對抗性測試——故意投餵邊界案例，觀察是否在正確的時間把正確的審核者拉進來——能暴露準確率指標掩蓋的缺口。我們建議企業把監督設計納入模型評估記分卡，因為準確率99%但100%無人監督的模型，仍然是負債。</p>
<h2 id="衡量成功與展示投資回報率">什麼情況下自動化可以無需人工審查？</h2>
<p>四個條件同時滿足時，無人值守是合理選擇：錯誤決策的影響小且可逆；決策量大到人工複核不經濟；模型在相關分佈上經過充分校準並有漂移監控；存在自動化的兜底機制——出問題時能快速回滾或降級到人工流程。</p>
<p>即便無人值守，審計不能缺席。領先團隊對無人值守決策做週期性抽樣複核——抽樣比例隨風險水平調整——並保留一鍵降級能力：當漂移監控觸發閾值時，系統自動切回異常複核模式。信任不是系統的一個開關設置，而是用證據持續贏取的屬性。</p>
<p>成熟度路徑也印證了這一點。幾乎沒有企業一開始就讓高風險決策無人值守；他們從全面人工監督起步，用覆蓋率和抽樣審計的資料證明模型值得更大自主權，再逐層放寬。自主權是掙來的，不是配置出來的。</p>
<h2 id="規模化營運模型">可規模化的監督營運模型是什麼樣的？</h2>
<p>一套實用的營運模型可以歸納為少數幾條規則：高風險決策需人工批准並記錄理由；中風險決策按異常複核並附帶決策支援摘要；低風險決策無人值守並做週期性抽樣審計。每一層都被記錄、度量，並按月向問責負責人彙報。營運模型清單如下：</p>
<ol>
<li>部署前按風險層級對每個自動化決策分類。</li>
<li>為每層指定具名問責負責人，並預先定義升級路徑。</li>
<li>連同上下文和理由記錄每次複核、覆蓋與批准。</li>
<li>把覆蓋率和審查時延作為一等營運指標監控。</li>
<li>用對抗性測試案例週期性審計迴路，而不只看生產統計。</li>
</ol>
<h2 id="關鍵要點">2026年的關鍵要點是什麼？</h2>
<ul>
<li>人類監督是2026年的監管與聲譽要求，不是設計上的點綴。</li>
<li>人工審查只在明確的節點創造價值——高後果、薄資料、新情況與問責環節。</li>
<li>風險分層監督（批准、複核、無人值守）勝過一刀切的人工審查。</li>
<li>為迴路裝上儀表：記錄決策、監控覆蓋率趨勢、用對抗性案例審計。</li>
<li>對話式分析工具讓審核者秒級調取決策證據，使監督與吞吐量兼容。</li>
</ul>
<h2 id="結論">為什麼監督仍是決定性因素？</h2>
<p>2026年的人在迴路AI，與其說是對人類的哲學承諾，不如說是嚴謹的系統設計。勝出的企業將監督視為一等公民——像其他控制項一樣被工程化、度量和審計。蜂啟諮詢幫助亞太地區的組織構建的正是這一點：有治理的對話式分析，在人們已經在用的工具裡、在決策需要的那一刻，呈現人類需要的證據。自動化是引擎，監督是方向盤——兩者都必須被設計，而且要一起設計。</p>
'''
TW_TOC = [
    ("理解當前格局", "為什麼人在迴路AI在2026年成為董事會級優先事項？"),
    ("監管要求2026", "2026年的監管要求對人類監督意味著什麼？"),
    ("關鍵原則與策略框架", "人類監督在哪些環節真正創造價值？"),
    ("實施方法與最佳實踐", "為什麼人類監督在實務中難以落地？"),
    ("監督團隊建設", "如何組建並培訓迴路中的人類團隊？"),
    ("常見陷阱及規避方法", "哪些監督實踐方法被證明有效？"),
    ("衡量成功與展示投資回報率", "什麼情況下自動化可以無需人工審查？"),
    ("規模化營運模型", "可規模化的監督營運模型是什麼樣的？"),
    ("關鍵要點", "2026年的關鍵要點是什麼？"),
    ("結論", "為什麼監督仍是決定性因素？"),
]

def process_tw():
    s = load(ZHTW)
    assert '人在迴路' in body_h1(s), "wrong file"
    if '為什麼人在迴路AI在2026年成為董事會級優先事項' in s:
        print("zh-TW already processed, skip"); return
    m = re.search(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")', s, re.S)
    assert m, "tw body anchor not found"
    body = TW_BODY + faq_block(TW_FAQ, "常見問題")
    s = s[:m.start()] + body + s[m.end():]
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in TW_TOC)
    side = "\n".join(f'                    <a href="#{i}" class="toc-link">{t}</a>' for i, t in TW_TOC)
    s = re.sub(r'<div class="toc-mobile-links">.*?</div>', lambda m: '<div class="toc-mobile-links">\n' + mob + '\n                </div>', s, count=1, flags=re.S)
    s = re.sub(r'<nav class="toc-links">.*?</nav>', lambda m: '<nav class="toc-links">\n' + side + '\n                </nav>', s, count=1, flags=re.S)
    s = fill_excerpts(s, ["資料質量自動化讓資料治理從被動補救轉為主動預防。"], "TW-excerpt")
    integrity(s, [
        '?v=20260901', '預約示範', '"@type": "FAQPage"',
        '為什麼人在迴路AI在2026年成為董事會級優先事項',
        '可規模化的監督營運模型',
    ], 11, "zh-TW")
    assert s.count('class="faq-item"') == 4
    save(ZHTW, s)
    print("zh-TW done")

process_en()
process_cn()
process_tw()
print("SLUG 3 COMPLETE")
