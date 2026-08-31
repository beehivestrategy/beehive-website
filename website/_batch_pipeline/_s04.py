import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "ai-governance-board-level-oversight"

EN_ADD = """
<h2 id="what-belongs-in-a-board-ai-risk-appetite-statement">What Belongs in a Board AI Risk Appetite Statement?</h2>
<p>A risk appetite statement is the shortest document a board will ever approve and the one that does the most work. It converts a vague feeling about AI into a set of boundaries that management can apply without coming back for permission on every use case. Three to five pages is enough, and the structure matters more than the length: classify AI use cases into risk tiers, state the board's appetite for each tier, and name the controls that are non-negotiable within it.</p>
<p>The tiers that work best are defined by consequence rather than by technology. A model that recommends which product to show a customer is a low-consequence use case; a model that declines a loan, prices an insurance policy, or screens a job applicant is high-consequence, regardless of how accurate it is. Boards often make the mistake of tiering by model type — generative versus predictive, third-party versus in-house — which produces a taxonomy that is obsolete within a year and a governance burden nobody can apply. Tiering by consequence survives model churn because the consequence does not change when the vendor does.</p>
<table class="article-table">
<thead><tr><th>Risk tier</th><th>Defining characteristic</th><th>Board appetite</th><th>Mandatory control</th></tr></thead>
<tbody>
<tr><td>Tier 1 — Low</td><td>Internal productivity; no customer or regulated outcome</td><td>Open; encourage experimentation</td><td>Usage logging and an acceptable-use policy</td></tr>
<tr><td>Tier 2 — Moderate</td><td>Influences customer experience but reversible by a human</td><td>Accept with monitoring</td><td>Human review path and quarterly quality reporting</td></tr>
<tr><td>Tier 3 — High</td><td>Affects credit, employment, pricing, safety, or regulated filings</td><td>Cautious; limited to approved use cases</td><td>Documented model validation, bias testing, and explainability</td></tr>
<tr><td>Tier 4 — Prohibited</td><td>Board has determined the organisation will not deploy</td><td>None</td><td>Explicit prohibition recorded in the risk register</td></tr>
</tbody>
</table>
<p>Two clauses make the statement operational. The first is a named owner for each tier — usually the accountable executive, not a committee — because anonymous ownership produces anonymous decisions. The second is a change trigger: any movement of a use case between tiers requires board notification, which prevents the slow migration of high-risk systems into low-risk buckets through incremental feature releases.</p>
<h2 id="what-does-good-board-reporting-on-ai-actually-look-like">What Does Good Board Reporting on AI Actually Look Like?</h2>
<p>Most AI reporting to boards fails for the same reason most project reporting fails: it describes activity instead of outcomes. A dashboard listing twelve pilots, their technology stacks, and their sprint status tells a director nothing they can act on. Effective reporting fits on one page, arrives on a fixed cadence, and answers four questions: what value did we realise, what risk did we take on, what changed since last quarter, and what decision do you need from us?</p>
<p>The metrics should be few and stable, because a board that receives a different set of numbers each quarter cannot detect trends. Value metrics should be expressed in the same units the board uses for other investments — revenue influenced, cost avoided, hours redeployed — with a clear statement of baseline and attribution method. Risk metrics should include the size of the AI inventory, the count of tier 3 systems, open model-risk findings with ages, and any incident since the last report. Both should be presented against the prior period, not just against a target, because drift is the signal directors are there to catch.</p>
<table class="article-table">
<thead><tr><th>Metric</th><th>Definition</th><th>Cadence</th><th>Owner</th></tr></thead>
<tbody>
<tr><td>Realised value</td><td>Measured benefit against pre-agreed baseline, with attribution method stated</td><td>Quarterly</td><td>CFO / business sponsor</td></tr>
<tr><td>Inventory size and tier mix</td><td>Count of AI systems by risk tier, with movement since last report</td><td>Quarterly</td><td>CIO / CDO</td></tr>
<tr><td>Open model-risk findings</td><td>Number, severity, and age of unresolved validation or bias findings</td><td>Quarterly</td><td>Model risk / internal audit</td></tr>
<tr><td>Incidents and near misses</td><td>Customer-impacting errors, escalations, and remediations completed</td><td>Every meeting</td><td>COO</td></tr>
<tr><td>Regulatory change exposure</td><td>Obligations with compliance dates inside the next four quarters</td><td>Semi-annually</td><td>General Counsel</td></tr>
</tbody>
</table>
<p>Directors should also read the absences. If the report contains no incidents at all, the detection capability is probably untested rather than the organisation being perfect. If every pilot shows positive ROI, the measurement framework is marketing rather than accounting. And if the same use case has appeared as "in progress" for three consecutive quarters, the constraint is organisational, not technical — which is precisely the kind of finding a board is uniquely positioned to act on.</p>
<h2 id="how-should-the-board-handle-an-ai-incident">How Should the Board Handle an AI Incident?</h2>
<p>Incidents are where governance either proves itself or is revealed as decoration. The failure pattern is consistent across industries: a model error reaches customers, the response is improvised, and the board learns about it from the press or from a regulator. A pre-agreed escalation ladder prevents that, and it costs almost nothing to build in advance.</p>
<p>The ladder should define three things for each severity level: who is notified and within how long, who has authority to switch the system off, and what must be documented before the system is switched back on. Severity is best defined by customer and regulatory consequence rather than by technical scope — a wrong answer to an internal analyst and a wrong answer in a customer-facing credit decision are not the same event, even if the root cause is identical. Crucially, the authority to disable a system must sit with an operational role that can act in minutes, with board notification following rather than preceding the action.</p>
<p>After the incident, the board should require a written review that distinguishes proximate cause from systemic cause. A model that hallucinated is a proximate cause; the absence of a review step before customer-facing output is the systemic one. Boards that accept proximate-cause explanations get the same incident again in a different system. Boards that insist on systemic cause get a control, an owner, and a date — which is the only durable output an incident review produces.</p>
"""

process(SLUG, {}, adds={"EN": EN_ADD}, tag=SLUG[:24])
