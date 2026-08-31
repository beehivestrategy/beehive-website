#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "ai-agent-orchestration-patterns-2026"

EN_RENAMES = {
 "which-orchestration-pattern-should-you-choose-first": "Which Orchestration Pattern Should You Choose First?",
}

EN_FAQ = [
 ("What are the main agent orchestration patterns in 2026?",
  "Five patterns cover most enterprise practice: pipeline, where agents execute in a fixed order and each passes an artifact to the next; router, where an entry agent classifies and dispatches to specialists; orchestrator-workers, where a planner decomposes a task dynamically and merges results; hierarchical, where layers of orchestrators manage sub-teams and provide approval gates; and autonomous collaboration, where agents negotiate through a shared workspace — the most flexible and the least governable."),
 ("Which orchestration pattern should an enterprise start with?",
  "Start with a pipeline or a router. They are deterministic, easy to test, cheap to run, and they produce a working closed loop that can be measured against a baseline. Move to orchestrator-workers only when decomposition genuinely depends on the input, and reserve autonomous collaboration for exploratory work where the decomposition cannot be known in advance."),
 ("How do you choose between orchestration patterns?",
  "Ask three questions. How predictable is the task — fixed flow favours a pipeline, dynamic flow favours orchestrator-workers. How low is the error tolerance — high-consequence work such as financial settlement or clinical decisions should use the most deterministic pattern and confine autonomy to low-risk steps. And how high are the observability requirements — regulated industries need a topology that can reconstruct the full decision chain, which favours pipelines and hierarchies."),
 ("What does the orchestration layer need to engineer for?",
  "Three things beyond the pattern itself. State: durable execution state in the orchestrator, append-only shared context with provenance, and agent-local scratch state kept local. Context: explicit selection of what is passed forward, with timestamps so stale evidence can be detected. Observability: a replayable trace of every run plus metrics, structured logs, alerts on policy violations, and an evaluation loop that converts production failures into permanent test cases."),
 ("What causes multi-agent orchestration projects to fail?",
  "The most common cause is not model capability but loss of control at the orchestration layer: task loops that never terminate, context lost between agents, permissions exceeded, and cost amplified by duplicate calls and unbounded retries. The second is orchestration sprawl — too many agents for anyone to reason about or test. Bounded scope, explicit tool contracts, and observability prevent both."),
]
EN = {"renames": EN_RENAMES, "faq": EN_FAQ,
      "excerpts": [
        "How to architect enterprise AI agents: the runtime, tool, and memory layers that make them dependable.",
        "Using AI scenario planning to stress-test supply chains before disruption hits.",
        "Demand sensing with AI: shortening the signal-to-decision loop in volatile markets."]}

