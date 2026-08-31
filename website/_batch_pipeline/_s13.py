import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "ai-powered-forecasting-weather-to-warehouse"

EN_ADD = """
<h2 id="which-external-signals-are-worth-integrating-and-in-what-order">Which External Signals Are Worth Integrating, and in What Order?</h2>
<p>External signals are not equally valuable, and integrating them in the wrong order is the fastest way to lose credibility with the planning team. Two properties determine priority: lead time, meaning how far ahead the signal is knowable, and coverage, meaning what share of your demand it actually explains. A signal with a long lead time but narrow coverage is worth less than a short-lead, broad-coverage signal, because planners can only act on what they can see soon enough to change an order.</p>
<p>Weather ranks first for most consumer businesses on both counts: forecasts are published up to fourteen days ahead with reasonable skill, and temperature moves demand across grocery, beverage, apparel, and home categories. Promotional and price calendars rank second, and they are the most underrated signal because they are entirely internal — many forecasting errors attributed to external volatility are actually caused by the model not knowing about a promotion that marketing planned six weeks ago. Event calendars rank third and matter enormously in specific geographies. Social and search trends have the longest potential lead time for individual products but the narrowest coverage, which is why they are usually the fourth signal rather than the first.</p>
<table class="article-table">
<thead><tr><th>Signal</th><th>Usable lead time</th><th>Coverage of demand</th><th>Integration effort</th></tr></thead>
<tbody>
<tr><td>Weather forecast</td><td>Up to 14 days</td><td>Broad across consumer categories</td><td>Low — mature APIs, stable schemas</td></tr>
<tr><td>Promotion and price calendar</td><td>4-8 weeks</td><td>Broad, but only promoted SKUs</td><td>Low — internal, though often unmodelled</td></tr>
<tr><td>Local events and holidays</td><td>2-12 weeks</td><td>Narrow but locally intense</td><td>Medium — semi-structured sources</td></tr>
<tr><td>Search and social trends</td><td>7-14 days for individual SKUs</td><td>Narrow, concentrated in trend-driven products</td><td>Medium — rate limits and definitional work</td></tr>
<tr><td>Economic indicators</td><td>Quarterly</td><td>Broad for discretionary categories</td><td>Low — published, but slow moving</td></tr>
<tr><td>Competitor pricing</td><td>Days</td><td>Narrow, price-elastic categories</td><td>High — collection and legal review</td></tr>
</tbody>
</table>
<p>The recommended sequence is therefore weather, then internal promotional calendars, then events, then social. Each step delivers a measurable accuracy improvement that can be shown to the planning team, which matters more than the order itself: planners who see one signal work will sponsor the next, whereas a programme that integrates six signals and cannot attribute any improvement loses its budget in the second year.</p>
<h2 id="how-do-you-measure-whether-an-external-signal-actually-helped">How Do You Measure Whether an External Signal Actually Helped?</h2>
<p>Adding a feature to a forecast model always improves in-sample fit and frequently fails out of sample, so the question is never whether the model likes the signal but whether the business performs better with it. The measurement that answers this is a backtest on historical periods that contained the relevant event, scored against a baseline model without the signal, using error metrics the planning team already trusts.</p>
<p>Start by selecting evaluation windows deliberately. If you are testing weather, evaluate on weeks when temperature deviated materially from seasonal normal — the heatwave weeks, the unseasonably cold fortnight — because a model that ignores weather will perform identically to one that includes it on ordinary weeks. If you are testing events, evaluate on event weeks and matched non-event weeks in the same geography. This is the step most teams skip, and it is why average accuracy over a full year can hide the entire benefit of the signal: the benefit is concentrated in exactly the periods that an annual average dilutes away.</p>
<table class="article-table">
<thead><tr><th>Measure</th><th>Definition</th><th>Why it matters to planners</th></tr></thead>
<tbody>
<tr><td>Weighted MAPE on event windows</td><td>Error on weeks where the signal deviated from normal</td><td>Shows value where it counts, not on average</td></tr>
<tr><td>Bias</td><td>Systematic over- or under-forecast</td><td>Bias drives stockouts or write-offs specifically</td></tr>
<tr><td>Stockout rate</td><td>SKU-store-weeks out of stock</td><td>The operational outcome planners are judged on</td></tr>
<tr><td>Spoilage or markdown rate</td><td>Written-off or discounted volume</td><td>The cost of over-forecasting</td></tr>
<tr><td>Planner override rate</td><td>Share of forecasts manually amended</td><td>High override means the model is not trusted</td></tr>
</tbody>
</table>
<p>Report all five, and be honest when a signal does not help. Some signals work beautifully for one category and are pure noise for another, and the credibility gained from saying so is what earns the planning team's cooperation on the next experiment. Forecast improvement is cumulative: the teams that run one disciplined signal evaluation per quarter compound gains, while the teams that demand a full platform before measuring anything end up with an expensive system whose accuracy nobody can explain.</p>
"""

H2FIX = {
    "EN": [
        ("beyond-historical-data-the-external-signal-advantage", "What Is the Advantage of External Signals Beyond Historical Data?"),
        ("the-mcp-integration-architecture-for-external-signals", "What MCP Integration Architecture Do External Signals Need?"),
        ("conversational-bi-for-forecast-intelligence", "How Does Conversational BI Deliver Forecast Intelligence?"),
        ("implementation-strategy-and-roi", "What Implementation Strategy Delivers ROI?"),
    ],
    "CN": [
        ("ai预测的核心优势", "AI 预测的核心优势是什么？"),
        ("从天气预测到业务预测", "如何从天气预测走向业务预测？"),
        ("预测系统的实施挑战", "预测系统的实施挑战有哪些？"),
        ("从试点到规模化生产的路径", "从试点到规模化生产的路径如何规划？"),
        ("技术基础设施与实施考量", "技术基础设施与实施考量是什么？"),
        ("组织准备与能力建设", "组织准备与能力建设如何推进？"),
        ("roi衡量与商业论证", "ROI 衡量与商业论证如何构建？"),
        ("风险管理与合规框架", "风险管理与合规框架如何建立？"),
    ],
    "TW": [
        ("the-mcp-integration-architecture-for-external-signals", "What MCP Integration Architecture Do External Signals Need?"),
        ("conversational-bi-for-forecast-intelligence", "How Does Conversational BI Deliver Forecast Intelligence?"),
        ("implementation-strategy-and-roi", "What Implementation Strategy Delivers ROI?"),
        ("規模化推廣的關鍵成功因素", "規模化推廣的關鍵成功因素有哪些？"),
        ("技術基礎設施與實施考量", "技術基礎設施與實施考量是什麼？"),
        ("中國市場特有的實施優勢", "中國市場特有的實施優勢有哪些？"),
        ("規模化推廣的關鍵成功因素-2", "規模化推廣的關鍵成功因素有哪些？"),
    ],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD}, tag=SLUG[:24])
