#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 13: supply-chain-ai-demand-sensing-real-time-apr
EN 1561 -> ~2600 ; CN/TW already long enough ; H2 -> questions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_by_text

SLUG = "supply-chain-ai-demand-sensing-real-time-apr"
ANCHOR = '            <section class="faq-section"'

EN_NEWS = """<h2 id="how-does-demand-sensing-differ-from-forecasting">How Does Demand Sensing Differ From Demand Forecasting?</h2>
<p>The two are often conflated, and the distinction matters because they answer different questions on different clocks. Traditional demand forecasting produces a baseline: given history, seasonality, and a promotional calendar, what will demand be over the next planning horizon? It is typically generated monthly, at an aggregate level of product and location, and it is optimised for stability — planners do not want the baseline moving under them. Demand sensing answers a different question: given what happened at the shelf today, what should we believe about the next few weeks? It runs daily or intra-day, at a much finer granularity, and it is optimised for responsiveness.</p>
<p>The practical consequence is that sensing does not replace forecasting; it sits on top of it. The monthly statistical forecast remains the governed baseline that finance and the S&OP process anchor on, and the sensing layer produces a continuously refreshed adjustment between cycles, with each adjustment attributable to a specific signal. This hybrid is easier to audit than a black-box model that regenerates the whole forecast, and it is easier for planners to trust, because they can see and challenge the delta rather than accepting or rejecting an entirely new number.</p>
<p>The horizon is the other distinguishing dimension. Sensing adds most of its value in the near horizon — the next two to eight weeks, where the planning cycle is too slow to react and where most of the bullwhip effect is generated. Beyond that horizon the statistical baseline and the promotional calendar dominate, and sensing signals carry little additional information. Programmes that implement sensing as a replacement for long-horizon forecasting tend to be disappointed by precisely this: the model looks no better at twelve months out, which was never where its value was.</p>
<h2 id="which-signals-actually-improve-accuracy">Which Signals Actually Improve Forecast Accuracy?</h2>
<p>Not every external signal earns its integration cost, and teams that ingest everything available usually discover that most of it adds noise. The signals with consistent, measurable value fall into four groups. Point-of-sale and sell-through data is the strongest by a wide margin, because it reflects actual consumption rather than shipments, and it removes the lag that causes every tier of the network to overreact to its own order pattern. Promotional and pricing signals are second — the promotion calendar, the actual discount depth, and competitor price moves — because promotional lift is the largest single source of forecast error in consumer businesses.</p>
<p>Weather and calendar signals are third and genuinely useful in categories with demonstrated weather sensitivity, though the temptation to add weather everywhere should be resisted: for most categories the effect is small and the model will simply learn to ignore it. Logistics and supply telemetry — port congestion, supplier lead-time drift, in-transit visibility — is fourth, and it matters more for the supply side of the equation than the demand side, feeding disruption early warning rather than the demand number itself.</p>
<p>The discipline that separates useful signals from noise is incremental validation: add one signal, measure the change in forecast error on a holdout period, and keep it only if the improvement is material and stable. Signals that improve accuracy by a fraction of a percent are not worth the pipeline they require, and a model with four well-understood inputs outperforms one with forty poorly understood inputs — not least because the planner can actually explain the four.</p>
<h2 id="how-do-you-measure-demand-sensing-value">How Do You Measure the Value of Demand Sensing?</h2>
<p>Three metrics carry the business case, and they should be baselined before the first model ships or the value claim will not survive scrutiny. Forecast accuracy is the first, expressed as Mean Absolute Percentage Error or, better, as forecast value added against a naive seasonal baseline — because absolute error is heavily influenced by which products you carry, while FVA isolates the improvement the model actually contributed. Inventory is the second, tracked as days of supply and as the split between working inventory and safety stock, since the point of a sharper signal is that less buffer is needed for the same service level.</p>
<p>Service level is the third, and it is the constraint that keeps the other two honest: a programme that cuts inventory while stock-outs rise has not created value, it has moved cost onto the customer. Report all three together, against a pre-deployment baseline, and the trade-offs become visible rather than arguable. Alongside them, track planner override rate — the share of model outputs a planner changes without documented evidence — because it is the earliest indicator of whether the system is trusted, and a rising override rate predicts a return to the old error pattern well before accuracy metrics move.</p>
<p>The value conversation lands best when it is framed in cash rather than in percentage points. A ten to twenty percent inventory reduction is working capital released; a reduction in lost sales is revenue recovered; fewer expedites is freight cost avoided. Translating the three metrics into those three numbers, with the finance team's own conversion factors, is what turns a supply chain improvement into a funded programme rather than an interesting pilot.</p>
"""

EN_H2 = [
    ("Industry Landscape and AI Adoption Dynamics",
     "What Is Driving AI Adoption in Supply Chain Demand Sensing?"),
    ("Key Use Cases and Implementation Patterns", "Which Use Cases Deliver Value First?"),
    ("Overcoming Implementation Challenges", "How Do You Overcome the Implementation Challenges?"),
    ("Deep Analysis of Industry Digital Transformation",
     "How Is Supply Chain Digital Transformation Evolving?"),
]
CN_H2 = [
    ("行业格局与AI采用动态", "是什么在推动供应链领域的AI采用？"),
    ("关键用例与实施模式", "哪些用例最先产生价值？"),
    ("克服实施挑战", "应当如何克服实施挑战？"),
    ("行业最佳实践与成功案例分析", "有哪些值得借鉴的行业最佳实践？"),
    ("战略实施路径与关键成功因素", "战略实施路径的关键成功因素是什么？"),
    ("企业实施路线图与成功因素", "企业应如何规划实施路线图？"),
]
TW_H2 = [
    ("行業格局與AI採用動態", "是什麼在推動供應鏈領域的AI採用？"),
    ("關鍵用例與實施模式", "哪些用例最先產生價值？"),
    ("克服實施挑戰", "應當如何克服實施挑戰？"),
    ("行業最佳實踐與成功案例分析", "有哪些值得借鑑的行業最佳實踐？"),
    ("戰略實施路徑與關鍵成功因素", "戰略實施路徑的關鍵成功因素是什麼？"),
    ("企業實施路線圖與成功因素", "企業應如何規劃實施路線圖？"),
]
# text appears twice -> two distinct question forms
CN_DUP = [
    ("行业数字化转型深度分析", "行业数字化转型正在如何演进？", 0),
    ("行业数字化转型深度分析", "行业数字化转型的深层动力是什么？", 1),
]
TW_DUP = [
    ("行業數位轉型深度分析", "行業數位轉型正在如何演進？", 0),
    ("行業數位轉型深度分析", "行業數位轉型的深層動力是什麼？", 1),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    assert h.count(ANCHOR) == 1
    h = h.replace(ANCHOR, "\n" + EN_NEWS + "\n" + ANCHOR)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body expanded")

    for old, new in EN_H2:
        retitle_by_text(en, old, new)
    for old, new in CN_H2:
        retitle_by_text(path_of(SLUG, "cn"), old, new)
    for old, new in TW_H2:
        retitle_by_text(path_of(SLUG, "tw"), old, new)
    for old, new, w in CN_DUP:
        retitle_by_text(path_of(SLUG, "cn"), old, new, which=w)
    for old, new, w in TW_DUP:
        retitle_by_text(path_of(SLUG, "tw"), old, new, which=w)
    print("H2s converted in en/cn/tw")
