# -*- coding: utf-8 -*-
"""Batch 2 content: slugs 6-10."""

S6 = "llm-orchestration-patterns-enterprise-production"

S6_EN_ADD = """
<h2 id="which-failure-modes-break-orchestration-in-production">Which Failure Modes Break Orchestration in Production?</h2>
<p>Orchestration failures are rarely model failures. The model produces something plausible; the workflow around it mishandles that output. Four failure modes account for most production incidents, and each has a specific structural defence.</p>
<p><strong>Non-idempotent tool calls.</strong> A workflow step that creates a record, sends a message, or moves money will eventually run twice — because of a retry, a timeout that was not actually a failure, or a user double-submitting. The defence is an idempotency key derived from the logical operation, not the request, plus a written policy for each tool: safe to retry, requires deduplication, or requires human confirmation. Teams that classify every tool this way before launch avoid the class of incident that is hardest to detect and most expensive to unwind.</p>
<p><strong>Silent degradation of retrieval.</strong> When retrieval returns slightly worse context, the model's answer remains fluent and becomes wrong. There is no error to catch. The defence is groundedness evaluation on a golden dataset with every deployment: does the answer cite the retrieved data, and does the cited data actually support the claim? Without that check, quality regressions ship silently and surface weeks later as user complaints.</p>
<p><strong>Context overflow under load.</strong> A workflow that works in testing with five documents fails in production with fifty, and the failure is a truncated prompt that produces a confident partial answer. The defence is explicit token budgeting per step, with a defined truncation policy — summarise, rank-and-select, or escalate to a human — rather than letting the framework silently drop content.</p>
<p><strong>Unbounded autonomy.</strong> The agent loops, or takes an action outside its intended scope, because nothing in the system caps iteration count, spend, or blast radius. The defence is boring and essential: maximum step counts, per-run cost ceilings, an allowlist of callable tools scoped to the specific workflow, and a mandatory human approval gate on any action that is externally visible or financially material.</p>
<h2 id="how-should-cost-latency-and-reliability-be-balanced">How Should Cost, Latency and Reliability Be Balanced?</h2>
<p>These three form a triangle, and the correct setting depends on what the workflow is for. An internal analytics assistant answering a finance director's question can take four seconds and cost a few cents; a customer-facing assistant handling thousands of concurrent sessions cannot. Naming the constraint explicitly at design time prevents the two most common mistakes: over-engineering for latency nobody cares about, and under-engineering for reliability on a path that touches money.</p>
<p>Three levers do most of the work. <strong>Model tiering</strong> — route by difficulty rather than sending everything to the largest model. In practice, 60-80% of enterprise requests are classification, extraction, or simple lookup that a small model handles identically well at a fraction of the cost, and a lightweight router that distinguishes "simple" from "requires reasoning" typically cuts spend by half with no measurable quality loss on the routed-easy portion. <strong>Caching at the right layer</strong> — semantic caching of retrieval results and of complete answers for repeated questions produces the largest single cost reduction in most deployments, because enterprise question distributions are heavily repetitive. <strong>Streaming</strong> — for interactive use, time-to-first-token matters more than total latency; a system that starts answering in 300 milliseconds feels faster than one that is complete in 800.</p>
<p>Reliability is where the sequencing advice from the opening of this article pays off. Idempotency, retries with backoff, checkpointing of long-running workflows, and dead-letter queues for failed runs are not optimisations to add later; they are the reason a system can be operated. Teams that build them first report dramatically less time spent on incident response after launch, which is the real cost centre in production LLM systems.</p>
<h2 id="what-does-a-production-ready-stack-include">What Does a Production-Ready Orchestration Stack Include?</h2>
<p>Beyond the orchestration framework itself, six components separate a demo from an operable system:</p>
<ul>
<li><strong>An evaluation harness</strong> — a golden dataset of 100-500 representative cases with known-good answers, run automatically on every change, with regression gates that block deployment. This is the single highest-leverage investment in the stack.</li>
<li><strong>Tracing</strong> — end-to-end visibility into every run: which route was taken, which tools were called, what was retrieved, how many tokens and how much money each step consumed. Without tracing, debugging an agent is guesswork.</li>
<li><strong>A prompt and policy registry</strong> — versioned, reviewable, and deployable independently of application code, because prompt changes are the most frequent source of behaviour change and need the same discipline as code.</li>
<li><strong>A human-in-the-loop gateway</strong> — a defined approval surface for high-stakes actions, with clear escalation routing and an audit record of who approved what.</li>
<li><strong>Cost attribution</strong> — spend tracked per workflow, per team, and per customer, so that unit economics are visible before they become a problem rather than after.</li>
<li><strong>A fallback path</strong> — what the system does when the model is unavailable, the retrieval index is stale, or confidence is below threshold. Systems without a designed fallback fail in whatever way is most convenient for the framework, which is rarely what the business wants.</li>
</ul>
<p>None of these are exotic, and none of them are the reason teams adopt orchestration frameworks. They are, however, consistently the reason some teams get to production and stay there while others stall at a convincing pilot.</p>
"""

S6_EN_FAQ = [
    ("Which orchestration pattern should an enterprise start with?",
     "Start with request routing, then wrap an orchestrator–workers pattern around your tools. Routing alone answers the 70-80% of requests that are simple lookups cheaply and quickly, and the orchestrator layer adds multi-step capability only where it is needed. Add a supervisor or evaluator agent once you are running three or more specialist workers."),
    ("When is a multi-agent architecture actually worth the complexity?",
     "When the workflow genuinely decomposes into independent specialist tasks with different tools, different data access, or different failure handling — and when those tasks are numerous enough that a single orchestrator prompt becomes unmanageable. Below three specialists, the coordination overhead usually exceeds the benefit."),
    ("How do you evaluate whether an LLM workflow is working?",
     "Maintain a golden dataset of 100-500 representative cases with known-good answers and re-run it on every change. Track regression rate, groundedness (does the answer cite retrieved data that actually supports it), latency percentiles, and cost per resolved task. Evaluation, not intuition, is what makes an agent safe to change."),
    ("What is the most common cause of production incidents in agent systems?",
     "Non-idempotent tool calls. A step that creates, sends, or spends will eventually execute twice because of a retry or a timeout misclassification. Classify every tool as safe-to-retry, requires-deduplication, or requires-human-confirmation, and pass an idempotency key derived from the logical operation."),
    ("How much can model tiering reduce cost?",
     "Typically 40-60% of inference spend, because the majority of enterprise requests are classification, extraction or simple lookup that a smaller model handles identically well. A router that distinguishes simple from reasoning-heavy requests preserves quality on the hard cases while removing most of the cost of the easy ones."),
]

