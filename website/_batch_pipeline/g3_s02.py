#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "mcp-tool-use-advanced-patterns"

EN_NEW = """
<h2 id="how-do-you-design-a-tool-schema-the-model-can-actually-use">How Do You Design a Tool Schema the Model Can Actually Use?</h2>
<p>Tool descriptions are the interface contract between a probabilistic caller and deterministic systems, and they are the single highest-leverage place to spend engineering time. A model cannot call a tool it does not understand, and it will confidently call the wrong one if two descriptions overlap. Six rules hold up in production.</p>
<table>
<thead>
<tr><th>Rule</th><th>Weak version</th><th>Production version</th></tr>
</thead>
<tbody>
<tr><td>Name as a verb phrase</td><td><code>data</code></td><td><code>query_revenue_by_region</code></td></tr>
<tr><td>One tool, one decision</td><td><code>run_report(type, params)</code> handling twelve report types</td><td>Separate tools per report, each with its own schema</td></tr>
<tr><td>Constrain the inputs</td><td><code>granularity: string</code></td><td><code>granularity: enum[day, week, month, quarter]</code></td></tr>
<tr><td>Trim the output</td><td>Returns 40,000 rows and fifty columns</td><td>Returns aggregates plus a row count and a sample</td></tr>
<tr><td>Say when not to use it</td><td>"Useful for data questions"</td><td>"Use for aggregated revenue. Do not use for row-level exports; use <code>export_dataset</code> instead."</td></tr>
<tr><td>Describe the failure modes</td><td>No error contract</td><td>"Returns 403 when the caller lacks scope for the requested region."</td></tr>
</tbody>
</table>
<p>The last two rows are the ones teams skip, and they are the ones that matter most. Negative guidance — when <em>not</em> to call a tool — is what prevents a model from picking a plausible-looking neighbour when twelve tools share a vocabulary. An explicit error contract is what lets the agent distinguish "retry this" from "stop and escalate", which is the difference between a loop that recovers and a loop that burns budget repeating a forbidden call.</p>
<p>Treat schemas as versioned public APIs. Every change to a description is a behavioural change to every agent that can see the tool, so put schemas in source control, review description edits like code, and keep a compatibility window when you rename or split a capability.</p>
<h2 id="what-does-a-production-tool-use-loop-look-like-end-to-end">What Does a Production Tool-Use Loop Look Like End to End?</h2>
<p>The abstract loop — plan, call, observe, iterate — hides most of the engineering. A single enterprise request, traced end to end, looks like this:</p>
<ol>
<li><strong>Request arrives with identity attached.</strong> A user asks "why did EMEA margin drop last quarter?" The requesting user's identity and entitlements travel with the request; the agent never holds a shared credential.</li>
<li><strong>Tool retrieval.</strong> With eighty registered tools, the agent does not see all eighty. A routing step selects the six relevant candidates and injects only their schemas into context, which keeps the prompt small and the choice tractable.</li>
<li><strong>Plan and first call.</strong> The agent plans a sequence — fetch revenue by region, fetch cost by region, compute margin — and issues the two independent calls concurrently rather than serially.</li>
<li><strong>Validation.</strong> Each result is checked against expectations: schema matches, row count is plausible, data freshness is inside the agreed window. A stale partition is caught here, not three steps later.</li>
<li><strong>Iteration under a budget.</strong> The agent refines — drills into the two regions driving the drop — bounded by a hard cap on steps, tool calls, and elapsed time. Exceeding the cap is a designed outcome that fails cheaply and escalates with the trace attached.</li>
<li><strong>Escalation or answer.</strong> If confidence is below threshold or the request touches a restricted scope, the agent hands off to a human with the full trace. Otherwise it answers, citing the tools, queries, and data timestamps it used.</li>
<li><strong>Record everything.</strong> The complete call trace — tools selected, arguments, results sizes, latency, cost — is written to the audit log. This is what makes the system debuggable after the fact and defensible to an auditor.</li>
</ol>
<p>Notice that the model is a minority of the code. Routing, validation, budgeting, and logging are most of the work, and they are what separate a demo that answers one question from a system that answers ten thousand a day.</p>
<h2 id="how-should-you-test-and-evaluate-tool-using-agents">How Should You Test and Evaluate Tool-Using Agents?</h2>
<p>Unit tests do not transfer. A tool-using agent can pass every component test and still pick the wrong tool, loop forever, or return a confidently wrong number. Evaluation needs five layers.</p>
<ul>
<li><strong>Golden task sets.</strong> Fifty to two hundred real questions with known-correct answers, run on every schema or prompt change. This is your regression suite, and it is the only thing that catches silent quality drift.</li>
<li><strong>Trace assertions.</strong> Assert on the sequence, not just the answer: the agent called the revenue tool before the margin calculation, it did not call the export tool, it stayed under eight steps.</li>
<li><strong>Fault injection.</strong> Make a tool return a 403, a timeout, a stale partition, and a malformed payload, then verify the agent classifies each correctly — retry, escalate, or stop. Most production incidents are classification failures, not capability failures.</li>
<li><strong>Budget tests.</strong> Assert worst-case cost and latency per task. A ten-step loop over a wide fan-out is affordable in a demo and unaffordable at ten thousand requests a day.</li>
<li><strong>Permission tests.</strong> Run the same question under several user identities and confirm the agent never returns data the caller could not have queried directly. This is the test that keeps a tool-use program out of the incident reports.</li>
</ul>
<p>Run the golden set in CI and the fault and permission suites on a schedule. The failure mode of agent systems is not a loud break; it is a gradual drift in tool selection accuracy that nobody notices until a business user stops trusting the answers.</p>
<h2 id="what-breaks-first-at-enterprise-scale">What Breaks First at Enterprise Scale?</h2>
<p>Five failure modes show up consistently once tool use moves from a pilot to a shared platform, and all of them are organisational as much as technical.</p>
<p><strong>Tool sprawl.</strong> Three teams ship forty tools each, half of them overlapping, and tool selection accuracy collapses. The fix is governance: a registry with named owners, a review before a tool becomes visible to shared agents, and a deprecation path. Treat tool count as a budget, not an achievement.</p>
<p><strong>Context bloat.</strong> Every tool schema and every verbose result consumes context, and cost grows while accuracy degrades. Retrieve tool schemas instead of listing them, trim results server-side, and summarise intermediate steps aggressively.</p>
<p><strong>Permission creep.</strong> Agents start scoped to one user and end up running under a service account because that was easier during an integration. Enforce per-request identity at the MCP layer so that the shortcut is not available, and alert on any agent identity that accesses data on behalf of more than one user.</p>
<p><strong>Cost surprises.</strong> A loop that costs pennies in testing costs thousands at production volume when a common query fans out across six tools and twelve model calls. Set per-request cost ceilings and surface cost per task on the same dashboard as latency.</p>
<p><strong>Silent failure.</strong> The worst outcome is an agent that answers confidently from a stale or partial result. Validation gates, freshness checks, and visible citations in every answer are what turn silent failure into a visible one.</p>
"""

