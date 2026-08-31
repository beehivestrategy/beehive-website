import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "energy-efficiency-ai-manufacturing"

EN_ADD = """
<h2 id="which-subsystems-deliver-the-fastest-energy-savings">Which Subsystems Deliver the Fastest Energy Savings?</h2>
<p>Energy programmes stall when they start with the whole plant. Plants that produce results in a single quarter almost always start with one subsystem, chosen on two criteria: how much energy it consumes and how much of that consumption is pure waste rather than work. Compressed air is the classic example — a system that converts only a small fraction of input electricity into useful work, where the Department of Energy's industrial programmes have long documented leaks wasting 20 to 30 percent of compressor output in plants without disciplined maintenance. It is simultaneously one of the largest loads and one of the most wasteful, which is why it is usually the right first target.</p>
<p>The useful way to compare subsystems is to separate the physics from the behaviour. Physics sets the theoretical floor: a motor driving a pump cannot use less than the hydraulic work requires. Behaviour is everything above that floor — running when not needed, holding pressure higher than the process requires, heating a furnace longer than the soak time demands. AI earns its return almost entirely on behaviour, because behavioural waste is invisible in monthly utility bills and only becomes obvious when you model consumption against production, shift, and ambient conditions at interval resolution.</p>
<table class="article-table">
<thead><tr><th>Subsystem</th><th>Share of plant load</th><th>Typical waste driver</th><th>AI lever</th></tr></thead>
<tbody>
<tr><td>Compressed air</td><td>10-20%</td><td>Leaks, excessive pressure setpoints, off-hours running</td><td>Pressure optimisation, leak detection from flow signatures</td></tr>
<tr><td>Motor-driven systems</td><td>~70% of industrial electricity</td><td>Oversized motors, throttling instead of speed control</td><td>Load matching, variable-speed scheduling</td></tr>
<tr><td>Process heating and furnaces</td><td>15-30%</td><td>Drift from optimal temperature band, excess soak time</td><td>Setpoint correction, burner degradation detection</td></tr>
<tr><td>HVAC and plant services</td><td>5-15%</td><td>Conditioning unoccupied zones, simultaneous heating and cooling</td><td>Occupancy-linked scheduling, setpoint conflict detection</td></tr>
<tr><td>Lighting and auxiliary</td><td>2-8%</td><td>Fixed schedules decoupled from production calendar</td><td>Shift-aware scheduling</td></tr>
</tbody>
</table>
<p>One caution on the numbers: they are starting points for an audit, not guarantees. A plant that has already run a compressed-air leak programme will not find another 25 percent in the same place, and a plant whose meters only cover the building boundary cannot see any of this at all. The audit always precedes the model, and the audit is what tells you which row of the table actually applies to you.</p>
<h2 id="what-does-a-90-day-plant-pilot-look-like">What Does a 90-Day Plant Pilot Look Like?</h2>
<p>The pilot design that survives contact with a production schedule has three properties: it targets one subsystem, it produces a saving the plant manager can see within one billing cycle, and it never asks operations to change how they run the line before the evidence exists. Ninety days is enough for all three, and short enough that the plant does not lose patience.</p>
<p>Days one to thirty are metering and baselining. Install or activate interval sub-metering on the target subsystem, pull the historian data for machine state and production count, and build a baseline that relates energy to production rather than to time alone — energy per unit is the only normalisation that survives a change in output. Days thirty-one to sixty are modelling and detection. Fit the baseline, surface the deviations, and validate each one with a plant engineer before anyone acts on it; this validation step is what converts a statistical anomaly into a work order. Days sixty-one to ninety are intervention and verification: implement the top three fixes, hold production constant, and compare metered consumption against the baseline over a full billing period.</p>
<table class="article-table">
<thead><tr><th>Window</th><th>Activity</th><th>Exit criterion</th></tr></thead>
<tbody>
<tr><td>Days 1-30</td><td>Sub-metering, historian integration, energy-per-unit baseline</td><td>Baseline explains historical consumption within an agreed tolerance</td></tr>
<tr><td>Days 31-60</td><td>Deviation detection and engineer validation</td><td>Ranked list of verified waste sources with estimated value</td></tr>
<tr><td>Days 61-90</td><td>Top three interventions, metered verification</td><td>Measured reduction against baseline, signed off by plant manager</td></tr>
</tbody>
</table>
<p>The most common pilot failure is skipping the baseline and jumping to a dashboard. A screen showing consumption by day is interesting, but it does not tell a plant manager whether Tuesday was wasteful, because Tuesday might have produced twice as much. Energy per unit, verified against a metered billing period, is the only number that ends the argument — and once that number is trusted, expanding the programme to the next subsystem becomes a budget conversation rather than a debate.</p>
"""

