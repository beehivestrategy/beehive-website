import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "financial-services-ai-fraud-detection-real-time"

EN_ADD = """
<h2 id="which-fraud-typologies-need-which-detection-approach">Which Fraud Typologies Need Which Detection Approach?</h2>
<p>"Fraud" is not one problem, and a single model trained on all of it will be mediocre at most of it. Each typology has a different signal, a different decision window, and a different acceptable response, which is why production fraud stacks are ensembles of specialised detectors rather than one general classifier. Mapping typologies to approaches is the single highest-value piece of design work in the programme, because it determines the feature pipeline, the latency budget, and the customer experience.</p>
<p>Card-not-present fraud is a per-transaction problem with a sub-second window: the signal is device, merchant, and behavioural deviation from the cardholder's own history, and the response is a decline or a step-up authentication. Account takeover is a session problem: the signal is login behaviour, credential-stuffing patterns, and rapid changes to contact details, and the response is a session challenge rather than a decline. First-party fraud and bust-out behaviour unfold over weeks: the signal is credit utilisation and repayment behaviour, and the response is a credit limit action, not a transaction block. Authorised push payment and scam fraud is the hardest category because the customer authorises the payment, so the signal is destination-account risk and behavioural anomaly in the instruction itself, and the response is an intervention — a warning, a delay, or a confirmation call.</p>
<table class="article-table">
<thead><tr><th>Typology</th><th>Primary signal</th><th>Decision window</th><th>Response</th></tr></thead>
<tbody>
<tr><td>Card-not-present</td><td>Device, merchant, and behavioural deviation</td><td>Sub-second</td><td>Decline or step-up authentication</td></tr>
<tr><td>Account takeover</td><td>Login anomalies, credential-stuffing patterns</td><td>Session</td><td>Session challenge, credential reset</td></tr>
<tr><td>First-party / bust-out</td><td>Utilisation and repayment trajectory</td><td>Weeks</td><td>Credit limit or account action</td></tr>
<tr><td>Authorised push payment</td><td>Destination-account risk, instruction anomaly</td><td>Minutes</td><td>Warning, delay, or confirmation call</td></tr>
<tr><td>Merchant and mule networks</td><td>Network graph structure across accounts</td><td>Days</td><td>Investigation and account closure</td></tr>
</tbody>
</table>
<h2 id="how-do-you-tune-the-false-positive-trade-off">How Do You Tune the False-Positive Trade-off?</h2>
<p>Fraud detection is an economics problem disguised as a modelling problem. Declining a fraudulent transaction saves the transaction value plus the chargeback and investigation cost; declining a legitimate one costs the margin on that transaction plus a share of the customer's lifetime value, and it generates a support contact on top. Those two numbers are rarely symmetric, and the correct operating point is wherever the total expected cost is minimised — not wherever the model's F1 score is maximised.</p>
<p>Working the arithmetic changes the decision. If the average fraudulent transaction is 400 currency units, chargeback and handling add 60, and the average legitimate transaction carries 30 units of margin with a customer lifetime value of 900, then a false decline costs roughly 1 to 2 percent of lifetime value in churn risk plus immediate margin — meaning the cost ratio is far closer to parity than most teams assume. The practical consequence is that a slightly lower detection threshold, combined with a step-up authentication path instead of a hard decline, usually dominates a high-threshold, hard-decline strategy. Give the good customer a way through, and the trade-off stops being a trade-off.</p>
<table class="article-table">
<thead><tr><th>Lever</th><th>Effect on fraud loss</th><th>Effect on customer friction</th></tr></thead>
<tbody>
<tr><td>Hard decline</td><td>Large reduction</td><td>High — blocked good customers</td></tr>
<tr><td>Step-up authentication</td><td>Moderate reduction</td><td>Low — good customers complete</td></tr>
<tr><td>Manual review queue</td><td>Moderate reduction</td><td>Medium — delays, but no blocks</td></tr>
<tr><td>Customer warning at point of payment</td><td>Small reduction</td><td>Very low — customer decides</td></tr>
<tr><td>Delayed settlement on new payees</td><td>Moderate reduction</td><td>Medium — affects speed expectations</td></tr>
</tbody>
</table>
<p>Two practices keep the operating point honest over time. Run champion-challenger continuously, so any proposed threshold or model change is measured against the incumbent on live traffic before promotion. And review the decline population, not just the alert population: sampling declined transactions and manually assessing whether they were truly fraudulent is the only way to detect the silent failure where a model has learned to decline a specific legitimate segment.</p>
<h2 id="what-governance-evidence-do-regulators-expect-for-fraud-models">What Governance Evidence Do Regulators Expect for Fraud Models?</h2>
<p>Fraud models sit squarely inside model risk management because they make automated decisions with financial consequences for customers. Supervisors do not prescribe a specific model, but they consistently expect documented development, documented validation, and demonstrable ongoing monitoring. The institutions that handle examinations well are the ones that produce this evidence as a by-product of normal engineering rather than assembling it under deadline.</p>
<table class="article-table">
<thead><tr><th>Artefact</th><th>What it demonstrates</th><th>Cadence</th></tr></thead>
<tbody>
<tr><td>Model documentation</td><td>Intended use, data lineage, features, assumptions, and limitations</td><td>Per model version</td></tr>
<tr><td>Independent validation</td><td>Conceptual soundness and outcome analysis by a party separate from development</td><td>At launch and on material change</td></tr>
<tr><td>Performance monitoring</td><td>Detection rate, false-positive rate, and drift against approved thresholds</td><td>Monthly</td></tr>
<tr><td>Adverse action reasonability</td><td>Customers receive an intelligible reason for a decline</td><td>Continuous</td></tr>
<tr><td>Override and exception log</td><td>Who bypassed a decision and why</td><td>Continuous</td></tr>
<tr><td>Change management record</td><td>Every threshold and model change, with approval</td><td>Per change</td></tr>
</tbody>
</table>
<p>The requirement that causes the most difficulty is explainability at the individual decision level. A gradient-boosted ensemble is defensible in aggregate but awkward when a customer asks why their payment was declined. The workable resolution is to separate the scoring model from the reason model: let a complex model produce the risk score, and generate the customer-facing reason from a small, interpretable set of factors that genuinely drove the decision. Institutions that design for this from the start avoid the painful retrofit of trying to explain a model that was never built to be explained.</p>
"""

