# -*- coding: utf-8 -*-
"""Batch 3 content: slugs 11-15."""

S11 = "hidden-cost-dashboard-sprawl-enterprises"

S11_EN_ADD = """
<h2 id="why-do-dashboards-multiply-in-the-first-place">Why Do Dashboards Multiply in the First Place?</h2>
<p>Sprawl is not a failure of discipline; it is the predictable output of a system with the wrong incentives. Understanding the mechanism is what makes the fix durable, because programmes that simply delete dashboards watch them grow back within two quarters.</p>
<p>Three forces drive multiplication. The first is that a dashboard is the cheapest way to answer an unscheduled question. When someone needs a number that no existing view provides, building a new dashboard takes hours and is fully within their control, whereas changing an existing one requires negotiating with its owner and risks breaking someone else's workflow. The rational individual choice is always to build new. The second is that dashboards are treated as free at the point of creation. Licensing is paid centrally, maintenance is invisible until it is overwhelming, and nobody sees the marginal cost of dashboard number 3,000. The third is that dashboards accumulate political value: they are evidence of work, they carry their builder's name, and retiring one feels like a judgement on the person who made it.</p>
<p>Each of those forces has a corresponding countermeasure, and all three are needed. Make asking cheaper than building: a conversational interface backed by a governed semantic layer means the unscheduled question is answered in seconds without an artefact. Make the marginal cost visible: publish the portfolio size, the maintenance hours, and the usage distribution where the people requesting new dashboards can see them. And depersonalise retirement: retire on usage evidence against a published threshold, applied uniformly, rather than through case-by-case negotiation.</p>
<h2 id="what-should-replace-the-dashboards-you-retire">What Should Replace the Dashboards You Retire?</h2>
<p>The most common objection to consolidation is legitimate: some dashboards are genuinely load-bearing, and asking a question every time is not always faster than glancing at a well-designed view. The honest answer is that consolidation is not elimination — it is a change in which artefacts are maintained deliberately.</p>
<p>A useful classification separates three categories. <strong>Monitored metrics</strong> — a small set of numbers that someone watches continuously, where a persistent visual with alerting is genuinely the right interface. These should be kept, but rebuilt on the governed semantic layer so they agree with everything else. <strong>Recurring questions</strong> — the monthly or weekly questions a team asks in the same shape every time. These belong in the semantic layer with a saved question, not in a bespoke dashboard, so the answer is always current and always consistent. <strong>Exploratory views</strong> — dashboards built to investigate something once. These should be retired without replacement, because the investigation is over and the artefact has no ongoing consumer.</p>
<p>Applying that classification in a real portfolio typically produces a result that surprises everyone involved: roughly 10-15% of dashboards are kept and rebuilt, 30-40% become saved questions, and the remainder can be retired with no loss. The reason the result surprises people is that the portfolio was never classified before, and the default assumption was that everything in it was being used.</p>
<p>One architectural requirement governs whether this holds: the semantic layer has to be shared across the surviving dashboards, the conversational interface, and every future artefact. If each surface keeps its own definitions, the organisation has not consolidated — it has simply moved the disagreement into a new place, and the trust cost that made sprawl expensive in the first place remains.</p>
"""

S11_EN_FAQ = [
    ("How do you know if your dashboard portfolio is sprawling?",
     "Run a 90-day usage audit: count how many dashboards were opened by someone other than their creator. In most large portfolios the answer is sobering — a large share have no external viewers at all. Add a second test: count how many dashboards produce numbers that disagree with another dashboard for the same period."),
    ("What is the real cost of dashboard sprawl?",
     "Licensing, maintenance hours, and — largest by far — the organisational cost of conflicting numbers. When two dashboards disagree, meetings become arguments about whose figure is right, decisions get deferred, and teams build shadow spreadsheets. That erosion of trust costs more than the licence line ever will."),
    ("Should all dashboards be replaced by conversational BI?",
     "No. Keep a small set of genuinely monitored metrics as persistent views with alerting, convert recurring questions into saved questions on the semantic layer, and retire exploratory views with no ongoing consumer. Consolidation is a change in what is maintained deliberately, not blanket elimination."),
    ("How do you retire a dashboard without a political fight?",
     "Publish the usage evidence and apply a uniform threshold. When the criterion is 'not opened by anyone but its creator in 90 days, with a two-week objection window,' retirement becomes an administrative action rather than a judgement about the person who built it."),
    ("What stops sprawl from coming back?",
     "Change the intake path. Every request for a new dashboard should first become a metric or a saved question in the semantic layer, with a dashboard created only when continuous monitoring is genuinely required. Without that change, the same incentives that produced the sprawl reproduce it within two quarters."),
]

S11_ZH_FAQ = [
    ("如何判斷企業的儀表板是否已經蔓延？",
     "做一次90天的使用稽核：統計有多少儀表板曾被建立者以外的人打開。在大型組合中，結果通常令人清醒——很大一部分儀表板完全沒有外部使用者。再加上第二個檢驗：統計有多少儀表板產出的數字，與其他儀表板在同一期間的結果不一致。"),
    ("儀表板蔓延的真正成本是什麼？",
     "授權費用、維護工時，以及——遠大於前兩者的——數字衝突所帶來的組織成本。當兩份儀表板數字不一致時，會議就變成爭論誰的數字正確、決策被延後、團隊開始建立影子試算表。這種信任的流失，成本遠超過授權費用。"),
    ("所有儀表板都應該被對話式BI取代嗎？",
     "不應該。保留少量確實需要持續監看的指標作為帶告警的常駐視圖；把週期性的問題轉為語義層上的已儲存問題；對於沒有持續使用者的探索性視圖則直接下線。整併是改變「什麼被有意識地維護」，而不是全面消除。"),
    ("如何在不引發政治爭議的情況下下線儀表板？",
     "公開使用證據並套用一致的門檻。當標準是「90天內除建立者外無人開啟，並有兩週異議期」時，下線就成為一項行政動作，而不是對建立者的評價。"),
    ("如何防止蔓延再次發生？",
     "改變需求入口。每一個新建儀表板的需求，都應先在語義層中成為指標或已儲存問題，只有確實需要持續監看時才建立儀表板。缺少這個改變，當初造成蔓延的誘因會在兩個季度內重現。"),
]

