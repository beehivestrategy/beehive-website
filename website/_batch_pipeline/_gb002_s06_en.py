# -*- coding: utf-8 -*-
"""Expand the EN body of ai-professional-services-beyond-billable-hours."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb002_h2 import rename_h2, add_tail_section, replace_faq_list, _read, _write

P = 'blog/articles/ai-professional-services-beyond-billable-hours.html'

# repair an unwrapped paragraph left by an earlier pass
raw = _read(P)
BAD = ('There is also a practical sequencing question every firm faces: how fast can this actually happen? '
       'Faster than most firms assume, because the analytics layer does not require replacing the firm&#39;s core systems.')
if BAD in raw and '<p>' + BAD not in raw:
    raw = raw.replace(BAD, '<p>' + BAD + '</p>')
    _write(P, raw)
    print('wrapped orphan paragraph')

for old, new in [
    ("Industry Transformation Through AI in 2025", "How Is AI Reshaping Professional Services in 2025?"),
    ("Financial Services: AI as a Competitive Differentiator", "Why Does AI Become a Competitive Differentiator for Firms?"),
    ("The Human-AI Collaboration Imperative", "How Should Firms Structure Human-AI Collaboration?"),
]:
    print(rename_h2(P, old, new))

S1 = """<p>Moving from hours to outcomes is a pricing problem before it is a technology problem, and the firms that do it well change three things at once.</p>
<p>First, they <strong>separate the deliverable from the effort</strong>. A fixed-fee engagement is only safe if you can predict your cost to deliver, and AI makes that possible for the first time on knowledge work: once drafting, review, and research capacity is measured in minutes rather than days, the distribution of effort on a repeatable matter narrows enough to price against. The firms that succeed start with their most standardised engagements — the ones they have delivered dozens of times — and expand the fixed-fee perimeter as the data accumulates.</p>
<p>Second, they <strong>price the outcome, not the activity</strong>. Value-based pricing works where the client can name what success looks like: a transaction that closes, a tax position that withstands review, a compliance programme that passes an examination. AI shifts the economics in the firm's favour because the marginal cost of the underlying work falls while the value of a correct outcome does not. The negotiation becomes about sharing that gap rather than about discounting hours.</p>
<p>Third, they <strong>renegotiate the efficiency split deliberately</strong>. Clients are sophisticated enough to know that work got faster, and they will ask for the saving. The firms that hold margin decide in advance what share of the efficiency gain they pass through, and they can articulate what the client receives in exchange — faster turnaround, deeper coverage, senior attention on the parts that matter. Losing that argument usually comes from not having decided the answer before the client asked.</p>"""

S2 = """<p>The talent question is the one partners raise most often and plan for least. If AI does the work juniors used to do, what do juniors learn, and who becomes the senior professional in five years?</p>
<p>The traditional apprenticeship was inefficient in ways that are easy to forget: juniors learned judgement partly by doing repetitive work and absorbing its patterns. Remove that work without replacing the learning and you get a thin bench. The firms redesigning this deliberately create three substitutions. <strong>Verification work replaces production work</strong>: reviewing a machine-generated first draft for errors, omissions, and unsupported inferences teaches the same pattern recognition that producing the draft did, and it is faster. <strong>Exception work replaces routine work</strong>: the cases the model gets wrong are the ones worth a junior's attention, and they are disproportionately the interesting ones. <strong>Structured rotation through client-facing work accelerates</strong>, because the constraint on that exposure was previously the time spent producing the deliverable.</p>
<p>Two metrics tell you whether the redesign is working. The first is ramp time to a defined competence threshold — if AI-enabled juniors are not reaching it faster, the firm has removed the work without replacing the learning. The second is the quality of work reaching partners for review: if partner review time is falling while rework rates are flat, the leverage is real; if review time is flat because output needs more correction, the firm has simply shifted the work upward.</p>
<p>There is also a hiring implication. Firms that advertise "no more document review" attract candidates for the wrong reason and lose them when the reality of verification work sets in. The honest pitch — you will spend your first two years directing and checking machine output rather than producing it, and you will reach client-facing judgement work faster — is both more accurate and more attractive to the people who will actually thrive.</p>"""

S3 = """<p>Professional services AI is unusual in that its inputs are the firm's most sensitive assets: client matter files, financial records, privileged communications, and personal data. That raises the bar on the data foundation in ways general-purpose AI deployments do not.</p>
<ul>
<li><strong>Matter-level entitlement.</strong> Any retrieval system must enforce the same conflict and confidentiality walls a partner observes. An assistant that can surface a document from an unrelated matter because it was in the same index is a professional-indemnity incident, not an inconvenience.</li>
<li><strong>Client-segregated context.</strong> Cross-client learning is valuable for the firm and unacceptable to clients unless explicitly agreed. The safe design keeps client data out of anything that could leak across engagements, including fine-tuning corpora and prompt caches.</li>
<li><strong>Source-grounded answers.</strong> A professional cannot act on an unsourced assertion. Every answer should carry the document, the figure, and the extraction path, so the professional can verify before advising.</li>
<li><strong>Retention aligned to engagement terms.</strong> Engagement letters set retention obligations, and AI artefacts — prompts, retrieved context, generated drafts — are part of the record. They need the same schedule as the matter file.</li>
</ul>
<p>The practical consequence is that the analytics and governance layer matters more than the model. A firm that connects a language model to an ungoverned document store has created a fast path to confidential material; a firm that connects it to a semantic layer enforcing matter-level entitlement has created leverage. This is also why deployment speed varies so much between firms with similar ambitions — the variable is rarely the model, it is whether governed access to the firm's own data already exists.</p>"""