CN_ADD = """
<h2 id="哪些子系统能最快带来能源节约">哪些子系统能最快带来能源节约？</h2>
<p>能源项目一上来就覆盖整个厂区，往往会停滞。能在一个季度内出成果的厂区，几乎总是从单个子系统起步，选择标准有两条：它消耗多少能源，以及其中有多少是纯粹浪费而非有效功。压缩空气就是典型例子——这套系统只把输入电力的一小部分转化为有用功，而美国能源部的工業計畫早已记录：在缺乏维护纪律的厂区，泄漏会浪费压缩机输出的 20% 到 30%。它同时是最大的负载之一、也是最浪费的系统之一，因此通常是最合适的首选目标。</p>
<p>比较各子系统的有效方法，是把物理规律与运行行为分开。物理决定了理论下限：驱动泵的电机不可能低于水力功所需。行为则是下限之上的一切——不需要时仍在运行、压力高于工艺所需、保温时间长于工艺要求。AI 的回报几乎全部来自行为层面，因为行为性浪费在月度水电费账单上是看不见的，只有当你以区间粒度把能耗对照产量、班次与环境条件建模时才会显现。</p>
<table class="article-table">
<thead><tr><th>子系统</th><th>占厂区负载比例</th><th>典型浪费来源</th><th>AI 切入点</th></tr></thead>
<tbody>
<tr><td>压缩空气</td><td>10-20%</td><td>泄漏、压力设定值过高、非生产时段运行</td><td>压力优化、基于流量特征的泄漏检测</td></tr>
<tr><td>电机驱动系统</td><td>约占工业用电 70%</td><td>电机选型过大、用节流代替调速</td><td>负载匹配、变频调度</td></tr>
<tr><td>工艺加热与熔炉</td><td>15-30%</td><td>偏离最优温度带、保温时间过长</td><td>设定值校正、燃烧器劣化检测</td></tr>
<tr><td>暖通空调与厂务设施</td><td>5-15%</td><td>调节无人区域、同时供热与供冷</td><td>基于在岗情况的调度、设定值冲突检测</td></tr>
<tr><td>照明与辅助设备</td><td>2-8%</td><td>固定时间表与生产日历脱节</td><td>按班次感知的调度</td></tr>
</tbody>
</table>
<p>关于这些数字有一点提醒：它们是审计的起点，而不是保证。已经做过压缩空气查漏项目的厂区，不可能在同一个地方再找出 25%；而计量只覆盖建筑边界的厂区，则根本看不到上述任何一项。审计永远先于建模，而审计正是告诉你表中哪一行真正适用于你的那一步。</p>
<h2 id="90天的厂区试点是什么样">90 天的厂区试点是什么样？</h2>
<p>能经受生产计划考验的试点设计有三个特征：只针对一个子系统、在一个计费周期内就产出厂长能看到的节约、并且在证据出现之前绝不要求运营改变产线运行方式。90 天足以做到这三点，也短到不至于让厂区失去耐心。</p>
<p>第 1 至 30 天用于计量与建立基线。在目标子系统上安装或启用区间分级计量，从历史库中提取设备状态与产量数据，并建立一条把能耗关联到产量而非仅关联到时间的基线——单位产品能耗是唯一能在产量变化时仍然成立的标准。第 31 至 60 天用于建模与检测。拟合基线、找出偏差，并在任何人据此行动之前，由厂区工程师逐条验证；正是这一步把一个统计异常转化为一张工单。第 61 至 90 天用于干预与验证：落实排名前三的整改措施，保持产量恒定，并在完整计费周期内把计量能耗与基线对比。</p>
<table class="article-table">
<thead><tr><th>时间窗</th><th>活动</th><th>准出标准</th></tr></thead>
<tbody>
<tr><td>第 1-30 天</td><td>分级计量、历史库集成、单位产品能耗基线</td><td>基线能在约定容差内解释历史能耗</td></tr>
<tr><td>第 31-60 天</td><td>偏差检测与工程师验证</td><td>带估值、经确认的浪费来源排序清单</td></tr>
<tr><td>第 61-90 天</td><td>落实前三项整改、计量验证</td><td>相对基线的实测下降，经厂长签字确认</td></tr>
</tbody>
</table>
<p>最常见的试点失败是跳过基线直接做仪表盘。一块按日显示能耗的屏幕很有意思，但它无法告诉厂长周二是否浪费了，因为周二的产量可能是平时的两倍。单位产品能耗——并经过一个完整计费周期的计量验证——是唯一能终结争论的数字；而一旦这个数字被信任，把项目扩展到下一个子系统就变成预算讨论，而不是一场辩论。</p>
"""