S6_ZH_FAQ = [
    ("企業應該從哪種編排模式開始？",
     "先做請求路由，再用編排者—工作者模式把工具包起來。路由單獨就能以低成本、低延遲處理70%至80%的簡單查詢請求；編排層只在需要時提供多步驟能力。當你運行三個以上的專業工作者時，再加入監督者或評估者代理。"),
    ("多代理架構在什麼情況下才值得它的複雜度？",
     "當工作流確實可以分解為相互獨立的專業任務，且這些任務使用不同的工具、不同的數據訪問權限或不同的失敗處理方式，同時任務數量多到單一編排提示詞已難以維護時。若少於三個專業工作者，協調開銷通常超過收益。"),
    ("如何評估一個LLM工作流是否正常運作？",
     "維護一份包含100到500個代表性案例、並帶有已知正確答案的黃金資料集，每次變更都自動重跑。追蹤回歸率、紮根性（答案是否引用了確實支持該結論的檢索數據）、延遲百分位，以及每個已解決任務的成本。讓代理可以安全變更的是評估，而不是直覺。"),
    ("代理系統在生產環境中最常見的事故原因是什麼？",
     "非冪等的工具調用。任何會新增、發送或扣款的步驟，最終都會因為重試或超時誤判而執行兩次。應把每個工具歸類為「可安全重試」「需要去重」或「需要人工確認」，並傳入由邏輯操作推導出的冪等鍵。"),
    ("模型分層能降低多少成本？",
     "通常可降低40%至60%的推理支出，因為企業請求的多數是分類、抽取或簡單查詢，較小的模型表現完全相同。用路由器區分「簡單」與「需要推理」的請求，可以在保留困難案例質量的同時，消除大部分簡單請求的成本。"),
]

S6_CN_H2 = [
    ("理解当前技术格局", "企业LLM编排的技术格局是怎样的？"),
    ("技术架构与集成模式", "常见的集成模式有哪些？"),
    ("性能基准与优化策略", "性能优化应该从哪些方面入手？"),
    ("企业部署最佳实践与实施建议", "企业部署有哪些最佳实践？"),
    ("企业实施路线图与成功因素", "企业实施路线图应该如何规划？"),
    ("战略实施路径与关键成功因素", "战略实施路径与关键成功因素是什么？"),
    ("企业实施路线图与成功因素", "实施过程中有哪些常见失败模式？"),
]
S6_TW_H2 = [
    ("理解當前技術格局", "企業LLM編排的技術格局是怎樣的？"),
    ("技術架構與整合模式", "常見的整合模式有哪些？"),
    ("效能基準與最佳化策略", "效能最佳化應該從哪些方面入手？"),
    ("企業部署最佳實踐與實施建議", "企業部署有哪些最佳實踐？"),
    ("企業實施路線圖與成功因素", "企業實施路線圖應該如何規劃？"),
    ("戰略實施路徑與關鍵成功因素", "戰略實施路徑與關鍵成功因素是什麼？"),
    ("企業實施路線圖與成功因素", "實施過程中有那些常見失敗模式？"),
]

# ---------------------------------------------------------------- slug 7
S7 = "supply-chain-demand-forecasting-ai"

S7_EN_ADD = """
<h2 id="how-should-forecast-accuracy-be-governed">How Should Forecast Accuracy Be Governed?</h2>
<p>Forecast accuracy is not a single number, and treating it as one is why so many programmes argue about quality instead of improving it. A governance model that works has four parts: the right error metric for the right decision, a bias check alongside the error check, an explicit exception process, and a written record of who overrode the model and why.</p>
<p>Error metric first. Weighted mean absolute percentage error is standard, but the weighting should follow the decision, not convention: if the decision is replenishment of high-volume items, weight by volume; if it is safety-stock sizing for long-tail items, weight by service-level impact. Reporting one unweighted number across a mixed portfolio hides both problems. Alongside the error measure, track bias — whether the forecast systematically over- or under-predicts — because bias is what quietly inflates inventory or causes stockouts while the absolute error looks stable.</p>
<p>The exception process matters more than most teams expect. No forecasting model handles promotions, supplier disruptions, or a competitor's exit well, and the planner who knows a promotion is coming will be right where the model is wrong. The system needs a first-class way to record a planned override, with a reason code, and it needs to keep the model's original output alongside the adjusted one. That record is what makes the next model iteration possible: without it, the training data silently contains the planners' adjustments and the model learns to predict its own corrections.</p>
<h3>Why the override log is the most valuable artefact</h3>
<p>Teams that maintain a clean override log learn things no accuracy dashboard shows. They discover which products are structurally unforecastable and should be managed with different policies. They find the categories where the model is systematically conservative, and can correct it. Most importantly, they can distinguish the two very different problems that both present as "bad forecast": a model that lacks signal, and a planning process that does not trust the model. These need opposite interventions, and without the log they are indistinguishable.</p>
<h2 id="how-do-you-embed-a-forecast-in-weekly-planning">How Do You Embed a Forecast in Weekly Planning?</h2>
<p>A forecast that is produced but not used is the most common outcome of AI forecasting programmes, and the cause is almost always workflow rather than accuracy. Planners have an existing ritual — usually a Monday review of a spreadsheet they built — and a new number in a new tool does not displace it. Embedding means changing the ritual, not adding an artefact.</p>
<p>The sequence that works starts by joining the existing review rather than replacing it. Bring the model's output into the meeting, alongside the planner's number, and discuss the difference. In the first month this is uncomfortable and enormously informative: the disagreements are exactly the places where local knowledge beats the model or vice versa. By the second month, define the default — the model's number stands unless overridden with a reason code — and the meeting shifts from reconciling two numbers to discussing exceptions.</p>
<p>Two design details determine whether this sticks. The first is latency: if the planner has to request a refreshed forecast and wait, they will use their own number. The forecast has to be there when the meeting starts, every week, without anyone asking. The second is explainability at the point of use: when a planner challenges a number, they need to see which inputs moved it — a promotion, a lead-time change, a shift in the demand signal — in the same screen, not in a report they have to request from an analyst.</p>
<p>The measurable outcome of a well-embedded forecast is not accuracy; it is the share of planning decisions made on the model's number without override, plus the time spent per planning cycle. Programmes that track those two see planner hours per cycle fall substantially while service levels hold, and that combination — not the error metric — is what funds expansion to the next product family.</p>
"""

S7_EN_FAQ = [
    ("How quickly can an AI forecasting programme show value?",
     "Most organisations see measurable improvements in forecast error and planner productivity within two to three months of a focused pilot, provided the scope is one decision and one data domain. Scaling across a full product portfolio typically takes twelve to eighteen months, and the constraint is usually data integration rather than modelling."),
    ("How much can AI forecasting reduce forecast error?",
     "Enterprises that scale machine-learning forecasting report 20-50% reductions in forecast error, around 15% lower logistics costs, and 35-75% improvement in inventory levels. Those ranges depend heavily on starting maturity: organisations moving from spreadsheet judgement see the largest gains, while those already running statistical baselines see smaller but still material improvements."),
    ("What data does an AI demand forecast need?",
     "At minimum, demand history with sufficient granularity, the promotional calendar, lead times by supplier and lane, current inventory positions, and product attributes. The most common failure is missing the causal signals — promotions, price changes, weather, competitor activity — because these usually live in systems outside the ERP."),
    ("Should planners be able to override the forecast?",
     "Yes, and the override must be recorded with a reason code. Planners hold local knowledge the model cannot see, particularly around promotions and supplier behaviour. The discipline is to keep the model's original output alongside the adjusted figure so the override log becomes training signal rather than invisible correction."),
    ("What is the most common reason forecasting programmes stall?",
     "The forecast is produced but not embedded in the weekly planning ritual, so planners keep using their own numbers. Programmes that join the existing review, make the model's number the default, and require reason-coded overrides to change it reach sustained adoption; programmes that publish a dashboard alongside existing practice do not."),
]

