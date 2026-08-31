#!/usr/bin/env python3
"""EN body expansion, batch 4 (final 5 slugs)."""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb002_lib import apply_ops

DATA = {}

DATA['ai-conversational-analytics-energy-sector-optimization'] = dict(before='Frequently Asked Questions', inserts=[
    ("Which Energy Use Cases Deliver Value First?", """
<p>Conversational analytics earns its place in energy operations where questions are frequent, answers are time-sensitive, and the person asking cannot wait for an analyst. Five use cases consistently clear that bar.</p>
<p><strong>Outage and asset performance review.</strong> "Which feeders had the most unplanned outages last quarter, and what did the maintenance history say?" Today this is a multi-day request spanning the historian, the asset management system, and spreadsheets. In natural language it is a question answered in minutes, and the answer includes the maintenance context that explains the pattern.</p>
<p><strong>Emissions and sustainability reporting.</strong> Reporting teams spend weeks reconciling data from plants, fleets, and purchased-energy records against multiple disclosure frameworks. A governed semantic layer with a natural-language interface turns a recurring reconciliation exercise into a query, and leaves an audit trail of how each figure was derived.</p>
<p><strong>Trading and scheduling support.</strong> "What was our realised margin on the day-ahead position last week, split by unit?" Traders need this during the day, not at month-end. The constraint is governance: trading data requires strict role-based access, which is why this use case only works on a platform that enforces permissions at query time.</p>
<p><strong>Procurement and fuel mix analysis.</strong> Comparing delivered cost, calorific value, and emissions intensity across suppliers and periods is exactly the kind of multi-source question that defeats dashboards and suits a conversational interface.</p>
<p><strong>Regulatory response.</strong> When a regulator asks a specific question with a deadline, the ability to answer from governed data in hours rather than weeks is a measurable reduction in exposure &mdash; and it is the use case that most often justifies the programme to a board.</p>
<p>The sequencing principle: start where the data is already governed and the question is already asked frequently. It is the frequency of the question, not the sophistication of the analytics, that determines adoption.</p>
"""),
    ("How Do You Integrate Conversational Analytics With SCADA and Historian Data?", """
<p>The integration question is where energy AI projects are won or lost, because operational technology was never designed for analytics access.</p>
<p><strong>Never query the historian directly.</strong> Historians are optimised for high-frequency writes and time-series retrieval; they are not a semantic layer, they do not know what a "unit" or an "outage" is, and exposing them to an analytics workload risks operational availability. Replicate into an analytics store on a defined cadence &mdash; near-real-time for operational metrics, hourly or daily for reporting &mdash; and query the replica.</p>
<p><strong>Build the semantic layer before the interface.</strong> The reason generic analytics tools fail in energy is that tag names carry the meaning. A tag like <code>UNIT3_GT_AUX_PWR</code> means something to the engineer who named it and nothing to a plant manager. Map tags to business concepts &mdash; unit, asset class, fuel type, operating state, emissions scope &mdash; and the natural-language interface becomes possible. This mapping is the majority of the work and the source of most of the value.</p>
<p><strong>Handle operational context explicitly.</strong> A value from a historian is meaningless without the state of the asset at the time: was the unit running, in startup, or offline? Encode operating state, load band, and ambient conditions as first-class dimensions, otherwise the model will compare incomparable periods and produce confident nonsense.</p>
<p><strong>Respect the network boundary.</strong> Replication should be one-directional, from OT to the analytics environment, through a controlled interface. No analytics component should ever be able to write to an operational system. This is a safety requirement, not an IT preference, and it is the first thing an operational-technology reviewer will check.</p>
<p><strong>Plan for tag churn.</strong> Tags get renamed, units get re-instrumented, and historians get migrated. Build the mapping as versioned metadata with alerts when upstream tags disappear, because silent breakage in a semantic layer produces wrong answers rather than errors.</p>
"""),
    ("What Does a Governed Energy Data Architecture Look Like?", """
<p>Governance in energy is not a compliance overlay; it is what makes operational and trading data usable by anyone beyond the team that owns it. Four layers, in order.</p>
<p><strong>Source and replication layer.</strong> Historians, SCADA replicas, ETRM and trading systems, asset management, ERP, and market feeds, landed in an analytics store with lineage recorded from the point of ingestion.</p>
<p><strong>Semantic layer.</strong> The business definitions: what counts as availability, how forced outage hours are calculated, how emissions intensity is normalised, which cost allocation applies to which unit. This layer must be owned &mdash; by a named person or team &mdash; and changes to it must be versioned. Without it, every team computes its own numbers and no two reports agree.</p>
<p><strong>Access and policy layer.</strong> Role-based access enforced at query time, with separation between trading, operations, and commercial data. Analysts and traders see different things even when asking the same question, and the enforcement happens in the platform rather than in the application's UI.</p>
<p><strong>Interface layer.</strong> Natural language on top, with every question and answer logged &mdash; who asked, what data was touched, what was returned. That log is simultaneously the audit trail, the adoption metric, and the source of the evaluation set that improves the system.</p>
<p>The architecture choice that matters most is the middle one. Organisations that build the semantic layer well can change models, interfaces, and vendors without rebuilding anything. Those that skip it rebuild every time.</p>
"""),
])

