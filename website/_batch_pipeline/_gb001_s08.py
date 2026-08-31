#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "ai-agent-composition-patterns"

EN_SECTIONS = [
 ("how-do-you-choose-between-composition-patterns",
  "How Do You Choose Between Composition Patterns for a Given Workflow?",
  """<p>The choice is determined by three properties of the workflow: whether the decomposition is knowable in advance, whether the steps are ordered, and where approval authority sits. Map those three and the pattern usually selects itself.</p>
<ul>
<li><strong>Pipeline</strong> when the steps are known, ordered, and produce one artifact each — report generation, data ingestion, document processing. It is the right default because it is the easiest to test and the cheapest to run.</li>
<li><strong>Orchestrator–worker</strong> when the work can be decomposed but the decomposition depends on the input — multi-source analysis, "explain this variance", research questions where the right sub-queries differ each time. You pay for a planning step and you gain a single control point.</li>
<li><strong>Blackboard</strong> when you cannot know the decomposition in advance at all — exploratory research synthesis, open-ended incident triage, situations where agents should contribute whatever they find to a shared workspace and the stopping condition is judgement rather than a plan.</li>
<li><strong>Hierarchy</strong> when the workflow already mirrors an approval structure — procurement above a threshold, anything with a compliance gate — because authority and escalation are part of the requirement rather than an afterthought.</li>
</ul>
<p>Most production systems are hybrids, and the usual shape is a pipeline shell with an orchestrator inside one or two stages. Resist the urge to pick one pattern for the whole estate; choose per workflow and document why, because the reason is what a future maintainer will need.</p>"""),

 ("what-does-a-well-defined-handoff-contract-look-like",
  "What Does a Well-Defined Handoff Contract Look Like?",
  """<p>Handoffs are where composed systems fail, and they fail quietly: an agent receives a slightly wrong artifact, produces a confidently wrong result, and the error is only visible several stages downstream. The fix is a contract between every pair of agents, and a contract means more than a shared data structure.</p>
<p>A usable contract has five parts. The schema defines the fields and their types, so a malformed artifact is rejected at the boundary rather than absorbed. The semantics define what each field means, in the terms of the domain — a "customer" in one agent's output is not necessarily the same entity as a "customer" in the next agent's input, and naming that difference prevents a whole class of silent error. The provenance records which agent produced the artifact, from which sources, at what time, so downstream consumers can decide how much to trust it.</p>
<p>The validation rules state what must be true before the artifact is accepted — non-empty, within a range, internally consistent — and what happens when validation fails: retry, escalate, or stop. And the failure semantics state whether the receiving agent should proceed with a partial artifact or halt, because "proceed with best effort" is the right answer in some workflows and catastrophic in others.</p>
<p>Write these down per boundary and test them explicitly. A system with five explicit contracts is more maintainable than a system with twenty agents and implicit assumptions.</p>"""),

 ("how-do-you-manage-state-and-memory-across-composed-agents",
  "How Do You Manage State and Memory Across Composed Agents?",
  """<p>State is the hardest part of composition because every pattern distributes it differently, and the failure modes are all variations on two themes: agents disagreeing about what is true, and agents losing what they knew.</p>
<p>Separate three kinds of state. Execution state is the progress of this run — which steps completed, what each produced, what is pending. It belongs in the orchestrator, in a durable store, so a failed run can be resumed rather than restarted. Shared context is the accumulated evidence all agents need — retrieved documents, tool results, intermediate calculations. It belongs in a shared, append-only workspace with explicit provenance, so two agents can disagree in the record rather than overwrite each other. Agent-local memory is the scratch state a single agent needs to do its job, and it should stay local so it cannot contaminate others.</p>
<p>Three rules keep this manageable. Make writes explicit and attributed, so any value can be traced to the agent and the step that produced it. Prefer append over overwrite for shared context, because an overwritten value destroys the audit trail that post-incident review depends on. And bound the context deliberately: what gets passed to the next agent should be an explicit selection, not "everything so far", because unbounded context raises cost and dilutes the signal.</p>"""),

 ("how-do-you-test-a-multi-agent-system-before-production",
  "How Do You Test a Multi-Agent System Before Production?",
  """<p>Testing composed agents requires three layers, and most teams build only the first. Component tests check each agent in isolation against a fixed set of inputs and expected outputs, with its tools mocked. These catch prompt regressions and parsing errors, and they are the cheapest layer to build and run.</p>
<p>Contract tests check the boundaries: for every handoff, feed malformed, incomplete, and adversarial artifacts and assert that the receiver rejects, retries, or escalates as designed. This is the layer that catches the silent corruption described above, and it is the one most often skipped because the artifacts look fine in normal operation.</p>
<p>End-to-end tests run complete workflows against a golden set of realistic tasks with verified outcomes, and they are the layer that tells you whether the system actually works. Score them on task completion, correctness of the final artifact, cost and latency per run, and the rate of correct refusals. Wire them into deployment as a gate, re-running on every prompt, tool, or model change, and slice results by workflow type — an aggregate pass rate will hide a single workflow that has quietly broken.</p>
<p>Add two production-layer practices: replay, so any failed run can be reconstructed step by step from logged inputs, and shadow mode, so a candidate change can run alongside the current system and be compared before it is promoted.</p>"""),
]

