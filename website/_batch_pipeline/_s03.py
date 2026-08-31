import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "professional-services-ai-leverage-growth"

EN_ADD = """
<h2 id="what-does-ai-leverage-look-like-on-a-firms-profit-and-loss">What Does AI Leverage Look Like on a Firm's Profit and Loss Statement?</h2>
<p>Professional services economics reduce to three ratios: utilisation, realisation, and leverage. Utilisation is the share of paid hours that are billable; realisation is the share of standard rates actually collected; leverage is the ratio of junior to senior hours on an engagement. AI moves all three, but it moves them by different mechanisms and at different speeds, and confusing the three is why some firms invest heavily and see nothing on the bottom line.</p>
<p>Utilisation improves first and most visibly, because it is a subtraction problem: every hour a consultant stops searching for a precedent, reformatting a deck, or reconciling two spreadsheets is an hour that can be billed. Realisation improves more slowly, and only if the firm changes how it prices — an engagement that used to take 400 hours and now takes 260 will still be billed at the old fee unless the commercial model is revisited. Leverage improves last, and it is the most valuable: when juniors can produce work that previously required a senior reviewer, the firm can take on more engagements without adding partners, which is the only structurally scalable path to margin growth.</p>
<table class="article-table">
<thead><tr><th>Metric</th><th>Typical pre-AI baseline</th><th>Mechanism of improvement</th><th>Realistic 12-month gain</th></tr></thead>
<tbody>
<tr><td>Utilisation</td><td>70-80%</td><td>Research, drafting, and formatting hours removed from delivery</td><td>3-6 percentage points</td></tr>
<tr><td>Realisation</td><td>85-92%</td><td>Better-scoped proposals and fewer write-offs from rework</td><td>1-3 percentage points</td></tr>
<tr><td>Leverage</td><td>3:1 to 5:1 junior to senior</td><td>Juniors producing partner-review-ready first drafts</td><td>0.5-1.0x improvement</td></tr>
<tr><td>Proposal cycle time</td><td>3-6 weeks</td><td>Automated research and first-draft generation</td><td>45-60% reduction</td></tr>
<tr><td>Revenue per partner</td><td>Baseline</td><td>Combination of the four effects above</td><td>8-15% uplift</td></tr>
</tbody>
</table>
<p>The trap in this table is the last row. Revenue per partner only rises if the freed capacity is sold, not absorbed. Firms that treat AI as a cost-reduction programme end up with idle capacity and quickly lose the people who produced the savings; firms that treat it as a capacity-creation programme redeploy the hours into more proposals, more engagements, and deeper client relationships. The difference is a management decision made in month one, not a technology outcome.</p>
<h2 id="how-should-firms-price-ai-augmented-engagements">How Should Firms Price AI-Augmented Engagements?</h2>
<p>When delivery takes 30% fewer hours, hourly billing quietly transfers the entire productivity gain to the client. Most firms discover this about two quarters after deployment, when utilisation is up but revenue is flat. Four pricing responses are in use, and the right answer is usually a blend rather than a single model.</p>
<p>Fixed-fee and milestone pricing converts efficiency into margin immediately and is the simplest place to start, but it requires honest scoping discipline or the firm absorbs the risk of scope creep. Value-based pricing ties the fee to a client outcome — a cost reduction, a successful system cutover, a regulatory clearance — and captures the most upside, but it demands the confidence to quantify value up front and the data to defend it afterwards. Subscription or retainer pricing works well for ongoing advisory work where the deliverable is access to judgement rather than a document, and it smooths the revenue volatility that makes professional services hard to value. Hybrid models — a fixed platform fee plus outcome-linked success components — are increasingly the default for AI-heavy engagements because they let the client see the efficiency gain while letting the firm keep some of it.</p>
<p>Whichever model a firm chooses, two mechanics matter more than the headline structure. First, instrument delivery from day one so you can prove the hours saved; without that evidence, every pricing conversation is an argument about anecdotes. Second, publish an internal policy on AI disclosure. Clients increasingly ask directly whether AI was used and how outputs were verified, and firms that answer confidently — with a documented review process, named reviewers, and a stated confidentiality posture — convert that question into a trust advantage rather than a defence.</p>
<h2 id="what-does-a-12-month-adoption-roadmap-look-like">What Does a 12-Month Adoption Roadmap Look Like?</h2>
<p>The firms that succeed sequence adoption around knowledge assets rather than around tools. Knowledge has to be findable before it can be reasoned over, and it has to be governed before it can be exposed to a model. That sequencing produces a four-quarter plan in which each quarter delivers something the firm can sell, not just something it can demo.</p>
<table class="article-table">
<thead><tr><th>Quarter</th><th>Focus</th><th>Deliverable</th><th>Success signal</th></tr></thead>
<tbody>
<tr><td>Q1</td><td>Knowledge inventory and governance</td><td>Classified corpus of proposals, engagement reports, and methodologies with named owners</td><td>Answerable questions with citations</td></tr>
<tr><td>Q2</td><td>Proposal and research augmentation</td><td>AI-drafted research packs and first-draft proposal sections</td><td>Proposal cycle time down 30%+</td></tr>
<tr><td>Q3</td><td>Delivery augmentation</td><td>Methodology guidance and precedent retrieval inside delivery teams</td><td>Measurable reduction in rework hours</td></tr>
<tr><td>Q4</td><td>Commercial model change</td><td>Revised pricing templates and AI disclosure policy</td><td>Realisation and revenue per partner improving</td></tr>
</tbody>
</table>
<p>Two organisational choices determine whether the roadmap completes. Assign a partner-level owner with a commercial target, not just a technology sponsor — adoption stalls when it is owned by IT and measured in logins. And start with one practice area rather than the whole firm: a single vertical with a motivated managing partner produces a reference case in one quarter, and a reference case does more for firm-wide adoption than any amount of centrally mandated training.</p>
"""

process(SLUG, {}, adds={"EN": EN_ADD}, tag=SLUG[:24])
