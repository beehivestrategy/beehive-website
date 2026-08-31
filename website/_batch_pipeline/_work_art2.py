# -*- coding: utf-8 -*-
import re, os, json
import opencc
cc = opencc.OpenCC('s2twp')
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = "data-lineage-tracking-for-regulatory-compliance"

# ---------- EN extra sections (question-style H2s) ----------
en_extra = '''
<h2 id="how-do-you-choose-a-lineage-tool-without-creating-another-silo">How Do You Choose a Lineage Tool Without Creating Another Silo?</h2>
<p>The lineage market is crowded with catalogue tools, transformation engines that ship their own lineage, and point solutions that only understand one platform. The mistake enterprises make is buying a separate lineage tool for each domain, which produces several partial maps that cannot be joined. The durable pattern is to treat lineage as a single governed asset with open ingestion: one store that accepts metadata from warehouses, lakes, orchestration tools, and notebooks alike. The tool that captures the most automated metadata is less important than the discipline of consolidating it.</p>
<p>In practice, prefer tooling that parses SQL and reads execution logs over tooling that depends on engineers annotating pipelines. The former keeps current as systems change; the latter decays the moment a pipeline is edited without a corresponding documentation update. When evaluating vendors, ask for a live demonstration of column-level lineage on a messy, real table — not a polished sample — because that is the scenario audits actually test.</p>
<h2 id="what-does-audit-ready-lineage-look-like-in-practice">What Does Audit-Ready Lineage Look Like in Practice?</h2>
<p>A regional bank we worked with treated its regulatory reports as a black box: a number on a dashboard with no traceable path back to source. After a regulator questioned one capital figure, the team spent eleven days reconstructing the logic by hand. We automated capture across ingestion, transformation, and reporting, then annotated the lineage graph with business terms and data-subject categories. The next time the same question arrived, the steward produced the full source-to-report graph in under three hours, with every transformation, owner, and sensitivity flag visible. The programme moved from archaeology to routine.</p>
<p>The lesson generalises: audit-readiness is not a property of the reports, it is a property of the system that produces them. If a demonstration requires manual work, the programme is not ready; if it requires a live query against governed lineage, it is.</p>
<h2 id="how-does-lineage-connect-to-ai-governance">How Does Lineage Connect to AI Governance?</h2>
<p>As enterprises deploy more models, lineage stops being only about reports and becomes about model inputs. A model is only as defensible as the data that trained and fed it; when a regulator or stakeholder asks why a model made a decision, the answer requires tracing features back to their sources. Lineage that covers both analytical reports and model feature pipelines lets an organisation answer "where did this training signal come from?" with the same evidence it uses for financial reporting.</p>
<p>This convergence is why we recommend a single lineage store that spans business intelligence and machine learning. It turns governance from a separate compliance exercise into one continuous record of how data becomes decisions — which is exactly what modern AI regulation increasingly expects.</p>
'''

# ---------- FAQ content per language ----------
en_faq = [
 ("What is data lineage and why does it matter for regulatory compliance?",
  "Data lineage is the automated, end-to-end record of how data moves, transforms, and is used across an enterprise. Regulators in banking, insurance, healthcare, and beyond now require organisations to show where a reported figure came from and how it was transformed. Without lineage, an enterprise cannot answer an auditor's questions, and it risks fines and reputational damage when those questions arrive unexpectedly."),
 ("Should lineage be table-level or column-level?",
  "Column-level lineage is what regulators increasingly expect. Table-level lineage tells you which table produced another table, but it cannot answer which specific column drove a value, which is what impact analysis, data-mapping audits, and data-subject access requests require. Capturing column-level lineage automatically is harder, but it is the difference between a lineage graph engineers can use and one compliance teams can act on."),
 ("How do you make lineage audit-ready without a massive manual project?",
  "Automate capture at every stage where data moves — parsing SQL, instrumenting transformation engines, and reading execution logs — rather than asking engineers to document pipelines by hand. Then annotate the graph with business terms, owners, and sensitivity classifications, reconcile it against execution logs to maintain trust, and rehearse regulator demonstrations on a regular cadence so the process becomes routine rather than a fire drill."),
 ("Does data lineage only help with compliance?",
  "No. Lineage pays for itself operationally through impact analysis: when a source schema changes or a vendor retires a feed, lineage shows every downstream report, model, and dashboard affected, turning a potential incident into a planned migration. Organisations that prioritise by regulatory exposure reach audit-ready lineage on critical reports in a single quarter, then extend coverage outward at a sustainable pace."),
]

