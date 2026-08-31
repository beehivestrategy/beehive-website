#!/usr/bin/env python3
"""EN body expansion, batch 3 (6 slugs)."""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb002_lib import apply_ops

DATA = {}

DATA['ai-compliance-audit-automation'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("How Do You Keep Automated Evidence Audit-Ready?", """
<p>Collecting evidence continuously is only half the problem; the other half is being able to reproduce it on demand, months later, for someone who was not there when it was generated.</p>
<p><strong>Timestamp and hash every artefact.</strong> An evidence item without an immutable timestamp is an assertion, not evidence. Write artefacts to storage that records creation time and prevents silent modification, and keep the hash in the index.</p>
<p><strong>Record the test, not just the result.</strong> A passed control test should store the query or rule that produced it, the dataset it ran against, and the version of both. When an auditor asks why a control passed in March, "the system said so" is not an answer; the stored rule and its inputs are.</p>
<p><strong>Separate the running log from the point-in-time pack.</strong> Continuous monitoring produces a stream; an audit needs a snapshot. Generate a dated evidence pack at each review cycle and freeze it. Auditors work with the pack; the stream is for your own operations.</p>
<p><strong>Test the retrieval path before you need it.</strong> Run a mock request twice a year: pick a control at random and produce its evidence within a business day. Teams that do this discover broken lineage, deleted artefacts, and orphaned owners while there is still time to fix them.</p>
"""),
])

DATA['ai-compliance-checklist-year-end-nov2025'] = dict(before='__FAQ__', inserts=[
    ("What Changes in 2026 Should the Year-End Review Anticipate?", """
<p>A year-end review that only looks backwards produces a plan that is obsolete by March. Four developments should shape what the review prioritises.</p>
<p><strong>The EU AI Act's transparency obligations for generated content begin to apply in August 2026.</strong> Any system producing synthetic text, image, audio, or video for external audiences needs a labelling mechanism in the generation path &mdash; not a manual step at export. Retrofitting this is materially harder than designing it in, so the review should flag affected systems now.</p>
<p><strong>High-risk obligations continue their phased application through 2026 and 2027.</strong> Systems in employment, credit, and essential services will face documentation, logging, and human-oversight requirements. If the review identifies candidates for this tier, the gap analysis belongs in this year's findings rather than next year's.</p>
<p><strong>Enforcement practice is becoming more specific.</strong> Regulators are moving from guidance to questions, and the questions increasingly concern evidence: what did you know, when, and can you show the data behind the decision. This is the argument for automated evidence collection over documentation created at review time.</p>
<p><strong>Model and vendor churn will continue.</strong> Foundation-model providers change terms, deprecate versions, and alter data-handling commitments. The review should record which external models each system depends on and require notification of material changes as a contractual condition &mdash; otherwise next year's inventory starts from scratch again.</p>
"""),
])

DATA['ai-compliance-quarterly-checklist-q4-2025'] = dict(before='__FAQ__', inserts=[
    ("How Do You Run the Q4 Review in Two Weeks Without Cutting Corners?", """
<p>A two-week sprint is realistic, but only if the scope is deliberately bounded. The mistake is trying to complete a full gap analysis in ten working days; the objective is a defensible position and a ranked list of what to fix next.</p>
<p><strong>Days 1&ndash;3: inventory and classify.</strong> Generate the inventory from discovery tooling rather than a survey, reconcile it with business owners, and apply the three-tier classification. Expect the first pass to surface systems nobody knew were running; log them as findings rather than spending days on them.</p>
<p><strong>Days 4&ndash;6: run the automated controls.</strong> Execute every test you already have &mdash; documentation currency, access review, retention rules, PII exposure, licence checks. Do not build new tests during the sprint; note the gaps for next quarter.</p>
<p><strong>Days 7&ndash;9: targeted manual review of Tier 2 systems only.</strong> High-risk systems get human attention: is the human-oversight step real and documented, are evaluation results current, are incidents being logged. Tier 3 systems get sampled, not reviewed exhaustively.</p>
<p><strong>Day 10: consolidate and sign.</strong> Produce the four artefacts, rank the findings, assign owners, and get the accountable owner's signature.</p>
<p>Three things must be out of scope: new policy drafting, platform procurement, and remediation of structural gaps. All three belong in the plan the review produces. Trying to do them inside the sprint is what turns a two-week review into a quarter-long one that finishes after the window it was meant to cover.</p>
"""),
    ("What Does Good Look Like for Human Oversight in Practice?", """
<p>Human oversight is the control most often claimed and least often implemented. Regulators and auditors increasingly test it directly, and the question they ask is narrow: can the named human actually override the system, and can you show that they did?</p>
<p><strong>Oversight must have authority, not just visibility.</strong> A reviewer who sees the output but cannot change the outcome is monitoring, not oversight. Implement a genuine override path &mdash; reject, modify, escalate &mdash; and log every exercise of it.</p>
<p><strong>Oversight must be resourced.</strong> If one analyst reviews 400 automated decisions an hour, the review is decorative. Set a realistic ratio based on decision complexity, and size the team to it. Where volume makes individual review impractical, sample intelligently: route low-confidence, high-impact, and outlier cases to humans and let high-confidence routine cases through with audit logging.</p>
<p><strong>Oversight must be documented at the time.</strong> Record who reviewed what, when, what they decided, and why. A training slide saying that staff review outputs is not evidence; a log of reviews with decisions and overrides is.</p>
<p><strong>Oversight must be tested.</strong> Periodically inject cases that should be caught and measure detection. Teams that run this exercise routinely find that override paths are broken, that reviewers default to accepting recommendations under time pressure, and that the interface nudges acceptance &mdash; all of which are fixable, and none of which are visible from a policy document.</p>
"""),
])

