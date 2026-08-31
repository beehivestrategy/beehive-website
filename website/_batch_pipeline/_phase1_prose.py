# -*- coding: utf-8 -*-
import re, os

BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

# EN prose to insert per slug: list of (h2_id, h2_text, html_block)
EN = {
"real-time-data-streaming-for-ai-powered-decision-making-part-2": [
("choosing-streaming-patterns","How Do You Choose Between Streaming Patterns for AI Workloads?",
"""<h2 id="choosing-streaming-patterns">How Do You Choose Between Streaming Patterns for AI Workloads?</h2>
<p>The pattern you choose should follow the decision, not the fashion. For anomaly detection and fraud, where the value is in catching the event within seconds, a simple event-at-a-time stream with a stateful scoring step is usually right: each record is scored as it arrives, and only the exceptions are surfaced. For personalisation and real-time bidding, where the model needs recent context about a user or a device, a micro-batch pattern — refreshing features every few seconds — balances freshness against compute cost better than true per-event processing. For agentic systems that react to business events, an event-driven pattern where each signal triggers a discrete agent task tends to be more resilient than a single monolithic pipeline, because a failure in one lane does not stall the others.</p>
<p>The trap is over-engineering. Most enterprises do not need sub-second latency everywhere; they need it at the handful of decisions where speed is the advantage. Start by ranking use cases by the cost of delay, then apply the lightest pattern that meets that latency. A streaming architecture that scores the wrong thing in real time delivers less value than a batch architecture that scores the right thing within the hour. The 2026 maturity signal is not throughput but decision coverage: what fraction of time-sensitive decisions now run on fresh data, and what fraction still wait on a nightly job.</p>"""),
("streaming-governance-production","What Does Good Streaming Governance Look Like in Production?",
"""<h2 id="streaming-governance-production">What Does Good Streaming Governance Look Like in Production?</h2>
<p>Streaming systems fail quietly, so governance has to be observable by default. That means schema enforcement at the door — every event is validated against a contract before it enters the pipeline — plus freshness, lag, and drift metrics exposed to the same dashboard the business uses. When a feature stops updating, the model should degrade gracefully and flag the gap rather than serve stale scores with false confidence. Lineage matters more in streaming than in batch, because the data is moving; you must be able to answer, for any prediction, which event version produced it.</p>
<p>Organisationally, streaming governance works best when the data platform team owns the pipes and the domain team owns the contracts, with a shared on-call rotation so neither side can point at the other when something breaks at 2 a.m. The enterprises that scale streaming successfully treat their event contracts as internal APIs with versioning and deprecation policies, exactly as they would for external services. That discipline is what keeps a real-time architecture trustworthy as the number of sources grows from five to five hundred — and it is the unglamorous reason most streaming pilots stay pilots while the disciplined ones become infrastructure.</p>"""),
],
"china-ai-model-wave-conversational-bi-evolution-2026": [
("evaluating-chinese-vendors","How Should Enterprises Evaluate a Chinese Conversational BI Vendor?",
"""<h2 id="evaluating-chinese-vendors">How Should Enterprises Evaluate a Chinese Conversational BI Vendor?</h2>
<p>Evaluation should start with the data boundary, not the demo. The defining question for any conversational BI vendor is whether the model answers from your live, permissioned data or from a generic cloud service trained elsewhere. Domestic Chinese models such as those from Alibaba, Baidu, and Zhipu have closed the gap with frontier labs on reasoning and Mandarin comprehension, but the enterprise value is created by the layer that connects the model to governed data, not by the model alone. A vendor that cannot show row-level permission enforcement, audit logging, and a semantic layer you control should not reach production, regardless of benchmark scores.</p>
<p>The second axis is deployment posture. Regulated and data-sensitive enterprises increasingly require private or on-premises deployment so that proprietary data never leaves the perimeter. Ask specifically how the vendor handles model updates, how prompts and results are retained, and what happens to your semantic definitions if you switch providers. The vendors winning enterprise deals in 2026 are the ones that treat the customer's knowledge graph and metric definitions as portable assets the customer owns, rather than lock-in. Pilot on three real questions your analysts ask weekly, measure answer accuracy against a human baseline, and only then decide.</p>"""),
("risks-and-mitigations","What Are the Risks and Mitigations When Adopting Domestic Models?",
"""<h2 id="risks-and-mitigations">What Are the Risks and Mitigations When Adopting Domestic Models?</h2>
<p>The principal risks are data residency, supply continuity, and capability drift. Data residency is addressed through deployment architecture: keep inference and storage inside the required jurisdiction, and prefer vendors with a clear private-deployment story. Supply continuity matters because the model landscape is shifting fast; mitigate it by separating the model from the application layer so a new model can be swapped in without rebuilding your connectors or semantic definitions. Capability drift is the quiet risk — a model that is state of the art today may be mid-pack in eighteen months — which is why an abstraction layer that lets you route queries to the best available model per task is a more durable investment than betting the roadmap on a single vendor.</p>
<p>None of these risks argue against adopting domestic models; they argue for adopting them with the same governance you would apply to any critical dependency. The enterprises that benefit most from the China AI model wave are those that use the local models as a cost-effective, jurisdiction-friendly compute layer while keeping their data, their definitions, and their evaluation harness firmly in hand. That combination — local models, owned semantics, rigorous measurement — is what turns a fast-moving model market into a durable analytical advantage rather than a recurrent procurement headache.</p>"""),
],
"agentic-workflows-enterprise-automation": [
("measuring-agentic-workflows","How Do You Measure Whether Agentic Workflows Are Actually Working?",
"""<h2 id="measuring-agentic-workflows">How Do You Measure Whether Agentic Workflows Are Actually Working?</h2>
<p>Measure the workflow, not the model. The headline metric is cycle time from trigger to completed outcome, compared against the manual baseline the agent replaced. If a procurement agent used to take three days and now takes four hours, that delta is the value; the model's accuracy score is irrelevant if the work is not getting done faster and correctly. Pair cycle time with two guardrail metrics: exception rate — the share of cases the agent had to escalate to a human — and rework rate, the share of agent outputs that were reversed or corrected. A healthy program drives exception rate down over time as the agent learns, without quietly pushing errors into production.</p>
<p>Beyond efficiency, measure leverage: how many distinct workflows one agent framework now serves, and how cheaply a new workflow can be added. The payoff of agentic automation is not one clever bot but a platform where the marginal cost of the next automation falls toward zero. Enterprises that track only cost savings miss this; the ones that also track workflow coverage and time-to-new-automation discover that the compounding effect — more workflows, lower unit cost — is where the strategic value lives. Report these weekly to the sponsor so the program is steered by evidence rather than demos.</p>"""),
("agentic-governance-guardrails","What Governance Guardrails Keep Autonomous Agents Safe?",
"""<h2 id="agentic-governance-guardrails">What Governance Guardrails Keep Autonomous Agents Safe?</h2>
<p>Safe autonomy is bounded autonomy. The first guardrail is action classification: agents may take low-risk, reversible actions automatically, but anything irreversible — sending money, deleting records, contacting customers — requires a human approval step or a hard policy check. The second is a permission boundary identical to the one applied to human users, enforced at the data layer so the agent sees only what its operator may see. The third is an immutable audit trail of every tool call, decision, and retrieved source, so any outcome can be reconstructed after the fact.</p>
<p>The fourth guardrail is kill-switch design: a way to freeze an agent's actions the moment behaviour looks wrong, without taking down the systems it depends on. The fifth is evaluation in production — shadow runs and canary deployments where the agent's proposed action is checked against a human's before it is allowed to act, until confidence is earned. Organisations that ship agents with these five guardrails move fast and stay safe; those that ship agents with only a prompt and good intentions tend to learn the hard way that autonomy without boundaries is just uncapped risk.</p>"""),
],
"enterprise-ai-governance-board-framework": [
("board-ai-oversight-agenda","What Should the Board's AI Oversight Agenda Cover?",
"""<h2 id="board-ai-oversight-agenda">What Should the Board's AI Oversight Agenda Cover?</h2>
<p>The board does not need to read model code; it needs to own the questions that determine whether AI creates or destroys value. The agenda should cover three standing items: risk exposure — where autonomous systems can cause harm or regulatory breach; value realisation — whether the portfolio is hitting the business baselines it was funded against; and capability trajectory — whether the organisation is building the data, talent, and governance muscle to stay competitive. Each item needs a single owner and a plain-language scorecard, so the board can see trend rather than incident.</p>
<p>A useful discipline is to require every material AI initiative to present a one-page pre-mortem: what would have to go wrong for this to embarrass the company in twelve months, and what guardrail prevents it. This forces teams to confront failure modes before launch rather than after, and it gives the board a concrete basis for challenge. The boards that govern AI well treat it as a continuing risk-and-return conversation, reviewed on a fixed cadence, not as a one-time approval of a strategy deck that is obsolete before the ink dries.</p>"""),
("board-review-cadence","How Often Should the Board Review AI Risk and Value?",
"""<h2 id="board-review-cadence">How Often Should the Board Review AI Risk and Value?</h2>
<p>Quarterly is the floor; the risk review in particular should be event-driven, not calendar-driven. AI incidents — a biased decision, a leaked prompt, a model that drifted — move faster than audit cycles, so the governance framework needs a trigger that escalates material events to the board within days, not at the next quarter-end. Value review can stay quarterly, because business impact accrues over a cycle, but it should be tied to the same baselines used at funding so the board is comparing promises to delivery.</p>
<p>The cadence also depends on deployment maturity. An enterprise in early experimentation needs a lighter touch; one with agents taking real actions on customer money needs a near-continuous risk signal aggregated into a monthly board digest with a clear escalate path. The mistake is treating AI governance as a compliance chore to be minimised. The enterprises pulling ahead treat the board review as the moment the strategy is tested against reality — and they use it to reallocate capital toward the initiatives that are actually compounding advantage.</p>"""),
],
"conversational-bi-human-resources-people-analytics": [
("hr-questions-conversational","Which HR Questions Benefit Most from Conversational Analytics?",
"""<h2 id="hr-questions-conversational">Which HR Questions Benefit Most from Conversational Analytics?</h2>
<p>People analytics has always been data-rich and insight-poor, because the questions are ad hoc and the reports are slow. Conversational BI changes that by letting any HR business partner ask, in plain language, who is at flight risk this quarter and why, where pay equity gaps sit by role and region, or which teams are overstretched against their goals — and get a sourced answer in seconds. The questions that benefit most are the recurring, judgement-heavy ones: attrition drivers, succession coverage, span-of-control strain, and the cost of unfilled critical roles.</p>
<p>The second class of high-value questions is the what-if: if we promoted from within for these roles, what would the cascade be; if we restructured this team, where would the skills gaps appear. These are exactly the questions leaders hesitate to ask because the analysis used to take weeks. When the answer arrives in the meeting, the conversation shifts from whether to act to how to act — which is the whole point of people analytics. The organisations seeing the fastest adoption are those that put the conversational layer directly inside the HRIS and the leadership dashboard, so the question is one click from the decision it informs.</p>"""),
("privacy-trust-people-analytics","How Do You Maintain Privacy and Trust in People Analytics?",
"""<h2 id="privacy-trust-people-analytics">How Do You Maintain Privacy and Trust in People Analytics?</h2>
<p>Trust is the product. The moment employees believe people analytics is surveillance, the data quality and the culture both degrade, so the governance has to be visible and consensual. That starts with role-based access: an HRBP sees their own population, a manager sees only their team, and no individual is ever singled out in an aggregate answer below a safe threshold. Every query and answer is logged, and the purpose of analysis is communicated plainly — to support development and fair treatment, not to police.</p>
<p>Technically, privacy is preserved by aggregating at a minimum group size, by separating identifiable source data from the analytic layer, and by letting employees see what is inferred about their team so the process feels transparent rather than opaque. The conversational layer should refuse to answer requests that would identify an individual, and should explain why. Enterprises that get this right turn people analytics from a function employees distrust into one they use to advocate for themselves — and that shift is what unlocks the value the data always promised but rarely delivered.</p>"""),
],
"case-study-consultancy-cut-reporting-time-mcp-bi": [
("what-made-10-day-possible","What Made the 10-Day Deployment Possible?",
"""<h2 id="what-made-10-day-possible">What Made the 10-Day Deployment Possible?</h2>
<p>The 10-day timeline was possible because the engagement refused to rebuild anything. The consultancy already had the data — in a warehouse, a CRM, and a billing system — it just could not reach it fast enough. The MCP layer wrapped those existing systems with standard connectors, so the conversational interface could query live project, billing, and utilization data without a warehouse modernization project. The semantic layer defined the handful of metrics that actually mattered — realization rate, write-off, at-risk accounts — once, and applied them everywhere.</p>
<p>The second enabler was scope discipline. The team did not try to answer every question on day one; it picked the eight questions partners asked most, proved them on real data with real permissions, and shipped. The third was treating the model as plumbing: a commodity frontier model handled the language, while the proprietary data and definitions did the work. That sequencing — connect, define, ask — is repeatable, and it is why a 10-day deployment is not a stunt but a pattern. The consultancy's existing data estate did almost all of the heavy lifting; the project's job was to remove the wait, not to add architecture.</p>"""),
("replicate-this-model","How Can Other Service Firms Replicate This Model?",
"""<h2 id="replicate-this-model">How Can Other Service Firms Replicate This Model?</h2>
<p>Any knowledge-intensive firm sitting on a warehouse of billable, client, and utilization data can replicate this in weeks, not quarters, by following the same three moves. First, inventory the questions your senior people ask repeatedly and that currently take an analyst hours — that is your value map. Second, stand up an MCP-connected conversational layer over the systems that hold those answers, with permissions that mirror your existing access rules. Third, define your core metrics once in a semantic layer so every answer means the same thing.</p>
<p>The firms that succeed treat this as a margin and talent play, not a technology pilot. The 71% faster reporting in the case study translated directly into partners spending more time with clients and less time waiting on reports — and into a new offering, because the firm could now sell analytics it had previously only wished it had. The replication risk is scope creep: resist the urge to model every edge case first. Prove the top eight questions, show the time saved, and let the second wave of use cases fund itself from the credibility the first wave earns.</p>"""),
],
"event-driven-architecture-for-ai-agent-orchestration-a-2026-update": [
("event-driven-risk-reduction","How Does Event-Driven Design Reduce Agent Orchestration Risk?",
"""<h2 id="event-driven-risk-reduction">How Does Event-Driven Design Reduce Agent Orchestration Risk?</h2>
<p>Event-driven orchestration contains failure by design. In a tightly coupled orchestrator, one stuck step can block the entire workflow; in an event-driven design, each business event — an order placed, a ticket opened, a reading breaching threshold — triggers a discrete agent task that runs, emits its result as a new event, and completes independently. If one lane fails, the others keep moving, and the failed lane can be retried or routed to a human without halting the system. That isolation is what makes agentic systems safe to run at scale.</p>
<p>The second risk reduction is observability. Because every step is an event with a producer, a payload, and a consumer, the whole workflow is naturally auditable and replayable. When an agent makes a wrong call, you can see exactly which event triggered it, what data it saw, and what it did — and you can replay the sequence to confirm the fix. In 2026, as agents take actions on real money and real customers, that forensic capability is not optional; it is the difference between an incident you can explain and one you cannot. Event-driven design makes the explanation automatic.</p>"""),
("event-vs-orchestrated-tradeoffs","What Are the Trade-Offs of Event-Driven vs Orchestrated Agents?",
"""<h2 id="event-vs-orchestrated-tradeoffs">What Are the Trade-Offs of Event-Driven vs Orchestrated Agents?</h2>
<p>The trade-off is control versus resilience. A central orchestrator gives you a single place to enforce sequencing, compensation, and global state — valuable when steps are tightly dependent, like a multi-stage approval. The cost is a single point of failure and a planning bottleneck: every new behaviour has to be encoded in the orchestrator. Event-driven designs invert that — they are loosely coupled, easy to extend, and inherently fault-isolating, but they make end-to-end guarantees harder and can let independent agents work at cross-purposes if the events are not well defined.</p>
<p>The 2026 pattern is hybrid: orchestrate the few workflows that genuinely need strict ordering, and let the rest be event-driven. The deciding question is whether a step's correctness depends on the outcome of the previous step. If yes, orchestrate; if each step is triggered by a business signal and emits its own signal, event-driven is simpler and safer. Most enterprises over-orchestrate; the maturity shift this year is recognising that events, not flows, are the natural unit for agentic work, and reserving orchestration for the narrow cases where sequence is the product.</p>"""),
],
"enterprise-data-catalog-ai-readiness-oct2025": [
("catalog-ai-ready","How Does a Data Catalog Become AI-Ready Rather Than Just Inventoried?",
"""<h2 id="catalog-ai-ready">How Does a Data Catalog Become AI-Ready Rather Than Just Inventoried?</h2>
<p>Most catalogs stop at inventory: a searchable list of tables and owners. AI-readiness goes further, because a model cannot use data it cannot understand. An AI-ready catalog captures the semantic layer — what each metric means, how it is computed, and how it relates to others — so a model querying "revenue" gets the same definition finance uses, not a guess. It also captures lineage, quality rules, and access policy per asset, so the conversational layer can answer not just what the data is but whether it is trustworthy and who may see it.</p>
<p>The practical test of AI-readiness is simple: can a non-technical user ask a question in plain language and get an answer grounded in catalogued, governed, documented data without a data engineer in the loop? If the answer is no, the catalog is a library, not a foundation. The enterprises that reach readiness do it incrementally — start with the fifty assets behind the questions leaders ask most, document their meaning and rules, and expand. The catalog becomes the contract between human intent and machine access, and that contract is what lets AI agents query with confidence instead of hallucination.</p>"""),
("catalog-value-metrics","What Metrics Show a Data Catalog Is Delivering Value?",
"""<h2 id="catalog-value-metrics">What Metrics Show a Data Catalog Is Delivering Value?</h2>
<p>The metric that matters is time-to-answer, not number of assets catalogued. A catalog with ten thousand entries that nobody queries delivers less value than one with two hundred well-documented, well-governed assets that answer real questions daily. Track how often the catalogued semantic layer is actually used to serve an AI answer, how much analyst time it removes, and how many "where does this number come from" disputes it resolves. Those are the signals of value; coverage alone is vanity.</p>
<p>Pair those with trust metrics: the share of catalogued assets with a defined owner, a quality rule, and an access policy. An asset without an owner will drift, and an AI answer built on it will eventually be wrong. The catalogs that compound value are the ones where every high-use asset has all three, reviewed on a fixed cadence, so the foundation stays solid as the data estate grows. Report these as a simple readiness score to the data governance sponsor, and the catalog stops being a metadata project and starts being the reason AI answers can be trusted.</p>"""),
("catalog-rollout-phasing","How Should Enterprises Phase a Data Catalog Rollout?",
"""<h2 id="catalog-rollout-phasing">How Should Enterprises Phase a Data Catalog Rollout?</h2>
<p>Phase one is scope, not software: pick the domain behind the most urgent questions — often finance, commercial, or operations — and catalogue its core assets with real definitions and owners. Phase two connects the catalog to the conversational or agentic layer so those definitions are enforced at query time; this is where the catalog starts preventing wrong answers rather than merely documenting data. Phase three expands to adjacent domains and adds automated quality and lineage capture so new assets arrive documented rather than as a backlog.</p>
<p>The common failure is boiling the ocean: trying to catalogue everything before delivering anything, so the program loses sponsorship before it shows value. The enterprises that succeed ship a working, queryable slice in the first month and let proven value pull the rest of the estate into the catalog. They also assign ownership explicitly — every asset has a human who is accountable for its meaning and its rules — because a catalog nobody owns becomes stale within a quarter. Phased, owned, and wired to the AI layer: that is the rollout that turns a catalog from a cost centre into competitive infrastructure.</p>"""),
],
"rag-architecture-patterns-enterprise-2025": [
("choosing-rag-pattern","How Do You Choose the Right RAG Pattern for Your Enterprise?",
"""<h2 id="choosing-rag-pattern">How Do You Choose the Right RAG Pattern for Your Enterprise?</h2>
<p>The choice starts with the knowledge, not the toolkit. If your answers must come from a stable, structured corpus — policies, product specs, a knowledge base — naive chunk-and-retrieve RAG is usually enough and cheapest to run. If the corpus is large and overlapping, hybrid retrieval that combines keyword and vector search reduces the wrong-document problem that pure vector search introduces. If answers must cite live operational data, RAG should retrieve from the semantic layer and the warehouse rather than from static documents, so the answer reflects now, not last quarter's export.</p>
<p>The second axis is correctness under pressure. For high-stakes domains, add re-ranking and a groundedness check that verifies the answer against the retrieved passages before it is shown, and refuse to answer when confidence is low. The pattern you pick should match the cost of being wrong: a customer-facing support bot can tolerate more ambiguity than an internal compliance assistant. The enterprises that get RAG right resist the temptation to over-build; they start with the simplest pattern that meets the accuracy bar, measure where it fails, and add complexity only where the failures actually hurt.</p>"""),
("rag-failure-modes","What Are the Most Common RAG Failure Modes in Production?",
"""<h2 id="rag-failure-modes">What Are the Most Common RAG Failure Modes in Production?</h2>
<p>The first failure mode is retrieval drift: the index goes stale, so the model answers from outdated context while everyone assumes it is current. The fix is a refresh pipeline with freshness SLAs and monitoring, not a one-time load. The second is chunking that breaks meaning — splitting a clause from its condition — so the retriever finds the words but not the sense. The third is silent hallucination, where the model fills gaps the retrieval missed; a groundedness check and a candid "I don't know" threshold are the antidote.</p>
<p>The fourth is permission blindness: retrieving documents a user should not see. RAG must enforce the same access control as the source system, filtered at retrieval time, not after. The fifth is evaluation debt — shipping RAG without a labelled set of questions and expected answers, so nobody notices when accuracy slips. The enterprises that run RAG reliably treat it as a system with a refresh, a guardrail, and a test suite, reviewed like any production service. RAG is not fire-and-forget; it is a pipeline whose output people act on, and the failure modes are all variants of forgetting that.</p>"""),
],
"cybersecurity-ai-threat-landscape-q4-2025": [
("attackers-using-ai","How Are Attackers Actually Using AI Today?",
"""<h2 id="attackers-using-ai">How Are Attackers Actually Using AI Today?</h2>
<p>The headline use is scale and fluency. AI lets attackers generate convincing, grammar-perfect phishing in any language at near-zero marginal cost, and it lets them tailor each message to a target's public footprint so the lure reads like an internal note. It also accelerates vulnerability research — summarising patches, finding exploit paths, and fuzzing faster than a human team. In Q4 2025 the shift worth noting is not a single new attack but the industrialisation of existing ones: the same phishing and recon work, produced faster and personalised to the individual, which raises both volume and click-through.</p>
<p>The second use is evasion. Attackers use generative models to mutate malware signatures and to write scripts that blend in with normal operations, lowering the chance of detection by rules-based tools. Deepfake voice and video are being used in targeted social-engineering against finance and help desks, where a convincing call can move money or reset access. None of this requires frontier capability; it requires access, which is now cheap. The defensive implication is that perimeter and signature controls alone are obsolete, and identity, behaviour, and verification are where the real fight now sits.</p>"""),
("defensive-priorities","What Defensive Capabilities Should Security Teams Prioritise?",
"""<h2 id="defensive-priorities">What Defensive Capabilities Should Security Teams Prioritise?</h2>
<p>Priority one is detection that assumes the email looks perfect: behavioural analytics that flag anomalous requests regardless of how plausible the message is, because the language is no longer a tell. Priority two is identity proofing for high-risk actions — outbound payments, access resets, credential changes — with out-of-band verification that a deepfake cannot satisfy. Priority three is AI-assisted defence: using your own models to triage alerts, summarise incidents, and draft responses faster than the attacker's automation can pivot.</p>
<p>Priority four is rehearsal: red-team the deepfake and phishing scenarios that now exist, so the help desk and finance know the procedure when the real one arrives. Priority five is supply-chain and model risk — if you consume AI features from vendors, know what data they retain and what they can do. The teams coping best are not buying more point tools; they are closing the gap between attack speed and response speed with automation of their own, and treating identity as the new perimeter. The threat landscape in Q4 2025 rewards organisations that assumed breach and engineered for response, not those that assumed their filters would hold.</p>"""),
],
"ai-success-metrics-beyond-accuracy": [
("leading-indicators","Which Leading Indicators Predict Long-Term AI Success?",
"""<h2 id="leading-indicators">Which Leading Indicators Predict Long-Term AI Success?</h2>
<p>Accuracy is a lagging indicator of model quality, not of business success. The leading indicators that actually predict durable value are adoption and cycle time: are people using the system weekly, and does the decision it serves happen faster than before. An AI capability nobody acts on creates zero value regardless of its F1 score. A second leading indicator is data-loop health — the share of each new decision's outcome that flows back to improve the next one — because that is what compounds advantage.</p>
<p>A third is reuse: how many workflows one platform now serves, and how cheaply a new one is added. Reuse signals that the organisation is building capability, not a museum of one-off pilots. A fourth is the ratio of production use cases to experiments; a healthy program converts a steady share of pilots into live systems rather than letting them die in the graveyard. Track these monthly and they will tell you, quarters early, whether the program is becoming infrastructure or becoming a cost — long before the annual ROI review would have revealed the truth.</p>"""),
("avoiding-vanity-metrics","How Do You Avoid Vanity Metrics in AI Programs?",
"""<h2 id="avoiding-vanity-metrics">How Do You Avoid Vanity Metrics in AI Programs?</h2>
<p>Vanity metrics are the ones that go up while value does not: number of models deployed, pilots launched, proofs of concept demoed, or benchmark scores beaten. They feel like progress and hide the fact that nothing reached a decision. The discipline is to report every AI initiative against a business baseline it was funded to move — margin, cycle time, retention, error rate — and to retire metrics that cannot be tied to one. If a metric does not change a decision, it is decoration.</p>
<p>The second guardrail is to measure against the counterfactual, not against zero. A chatbot that answers 80% of queries sounds good until you learn the old FAQ answered 70% and the new one just sounds nicer while deflecting the hard ones. Ask what changed for the customer or the cost line, not what the dashboard shows. The programs that avoid vanity metrics are the ones whose sponsors refuse to celebrate deployment and insist on evidence of impact — and they are the ones whose AI budgets survive the moment the broader spend comes under scrutiny.</p>"""),
],
"why-edge-ai-manufacturing-logistics-energy": [
("edge-ai-business-case","How Do You Justify an Edge AI Investment to the Board?",
"""<h2 id="edge-ai-business-case">How Do You Justify an Edge AI Investment to the Board?</h2>
<p>The board case for edge AI is about latency, continuity, and data cost — three things the cloud cannot fully solve on a factory floor or a remote site. Latency: a quality check that must happen in milliseconds to catch a defect on the line cannot wait for a round trip to a region. Continuity: when the network drops, a cloud-dependent process stops, but an edge model keeps the line running. Data cost: shipping every sensor reading to the cloud is expensive and often unnecessary when the decision can be made where the data is born.</p>
<p>The justification should be use-case-led, not technology-led. Pick one process where a stopped line, a missed defect, or a delayed dispatch costs real money, and show the payback from moving the inference to the edge. In manufacturing that is in-line inspection; in logistics it is route and load optimisation at the depot; in energy it is predictive maintenance on assets far from connectivity. Frame the investment as risk reduction and margin protection first, and capacity expansion second. Boards fund edge AI when the alternative — a line that cannot inspect itself, a site that goes blind when the link drops — is the more expensive option, which on heavy industry it usually is.</p>"""),
("edge-ai-hidden-costs","What Are the Hidden Costs of Edge AI Deployments?",
"""<h2 id="edge-ai-hidden-costs">What Are the Hidden Costs of Edge AI Deployments?</h2>
<p>The visible cost is hardware; the hidden cost is lifecycle. Hundreds of edge devices mean hundreds of models to update, monitor, and patch, often in places with no IT staff and intermittent connectivity. If you do not design for over-the-air update, health telemetry, and graceful degrade, the edge fleet becomes a maintenance liability that fills the very downtime it was meant to prevent. The second hidden cost is data drift: an edge model trained on one site's conditions may misread another's, and without centralized monitoring you will not notice until scrap climbs.</p>
<p>The third is security at the physical edge, where devices are easier to tamper with than a guarded data centre. Mitigate by treating edge nodes as untrusted endpoints with signed updates and encrypted local storage, and by centralising the model and data governance so the fleet is one managed system, not a swarm of islands. The enterprises that scale edge AI profitably are the ones that budgeted for the fleet's whole life — update, observe, secure — before the first device shipped, and that is the number the board should see, not just the unit price.</p>"""),
],
"the-future-of-work-ai-augmented-decision-making": [
("division-of-labour","How Does AI Change the Division of Labour Between Humans and Systems?",
"""<h2 id="division-of-labour">How Does AI Change the Division of Labour Between Humans and Systems?</h2>
<p>AI does not replace the decision; it reshapes who does the preparatory work. The routine synthesis — gathering the data, building the comparison, surfacing the anomaly — moves from the human to the system, which means the human spends their attention on judgement, trade-offs, and accountability: the parts AI cannot own. The division that works is humans setting the frame and the values, AI supplying the evidence at the speed of the conversation, and humans making the call. That is augmentation, not substitution, and it is more productive than either alone.</p>
<p>The organisations that get this right redesign the workflow around the new split rather than bolting AI onto the old one. A monthly business review becomes a live session where leaders ask and the system answers, so the meeting is for deciding, not for waiting for a report. A front-line manager spends less time compiling and more time coaching. The risk is the inverse — a workforce that defers to the system's suggestion without the evidence to challenge it — which is why the human's role must include the right and the habit of interrogation. The future of work is not humans versus machines; it is humans with machines, where each does the part it is better at.</p>"""),
("decision-maker-skills","What Skills Do Decision-Makers Need in an AI-Augmented Workplace?",
"""<h2 id="decision-maker-skills">What Skills Do Decision-Makers Need in an AI-Augmented Workplace?</h2>
<p>The scarce skill becomes asking good questions and judging answers, not producing the analysis. A decision-maker who can frame the real question — what would change my mind, what is the downside, what does the data not show — gets far more from an AI system than one who accepts the first chart. That is a return to first principles: clarity about the decision, comfort with uncertainty, and the discipline to demand a sourced answer rather than a confident one.</p>
<p>The second skill is trust calibration — knowing when to delegate to the system and when to insist on human review, which depends on understanding where the model is reliable and where it is not. The third is leading a team that works with AI: setting norms so people use the system to think better, not to outsource thinking. Enterprises that invest in these human skills alongside the technology pull ahead, because the bottleneck stops being the data and becomes the quality of the judgement applied to it. The augmented workplace rewards the curious and the rigorous, and quietly exposes the passive — which is exactly why the skills question deserves a place on the leadership agenda.</p>"""),
],
"text-to-sql-accuracy-enterprise-trust": [
("testing-text-to-sql","How Should Enterprises Test Text-to-SQL Before Trusting It?",
"""<h2 id="testing-text-to-sql">How Should Enterprises Test Text-to-SQL Before Trusting It?</h2>
<p>Trust is earned by a test suite, not a demo. Before any user relies on a text-to-SQL system, build a labelled set of representative questions with the SQL you would accept and the answer you expect, covering the phrasings real people actually use — including the ambiguous and the malicious. Run every release against that set, and report pass rate by question type, not as a single number. The questions that reveal weakness are the ones with implicit dates, ambiguous entity names, and joins across domains, because that is where models guess.</p>
<p>Add a groundedness check at query time: the system should show the SQL it generated and the tables it touched, so a reviewer can confirm the logic before the answer is used in a decision. For high-stakes questions, require an approval step until confidence is proven. The enterprises that trust text-to-SQL did not lower their standards; they made the standards automatic — every answer checked against the test set's expectations and the semantic layer's definitions, with a clear path to a human when the system is unsure. Test it like production code, because for the business that is exactly what it is.</p>"""),
("semantic-layer-accuracy","What Role Does the Semantic Layer Play in Text-to-SQL Accuracy?",
"""<h2 id="semantic-layer-accuracy">What Role Does the Semantic Layer Play in Text-to-SQL Accuracy?</h2>
<p>The semantic layer is the difference between a query that runs and a query that means the right thing. Natural language is ambiguous — "revenue" can mean booked, recognised, or collected — and without a shared definition the model guesses from column names, which is where most errors originate. A semantic layer maps business terms to the exact tables, joins, and calculations they represent, so when a user says revenue the system knows which definition and which data to use, consistently, every time.</p>
<p>This is also what makes text-to-SQL trustworthy across an organisation rather than per-analyst. When the definition lives once in the semantic layer, finance, sales, and operations get the same answer to the same question, and a change to the definition propagates everywhere instead of hiding in one person's SQL. Combined with the test suite, the semantic layer turns text-to-SQL from a clever toy that occasionally lies into a dependable interface to the data — and dependability, not fluency, is what earns the enterprise trust that turns a question in chat into a decision made with confidence.</p>"""),
],
"2026-ai-budget-planning-enterprise-guide-nov2025": [
("budget-defend-explore","How Should AI Budget Be Allocated Between Defend and Explore?",
"""<h2 id="budget-defend-explore">How Should AI Budget Be Allocated Between Defend and Explore?</h2>
<p>Split the budget the way a sensible portfolio is split: the majority defends and extends what already works, a minority explores what might. The defend side funds the production systems delivering measurable margin, cycle time, or retention today — and the unglamorous work of keeping them accurate, governed, and adopted. The explore side funds a smaller set of bets on new moats: a novel model application, a new data source, an agentic workflow no competitor has. A common error is inverting the split, pouring most of the budget into speculative pilots while the systems actually paying for themselves starve for maintenance.</p>
<p>The allocation should be explicit and reviewed, not a line in a larger spreadsheet. Give the defend portfolio a clear ROI bar and the explore portfolio a clear learn-or-kill criterion at ninety days. The 2026 planning discipline is to fund outcomes, not activity: every dollar maps to a decision it is meant to improve, and the budget resets when the evidence does. Enterprises that allocate this way avoid both the pilot graveyard and the innovation theatre, and they can show the board exactly why each portion of spend exists and what it is on track to return.</p>"""),
("mid-year-reallocation","What Should Trigger a Mid-Year Reallocation of AI Spend?",
"""<h2 id="mid-year-reallocation">What Should Trigger a Mid-Year Reallocation of AI Spend?</h2>
<p>Reallocate when the evidence says the plan was wrong, which it often is. A defend initiative that has clearly hit its baseline and is compounding should get more to scale; one that has stalled should lose funding to something that is working. An explore bet that has learned its lesson — the market moved, the model disappointed, the use case was not real — should be killed cleanly rather than carried on hope. The trigger is the ninety-day review, taken seriously, not the annual budget cycle.</p>
<p>The second trigger is a shift in the external landscape: a new model capability, a competitor move, or a regulation that changes the calculus. The 2026 environment moves fast enough that a plan written in November can be obsolete by March, and the budgets that win are the ones with a reallocation mechanism built in rather than a fixed envelope defended by inertia. Make the rule simple — capital follows evidence, quarterly — and the budget becomes a steering instrument instead of a commitment device. Boards trust a plan that can be corrected more than one that is rigidly adhered to past the point of usefulness.</p>"""),
],
}

