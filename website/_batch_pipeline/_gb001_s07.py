#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "ai-adoption-barriers-change-management"

EN_SECTIONS = [
 ("what-does-effective-change-management-for-ai-actually-look-like",
  "What Does Effective Change Management for AI Actually Look Like?",
  """<p>Most AI change management fails because it is delivered as communication rather than as redesign. A town hall explaining that the new system will make everyone more productive does not change behaviour, because the barriers are not informational. People do not adopt a tool when they cannot tell whether its output is trustworthy, when using it makes them accountable for a decision they did not make, when it adds a step to a workflow that is already measured on throughput, or when being seen to need it feels like an admission that the job is being automated.</p>
<p>Effective programmes work on four concrete things. First, redesign the workflow, not just the tool: decide explicitly what the human does, what the system does, and what happens when they disagree — then measure the new process, because if the old throughput target stays in place, people will revert to the old method to hit it. Second, build verification into the interface: show the source, the confidence, and how to check the answer, so trust can be calibrated rather than demanded.</p>
<p>Third, train on exceptions, not on features. Users do not need a tour of the interface; they need to know what to do when the output looks wrong, and they need a named person to escalate to. Fourth, recruit and equip credible internal champions from the teams doing the work — adoption spreads through peers who can say "I use this and here is where it saved me an hour", not through executive memos.</p>"""),

 ("how-do-you-measure-ai-adoption-not-just-deployment",
  "How Do You Measure AI Adoption, Not Just Deployment?",
  """<p>Deployment is a milestone; adoption is a behaviour. The distinction matters because nearly every stalled AI programme has green status on deployment and red status on usage. A useful adoption metric set has five measures, and all of them should be visible to the business owner, not just the project team.</p>
<ul>
<li><strong>Reach:</strong> what share of the intended users have used the system at least once in the last week. This separates a licensed pilot from a used one.</li>
<li><strong>Depth:</strong> what share of the relevant decisions or tasks are routed through the system. A tool used for 10% of applicable work has not changed the process.</li>
<li><strong>Retention:</strong> of users who try it, what share are still active after 30, 60, and 90 days. Early abandonment is the clearest signal that trust or workflow fit has failed.</li>
<li><strong>Override and correction rate:</strong> how often users accept the output unedited versus rewriting it. A high correction rate means the system is relocating work, not removing it.</li>
<li><strong>Outcome delta:</strong> cycle time, error rate, or cost per task compared with the pre-deployment baseline. This is the measure that survives a budget review.</li>
</ul>
<p>Pair these with qualitative signal: a short monthly survey asking users what the system gets wrong, plus a review of every escalation. Programmes that instrument adoption catch failure in the first month; programmes that only track deployment find out a year later, at renewal.</p>"""),

 ("which-roles-and-skills-does-an-ai-ready-organisation-need",
  "Which Roles and Skills Does an AI-Ready Organisation Need?",
  """<p>An AI-ready organisation is defined less by having machine-learning engineers than by having the roles that connect models to decisions. Four are consistently present in programmes that scale.</p>
<p>The first is an executive sponsor with budget authority, usually the CIO, CDO, or the business leader who owns the process being changed. Sponsorship is not a signature on a business case; it is the willingness to change a performance target when the AI-assisted workflow requires it. The second is a translator role — often titled analytics engineer, AI product manager, or business technologist — who can hold a conversation with both the data team and the operations team and turn a vague request into a testable use case. This role is the single most common gap and the most common cause of projects that are technically successful and operationally irrelevant.</p>
<p>The third is a data owner per domain, accountable for the definitions and quality of the data feeding the system, because every model inherits the quality of its inputs and someone has to own that. The fourth is a change and enablement lead who owns training, communications, and the feedback loop from users back to the build team.</p>
<p>Beyond roles, three skills need to be distributed rather than centralised: knowing what the system is good at and where it fails, knowing how to verify an output, and knowing when to escalate. Those three are what turn a workforce from passive recipients into competent supervisors of AI.</p>"""),

 ("how-do-you-handle-job-displacement-fear-honestly",
  "How Do You Handle Job-Displacement Fear Honestly?",
  """<p>Fear of displacement is the most under-managed risk in enterprise AI, and it is usually handled with reassurance that nobody believes. Vague promises that "AI will augment rather than replace" ring hollow to teams who have watched headcount fall in the function next door, and once trust is lost on this point, adoption becomes performative: people use the system just enough to satisfy a metric and no more.</p>
<p>The honest alternative is specificity about what is changing. Say which tasks are being automated, which are being reweighted, and what the organisation is committing to for the people affected. Where roles will shrink, say so early and pair it with a real path — retraining with paid time to do it, internal mobility with priority for affected teams, or natural attrition with a hiring freeze. Where roles will grow, name them and make the route into them visible.</p>
<p>Three practices help. Involve the affected teams in designing the new workflow, because people support what they helped build and resist what was done to them. Publish a measure of how the work is changing — hours shifted from data preparation to judgement, for example — so the claim can be checked. And make managers accountable for having the conversation, since a survey or an all-hands does not substitute for a manager telling a team what this means for them.</p>
<p>Organisations that do this do not eliminate fear; they convert it into a plan, which is enough to keep adoption real.</p>"""),
]