S11_CN_H2 = [
    ("The Hidden Costs: Conflicting Numbers and Eroded Trust", "隐藏成本：数字冲突与被侵蚀的信任是什么？"),
    ("How Conversational BI Eliminates Dashboard Sprawl", "对话式BI如何消除仪表板蔓延？"),
    ("The Migration Path from Dashboards to Conversational BI", "从仪表板迁移到对话式BI的路径是什么？"),
    ("规模化推广的关键成功因素", "规模化推广的关键成功因素是什么？"),
    ("技术基础设施与实施考量", "技术基础设施应该如何考量？"),
    ("中国市场特有的实施优势", "中国市场有哪些特有的实施优势？"),
    ("规模化推广的关键成功因素", "如何防止仪表板蔓延再次发生？"),
]
S11_TW_H2 = [
    ("儀表板蔓延的規模", "儀表板蔓延的規模有多大？"),
    ("隱藏成本：衝突的數字與被侵蝕的信任", "隱藏成本：數字衝突與被侵蝕的信任是什麼？"),
    ("對話式 BI 如何消除儀表板蔓延", "對話式BI如何消除儀表板蔓延？"),
    ("從儀表板遷移到對話式 BI 的路徑", "從儀表板遷移到對話式BI的路徑是什麼？"),
]

# ---------------------------------------------------------------- slug 12
S12 = "sovereign-ai-data-localization-global-enterprise"

S12_EN_ADD = """
<h2 id="how-do-you-architect-for-data-residency-without-fragmenting">How Do You Architect for Data Residency Without Fragmenting?</h2>
<p>The default response to localisation requirements — build a separate stack in each country — produces exactly the outcome enterprises fear: duplicated infrastructure, inconsistent data, divergent models, and a cost base that scales linearly with the number of jurisdictions. The alternative is a layered architecture that localises what must be local and shares everything else.</p>
<p>Four layers make this work. The <strong>control plane</strong> — identity, policy, audit, model registry, prompt and metric definitions — is global and contains no personal or regulated data, so it can be shared everywhere. The <strong>semantic layer</strong> is global in definition and local in execution: one definition of revenue, executed against the data resident in each market. The <strong>data plane</strong> is regional: raw personal data, training corpora, and anything subject to localisation stay inside the jurisdiction. The <strong>inference layer</strong> is placed by requirement — a model may run in-country for regulated workloads and regionally for others, provided the request and response path never moves regulated data across the boundary.</p>
<p>The discipline that keeps this coherent is a data classification scheme applied at ingestion, not at query time. Every field entering the platform carries a residency tag — public, internal, personal, regulated, in-country-only — and the query planner consults those tags before execution. Systems that attempt to infer residency at query time make mistakes under exactly the conditions that matter: joins that combine two permissible datasets into a result that is not permissible.</p>
<h2 id="what-does-a-localisation-assessment-actually-involve">What Does a Localisation Assessment Actually Involve?</h2>
<p>A localisation assessment answers four questions per market, and the order matters because each answer constrains the next.</p>
<ol>
<li><strong>What data is in scope?</strong> Not "all customer data" but a specific inventory by category: personal information, important data as defined locally, employee data, telemetry, and derived features. Most organisations discover that a small fraction of their estate is actually in scope, and that the estate was over-classified through caution.</li>
<li><strong>Where must it reside?</strong> Some categories require in-country storage; others permit transfer under a standard contract, a security assessment, or a certification. The answer is rarely binary, and the difference between "must stay" and "may leave with conditions" drives the architecture.</li>
<li><strong>What processing is permitted?</strong> Training, inference, analytics, and support access each carry different conditions. A category that may be stored in-country may still not be used to train a model that serves another market.</li>
<li><strong>What is the transfer mechanism and its durability?</strong> Approved mechanisms change. An assessment that records the current mechanism, its review date, and the fallback if it lapses is worth more than one that records only today's answer.</li>
</ol>
<p>The output should be a residency matrix — data category by market, with the required placement and the governing citation — maintained as a living artefact. This matrix is what makes the architecture reviewable, and it is the artefact regulators and enterprise customers increasingly ask to see.</p>
<h2 id="what-should-enterprises-do-this-quarter">What Should Enterprises Do This Quarter?</h2>
<p>Three actions are defensible for any multinational, regardless of how mature its current posture is, because all three reduce cost under every plausible regulatory future.</p>
<p>First, classify data at ingestion with residency tags, even if no localisation requirement applies today. Retro-fitting classification across a mature estate is the single most expensive localisation task, and doing it once, early, converts a future project into a configuration change. Second, separate the control plane from the data plane now. Organisations that have made this split can add a regional deployment in weeks; organisations whose policy, identity, and data layers are entangled face a multi-quarter programme when the next jurisdiction introduces a requirement.</p>
<p>Third, build the evidence habit. Record where regulated data was processed, which model ran, under which mechanism, and who approved it. The enterprises that treat sovereignty as an architecture constraint rather than a legal exception report materially lower compliance cost and faster time-to-market in new jurisdictions — not because they comply less, but because they can demonstrate compliance without assembling it retrospectively.</p>
"""

S12_EN_FAQ = [
    ("What does sovereign AI mean for a global enterprise?",
     "That the single-global-stack assumption no longer holds. Enterprises must decide, market by market, which data stays local, which models can run from regional infrastructure, and which capabilities require in-country deployment. The practical response is a layered architecture: a global control plane and semantic layer, with a regional data plane and inference placed by requirement."),
    ("How many jurisdictions have data-localization requirements?",
     "More than 60 jurisdictions have some form of data-localization measure, and the number grows each year. The requirements differ substantially — some mandate in-country storage, others permit transfer under standard contracts, security assessments, or certifications — which is why a per-market residency matrix is more useful than a global policy."),
    ("Does localisation mean building a separate stack in every country?",
     "No, and doing so is the most expensive response available. Localise the data plane, where regulated data actually lives, and share the control plane — identity, policy, audit, model registry — and the semantic layer globally. Only inference placement needs to vary by market, and only where the workload is regulated."),
    ("How should data residency be enforced technically?",
     "Classify every field at ingestion with a residency tag and have the query planner consult those tags before execution. Inferring residency at query time fails on the cases that matter most: joins that combine two individually permissible datasets into a result that is not permissible to move."),
    ("What is the highest-leverage action for enterprises starting now?",
     "Classify data at ingestion and separate the control plane from the data plane. Both reduce cost under any regulatory future, and both turn a future localisation project into a configuration change rather than a multi-quarter rebuild."),
]

