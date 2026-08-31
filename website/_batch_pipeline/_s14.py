import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "best-data-catalog-tools-governance-discovery-2026"

EN_ADD = """
<h2 id="what-does-an-ai-ready-catalog-need-that-a-traditional-one-does-not">What Does an AI-Ready Catalog Need That a Traditional One Does Not?</h2>
<p>A catalog built for humans and a catalog built for AI systems have different requirements, and the gap is wider than most buyers expect. A human searching for data can infer context from a column name, ask a colleague, and recognise when a result is wrong. An AI system can do none of those things: it consumes metadata literally, it cannot ask, and it will confidently use the wrong asset if the metadata permits it. That asymmetry turns several "nice to have" catalog features into hard requirements once agents and copilots are consumers.</p>
<p>The first requirement is machine-readable semantics. Business glossaries must be structured enough to be queried — each metric with one definition, one owner, and one approved source — because a retrieval system that finds three conflicting definitions of revenue will pick one and present it as fact. The second is lineage at column level with a programmatic API: when an answer is challenged, the system must be able to show which upstream fields produced it, and that trace has to be retrievable by a machine, not just rendered in a diagram. The third is enforcement rather than documentation: the catalog's classifications and policies must be honoured at query time, so an agent asking about a restricted field is refused rather than warned. The fourth is freshness metadata — an asset that has not been refreshed in six weeks should be marked stale, because a model cannot tell the difference between current and abandoned data.</p>
<table class="article-table">
<thead><tr><th>Capability</th><th>Traditional catalog emphasis</th><th>AI-ready requirement</th></tr></thead>
<tbody>
<tr><td>Business glossary</td><td>Human-readable definitions in a UI</td><td>Structured, queryable, one owner per term</td></tr>
<tr><td>Lineage</td><td>Visual, table-level</td><td>Column-level, retrievable via API</td></tr>
<tr><td>Access policy</td><td>Documented in the catalog</td><td>Enforced at query time for machine consumers</td></tr>
<tr><td>Freshness</td><td>Occasional quality score</td><td>Machine-readable staleness on every asset</td></tr>
<tr><td>Access pattern</td><td>Web UI and BI plugins</td><td>API and MCP server for programmatic retrieval</td></tr>
<tr><td>Certification</td><td>Steward review workflow</td><td>Certified-asset flag that retrieval systems can filter on</td></tr>
</tbody>
</table>
<p>The practical test when evaluating tools is to ask the vendor to demonstrate a machine consumer, not a human one: have an agent answer a business question using only the catalog's metadata, with lineage and certification enforced. Tools that pass this test will keep working as your AI surface expands; tools that only demo well in a browser will become the bottleneck the moment an assistant is pointed at them.</p>
<h2 id="what-does-a-catalog-implementation-actually-involve">What Does a Catalog Implementation Actually Involve?</h2>
<p>Catalog projects fail for a predictable reason: they are scoped as software installations and are really organisational change programmes. The tool is the easy part. The hard parts are agreeing who owns which data, populating the glossary with definitions people accept, and keeping it current after the implementation team disbands. Buyers who budget for the second half get a catalog that is used; buyers who budget only for licences and connectors get an empty one within a year.</p>
<p>A realistic implementation runs in four phases. Phase one is scoping and connection: choose two or three high-value domains rather than the entire estate, connect the sources that matter to them, and inventory what is already documented. Phase two is ownership and glossary: assign a named steward to every asset class in scope and agree the definitions of the top twenty business terms, which is where most of the political work sits. Phase three is automation: turn on automated harvesting, classification, and lineage so that coverage grows without manual effort, and add quality rules to the assets the business actually queries. Phase four is consumption: wire the catalog into BI tools, into search, and into the AI surface, and instrument which assets are being used and which are being ignored.</p>
<table class="article-table">
<thead><tr><th>Phase</th><th>Focus</th><th>Exit criterion</th></tr></thead>
<tbody>
<tr><td>1 — Scope and connect</td><td>Two or three high-value domains, source connections</td><td>Inventory of in-scope assets with owners identified</td></tr>
<tr><td>2 — Own and define</td><td>Named stewards, top twenty business terms agreed</td><td>Glossary signed off by the business, not just IT</td></tr>
<tr><td>3 — Automate</td><td>Harvesting, classification, lineage, quality rules</td><td>Coverage grows without manual curation</td></tr>
<tr><td>4 — Consume</td><td>BI, search, and AI integration with usage instrumentation</td><td>Measurable usage and a documented time saving</td></tr>
</tbody>
</table>
<h2 id="how-do-you-measure-catalog-return-on-investment">How Do You Measure Catalog Return on Investment?</h2>
<p>Catalog ROI is real but indirect, which is why it is so often asserted rather than measured. Three benefit pools are defensible and each can be instrumented. Analyst time saved is the most accessible: survey or instrument how long data professionals spend locating and validating an asset before and after, and multiply by the number of searches. Reduced duplication is the second: when teams can find an existing certified asset, they stop building their own copy, and the avoided cost is the compute plus the maintenance of that copy. Risk avoided is the third and the hardest to quantify, but it becomes concrete when a regulatory request or a data subject access request can be answered from lineage in hours rather than weeks.</p>
<table class="article-table">
<thead><tr><th>Benefit pool</th><th>How to measure it</th><th>Typical signal after 12 months</th></tr></thead>
<tbody>
<tr><td>Analyst time saved</td><td>Time to locate and validate an asset, before vs after</td><td>20-40% reduction in discovery time</td></tr>
<tr><td>Duplication avoided</td><td>Count of new copies of existing assets</td><td>Measurable decline in shadow extracts</td></tr>
<tr><td>Risk and compliance</td><td>Time to answer an access or lineage request</td><td>Weeks reduced to hours</td></tr>
<tr><td>AI accuracy</td><td>Share of AI answers sourced from certified assets</td><td>Higher trust and fewer corrections</td></tr>
<tr><td>Adoption</td><td>Monthly active searchers and repeat users</td><td>The leading indicator for all of the above</td></tr>
</tbody>
</table>
<p>Adoption deserves special attention because it is the only metric that predicts the others. A catalog with high coverage and low usage has failed, and the cause is almost always that the definitions were written by IT and do not match how the business talks. Measure monthly active searchers from month one, and if it is flat, fix the glossary before buying more connectors.</p>
"""

