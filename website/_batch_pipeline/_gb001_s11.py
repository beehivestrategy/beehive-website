#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "ai-agent-governance-production"

# EN already meets the word floor: FAQ + structural checks only.
EN_FAQ = [
 ("What is AI agent governance in production?",
  "It is the set of controls that let autonomous systems act inside defined boundaries: least-privilege permissions, guardrails enforced at the tool-call layer, human approval gates for consequential actions, immutable audit logging, and monitoring that alerts on out-of-policy behaviour. What distinguishes production governance from policy documents is that the controls execute in the path of the action rather than describing it after the fact."),
 ("Which agents should be governed first?",
  "Govern by blast radius and autonomy. Agents with write access — those that update records, send messages, execute transactions, or trigger workflows — come before read-only assistants, and agents that chain multiple tools carry compounding risk. The sequencing rule is that the more consequential the action, the more controls it requires before production, rather than applying uniform machinery to every agent."),
 ("How do guardrails work at the tool-call layer?",
  "In five layers: instruction sets that set boundaries in natural language but are advisory only; tool-call validation that checks every invocation against a schema, an allowlist, and a parameter policy before execution; a policy engine that evaluates each call against data-access rules for the calling agent; human approval gates for high-impact or irreversible actions; and immutable logging of every attempted and executed action with its policy decision."),
 ("How long does it take to stand up agent governance?",
  "A pragmatic 90-day rollout is realistic. Days 1 to 14 inventory agents and classify them by risk. Days 15 to 42 define the governance policy and the agent registry with per-tier guardrails. Days 43 to 70 pilot on two or three high-risk agents with monitoring wired to alert on out-of-policy calls and permission drift. Days 71 to 90 harden controls, onboard the next tier, and establish the review cadence."),
 ("What happens when a governed agent fails?",
  "Three controls matter. A kill switch halts execution across all of the agent's tool connections immediately. Rollback reverses actions that are reversible — recalling a queued message, cancelling a pending transaction, discarding a draft record. Forensic replay reconstructs exactly what the agent saw, decided, and did from the audit trail, turning an incident into a reproducible defect rather than an unexplained one."),
]
EN = {"faq": EN_FAQ,
      "excerpts": [
        "Building inclusive AI and data teams: what the evidence says actually changes outcomes.",
        "Why your data strategy needs a dedicated AI agent layer in 2026.",
        "Vector databases for enterprise search: a practical 2026 guide."]}

# ------------------------------------------------------------------ zh-CN
ZHCN_SECTIONS = [
 ("智能体治理中的权限应如何设计",
  "智能体治理中的权限应如何设计？",
  """<p>权限是治理中最先要落实、也最常被做错的一环。核心原则是按请求者身份执行最小权限，而不是给智能体一个宽泛的服务账号。具体做法是：每个工具调用都携带调用者的身份或所属群组，在执行时对照源系统的权限策略做鉴权；智能体本身不持有超越任何单个用户的权限，这样一次被诱导的运行就不会变成全组织范围的数据暴露。</p>
<p>权限设计要落在四个粒度上。工具粒度决定这个智能体可以调用哪些工具；参数粒度决定调用时允许的取值范围——退款金额上限、可写入的字段、可访问的租户；数据粒度决定行级与列级的可见性，包括脱敏规则；以及动作粒度决定哪些操作需要人工审批。四个粒度缺一，都会留下绕过路径：只控制工具而放任参数，攻击者可以通过极端参数值达到越权效果。</p>
<p>最后必须考虑权限的时效性。权限变更要能在分钟级生效，缓存的授权结果要随权限变化失效，并且每次越权尝试都要被记录为安全事件——被拦截的尝试是最有价值的红队数据，因为它直接告诉你攻击者在试探什么。</p>"""),

 ("如何为智能体建立可用的审计追踪",
  "如何为智能体建立真正可用的审计追踪？",
  """<p>治理的可信度取决于一件事：出事之后能不能在几分钟内说清楚发生了什么。这要求审计追踪记录的不只是结果，而是完整的过程。一条可用的审计记录应包含六个要素：请求者身份、智能体的规划步骤、每一次工具调用及其入参与返回值、被调用数据的来源与版本、策略引擎的判定结果，以及最终动作与耗时。</p>
<p>存储上有三条硬性要求。追加写入且不可篡改，否则审计本身就成了可被攻击的对象；结构化且可检索，使"某个智能体上周有没有访问过这张表"这类问题能直接在查询界面得到答案，而不需要工程师翻日志；以及与业务标识对齐，让一条技术轨迹可以关联到具体的客户、订单或工单，因为合规问题通常以业务语言被提出。</p>
<p>审计追踪还必须是可回放的。出问题时，工程师应当能够依据记录的输入重建整条执行链，而不是重新运行一遍再猜测。可以回放的审计既缩短了故障定位时间，也让"模型为什么这么做"这类问题有据可答——这是让业务方继续信任系统的前提。</p>"""),

 ("智能体治理的成熟度分几个阶段",
  "智能体治理的成熟度分几个阶段？",
  """<p>把治理当成一次性项目，几乎必然失败；把它当成一条成熟度曲线，就知道下一步该补什么。实践中可以分四阶段。</p>
<ul>
<li><strong>第一阶段——人工审批：</strong>智能体只做建议，人类执行全部动作。治理成本最低，价值也最低，适合尚未建立信任的早期。</li>
<li><strong>第二阶段——受控执行：</strong>低风险动作自动执行，高风险动作设卡；已有智能体清单、权限边界与基础日志。多数组织应当以此为目标基线。</li>
<li><strong>第三阶段——策略即代码：</strong>权限、阈值与审批规则以版本化配置存在，变更需评审并留存记录；监控覆盖越权调用、权限漂移与异常动作序列，并有演练过的事件响应流程。</li>
<li><strong>第四阶段——持续治理：</strong>治理指标进入经营看板，新智能体的准入、定期复审与退出有固定节奏，历史决策可追溯可解释。</li>
</ul>
<p>关键不在于跳到第四阶段，而在于清楚自己处于哪个阶段，以及下一阶段最缺的是哪一项能力。多数事故都发生在组织以为自己在第三阶段、实际仍停留在第一或第二阶段的时候。</p>"""),

 ("如何让治理不拖慢交付速度",
  "如何让治理不拖慢交付速度？",
  """<p>治理最常见的失败不是控制不足，而是控制过重导致团队绕过它。避免这一点，需要把治理做成一条流水线上的关卡，而不是一道独立的审批墙。</p>
<p>第一，把策略写成代码并纳入版本管理，让权限、阈值与审批规则像其他配置一样被评审、被回滚、被复用，而不是每次靠人工判断。第二，按风险分层：低风险动作默认放行并事后抽检，高风险动作才走完整流程，这样审批队列里只有真正需要人判断的事项。第三，提供自助路径：团队可以通过标准模板申请新智能体，模板自带权限边界、日志要求与评估门槛，满足条件即自动放行，不满足则明确告知缺什么。</p>
<p>第四，把评估接入部署关卡，用黄金集的回归结果替代主观评审——分数达标即通过，团队不必等待会议。第五，度量并公开治理自身的效率：新智能体的平均准入时长、审批积压量、误拦率。治理如果不能被度量，就会像其他没有服务水平的内部流程一样，被人绕开。</p>"""),
]