EN_FAQ = [
 ("What is agent composition in AI systems?",
  "Agent composition is how you divide a workflow among specialised AI agents and coordinate their work — the decomposition, the orchestration pattern, the handoff contracts, and the guardrails that bind them. It matters because most production failures in agentic systems come from composition rather than model quality: wrong tool calls, stale data, permission errors, and silent partial completions all occur at the seams between agents."),
 ("Which agent composition pattern should we use?",
  "Match the pattern to the workflow. Use a pipeline when steps are known, ordered, and produce one artifact each. Use orchestrator–worker when decomposition depends on the input. Use a blackboard when the decomposition cannot be known in advance, such as exploratory synthesis. Use a hierarchy when the workflow mirrors an approval structure with escalating authority. Most production systems are hybrids — commonly a pipeline shell with an orchestrator inside one or two stages."),
 ("How many agents is too many?",
  "Start with the smallest number that covers the workflow, and split an agent only when its charter becomes ambiguous or its tool set grows incompatible. If a step can be expressed as a function, a prompt, or a deterministic rule, it should be — agents earn their place only where judgement, tool use, or adaptation to unstructured input is genuinely required. Cost, complexity, and orchestration surface all rise superlinearly with agent count."),
 ("How do you prevent errors at agent handoffs?",
  "Define an explicit contract at every boundary with five parts: schema, semantics, provenance, validation rules, and failure semantics. The contract should state what must be true before an artifact is accepted and what happens when validation fails — retry, escalate, or stop. Then test those boundaries deliberately with malformed and incomplete inputs, because handoff errors are invisible in normal operation and expensive several stages downstream."),
 ("How should state be shared between composed agents?",
  "Separate three kinds. Execution state — progress of the run — belongs in the orchestrator in a durable store so failed runs can resume. Shared context — evidence all agents need — belongs in an append-only workspace with explicit provenance so agents can disagree in the record rather than overwrite each other. Agent-local scratch state stays local. Prefer append over overwrite, attribute every write, and pass an explicit selection forward rather than everything so far."),
]

EN_RENAMES = {
 "understanding-the-current-landscape": "What Does the Current Agent Composition Landscape Look Like?",
 "key-principles-and-strategic-framework": "Which Principles Should Guide Agent Composition?",
 "implementation-approach-and-best-practices": "What Implementation Approach and Best Practices Work?",
 "measuring-success-and-demonstrating-roi": "How Do You Measure Success and Demonstrate ROI?",
 "common-pitfalls-and-how-to-avoid-them": "What Are the Common Pitfalls and How Do You Avoid Them?",
 "key-takeaways": "What Are the Key Takeaways?",
 "conclusion": "What Should Engineering Leaders Conclude?",
}

EN = {"renames": EN_RENAMES, "sections": EN_SECTIONS, "faq": EN_FAQ,
      "excerpts": [
        "Building inclusive AI and data teams: what the evidence says actually changes outcomes.",
        "Why your data strategy needs a dedicated AI agent layer in 2026.",
        "Vector databases for enterprise search: a practical 2026 guide."]}