DATA['ai-copyright-infringement-training-data-legal'] = dict(before='__FAQ__', inserts=[
    ("What Does Data Provenance Actually Require?", """
<p>"We documented our datasets" is not provenance. Provenance means that for any training corpus, you can answer four questions without a research project: where did it come from, what licence or legal basis applies, when was it acquired, and what has it been used for since.</p>
<p><strong>Where it came from.</strong> Record the source URL or provider, the retrieval method, the retrieval date, and the entity that retrieved it. Scraped web data needs the crawl scope and the robots.txt state at the time. Purchased data needs the contract reference. Internal data needs the originating system and its own retention constraints.</p>
<p><strong>What licence or legal basis applies.</strong> For each source: public domain, permissive licence, restrictive licence with conditions, licence-by-contract, or reliance on an exception such as text and data mining. Crucially, record the <strong>reservations</strong> &mdash; opt-outs, robots directives, and terms-of-service restrictions &mdash; because under regimes like EU Article 4, a valid opt-out changes the legal position regardless of what the licence would otherwise permit.</p>
<p><strong>When it was acquired.</strong> Legal position is time-dependent: a work that was permissively licensed when collected may not be today, and an opt-out posted after collection may or may not bind you. Acquisition dates are the evidence that resolves this, and they are the field most often missing from dataset registries.</p>
<p><strong>What it has been used for.</strong> Which model versions were trained on which corpora, and which of those models are in production. This is the question that determines your exposure when a claim arrives, and it is unanswerable without lineage between corpus and model version.</p>
<p>Store all four in a registry that is queryable and version-controlled. A spreadsheet maintained by one person is a registry that will not survive the first serious request &mdash; and the request always arrives with a deadline.</p>
"""),
    ("How Should Enterprises Handle Open-Source and Scraped Data?", """
<p>Open-source and scraped corpora are the two highest-volume and highest-risk categories in most training pipelines, and they need opposite treatment.</p>
<p><strong>Open-source and permissively licensed data.</strong> The risk is rarely the licence text; it is attribution and downstream conditions. Build an automated licence-normalisation step that maps each dataset's declared licence to a canonical identifier, flags conditions &mdash; attribution, share-alike, non-commercial &mdash; and blocks ingestion when a condition conflicts with your use. The common failure is inheriting a dataset whose licence chain is incomplete: a permissively licensed wrapper around restrictively licensed content. Verify recursively where the volume is material.</p>
<p><strong>Scraped data.</strong> Three controls. First, respect robots.txt and terms-of-service restrictions, and retain the evidence that you did &mdash; including the state of those files at crawl time, since they change. Second, honour opt-out mechanisms: in the EU, Article 4 text-and-data-mining reservations must be checked before use, and equivalent or emerging mechanisms exist elsewhere. Third, filter for known restricted sets: paywalled content, member-only repositories, and datasets published with explicit no-training notices.</p>
<p><strong>Practical mitigation.</strong> Where the provenance of a corpus cannot be established, the choices are to exclude it or to document the residual risk and get a decision recorded at an appropriate level. What is not acceptable is silence: unassessed corpora are the ones that produce surprises, and a recorded risk decision is defensible in a way that an unexamined one is not.</p>
<p>Finally, keep the exclusion list. The set of sources you decided not to use, and why, is one of the most persuasive artefacts you can produce when someone asks whether you took this seriously.</p>
"""),
    ("What Happens When a Copyright Claim Arrives?", """
<p>Preparation determines the cost of a claim far more than the merits do. Enterprises that have done the provenance work respond in days; those that have not spend months reconstructing their own history, usually under a deadline.</p>
<p><strong>Step 1 &mdash; identify exposure.</strong> Query the corpus-to-model lineage: which models were trained on the disputed material, which versions are in production, and which products or features depend on them. If this takes more than a day, that is the finding to fix afterwards.</p>
<p><strong>Step 2 &mdash; preserve evidence, do not clean up.</strong> Issue a litigation hold over the relevant datasets, model versions, training logs, and the provenance records. Deleting material after notice converts a manageable claim into a much worse one, and this is the step most often got wrong in the first 48 hours.</p>
<p><strong>Step 3 &mdash; assess the licence position.</strong> Retrieve the recorded licence, acquisition date, and any opt-out state. The answer here usually determines whether the matter resolves quickly or not.</p>
<p><strong>Step 4 &mdash; evaluate remediation options.</strong> Depending on exposure: retrain without the corpus, remove the affected model version from production, licence the content retroactively, or defend the position. Cost of retraining is the practical constraint, which is why model-level lineage pays for itself &mdash; retraining one model is a project; retraining everything is a programme.</p>
<p><strong>Step 5 &mdash; close the loop.</strong> Update the registry, the exclusion list, and the intake controls so the same corpus cannot be ingested again. Claims that do not produce a control change tend to recur.</p>
"""),
])

