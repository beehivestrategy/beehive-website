# -*- coding: utf-8 -*-
"""Batch 1 content: slugs 1-5."""

S1 = "conversational-bi-executives-natural-language-queries"

S1_EN_ADD = """
<h2 id="what-do-executives-actually-ask">What Do Executives Actually Ask?</h2>
<p>Query logs from executive deployments converge on a small set of patterns, and the concentration is more extreme than most teams expect. Roughly twenty question shapes account for more than 70% of everything senior leaders type, and the top five — "are we on plan?", "why did we miss?", "what changed since last week?", "which segment or region is driving this?", and "what happens if we do nothing?" — typically cover 40% on their own. That concentration is the single most useful fact in executive analytics, because it means a team does not need universal coverage to be useful. It needs depth on a short list, delivered perfectly.</p>
<p>The pattern that surprises analytics teams most is repetition. Executives ask the same question over and over, not because they forgot the answer, but because the answer changes every day and the question is how they check the pulse of the business. A CFO who asks "where are we on opex?" every Monday morning is not asking for a report; they are performing a ritual of control. Treating that repetition as a failure of self-service — and responding by building yet another dashboard — misses the point entirely. The right response is to make the repeated question instant, conversational, and identical in answer every time it is asked.</p>
<p>The second pattern is that executive questions are comparative and time-anchored rather than dimensional. An analyst asks for revenue by region, channel, and product over thirteen weeks. An executive asks whether this quarter is tracking better or worse than the plan the board approved. The underlying data is the same; the framing is a comparison against a commitment, not a slice of a cube. Semantic layers built primarily for dimensional slicing therefore need an explicit layer of business commitments — plan, forecast, prior period, target — modelled as first-class objects, or the executive's most common question will be the one the system handles worst.</p>
<h3>Why the mobile and IM channel changes the question mix</h3>
<p>When conversational BI is delivered inside the messaging tools executives already live in — WeChat Work, Teams, Slack — the query mix shifts again. Questions get shorter, they arrive at odd hours, and follow-up rates roughly double, because the friction of opening a separate BI tool disappears. In IM-native deployments, the median executive question is under eight words, and the median session contains three or more turns. That is a different product from a desktop query box, and it rewards platforms designed for short, threaded, context-carrying exchanges rather than for a single well-formed question typed into a search bar.</p>
<h2 id="how-should-executive-answers-be-designed">How Should Answers Be Designed for Executive Attention?</h2>
<p>An executive answer has a different job from an analyst answer. The analyst wants the data and the ability to interrogate it. The executive wants the conclusion, the confidence, and the two or three drivers that explain it — in that order, and in under thirty seconds. Designing for that constraint means changing three things about how responses are generated.</p>
<p>First, lead with the answer, not the chart. "Gross margin is 42.1%, down 180 basis points against plan" is the answer; the waterfall chart is supporting evidence that follows. Most BI tools invert this, opening with a visualisation and leaving the reader to extract the conclusion. Second, state the comparison baseline explicitly. A number without a baseline is not information; executives will immediately ask "against what?" if the system does not say. Third, name the drivers in business language. "The variance is driven by freight costs in APAC and a mix shift toward lower-margin enterprise deals" is actionable; "dimension: region, measure: cogs" is not.</p>
<p>Confidence signalling matters just as much. Executives do not need false precision, and they penalise systems that present an estimate with the same authority as a booked actual. Showing whether a figure is actual, forecast, or estimated, and whether the underlying data refreshed this morning or three days ago, is what converts a conversational answer from a novelty into a decision input. Teams that added explicit freshness and confidence markers to executive answers consistently report higher trust scores than teams that only improved raw accuracy.</p>
<h2 id="what-does-a-90-day-executive-rollout-look-like">What Does a 90-Day Executive Rollout Look Like?</h2>
<p>Executive analytics programmes fail when they are scoped as platform projects. They succeed when they are scoped as coverage of a specific meeting. The most reliable 90-day pattern starts with one recurring leadership ritual and works outward from it.</p>
<ol>
<li><strong>Weeks 1-2 — instrument the meeting.</strong> Sit in the weekly leadership review and write down every question that could not be answered live. That list, not a data catalogue, is the requirements document. Expect twenty to forty distinct questions, and expect the top ten to cover most of the volume.</li>
<li><strong>Weeks 3-5 — build the semantic layer for those questions only.</strong> Define each metric once, with an owner, a calculation, and the synonyms executives actually use. Ten well-governed metrics beat two hundred loosely defined ones, because the failure mode executives notice is inconsistency, not missing coverage.</li>
<li><strong>Weeks 6-8 — run the meeting live.</strong> Put the conversational interface in the room and answer the questions in the meeting rather than after it. This is the step that creates belief, and it is also the step that exposes the gaps in the semantic layer fastest.</li>
<li><strong>Weeks 9-12 — expand and automate.</strong> Add follow-up depth to the questions that generated the most discussion, introduce proactive alerts for the metrics that moved most, and extend access to the next tier of leadership.</li>
</ol>
<p>Two disciplines separate the rollouts that stick from the ones that stall. The first is a named owner for every metric, so that when an answer is questioned there is a person, not a committee, who resolves it. The second is a visible log of every question asked and whether it was answered — because the fastest way to improve coverage is to look weekly at what executives asked for and did not get.</p>
<p>By the end of a well-run 90 days, the measurable outcome is not adoption; it is the share of leadership-meeting questions answered live. Teams that track that single number watch it move from near zero to 60-70%, and that movement is what funds the rest of the programme.</p>
"""