# ------------------------------------------------------------------ zh-CN
ZHCN_SECTIONS = [
 ("编排中的失败恢复应如何设计",
  "编排中的失败恢复应如何设计？",
  """<p>多智能体系统的失败是常态，真正决定可用性的不是失败率，而是恢复路径。设计上要把失败分成三类，并为每一类预设动作。瞬时失败——接口超时、限流、网络抖动——应当按指数退避重试，并设定明确的上限；超过上限即转入下一类处理。持久失败——数据源不可用、参数不合法、权限被拒——重试没有意义，应当立即上报，并把上下文完整地交给人工。</p>
<p>第三类最危险，也最容易被忽略：静默的部分完成。某个步骤失败了，下游智能体却带着不完整的状态继续推进，产出一个看起来完整、实际上缺了关键证据的结果。防御方式是显式契约——每个交付物在边界处被校验，不满足即拒绝、重试或停止，而不是被下游吸收。</p>
<p>此外要落实三项机制。检查点：在关键步骤后持久化状态，使长流程可以从断点恢复，而不是从头重跑。补偿动作：对已产生的副作用准备逆向操作，撤回已排队的消息、取消待处理的交易。以及一键停止与回滚演练——没有演练过的停止开关，在真实事故中往往不可用。</p>"""),

 ("编排的人机协同边界应如何划定",
  "编排中的人机协同边界应如何划定？",
  """<p>自主性的边界应当按后果划定，而不是按技术可行性划定。判断标准很朴素：如果这个动作做错了，且一周内没人发现，最坏会发生什么？答案涉及资金流动、对客户的对外沟通，或他人所依赖的数据记录时，这个动作就应当设卡。</p>
<p>实践中用四个刻度来界定。范围：这个智能体可以触达哪些工具与数据集。阈值：它可以免审批处理的金额与数量上限——退款上限、订单金额、影响的记录条数。可逆性：可撤销的动作（生成草稿报告）与不可撤销的动作（对外发送）要区别对待。影响半径：单次运行最多可以触及多少条记录或多少个客户，使系统性错误在设计上被限制住，而不是在规模上被发现。</p>
<p>上报路径要指向具名角色，而不是一个队列——"上报给当班收入分析员"会被处理，"上报给财务团队"不会。同时要跟踪上报率与上报准确率：什么都要问的智能体是多了几道工序的助手，什么都不问的智能体则是在等待第一次事故的 unbounded 智能体。</p>"""),

 ("编排模式的成本结构如何管理",
  "编排模式的成本结构应如何管理？",
  """<p>不同模式的成本结构差异很大。流水线最省——固定的步骤数、确定的调用次数，成本可预测。路由模式次之，只多了一次分类调用。编排者—工人模式的成本随动态拆解出来的子任务数量波动，方差最大。层次结构因层层传递而带来额外开销。自主协作模式最贵，因为协商与重试的轮次不可预知。</p>
<p>无论采用哪种模式，成本失控都来自三个可预防的原因。无上限的重试与循环，而且往往恰好在最难的失败案例上消耗最多；上下文无界传递，使 token 成本随步骤数增长，同时稀释有效信号；以及模型选型单一，用前沿模型去做分类、路由与重排这类简单任务。</p>
<p>管理上按"每个已完成任务的成本"衡量，而不是按每次调用的成本。为每个工作流设定预算与告警阈值，让超支在当天被发现；缓存可复用的检索结果与工具返回，并在数据源更新时失效；把小模型用在简单步骤，把前沿模型留给最终综合与需要判断的环节。</p>"""),
]

ZHCN_FAQ = [
 ("2026年主流的智能体编排模式有哪些？",
  "五种模式覆盖了多数企业实践。流水线：智能体按固定顺序执行，前一个的输出作为后一个的输入。路由：入口智能体先分类，再分发给专家智能体。编排者—工人：编排者动态拆解任务、分发给多个工人并汇总结果。层次结构：多级编排者逐层管理，形成树状结构并提供审批关卡。自主协作：多个智能体通过共享工作区或消息总线自主协商，灵活性最高，可治理性最差。"),
 ("企业应首先采用哪种编排模式？",
  "从流水线或路由模式起步。它们具有确定性、容易测试、运行成本低，并且能跑通一个可对照基准衡量价值的业务闭环。只有当拆解方式确实取决于输入时，才转向编排者—工人模式；自主协作模式则应保留给拆解方式无法预先得知的探索性任务。"),
 ("如何在编排模式之间做选择？",
  "问三个问题。任务的可预测性有多高——流程固定选流水线，流程动态选编排者—工人；错误容忍度有多低——金融结算、临床决策等高影响场景应优先选择确定性强的模式，把自主性限制在低风险环节；可观测性要求有多高——受监管行业必须能完整还原决策链，因此更适合层次结构与流水线。"),
 ("编排层需要在工程上做到什么？",
  "除模式本身之外还有三件事。状态：执行状态持久化在编排者中、共享上下文仅追加且带溯源、智能体本地暂存状态保持本地。上下文：显式挑选向前传递的内容，并带上时间戳以便识别陈旧证据。可观测性：每次运行都可重放的追踪，加上指标、结构化日志、针对策略违规的告警，以及把生产失败转化为永久测试用例的评估闭环。"),
 ("多智能体编排项目失败的原因是什么？",
  "最常见的原因不是模型能力，而是在编排层失去了控制：永不终止的任务循环、智能体之间丢失的上下文、越界的权限，以及被重复调用与无界重试放大的成本。其次是编排蔓延——智能体多到没有人能够推理或测试。有界的范围、显式的工具契约与可观测性可以同时防范这两类问题。"),
]

ZHCN_RENAMES = {
 "2026年主流的五种智能体编排模式": "2026年主流的五种智能体编排模式是什么？",
 "编排层的工程实践-状态-上下文与可观测性": "编排层的工程实践应覆盖哪些方面？",
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
