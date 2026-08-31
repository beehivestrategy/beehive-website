import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "voice-interface-enterprise-analytics-accessibility"

EN_ADD = """
<h2 id="which-work-contexts-genuinely-benefit-from-voice">Which Work Contexts Genuinely Benefit From Voice?</h2>
<p>Voice is not a universal upgrade; it is the right interface for a specific set of conditions, and naming those conditions is the difference between a deployment people use and one they try once. Three conditions predict success: the user's hands or eyes are occupied, the question is short and recurring, and the answer can be expressed in a sentence. When all three hold, voice beats every screen-based alternative. When any one fails — a complex exploratory question, a quiet desk, a need for visual comparison — voice is friction rather than convenience.</p>
<p>That filter maps cleanly onto roles. Warehouse and logistics supervisors asking for stock levels, shipment status, or exception counts are the canonical fit: hands busy, questions repeated dozens of times a day, answers short. Field service engineers asking for parts availability, job history, or the next appointment fit the same pattern. Healthcare staff asking for bed occupancy or staff allocation fit on the hands-busy dimension and add an infection-control argument for touch-free interaction. Executives asking for a figure before a meeting fit on the brevity dimension but require strict confidentiality controls, because the query often happens in a shared space.</p>
<table class="article-table">
<thead><tr><th>Context</th><th>Constraint</th><th>Design implication</th></tr></thead>
<tbody>
<tr><td>Warehouse floor</td><td>Hands busy, high ambient noise</td><td>Noise suppression; push-to-talk; short answers</td></tr>
<tr><td>Field service</td><td>Outdoor noise, intermittent connectivity</td><td>Offline-tolerant requests; confirm-before-action</td></tr>
<tr><td>Healthcare ward</td><td>Touch-free requirement, privacy</td><td>Wake-word activation; no sensitive data spoken aloud by default</td></tr>
<tr><td>Executive mobile</td><td>Shared physical space</td><td>Confidentiality filter; offer screen-only answers for sensitive classes</td></tr>
<tr><td>Retail floor</td><td>Customer present</td><td>Whisper mode; numerical answers only</td></tr>
<tr><td>Desk-based analyst</td><td>Complex exploratory questions</td><td>Voice as an entry point; screen for the actual analysis</td></tr>
</tbody>
</table>
<h2 id="how-do-you-design-a-voice-response-people-can-act-on">How Do You Design a Voice Response People Can Act On?</h2>
<p>Voice output obeys different rules from visual output because working memory, not screen space, is the constraint. A dashboard can show twenty numbers and let the reader scan; a voice answer that lists twenty numbers will be forgotten by the fifth. The design target is a response that fits in roughly thirty seconds of speech, leads with the answer, and offers the detail as a follow-up rather than including it.</p>
<p>Four rules get you there. Lead with the number and its direction — "On-hand stock for SKU 4471 is 1,860 units, down 12 percent since Monday" — rather than restating the question. Round aggressively and say that you rounded, because a spoken figure with false precision is worse than an approximate one. Name the period and the source explicitly, since the listener cannot see a header. And end with a single next step or offer, not a menu: "Want the breakdown by depot?" gives the listener one decision, whereas a list of five options exceeds what anyone retains from speech.</p>
<table class="article-table">
<thead><tr><th>Design rule</th><th>Poor voice response</th><th>Effective voice response</th></tr></thead>
<tbody>
<tr><td>Lead with the answer</td><td>"You asked about stock for SKU 4471..."</td><td>"1,860 units, down 12 percent since Monday."</td></tr>
<tr><td>Round and disclose</td><td>"1,860.4 units"</td><td>"About 1,860 units."</td></tr>
<tr><td>State period and source</td><td>Implicit</td><td>"As of 09:00, from the warehouse system."</td></tr>
<tr><td>One next step</td><td>Five follow-up options listed</td><td>"Want the breakdown by depot?"</td></tr>
<tr><td>Confirm before action</td><td>"I have reordered 500 units."</td><td>"Shall I raise a replenishment request for 500?"</td></tr>
<tr><td>Fail audibly</td><td>Silence or a generic error</td><td>"I could not reach the warehouse system. Try again shortly."</td></tr>
</tbody>
</table>
<p>Error handling deserves disproportionate attention, because voice errors are more costly than visual ones: there is no transcript to re-read, and a misunderstood number is remembered as fact. The system should always say what it heard before acting on it, should repeat numbers back digit by digit for any action with financial or safety consequence, and should never guess silently. Those three habits cost a few seconds per interaction and prevent nearly every class of serious voice misuse.</p>
<h2 id="what-accuracy-and-latency-budgets-are-realistic">What Accuracy and Latency Budgets Are Realistic?</h2>
<p>Voice analytics fails on perceived slowness long before it fails on accuracy. Users tolerate a wrong answer they can correct; they abandon an interface that makes them wait. The whole round trip — wake word, capture, transcription, understanding, query, and spoken response — needs to land inside about two seconds for a simple question, because conversational turn-taking breaks down beyond that and users start talking over the system.</p>
<p>That budget decomposes roughly as follows: capture and endpoint detection around 300 milliseconds, transcription 300 to 600, natural-language understanding and semantic resolution 150 to 300, query execution 200 to 800 depending on the warehouse, and speech synthesis 200 to 400. The largest controllable component is usually query execution, which is why a semantic layer with pre-aggregated, purpose-built models matters as much here as anywhere else — voice exposes data latency more brutally than any dashboard, because there is no loading spinner to hide behind.</p>
<table class="article-table">
<thead><tr><th>Stage</th><th>Typical budget</th><th>Improvement lever</th></tr></thead>
<tbody>
<tr><td>Capture and endpointing</td><td>~300 ms</td><td>Push-to-talk instead of open microphone</td></tr>
<tr><td>Transcription</td><td>300-600 ms</td><td>Streaming ASR; domain vocabulary hints</td></tr>
<tr><td>Understanding and resolution</td><td>150-300 ms</td><td>Cached semantic mappings for frequent intents</td></tr>
<tr><td>Query execution</td><td>200-800 ms</td><td>Pre-aggregated models; result caching</td></tr>
<tr><td>Speech synthesis</td><td>200-400 ms</td><td>Pre-generated phrases for common numeric patterns</td></tr>
</tbody>
</table>
<p>On accuracy, measure the outcomes that matter rather than the vendor's word error rate. Transcription word error rate matters less than intent accuracy, and intent accuracy matters less than answer accuracy — the share of spoken questions that produced a correct, acted-upon answer. Track all three, but hold the programme to the third, because a system that transcribes perfectly and resolves the wrong metric is still useless.</p>
"""

