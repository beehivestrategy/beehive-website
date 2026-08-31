#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "zero-trust-architecture-for-ai-platforms"

EN_NEW = """
<h2 id="how-do-you-defend-against-prompt-injection-and-agent-manipulation">How Do You Defend Against Prompt Injection and Agent Manipulation?</h2>
<p>Zero trust assumes the caller may be compromised, and for AI agents that assumption is literal. Prompt injection is not an exotic attack: any document, web page, ticket comment, or retrieved record that reaches the model can carry instructions. An agent that reads a poisoned support ticket and then calls a tool with broad scope is the agentic equivalent of a SQL injection, and it is defended the same way — by never treating the untrusted input as executable authority.</p>
<p>The defence has three layers. First, separate instructions from data at the protocol level: retrieved content arrives as data with a declared provenance, never as part of the system prompt. Second, enforce the capability allowlist at the MCP gateway, so that even a successfully manipulated model cannot invoke a tool outside the approved set or access data beyond the caller's entitlements. Third, require confirmation for state-changing actions — writes, exports, payments, permission changes — regardless of how confident the agent claims to be.</p>
<p>Two practical tests separate a real defence from a slide. Attempt a privilege escalation through content: plant a plausible instruction inside a document the agent will retrieve, and confirm nothing happens. Then attempt a scope violation: ask a low-entitlement user for data the agent can technically reach, and confirm the gateway refuses. If either test succeeds, the allowlist is living in the prompt rather than in the infrastructure.</p>
<h2 id="what-governance-controls-do-auditors-expect-for-ai-platforms">What Governance Controls Do Auditors Expect for AI Platforms?</h2>
<p>Auditors do not ask whether your agents are secure; they ask you to demonstrate four things, and the answers need to be reproducible rather than asserted.</p>
<ul>
<li><strong>Complete agent inventory.</strong> Every agent, its purpose, its owner, the systems it can reach, and the date of last review. Organisations that cannot produce this list fail the first question, and the list is the foundation for everything else.</li>
<li><strong>Identity and entitlement mapping.</strong> For each agent, the identity it acts under and the entitlements attached. Shared service accounts are the most common finding, because they make attribution impossible after an incident.</li>
<li><strong>Access logs with context.</strong> Not just "agent X queried table Y" but the requesting user, the query, the scope granted, the rows returned, and the decision. Logs that cannot reconstruct a decision do not satisfy an auditor.</li>
<li><strong>Change and revocation evidence.</strong> How an agent's permissions are changed, who approves it, and how quickly access can be revoked. An annual review cycle is not an answer when the agent fleet changes weekly.</li>
</ul>
<p>The teams that pass these reviews comfortably are the ones that built the controls into the data access path from the start. Retrofitting attribution onto a year of logs written by a shared account is the expensive alternative, and it rarely satisfies anyone.</p>
<h2 id="how-does-zero-trust-apply-to-the-semantic-layer-itself">How Does Zero Trust Apply to the Semantic Layer Itself?</h2>
<p>There is an uncomfortable recursion here: the component enforcing your security policy is itself software with credentials, dependencies, and an attack surface. Treating the semantic layer as implicitly trusted recreates the perimeter model one level down, and it is the mistake sophisticated teams make most often.</p>
<p>Apply the same discipline to the gateway that you apply to the agents. Run it under its own least-privilege machine identity rather than a database superuser. Sign and version every semantic definition, so a metric definition cannot be silently altered to widen what a query returns. Restrict who can publish a new data product or change an entitlement mapping, and require the same review you would require for a production code change, because that is what it is. Log the gateway's own administrative actions separately from the access logs it produces, so that an attacker who gains query access cannot edit the record of how they got it.</p>
<p>Then test it. Add the gateway to the same inventory, the same least-privilege review, and the same anomaly detection you apply to agents — with alerting on administrative actions rather than data access. A control plane that is exempt from its own policy is not a control plane.</p>
<h2 id="what-are-the-most-common-zero-trust-implementation-mistakes">What Are the Most Common Zero Trust Implementation Mistakes?</h2>
<p>Five mistakes account for most stalled programmes.</p>
<p><strong>Buying a product instead of adopting a posture.</strong> Zero trust is not a SKU. Vendors sell components — identity, gateway, monitoring — but the posture is the operating discipline around them: per-request verification, least privilege, and automated response. Programmes that start with procurement stall; programmes that start with the agent inventory and the access path finish.</p>
<p><strong>Scoping agents to service accounts for convenience.</strong> It is easier during integration and it destroys attribution permanently. Enforce per-request identity at the gateway so the shortcut is unavailable, and alert on any agent identity acting on behalf of more than one user.</p>
<p><strong>Logging without response.</strong> A comprehensive audit trail is not a control if nothing reads it. At agent speed, an alert that waits for a human is a record of what already happened; revocation and escalation have to be automated for the highest-risk data.</p>
<p><strong>Treating human and machine identities as the same problem.</strong> They have different lifetimes, different behavioural patterns, and different revocation paths. Machine identities already outnumber human identities in most large enterprises, and they need their own lifecycle management.</p>
<p><strong>Attempting full coverage before delivering anything.</strong> Sequence by risk: inventory, identity, gateway, logging, then automated response on the most sensitive data first. Programmes that sequence by data source instead of by risk run out of patience before they reach the data that matters.</p>
"""