ZHCN_FAQ = [
 ("什么是生产环境中的AI智能体治理？",
  "它是让自主系统在既定边界内行动的一组控制：最小权限、在工具调用层强制执行的护栏、对高后果动作设置的人工审批关卡、不可篡改的审计日志，以及对偏离策略行为的监控告警。生产级治理与政策文件的区别在于，这些控制是在动作执行的路径上生效，而不是在事后对动作做描述。"),
 ("哪些智能体应该优先纳入治理？",
  "按影响半径与自主程度排序。具备写入权限的智能体——会更新记录、发送消息、执行交易或触发工作流的——优先于只读助手；会串联多个工具的智能体则带来叠加风险。排序规则是：动作后果越严重，投产前需要的控制越多，而不是对每个智能体套用同一套机制。"),
 ("工具调用层的护栏是如何工作的？",
  "分五层：指令集用自然语言设定边界，但只具建议性；工具调用校验在执行前比对模式、白名单与参数策略；策略引擎依据调用方的数据访问规则评估每一次调用；对高影响或不可逆动作设置人工审批关卡；以及对每一次尝试执行与实际执行的动作连同其策略判定做不可篡改的记录。"),
 ("建立智能体治理需要多长时间？",
  "90天的务实推进是可行的。第1到14天清点智能体并做风险分级；第15到42天定义治理策略与智能体注册表，并按风险层级配置护栏；第43到70天在两到三个高风险智能体上试点，并把监控接到越权调用、权限漂移等告警上；第71到90天加固控制、接入下一批智能体，并建立定期复审节奏。"),
 ("当一个受治理的智能体失败时该怎么办？",
  "三项控制至关重要。一键停止开关能立即终止该智能体在全部工具连接上的执行；回滚用于撤销可逆的动作——撤回已排队的消息、取消待处理的交易、丢弃草稿记录；取证重放则依据审计线索重建智能体看到了什么、决定了什么、做了什么，把一次事故转化为可复现的缺陷，而不是一团无法解释的现象。"),
]

ZHCN_RENAMES = {
 "理解当前格局": "当前智能体治理的格局是怎样的？",
 "关键原则与战略框架": "哪些关键原则构成治理的战略框架？",
 "实施方法与最佳实践": "什么样的实施方法与最佳实践有效？",
 "衡量成功与展示投资回报率": "如何衡量治理成效并展示投资回报？",
 "常见陷阱及规避方法": "常见的陷阱有哪些，如何规避？",
 "关键要点": "有哪些关键要点？",
 "结论": "企业可以得出什么结论？",
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