DATA['ai-consulting-delivery-models'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("How Do You Write a Statement of Work for an AI Engagement?", """
<p>Most AI engagements that disappoint were specified in a document that made disappointment inevitable. Three clauses change the outcome more than any other part of the SOW.</p>
<p><strong>Define the first deliverable as something that runs.</strong> "Discovery report" invites a document; "a working answer to these five questions, over this data, with measured accuracy" invites a system. Specify the acceptance test for the first increment &mdash; the questions, the data, the accuracy threshold &mdash; and the engagement's trajectory changes immediately.</p>
<p><strong>Name the data dependencies and who supplies them.</strong> The most common cause of schedule slip is not modelling; it is waiting for access. List every data source, its owner, the access mechanism, and the date it is needed. Require the client to confirm access within a defined window, and make the dependency explicit in the schedule.</p>
<p><strong>Specify the handover state.</strong> Engagements end, and the question at the end is whether something continues to run. Define the artefacts &mdash; code, configuration, semantic definitions, evaluation set, runbook &mdash; and the capability state of the client team. If the client is meant to operate it, the SOW should include the enablement hours and the shadowing period that makes that realistic.</p>
<p>Add one more: a <strong>stop condition</strong> at the first gate. If the feasibility threshold is not met after the first increment, the engagement either re-scopes or ends. This is uncomfortable to negotiate and is the single best predictor of an engagement that delivers rather than one that extends.</p>
"""),
])

DATA['ai-consulting-delivery-models-20260126'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("What Should the First 90 Days Actually Deliver?", """
<p>The 90-day loop has become the standard unit of AI delivery, and its value depends entirely on what happens inside it. A well-run first loop produces three things: a decision, a working increment, and a measured baseline.</p>
<p><strong>Days 1&ndash;30: frame and prove feasibility.</strong> The output is not a strategy deck. It is a narrow, testable statement: for this specific set of questions, over this specific data, we can produce answers at this accuracy. Getting to that requires data access, a semantic layer over the relevant sources, and an evaluation set built from real questions with known-good answers. If the evaluation set cannot be built, that is the finding &mdash; and it is better to know at day 30 than at month nine.</p>
<p><strong>Days 31&ndash;60: build the thinnest working increment.</strong> Put it in front of the actual users, in the actual workflow, with instrumentation on every interaction. The temptation at this stage is to broaden scope; resist it. The increment's job is to generate real usage data and real objections from the people whose work it changes.</p>
<p><strong>Days 61&ndash;90: measure and decide.</strong> Compare against the baseline defined at the start, in the unit the business cares about. Then make an explicit decision: scale, re-scope, or stop. Write the decision down with the numbers behind it.</p>
<p>Two practices separate loops that compound from loops that repeat. First, <strong>carry the evaluation set forward</strong> &mdash; it becomes the regression suite for every subsequent increment, and it is the asset that makes the second loop faster than the first. Second, <strong>hold the loop boundary</strong>: if a loop cannot produce a decision in 90 days, it was scoped too broadly, and extending it is usually worse than splitting it.</p>
"""),
    ("How Do You Avoid the Pilot Trap in AI Delivery?", """
<p>The pilot trap is not a technology failure; it is a structural one. Pilots are funded as experiments, and experiments are not required to have an operating model, an owner, or a budget line. So they succeed technically and die organisationally.</p>
<p>Three conditions distinguish a pilot designed to scale from one designed to demo.</p>
<p><strong>The pilot runs on production infrastructure.</strong> If it runs on a laptop, a separate cloud account, or a hand-curated dataset, the first thing that happens after approval is a rebuild &mdash; and the rebuild is where most momentum dies. Running on production infrastructure from day one is slower for the first six weeks and dramatically faster over the year.</p>
<p><strong>The pilot has a named production owner.</strong> Not a sponsor &mdash; an owner who will run it after the project team leaves, and who is allocated time during the pilot to do so. Without this, the handover conversation happens after success, when nobody has budgeted for it.</p>
<p><strong>The pilot has a scale case that was written before it started.</strong> What does it cost to run at ten times the volume, who pays, and what has to be true for that to be approved? Writing this down at the outset converts a successful pilot into a funded programme rather than an internal case study.</p>
<p>The corollary: fund fewer pilots. An organisation running twenty pilots has usually made a decision not to commit to any of them. Three pilots, each with production infrastructure, a named owner, and a pre-written scale case, produce more deployed capability than twenty that have none of these.</p>
"""),
])

