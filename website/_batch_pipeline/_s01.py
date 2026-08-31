import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "fall-conference-roundup-ai-announcements-oct2025"

EN_ADD = """
<h2 id="which-announcements-matter-most-for-enterprise-buyers-in-2026">Which Announcements Matter Most for Enterprise Buyers in 2026?</h2>
<p>Not every keynote deserves a line in your roadmap. The useful way to sort the fall 2025 announcements is by the layer of your stack they change, because that determines who has to do the work. Model releases change cost and quality but rarely change architecture; platform runtimes change where agents live and how they are governed; connectivity standards change how quickly you can attach your own data. Buyers who classify announcements this way stop chasing every release and start investing in the two or three that actually remove a constraint.</p>
<p>Applied to this season, the classification produces a short list. AgentKit, Agentforce 360, Copilot Studio, and the AWS agent services all sit in the runtime layer, and the runtime you pick will determine your identity model, your audit log format, and your evaluation tooling for years. The Model Context Protocol sits in the connectivity layer, and it is the only announcement on the list that reduces work rather than adding it, because a connector written once against MCP can be reused across any compliant client. Outcome-based pricing sits in the commercial layer, and it changes how you budget more than how you build.</p>
<table class="article-table">
<thead><tr><th>Announcement</th><th>Layer it changes</th><th>What it means for a 2026 plan</th></tr></thead>
<tbody>
<tr><td>OpenAI AgentKit and ChatGPT apps</td><td>Agent runtime and distribution</td><td>Faster prototyping, but you still own data access, permissions, and evaluation</td></tr>
<tr><td>Salesforce Agentforce 360</td><td>Agent runtime over CRM</td><td>Strong if your customer data already lives in Salesforce; weak if it is fragmented</td></tr>
<tr><td>Microsoft Copilot Studio</td><td>Agent runtime plus governance</td><td>Attractive when Microsoft 365 is already the identity and audit backbone</td></tr>
<tr><td>AWS agentic services</td><td>Infrastructure and orchestration</td><td>Best fit when agents must sit next to existing data pipelines and lakehouse storage</td></tr>
<tr><td>Model Context Protocol</td><td>Connectivity standard</td><td>Write the connector once, reuse it across clients; the clearest reduction in future work</td></tr>
<tr><td>Outcome-based pricing</td><td>Commercial model</td><td>Budget per resolved task, not per seat; requires task-level telemetry to control spend</td></tr>
</tbody>
</table>
<p>The practical conclusion is unglamorous but valuable: standardise the data and connectivity layer now, and keep the runtime decision reversible. Every platform wants to be the control plane, and the way to avoid being locked into the wrong one is to own the definitions, the connectors, and the permission model yourself. Organisations that do this can swap agent runtimes in weeks; organisations that let a vendor define their metrics cannot.</p>
<h2 id="how-do-you-tell-durable-capability-from-conference-hype">How Do You Tell Durable Capability From Conference Hype?</h2>
<p>Conference demos are optimised for applause, not for your operating environment. A five-question test cuts through the theatre quickly. First: does the capability run on data you actually govern, or only on the vendor's sample dataset? Second: can you reproduce the demo with your own identity model and access controls turned on? Third: what happens when the model is wrong — is there an evaluation harness, a fallback, and a human escalation path? Fourth: who owns the audit log, and can you export it to your own SIEM? Fifth: is the price tied to a unit you can measure and cap, such as resolved tasks, rather than to an open-ended token count?</p>
<p>The answers separate durable capability from staged capability with uncomfortable reliability. Durable capabilities survive all five questions: they degrade gracefully, they are observable, and they can be switched off without breaking a business process. Staged capabilities answer the first question with a caveat about "roadmap," the third with a slide about safety, and the fifth with a pricing calculator. When a vendor cannot tell you what happens on the failure path, you have learned the most important thing about the product.</p>
<p>There is also a timing signal worth reading. Capabilities that ship with governance tooling, evaluation frameworks, and migration documentation in the same release are usually production-grade, because vendors only invest in the boring parts when enterprise customers have already demanded them. Capabilities announced with a waitlist and no documentation are invitations to be a beta site. Neither is wrong, but only one belongs on a roadmap with a committed date attached.</p>
<h2 id="what-does-a-90-day-post-conference-action-plan-look-like">What Does a 90-Day Post-Conference Action Plan Look Like?</h2>
<p>The value of conference season decays fast: within about six weeks the announcements are common knowledge and the internal momentum is gone. A 90-day plan converts attention into an asset. Weeks one and two are for inventory — capture every announced capability that maps to a real workflow, score it on value and feasibility, and assign a named owner to the top three. Weeks three to six are for the data layer: confirm that the metrics behind your chosen use case have documented definitions and a single accountable owner, and build or validate the connectors that expose them.</p>
<p>Weeks seven to ten are for the pilot itself. Choose a surface where the same question gets asked repeatedly — pipeline status, ticket backlog, month-end variance — and put a conversational answer in front of twenty to fifty real users in the tool they already use. Instrument it from day one: log every question, every answer, every thumbs-down, and every escalation to a human. Weeks eleven to thirteen are for the decision: review the logs against the success metrics you set in week one, and either scale the pilot, adjust it, or kill it explicitly. A pilot that ends with a written decision is worth more than one that drifts.</p>
<table class="article-table">
<thead><tr><th>Phase</th><th>Deliverable</th><th>Exit criterion</th></tr></thead>
<tbody>
<tr><td>Weeks 1-2</td><td>Ranked capability inventory with named owners</td><td>Three use cases scored on value and feasibility</td></tr>
<tr><td>Weeks 3-6</td><td>Governed metric definitions and connectors</td><td>Top use case answers correctly against production data</td></tr>
<tr><td>Weeks 7-10</td><td>Live pilot with 20-50 users and full instrumentation</td><td>Question logs, answer quality scores, escalation rate</td></tr>
<tr><td>Weeks 11-13</td><td>Written scale / adjust / kill decision</td><td>Decision reviewed by the budget owner</td></tr>
</tbody>
</table>
<p>Two failure modes wreck most post-conference plans. The first is starting with model selection instead of use-case selection, which produces an impressive evaluation spreadsheet and no users. The second is skipping instrumentation, which produces a pilot that everyone enjoyed and nobody can justify funding. Both are avoided by the same discipline: decide what you will measure before you decide what you will build.</p>
"""