S7_ZH_ADD = """
<h2 id="需求預測的準確率應該如何治理">需求預測的準確率應該如何治理？</h2>
<p>預測準確率不是單一數字；把它當成單一數字，正是許多專案忙於爭論質量而非改善質量的原因。一套有效的治理模型包含四個部分：為不同決策選擇合適的誤差指標、在誤差之外同時檢視偏差、建立明確的例外覆寫流程，以及記錄誰在何時以什麼理由覆寫了模型。</p>
<p>首先是誤差指標。加權平均絕對百分比誤差是常用標準，但權重應跟隨決策而非慣例：如果決策是為高銷量品補貨，就按銷量加權；如果決策是為長尾品設定安全庫存，就按服務水平影響加權。在混合的產品組合上只報告一個未加權的數字，會同時掩蓋這兩類問題。在誤差之外，還必須追蹤偏差——預測是否系統性地偏高或偏低——因為當絕對誤差看起來穩定時，偏差正是悄悄推高庫存或造成缺貨的原因。</p>
<p>例外流程的重要性超出多數團隊的預期。沒有任何預測模型能很好地處理促銷、供應商中斷或競爭對手退出，而知道促銷即將到來的規劃人員，在這些時刻往往比模型更準確。系統需要一個正式的機制來記錄計畫中的覆寫，並附帶原因代碼，同時保留模型的原始輸出。這份記錄讓下一次模型迭代成為可能：缺少它，訓練數據就會悄悄包含規劃人員的調整，模型等於在學習預測自己的修正值。</p>
<h3>為什麼覆寫日誌是最有價值的產出</h3>
<p>維持乾淨覆寫日誌的團隊，會學到任何準確率儀表板都看不到的東西。他們能發現哪些產品在結構上不可預測，因而應該用不同的策略管理；能找出模型系統性保守的品類並加以修正。更重要的是，他們能區分兩種都表現為「預測不準」但性質截然不同的問題：模型缺乏信號，以及規劃流程不信任模型。這兩者需要相反的措施，而沒有日誌就無法分辨。</p>
<h2 id="如何把預測嵌入每週的規劃流程">如何把預測嵌入每週的規劃流程？</h2>
<p>產生了預測卻無人使用，是AI需求預測專案最常見的結果，而原因幾乎總在流程而非準確率。規劃人員已有既定做法——通常是週一檢視一份自己建立的試算表——而新工具裡的新數字並不會自動取代它。所謂嵌入，是改變這個做法，而不是多增加一份產出。</p>
<p>有效的做法是先加入既有的複盤會議，而不是取代它。把模型的輸出帶進會議，與規劃人員的數字並列，討論兩者的差異。第一個月會有些不適應，但收穫極大：分歧之處，正是本地知識勝過模型或反之的地方。到第二個月，定義預設規則——模型的數字成立，除非以原因代碼覆寫——會議便從核對兩個數字，轉為討論例外情況。</p>
<p>兩個設計細節決定這套做法能否持續。第一是延遲：如果規劃人員必須提出請求並等待刷新，他們就會用自己的數字。預測必須在每週會議開始時就已經在那裡，不需要任何人開口。第二是使用現場的可解釋性：當規劃人員質疑某個數字時，他們需要在同一個畫面看到是哪些輸入推動了它——促銷、前置時間變化、需求信號的偏移——而不是要向分析師索取一份報告。</p>
<p>嵌入良好的預測，其可衡量的成果不是準確率，而是在未覆寫情況下直接採用模型數字的規劃決策佔比，以及每個規劃週期所花費的時間。追蹤這兩項的專案，會看到每週期的規劃工時大幅下降而服務水平維持不變；正是這個組合——而不是誤差指標——支撐著向下一個產品系列的擴展。</p>
"""

S7_ZH_FAQ = [
    ("AI需求預測專案多久能看到價值？",
     "多數企業在聚焦的試點開始後兩到三個月內，就能在預測誤差與規劃人員效率上看到可衡量的改善，前提是範圍限定為一個決策與一個數據域。擴展到完整產品組合通常需要十二到十八個月，而瓶頸通常是數據整合而非建模。"),
    ("AI預測能把預測誤差降低多少？",
     "規模化應用機器學習預測的企業報告預測誤差降低20%至50%、物流成本下降約15%、庫存水平改善35%至75%。這些區間很大程度取決於起點成熟度：從試算表判斷起步的企業收益最大；已經運行統計基線的企業改善幅度較小但仍相當可觀。"),
    ("AI需求預測需要哪些數據？",
     "至少需要足夠精細的需求歷史、促銷日曆、按供應商與線路區分的前置時間、當前庫存狀況，以及產品屬性。最常見的失敗是缺少因果信號——促銷、價格變動、天氣、競爭對手動態——因為這些數據通常存在於ERP之外的系統中。"),
    ("規劃人員是否應該能夠覆寫預測？",
     "應該，且覆寫必須附帶原因代碼記錄下來。規劃人員掌握模型看不到的本地知識，尤其在促銷與供應商行為方面。關鍵紀律是保留模型的原始輸出與調整後數值並列，使覆寫日誌成為訓練信號，而不是看不見的修正。"),
    ("預測專案停滯最常見的原因是什麼？",
     "預測被產生但沒有嵌入每週的規劃流程，規劃人員因此繼續使用自己的數字。加入既有複盤會議、讓模型的數字成為預設值、並要求以原因代碼覆寫的專案，才能達到持續採用；只是在既有做法旁邊發布儀表板的專案則做不到。"),
]

S7_CN_H2 = [
    ("为什么重要", "为什么AI需求预测如此重要？"),
    ("常见挑战", "导入AI需求预测有哪些常见挑战？"),
    ("如何开始", "企业应该如何开始导入AI需求预测？"),
    ("核心要点", "本文的核心要点是什么？"),
]
S7_TW_H2 = [
    ("匯入AI需求預測的常見挑戰有哪些？", "導入AI需求預測有哪些常見挑戰？"),
    ("企業應該如何開始匯入？", "企業應該如何開始導入AI需求預測？"),
]

# ---------------------------------------------------------------- slug 8
S8 = "multi-turn-conversations-in-bi-how-ai-maintains-context"