# zh prose: slug -> { "cn": [...], "tw": [...] } each item (h2id, h2text, html)
ZH = {
"china-ai-model-wave-conversational-bi-evolution-2026": {
"cn": [
("cn-evaluating-vendors","企业应如何评估中国的对话式BI厂商？",
"""<h2 id="cn-evaluating-vendors">企业应如何评估中国的对话式BI厂商？</h2>
<p>评估应从数据边界开始，而不是从演示开始。对任何对话式BI厂商来说，决定性的问题是：它的模型是从你实时、受权限控制的数据中作答，还是从一个在别处训练的通用云服务中作答。阿里巴巴、百度和智谱等国内模型在推理和中文理解上已逼近前沿实验室，但企业价值是由连接模型与受治理数据的那一层创造的，而非模型本身。一个无法展示行级权限控制、审计日志以及你所掌控的语义层的厂商，无论基准分数多高，都不应进入生产环境。</p>
<p>第二个维度是部署形态。受监管和对数据敏感的企业越来越要求私有化或本地部署，使专有数据永不离开边界。应具体询问厂商如何处理模型更新、提示词与结果如何留存，以及若更换供应商你的语义定义会怎样。在2026年赢得企业订单的厂商，是把客户的知识图谱和指标定义当作客户拥有的可移植资产，而非锁定手段。用分析师每周真实提出的三个问题做试点，对照人工基线衡量答案准确率，再作决定。</p>"""),
("cn-risks","采用国产模型有哪些风险与缓解措施？",
"""<h2 id="cn-risks">采用国产模型有哪些风险与缓解措施？</h2>
<p>主要风险是数据驻留、供应连续性和能力漂移。数据驻留通过部署架构解决：把推理与存储留在所需司法辖区内，优先选择有清晰私有部署方案的厂商。供应连续性很重要，因为模型格局变化很快；缓解办法是把模型与应用层分离，以便在不重建连接器和语义定义的情况下替换新模型。能力漂移是隐性风险——今天最先进的模型十八个月后可能沦为中游——因此一个能把查询按任务路由到最佳可用模型的抽象层，比把路线图押注在单一厂商上更持久。</p>
<p>这些风险都不构成不采用国产模型的理由；它们只说明应以对待任何关键依赖的同样治理方式来采用。从中国AI模型浪潮中获益最多的企业，是把本地模型当作高性价比、符合司法辖区的计算层，同时牢牢掌握自己的数据、定义和评估体系。这种组合——本地模型、自有语义、严格度量——才能把快速变动的模型市场转化为持久的解析优势，而非反复出现的采购难题。</p>"""),
],
"tw": [
("tw-evaluating-vendors","企業應如何評估中國的對話式BI廠商？",
"""<h2 id="tw-evaluating-vendors">企業應如何評估中國的對話式BI廠商？</h2>
<p>評估應從資料邊界開始，而不是從示範開始。對任何對話式BI廠商來說，決定性的問題是：它的模型是從你即時、受權限控制的資料中作答，還是從一個在別處訓練的通用雲端服務中作答。阿里巴巴、百度和智譜等國內模型在推理和中文理解上已逼近前沿實驗室，但企業價值是由連接模型與受治理資料的那一層創造的，而非模型本身。一個無法展示列級權限控制、稽核日誌以及你所掌控的語意層的廠商，無論基準分數多高，都不應進入生產環境。</p>
<p>第二個維度是部署形態。受監管與對資料敏感的企業越來越要求私有化或本地部署，使專有資料永不離開邊界。應具體詢問廠商如何處理模型更新、提示詞與結果如何留存，以及若更換供應商你的語意定義會怎樣。在2026年贏得企業訂單的廠商，是把客戶的知識圖譜和指標定義當作客戶擁有的可移植資產，而非鎖定手段。用分析師每週真實提出的三個問題做試點，對照人工基線衡量答案準確率，再作決定。</p>"""),
("tw-risks","採用國產模型有哪些風險與緩解措施？",
"""<h2 id="tw-risks">採用國產模型有哪些風險與緩解措施？</h2>
<p>主要風險是資料駐留、供應連續性和能力漂移。資料駐留透過部署架構解決：把推理與儲存留在所需司法管轄區內，優先選擇有清晰私有部署方案的廠商。供應連續性很重要，因為模型格局變化很快；緩解辦法是把模型與應用層分離，以便在不重建連接器和語意定義的情況下替換新模型。能力漂移是隱性風險——今天最先進的模型十八個月後可能淪為中遊——因此一個能把查詢按任務路由到最佳可用模型的抽象層，比把路線圖押注在單一廠商上更持久。</p>
<p>這些風險都不構成不採用國產模型的理由；它們只說明應以對待任何關鍵依賴的同樣治理方式來採用。從中國AI模型浪潮中獲益最多的企業，是把本地模型當作高性價比、符合司法管轄區的運算層，同時牢牢掌握自己的資料、定義和評估體系。這種組合——本地模型、自有語意、嚴格度量——才能把快速變動的模型市場轉化為持久的解析優勢，而非反覆出現的採購難題。</p>"""),
],
},
"competitive-advantage-through-ai": {
"cn": [
("cn-coe","企业应如何建立能持續優勢的AI卓越中心？",
"""<h2 id="cn-coe">企业应如何建立能持續優勢的AI卓越中心？</h2>
<p>卓越中心是把偶發洞察轉化為日常決策的機構載體。能夠複合優勢的組織，並非運行最多試點的組織，而是建立了一個受高層贊助的小團隊，負責跨職能的數據迴路、語意層與採用指標。卓越中心應刻意跨職能：擁有管線的數據工程師、擁有業務問題的分析翻譯者、擁有決策的領域主管，以及負責採用的變革主管。向擁有預算權的治理委員會報告，卓越中心的職責是讓下一個AI用例比上一個更便宜——透過復用連接器、復用指標定義、復用對話式介面，而非重新建造。</p>
<p>實務上卓越中心運作的是投資組合而非積壓清單。約七成產能用於守護既有護城河——定價、留存、供給配置——這些領域的速度與洞察直接改變競爭等式；其餘三成資助少數可能創造新護城河的賭注。區分卓越中心與研究實驗室的紀律是九十天價值週期：每項計畫都在真實用戶、真實資料上線，對照真實基線衡量，要麼融入平台，要麼退場。託管式對話層約兩週即可在現有系統上線，意味著卓越中心在第一次季審前就展現價值——而這份早期信譽，正是當懷疑者質疑「模型並非重點」時保護計畫的關鍵。</p>"""),
("cn-practice","AI競爭優勢在實務上長什麼樣？",
"""<h2 id="cn-practice">AI競爭優勢在實務上長什麼樣？</h2>
<p>想像一家區域零售商，其定價團隊過去每週重設促銷價格，在人工檢視上季售罄數據後才動作，而那份數據往往來不及發揮作用。在把對話層接入即時銷售點與庫存資料後，同一團隊每天早晨詢問哪些門市的哪些商品因缺貨或降價而流失毛利，並在數秒內得到有出處的答案。一季之內，定價的決策延遲從九天降至一天以內，僅在風險商品上挽回的毛利就抵銷了整個計畫成本。模型是大眾化的；優勢在於專有迴路——銷售點、庫存與定價決策每小時而非每月相互餵養。</p>
<p>再想像一家物流營運商，把對話式分析嵌入其調度工具。調度員不再把試算表匯出給中央團隊，而是直接在對話中詢問某條路線為何錯過時窗，答案根植於即時車況與天氣。結果不是更好的儀表板，而是誰能行動、行動多快的根本改變。這種模式——洞察抵達行動者、行動被記錄、結果回饋資料——就是護城河。這也解釋了為何從AI獲得顯著財務效益的約10%企業，並非以模型品質取勝，而是以專有資料轉化為唯有它們能做的決策之速度取勝。</p>"""),
],
"tw": [
("tw-coe","企業應如何建立能持續優勢的AI卓越中心？",
"""<h2 id="tw-coe">企業應如何建立能持續優勢的AI卓越中心？</h2>
<p>卓越中心是把偶發洞察轉化為日常決策的機構載體。能夠複合優勢的組織，並非運行最多試點的組織，而是建立了一個受高層贊助的小團隊，負責跨職能的資料迴路、語意層與採用指標。卓越中心應刻意跨職能：擁有管線的資料工程師、擁有業務問題的分析翻譯者、擁有決策的領域主管，以及負責採用的變革主管。向擁有預算權的治理委員會報告，卓越中心的職責是讓下一個AI用例比上一個更便宜——透過復用連接器、復用指標定義、復用對話式介面，而非重新建造。</p>
<p>實務上卓越中心運作的是投資組合而非積壓清單。約七成產能用於守護既有護城河——定價、留存、供給配置——這些領域的速度與洞察直接改變競爭等式；其餘三成資助少數可能創造新護城河的賭注。區分卓越中心與研究實驗室的紀律是九十天價值週期：每項計畫都在真實用戶、真實資料上線，對照真實基線衡量，要麼融入平台，要麼退場。託管式對話層約兩週即可在現有系統上線，意味著卓越中心在第一次季審前就展現價值——而這份早期信譽，正是當懷疑者質疑「模型並非重點」時保護計畫的關鍵。</p>"""),
("tw-practice","AI競爭優勢在實務上長什麼樣？",
"""<h2 id="tw-practice">AI競爭優勢在實務上長什麼樣？</h2>
<p>想像一家區域零售商，其定價團隊過去每週重設促銷價格，在人工檢視上季售罄數據後才動作，而那份數據往往來不及發揮作用。在把對話層接入即時銷售點與庫存資料後，同一團隊每天早晨詢問哪些門市的哪些商品因缺貨或降價而流失毛利，並在數秒內得到有出處的答案。一季之內，定價的決策延遲從九天降至一天以內，僅在風險商品上挽回的毛利就抵銷了整個計畫成本。模型是大眾化的；優勢在於專有迴路——銷售點、庫存與定價決策每小時而非每月相互餵養。</p>
<p>再想像一家物流營運商，把對話式分析嵌入其調度工具。調度員不再把試算表匯出給中央團隊，而是直接在對話中詢問某條路線為何錯過時窗，答案根植於即時車況與天氣。結果不是更好的儀表板，而是誰能行動、行動多快的根本改變。這種模式——洞察抵達行動者、行動被記錄、結果回饋資料——就是護城河。這也解釋了為何從AI獲得顯著財務效益的約10%企業，並非以模型品質取勝，而是以專有資料轉化為唯有它們能做的決策之速度取勝。</p>"""),
],
},
"agentic-workflows-enterprise-automation": {
"cn": [
("cn-measure","企业如何衡量智能体工作流是否真正奏效？",
"""<h2 id="cn-measure">企业如何衡量智能体工作流是否真正奏效？</h2>
<p>衡量工作流，而非模型。首要指標是從觸發到完成結果的週期時間，對照被取代的人工基線。若採購智能體過去要三天、現在四小時，這個差值就是價值；模型準確率若工作未能更快且正確地完成便毫無意義。把週期時間與兩個防護指標配對：例外率——智能體必須上報給人類的案件佔比——以及返工率，即被撤回或修正的智能體產出佔比。健康的計畫隨著智能體學習而壓低例外率，且不會悄悄把錯誤推進生產。</p>
<p>除了效率，還要衡量槓桿：一個智能體框架現在服務多少個不同的工作流，以及新增一個工作流有多便宜。智能體自動化的回報不在於一個聰明的機器人，而在於一個平台——其下一個自動化的邊際成本趨近於零。只追蹤成本節省的企業錯失了這點；同時追蹤工作流覆蓋率與新增自動化所需時間的企業，會發現複合效應——更多工作流、更低單位成本——才是策略價值所在。每週向贊助者報告，讓計畫由證據而非演示來引導。</p>"""),
("cn-guardrails","哪些治理防護欄能讓自主智能體保持安全？",
"""<h2 id="cn-guardrails">哪些治理防護欄能讓自主智能體保持安全？</h2>
<p>安全的自主是受限的自主。第一道防護欄是動作分類：智能體可自動執行低風險、可逆的動作，但任何不可逆的——付款、刪除記錄、聯繫客戶——都需人工核准步驟或嚴格的政策檢查。第二道是與人類使用者相同的權限邊界，在資料層強制執行，使智能體只看到其操作者可得看的內容。第三道是每個工具呼叫、決策與檢索來源的不可竄改稽核軌跡，以便事後重建任何結果。</p>
<p>第四道防護欄是終止開關設計：在行為看起來出錯時凍結智能體動作，而不影響其所依賴的系統。第五道是在生產中評估——影子運行與金絲雀部署，在智能體獲准行動前先将其提議動作與人類對照，直到建立信心。具備這五道防護欄的組織既快又安全；只靠提示詞與良好意願就部署智能體的組織，往往會以艱難方式學到：沒有邊界的自主只是無上限的風險。</p>"""),
],
"tw": [
("tw-measure","企業如何衡量智能體工作流是否真正奏效？",
"""<h2 id="tw-measure">企業如何衡量智能體工作流是否真正奏效？</h2>
<p>衡量工作流，而非模型。首要指標是從觸發到完成結果的週期時間，對照被取代的人工基線。若採購智能體過去要三天、現在四小時，這個差值就是價值；模型準確率若工作未能更快且正確地完成便毫無意義。把週期時間與兩個防護指標配對：例外率——智能體必須上報給人類的案件佔比——以及返工率，即被撤回或修正的智能體產出佔比。健康的計畫隨著智能體學習而壓低例外率，且不會悄悄把錯誤推進生產。</p>
<p>除了效率，還要衡量槓桿：一個智能體框架現在服務多少個不同的工作流，以及新增一個工作流有多便宜。智能體自動化的回報不在於一個聰明的機器人，而在於一個平台——其下一個自動化的邊際成本趨近於零。只追蹤成本節省的企業錯失了這點；同時追蹤工作流覆蓋率與新增自動化所需時間的企業，會發現複合效應——更多工作流、更低單位成本——才是策略價值所在。每週向贊助者報告，讓計畫由證據而非示範來引導。</p>"""),
("tw-guardrails","哪些治理防護欄能讓自主智能體保持安全？",
"""<h2 id="tw-guardrails">哪些治理防護欄能讓自主智能體保持安全？</h2>
<p>安全的自主是受限的自主。第一道防護欄是動作分類：智能體可自動執行低風險、可逆的動作，但任何不可逆的——付款、刪除記錄、聯繫客戶——都需人工核准步驟或嚴格的政策檢查。第二道是與人類使用者相同的權限邊界，在資料層強制執行，使智能體只看到其操作者可得看的內容。第三道是每個工具呼叫、決策與檢索來源的不可竄改稽核軌跡，以便事後重建任何結果。</p>
<p>第四道防護欄是終止開關設計：在行為看起來出錯時凍結智能體動作，而不影響其所依賴的系統。第五道是在生產中評估——影子運行與金絲雀部署，在智能體獲准行動前先將其提議動作與人類對照，直到建立信心。具備這五道防護欄的組織既快又安全；只靠提示詞與良好意願就部署智能體的組織，往往會以艱難方式學到：沒有邊界的自主只是無上限的風險。</p>"""),
],
},
"why-edge-ai-manufacturing-logistics-energy": {
"cn": [
("cn-business-case","企业如何向董事会论证边缘AI投资？",
"""<h2 id="cn-business-case">企业如何向董事会论证边缘AI投资？</h2>
<p>边缘AI的董事会論證關乎延遲、連續性與資料成本——這三項雲端在工廠現場或偏遠站點都無法完全解決。延遲：必須在毫秒內完成的產線缺陷檢測，無法等待與區域的來回傳輸。連續性：網路中斷時，依賴雲端的流程會停止，而邊緣模型讓產線持續運轉。資料成本：把每筆感測器讀數送往雲端既昂貴又往往不必要，因為決策可在資料誕生之處完成。</p>
<p>論證應以用例為導向，而非技術為導向。選一個停線、漏檢或缺貨調度會花真金白銀的流程，展示把推論移到邊緣的回收期。製造業是在線檢測；物流業是場站的路線與裝載最佳化；能源業是遠離連線資產的預測性維護。先把投資框定為風險降低與毛利保護，其次才是產能擴張。當替代方案——無法自我檢測的產線、連結中斷就失明的站點——是更昂貴的選項時，董事會才會資助邊緣AI，而在重工業中它通常就是。</p>"""),
("cn-hidden-costs","边缘AI部署有哪些隐性成本？",
"""<h2 id="cn-hidden-costs">边缘AI部署有哪些隐性成本？</h2>
<p>可見成本是硬體；隱性成本是生命週期。數百個邊緣裝置意味數百個需更新、監控與修補的模型，且往往位於沒有IT人員、連線間斷之處。若未設計空中更新、健康遙測與優雅降級，邊緣機群會變成維運負債，填滿它原本要防止的停機。第二項隱性成本是資料漂移：在一個站點條件訓練的邊緣模型可能誤讀另一個站點，而沒有集中監控，你直到廢料上升才會發現。</p>
<p>第三項是實體邊緣的安全，裝置比受保護的資料中心更容易被竄改。緩解方式是把邊緣節點當作不可信端點，採用簽署更新與加密本地儲存，並集中管理模型與資料治理，使機群成為一個受管系統而非孤島。能獲利擴展邊緣AI的企業，是在首台裝置出貨前就為機群整個生命週期——更新、觀察、保全——編列預算，而這正是董事會該看到的數字，而非僅是單價。</p>"""),
],
"tw": [
("tw-business-case","企業如何向董事會論證邊緣AI投資？",
"""<h2 id="tw-business-case">企業如何向董事會論證邊緣AI投資？</h2>
<p>邊緣AI的董事會論證關乎延遲、連續性與資料成本——這三項雲端在工廠現場或偏遠站點都無法完全解決。延遲：必須在毫秒內完成的產線缺陷檢測，無法等待與區域的來回傳輸。連續性：網路中斷時，依賴雲端的流程會停止，而邊緣模型讓產線持續運轉。資料成本：把每筆感測器讀數送往雲端既昂貴又往往不必要，因為決策可在資料誕生之處完成。</p>
<p>論證應以用例為導向，而非技術為導向。選一個停線、漏檢或缺貨調度會花真金白銀的流程，展示把推論移到邊緣的回收期。製造業是在線檢測；物流業是場站的路線與裝載最佳化；能源業是遠離連線資產的預測性維護。先把投資框定為風險降低與毛利保護，其次才是產能擴張。當替代方案——無法自我檢測的產線、連結中斷就失明的站點——是更昂貴的選項時，董事會才會資助邊緣AI，而在重工業中它通常就是。</p>"""),
("tw-hidden-costs","邊緣AI部署有哪些隱性成本？",
"""<h2 id="tw-hidden-costs">邊緣AI部署有哪些隱性成本？</h2>
<p>可見成本是硬體；隱性成本是生命週期。數百個邊緣裝置意味數百個需更新、監控與修補的模型，且往往位於沒有IT人員、連線間斷之處。若未設計空中更新、健康遙測與優雅降級，邊緣機群會變成維運負債，填滿它原本要防止的停機。第二項隱性成本是資料漂移：在一個站點條件訓練的邊緣模型可能誤讀另一個站點，而沒有集中監控，你直到廢料上升才會發現。</p>
<p>第三項是實體邊緣的安全，裝置比受保護的資料中心更容易被竄改。緩解方式是把邊緣節點當作不可信端點，採用簽署更新與加密本地儲存，並集中管理模型與資料治理，使機群成為一個受管系統而非孤島。能獲利擴展邊緣AI的企業，是在首台裝置出貨前就為機群整個生命週期——更新、觀察、保全——編列預算，而這正是董事會該看到的數字，而非僅是單價。</p>"""),
],
},
"text-to-sql-accuracy-enterprise-trust": {
"cn": [
("cn-testing","企业应在信任Text-to-SQL前如何测试它？",
"""<h2 id="cn-testing">企业应在信任Text-to-SQL前如何测试它？</h2>
<p>信任由測試套件贏得，而非演示。在任何使用者依賴text-to-SQL系統前，先建立一組帶標記的代表性問題，附上你可接受的SQL與預期答案，涵蓋人們實際使用的說法——包括模糊與惡意的。每次發佈都對這組執行，並按問題類型而非單一數字報告通過率。暴露弱點的是那些含隱含日期、實體名稱模糊、跨領域連接的問題，因為那正是模型猜測之處。</p>
<p>在查詢時加入依據性檢查：系統應展示它生成的SQL與觸及的資料表，以便審核者在答案用於決策前確認邏輯。對高風險問題，在證明信心前要求核准步驟。信任text-to-SQL的企業並未降低標準；他們把標準自動化——每個答案都對照測試集預期與語意層定義檢查，並在系統不確定時有明確通往人類的路徑。像生產程式碼一樣測試它，因為對業務而言它正是如此。</p>"""),
("cn-semantic","语义层在Text-to-SQL准确性中扮演什么角色？",
"""<h2 id="cn-semantic">语义层在Text-to-SQL准确性中扮演什么角色？</h2>
<p>語意層是查詢「能跑」與「意義正確」之間的區別。自然語言是模糊的——「營收」可能指已下單、已認列或已收款——沒有共享定義，模型就從欄位名稱猜測，多數錯誤由此而生。語意層把業務術語對應到確切的資料表、連接與計算，因此當使用者說營收，系統知道用哪個定義、哪些資料，且每次一致。</p>
<p>這也是text-to-SQL在整個組織可信、而非僅止於單一分析師的原因。當定義只存在語意層一次，財務、業務與營運對同一問題得到相同答案，而定義的變更會傳播到各處，而非藏在某个人的SQL裡。結合測試套件，語意層把text-to-SQL從偶爾說謊的聰明玩具，變成可依賴的資料介面——而可依賴，而非流暢，才是為企業贏得信任、把對話中的提問轉化為有信心做出的決策的關鍵。</p>"""),
],
"tw": [
("tw-testing","企業應在信任Text-to-SQL前如何測試它？",
"""<h2 id="tw-testing">企業應在信任Text-to-SQL前如何測試它？</h2>
<p>信任由測試套件贏得，而非示範。在任何使用者依賴text-to-SQL系統前，先建立一組帶標記的代表性問題，附上你可接受的SQL與預期答案，涵蓋人們實際使用的說法——包括模糊與惡意的。每次發佈都對這組執行，並按問題類型而非單一數字報告通過率。暴露弱點的是那些含隱含日期、實體名稱模糊、跨領域連接的問題，因為那正是模型猜測之處。</p>
<p>在查詢時加入依據性檢查：系統應展示它生成的SQL與觸及的資料表，以便審核者在答案用於決策前確認邏輯。對高風險問題，在證明信心前要求核准步驟。信任text-to-SQL的企業並未降低標準；他們把標準自動化——每個答案都對照測試集預期與語意層定義檢查，並在系統不確定時有明確通往人類的路徑。像生產程式碼一樣測試它，因為對業務而言它正是如此。</p>"""),
("tw-semantic","語意層在Text-to-SQL準確性中扮演什麼角色？",
"""<h2 id="tw-semantic">語意層在Text-to-SQL準確性中扮演什麼角色？</h2>
<p>語意層是查詢「能跑」與「意義正確」之間的區別。自然語言是模糊的——「營收」可能指已下單、已認列或已收款——沒有共享定義，模型就從欄位名稱猜測，多數錯誤由此而生。語意層把業務術語對應到確切的資料表、連接與計算，因此當使用者說營收，系統知道用哪個定義、哪些資料，且每次一致。</p>
<p>這也是text-to-SQL在整個組織可信、而非僅止於單一分析師的原因。當定義只存在語意層一次，財務、業務與營運對同一問題得到相同答案，而定義的變更會傳播到各處，而非藏在某個人的SQL裡。結合測試套件，語意層把text-to-SQL從偶爾說謊的聰明玩具，變成可依賴的資料介面——而可依賴，而非流暢，才是為企業贏得信任、把對話中的提問轉化為有信心做出的決策的關鍵。</p>"""),
],
},
}

