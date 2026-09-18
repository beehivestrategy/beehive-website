# -*- coding: utf-8 -*-
"""Slug 9: building-an-ai-ready-workforce-training-vs-hiring-part-2 — EN expand + H2 interrogative + FAQ rebuild; zh targeted expansion."""
import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/tmp")
from common import (load, save, rep1, re_dl, build_faq_list, build_jsonld,
                    body_h1, fill_excerpts, integrity, FAQ_RX, JSONLD_RX)

W = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/"
EN = W + "blog/articles/building-an-ai-ready-workforce-training-vs-hiring-part-2.html"
ZHCN = W + "zh-cn/blog/articles/building-an-ai-ready-workforce-training-vs-hiring-part-2.html"
ZHTW = W + "zh-tw/blog/articles/building-an-ai-ready-workforce-training-vs-hiring-part-2.html"

# ---------------- EN ----------------
EN_FAQ = [
    ("What is the right split between training and hiring for AI talent?",
     "The emerging standard across our client engagements is a 60/40 split: 60-70% of the AI talent budget to upskilling existing staff in data literacy, prompt engineering, and analytics interpretation, and 30-40% to strategic external hires in deep technical specializations like MLOps and data engineering. Upskilling a mid-level analyst costs USD 18,000-32,000 over 12 months, while external hiring commands a 35-60% salary premium plus roughly 25% in first-year recruitment and onboarding costs — and the workforce you train is the workforce you keep."),
    ("When should an enterprise hire AI talent externally instead of upskilling?",
     "Hire externally when the skill is scarce, the timeline is short, and the knowledge cannot be built quickly. Three situations dominate: standing up a new capability with no internal base, where three senior specialists beat training twelve people over eighteen months; time-critical work where a regulatory deadline or product launch depends on the capability; and benchmark-setting roles, where someone who has built this exact thing before can teach the internal team while building it. Hire for scarcity and speed; train for scale and continuity."),
    ("How do you keep AI talent from leaving?",
     "Address three dimensions at once. Intellectual retention: put top performers on genuinely challenging, high-impact projects and rotate them across business units. Financial retention: tie AI-specific equity or bonuses to model performance and business outcomes — one manufacturer's model royalty scheme cut team attrition by 60% in a year. Cultural retention: leaders must actually act on data, because AI talent disengages rapidly where managers override model recommendations with intuition. Financial incentives alone are a race you cannot win — PwC finds AI skills command wage premiums of up to 25%."),
    ("How long does it take to upskill an employee to AI competency?",
     "Benchmark data across Asia-Pacific enterprises shows upskilling a mid-level analyst to AI competency costs USD 18,000-32,000 over 12 months, including courses, certification, mentoring, and lost productivity during the learning curve. Completion and transfer depend on program design: organizations that ring-fence 20% of working hours for structured learning achieve 90%+ completion, while those that treat participation as discretionary see 70% dropout. Competency gates — building and deploying a model that passes peer review — matter more than course certificates."),
]

EN_TOC = [
    ("the-economics-of-build-versus-buy-talent", "What Are the Economics of Building Versus Buying AI Talent?"),
    ("when-should-you-hire-instead-of-train", "When Should You Hire Instead of Train?"),
    ("structuring-internal-ai-academies-that-deliver", "How Do You Structure an Internal AI Academy That Delivers?"),
    ("retention-strategies-in-a-hyper-competitive-market", "Which Retention Strategies Work in a Hyper-Competitive Market?"),
    ("measuring-workforce-ai-readiness-maturity", "How Do You Measure Workforce AI Readiness Maturity?"),
    ("key-takeaways", "What Are the Key Takeaways on Training Versus Hiring?"),
    ("conclusion", "Why Does the Training Versus Hiring Decision Define AI Program Success?"),
]

EN_PARA_M = '''<p>Measurement cadence matters as much as the metrics themselves. Quarterly re-measurement against the baseline keeps the four dimensions honest, and benchmarking against industry peers keeps the targets ambitious: the enterprises that progress fastest publish their maturity scores internally, tie academy funding to movement in the scores, and review the numbers with the same discipline they apply to revenue metrics. The measurement loop also closes the build-versus-buy decision. If technical competency is rising but applied execution stays flat, the gap is usually tooling or data access rather than training — and adding another course will not close it. If applied execution is strong but cultural indicators lag, leaders are overriding the outputs, and the organization reads that signal quickly. Reading the four dimensions together tells you whether the next dollar belongs to the academy, the platform, or the retention program — which is how talent budgets, like the talent itself, stay aligned with outcomes.</p>'''