CN_ADD = """
<h2 id="哪些发布对2026年企业买家最重要">哪些发布对2026年的企业买家最重要？</h2>
<p>并非每一场主题演讲都值得写进路线图。给2025年秋季的发布会排序，最有用的方式是按它改变的是技术栈的哪一层，因为这一层决定了谁来做后续的工作。模型发布改变的是成本与质量，很少改变架构；平台运行时改变的是智能体运行在哪里、如何被治理；连接标准改变的是你多快能把自己的数据接进来。用这种方式分类的买家，会停止追逐每一个新版本，转而投资到真正能消除约束的那两三项上。</p>
<p>按这个框架梳理本季的发布，会得到一份很短的清单。AgentKit、Agentforce 360、Copilot Studio 以及 AWS 的智能体服务都属于运行时层；你选的运行时将决定未来数年的身份模型、审计日志格式与评估工具。模型上下文协议（MCP）属于连接层，它是清单上唯一减少而不是增加工作量的发布——因为按 MCP 写一次的连接器，可以在任何兼容的客户端上复用。按结果计费属于商业层，它改变的更多是预算方式而不是构建方式。</p>
<table class="article-table">
<thead><tr><th>发布内容</th><th>改变的层级</th><th>对2026年规划的意义</th></tr></thead>
<tbody>
<tr><td>OpenAI AgentKit 与 ChatGPT 应用</td><td>智能体运行时与分发</td><td>原型更快，但数据接入、权限与评估仍由你负责</td></tr>
<tr><td>Salesforce Agentforce 360</td><td>基于 CRM 的智能体运行时</td><td>若客户数据已在 Salesforce 中则优势明显；若数据分散则效果有限</td></tr>
<tr><td>Microsoft Copilot Studio</td><td>智能体运行时兼治理</td><td>当 Microsoft 365 已是身份与审计主干时极具吸引力</td></tr>
<tr><td>AWS 智能体服务</td><td>基础设施与编排</td><td>当智能体需紧邻现有数据管道与数据湖时最合适</td></tr>
<tr><td>模型上下文协议（MCP）</td><td>连接标准</td><td>连接器一次编写、跨客户端复用，对未来工作量的削减最明确</td></tr>
<tr><td>按结果计费</td><td>商业模式</td><td>按已解决任务而非席位编列预算，需要任务级遥测来控制支出</td></tr>
</tbody>
</table>
<p>务实的结论并不耀眼但很有价值：现在就把数据与连接层标准化，同时让运行时的选择保持可逆。每个平台都想成为控制面，而避免被锁死在错误平台上的方法，是自己掌握指标定义、连接器与权限模型。做到这一点的组织可以在数周内更换智能体运行时；把指标定义权交给供应商的组织则做不到。</p>
<h2 id="如何区分持久能力与会议炒作">如何区分持久的能力与会议炒作？</h2>
<p>会议演示是为掌声优化的，而不是为你的运行环境优化的。一个五问测试可以很快穿透这些表演。第一：这个能力跑在你真正治理的数据上，还是只跑在厂商的示例数据集上？第二：开启你自己的身份模型与访问控制后，你还能复现这个演示吗？第三：模型出错时会发生什么——是否有评估机制、降级方案和人工升级路径？第四：谁拥有审计日志，你能否把它导出到自己的 SIEM？第五：价格是否绑定在你可以度量和封顶的单位上（例如已解决的任务数），而不是一个上不封顶的 token 计数？</p>
<p>这些答案能非常可靠地区分持久能力与舞台能力。持久的能力能通过全部五问：它会优雅降级、可观测，并且可以在不破坏业务流程的前提下被关掉。舞台能力对第一问的回答是带一个"路线图"的补充说明，对第三问的回答是几页关于安全的幻灯片，对第五问的回答是一个价格计算器。当厂商说不清失败路径上会发生什么时，你已经了解到这个产品最重要的信息了。</p>
<p>还有一个值得解读的时机信号。与治理工具、评估框架和迁移文档同批发布的能力通常已达到生产级，因为只有在企业客户已经提出要求之后，厂商才会投资做这些枯燥的部分。而只公布等待名单、没有任何文档的能力，是在邀请你去做测试场。两者都没有错，但只有其中一个适合写进有承诺日期的路线图。</p>
<h2 id="会后的90天行动计划应该是什么样">会后的90天行动计划应该是什么样？</h2>
<p>会议季的价值衰减得很快：大约六周之内，这些发布已成为常识，内部的推动力也随之消散。90天计划能把注意力转化为资产。第1至2周用于盘点——记录每一个能映射到真实工作流程的新能力，按价值与可行性打分，并为前三项指定具名负责人。第3至6周用于数据层——确认所选用例背后的指标有书面定义和唯一问责人，并构建或验证能暴露这些指标的连接器。</p>
<p>第7至10周用于试点本身。选择一个会被反复提出同类问题的界面——管道状态、工单积压、月末差异——并在用户已经在用的工具里，为二十到五十名真实用户提供对话式答案。从第一天起就埋点：记录每一个问题、每一个答案、每一次点踩、每一次转人工。第11至13周用于决策：把日志与第1周设定的成功指标对照，然后明确地扩大试点、调整试点或终止试点。一个以书面决策收尾的试点，比一个不了了之的试点有价值得多。</p>
<table class="article-table">
<thead><tr><th>阶段</th><th>交付物</th><th>准出标准</th></tr></thead>
<tbody>
<tr><td>第1-2周</td><td>带具名负责人的能力排序清单</td><td>三个用例完成价值与可行性打分</td></tr>
<tr><td>第3-6周</td><td>已治理的指标定义与连接器</td><td>首选用例能基于生产数据给出正确答案</td></tr>
<tr><td>第7-10周</td><td>20-50名用户、完整埋点的上线试点</td><td>问题日志、答案质量评分、转人工率</td></tr>
<tr><td>第11-13周</td><td>书面的扩大／调整／终止决策</td><td>决策经预算负责人评审</td></tr>
</tbody>
</table>
<p>有两个失败模式会毁掉大多数会后计划。第一个是先选模型而不是先选用例，结果产出一份漂亮的评估表格却没有任何用户。第二个是跳过埋点，结果试点人人叫好却没人能论证该继续投钱。两者都靠同一套纪律来避免：在决定建什么之前，先决定要度量什么。</p>
"""

