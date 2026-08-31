#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "ai-strategy-maturity-assessment"

EN_NEW = """
<h2 id="how-do-you-score-each-dimension-with-evidence">How Do You Score Each Dimension With Evidence?</h2>
<p>The difference between a maturity assessment that changes a budget and one that produces a slide is whether scores are anchored to evidence. Four dimensions, each with a scoring rule that a newcomer could verify.</p>
<table>
<thead>
<tr><th>Dimension</th><th>Level 1 evidence</th><th>Level 3 evidence</th><th>Level 4 evidence</th></tr>
</thead>
<tbody>
<tr><td>Strategy and governance</td><td>No charter; AI activity is informal and unbudgeted</td><td>Published charter, named risk owner, coverage reported to the board quarterly</td><td>Governance determines which AI products the company builds, not just which are permitted</td></tr>
<tr><td>Data foundation</td><td>Data extracted manually for each project</td><td>Priority domains sit on connected, quality-monitored data with named owners</td><td>Data products are published, versioned and reused across the business</td></tr>
<tr><td>Talent and operating model</td><td>A handful of enthusiasts</td><td>Defined roles, a training path, and a support model for production systems</td><td>Building and running AI is a standing organisational capability</td></tr>
<tr><td>Demonstrated business value</td><td>Anecdotes from pilots</td><td>Named workflows with baseline-to-current deltas reconciled by finance</td><td>AI contributions appear in the operating plan, not in the innovation report</td></tr>
</tbody>
</table>
<p>Two rules keep the scoring honest. First, require the artefact, not the assertion: a charter document, a dashboard URL, a reconciled number, a named owner. If the artefact cannot be produced during the session, the dimension scores one level lower. Second, score the organisation at the lowest level among the dimensions a given claim depends on. Level 4 governance running on level 2 data produces level 2 outcomes, and reporting the average hides exactly the thing that needs funding.</p>
<p>Record the dissenting view. When a business leader and the platform team disagree by two levels, that disagreement is the most informative output of the exercise — it usually marks an ownership gap rather than a measurement error.</p>
<h2 id="what-does-level-1-versus-level-4-look-like-in-practice">What Does Level 1 Versus Level 4 Look Like in Practice?</h2>
<p>Level 1 organisations are easy to recognise: AI work happens because someone enthusiastic made it happen. Models live in notebooks, pilots are announced internally and quietly abandoned, and if you ask how many AI systems are in production the honest answer is that nobody is certain. Spend is spread across departments with no portfolio view, and the board receives updates about activity rather than outcomes.</p>
<p>Level 4 organisations look less glamorous than the hype suggests. There is a portfolio of production workflows, each with a named business owner and a measured outcome. The data those workflows depend on has owners and quality monitoring. Governance is a working process with a queue, not a document. Most tellingly, the conversation has shifted from "should we do AI" to "which three workflows graduate next quarter" — and the people asking are business leaders, not the AI team.</p>
<p>The transition is not primarily a technology problem. Level 2 to level 3 happens when a workflow graduates to production with an owner and a measured number. Level 3 to level 4 happens when the operating model adapts around it: budgets move to the teams that own the workflows, hiring plans account for AI-supported processes, and governance becomes fast enough that teams route through it rather than around it. Organisations stuck at level 3 are almost always stuck on the second half.</p>
<h2 id="who-should-run-the-assessment-and-who-should-own-the-result">Who Should Run the Assessment and Who Should Own the Result?</h2>
<p>Assessment ownership is a governance question before it is a project management one. The facilitator should sit outside the team whose work is being scored — an internal strategy or audit function works well, as does an external adviser, because the value of the exercise depends on people being willing to say "we are level 2" in front of their peers.</p>
<p>The input group needs four constituencies: the business functions that own candidate workflows, the data and platform teams who know what the infrastructure can actually support, risk or internal audit, and at least one sceptic. Excluding the sceptic is the most common and most damaging shortcut — it produces a consensus document that falls apart the first time someone asks for evidence.</p>
<p>Ownership of the <em>result</em> is different and more important. The output should name one executive accountable for the binding constraint and one funded initiative against it. If the assessment ends with a shared recommendation to "improve data readiness" and no named owner, it has produced awareness rather than a decision. The cleanest test: can you name the person who will be asked, in two quarters, why the number has not moved?</p>
<h2 id="how-do-you-turn-the-assessment-into-a-funded-roadmap">How Do You Turn the Assessment Into a Funded Roadmap?</h2>
<p>Most assessments fail after the workshop, in the gap between a prioritised list and an actual budget line. Closing that gap takes four steps.</p>
<ol>
<li><strong>Name the binding constraint in one sentence.</strong> Not three priorities — one. The dimension that, left unchanged, makes progress in the others irrelevant. Everything else in the roadmap is sequenced behind it.</li>
<li><strong>Convert it into a single funded initiative.</strong> A target level, a named executive owner, a date, and the metric that will demonstrate the move. One initiative converts; a list of nine diffuses.</li>
<li><strong>Attach a validation mechanism.</strong> Put a working system in front of the organisation within weeks rather than quarters. A managed deployment that connects to existing data and delivers answers in the tools people already use turns an abstract maturity claim into something the organisation can react to — and reactions are data.</li>
<li><strong>Set the re-assessment date before leaving the room.</strong> Six months, same rubric, ideally the same facilitator. Without a date, the assessment becomes a historical artefact within two quarters.</li>
</ol>
<p>The organisations that compound AI capability treat the assessment as a recurring governance instrument rather than a one-off diagnostic. The ones that drift treat it as a report, file it, and start the next planning cycle from memory.</p>
"""