# Build EN FAQ section + JSON-LD from list
def faq_section(items, num_start=1):
    out = ['<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">',
           '    <h2 class="faq-section-title">',
           '        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
           '        Frequently Asked Questions',
           '    </h2>',
           '    <div class="faq-list">']
    for i,(q,a) in enumerate(items, num_start):
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
    obj = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":ent}
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(obj, ensure_ascii=False, indent=2)

en_faq_html = faq_section(en_faq)
en_jsonld = faq_jsonld(en_faq)

# ---------- Inject EN ----------
en_path = os.path.join(ROOT, "blog/articles/%s.html"%slug)
html = open(en_path, encoding='utf-8').read()
m = re.search(r'(<p class="article-lead">.*?)(<nav class="article-nav")', html, re.S)
existing = m.group(1)
new_inner = existing + en_extra + en_faq_html + "\n" + en_jsonld + "\n"
html = html[:m.start(1)] + new_inner + html[m.end(1):]
open(en_path,'w',encoding='utf-8').write(html)
print("EN written")

# ---------- Chinese (Simplified) full body ----------
cn_sections = '''<p class="article-lead">监管机构已经不再接受"我们不知道这个数字从哪里来"这类回答。数据血缘（data lineage）——关于数据如何流动、转换与使用的完整、自动化记录——已经成为银行、保险、医疗乃至越来越多行业的合规硬性要求。本文解释企业如何构建既能满足监管、又能在运营中收回成本的数据血缘体系。</p>
<h2 id="the-current-landscape">当前监管环境发生了什么变化？</h2>
<p>监管环境在迅速收紧。欧盟《通用数据保护条例》（GDPR）仅在 2023 年一年就开出了 44.8 亿欧元的罚单，欧洲数据保护委员会报告这一数字在 2024 年攀升至超过 52 亿欧元。2024 年 8 月生效的《欧盟人工智能法案》为 AI 系统增加了透明度义务；而在银行业，BCBS 239 等-sector 规则长期要求机构证明其风险数据的来源与转换过程。在亚太地区，从新加坡金融管理局到澳大利亚审慎监管局，监管者都在问同一个问题：把血缘拿出来给我们看。</p>
<p>商业现实与监管现实同步。数据负责人不能再靠指向一个仪表盘来回答"这份报告准确吗？"，而必须能够把一个数字沿着每一次转换、连接与聚合追溯回源头。我们在该地区的工作表明，<strong>不到三分之一的企业在其全部数据资产上拥有自动化的、列级别的数据血缘</strong>——其余企业依赖的文档，在写下的当天就已经过时。</p>
<h2 id="key-implementation-challenges">实施数据血缘的关键挑战是什么？</h2>
<p>第一个挑战是覆盖。只有当血缘完整时它才具有合规意义，而完整性很难做到：现代数据资产混合了数据仓库、数据湖、流式平台和数十种转换工具，每一种都有自己的元数据。人工捕获血缘——让工程师记录他们的管道——会失败，因为文档不会被更新、不可信，也无法扩展到成千上万张表。唯一可持续的做法是在数据移动的每一个阶段自动捕获。</p>
<p>第二个挑战是粒度。表级别血缘能回答"这张表从哪来"，但监管者越来越想要列级别血缘——是哪一列通过哪些转换产生了这个值。列级别血缘自动捕获难度大得多，但它正是影响分析、数据映射审计和GDPR数据主体访问请求得以落地的关键。我们的评估发现，团队通常会把这个差距低估一倍。</p>
<p>第三个挑战是信任。不完整或自相矛盾的数据血缘元数据比没有更糟，因为它给合规团队虚假的信心。企业必须校验血缘——把捕获的元数据与实际执行日志核对——并且必须能说清资产中哪些部分被覆盖了、哪些没有。</p>
<p>第四个挑战是工具蔓延。数据血缘元数据散落在数据目录、编排工具、数据仓库和笔记本中；为每个领域各买一套血缘工具的企业，最终得到一张无法拼接的地图。成功的组织把血缘整合进一个受治理的存储，以开放的摄取方式接受来自每个阶段的元数据，而不是维护彼此矛盾的平行血缘系统。</p>
<h2 id="what-do-you-show-a-regulator-on-a-monday-morning">周一早上你拿什么给监管者看？</h2>
<p>这是每个合规项目都应为之设计的目标。当审计者问某个具体数字是如何产生的，企业应当能在数小时内产出从源到报告的可视化血缘图，标注每一次转换、确认每一个负责人、标记每一个数据主体类别。如果这一演示需要一周的人工考古，那么无论治理材料多么光鲜，项目都还没准备好。</p>
<p>为这个目标而设计会改变优先级。它意味着血缘必须可查询，而不仅仅是可视化；意味着系统必须捕获执行历史，而不仅仅是设计；意味着合规团队必须以规律节奏用实时查询演练这一演示，直到流程变成日常。以这种方式演练的企业总能持续发现漏洞——一个未被监控的老旧抽取、一次未记录的手动调整——否则它们只会在真实审计中暴露。</p>
<p>答案的一部分也是组织层面的：为每个监管领域指定一名具名数据管家，有权签字确认血缘准确且最新。监管者很看重"血缘是某人的职责"这一证据，而不只是一种系统输出。当我们陪同客户应对监管时，成熟度最强的单一信号，就是管家能在不回头找工程团队的情况下回答关于血缘图谱的追问。</p>
<h2 id="practical-approaches-that-work">哪些实操方法真正有效？</h2>
<p>在源头自动捕获。无论选择何种血缘工具，捕获都应是自动的——解析 SQL、插桩转换引擎、读取执行日志——而不是手动标注。手动血缘是一个会腐烂的文档项目；自动血缘是一个能自我更新的运营系统。在我们的项目中，自动捕获的组织在两个季度内对其受治理资产的血缘覆盖达到 95% 以上，而依赖手动文档的团队大约只有一半。</p>
<p>把血缘叠加到语义层。当血缘连接到业务定义时，它的价值会大幅提升——驱动自助式分析的同一语义层，可以用业务术语、负责人和敏感度分类来标注血缘。一张标注着"客户主数据——财务负责人——个人数据——受限"的血缘图，合规团队可以立即使用；而一张原始技术图还需要翻译。正是在这里，血缘从工程师的工具变成整个组织的资产。</p>
<p>让血缘服务于运营价值，而不只是合规。影响分析——"如果这个源变了，什么会断？"——让血缘系统的回报远超其成本。当源系统变更表结构或供应商停掉某个数据源，血缘会告诉你受影响的每一个下游报告、模型和仪表盘，把潜在的救火变成有计划的迁移。从按风险排序的资产开始：没有企业能在一个季度内映射每张表，所以先从支撑监管报告、财务报表和面向客户决策的数据集开始——也就是审计者会首先审查的那些。在我们的项目中，按监管暴露排序的企业能在单个季度内让关键报告达到审计就绪的血缘，然后以可持续的节奏向外扩展。一个务实的构建顺序如下：</p>
<ol>
<li>在摄取、转换和报告各阶段自动捕获血缘</li>
<li>用业务术语、负责人和敏感度分类标注血缘</li>
<li>以规律节奏演练监管演示，直到它成为日常</li>
<li>把血缘连接到影响分析，用于变更管理与事件响应</li>
<li>将捕获的血缘与执行日志核对，以维持信任</li>
<li>如实报告覆盖率——清楚资产中哪些部分已被映射、哪些没有</li>
</ol>
<p>最后，像对待资产一样治理血缘。指定一名血缘负责人，把血缘存储当作关键基础设施并加以监控，并把血缘准确性纳入数据质量报告。当血缘本身被治理，它就能在组织重组、工具变更和人员流动中存活下来——而这正是一个合规项目最容易瓦解的时刻。</p>
<h2 id="how-do-you-choose-a-lineage-tool-without-creating-another-silo">如何选择血缘工具而不制造新的孤岛？</h2>
<p>血缘市场挤满了数据目录工具、自带血缘的转型引擎，以及只能理解单一平台的单点方案。企业常犯的错误是为每个领域各买一套血缘工具，结果产生几张无法拼接的局部地图。可持续的模式是把血缘当作单一受治理资产、以开放摄取来对待：一个存储，同样接受来自数据仓库、数据湖、编排工具和笔记本的元数据。能捕获最多自动元数据的工具，不如把元数据整合起来的纪律重要。</p>
<p>在实践中，优先选择能解析 SQL 并读取执行日志的工具，而不是依赖工程师标注管道的工具。前者随系统变化保持最新；后者在管道被编辑却未同步更新文档的那一刻就开始腐烂。评估供应商时，要求在一个混乱的真实表上现场演示列级别血缘——而不是精心准备的样例——因为那才是审计真正测试的场景。</p>
<h2 id="what-does-audit-ready-lineage-look-like-in-practice">审计就绪的血缘在实践中是什么样子？</h2>
<p>我们合作过的一家地区性银行，曾把它的监管报告当作黑盒：仪表盘上的一个数字，没有可追溯的回源路径。在监管者质疑其中一个资本数字后，团队花了十一天手工重建逻辑。我们在摄取、转换和报告各环节自动捕获血缘，再用业务术语和数据主体类别标注血缘图。下一次同样的问题到来时，管家在不到三小时内就产出了从源到报告的完整图谱，每一次转换、负责人和敏感度标记都清晰可见。项目从考古变成了日常。</p>
<p>这个教训具有普遍性：审计就绪不是报告本身的属性，而是生产报告的系统的属性。如果一次演示需要人工，项目就没准备好；如果它需要针对受治理血缘的一次实时查询，那就准备好了。</p>
<h2 id="how-does-lineage-connect-to-ai-governance">血缘如何与 AI 治理连接？</h2>
<p>随着企业部署更多模型，血缘不再只关乎报告，也开始关乎模型输入。一个模型的可辩护性，取决于训练和喂给它的数据；当监管者或干系人问"模型为何做出这个决定"，答案需要把特征追溯回源头。同时覆盖分析报告和模型特征管道的血缘，让组织能用它与财务报告相同的证据来回答"这个训练信号从哪来"。</p>
<p>这种融合正是我们建议用单一血缘存储贯通商业智能与机器学习的理由。它把治理从一项独立的合规活动，变成一条"数据如何成为决策"的连续记录——而这恰恰是现代 AI 监管越来越期望的。</p>'''

