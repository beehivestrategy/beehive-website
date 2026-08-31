#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "mcp-future-enterprise-data-integration"

EN_NEW = """
<h2 id="what-does-the-connector-ecosystem-mean-for-build-versus-buy">What Does the Connector Ecosystem Mean for Build Versus Buy?</h2>
<p>The emerging connector marketplace changes a calculation most enterprises made years ago. Historically, every integration was built, owned, and maintained internally. As pre-built connectors for common sources become available and shared, the economics shift — but not uniformly.</p>
<table>
<thead>
<tr><th>Source type</th><th>Recommended approach</th><th>Reasoning</th></tr>
</thead>
<tbody>
<tr><td>Commodity SaaS (CRM, helpdesk, marketing)</td><td>Buy or adopt shared connector</td><td>Schema is stable and public; maintaining your own adds no competitive advantage</td></tr>
<tr><td>Major cloud warehouses and lakes</td><td>Adopt shared connector, own the semantic layer</td><td>The connector is plumbing; the definitions on top are the asset</td></tr>
<tr><td>Core operational systems (ERP, core banking)</td><td>Build, or adopt and harden</td><td>Customisations, entitlement logic and audit requirements are specific to your installation</td></tr>
<tr><td>Proprietary or differentiating data</td><td>Build and keep in-house</td><td>This is where the connector itself encodes business logic you do not want to publish</td></tr>
</tbody>
</table>
<p>The trap is treating adoption as free. A shared connector still needs to be reviewed, pinned to a version, monitored, and owned by a named team. Organisations that adopt connectors without assigning ownership end up with exactly the sprawl they were trying to escape, except now the failures happen in someone else's code that nobody internally understands.</p>
<p>A useful rule: adopt the connector, own the contract. Whatever the connector does, your semantic layer defines what it means, your gateway controls who can call it, and your team is accountable when it breaks.</p>
<h2 id="how-should-you-govern-a-shared-connector-library">How Should You Govern a Shared Connector Library?</h2>
<p>A central connector library is the single highest-leverage investment in an MCP programme, because it converts a recurring per-project cost into a shared asset. It also fails in a predictable way when governance is missing. Five practices keep it working.</p>
<ul>
<li><strong>Version everything and pin it.</strong> Each connector has a version, each consumer pins to a version, and upgrades are scheduled rather than automatic. Silent connector updates are a common source of behaviour changes nobody can explain.</li>
<li><strong>Review before registration.</strong> A connector becomes visible to shared agents only after a review covering authentication, data scope, logging, and cost profile. This is the same discipline applied to any production dependency.</li>
<li><strong>Assign a named owner per connector.</strong> Not per project — per connector, with a support expectation. Ownership at this level is what prevents the orphaned integration that breaks during an incident and has no maintainer.</li>
<li><strong>Publish capability documentation.</strong> What the connector can do, what it must not be used for, its rate limits, and its failure modes. This documentation is also input to the tool descriptions the model sees, so it directly affects accuracy.</li>
<li><strong>Monitor usage and cost centrally.</strong> Per-connector call volume, error rate, latency and cost, on one dashboard. Adoption without visibility is how a shared library becomes an unbudgeted line item.</li>
</ul>
<p>Start with the five to ten sources that cover most of your usage. A library built for every system on the first pass takes a year and ships late; one built for the top ten ships in a quarter and covers the majority of real demand.</p>
<h2 id="what-breaks-when-agents-start-calling-each-other">What Breaks When Agents Start Calling Each Other?</h2>
<p>Multi-agent orchestration is the most promising and least mature part of the roadmap. One agent delegates sub-queries to specialised agents, each with its own tools and data. Three problems appear as soon as this moves from demonstration to production.</p>
<p><strong>Identity and authority chains.</strong> If agent A calls agent B on a user's behalf, whose authority applies? The correct answer is the intersection — B may only do what both B's allowlist and the originating user's entitlements permit — but most frameworks do not enforce this automatically. Without an explicit rule, delegation quietly becomes privilege escalation.</p>
<p><strong>Error propagation.</strong> A failure three agents deep surfaces as a vague answer rather than an error. Distributed tracing across agent boundaries is not optional: every sub-call needs to carry the trace identifier, and the final answer needs to be able to name what failed and where.</p>
<p><strong>Cost and latency multiplication.</strong> A query that fans out to four agents, each making several model calls, costs far more than the sum of its parts because context is re-sent at each hop. Budget ceilings have to be set at the task level, not the agent level, or a single question can consume a day's budget.</p>
<p>All three are solvable, and all three are architectural rather than model problems. The organisations that get value from multi-agent systems in the near term are the ones that build the trace and budget infrastructure before they build the second agent.</p>
<h2 id="how-do-you-prepare-your-data-roadmap-for-mcp">How Do You Prepare Your Data Roadmap for MCP?</h2>
<p>MCP changes three decisions on a data roadmap, and the changes are cheap to make now and expensive to retrofit.</p>
<ol>
<li><strong>Integration strategy: centralise the connector layer.</strong> Stop approving point-to-point integrations per AI project. Establish a connector library owned by the data integration team, built for the most-used sources first. This is the decision with the clearest payback, and it can be made in the current planning cycle.</li>
<li><strong>Semantic layer: treat it as infrastructure, not project scope.</strong> Every MCP deployment depends on shared definitions of the business's metrics. If the semantic layer is funded per project, every project rebuilds it. Fund it as a platform and every downstream use case gets cheaper.</li>
<li><strong>Governance: move enforcement to the protocol boundary.</strong> Allowlists, entitlements, and audit are far easier to enforce once at the MCP gateway than separately in every application. Roadmaps that place governance inside individual tools will find the controls inconsistent within a year.</li>
</ol>
<p>One sequencing caution: do not wait for the protocol to stabilise. The parts that matter for your roadmap — connector consolidation, semantic layer, gateway-based governance — are valuable regardless of how the specification evolves, and they are the parts that take longest. Organisations that wait for certainty typically start the same work eighteen months later, under more competitive pressure.</p>
"""