def process_en():
    s = load(EN)
    h1 = body_h1(s)
    assert "Workforce" in h1, "wrong file? h1=" + h1
    if 'What Are the Economics of Building Versus Buying AI Talent?' in s:
        print("EN already processed, skip")
        return
    # 1) H2 interrogative conversions (keep ids)
    s = rep1(s, '<h2 id="the-economics-of-build-versus-buy-talent">The Economics of Build Versus Buy Talent</h2>',
             '<h2 id="the-economics-of-build-versus-buy-talent">What Are the Economics of Building Versus Buying AI Talent?</h2>', 'h2-1')
    s = rep1(s, '<h2 id="structuring-internal-ai-academies-that-deliver">Structuring Internal AI Academies That Deliver</h2>',
             '<h2 id="structuring-internal-ai-academies-that-deliver">How Do You Structure an Internal AI Academy That Delivers?</h2>', 'h2-2')
    s = rep1(s, '<h2 id="retention-strategies-in-a-hyper-competitive-market">Retention Strategies in a Hyper-Competitive Market</h2>',
             '<h2 id="retention-strategies-in-a-hyper-competitive-market">Which Retention Strategies Work in a Hyper-Competitive Market?</h2>', 'h2-3')
    s = rep1(s, '<h2 id="measuring-workforce-ai-readiness-maturity">Measuring Workforce AI Readiness Maturity</h2>',
             '<h2 id="measuring-workforce-ai-readiness-maturity">How Do You Measure Workforce AI Readiness Maturity?</h2>', 'h2-4')
    s = rep1(s, '<h2 id="key-takeaways">Key Takeaways</h2>',
             '<h2 id="key-takeaways">What Are the Key Takeaways on Training Versus Hiring?</h2>', 'h2-5')
    s = rep1(s, '<h2 id="conclusion">Conclusion</h2>',
             '<h2 id="conclusion">Why Does the Training Versus Hiring Decision Define AI Program Success?</h2>', 'h2-6')
    # 2) append paragraph (word count floor)
    anchor_m = 'none of it matters if it does not move outcomes.</p>'
    assert s.count(anchor_m) == 1
    s = s.replace(anchor_m, anchor_m + '\n' + EN_PARA_M)
    # 3) remove head FAQPage
    s = re_dl(s, JSONLD_RX, '', 'head-faqpage-remove')
    # 4) rebuild FAQ list (h3-wrapped, topical)
    new_faq = '<div class="faq-list">\n' + build_faq_list(EN_FAQ) + '\n                </div>\n            </section>'
    s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'faq-list')
    old_nav = '</section>\n\n            <nav class="article-nav"'
    assert s.count(old_nav) == 1
    s = s.replace(old_nav, '</section>\n' + build_jsonld(EN_FAQ) + '\n\n            <nav class="article-nav"')
    # 5) TOC sync
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in EN_TOC)
    s = re_dl(s, r'<div class="toc-mobile-links">.*?</div>', '<div class="toc-mobile-links">\n' + mob + '\n                </div>', 'toc-mobile')
    # 6) excerpts
    s = fill_excerpts(s, [
        "How inclusive data teams catch the blind spots homogeneous hiring misses.",
        "Where the AI agent layer fits in a modern data strategy — and what to build first.",
        "A practical 2026 guide to vector databases and enterprise semantic search.",
    ], "EN-excerpt")
    integrity(s, [
        '?v=20260901', '"@type": "BlogPosting"', '"@type": "BreadcrumbList"',
        'id="when-should-you-hire-instead-of-train"',
        'id="measuring-workforce-ai-readiness-maturity"',
        'What Are the Key Takeaways on Training Versus Hiring?',
        '"@type": "FAQPage"', 'Book a Demo',
    ], 7, "EN")
    assert "Workforce" in body_h1(s)
    assert s[:s.index('</head>')].count('FAQPage') == 0
    save(EN, s)
    print("EN done")