CN_ADD = """
<h2 id="面向AI就绪的目录需要什么">面向 AI 就绪的数据目录需要什么？</h2>
<p>为人构建的数据目录与为 AI 系统构建的数据目录，要求并不相同，而且这个差距比大多数采购者预期的更大。人类搜索数据时可以从列名推断上下文、向同事求助，并且能察觉结果是错的。AI 系统这三件事一件都做不到：它按字面理解元数据、无法发问，而且只要元数据允许，它会自信地使用错误的资产。一旦智能体与 Copilot 成为使用者，这种不对称就把好几个「锦上添花」的目录能力变成了硬性要求。</p>
<p>第一项要求是机器可读的语义。业务术语表必须具备可被查询的结构——每个指标只有一个定义、一位负责人、一个核准来源——因为如果一个检索系统找到三种互相冲突的收入定义，它会挑一个并当作事实呈现。第二项是具备编程接口的列级血缘：当答案受到质疑时，系统必须能展示是哪几个上游字段产生了它，而且这条追溯要能被机器读取，而不只是在图上画出来。第三项是执行而非记录：目录的分级与策略必须在查询时生效，使询问受限字段的智能体被拒绝，而不只是被提醒。第四项是新鲜度元数据——六周未刷新的资产应被标记为过期，因为模型无法区分当前数据与废弃数据。</p>
<table class="article-table">
<thead><tr><th>能力</th><th>传统目录的重点</th><th>面向 AI 就绪的要求</th></tr></thead>
<tbody>
<tr><td>业务术语表</td><td>界面上供人阅读的定义</td><td>结构化、可查询，每个术语一位负责人</td></tr>
<tr><td>血缘</td><td>可视化、表级</td><td>列级，可通过 API 取得</td></tr>
<tr><td>访问策略</td><td>记录在目录中</td><td>在查询时对机器使用者强制执行</td></tr>
<tr><td>新鲜度</td><td>偶发的质量评分</td><td>每个资产都带机器可读的过期标记</td></tr>
<tr><td>访问方式</td><td>网页界面与 BI 插件</td><td>面向程序化检索的 API 与 MCP 服务器</td></tr>
<tr><td>认证</td><td>数据管理员审核流程</td><td>可供检索系统筛选的已认证资产标记</td></tr>
</tbody>
</table>
<p>评估工具时最实用的检验，是要求厂商演示机器使用者而非人类使用者：让一个智能体仅凭目录的元数据回答一个业务问题，并强制执行血缘与认证。能通过这项检验的工具，会随着你的 AI 界面扩展而持续可用；只擅长在浏览器里演示的工具，一旦有助手接入就会立刻成为瓶颈。</p>
<h2 id="数据目录的实施究竟包含什么">数据目录的实施究竟包含什么？</h2>
<p>目录项目会失败，原因很可预测：它们被按软件安装来立项，而实际上是一场组织变革。工具是简单的部分；困难的部分是就「谁拥有哪些数据」达成一致、把术语表填上大家认可的定义，以及实施团队解散后仍能保持更新。愿意为后半段编列预算的买家会得到一个被使用的目录；只为授权与连接器编列预算的买家，会在一年内得到一个空目录。</p>
<p>务实的实施分为四个阶段。第一阶段是范围与连接：选择两到三个高价值域而不是整个数据资产，连接与之相关的源系统，并盘点已有的文档。第二阶段是归属与术语：为范围内的每一类资产指定具名的数据管理员，并就前二十个业务术语达成一致——大部分政治性工作就在这一步。第三阶段是自动化：开启自动采集、分类与血缘，使覆盖率在无需人工投入的情况下增长，并对业务真正查询的资产添加质量规则。第四阶段是消费：把目录接入 BI 工具、搜索与 AI 界面，并埋点统计哪些资产被使用、哪些被忽略。</p>
<table class="article-table">
<thead><tr><th>阶段</th><th>重点</th><th>准出标准</th></tr></thead>
<tbody>
<tr><td>1 — 范围与连接</td><td>两到三个高价值域、源系统连接</td><td>范围内资产盘点完成，负责人已确认</td></tr>
<tr><td>2 — 归属与定义</td><td>具名管理员、前二十个业务术语达成一致</td><td>术语表由业务方而非仅 IT 签署确认</td></tr>
<tr><td>3 — 自动化</td><td>采集、分类、血缘、质量规则</td><td>覆盖率在无需人工整理的情况下增长</td></tr>
<tr><td>4 — 消费</td><td>接入 BI、搜索与 AI，并埋点统计使用情况</td><td>使用量可衡量，时间节省有据可查</td></tr>
</tbody>
</table>
<h2 id="如何衡量数据目录的投资回报">如何衡量数据目录的投资回报？</h2>
<p>目录的投资回报是真实的但也是间接的，这正是它常被断言而不被衡量的原因。有三个收益池是可以论证、也都可以埋点度量的。分析师节省的时间最容易衡量：调查或埋点统计专业人员在上线与之前定位并验证一个资产所需的时间，再乘以检索次数。减少重复建设是第二个：当团队能找到已有的已认证资产，就不会再造一份自己的副本，而避免的成本就是该副本的计算与维护开销。规避风险是第三个、也最难量化，但当一项监管质询或数据主体访问请求能从血缘出发在数小时而非数周内完成时，它就变得具体了。</p>
<table class="article-table">
<thead><tr><th>收益池</th><th>如何度量</th><th>12 个月后的典型信号</th></tr></thead>
<tbody>
<tr><td>分析师时间节省</td><td>上线前后定位并验证资产所需时间</td><td>发现时间减少 20-40%</td></tr>
<tr><td>避免重复建设</td><td>既有资产的新增副本数量</td><td>影子抽取显著减少</td></tr>
<tr><td>风险与合规</td><td>响应访问或血缘请求的时间</td><td>从数周缩短到数小时</td></tr>
<tr><td>AI 准确性</td><td>来自已认证资产的答案占比</td><td>信任度提升、修正次数减少</td></tr>
<tr><td>采用度</td><td>月活跃检索者与重复使用人数</td><td>以上各项的先行指标</td></tr>
</tbody>
</table>
<p>采用度值得特别关注，因为它是唯一能预测其他各项的指标。覆盖率高但使用率低的目录就是失败了，而原因几乎总是定义由 IT 撰写、与业务的说法不一致。从第一个月起就度量月活跃检索者；如果数字持平，先修好术语表，再考虑购买更多连接器。</p>
"""