CN_NEW = """
<h2 id="how-do-you-defend-against-prompt-injection-and-agent-manipulation">如何防御提示词注入与智能体被操控？</h2>
<p>零信任假设调用方可能已经失陷，而对AI智能体来说，这个假设是字面意义上的。提示词注入并不罕见：任何进入模型的文档、网页、工单评论或检索到的记录，都可能携带指令。一个读取了被投毒的支持工单、随后带着宽泛权限调用工具的智能体，就是智能体世界的SQL注入，防御方式也相同——永远不要把不可信输入当作可执行的授权。</p>
<p>防御分为三层。第一，在协议层把指令与数据分开：检索到的内容以"数据"的身份带着来源声明进入，绝不进入系统提示词。第二，在MCP网关强制执行能力白名单，这样即使模型被成功操控，也无法调用批准清单之外的工具，或访问超出调用方授权范围的数据。第三，对写操作、导出、付款、权限变更等改变状态的动作强制二次确认，无论智能体自称有多高的置信度。</p>
<p>有两个测试可以区分真实的防御与幻灯片上的防御。第一个是通过内容进行权限提升：在智能体将要检索的文档里植入一条看起来合理的指令，然后确认什么都没有发生。第二个是越权访问：让一名低权限用户请求智能体技术上能够触达的数据，确认网关拒绝。任一测试通过，都说明白名单写在提示词里，而不是写在基础设施里。</p>
<h2 id="what-governance-controls-do-auditors-expect-for-ai-platforms">审计方对AI平台期待哪些治理控制？</h2>
<p>审计方不会问你的智能体是否安全，他们会要求你证明四件事，而且答案必须可复现，而不是口头承诺。</p>
<ul>
<li><strong>完整的智能体清单。</strong>每个智能体的用途、负责人、可触达的系统，以及最近一次评审的日期。拿不出这份清单的组织会在第一个问题上失败，而这正是其余一切的基础。</li>
<li><strong>身份与授权映射。</strong>每个智能体以什么身份运行、附带哪些授权。共享服务账号是最常见的审计发现，因为它让事件发生后的归因变得不可能。</li>
<li><strong>带上下文的访问日志。</strong>不只是"智能体X查询了表Y"，还要有请求用户、查询语句、被授予的范围、返回的行数以及判定依据。无法还原一次决策的日志无法让审计方满意。</li>
<li><strong>变更与吊销的证据。</strong>智能体权限如何变更、由谁批准、访问可以多快被吊销。当智能体规模每周都在变化时，"一年评审一次"不是答案。</li>
</ul>
<p>能从容通过这类评审的团队，都是从一开始就把控制嵌入数据访问路径的。反过来，给一个共享账号写了一年的日志做归因补录，既昂贵，又很少能让任何人满意。</p>
<h2 id="how-does-zero-trust-apply-to-the-semantic-layer-itself">零信任如何应用于语义层自身？</h2>
<p>这里存在一个不太舒服的递归：执行安全策略的组件本身也是软件，也有凭证、依赖和攻击面。把语义层默认视为可信，等于在下一层重建了边界模型——而恰恰是成熟的团队最常犯这个错误。</p>
<p>把用于智能体的同一套纪律用在网关上。让它以自身的最小权限机器身份运行，而不是数据库超级用户。对每个语义定义签名并版本化，这样指标定义就不会被悄悄改宽、让查询返回更多数据。限制谁能发布新的数据产品、谁能修改授权映射，并要求与生产代码变更同级的评审——因为它本来就是。把网关自身的管理操作日志与它产生的访问日志分开存放，这样即使攻击者获得了查询权限，也无法篡改自己进入方式的记录。</p>
<p>然后测试它。把网关纳入同一份清单、同一套最小权限评审、同一套异常检测——只是告警对象从数据访问改为管理操作。一个可以豁免自身策略的控制平面，不是控制平面。</p>
<h2 id="what-are-the-most-common-zero-trust-implementation-mistakes">最常见的零信任落地错误有哪些？</h2>
<p>五个错误解释了大多数停滞的项目。</p>
<p><strong>采购一个产品，而不是采取一种姿态。</strong>零信任不是一个SKU。厂商售卖的是组件——身份、网关、监控——但姿态是围绕它们的运营纪律：逐请求验证、最小权限、自动响应。从采购开始的项目会停滞，从智能体清单和访问路径开始的项目会完成。</p>
<p><strong>为了省事把智能体挂到服务账号上。</strong>集成时确实更方便，但它会永久摧毁归因能力。在网关强制执行逐请求身份，让这条捷径不可用，并对任何代表多于一个用户行事的智能体身份发出告警。</p>
<p><strong>只记录不响应。</strong>如果没有人读取，再完整的审计轨迹也不是控制措施。在智能体的速度下，等待人工处理的告警只是对既成事实的记录；对最高风险的数据，吊销与升级必须自动化。</p>
<p><strong>把人类身份与机器身份当成同一个问题。</strong>它们的生命周期、行为模式和吊销路径都不同。在多数大型企业中，机器身份的数量已经超过人类身份，它们需要独立的生命周期管理。</p>
<p><strong>在交付任何成果之前追求全覆盖。</strong>应按风险排序推进：先清单、再身份、网关、日志，最后对最敏感的数据启用自动响应。按数据源而不是按风险排序的项目，往往在触及真正重要的数据之前就耗尽了耐心。</p>
"""