S8_EN_ADD = """
<h2 id="how-should-conversation-state-be-modelled">How Should Conversation State Be Modelled?</h2>
<p>Externalising memory is the right instinct, but an ad-hoc state object tends to accrete fields until nobody is sure which one is authoritative. A cleaner model treats the conversation state as a small, typed structure with four slots, each of which has an explicit precedence rule when a new turn arrives.</p>
<ul>
<li><strong>Subject</strong> — the metric or measure under discussion: revenue, margin, headcount, units shipped. A new turn that names a metric replaces the subject; a turn that does not leaves it in place.</li>
<li><strong>Dimensions and filters</strong> — region, channel, product, time period, and any explicit constraints. These are the most frequently modified part of the state, and they are what "by month" or "only for Shanghai" actually changes.</li>
<li><strong>Operation</strong> — comparison, ranking, trend, decomposition, or threshold check. This is the part most state models omit, and its absence is why an assistant that handled "compare to last year" well then fails on "which regions are worst?"</li>
<li><strong>Result pointers</strong> — references to the previous result sets, so that "of those, which grew fastest?" can be resolved without re-running the original query.</li>
</ul>
<p>The precedence rule matters more than the structure. When a user says "now break that down by channel, but only for the top three regions," three slots change at once and one stays. Systems that resolve slot-by-slot with a defined order — filters before dimensions, dimensions before subject — behave predictably; systems that re-derive the whole state from the latest utterance produce the erratic behaviour users describe as the assistant "losing the thread."</p>
<h2 id="what-breaks-multi-turn-conversations-in-practice">What Breaks Multi-Turn Conversations in Practice?</h2>
<p>Beyond context-window exhaustion, four specific problems recur in production deployments, and each is solvable with a specific technique.</p>
<p><strong>Ambiguous numeric references.</strong> "What about last year?" could mean the same period last year, the full prior year, or a year-over-year comparison at the current granularity. Rather than guessing, the highest-quality behaviour is to resolve the most probable interpretation, state it explicitly in the answer ("same period last year, January to March"), and offer the alternatives. Stating the interpretation costs one sentence and eliminates most silent misinterpretation.</p>
<p><strong>Drill-down chains that exceed the schema.</strong> A user asks for revenue by region, then by city, then by store, then by product — and the fourth level does not exist at that granularity. The correct response is not an error or a hallucinated chart but a graceful boundary statement: what the finest available granularity is, and an offer to approximate it. Handling the edge of the schema well is a large part of what makes an assistant feel competent.</p>
<p><strong>Topic drift inside a single thread.</strong> A conversation about margins slides into a conversation about headcount and back again. Topic detection should therefore be soft rather than binary: maintain a stack of analytical contexts rather than a single one, so that returning to a previous topic restores its state instead of starting again.</p>
<p><strong>Permission leakage across turns.</strong> As the conversation state accumulates filters and entities, it can accumulate access to data the user should not see in combination — a filter that was legitimate in one context exposing an aggregation that is not permitted in another. Every resolved query must be re-authorised against the full accumulated state, not just against the newest turn.</p>
<h2 id="how-do-you-test-a-multi-turn-assistant">How Do You Test a Multi-Turn Assistant?</h2>
<p>Single-turn evaluation misses most of what goes wrong. The unit of testing has to be the conversation, not the question, and the practical approach is a scripted dialogue suite: twenty to fifty multi-turn transcripts covering the patterns users actually produce — refinement, drill-down, comparison, topic switch, return, and correction — each with known-good final states and expected answers.</p>
<p>Three metrics come out of running that suite. <strong>State accuracy</strong>: after N turns, does the resolved query specification match the expected one? <strong>Answer accuracy at depth</strong>: accuracy measured separately at turn one, turn five, and turn fifteen, because the whole point of the architecture is that accuracy should not degrade with depth — if it does, the externalised state is not working. <strong>Recovery rate</strong>: when the user corrects the assistant ("no, I meant by quarter"), how often does the next turn get it right?</p>
<p>Add one production signal that is cheap and highly diagnostic: the rate at which users abandon a thread and start a new one. High abandonment after three or four turns is the clearest indicator that context handling is failing, and it is visible in logs without any labelling effort.</p>
"""

S8_EN_FAQ = [
    ("Why does a BI assistant lose context after a few turns?",
     "Because the full conversation history is being replayed into the context window, which is a finite resource. After five to ten turns, earlier content is truncated or crowded out, and the model begins answering as if the earlier turns never happened. The fix is to externalise state into a structured object and send only a compact summary with each new turn."),
    ("How should conversation state be structured?",
     "As four typed slots with explicit precedence rules: the subject (the metric under discussion), dimensions and filters, the operation (comparison, ranking, trend, decomposition), and pointers to previous result sets. Resolving each slot in a defined order is what makes follow-ups behave predictably."),
    ("How does an AI resolve references like 'that' or 'by month'?",
     "By maintaining an entity graph of the metrics, dimensions and filters introduced so far, and resolving pronouns and elliptical phrases against it. Deterministic resolution against a structured state is far more reliable than asking the model to infer the referent from raw history, and it makes the resolution auditable."),
    ("When should the conversation context be reset?",
     "On a detected topic shift — when the user moves from one analytical subject to an unrelated one. Best practice is a stack of contexts rather than a single one, so that returning to an earlier topic restores its state instead of starting from scratch, and history remains retrievable even after a reset."),
    ("How do you test whether multi-turn context handling works?",
     "Test conversations, not questions. Build a suite of 20-50 scripted multi-turn transcripts covering refinement, drill-down, comparison, topic switch and correction, and measure state accuracy, answer accuracy at turn one versus turn five versus turn fifteen, and recovery rate after a user correction."),
]

S8_ZH_ADD = """
<h2 id="對話狀態應該如何建模">對話狀態應該如何建模？</h2>
<p>把記憶外部化是正確的方向，但臨時拼湊的狀態物件往往不斷新增欄位，最後沒人確定哪一個才是權威來源。更乾淨的做法，是把對話狀態視為一個小而帶型別的結構，包含四個槽位，每個槽位在新的一輪到來時都有明確的優先順序規則。</p>
<ul>
<li><strong>主題</strong>——當前討論的指標或度量：營收、毛利、員工人數、出貨量。新的一輪若明確說出指標就替換主題；若沒有，則維持不變。</li>
<li><strong>維度與篩選條件</strong>——地區、渠道、產品、時間區間，以及任何明確的限制。這是狀態中最常被修改的部分，也正是「按月」或「只要上海」實際改變的內容。</li>
<li><strong>操作</strong>——比較、排序、趨勢、分解或閾值檢查。這是多數狀態模型遺漏的部分；正因缺少它，能處理好「跟去年同期比」的助理，卻會在「哪些地區表現最差？」上失敗。</li>
<li><strong>結果指標</strong>——指向先前結果集的引用，使「在這些當中，哪些成長最快？」無需重跑原始查詢即可求解。</li>
</ul>
<p>優先順序規則比結構更重要。當使用者說「現在按渠道拆分，但只看前三大地區」，三個槽位同時改變，一個維持不變。以定義好的順序逐槽求解的系統——先篩選條件、再維度、最後主題——行為可預測；而每次都從最新一句重新推導整個狀態的系統，則會出現使用者所說「助理斷線了」的反覆無常行為。</p>
<h2 id="實務上多輪對話會在哪些地方出問題">實務上多輪對話會在哪些地方出問題？</h2>
<p>除了上下文視窗耗盡之外， production 部署中有四類問題反覆出現，每一類都有對應的解法。</p>
<p><strong>數字指涉的歧義。</strong>「那去年呢？」可能指去年同期、上一個完整年度，或在當前粒度下做年增比較。與其猜測，更好的做法是解析最可能的解讀，在答案中明確說明（「去年同期，一月到三月」），並提供其他選項。說明解讀只需一句話，卻能消除大部分靜默的誤解。</p>
<p><strong>下鑽鏈超過schema範圍。</strong>使用者依序要求按地區、城市、門市、產品拆分，而第四層在該粒度下並不存在。正確的回應不是報錯，也不是幻化出一張圖表，而是優雅地說明邊界：目前可用的最細粒度是什麼，以及是否願意用近似方式呈現。妥善處理schema的邊界，是讓助理顯得專業的重要部分。</p>
<p><strong>單一對話中的主題漂移。</strong>一段關於毛利的對話滑向員工人數，之後又繞回來。因此主題偵測應是軟性而非二元的：維護一個分析上下文堆疊而非單一上下文，回到先前主題時就能恢復其狀態，而不是重新開始。</p>
<p><strong>跨輪次的權限洩漏。</strong>隨著對話狀態累積篩選條件與實體，它可能同時累積了使用者不應看到的數據訪問權——某個在一個上下文中合法的篩選條件，會暴露出在另一個上下文中不被允許的聚合結果。每一個求解出的查詢，都必須針對完整累積的狀態重新授權，而不是只針對最新一輪。</p>
<h2 id="如何測試多輪對話助理">如何測試多輪對話助理？</h2>
<p>單輪評估會漏掉大部分出問題的地方。測試單位必須是「對話」而非「問題」，實用的做法是建立腳本化的對話測試集：二十到五十段多輪對話腳本，涵蓋使用者實際會產生的模式——細化、下鑽、比較、切換主題、返回、修正——每段都帶有已知正確的最終狀態與預期答案。</p>
<p>執行這套測試集可以得到三項指標。<strong>狀態準確率</strong>：在第N輪之後，求解出的查詢規格是否與預期一致？<strong>深度上的答案準確率</strong>：分別在第一輪、第五輪、第十五輪衡量準確率，因為這套架構的重點正是準確率不應隨深度下降——若下降，說明外部化狀態沒有發揮作用。<strong>恢復率</strong>：當使用者修正助理時（「不，我是指按季」），下一輪能做對的比例有多高？</p>
<p>再補一個成本低但診斷價值高的生產訊號：使用者放棄當前對話並另開新對話的比例。在第三、四輪之後出現高放棄率，是上下文處理失敗最清晰的指標，而且無需任何標註就能在日誌中看見。</p>
"""