# ---------------- zh-CN ----------------
CN_FAQ = [
    ("培训和招聘AI人才的最佳预算分配比例是多少？",
     "我们客户实践中浮现的标准是60/40分配：将AI人才预算的60%-70%用于提升现有员工的数据素养、提示工程和数据分析解读能力，30%-40%用于MLOps、数据工程等深度技术领域的战略性外部招聘。把一名中级分析师培养至AI胜任水平12个月成本为18,000-32,000美元，而外部招聘需支付35%-60%的薪资溢价、第一年再增加约25%的招聘与入职成本——而且你培训出的队伍才是你留得住的队伍。"),
    ("什么情况下应该外部招聘而不是内部培养？",
     "当技能稀缺、时间紧迫、且知识无法快速内建时，选择外部招聘。三种情形最典型：从零建立一项新能力，招聘三名资深专家胜过花十八个月培养十二个人；监管截止日期或产品发布取决于这项能力的时间刚性工作；以及标杆设定者岗位——一个亲手做过这件事、并能在建设过程中教会内部团队的人。为稀缺和速度而招聘；为规模和延续而培养。"),
    ("留住AI人才最有效的方法是什么？",
     "同时着手三个维度。智力留才：让顶尖人才持续接触真正具有挑战性、高影响力的项目，并通过轮岗跨部门流动。财务留才：把AI专项股权或奖金与模型性能和业务成果挂钩——一家制造业客户的模型版税计划让团队离职率一年内下降60%。文化留才：领导者必须真正基于数据行动，因为当管理者用直觉推翻模型建议时，AI人才会迅速失去热情。单靠财务激励赢不了——普华永道发现AI技能的工资溢价高达25%。"),
    ("将一名员工培养至AI胜任水平需要多长时间？",
     "亚太企业的基准数据显示，将一名中级分析师培养至AI胜任水平，12个月内的成本为18,000-32,000美元，包括课程、认证、导师指导和学习曲线期间损失的生产力。完成率与技能转移取决于项目设计：为结构化学习预留20%工作时间的组织完成率超过90%，而把参与当作可选活动的组织流失率高达70%。能力门槛——构建并部署一个通过同行评审的模型——比课程结业证书更重要。"),
]

CN_TOC = [
    ("培养与招聘的经济学分析", "培养与购买AI人才的经济学账怎么算？"),
    ("何时应该选择外部招聘", "何时应该选择外部招聘而非内部培养？"),
    ("构建高效的内部ai学院", "如何构建能真正交付成果的内部AI学院？"),
    ("激烈竞争市场中的留才策略", "激烈竞争中哪些留才策略真正有效？"),
    ("衡量人才队伍的ai就绪成熟度", "如何衡量人才队伍的AI就绪成熟度？"),
    ("核心要点", "关于培养与招聘的核心要点有哪些？"),
    ("结论", "为什么培养与招聘的决策决定AI项目成败？"),
]

CN_NEWSEC = '''<h2 id="何时应该选择外部招聘">何时应该选择外部招聘而非内部培养？</h2>
<p>当技能稀缺、时间紧迫、且知识无法快速内建时，选择外部招聘。三种情形最典型。第一，当你从零建立一项新能力——第一支MLOps团队、数据工程职能、平台团队——招聘三名资深专家，胜过花十八个月培养十二个人。第二，当工作具有时间刚性且市场窗口真实存在：如果监管截止日期或产品发布取决于这项能力，35%-60%的溢价买到的是你没有的几个月时间。第三，当你需要一个标杆设定者——一个亲手做过这件事、并能在建设过程中教会内部团队的人。企业常犯的错误，是为现有员工通过12个月、18,000-32,000美元培养路径就能胜任的岗位支付外部溢价，然后眼看着新员工两年后离职，因为领域背景从未真正转移。为稀缺和速度而招聘；为规模和延续而培养。</p>
<p>另一个招聘与培养的触发器是留才算术。如果你留不住现有的人——而AI人才流失正是企业AI项目的隐形杀手——每一分培训投入都会从大门流失。正如前文数据所示，AI员工流失率高于中位数的企业，生产部署周期要长40%，知识流失事件高出3倍。在扩大任何学院规模之前，先修复留才问题；否则你培养的，是竞争对手未来的员工。</p>'''