CN_NEW = """
<h2 id="how-do-you-score-each-dimension-with-evidence">如何用证据为每个维度打分？</h2>
<p>一次成熟度评估能否改变预算，取决于评分是否锚定在证据上。四个维度，每个都有一条新人也能核实的评分规则。</p>
<table>
<thead>
<tr><th>维度</th><th>等级1的证据</th><th>等级3的证据</th><th>等级4的证据</th></tr>
</thead>
<tbody>
<tr><td>战略与治理</td><td>没有章程，AI活动是零散且无预算的</td><td>已发布章程，有具名的风险责任人，覆盖率每季度向董事会汇报</td><td>治理决定公司构建哪些AI产品，而不只是允许哪些</td></tr>
<tr><td>数据基础</td><td>每个项目都手工抽取数据</td><td>优先领域的数据已连通、有质量监控和具名责任人</td><td>数据产品被发布、版本化，并在全业务范围内复用</td></tr>
<tr><td>人才与运营模式</td><td>只有几位热衷者</td><td>角色明确、有培养路径，生产系统有支持机制</td><td>构建与运营AI已成为一项常设的组织能力</td></tr>
<tr><td>已证明的业务价值</td><td>来自试点的轶事</td><td>有具名工作流，且有经财务核对的基线到当前的变化值</td><td>AI的贡献出现在经营计划里，而不是创新报告里</td></tr>
</tbody>
</table>
<p>有两条规则能保证评分诚实。第一，要求的是物证而不是断言：章程文件、仪表盘链接、经核对的数字、具名责任人。如果在会议中拿不出物证，该维度就降一级。第二，某项主张所依赖的多个维度中，按最低的那个等级给组织打分。等级4的治理跑在等级2的数据上，产出的是等级2的结果；而汇报平均值，恰好掩盖了最需要投入的那一处。</p>
<p>要记录不同意见。当业务负责人与平台团队的评分相差两级时，这个分歧正是本次评估最有信息量的产出——它通常标志着一个责任归属的缺口，而不是一次测量误差。</p>
<h2 id="what-does-level-1-versus-level-4-look-like-in-practice">等级1与等级4在实践中的差别是什么？</h2>
<p>等级1的组织很容易辨认：AI工作之所以发生，是因为某个有热情的人让它发生了。模型躺在笔记本里，试点在内部宣布后又悄然放弃；如果你问有多少个AI系统在生产中运行，诚实的答案是没有人确定。支出分散在各业务部门，没有组合视图，而董事会收到的是关于活动量而非结果的汇报。</p>
<p>等级4的组织看起来没有炒作所暗示的那么炫目。那里有一组生产工作流，每一个都有具名的业务负责人和可度量的成果；这些工作流所依赖的数据有责任人和质量监控；治理是一套带队列的运作流程，而不是一份文档。最能说明问题的是，讨论已经从"我们要不要做AI"转向"下个季度哪三个工作流晋级"——而提出这个问题的是业务负责人，不是AI团队。</p>
<p>这个跃迁主要不是技术问题。从等级2到等级3，发生在某个工作流带着责任人和可度量数字晋级到生产环境时。从等级3到等级4，则发生在运营模式围绕它完成调整时：预算流向拥有工作流的团队，招聘计划把AI支持的流程考虑在内，而治理快到让团队愿意走流程而不是绕开它。卡在等级3的组织，几乎总是卡在后半段。</p>
<h2 id="who-should-run-the-assessment-and-who-should-own-the-result">评估由谁来主持，结果由谁来负责？</h2>
<p>评估的归属首先是一个治理问题，其次才是项目管理问题。主持人应当来自被评分团队之外——内部战略或审计职能都合适，外部顾问也可以，因为这次评估的价值取决于人们是否愿意在同僚面前说出"我们是等级2"。</p>
<p>参与输入的需要有四类人：拥有候选工作流的业务职能、清楚基础设施实际承载能力的平台团队、风险或内审部门，以及至少一位质疑者。把质疑者排除在外是最常见也最具破坏性的捷径——它会产出一份在第一次被要求出示证据时就崩塌的共识文件。</p>
<p><em>结果</em>的归属则不同，也更重要。产出应当明确一位对约束性瓶颈负责的高管，以及一个针对它的、已获预算的举措。如果评估以"提升数据就绪度"这样一个共同建议收尾，却没有具名责任人，那么它产出的是认知，而不是决策。最简单的检验方式是：你能说出两个季度后谁会被问到"为什么这个数字没有变化"吗？</p>
<h2 id="how-do-you-turn-the-assessment-into-a-funded-roadmap">如何把评估转化为一份有预算的路线图？</h2>
<p>多数评估是在工作坊之后失败的，失败在"优先事项清单"与"实际预算条目"之间的那道鸿沟上。弥合它需要四步。</p>
<ol>
<li><strong>用一句话指出约束性瓶颈。</strong>不是三个优先事项，而是一个。那个如果不变、其他维度的进展就变得无关紧要的维度。路线图中的其他事项都排在它后面。</li>
<li><strong>把它转化为一个已获预算的举措。</strong>包含目标等级、具名的高管责任人、截止日期，以及能证明跃迁发生的指标。一个举措能促成改变，九个只会稀释注意力。</li>
<li><strong>附上一个验证机制。</strong>在数周内而不是数个季度内，把一个可运行的系统摆到组织面前。一次接入现有数据、并在人们已在使用的工具里给出答案的托管式部署，会把抽象的成熟度主张变成组织能够作出反应的东西——而这些反应本身就是数据。</li>
<li><strong>在散会之前定好复评日期。</strong>六个月，同一套评分标准，最好还是同一位主持人。没有日期，评估会在两个季度内变成一份历史文件。</li>
</ol>
<p>能够持续积累AI能力的组织，把评估当作一项周期性的治理工具，而不是一次性的诊断。随波逐流的组织则把它当成一份报告，归档了事，然后在下一个规划周期凭记忆重新开始。</p>
"""

