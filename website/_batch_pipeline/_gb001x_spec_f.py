# -*- coding: utf-8 -*-
"""Final top-up: push remaining EN files past 3,000 words."""

SPECS = {}

SPECS["predictions-enterprise-data-analytics-2026"] = {
    "EN": {"new": [
        ("what-should-you-stop-doing-in-2026",
         "What Should You Stop Doing in 2026?",
         ["<p>Planning conversations are almost entirely about what to start, and the returns from "
          "stopping are frequently larger. Three practices are worth retiring deliberately, because "
          "each consumes capacity that the 2026 agenda needs elsewhere.</p>",
          "<p>Stop building dashboards to answer a single question. The economics have changed: the "
          "marginal cost of a conversational answer is now far below the marginal cost of a new "
          "dashboard including its maintenance. Keep the monitoring dashboards, and route "
          "one-off requests to questions rather than to builds. Teams that make this shift "
          "consistently recover a meaningful share of analyst capacity within two quarters.</p>",
          "<p>Stop running model evaluations as a manual exercise. A spreadsheet of test questions "
          "checked before each release works until the release cadence increases, and then it becomes "
          "the bottleneck and gets skipped. Encoding the evaluation set and running it in CI is a "
          "week of work that removes a permanent constraint, and it is the single highest-return "
          "engineering investment most AI teams have not made.</p>",
          "<p>Stop treating the semantic layer as a reporting concern. It is the control surface that "
          "determines whether an AI system gives correct answers, and teams that staff it as a "
          "side-effect of BI work consistently find that their AI deployments underperform for "
          "reasons that have nothing to do with the model.</p>",
          "<p>None of these are cost savings in the sense a CFO will recognise immediately. They are "
          "capacity releases: the same team, doing work that compounds, instead of work that "
          "depreciates.</p>"]),
    ]},
}

SPECS["conversational-bi-dashboards-why-executives-switching"] = {
    "EN": {"new": [
        ("how-do-you-handle-a-question-the-system-cannot-answer",
         "How Do You Handle a Question the System Cannot Answer?",
         ["<p>Refusal behaviour is one of the most under-designed aspects of conversational analytics "
          "and one of the most consequential for trust. A system that always attempts an answer will "
          "eventually answer confidently and wrongly; a system that refuses too often is abandoned as "
          "unhelpful. The design goal is a specific, useful refusal.</p>",
          "<p>A useful refusal does three things. It says what it could not do and why, in terms the "
          "user can act on: not &quot;I could not process that request&quot; but &quot;I do not have a "
          "certified definition for customer lifetime value yet&quot;. It offers the nearest thing it "
          "can do: &quot;I can show you revenue by cohort for the last eight quarters&quot;. And it "
          "captures the request, so that the gap appears in the semantic layer backlog rather than "
          "vanishing.</p>",
          "<p>Three distinct situations need distinct responses, and conflating them is the usual "
          "design error. A question the system cannot map to a known metric is a coverage gap and "
          "should be logged as such. A question that is genuinely ambiguous — "
          "&quot;how are we doing&quot; — should trigger clarification rather than a guess, and the "
          "clarification options should be drawn from the metric catalogue. A question the user is not "
          "authorised to answer is a permissions outcome and should be stated plainly, without "
          "revealing whether the data exists.</p>",
          "<p>Measure the refusal rate and review it. A high rate in a specific domain almost always "
          "means the semantic layer is thin there, and the refusal log is the most accurate demand "
          "signal you will get. Teams that review it weekly close coverage gaps in the order users "
          "actually care about, which is why their refusal rates fall steadily while their usage "
          "rises.</p>"]),
    ]},
}