S1_EN_FAQ = [
    ("How accurate are conversational BI responses for executive queries?",
     "On the common executive patterns that make up most query volume, mature deployments resolve 85-95% of questions correctly, and the semantic layer guarantees that two executives phrasing the same question differently receive the same number. Coverage of long-tail questions is lower at launch and improves as the metric catalogue and synonym lists mature, typically passing 95% on core patterns within six months."),
    ("What is the role of the semantic layer in executive analytics?",
     "The semantic layer is what makes an answer trustworthy. It maps the words executives use to a single governed definition of each metric, holds the comparison baselines such as plan, forecast and prior period, and enforces row-level permissions. Without it, a conversational interface produces fluent answers that disagree with each other, which is worse than having no interface at all."),
    ("How long does it take before executives actually trust the answers?",
     "Trust builds through repetition rather than demonstration. Expect three to four weeks of daily use before an executive stops cross-checking the answer against a report, and two to three months before they cite the number in a meeting without verification. Publishing metric ownership, last-refresh times and confidence markers shortens that curve measurably."),
    ("Can conversational BI be delivered inside the tools executives already use?",
     "Yes, and it materially increases usage. Deployments that put the interface inside WeChat Work, Teams or Slack see shorter questions and roughly double the number of follow-up turns per session, because the friction of opening a separate BI tool disappears. The platform requirement is an API-first architecture and a permission model that respects the identity of the messaging account."),
    ("What should be measured to prove the programme is working?",
     "Track the share of leadership-meeting questions answered live, median time from question to answer, question repetition rate, and self-reported trust scores. Avoid measuring logins or query counts: high query volume with low answered-live rates means the system is being tried and found wanting, not adopted."),
]

S1_ZH_FAQ = [
    ("高管使用對話式BI時，回答的準確率有多高？",
     "在佔據大部分提問量的常見高管問題模式上，成熟部署的解析準確率為85%至95%；語義層能保證不同高管用不同措辭提出同一問題時得到同一個數字。長尾問題在初期的覆蓋率較低，會隨指標目錄與同義詞庫的成熟而提升，通常在六個月內核心模式的準確率可超過95%。"),
    ("語義層在高管分析中扮演什麼角色？",
     "語義層是答案可信的基礎。它把高管使用的詞彙映射到每個指標唯一的受控定義，維護計劃、預測、去年同期等比較基準，並落實行級權限。缺少語義層，對話界面會給出流暢但彼此矛盾的答案，這比沒有界面更糟。"),
    ("高管需要多久才會真正信任這些答案？",
     "信任靠重複使用建立，而不是靠一次演示。一般需要三到四週的日常使用，高管才會停止拿報表交叉核對；需要兩到三個月，才會在會議上直接引用這個數字而不再驗證。公開指標責任人、最後更新時間與置信標記，可以明顯縮短這個過程。"),
    ("對話式BI能否嵌入高管日常使用的工具中？",
     "可以，而且能顯著提升使用率。把界面放進企業微信、Teams或Slack的部署中，提問更短、每輪會話的追問次數約翻倍，因為打開獨立BI工具的摩擦消失了。平台側的要求是API優先的架構，以及能識別消息帳號身份的權限模型。"),
    ("應該用哪些指標證明項目正在見效？",
     "追蹤管理層會議中現場得到回答的問題比例、從提問到獲得答案的中位時長、問題重複率，以及使用者自評的信任度。不要只看登入數或查詢量：查詢量高但現場回答率低，說明系統在被試用後未被信任，而不是被採用。"),
]

S1_CN_H2 = [
    ("当前格局与关键趋势", "对话式BI的当前格局与关键趋势是什么？"),
    ("实施框架与最佳实践", "企业应该如何落地对话式BI？"),
    ("衡量影响与展示价值", "如何衡量对话式BI的影响与价值？"),
    ("克服常见挑战", "落地对话式BI有哪些常见挑战？"),
    ("ROI衡量与商业论证", "如何构建对话式BI的ROI论证？"),
    ("风险管理与合规框架", "对话式BI需要怎样的风险与合规框架？"),
]
S1_TW_H2 = [
    ("規模化推廣的關鍵成功因素", "規模化推廣的關鍵成功因素是什麼？"),
    ("技術基礎設施與實施考量", "技術基礎設施該如何考量？"),
    ("中國市場特有的實施優勢", "中國市場有哪些特有的實施優勢？"),
]

# ---------------------------------------------------------------- slug 2
S2 = "retail-ai-personalization-early-2025"

S2_EN_ADD = """
<h2 id="what-data-does-retail-personalization-actually-need">What Data Does Retail Personalization Actually Need?</h2>
<p>Personalisation programmes are usually sold as a modelling problem and delivered as a data problem. The models are, by 2025, largely commoditised: collaborative filtering, gradient-boosted ranking, sequence models for next-basket prediction, and embedding-based retrieval are available as managed services from every major cloud. What separates the retailers seeing 5-15% revenue lift from the ones running pilots that stall is the state of the identity, event and inventory data underneath.</p>
<p>Three data foundations matter more than model choice. The first is identity resolution: a retailer that cannot reliably connect a web session, an app session, a loyalty number, and an in-store purchase to one customer is personalising four separate strangers. The practical target is not perfection but a measured match rate — most retailers should know their recognised-visitor rate per channel and treat anything below 50% as the binding constraint on the programme. The second is event freshness. A recommendation that reflects browsing behaviour from last night is worth a fraction of one that reflects the last ten minutes, and the gap shows up directly in click-through. The third is inventory and margin awareness. A recommendation engine that promotes an item which is out of stock, or one carrying a negative contribution margin once fulfilment is included, actively destroys value while reporting healthy engagement.</p>
<h3>The measurement trap</h3>
<p>The most common failure in retail personalisation is attributing to the algorithm what was caused by the merchandising calendar. A lift measured against a pre-period that happens to include a promotional weekend is not a lift. The discipline that fixes this is holdout-based measurement: keep a randomised control group that receives no personalisation, at a level large enough to detect a two to three point difference, and hold it for a full season. Retailers who adopt persistent holdouts routinely discover that some of their most celebrated personalisation wins were seasonal artefacts — and, just as often, that genuinely valuable placements were being undervalued.</p>
<h2 id="how-do-you-scale-personalization-across-channels">How Do You Scale Personalization Across Channels?</h2>
<p>Single-channel personalisation is a solved problem; cross-channel personalisation is where 2025 programmes are actually being won and lost. The customer does not experience channels, they experience a brand, and the inconsistency is what they notice: an email recommending a product they bought in-store yesterday, a website hero banner ignoring a category they browse weekly, an app promotion that contradicts the price shown online.</p>
<p>Scaling across channels requires one decision layer rather than one per channel. Concretely, that means a central decisioning service that owns the customer's next-best-action and is called by every channel at render time, rather than four teams each running their own ranking logic against their own data copy. The pattern has three components: a shared customer profile assembled from all channels, a shared catalogue and inventory view, and a decision API that returns a ranked set of actions with an explanation. Channels then compete for the same decision rather than making independent ones, which is what makes frequency capping, offer suppression, and margin-aware ranking possible at all.</p>
<p>The organisational change is harder than the technical one. Cross-channel decisioning means someone owns the customer's experience end to end, which in most retail structures means taking a measure of autonomy away from channel teams. The retailers that have made this work typically start with a narrow, high-value scope — offer suppression and frequency capping across email and app — prove the revenue impact, then extend to ranking and content.</p>
<h2 id="what-should-retailers-do-in-the-first-100-days">What Should Retailers Do in the First 100 Days?</h2>
<p>The difference between a personalisation programme that compounds and one that gets shelved is usually decided in the first hundred days. A practical sequence:</p>
<ul>
<li><strong>Days 1-20 — measure the baseline honestly.</strong> Establish the recognised-visitor rate by channel, the share of sessions with any personalisation at all, the current conversion and AOV by segment, and the lag between an event happening and it being available for decisioning. Most retailers find the last number is the embarrassing one.</li>
<li><strong>Days 21-45 — pick one decision and instrument it.</strong> Not "personalise the homepage" but "rank the four category tiles on the homepage by predicted affinity." One decision, one surface, one metric. Build the holdout at the same time.</li>
<li><strong>Days 46-70 — close the loop with the business teams.</strong> Put the results in front of merchants and buyers weekly. The qualitative feedback on why a recommendation was wrong — seasonality, a supplier issue, a margin constraint the model cannot see — is the highest-value input to the next iteration.</li>
<li><strong>Days 71-100 — extend to the second surface and write down the operating model.</strong> Who owns the profile? Who approves a new decision? What is the escalation path when a recommendation is commercially wrong? Programmes that skip this step stall at the second surface.</li>
</ul>
<p>Throughout, the guardrail that keeps personalisation from becoming intrusion is transparency of value exchange: the customer should be able to see that the brand is using what it knows to save them time or money. Retailers who state the benefit explicitly — "we remembered your size," "this is back in stock in your store" — see materially higher opt-in rates than those who personalise silently.</p>
"""

