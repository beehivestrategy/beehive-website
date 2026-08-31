#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "ai-agent-evaluation-metrics"

EN_SECTIONS = [
 ("how-do-you-evaluate-agent-behaviour-on-the-cases-that-matter",
  "How Do You Evaluate Agent Behaviour on the Cases That Matter?",
  """<p>An aggregate pass rate is the least useful number an evaluation programme can produce, because the failures that end a deployment are concentrated in a small slice of traffic. The fix is to stratify the golden set before you measure anything. Tag every case by workflow type, by data source, by whether it requires tool use, and by how consequential a wrong answer would be. Then report each stratum separately and set a floor for each, because a system can hold a 95% aggregate while failing 40% of the high-consequence cases — which is precisely the profile of an agent that gets switched off after one incident.</p>
<p>Build the case set from reality, not imagination. Mine production logs for the questions users actually asked, including the ones the system handled badly, and add the categories that pilots never cover: ambiguous requests, contradictory inputs, missing permissions, expired data, and instructions embedded in retrieved content. Weight the set toward the cases where a wrong action is expensive rather than toward the cases the system already handles well.</p>
<p>Then hold the set still. A golden set that is edited whenever the system fails will show constant improvement and measure nothing; add new cases on a schedule, version the set, and compare like with like.</p>"""),

 ("how-do-you-separate-model-regressions-from-system-failures",
  "How Do You Separate Model Regressions from System Failures?",
  """<p>When an agent's metrics drop, the cause is rarely the model. Agent performance is the product of a prompt, a retrieval layer, a tool set, an orchestration path, and a model, and any of them can change without a code change — a source system is updated, an index goes stale, an API tightens its schema, a prompt is edited in a content tool. Diagnostic value comes from attributing the failure to a layer before anyone starts tuning.</p>
<p>Run the evaluation suite at every layer. Component-level scores tell you whether each individual step still retrieves, classifies, or calls tools correctly. End-to-end scores tell you whether the composed system still completes tasks. When end-to-end drops but components hold, the fault is in composition or handoffs. When a single component drops, the fault is localised and usually cheap to fix. When both drop together, suspect the model or the data underneath it.</p>
<p>Two practices make this fast. Log the full trace of every evaluated run — plan, tool calls, inputs, outputs, timings — so a failing case can be replayed rather than re-run and guessed at. And pin your dependencies in evaluation: record the model version, prompt hash, index snapshot, and tool schema for every run, because a metric you cannot reproduce is a metric you cannot debug.</p>"""),

 ("how-do-you-evaluate-agent-safety-and-refusal-behaviour",
  "How Do You Evaluate Agent Safety and Refusal Behaviour?",
  """<p>Safety evaluation needs its own suite, because it is adversarial in a way task evaluation is not, and because the two desirable behaviours pull against each other: an agent that never acts is safe and useless, and one that always acts is useful until it is not.</p>
<p>Measure four things. Unauthorised action rate: how often the agent attempts a tool call, data access, or write outside its permitted scope, tested with red-team cases that embed instructions in retrieved documents, support tickets, and record fields. Sensitive-data leakage: whether outputs or logs expose data the requester should not see, tested with canary values planted in sources. Harmful-action severity: not just whether a violation occurred but what it would have cost, since a blocked export and a blocked payment are different events. And over-refusal rate: how often the agent declines a legitimate request it should have handled, which is the failure mode that quietly destroys adoption.</p>
<p>The balance is the point. Track safety and over-refusal together and tune them as a pair, because tightening guardrails always raises refusal, and the right setting is the one where high-consequence actions are gated while routine ones are not. Then keep the suite current: every production incident and every near miss becomes a permanent test case, so the evaluation programme learns at the same rate as the system.</p>"""),
]