DATA['ai-cost-optimization-strategies'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("How Do You Route Work to the Right Model Size?", """
<p>Model routing is the single largest lever on inference spend, and most organisations leave it entirely on the table because they treat model choice as a per-application decision made once at build time.</p>
<p><strong>Classify tasks by capability requirement, not by team.</strong> Most enterprise AI work falls into four tiers. Extraction and classification &mdash; pulling fields from documents, routing tickets, labelling content &mdash; needs a small model. Summarisation and rewriting needs a mid-sized one. Multi-step reasoning over retrieved context needs a larger model. Genuine open-ended analysis needs a frontier model. In a typical enterprise portfolio, more than half of requests fall in the first two tiers.</p>
<p><strong>Route dynamically at request time.</strong> A router classifies each incoming request and sends it to the smallest model that will clear the quality bar for that task. Implemented well, this cuts blended cost per request substantially without a measurable quality change, because the expensive model is reserved for the minority of requests that need it.</p>
<p><strong>Use escalation, not just routing.</strong> Send the request to the small model first, evaluate confidence or run a lightweight verifier, and escalate to the larger model only when the result is uncertain. This is cheaper than routing everything to a large model and more reliable than never escalating.</p>
<p><strong>Measure quality per tier, separately.</strong> Routing fails when quality is measured in aggregate: a blended accuracy figure hides the fact that one tier is degrading. Track accuracy per task tier against an explicit threshold, and alert when a tier crosses it.</p>
<p><strong>Re-evaluate quarterly.</strong> Model pricing and capability move quickly; a routing table built twelve months ago is almost certainly wrong. Keep the evaluation set stable so the comparison is meaningful, and re-run it against new models on a fixed cadence.</p>
"""),
    ("Where Do Hidden AI Costs Accumulate?", """
<p>The visible line &mdash; token spend &mdash; is usually the smaller half of the bill. Five hidden costs account for most of the budget surprises enterprises report.</p>
<p><strong>Agentic multiplication.</strong> A single user request that triggers a planning step, three tool calls, a retrieval step, and a synthesis step can consume an order of magnitude more tokens than the request itself. Without per-trace cost attribution, this is invisible until the invoice arrives.</p>
<p><strong>Development and evaluation traffic.</strong> Teams testing against production endpoints with production-sized prompts generate meaningful spend that no business case accounted for. Separate development, staging, and production budgets, and meter them independently.</p>
<p><strong>Duplicated retrieval and embedding.</strong> Three teams embedding the same corpus three times, rebuilding indexes on every deployment, and re-embedding documents that have not changed. Shared embedding and retrieval infrastructure eliminates this, and it is one of the strongest arguments for a central platform rather than per-team builds.</p>
<p><strong>Idle provisioned capacity.</strong> Reserved GPU or endpoint capacity bought for a peak that occurs two days a month. Track utilisation against commitment and right-size on a quarterly cycle.</p>
<p><strong>Rework from ungoverned data.</strong> The largest hidden cost of all: teams rebuilding pipelines, cleaning data, and reconciling definitions because no shared semantic layer exists. It shows up as salaries and delay rather than as an AI invoice, which is exactly why it survives cost reviews.</p>
<p>The control that catches all five is per-use-case unit economics: cost per request, per decision, or per outcome, attributed to a business owner. Once someone's name is next to a number, the number starts to improve.</p>
"""),
])