S12_ZH_FAQ = [
    ("主權AI對全球企業意味著什麼？",
     "意味著「單一全球技術棧」的假設已經不成立。企業必須逐市場決定哪些數據留在本地、哪些模型可以從區域基礎設施運行、哪些能力需要在境內部署。務實的回應是分層架構：控制層與語義層全球共享，數據層區域化，推理層則按需求放置。"),
    ("有多少司法管轄區存在數據本地化要求？",
     "已有超過60個司法管轄區實施了某種形式的數據本地化措施，且數量逐年增加。各項要求差異很大——有的強制境內存儲，有的允許在標準合同、安全評估或認證條件下跨境傳輸——因此按市場建立數據駐留矩陣，比制定全球統一政策更有用。"),
    ("本地化是否意味著每個國家都要建一套獨立技術棧？",
     "不是，而且這是成本最高的做法。只需把數據層——即受監管數據實際所在之處——本地化，控制層（身份、策略、審計、模型註冊）與語義層則全球共享。只有推理層的放置需要按市場調整，且僅限於受監管的工作負載。"),
    ("技術上應如何落實數據駐留？",
     "在數據接入時就為每個欄位標記駐留標籤，並讓查詢規劃器在執行前檢查這些標籤。在查詢時才推斷駐留，會在最關鍵的場景失效：把兩個各自合規的數據集連接後，得到的結果可能不允許跨境。"),
    ("對剛開始的企業來說，槓桿最高的行動是什麼？",
     "在數據接入時就完成分類，並把控制層與數據層分離。無論監管如何演變，這兩項都能降低成本，並把未來的本地化專案從長達數季的重建，轉變為一次配置變更。"),
]

S12_CN_H2 = [
    ("全球监管格局概览", "全球数据本地化的监管格局是怎样的？"),
    ("企业AI系统的合规要求", "企业AI系统需要满足哪些合规要求？"),
    ("构建可持续的合规计划", "如何构建可持续的合规计划？"),
    ("合规技术工具与自动化合规方案", "有哪些合规技术工具与自动化方案？"),
    ("企业AI合规体系构建指南", "企业AI合规体系应该如何构建？"),
    ("战略实施路径与关键成功因素", "战略实施路径与关键成功因素是什么？"),
    ("企业实施路线图与成功因素", "企业实施路线图应该如何规划？"),
    ("行业数字化转型深度分析", "行业数字化转型对主权AI提出了什么要求？"),
]
S12_TW_H2 = [
    ("全球監管格局概覽", "全球數據本地化的監管格局是怎樣的？"),
    ("企業AI系統的合規要求", "企業AI系統需要滿足那些合規要求？"),
    ("構建可持續的合規計劃", "如何構建可持續的合規計劃？"),
    ("合規技術工具與自動化合規方案", "有哪些合規技術工具與自動化方案？"),
    ("企業AI合規體系構建指南", "企業AI合規體系應該如何構建？"),
    ("戰略實施路徑與關鍵成功因素", "戰略實施路徑與關鍵成功因素是什麼？"),
    ("企業實施路線圖與成功因素", "企業實施路線圖應該如何規劃？"),
    ("行業數位轉型深度分析", "行業數位轉型對主權AI提出了什麼要求？"),
]

# ---------------------------------------------------------------- slug 13
S13 = "text-to-sql-accuracy-benchmarks-2025"

S13_EN_ADD = """
<h2 id="why-do-benchmark-scores-overstate-production-accuracy">Why Do Benchmark Scores Overstate Production Accuracy?</h2>
<p>The gap between a leaderboard number and what happens in your warehouse is not a measurement error; it is structural. Published benchmarks evaluate a model against a fixed, documented schema with a question set that was written alongside it. Production means a schema nobody documented, column names that encode two meanings, tables that were deprecated but not dropped, and questions phrased in the vocabulary of a specific department.</p>
<p>Three specific factors account for most of the gap. <strong>Schema quality</strong> — benchmarks use clean, normalised schemas with meaningful names; real warehouses have <code>amt_2</code> beside <code>amount_final_v3</code>, and the correct choice is tribal knowledge. <strong>Question ambiguity</strong> — benchmark questions are unambiguous by construction; a real question like "what were sales last quarter?" has three defensible readings depending on whether sales means booked, invoiced, or shipped. <strong>Value grounding</strong> — benchmarks rarely test whether the model knows that "EMEA" in this company excludes Turkey, or that the fiscal year starts in February. The model can generate perfectly valid SQL that encodes the wrong business meaning.</p>
<p>This is why the first recommendation in any serious deployment is to stop quoting the leaderboard and build a golden set instead: 200 to 500 real questions your business actually asks, each with a verified SQL query or result. That set becomes the only accuracy number that matters, and it typically lands 15 to 25 points below the published benchmark on first run — which is useful, because it is the real starting point for improvement.</p>
<h2 id="what-safety-net-does-production-text-to-sql-need">What Safety Net Does Production Text-to-SQL Need?</h2>
<p>Deploying text-to-SQL without guardrails produces a specific and damaging failure: a confident, well-formatted, wrong number that nobody catches. The guardrails are not exotic, and each one addresses a named failure mode.</p>
<ul>
<li><strong>Confidence thresholds with abstention.</strong> The system must be able to say "I am not sure what you mean by X" rather than guessing among three plausible joins. A system that abstains on 10% of questions and is right on the rest is far more useful than one that always answers and is silently wrong on a fifth of them.</li>
<li><strong>Result preview before commitment.</strong> Show the generated SQL or a plain-language restatement of the interpretation before the answer is presented as fact. This catches the largest class of errors — correct SQL for the wrong question — because the user recognises their own intent better than any validator can.</li>
<li><strong>Row and column-level permission enforcement.</strong> Inherited from the existing BI permissions, never reimplemented. The assistant must answer with the same access the user already has, and that rule must hold for queries the model constructs dynamically rather than for a fixed report.</li>
<li><strong>Guardrails on expensive queries.</strong> A generated query can accidentally produce a full-table scan across a billion rows. Cost estimation and row-limit defaults are operational necessities, not optimisations.</li>
<li><strong>Feedback capture.</strong> Every wrong answer the user flags is a training example and a regression test. Teams that wire this loop see accuracy improvements compound; teams that do not plateau at their launch quality.</li>
</ul>
<p>The pattern behind all five is the same: the model is the least reliable part of the system, and the architecture around it is what makes the output safe to act on.</p>
<h2 id="where-is-text-to-sql-headed-next">Where Is Text-to-SQL Headed Next?</h2>
<p>Two developments matter more than incremental benchmark gains. The first is the shift from SQL generation as the goal to governed intent resolution: the semantic layer, not the SQL string, becomes the contract. When a question resolves to a defined metric with a defined calculation, the generated SQL is a detail rather than the risk. This is the change that closes most of the gap between benchmark and production, and it is why the platforms that invest in semantic modelling pull ahead of those that only improve generation.</p>
<p>The second is agentic validation: instead of returning the first plausible query, the system generates candidates, executes them against a sandboxed replica, compares results for consistency, and selects or abstains. Early production deployments of this pattern report meaningful accuracy gains and, more importantly, a large reduction in silent errors — which is the outcome that actually determines whether users keep trusting the system.</p>
"""