EN_FAQ = [
 ("Which metrics matter most when evaluating AI agents?",
  "Five layers, not one score: task success rate including partial credit for multi-step tasks; reliability measured as consistency across runs, inputs, and time; safety measured as the rate and severity of unauthorised actions, data leaks, and consequential hallucinations; efficiency measured as cost per completed task, token use, and latency; and trust measured through override rates, abandonment, and post-deployment correction volume."),
 ("Why is a single accuracy score misleading for AI agents?",
  "Because agents take actions, not just produce text. An agent can complete a task and still be unsafe, expensive, or opaque; it can be correct on the happy path and destructive on the edge case; and it can pass every test while remaining distrusted by the people who supervise it. A single accuracy figure also hides concentration of failure — a system can hold a 95% aggregate while failing 40% of the high-consequence cases."),
 ("How do you build a golden set for agent evaluation?",
  "Mine production logs for what users actually asked, including cases the system handled badly, then add the categories pilots never cover: ambiguous requests, contradictory inputs, missing permissions, stale data, and instructions embedded in retrieved content. Stratify every case by workflow, data source, tool use, and consequence, report each stratum separately, and version the set so you compare like with like."),
 ("How can you tell whether a regression came from the model or the system?",
  "Score at every layer. If end-to-end results drop while component-level scores hold, the fault is in composition or handoffs. If a single component drops, the fault is localised. If both drop together, suspect the model or the underlying data. Pin model version, prompt hash, index snapshot, and tool schema for every run, and log full traces so failing cases can be replayed instead of guessed at."),
 ("How should agents be evaluated for safety?",
  "With a dedicated adversarial suite measuring four things: unauthorised action rate, tested by embedding instructions in retrieved content and record fields; sensitive-data leakage, tested with canary values; harmful-action severity, not just occurrence; and over-refusal rate, because an agent that declines legitimate work is safe and useless. Track safety and over-refusal as a pair and convert every incident into a permanent test case."),
]

EN_RENAMES = {
 "understanding-the-current-landscape": "What Does the Current Agent Evaluation Landscape Look Like?",
 "key-principles-and-strategic-framework": "Which Principles Should Guide Agent Evaluation?",
 "implementation-approach-and-best-practices": "What Implementation Approach and Best Practices Work?",
 "measuring-success-and-demonstrating-roi": "How Do You Measure Success and Demonstrate ROI?",
 "common-pitfalls-and-how-to-avoid-them": "What Are the Common Pitfalls and How Do You Avoid Them?",
 "key-takeaways": "What Are the Key Takeaways?",
 "conclusion": "What Should Teams Conclude About Agent Evaluation?",
}

EN = {"renames": EN_RENAMES, "sections": EN_SECTIONS, "faq": EN_FAQ,
      "excerpts": [
        "Building inclusive AI and data teams: what the evidence says actually changes outcomes.",
        "Why your data strategy needs a dedicated AI agent layer in 2026.",
        "Vector databases for enterprise search: a practical 2026 guide."]}

ZHCN_SECTIONS = [
 ("如何评估智能体在关键场景下的行为",
  "如何评估智能体在真正重要的场景下的行为？",
  """<p>聚合通过率是评估体系能产出的最没用的数字，因为终结一次部署的失败往往集中在很小一部分流量上。解决办法是在做任何度量之前先对黄金集分层。按工作流类型、数据来源、是否需要工具调用，以及错误答案的后果严重程度，为每一个用例打标签；然后分层单独报告，并为每层设定下限——因为一个系统完全可能在聚合层面保持95%，却在后果严重的用例上失败40%，而这正是一个在一次事故之后被关停的智能体的典型画像。</p>
<p>用例集要从现实中构建，而不是靠想象。从生产日志里挖掘用户真正问过的问题，包括系统处理得很糟的那些，并补上试点从不会覆盖的类别：模糊的请求、相互矛盾的输入、缺失的权限、过期的数据，以及嵌入在检索内容中的指令。让用例集向"做错代价高"的场景倾斜，而不是向系统已经处理得很好的场景倾斜。</p>
<p>然后把用例集固定住。一个每当系统失败就被修改的黄金集，只会显示出持续改善，却什么也没有度量；应当按节奏新增用例、对用例集做版本管理，并进行同类比较。</p>"""),

 ("如何区分模型回归与系统故障",
  "如何区分模型回归与系统故障？",
  """<p>当智能体的指标下滑时，原因很少是模型。智能体的表现是提示词、检索层、工具集、编排路径与模型共同作用的结果，其中任何一环都可能在没有代码变更的情况下发生变化——源系统被更新、索引变旧、API收紧了结构、提示词在内容工具里被改了一个字。真正的诊断价值在于，在任何调优开始之前先把失败归因到某一层。</p>
<p>在每一层都跑评估套件。组件级分数告诉你每个单独步骤是否仍然能正确检索、分类或调用工具；端到端分数告诉你组合后的系统是否仍能完成任务。当端到端下滑而组件保持时，问题出在组合或交接；当单个组件下滑时，问题被局部化，通常修复成本很低；当两者同时下滑时，应怀疑模型或其底层数据。</p>
<p>两项实践能让这个过程变快。记录每一次被评估运行的完整轨迹——规划、工具调用、输入输出与耗时——使失败的用例可以被重放，而不是重跑加猜测。并且在评估中固定依赖：为每次运行记录模型版本、提示词哈希、索引快照与工具结构，因为一个无法复现的指标就是一个无法调试的指标。</p>"""),

 ("如何评估智能体的安全性与拒答行为",
  "如何评估智能体的安全性与拒答行为？",
  """<p>安全性评估需要独立的套件，因为它在性质上是对抗性的，而任务评估不是；也因为两种可取的行为彼此拉扯：一个从不动手的智能体是安全的，也是无用的；一个总是动手的智能体则有用，直到它不再有用为止。</p>
<p>度量四件事。越权动作率：智能体尝试超出许可范围的工具调用、数据访问或写入的频率，用把指令嵌入检索文档、工单与记录字段的红队用例来测试。敏感数据泄露：输出或日志是否暴露了请求者不应看到的数据，用埋在数据源中的金丝雀值来测试。有害动作严重度：不只是违规是否发生，而是它本会造成多大代价——被拦截的导出与被拦截的付款是两种量级的事件。过度拒答率：智能体有多大比例拒绝了本应处理的合法请求，这是会悄悄摧毁采纳率的失败模式。</p>
<p>关键在于平衡。把安全性与过度拒答放在一起跟踪、成对调优，因为收紧护栏必然抬高拒答率，而正确的设置是高后果动作被设卡、日常动作不设卡。然后保持套件的时效性：每一次生产事故与每一次险情都变成永久测试用例，使评估体系与系统以同样的速度学习。</p>"""),
]