SPECS["ai-vendor-contract-negotiation-tips-nov2025"] = {
    "EN": {"new": [
        ("how-do-you-manage-a-vendor-after-signature",
         "How Do You Manage a Vendor After Signature?",
         ["<p>Value leakage after signature is larger than value lost during negotiation in most AI "
          "procurements, and it is almost entirely unmanaged. The contract sets the terms; whether "
          "you realise them depends on practices that have to be in place from the first month.</p>",
          "<p>Assign a vendor owner with a defined scope, not a shared inbox. That person owns the "
          "renewal calendar, the consumption forecast against committed spend, the sub-processor "
          "change notices, and the incident contacts. Without a named owner, renewal notices arrive "
          "with weeks rather than months of warning, and auto-renewal clauses fire.</p>",
          "<p>Track consumption against commitment monthly. Both failure modes are expensive: "
          "exceeding commitment triggers overage at punitive rates, and falling short means paying for "
          "capacity nobody used. A simple monthly review with a three-month forecast catches both in "
          "time to act, and it gives you a factual basis for the renewal conversation rather than an "
          "anecdotal one.</p>",
          "<p>Exercise the contractual rights you negotiated, because rights that are never exercised "
          "become difficult to enforce. Request the sub-processor list when it changes. Ask for the "
          "deletion confirmation on the schedule the contract specifies. Require notice before a "
          "material model change and re-run your evaluation set when one arrives. Each of these takes "
          "an hour and each one is the difference between a paper control and a real one.</p>",
          "<p>Finally, keep the benchmark current. Re-run a small version of the original evaluation "
          "each year so that renewal is a comparison rather than a renegotiation from memory, and so "
          "that a competing proposal can be assessed against evidence you already hold.</p>"]),
    ]},
}

SPECS["enterprise-architecture-ai-era"] = {
    "EN": {"new": [
        ("how-do-you-migrate-without-a-big-bang",
         "How Do You Migrate Without a Big Bang?",
         ["<p>Architecture programmes fail more often from sequencing than from design, and the "
          "failure has a standard shape: a multi-year rebuild approved on a future-state diagram, "
          "which delivers nothing for eighteen months and is cancelled in month fifteen. The "
          "alternative is not incrementalism for its own sake but a specific pattern that delivers "
          "continuously.</p>",
          "<p>The pattern is to route new work through the new architecture while leaving existing "
          "systems in place. Put the semantic layer and the governed access boundary in front of "
          "everything new, and let legacy consumers keep reading from the old path until they have a "
          "reason to move. This produces value from the first quarter, because the first new use case "
          "is delivered on the new stack, and it avoids the migration project that has no deliverable "
          "until it is finished.</p>",
          "<p>Prioritise what to move by two questions: how much does this consumer cost to maintain "
          "where it is, and how much risk does it carry. High-cost, high-risk consumers move first, "
          "and they fund the programme with their own savings. Low-cost, low-risk consumers may never "
          "need to move, which is a legitimate outcome rather than an incomplete migration.</p>",
          "<p>Keep one invariant through the transition: one definition of every business term. Where "
          "a legacy system and the semantic layer disagree, the semantic layer wins for anything new, "
          "and the discrepancy gets logged and resolved. Allowing two sources of truth during a "
          "migration is what turns a three-year programme into a five-year one.</p>",
          "<p>Finally, publish a deprecation date for each legacy path once its replacement is live. "
          "Without a date, both paths persist indefinitely, and the programme ends up maintaining the "
          "old architecture and the new one.</p>"]),
    ]},
}

SPECS["ai-roi-real-world-enterprise-case-studies-apr"] = {
    "EN": {"new": [
        ("what-should-you-do-when-a-pilot-stalls",
         "What Should You Do When a Pilot Stalls?",
         ["<p>Stalled pilots are the normal outcome rather than the exception, and how an organisation "
          "handles them determines whether the programme recovers. The instinct is to extend the "
          "pilot, which is almost always the wrong response, because the causes of stalling are "
          "specific and diagnosable.</p>",
          "<p>Three causes account for most stalls, and they have different remedies. Coverage: the "
          "system cannot answer enough of the questions users ask, so they stop asking. The remedy is "
          "semantic layer work, not more promotion, and the refusal log tells you exactly what to "
          "build. Trust: the system answered wrongly once and users retreated. The remedy is "
          "evaluation infrastructure plus visible correction handling, and it requires acknowledging "
          "the specific failure publicly rather than waiting for confidence to return on its own.</p>",
          "<p>The third cause is workflow fit: the answers are correct but arrive somewhere users are "
          "not. The remedy is integration into the tool where the decision actually happens — the CRM, "
          "the planning system, the messaging platform — rather than another interface to check.</p>",
          "<p>Diagnose by instrumenting before extending. Two weeks of logging on questions asked, "
          "answers returned, refusals, and corrections will identify which of the three it is, and the "
          "answer is rarely the one assumed in the steering committee. Extending an undiagnosed pilot "
          "buys time and spends credibility.</p>",
          "<p>Set a decision point in advance: at the end of the diagnostic period, the pilot either "
          "has a named remediation with an owner and a date, or it is closed. Programmes that cannot "
          "close pilots accumulate a portfolio of zombie proofs of concept that consume attention and "
          "distort the portfolio view of what is working.</p>"]),
    ]},
}

