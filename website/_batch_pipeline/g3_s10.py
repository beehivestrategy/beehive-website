#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "mcp-security-model-access-control-enterprise"

EN_NEW = """
<h2 id="how-should-you-scope-tool-permissions-per-user">How Should You Scope Tool Permissions Per User?</h2>
<p>The single most consequential design decision in an MCP deployment is whose authority a tool call runs under. Shared service accounts are the common shortcut, and they are also the decision that makes every other control weaker: if all calls run under one identity, per-user least privilege is impossible, attribution after an incident is impossible, and revocation means breaking the integration for everyone.</p>
<p>The correct model is delegated authority. The agent authenticates as itself, the user authenticates through single sign-on, and the resulting token carries the intersection of the two: the agent may only invoke tools on its allowlist, and it may only read data the requesting user is entitled to. A finance analyst and a warehouse supervisor asking the same question receive different answers, because the gateway resolves scope per request rather than per session.</p>
<p>In practice this means three things must be true. Tokens are issued per user and are short-lived, scoped to the specific tool and dataset rather than to the server as a whole. Permissions are resolved at the gateway, not inside the server, so a misconfigured server cannot widen its own access. And the effective scope is recorded with the call, so an auditor can reconstruct not just who asked but what they were entitled to at that moment.</p>
<p>Two scoping patterns cover most enterprise cases. <strong>Coarse scoping by data domain</strong> — this agent may read revenue and cost data, not HR records — is the right starting point and can usually be derived from existing RBAC roles. <strong>Row and column level scoping</strong> is required where entitlements vary within a domain, and it is best enforced at the server or the semantic layer where the query is constructed, because filtering after the fact means restricted data was technically retrieved.</p>
<h2 id="what-does-an-mcp-gateway-need-to-enforce">What Does an MCP Gateway Need to Enforce?</h2>
<p>If tool permissions are the policy, the gateway is where the policy becomes real. Six checks, in this order, and note that the sequence matters: cheap rejections first, expensive ones last.</p>
<table>
<thead>
<tr><th>Order</th><th>Check</th><th>Failure action</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Server is on the approved, versioned allowlist</td><td>Reject and alert — an unregistered server is an incident, not a warning</td></tr>
<tr><td>2</td><td>Caller identity is authenticated and the token is valid</td><td>Reject, force re-authentication</td></tr>
<tr><td>3</td><td>Tool is on the caller's allowlist</td><td>Reject and log the attempt with the full request context</td></tr>
<tr><td>4</td><td>Requested scope is within the caller's entitlements</td><td>Reject, return an explainable refusal rather than an empty result</td></tr>
<tr><td>5</td><td>Rate and cost budget for this caller is not exhausted</td><td>Throttle, notify the owner</td></tr>
<tr><td>6</td><td>Result passes output validation and masking rules</td><td>Mask or redact, then return with a note that redaction occurred</td></tr>
</tbody>
</table>
<p>Step four is where most implementations are weak. A gateway that returns an empty result set for an unauthorised query has technically enforced access control and practically leaked information, because the absence of data is itself a signal. Return an explicit, explainable refusal: the caller lacks entitlement for that dataset, and here is who to ask.</p>
<p>Step six is the one teams forget until a masking requirement appears in an audit. Output validation is also the last line of defence against prompt injection arriving through retrieved content: if a document the agent read contains instructions, output validation strips the instruction-bearing content before it reaches the model's next step.</p>
<h2 id="how-do-you-audit-mcp-tool-calls">How Do You Audit MCP Tool Calls?</h2>
<p>Logging in this category is usually either voluminous and useless, or absent. The useful middle is a structured record per call with seven fields.</p>
<ul>
<li><strong>Caller identity</strong> — both the agent identity and the on-behalf-of user.</li>
<li><strong>Tool and version</strong> — the specific tool invoked and the server version that served it, so behaviour changes can be correlated with deployments.</li>
<li><strong>Arguments</strong> — the full parameter set, redacted where arguments contain sensitive values.</li>
<li><strong>Scope granted</strong> — the entitlements actually applied, not just the roles nominally held.</li>
<li><strong>Result shape</strong> — row count, columns returned, and whether masking was applied. Not the results themselves, which keeps the audit log from becoming a second copy of the data.</li>
<li><strong>Decision and latency</strong> — allowed, rejected, throttled, or masked, with timings.</li>
<li><strong>Trace identifier</strong> — linking the call to the broader agent task, so a single user question can be reconstructed end to end.</li>
</ul>
<p>Three operational rules make the log worth keeping. Write it append-only and separately from the application logs the gateway itself produces, so an attacker who gains query access cannot edit the record. Retain it long enough to cover your regulatory window — ninety days is a common floor and one year is safer in regulated sectors. And alert on the gateway's own administrative actions, because changes to the allowlist or the policy are the highest-signal events in the whole system.</p>
<p>The test of an audit capability is a reconstruction exercise: pick a question asked three months ago and rebuild, from logs alone, what the agent did, what data it touched, and whether the access was authorised. If that takes more than a few minutes, the logging is not yet a control.</p>
<h2 id="what-are-the-most-common-mcp-security-mistakes">What Are the Most Common MCP Security Mistakes?</h2>
<p>Five mistakes account for most of the risk in real deployments, and none of them requires sophisticated tooling to avoid.</p>
<p><strong>Running servers with ambient credentials.</strong> A server launched with a database superuser connection string makes every downstream control decorative. Issue per-server identities scoped to what that server actually needs, and rotate them.</p>
<p><strong>Treating the allowlist as configuration rather than policy.</strong> If the tool list lives in an editable file on the host, it will be edited during an outage and never restored. Put it in version control with review, and have the gateway fetch from the approved source rather than trusting local state.</p>
<p><strong>Passing credentials through model context.</strong> Tokens that appear in prompts appear in logs, in provider-side retention, and potentially in another user's context after a bug. Keep secrets out of context entirely; the gateway injects them at execution time.</p>
<p><strong>Trusting tool output.</strong> Everything a tool returns is untrusted input to the next model step. Validate schema and volume, strip instruction-like content from retrieved documents, and treat unexpected shapes as errors rather than as data to reason about.</p>
<p><strong>Never testing the controls.</strong> Plant an instruction in a retrieved document and confirm nothing happens. Ask for data outside the caller's entitlement and confirm the refusal. Rotate a token and confirm the server fails closed rather than open. Controls that have never been exercised are assumptions, not controls.</p>
"""