TW_ADD = """
<h2 id="面向AI就緒的目錄需要什麼">面向 AI 就緒的數據目錄需要什麼？</h2>
<p>為人建置的數據目錄與為 AI 系統建置的數據目錄，要求並不相同，而這個差距比大多數採購者預期的更大。人類搜尋資料時可以從欄位名稱推斷上下文、向同事求助，並且能察覺結果是錯的。AI 系統這三件事一件都做不到：它按字面理解中繼資料、無法發問，而且只要中繼資料允許，它會自信地使用錯誤的資產。一旦智慧代理與 Copilot 成為使用者，這種不對稱就把好幾個「錦上添花」的目錄能力變成硬性要求。</p>
<p>第一項要求是機器可讀的語意。業務術語表必須具備可被查詢的結構——每個指標只有一個定義、一位負責人、一個核准來源——因為如果一個檢索系統找到三種互相衝突的營收定義，它會挑一個並當作事實呈現。第二項是具備程式介面的欄位層級血緣：當答案受到質疑時，系統必須能展示是哪幾個上游欄位產生了它，而且這條追溯要能被機器讀取，而不只是在圖上畫出來。第三項是執行而非記錄：目錄的分級與政策必須在查詢時生效，使詢問受限欄位的智慧代理被拒絕，而不只是被提醒。第四項是新鮮度中繼資料——六週未更新的資產應被標記為過期，因為模型無法區分目前資料與廢棄資料。</p>
<table class="article-table">
<thead><tr><th>能力</th><th>傳統目錄的重點</th><th>面向 AI 就緒的要求</th></tr></thead>
<tbody>
<tr><td>業務術語表</td><td>介面上供人閱讀的定義</td><td>結構化、可查詢，每個術語一位負責人</td></tr>
<tr><td>血緣</td><td>視覺化、表層級</td><td>欄位層級，可透過 API 取得</td></tr>
<tr><td>存取政策</td><td>記錄在目錄中</td><td>在查詢時對機器使用者強制執行</td></tr>
<tr><td>新鮮度</td><td>偶發的品質評分</td><td>每個資產都帶機器可讀的過期標記</td></tr>
<tr><td>存取方式</td><td>網頁介面與 BI 外掛</td><td>面向程式化檢索的 API 與 MCP 伺服器</td></tr>
<tr><td>認證</td><td>資料管理員審核流程</td><td>可供檢索系統篩選的已認證資產標記</td></tr>
</tbody>
</table>
<p>評估工具時最實用的檢驗，是要求供應商展示機器使用者而非人類使用者：讓一個智慧代理僅憑目錄的中繼資料回答一個業務問題，並強制執行血緣與認證。能通過這項檢驗的工具，會隨著你的 AI 介面擴充而持續可用；只擅長在瀏覽器中展示的工具，一旦有助理接入就會立刻成為瓶頸。</p>
<h2 id="數據目錄的實施究竟包含什麼">數據目錄的實施究竟包含什麼？</h2>
<p>目錄專案會失敗，原因很可預測：它們被按軟體安裝來立案，而實際上是一場組織變革。工具是簡單的部分；困難的部分是就「誰擁有哪些資料」達成共識、把術語表填上大家認可的定義，以及實施團隊解散後仍能維持更新。願意為後半段編列預算的買家會得到一個被使用的目錄；只為授權與連接器編列預算的買家，會在一年內得到一個空目錄。</p>
<p>務實的實施分為四個階段。第一階段是範圍與連接：選擇兩到三個高價值領域而不是整個資料資產，連接與之相關的來源系統，並盤點既有文件。第二階段是歸屬與術語：為範圍內的每一類資產指定具名的資料管理員，並就前二十個業務術語達成共識——大部分政治性工作就在這一步。第三階段是自動化：開啟自動採集、分類與血緣，使覆蓋率在無須人工投入的情況下成長，並對業務真正查詢的資產加入品質規則。第四階段是使用：把目錄接入 BI 工具、搜尋與 AI 介面，並埋點統計哪些資產被使用、哪些被忽略。</p>
<table class="article-table">
<thead><tr><th>階段</th><th>重點</th><th>准出標準</th></tr></thead>
<tbody>
<tr><td>1 — 範圍與連接</td><td>兩到三個高價值領域、來源系統連接</td><td>範圍內資產盤點完成，負責人已確認</td></tr>
<tr><td>2 — 歸屬與定義</td><td>具名管理員、前二十個業務術語達成共識</td><td>術語表由業務方而非僅 IT 簽署確認</td></tr>
<tr><td>3 — 自動化</td><td>採集、分類、血緣、品質規則</td><td>覆蓋率在無須人工整理的情況下成長</td></tr>
<tr><td>4 — 使用</td><td>接入 BI、搜尋與 AI，並埋點統計使用情況</td><td>使用量可衡量，時間節省有據可查</td></tr>
</tbody>
</table>
<h2 id="如何衡量數據目錄的投資回報">如何衡量數據目錄的投資回報？</h2>
<p>目錄的投資回報是真實的但也是間接的，這正是它常被斷言而不被衡量的原因。有三個收益池是可以論證、也都可以埋點衡量的。分析師節省的時間最容易衡量：調查或埋點統計專業人員在上線前後定位並驗證一個資產所需的時間，再乘以檢索次數。減少重複建置是第二個：當團隊能找到既有的已認證資產，就不會再造一份自己的副本，而避免的成本就是該副本的運算與維護開銷。規避風險是第三個、也最難量化，但當一項監理質詢或資料主體存取請求能從血緣出發在數小時而非數週內完成時，它就變得具體了。</p>
<table class="article-table">
<thead><tr><th>收益池</th><th>如何衡量</th><th>12 個月後的典型訊號</th></tr></thead>
<tbody>
<tr><td>分析師時間節省</td><td>上線前後定位並驗證資產所需時間</td><td>發現時間減少 20-40%</td></tr>
<tr><td>避免重複建置</td><td>既有資產的新增副本數量</td><td>影子抽取顯著減少</td></tr>
<tr><td>風險與合規</td><td>回應存取或血緣請求的時間</td><td>從數週縮短到數小時</td></tr>
<tr><td>AI 準確性</td><td>來自已認證資產的答案占比</td><td>信任度提升、修正次數減少</td></tr>
<tr><td>採用度</td><td>每月活躍檢索者與重複使用人數</td><td>以上各項的先行指標</td></tr>
</tbody>
</table>
<p>採用度值得特別關注，因為它是唯一能預測其他各項的指標。覆蓋率高但使用率低的目錄就是失敗了，而原因幾乎總是定義由 IT 撰寫、與業務的說法不一致。從第一個月起就衡量每月活躍檢索者；如果數字持平，先修好術語表，再考慮購買更多連接器。</p>
"""

H2FIX = {
    "EN": [
        ("the-modern-data-catalog", "What Is the Modern Data Catalog?"),
        ("ranking-the-8-best-data-catalog-tools", "What Are the 8 Best Data Catalog Tools Ranked?"),
        ("selection-by-priority", "How Should You Select a Catalog by Priority?"),
    ],
    "CN": [
        ("现代-data-catalog", "现代 Data Catalog 是什么？"),
        ("ranking-the-8-best-data-catalog-tools", "八大最佳数据目录工具如何排名？"),
        ("按-选择-priority", "如何按优先级选择数据目录？"),
    ],
    "TW": [
        ("現代-data-catalog", "現代 Data Catalog 是什麼？"),
        ("ranking-the-8-best-data-catalog-tools", "八大最佳數據目錄工具如何排名？"),
        ("按-選擇-priority", "如何按優先順序選擇數據目錄？"),
    ],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD, "CN": CN_ADD, "TW": TW_ADD},
        cta_fix={"TW": ('<a href="/zh-tw/contact" class="article-cta-btn">預約演示</a>',
                        '<a href="/zh-tw/contact" class="article-cta-btn">預約示範</a>')},
        tag=SLUG[:24])
