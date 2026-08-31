#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "conversational-bi-empowers-non-technical-teams-2025"

EN_NEW = """
<h2 id="which-teams-benefit-first-and-why">Which Teams Benefit First and Why?</h2>
<p>Conversational BI does not land evenly across an organisation, and pretending otherwise is how pilots lose momentum. The teams that benefit first share three characteristics: they ask a high volume of similar questions, their questions depend on data that already exists in governed systems, and they currently wait on someone else to get answers.</p>
<table>
<thead>
<tr><th>Team</th><th>Typical first questions</th><th>Why it lands fast</th></tr>
</thead>
<tbody>
<tr><td>Marketing</td><td>Which channel drove the drop in trial sign-ups this fortnight, and is it a volume or conversion problem?</td><td>Campaign and web analytics data usually already sits in the warehouse with clean dimensions</td></tr>
<tr><td>Finance</td><td>How does actual spend to date compare with plan by cost centre, and where are the variances concentrated?</td><td>Metric definitions are already governed, which removes the hardest part of the work</td></tr>
<tr><td>Operations</td><td>Which sites are running below throughput target this week, and what is the common factor?</td><td>Questions are repetitive and operational, so the semantic layer pays back quickly</td></tr>
<tr><td>HR</td><td>What is attrition by tenure band and department, and how does it compare with last year?</td><td>High question volume, historically served by a slow ticket queue</td></tr>
<tr><td>Sales</td><td>Which accounts have open opportunities past their expected close date, and what is the pipeline at risk?</td><td>CRM data is structured and the questions are highly patterned</td></tr>
</tbody>
</table>
<p>Teams that struggle first are the ones whose questions depend on data that is not yet connected or whose key metrics have no agreed definition. That is not a reason to exclude them — it is a reason to start elsewhere and treat the semantic layer work they need as a funded follow-on.</p>
<p>The pattern worth watching is the second team, not the first. First-team adoption can be explained by an enthusiastic champion. Second-team adoption, without that champion, is the evidence that the tool works rather than that a person made it work.</p>
<h2 id="what-does-good-look-like-for-a-governed-answer">What Does Good Look Like for a Governed Answer?</h2>
<p>The difference between a governed answer and a confident guess is not the tone — it is whether the answer carries everything a sceptical reader needs to act on it. Four elements, all visible in the response.</p>
<ul>
<li><strong>The metric definition.</strong> The answer states which definition it used. "Gross revenue, excluding refunds, as defined in the finance semantic model" is an answer a CFO can accept; "revenue: 4.2M" is not, because it invites a second question about what revenue means.</li>
<li><strong>The data provenance.</strong> Source system, table, and freshness timestamp. An executive who can see that the figure reflects data as of 06:00 today knows how much to trust it in a fast-moving situation.</li>
<li><strong>The scope and filters applied.</strong> Region, period, and any exclusions, stated explicitly rather than implied. Most disputes about numbers turn out to be disputes about scope.</li>
<li><strong>The authorisation context.</strong> Confirmation that the answer reflects only data the user is entitled to see, which matters the moment sensitive columns exist in the source.</li>
</ul>
<p>These four elements are also what make the answer defensible later. When someone challenges a decision six weeks on, the question is never "was the number right" — it is "what exactly did the number mean and where did it come from". An answer that carried its own context can be reconstructed in seconds.</p>
<h2 id="how-do-you-prevent-confident-wrong-answers">How Do You Prevent Confident Wrong Answers?</h2>
<p>The risk that worries every data leader is not that the system refuses to answer; it is that it answers fluently and incorrectly. Four controls reduce that risk to an acceptable level, and they are mostly semantic layer work rather than model work.</p>
<p><strong>Constrain the vocabulary before you expose the tool.</strong> The semantic layer should define the metrics and dimensions users can ask about. Questions about undefined concepts should return "that is not defined in our metrics" rather than an improvised calculation. This single control prevents most wrong answers, because most wrong answers are reasonable-sounding misinterpretations of undefined terms.</p>
<p><strong>Refuse rather than approximate.</strong> When a question cannot be answered from available data, the correct behaviour is an explicit statement of what is missing. A system that says "I do not have cost data before March 2024" builds more trust than one that silently extrapolates.</p>
<p><strong>Surface ambiguity instead of resolving it silently.</strong> "Revenue last quarter" may mean calendar or fiscal quarter. A governed system asks, or states which it assumed and offers the alternative. Silent resolution is how two executives end up quoting different numbers from the same tool.</p>
<p><strong>Log every question and answer, and review the failures.</strong> The questions users ask are the specification for the semantic layer. Reviewing the ones that produced poor answers weekly is the fastest improvement loop available, and it converts user behaviour into governance input.</p>
<h2 id="how-do-you-drive-adoption-beyond-the-first-team">How Do You Drive Adoption Beyond the First Team?</h2>
<p>Pilots with one enthusiastic team almost always succeed. Rollout is where programmes stall, and the failure is predictable enough to be designed against.</p>
<p><strong>Start with questions, not dashboards.</strong> Collect thirty real questions from the target team before configuring anything, and make sure the system answers them correctly. Adoption follows usefulness, and usefulness is measured against the questions people actually ask — which are almost never the ones stakeholders imagine in planning meetings.</p>
<p><strong>Put it where people already work.</strong> Adoption collapses when answering a question requires opening a new tool. Deploying into the chat platform the team already lives in is the difference between a system used daily and one used in training sessions.</p>
<p><strong>Publish the answers, not just the tool.</strong> When someone asks a good question and gets a useful answer, share both in the team channel. Most people need to see a colleague get value before they will try it themselves, and the shared answer demonstrates the vocabulary without any training.</p>
<p><strong>Measure the queue, not the logins.</strong> The metric that persuades a sceptical executive is the drop in ad-hoc requests reaching the analytics team. Organisations consistently report that volume falling by more than half once teams self-serve, and that number is worth more than any adoption percentage.</p>
<p>Finally, assign an owner for the semantic layer. Adoption plateaus when new questions outpace defined metrics, and the plateau is always an ownership problem rather than a technology problem.</p>
"""

