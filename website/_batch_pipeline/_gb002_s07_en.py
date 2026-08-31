# -*- coding: utf-8 -*-
"""Expand the EN body of ai-risk-assessment-year-end-enterprise-oct2025."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb002_h2 import rename_h2, add_tail_section, replace_faq_list

P = 'blog/articles/ai-risk-assessment-year-end-enterprise-oct2025.html'

for old, new in [
    ("The Risk Picture Heading Into 2026", "What Does the AI Risk Picture Look Like Heading Into 2026?"),
    ("Key Benefits and ROI Considerations", "What Return Does an AI Risk Assessment Deliver?"),
    ("Implementation Roadmap and Next Steps", "How Do You Run an AI Risk Assessment in 60 Days?"),
]:
    print(rename_h2(P, old, new))

S1 = """<p>Every downstream finding depends on the inventory, and the inventory is almost always incomplete on the first pass. Most enterprises undercount their AI systems by a wide margin, because the systems that carry the most risk are frequently not registered as AI at all.</p>
<p>Four sources, searched together, close most of the gap. <strong>Procurement and expense records</strong> surface shadow adoption: the free-tier tools and embedded features business units started using without a review, which is where a large share of unmanaged data flow originates. <strong>API and cloud billing</strong> reveals model calls by key and by project, which is the most reliable evidence of what is actually running in production rather than what was approved. <strong>Code and repository search</strong> finds direct model integrations, prompt templates, and agent definitions that were built by engineering without a governance ticket. <strong>Embedded feature review</strong> of the SaaS estate identifies AI capabilities that vendors enabled inside products you already pay for — the category that surprises assessment teams most, because it arrives without a purchase decision.</p>
<p>For each system discovered, capture six fields: business owner, technical owner, the data it can reach, the decisions it influences, whether it is customer-facing, and which regulatory regimes apply. Six fields is enough to classify risk and assign remediation; anything longer and the inventory stops being maintained. The output that matters is not the count of systems but the count of systems with a named owner — an unowned system cannot be remediated, and the size of that gap is usually the single most useful number an assessment produces.</p>"""

S2 = """<p>A red-team pass on an AI system is not a penetration test with a different name. The objective is not to break in but to make the system do something its designers did not intend, using only the access a legitimate user or an external party would have.</p>
<p>Five test classes cover most of the realistic exposure:</p>
<ul>
<li><strong>Prompt injection, direct and indirect.</strong> Can instructions embedded in retrieved documents, web pages, images, or uploaded files change the system's behaviour? Indirect injection through retrieved content is the variant most often missed, because the payload never comes from the user.</li>
<li><strong>Data leakage through output.</strong> Can the system be induced to reveal another user's records, training excerpts, system prompts, or internal identifiers? Test with targeted extraction attempts rather than obvious requests, and test across tenants if the system is multi-tenant.</li>
<li><strong>Entitlement escalation.</strong> Does a user with restricted access receive the same answer as a privileged user? The failure mode is rarely a missing login check and usually a retrieval layer that does not carry the caller's permissions into the query.</li>
<li><strong>Output robustness.</strong> What happens under ambiguous, adversarial, or out-of-distribution inputs? Systems that fabricate confidently under uncertainty are a distinct risk from systems that refuse.</li>
<li><strong>Agent and tool abuse.</strong> If the system can call tools — send email, query databases, execute transactions — can it be induced to take an unintended action? Logging of tool calls matters as much as blocking them.</li>
</ul>
<p>Record every finding with reproduction steps, severity, and the specific control that should have prevented it. That last field is what turns a red-team report into a remediation plan: a finding without a corresponding control is an observation, whereas a finding mapped to a named control is a work item with an owner.</p>"""

S3 = """<p>An assessment that ends with a risk register and no recurring process produces a snapshot that is obsolete within a quarter. Three mechanisms keep it alive.</p>
<p>First, <strong>a standing review cadence with a defined trigger set</strong>. Quarterly review is the floor, but the more useful design is event-driven: a new model version, a new data source, a new vendor, a material prompt change, or an incident all reopen the assessment for the affected system. AI systems change faster than annual governance cycles, so trigger-based review is what keeps the register accurate.</p>
<p>Second, <strong>a single accountable owner per system, with decision rights</strong>. Committees that approve AI deployments but do not own them create the classic gap: nobody is responsible for the model after launch. The workable split is a business owner accountable for outcomes and acceptable risk, a technical owner accountable for monitoring and rollback, and a governance function accountable for the framework and the evidence. Where those three are unclear, findings stall.</p>
<p>Third, <strong>assessment artefacts wired into existing processes</strong> rather than maintained separately. Model inventories should feed procurement and vendor review; risk classifications should feed release gates; incident playbooks should be tested alongside existing security exercises. Every artefact that lives only in the assessment document will decay, and the assessment will be repeated from scratch next year — which is precisely the outcome the exercise is meant to prevent.</p>"""

S4 = """<p>Boards and budget holders do not need a risk register; they need a legible trend. A small set of posture metrics, measured identically each quarter, answers the question that actually gets asked — is our exposure going up or down?</p>
<table class="data-table"><thead><tr><th>Metric</th><th>What it shows</th><th>Healthy trajectory</th></tr></thead><tbody>
<tr><td>Share of production AI systems with a named owner and rollback plan</td><td>Whether accountability exists</td><td>Rising; target near 100% for customer-facing systems</td></tr>
<tr><td>Share of high-risk data sources under enforced permissioning</td><td>Whether access controls reach the data</td><td>Rising, with unclassified sources approaching zero</td></tr>
<tr><td>Mean time to remediate an open finding</td><td>Whether the process has teeth</td><td>Falling quarter over quarter</td></tr>
<tr><td>Count of unclassified or shadow AI systems</td><td>Whether discovery is keeping pace with adoption</td><td>Falling, or rising then falling as discovery improves</td></tr>
<tr><td>Share of models with evaluation sets re-run on change</td><td>Whether testing is real or aspirational</td><td>Rising toward full coverage</td></tr>
</tbody></table>
<p>Two cautions make the difference between a useful metric and a vanity one. Report the denominator as well as the numerator — "eight findings remediated" means nothing without "of nineteen open" — and resist the urge to change definitions between quarters. The most common failure is redefining what counts as an AI system just as the number starts to look bad, which destroys the trend exactly when it becomes informative.</p>
<p>Pair the posture metrics with one forward-looking number: the estimated cost of the top five unmitigated risks, expressed in the same units as the remediation budget. That framing converts an abstract risk discussion into a capital allocation decision, and it is the version of the assessment that survives contact with a budget review.</p>"""

for sid, title, body in [
    ("how-do-you-build-a-complete-ai-system-inventory", "How Do You Build a Complete AI System Inventory?", S1),
    ("what-should-a-red-team-exercise-on-an-ai-system-cover", "What Should a Red-Team Exercise on an AI System Cover?", S2),
    ("how-should-ai-risk-be-governed-after-the-assessment", "How Should AI Risk Be Governed After the Assessment?", S3),
    ("which-metrics-show-whether-ai-risk-is-actually-falling", "Which Metrics Show Whether AI Risk Is Actually Falling?", S4),
]:
    print(add_tail_section(P, sid, title, body))

FAQ = [
    ("How long does a year-end AI risk assessment take?",
     "Sixty days is realistic for a mid-sized enterprise, run in three passes: roughly two to three weeks on inventory, two to three weeks on testing the highest-exposure systems, and the remainder on remediation planning and governance setup. The variable that moves this most is inventory quality — organisations that have never enumerated their AI systems, including embedded SaaS features and shadow deployments, should budget the first pass generously, because everything downstream depends on it."),
    ("What is the single most common finding in AI risk assessments?",
     "Unowned systems. Assessments routinely discover AI applications — embedded vendor features, departmental pilots, free-tier tools — with no named business or technical owner, which means nobody is monitoring drift, nobody owns the rollback decision, and no one can say what data the system can reach. Assigning owners is usually the cheapest and highest-value remediation in the entire plan, and it is a prerequisite for everything else."),
    ("Do we need to assess AI features embedded in the SaaS tools we already buy?",
     "Yes, and this is the category most often missed. Vendors enable AI capabilities inside products you already pay for, so the adoption arrives without a purchase decision, a review, or a data protection assessment. Review your SaaS estate for enabled AI features, determine what data each one can reach and whether it is used for the vendor's own model training, and record the outcome in the same inventory as your in-house systems."),
    ("How does the EU AI Act change what the assessment needs to cover?",
     "It makes classification and documentation mandatory rather than advisable. Obligations for general-purpose AI models have applied since 2 August 2025, with fines up to €35 million or 7% of global annual turnover for prohibited practices. Practically, the assessment must classify each system against the Act's risk tiers, produce or update model documentation, and demonstrate human oversight — evidence that regulators expect to be able to inspect rather than take on trust."),
    ("Is a red-team exercise necessary, or is a security review enough?",
     "A conventional security review does not cover the failure modes specific to AI systems. Prompt injection through retrieved content, data leakage induced by careful phrasing, and tool misuse by an agent are not findings a standard review produces. A targeted red-team pass on the systems that touch customers or personal data is the only way to test them, and it is inexpensive relative to the exposure it closes."),
    ("What should we do with the findings once the assessment is complete?",
     "Convert them into a short, owned, dated remediation plan and wire review into an existing cadence. A register of five to ten prioritised items with named owners and deadlines is far more effective than a comprehensive spreadsheet, and the artefacts should feed procurement, release gates, and incident playbooks rather than living in a standalone document. Re-run the assessment on triggers — new model, new data source, new vendor, material prompt change — rather than waiting a year."),
]
print(replace_faq_list(P, FAQ, "en"))