CN_P_ECO = '''<p>宏观语境为这一决策增加了紧迫性。世界经济论坛《2025年未来就业报告》显示：70%的企业预期AI将变革其业务，六成劳动者需要在2030年之前接受再培训，但当前只有一半劳动者能够获得足够的培训机会。企业面对的不是"培训还是招聘"的选择题，而是如何在大限之前同时做好两者的执行题。LinkedIn《2025年职场学习报告》的发现同样关键：当今工作中用到的技能约有70%将在2030年前发生改变——这意味着你培训出的队伍，才是你留得住的队伍。</p>'''

CN_P_RET = '''<p>薪资压力数据强化了三个维度并重的原因。普华永道AI就业晴雨表发现，拥有热门AI技能的劳动者可享受最高25%的工资溢价——单靠财务激励，你无法在每一个出价者面前赢得竞争。你能赢得的是组合拳：有竞争力的薪酬、智力上严肃的工作、以及一个真正基于数据行动的文化。正是这个组合，让留才对话围绕工作本身展开，而不是围绕offer展开。</p>'''

CN_P_MET = '''<p>衡量的节奏与指标本身同等重要。每季度对照基线复测，让四个维度保持诚实；对照行业同侪对标，让目标保持进取。行动最快的企业将成熟度评分在内部公开、把学院预算与评分变化挂钩、并以对待收入指标同样的纪律审视这些数字。衡量闭环也回答了培养与招聘的取舍：如果技术能力在上升而实践执行停滞，缺口通常在工具或数据权限而非培训——再加一门课也无法弥合。把四个维度放在一起读，就能判断下一笔预算该投向学院、平台还是留才计划。</p>'''

CN_P_CONC = '''<p>同样的纪律也延伸到团队使用的工具：当分析能力以托管对话式BI服务的形态交付——约两周上线、无需重建数据仓库——员工队伍的AI素养就会转化为日常实践。人们在聊天中提问、获得有出处的答案，积累起任何单一培训课程都无法提供的肌肉记忆。人才战略与平台战略是同一个战略，把两者当作一件事来做的企业，两年后依然拥有最好的人才——和最好的答案。</p>'''

