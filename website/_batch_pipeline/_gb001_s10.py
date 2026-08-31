#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "ai-agent-frameworks-comparison-may-2025"

EN_SECTIONS = [
 ("how-do-the-leading-frameworks-compare-on-the-decisions-that-matter",
  "How Do the Leading Frameworks Compare on the Decisions That Matter?",
  """<p>Feature matrices age badly, so compare frameworks on the decisions you will actually have to live with. Four axes separate them in practice.</p>
<ul>
<li><strong>Control versus speed.</strong> LangGraph gives you the most control — you define the graph, the edges, and the state transitions explicitly, which means you can reason about and test every path, at the cost of writing more code. CrewAI optimises for speed: role-based crews assemble in a few lines and produce working multi-agent behaviour quickly, with less control over the exact execution path. AutoGen sits between them, making multi-agent conversation the primitive and letting you shape the dialogue.</li>
<li><strong>Fit with your stack.</strong> If your engineering organisation is .NET-centric, Semantic Kernel is the natural path and the others will feel foreign. If your problem is primarily retrieval over a large document estate, LlamaIndex solves the part that usually consumes the project.</li>
<li><strong>Operational maturity.</strong> Ask specifically about tracing, replay, and evaluation hooks. A framework that cannot show you the full trace of a run will be painful the first time something goes wrong in production, and by then switching is expensive.</li>
<li><strong>Ecosystem gravity.</strong> Frameworks with large communities get connectors, examples, and fixes faster. This is the least technical axis and often the most decisive one for a small team.</li>
</ul>
<p>The pragmatic answer for most enterprises is to pick the framework that matches how your team already thinks about the problem, and to keep the framework at arm's length from the rest of the architecture so the choice stays reversible.</p>"""),

 ("which-integration-patterns-matter-more-than-framework-choice",
  "Which Integration Patterns Matter More Than Framework Choice?",
  """<p>Teams spend weeks comparing frameworks and then lose months to integration. Four patterns do more for production outcomes than the framework decision, and all four are worth designing before the first agent is written.</p>
<p>Keep the framework behind an interface. Your agents should call your own service layer rather than reaching into systems directly, so tool implementations can be tested once, permissioned once, and reused across frameworks. When a tool call is a call to your API, the framework becomes an orchestration detail rather than an architectural commitment.</p>
<p>Resolve permissions at the boundary, not in the prompt. Every tool call should carry the requesting identity and be authorised against source-system entitlements at execution time. Frameworks do not do this for you, and it is the difference between a contained mistake and a data incident.</p>
<p>Make state durable outside the framework. Persist run state, evidence, and outcomes in your own store so a run can be resumed, replayed, and audited independently of whichever framework produced it. And instrument from day one: emit a trace for every plan step, tool call, and result, with the model version and prompt hash attached, because the first production incident will be debugged from those traces.</p>"""),

 ("how-do-you-keep-the-framework-choice-reversible",
  "How Do You Keep the Framework Choice Reversible?",
  """<p>The agent framework market is young enough that whichever you choose will look different in two years, and several teams have already been through a migration. Reversibility is therefore worth designing in, and it costs less than it sounds.</p>
<p>Isolate three things. Agent logic — prompts, tool definitions, and handoff contracts — should live in your repository as versioned artefacts rather than inside framework-specific objects, so the same logic can be re-hosted. Tool implementations should be plain services with a stable interface, called by thin framework adapters. Evaluation should be external: a golden set of tasks and a scoring harness that run against the deployed system, not against framework internals, so a migration can be validated by comparing scores rather than by re-testing everything by hand.</p>
<p>Then set a trigger for revisiting the choice rather than revisiting it continuously: a framework change should be considered when a required capability is missing, when operational pain is measurable, or when the ecosystem has clearly consolidated — and not because a new release looked interesting. Migrations that follow that discipline are routine; migrations driven by novelty are what produce the stalled rewrites that give agent projects their cancellation statistics.</p>"""),
]

EN_FAQ = [
 ("Which AI agent framework should our team choose in 2025?",
  "There is no single best framework, only a best fit. Choose LangGraph when you need explicit control over state and execution paths and can afford more engineering. Choose CrewAI when speed matters and role-based crews map naturally onto the work. Choose AutoGen when multi-agent conversation is the natural primitive. Choose Semantic Kernel in a .NET-centric organisation, and LlamaIndex when the hard part is retrieval over a large document estate."),
 ("What matters more than the framework choice?",
  "Integration patterns. Keep the framework behind your own service interface so tool implementations are written, tested, and permissioned once; resolve permissions at execution time against source-system entitlements rather than in the prompt; persist run state outside the framework so runs can be replayed and audited; and emit traces for every plan step and tool call from day one."),
 ("Are AI agent frameworks production-ready?",
  "Yes, with caveats. The frameworks converged on shared primitives — planning, tool use, memory, and hand-off — and the surrounding infrastructure matured through the Model Context Protocol, which removed much of the bespoke connector work. The caveat is operational: production readiness depends less on the framework than on whether you have evaluation, tracing, permission enforcement, and run controls around it."),
 ("How do you avoid being locked into one agent framework?",
  "Isolate agent logic as versioned artefacts in your own repository rather than framework objects, implement tools as plain services behind thin framework adapters, and keep evaluation external so a migration can be validated by comparing golden-set scores. Then revisit the choice only on a defined trigger — a missing capability, measurable operational pain, or clear ecosystem consolidation."),
 ("How should enterprises evaluate agent frameworks on cost?",
  "Measure cost per completed task rather than cost per call, because frameworks differ in how many model round trips an orchestrated task requires. Track token consumption, the number of tool calls per task, retry behaviour on failure, and p95 latency, then run the same golden set of tasks across candidate frameworks and compare those four numbers directly."),
]