S8_ZH_FAQ = [
    ("為什麼BI助理在幾輪之後就會失去上下文？",
     "因為整套對話歷史被重複放入上下文視窗，而上下文視窗是有限的資源。五到十輪之後，較早的內容會被截斷或擠出，模型便開始像前面的對話從未發生過一樣回答。解法是把狀態外部化為結構化物件，每一輪只發送精簡的摘要。"),
    ("對話狀態應該如何結構化？",
     "分為四個帶型別的槽位並配備明確的優先順序規則：主題（當前討論的指標）、維度與篩選條件、操作（比較、排序、趨勢、分解），以及指向先前結果集的指標。依照定義好的順序逐槽求解，是讓追問行為可預測的關鍵。"),
    ("AI如何解析「那個」「按月」之類的指涉？",
     "透過維護一個實體圖，記錄迄今出現過的指標、維度與篩選條件，再據此解析代詞與省略語。對結構化狀態做確定性解析，遠比讓模型從原始歷史中推論指涉對象可靠，而且讓解析過程可被審計。"),
    ("什麼時候應該重置對話上下文？",
     "在偵測到主題切換時——使用者從一個分析主題轉向無關的另一個主題。較佳做法是維護上下文堆疊而非單一上下文，這樣回到先前主題時能恢復其狀態，而不必重新開始；即使重置，歷史仍應可被取回。"),
    ("如何測試多輪上下文處理是否正常？",
     "測試對話，而非單一問題。建立二十到五十段腳本化的多輪對話，涵蓋細化、下鑽、比較、主題切換與修正，並衡量狀態準確率、第一輪與第五輪及第十五輪的答案準確率，以及使用者修正後的恢復率。"),
]

S8_CN_H2 = [
    ("上下文窗口问题", "什么是上下文窗口问题？"),
    ("参考分辨率", "AI应该如何解析代词与省略指代？"),
    ("上下文窗口管理策略", "上下文窗口应该如何管理？"),
    ("何时重置上下文", "什么时候应该重置上下文？"),
    ("要点", "本文的核心要点是什么？"),
    ("结论", "设计多轮对话的下一步是什么？"),
]
S8_TW_H2 = [
    ("什麼是上下文視窗問題？", "什麼是上下文窗口問題？"),
    ("上下文視窗應該如何管理？", "上下文窗口應該如何管理？"),
    ("本文要點是什麼？", "本文的核心要點是什麼？"),
]

# ---------------------------------------------------------------- slug 9
S9 = "real-estate-ai-property-valuation"

S9_EN_FAQ = [
    ("How accurate are automated valuation models today?",
     "Automated valuation models now price homes within roughly 2% of eventual sale price in markets with good transaction data. Accuracy degrades sharply in thin markets, for unusual properties, and when comparable sales are stale, which is why production systems publish a confidence score and route low-confidence cases to human appraisal rather than reporting a single number."),
    ("What data does an AI valuation model need?",
     "Transaction history with sale prices and dates, property attributes (size, condition, type, age), location data at neighbourhood granularity, and the local market context that moves prices — interest rates, inventory levels, days-on-market. Programmes stall far more often on deduplicating and standardising these records than on model selection."),
    ("Is human oversight still required for AI valuations?",
     "Yes, for regulated use. Lenders must be able to explain and defend a valuation, which means a human appraiser reviews low-confidence or high-value cases, and the model's contribution is documented. The practical design is risk-based triage: automate the high-confidence, low-value cases and reserve human capacity for the ones that carry material risk."),
    ("How should an organisation start with AI property valuation?",
     "Start with a portfolio-level use case where risk is low and volume is high — bulk valuation for asset management, market trend analysis, or acquisition screening. Run the model alongside human appraisals for several months, compare results, and only then move to decision-grade use such as loan triage."),
    ("What are the main compliance risks in AI valuation?",
     "Model risk, where a model trained on one market regime fails in another; fair-lending risk, where proxy variables produce disparate outcomes across protected groups; and explainability risk, where the institution cannot explain a specific valuation to a regulator or a customer. Continuous backtesting, disparate-impact testing, and per-valuation reason codes address these directly."),
]

