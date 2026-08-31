import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "logistics-route-optimization-ai-real-time"

EN_ADD = """
<h2 id="how-do-you-model-the-constraints-that-break-naive-routing">How Do You Model the Constraints That Break Naive Routing?</h2>
<p>Route optimization is a constrained problem long before it is an AI problem, and the reason so many pilots fail is that the demo solves the travelling-salesman version while the business operates the vehicle-routing version. Shortest path is not the objective; feasible-and-cheapest is. A plan that saves nine minutes but violates a driver's hours-of-service limit is not a better plan, it is a compliance incident.</p>
<p>The constraints arrive in three families. Hard constraints cannot be broken under any circumstances: driver hours and rest requirements, vehicle weight and volume capacity, hazmat and access restrictions, and any delivery window the customer has contractually fixed. Soft constraints can be broken at a known cost: a preferred delivery window, a preferred driver, a target return time to depot. Stochastic constraints are the ones that make real-time necessary — traffic, dwell time at the dock, weather, and vehicle breakdown, none of which are known at plan time and all of which invalidate a static plan within an hour.</p>
<table class="article-table">
<thead><tr><th>Constraint family</th><th>Examples</th><th>Modelling approach</th><th>Cost of getting it wrong</th></tr></thead>
<tbody>
<tr><td>Hard</td><td>Hours of service, vehicle capacity, access restrictions</td><td>Infeasible solutions rejected outright</td><td>Regulatory penalty, failed delivery</td></tr>
<tr><td>Soft</td><td>Preferred windows, driver preference, depot return time</td><td>Penalty cost in the objective function</td><td>Overtime, poor driver retention</td></tr>
<tr><td>Stochastic</td><td>Traffic, dock dwell time, weather, breakdown</td><td>Distributions plus continuous replanning</td><td>Missed windows, compensation claims</td></tr>
<tr><td>Commercial</td><td>Contracted service levels, priority customers</td><td>Weighted objective with service tiers</td><td>Churn, contractual penalties</td></tr>
</tbody>
</table>
<p>The practical guidance is to encode the hard constraints first and let the optimiser be conservative, then add soft constraints with explicit penalties that a dispatcher can read. Dispatchers distrust a plan they cannot explain, and a plan that shows "this stop moved because it saved 40 minutes and cost 5 minutes of window deviation" gets accepted, while a black-box reordering gets overridden manually — at which point the optimisation has delivered nothing.</p>
<h2 id="what-does-a-replanning-loop-look-like-in-production">What Does a Replanning Loop Look Like in Production?</h2>
<p>Real-time optimization is not a faster plan; it is a loop that decides when to replan, what to change, and who needs to know. The event that triggers a replan matters as much as the algorithm that computes it, because replanning too often produces churn — drivers receiving changed instructions every few minutes stop trusting the system — while replanning too rarely reproduces the static-plan problem with extra compute.</p>
<p>A workable loop has four stages. Detection compares the current state against the plan and flags only material deviations: a vehicle running more than an agreed number of minutes behind, a new order arriving inside a cutoff, a vehicle dropping out, or a dock dwell time exceeding its expected range. Evaluation scores candidate replans against the objective and against a stability penalty, so the system prefers a plan that changes few stops unless the gain is large. Commitment applies the change only within a freeze window — stops already being served or within a short horizon are locked. Communication pushes the change to the driver, the dispatcher, and, where the customer is affected, the customer notification system, in that order.</p>
<table class="article-table">
<thead><tr><th>Trigger</th><th>Typical threshold</th><th>Response</th></tr></thead>
<tbody>
<tr><td>Vehicle behind plan</td><td>More than 10-15 minutes behind schedule</td><td>Re-evaluate remaining stops; notify affected customers</td></tr>
<tr><td>New order received</td><td>Inside the same-day cutoff and serviceable region</td><td>Insertion test with stability penalty; commit if net positive</td></tr>
<tr><td>Vehicle breakdown</td><td>Immediate</td><td>Full reassignment of remaining stops across the fleet</td></tr>
<tr><td>Dwell time overrun</td><td>Exceeds expected dwell by the agreed margin</td><td>Downstream window recalculation</td></tr>
<tr><td>Traffic incident</td><td>Confirmed incident on a planned corridor</td><td>Corridor re-sequencing within the freeze window</td></tr>
</tbody>
</table>
<p>The freeze window is the detail that separates a usable system from an unusable one. Drivers need a horizon within which their instructions are stable, typically the next two to three stops. Fix that horizon, publish it, and honour it except in a genuine exception, and adoption follows; change instructions continuously in pursuit of a marginally better plan and the system gets ignored.</p>
<h2 id="how-do-you-prove-roi-on-route-optimization">How Do You Prove ROI on Route Optimization?</h2>
<p>Logistics ROI is unusually measurable because almost every improvement maps to a line item that already exists in the accounts. The discipline is to attribute honestly: compare like-for-like periods on matched lanes, hold service levels constant, and separate the optimisation effect from fuel price movement and volume mix. Without that discipline, a good result is indistinguishable from a favourable quarter.</p>
<table class="article-table">
<thead><tr><th>Value source</th><th>How it is measured</th><th>Typical first-year range</th></tr></thead>
<tbody>
<tr><td>Distance and fuel</td><td>Kilometres per drop, fuel per kilometre, on matched lanes</td><td>5-12% reduction</td></tr>
<tr><td>Driver hours and overtime</td><td>Paid hours per drop; overtime hours per week</td><td>4-10% reduction</td></tr>
<tr><td>Failed and re-delivered drops</td><td>Re-delivery rate and compensation paid per period</td><td>10-25% reduction</td></tr>
<tr><td>Fleet utilisation</td><td>Drops per vehicle per day; empty running</td><td>3-8% improvement</td></tr>
<tr><td>Customer retention</td><td>Repeat order rate among customers with improved ETA accuracy</td><td>2-6% improvement</td></tr>
</tbody>
</table>
<p>The composite effect is consistent with the industry figures: carriers that execute well report cost reductions in the mid-teens and revenue improvements in the high single to low double digits within a year. But the distribution is wide, and the variance is explained almost entirely by data quality and by whether drivers actually follow the plan. Those two factors, not the solver, determine which end of the range a carrier lands on — which is why the unglamorous work of governed data and dispatcher trust is where the return is really earned.</p>
"""