S13_EN_FAQ = [
    ("How accurate is text-to-SQL in 2025?",
     "On the BIRD benchmark, the hardest widely used real-world benchmark, the strongest published results sit in the mid-70s percent for execution accuracy, while the cleaner Spider leaderboard is crowded with systems above 90%. The gap between those two numbers is the story: clean schemas are nearly solved, messy real-world business schemas are not."),
    ("Why is production accuracy lower than benchmark accuracy?",
     "Because benchmarks use documented, unambiguous schemas and unambiguous questions. Production means undocumented schemas with ambiguous column names, questions with several defensible readings, and company-specific definitions the model has no way to know. Expect your own golden set to score 15-25 points below published benchmarks on first run."),
    ("What are the main failure modes of text-to-SQL?",
     "Ambiguity is the largest — two tables both containing a 'date' or 'status' column, or a question that maps to several plausible joins. The second is value grounding, where the model generates valid SQL that encodes the wrong business meaning. The third is silent error: a confident, well-formatted, wrong answer that nobody catches."),
    ("What guardrails are needed to deploy text-to-SQL safely?",
     "Confidence thresholds with explicit abstention, a restatement of the interpretation before the answer is presented as fact, permission enforcement inherited from the existing BI layer, cost and row-limit guardrails on generated queries, and a feedback loop that converts every flagged error into a regression test."),
    ("Should accuracy be measured against public benchmarks?",
     "Only as a sanity check. The number that matters comes from a golden set of 200-500 questions your business actually asks, each with verified SQL or results, re-run on every change. That set is both your accuracy metric and your regression suite."),
]

S13_ZH_FAQ = [
    ("2025年text-to-SQL的準確率如何？",
     "在最困難的廣泛使用基準BIRD上，已發布的最佳結果執行準確率約在70%中段；而較乾淨的Spider榜單上，超過90%的系統比比皆是。這兩個數字之間的差距就是全貌：乾淨的schema幾乎已解決，混亂的真實業務schema則還沒有。"),
    ("為什麼生產環境的準確率低於基準測試？",
     "因為基準測試使用的是有文件、無歧義的schema與無歧義的問題。生產環境則是沒有文件的schema、含義不明的欄位名稱、有多種合理解讀的問題，以及模型無從得知的企業特定定義。首次執行時，你自己的黃金測試集通常比公開基準低15到25個百分點。"),
    ("text-to-SQL的主要失敗模式是什麼？",
     "最大的是歧義——兩個資料表都有「日期」或「狀態」欄位，或一個問題對應到多種看似合理的連接方式。其次是取值對齊：模型產生了有效的SQL，但編碼了錯誤的業務含義。第三是靜默錯誤：一個自信、格式正確但錯誤的答案，且沒有人發現。"),
    ("部署text-to-SQL需要哪些防護措施？",
     "帶明確「拒答」機制的置信度門檻；在把答案作為事實呈現之前，先重述系統的解讀；沿用既有BI層的權限控制；對生成的查詢加上成本與列數限制；以及把每個被標記的錯誤轉為回歸測試的回饋迴路。"),
    ("準確率應該用公開基準來衡量嗎？",
     "只能作為健全性檢查。真正重要的數字來自一份包含200到500個企業實際會問的問題、且每個都有已驗證SQL或結果的黃金測試集，並在每次變更時重跑。這份測試集既是準確率指標，也是回歸測試套件。"),
]

S13_CN_H2 = [
    ("自然语言分析的发展格局", "自然语言分析的发展格局是怎样的？"),
    ("技术架构与性能", "text-to-SQL的技术架构与性能如何？"),
    ("用户体验与采用模式", "用户体验与采用模式有哪些特点？"),
    ("企业整合考量", "企业整合需要考量哪些因素？"),
    ("战略建议", "有哪些战略层面的建议？"),
]
S13_TW_H2 = [
    ("自然語言分析的發展格局", "自然語言分析的發展格局是怎樣的？"),
    ("技術架構與效能", "text-to-SQL的技術架構與效能如何？"),
    ("使用者體驗與採用模式", "使用者體驗與採用模式有哪些特點？"),
    ("企業整合考量", "企業整合需要考量那些因素？"),
    ("戰略建議", "有哪些戰略層面的建議？"),
]

# ---------------------------------------------------------------- slug 14
S14 = "pipl-compliance-for-ai-systems-a-practical-guide"