S2_EN_FAQ = [
    ("What is the realistic revenue lift from retail AI personalization in 2025?",
     "Retailers executing well report 5-15% revenue lift and 10-30% improvement in marketing spend efficiency, with personalisation leaders generating around 40% more revenue from these activities than average performers. Those numbers depend on identity resolution quality and on measurement discipline; programmes without a randomised holdout frequently overstate lift by attributing seasonal effects to the algorithm."),
    ("How much customer data do you need before personalization is worth running?",
     "Less than most programmes assume, provided the data is connected. A single recognised identifier plus six to eight weeks of behavioural events is enough to run meaningful affinity-based ranking. The binding constraint is usually identity resolution across channels rather than volume — a retailer that recognises 40% of its traffic cannot personalise the other 60%."),
    ("How do retailers personalize without triggering privacy complaints?",
     "Anchor every use to a stated value exchange and to the purpose the customer agreed to. Practically: use first-party data collected with clear consent, prefer on-site behavioural context over sensitive attributes, offer visible controls, and never personalise in a way that reveals inference the customer did not expect. Transparency about why a recommendation appeared raises engagement rather than lowering it."),
    ("Should personalization be built in-house or bought?",
     "Buy the ranking and retrieval infrastructure, build the decision layer. Recommendation models, feature stores and experimentation platforms are commodity services; the customer profile, the catalogue and margin logic, and the next-best-action policy are where a retailer's actual differentiation lives and where vendor software cannot encode its specific economics."),
    ("What is the most common reason personalization programmes stall?",
     "Measurement credibility. Programmes that cannot separate algorithmic lift from merchandising calendar effects lose internal trust after the first season, usually when a reported win fails to repeat. Persistent randomised holdouts, agreed before launch and held for a full season, are the single most reliable defence against this."),
]

S2_ZH_FAQ = [
    ("2025年零售AI個性化能帶來多少實際的營收提升？",
     "執行到位的零售商報告營收提升5%至15%，營銷支出效率提升10%至30%；個性化領先者從這些活動中獲得的營收比平均水平高出約40%。這些數字取決於身份識別的質量與衡量紀律：沒有隨機對照組的項目，往往把季節性因素誤算成算法效果，從而高估提升幅度。"),
    ("需要多少顧客數據才值得啟動個性化？",
     "只要數據是打通的，所需量比多數項目想像的少。一個可識別的身份標識加上六到八週的行為事件，就足以支撐有意義的偏好排序。真正的瓶頸通常是跨渠道的身份識別率，而不是數據量——只能識別40%流量的零售商，無法為其餘60%提供個性化。"),
    ("零售商如何在個性化的同時避免引發隱私顧慮？",
     "把每一次使用都錨定在明確的價值交換和顧客已同意的用途上。具體做法：優先使用徵得明確同意的第一方數據；優先使用站內行為上下文而非敏感屬性；提供可見的控制開關；絕不以顧客意料之外的方式暴露推斷結果。說明推薦出現的原因會提高而非降低參與度。"),
    ("個性化應該自建還是採購？",
     "排序與檢索基礎設施採購，決策層自建。推薦模型、特徵平台與實驗平台都是標準化的雲服務；顧客畫像、目錄與毛利邏輯、以及「下一步最佳動作」策略，才是零售商真正的差異所在，也是供應商軟體無法編碼其具體經營邏輯的部分。"),
    ("個性化項目停滯最常見的原因是什麼？",
     "衡量結果失去可信度。無法區分算法提升與商品日曆效應的項目，會在第一個季度之後失去內部信任，通常是當一次報告的提升未能重現時。在啟動前就約定、並保留整個季度的隨機對照組，是對抗這一問題最可靠的做法。"),
]

