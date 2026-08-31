#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

TOP = {
"what-is-mlops-machine-learning-operations": ("""
<h2 id="how-does-mlops-connect-to-conversational-analytics">How Does MLOps Connect to Conversational Analytics?</h2>
<p>Teams running MLOps and teams deploying conversational analytics often sit in different parts of the organisation, and the separation costs both of them. The connection is closer than it looks: a conversational analytics platform contains models — natural-language understanding, query generation, answer composition, and the semantic layer mappings behind them — and all of them need the same lifecycle discipline.</p>
<p>The practical overlap is in three places. Versioning applies to the semantic layer as much as to the model: when a metric definition changes, the change needs a version, an owner, and a record of which answers used the previous definition. Evaluation needs golden question sets rather than test datasets — a curated list of real business questions with known-correct answers, run on every semantic or model change, which is the only reliable way to catch silent quality drift in answers. And monitoring needs to track answer correctness over time, not just latency, which means sampling real questions and reviewing whether the answer was right.</p>
<p>The organisational lesson is that the same operating model serves both. Named owners, promotion gates, rollback paths, and drift monitoring are discipline-independent; only the artefacts change. Organisations that run these as one capability rather than two programmes avoid building duplicate review processes and, more importantly, avoid the gap where analytics answers change without anyone being accountable for the change.</p>
""", '<h2 id="beehive-strategy-and-mlops">'),

"federated-learning-data-governance-challenges": ("""
<h2 id="what-should-a-federated-pilot-measure">What Should a Federated Pilot Measure?</h2>
<p>Federated pilots are typically justified on privacy grounds and evaluated on model accuracy, and both measures are insufficient. A pilot that produces an accurate model through a process nobody can audit has proved the wrong thing, because the governance burden arrives in production, not in the pilot.</p>
<p>Four measures belong in the pilot scorecard. <strong>Model quality</strong> against a centrally held validation set, compared with the centralised baseline the federated approach is replacing — if federation costs more than a few points of accuracy, the trade-off needs an explicit decision. <strong>Privacy posture</strong>, recorded as the actual configuration: aggregation protocol, differential privacy epsilon, clipping bounds, and whether any single node's update could be isolated. <strong>Governance evidence</strong>: can the pilot produce, on request, the full training record — which nodes participated, which data versions, which approvals, which update round contributed what. <strong>Operational cost</strong>: coordination overhead per round, time to onboard a new node, and the effort required to investigate a quality failure.</p>
<p>The last two are where pilots usually fail, and they are the measures that predict whether the approach scales past three nodes. A pilot designed around all four produces a decision rather than a demonstration.</p>
""", '<section class="faq-section"'),

"ai-strategy-maturity-assessment": ("""
<h2 id="how-do-conversational-interfaces-change-the-maturity-picture">How Do Conversational Interfaces Change the Maturity Picture?</h2>
<p>Conversational analytics changes what maturity looks like in one specific way: it removes the interface as a barrier, which shifts the constraint to the data foundation and the semantic layer. That is useful diagnostically, because it makes the real maturity level visible faster than any workshop.</p>
<p>In organisations at levels 1 and 2, giving business users a natural-language interface produces a burst of questions the platform cannot answer well — not because the model is weak, but because the metrics are undefined, the data is not connected, or ownership is unclear. That burst is the most accurate maturity assessment available, and it costs a fortnight rather than a quarter.</p>
<p>In organisations at level 3 and above, the same deployment produces immediate adoption, because the definitions exist and the data is connected. The difference in outcome between the two is entirely attributable to the dimensions the model measures, which is why several organisations now use a two-week conversational deployment as an input to their formal assessment rather than waiting for the assessment to complete before deploying anything.</p>
<p>The caution is that a poor first experience is expensive. Deploying to an organisation whose semantic layer is not ready produces answers users learn to distrust, and distrust is harder to reverse than ignorance. Assess the data foundation first, then deploy where it will succeed.</p>
""", '<h2 id="key-takeaways">'),

"mcp-security-model-access-control-enterprise": ("""
<h2 id="how-do-you-roll-out-mcp-security-without-blocking-teams">How Do You Roll Out MCP Security Without Blocking Teams?</h2>
<p>Security programmes in this category fail in a recognisable way: controls are announced, teams route around them, and the organisation ends up with less visibility than before. Three practices avoid that outcome.</p>
<p><strong>Provide a paved road before publishing restrictions.</strong> Teams will accept a gateway requirement only if the gateway is genuinely easier than bypassing it. That means pre-approved connectors for the common sources, a template for registering a new one, and a turnaround commitment on reviews. A review queue with no service level is the single fastest way to create shadow deployments.</p>
<p><strong>Sequence controls by risk, not by completeness.</strong> Start with identity and allowlists, which are cheap and cover most of the exposure. Add output validation, masking, and cost budgets in the second wave. Trying to enforce all six gateway checks on day one produces a backlog of exceptions and a reputation for blocking delivery.</p>
<p><strong>Make the safe path observable.</strong> Give teams a dashboard of their own agents' calls, rejections and costs. Visibility converts security from a gate into a feedback loop, and it surfaces misconfigurations before they become incidents — usually by the team that created them.</p>
<p>The measure of success is not zero violations; it is zero <em>unknown</em> deployments. Every agent calling tools through the gateway, with identity attached and logs flowing, is a manageable risk even when individual configurations are imperfect.</p>
""", '<section class="faq-section"'),

"china-pipl-enforcement-update-summer-2025": ("""
<h2 id="what-should-be-in-a-china-data-protection-incident-response-plan">What Should Be in a China Data Protection Incident Response Plan?</h2>
<p>Incident response obligations are the area where planning is cheapest and improvisation most costly, because the deadlines are statutory and begin on discovery rather than on assessment. Four elements need to exist before an incident, not during one.</p>
<p><strong>A classification rule.</strong> Not every incident requires notification, but the determination must be made against a documented threshold rather than judgement under pressure. Define in advance which events — volume of personal information affected, categories involved, whether sensitive personal information is implicated — trigger reporting and to whom.</p>
<p><strong>A notification path with named authorities and owners.</strong> Which regulator, which internal approver, which external counsel, and the order in which they are contacted. The common failure is spending the first day deciding who decides.</p>
<p><strong>A communications plan for affected individuals.</strong> Where notification is required, the message, the channel, and the timing need to be drafted and approved in advance. Drafting under deadline, in two languages, with legal review, is how organisations miss statutory windows.</p>
<p><strong>An evidence pack.</strong> The record an authority will expect: what happened, when it was discovered, what data was affected, what was done, and what has changed since. Build the pack as the response proceeds rather than reconstructing it afterwards.</p>
<p>Test the plan annually with a tabletop exercise. The first run almost always reveals that the hardest part is not the technical containment — it is locating the affected data quickly enough to answer the first question anyone asks.</p>
""", '<section class="faq-section"'),

"data-contract-enforcement-in-production-pipelines": ("""
<h2 id="how-do-contracts-work-with-streaming-and-real-time-sources">How Do Contracts Work With Streaming and Real-Time Sources?</h2>
<p>Contracts are often presented as a batch-oriented discipline, which leads teams to conclude they do not apply to streaming pipelines. They do, but the enforcement points differ and the semantics matter more.</p>
<p>For a stream, the schema section behaves as it does in batch, with one addition: the key and partitioning scheme belong in the contract, because changing them is as breaking as renaming a field and far easier to do accidentally. The semantics section carries the event-time definition — which timestamp denotes when the thing happened, as opposed to when it was processed — because nearly every late-data bug traces back to a disagreement about that distinction.</p>
<p>Service levels take on more weight in streaming. Freshness becomes lag tolerance: the maximum acceptable delay between event time and availability, with an alert threshold below the contractual limit so the team hears about degradation before consumers do. Volume expectations become a range with seasonal adjustment, since a stream that legitimately triples at month-end should not generate an incident.</p>
<p>Enforcement moves to three places: schema validation at the producer on publish, compatibility checking against registered consumers before a schema version is promoted, and runtime assertions inside the consumer's stream processing job with a dead-letter queue for records that fail. The dead-letter queue is what makes runtime enforcement survivable — bad records are captured and counted rather than silently dropped or allowed to halt the pipeline.</p>
""", '<h2 id="key-takeaways">'),

"conversational-bi-empowers-non-technical-teams-2025": ("""
<h2 id="what-should-leaders-do-in-the-first-30-days">What Should Leaders Do in the First 30 Days?</h2>
<p>The first month determines whether a conversational BI deployment becomes infrastructure or a forgotten pilot. Four actions, in order.</p>
<p><strong>Week one: collect real questions, not requirements.</strong> Ask each target team for ten questions they asked last month and could not answer quickly. This list is the specification, it is more accurate than any workshop output, and it immediately reveals which metrics are undefined — which is the actual work.</p>
<p><strong>Week two: map the semantic layer to what already exists.</strong> Reuse the definitions finance and operations already sign off on. The strongest implementations do not rebuild the data stack; they expose what is already governed. Where a definition does not exist, assign an owner and a deadline rather than improvising one.</p>
<p><strong>Week three: pilot with two teams and watch the failures.</strong> Two, not one, because the second team without a champion is the real test. Log every question that returns a poor answer; that log is the highest-value artefact of the pilot and the input to week four.</p>
<p><strong>Week four: publish the wins and fix the gaps.</strong> Share the best answers in team channels so the vocabulary spreads by example, and close the top five semantic gaps surfaced by the failure log. Then measure the one number that matters: the change in ad-hoc requests reaching the analytics team.</p>
<p>Leaders who skip week one usually spend month two discovering that the tool answers questions nobody was asking.</p>
""", '<section class="faq-section"'),

"mcp-future-enterprise-data-integration": ("""
<h2 id="what-skills-does-an-mcp-programme-need">What Skills Does an MCP Programme Need?</h2>
<p>MCP programmes are usually staffed as integration projects, and that is why they underdeliver. The work is closer to platform engineering with a governance component, and the skill mix reflects that. Four roles matter.</p>
<p><strong>Platform or integration engineering</strong> owns the connector library, the gateway, and the deployment pipeline. This is the role most organisations staff first and the only one that is obviously required — it is necessary but not sufficient.</p>
<p><strong>Semantic modelling</strong> is the role most often missing. Somebody has to own the definitions the agents reason over: which metrics exist, what they mean, which are certified, and who approves changes. Without it, agents produce fluent answers over undefined concepts, and accuracy problems get misdiagnosed as model problems.</p>
<p><strong>Security engineering with machine identity experience</strong> is needed for the gateway controls: delegated authority, allowlists, audit logging, and revocation. This is materially different from application security, and teams without machine identity experience tend to reinvent service accounts.</p>
<p><strong>A product owner for the tool surface</strong> treats tools and connectors as products with users, documentation, and a lifecycle. This is what prevents sprawl, because someone is accountable for whether the library is actually usable rather than merely complete.</p>
<p>Most enterprises do not need four new hires; they need one new role — semantic modelling — and a clear assignment of the other three to existing teams. The failure mode is assuming the work belongs to whoever is enthusiastic about agents.</p>
""", '<section class="faq-section"'),

"data-marketplace-enterprise-data-monetization-strategy": ("""
<h2 id="what-does-a-data-product-manager-actually-do">What Does a Data Product Manager Actually Do?</h2>
<p>The data product manager role is the largest organisational lever in a marketplace programme and the one most enterprises have to create rather than assign. It is genuinely hybrid: part product manager, part data steward, and the two halves pull in different directions.</p>
<p>The product half owns demand. Which questions are consumers trying to answer, which products should exist, what the definition and freshness commitment should be, and what the roadmap is. This is the side that prevents the most common marketplace failure — a catalogue built from what data happens to be available rather than from what anyone needs.</p>
<p>The steward half owns trust. Lineage is complete, sensitivity is classified, rights are verified, quality is monitored, and the permitted-use register is current. This is the side that prevents the second most common failure: a product that sells well until someone asks where the data came from.</p>
<p>Three practices make the role work. Give each product manager a small portfolio rather than a domain, so accountability is specific. Give them a direct channel to the consumers, because the failure log and the unanswered-search log are their primary inputs. And measure them on reuse and time-to-access rather than on catalogue size, because a large catalogue of unused products is the metric that kills these programmes.</p>
<p>Where enterprises cannot hire for the role, the workable interim is a pair: a product owner from the business side and a data steward from governance, jointly accountable and measured on the same numbers. It is less efficient than one owner, but far better than leaving the accountability unassigned.</p>
""", '<section class="faq-section"'),
}

for slug, (block, anchor) in TOP.items():
    s = F.load(slug, "EN")
    b = F.get_body(s)
    marker = block.strip()[:70]
    if marker in b:
        print("skip", slug); continue
    if anchor.startswith('<section') and '<section class="faq-section"' in b:
        anchor = '<section class="faq-section"'
    if anchor not in b:
        for alt in ('<section class="faq-section"', '<h2 id="key-takeaways">', '<h2 id="beehive-strategy-and-mlops">'):
            if alt in b:
                anchor = alt; break
    b = b.replace(anchor, block.strip() + "\n" + anchor, 1)
    F.save(slug, "EN", F.set_body(s, b))
    s = F.load(slug, "EN")
    F.save(slug, "EN", F.sync_toc(s))
    print(slug, F.stats(F.load(slug, "EN")))