H2FIX = {
    "EN": [
        ("the-limits-of-traditional-bi-and-the-case-for-change", "What Are the Limits of Traditional BI and the Case for Change?"),
        ("core-technology-components", "What Are the Core Technology Components?"),
        ("implementation-strategy-and-best-practices", "What Implementation Strategy and Best Practices Work?"),
        ("in-depth-analysis-of-conversational-bi-technical-architecture", "What Does an In-Depth Analysis of Conversational BI Architecture Show?"),
    ],
    "CN": [
        ("传统bi的局限性与变革的理由", "传统 BI 的局限性与变革的理由是什么？"),
        ("核心技术组件", "核心技术组件有哪些？"),
        ("实施策略与最佳实践", "实施策略与最佳实践如何落地？"),
        ("对话式bi的进阶能力与未来演进", "对话式 BI 的进阶能力与未来演进是什么？"),
        ("对话式bi技术架构深度解析", "对话式 BI 技术架构应如何深度解析？"),
        ("战略实施路径与关键成功因素", "战略实施路径与关键成功因素是什么？"),
        ("企业实施路线图与成功因素", "企业实施路线图与成功因素有哪些？"),
        ("行业数字化转型深度分析", "行业数字化转型的深度分析是什么？"),
    ],
    "TW": [
        ("傳統bi的局限性與變革的理由", "傳統 BI 的局限性與變革的理由是什麼？"),
        ("核心技術組件", "核心技術組件有哪些？"),
        ("實施策略與最佳實踐", "實施策略與最佳實踐如何落實？"),
        ("對話式bi的進階能力與未來演進", "對話式 BI 的進階能力與未來演進是什麼？"),
        ("對話式bi技術架構深度解析", "對話式 BI 技術架構應如何深度解析？"),
        ("戰略實施路徑與關鍵成功因素", "戰略實施路徑與關鍵成功因素是什麼？"),
        ("企業實施路線圖與成功因素", "企業實施路線圖與成功因素有哪些？"),
        ("行業數位轉型深度分析", "行業數位轉型的深度分析是什麼？"),
    ],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD}, tag=SLUG[:24])
