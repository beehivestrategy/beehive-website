import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "what-is-ai-agent-autonomous-system"

EN_ADD = """
<h2 id="what-should-an-agent-be-allowed-to-do">What Should an Agent Be Allowed to Do?</h2>
<p>Autonomy is not a switch; it is a dial, and the most common enterprise mistake is setting it once for the whole system instead of per capability. A single agent can be read-only for financial data, draft-only for customer emails, and fully autonomous for internal ticket triage — and it should be. The discipline is to define autonomy per action class, then grant the least autonomy each class can tolerate while still being useful.</p>
<p>Five levels are enough to describe almost every deployment. At level zero the agent only answers and never acts. At level one it prepares — drafts an email, stages a record change, proposes a re-order — and a human approves. At level two it acts within a bounded envelope: it may reorder stock below a threshold, but only up to a value cap. At level three it acts and reports, with exceptions escalated after the fact. At level four it acts autonomously with periodic audit and no per-action review. Most successful enterprises run the bulk of their agents at levels one and two, and promote individual capabilities upward only after months of clean audit history.</p>
<table class="article-table">
<thead><tr><th>Autonomy level</th><th>What the agent does</th><th>Human involvement</th><th>Typical enterprise use</th></tr></thead>
<tbody>
<tr><td>0 — Answer</td><td>Retrieves and explains; never changes state</td><td>Initiates every request</td><td>Conversational analytics, policy Q&amp;A</td></tr>
<tr><td>1 — Prepare</td><td>Drafts or stages an action</td><td>Approves each item</td><td>Customer replies, journal entries</td></tr>
<tr><td>2 — Bounded act</td><td>Acts within a value or scope cap</td><td>Reviews exceptions</td><td>Replenishment below a threshold</td></tr>
<tr><td>3 — Act and report</td><td>Acts broadly, escalates anomalies</td><td>Reviews summary</td><td>Ticket routing, routine reconciliation</td></tr>
<tr><td>4 — Autonomous</td><td>Acts without per-action review</td><td>Audits periodically</td><td>Infrastructure scaling, spam filtering</td></tr>
</tbody>
</table>
<p>Two properties make any level safe. First, reversibility: prefer actions that can be undone, and require approval for those that cannot. Second, traceability: every action must be attributable to a goal, a tool call, and an authorising policy, or the audit trail will not survive the first serious incident. Autonomy without those two properties is not autonomy — it is an unmanaged liability.</p>
<h2 id="how-do-you-evaluate-an-agent-before-trusting-it">How Do You Evaluate an Agent Before Trusting It in Production?</h2>
<p>Agents fail differently from models, so they need a different evaluation. A model is judged on the quality of its output; an agent is judged on whether it completed the task, whether it did so within its authority, and whether it knew when to stop. That means an evaluation harness that scores trajectories, not just answers, and a held-out set of tasks that includes deliberately adversarial scenarios.</p>
<p>The practical harness has four components. Task success measures whether the goal was actually achieved, verified against the system of record rather than against the agent's own report. Tool discipline measures whether the agent called only permitted tools with permitted parameters, and whether it attempted anything outside its authority — an attempted unauthorised call is a finding even if it was blocked. Efficiency measures steps, tokens, and wall-clock time, because an agent that succeeds by trying forty paths is too expensive to run. Escalation behaviour measures whether the agent asked for help when it should have, which is the hardest metric to build and the most predictive of production behaviour.</p>
<table class="article-table">
<thead><tr><th>Dimension</th><th>Metric</th><th>Why it matters</th></tr></thead>
<tbody>
<tr><td>Task success</td><td>Goal completion verified against system of record</td><td>Self-reported success is unreliable</td></tr>
<tr><td>Tool discipline</td><td>Unauthorised or out-of-scope call attempts</td><td>Predicts breach risk better than accuracy</td></tr>
<tr><td>Efficiency</td><td>Steps, tokens, and time per completed task</td><td>Determines unit economics</td></tr>
<tr><td>Escalation</td><td>Correct escalation rate on ambiguous tasks</td><td>Determines how much supervision is needed</td></tr>
<tr><td>Consistency</td><td>Variance in outcome across repeated identical tasks</td><td>High variance destroys user trust</td></tr>
</tbody>
</table>
<p>Run the harness on every change to prompts, tools, or models — not once at launch. Agent behaviour drifts when any of those three moves, and the drift is rarely visible in the happy-path demo. Teams that adopt continuous evaluation ship changes confidently; teams that evaluate once, manually, end up freezing their agents in place out of fear, which is the opposite of the point.</p>
"""