FAQ = {
 "EN": [
  ("Is MCP stable enough to build a data strategy on?",
   "The core capability model - tools, resources, prompts over a standard transport - is stable and widely adopted. The areas still moving are streaming extensions and multi-agent orchestration. The pragmatic approach is to build on the stable core now, since connector consolidation, semantic layer work and gateway-based governance deliver value regardless of how the specification evolves."),
  ("Should we build our own connectors or adopt shared ones?",
   "Adopt for commodity SaaS and major cloud platforms, build for core operational systems and proprietary data where your installation's customisations and entitlement logic matter. In every case, adopt the connector but own the contract: your semantic layer defines meaning, your gateway controls access, your team owns failures."),
  ("How do we stop a shared connector library becoming sprawl?",
   "Version and pin every connector, require a review before registration, assign a named owner per connector rather than per project, publish capability and failure-mode documentation, and monitor usage, errors and cost centrally. Start with the five to ten sources covering most demand rather than attempting full coverage."),
  ("What is the biggest risk in multi-agent orchestration?",
   "Delegation becoming privilege escalation. When agent A calls agent B on a user's behalf, the effective authority must be the intersection of B's allowlist and the originating user's entitlements - most frameworks do not enforce this automatically. Distributed tracing and task-level budgets are the other two requirements that must precede the second agent."),
 ],
 "zh-CN": [
  ("MCP是否已经稳定到可以承载数据战略？",
   "核心能力模型——基于标准传输的工具、资源与提示词——已经稳定并被广泛采用。仍在演进的是流式扩展与多智能体编排。务实的做法是现在就在稳定的核心上建设，因为连接器整合、语义层工作和基于网关的治理，无论规范如何演进都能交付价值。"),
  ("我们应该自建连接器还是采用共享连接器？",
   "通用SaaS和主流云平台采用共享连接器；核心业务系统和专有数据则自建，因为你的安装实例中的定制逻辑与授权逻辑至关重要。无论哪种情况，都要“采用连接器，但拥有契约”：语义层定义含义，网关控制访问，团队对故障负责。"),
  ("如何避免共享连接器库变成新的混乱源头？",
   "对每个连接器做版本化并锁定版本；注册前必须通过评审；按连接器而不是按项目指定责任人；公开能力说明与失效模式文档；集中监控用量、错误与成本。从覆盖大部分需求的五到十个数据源开始，而不要试图一次做到全覆盖。"),
  ("多智能体编排中最大的风险是什么？",
   "是委托演变为权限提升。当智能体A代表用户调用智能体B时，有效权限必须是B的白名单与发起用户授权的交集——而多数框架并不会自动执行这一点。分布式追踪与任务级预算，是另外两项必须在引入第二个智能体之前就具备的能力。"),
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
        "From Protocol to Platform": "How Does MCP Evolve From Protocol to Platform?",
        "Real-Time and Streaming Support": "How Will Real-Time and Streaming Support Work?",
        "Multi-Agent Orchestration": "What Changes With Multi-Agent Orchestration?",
        "Strategic Deployment Recommendations": "What Are the Strategic Deployment Recommendations?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    ren_cn = {
        "Real-Time and Streaming Support": "实时与流式数据支持将如何演进？",
        "Multi-Agent Orchestration": "多智能体编排会带来什么变化？",
        "Strategic Deployment Recommendations": "战略部署上有哪些建议？",
        "技术基础设施与实施考量": "技术基础设施与实施上需要考虑什么？",
        "中国市场特有的实施优势": "中国市场有哪些特有的实施优势？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    dup = "规模化推广的关键成功因素"
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(dup) + r'(</h2>)', r'\g<1>' + "规模化推广的关键成功因素是什么？" + r'\g<2>', b, count=1)
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(dup) + r'(</h2>)', r'\g<1>' + "从试点走向规模化需要注意什么？" + r'\g<2>', b, count=1)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    s = F.load(SLUG, "zh-TW")
    b = F.get_body(s)
    ren_tw = {
        "從協議到平台": "MCP如何从协议演进为平台？",
        "即時與串流支援": "实时与流式数据支持将如何运作？",
        "多智慧代理編排": "多智慧代理編排會帶來什麼變化？",
        "戰略部署建議": "戰略部署上有哪些建議？",
    }
    for old, new in ren_tw.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + F.S2TWP.convert(new) + r'\g<2>', b)
    F.save(SLUG, "zh-TW", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