def process_cn():
    s = load(ZHCN)
    h1 = body_h1(s)
    assert '人才' in h1, "wrong file? h1=" + h1
    if 'id="何时应该选择外部招聘"' in s:
        print("CN already processed, skip")
        return
    # 1) H2 interrogative conversions (keep ids)
    s = rep1(s, '<h2 id="培养与招聘的经济学分析">培养与招聘的经济学分析</h2>',
             '<h2 id="培养与招聘的经济学分析">培养与购买AI人才的经济学账怎么算？</h2>', 'cn-h2-1')
    s = rep1(s, '<h2 id="构建高效的内部ai学院">构建高效的内部AI学院</h2>',
             '<h2 id="构建高效的内部ai学院">如何构建能真正交付成果的内部AI学院？</h2>', 'cn-h2-2')
    s = rep1(s, '<h2 id="激烈竞争市场中的留才策略">激烈竞争市场中的留才策略</h2>',
             '<h2 id="激烈竞争市场中的留才策略">激烈竞争中哪些留才策略真正有效？</h2>', 'cn-h2-3')
    s = rep1(s, '<h2 id="衡量人才队伍的ai就绪成熟度">衡量人才队伍的AI就绪成熟度</h2>',
             '<h2 id="衡量人才队伍的ai就绪成熟度">如何衡量人才队伍的AI就绪成熟度？</h2>', 'cn-h2-4')
    s = rep1(s, '<h2 id="核心要点">核心要点</h2>',
             '<h2 id="核心要点">关于培养与招聘的核心要点有哪些？</h2>', 'cn-h2-5')
    s = rep1(s, '<h2 id="结论">结论</h2>',
             '<h2 id="结论">为什么培养与招聘的决策决定AI项目成败？</h2>', 'cn-h2-6')
    # 2) new section + appended paragraphs
    a1 = '这一比例在成本效率和能力广度之间实现了最佳平衡。</p>'
    assert s.count(a1) == 1
    s = s.replace(a1, a1 + '\n' + CN_P_ECO)
    s = rep1(s, '<h2 id="构建高效的内部ai学院">', CN_NEWSEC + '\n<h2 id="构建高效的内部ai学院">', 'cn-newsec')
    a2 = '能够以显著更高的比例留住人才。</p>'
    assert s.count(a2) == 1
    s = s.replace(a2, a2 + '\n' + CN_P_RET)
    a3 = '就能转化为可衡量的生产力或质量提升。</p>'
    assert s.count(a3) == 1
    s = s.replace(a3, a3 + '\n' + CN_P_MET)
    a4 = '并与业务成果紧密耦合。</p>'
    assert s.count(a4) == 1
    s = s.replace(a4, a4 + '\n' + CN_P_CONC)
    # 3) rebuild FAQ (remove old body FAQPage first, then insert new faq + JSON-LD)
    s = re_dl(s, JSONLD_RX, '', 'cn-body-faqpage-remove')
    new_faq = ('<div class="faq-list">\n' + build_faq_list(CN_FAQ) +
               '\n                </div>\n            </section>\n' + build_jsonld(CN_FAQ))
    s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'cn-faq-list')
    # 4) TOC sync
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{t}</a>' for o, t in CN_TOC)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
    assert s2 != s, "cn toc replace failed"
    s = s2
    # 5) excerpts
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "数据质量自动化让数据治理从被动补救转向主动预防。",
        ], "CN-excerpt")
    integrity(s, [
        '?v=20260901', '预约演示', '"@type": "FAQPage"',
        'id="何时应该选择外部招聘"', 'id="构建高效的内部ai学院"',
        '18,000-32,000美元', '60/40', '对话式BI',
    ], 7, "zh-CN")
    assert '人才' in body_h1(s)
    save(ZHCN, s)
    print("CN done")

# ---------------- zh-TW ----------------
TW_FAQ = [
    ("培訓和招聘AI人才的最佳預算分配比例是多少？",
     "我們客戶實踐中浮現的標準是60/40分配：將AI人才預算的60%-70%用於提升現有員工的資料素養、提示工程和資料分析解讀能力，30%-40%用於MLOps、資料工程等深度技術領域的戰略性外部招聘。把一名中級分析師培養至AI勝任水平12個月成本為18,000-32,000美元，而外部招聘需支付35%-60%的薪資溢價、第一年再增加約25%的招聘與入職成本——而且你培訓出的隊伍才是你留得住的隊伍。"),
    ("什麼情況下應該外部招聘而不是內部培養？",
     "當技能稀缺、時間緊迫、且知識無法快速內建時，選擇外部招聘。三種情形最典型：從零建立一項新能力，招聘三名資深專家勝過花十八個月培養十二個人；監管截止日期或產品發布取決於這項能力的時間剛性工作；以及標杆設定者崗位——一個親手做過這件事、並能在建設過程中教會內部團隊的人。為稀缺和速度而招聘；為規模和延續而培養。"),
    ("留住AI人才最有效的方法是什麼？",
     "同時著手三個維度。智力留才：讓頂尖人才持續接觸真正具有挑戰性、高影響力的項目，並通過輪崗跨部門流動。財務留才：把AI專項股權或獎金與模型性能和業務成果掛鉤——一家製造業客戶的模型版稅計劃讓團隊離職率一年內下降60%。文化留才：領導者必須真正基於資料行動，因為當管理者用直覺推翻模型建議時，AI人才會迅速失去熱情。單靠財務激勵贏不了——資誠（PwC）發現AI技能的薪資溢價高達25%。"),
    ("將一名員工培養至AI勝任水平需要多長時間？",
     "亞太企業的基準數據顯示，將一名中級分析師培養至AI勝任水平，12個月內的成本為18,000-32,000美元，包括課程、認證、導師指導和學習曲線期間損失的生產力。完成率與技能轉移取決於專案設計：為結構化學習預留20%工作時間的組織完成率超過90%，而把參與當作可選活動的組織流失率高達70%。能力門檻——構建並部署一個通過同儕審查的模型——比課程結業證書更重要。"),
]