FAQ = {
 "EN": [
  ("Is zero trust for AI the same as zero trust for employees?",
   "The principles are identical - never trust, always verify - but the implementation differs. Employees authenticate once per session and act at human speed; agents must authenticate per request and act at machine speed. That makes automated response mandatory rather than optional, and it makes machine identity lifecycle management a first-class problem rather than an afterthought."),
  ("Do we need to replace our existing identity provider?",
   "Usually not. Most enterprises extend the existing IdP to issue and manage machine identities for agents, then enforce authorisation at the MCP gateway using the entitlements already stored there. The new work is the agent inventory, per-request enforcement, and automated revocation - not a replacement identity platform."),
  ("How do we start if we have no agent inventory?",
   "Start with the data, not the agents. List the systems agents can reach and work backwards: query the gateway and access logs to see which identities touched those systems in the last 30 days, then assign an owner to each. Most organisations discover substantially more active agents than they expected, which is itself the argument for doing the exercise."),
  ("How quickly should access be revoked when an anomaly is detected?",
   "For the highest-risk data, revocation should be automatic and measured in seconds, with a human notified immediately afterwards. For lower-risk data, a short confirmation window is acceptable. The test is whether your response time is faster than the agent's rate of data access - if it is not, the control is documentation rather than defence."),
 ],
 "zh-CN": [
  ("面向AI的零信任与面向员工的零信任是一回事吗？",
   "原则完全相同——从不信任，始终验证——但落地方式不同。员工每次会话认证一次，以人类速度行动；智能体必须逐请求认证，以机器速度行动。这使得自动响应成为必需而非可选，也让机器身份的生命周期管理成为一等问题，而不是事后补充。"),
  ("需要替换现有的身份提供商吗？",
   "通常不需要。多数企业会扩展现有IdP，让它为智能体签发和管理机器身份，然后在MCP网关基于其中已有的授权数据执行鉴权。新增的工作是智能体清单、逐请求执行和自动吊销，而不是更换身份平台。"),
  ("如果完全没有智能体清单，应该从哪里开始？",
   "从数据开始，而不是从智能体开始。列出智能体能够触达的系统，然后反向追溯：查询网关与访问日志，看过去30天有哪些身份接触过这些系统，再为每一个指定负责人。多数组织会发现活跃的智能体数量远超预期，而这本身就是做这件事的理由。"),
  ("检测到异常时，访问应该多快被吊销？",
   "对最高风险的数据，吊销应当自动化并以秒计，随后立即通知到人。对风险较低的数据，可以接受一个较短的确认窗口。检验标准是：你的响应速度是否快于智能体访问数据的速度——如果不是，这个控制就只是文档，而不是防御。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<h2 id="key-takeaways">Key Takeaways</h2>'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n" + anchor, 1)
    ren = {
        "Core Zero Trust Principles for AI": "What Are the Core Zero Trust Principles for AI?",
        "Identity for AI Agents": "Why Does Every AI Agent Need Its Own Identity?",
        "Data Access Controls via MCP": "How Do You Enforce Data Access Control Through MCP?",
        "Anomaly Detection and Response": "How Should Anomaly Detection and Automated Response Work?",
        "A Pragmatic Roadmap for Zero Trust": "What Does a Pragmatic Zero Trust Roadmap Look Like?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    anchor = '<h2 id="要点">要点</h2>'
    assert anchor in b, "cn anchor"
    b = b.replace(anchor, CN_NEW.strip() + "\n" + anchor, 1)
    ren_cn = {
        "人工智能核心零信任原则": "人工智能的零信任核心原则是什么？",
        "AI 代理的身份": "为什么每个AI代理都需要独立身份？",
        "通过 MCP 进行数据访问控制": "如何通过MCP落地数据访问控制？",
        "异常检测和响应": "异常检测与自动响应应该如何运作？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    for old, new in [('id="为什么传统边界安全挡不住AI风险？"', 'id="why-do-ai-agents-change-the-threat-model"'),
                     ('id="人工智能核心零信任原则"', 'id="what-are-the-core-zero-trust-principles"'),
                     ('id="AI 代理的身份"', 'id="why-every-agent-needs-its-own-identity"'),
                     ('id="通过 MCP 进行数据访问控制"', 'id="how-to-enforce-data-access-control-via-mcp"'),
                     ('id="异常检测和响应"', 'id="how-anomaly-detection-and-response-work"'),
                     ('id="要点"', 'id="key-takeaways"'),
                     ('id="结论"', 'id="conclusion"')]:
        b = b.replace(old, new)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