DATA['ai-cost-optimization-strategies-enterprise'] = dict(before='Frequently asked questions', inserts=[
    ("What Does AI Spend Look Like Before and After Discipline?", """
<p>The pattern is consistent enough to be a diagnostic. Consider a mid-sized enterprise running twelve AI use cases with no central cost governance.</p>
<p><strong>Before.</strong> Monthly inference spend is roughly $180,000 and growing 15% quarter on quarter. Nobody can attribute it to a use case. Four business units hold separate vendor accounts. Two use cases account for most of the volume, but which two is a matter of opinion. Prompts average 4,000 tokens because nobody has revisited them since launch. An agentic workflow in one unit makes eleven model calls per request. Evaluation and development traffic runs through production endpoints. The finance team sees a single line item labelled "AI" and no way to forecast it.</p>
<p><strong>After two quarters of discipline.</strong> Instrumentation attributes every call to a use case and an owner, which immediately reveals that 60% of spend sits in two workflows. Routing sends extraction and classification &mdash; about half of all requests &mdash; to small models, cutting blended cost per request by roughly half. Prompt and context trimming removes a third of input tokens with no quality change, verified against a held-out evaluation set. Caching eliminates a large share of repeated queries. The agentic workflow is restructured to make four calls instead of eleven. Development traffic moves to a separate metered budget. Shared embedding infrastructure removes three duplicate pipelines.</p>
<p><strong>Result.</strong> Spend of roughly $85,000 per month serving materially more volume, with unit cost per request down by more than half and a forecast finance can actually use. No use case was cancelled, and no quality threshold was breached &mdash; which is the point. The savings came from removing waste, not from doing less.</p>
<p>The generalisable lesson: the first two quarters of AI cost work are almost entirely instrumentation and routing. The sophisticated optimisations matter later, and are worthless without the measurements that come first.</p>
"""),
    ("How Do You Build a Business Case for AI Cost Governance?", """
<p>Cost governance programmes compete for funding against revenue-generating initiatives, and they lose when they are framed as cost cutting. Three framings work better.</p>
<p><strong>Fund the next use case.</strong> The most persuasive argument is not "we will spend less"; it is "the recoverable spend in the current portfolio funds the next three use cases without new budget". For a leadership team under pressure to show AI progress, this converts a cost conversation into a capacity conversation.</p>
<p><strong>Frame it as risk reduction.</strong> Unattributed AI spend is an uncontrolled financial exposure: finance cannot forecast it, procurement cannot consolidate it, and shadow AI creates contractual and data-protection risk that has nothing to do with the amount. Governance closes all three, and the audit and compliance angle is often what secures the sponsor.</p>
<p><strong>Quantify with a two-week diagnostic rather than an estimate.</strong> Instrument the top five workflows, measure current unit cost, and identify the recoverable share. A diagnostic that shows 30&ndash;40% recoverable spend, measured rather than assumed, is a far stronger case than a benchmark slide.</p>
<p>Then structure the programme itself cheaply. The first phase is instrumentation and reporting &mdash; typically weeks, not quarters, and requiring no platform purchase. Fund the remediation from the savings it identifies, and the programme becomes self-financing after the first cycle. That is the version that gets approved.</p>
"""),
    ("Which Metrics Belong on an AI Cost Dashboard?", """
<p>A cost dashboard that shows only total spend produces the wrong behaviour: teams cut usage rather than waste. Six metrics, reported per use case and per owner, produce the right behaviour.</p>
<p><strong>Cost per unit of value</strong> &mdash; cost per answered question, per processed claim, per generated and accepted output. This is the headline metric, because it is the only one that connects spend to what the business gets.</p>
<p><strong>Requests and cost by model tier.</strong> Shows whether routing is working: if most requests still go to the largest tier, the lever is untouched.</p>
<p><strong>Input tokens per request.</strong> The fastest-moving indicator of prompt and context bloat. A rising trend here is almost always fixable.</p>
<p><strong>Cache hit rate.</strong> Low hit rates on repetitive workloads indicate free savings.</p>
<p><strong>Development versus production split.</strong> Development traffic above roughly 15% of total usually means testing is running against production endpoints.</p>
<p><strong>Cost trend against volume trend.</strong> If volume is flat and cost is rising, something has changed in the pipeline &mdash; a model swap, a prompt change, a new agent step. This is the metric that catches regressions nobody intended.</p>
<p>Report all six monthly to the use-case owners, not only to finance. Cost becomes manageable at the point where the person who can change it is the person who sees it.</p>
"""),
])