H2FIX = {
    "EN": [
        ("industry-landscape-and-ai-adoption-dynamics", "What Does the Industry Landscape and AI Adoption Picture Look Like?"),
        ("key-use-cases-and-implementation-patterns", "What Are the Key Use Cases and Implementation Patterns?"),
        ("overcoming-implementation-challenges", "How Do You Overcome Implementation Challenges?"),
        ("deep-analysis-of-industry-digital-transformation", "What Does a Deep Analysis of Industry Digital Transformation Show?"),
    ],
    "CN": [
        ("行业格局与ai采用动态", "行业格局与 AI 采用动态如何？"),
        ("关键用例与实施模式", "关键用例与实施模式有哪些？"),
        ("克服实施挑战", "如何克服实施挑战？"),
        ("行业最佳实践与成功案例分析", "行业最佳实践与成功案例有哪些？"),
        ("行业数字化转型深度分析", "行业数字化转型的深度分析是什么？"),
        ("战略实施路径与关键成功因素", "战略实施路径与关键成功因素是什么？"),
        ("企业实施路线图与成功因素", "企业实施路线图与成功因素有哪些？"),
        ("行业数字化转型深度分析-2", "行业数字化转型的深度分析是什么？"),
    ],
    "TW": [
        ("行業格局與ai採用動態", "行業格局與 AI 採用動態如何？"),
        ("關鍵用例與實施模式", "關鍵用例與實施模式有哪些？"),
        ("克服實施挑戰", "如何克服實施挑戰？"),
        ("行業最佳實踐與成功案例分析", "行業最佳實踐與成功案例有哪些？"),
        ("行業數位轉型深度分析", "行業數位轉型的深度分析是什麼？"),
        ("戰略實施路徑與關鍵成功因素", "戰略實施路徑與關鍵成功因素是什麼？"),
        ("企業實施路線圖與成功因素", "企業實施路線圖與成功因素有哪些？"),
        ("行業數位轉型深度分析-2", "行業數位轉型的深度分析是什麼？"),
    ],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD}, tag=SLUG[:24])