S14_EN_ADD = """
<h2 id="how-do-you-map-personal-information-through-an-ai-system">How Do You Map Personal Information Through an AI System?</h2>
<p>PIPL compliance for AI is impossible without a map of where personal information actually goes, and most organisations discover that their AI systems touch more personal data through more paths than anyone had documented. The exercise is a data-flow inventory, and it needs to cover five stages rather than the two that usually get attention.</p>
<p><strong>Ingestion</strong> — every source that carries personal information into the platform: CRM, HR systems, support tickets, chat logs, web analytics, third-party data. <strong>Training and fine-tuning</strong> — which datasets were used, whether personal information was present, and whether it was anonymised or de-identified before use, because de-identified data is treated differently from anonymised data under PIPL. <strong>Retrieval and grounding</strong> — the documents a RAG system pulls into context at query time, which is the path most often missed entirely; a model trained only on public data can still surface personal information at inference through retrieval. <strong>Inference and output</strong> — what the model returns, to whom, and whether the output itself constitutes personal information. <strong>Logging and evaluation</strong> — prompts, responses, and human review queues, which routinely retain personal information long after the business purpose has ended.</p>
<p>The output is a processing-activity record per system, and it is the artefact PIPL expects: the categories of personal information, the purpose, the legal basis, the retention period, the recipients, the cross-border transfers, and the security measures. Building this record per system is most of the compliance work, and it is also what makes every other obligation — consent, localisation, automated decision-making rules, audit trails — answerable.</p>
<h2 id="what-does-lawful-basis-and-consent-look-like-for-ai">What Does Lawful Basis and Consent Look Like for AI?</h2>
<p>PIPL permits processing on several bases, and consent is only one of them. For AI systems, the practical question is which basis applies to each processing activity, because getting this wrong is what turns a lawful system into an unlawful one.</p>
<p>Contract performance and human-resource management cover a large share of enterprise AI use — processing employee data to run internal systems, or customer data to deliver a service the customer bought. Where the AI use goes beyond what the individual would reasonably expect from that relationship, separate consent is required, and it must be specific: consent to "improve our services" does not cover training a model on a customer's support conversations. For sensitive personal information — biometrics, health, financial accounts, location tracking, and the personal information of minors — the requirements tighten further, requiring specific purpose and necessity plus separate consent in most cases.</p>
<p>Two design consequences follow. First, consent capture has to be granular and versioned: record what was consented to, when, in what wording, and which processing activities it authorised. Second, withdrawal has to be operationally real. When an individual withdraws consent, the system must be able to stop using their data for the affected purpose, which in an AI context may mean excluding them from future training runs and, in some interpretations, addressing data already incorporated into a model. Architectures that separate the training corpus from the served model — so that a retrained model can be produced without the withdrawn individual's data — are materially easier to operate than those that cannot.</p>
<h2 id="how-should-a-pipl-programme-be-sequenced">How Should a PIPL Programme Be Sequenced?</h2>
<p>Sequencing matters because the obligations interact: localisation decisions constrain architecture, and architecture decisions determine what consent is needed. A workable order:</p>
<ol>
<li><strong>Weeks 1-4 — scope and inventory.</strong> Determine whether PIPL applies, then build the data-flow inventory and processing-activity records for the AI systems in scope. Nothing else can be answered properly until this exists.</li>
<li><strong>Weeks 5-8 — classify and place.</strong> Classify every data category, decide what must remain in China, and settle the transfer mechanism for anything that crosses the border. This is the point at which architecture changes are cheapest.</li>
<li><strong>Weeks 9-12 — consent, explanation and audit.</strong> Align consent capture with the actual processing activities, build the explanation capability for automated decisions, and stand up the audit trail: what data, what purpose, which model, what decision, who is accountable.</li>
<li><strong>Ongoing — monitoring and reassessment.</strong> Personal information protection impact assessments for high-risk processing, periodic review of transfer mechanisms, and a reassessment whenever a system's purpose or data sources change materially.</li>
</ol>
<p>The organisations that handle this best treat these as architecture requirements rather than legal review gates. Localisation, purpose-limited access, explainability, and auditability are the features that let an AI platform operate in China at all — and they build the trust that drives adoption with both customers and regulators.</p>
"""

S14_EN_FAQ = [
    ("Does PIPL apply to a foreign company's AI system?",
     "Yes, if it processes the personal information of individuals in China — customers, employees, or website visitors — regardless of where the company is established. There is no small-processor exemption. The practical test is whether the system touches personal information of people in China, not where the servers sit."),
    ("What are the penalties for PIPL non-compliance?",
     "For serious violations, fines up to 50 million yuan or 5% of the previous year's annual revenue, along with suspension of business, revocation of licences, and potential personal liability for responsible individuals. Less serious violations carry corrective orders and fines up to one million yuan."),
    ("Must training data stay in China?",
     "Personal information of Chinese residents must be stored on servers in China, which extends to training data, model inputs, and outputs containing personal information. Cross-border transfer is possible but requires a mechanism — a security assessment, standard contract, or certification — and the applicable mechanism depends on the data category and volume."),
    ("What does PIPL require for automated decision-making?",
     "That the individual is informed an automated decision is being made, can request an explanation of the decision logic in understandable terms, and can refuse decisions made solely by automated means in certain contexts. Transparency and fairness are also required, which means documenting the logic and testing for discriminatory outcomes."),
    ("What audit records does PIPL expect for AI systems?",
     "Records of processing activities: what personal information was used, for what purpose, under which legal basis, which model processed it, what decision resulted, who is accountable, how long it is retained, and whether it crossed a border. These records must be maintained and available to demonstrate compliance."),
]