ZHCN_SECTIONS = [
 ("如何在组合模式之间做选择",
  "如何为给定的工作流选择组合模式？",
  """<p>选择取决于工作流的三个属性：拆解方式是否可预先确定、步骤之间是否有序、以及审批权落在哪里。把这三个问题回答清楚，模式通常会自己浮现。</p>
<ul>
<li><strong>流水线：</strong>当步骤已知、有序、且每步产出一个交付物时——报告生成、数据接入、文档处理。它是正确的默认选择，因为最容易测试、运行成本最低。</li>
<li><strong>编排者—工作者：</strong>当工作可以拆解、但拆解方式取决于输入时——多源分析、"解释这个差异"、每次子查询都不同的研究性问题。你需要为一个规划步骤付费，换来的是一个统一的控制点。</li>
<li><strong>黑板模式：</strong>当拆解方式完全无法预先得知时——探索性的研究综合、开放式的事件分诊、智能体应当把各自发现共享到公共工作区、且停止条件是判断而非计划的情境。</li>
<li><strong>层级模式：</strong>当工作流本身就映射了审批结构时——超过阈值的采购、任何带合规关卡的流程——因为权限与上报是需求的一部分，而不是事后补充。</li>
</ul>
<p>多数生产系统都是混合形态，最常见的形状是"流水线外壳 + 内部一到两个阶段的编排者"。不要为整个技术栈强行选定一种模式；按工作流分别选择并记录理由，因为理由正是未来的维护者最需要的东西。</p>"""),

 ("一份定义良好的交接契约是什么样的",
  "一份定义良好的交接契约是什么样的？",
  """<p>交接是组合系统失败的地方，而且失败得很安静：某个智能体收到一个略微错误的交付物，产出一个自信的错误结果，而错误要到下游好几步之后才可见。解决办法是每对智能体之间都有一份契约，而契约的含义不止是共享的数据结构。</p>
<p>一份可用的契约包含五个部分。模式定义字段与类型，使畸形的交付物在边界处被拒绝，而不是被吸收。语义定义每个字段在业务语境中的含义——一个智能体输出中的"客户"，未必与下一个智能体输入中的"客户"是同一个实体，把这种差异讲清楚，可以消除一整类静默错误。溯源记录交付物由哪个智能体、基于哪些来源、在什么时间产出，让下游消费者可以判断该信任它多少。</p>
<p>校验规则说明交付物被接受之前必须成立的条件——非空、落在区间内、内部一致——以及校验失败时怎么办：重试、上报还是终止。失败语义说明接收方应当带着不完整的交付物继续，还是停下来，因为"尽力而为"在有些工作流里是正确答案，在另一些里是灾难。</p>
<p>在每个边界上把这些写出来并显式测试。一个有五份显式契约的系统，比一个由二十个智能体和一堆隐含假设构成的系统更可维护。</p>"""),

 ("如何在组合的智能体之间管理状态与记忆",
  "如何在组合的智能体之间管理状态与记忆？",
  """<p>状态是组合中最困难的部分，因为每种模式分发状态的方式都不同，而所有失败模式都是两个主题的变体：智能体对"什么是真的"产生分歧，以及智能体丢失了它们曾经知道的东西。</p>
<p>把状态分成三类。执行状态是本次运行的进度——哪些步骤已完成、各自产出了什么、什么还在等待。它属于编排者，存放在持久化存储中，使失败的运行可以被恢复而不是重启。共享上下文是所有智能体都需要的累积证据——检索到的文档、工具结果、中间计算。它属于一个共享的、仅追加的工作区，并带有显式溯源，使两个智能体可以在记录中保留分歧，而不是互相覆盖。智能体本地记忆是单个智能体完成自身工作所需的暂存状态，应当保持本地，避免污染其他智能体。</p>
<p>三条规则让这一切可控。写入必须显式且可归属，使任何数值都能追溯到产出它的智能体与步骤。共享上下文优先追加而非覆盖，因为被覆盖的数值会毁掉事后复盘所依赖的审计线索。并且要有意识地约束上下文：传递给下一个智能体的内容应该是显式挑选出来的，而不是"目前为止的全部"——无界的上下文会推高成本并稀释信号。</p>"""),

 ("如何在投产前测试多智能体系统",
  "如何在投产前测试多智能体系统？",
  """<p>测试组合式智能体需要三层，而多数团队只建了第一层。组件测试在隔离环境中，用固定的输入集与预期输出、并把工具打桩，来检查每个智能体。它们能捕捉提示词回归与解析错误，也是构建和运行成本最低的一层。</p>
<p>契约测试检查边界：对每一处交接，喂入畸形、不完整与对抗性的交付物，并断言接收方按设计拒绝、重试或上报。这是能捕捉上述静默损坏的一层，也最常被跳过，因为在正常运行中交付物看起来都很好。</p>
<p>端到端测试用一份贴近真实、结果经过验证的任务黄金集跑完整工作流，这是能告诉你系统是否真的可用的那一层。按任务完成率、最终交付物的正确性、每次运行的成本与延迟、以及正确拒答率来打分。把它们接入部署流程作为关卡，在每次提示词、工具或模型变更时重跑，并按工作流类型拆分结果——聚合的通过率会掩盖某一条工作流已经悄悄失效的事实。</p>
<p>再补充两项生产层实践：重放，使任何失败的运行都能依据记录的输入被逐步重建；以及影子模式，使候选变更在晋升之前可以与当前系统并行运行并做对比。</p>"""),
]

