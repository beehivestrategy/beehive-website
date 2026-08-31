import os, re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def sec(h2, body):
    return f'\n<h2>{h2}</h2>\n<p>{body}</p>\n'

# (slug, lang) -> list of (h2, body)
ADD = {
 # ---------------- EN under threshold ----------------
 ("education-personalised-learning-pathways-through-data-a-2026-update","en"): [
   ("How Do You Measure Whether Personalisation Is Actually Helping Students?",
    "Personalisation should be judged by learning outcomes, not by the sophistication of the model. Track a small set of leading indicators&mdash;improvement in mastery assessments, reduction in disengagement signals, and faster recovery after a missed concept&mdash;alongside qualitative teacher feedback. Avoid over-indexing on engagement time alone, which can reward addictive design rather than learning. The strongest programmes run controlled comparisons across cohorts, so leaders can see whether personalised pathways move the metrics that matter before scaling further."),
 ],
 ("ai-supply-chain-resilience-scenario-planning","en"): [
   ("How Do You Scale Scenario Planning Across the Enterprise?",
    "Scaling works best when scenario models become a shared service rather than a bespoke analysis owned by one team. Publish a catalogue of reusable scenarios, standardise the input signals, and let business units subscribe to the views they need. This turns occasional war-gaming into a continuous operational habit that survives personnel changes and keeps resilience thinking close to daily decisions."),
 ],
 ("data-mesh-vs-data-warehouse-choosing-the-right-architecture","en"): [
   ("How Do You Avoid the Most Common Data Mesh Failure Modes?",
    "The dominant failure is treating data mesh as a pure technology rollout while ignoring the organisational shift. When domains lack incentive or capacity to own data products, quality degrades and the platform becomes a bottleneck. Mitigate this by funding domain teams explicitly for data product ownership, measuring them on consumption and trust, and giving the platform group a mandate to provide self-serve capabilities instead of delivering every request by hand."),
 ],
 ("natural-language-query-accuracy","en"): [
   ("How Do You Make Accuracy Improvements Visible to the Whole Team?",
    "Accuracy is a team sport, so make the metric visible. Publish a weekly accuracy dashboard, share representative failures in a shared channel, and celebrate fixes that move the number. When progress is transparent, engineers, linguists, and analysts align around the same target instead of debating anecdotes, and continuous improvement becomes part of the culture rather than a one-off project."),
 ],
 # ---------------- zh-CN under threshold ----------------
 ("ai-regulatory-sandbox-participation","zh-CN"): [
   ("参与沙盒后，团队应如何管理模型变更？",
    "进入监管沙盒不等于合规工作的结束，反而对模型变更管理提出了更高要求。监管方通常要求对模型上线后的每一次显著改动都保留审计轨迹，包括训练数据来源、特征定义、阈值调整与回滚方案。团队应建立与金融级系统相当的变更控制流程：任何影响决策逻辑的发布都需经过独立的模型验证与业务审批。同时要把沙盒期间收集的真实反馈沉淀为回归测试集，确保迭代不会悄悄退化公平性指标。最成熟的参与方会把沙盒当作持续验证的跑道，而不是一次性审批，从而在正式监管框架下更快、更稳地扩展应用场景。"),
 ],
 ("retail-fraud-detection-ai","zh-CN"): [
   ("零售业如何用合成数据弥补样本不足？",
    "零售欺诈样本天然稀少且高度不平衡，真实标注的欺诈案例往往只占交易的极小比例，直接训练容易导致模型对罕见攻击视而不见。成熟的团队会引入合成数据与受控对抗样本，模拟新型盗刷、账户接管与退货欺诈的路径，从而扩充少数类的覆盖。合成数据还能在保护顾客隐私的前提下，让模型学习到敏感行为模式而不接触真实个人资料。关键在于把合成样本与真实反馈闭环结合：当线上出现新类型欺诈，立即抽取特征、人工标注并回流训练集。配合定期的重平衡与漂移检测，零售欺诈模型才能在样本不足的前提下，依然保持对新兴攻击的敏感度与召回率。"),
 ],
 ("mcp-vs-rest-api-vs-graphql-complete-comparison","zh-CN"): [
   ("MCP 如何影响前端与后端的协作方式？",
    "传统集成里，前端每接入一个新能力都要后端写一套专用接口，需求排队、发布缓慢。MCP 把工具、资源与提示抽象成统一协议，前端只需声明「我需要查询订单」这类意图，由 MCP 服务器负责把意图映射到具体系统与凭证。这让前端团队可以更快地组合能力，而后端只需维护好各自领域的 MCP 服务器。协作边界从「逐接口对接」变成「逐能力注册」，显著降低了跨团队沟通成本，也减少了因接口契约频繁变更引发的回归问题。"),
   ("在遗留系统上落地 MCP 有哪些务实路径？",
    "多数企业并不会推倒重来，而是把 MCP 作为遗留系统的现代化适配层。常见做法是先为非核心但调用频繁的能力（如配置读取、日志查询、元数据检索）封装 MCP 服务器，验证协议与治理模型，再逐步把关键业务系统接入。对于没有原生 API 的旧系统，可以用一对脚本化的连接器包装现有命令行或数据库访问，在不改动原系统的前提下暴露为 MCP 工具。这种渐进策略能把风险控制在可回滚的范围内，让组织在获得 AI 原生集成红利的同时，不必承担一次性大重构的成本与不确定性。"),
 ],
 ("data-mesh-vs-data-warehouse-choosing-the-right-architecture","zh-CN"): [
   ("数据网格如何与数据治理框架共存？",
    "数据网格常被误读为「放弃集中治理」，事实恰恰相反：它把治理从中心化的管控，转变为可组合的策略与标准。全局治理团队负责定义身份、安全、分类与互操作标准，而各领域团队在本地执行这些标准并对外提供可发现、可信任的数据产品。这种「联邦式治理」让合规要求以代码与契约的形式内嵌在数据产品中，而不是靠人工审批层层把关。结果是在保持规模灵活性的同时，依然满足审计、隐私与可追溯的硬性要求。"),
   ("怎样判断你的组织已经准备好数据网格？",
    "数据网格不是技术选型，而是组织成熟度的体现。在启动之前，先确认三件事：第一，业务域边界是否清晰，能否明确每个数据产品的归属团队；第二，平台团队是否具备为领域提供自助能力（而非接手开发）的意愿与预算；第三，是否存在足够的激励机制，让领域团队愿意长期维护数据质量。如果这三点的答案都是肯定的，数据网格能显著加速价值交付；如果仍依赖中心团队逐需求交付，那么先在平台与契约上补课，会比仓促推行网格带来更稳妥的回报。"),
 ],
 ("education-personalised-learning-pathways-through-data-a-2026-update","zh-CN"): [
   ("个性化学习如何与现有教学管理系统集成？",
    "个性化学习路径要真正落地，必须接入学校已有的学生信息系统（SIS）、学习管理系统（LMS）与教务排课系统。许多项目失败，是因为把数据平台当作独立孤岛来建设。正确的做法是把数据产品作为共享能力，通过标准接口把成绩、出勤、作业完成度与课堂行为信号汇聚到统一的学科域中。教师在原有 LMS 界面里就能看到推荐路径，而不是被迫切换到一个新系统。集成时优先采用事件驱动的同步方式，保证学生进度变化能在数分钟内反映到路径引擎。同时要保留教师在回路中的最终决策权：系统给出建议，教师确认或调整。这种「人在回路」的设计既保证了规模化的个性体验，又不削弱教育的专业判断，也更容易通过学校的治理与隐私审查。"),
   ("如何向家长与学生沟通个性化学习的价值？",
    "个性化学习常常被误解为「用算法取代老师」。有效的沟通应当把重点放在学生的成长与自主权上，而不是技术本身。学校可以通过季度学习报告，用可视化方式展示每位学生在阅读、数学与探究能力上的进步曲线，并说明路径调整背后的原因。家长最关心的是孩子是否在被公平对待，因此要公开路径推荐的维度与边界，明确哪些因素会影响建议、哪些不会。学生层面，则应让他们看到自己可以主动选择挑战难度与目标，从而建立学习的 ownership。当个性化成为可见、可解释、可参与的过程，抵触情绪会显著降低，项目也更容易获得持续的资金与政策支持。"),
 ],
 # ---------------- zh-TW under threshold ----------------
 ("ai-regulatory-sandbox-participation","zh-TW"): [
   ("參與沙盒後，團隊應如何管理模型變更？",
    "進入監管沙盒不等於合規工作的結束，反而對模型變更管理提出了更高要求。監管方通常要求對模型上線後的每一次顯著改動都保留審計軌跡，包括訓練資料來源、特徵定義、閾值調整與回滾方案。團隊應建立與金融級系統相當的變更控制流程：任何影響決策邏輯的發布都需經過獨立的模型驗證與業務審批。同時要把沙盒期間收集的真實回饋沉澱為回歸測試集，確保迭代不會悄悄退化公平性指標。最成熟的參與方會把沙盒當成持續驗證的跑道，而不是一次性審批，從而在正式監管框架下更快、更穩地擴展應用場景。"),
 ],
 ("retail-fraud-detection-ai","zh-TW"): [
   ("零售業如何用合成資料彌補樣本不足？",
    "零售詐欺樣本天然稀少且高度不平衡，真實標註的詐欺案例往往只占交易的極小比例，直接訓練容易導致模型對罕見攻擊視而不見。成熟的團隊會引入合成資料與受控對抗樣本，模擬新型盜刷、帳戶接管與退貨詐欺的路徑，從而擴充少數類的覆蓋。合成資料還能在保護顧客隱私的前提下，讓模型學習到敏感行為模式而不接觸真實個人資料。關鍵在於把合成樣本與真實回饋閉環結合：當線上出現新類型詐欺，立即抽取特徵、人工標註並回流訓練集。配合定期的重平衡與漂移檢測，零售詐欺模型才能在樣本不足的前提下，依然保持對新興攻擊的敏感度與召回率。"),
 ],
 ("mcp-vs-rest-api-vs-graphql-complete-comparison","zh-TW"): [
   ("MCP 如何影響前端與後端的協作方式？",
    "傳統整合裡，前端每接入一個新能力都要後端寫一套專用介面，需求排隊、發布緩慢。MCP 把工具、資源與提示抽象成統一協議，前端只需宣告「我需要查詢訂單」這類意圖，由 MCP 伺服器負責把意圖映射到具體系統與憑證。這讓前端團隊可以更快地組合能力，而後端只需維護好各自領域的 MCP 伺服器。協作邊界從「逐介面對接」變成「逐能力註冊」，顯著降低了跨團隊溝通成本，也減少了因介面契約頻繁變更引發的回歸問題。"),
   ("在遺留系統上落地 MCP 有哪些務實路徑？",
    "多數企業並不會推倒重來，而是把 MCP 作為遺留系統的現代化適配層。常見做法是先為非核心但呼叫頻繁的能力（如設定讀取、日誌查詢、元資料檢索）封裝 MCP 伺服器，驗證協議與治理模型，再逐步把關鍵業務系統接入。對於沒有原生 API 的舊系統，可以用一對腳本化的連接器包裝現有命令列或資料庫存取，在不改動原系統的前提下暴露為 MCP 工具。這種漸進策略能把風險控制在可回滾的範圍內，讓組織在獲得 AI 原生整合紅利的同時，不必承擔一次性大重構的成本與不確定性。"),
 ],
 ("data-mesh-vs-data-warehouse-choosing-the-right-architecture","zh-TW"): [
   ("資料網格如何與資料治理框架共存？",
    "資料網格常被誤讀為「放棄集中治理」，事實恰恰相反：它把治理從中心化的管控，轉變為可組合的策略與標準。全域治理團隊負責定義身分、安全、分類與互通標準，而各領域團隊在本地執行這些標準並對外提供可發現、可信任的資料產品。這種「聯邦式治理」讓合規要求以程式碼與契約的形式內嵌在資料產品中，而不是靠人工審批層層把關。結果是在保持規模靈活性的同時，依然滿足審計、隱私與可追溯的硬性要求。"),
   ("怎樣判斷你的組織已經準備好資料網格？",
    "資料網格不是技術選型，而是組織成熟度的體現。在啟動之前，先確認三件事：第一，業務域邊界是否清晰，能否明確每個資料產品的歸屬團隊；第二，平台團隊是否具備為領域提供自助能力（而非接手開發）的意願與預算；第三，是否存在足夠的激勵機制，讓領域團隊願意長期維護資料品質。如果這三點的答案都是肯定的，資料網格能顯著加速價值交付；如果仍依賴中心團隊逐需求交付，那麼先在平台與契約上補課，會比倉促推行網格帶來更穩妥的回報。"),
 ],
 ("education-personalised-learning-pathways-through-data-a-2026-update","zh-TW"): [
   ("個人化學習如何與現有教學管理系統整合？",
    "個人化學習路徑要真正落地，必須接入學校既有的學生資訊系統（SIS）、學習管理系統（LMS）與教務排課系統。許多專案失敗，是因為把資料平台當成獨立孤島來建設。正確的做法是把資料產品作為共享能力，透過標準介面把成績、出勤、作業完成度與課堂行為訊號匯聚到統一的學科域中。教師在原有 LMS 介面裡就能看到推薦路徑，而不是被迫切換到一個新系統。整合時優先採用事件驅動的同步方式，確保學生進度變化能在數分鐘內反映到路徑引擎。同時要保留教師在迴路中的最終決策權：系統給出建議，教師確認或調整。這種「人在迴路」的設計既保證了規模化的個人體驗，又不削弱教育的專業判斷，也更容易通過學校的治理與隱私審查。"),
   ("如何向家長與學生溝通個人化學習的價值？",
    "個人化學習常常被誤解為「用演算法取代老師」。有效的溝通應當把重點放在學生的成長與自主權上，而不是技術本身。學校可以透過季度學習報告，用視覺化方式展示每位學生在閱讀、數學與探究能力上的進步曲線，並說明路徑調整背後的原因。家長最關心的是孩子是否受到公平對待，因此要公開路徑推薦的維度與邊界，明確哪些因素會影響建議、哪些不會。學生層面，則應讓他們看到自己可以主動選擇挑戰難度與目標，從而建立學習的 ownership。當個人化成為可見、可解釋、可參與的過程，抵觸情緒會顯著降低，專案也更容易獲得持續的資金與政策支持。"),
 ],
}