S2_CN_H2 = [
    ("2025年AI驱动的行业转型", "2025年AI驱动的行业转型体现在哪些方面？"),
    ("金融服务：AI作为竞争差异化因素", "为什么金融服务把AI视为竞争差异化的关键？"),
    ("人机协作的必要性", "为什么零售AI必须保留人机协作？"),
]
S2_TW_H2 = [
    ("2025年AI驅動的行業轉型", "2025年AI驅動的行業轉型體現在哪些方面？"),
    ("金融服務：AI作為競爭差異化因素", "為什麼金融服務把AI視為競爭差異化的關鍵？"),
    ("人機協作的必要性", "為什麼零售AI必須保留人機協作？"),
]

# ---------------------------------------------------------------- slug 3
S3 = "conversational-analytics-financial-planning"

S3_EN_ADD = """
<h2 id="what-breaks-when-conversational-analytics-meets-the-close">What Breaks When Conversational Analytics Meets the Close?</h2>
<p>The monthly close is the stress test that separates a conversational analytics demo from a finance-grade system, and there are four specific places where unprepared deployments fail. Understanding them in advance is most of the work.</p>
<p>The first is the restatement problem. Actuals get revised: an accrual is trued up, an intercompany elimination moves, a late invoice lands. A conversational system that answered "what was Q2 gross margin?" on the 3rd of the month must be able to acknowledge that the number it gives on the 20th is different, and explain why. Finance users will forgive a changed number and will never forgive an unexplained one. The requirement is a versioned actuals store with as-of querying, so the platform can answer both "what is the margin?" and "what did we think the margin was during the close?"</p>
<p>The second is the reconciliation requirement. When a conversational answer differs from the board pack by even a rounding rule, trust collapses instantly. That means the semantic layer cannot be a parallel implementation of finance logic; it must read the same definitions the planning and consolidation systems use, ideally by calling them rather than re-implementing them. The third is period intelligence — fiscal calendars, 4-4-5 retail calendars, thirteen-week quarters, and the difference between "last month" in the management calendar and in the ledger. A surprising share of finance query errors are calendar errors. The fourth is permissioning at the entity level: a regional CFO may see their region's actuals and the consolidated plan, but not other regions' detail, and that rule has to hold inside a conversational answer that may be forwarded into a chat thread.</p>
<h2 id="how-do-you-govern-a-finance-semantic-layer">How Do You Govern a Finance Semantic Layer?</h2>
<p>A finance semantic layer is not a data project; it is an accountability structure expressed in metadata. Each metric needs four things recorded: a single calculation, stated in business language and in code; a named owner who resolves disputes; a version history, because definitions change and users need to know when; and a usage scope that says which reports and which conversations are allowed to use it.</p>
<p>The governance operating model that works in practice is small and boring. A metrics council of four to six people — usually the FP&amp;A lead, the controller, one business-partner representative, and the analytics owner — meets monthly, reviews proposed definition changes, and approves or rejects them. Every change is versioned with an effective date. Every deprecated metric keeps working for a defined sunset period so that historical questions still resolve. This is unglamorous, and it is the difference between a semantic layer that finance trusts and one that finance routes around with spreadsheets.</p>
<p>One specific practice pays disproportionate dividends: publishing the definition alongside the answer. When a conversational response to "what is our EBITDA?" can be expanded to show the exact calculation, the owner's name, and the last revision date, disputes stop being about whose number is right and start being about what the business should do. Teams that implement definition-on-demand report a sharp drop in the volume of reconciliation tickets within two cycles.</p>
<h2 id="what-does-good-look-like-after-two-planning-cycles">What Does Good Look Like After Two Planning Cycles?</h2>
<p>The honest test of a conversational FP&amp;A deployment is what has changed by the second full planning cycle. Three outcomes are realistic and worth holding the programme to.</p>
<ul>
<li><strong>Assembly time collapses.</strong> Finance teams commonly spend up to 70% of their effort collecting, validating and assembling data. In a working deployment, that figure drops by roughly half within two cycles, because the semantic layer performs the definition and validation work and the conversational interface removes the extract-and-rebuild step.</li>
<li><strong>The question backlog becomes visible and shrinkable.</strong> Every unanswered question is logged. By the second cycle, the log is the roadmap, and the share of leadership questions answered live during the review meeting typically moves from near zero past 60%.</li>
<li><strong>Scenario work becomes routine rather than heroic.</strong> When "what happens to full-year margin if freight stays at this level and we hold headcount flat?" takes seconds instead of a day of analyst time, the number of scenarios the business actually considers rises sharply. This is the outcome that changes decisions, and it is the one that is hardest to attribute but most valuable.</li>
</ul>
<p>What should not be expected is the elimination of the analyst role. The teams that gain most are the ones that redeploy analyst capacity from assembly to interpretation — from producing the variance to explaining it — and that redeployment, not headcount reduction, is where the ROI actually shows up in the second cycle.</p>
"""

S3_EN_FAQ = [
    ("How accurate is conversational analytics on finance-specific questions?",
     "On a well-scoped planning vocabulary, natural-language understanding resolves intent correctly more than 94% of the time. The larger accuracy risk is not parsing but definition: if the semantic layer does not reuse the definitions the planning and consolidation systems use, a correctly parsed question still produces a number that does not reconcile with the board pack."),
    ("Can conversational analytics handle restated actuals after the close?",
     "Yes, if the platform stores versioned actuals and supports as-of querying. This is a hard requirement rather than a nice-to-have, because finance users will accept a number that changed and will not accept one that changed without explanation. Ask any vendor to demonstrate a restatement before you buy."),
    ("Does conversational FP&A work with existing planning tools?",
     "It should connect to them rather than replace them. The practical pattern is a semantic layer that calls the planning model and the ledger directly, so scenario questions resolve against the same assumptions the plan uses. Re-implementing planning logic in the analytics layer is the most common architectural mistake and the most expensive to unwind."),
    ("How long before a finance team sees measurable value?",
     "Expect the first visible win inside one monthly business review cycle, typically four to six weeks, and a material change in how the team spends its time by the second full planning cycle. Programmes scoped to one recurring meeting outperform programmes scoped to a department."),
    ("What stops finance teams from trusting conversational answers?",
     "Unreconciled numbers, unexplained restatements, and invisible ownership. All three are solved by governance rather than by model accuracy: reuse the approved definitions, version every change, publish the owner beside every answer, and surface the calculation on demand."),
]

