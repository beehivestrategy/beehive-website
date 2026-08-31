import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "real-time-data-streaming-for-ai-powered-decision-making-a-2026-update"

EN_ADD = """
<h2 id="which-architecture-patterns-fit-which-decision-latency">Which Architecture Patterns Fit Which Decision Latency?</h2>
<p>"Real-time" is not one requirement, and treating it as one is the most common cause of streaming overspend. The right architecture depends on how quickly the decision must be made, and the honest answer is that most business decisions need seconds to minutes, not microseconds. Mapping your decisions to a latency band before choosing technology typically cuts the platform bill by half, because the expensive part of streaming is nearly always the sub-second path, and very few decisions genuinely need it.</p>
<p>Three bands cover almost everything. Sub-second streaming is required when the system itself must act without a human — blocking a fraudulent payment, preventing a machine from producing defective parts, throttling an API. This band needs an event broker, stream processing with state, and a model deployed inline, and it carries the highest operational burden. Seconds-to-minutes streaming is the sweet spot for human-in-the-loop decisions: alerting a store manager that shelf stock will run out this afternoon, escalating a logistics exception, surfacing a margin leak to a category buyer. This band can usually be served by change-data-capture into a lakehouse with incremental materialised views, which is dramatically cheaper to run. Minutes-to-hours covers the large class of decisions that are currently daily batch and would benefit from a shorter cycle — replenishment replanning, workforce reallocation, campaign pacing.</p>
<table class="article-table">
<thead><tr><th>Latency band</th><th>Representative pattern</th><th>Typical decisions</th><th>Relative run cost</th></tr></thead>
<tbody>
<tr><td>Sub-second</td><td>Event broker + stateful stream processing + inline model scoring</td><td>Fraud block, machine interlock, dynamic price serve</td><td>High</td></tr>
<tr><td>Seconds to minutes</td><td>Change data capture + incremental views + push alerting</td><td>Stock-out alert, route exception, margin anomaly</td><td>Medium</td></tr>
<tr><td>Minutes to hours</td><td>Micro-batch on a short cycle + scheduled conversational digest</td><td>Replenishment replan, shift reallocation, campaign pacing</td><td>Low</td></tr>
<tr><td>Daily</td><td>Classic batch warehouse load</td><td>Financial close, regulatory reporting</td><td>Lowest</td></tr>
</tbody>
</table>
<p>Two architectural cautions follow from this table. First, resist the urge to build one pipeline that serves every band: the sub-second path will drag the whole system toward its own cost and reliability profile. Second, prefer an event log as the single source of truth and derive the other bands from it. When the alert, the dashboard, and the month-end report are all projections of the same immutable event stream, the perpetual argument about why two numbers disagree simply stops happening.</p>
<h2 id="how-do-you-build-a-streaming-business-case-that-survives-the-cfo">How Do You Build a Streaming Business Case That Survives the CFO?</h2>
<p>Streaming business cases fail in finance review for a predictable reason: they quantify the technology and hand-wave the decision. A proposal that promises "real-time visibility" invites the question "visible to whom, and what will they do differently?" A proposal that states the decision, the owner, the current latency, the target latency, and the value per improved decision gets funded. The arithmetic is not complicated; it just has to be explicit.</p>
<p>Take a concrete illustration. A regional retailer runs 400 stores and detects out-of-shelf conditions through a nightly sales scan, so the average stock-out persists for 14 hours before anyone acts. Assume 3 stock-out events per store per week, an average lost margin of 180 currency units per event, and that acting within one hour recovers 60% of the loss. The annual recovered margin is 400 stores x 3 events x 52 weeks x 180 units x 60%, which is roughly 6.7 million currency units. Against a streaming platform and integration cost in the low seven figures, the payback is inside a quarter — and that is before counting the second-order benefit that every scored event becomes training data for the next model generation. The point of the example is not the numbers; it is that each input is a number somebody in the business can challenge and then own.</p>
<table class="article-table">
<thead><tr><th>Business case line</th><th>What finance needs to see</th><th>Common omission</th></tr></thead>
<tbody>
<tr><td>Decision and owner</td><td>Named decision, named accountable manager</td><td>"Business users" as the owner</td></tr>
<tr><td>Current vs target latency</td><td>Measured baseline in minutes, target in minutes</td><td>No baseline measured at all</td></tr>
<tr><td>Value per improved decision</td><td>Margin recovered or loss avoided, per event</td><td>Total addressable market instead of per-event value</td></tr>
<tr><td>Event volume</td><td>Events per period, with source system named</td><td>Volume assumed from a vendor benchmark</td></tr>
<tr><td>Cost to run</td><td>Platform, integration, and three-year run cost</td><td>Only build cost, no run cost</td></tr>
<tr><td>Measurement plan</td><td>How the benefit will be verified after go-live</td><td>No post-implementation review</td></tr>
</tbody>
</table>
<p>Finally, size the pilot so that it can fail cheaply. One decision, one region, one product category, ninety days. A pilot narrow enough to measure is far more persuasive than a platform programme broad enough that nobody can attribute the result to it.</p>
<h2 id="what-does-a-30-60-90-day-streaming-rollout-look-like">What Does a 30-60-90 Day Streaming Rollout Look Like?</h2>
<p>The organisations that reach production quickly share one habit: they start from the decision and work backwards to the pipeline, rather than building infrastructure and waiting for use cases to arrive. A 30-60-90 structure keeps that discipline and produces something demonstrable at each milestone.</p>
<p>Days one to thirty are for instrumentation and baselining. Identify the three decisions with the clearest if-then action, measure how long each currently takes end to end, and record the current loss rate. This step is unglamorous and decisive: without a measured baseline, no later claim of improvement is credible, and most teams are surprised by how large the gap is between the assumed and actual decision latency. Days thirty-one to sixty are for the first loop. Stand up change-data-capture or event publishing from the source system, land the events in a queryable store, and deliver the first alert or answer into the channel where the decision-maker already works — an IM thread, a scheduled digest, or a conversational query. Days sixty-one to ninety are for closing the loop: confirm that the action was taken, measure the changed outcome against the baseline, and write down the decision to scale, adjust, or stop.</p>
<table class="article-table">
<thead><tr><th>Window</th><th>Focus</th><th>Exit criterion</th></tr></thead>
<tbody>
<tr><td>Days 1-30</td><td>Decision inventory, latency baseline, loss measurement</td><td>Three decisions with measured baselines and named owners</td></tr>
<tr><td>Days 31-60</td><td>First event-to-action loop in production</td><td>Alert or answer delivered inside target latency</td></tr>
<tr><td>Days 61-90</td><td>Outcome verification and scale decision</td><td>Written comparison against baseline, reviewed by the sponsor</td></tr>
</tbody>
</table>
<p>The single most common reason these rollouts stall is that no one is assigned to act on the alert. Streaming infrastructure that produces notifications nobody owns is an expensive way to generate noise. Assign the response before you build the pipeline, and the technology becomes the easy part.</p>
"""