TW_ADD = """
<h2 id="哪些子系統能最快帶來能源節約">哪些子系統能最快帶來能源節約？</h2>
<p>能源專案一上來就涵蓋整個廠區，往往會停滯。能在一個季度內產出成果的廠區，幾乎總是從單一子系統起步，選擇標準有兩條：它消耗多少能源，以及其中有多少是純粹浪費而非有效功。壓縮空氣就是典型例子——這套系統只把輸入電力的一小部分轉化為有用功，而美國能源部的工業計畫早已記錄：在缺乏維護紀律的廠區，洩漏會浪費壓縮機輸出的 20% 到 30%。它同時是最大的負載之一、也是最浪費的系統之一，因此通常是最合適的首選目標。</p>
<p>比較各子系統的有效方法，是把物理規律與運行行為分開。物理決定了理論下限：驅動泵的馬達不可能低於水力功所需。行為則是下限之上的一切——不需要時仍在運轉、壓力高於製程所需、保溫時間長於製程要求。AI 的回報幾乎全部來自行為層面，因為行為性浪費在月度水電費帳單上看不見，只有當你以區間粒度把能耗對照產量、班次與環境條件建模時才會顯現。</p>
<table class="article-table">
<thead><tr><th>子系統</th><th>占廠區負載比例</th><th>典型浪費來源</th><th>AI 切入點</th></tr></thead>
<tbody>
<tr><td>壓縮空氣</td><td>10-20%</td><td>洩漏、壓力設定值過高、非生產時段運轉</td><td>壓力最佳化、以流量特徵進行的洩漏偵測</td></tr>
<tr><td>馬達驅動系統</td><td>約占工業用電 70%</td><td>馬達選型過大、以節流代替調速</td><td>負載匹配、變頻排程</td></tr>
<tr><td>製程加熱與熔爐</td><td>15-30%</td><td>偏離最佳溫度帶、保溫時間過長</td><td>設定值校正、燃燒器劣化偵測</td></tr>
<tr><td>空調與廠務設施</td><td>5-15%</td><td>調節無人區域、同時供熱與供冷</td><td>以在崗情況為基礎的排程、設定值衝突偵測</td></tr>
<tr><td>照明與輔助設備</td><td>2-8%</td><td>固定排程與生產日曆脫節</td><td>依班次感知的排程</td></tr>
</tbody>
</table>
<p>關於這些數字有一點提醒：它們是稽核的起點，而不是保證。已經做過壓縮空氣查漏專案的廠區，不可能在同一個地方再找出 25%；而計量只涵蓋建築邊界的廠區，則根本看不到上述任何一項。稽核永遠先於建模，而稽核正是告訴你表中哪一行真正適用於你的那一步。</p>
<h2 id="90天的廠區試點是什麼樣">90 天的廠區試點是什麼樣？</h2>
<p>能經受生產排程考驗的試點設計有三個特徵：只針對單一子系統、在一個計費週期內就產出廠長能看到的節約、並且在證據出現之前絕不要求營運改變產線運行方式。90 天足以做到這三點，也短到不至於讓廠區失去耐心。</p>
<p>第 1 至 30 天用於計量與建立基線。在目標子系統上安裝或啟用區間分級計量，從歷史資料庫中擷取設備狀態與產量資料，並建立一條把能耗關聯到產量而非僅關聯到時間的基線——單位產品能耗是唯一能在產量變化時仍然成立的標準。第 31 至 60 天用於建模與偵測。擬合基線、找出偏差，並在任何人據此行動之前，由廠區工程師逐條驗證；正是這一步把一個統計異常轉化為一張工單。第 61 至 90 天用於介入與驗證：落實排名前三的改善措施，維持產量恆定，並在完整計費週期內把計量能耗與基線對比。</p>
<table class="article-table">
<thead><tr><th>時間窗</th><th>活動</th><th>准出標準</th></tr></thead>
<tbody>
<tr><td>第 1-30 天</td><td>分級計量、歷史資料庫整合、單位產品能耗基線</td><td>基線能在約定容差內解釋歷史能耗</td></tr>
<tr><td>第 31-60 天</td><td>偏差偵測與工程師驗證</td><td>帶估值、經確認的浪費來源排序清單</td></tr>
<tr><td>第 61-90 天</td><td>落實前三項改善、計量驗證</td><td>相對基線的實測下降，經廠長簽核確認</td></tr>
</tbody>
</table>
<p>最常見的試點失敗是跳過基線直接做儀表板。一塊按日顯示能耗的螢幕很有意思，但它無法告訴廠長週二是否浪費了，因為週二的產量可能是平時的兩倍。單位產品能耗——並經過一個完整計費週期的計量驗證——是唯一能終結爭論的數字；而一旦這個數字被信任，把專案擴展到下一個子系統就變成預算討論，而不是一場辯論。</p>
"""