S14_ZH_ADD = """
<h2 id="AI系統中的個人信息應該如何盤點">AI系統中的個人信息應該如何盤點？</h2>
<p>要讓AI系統符合PIPL，必須先掌握個人信息實際流向何處；多數企業會發現，其AI系統接觸到的個人信息量與路徑，都遠超過既有的文件記錄。這項工作是數據流程盤點，而且必須涵蓋五個階段，而不只是通常被關注的兩個。</p>
<p><strong>接入</strong>——所有把個人信息帶入平台的來源：CRM、人力資源系統、客服工單、聊天記錄、網站分析、第三方數據。<strong>訓練與微調</strong>——使用了哪些數據集、其中是否包含個人信息、以及在使用前是否做了匿名化或去標識化處理，因為PIPL對去標識化數據與匿名化數據的處理方式不同。<strong>檢索與紮根</strong>——RAG系統在查詢時把哪些文件拉進上下文，這是最常被完全忽略的路徑：一個只用公開數據訓練的模型，仍可能透過檢索在推理時帶出個人信息。<strong>推理與輸出</strong>——模型回傳了什麼、給了誰，以及輸出本身是否構成個人信息。<strong>日誌與評估</strong>——提示詞、回應與人工複核佇列，這些往往在業務目的結束後仍長期保留個人信息。</p>
<p>產出是每個系統的處理活動記錄，而這正是PIPL所要求的產物：個人信息的類別、處理目的、法律依據、保存期限、接收方、跨境傳輸情況，以及安全措施。逐系統建立這份記錄，是合規工作的主要內容，也是讓其他所有義務——同意、本地化、自動化決策規則、審計追蹤——都能被回答的前提。</p>
<h2 id="AI場景下的合法性基礎與同意應該如何設計">AI場景下的合法性基礎與同意應該如何設計？</h2>
<p>PIPL允許多種處理依據，同意只是其中之一。對AI系統而言，實務問題是每項處理活動適用哪一種依據，因為判斷錯誤會把合法的系統變成不合法的系統。</p>
<p>合同履行與人力資源管理涵蓋了企業AI應用的很大一部分：為運行內部系統而處理員工數據，或為交付客戶已購買的服務而處理客戶數據。當AI的使用超出個人在該關係中合理預期的範圍時，就需要單獨同意，而且必須是具體的——同意「改善我們的服務」並不涵蓋用客戶的客服對話來訓練模型。對於敏感個人信息——生物識別、健康、金融帳戶、行蹤軌跡，以及未成年人的個人信息——要求進一步提高，在大多數情況下需要特定目的與必要性，並取得單獨同意。</p>
<p>這帶來兩項設計上的結果。第一，同意的取得必須是細粒度且帶版本記錄的：記錄同意的內容、時間、用語，以及它授權了哪些處理活動。第二，撤回必須在營運上真正可行。當個人撤回同意時，系統必須能停止將其數據用於受影響的目的；在AI情境下，這可能意味著將其排除於未來的訓練之外，在某些解讀下還需處理已納入模型的數據。把訓練語料與提供服務的模型分開的架構——使得在移除該個人的數據後能重新產出模型——在營運上明顯比做不到的架構更容易。</p>
<h2 id="PIPL合規工作應該如何排序">PIPL合規工作應該如何排序？</h2>
<p>排序很重要，因為各項義務彼此牽動：本地化決策限制架構選擇，而架構決策又決定了需要取得哪種同意。可行的順序如下：</p>
<ol>
<li><strong>第1至4週——範圍與盤點。</strong>判斷PIPL是否適用，然後為範圍內的AI系統建立數據流程盤點與處理活動記錄。在這些完成之前，其他問題都無法被正確回答。</li>
<li><strong>第5至8週——分類與放置。</strong>為每個數據類別分類，決定哪些必須留在中國境內，並為跨境的數據確定傳輸機制。這是架構變更成本最低的時點。</li>
<li><strong>第9至12週——同意、解釋與審計。</strong>讓同意的取得與實際處理活動對齊，建立自動化決策的解釋能力，並建置審計追蹤：用了什麼數據、出於什麼目的、由哪個模型處理、做出什麼決定、誰負責。</li>
<li><strong>持續——監控與重新評估。</strong>對高風險處理活動進行個人信息保護影響評估，定期檢視傳輸機制，並在系統目的或數據來源發生重大變化時重新評估。</li>
</ol>
<p>處理得最好的企業，是把這些當成架構需求，而不是法務審查的關卡。本地化、按目的限制的訪問、可解釋性與可審計性，正是讓AI平台能在中國市場運作的特性，同時也建立客戶與監管機構的信任。</p>
"""

S14_ZH_FAQ = [
    ("PIPL是否適用於外國公司的AI系統？",
     "適用，只要該系統處理中國境內個人的個人信息——客戶、員工或網站訪客——無論公司註冊地在何處。PIPL沒有小型處理者豁免。實務判斷標準是系統是否接觸中國境內個人的個人信息，而不是伺服器位於何處。"),
    ("違反PIPL的處罰是什麼？",
     "情節嚴重的，可處最高5,000萬元人民幣或上一年度營業額5%的罰款，並可責令暫停業務、吊銷許可證，以及對責任人員追究個人責任。情節較輕的，則為責令改正並處最高100萬元罰款。"),
    ("訓練數據必須留在中國境內嗎？",
     "中國境內居民的個人信息必須存儲在中國境內的伺服器上，這延伸到訓練數據、模型輸入與含有個人信息的輸出。跨境傳輸是可能的，但需要具備相應機制——安全評估、標準合同或認證——適用哪種機制取決於數據類別與數量。"),
    ("PIPL對自動化決策有什麼要求？",
     "要求告知個人正在進行自動化決策、可要求以可理解的方式獲得決策邏輯的解釋，並在特定情境下拒絕僅由自動化方式做出的決定。同時要求透明度與公平性，這表示必須記錄決策邏輯並檢測是否存在歧視性結果。"),
    ("PIPL對AI系統的審計記錄有什麼要求？",
     "要求保存處理活動記錄：使用了哪些個人信息、出於什麼目的、依據何種法律基礎、由哪個模型處理、做出了什麼決定、誰負責、保存多久，以及是否跨境。這些記錄必須持續保存，並可用於證明合規。"),
]

S14_CN_H2 = [
    ("AI 系统的 PIPL 要求", "PIPL对AI系统提出了哪些要求？"),
    ("数据本地化实践", "数据本地化在实践中如何落地？"),
    ("自动决策合规性", "自动化决策需要满足哪些合规要求？"),
    ("审计追踪和责任", "企业应如何建立审计追踪与问责机制？"),
    ("要点", "本文的核心要点是什么？"),
    ("结论", "合规工作应该从哪里开始？"),
]
S14_TW_H2 = [
    ("合規工作應該從哪裡開始？", "合規工作應該從哪裡開始？"),
    ("本文要點是什麼？", "本文的核心要點是什麼？"),
]

# ---------------------------------------------------------------- slug 15
S15 = "mcp-connector-ecosystem-expansion-q4-2025"

