#!/usr/bin/env python3
"""EN body expansion, batch 5 (top-ups to clear the 2,500-word floor)."""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb002_lib import apply_ops

DATA = {}

DATA['ai-content-labeling-regulations'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("How Should Labeling Requirements Be Wired Into Content Operations?", """
<p>Labeling obligations are met by systems, not by guidelines. The operational question is where the control sits in the content lifecycle, and the answer is: at every transition where content changes hands.</p>
<p><strong>At generation.</strong> The generation service records provenance &mdash; model, version, prompt template, input sources &mdash; and marks the output. This is the only point at which you know for certain that the content is synthetic.</p>
<p><strong>At review and approval.</strong> Reviewers see the provenance record and confirm whether a disclosure is required for the intended channel and audience. This is a human decision, because it depends on context the system does not have: is this internal, is it editorial, is it going to a regulated market.</p>
<p><strong>At distribution.</strong> The publishing layer applies the disclosure appropriate to the channel, and refuses to publish into channels where required disclosure is missing. Making this a hard gate rather than a warning is what prevents deadline pressure from silently removing labels.</p>
<p><strong>At update and re-export.</strong> Content gets cropped, re-rendered, translated, and repackaged. Every transform must carry the provenance record forward, and any transform that destroys a visible mark must reapply it. This is the step that breaks most often, and it is where quarterly path testing earns its keep.</p>
<p>Assign an owner to each transition. Labeling fails at the seams between teams, not within them, and the seam is always the hand-off nobody owns.</p>
"""),
])

DATA['ai-conversational-analytics-energy-sector-optimization'] = dict(before='Frequently Asked Questions', inserts=[
    ("How Should Energy Teams Measure Adoption?", """
<p>Adoption is the metric that separates deployed from used, and most energy analytics programmes measure the wrong thing. Licence counts and query volumes tell you the system is reachable; they do not tell you it changed a decision.</p>
<p><strong>Measure decision coverage, not query count.</strong> Of the recurring operational decisions in scope &mdash; outage review, fuel selection, emissions reporting, scheduling &mdash; what proportion now start with the system rather than with a spreadsheet request? That proportion is adoption, and it is measured by surveying decision owners, not by reading logs.</p>
<p><strong>Measure time-to-answer against a baseline.</strong> Record how long each of those decisions took before deployment. The delta is the value story, and it is almost always larger than expected because the baseline includes queue time, not just analysis time.</p>
<p><strong>Measure trust signals.</strong> Do users act on the answer directly, or do they re-verify it in another system? Re-verification rates falling over time is the clearest evidence the semantic layer is working.</p>
<p><strong>Measure the questions that fail.</strong> Unanswered or abandoned queries are the roadmap. Reviewed weekly in the first quarter, they tell you which definitions are missing and which data sources are not connected &mdash; and fixing the top ten usually lifts adoption more than any new feature.</p>
"""),
])

DATA['ai-copyright-infringement-training-data-legal'] = dict(before='__FAQ__', inserts=[
    ("How Should AI Vendors and Model Providers Be Assessed?", """
<p>Enterprises rarely train foundation models; they fine-tune, retrieve, and deploy. That shifts the copyright question from what you trained on to what your vendor trained on &mdash; and what they will indemnify.</p>
<p><strong>Ask for the training-data position in writing.</strong> Which corpora, which licences, what opt-out handling, and what filtering was applied. Vague answers about "publicly available data" are not a position. Providers with mature programmes publish this; those without one will offer marketing material instead.</p>
<p><strong>Negotiate indemnity, and read its scope.</strong> Many indemnities cover only output claims &mdash; that the generated text infringes &mdash; and exclude claims arising from training data. Others cap at fees paid, which is immaterial next to exposure. Establish which of the three you are getting: output indemnity, training-data indemnity, or neither.</p>
<p><strong>Check the data-handling terms for your inputs.</strong> Whether prompts and outputs are retained, used for training, or logged for abuse monitoring determines your own obligations downstream, particularly where customer or employee data is involved.</p>
<p><strong>Assess change risk.</strong> Providers change models, terms, and datasets. Require notice of material changes to training-data practices or indemnity scope, and include a termination right if the change is unacceptable. A vendor's copyright position today is not a commitment about next year.</p>
"""),
])

DATA['ai-cost-optimization-strategies'] = dict(before='What Are the Key Takeaways?', inserts=[
    ("Who Should Own AI Cost Governance?", """
<p>AI spend becomes manageable when a specific person is accountable for it, and stays theoretical when it is everybody's concern. Three roles, clearly separated.</p>
<p><strong>The platform owner</strong> owns unit economics: instrumentation, routing policy, caching, shared retrieval infrastructure, and the cost dashboard. This is an engineering accountability, measured in cost per request and in coverage &mdash; what proportion of AI spend is attributed to an owner.</p>
<p><strong>The use-case owner</strong> owns the value side: whether the spend on their workflow is justified by the outcome. Every AI workflow should have a named business owner whose budget line it sits on. Workflows without one are the ones that should be questioned first.</p>
<p><strong>Finance</strong> owns forecasting and the chargeback mechanism. Not setting policy on models &mdash; but translating consumption into a form business units recognise, and holding the variance conversation each month.</p>
<p>A small cross-functional review &mdash; platform, finance, and the largest use-case owners &mdash; meeting monthly is what makes it operate. Escalation belongs with whoever owns the AI portfolio. The failure mode to avoid is placing cost governance in a central committee with no engineering authority: it produces reports, not reductions.</p>
"""),
])

DATA['ai-cost-optimization-strategies-enterprise'] = dict(before='Frequently asked questions', inserts=[
    ("How Do You Stop Shadow AI From Reappearing?", """
<p>Every organisation that has run an AI cost programme has discovered unauthorised accounts, and most have watched them return within two quarters. Shadow AI is a supply problem, not a compliance problem: teams go around the platform because the platform is slower or less capable than what they can get themselves.</p>
<p><strong>Make the internal path faster.</strong> If provisioning a sanctioned model endpoint takes six weeks and a credit card takes six minutes, policy will lose every time. Target same-day provisioning for standard configurations, with pre-approved models, standard data-handling terms, and a self-service request path.</p>
<p><strong>Provide detection, not just prohibition.</strong> Monitor for unapproved model-provider usage at the network and expense level: API endpoints in egress traffic, unfamiliar SaaS charges on corporate cards, and new vendor requests in accounts payable. Detection turns an unenforceable rule into a conversation.</p>
<p><strong>Convert discovered usage into governed usage.</strong> When you find a team using an unapproved tool, the productive response is not "stop" &mdash; it is "here is the same capability with your data governed and your costs attributed". Most teams are not avoiding governance; they are avoiding friction.</p>
<p><strong>Publish what is approved and why.</strong> A short, maintained list of approved models, their approved data classes, and their cost per request removes the ambiguity that drives teams to their own arrangements. Ambiguity, not rebellion, is the main cause of shadow AI.</p>
<p>Measure success by the share of AI spend flowing through governed infrastructure. That single ratio tells you whether the platform is winning.</p>
"""),
])

if __name__ == '__main__':
    for slug, d in DATA.items():
        changed = apply_ops(slug, 'en', inserts=d['inserts'], before=d['before'])
        print(('inserted ' if changed else 'noop     ') + slug)