CN_ADD = """
<h2 id="应该允许智能体做什么">应该允许智能体做什么？</h2>
<p>自主性不是一个开关，而是一个旋钮；企业最常见的错误是给整个系统统一设定一次，而不是按能力分别设定。同一个智能体可以对财务数据只读、对客户邮件只起草、对内部工单分派完全自主——而且它本就应该如此。纪律在于按行动类别定义自主性，然后在仍然有用的前提下，授予每个类别可以容忍的最低自主度。</p>
<p>五个层级足以描述几乎所有部署。第 0 级：智能体只回答，从不行动。第 1 级：它做准备工作——起草邮件、暂存记录变更、提出补货建议——由人审批。第 2 级：它在有边界的范围内行动，例如可以在阈值以下补货，但不超过金额上限。第 3 级：它行动并汇报，异常事后升级。第 4 级：它完全自主行动，只做周期性审计、不做事前逐项复核。大多数成功的企业让智能体主体运行在第 1 级和第 2 级，只有在数月无瑕疵的审计记录之后，才把个别能力向上提升。</p>
<table class="article-table">
<thead><tr><th>自主级别</th><th>智能体做什么</th><th>人的参与方式</th><th>典型企业用途</th></tr></thead>
<tbody>
<tr><td>0 — 回答</td><td>检索并解释，从不改变状态</td><td>发起每一次请求</td><td>对话式分析、制度问答</td></tr>
<tr><td>1 — 准备</td><td>起草或暂存一个动作</td><td>逐项审批</td><td>客户回复、凭证分录</td></tr>
<tr><td>2 — 有界行动</td><td>在金额或范围上限内行动</td><td>复核例外情况</td><td>低于阈值的补货</td></tr>
<tr><td>3 — 行动并汇报</td><td>大范围行动，异常升级</td><td>审阅汇总</td><td>工单路由、例行对账</td></tr>
<tr><td>4 — 自主</td><td>行动前不需逐项复核</td><td>周期性审计</td><td>基础设施扩容、垃圾邮件过滤</td></tr>
</tbody>
</table>
<p>有两个属性能让任何级别都变得安全。第一是可逆性：优先选择可以撤销的动作，对不可撤销的动作要求审批。第二是可追溯性：每个动作都必须能归因到一个目标、一次工具调用和一条授权策略，否则审计轨迹撑不过第一次严重事故。缺少这两项属性的自主性不是自主性，而是一项没人管理的负债。</p>
<h2 id="如何在投产前评估一个智能体">如何在投产前评估一个智能体？</h2>
<p>智能体的失效方式与模型不同，因此需要不同的评估方法。模型按输出质量评判；智能体则按是否完成任务、是否在授权范围内完成、以及是否知道何时该停下来评判。这意味着需要一个评估框架来对行为轨迹打分，而不只是对答案打分，并且要有一组包含刻意对抗场景的留出任务集。</p>
<p>实用的框架包含四个部分。任务成功率衡量目标是否真正达成，并且要对照记录系统而非智能体自己的汇报来验证。工具纪律衡量智能体是否只调用了被允许的工具与参数，以及是否尝试过越权操作——一次被拦截的越权调用尝试同样算作一个问题。效率衡量步骤数、token 数与耗时，因为一个靠尝试四十条路径才成功的智能体，运行成本太高。升级行为衡量智能体是否在该求助时求助，这是最难构建的指标，也是对生产环境行为最具预测性的指标。</p>
<table class="article-table">
<thead><tr><th>维度</th><th>指标</th><th>为什么重要</th></tr></thead>
<tbody>
<tr><td>任务成功率</td><td>对照记录系统验证的目标完成情况</td><td>自我汇报的成功率不可靠</td></tr>
<tr><td>工具纪律</td><td>越权或超出范围的调用尝试</td><td>比准确率更能预测违规风险</td></tr>
<tr><td>效率</td><td>每个完成任务的步骤、token 与时间</td><td>决定单位经济模型</td></tr>
<tr><td>升级行为</td><td>模糊任务上的正确升级率</td><td>决定需要多少人工监督</td></tr>
<tr><td>一致性</td><td>重复相同任务的结果方差</td><td>方差过大会摧毁用户信任</td></tr>
</tbody>
</table>
<p>提示词、工具或模型每次变动都要跑一遍这个框架，而不是上线时跑一次。三者中任何一个变化，智能体行为就会漂移，而这种漂移在标准演示路径上几乎看不出来。采用持续评估的团队能放心地发布变更；只做一次性人工评估的团队，最终会因为担心而把智能体冻结在原地，这与智能体的初衷正好相反。</p>
"""