cn_faq = [
 ("什么是数据血缘，它为何对监管合规重要？",
  "数据血缘是关于数据如何在企业内流动、转换与使用的自动化端到端记录。银行、保险、医疗等行业的监管者现在要求组织展示报告数字的来源及其转换过程。没有血缘，企业无法回答审计者的问题，并在这些问题意外到来时面临罚款与声誉损害的风险。"),
 ("血缘应该是表级别还是列级别？",
  "列级别血缘正越来越被监管者所期望。表级别血缘告诉你哪张表产生了另一张表，却无法回答是哪个具体列驱动了某个值——而影响分析、数据映射审计和数据主体访问请求恰恰需要这一点。自动捕获列级别血缘更难，但它是血缘图从「工程师能用」变为「合规团队可执行」的关键差别。"),
 ("如何在不进行庞大手动项目的情况下让血缘达到审计就绪？",
  "在数据移动的每个阶段自动捕获——解析 SQL、插桩转换引擎、读取执行日志——而不是让工程师手工记录管道。然后用业务术语、负责人和敏感度分类标注图谱，将其与执行日志核对以维持信任，并以规律节奏演练监管演示，使流程成为日常而非救火。"),
 ("数据血缘只对合规有帮助吗？",
  "不是。血缘通过影响分析在运营上就能收回成本：当源表结构变更或供应商停掉某个数据源，血缘会显示受影响的每一个下游报告、模型和仪表盘，把潜在的事故变成有计划的迁移。按监管暴露排序的组织能在单个季度内让关键报告达到审计就绪的血缘，然后以可持续节奏向外扩展覆盖。"),
]