DATA['ai-credit-scoring-alternative-data'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("How Do You Validate an Alternative Data Source Before Buying It?", """
<p>Alternative data vendors sell predictive power, and the claims are difficult to verify before purchase. A structured validation prevents the most common expensive mistake: buying a signal that predicts something you already know.</p>
<p><strong>Ask for a backtest on your population, not theirs.</strong> Vendor performance measured on a different portfolio tells you very little. Provide a masked historical sample &mdash; applications, decisions, and realised outcomes &mdash; and require the vendor to return performance measured on it. If they will not, that is the answer.</p>
<p><strong>Measure incremental lift over your existing model.</strong> This is the test that matters. A data source with strong standalone predictive power often adds nothing once bureau data and internal history are already in the model. Compute the change in AUC or KS, and more importantly the change in approval rate at constant loss. If the lift is inside the noise band, do not buy it.</p>
<p><strong>Test stability across vintages and segments.</strong> A signal that works in one quarter and degrades in the next is a monitoring liability. Require performance broken out by period and by segment, and check specifically for degradation among the thin-file population the data is supposed to help &mdash; that group is often where the evidence is weakest.</p>
<p><strong>Check coverage before accuracy.</strong> A source that predicts well for 20% of applicants has a much lower ceiling than one that predicts adequately for 80%. Coverage is usually the constraint, and it is the first thing to establish.</p>
<p><strong>Verify the compliance position.</strong> Source of the data, consent basis, permissible-purpose status, and whether the vendor can support adverse-action reason codes. A signal you cannot explain to a regulator is a signal you cannot deploy, regardless of its lift.</p>
"""),
    ("What Does Fair Lending Compliance Require for Alternative-Data Models?", """
<p>Alternative data expands access and expands scrutiny at the same time. Regulators are not hostile to it; they are hostile to unexplained decisions and to proxies that recreate protected-class effects through other variables.</p>
<p><strong>Document the business justification for every feature.</strong> Each variable needs a written rationale connecting it to creditworthiness &mdash; not just to predictive performance. A feature that predicts well but has no plausible causal link to repayment is a liability, particularly if it correlates with a protected characteristic.</p>
<p><strong>Test for disparate impact, explicitly.</strong> Run the analysis on approval rates and on pricing by protected-class proxy where permitted, using the same methodology you would apply to a traditional model. Where a disparity appears, the question you must be able to answer is whether a less discriminatory alternative exists that achieves the same business objective &mdash; so test those alternatives before you need the answer.</p>
<p><strong>Solve adverse-action reasoning before deployment.</strong> Complex models make reason codes hard. If you cannot generate a specific, accurate principal reason for a decline, you cannot deploy the model in a regulated lending decision. Plan for this in model design &mdash; constrain the feature set, or use a surrogate model for reason generation &mdash; rather than discovering it at launch.</p>
<p><strong>Monitor continuously, not annually.</strong> Alternative data drifts faster than bureau data because the underlying services and behaviours change. Set thresholds on both model performance and fairness metrics, alert on breach, and keep a documented governance record of every review.</p>
<p><strong>Keep the human accountable.</strong> Fully automated adverse decisions on thin-file applicants attract the most attention. A documented review path for declines near the cut-off, and for overrides, is both a compliance control and a practical source of the outcome data that improves the model.</p>
"""),
])

if __name__ == '__main__':
    for slug, d in DATA.items():
        changed = apply_ops(slug, 'en', inserts=d['inserts'], before=d['before'])
        print(('inserted ' if changed else 'noop     ') + slug)
