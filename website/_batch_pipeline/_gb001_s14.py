#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb001_lib as L
from _gb001_apply import apply

SLUG = "ai-agents-professional-services-beyond-billable-hours"


def dedupe_en_heading(slug):
    """The EN file contains the same h2 id twice; give the second one a unique id,
    distinct question text, and matching TOC entries."""
    h = L.read(slug, "en")
    occurrences = [m for m in re.finditer(
        r'<h2 id="what-ai-agents-actually-do-in-a-professional-services-firm"[^>]*>.*?</h2>', h, re.S)]
    if len(occurrences) != 2:
        return
    second = occurrences[1]
    new_id = "what-do-agents-do-day-to-day-in-a-firm"
    new_text = "What Do Agents Actually Do Day to Day Inside a Firm?"
    h = h[:second.start()] + f'<h2 id="{new_id}">{new_text}</h2>' + h[second.end():]
    # TOC: the second link with the old anchor becomes the new one
    for cls in ("toc-link", "toc-mobile-link"):
        links = list(re.finditer(r'<a href="#what-ai-agents-actually-do-in-a-professional-services-firm" class="%s">.*?</a>' % cls, h, re.S))
        if len(links) == 2:
            l = links[1]
            h = h[:l.start()] + f'<a href="#{new_id}" class="{cls}">{new_text}</a>' + h[l.end():]
    L.write(slug, "en", h)


EN_RENAMES = {
 "what-ai-agents-actually-do-in-a-professional-services-firm": "What Do AI Agents Actually Do in a Professional Services Firm?",
 "the-professional-services-data-paradox": "What Is the Professional Services Data Paradox?",
 "how-mcp-powered-conversational-bi-connects-the-dots": "How Does MCP-Powered Conversational BI Connect the Dots?",
 "real-results-what-early-adopters-are-seeing": "What Results Are Early Adopters Actually Seeing?",
 "getting-started-a-30-day-implementation-roadmap": "What Does a 30-Day Implementation Roadmap Look Like?",
 "conclusion": "What Should Firm Leaders Conclude?",
}

EN_FAQ = [
 ("What can AI agents actually do in a professional services firm?",
  "The work that pays back fastest is the preparation work around billable time: assembling the client data pack before a review, drafting the first version of a recurring report, reconciling figures across systems before a partner signs off, and answering routine client questions from governed data. These are high-volume, well-structured tasks where an agent can work inside defined permissions and a human reviews the output."),
 ("What is the professional services data paradox?",
  "Firms advise clients on data strategy while their own data is fragmented across practice-management systems, document stores, spreadsheets, and email. The paradox is that the expertise exists but is trapped in formats no system can reason over, so partners rebuild the same analysis for every client. Agents only create value once that fragmentation is addressed at the retrieval layer rather than by another migration."),
 ("How does an agent respect client confidentiality?",
  "By resolving permissions at execution time rather than in the prompt. Each tool call carries the requesting user's identity and is authorised against the engagement-level entitlements already held in the firm's systems, so an agent cannot surface one client's material to someone not staffed on that engagement. Every access is logged, which is what makes the arrangement defensible to a client or a regulator."),
 ("How do you measure ROI on agents in a professional services firm?",
  "Measure hours returned to billable or higher-value work, cycle time on recurring deliverables, and the reduction in rework caused by inconsistent figures. Establish a baseline before deployment and use a paired comparison where possible: the same recurring report prepared with and without the agent, compared on hours and error rate. Realisation and write-off rates are the financial metrics partners will actually accept."),
 ("How do you avoid agent-washing when buying?",
  "Ask four questions and require demonstrations against your own data. Which decisions does the agent make without a human? What happens when the underlying data is missing or contradictory? Can you see the source and the reasoning behind any figure it produces? And what are the verified error rates from comparable deployments, not a demo environment? Vendors that cannot answer the last two are selling automation theatre."),
]
EN = {"renames": EN_RENAMES, "faq": EN_FAQ,
      "excerpts": [
        "How to architect enterprise AI agents: the runtime, tool, and memory layers that make them dependable.",
        "Using AI scenario planning to stress-test supply chains before disruption hits.",
        "Demand sensing with AI: shortening the signal-to-decision loop in volatile markets."]}