S3_ZH_FAQ = [
    ("對話式分析在財務專業問題上的準確率如何？",
     "在範圍界定良好的規劃詞彙上，自然語言理解的意圖識別準確率超過94%。更大的準確性風險不在於解析，而在於定義：如果語義層沒有複用規劃與合併系統使用的定義，即使問題被正確解析，得出的數字仍無法與董事會報告對齊。"),
    ("對話式分析能否處理結帳後的重述？",
     "可以，前提是平台保存版本化的實際值並支持「截至某一時點」的查詢。這是硬性要求而非加分項，因為財務人員可以接受數字變化，但不能接受變化而沒有解釋。在採購前，應要求供應商演示一次重述場景。"),
    ("對話式財務規劃能否與現有規劃工具配合？",
     "它應該連接而非取代現有工具。實用的模式是語義層直接調用規劃模型與總帳，使情景問題在與計劃相同的假設下求解。在分析層重新實現規劃邏輯，是最常見也最難逆轉的架構錯誤。"),
    ("財務團隊需要多久才能看到可衡量的價值？",
     "通常在一個月度經營複盤週期內（約四到六週）就能看到第一個可見的成果；到第二個完整規劃週期，團隊的時間分配會發生實質改變。圍繞一次固定會議來界定範圍的項目，效果優於按部門界定範圍的項目。"),
    ("是什麼阻礙財務團隊信任對話式答案？",
     "數字對不上、重述沒有解釋、責任人不可見。這三點都靠治理而非模型準確率來解決：複用已批准的定義、對每次變更做版本管理、在每個答案旁公開責任人，並支持按需查看計算過程。"),
]

S3_CN_H2 = [
    ("传统BI的局限性与变革的理由", "传统BI在财务场景中有哪些局限？"),
    ("核心技术组件", "对话式财务分析需要哪些核心技术组件？"),
    ("实施策略与最佳实践", "财务团队应该如何实施对话式分析？"),
    ("对话式BI的进阶能力与未来演进", "对话式BI的进阶能力将如何演进？"),
    ("对话式BI技术架构深度解析", "对话式BI的技术架构应该如何设计？"),
    ("战略实施路径与关键成功因素", "战略实施路径与关键成功因素是什么？"),
    ("企业实施路线图与成功因素", "企业实施路线图应该如何规划？"),
    ("行业数字化转型深度分析", "财务数字化转趋势对企业意味着什么？"),
]
S3_TW_H2 = [
    ("傳統BI的侷限性與變革的理由", "傳統BI在財務場景中有哪些侷限？"),
    ("核心技術元件", "對話式財務分析需要哪些核心技術元件？"),
    ("實施策略與最佳實踐", "財務團隊應該如何實施對話式分析？"),
    ("對話式BI的進階能力與未來演進", "對話式BI的進階能力將如何演進？"),
    ("對話式BI技術架構深度解析", "對話式BI的技術架構應該如何設計？"),
    ("戰略實施路徑與關鍵成功因素", "戰略實施路徑與關鍵成功因素是什麼？"),
    ("企業實施路線圖與成功因素", "企業實施路線圖應該如何規劃？"),
    ("行業數位轉型深度分析", "財務數位轉型趨勢對企業意味著什麼？"),
]

# ---------------------------------------------------------------- slug 4
S4 = "q3-2025-enterprise-ai-compliance-landscape"

S4_EN_ADD = """
<h2 id="what-does-a-defensible-ai-inventory-look-like">What Does a Defensible AI Inventory Look Like?</h2>
<p>Every obligation in the Q3 2025 landscape — EU GPAI documentation, prohibition screening, China's labeling rule, Colorado's impact assessments, California's covered-model thresholds — presumes one artefact: a complete, current inventory of the AI systems you operate. It is the least glamorous deliverable in enterprise AI compliance and the one that determines whether everything else is possible. Most enterprises that attempt it discover 30-50% more AI in production than they knew about, largely embedded in vendor software.</p>
<p>A defensible inventory records, for each system: the business owner, the technical owner, the purpose, the data categories processed, whether the system is built or bought, the vendor and contract reference, the jurisdictions and user populations it touches, the risk classification under each applicable regime, and the date of last review. The vendor-embedded category deserves particular attention, because a procurement decision made eighteen months ago may have quietly brought a general-purpose model into a customer-facing workflow, and that system is in scope whether or not anyone in the AI programme knows about it. The practical discovery mechanism is not a survey but a contract and architecture review: read the AI and data-processing terms in vendor agreements, and add an AI-disclosure question to the intake process for every new purchase.</p>
<p>The inventory has to be a living system, not a spreadsheet produced once. The pattern that works is to attach the inventory step to an existing control gate — procurement, architecture review, or change management — so that a system cannot reach production without an entry. Enterprises that bolt the inventory onto an existing gate keep it current; enterprises that run it as a quarterly exercise watch it decay within two cycles.</p>
<h2 id="how-should-multinationals-handle-conflicting-obligations">How Should Multinationals Handle Conflicting Obligations?</h2>
<p>Conflict between jurisdictions is real, but it is less common than apparent conflict. Most divergence is in thresholds and timing rather than in substance, which means the practical strategy is to build to the strictest applicable requirement and document the mapping — rather than maintaining a separate system per jurisdiction.</p>
<p>Three conflicts are genuine and require a decision rather than a mapping. The first is training-data transparency versus trade-secret protection: EU documentation duties expect disclosure about training data that vendors treat as proprietary, and the resolution is contractual, by obtaining documentation rights in procurement rather than trying to extract them later. The second is data localisation versus centralised model operations: China's localisation expectations for personal information and certain data categories conflict with a single global feature store, and the resolution is architectural — regional deployment with a shared semantic layer and no raw personal data crossing the boundary. The third is automated decision-making rights: where individuals have a right to explanation and to human intervention, a system designed for fully automated throughput needs a designed escalation path, and that path has to exist before launch, not after the first complaint.</p>
<p>The governing principle that regulators in every jurisdiction have signalled is demonstrability. An enterprise that can show what it did, when, on what basis, and who approved it is in a materially stronger position than one that merely believes it complied. This is why audit trails are not an afterthought: they are the artefact that converts a compliance programme from an assertion into evidence.</p>
<h2 id="what-should-be-done-in-the-next-90-days">What Should Compliance Teams Do in the Next 90 Days?</h2>
<p>Sequenced by date and by exposure, the next ninety days have a clear shape for a multinational that has not yet built a programme.</p>
<ol>
<li><strong>Days 1-30 — close what is already overdue.</strong> EU GPAI documentation for any general-purpose model in scope; content labeling for any pipeline producing AI-generated content for China; prohibition screening across the whole AI inventory. These are obligations with dates already passed, and they are where enforcement attention is concentrated.</li>
<li><strong>Days 31-60 — build the inventory and the risk classification.</strong> Discover, classify, assign owners. Produce the mapping from each system to each applicable regime, and identify the systems that are high-risk in at least one jurisdiction. Expect this to be the largest single piece of work.</li>
<li><strong>Days 61-90 — stand up the operating model.</strong> Metrics council equivalent for AI: a named approver for new use cases, a standing review for systems changing materially, an incident path for model failures or complaints, and an audit-trail format that satisfies the strictest regime you operate under.</li>
</ol>
<p>Two investments made in this window pay for themselves repeatedly. The first is a standard documentation template — model card, data summary, purpose statement, human-oversight description — that every use case fills in, because regulators in different jurisdictions ask the same underlying questions in different formats. The second is a procurement clause set covering AI disclosure, training-data documentation rights, and audit cooperation, because the fastest-growing share of enterprise AI exposure arrives through vendor contracts rather than internal builds.</p>
"""