TW_ADD = """
<h2 id="哪些發布對2026年企業買家最重要">哪些發布對2026年的企業買家最重要？</h2>
<p>並非每一場主題演講都值得寫進路線圖。為2025年秋季的發布會排序，最有用的方式是按它改變的是技術堆疊的哪一層，因為這一層決定了誰來做後續的工作。模型發布改變的是成本與品質，很少改變架構；平台執行環境改變的是智慧代理運行在哪裡、如何被治理；連接標準改變的是你多快能把自己的資料接進來。用這種方式分類的買家，會停止追逐每一個新版本，轉而投資到真正能消除限制的那兩三項上。</p>
<p>按這個框架梳理本季的發布，會得到一份很短的清單。AgentKit、Agentforce 360、Copilot Studio 以及 AWS 的智慧代理服務都屬於執行環境層；你選的執行環境將決定未來數年的身分模型、稽核紀錄格式與評估工具。模型上下文協定（MCP）屬於連接層，它是清單上唯一減少而不是增加工作量的發布——因為按 MCP 寫一次的連接器，可以在任何相容的用戶端上重複使用。按結果計費屬於商業層，它改變的更多是預算方式而不是建置方式。</p>
<table class="article-table">
<thead><tr><th>發布內容</th><th>改變的層級</th><th>對2026年規劃的意義</th></tr></thead>
<tbody>
<tr><td>OpenAI AgentKit 與 ChatGPT 應用程式</td><td>智慧代理執行環境與分發</td><td>原型更快，但資料接入、權限與評估仍由你負責</td></tr>
<tr><td>Salesforce Agentforce 360</td><td>以 CRM 為基礎的智慧代理執行環境</td><td>若客戶資料已在 Salesforce 中則優勢明顯；若資料分散則效果有限</td></tr>
<tr><td>Microsoft Copilot Studio</td><td>智慧代理執行環境兼治理</td><td>當 Microsoft 365 已是身分與稽核主幹時極具吸引力</td></tr>
<tr><td>AWS 智慧代理服務</td><td>基礎設施與編排</td><td>當智慧代理需緊鄰既有資料管線與資料湖時最合適</td></tr>
<tr><td>模型上下文協定（MCP）</td><td>連接標準</td><td>連接器一次撰寫、跨用戶端重複使用，對未來工作量的削減最明確</td></tr>
<tr><td>按結果計費</td><td>商業模式</td><td>按已解決任務而非席次編列預算，需要任務級遙測來控制支出</td></tr>
</tbody>
</table>
<p>務實的結論並不耀眼但很有價值：現在就把資料與連接層標準化，同時讓執行環境的選擇保持可逆。每個平台都想成為控制面，而避免被鎖死在錯誤平台上的方法，是自己掌握指標定義、連接器與權限模型。做到這一點的組織可以在數週內更換智慧代理執行環境；把指標定義權交給供應商的組織則做不到。</p>
<h2 id="如何區分持久能力與會議炒作">如何區分持久的能力與會議炒作？</h2>
<p>會議展示是為掌聲最佳化的，而不是為你的運行環境最佳化的。一個五問測試可以很快穿透這些表演。第一：這個能力跑在你真正治理的資料上，還是只跑在廠商的範例資料集上？第二：開啟你自己的身分模型與存取控制後，你還能重現這個展示嗎？第三：模型出錯時會發生什麼——是否有評估機制、降級方案和人工升級路徑？第四：誰擁有稽核紀錄，你能否把它匯出到自己的 SIEM？第五：價格是否綁定在你可以衡量和設定上限的單位上（例如已解決的任務數），而不是一個沒有上限的 token 計數？</p>
<p>這些答案能非常可靠地區分持久能力與舞台能力。持久的能力能通過全部五問：它會優雅降級、可觀測，並且可以在不破壞業務流程的前提下被關閉。舞台能力對第一問的回答是帶一個「路線圖」的補充說明，對第三問的回答是幾頁關於安全的簡報，對第五問的回答是一個價格計算機。當廠商說不清失敗路徑上會發生什麼時，你已經了解到這個產品最重要的資訊了。</p>
<p>還有一個值得解讀的時機訊號。與治理工具、評估框架和遷移文件同批發布的能力通常已達到生產級，因為只有在企業客戶已經提出要求之後，廠商才會投資做這些枯燥的部分。而只公布等待名單、沒有任何文件的能力，是在邀請你去做測試場。兩者都沒有錯，但只有其中一個適合寫進有承諾日期的路線圖。</p>
<h2 id="會後的90天行動計畫應該是什麼樣">會後的90天行動計畫應該是什麼樣？</h2>
<p>會議季的價值衰減得很快：大約六週之內，這些發布已成為常識，內部的推動力也隨之消散。90天計畫能把注意力轉化為資產。第1至2週用於盤點——記錄每一個能對應到真實工作流程的新能力，按價值與可行性評分，並為前三項指定具名負責人。第3至6週用於資料層——確認所選用例背後的指標有書面定義和唯一問責人，並建置或驗證能暴露這些指標的連接器。</p>
<p>第7至10週用於試點本身。選擇一個會被反覆提出同類問題的介面——管道狀態、工單積壓、月末差異——並在使用者已經在用的工具裡，為二十到五十名真實使用者提供對話式答案。從第一天起就埋點：記錄每一個問題、每一個答案、每一次倒退、每一次轉人工。第11至13週用於決策：把紀錄與第1週設定的成功指標對照，然後明確地擴大試點、調整試點或終止試點。一個以書面決策收尾的試點，比一個不了了之的試點有價值得多。</p>
<table class="article-table">
<thead><tr><th>階段</th><th>交付物</th><th>准出標準</th></tr></thead>
<tbody>
<tr><td>第1-2週</td><td>帶具名負責人的能力排序清單</td><td>三個用例完成價值與可行性評分</td></tr>
<tr><td>第3-6週</td><td>已治理的指標定義與連接器</td><td>首選用例能基於生產資料給出正確答案</td></tr>
<tr><td>第7-10週</td><td>20-50名使用者、完整埋點的上線試點</td><td>問題紀錄、答案品質評分、轉人工率</td></tr>
<tr><td>第11-13週</td><td>書面的擴大／調整／終止決策</td><td>決策經預算負責人審查</td></tr>
</tbody>
</table>
<p>有兩個失敗模式會毀掉大多數會後計畫。第一個是先選模型而不是先選用例，結果產出一份漂亮的評估表格卻沒有任何使用者。第二個是跳過埋點，結果試點人人叫好卻沒人能論證該繼續投錢。兩者都靠同一套紀律來避免：在決定建什麼之前，先決定要衡量什麼。</p>
"""

H2FIX = {
    "EN": [("the-patterns-behind-the-headlines", "What Patterns Sit Behind the Headlines?")],
    "CN": [("常见问题解答", "企业最常提出的问题有哪些？")],
    "TW": [("常見問題解答", "企業最常提出的問題有哪些？")],
}


def run(lang, add):
    html = load(SLUG, lang)
    before = en_words(html) if lang == "EN" else cjk(html)
    html = fix_rec_hrefs(html)
    html = wrap_faq_h3(html)
    for hid, new in H2FIX[lang]:
        html, ok = set_h2_text(html, hid, new)
        if not ok:
            print("  !! h2 not found", lang, hid)
    if add:
        html = insert_before_faq(html, add)
    save(SLUG, lang, html)
    after = en_words(html) if lang == "EN" else cjk(html)
    return before, after


for lang, add in (("EN", EN_ADD), ("CN", CN_ADD), ("TW", TW_ADD)):
    b, a = run(lang, add)
    print(SLUG, lang, b, "->", a)