# ------------------------------------------------------------------ zh-CN
ZHCN_SECTIONS = [
 ("智能体如何保护客户机密与权限边界",
  "智能体如何保护客户机密与权限边界？",
  """<p>专业服务机构对智能体最合理的担忧不是准确率，而是保密。一次把甲方资料暴露给未被授权团队的事故，其代价远超任何效率收益。因此权限不能写在提示词里，而必须在执行时解析：每一次工具调用都携带请求者的身份，并对照事务所既有的项目级授权做鉴权；智能体自身不持有超越任何单个用户的权限。</p>
<p>粒度上要控制到项目级与文档级。项目级决定某人是否属于该项目的授权团队；文档级决定具体工作底稿、合同草稿与邮件是否可见。两者缺一都会留下漏洞：只有项目级控制，会让项目内部的敏感文件对全部成员敞开；只有文档级控制，则难以应对人员调动后的权限变更。</p>
<p>此外要有两项配套。一是完整的访问日志，记录谁、在什么时间、通过哪个智能体、访问了哪份资料，这既是客户尽调时的证据，也是事故复盘的依据。二是红队测试，定期用甲方的名义构造越权请求，验证拦截是否真的生效——没有被验证过的权限控制，通常只在设计文档里有效。</p>"""),

 ("事务所应如何衡量智能体的投资回报",
  "事务所应如何衡量智能体的投资回报？",
  """<p>合伙人会接受的指标只有三类：回收的工时、交付周期与核销率。回收工时衡量的是原本消耗在资料整理、底稿准备与重复计算上的时间，有多少回到可计费或更高价值的工作上。交付周期衡量的是周期性交付物——季度报告、审阅底稿、客户数据包——从启动到合伙人复核所需的时间变化。核销率与实现率则是最有说服力的财务指标，因为返工与不一致的数字正是核销的主要来源之一。</p>
<p>方法上要建立部署前的基准线，并尽量做配对比较：同一份周期性报告分别在有、无智能体辅助的情况下准备，比较工时与错误率。只比较"部署前后"的数字，很容易被当季业务复杂度与人员变动所污染，进而在合伙人会议上被质疑。</p>
<p>还要跟踪采纳度指标，因为回报只在被使用时才产生：目标用户中过去一周至少使用过一次的比例、适用任务中由智能体处理的比例、以及输出被原样接受而非重写的比例。第三项尤其关键——高修改率意味着工作只是被搬了位置，而不是被消除。</p>"""),

 ("如何避免在采购时被智能体包装所误导",
  "如何避免在采购时被智能体包装所误导？",
  """<p>市场上大量产品把脚本化的工作流称为"智能体"。四个问题可以快速区分真实能力与包装：哪些决策是智能体在没有人工参与的情况下做出的？当底层数据缺失或相互矛盾时会发生什么？能否看到任何一个数字背后的来源与推理过程？以及在可比部署中经核实的错误率是多少，而不是演示环境中的效果？</p>
<p>要求用事务所自己的数据做验证，而不是供应商准备的样例。真正的能力体现在边界场景上：口径不一致的表格、缺失的期间数据、同一客户在不同系统中的不同编号。能在这些情况下明确拒答或标注不确定性的系统，比在干净数据上表现完美的系统更值得采购。</p>
<p>最后看三件事：权限是否在执行时按身份解析、每次运行是否有可回放的追踪记录、以及错误率是否有书面承诺并附带评估方法。供应商若无法回答后两项，卖的通常是自动化剧场，而不是可治理的智能体能力。</p>"""),
]

ZHCN_FAQ = [
 ("AI智能体在专业服务事务所中实际能做什么？",
  "回本最快的是计费时间周围的准备工作：复核前整理客户数据包、周期性报告的初稿、合伙人签字前跨系统的数字核对，以及基于受治理数据回答客户的例行问询。这些任务量大、结构清晰，智能体可以在明确权限内工作，由人工复核产出。"),
 ("什么是专业服务的数据悖论？",
  "事务所一边为客户提供数据战略建议，一边让自己的数据散落在业务管理系统、文档库、电子表格与邮件之中。悖论在于专业能力是存在的，却被困在系统无法推理的格式里，于是合伙人为每个客户反复重建同一套分析。只有先在检索层解决这种碎片化，而不是再迁移一次数据，智能体才能产生价值。"),
 ("智能体如何保护客户机密？",
  "在执行时而非在提示词中解析权限。每一次工具调用都携带请求者身份，并对照事务所既有的项目级授权做鉴权，因此智能体无法把某一客户的数据呈现给未被安排在该项目上的人员。每一次访问都会被记录，这正是面对客户或监管时能够自证的基础。"),
 ("事务所应如何衡量智能体的投资回报？",
  "衡量三项：回流到计费或更高价值工作的工时、周期性交付物的交付周期，以及由数字不一致导致的返工减少。部署前建立基准线，并尽量做配对比较——同一份周期性报告在有、无智能体辅助下的工时与错误率对比。实现率与核销率是合伙人真正会接受的财务指标。"),
 ("采购时如何避免被智能体包装误导？",
  "提出四个问题并要求用事务所自己的数据验证：哪些决策由智能体在无人工参与下做出？底层数据缺失或矛盾时会发生什么？能否看到任何数字背后的来源与推理？在可比部署中经核实的错误率是多少？此外确认权限是否按身份在执行时解析、每次运行是否可回放。答不出后两项的供应商，卖的通常是自动化剧场。"),
]

ZHCN_RENAMES = {
 "专业服务数据悖论": "什么是专业服务的数据悖论？",
 "人工智能代理在专业服务公司中实际做什么": "AI智能体在专业服务公司中实际做什么？",
 "mcp-支持的对话式-bi-如何连接各个点": "MCP驱动的对话式BI如何把数据连起来？",
 "真实结果-早期采用者所看到的": "早期采用者看到了哪些真实结果？",
 "入门-30-天实施路线图": "30天实施路线图是什么样的？",
 "结论": "事务所领导者可以得出什么结论？",
}

ZHCN = {"renames": ZHCN_RENAMES, "sections": ZHCN_SECTIONS, "faq": ZHCN_FAQ,
        "excerpts": [
          "企业AI智能体的架构方法：让系统可靠的运行时、工具与记忆三层设计。",
          "用AI情景规划在供应链受扰动之前完成压力测试。",
          "用AI做需求感知，缩短波动市场中的信号到决策链路。"]}

import _gb001_s2t as T
ZHTW = T.spec_s2tw(ZHCN)

if __name__ == "__main__":
    dedupe_en_heading(SLUG)
    for lang, spec in (("en", EN), ("zh-CN", ZHCN), ("zh-TW", ZHTW)):
        b, a, n = apply(SLUG, lang, spec)
        print(f"{SLUG} {lang}: {b} -> {a}  [{', '.join(n)}]")