cn_faq_html = faq_section(cn_faq)
cn_jsonld = faq_jsonld(cn_faq)
cn_inner = cn_sections + "\n" + cn_faq_html + "\n" + cn_jsonld + "\n"

tw_inner = cc.convert(cn_inner)

for lang, inner in (("zh-cn", cn_inner), ("zh-tw", tw_inner)):
    p = os.path.join(ROOT, "%s/blog/articles/%s.html"%(lang, slug))
    h = open(p, encoding='utf-8').read()
    mm = re.search(r'(<p class="article-lead">.*?)(<nav class="article-nav")', h, re.S)
    h = h[:mm.start(1)] + inner + h[mm.end(1):]
    open(p,'w',encoding='utf-8').write(h)
    print(lang, "written")

# ---------- verify ----------
for lang,pat in (("en","blog/articles/%s.html"),("zh-cn","zh-cn/blog/articles/%s.html"),("zh-tw","zh-tw/blog/articles/%s.html")):
    p=os.path.join(ROOT, pat%slug)
    h=open(p,encoding='utf-8').read()
    body=re.search(r'<article class="article-content" id="article-content">(.*?)</article>',h,re.S).group(1)
    if lang=="en":
        w=len(re.findall(r"[A-Za-z0-9']+", body))
        print(lang,"words=",w,"faq=",body.count('faq-item'),"jsonld=", 'FAQPage' in h, "css=", h.count('article.css?v=20260826'),"js=",h.count('article.js?v=20260826'),"footer=",h.count('footer class="footer"'))
    else:
        c=len(re.findall(r'[\u4e00-\u9fff]', body))
        print(lang,"cjk=",c,"faq=",body.count('faq-item'),"jsonld=", 'FAQPage' in h, "css=", h.count('article.css?v=20260826'),"js=",h.count('article.js?v=20260826'),"footer=",h.count('footer class="footer"'))