H2FIX = {
    "EN": [
        ("industry-ai-maturity-in-2026", "How Mature Is AI in Financial Services in 2026?"),
        ("domain-specific-implementation-patterns", "What Are the Domain-Specific Implementation Patterns?"),
        ("roi-measurement-and-value-realization", "How Is ROI Measured and Value Realized?"),
        ("overcoming-industry-specific-barriers", "How Do You Overcome Industry-Specific Barriers?"),
        ("frequently-asked-questions", "What Questions Come Up Most Often?"),
    ],
    "CN": [
        ("domain-specific-implementation-patterns", "What Are the Domain-Specific Implementation Patterns?"),
        ("roi-measurement-and-value-realization", "How Is ROI Measured and Value Realized?"),
        ("overcoming-industry-specific-barriers", "How Do You Overcome Industry-Specific Barriers?"),
        ("常见问题", "常见问题有哪些？"),
        ("规模化推广的关键成功因素", "规模化推广的关键成功因素有哪些？"),
        ("技术基础设施与实施考量", "技术基础设施与实施考量是什么？"),
        ("中国市场特有的实施优势", "中国市场特有的实施优势有哪些？"),
    ],
    "TW": [
        ("2026-年產業-ai-成熟度", "2026 年產業 AI 成熟度如何？"),
        ("領域特定實施模式", "領域特定實施模式有哪些？"),
        ("投資回報衡量與價值實現", "投資回報如何衡量與實現？"),
        ("克服產業特定障礙", "如何克服產業特定障礙？"),
    ],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD}, tag=SLUG[:24])