EN_RENAMES = {
 "understanding-the-current-technology-landscape": "What Does the Current Agent Framework Landscape Look Like?",
 "technical-architecture-and-integration-patterns": "Which Technical Architecture and Integration Patterns Work Best?",
 "performance-benchmarks-and-optimization-strategies": "How Do You Benchmark and Optimize Agent Framework Performance?",
 "from-framework-choice-to-production-value": "How Do You Turn Framework Choice into Production Value?",
}

EN = {"renames": EN_RENAMES, "sections": EN_SECTIONS, "faq": EN_FAQ,
      "excerpts": [
        "How to architect enterprise AI agents: the runtime, tool, and memory layers that make them dependable.",
        "Using AI scenario planning to stress-test supply chains before disruption hits.",
        "Demand sensing with AI: shortening the signal-to-decision loop in volatile markets."]}

ZHCN_RENAMES = {
 "理解当前技术格局": "当前智能体框架的格局是怎样的？",
 "技术架构与集成模式": "哪些技术架构与集成模式最有效？",
 "性能基准与优化策略": "如何做智能体框架的性能基准与优化？",
 "企业部署最佳实践与实施建议": "企业部署有哪些最佳实践与实施建议？",
 "企业实施路线图与成功因素": "企业实施路线图与关键成功因素是什么？",
 "战略实施路径与关键成功因素": "战略实施路径应如何设计？",
 "企业实施路线图与成功因素-2": "企业实施路线图中最容易被忽略的是什么？",
}

ZHCN_FAQ = [
 ("2025年团队应该选择哪个AI智能体框架？",
  "没有唯一的最佳框架，只有最合适的选择。当你需要对状态与执行路径有显式控制、并且能够投入更多工程资源时，选择 LangGraph；当速度至关重要、且基于角色的团队能自然映射到实际工作时，选择 CrewAI；当多智能体对话是最自然的抽象时，选择 AutoGen；在以 .NET 为核心的组织中选择 Semantic Kernel；而当难点在于对大规模文档资产的检索时，选择 LlamaIndex。"),
 ("比框架选择更重要的是什么？",
  "是集成模式。把框架放在你自己的服务接口之后，使工具实现只编写、测试和授权一次；在执行时依据源系统的权限体系做鉴权，而不是在提示词里做；把运行状态持久化在框架之外，使每次运行可以被重放与审计；并从第一天起为每一个规划步骤与工具调用输出追踪记录。"),
 ("AI智能体框架是否已经可用于生产？",
  "可以，但有前提。各框架已经收敛到共同的抽象——规划、工具调用、记忆与交接——而周边基础设施通过模型上下文协议走向成熟，省去了大量定制连接器的工作。前提在运营层面：能否用于生产，更多取决于你是否在其外围建立了评估、追踪、权限执行与运行控制，而不是框架本身。"),
 ("如何避免被单一智能体框架锁定？",
  "把智能体逻辑作为版本化资产存放在自己的代码库中，而不是塞进框架特有的对象里；把工具实现做成纯服务，由薄的框架适配层调用；并保持评估的外部化，使迁移可以通过对比黄金集得分来验证。此后只在明确的触发条件下重新审视选择——能力缺失、运营痛苦可量化，或生态明显整合完成。"),
 ("企业应如何评估智能体框架的成本？",
  "按每个已完成任务的成本衡量，而不是按每次调用的成本，因为不同框架完成一个被编排的任务所需的模型往返次数不同。跟踪 token 消耗、每任务的工具调用次数、失败时的重试行为与 p95 延迟，然后用同一份任务黄金集在各候选框架上运行，直接比较这四项数字。"),
]

ZHCN = {"renames": ZHCN_RENAMES, "faq": ZHCN_FAQ,
        "excerpts": [
          "企业AI智能体的架构方法：让系统可靠的运行时、工具与记忆三层设计。",
          "用AI情景规划在供应链受扰动之前完成压力测试。",
          "用AI做需求感知，缩短波动市场中的信号到决策链路。"]}

import _gb001_s2t as T
ZHTW = T.spec_s2tw(ZHCN)

if __name__ == "__main__":
    for lang, spec in (("en", EN), ("zh-CN", ZHCN), ("zh-TW", ZHTW)):
        b, a, n = apply(SLUG, lang, spec)
        print(f"{SLUG} {lang}: {b} -> {a}  [{', '.join(n)}]")