CN_ADD = """
<h2 id="哪些架构模式匹配哪种决策延迟">哪些架构模式匹配哪种决策延迟？</h2>
<p>"实时"并不是同一个需求，把它当成同一个需求是流式项目超支最常见的原因。正确的架构取决于决策必须多快做出，而诚实的答案是：大多数业务决策需要的是秒级到分钟级，而不是微秒级。在选择技术之前先把决策映射到延迟档位，通常能把平台账单砍掉一半，因为流式架构中最昂贵的部分几乎总是亚秒级通路，而真正需要它的决策非常少。</p>
<p>三个档位几乎可以覆盖所有场景。亚秒级流式适用于系统必须在无人介入时自行行动的场景——拦截欺诈支付、阻止设备继续生产缺陷件、对 API 限流。这一档需要事件代理、带状态的流处理以及内联部署的模型，运维负担最重。秒级到分钟级是人机协同决策的最佳区间：提醒店长某个货架今天下午会缺货、升级物流异常、把毛利异常推送给品类采购。这一档通常可以用变更数据捕获（CDC）加增量物化视图来实现，运行成本低得多。分钟级到小时级覆盖了目前仍是每日批处理、但缩短周期就能受益的一大类决策——补货重排、人力重新分配、营销投放节奏调整。</p>
<table class="article-table">
<thead><tr><th>延迟档位</th><th>代表性模式</th><th>典型决策</th><th>相对运行成本</th></tr></thead>
<tbody>
<tr><td>亚秒级</td><td>事件代理＋带状态流处理＋内联模型打分</td><td>欺诈拦截、设备联锁、动态定价下发</td><td>高</td></tr>
<tr><td>秒级到分钟级</td><td>变更数据捕获＋增量视图＋主动推送告警</td><td>缺货提醒、路径异常、毛利异常</td><td>中</td></tr>
<tr><td>分钟级到小时级</td><td>短周期微批＋定时对话式摘要</td><td>补货重排、班次再分配、投放节奏</td><td>低</td></tr>
<tr><td>每日</td><td>经典批处理数仓加载</td><td>财务结账、监管报送</td><td>最低</td></tr>
</tbody>
</table>
<p>从这张表可以得出两点架构提醒。第一，不要试图用一条管道服务所有档位：亚秒级通路会把整个系统拖向它的成本与可靠性画像。第二，优先把事件日志作为唯一事实来源，再从它派生出其他档位。当告警、仪表盘和月末报表都是同一条不可变事件流的投影时，"两个数字为什么不一致"这种无休止的争论就会自然消失。</p>
<h2 id="如何构建经得起CFO审视的流式业务论证">如何构建经得起 CFO 审视的流式业务论证？</h2>
<p>流式项目的商业论证在财务评审中被否，原因往往是可预测的：它们量化了技术，却对决策一笔带过。一份承诺"实时可视化"的提案会招来一个问题——"给谁看？看了之后会做什么不同的事？"而一份写清楚决策、责任人、当前延迟、目标延迟以及每次决策改进对应价值的提案，则能拿到预算。算术并不复杂，只是必须写得明确。</p>
<p>举一个具体例子。某区域零售商有 400 家门店，通过每日一次的销售扫描发现缺货，因此平均缺货状态会持续 14 小时才有人处理。假设每店每周发生 3 次缺货、每次平均损失毛利 180 个货币单位，且在一小时内采取行动可挽回 60% 的损失。那么年度可挽回毛利约为 400 家门店 × 3 次 × 52 周 × 180 单位 × 60%，约为 670 万个货币单位。对比一个七位数低段的流式平台与集成成本，投资回收期在一个季度之内——这还没有计入二阶收益：每一个被打分的事件都会成为下一代模型的训练数据。这个例子的重点不是这些数字，而是每一项输入都是业务方可以质疑、进而可以认领的数字。</p>
<table class="article-table">
<thead><tr><th>商业论证条目</th><th>财务需要看到什么</th><th>常见遗漏</th></tr></thead>
<tbody>
<tr><td>决策与责任人</td><td>具名的决策、具名的问责经理</td><td>把"业务用户"当作责任人</td></tr>
<tr><td>当前与目标延迟</td><td>以分钟计量的基线，以及以分钟计量的目标</td><td>根本没有测量基线</td></tr>
<tr><td>每次决策改进的价值</td><td>每次事件挽回的毛利或避免的损失</td><td>用总体可触达市场代替单事件价值</td></tr>
<tr><td>事件体量</td><td>每周期事件数，并注明来源系统</td><td>依据厂商基准假设体量</td></tr>
<tr><td>运行成本</td><td>平台、集成与三年运行成本</td><td>只算建设成本、不算运行成本</td></tr>
<tr><td>度量计划</td><td>上线后如何验证收益</td><td>没有上线后复盘</td></tr>
</tbody>
</table>
<p>最后，把试点规模设计成可以低成本失败：一个决策、一个区域、一个品类、九十天。一个窄到可度量的试点，远比一个宽到无人能把结果归因于它的平台项目更有说服力。</p>
<h2 id="30-60-90天的流式上线路径是什么样">30-60-90 天的流式上线路径是什么样？</h2>
<p>那些快速进入生产的组织有一个共同习惯：它们从决策出发倒推管道，而不是先建基础设施再等用例出现。30-60-90 的结构能保持这种纪律，并在每个里程碑都产出可展示的成果。</p>
<p>第 1 至 30 天用于埋点与建立基线。找出三个 if-then 行动最清晰的决策，测量每个决策当前端到端需要多久，并记录当前的损失率。这一步枯燥但决定性：没有实测基线，事后任何改进的说法都不可信；而且大多数团队会惊讶地发现，假设的决策延迟与实际情况差距有多大。第 31 至 60 天用于打通第一个闭环。从源系统接入变更数据捕获或事件发布，把事件落到可查询的存储中，并把第一条告警或答案送达到决策者已经在用的渠道——IM 会话、定时摘要，或对话式提问。第 61 至 90 天用于闭合回路：确认行动已被执行，把变化后的结果与基线对比，并写下扩大、调整或停止的书面决策。</p>
<table class="article-table">
<thead><tr><th>时间窗</th><th>重点</th><th>准出标准</th></tr></thead>
<tbody>
<tr><td>第 1-30 天</td><td>决策盘点、延迟基线、损失度量</td><td>三个决策具备实测基线与具名责任人</td></tr>
<tr><td>第 31-60 天</td><td>第一条事件到行动的闭环上线</td><td>告警或答案在目标延迟内送达</td></tr>
<tr><td>第 61-90 天</td><td>结果验证与扩量决策</td><td>与基线的书面对比，经发起人评审</td></tr>
</tbody>
</table>
<p>这些上线路径最常见的停滞原因是：没有人被指派去响应告警。产生无人认领通知的流式基础设施，只是一种昂贵的噪音制造方式。在建设管道之前就把响应责任分派下去，技术反而会变成最简单的部分。</p>
"""