S4 = """<p>Most firms measure AI adoption with activity metrics — licences issued, prompts run, documents processed — and then cannot answer the partner who asks whether any of it improved the business. Four measures connect adoption to outcomes.</p>
<table class="data-table"><thead><tr><th>Measure</th><th>What it captures</th><th>Healthy signal</th></tr></thead><tbody>
<tr><td>Cycle time per standard engagement</td><td>Whether delivery actually got faster</td><td>Falling, with quality held constant</td></tr>
<tr><td>Realisation rate</td><td>Whether the efficiency reached the P&amp;L</td><td>Stable or rising despite fewer hours billed</td></tr>
<tr><td>Leverage mix</td><td>Whether senior time moved up the value chain</td><td>Partner time shifting from review to origination</td></tr>
<tr><td>Rework rate on AI-assisted output</td><td>Whether the output is actually usable</td><td>Falling as prompts and verification mature</td></tr>
</tbody></table>
<p>The second row is the one that gets skipped, and it is where the strategy either holds or fails. Efficiency that shows up only as fewer billed hours is a revenue problem, not a productivity gain; it has to show up as improved realisation on fixed-fee work, as more engagements won, or as capacity redeployed to origination. Firms that measure the first and not the second routinely conclude that AI is eroding revenue, when what is actually happening is that they improved delivery without changing how they sell.</p>
<p>One caution on baselines: measure before deployment, not after. Firms that start measuring once the tool is live have no counterfactual, and the resulting debate about whether a 20% cycle-time improvement is real or seasonal tends to stall the programme at exactly the moment it needs a second phase of funding.</p>"""

for sid, title, body in [
    ("how-do-you-move-from-billable-hours-to-value-based-pricing", "How Do You Move From Billable Hours to Value-Based Pricing?", S1),
    ("what-changes-for-junior-professionals-and-the-talent-pipeline", "What Changes for Junior Professionals and the Talent Pipeline?", S2),
    ("what-data-and-governance-do-professional-services-ai-need", "What Data and Governance Do Professional Services AI Systems Need?", S3),
    ("how-do-you-measure-whether-ai-adoption-is-paying-off", "How Do You Measure Whether AI Adoption Is Paying Off?", S4),
]:
    print(add_tail_section(P, sid, title, body))

FAQ = [
    ("Will AI eliminate the billable hour?",
     "Not in the near term, but it is changing what the billable hour buys. Clients increasingly refuse to pay professional rates for work a machine performs, so the hours attributed to routine production are compressing. What is growing is fixed-fee and value-based work, where AI makes the cost of delivery predictable enough to price against. The practical shift is not the disappearance of time-based billing but the migration of high-margin work toward engagements priced on outcome."),
    ("How should a firm start moving to value-based pricing?",
     "Start with the engagements you have delivered most often. Standardised matters have a narrow enough effort distribution to price safely once AI compresses the production work, and they give you the delivery data to price the next tier confidently. Set a baseline on cycle time and cost before you begin, decide deliberately what share of the efficiency gain you pass to the client, and expand the fixed-fee perimeter only where the data supports it."),
    ("What happens to junior professionals if AI does the entry-level work?",
     "They need a redesigned apprenticeship, and the firms doing this well replace production work with verification and exception work. Reviewing machine-generated drafts for errors and omissions builds the same pattern recognition that drafting did, and it is faster; the cases the model gets wrong are disproportionately the instructive ones. The measurable test is ramp time to a defined competence threshold — if it is not falling, the firm has removed the work without replacing the learning."),
    ("How do firms keep client data safe when using AI?",
     "By enforcing entitlement at the data layer rather than trusting the model. Matter-level access controls must apply to AI retrieval exactly as they apply to a partner, client data must not flow into shared fine-tuning corpora or cross-client caches, and every answer should carry its source so a professional can verify it before advising. AI artefacts such as prompts and generated drafts are also part of the matter record and inherit its retention obligations."),
    ("Which professional services functions benefit most from AI?",
     "The ones with high document volume and repeatable structure: legal document review, contract analysis, and due diligence; accounting reconciliation, classification, and disclosure drafting; audit sampling and testing; and consulting research synthesis and benchmarking. In each case the machine handles exhaustive reading and computation while the professional owns interpretation, judgement, and the client conversation. The gain is largest where volume is high and the underlying pattern is stable."),
    ("How quickly can a professional services firm deploy AI on its own data?",
     "Weeks rather than quarters for a first working capability, provided the firm is not rebuilding its data estate. A conversational analytics layer that connects to existing time-and-expense, CRM, and matter or engagement systems can answer utilisation, realisation, pipeline, and margin questions in about two weeks. The long pole is usually governed access and metric definitions, not the model — firms with clean entitlement models and agreed definitions move fastest."),
]
print(replace_faq_list(P, FAQ, "en"))
