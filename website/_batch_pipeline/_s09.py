import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "microsoft-teams-analytics-dashboards"

EN_ADD = """
<h2 id="how-do-you-design-the-conversation-for-a-chat-analytics-surface">How Do You Design the Conversation for a Chat Analytics Surface?</h2>
<p>A dashboard is designed by arranging visuals; a chat analytics surface is designed by writing conversations. That difference catches most teams unprepared, because the skills that make a good report — dense layout, many metrics, careful labelling — are close to the opposite of what works in a thread. In chat, the answer has to fit a message, name the number, and state the period and the source, or the reader will ask again in a follow-up that costs more than the original question.</p>
<p>The practical design rule is to optimise for the first reply rather than for completeness. A good first reply answers the literal question, states the scope it assumed, and offers the two most likely follow-ups as buttons or suggested prompts. A bad first reply returns a table with thirty rows, or asks the user to choose from a menu before showing anything. The reason is behavioural: in a channel, other people read the answer too, and a compact, sourced answer gets trusted and reused, while a wall of output gets scrolled past and the channel goes back to guessing.</p>
<table class="article-table">
<thead><tr><th>Interaction</th><th>Weak design</th><th>Strong design</th></tr></thead>
<tbody>
<tr><td>Asking for a figure</td><td>Bot returns a link to a report</td><td>Bot states the number, period, and source, and offers a drill-down</td></tr>
<tr><td>Ambiguous question</td><td>Bot guesses silently</td><td>Bot restates its interpretation and asks for confirmation</td></tr>
<tr><td>Data not available</td><td>Bot returns an empty result</td><td>Bot says what it cannot answer and who owns that data</td></tr>
<tr><td>Threshold alert</td><td>Alert fires on every small movement</td><td>Alert fires on a defined threshold with the delta and a link to detail</td></tr>
<tr><td>Follow-up</td><td>User restates the whole question</td><td>Bot carries context so "and by region?" works</td></tr>
</tbody>
</table>
<p>Two habits make the difference between a bot that is used and one that is tolerated. First, teach it to say no gracefully: "I do not have that data" is far more trust-building than a plausible answer assembled from the wrong table. Second, publish a short list of what it can answer. Users cannot ask for something they do not know exists, and most low adoption is really low awareness.</p>
<h2 id="how-should-permissions-and-audit-work-in-a-shared-channel">How Should Permissions and Audit Work in a Shared Channel?</h2>
<p>Chat collapses the distance between asking and sharing, which is exactly why permissions cannot be an afterthought. In a BI portal, a user navigates to a report they are entitled to see. In a channel, a user asks a question in front of an audience, and the answer is broadcast to everyone in that conversation. The control that matters is therefore not "may this user query this data?" but "may this user receive this answer in this channel?" — a subtly different question that most BI security models were never designed to answer.</p>
<p>The workable pattern is answer-level authorisation. Every query carries the asker's identity, the semantic layer resolves the permitted scope for that identity, and the answer is filtered before it is rendered — so the same question asked by a regional manager and by a finance director returns different, correctly scoped numbers. Where the asker's permissions do not cover part of the answer, the assistant should return the permitted portion and state clearly that the rest was withheld, rather than refusing the whole question. Row-level security, column-level masking, and data classification all have to be inherited from the warehouse rather than reimplemented in the bot, or the two will drift apart within a quarter.</p>
<table class="article-table">
<thead><tr><th>Control</th><th>What it does</th><th>Failure it prevents</th></tr></thead>
<tbody>
<tr><td>Identity propagation</td><td>Carries the asker's identity into every query</td><td>Bot answering with a service account's broad permissions</td></tr>
<tr><td>Answer-level filtering</td><td>Filters results to the asker's permitted scope</td><td>Revenue figures visible to a channel with external guests</td></tr>
<tr><td>Partial-response disclosure</td><td>Returns permitted data and states what was withheld</td><td>Silent truncation that looks like a complete answer</td></tr>
<tr><td>Source attribution</td><td>Every number names its definition and source system</td><td>Two channels arguing about whose figure is right</td></tr>
<tr><td>Query logging</td><td>Records who asked what, where, and what was returned</td><td>No audit trail when a compliance question is raised</td></tr>
<tr><td>Channel sensitivity rules</td><td>Blocks or redacts sensitive classes in shared channels</td><td>A casual question leaking regulated data</td></tr>
</tbody>
</table>
<h2 id="what-does-a-phased-teams-rollout-look-like">What Does a Phased Teams Rollout Look Like?</h2>
<p>The rollout pattern that avoids muting is to earn the right to speak. Start narrow — one channel, one question type, one high-frequency decision — and expand only when the channel's own members ask for more. This is the opposite of a big-bang deployment, and it works because notification fatigue is the dominant failure mode: a bot that is useful in one channel gets invited to the next, whereas a bot pushed everywhere at once gets muted everywhere at once.</p>
<p>Phase one is read-only question answering in a single channel with an enthusiastic owner, instrumented from day one for question volume, answer acceptance, and escalation to a human. Phase two adds threshold alerts, but only for thresholds the channel's owner has explicitly chosen and named. Phase three introduces the assistant into adjacent channels by invitation, with a short onboarding message explaining what it can and cannot answer. Phase four connects the assistant to actions — creating a ticket, requesting an approval — always with a human confirmation step inside the same thread.</p>
<table class="article-table">
<thead><tr><th>Phase</th><th>Capability added</th><th>Adoption signal to watch</th></tr></thead>
<tbody>
<tr><td>1</td><td>Read-only Q&amp;A in one channel</td><td>Repeat users per week, not total questions</td></tr>
<tr><td>2</td><td>Owner-chosen threshold alerts</td><td>Alerts acted on rather than ignored</td></tr>
<tr><td>3</td><td>Invitation-only expansion</td><td>Channels requesting access unprompted</td></tr>
<tr><td>4</td><td>Actions with in-thread confirmation</td><td>Completed actions and time saved</td></tr>
</tbody>
</table>
<p>The metric that predicts long-term success is not question count; it is the number of people who ask a second question. A bot that answers once curiosity is satisfied has been a novelty. A bot that becomes the place a team checks before a meeting has changed how the team works — and that is the outcome worth designing the rollout around.</p>
"""