TW_ADD = """
<h2 id="哪些架構模式匹配哪種決策延遲">哪些架構模式匹配哪種決策延遲？</h2>
<p>「即時」並不是同一個需求，把它當成同一個需求是串流專案超支最常見的原因。正確的架構取決於決策必須多快做出，而誠實的答案是：大多數商業決策需要的是秒級到分鐘級，而不是微秒級。在選擇技術之前先把決策對應到延遲層級，通常能把平台帳單砍掉一半，因為串流架構中最昂貴的部分幾乎總是亞秒級路徑，而真正需要它的決策非常少。</p>
<p>三個層級幾乎可以涵蓋所有情境。亞秒級串流適用於系統必須在無人介入時自行行動的情境——攔截詐欺支付、阻止設備繼續生產瑕疵品、對 API 限流。這一級需要事件代理、具狀態的串流處理以及內聯部署的模型，維運負擔最重。秒級到分鐘級是人機協同決策的最佳區間：提醒店長某個貨架今天下午會缺貨、升級物流異常、把毛利異常推送給品類採購。這一級通常可以用變更資料擷取（CDC）搭配增量具體化檢視來實現，運行成本低得多。分鐘級到小時級涵蓋了目前仍是每日批次處理、但縮短週期就能受益的一大類決策——補貨重排、人力重新分配、行銷投放節奏調整。</p>
<table class="article-table">
<thead><tr><th>延遲層級</th><th>代表性模式</th><th>典型決策</th><th>相對運行成本</th></tr></thead>
<tbody>
<tr><td>亞秒級</td><td>事件代理＋具狀態串流處理＋內聯模型評分</td><td>詐欺攔截、設備連鎖、動態定價下發</td><td>高</td></tr>
<tr><td>秒級到分鐘級</td><td>變更資料擷取＋增量檢視＋主動推送告警</td><td>缺貨提醒、路徑異常、毛利異常</td><td>中</td></tr>
<tr><td>分鐘級到小時級</td><td>短週期微批次＋定時對話式摘要</td><td>補貨重排、班次再分配、投放節奏</td><td>低</td></tr>
<tr><td>每日</td><td>經典批次處理資料倉儲載入</td><td>財務結帳、監理申報</td><td>最低</td></tr>
</tbody>
</table>
<p>從這張表可以得出兩點架構提醒。第一，不要試圖用一條管線服務所有層級：亞秒級路徑會把整個系統拖向它的成本與可靠性樣貌。第二，優先把事件日誌作為唯一事實來源，再從它派生出其他層級。當告警、儀表板與月末報表都是同一條不可變事件流的投影時，「兩個數字為什麼不一致」這種無止盡的爭論就會自然消失。</p>
<h2 id="如何建構經得起CFO審視的串流商業論證">如何建構經得起 CFO 審視的串流商業論證？</h2>
<p>串流專案的商業論證在財務審查中被否，原因往往是可預測的：它們量化了技術，卻對決策一筆帶過。一份承諾「即時可視化」的提案會招來一個問題——「給誰看？看了之後會做什麼不同的事？」而一份寫清楚決策、負責人、目前延遲、目標延遲以及每次決策改善對應價值的提案，則能拿到預算。算術並不複雜，只是必須寫得明確。</p>
<p>舉一個具體例子。某區域零售商有 400 家門市，透過每日一次的銷售掃描發現缺貨，因此平均缺貨狀態會持續 14 小時才有人處理。假設每店每週發生 3 次缺貨、每次平均損失毛利 180 個貨幣單位，且在一小時內採取行動可挽回 60% 的損失。那麼年度可挽回毛利約為 400 家門市 × 3 次 × 52 週 × 180 單位 × 60%，約為 670 萬個貨幣單位。對比一個七位數低段的串流平台與整合成本，投資回收期在一個季度之內——這還沒有計入二階效益：每一個被評分的事件都會成為下一代模型的訓練資料。這個例子的重點不是這些數字，而是每一項輸入都是業務方可以質疑、進而可以認領的數字。</p>
<table class="article-table">
<thead><tr><th>商業論證條目</th><th>財務需要看到什麼</th><th>常見遺漏</th></tr></thead>
<tbody>
<tr><td>決策與負責人</td><td>具名的決策、具名的問責經理</td><td>把「業務使用者」當成負責人</td></tr>
<tr><td>目前與目標延遲</td><td>以分鐘衡量的基線，以及以分鐘衡量的目標</td><td>根本沒有衡量基線</td></tr>
<tr><td>每次決策改善的價值</td><td>每次事件挽回的毛利或避免的損失</td><td>用整體可觸及市場代替單一事件價值</td></tr>
<tr><td>事件量體</td><td>每週期事件數，並註明來源系統</td><td>依據供應商基準假設量體</td></tr>
<tr><td>運行成本</td><td>平台、整合與三年運行成本</td><td>只算建置成本、不算運行成本</td></tr>
<tr><td>衡量計畫</td><td>上線後如何驗證效益</td><td>沒有上線後檢討</td></tr>
</tbody>
</table>
<p>最後，把試點規模設計成可以低成本失敗：一個決策、一個區域、一個品類、九十天。一個窄到可衡量的試點，遠比一個寬到無人能把結果歸因於它的平台專案更有說服力。</p>
<h2 id="30-60-90天的串流上線路徑是什麼樣">30-60-90 天的串流上線路徑是什麼樣？</h2>
<p>那些快速進入生產的組織有一個共同習慣：它們從決策出發回推管線，而不是先建基礎設施再等用例出現。30-60-90 的結構能維持這種紀律，並在每個里程碑都產出可展示的成果。</p>
<p>第 1 至 30 天用於埋點與建立基線。找出三個 if-then 行動最清晰的決策，衡量每個決策目前端對端需要多久，並記錄目前的損失率。這一步枯燥但具決定性：沒有實測基線，事後任何改善的說法都不可信；而且大多數團隊會驚訝地發現，假設的決策延遲與實際情況差距有多大。第 31 至 60 天用於打通第一個閉環。從來源系統接入變更資料擷取或事件發布，把事件落到可查詢的儲存中，並把第一則告警或答案送達到決策者已經在用的管道——IM 對話、定時摘要，或對話式提問。第 61 至 90 天用於閉合迴路：確認行動已被執行，把變化後的結果與基線對比，並寫下擴大、調整或停止的書面決策。</p>
<table class="article-table">
<thead><tr><th>時間窗</th><th>重點</th><th>准出標準</th></tr></thead>
<tbody>
<tr><td>第 1-30 天</td><td>決策盤點、延遲基線、損失衡量</td><td>三個決策具備實測基線與具名負責人</td></tr>
<tr><td>第 31-60 天</td><td>第一條事件到行動的閉環上線</td><td>告警或答案在目標延遲內送達</td></tr>
<tr><td>第 61-90 天</td><td>結果驗證與擴量決策</td><td>與基線的書面對比，經發起人審查</td></tr>
</tbody>
</table>
<p>這些上線路徑最常見的停滯原因是：沒有人被指派去回應告警。產生無人認領通知的串流基礎設施，只是一種昂貴的噪音製造方式。在建置管線之前就把回應責任分派下去，技術反而會變成最簡單的部分。</p>
"""