FAQ = {
 "EN": [
  ("How often should an AI maturity assessment be repeated?",
   "Re-assess on a six-month cadence with a lightweight quarterly check-in on the dimensions in motion, and run the full four-dimension assessment annually with the same rubric. Comparability matters more than precision - a consistent methodology that shows direction of travel is more useful to a board than a sophisticated model applied differently each time."),
  ("What is the single most common reason assessments fail?",
   "They end with a prioritised list instead of a funded decision. If the output does not name one binding constraint, one executive owner, one funded initiative with a target level and a date, and a re-assessment date, the assessment produced awareness rather than change."),
  ("Who should be in the room for the scoring session?",
   "Business functions that own candidate workflows, the data and platform teams who know what the infrastructure can support, someone from risk or internal audit, and at least one sceptic. The facilitator should sit outside the AI team, and the enthusiasts who built the pilots should not score their own work."),
  ("How quickly can an assessment turn into something working?",
   "The assessment itself runs in eight to twelve weeks, but validation should not wait for it to finish. Putting a working system in front of the organisation within two weeks - connected to existing data, answering questions in the tools people already use - turns abstract maturity claims into reactions you can measure."),
 ],
 "zh-CN": [
  ("AI成熟度评估应该多久做一次？",
   "建议以六个月为周期复评，并针对正在变化的维度做轻量级的季度检查；完整的四维度评估则每年用同一套评分标准做一次。可比性比精确度更重要——对董事会而言，一套能显示变化趋势的一致方法，比每次都用不同方式套用的复杂模型更有用。"),
  ("评估失败最常见的原因是什么？",
   "它们以一份优先事项清单收尾，而不是一个已获预算的决策。如果产出没有明确指出唯一的约束性瓶颈、一位高管责任人、一个带目标等级和截止日期的已获预算举措，以及复评日期，那么这次评估产出的是认知，而不是改变。"),
  ("评分会议应该让谁参加？",
   "拥有候选工作流的业务职能、清楚基础设施承载能力的平台团队、风险或内审部门的代表，以及至少一位质疑者。主持人应当来自AI团队之外，而构建试点的热情推动者不应给自己的工作打分。"),
  ("评估多久能转化为可运行的东西？",
   "评估本身需要八到十二周，但验证不必等它结束。在两周内把一个可运行的系统摆到组织面前——接入现有数据、在人们已在使用的工具里回答问题——会把抽象的成熟度主张变成可以衡量的反应。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<h2 id="key-takeaways">Key Takeaways</h2>'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n" + anchor, 1)
    ren = {
        "Understanding the Current Landscape": "Where Does Your Organisation Actually Stand on AI?",
        "Key Principles and Strategic Framework": "What Principles Should Guide a Maturity Assessment?",
        "Implementation Approach and Best Practices": "How Should the Assessment Be Run?",
        "Measuring Success and Demonstrating ROI": "How Do You Measure Success and Demonstrate ROI?",
        "Common Pitfalls and How to Avoid Them": "What Are the Most Common Pitfalls and How Do You Avoid Them?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    b = b.replace("ssessing where your orgizaion st与关于  AI journey", "评估组织在AI旅程中所处的位置")
    b = b.replace("ssessing where your orgizaion st与关于 AI journey", "评估组织在AI旅程中所处的位置")
    anchor = '<h2 id="关键要点">关键要点</h2>'
    assert anchor in b
    b = b.replace(anchor, CN_NEW.strip() + "\n" + anchor, 1)
    ren_cn = {
        "理解当前格局": "贵组织在AI上究竟处于什么位置？",
        "关键原则与战略框架": "成熟度评估应该遵循哪些原则？",
        "实施方法与最佳实践": "评估应该如何开展？",
        "衡量成功与展示投资回报率": "如何衡量成效并展示投资回报？",
        "常见陷阱及规避方法": "最常见的陷阱有哪些，如何规避？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    for old, new in [('id="理解当前格局"', 'id="where-does-your-organisation-actually-stand"'),
                     ('id="关键原则与战略框架"', 'id="what-principles-should-guide-an-assessment"'),
                     ('id="实施方法与最佳实践"', 'id="how-should-the-assessment-be-run"'),
                     ('id="衡量成功与展示投资回报率"', 'id="how-do-you-measure-success-and-demonstrate-roi"'),
                     ('id="常见陷阱及规避方法"', 'id="what-are-the-most-common-pitfalls"'),
                     ('id="关键要点"', 'id="key-takeaways"'),
                     ('id="结论"', 'id="conclusion"')]:
        b = b.replace(old, new)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