def cjk_count(s): return len(re.findall(r'[\u3400-\u9fff\uf900-\ufaff]', s))
def en_words(s): return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))

for (slug, lang), sections in ADD.items():
    prefix = "" if lang=="en" else lang.lower()+"/"
    p = os.path.join(ROOT, prefix+"blog/articles/"+slug+".html")
    with open(p, encoding='utf-8') as f:
        html = f.read()
    # guard: ensure h1 matches slug context (re-read h1)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    h1t = re.sub(r'<[^>]+>','',h1.group(1)).strip() if h1 else ""
    block = "".join(sec(h2,b) for h2,b in sections)
    anchor = re.search(r'<section class="faq-section"', html)
    if not anchor:
        print(f"NO FAQ ANCHOR: {slug} {lang}"); continue
    html2 = html[:anchor.start()] + block + html[anchor.start():]
    with open(p, "w", encoding='utf-8') as f:
        f.write(html2)
    # measure
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html2, re.S)
    body = m.group(1) if m else html2
    if lang=="en":
        print(f"{slug[:40]:40} {lang} +{en_words(block)}w h1='{h1t[:30]}'")
    else:
        print(f"{slug[:40]:40} {lang} +{cjk_count(block)}cjk h1='{h1t[:20]}'")
print("DONE")
