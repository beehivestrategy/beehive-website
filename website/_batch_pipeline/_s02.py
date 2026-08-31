import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "mcp-enterprise-data-access-security-patterns"

EN_ADD = """
<h2 id="what-does-a-zero-trust-mcp-reference-architecture-look-like">What Does a Zero-Trust MCP Reference Architecture Look Like?</h2>
<p>Zero-trust becomes concrete when you stop describing it as a principle and start drawing zones. A workable MCP reference architecture has five, and the boundaries between them are where controls live. In the <em>client zone</em> sit the models, agents, and chat surfaces that originate requests; nothing here is trusted, and nothing here should hold a credential that outlives a single request. In the <em>gateway zone</em> a policy enforcement point authenticates the caller, resolves its identity to a principal, and decides whether the requested tool and parameter combination is permitted at all. The gateway is the only component allowed to reject a call, and it must fail closed.</p>
<p>In the <em>server zone</em> the MCP server exposes a deliberately narrow tool surface and holds no standing privileges of its own. In the <em>data boundary zone</em> the warehouse, lakehouse, or SaaS API applies its own row-level security, masking, and classification policies — inherited, not reimplemented. In the <em>telemetry zone</em> every invocation is recorded in a tamper-evident log with caller, tool, parameters, response size, and the policy decision that allowed it. The crucial property is that no single zone can both request data and authorise access to it; separation of duties is enforced structurally rather than by policy document.</p>
<table class="article-table">
<thead><tr><th>Zone</th><th>Primary control</th><th>Failure it prevents</th></tr></thead>
<tbody>
<tr><td>Client / agent</td><td>Short-lived, scoped credentials; no standing secrets</td><td>Credential theft from a compromised agent or plugin</td></tr>
<tr><td>Gateway / policy</td><td>Authentication, authorisation, parameter allowlists, rate limits</td><td>Prompt injection escalating into arbitrary tool invocation</td></tr>
<tr><td>MCP server</td><td>Narrow tool surface; concise, constraint-stating tool descriptions</td><td>Tool abuse and accidental over-permissioning</td></tr>
<tr><td>Data boundary</td><td>Impersonation or least-privilege roles; inherited RLS and masking</td><td>Models seeing rows or columns a human analyst could not query</td></tr>
<tr><td>Telemetry</td><td>Tamper-evident invocation log with policy decision attached</td><td>Undetectable exfiltration hidden inside routine model traffic</td></tr>
</tbody>
</table>
<h2 id="how-should-write-actions-approvals-and-rollback-be-handled">How Should Write Actions, Approvals, and Rollback Be Handled?</h2>
<p>Read paths and write paths are different risk categories and must not share a control model. A read that goes wrong leaks one answer; a write that goes wrong changes a record, sends an email, or moves money. Most MCP incidents we see in the field involve write tools that were added for convenience and then inherited the permissions of whatever service account happened to be configured. Six controls make write paths safe enough to expose to an agent.</p>
<p>First, make write capability explicit and separate: a server that only needs to answer questions should expose no write tools at all, and a server that does should declare them as a distinct, separately approved class. Second, require human approval for any action whose blast radius exceeds one record — approval should be a first-class step in the agent's workflow, not an afterthought bolted on after the first incident. Third, give every write an idempotency key so a retried or duplicated call cannot double-post an order or a payment. Fourth, offer a dry-run or diff mode: let the agent show the proposed change and its downstream effect before anything is committed. Fifth, define the compensating action for every write you expose; if you cannot describe how to undo it, do not expose it. Sixth, cap volume with rate limits and budget ceilings so a runaway loop becomes a stopped process rather than a corrupted quarter.</p>
<p>These controls are also what make agentic analytics adoptable. A conversational BI assistant that only reads through governed, approved tools can be deployed broadly and quickly; one that can quietly update a forecast or rewrite a budget line cannot, no matter how impressive the demo. The fastest route to production is almost always read-first, write-later, with the write surface added only after the audit trail has proven itself in read-only operation.</p>
<h2 id="what-evidence-do-auditors-and-risk-committees-expect">What Evidence Do Auditors and Risk Committees Expect?</h2>
<p>Security architecture only survives contact with an audit if it produces artefacts. The pattern that satisfies both internal risk committees and external auditors is to treat every MCP server as a registered application with an owner, a data classification, and a documented approval history. That registration then drives everything else: reviews, penetration tests, log retention, and decommissioning. Teams that skip registration end up with orphaned servers that nobody owns and nobody dares to switch off.</p>
<table class="article-table">
<thead><tr><th>Artefact</th><th>What it contains</th><th>Who signs it</th></tr></thead>
<tbody>
<tr><td>Tool inventory</td><td>Every exposed tool, its data classification, owner, and approval date</td><td>Data owner and platform owner</td></tr>
<tr><td>Identity map</td><td>Which principals and machine identities can invoke which tools</td><td>Identity and access management lead</td></tr>
<tr><td>Decision log</td><td>Immutable record of each invocation with the policy decision</td><td>Platform engineering</td></tr>
<tr><td>Threat model</td><td>Prompt injection, tool abuse, and data exfiltration scenarios with mitigations</td><td>Security architecture</td></tr>
<tr><td>Incident runbook</td><td>Revocation steps, kill switch, and notification path for agent misuse</td><td>Security operations</td></tr>
<tr><td>Retention schedule</td><td>How long logs are kept and who can read them</td><td>Compliance</td></tr>
</tbody>
</table>
<p>One practical note on logging: capture the parameters and the policy decision, but treat response payloads as sensitive. Logging full result sets turns your audit store into a second copy of the data you were trying to protect, and it will eventually be subpoenaed or breached. Log the shape and size of the response — row counts, columns touched, classification level — and keep payload-level detail only where a specific investigation requires it. That single design choice is usually the difference between an audit programme that scales and one that is quietly abandoned.</p>
"""

H2FIX = {
    "CN": [("常见问题", "企业在 MCP 安全上最常问的问题有哪些？")],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD}, tag=SLUG[:24])