SPECS["data-privacy-compliance-audits-ai-systems"] = {
    "EN": {"new": [
        ("how-do-you-scope-an-audit-across-many-models",
         "How Do You Scope an Audit Across Many Models?",
         ["<p>Organisations that get past their first AI audit almost immediately face a scaling "
          "problem: dozens or hundreds of models, one audit team, and no defensible way to decide what "
          "gets examined this year. Ad-hoc selection produces arbitrary coverage, and attempting "
          "everything produces nothing.</p>",
          "<p>Risk-tier first, on criteria that can be applied consistently by someone who did not "
          "build the model. The factors that carry the most weight are the consequence of an incorrect "
          "output, the degree of automation — whether a human is meaningfully in the loop or merely "
          "nominally — the sensitivity of the data involved, the population affected, and whether "
          "the use case falls under an existing regulatory regime. Four tiers is usually enough, and "
          "the top tier should be small enough to audit exhaustively.</p>",
          "<p>Then apply different depths per tier. Top tier: full audit, annually or on material "
          "change, with external review. Second tier: full internal audit on a two-year rotation, with "
          "automated checks running continuously. Third tier: automated checks plus a sampled "
          "documentation review. Fourth tier: automated checks only. This is what makes the programme "
          "proportionate rather than uniform.</p>",
          "<p>Automate the parts that are mechanical, because that is what makes the depth affordable. "
          "Provenance checks, retention verification, access-log review, and drift measurement can all "
          "run as jobs against the catalogue and the pipeline metadata. That frees the audit team for "
          "the parts that require judgement: reading a use case, interviewing a system owner, and "
          "assessing whether the stated purpose matches what the system actually does.</p>",
          "<p>Publish the tiering and the schedule. Teams that know their model will be audited in Q3 "
          "prepare, and preparation is where most of the remediation actually happens.</p>"]),
    ]},
}

SPECS["financial-services-ai-compliance-innovation"] = {
    "EN": {"new": [
        ("how-do-you-prove-a-model-is-under-control-to-a-supervisor",
         "How Do You Prove a Model Is Under Control to a Supervisor?",
         ["<p>Supervisory conversations about AI have converged on a small set of questions, and "
          "institutions that prepare for those specific questions spend far less time in examination "
          "than those that prepare a general narrative. The questions are predictable enough to build "
          "against.</p>",
          "<p>First: what AI are you running, and who owns it. This requires a complete inventory with "
          "a named business owner per system, and it is the question on which most institutions are "
          "weakest, because use cases enter through business teams and vendor features rather than "
          "through a central process. An inventory with gaps is a finding in itself.</p>",
          "<p>Second: how did you decide this use case was appropriate. The expected answer is a "
          "documented intake and risk-tiering decision, with the artefacts the model risk framework "
          "requires — intended use, data basis, human oversight design, validation results. "
          "Supervisors are generally less concerned with the conclusion than with the consistency of "
          "the process that produced it.</p>",
          "<p>Third: what happens when it is wrong. This means the monitoring plan, the thresholds, "
          "the escalation path, and evidence that the alerts are acted on. An institution that can "
          "show a drift alert from March, the investigation, and the resulting change is making a "
          "much stronger case than one showing a clean dashboard, because a clean dashboard suggests "
          "nobody is looking.</p>",
          "<p>Fourth: can you reconstruct a decision. Produce the trace for a sampled case — inputs, "
          "retrieved context, tools invoked, policy applied, output, human review. Being able to do "
          "this on request, within a day, is the single most persuasive demonstration of control "
          "available, and it is an architecture property rather than a documentation exercise.</p>"]),
    ]},
}