S9_ZH_ADD = """
<h2 id="AI估值的資料基礎應該如何準備">AI估值的數據基礎應該如何準備？</h2>
<p>在房地產估值專案中，數據準備的工作量通常佔整體投入的一半以上，而它也是決定模型能否上線的關鍵。與其追求更多的數據源，更務實的做法是把三類基礎資料做扎實。</p>
<p>第一類是交易記錄。需要包含成交價格、成交日期、產權類型與交易條件，並且要能被標準化：同一個物件在不同系統中可能有不同的地址寫法、不同的面積單位，甚至重複的記錄。重複記錄尤其危險，因為它會讓模型在訓練時看到自己的答案，從而在回測中表現極好、在實務中表現很差。第二類是物件屬性：面積、房齡、格局、樓層、裝修狀況、車位與景觀等。這些欄位的完整性往往比模型的複雜度更能決定誤差。第三類是區位與市場上下文：學區、交通可達性、商圈與生活機能，以及會推動價格的市場變數——利率、庫存量、平均銷售天數。</p>
<p>在準備過程中，有兩個判斷值得在做模型之前就做出來。其一是確定「可比物件」的定義規則，並把它寫成可重現的邏輯，因為估值的核心是比較，而比較的基礎必須一致。其二是為每一筆資料標記來源與更新時間，因為當某個估值被質疑時，能否追溯到具體的資料來源，決定了這個估值是否可被辯護。</p>
<h2 id="如何評估與監控一個估值模型">如何評估與監控一個估值模型？</h2>
<p>估值模型的評估不能只看平均誤差，因為誤差的分佈比平均值更重要。實務上應同時追蹤三層指標。營運層面看模型本身：中位絕對誤差、落在最終成交價5%以內的估價佔比、以及各區段與各價格帶的覆蓋率——覆蓋率低的區段往往正是模型最容易出錯的地方。業務層面看決策效果：人工複核的比例、平均核保或估價週期、以及每個案件的處理成本。風險層面看穩定性：不同市場環境下的回測表現，以及不同群體之間的結果差異。</p>
<p>監控的核心是「漂移」。房地產市場具有明顯的週期性，利率、庫存與政策的變化會改變價格形成的機制，而一個在過去兩年表現良好的模型，可能在新的環境下系統性高估或低估。因此必須設定固定的回測節奏——通常每月一次快速檢查、每季一次完整回測——並為誤差設定明確的警戒線：一旦超出，就自動降低自動化的比例，把更多案件轉入人工複核。</p>
<p>另一個常被忽略的監控項目是輸入的完整性。當某個資料源中斷或某個欄位的缺失率突然上升時，模型往往不會報錯，只會靜默地變差。把輸入欄位的缺失率與異常值比例納入日常監控，通常能在誤差指標惡化之前就發現問題。</p>
<h2 id="人機協作的估值流程應該如何設計">人機協作的估值流程應該如何設計？</h2>
<p>可落地的設計是風險導向的分流，而不是讓AI與人工各自獨立作業。具體做法是為每個估值計算一個置信度，並依置信度與案件金額決定處理路徑：高置信度且金額低的案件全自動通過；高置信度但金額高的案件自動產出、人工抽查；低置信度的案件一律轉人工，但AI提供初始值與可比物件清單作為參考。</p>
<p>這套流程要能運作，介面上必須支援三件事。第一是解釋性：估算人員要能看到這個估值是由哪些可比物件、哪些調整項得出的，而不是一個黑盒數字。第二是可修改性：估算人員要能調整可比物件或調整係數，並即時看到估值的變化。第三是留痕：每一次調整的內容與理由都必須被記錄，因為這些記錄既是合規要求，也是讓模型持續改進的訓練信號。</p>
<p>在導入順序上，先從風險低、批量大的場景開始——資產管理的批量估值、市場趨勢分析、或收購案的初步篩選——讓模型與人工鑑價並行幾個月，累積對照結果。當對照結果穩定且團隊對模型有足夠理解之後，再推進到決策級的用途，例如貸款的案件分流。這個順序既能控制風險，也能在組織內部逐步建立信任。</p>
"""

S9_ZH_FAQ = [
    ("自動估值模型目前的準確率如何？",
     "在交易數據完善的市場中，自動估值模型對住宅的估價與最終成交價的差距約在2%以內。但在交易稀薄的市場、特殊物件，以及可比成交案例過舊的情況下，準確率會明顯下降。因此生產環境中的系統應同時輸出置信度，並把低置信度的案件轉入人工鑑價，而不是只給出單一數字。"),
    ("AI估值模型需要哪些數據？",
     "需要含成交價格與日期的交易記錄、物件屬性（面積、狀況、類型、屋齡）、到鄰里粒度的區位資料，以及會推動價格的市場情境——利率、庫存量、平均銷售天數。專案停滯的原因，往往是這些記錄的去重與標準化，而不是模型選擇。"),
    ("AI估值是否仍需要人工監督？",
     "在受監管的用途中需要。金融機構必須能夠解釋並為估值辯護，這表示低置信度或高金額的案件需由人工鑑價師複核，且模型的貢獻必須被記錄。實務設計是風險導向的分流：自動化處理高置信度、低金額的案件，把人工產能留給風險重大的案件。"),
    ("企業應該如何開始導入AI物業估值？",
     "從風險低、批量大的場景開始——資產管理的批量估值、市場趨勢分析，或收購案的初步篩選。讓模型與人工鑑價並行數月並比較結果，穩定之後再推進到決策級用途，例如貸款案件的分流。"),
    ("AI估值的主要合規風險是什麼？",
     "模型風險：在某種市場環境下訓練的模型，在另一種環境下失效；公平授信風險：代理變數導致不同群體間的結果出現差異；可解釋性風險：機構無法向監管機構或客戶解釋某個具體估值。持續回測、差異影響測試，以及逐筆估值的原因代碼，可直接對應這些風險。"),
]

S9_CN_H2 = [
    ("理解当前格局", "AI物业估值的当前格局是什么？"),
    ("关键原则与战略框架", "AI估值的关键原则与战略框架是什么？"),
    ("实施方法与最佳实践", "企业应该如何实施AI估值？"),
    ("衡量成功与展示投资回报率", "如何衡量AI估值的投资回报？"),
    ("常见陷阱及规避方法", "AI估值有哪些常见陷阱？"),
    ("关键要点", "本文的关键要点是什么？"),
    ("结论", "企业导入AI估值的下一步是什么？"),
]
S9_TW_H2 = [
    ("企業匯入AI估值的下一步是什麼？", "企業導入AI估值的下一步是什麼？"),
]

# ---------------------------------------------------------------- slug 10
S10 = "anatomy-of-analytics-failure-metric-drift-and-trust-gaps"

