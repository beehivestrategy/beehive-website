#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "ai-agent-orchestration-2026"

EN_RENAMES = {
 "understanding-the-current-landscape": "What Does the Current Agent Orchestration Landscape Look Like?",
 "key-principles-and-strategic-framework": "Which Principles Should Guide Agent Orchestration?",
 "implementation-approach-and-best-practices": "What Implementation Approach and Best Practices Work?",
 "measuring-success-and-demonstrating-roi": "How Do You Measure Success and Demonstrate ROI?",
 "common-pitfalls-and-how-to-avoid-them": "What Are the Common Pitfalls and How Do You Avoid Them?",
 "practical-first-steps": "What Are the Practical First Steps?",
 "key-takeaways": "What Are the Key Takeaways?",
 "conclusion": "What Should Teams Conclude About Orchestration?",
}

EN_FAQ = [
 ("What is AI agent orchestration?",
  "It is the layer that plans, routes, and supervises the work of one or more agents — deciding which agent handles which step, passing state between them, enforcing permissions at each tool call, and handling failure and escalation. Orchestration is what turns a collection of capable agents into a dependable business process, and it is where most production engineering effort now sits."),
 ("How is orchestration different from choreography?",
  "Orchestration uses a central controller that directs each step and holds the state, which gives you one place to log, enforce policy, and recover from failure. Choreography lets agents react to events independently, which scales better and couples services less tightly but makes global behaviour harder to reason about and audit. Most enterprises start with orchestration and introduce choreography only where the coordination overhead becomes the constraint."),
 ("What are the building blocks of production orchestration?",
  "A planner that decomposes the request, a registry of agents and their capabilities, a durable state store that survives failures, a tool gateway that enforces schema validation and per-call authorisation, a policy engine that applies guardrails, a human-in-the-loop escalation path, and tracing that records every step with its inputs and outputs so any run can be replayed."),
 ("How do you scale orchestration without breaking trust?",
  "Scale the control plane before the agent count. Enforce permissions at call time rather than in prompts, keep state durable and attributed so runs can be replayed, publish confidence with every recommendation, and make escalation a named role rather than a queue. Then instrument adoption — override rates, abandonment, and correction volume — because trust failures appear in usage long before they appear in accuracy metrics."),
 ("What are the most common orchestration failure modes?",
  "Silent partial completion, where a step fails and downstream agents proceed on incomplete state; permission drift, where an agent accumulates access beyond its original charter; cost runaway from unbounded retry loops; context bloat, where everything so far is passed forward and dilutes the signal; and orchestration sprawl, where too many agents make the system impossible to reason about or test."),
]
EN = {"renames": EN_RENAMES, "faq": EN_FAQ,
      "excerpts": [
        "How to architect enterprise AI agents: the runtime, tool, and memory layers that make them dependable.",
        "Using AI scenario planning to stress-test supply chains before disruption hits.",
        "Demand sensing with AI: shortening the signal-to-decision loop in volatile markets."]}

