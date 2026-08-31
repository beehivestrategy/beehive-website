#!/usr/bin/env python3
"""EN body expansion, batch 2 (4 slugs + 2 top-ups)."""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb002_lib import apply_ops

DATA = {}

# ---- top-ups -------------------------------------------------------------
DATA['ai-budget-justification-framework-q4-planning'] = dict(before='__FAQ__', inserts=[
    ("How Should You Present the Case to the Committee?", """
<p>The content of the pack matters less, in the room, than the order in which it arrives. Committees do not read a business case; they interrogate it, and they interrogate in a predictable sequence.</p>
<p>Lead with the problem and its measured cost, in the language of the function that owns it. "The close takes eleven days and consumes 6,000 hours" lands before "we would like to deploy a conversational analytics platform". The second sentence invites a debate about technology; the first invites agreement that something should be done.</p>
<p>Then present the single use case and its five-line model. One use case, fully costed, beats five partial ones, because it lets the committee make a decision rather than a judgement about your forecasting ability.</p>
<p>Next, present the risk register and the stop condition. Doing this proactively &mdash; before anyone asks &mdash; is what separates a proposal from a pitch. Committees fund teams that have already found the problems.</p>
<p>Close with the ask, stated precisely: the amount, the period, the decision you need on that day, and what you will deliver by the next review. Ambiguous asks get deferred, and a deferral in Q4 planning usually means the item drops out of the cycle entirely.</p>
<p>Two practical notes. Circulate the pack at least three working days ahead and offer a walkthrough to the CFO's analyst &mdash; most cases are won or lost in that conversation, not in the meeting. And bring the person who will run the programme, not only the person who wrote the case. Committees fund operators.</p>
"""),
])

DATA['ai-competitive-moat-2026'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("What Does a Durable AI Moat Look Like in Practice?", """
<p>The abstraction gets clearer with two concrete cases.</p>
<p><strong>Industrial maintenance.</strong> A manufacturer with fifteen years of sensor history, maintenance logs, and failure outcomes builds a model that predicts bearing failure six weeks out. The model itself is replicable &mdash; any competitor can train one. What is not replicable is the outcome data: fifteen years of what actually happened after each prediction, including the false positives that turned out to be something else. Each maintenance cycle adds ground truth, the model improves, and the downtime reduction compounds. A competitor entering the market in 2026 starts with zero outcome history, and no amount of model spending closes that gap quickly.</p>
<p><strong>Commercial lending.</strong> A lender that has underwritten a specific segment for a decade holds approved-and-declined records, repayment performance, and the macro conditions that applied. Combined with cash-flow data, this supports approvals the bureaus cannot. The moat is not the credit model; it is the combination of exclusive performance data, a workflow that underwriters actually use, and the regulatory track record that lets the lender deploy it. A challenger with a better algorithm and no performance history is still guessing.</p>
<p>Both cases share the same structure: exclusive data that accumulates through normal operations, a workflow that captures corrections and outcomes, and a system that gets measurably better every quarter. Notice what is absent from both &mdash; a proprietary model. In 2026, the model is the part everyone has.</p>
<p>The implication for planning is direct. If your AI roadmap is mostly model work &mdash; fine-tuning, prompt optimisation, vendor selection &mdash; you are investing in the layer that commoditises fastest. If it is mostly data plumbing, semantic consistency, outcome capture, and workflow embedding, you are investing in the layer that does not.</p>
"""),
])