S10_EN_ADD = """
<h2 id="how-do-you-detect-metric-drift-before-it-spreads">How Do You Detect Metric Drift Before It Spreads?</h2>
<p>Drift is invisible by construction: nobody announces that revenue now includes shipping. Detecting it therefore requires instrumentation rather than vigilance, and there are four signals that work.</p>
<p>The first is definitional versioning with a published changelog. Every metric definition lives in a versioned store; every change increments a version and produces an entry stating what changed, when, and who approved it. This does not prevent drift, but it converts silent drift into a visible event. The second is distributional monitoring: track the statistical distribution of each metric's values over time, and alert when the distribution shifts in a way the underlying business cannot explain. A definition change usually shows up as a step change in the distribution, while genuine business movement is smoother.</p>
<p>The third is reconciliation between independent consumers. If the sales dashboard and the finance report compute revenue through different paths — different tables, different logic — then any divergence between them is a drift signal by definition. Teams that systematically compare the same metric across two or more independent implementations catch drift within days rather than quarters. The fourth is the cheapest and most underrated: a standing question in every business review, "has this number's definition changed since we last looked at it?" asked out loud, with the answer recorded.</p>
<h2 id="what-does-a-governed-metric-actually-contain">What Does a Governed Metric Actually Contain?</h2>
<p>Treating metrics as products only works if the product has a specification. A complete metric definition is short — it fits on a screen — and contains eight fields: the business name, the plain-language definition a non-technical reader can act on, the technical calculation, the grain (what one row means), the source of record, the named owner, the current version with its effective date, and the known caveats. The caveats field is the one teams skip and the one that prevents the most disputes: "excludes intercompany eliminations," "restated after close," "not comparable before FY2024."</p>
<p>Around the definition sit four obligations that make it a product rather than a document. A service level — the metric is available, documented, and correct to an agreed standard. A change process — proposed changes are reviewed, versioned, and communicated before they take effect. A deprecation policy — superseded definitions keep working for a defined sunset period so historical questions still resolve. And a feedback channel — consumers can report an error or request a change in one step, and receive a response within an agreed time.</p>
<p>The organisational question is who does this work, and the answer that scales is a federated model: a small central team owns the platform, the standards, and the change process, while metric ownership sits with the domain that understands the number. Central teams that try to own every definition become a bottleneck and are routed around; fully decentralised teams produce definitions that conflict. The federation, with a standing council that adjudicates cross-domain disputes, is the structure that holds.</p>
<h2 id="what-does-recovery-look-like">What Does Recovery Look Like?</h2>
<p>Organisations that have closed a trust gap describe a similar arc, and it is worth stating plainly because it sets expectations for the work. The first month is diagnostic and uncomfortable: an audit of the metrics that matter, the discovery that many have multiple definitions, and the political work of deciding which one wins. The second and third months are structural — building the versioned store, assigning owners, migrating the highest-traffic reports to the governed definitions. Nothing visibly improves for business users during this phase, and programmes that promise otherwise lose credibility.</p>
<p>The turning point usually comes in the second quarter, when the first disputed number resolves in minutes rather than days because the definition, the owner, and the calculation are all one click away. That experience is what changes behaviour: business teams stop building shadow spreadsheets when the official number becomes faster to trust than their own. By the second quarter, the measurable signals are a declining volume of reconciliation tickets, a rising share of decisions taken on governed metrics, and — most tellingly — a fall in the number of parallel definitions in active use.</p>
<p>The failure mode of recovery programmes is treating this as a communications problem. Publishing a data dictionary does not close a trust gap, because the gap was never about documentation; it was about whether the numbers agree and whether anyone is accountable when they do not. Structure first, then communicate — and the communication that matters is the changelog, not the announcement.</p>
"""

S10_EN_FAQ = [
    ("What is metric drift and how does it happen?",
     "Metric drift is the silent change of a business metric's definition over time. It is almost never deliberate: someone adds shipping fees to revenue because finance asked, someone excludes returns because the product team asked, and within two quarters the same word means two different things. Because nobody announces the change, it is invisible until two reports disagree."),
    ("How do you detect metric drift before it spreads?",
     "Four signals work together: version every definition and publish a changelog; monitor each metric's value distribution for unexplained step changes; reconcile the same metric across independent consumers so divergence is a drift signal by construction; and ask out loud at every business review whether a definition changed since the last look."),
    ("What should a governed metric definition contain?",
     "Eight fields: business name, plain-language definition, technical calculation, grain, source of record, named owner, current version with effective date, and known caveats. The caveats field is the most-skipped and the most valuable, because it pre-empts the disputes that erode trust."),
    ("Who should own metric definitions?",
     "A federated model: a small central team owns the platform, standards and change process, while domain teams own the definitions they understand. Central ownership of every definition becomes a bottleneck and gets routed around; fully decentralised ownership produces conflicting definitions."),
    ("How long does it take to close a trust gap?",
     "Expect one month of uncomfortable diagnosis, two to three months of structural work with no visible improvement for business users, and a turning point in the second quarter when the first disputed number resolves in minutes. Programmes that promise early visible wins lose credibility before the structural work lands."),
]

S10_ZH_ADD = """
<h2 id="如何在指標漂移擴散之前發現它">如何在指標漂移擴散之前發現它？</h2>
<p>漂移在本質上是不可見的：沒有人會宣布「營收現在包含運費了」。因此發現它依賴的是機制而非警覺性，而以下四種訊號是有效的。</p>
<p>第一是帶發布記錄的定義版本管理。每個指標定義都存在版本化的儲存中；每次變更都遞增版本，並產生一條記錄，說明改了什麼、何時改的、由誰批准。這不能防止漂移，但能把靜默的漂移變成可見的事件。第二是分佈監控：追蹤每個指標數值的統計分佈隨時間的變化，當分佈出現業務無法解釋的變動時發出告警。定義變更通常表現為分佈上的階躍，而真實的業務波動則較為平滑。</p>
<p>第三是獨立消費端之間的對帳。如果銷售儀表板與財務報表透過不同路徑計算營收——不同的資料表、不同的邏輯——那麼兩者之間的任何差異，按定義就是漂移訊號。系統性地比較同一指標在兩個以上獨立實作中的結果，能在數天而非數季之內發現漂移。第四種成本最低也最被低估：在每次經營複盤會議上固定問一句「這個數字的定義，自上次檢視以來有變過嗎？」，把答案記錄下來。</p>
<h2 id="受控指標具體應包含哪些內容">受控指標具體應包含哪些內容？</h2>
<p>把指標當成產品來治理，前提是這個產品有規格。一份完整的指標定義很短——一屏就能看完——並包含八個欄位：業務名稱、非技術人員也能據以行動的白話定義、技術計算式、粒度（一列代表什麼）、權威來源、具名負責人、當前版本及其生效日期，以及已知的限制條件。限制條件這一欄最常被省略，卻能避免最多的爭議：「不含內部交易沖銷」「結帳後會重述」「2024會計年度之前不可比較」。</p>
<p>圍繞這份定義，還有四項義務，使它成為產品而不只是一份文件。服務水準：指標可用、有文件、並達到約定的正確性標準。變更流程：變更需經審查、版本化，並在生效前完成溝通。下線政策：被取代的定義在約定的日落期內繼續可用，使歷史問題仍能求解。回饋管道：使用者能一步回報錯誤或提出變更，並在約定時間內得到回應。</p>
<p>組織上的問題是誰來做這件事，而能規模化的答案是聯邦式模型：一個小的中央團隊擁有平台、標準與變更流程，指標的所有權則歸屬於最理解這個數字的業務領域。試圖擁有所有定義的中央團隊會成為瓶頸並被繞過；完全去中心化的團隊則會產出互相矛盾的定義。聯邦制加上一個負責裁決跨域爭議的常設委員會，才是能持久的結構。</p>
<h2 id="修復信任差距的過程是什麼樣的">修復信任差距的過程是什麼樣的？</h2>
<p>已經修復信任差距的組織所描述的過程相當類似，值得直白地說明，因為它為這項工作設定了正確的預期。第一個月是診斷期，而且並不好受：盤點重要的指標、發現許多指標存在多套定義、並進行政治協調以決定哪一套勝出。第二與第三個月是結構期——建立版本化儲存、指派負責人、把流量最高的報表遷移到受控定義上。這個階段對業務使用者而言沒有任何可見的改善，而承諾過早見效的專案往往會在此失去可信度。</p>
<p>轉折點通常出現在第二季：當第一個被質疑的數字在幾分鐘內就被釐清，因為定義、負責人與計算式都只需一次點擊就能看到。這個經驗會改變行為：當官方數字比自己維護的試算表更快取得信任時，業務團隊就會停止建立影子報表。到第二季，可衡量的訊號包括對帳工單數量下降、基於受控指標做出的決策比例上升，以及最能說明問題的一項——仍在使用的平行定義數量下降。</p>
<p>修復專案常見的失敗模式，是把它當成溝通問題。發布資料字典並不能彌合信任差距，因為差距從來不在於文件，而在於數字是否一致，以及不一致時是否有人負責。先建立結構，再談溝通——而真正重要的溝通是變更記錄，不是公告。</p>
"""