EN_FAQ = [
 ("Why do AI projects fail even when the technology works?",
  "Because the failure is usually adoption, not accuracy. Tools are deployed, test metrics look strong, and business users quietly keep working the old way because they cannot tell whether the output is trustworthy, the system was added to a workflow whose performance targets did not change, or nobody explained what to do when it is wrong. Treating adoption as a measured objective from day one — reach, depth, retention, override rate, outcome delta — is the difference between a deployed tool and a used one."),
 ("What is the biggest barrier to enterprise AI adoption?",
  "Workflow fit rather than model quality. When an AI system is layered onto a process whose throughput targets, incentives, and escalation paths are unchanged, rational users revert to the old method to hit their numbers. The programmes that succeed redesign the process alongside the tool: who does what, what happens when the human disagrees with the system, and which targets change."),
 ("How should organisations measure AI adoption?",
  "Track five measures: reach (share of intended users active in the last week), depth (share of applicable decisions routed through the system), retention (still active at 30, 60, and 90 days), override and correction rate (how often output is accepted unedited), and outcome delta against the pre-deployment baseline. Pair them with a short monthly survey on what the system gets wrong and a review of every escalation."),
 ("Which roles are needed for an AI-ready organisation?",
  "An executive sponsor with budget authority who will change performance targets when the workflow requires it; a translator role — analytics engineer or AI product manager — who can convert a business request into a testable use case; a data owner per domain accountable for definitions and quality; and a change and enablement lead who owns training and the user feedback loop. The translator role is the most common gap."),
 ("How do you address employee fear of AI-driven job displacement?",
  "Replace reassurance with specificity. State which tasks are being automated, which are being reweighted, and what is committed to affected people — retraining with paid time, internal mobility priority, or managed attrition. Involve affected teams in designing the new workflow, publish a measure of how the work is changing so the claim can be checked, and hold managers accountable for having the conversation directly."),
]

EN_RENAMES = {
 "the-strategic-imperative-for-ai-adoption-in-2025": "Why Is AI Adoption a Strategic Imperative in 2025?",
 "from-pilot-to-production-the-scaling-challenge": "What Makes Scaling from Pilot to Production So Hard?",
 "building-an-ai-ready-organisation": "How Do You Build an AI-Ready Organisation?",
}

EN = {"renames": EN_RENAMES, "sections": EN_SECTIONS, "faq": EN_FAQ,
      "excerpts": [
        "Building inclusive AI and data teams: what the evidence says actually changes outcomes.",
        "Why your data strategy needs a dedicated AI agent layer in 2026.",
        "Vector databases for enterprise search: a practical 2026 guide."]}

ZHCN_RENAMES = {
 "2025年企业ai采用的战略要务": "为什么AI采用在2025年是战略要务？",
 "从试点到生产-扩展挑战": "从试点到生产，扩展的挑战在哪里？",
 "构建ai就绪组织": "如何构建AI就绪的组织？",
}

ZHCN_FAQ = [
 ("为什么技术上成功的AI项目依然会失败？",
  "因为失败通常发生在采纳环节，而不是准确率环节。工具部署了，测试指标很好看，业务用户却悄悄沿用旧方法——原因是他们无法判断输出是否可信、系统被叠加到一个绩效目标没有改变的流程上、或者没有人告诉他们在系统出错时该怎么办。从第一天起就把采纳当作可衡量的目标——覆盖率、使用深度、留存率、覆盖修改率、结果增量——是「部署了工具」与「工具被真正使用」之间的分水岭。"),
 ("企业AI采用的最大障碍是什么？",
  "是流程适配，而不是模型质量。当AI系统被叠加到一个吞吐量目标、激励机制与上报路径都没有变化的流程之上时，理性的用户会为了完成指标而回到旧方法。成功的项目会把流程与工具一起重新设计：谁做什么、当人与系统意见不一致时如何处理、以及哪些考核指标需要随之改变。"),
 ("组织应该如何衡量AI采纳度？",
  "跟踪五项指标：覆盖率（目标用户中过去一周至少使用过一次的比例）、使用深度（适用决策中被系统处理的比例）、留存率（30天、60天、90天后仍然活跃的比例）、覆盖与修改率（输出被原样接受的比例），以及相对部署前基准线的结果增量。此外再配一份简短的月度问卷，询问用户系统在哪里出错，并对每一次上报做复盘。"),
 ("AI就绪的组织需要哪些角色？",
  "需要有预算权、并且愿意在流程需要时调整绩效目标的 executive sponsor；需要一个「翻译者」角色——分析工程师或AI产品经理——能把业务需求转化为可验证的用例；需要每个业务域的数据责任人，对定义与数据质量负责；还需要一位变革与赋能负责人，负责培训与用户反馈闭环。其中「翻译者」是最常见的缺口。"),
 ("如何应对员工对AI取代岗位的担忧？",
  "用具体性替代安慰。明确说明哪些任务将被自动化、哪些将被重新配比，以及组织对受影响员工的承诺——带带薪学习时间的再培训、内部转岗优先权，或有管理的自然减员。让受影响的团队参与新流程的设计，公开一项衡量工作方式变化的指标以便被检验，并让管理者承担起直接沟通的责任。"),
]

ZHCN = {"renames": ZHCN_RENAMES, "faq": ZHCN_FAQ,
        "excerpts": [
          "生成式AI在企业搜索中的应用：从检索到可信答案。",
          "用AI驱动的数据可视化，让洞察真正被看见。",
          "数据质量自动化：从被动响应走向主动治理。"]}

import _gb001_s2t as T
ZHTW = T.spec_s2tw(ZHCN)

if __name__ == "__main__":
    for lang, spec in (("en", EN), ("zh-CN", ZHCN), ("zh-TW", ZHTW)):
        b, a, n = apply(SLUG, lang, spec)
        print(f"{SLUG} {lang}: {b} -> {a}  [{', '.join(n)}]")