# ---- new slugs -----------------------------------------------------------
DATA['ai-compliance-audit-automation'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("Which Controls Should You Automate First?", """
<p>The temptation is to automate the whole control library. The discipline is to automate the controls that are high-frequency, evidence-heavy, and rule-deterministic &mdash; and to leave judgement-based controls to humans for now.</p>
<p><strong>Start with model inventory completeness.</strong> Every other control depends on knowing what exists. Automate the discovery: scan for model registries, API calls to foundation-model providers, notebook environments, and deployment manifests, then reconcile against the official inventory. Unregistered models are the single largest source of audit findings, and discovery is entirely mechanical.</p>
<p><strong>Then automate evidence freshness.</strong> Auditors rarely fail you for having no policy; they fail you for having a policy with a twelve-month-old review date. Wire the checks: does every in-scope model have a current model card, a documented evaluation result, a named owner, and a risk classification that matches its use? These are queries against metadata, and they can run nightly.</p>
<p><strong>Then automate the technical controls.</strong> PII detection in training and prompt data, licence verification for datasets and model weights, retention-rule enforcement on prompts and outputs, and access-review attestation. Each produces a binary, timestamped result &mdash; exactly what an evidence pack needs.</p>
<p><strong>Leave these to humans in year one:</strong> risk-tier decisions on ambiguous use cases, proportionality arguments, and anything requiring a documented judgement about intent. Automating judgement badly generates findings rather than preventing them.</p>
<p>A useful sequencing rule: automate a control only when you can write the test, the evidence artefact, and the escalation path on a single page. If you cannot describe the artefact, you are not ready to automate it.</p>
"""),
    ("How Do Automated Audits Change the Compliance Team's Job?", """
<p>The concern that automation removes the compliance function is backwards. Automation removes the parts of the job that were never a good use of a trained compliance professional &mdash; and exposes how much of the role was evidence assembly.</p>
<p>In a manual cycle, a team might spend six to eight weeks per audit gathering artefacts from a dozen systems, chasing owners, and reconciling versions. That work is not judgement; it is logistics. Automated evidence collection collapses it to days, and the compliance team's time shifts to the decisions that actually require expertise: whether a use case is high-risk, whether a mitigation is proportionate, whether a vendor's assurance is sufficient.</p>
<p>Three new responsibilities appear. First, <strong>control design</strong>: someone has to decide what each automated test asserts, and a badly specified test produces false assurance, which is worse than no assurance. Second, <strong>exception triage</strong>: continuous testing generates a stream of exceptions, and someone must own the queue, distinguish genuine findings from noise, and tune thresholds. Third, <strong>regulatory translation</strong>: when a new obligation lands, someone maps it to controls and updates the tests. That is legal analysis, not tooling.</p>
<p>Practically, most compliance teams need one person with enough technical fluency to specify tests and read a data lineage graph. That is usually a retraining problem, not a hiring one &mdash; and it is the highest-return investment in the programme.</p>
<p>The measurable outcome is a shift in the ratio of time spent. Teams running continuous audit typically move from roughly 70% collection and 30% judgement to the inverse. That is the change worth funding.</p>
"""),
])

DATA['ai-compliance-checklist-year-end-nov2025'] = dict(before='__FAQ__', inserts=[
    ("Who Should Own Each Item on the Year-End Checklist?", """
<p>A checklist without named owners becomes a document that everyone agrees with and nobody completes. Assign the year-end review across four roles before it starts.</p>
<p><strong>The compliance or legal lead</strong> owns the regulatory layer: which obligations changed this year, which apply to which deployments, and what the resulting policy updates are. This is the only item that genuinely requires legal judgement, and it should be done first, because it sets the standard everything else is measured against.</p>
<p><strong>The data or platform owner</strong> owns the inventory: every model in production, its data sources, its jurisdiction, its classification, and its documentation status. In most organisations this is the least complete artefact and the one that takes longest, so start it early.</p>
<p><strong>The business owner of each use case</strong> owns the operational evidence: that the system performs as documented, that humans review the outputs that require review, that incidents have been logged, and that the training data is still what the documentation says it is. Compliance cannot attest to this on the business's behalf, and auditors will ask the business owner directly.</p>
<p><strong>The security or IT function</strong> owns access, retention, and vendor assurance: who can reach the systems and their data, how long prompts and outputs are kept, and whether third-party model providers meet the commitments you rely on.</p>
<p>One role is missing from most year-end reviews and should not be: <strong>the person who will be accountable next year</strong>. If the review is run by someone who moves on in January, the findings lose their institutional memory. Name the owner of the resulting risk register as part of the exercise.</p>
"""),
    ("What Evidence Should You Keep, and for How Long?", """
<p>Evidence is only useful if it is findable and versioned. Three principles keep an evidence store defensible without turning it into an archive project.</p>
<p><strong>Keep the artefact, not the screenshot.</strong> A PDF export of a dashboard proves that a dashboard existed; it does not prove what the underlying data said at the time. Prefer structured exports &mdash; the evaluation result file, the model card in version control, the access review export &mdash; because they carry metadata and can be re-queried.</p>
<p><strong>Version everything.</strong> When a model card or policy is updated, the previous version must remain retrievable with its effective dates. Auditors routinely ask what the documented position was at a specific date, not what it is today. Version control or an immutable store handles this; a shared drive with filenames ending in "final_v3" does not.</p>
<p><strong>Match retention to obligation, then stop.</strong> Align retention periods to the relevant regulatory requirement and to your own litigation and audit horizon. Keeping prompts and outputs forever is a liability as much as a control; keeping them for thirty days when a regulator may ask about a decision made eight months ago is a gap. Write the period down, apply it automatically, and record that you applied it.</p>
<p>Finally, keep a single index. An evidence store without an index is a store that fails under time pressure, and audits are always under time pressure. The index should map each obligation to the control, the artefact, its location, and its owner &mdash; which is the same structure the auditor will use to ask for it.</p>
"""),
    ("How Do You Turn Year-End Findings Into Next Year's Plan?", """
<p>The value of the year-end review is not the report; it is whether the findings change what gets funded in January. Three moves make that happen.</p>
<p><strong>Convert findings into a ranked risk register.</strong> Each finding gets a likelihood, an impact, an owner, and a remediation estimate. Ranked registers get funded; lists of observations get filed. Where several findings share a root cause &mdash; incomplete inventory, missing documentation, no evaluation threshold &mdash; group them, because remediation is cheaper at the cause than at the symptom.</p>
<p><strong>Separate remediation into three horizons.</strong> Immediate items are the ones that change an existing compliance position: an unclassified high-risk system, a missing human-review step, a retention rule that is not enforced. These go into the current quarter. Structural items &mdash; no central inventory, no evaluation harness, no evidence automation &mdash; go into the annual plan with a business case. Monitoring items are accepted risks with a named owner and a review date.</p>
<p><strong>Budget for the structural items properly.</strong> The reason the same findings reappear each year is that remediation was scoped as a documentation exercise rather than a capability build. Automating evidence collection, standing up an evaluation harness, or consolidating the model inventory are engineering projects with real cost. Funding them once is cheaper than funding the manual version every year.</p>
<p>Set a mid-year checkpoint. A year-end review that is only revisited at the next year-end is a ritual; one reviewed at the half produces a materially different conversation twelve months later.</p>
"""),
])

