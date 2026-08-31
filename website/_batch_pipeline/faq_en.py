import sys, json
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline")
from lib import *

SVG_SEC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
SVG_CHEV = '<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>'

def build_faq(qa):
    items=""
    for i,(q,a) in enumerate(qa,1):
        items+=f'''                    <div class="faq-item">
                        <button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">{i}</span><span>{i} {q}</span></span>
                            {SVG_CHEV}
                        </button>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{a}</div></div>
                    </div>
'''
    return f'''            <section class="faq-section" id="faq" aria-label="Frequently Asked Questions">
                <h2 class="faq-section-title">
                    {SVG_SEC}
                    Frequently Asked Questions
                </h2>
                <div class="faq-list">
{items}                </div>
            </section>
'''

def build_jsonld(qa):
    ents=[{"@type":"Question","name":f"{i} {q}","acceptedAnswer":{"@type":"Answer","text":a}} for i,(q,a) in enumerate(qa,1)]
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":ents}, ensure_ascii=False)

EXTRA = {
"data-quality-at-scale-monitoring-alerting-remediation": '''
<h2 id="how-do-you-prove-data-quality-investment-pays-off">How Do You Prove Data Quality Investment Pays Off?</h2>
<p>The proof is in the incidents that did not happen. Track the volume of data defects reaching consumers quarter over quarter, the mean-time-to-detection on the ones that occur, and the share of critical datasets with a named owner and a current quality score. As monitoring and remediation mature, the first two fall and the third rises — and each prevented incident maps to a concrete cost avoided, whether a wrong forecast, a duplicated effort, or a regulatory exposure. That is the business case, stated in operational terms the board understands.</p>
'''
}

FAQS = {
"data-quality-at-scale-monitoring-alerting-remediation": [
("What are the five dimensions of data quality that every monitoring programme should track?",
 "Every monitoring programme should track completeness (are expected records present), accuracy (do values match the source of truth), consistency (do related fields and tables agree), timeliness (is the data fresh enough for its purpose), and validity (do values conform to expected formats and ranges). Each dimension needs its own checks and use-case-specific thresholds, because the same dataset can be excellent for one purpose and unusable for another."),
("How should data quality alerting be tiered to avoid alert fatigue?",
 "Alerting should be tiered so volume is proportional to risk. Tier 1 critical issues — missing or fundamentally wrong data — pause downstream systems and page the data team immediately. Tier 2 warnings flag the issue on affected surfaces and open a ticket with a review deadline. Tier 3 info anomalies are logged and correlated for periodic review. This keeps critical signals visible while preventing the fatigue that causes teams to ignore alerts."),
("What role does remediation play in a data quality programme?",
 "Remediation is the half of the job after detection. It means defining a workflow for each issue type, auto-remediating where possible — backfilling missing records, correcting known schema mismatches, quarantining bad batches before they reach consumers — and converting every incident into a new automated prevention check. Without remediation, detection merely accumulates a backlog of known-bad data, which is not meaningfully better than not detecting at all.")
],
"agentic-ai-the-next-evolution-of-enterprise-automation-a-2026-update": [
("What is agentic AI and how does it differ from traditional automation?",
 "Agentic AI refers to systems that pursue a goal autonomously: they plan, choose tools, take actions, and adapt to results, rather than executing a fixed deterministic workflow. Traditional automation follows a script; an agent interprets the objective and decides the steps. That autonomy is what makes agents powerful for open-ended knowledge work, and it is also what makes them riskier, because their behaviour is not fully predetermined."),
("Why do agentic AI deployments stall in production?",
 "They stall for predictable reasons: no clear owner for the agent's decisions, weak evaluation of what the agent actually does, ungoverned access to tools and data, and no human-in-the-loop on consequential steps. Each gap turns a promising prototype into a liability. Deployments that reach production are the ones that assigned ownership, measured behaviour, scoped access, and kept a person accountable for the outcomes."),
("What governance controls does agentic AI require?",
 "Agentic AI requires scoped tool and data access so the agent can only act within its mandate, logged actions so every step is investigable after the fact, human approval on consequential decisions, and monitored retrieval so it reasons from governed sources rather than improvising. These controls are what make autonomy safe to deploy, and they are far easier to enforce when the agent sits on a governed data and access layer from the start.")
],
"automated-data-cataloguing-with-ai-classification-part-3": [
("How does AI classification improve automated data cataloguing?",
 "AI classification reads the content and metadata of datasets and automatically assigns sensitivity labels, business-domain tags, and semantic descriptions that used to be entered by hand. This scales curation to thousands of assets, keeps the catalogue current as data changes, and surfaces meaning that manual processes miss. The result is a catalogue that is populated and maintained without a small army of data stewards."),
("What makes a data catalogue earn its keep with users?",
 "A catalogue earns its keep when it pays users back faster than it taxes them: a business analyst finds the right dataset in seconds, sees a trusted definition and owner, and trusts the answer enough to act. If the catalogue only adds documentation overhead, teams route around it. The ones that stick make discovery, trust, and policy enforcement the fastest path to the data, so using the catalogue is easier than not using it."),
("How should organisations handle sensitive data discovery with AI classification?",
 "AI classification should actively scan for personally identifiable and otherwise sensitive data, flag it to the owning domain, and route it into the policy engine that applies masking and access rules automatically. Discovery is only valuable if it triggers action: a sensitive column found but left ungoverned is a liability, whereas one found and automatically protected is a risk retired. The classification step and the enforcement step must be connected.")
]
}

for slug, qa in FAQS.items():
    h = read(slug, "blog/articles")
    before = article_metric(h, "EN")
    faq_html = build_faq(qa)
    h2, added = add_faq_section(h, faq_html)
    h2, jadded = inject_jsonld_in_head(h2, build_jsonld(qa))
    if slug in EXTRA:
        h2 = inject_expansion(h2, EXTRA[slug])
    write(slug, "blog/articles", h2)
    after = article_metric(h2, "EN")
    print(f"{slug}: EN {before} -> {after} faq_added={added} jsonld={jadded} {'OK' if after>=2500 else 'SHORT'}")