H2FIX = {
    "EN": [
        ("the-current-landscape", "What Does the Current Streaming Landscape Look Like in 2026?"),
        ("why-latency-is-a-financial-question", "Why Is Latency a Financial Question?"),
        ("key-implementation-challenges", "What Are the Key Implementation Challenges?"),
        ("practical-approaches-that-work", "Which Practical Approaches Actually Work?"),
        ("key-takeaways", "What Are the Key Takeaways?"),
        ("conclusion", "What Should You Conclude and Do Next?"),
    ],
    "CN": [
        ("理解当前格局", "如何理解当前格局？"),
        ("关键原则与战略框架", "关键原则与战略框架是什么？"),
        ("实施方法与最佳实践", "如何落地实施方法与最佳实践？"),
        ("衡量成功与展示投资回报率", "如何衡量成功并展示投资回报率？"),
        ("常见陷阱及规避方法", "常见陷阱有哪些，应如何规避？"),
        ("关键要点", "关键要点有哪些？"),
        ("结论", "结论与下一步行动是什么？"),
    ],
    "TW": [
        ("理解當前格局", "如何理解當前格局？"),
        ("關鍵原則與策略框架", "關鍵原則與策略框架是什麼？"),
        ("實施方法與最佳實踐", "如何落實實施方法與最佳實踐？"),
        ("衡量成功與展示投資回報率", "如何衡量成功並展示投資回報率？"),
        ("常見陷阱及規避方法", "常見陷阱有哪些，應如何規避？"),
        ("關鍵要點", "關鍵要點有哪些？"),
        ("結論", "結論與下一步行動是什麼？"),
    ],
}