def insert_prose(html, items):
    # choose anchor
    if '<section class="faq-section"' in html:
        anchor = '<section class="faq-section"'
        idx = html.index(anchor)
        # insert before the line start of anchor (keep indentation simple: put block then newline then anchor)
        pre = html[:idx]
        post = html[idx:]
        block = "\n".join(items) + "\n"
        return pre + block + post
    else:
        anchor = '<nav class="article-nav"'
        idx = html.index(anchor)
        pre = html[:idx]
        post = html[idx:]
        block = "\n".join(items) + "\n"
        return pre + block + post

for slug, items in EN.items():
    fn = os.path.join(BASE, "blog/articles", slug + ".html")
    html = open(fn, encoding="utf-8").read()
    head0 = html[:html.index("<body")]
    # only insert if not already inserted (check marker)
    if "id=\"choosing-streaming-patterns\"" in html or "id=\"cn-evaluating-vendors\"" in html:
        print("SKIP (already has prose):", slug)
        continue
    new = insert_prose(html, [it[2] for it in items])
    # validate head unchanged
    assert new[:new.index("<body")] == head0, "HEAD CHANGED "+slug
    assert "?v=20260826" in new
    open(fn, "w", encoding="utf-8").write(new)
    print("EN prose inserted:", slug)

for slug, langs in ZH.items():
    for lg, items in langs.items():
        sub = "zh-cn/blog/articles" if lg=="cn" else "zh-tw/blog/articles"
        fn = os.path.join(BASE, sub, slug + ".html")
        html = open(fn, encoding="utf-8").read()
        head0 = html[:html.index("<body")]
        marker = items[0][0]
        if ('id="%s"'%marker) in html:
            print("SKIP (already has prose):", slug, lg)
            continue
        new = insert_prose(html, [it[2] for it in items])
        assert new[:new.index("<body")] == head0, "HEAD CHANGED "+slug+" "+lg
        assert "?v=20260826" in new
        open(fn, "w", encoding="utf-8").write(new)
        print("ZH prose inserted:", slug, lg)
print("DONE phase1 prose")