ZHCN_FAQ = [
 ("什么是AI系统中的智能体组合？",
  "智能体组合是指如何把一个工作流拆分给若干专业化的AI智能体、并协调它们的工作——包括拆解方式、编排模式、交接契约以及约束它们的护栏。它之所以重要，是因为智能体系统在生产中多数失败来自组合而非模型质量：错误的工具调用、过期数据、权限错误与静默的部分完成，都发生在智能体之间的接缝处。"),
 ("我们应该采用哪种智能体组合模式？",
  "让模式匹配工作流。步骤已知、有序且每步产出一个交付物时用流水线；拆解方式取决于输入时用编排者—工作者；拆解方式完全无法预先得知时（如探索性综合）用黑板模式；工作流本身映射了带逐级授权的审批结构时用层级模式。多数生产系统是混合形态，常见形状是流水线外壳加内部一到两个阶段的编排者。"),
 ("多少个智能体算太多？",
  "从能覆盖工作流的最小数量起步，只有当某个智能体的职责变得模糊、或它的工具集变得互不相容时才拆分。如果一个步骤可以用函数、提示词或确定性规则表达，那就应该那样做——只有在确实需要判断、工具调用或适应非结构化输入时，智能体才配占一个位置。成本、复杂度与编排面积都随智能体数量呈超线性增长。"),
 ("如何防止智能体交接处出错？",
  "在每个边界定义一份显式契约，包含五个部分：模式、语义、溯源、校验规则与失败语义。契约应说明交付物被接受之前必须成立的条件，以及校验失败时的处理方式——重试、上报还是终止。然后用畸形与不完整的输入显式测试这些边界，因为交接错误在正常运行中不可见，却会在下游好几步之后造成昂贵代价。"),
 ("组合的智能体之间应如何共享状态？",
  "分成三类。执行状态（本次运行进度）属于编排者，存放在持久化存储中，使失败的运行可以恢复；共享上下文（所有智能体都需要的证据）属于仅追加的工作区并带显式溯源，使智能体可以在记录中保留分歧而非互相覆盖；智能体本地的暂存状态保持本地。优先追加而非覆盖，每次写入都要可归属，并显式挑选向前传递的内容，而不是把到目前为止的全部都传下去。"),
]

ZHCN_RENAMES = {
 "理解当前格局": "当前智能体组合的格局是怎样的？",
 "关键原则与战略框架": "哪些原则应该指导智能体组合？",
 "实施方法与最佳实践": "什么样的实施方法与最佳实践有效？",
 "衡量成功与展示投资回报率": "如何衡量成功并展示投资回报？",
 "常见陷阱及规避方法": "常见的陷阱有哪些，如何规避？",
 "关键要点": "有哪些关键要点？",
 "结论": "工程负责人可以得出什么结论？",
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