TW_TOC = [
    ("培養與招聘的經濟學分析", "培養與購買AI人才的經濟學帳怎麼算？"),
    ("何時應該選擇外部招聘", "何時應該選擇外部招聘而非內部培養？"),
    ("構建高效的內部ai學院", "如何構建能真正交付成果的內部AI學院？"),
    ("激烈競爭市場中的留才策略", "激烈競爭中哪些留才策略真正有效？"),
    ("衡量人才隊伍的ai就緒成熟度", "如何衡量人才隊伍的AI就緒成熟度？"),
    ("核心要點", "關於培養與招聘的核心要點有哪些？"),
    ("結論", "為什麼培養與招聘的決策決定AI專案成敗？"),
]

TW_NEWSEC = '''<h2 id="何時應該選擇外部招聘">何時應該選擇外部招聘而非內部培養？</h2>
<p>當技能稀缺、時間緊迫、且知識無法快速內建時，選擇外部招聘。三種情形最典型。第一，當你從零建立一項新能力——第一支MLOps團隊、資料工程職能、平台團隊——招聘三名資深專家，勝過花十八個月培養十二個人。第二，當工作具有時間剛性且市場窗口真實存在：如果監管截止日期或產品發布取決於這項能力，35%-60%的溢價買到的是你沒有的幾個月時間。第三，當你需要一個標杆設定者——一個親手做過這件事、並能在建設過程中教會內部團隊的人。企業常犯的錯誤，是為現有員工通過12個月、18,000-32,000美元培養路徑就能勝任的崗位支付外部溢價，然後眼看著新員工兩年後離職，因為領域背景從未真正轉移。為稀缺和速度而招聘；為規模和延續而培養。</p>
<p>另一個招聘與培養的觸發器是留才算術。如果你留不住現有的人——而AI人才流失正是企業AI專案的隱形殺手——每一分培訓投入都會從大門流失。正如前文數據所示，AI員工流失率高於中位數的企業，生產部署週期要長40%，知識流失事件高出3倍。在擴大任何學院規模之前，先修復留才問題；否則你培養的，是競爭對手未來的員工。</p>'''

TW_P_ECO = '''<p>宏觀語境為這一決策增加了緊迫性。世界經濟論壇《2025年未來就業報告》顯示：70%的企業預期AI將變革其業務，六成勞動者需要在2030年之前接受再培訓，但當前只有一半勞動者能夠獲得足夠的培訓機會。企業面對的不是「培訓還是招聘」的選擇題，而是如何在大限之前同時做好兩者的執行題。LinkedIn《2025年職場學習報告》的發現同樣關鍵：當今工作中用到的技能約有70%將在2030年前發生改變——這意味著你培訓出的隊伍，才是你留得住的隊伍。</p>'''

TW_P_RET = '''<p>薪資壓力數據強化了三個維度並重的原因。資誠（PwC）AI就業晴雨表發現，擁有熱門AI技能的勞動者可享受最高25%的工資溢價——單靠財務激勵，你無法在每一個出價者面前贏得競爭。你能贏得的是組合拳：有競爭力的薪酬、智力上嚴肅的工作、以及一個真正基於資料行動的文化。正是這個組合，讓留才對話圍繞工作本身展開，而不是圍繞offer展開。</p>'''

TW_P_MET = '''<p>衡量的節奏與指標本身同等重要。每季度對照基線複測，讓四個維度保持誠實；對照行業同儕對標，讓目標保持進取。行動最快的企業將成熟度評分在內部公開、把學院預算與評分變化掛鉤、並以對待收入指標同樣的紀律審視這些數字。衡量閉環也回答了培養與招聘的取捨：如果技術能力在上升而實踐執行停滯，缺口通常在工具或資料權限而非培訓——再加一門課也無法彌合。把四個維度放在一起讀，就能判斷下一筆預算該投向學院、平台還是留才計劃。</p>'''

TW_P_CONC = '''<p>同樣的紀律也延伸到團隊使用的工具：當分析能力以託管對話式BI服務的形態交付——約兩週上線、無需重建資料倉儲——員工隊伍的AI素養就會轉化為日常實踐。人們在聊天中提問、獲得有出處的答案，積累起任何單一培訓課程都無法提供的肌肉記憶。人才戰略與平台戰略是同一個戰略，把兩者當作一件事來做的企業，兩年後依然擁有最好的人才——和最好的答案。</p>'''