S4_EN_FAQ = [
    ("What is the single highest-priority action for Q3 2025 compliance?",
     "Complete an AI system inventory with risk classification under each jurisdiction you operate in. Every other obligation — GPAI documentation, prohibition screening, labeling, impact assessments — depends on knowing which systems exist, and most enterprises find 30-50% more AI in production than they expected, mainly inside vendor software."),
    ("Do the EU AI Act obligations apply to companies outside the EU?",
     "Yes, where the system is placed on the EU market or its output is used in the EU. The GPAI obligations that applied on 2 August 2025 reach providers putting general-purpose models on the EU market regardless of where the provider is established, and deployers using those models in EU-facing workflows carry their own downstream duties."),
    ("How should enterprises handle obligations that genuinely conflict across jurisdictions?",
     "Build to the strictest applicable requirement and document the mapping, reserving genuine architectural divergence for the three real conflicts: training-data disclosure versus trade secrets (solve contractually), data localisation versus centralised operations (solve with regional deployment), and automated decision-making rights (solve with a designed escalation path)."),
    ("What evidence do regulators actually expect?",
     "Demonstrability: what was done, when, on what basis, and who approved it. In practice that means a versioned inventory, documented risk classifications, impact assessments where required, records of human oversight, and immutable logs of material decisions about each system. An audit trail built at launch is far more persuasive than one reconstructed later."),
    ("How much of enterprise AI compliance risk comes from vendors?",
     "A growing majority. Procurement decisions made before a programme existed routinely bring general-purpose models into customer-facing workflows without the AI team's knowledge. The practical controls are an AI-disclosure question in procurement intake, contractual rights to training-data documentation, and audit-cooperation clauses in vendor agreements."),
]

S4_ZH_FAQ = [
    ("2025年第三季度合規工作的首要任務是什麼？",
     "完成AI系統盤點，並按業務涉及的每個司法管轄區做風險分類。其他所有義務——通用AI文檔、禁止性用途篩查、內容標識、影響評估——都依賴於知道系統的存在；多數企業會發現生產環境中的AI比預期多出30%至50%，主要來自供應商軟體。"),
    ("歐盟AI法案的義務是否適用於歐盟以外的公司？",
     "適用，前提是系統被投放歐盟市場或其輸出在歐盟境內被使用。2025年8月2日生效的通用AI義務約束所有將通用模型投放歐盟市場的提供者，無論其註冊地在何處；在面向歐盟的工作流中使用這些模型的部署方也承擔各自的下游義務。"),
    ("企業應如何處理跨司法管轄區真正衝突的義務？",
     "按最嚴格的要求建設並記錄映射關係，只把真正的架構性分歧留給三類實質衝突：訓練數據披露與商業秘密保護（通過合同解決）、數據本地化與集中運營（通過區域化部署解決）、自動化決策權利（通過設計好的升級路徑解決）。"),
    ("監管機構真正期望的是什麼樣的證據？",
     "可證明性：做了什麼、何時做的、基於什麼依據、由誰批准。具體而言是帶版本的系統盤點、有據可查的風險分類、必要時的影響評估、人工監督記錄，以及關於每個系統重大決策的不可篡改日誌。在系統上線時就建立的審計追蹤，遠比事後重建更有說服力。"),
    ("企業AI合規風險有多大比例來自供應商？",
     "佔比正在持續上升。在合規體系建立之前做出的採購決策，常常把通用模型帶入面向客戶的工作流，而AI團隊並不知情。可行的控制手段包括：在採購准入環節加入AI披露問項、在合同中約定訓練數據文檔的獲取權，以及在供應商協議中加入審計配合條款。"),
]

S4_CN_H2 = [
    ("2025年中期的监管格局", "2025年中期的监管格局是怎样的？"),
    ("关键合规要求", "企业需要满足哪些关键合规要求？"),
    ("跨司法管辖区挑战", "跨司法管辖区运营有哪些挑战？"),
    ("实施策略", "企业应该采取怎样的实施策略？"),
    ("为下一波监管浪潮做准备", "企业应该如何为下一波监管浪潮做准备？"),
]
S4_TW_H2 = [
    ("2025年中的監管格局", "2025年中的監管格局是怎樣的？"),
    ("關鍵合規要求", "企業需要滿足哪些關鍵合規要求？"),
    ("跨司法管轄區挑戰", "跨司法管轄區運營有哪些挑戰？"),
    ("實施策略", "企業應該採取怎樣的實施策略？"),
    ("為下一波監管浪潮做準備", "企業應該如何為下一波監管浪潮做準備？"),
]