FAQ = {
 "EN": [
  ("How is MCP different from building a traditional API integration?",
   "A traditional integration is point to point: you write and maintain a connector for every model-to-system pair. MCP standardises the capability description, so one MCP server can be discovered and invoked by any compatible client. The saving is not the first integration, it is the twentieth - and the uniform place it gives you to enforce allowlists, identity and audit."),
  ("How many tools should a single MCP server expose?",
   "Fewer than teams want. Tool selection accuracy degrades as candidate count grows, so expose narrowly scoped tools and use a retrieval step to inject only the relevant schemas into context. A practical ceiling is roughly twenty visible tools per agent, with a registry and named owners governing anything beyond that."),
  ("How do you stop an agent from making unauthorised tool calls?",
   "Enforce the allowlist at the MCP layer rather than in the prompt, so a manipulated model cannot invoke an unlisted capability. Run every call under the requesting user's identity rather than a shared service account, keep credentials out of model context, and log each call with identity, arguments and scope for post-hoc audit."),
  ("What does it cost to run tool-using agents at enterprise scale?",
   "Cost is driven by round trips and context size, not by model size. Parallel fan-out, server-side aggregation and aggressive trimming of tool outputs typically cut cost per task by more than half. Set a per-request ceiling on steps, tool calls and tokens, and monitor cost per task alongside latency from the first week."),
 ],
 "zh-CN": [
  ("MCP与传统的API集成有什么不同？",
   "传统集成是点对点的：每一组模型与系统的对接都需要单独编写和维护连接器。MCP把能力描述标准化，因此一个MCP服务器可以被任何兼容的客户端发现并调用。真正的节省不在于第一次集成，而在于第二十次——以及它提供了一个统一的位置来强制执行工具白名单、身份校验和审计。"),
  ("一个MCP服务器应该暴露多少个工具？",
   "比团队想要的更少。候选工具数量越多，工具选择的准确率越低，因此应该暴露范围收窄的工具，并用检索步骤只把相关的模式注入上下文。经验上的上限是每个智能体可见约二十个工具，超过这个规模就需要用注册表和具名负责人来治理。"),
  ("如何阻止智能体发起未授权的工具调用？",
   "把白名单执行在MCP层，而不是写在提示词里，这样即使模型被操控也无法调用清单之外的能力。每次调用都使用请求用户的身份，而非共享服务账号；凭证绝不进入模型上下文；每次调用都要记录身份、参数与授权范围，以便事后审计。"),
  ("在企业规模上运行会调用工具的智能体，成本如何？",
   "成本主要由往返次数和上下文体积决定，而不是模型规模。并行扇出、服务端聚合以及大幅裁剪工具输出，通常能把单次任务的成本压低一半以上。从第一周起，就要为步骤数、工具调用数和token数设定单次请求上限，并把单次任务成本与延迟放在同一个仪表盘上监控。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<section class="faq-section"'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n\n            " + anchor, 1)
    ren = {
        "The Current State of Enterprise Architecture": "Why Does Enterprise Architecture Need a Common Tool Protocol?",
        "Technical Implementation Patterns": "Which Implementation Patterns Hold Up in Production?",
        "Performance and Scalability Considerations": "What Determines Performance and Scalability?",
        "Security and Compliance Integration": "How Do You Integrate Security and Compliance?",
        "Looking Ahead: What to Expect": "What Should Enterprises Expect Next From MCP?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    ren_cn = {
        "企业架构现状": "为什么企业架构需要统一的工具协议？",
        "技术实施模式": "哪些实施模式在生产环境中站得住脚？",
        "性能与可扩展性考量": "什么决定了性能与可扩展性？",
        "安全与合规整合": "如何整合安全与合规？",
        "未来展望": "企业接下来应该期待MCP带来什么？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