TW_ADD = """
<h2 id="應該允許智慧代理做什麼">應該允許智慧代理做什麼？</h2>
<p>自主性不是一個開關，而是一個旋鈕；企業最常見的錯誤是替整個系統統一設定一次，而不是按能力分別設定。同一個智慧代理可以對財務資料唯讀、對客戶郵件只起草、對內部工單分派完全自主——而且它本來就應該如此。紀律在於按行動類別定義自主性，然後在仍然有用的前提下，授予每個類別可以容忍的最低自主程度。</p>
<p>五個層級足以描述幾乎所有部署。第 0 級：智慧代理只回答，從不行動。第 1 級：它做準備工作——起草郵件、暫存紀錄變更、提出補貨建議——由人審批。第 2 級：它在有邊界的範圍內行動，例如可以在門檻以下補貨，但不超過金額上限。第 3 級：它行動並回報，異常事後升級。第 4 級：它完全自主行動，只做週期性稽核、不做事前逐項覆核。大多數成功的企業讓智慧代理主體運行在第 1 級和第 2 級，只有在數月無瑕疵的稽核紀錄之後，才把個別能力向上提升。</p>
<table class="article-table">
<thead><tr><th>自主層級</th><th>智慧代理做什麼</th><th>人的參與方式</th><th>典型企業用途</th></tr></thead>
<tbody>
<tr><td>0 — 回答</td><td>檢索並解釋，從不改變狀態</td><td>發起每一次請求</td><td>對話式分析、制度問答</td></tr>
<tr><td>1 — 準備</td><td>起草或暫存一個動作</td><td>逐項審批</td><td>客戶回覆、憑證分錄</td></tr>
<tr><td>2 — 有界行動</td><td>在金額或範圍上限內行動</td><td>覆核例外情況</td><td>低於門檻的補貨</td></tr>
<tr><td>3 — 行動並回報</td><td>大範圍行動，異常升級</td><td>審閱彙總</td><td>工單路由、例行對帳</td></tr>
<tr><td>4 — 自主</td><td>行動前不需逐項覆核</td><td>週期性稽核</td><td>基礎設施擴充、垃圾郵件過濾</td></tr>
</tbody>
</table>
<p>有兩項屬性能讓任何層級都變得安全。第一是可逆性：優先選擇可以撤銷的動作，對不可撤銷的動作要求審批。第二是可追溯性：每個動作都必須能歸因到一個目標、一次工具呼叫和一條授權政策，否則稽核軌跡撐不過第一次嚴重事故。缺少這兩項屬性的自主性不是自主性，而是一項沒人管理的負債。</p>
<h2 id="如何在投產前評估一個智慧代理">如何在投產前評估一個智慧代理？</h2>
<p>智慧代理的失效方式與模型不同，因此需要不同的評估方法。模型按輸出品質評判；智慧代理則按是否完成任務、是否在授權範圍內完成、以及是否知道何時該停下來評判。這意味著需要一套評估框架來對行為軌跡評分，而不只是對答案評分，並且要有一組包含刻意對抗情境的保留任務集。</p>
<p>實用的框架包含四個部分。任務成功率衡量目標是否真正達成，並且要對照紀錄系統而非智慧代理自己的回報來驗證。工具紀律衡量智慧代理是否只呼叫了被允許的工具與參數，以及是否嘗試過越權操作——一次被攔截的越權呼叫嘗試同樣算作一個問題。效率衡量步驟數、token 數與耗時，因為一個靠嘗試四十條路徑才成功的智慧代理，運行成本太高。升級行為衡量智慧代理是否在該求助時求助，這是最難建構的指標，也是對生產環境行為最具預測性的指標。</p>
<table class="article-table">
<thead><tr><th>維度</th><th>指標</th><th>為什麼重要</th></tr></thead>
<tbody>
<tr><td>任務成功率</td><td>對照紀錄系統驗證的目標完成情況</td><td>自我回報的成功率不可靠</td></tr>
<tr><td>工具紀律</td><td>越權或超出範圍的呼叫嘗試</td><td>比準確率更能預測違規風險</td></tr>
<tr><td>效率</td><td>每個完成任務的步驟、token 與時間</td><td>決定單位經濟模型</td></tr>
<tr><td>升級行為</td><td>模糊任務上的正確升級率</td><td>決定需要多少人工監督</td></tr>
<tr><td>一致性</td><td>重複相同任務的結果變異</td><td>變異過大會摧毀使用者信任</td></tr>
</tbody>
</table>
<p>提示詞、工具或模型每次變動都要跑一遍這個框架，而不是上線時跑一次。三者中任何一個變化，智慧代理行為就會漂移，而這種漂移在標準展示路徑上幾乎看不出來。採用持續評估的團隊能放心地發布變更；只做一次性人工評估的團隊，最終會因為擔心而把智慧代理凍結在原地，這與智慧代理的初衷正好相反。</p>
"""