EN_FAQ = [
    ("What is the difference between real-time data streaming and traditional batch processing?",
     "Batch processing collects events over a period and processes them together on a schedule, so the data a decision-maker sees is always at least as old as the last run. Streaming publishes each event as it happens and processes it continuously, so a decision can be made while the event is still relevant. In practice most organisations run both: streaming for decisions with a defined action, batch for reporting and regulatory work."),
    ("How real-time does a business decision actually need to be?",
     "Far less often than vendors imply. Genuine sub-second requirements are limited to cases where a system must act without a human, such as blocking a fraudulent transaction or stopping a machine. Most operational decisions are well served by seconds-to-minutes latency, which can be delivered with change data capture and incremental views at a fraction of the cost of a sub-second architecture."),
    ("Do we need a dedicated streaming platform team to get started?",
     "Not to start. The scarce skills are needed to run a stateful, sub-second platform at scale, not to publish events and query them incrementally. A common path is to begin with a managed service that owns the platform, schema registry, and observability, prove value on one decision loop, and only then decide whether in-house streaming engineering is justified by the volume of use cases."),
    ("How does streaming data connect to conversational analytics?",
     "The events land in a queryable store with defined semantics, and a conversational layer translates a natural-language question into a governed query against it. That lets a business user ask what changed in the last hour and receive a sourced answer in a chat or IM thread, with the same definitions and permissions that govern the warehouse, rather than waiting for a dashboard or an overnight job."),
]