ZHCN_FAQ = [
 ("评估AI智能体时哪些指标最重要？",
  "是五层，而不是一个分数：任务成功率（多步任务需计算部分得分）；可靠性，即以跨运行、跨输入、跨时间的一致性来衡量；安全性，即以越权动作、数据泄露与会产生后果的幻觉的发生率和严重度来衡量；效率，即按每个已完成任务的成本、token消耗与延迟来衡量；以及信任，即通过覆盖修改率、放弃使用率与部署后的修正量来衡量。"),
 ("为什么单一的准确率对AI智能体具有误导性？",
  "因为智能体是在采取行动，而不只是产出文本。一个智能体可以完成任务却依然不安全、昂贵或不透明；可以在顺利路径上正确，却在边界场景上具有破坏性；也可以通过所有测试，却始终不被必须监督它的人信任。单一的准确率还会掩盖失败的集中程度——一个系统完全可能在聚合层面保持95%，却在后果严重的用例上失败40%。"),
 ("如何构建智能体评估的黄金集？",
  "从生产日志中挖掘用户真正问过的问题，包括系统处理得很糟的那些，然后补上试点从不覆盖的类别：模糊请求、矛盾输入、缺失权限、过期数据，以及嵌入检索内容中的指令。按工作流、数据来源、工具调用与后果严重程度对每个用例分层，分层单独报告，并对用例集做版本管理以便同类比较。"),
 ("如何判断指标下滑来自模型还是系统？",
  "在每一层都打分。如果端到端结果下滑而组件级分数保持，问题出在组合或交接；如果单个组件下滑，问题被局部化；如果两者同时下滑，应怀疑模型或其底层数据。为每次运行固定模型版本、提示词哈希、索引快照与工具结构，并记录完整轨迹，使失败用例可以被重放而不是靠猜测。"),
 ("智能体的安全性应当如何评估？",
  "用专门的对抗性套件度量四件事：越权动作率（通过把指令嵌入检索内容与记录字段来测试）、敏感数据泄露（用金丝雀值测试）、有害动作严重度（而不只是是否发生），以及过度拒答率（因为拒绝合法工作的智能体既安全又无用）。把安全性与过度拒答作为一对指标跟踪，并把每次事故转化为永久测试用例。"),
]

ZHCN_RENAMES = {
 "理解当前格局": "当前智能体评估的格局是怎样的？",
 "关键原则与战略框架": "哪些原则应该指导智能体评估？",
 "实施方法与最佳实践": "什么样的实施方法与最佳实践有效？",
 "衡量成功与展示投资回报率": "如何衡量成功并展示投资回报？",
 "常见陷阱及规避方法": "常见的陷阱有哪些，如何规避？",
 "关键要点": "有哪些关键要点？",
 "结论": "团队应该对智能体评估得出什么结论？",
}

ZHCN = {"renames": ZHCN_RENAMES, "sections": ZHCN_SECTIONS, "faq": ZHCN_FAQ,
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