# ---------------------------------------------------------------- slug 5
S5 = "design-ai-augmented-dashboards"

S5_EN_ADD = """
<h2 id="what-should-an-ai-dashboard-show-that-a-traditional-one-cannot">What Should an AI Dashboard Show That a Traditional One Cannot?</h2>
<p>The test of an AI-augmented dashboard is not that it has a chat box bolted onto a chart grid. It is that it answers three questions a traditional dashboard structurally cannot: what changed, why it changed, and what to do about it. Most dashboard portfolios answer none of them, because they were designed to display measures, not to explain movements.</p>
<p><strong>What changed</strong> requires anomaly detection running against every metric on the screen, with a baseline that understands seasonality and the business calendar. A 4% dip in Monday traffic is noise; a 4% dip in the first hour of a promotion is a problem. The difference is the baseline, and a static target line is not a baseline. <strong>Why it changed</strong> requires automated driver analysis: decomposing a variance across its contributing dimensions and ranking them by contribution, so the reader is shown "the change is 70% explained by two regions and one product line" rather than being handed a chart and invited to investigate. <strong>What to do about it</strong> is the hardest and least automated of the three, and the honest answer is that most platforms stop at the first two — which is still a large improvement over the status quo, provided the interface is explicit about which claims are machine-generated and which are human interpretation.</p>
<p>The design consequence is that the dashboard's default state changes. A traditional dashboard is a grid the user interrogates. An AI-augmented dashboard is a narrative the user can interrogate: a headline statement about what moved, the evidence beneath it, and the ability to ask a follow-up question in place. Users who are shown a conclusion and then permitted to challenge it consistently reach an accurate understanding faster than users who are shown data and asked to find the conclusion themselves.</p>
<h2 id="how-do-you-keep-ai-insights-from-becoming-noise">How Do You Keep AI Insights From Becoming Noise?</h2>
<p>Proactive insight delivery is the highest-value feature in an AI dashboard and the fastest way to destroy its value. The failure mode is well documented: alerts fire on everything, users learn that the alerts are noise, and within weeks the notification channel is muted. Preventing it requires treating insight delivery as a product with a budget rather than a feature that is switched on.</p>
<p>Three constraints work. The first is a volume budget: a user should receive a small, fixed number of insights per period — typically three to five per week — which forces ranking by materiality rather than by statistical significance alone. The second is materiality thresholds expressed in business units, not standard deviations: alert when margin moves more than a defined basis-point band or when a metric crosses a commitment threshold, not when a z-score exceeds two. The third is suppression logic: no duplicate insights about the same driver, no alerts on metrics the user has already seen and dismissed this week, and no insight that cannot name at least one driver.</p>
<p>The fourth constraint is the one most often skipped — a feedback channel. Every insight needs a one-click "not useful" control, and that signal has to feed the ranking model. Teams that instrument insight quality this way see relevance scores climb steadily; teams that do not are guessing, and their alert volume tends to grow rather than shrink because nobody can safely turn anything off.</p>
<h2 id="what-is-the-migration-path-from-static-to-ai-augmented">What Is the Migration Path From Static to AI-Augmented?</h2>
<p>Replacing a dashboard portfolio wholesale is the approach that fails; the portfolios are large, politically embedded, and some of them are load-bearing. The migration that works is additive and evidence-driven.</p>
<ol>
<li><strong>Instrument before you change anything.</strong> Measure actual usage per dashboard, not page views but distinct decision-makers per month. Most enterprises find that a small fraction of dashboards carry nearly all the value and a long tail has none.</li>
<li><strong>Augment the top decile first.</strong> Take the ten or twenty dashboards that carry the most decision traffic and add anomaly detection, driver explanation, and natural-language query. This is where the 30-45% improvements in comprehension and time-to-action are actually realised.</li>
<li><strong>Retire on evidence, in public.</strong> For the long tail, publish the usage data and set a review date. Dashboards nobody defends get retired. Doing this with the numbers visible converts a political argument into an administrative one.</li>
<li><strong>Make the conversational path the default for new requests.</strong> Every new "can you build a dashboard for X?" becomes "let's add X to the semantic layer so the question can be asked." This is the step that prevents regrowth.</li>
</ol>
<p>Throughout, one architectural decision determines whether the migration holds: the semantic layer must be shared. If the conversational interface and the dashboards read from different definitions, the organisation ends up with two numbers for everything and the trust problem gets worse rather than better.</p>
"""

S5_EN_FAQ = [
    ("What makes an AI dashboard different from a traditional one?",
     "It explains rather than only displays. Beyond visualisation, an AI-augmented dashboard runs anomaly detection against a seasonality-aware baseline, decomposes variances into ranked drivers, accepts natural-language follow-up questions, and can push a small number of material insights proactively. The default state changes from a grid the user interrogates to a narrative the user challenges."),
    ("How do you balance AI insights with traditional charts?",
     "Keep charts for known metrics and trends, where visual comparison is genuinely efficient, and use AI overlays for the three things charts handle badly: detecting that something moved, explaining which dimensions caused it, and surfacing it without being asked. Never let a machine-generated annotation replace the underlying numbers — always keep the source values visible beneath the explanation."),
    ("How do you stop proactive alerts from becoming noise?",
     "Impose a volume budget of roughly three to five insights per user per week, set thresholds in business units rather than statistical ones, suppress duplicates and recently dismissed items, require every alert to name at least one driver, and add a one-click 'not useful' control that feeds the ranking model."),
    ("Should existing dashboards be replaced?",
     "Not wholesale. Measure real usage first, augment the small set that carries most decision traffic, and retire the long tail on published evidence with a review date. Then change the intake process so new requests add metrics to the semantic layer instead of producing new dashboards, which is what prevents the sprawl returning."),
    ("What architecture does an AI dashboard need?",
     "A governed semantic layer shared with every other consumption surface, an event or streaming path fresh enough for the decisions being made, a metric store with versioned definitions, and a permission model that survives an answer being forwarded into a chat thread. Without the shared semantic layer, AI and dashboards will disagree and trust will fall."),
]