CN_FAQ = [
    ("实时数据流与传统批处理有什么区别？",
     "批处理在一段时间内收集事件，再按计划统一处理，因此决策者看到的数据至少和上一次运行一样旧。流式处理则在事件发生时即发布并持续处理，使决策能在事件仍有意义时做出。实践中大多数组织两者并用：流式服务有明确行动的决策，批处理服务报表与监管报送。"),
    ("业务决策到底需要多实时？",
     "远没有厂商暗示的那么频繁。真正的亚秒级需求仅限于系统必须无人介入自行行动的场景，例如拦截欺诈交易或停机。大多数运营决策用秒级到分钟级延迟就已足够，而这可以通过变更数据捕获与增量视图来实现，成本仅为亚秒级架构的一小部分。"),
    ("启动时是否需要专门的流式平台团队？",
     "起步阶段并不需要。稀缺技能主要用于大规模运行带状态、亚秒级的平台，而不是发布事件并做增量查询。常见路径是先用托管服务承担平台、schema 注册表与可观测性，在一个决策闭环上验证价值，再根据用例规模决定内部流式工程团队是否值得设立。"),
    ("流式数据如何与对话式分析结合？",
     "事件落入具备明确语义的可查询存储后，对话层把自然语言问题翻译成受治理的查询来执行。这让业务用户可以问「过去一小时发生了什么变化」，并在聊天或 IM 会话中收到带出处的答案，且沿用与数据仓库一致的定义与权限，而不必等待仪表盘或隔夜任务。"),
]