S10_ZH_FAQ = [
    ("什麼是指標漂移，它是怎麼發生的？",
     "指標漂移是業務指標的定義隨時間靜默改變。它幾乎從來不是刻意的：有人因為財務要求而把運費加入營收，有人因為產品團隊要求而排除退貨，兩個季度之後同一個詞就代表了兩種不同的東西。由於沒有人宣布這個變更，在兩份報表出現分歧之前它都是不可見的。"),
    ("如何在指標漂移擴散之前發現它？",
     "四種訊號需要並用：為每個定義做版本管理並發布變更記錄；監控每個指標的數值分佈是否出現無法解釋的階躍；在多個獨立消費端之間對帳同一指標，使差異按定義成為漂移訊號；以及在每次經營複盤會議上明確詢問定義自上次檢視以來是否變更。"),
    ("受控指標的定義應包含哪些內容？",
     "八個欄位：業務名稱、非技術人員可據以行動的白話定義、技術計算式、粒度、權威來源、具名負責人、當前版本與生效日期，以及已知的限制條件。限制條件最常被省略，卻最有價值，因為它能預先化解侵蝕信任的爭議。"),
    ("指標定義應該由誰擁有？",
     "聯邦式模型：一個小的中央團隊擁有平台、標準與變更流程，業務領域團隊則擁有他們最理解的定義。由中央擁有所有定義會成為瓶頸並被繞過；完全去中心化則會產出互相矛盾的定義。"),
    ("彌合信任差距需要多久？",
     "預期是一個月不好受的診斷期、兩到三個月對業務使用者沒有可見改善的結構期，以及第二季出現的轉折點——第一個被質疑的數字在幾分鐘內被釐清。承諾過早見效的專案，往往在結構工作落地之前就失去了可信度。"),
]

S10_CN_H2 = [
    ("故障一：公制漂移", "失败之一：什么是指标漂移？"),
    ("失败之二：定义模糊", "失败之二：为什么定义模糊会拖垮分析？"),
    ("失败三：信任差距", "失败之三：信任差距是怎么形成的？"),
    ("解决方案：将受控指标作为产品", "解决方案：为什么要把受控指标当成产品？"),
    ("要点", "本文的核心要点是什么？"),
    ("结论", "企业该从哪一步开始修复信任？"),
]
S10_TW_H2 = [
    ("本文要點是什麼？", "本文的核心要點是什麼？"),
]

DATA = {
    S6: {
        "EN": {"h2": [
            ("Understanding the Current Technology Landscape", "What Does the Enterprise Orchestration Landscape Look Like?"),
            ("Technical Architecture and Integration Patterns", "Which Integration Patterns Cover Most Production Use Cases?"),
            ("Performance Benchmarks and Optimization Strategies", "How Do You Optimize Orchestration Performance?"),
        ], "add": S6_EN_ADD, "faq": S6_EN_FAQ},
        "ZH_FAQ_TRAD": S6_ZH_FAQ,
        "ZH_CN_H2": S6_CN_H2, "ZH_TW_H2": S6_TW_H2,
    },
    S7: {
        "EN": {"h2": [
            ("Why it matters", "Why Does AI Demand Forecasting Matter Now?"),
            ("Common challenges", "What Blocks AI Forecasting Programmes?"),
            ("How to get started", "How Should a First Forecasting Pilot Be Scoped?"),
            ("Key takeaways", "What Are the Key Takeaways?"),
        ], "add": S7_EN_ADD, "faq": S7_EN_FAQ},
        "ZH_ADD_TRAD": S7_ZH_ADD,
        "ZH_FAQ_TRAD": S7_ZH_FAQ,
        "ZH_CN_H2": S7_CN_H2, "ZH_TW_H2": S7_TW_H2,
    },
    S8: {
        "EN": {"h2": [
            ("The Context Window Problem", "What Is the Context Window Problem?"),
            ("Reference Resolution", "How Should an AI Resolve 'That' and 'By Month'?"),
            ("Context Window Management Strategy", "How Should Context Be Managed Across Turns?"),
            ("When to Reset Context", "When Should Conversation Context Be Reset?"),
            ("Key Takeaways", "What Are the Key Takeaways?"),
            ("Conclusion", "What Should Teams Build First?"),
        ], "add": S8_EN_ADD, "faq": S8_EN_FAQ},
        "ZH_ADD_TRAD": S8_ZH_ADD,
        "ZH_FAQ_TRAD": S8_ZH_FAQ,
        "ZH_CN_H2": S8_CN_H2, "ZH_TW_H2": S8_TW_H2,
    },
    S9: {
        "EN": {"h2": [
            ("Understanding the Current Landscape", "What Is the Current State of AI Property Valuation?"),
            ("Key Principles and Strategic Framework", "What Are the Key Principles of AI Valuation?"),
            ("Implementation Approach and Best Practices", "How Should Organisations Implement AI Valuation?"),
            ("Measuring Success and Demonstrating ROI", "How Do You Measure AI Valuation ROI?"),
            ("Common Pitfalls and How to Avoid Them", "Which Pitfalls Undermine Valuation AI Programmes?"),
            ("Risk and Compliance Considerations for AI Valuation", "What Compliance Risks Does AI Valuation Carry?"),
            ("Practical First Steps", "What Are the Practical First Steps?"),
            ("Key Takeaways", "What Are the Key Takeaways?"),
            ("Conclusion", "What Should Organisations Do Next?"),
        ], "faq": S9_EN_FAQ},
        "ZH_ADD_TRAD": S9_ZH_ADD,
        "ZH_FAQ_TRAD": S9_ZH_FAQ,
        "ZH_CN_H2": S9_CN_H2, "ZH_TW_H2": S9_TW_H2,
    },
    S10: {
        "EN": {"h2": [
            ("Failure 1: Metric Drift", "Failure 1: What Is Metric Drift?"),
            ("Failure 2: Definition Ambiguity", "Failure 2: How Does Definition Ambiguity Hurt?"),
            ("Failure 3: The Trust Gap", "Failure 3: How Does the Trust Gap Form?"),
            ("The Solution: Governed Metrics as Products", "What Is the Solution: Governed Metrics as Products?"),
            ("Key Takeaways", "What Are the Key Takeaways?"),
            ("Conclusion", "Where Should Organisations Start?"),
        ], "add": S10_EN_ADD, "faq": S10_EN_FAQ},
        "ZH_ADD_TRAD": S10_ZH_ADD,
        "ZH_FAQ_TRAD": S10_ZH_FAQ,
        "ZH_CN_H2": S10_CN_H2, "ZH_TW_H2": S10_TW_H2,
    },
}