S15_EN_ADD = """
<h2 id="what-changes-now-that-mcp-is-neutral-infrastructure">What Changes Now That MCP Is Neutral Infrastructure?</h2>
<p>The move of MCP under the Linux Foundation's Agentic AI Foundation in December 2025 changed the risk calculus for enterprise adopters more than any feature release. While the protocol was associated primarily with one vendor, adopting it meant accepting a degree of platform dependency. Under neutral governance, with OpenAI, Google and Microsoft all supporting it and thousands of tool builders shipping servers, the protocol becomes infrastructure in the same category as HTTP or SQL: something you build on rather than something you bet on.</p>
<p>Three practical consequences follow. First, procurement risk falls — enterprises can require MCP support in vendor evaluations without implicitly choosing a platform. Second, internal build decisions get easier: an MCP server written for one assistant works with any compliant client, so integration work stops being stranded when a model or assistant changes. Third, the security conversation changes shape. A neutral protocol attracts scrutiny, and the enterprise question shifts from "whose protocol is this?" to the harder and more useful question of how tool access is authorised, scoped, and audited.</p>
<p>That last point deserves emphasis, because it is where most MCP deployments are weakest. A protocol that makes it easy to connect an agent to everything also makes it easy to connect an agent to too much. The governance requirement is a tool registry with explicit scoping: every server declares which resources and tools it exposes, every client declares which it may call, and the intersection is what the agent can actually reach — with every call logged.</p>
<h2 id="how-do-you-evaluate-a-connector-before-trusting-it">How Do You Evaluate a Connector Before Trusting It?</h2>
<p>Breadth of the catalogue is the least useful criterion. What matters is whether a specific connector behaves safely and predictably under the conditions your agents will actually create. Six checks separate production-grade connectors from demos.</p>
<ul>
<li><strong>Authentication and scoping.</strong> Does it use OAuth or short-lived credentials rather than a shared service account, and can permissions be scoped per agent rather than per installation?</li>
<li><strong>Read/write boundaries.</strong> Are write tools clearly separated from read tools, so a read-only agent can be configured to be structurally incapable of writing?</li>
<li><strong>Pagination and limits.</strong> Does it handle large result sets properly, and does it enforce sensible limits rather than pulling an entire table into a prompt?</li>
<li><strong>Error semantics.</strong> Does it return structured, actionable errors — permission denied, rate limited, resource not found — rather than a generic failure the model will hallucinate around?</li>
<li><strong>Idempotency on writes.</strong> For any tool that creates or mutates, does it accept an idempotency key? This is the single most important property for tools that will be called by a retrying agent.</li>
<li><strong>Observability.</strong> Does it emit traces with the request, the tool, the arguments, and the outcome, so that a bad agent action can be reconstructed after the fact?</li>
</ul>
<p>A connector that fails any of the first two should not be deployed in an enterprise context regardless of how useful it looks. A connector that fails the last three will work in testing and produce incidents in production.</p>
<h2 id="what-does-a-first-mcp-deployment-look-like">What Does a First MCP Deployment Look Like?</h2>
<p>The deployments that reach production share a shape: narrow scope, read-only first, one measurable workflow. The pattern that works:</p>
<ol>
<li><strong>Pick the workflow by question volume, not by ambition.</strong> Find the five to ten questions your teams ask most often across the systems they ask them about. That set defines the first servers to build — usually the data platform plus two or three operational systems.</li>
<li><strong>Deploy read-only and measure.</strong> Stand up the servers with read tools only, wire them to one assistant, and run for four to six weeks. Track the share of questions answered without human escalation and the accuracy against a golden set. This phase proves value without creating risk.</li>
<li><strong>Add write tools behind approval.</strong> Introduce the first mutating tool — creating a ticket, updating a record — with human approval on every call, an idempotency key, and full tracing. Approve based on the error rate observed in the read-only phase.</li>
<li><strong>Scale by server, not by agent.</strong> Extend coverage by adding servers and tools to the same governed registry rather than by giving more agents unrestricted access. Centralising the registry is what keeps the audit surface tractable as the estate grows.</li>
</ol>
<p>The measurable outcome to hold the programme to is not the number of connectors deployed. It is the reduction in integration maintenance effort and the share of questions answered end-to-end without a human in the loop. Those two numbers determine whether the connector investment compounds, and they are visible within the first quarter.</p>
"""

S15_EN_FAQ = [
    ("Why has MCP become the standard interface between agents and data?",
     "Because it solves the last-mile problem every enterprise AI project hits: getting a model to safely read from and act on the systems where the business actually runs. Before MCP, every agent needed bespoke integrations for every system, and every integration broke when an API changed. A single protocol turns an N-times-M integration problem into an N-plus-M one."),
    ("What changed in the connector ecosystem in Q4 2025?",
     "The ecosystem stopped being a promise and became a catalogue. Enterprise connectors now span data platforms, operational systems, productivity and collaboration tools, and developer infrastructure — and in December 2025 the protocol moved under the Linux Foundation's Agentic AI Foundation, signalling neutral governance rather than single-vendor control."),
    ("Is it safe to give an agent access to production systems through MCP?",
     "Yes, with the right controls: a tool registry with explicit scoping, per-agent permission grants, read/write separation, idempotency keys on mutating tools, and tracing of every call. The protocol makes broad connection easy, which makes deliberate scoping the most important design decision in a deployment."),
    ("How should an enterprise start with MCP?",
     "Pick the workflow by question volume rather than ambition, deploy read-only against the data platform plus two or three operational systems, measure for four to six weeks, then add write tools behind human approval. Scale by adding servers to a governed registry rather than by broadening agent permissions."),
    ("How do you measure whether an MCP investment is paying off?",
     "Track the reduction in integration maintenance effort — fewer bespoke connectors, fewer breakages when APIs change — and the share of questions answered end-to-end without human escalation. Connector count is not the metric; coverage of real questions is."),
]