def process_tw():
    s = load(ZHTW)
    h1 = body_h1(s)
    assert '人才' in h1, "wrong file? h1=" + h1
    if 'id="何時應該選擇外部招聘"' in s:
        print("TW already processed, skip")
        return
    # 1) H2 interrogative conversions (keep ids)
    s = rep1(s, '<h2 id="培養與招聘的經濟學分析">培養與招聘的經濟學分析</h2>',
             '<h2 id="培養與招聘的經濟學分析">培養與購買AI人才的經濟學帳怎麼算？</h2>', 'tw-h2-1')
    s = rep1(s, '<h2 id="構建高效的內部ai學院">構建高效的內部AI學院</h2>',
             '<h2 id="構建高效的內部ai學院">如何構建能真正交付成果的內部AI學院？</h2>', 'tw-h2-2')
    s = rep1(s, '<h2 id="激烈競爭市場中的留才策略">激烈競爭市場中的留才策略</h2>',
             '<h2 id="激烈競爭市場中的留才策略">激烈競爭中哪些留才策略真正有效？</h2>', 'tw-h2-3')
    s = rep1(s, '<h2 id="衡量人才隊伍的ai就緒成熟度">衡量人才隊伍的AI就緒成熟度</h2>',
             '<h2 id="衡量人才隊伍的ai就緒成熟度">如何衡量人才隊伍的AI就緒成熟度？</h2>', 'tw-h2-4')
    s = rep1(s, '<h2 id="核心要點">核心要點</h2>',
             '<h2 id="核心要點">關於培養與招聘的核心要點有哪些？</h2>', 'tw-h2-5')
    s = rep1(s, '<h2 id="結論">結論</h2>',
             '<h2 id="結論">為什麼培養與招聘的決策決定AI專案成敗？</h2>', 'tw-h2-6')
    # 2) new section + appended paragraphs
    a1 = '這一比例在成本效率和能力廣度之間實現了最佳平衡。</p>'
    assert s.count(a1) == 1
    s = s.replace(a1, a1 + '\n' + TW_P_ECO)
    s = rep1(s, '<h2 id="構建高效的內部ai學院">', TW_NEWSEC + '\n<h2 id="構建高效的內部ai學院">', 'tw-newsec')
    a2 = '能夠以顯著更高的比例留住人才。</p>'
    assert s.count(a2) == 1
    s = s.replace(a2, a2 + '\n' + TW_P_RET)
    a3 = '就能轉化為可衡量的生產力或質量提升。</p>'
    assert s.count(a3) == 1
    s = s.replace(a3, a3 + '\n' + TW_P_MET)
    a4 = '並與業務成果緊密耦合。</p>'
    assert s.count(a4) == 1
    s = s.replace(a4, a4 + '\n' + TW_P_CONC)
    # 3) rebuild FAQ (remove old body FAQPage first, then insert new faq + JSON-LD)
    s = re_dl(s, JSONLD_RX, '', 'tw-body-faqpage-remove')
    new_faq = ('<div class="faq-list">\n' + build_faq_list(TW_FAQ) +
               '\n                </div>\n            </section>\n' + build_jsonld(TW_FAQ))
    s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'tw-faq-list')
    # 4) TOC sync
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{t}</a>' for o, t in TW_TOC)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
    assert s2 != s, "tw toc replace failed"
    s = s2
    # 5) excerpts
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "資料品質自動化讓資料治理從被動補救轉向主動預防。",
        ], "TW-excerpt")
    integrity(s, [
        '?v=20260901', '預約示範', '"@type": "FAQPage"',
        'id="何時應該選擇外部招聘"', 'id="構建高效的內部ai學院"',
        '18,000-32,000美元', '60/40', '對話式BI',
    ], 7, "zh-TW")
    assert '人才' in body_h1(s)
    save(ZHTW, s)
    print("TW done")

if __name__ == "__main__":
    process_en()
    process_cn()
    process_tw()
    print("ALL DONE")