FAQ = {
 "EN": [
  ("Is MCP secure enough for enterprise use out of the box?",
   "Not by default. MCP is a well-designed trust boundary rather than a security product: it does not authenticate servers, does not validate tool output, and relies on whatever transport you configure. Enterprise readiness comes from the controls around it - OAuth 2.1 with scoped per-user tokens, a gateway enforcing an allowlist, output validation, and complete audit logging."),
  ("Should MCP servers run under a service account?",
   "No. Service accounts make per-user least privilege impossible and destroy attribution after an incident. Use delegated authority: the agent authenticates as itself, the user authenticates through single sign-on, and the effective scope is the intersection of the two, resolved per request at the gateway."),
  ("How do you stop prompt injection through tool results?",
   "Treat every tool result as untrusted input. Validate schema and volume before the next step acts on it, strip instruction-like content from retrieved documents at the output validation stage, and enforce the tool allowlist at the gateway so a manipulated model cannot invoke an unlisted capability regardless of what it read."),
  ("What should be logged for each MCP tool call?",
   "Caller identity including the on-behalf-of user, tool and server version, redacted arguments, the scope actually granted, result shape with masking status, the decision and latency, and a trace identifier linking the call to the wider agent task. Store it append-only, separate from application logs, and alert on administrative actions."),
 ],
 "zh-CN": [
  ("MCP开箱即用地满足企业安全要求吗？",
   "默认状态下不满足。MCP是一个设计良好的信任边界，而不是一个安全产品：它不对服务器做身份认证，不校验工具输出，并且依赖于你所选择的传输方式。企业级可用性来自围绕它的控制措施——带逐用户作用域令牌的OAuth 2.1、执行白名单的网关、输出校验，以及完整的审计日志。"),
  ("MCP服务器应该运行在服务账号下吗？",
   "不应该。服务账号会让逐用户最小权限变得不可能，也会在事件发生之后摧毁归因能力。应使用委托授权：智能体以自身身份认证，用户通过单点登录认证，有效作用域是两者的交集，并在网关逐请求解析。"),
  ("如何阻止通过工具返回结果实施的提示词注入？",
   "把每一个工具返回结果都当作不可信输入。在下一步动作之前校验模式与数据量，在输出校验阶段剥离检索文档中的指令性内容，并在网关强制执行工具白名单——这样无论模型读到了什么，被操控的模型都无法调用清单之外的能力。"),
  ("每次MCP工具调用应该记录哪些内容？",
   "包括调用方身份（含所代表的用户）、工具与服务器版本、脱敏后的参数、实际授予的作用域、带脱敏状态的结果形态、判定与延迟，以及把本次调用与更大范围智能体任务关联起来的追踪标识。日志应追加写入、与应用日志分开存放，并对管理操作设置告警。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<section class="faq-section"'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n\n            " + anchor, 1)
    ren = {
        "Understanding the Current Technology Landscape": "What Does the MCP Threat Model Look Like?",
        "Technical Architecture and Integration Patterns": "What Does a Secure Enterprise MCP Architecture Include?",
        "Performance Benchmarks and Optimization Strategies": "How Much Overhead Do Security Controls Add?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    ren_cn = {
        "理解当前技术格局": "MCP部署的威胁模型是什么样的？",
        "技术架构与集成模式": "安全的企业MCP架构包含哪些组件？",
        "性能基准与优化策略": "安全控制会带来多少性能开销？",
        "企业部署最佳实践与实施建议": "企业MCP安全策略应该包含什么？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    dup = "企业实施路线图与成功因素"
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(dup) + r'(</h2>)', r'\g<1>' + "企业实施路线图的关键成功因素有哪些？" + r'\g<2>', b, count=1)
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(dup) + r'(</h2>)', r'\g<1>' + "规模化推广需要注意什么？" + r'\g<2>', b, count=1)
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape("战略实施路径与关键成功因素") + r'(</h2>)', r'\g<1>' + "战略实施路径与关键成功因素是什么？" + r'\g<2>', b, count=1)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