S15_ZH_FAQ = [
    ("MCP為什麼會成為代理與數據之間的標準介面？",
     "因為它解決了每個企業AI專案都會遇到的「最後一哩」問題：讓模型安全地讀取並操作業務實際運行的系統。在MCP之前，每個代理都需要為每個系統做客製化整合，而且每次API變更都會造成整合失效。單一協定把N乘以M的整合成為N加M的問題。"),
    ("2025年第四季度的連接器生態發生了什麼變化？",
     "生態系統從承諾變成了目錄。企業級連接器已涵蓋數據平台、營運系統、生產力與協作工具，以及開發基礎設施；而在2025年12月，該協定被納入Linux基金會旗下的Agentic AI Foundation，象徵著中立治理而非單一供應商控制。"),
    ("讓代理透過MCP存取生產系統是否安全？",
     "在具備適當控制的前提下是安全的：帶明確範圍的工具註冊表、按代理授予的權限、讀寫分離、變更類工具的冪等鍵，以及對每次呼叫的追蹤。協定讓廣泛連接變得容易，因此「刻意的範圍控制」成為部署中最重要的設計決策。"),
    ("企業應該如何開始導入MCP？",
     "依提問量而非野心來選擇工作流；先以唯讀方式對接數據平台與兩三個營運系統；衡量四到六週；然後在人工批准下加入寫入工具。擴展時應在受治理的註冊表中增加伺服器，而不是放寬代理的權限。"),
    ("如何衡量MCP的投資是否值得？",
     "追蹤整合維護工作的減少——更少的客製化連接器、API變更時更少的故障——以及無需人工介入即可端到端回答的問題佔比。連接器數量不是指標；對真實問題的覆蓋率才是。"),
]

S15_CN_H2 = [
    ("核心收益与投资回报考量", "MCP的核心收益与投资回报如何评估？"),
    ("实施路线图与后续步骤", "企业应该如何规划MCP的实施路线图？"),
    ("案例分析与行业洞察", "有哪些值得参考的行业案例与洞察？"),
    ("未来展望与行动建议", "MCP的未来展望与行动建议是什么？"),
    ("关键成功因素与常见陷阱", "MCP落地的关键成功因素与常见陷阱是什么？"),
    ("蜂启咨询的专业洞察", "蜂启咨询对MCP有哪些专业洞察？"),
]
S15_TW_H2 = [
    ("核心收益與投資回報考量", "MCP的核心收益與投資回報如何評估？"),
    ("實施路線圖與後續步驟", "企業應該如何規劃MCP的實施路線圖？"),
    ("案例分析與行業洞察", "有哪些值得參考的行業案例與洞察？"),
    ("未來展望與行動建議", "MCP的未來展望與行動建議是什麼？"),
    ("關鍵成功因素與常見陷阱", "MCP落地的關鍵成功因素與常見陷阱是什麼？"),
    ("蜂啟諮詢的專業洞察", "蜂啟諮詢對MCP有哪些專業洞察？"),
]

DATA = {
    S11: {
        "EN": {"h2": [
            ("The Scale of Dashboard Sprawl", "How Large Is the Dashboard Sprawl Problem?"),
            ("Building the Business Case for Retiring Dashboards", "How Do You Build the Business Case for Retiring Dashboards?"),
        ], "add": S11_EN_ADD, "faq": S11_EN_FAQ},
        "ZH_FAQ_TRAD": S11_ZH_FAQ,
        "ZH_CN_H2": S11_CN_H2, "ZH_TW_H2": S11_TW_H2,
    },
    S12: {
        "EN": {"h2": [
            ("Global Regulatory Landscape Overview", "What Does the Global Data-Localization Landscape Look Like?"),
            ("Compliance Requirements for Enterprise AI", "Which Compliance Requirements Apply to Enterprise AI?"),
            ("Building a Sustainable Compliance Program", "How Do You Build a Sustainable Compliance Programme?"),
            ("Enterprise AI Compliance System Construction Guide", "How Should an Enterprise AI Compliance System Be Built?"),
            ("A Framework for Sovereignty-Aware AI Architecture", "What Does a Sovereignty-Aware AI Architecture Look Like?"),
        ], "add": S12_EN_ADD, "faq": S12_EN_FAQ},
        "ZH_FAQ_TRAD": S12_ZH_FAQ,
        "ZH_CN_H2": S12_CN_H2, "ZH_TW_H2": S12_TW_H2,
    },
    S13: {
        "EN": {"h2": [
            ("The Evolving Landscape of Natural Language Analytics", "How Has Natural Language Analytics Evolved?"),
            ("Technical Architecture and Performance", "What Architecture Delivers Accurate Text-to-SQL?"),
            ("User Experience and Adoption Patterns", "Which Adoption Patterns Actually Work?"),
            ("Enterprise Integration Considerations", "What Does Enterprise Integration Require?"),
            ("Strategic Recommendations", "What Should Enterprises Do Next With Text-to-SQL?"),
        ], "add": S13_EN_ADD, "faq": S13_EN_FAQ},
        "ZH_FAQ_TRAD": S13_ZH_FAQ,
        "ZH_CN_H2": S13_CN_H2, "ZH_TW_H2": S13_TW_H2,
    },
    S14: {
        "EN": {"h2": [
            ("PIPL Requirements for AI Systems", "What Are PIPL's Requirements for AI Systems?"),
            ("Data Localisation in Practice", "How Does Data Localisation Work in Practice?"),
            ("Automated Decision-Making Compliance", "What Does Automated Decision-Making Compliance Require?"),
            ("Audit Trails and Accountability", "What Audit Trails Does PIPL Expect?"),
            ("Key Takeaways", "What Are the Key Takeaways?"),
            ("Conclusion", "Where Should Compliance Work Start?"),
        ], "add": S14_EN_ADD, "faq": S14_EN_FAQ},
        "ZH_ADD_TRAD": S14_ZH_ADD,
        "ZH_FAQ_TRAD": S14_ZH_FAQ,
        "ZH_CN_H2": S14_CN_H2, "ZH_TW_H2": S14_TW_H2,
    },
    S15: {
        "EN": {"h2": [
            ("The Connector Ecosystem in Q4 2025: Scale and Breadth", "How Broad Is the MCP Connector Ecosystem in Q4 2025?"),
            ("Key Benefits and ROI Considerations", "What Are the Key Benefits and ROI Considerations?"),
            ("Implementation Roadmap and Next Steps", "What Does an MCP Implementation Roadmap Look Like?"),
        ], "add": S15_EN_ADD, "faq": S15_EN_FAQ},
        "ZH_FAQ_TRAD": S15_ZH_FAQ,
        "ZH_CN_H2": S15_CN_H2, "ZH_TW_H2": S15_TW_H2,
    },
}