FAQ = {
 "EN": [
  ("Do non-technical teams really need no training?",
   "They need no query-language training, which is the barrier that matters. Users still need to know which metrics exist and what they mean - which is why the semantic layer, published definitions, and shared examples matter more than formal training. Teams that see a colleague get a useful answer adopt fastest."),
  ("How is this different from adding a chatbot to an existing BI tool?",
   "A chatbot over BI can only answer questions the pre-built dashboards already cover. Conversational BI resolves intent against the semantic layer, so unanticipated questions still return governed answers - and each answer carries its metric definition, source, freshness and scope."),
  ("What stops the system giving a confidently wrong answer?",
   "Constraint before improvisation. The semantic layer defines which metrics exist, undefined concepts return an explicit refusal rather than a guess, ambiguity is surfaced rather than silently resolved, and every question and answer is logged for weekly review."),
  ("How quickly can non-technical teams see value?",
   "A focused deployment mapping the semantic layer to an existing warehouse and piloting with two business teams typically shows value within the first quarter. The critical success factor is mapping to existing governed metric definitions rather than rebuilding the data stack."),
 ],
 "zh-CN": [
  ("非技术团队真的不需要培训吗？",
   "他们不需要查询语言方面的培训，而这正是真正构成障碍的部分。用户仍然需要知道存在哪些指标、它们各自的含义——这就是为什么语义层、公开发布的定义和共享示例比正式培训更重要。看到同事拿到有用答案的团队，采用速度最快。"),
  ("这与在现有BI工具上加一个聊天机器人有什么不同？",
   "构建在BI之上的聊天机器人只能回答预置仪表盘已经覆盖的问题。对话式BI则针对语义层解析意图，因此未被预见的问题也能返回受治理的答案——而且每个答案都携带指标定义、来源、时效性和作用域。"),
  ("如何避免系统给出自信却错误的答案？",
   "先约束，再谈生成。语义层定义了存在哪些指标，未定义的概念会返回明确的拒绝而不是猜测，歧义会被显式呈现而不是被静默消解，并且每一个问题与答案都会被记录以供每周复盘。"),
  ("非技术团队多久能看到价值？",
   "一次聚焦的部署——把语义层映射到现有数据仓库，并在两个业务团队中试点——通常在第一个季度内就能显现价值。关键成功因素是映射到已有的、受治理的指标定义，而不是重建数据栈。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<section class="faq-section"'
    if anchor not in b:
        anchor = '<section[^>]*faq-section'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n\n            " + anchor, 1)
    ren = {
        "Key Benefits and ROI Considerations": "What Benefits and ROI Should Non-Technical Teams Expect?",
        "Implementation Roadmap and Next Steps": "What Does an Implementation Roadmap Look Like?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    ren_cn = {
        "核心收益与投资回报考量": "非技术团队能获得哪些收益与投资回报？",
        "实施路线图与后续步骤": "落地路线图与后续步骤是什么？",
        "常见问题解答": "企业最常问的问题有哪些？",
        "案例分析与行业洞察": "有哪些可借鉴的案例与行业洞察？",
        "未来展望与行动建议": "未来展望与行动建议是什么？",
        "关键成功因素与常见陷阱": "关键成功因素与常见陷阱有哪些？",
        "蜂启咨询的专业洞察": "蜂启咨询的专业洞察是什么？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