DATA['ai-content-labeling-regulations'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("How Should Disclosure Be Built Into the Generation Pipeline?", """
<p>Bolting labels on at export is the most common design mistake, and it fails in a predictable way: the moment content leaves through a channel that does not pass through the export step, the label disappears.</p>
<p><strong>Label at generation, persist in metadata, render at distribution.</strong> Three layers, each with a different failure mode. Generation-time marking &mdash; a visible mark or an embedded watermark applied by the model pipeline &mdash; survives downstream handling best. Metadata (C2PA-style content credentials, or equivalent provenance records) survives platforms that respect it and is stripped by those that do not. Rendering at distribution &mdash; a visible disclosure applied by the publishing layer &mdash; is the most reliable for end-user transparency because you control it, and it is the layer regulators can actually see.</p>
<p><strong>Make the pipeline default-on.</strong> If labelling is a step a user has to remember, it will be skipped under deadline. The generation service should mark output by default, and require an explicit, logged action to suppress marking &mdash; with suppression permitted only for internal or clearly non-public use.</p>
<p><strong>Track the provenance record, not just the mark.</strong> A record of which model, which version, which prompt template, and which input sources produced an asset is what you will need when a regulator, a platform, or a customer asks. Visible marks answer the user's question; provenance records answer everyone else's.</p>
<p><strong>Test the whole path quarterly.</strong> Publish a test asset through every distribution channel you use &mdash; web, app, email, social, partner feeds &mdash; and check what survives. Channels change their handling of metadata without notice, and this test is the only way to find out before it matters.</p>
"""),
    ("What Should Enterprises Do About Third-Party and User-Generated Synthetic Content?", """
<p>Obligations rarely stop at content you generate. Most regimes also reach content you publish, distribute, or host, which pulls third-party and user-generated synthetic media into scope.</p>
<p><strong>For third-party content you publish:</strong> require provenance disclosure in supplier and agency contracts. Ask for the provenance record, not just an assurance that content is human-authored. Where a supplier cannot provide it, treat the content as AI-generated and label accordingly &mdash; the risk of under-labelling sits with the publisher in most regimes, not the creator.</p>
<p><strong>For user-generated content:</strong> the practical standard is a notice-and-action mechanism rather than universal pre-screening. Provide a reporting route for undisclosed synthetic content, act on reports within a defined window, and log the actions. Platforms that document a functioning process are in a materially better position than those that claim they cannot detect everything.</p>
<p><strong>For detection:</strong> use it as triage, not as proof. Detection of synthetic media is imperfect and degrades as generation improves. Use detector scores to prioritise human review, never as the sole basis for removal or for an assurance that content is authentic.</p>
<p><strong>For your own brand:</strong> publish a clear position on how you use generative AI and how you mark it. In practice this does more for trust than any single technical control, and it gives customer-facing teams a consistent answer &mdash; which is usually the first thing that breaks during an incident.</p>
"""),
])

if __name__ == '__main__':
    for slug, d in DATA.items():
        changed = apply_ops(slug, 'en', inserts=d['inserts'], before=d['before'])
        print(('inserted ' if changed else 'noop     ') + slug)