CN_ADD = """
<h2 id="如何设计对话式分析的交互">如何设计对话式分析的交互？</h2>
<p>仪表盘是通过排布视觉元素来设计的；对话式分析界面则是通过编写对话来设计的。这个差异常常让团队措手不及，因为做出一份好报表所需的技能——密集布局、多指标、细致标注——几乎与在会话线程中奏效的做法相反。在聊天中，答案必须能放进一条消息里，要点明数字，并说明统计区间与来源，否则读者会用一次追问来补充，而追问的成本比原始问题还高。</p>
<p>实用的设计原则是：优先优化第一次回复，而不是追求完整。好的首次回复会回答字面问题、说明它所假设的口径，并把两个最可能的后续追问以按钮或推荐问法的形式给出。糟糕的首次回复则返回一张三十行的表格，或者在展示任何内容之前先让用户从菜单里选择。原因在于行为层面：在频道中，其他人也会读到这个答案，一个简洁、带出处的答案会被信任并反复引用；而一整屏的输出会被滑过去，频道随后又回到猜数字的状态。</p>
<table class="article-table">
<thead><tr><th>交互场景</th><th>较弱的设计</th><th>较强的设计</th></tr></thead>
<tbody>
<tr><td>询问某个数值</td><td>机器人返回一个报表链接</td><td>机器人给出数字、区间与来源，并提供下钻</td></tr>
<tr><td>问题含糊</td><td>机器人默默猜测</td><td>机器人复述自己的理解并请求确认</td></tr>
<tr><td>数据不存在</td><td>机器人返回空结果</td><td>机器人说明无法回答的内容以及该数据归属谁</td></tr>
<tr><td>阈值告警</td><td>任何微小波动都触发告警</td><td>按既定阈值触发，并给出变化量与详情链接</td></tr>
<tr><td>连续追问</td><td>用户重述整个问题</td><td>机器人保留上下文，使「按地区呢？」可以成立</td></tr>
</tbody>
</table>
<p>有两个习惯决定了机器人是被使用还是被忍耐。第一，教会它优雅地说不：「我没有这份数据」远比用错误的表拼出一个貌似合理的答案更能建立信任。第二，公开一份简短的能力清单。用户不会去问他们不知道存在的功能，大多数低使用率的真实原因是低知晓率。</p>
<h2 id="共享频道中的权限与审计应如何设计">共享频道中的权限与审计应如何设计？</h2>
<p>聊天把「提问」与「分享」之间的距离压缩到几乎为零，这正是权限不能事后补救的原因。在 BI 门户中，用户会导航到自己有权查看的报表；而在频道中，用户是在一群人面前提问，答案会广播给会话中的所有人。因此真正重要的控制不是「该用户能否查询这份数据」，而是「该用户能否在这个频道里收到这个答案」——这个细微的差别，是大多数 BI 安全模型从未被设计来回答的。</p>
<p>可行的模式是答案级授权。每次查询都携带提问者的身份，语义层解析出该身份被允许的范围，并在渲染之前对答案进行过滤——于是区域经理和财务总监提出同一个问题，会得到各自范围内、都正确的不同数字。当提问者的权限无法覆盖答案的某一部分时，助手应返回被允许的部分，并明确说明其余部分已被隐藏，而不是整体拒绝回答。行级安全、列级脱敏与数据分级都必须从数据仓库继承，而不是在机器人里重新实现，否则两者在一个季度内就会产生偏差。</p>
<table class="article-table">
<thead><tr><th>控制项</th><th>作用</th><th>可预防的失效</th></tr></thead>
<tbody>
<tr><td>身份传递</td><td>把提问者身份带入每一次查询</td><td>机器人以服务账号的宽泛权限作答</td></tr>
<tr><td>答案级过滤</td><td>按提问者权限范围过滤结果</td><td>含外部访客的频道看到营收数字</td></tr>
<tr><td>部分响应披露</td><td>返回许可数据并说明被隐藏的部分</td><td>静默截断，看起来却像完整答案</td></tr>
<tr><td>来源标注</td><td>每个数字注明定义与来源系统</td><td>两个频道争论谁的数字才对</td></tr>
<tr><td>查询日志</td><td>记录谁在何处问了什么、返回了什么</td><td>合规质询时没有审计轨迹</td></tr>
<tr><td>频道敏感度规则</td><td>在共享频道中拦截或遮蔽敏感数据分级</td><td>随口一问导致受监管数据泄露</td></tr>
</tbody>
</table>
<h2 id="分阶段的Teams推广路径是什么样">分阶段的 Teams 推广路径是什么样？</h2>
<p>能避免被静音的推广模式，是先赢得发言的资格。从窄处开始——一个频道、一类问题、一个高频决策——只有当该频道成员自己提出更多需求时才扩展。这与一次性全面铺开正好相反，而它之所以有效，是因为通知疲劳是最主要的失效模式：在一个频道里有用的机器人会被邀请进下一个频道，而被一次性推到所有地方的机器人会在所有地方同时被静音。</p>
<p>第一阶段是在单一频道中做只读问答，配一位积极的频道负责人，并从第一天起埋点统计提问量、答案采纳率与转人工率。第二阶段加入阈值告警，但仅限于频道负责人明确选定并命名的阈值。第三阶段通过邀请制把助手引入相邻频道，并附一段简短的上手说明，讲清它能回答什么、不能回答什么。第四阶段把助手连接到动作——创建工单、发起审批——并且始终在同一线程中保留人工确认步骤。</p>
<table class="article-table">
<thead><tr><th>阶段</th><th>新增能力</th><th>需关注的采用信号</th></tr></thead>
<tbody>
<tr><td>1</td><td>单一频道内只读问答</td><td>每周重复使用者数，而非提问总数</td></tr>
<tr><td>2</td><td>由负责人选定的阈值告警</td><td>告警被处理，而非被忽略</td></tr>
<tr><td>3</td><td>邀请制扩展</td><td>其他频道主动申请接入</td></tr>
<tr><td>4</td><td>带线程内确认的动作</td><td>已完成动作数与节省的时间</td></tr>
</tbody>
</table>
<p>预测长期成功的指标不是提问次数，而是提出第二个问题的人数。只在好奇心被满足时回答一次的机器人，只是一个新鲜玩意儿；而成为团队开会前必查之地的机器人，改变了团队的协作方式——而这才值得围绕它来设计推广路径。</p>
"""