H2FIX = {
    "EN": [
        ("types-of-ai-agents", "What Types of AI Agents Exist?"),
        ("why-ai-agents-matter-for-enterprises", "Why Do AI Agents Matter for Enterprises?"),
        ("beehive-strategy-and-ai-agents", "How Does Beehive Strategy Approach AI Agents?"),
        ("key-considerations-for-implementation", "What Are the Key Considerations for Implementation?"),
        ("beehive-strategy-comprehensive-approach", "What Does Beehive Strategy's Comprehensive Approach Include?"),
    ],
    "CN": [
        ("如何工作", "AI 智能体如何工作？"),
        ("为什么对企业重要", "为什么 AI 智能体对企业重要？"),
        ("蜂启咨询与ai智能体", "蜂启咨询与 AI 智能体有何关联？"),
        ("核心优势与技术特点", "核心优势与技术特点是什么？"),
        ("实施策略与成功要素", "实施策略与成功要素有哪些？"),
        ("行业应用与未来展望", "行业应用与未来展望如何？"),
        ("总结与关键建议", "如何总结关键建议？"),
        ("蜂启咨询的综合解决方案", "蜂启咨询的综合解决方案是什么？"),
    ],
    "TW": [
        ("如何運作", "AI 智慧代理如何運作？"),
        ("為什麼對企業重要", "為什麼 AI 智慧代理對企業重要？"),
        ("蜂啟諮詢與ai智能體", "蜂啟諮詢與 AI 智慧代理有何關聯？"),
        ("核心優勢與技術特點", "核心優勢與技術特點是什麼？"),
        ("實施策略與成功要素", "實施策略與成功要素有哪些？"),
        ("產業應用與未來展望", "產業應用與未來展望如何？"),
        ("總結與關鍵建議", "如何總結關鍵建議？"),
        ("蜂啟諮詢的綜合解決方案", "蜂啟諮詢的綜合解決方案是什麼？"),
    ],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD, "CN": CN_ADD, "TW": TW_ADD}, tag=SLUG[:24])