DATA['ai-compliance-quarterly-checklist-q4-2025'] = dict(before='__FAQ__', inserts=[
    ("How Do You Classify AI Systems Without Over-Engineering It?", """
<p>Classification is where quarterly reviews stall, because teams try to build a perfect taxonomy before they classify anything. A three-tier scheme, applied consistently, is enough to run a defensible Q4 review.</p>
<p><strong>Tier 1 &mdash; prohibited or unacceptable.</strong> Anything falling into a prohibited category under the EU AI Act or equivalent local restriction: social scoring, certain biometric categorisation, manipulation-based systems. These are not risk-managed; they are stopped. If you find one, the finding is immediate and the remediation is removal.</p>
<p><strong>Tier 2 &mdash; high-risk or regulated-decision.</strong> Systems used in employment, credit, insurance pricing, essential services, or safety-relevant operations, plus anything the EU AI Act classifies as high-risk. These carry documentation, human-oversight, logging, and evaluation obligations. This tier should be small; if it contains most of your inventory, your thresholds are too conservative and the review will not be actionable.</p>
<p><strong>Tier 3 &mdash; limited or minimal risk.</strong> Internal productivity, summarisation, search, code assistance, and most analytical use cases. Obligations are transparency-focused where they exist at all.</p>
<p>Two rules keep it proportionate. Classify by <strong>use</strong>, not by <strong>model</strong> &mdash; the same foundation model can be Tier 2 in an underwriting workflow and Tier 3 in an internal search tool. And record the reasoning in one sentence per system, because that sentence is what an auditor will read first.</p>
<p>Re-classify on material change: new data source, new decision scope, new jurisdiction, or a change from advisory to automated output. Classification is a state, not a one-time event, and drift between reviews is the most common source of findings.</p>
"""),
    ("What Should the Q4 Review Produce as Evidence?", """
<p>A quarterly review is only useful if it leaves behind artefacts that a regulator, an internal auditor, or a board committee could rely on without a reconstruction exercise. Four artefacts, produced every quarter.</p>
<p><strong>1. A current inventory export</strong> listing every AI system, its business owner, its classification, its data sources, its jurisdictions, and its deployment status. It should be generated from the system of record, not assembled by hand, and it should carry the date of generation.</p>
<p><strong>2. A control test result set</strong> showing which automated checks ran, what passed, what failed, and when. Passing tests are as important as failures: an auditor asking whether documentation is current wants to see the test that confirms it, run recently.</p>
<p><strong>3. An exceptions log</strong> with each exception, its owner, its remediation status, and its age. Unexplained aged exceptions are the clearest signal of a programme that performs the review but does not act on it.</p>
<p><strong>4. A signed summary</strong> &mdash; one page, from the accountable owner, stating the review was completed, what changed since last quarter, and what remains open. This is the artefact that converts a set of test results into an attestation, and it is the one most often missing.</p>
<p>Store all four in the same location with a consistent naming convention and a retention period that matches your obligations. A review whose outputs are scattered across inboxes and slide decks has not produced evidence, even if the work was done.</p>
"""),
    ("How Should Q4 Findings Feed Into Q1 Planning?", """
<p>Quarterly compliance reviews lose their value when they are treated as a reporting obligation rather than an input to the next planning cycle. The handoff from Q4 to Q1 is where the return is captured.</p>
<p><strong>Carry the open items forward explicitly.</strong> Every finding that remains open at year-end should appear in Q1 with an owner, a date, and a status &mdash; not as an appendix to a report, but as a line in someone's plan. Findings that have to be rediscovered in March are findings that will recur in Q4.</p>
<p><strong>Convert recurring findings into projects.</strong> If the same item &mdash; incomplete model cards, missing evaluation results, stale access reviews &mdash; appears in three consecutive quarters, it is not a compliance failure; it is a missing capability. Fund it as a project with a scope and a budget, and the finding disappears permanently instead of being remediated repeatedly.</p>
<p><strong>Set the Q1 regulatory watch.</strong> Q4 is the natural point to list the obligations landing in the coming year, assign someone to track each, and decide which require work before they take effect. Most compliance surprises are known in advance; they are simply unowned.</p>
<p><strong>Report the trend, not just the status.</strong> A single quarter's results tell a committee very little. Three quarters of trend &mdash; exception count falling, time-to-evidence falling, coverage rising &mdash; tells them whether the programme is working, and is far more likely to secure next year's budget.</p>
"""),
])