TW_ADD = """
<h2 id="如何設計對話式分析的互動">如何設計對話式分析的互動？</h2>
<p>儀表板是透過排列視覺元素來設計的；對話式分析介面則是透過撰寫對話來設計的。這個差異常讓團隊措手不及，因為做出一份好報表所需的技能——密集佈局、多指標、細緻標註——幾乎與在對話執行緒中奏效的做法相反。在聊天中，答案必須能放進一則訊息裡，要點明數字，並說明統計區間與來源，否則讀者會用一次追問來補充，而追問的成本比原始問題還高。</p>
<p>實用的設計原則是：優先最佳化第一次回覆，而不是追求完整。好的首次回覆會回答字面問題、說明它所假設的口徑，並把兩個最可能的後續追問以按鈕或推薦問法的形式提供。糟糕的首次回覆則回傳一張三十列的表格，或在呈現任何內容之前先讓使用者從選單中選擇。原因在於行為層面：在頻道中，其他人也會讀到這個答案，一個簡潔、帶出處的答案會被信任並反覆引用；而一整屏的輸出會被滑過去，頻道隨後又回到猜數字的狀態。</p>
<table class="article-table">
<thead><tr><th>互動情境</th><th>較弱的設計</th><th>較強的設計</th></tr></thead>
<tbody>
<tr><td>詢問某個數值</td><td>機器人回傳一個報表連結</td><td>機器人給出數字、區間與來源，並提供下鑽</td></tr>
<tr><td>問題含糊</td><td>機器人默默猜測</td><td>機器人複述自己的理解並請求確認</td></tr>
<tr><td>資料不存在</td><td>機器人回傳空結果</td><td>機器人說明無法回答的內容以及該資料歸屬誰</td></tr>
<tr><td>門檻告警</td><td>任何微小波動都觸發告警</td><td>依既定門檻觸發，並提供變化量與詳情連結</td></tr>
<tr><td>連續追問</td><td>使用者重述整個問題</td><td>機器人保留上下文，使「按地區呢？」可以成立</td></tr>
</tbody>
</table>
<p>有兩個習慣決定了機器人是被使用還是被忍耐。第一，教會它優雅地說不：「我沒有這份資料」遠比用錯誤的表拼出一個貌似合理的答案更能建立信任。第二，公開一份簡短的能力清單。使用者不會去問他們不知道存在的功能，大多數低使用率的真實原因是低知曉率。</p>
<h2 id="共用頻道中的權限與稽核應如何設計">共用頻道中的權限與稽核應如何設計？</h2>
<p>聊天把「提問」與「分享」之間的距離壓縮到幾乎為零，這正是權限不能事後補救的原因。在 BI 入口網站中，使用者會導覽到自己有權檢視的報表；而在頻道中，使用者是在一群人面前提問，答案會廣播給對話中的所有人。因此真正重要的控制不是「該使用者能否查詢這份資料」，而是「該使用者能否在這個頻道裡收到這個答案」——這個細微的差別，是大多數 BI 安全模型從未被設計來回答的。</p>
<p>可行的模式是答案級授權。每次查詢都攜帶提問者的身分，語意層解析出該身分被允許的範圍，並在呈現之前對答案進行過濾——於是區域經理和財務總監提出同一個問題，會得到各自範圍內、都正確的不同數字。當提問者的權限無法涵蓋答案的某一部分時，助理應回傳被允許的部分，並明確說明其餘部分已被隱藏，而不是整體拒絕回答。列級安全、欄位級遮罩與資料分級都必須從資料倉儲繼承，而不是在機器人裡重新實作，否則兩者在一個季度內就會產生偏差。</p>
<table class="article-table">
<thead><tr><th>控制項</th><th>作用</th><th>可預防的失效</th></tr></thead>
<tbody>
<tr><td>身分傳遞</td><td>把提問者身分帶入每一次查詢</td><td>機器人以服務帳號的寬泛權限作答</td></tr>
<tr><td>答案級過濾</td><td>依提問者權限範圍過濾結果</td><td>含外部訪客的頻道看到營收數字</td></tr>
<tr><td>部分回應揭露</td><td>回傳許可資料並說明被隱藏的部分</td><td>靜默截斷，看起來卻像完整答案</td></tr>
<tr><td>來源標註</td><td>每個數字註明定義與來源系統</td><td>兩個頻道爭論誰的數字才對</td></tr>
<tr><td>查詢紀錄</td><td>記錄誰在何處問了什麼、回傳了什麼</td><td>合規質詢時沒有稽核軌跡</td></tr>
<tr><td>頻道敏感度規則</td><td>在共用頻道中攔截或遮罩敏感資料分級</td><td>隨口一問導致受監管資料外洩</td></tr>
</tbody>
</table>
<h2 id="分階段的Teams推廣路徑是什麼樣">分階段的 Teams 推廣路徑是什麼樣？</h2>
<p>能避免被靜音的推廣模式，是先贏得發言的資格。從窄處開始——一個頻道、一類問題、一個高頻決策——只有當該頻道成員自己提出更多需求時才擴充。這與一次性全面鋪開正好相反，而它之所以有效，是因為通知疲勞是最主要的失效模式：在一個頻道裡有用的機器人會被邀請進下一個頻道，而被一次性推到所有地方的機器人會在所有地方同時被靜音。</p>
<p>第一階段是在單一頻道中做唯讀問答，並安排一位積極的頻道負責人，從第一天起就埋點統計提問量、答案採納率與轉人工率。第二階段加入門檻告警，但僅限於頻道負責人明確選定並命名的門檻。第三階段透過邀請制把助理引入相鄰頻道，並附一段簡短的上手說明，講清它能回答什麼、不能回答什麼。第四階段把助理連接到動作——建立工單、發起審批——並且始終在同一執行緒中保留人工確認步驟。</p>
<table class="article-table">
<thead><tr><th>階段</th><th>新增能力</th><th>需關注的採用訊號</th></tr></thead>
<tbody>
<tr><td>1</td><td>單一頻道內唯讀問答</td><td>每週重複使用人數，而非提問總數</td></tr>
<tr><td>2</td><td>由負責人選定的門檻告警</td><td>告警被處理，而非被忽略</td></tr>
<tr><td>3</td><td>邀請制擴充</td><td>其他頻道主動申請接入</td></tr>
<tr><td>4</td><td>帶執行緒內確認的動作</td><td>已完成動作數與節省的時間</td></tr>
</tbody>
</table>
<p>預測長期成功的指標不是提問次數，而是提出第二個問題的人數。只在好奇心被滿足時回答一次的機器人，只是一個新鮮玩意兒；而成為團隊開會前必查之地的機器人，改變了團隊的協作方式——而這才值得圍繞它來設計推廣路徑。</p>
"""

H2FIX = {
    "EN": [
        ("why-it-matters", "Why Does Analytics Inside Teams Matter?"),
        ("common-challenges", "What Are the Common Challenges?"),
        ("how-to-get-started", "How Do You Get Started?"),
        ("frequently-asked-questions", "What Are the Most Frequently Asked Questions?"),
        ("key-takeaways", "What Are the Key Takeaways?"),
    ],
    "CN": [
        ("为什么重要", "为什么重要？"),
        ("常见挑战", "常见挑战有哪些？"),
        ("如何开始", "如何开始？"),
        ("核心要点", "核心要点有哪些？"),
        ("常见问题", "常见问题有哪些？"),
    ],
    "TW": [
        ("爲什麼重要", "爲什麼重要？"),
        ("常見挑戰", "常見挑戰有哪些？"),
        ("如何開始", "如何開始？"),
        ("核心要點", "核心要點有哪些？"),
        ("常見問題", "常見問題有哪些？"),
    ],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD, "CN": CN_ADD, "TW": TW_ADD},
        cta_fix={"TW": ('<a href="/zh-tw/contact" class="article-cta-btn">預約演示</a>',
                        '<a href="/zh-tw/contact" class="article-cta-btn">預約示範</a>')},
        tag=SLUG[:24])