# ------------------------------------------------------------------ zh-CN
ZHCN_SECTIONS = [
 ("编排中的状态与上下文应如何管理",
  "编排中的状态与上下文应如何管理？",
  """<p>编排的复杂度大多来自状态，而不是来自智能体本身。把状态分成三类处理，系统就会清晰很多。执行状态记录本次运行进度——哪些步骤完成、产出什么、什么在等待；它属于编排者，存放在持久化存储中，使失败的运行可以恢复而不是重启。共享上下文是所有智能体都需要的证据——检索结果、工具返回、中间计算；它属于一个仅追加的工作区，并带显式溯源，使两个智能体可以在记录中保留分歧，而不是互相覆盖。智能体本地记忆则是单个智能体完成自身工作所需的暂存状态，应当保持本地，避免污染他人。</p>
<p>三条规则让状态可控：写入必须可归属，任何数值都能追溯到产出它的智能体与步骤；共享上下文优先追加而非覆盖，因为覆盖会毁掉事后复盘所依赖的审计线索；以及向前传递的内容必须显式挑选，而不是把"目前为止的全部"都传下去——无界的上下文既推高成本，也稀释了模型真正需要的信号。</p>
<p>还有一个常被忽略的细节：上下文需要有过期机制。检索到的证据应当带上来源与时间戳，超时的证据应被重新获取或在回答中被标注为陈旧，否则系统会在数据已经变化之后继续自信地引用旧值。</p>"""),

 ("编排层需要哪些可观测性能力",
  "编排层需要哪些可观测性能力？",
  """<p>可观测性决定了编排系统能否被运维。最低要求是为每一次运行产出一条可回放的追踪记录：请求者身份、规划步骤、每一次工具调用及其入参与返回值、所用数据的来源与版本、策略判定结果、耗时与成本。缺少任何一项，事故复盘都会退化成猜测。</p>
<p>在此之上需要四类信号。指标：任务完成率、各步骤耗时分布、每次运行的成本、重试次数、升级到人工的比例。日志：结构化、可检索，并能关联到业务标识——客户、订单、工单，因为问题通常以业务语言被提出。告警：针对越权调用、权限漂移、成本突增、异常动作序列与静默的部分完成。追踪：跨智能体的调用链，使一次失败可以被逐步重放。</p>
<p>最后是评估闭环。把生产中的失败与险情持续转化为黄金集用例，并在每次提示词、工具或模型变更后重跑。可观测性如果只用于排障，价值只兑现了一半；把它接到评估上，系统才会随运行时间变得更好，而不是仅仅更容易被解释。</p>"""),

 ("编排的成熟度应如何分阶段推进",
  "编排的成熟度应如何分阶段推进？",
  """<p>把编排一次性建成平台，是这类项目最常见的失败方式。更可靠的路径是分四步走，每一步都产出可验证的东西。</p>
<ul>
<li><strong>第一步，单一闭环：</strong>选一个高价值、边界清晰的决策——报告生成、异常分诊、问询答复——用最少的智能体跑通，并建立对照基准。产出：一个季度内可衡量的价值证据。</li>
<li><strong>第二步，共享底座：</strong>把工具网关、权限执行、状态存储与追踪抽象出来，供后续所有工作流复用。产出：新增工作流的边际成本显著下降。</li>
<li><strong>第三步，治理与准入：</strong>建立智能体注册表、策略即代码的护栏、审批关卡与审计线索。产出：可以通过合规与安全评审的准入流程。</li>
<li><strong>第四步，规模化运营：</strong>编排指标进入经营看板，新工作流按模板自助接入，历史决策可追溯可解释。产出：编排成为常规能力而非项目。</li>
</ul>
<p>判断何时进入下一步的标准很朴素：上一步的产出是否已经被量化验证。提前进入第三步的组织，通常会在治理上投入大量精力，却还没有一个真正被使用的闭环。</p>"""),

 ("如何控制编排的成本",
  "如何控制编排的成本？",
  """<p>编排系统的成本超支几乎总是源于三个可预防的原因。第一是重试循环没有上限：自我修正在缺少约束时会不断重试，而且往往恰好在那些已经失败的困难问题上消耗最多。应当显式设定重试次数与总预算，超过即停止并交人工。第二是上下文无界：把到目前为止的全部内容都传递给下一步，token 成本随步骤数呈平方级增长，同时还会降低答案质量。应当显式挑选向前传递的内容。</p>
<p>第三是模型选型单一：用前沿模型去做分类、路由与重排这类简单任务。把小模型用在简单步骤、前沿模型只用于最终综合与需要判断的环节，通常能在不牺牲质量的前提下显著降低单次运行成本。</p>
<p>管理上要按"每个已完成任务的成本"来衡量，而不是按每次调用的成本——前者才与业务价值对齐。再加两个护栏：缓存可复用的检索结果与工具返回，并在数据源更新时失效；以及为每个工作流设定成本预算与告警阈值，让超支在当天被发现，而不是在月度账单里。</p>"""),
]

ZHCN_FAQ = [
 ("什么是AI智能体编排？",
  "它是规划、路由与监督一个或多个智能体工作的那一层：决定哪个智能体处理哪个步骤、在它们之间传递状态、在每次工具调用时执行权限校验，并处理失败与上报。编排把一组各有所长的智能体变成一个可依赖的业务流程，也是当前生产工程中投入最集中的地方。"),
 ("编排与协同有什么区别？",
  "编排由一个中央控制器指挥每一步并持有状态，因此有统一的记录、策略执行与故障恢复位置。协同让智能体各自对事件做出反应，扩展性更好、耦合更松，但整体行为更难被推理和审计。多数企业从编排起步，只有当协调开销真正成为瓶颈时，才在局部引入协同。"),
 ("生产级编排由哪些基础构件组成？",
  "包括：拆解请求的规划器；记录智能体及其能力的注册表；能在故障中存活的持久化状态存储；执行结构校验与逐次调用鉴权的工具网关；执行护栏的策略引擎；人工介入的上报通道；以及记录每一步输入输出的追踪能力，使任何一次运行都可以被重放。"),
 ("如何在扩大编排规模的同时不损害信任？",
  "先扩展控制平面，再增加智能体数量。在调用时而非在提示词中执行权限；保持状态持久化且可归属，使运行可回放；把置信度随每条建议一起呈现；把上报指向具名角色而不是一个队列。然后度量采纳情况——覆盖修改率、放弃使用率与修正量，因为信任的崩塌会先出现在用量上，很久之后才体现在准确率指标上。"),
 ("编排最常见的失败模式有哪些？",
  "静默的部分完成——某一步失败，下游智能体却带着不完整的状态继续；权限漂移——智能体逐渐累积超出最初授权的访问权限；无界重试循环导致的成本失控；上下文膨胀——把到目前为止的全部内容向前传递，稀释了有效信号；以及编排蔓延——智能体过多使系统无法被推理或测试。"),
]

ZHCN_RENAMES = {
 "理解当前格局": "当前智能体编排的格局是怎样的？",
 "关键原则与战略框架": "哪些关键原则构成编排的战略框架？",
 "实施方法与最佳实践": "什么样的实施方法与最佳实践有效？",
 "衡量成功与展示投资回报率": "如何衡量成功并展示投资回报？",
 "常见陷阱及规避方法": "常见的陷阱有哪些，如何规避？",
 "关键要点": "有哪些关键要点？",
 "结论": "团队应该对编排得出什么结论？",
}

ZHCN = {"renames": ZHCN_RENAMES, "sections": ZHCN_SECTIONS, "faq": ZHCN_FAQ,
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