DATA['ai-consulting-delivery-models'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("How Should Outcome-Based Pricing Actually Be Structured?", """
<p>Outcome-based pricing is widely requested and often badly constructed, which is why so many pilots of it quietly revert to time and materials. Three design decisions determine whether it works.</p>
<p><strong>Choose a metric the vendor can influence and the buyer can verify.</strong> "Revenue uplift" fails both tests: it is influenced by market conditions and verified only after a long lag. "Cost per processed claim", "percentage of tickets deflected at constant satisfaction", or "time from request to insight" work because both parties can measure them from systems they already have. If the two parties will argue about the number, the model will fail regardless of the outcome.</p>
<p><strong>Split the fee into three components.</strong> A fixed platform component covering the run state, which is not contingent. A delivery component tied to milestones the vendor controls &mdash; go-live, integration complete, adoption threshold met. And a contingent component tied to the shared outcome. Roughly half the fee contingent is the point at which behaviour genuinely changes; below about a third, it does not.</p>
<p><strong>Define the measurement window and the baseline up front.</strong> Both must be agreed before work starts, ideally during a paid diagnostic. Renegotiating the baseline after go-live is the most common failure mode, and it usually happens because the baseline was never measured &mdash; only estimated.</p>
<p>Two clauses protect both sides. A <strong>data-access clause</strong>: the vendor gets the operational data needed to deliver the outcome, without which contingency is unfair. And a <strong>change-control clause</strong>: if the buyer changes the process or the data, the baseline is re-set by agreement rather than by argument.</p>
"""),
    ("What Does a Good Managed AI Service Contract Include?", """
<p>Managed services transfer operational responsibility, and the contract has to make that transfer real rather than rhetorical. Beyond the commercial terms, five clauses determine whether the arrangement works.</p>
<p><strong>Service levels tied to business outcomes, not uptime.</strong> Uptime is table stakes. What matters is answer accuracy against an agreed threshold, response latency, and time-to-resolution when accuracy degrades. Define the measurement method, the sample, and who adjudicates disputes.</p>
<p><strong>A named run team with continuity commitments.</strong> Managed services fail when the delivery team rotates off and knowledge goes with it. Name the roles, set a minimum tenure or a documented handover process, and require that run documentation be maintained as a deliverable rather than a courtesy.</p>
<p><strong>An exit and portability clause.</strong> The buyer should be able to leave with the configuration, the semantic definitions, the prompts, the evaluation set, and the operational data. Without this, the managed service becomes lock-in by another name &mdash; and it is the clause most often negotiated away in exchange for a discount.</p>
<p><strong>A change and improvement mechanism.</strong> Models, vendors, and prices move quickly. The contract needs a defined cadence for evaluating model swaps, incorporating new capabilities, and passing through cost reductions, rather than a change-order process that prices every improvement as new work.</p>
<p><strong>A capability-transfer obligation.</strong> The best managed services make themselves partially unnecessary. Require documented knowledge transfer and a defined internal capability build, with the buyer's team taking on more of the run over time. It protects the buyer and, counter-intuitively, improves retention &mdash; because the service keeps demonstrating value rather than dependency.</p>
"""),
])

if __name__ == '__main__':
    for slug, d in DATA.items():
        changed = apply_ops(slug, 'en', inserts=d['inserts'], before=d['before'])
        print(('inserted ' if changed else 'noop     ') + slug)