H2FIX = {
    "EN": [
        ("understanding-the-current-landscape", "What Does the Current Energy Landscape Look Like for Manufacturers?"),
        ("key-principles-and-strategic-framework", "What Are the Key Principles and the Strategic Framework?"),
        ("implementation-approach-and-best-practices", "What Implementation Approach and Best Practices Work?"),
        ("measuring-success-and-demonstrating-roi", "How Do You Measure Success and Demonstrate ROI?"),
        ("common-pitfalls-and-how-to-avoid-them", "What Are the Common Pitfalls and How Do You Avoid Them?"),
        ("key-takeaways", "What Are the Key Takeaways?"),
        ("conclusion", "What Should Manufacturers Conclude and Do Next?"),
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
        ("理解当前格局", "如何理解當前格局？"),
        ("关键原则与戰略框架", "關鍵原則與策略框架是什麼？"),
        ("實施方法与最佳實踐", "如何落實實施方法與最佳實踐？"),
        ("衡量成功与展示投資回報率", "如何衡量成功並展示投資回報率？"),
        ("常见陷阱及规避方法", "常見陷阱有哪些，應如何規避？"),
        ("關鍵要點", "關鍵要點有哪些？"),
        ("结论", "結論與下一步行動是什麼？"),
    ],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD, "CN": CN_ADD, "TW": TW_ADD}, tag=SLUG[:24])