TW_FAQ = [
    ("即時資料串流與傳統批次處理有什麼差別？",
     "批次處理在一段時間內收集事件，再按排程統一處理，因此決策者看到的資料至少和上一次執行一樣舊。串流處理則在事件發生時即發布並持續處理，使決策能在事件仍有意義時做出。實務上大多數組織兩者並用：串流服務有明確行動的決策，批次服務報表與監理申報。"),
    ("商業決策到底需要多即時？",
     "遠沒有供應商暗示的那麼頻繁。真正的亞秒級需求僅限於系統必須無人介入自行行動的情境，例如攔截詐欺交易或停機。大多數營運決策用秒級到分鐘級延遲就已足夠，而這可以透過變更資料擷取與增量檢視來實現，成本僅為亞秒級架構的一小部分。"),
    ("啟動時是否需要專門的串流平台團隊？",
     "起步階段並不需要。稀缺技能主要用於大規模運行具狀態、亞秒級的平台，而不是發布事件並做增量查詢。常見路徑是先用託管服務承擔平台、schema 登錄表與可觀測性，在一個決策閉環上驗證價值，再依用例規模決定內部串流工程團隊是否值得設立。"),
    ("串流資料如何與對話式分析結合？",
     "事件落入具備明確語意的可查詢儲存後，對話層把自然語言問題翻譯成受治理的查詢來執行。這讓業務使用者可以問「過去一小時發生了什麼變化」，並在聊天或 IM 對話中收到帶出處的答案，且沿用與資料倉儲一致的定義與權限，而不必等待儀表板或隔夜工作。"),
]

process(SLUG, H2FIX,
        adds={"EN": EN_ADD, "CN": CN_ADD, "TW": TW_ADD},
        add_faq={"EN": ("Frequently Asked Questions", EN_FAQ),
                 "CN": ("常见问题", CN_FAQ),
                 "TW": ("常見問題", TW_FAQ)},
        tag=SLUG[:24])