S5_ZH_FAQ = [
    ("AI儀表板與傳統儀表板有什麼不同？",
     "它在於解釋而不只是展示。除可視化之外，AI增強儀表板會基於考慮季節性的基準線做異常檢測、將差異分解為按貢獻排序的驅動因素、支持自然語言追問，並能主動推送少量重要的洞察。默認狀態從「用戶去查詢的圖表格」變成「用戶可以質疑的一段敘述」。"),
    ("如何平衡AI洞察與傳統圖表？",
     "圖表用於已知的指標與趨勢，因為視覺比較在這些場景確實高效；AI疊加層用於圖表處理不好的三件事：發現指標發生了變化、解釋是哪些維度造成的、以及在沒有被詢問時主動呈現。永遠不要讓機器生成的註解取代底層數字——解釋之下必須保留原始數值。"),
    ("如何避免主動告警變成噪音？",
     "設定每位用戶每週三到五條的數量預算；用業務單位而非統計單位設定閾值；抑制重複項與用戶本週已忽略的內容；要求每條告警至少能說出一個驅動因素；並加入「沒用」的一鍵反饋，讓該信號回流到排序模型。"),
    ("現有儀表板是否應該被替換？",
     "不應整體替換。先衡量真實使用情況，增強承載最多決策流量的那一小部分，再依據公開的證據為長尾設定複審日期並下線。然後改變需求入口：新需求應把指標加入語義層，而不是新建儀表板，這樣才能防止蔓延再次發生。"),
    ("AI儀表板需要怎樣的技術架構？",
     "需要一個與所有其他消費端共享的受控語義層、足夠新鮮以支撐當前決策的事件或流式管道、帶版本管理的指標儲存，以及即使答案被轉發到聊天會話中仍然有效的權限模型。缺少共享語義層，AI與儀表板會給出相互矛盾的數字，信任反而下降。"),
]

S5_CN_H2 = [
    ("为什么传统仪表板正在不足", "为什么传统仪表板越来越不够用？"),
    ("AI增强仪表板设计原则", "AI增强仪表板的设计原则是什么？"),
    ("对话式交互与主动洞察", "对话式交互与主动洞察如何结合？"),
    ("AI仪表板的技术架构", "AI仪表板需要怎样的技术架构？"),
]
S5_TW_H2 = [
    ("為什麼傳統儀錶板正在不足", "為什麼傳統儀表板越來越不夠用？"),
    ("AI增強儀錶板設計原則", "AI增強儀表板的設計原則是什麼？"),
    ("對話式互動與主動洞察", "對話式互動與主動洞察如何結合？"),
    ("AI儀錶板的技術架構", "AI儀表板需要怎樣的技術架構？"),
]

DATA = {
    S1: {
        "EN": {"h2": [
            ("The Conversational BI Revolution", "Why Is Conversational BI Reshaping Executive Analytics?"),
            ("Architecture and Technical Foundation", "What Architecture Does Conversational BI Need?"),
            ("Implementation Best Practices", "How Should Enterprises Roll Out Conversational BI?"),
            ("Measuring Conversational BI Impact", "How Do You Measure Conversational BI Impact?"),
        ], "add": S1_EN_ADD, "faq": S1_EN_FAQ},
        "zh-CN": {"h2": S1_CN_H2, "faq": S1_ZH_FAQ},
        "zh-TW": {"h2": S1_TW_H2, "faq": S1_ZH_FAQ},
    },
    S2: {
        "EN": {"h2": [
            ("From Recommendations to Conversations", "From Recommendations to Conversations: What Changes?"),
            ("Measuring Personalization ROI and Getting Started", "How Should Retailers Measure Personalization ROI?"),
        ], "add": S2_EN_ADD, "faq": S2_EN_FAQ},
        "zh-CN": {"h2": S2_CN_H2, "faq": S2_ZH_FAQ},
        "zh-TW": {"h2": S2_TW_H2, "faq": S2_ZH_FAQ},
    },
    S3: {
        "EN": {"h2": [
            ("The Limits of Traditional BI and the Case for Change", "What Are the Limits of Traditional BI in Finance?"),
            ("Core Technology Components", "What Core Components Does Conversational FP&A Need?"),
            ("Implementation Strategy and Best Practices", "How Should Finance Teams Implement Conversational Analytics?"),
            ("Use Cases Across the Planning Cycle", "Where Does Conversational Analytics Fit in the Planning Cycle?"),
            ("In-Depth Analysis of Conversational BI Technical Architecture", "How Should the Conversational BI Architecture Be Built?"),
        ], "add": S3_EN_ADD, "faq": S3_EN_FAQ},
        "zh-CN": {"h2": S3_CN_H2, "faq": S3_ZH_FAQ},
        "zh-TW": {"h2": S3_TW_H2, "faq": S3_ZH_FAQ},
    },
    S4: {
        "EN": {"h2": [
            ("The Regulatory Landscape in Mid-2025", "What Does the AI Regulatory Landscape Look Like in Mid-2025?"),
            ("Key Compliance Requirements", "Which Compliance Requirements Matter Most Now?"),
            ("Cross-Jurisdictional Challenges", "What Makes Cross-Jurisdictional Compliance Hard?"),
            ("Implementation Strategies", "How Should Compliance Work Be Sequenced?"),
            ("Preparing for the Next Wave of Regulation", "How Do You Prepare for the Next Wave of AI Regulation?"),
        ], "add": S4_EN_ADD, "faq": S4_EN_FAQ},
        "zh-CN": {"h2": S4_CN_H2, "faq": S4_ZH_FAQ},
        "zh-TW": {"h2": S4_TW_H2, "faq": S4_ZH_FAQ},
    },
    S5: {
        "EN": {"h2": [
            ("Principles of AI-Augmented Dashboard Design", "What Are the Principles of AI-Augmented Dashboard Design?"),
            ("Technical Architecture for AI Dashboards", "What Architecture Do AI Dashboards Need?"),
        ], "add": S5_EN_ADD, "faq": S5_EN_FAQ},
        "zh-CN": {"h2": S5_CN_H2, "faq": S5_ZH_FAQ},
        "zh-TW": {"h2": S5_TW_H2, "faq": S5_ZH_FAQ},
    },
}
