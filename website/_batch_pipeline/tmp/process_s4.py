# -*- coding: utf-8 -*-
"""Slug 4: business-case-real-time-analytics-logistics — EN expand, zh H2/FAQ/TOC/lead fixes."""
import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/tmp")
from common import (load, save, rep1, re_dl, build_faq_list, build_jsonld,
                    body_h1, fill_excerpts, integrity, FAQ_RX, JSONLD_RX)

W = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/"
EN = W + "blog/articles/business-case-real-time-analytics-logistics.html"
ZHCN = W + "zh-cn/blog/articles/business-case-real-time-analytics-logistics.html"
ZHTW = W + "zh-tw/blog/articles/business-case-real-time-analytics-logistics.html"

# ---------------- EN ----------------
EN_FAQ = [
    ("How much does stale information actually cost a logistics operation?",
     "The cost shows up in four places: expedited freight to recover shipments discovered late, service-level penalties and credits on missed windows, cold-chain losses found after the product is already compromised, and the customer-retention impact of reactive communication. Because the gap between an event and its visibility is where those costs are incurred, closing it with real-time analytics targets the largest avoidable cost pools in logistics rather than marginal overhead."),
    ("What data sources does real-time logistics analytics need to connect?",
     "The core sources are your transportation management system (TMS), warehouse management system (WMS), and ERP, plus live feeds: GPS and telematics from vehicles, scanning events and IoT sensors from warehouses, and external feeds such as weather, traffic, and port status. Governed connectors in the MCP style link these systems without rebuilding your data estate, and a semantic layer keeps metrics like on-time delivery consistently defined across every customer and service tier."),
    ("How quickly can real-time analytics be deployed, and do we need to rebuild our data warehouse?",
     "A managed conversational BI service typically deploys in about two weeks against the warehouse and operational systems you already run — the connectors, semantic layer, and governance are operated for you. An in-house real-time platform, by contrast, is a multi-quarter engineering project. Starting with a managed service lets you capture exception-management ROI in the first 90 days before deciding how much to build internally."),
    ("How does conversational BI work for dispatchers and warehouse teams in practice?",
     "Operations staff ask questions in natural language, usually inside the chat and IM tools they already use — for example, \u201cwhich shipments are at risk of missing their window today?\u201d — and receive a prioritized list with risk factors and recommended actions. When a delay, route deviation, or temperature excursion is detected, the alert reaches the right team immediately, so response happens in minutes instead of at the end-of-day report."),
]

EN_NEW1 = '''<h2 id="how-does-real-time-analytics-change-daily-decisions">How Does Real-Time Analytics Change Daily Decisions on the Ground?</h2>
<p>The clearest way to see the value is to compare the same morning with and without real-time visibility. In the batch world, a dispatcher starts the day reviewing yesterday's exception report, calls carriers about shipments that went sideways twelve hours ago, and spends the first hours reconstructing what already happened. In the real-time world, the same dispatcher opens the chat window and asks which shipments are at risk today — and gets a ranked list with reasons: a border crossing is congested, a container's temperature is trending upward, a dock at the destination warehouse is running behind. The conversation shifts from archaeology to allocation: where to spend attention before problems become losses.</p>
<p>Warehouse managers see a parallel shift. Instead of discovering at shift-end that a packing station became a bottleneck at 10 a.m., they get notified when queue depth crosses the threshold, in time to rebalance staff while the shift is still recoverable. Because conversational BI delivers answers in the IM tools operations teams already use, adoption does not depend on anyone learning a new dashboard — the analytics arrive where the decisions are already being made. That is the practical difference real-time analytics makes: not better charts, but better-timed decisions by the people closest to the freight.</p>'''

EN_NEW2 = '''<h2 id="which-metrics-prove-real-time-analytics-roi">Which Metrics Prove the ROI of Real-Time Logistics Analytics?</h2>
<p>Measurement discipline starts with a baseline taken before deployment. The metrics that move first are operational: exception detection time (minutes from event to awareness), expedite spend per period, cold-chain loss rate per container, and the percentage of delayed shipments where an alternative routing was still viable when the delay was caught. These are the direct expressions of the visibility gap, and they typically improve within the first quarter as exception handling goes real time.</p>
<p>The second tier of metrics captures business outcomes: on-time delivery percentage by customer and service tier, cost per shipment, penalty and credit totals, and customer-retention figures on affected lanes. One caution matters here — definitions must live in the semantic layer, not in each team's spreadsheet. If "on-time" means one thing to sales and another to operations, the ROI conversation collapses into a debate about numbers. Teams that hold the line on shared definitions can usually demonstrate payback within the first two quarters, because the metrics being compared before and after are genuinely the same metrics.</p>'''

EN_PARA_A = '''<p>One architectural decision deserves special attention: event freshness versus context depth. A pure streaming pipeline is fast but context-poor — it knows a container's temperature rose, but not that this particular customer carries a penalty clause at 97% on-time. The value comes from joining the live event against master data, contracts, and customer history in the TMS and ERP, which is exactly what the connector layer exists for. When evaluating vendors, test this join explicitly: ask the system why a shipment is at risk and check whether the answer cites the business consequence or merely repeats the sensor reading.</p>'''

EN_PARA_B = '''<p>Beyond the big three, two quieter use cases repay the investment. Customs and compliance monitoring turns clearance delays from surprises into managed events, with documents chased the moment a status stalls. And customer-facing operations teams use the same live data proactively: telling a customer their shipment will be late — with the recovery plan — before the customer discovers it themselves converts a service failure into a retention moment. Neither use case needs new infrastructure; both reuse the same real-time stream and semantic definitions the primary use cases established.</p>'''

def process_en():
    s = load(EN)
    h1 = body_h1(s)
    assert "Real-Time Analytics" in h1 and "Logistics" in h1, "wrong file? h1=" + h1
    if 'how-does-real-time-analytics-change-daily-decisions' in s:
        print("EN already processed, skip")
        return
    # 1) H2 question-form conversions (keep ids)
    s = rep1(s, '<h2 id="the-cost-of-batch-analytics-in-logistics">The Cost of Batch Analytics in Logistics</h2>',
             '<h2 id="the-cost-of-batch-analytics-in-logistics">What Does Batch Analytics Really Cost Logistics Operations?</h2>', 'h2-1')
    s = rep1(s, '<h2 id="real-time-analytics-architecture-for-logistics">Real-Time Analytics Architecture for Logistics</h2>',
             '<h2 id="real-time-analytics-architecture-for-logistics">What Does a Real-Time Analytics Architecture for Logistics Look Like?</h2>', 'h2-2')
    s = rep1(s, '<h2 id="high-value-use-cases">High-Value Use Cases</h2>',
             '<h2 id="high-value-use-cases">Which Logistics Use Cases Deliver the Highest Real-Time ROI?</h2>', 'h2-3')
    s = rep1(s, '<h2 id="building-the-business-case">Building the Business Case</h2>',
             '<h2 id="building-the-business-case">How Do You Build the Business Case for Real-Time Logistics Analytics?</h2>', 'h2-4')
    # 2) extra paragraphs in existing sections
    s = rep1(s, 'reserved for data scientists.</p>',
             'reserved for data scientists.</p>\n' + EN_PARA_A, 'paraA')
    s = rep1(s, 'expediting, empty miles, labor, and lost customer value.</p>',
             'expediting, empty miles, labor, and lost customer value.</p>\n' + EN_PARA_B, 'paraB')
    # 3) two new sections before pay-back section
    anchor_c = '<h2 id="how-fast-does-real-time-analytics-pay-back">'
    s = rep1(s, anchor_c, EN_NEW1 + "\n" + EN_NEW2 + "\n" + anchor_c, 'new-sections')
    # 4) remove head FAQPage (tempered regex)
    s = re_dl(s, JSONLD_RX, '', 'head-faqpage-remove')
    # 5) replace FAQ list with topic Q&A (h3-wrapped)
    new_faq = '<div class="faq-list">\n' + build_faq_list(EN_FAQ) + '\n                </div>\n            </section>'
    s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'faq-list')
    # 6) place matching JSON-LD right after FAQ section
    old_nav = '</section>\n\n            <nav class="article-nav"'
    assert s.count(old_nav) == 1
    s = s.replace(old_nav, '</section>\n' + build_jsonld(EN_FAQ) + '\n\n            <nav class="article-nav"')
    # 7) TOC sync (mobile only — no sidebar in this template)
    toc_entries = [
        ("the-cost-of-batch-analytics-in-logistics", "What Does Batch Analytics Really Cost Logistics Operations?"),
        ("real-time-analytics-architecture-for-logistics", "What Does a Real-Time Analytics Architecture for Logistics Look Like?"),
        ("high-value-use-cases", "Which Logistics Use Cases Deliver the Highest Real-Time ROI?"),
        ("building-the-business-case", "How Do You Build the Business Case for Real-Time Logistics Analytics?"),
        ("how-does-real-time-analytics-change-daily-decisions", "How Does Real-Time Analytics Change Daily Decisions on the Ground?"),
        ("which-metrics-prove-real-time-analytics-roi", "Which Metrics Prove the ROI of Real-Time Logistics Analytics?"),
        ("how-fast-does-real-time-analytics-pay-back", "How Fast Does Real-Time Analytics Pay Back?"),
        ("what-should-logistics-leaders-do-first", "What Should Logistics Leaders Do First?"),
    ]
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in toc_entries)
    s = re_dl(s, r'<div class="toc-mobile-links">.*?</div>', '<div class="toc-mobile-links">\n' + mob + '\n                </div>', 'toc-mobile')
    # 8) excerpts
    s = fill_excerpts(s, [
        "Why diverse data teams catch the blind spots that homogeneous teams miss, and how to build inclusion into AI hiring.",
        "Why the AI agent layer is becoming the missing piece of modern data strategy — and how to position it for 2026.",
        "A practical 2026 guide to vector databases and enterprise semantic search.",
    ], "EN-excerpt")
    # integrity BEFORE save
    integrity(s, [
        '?v=20260901', '"@type": "BlogPosting"', '"@type": "BreadcrumbList"',
        'id="how-does-real-time-analytics-change-daily-decisions"',
        'id="which-metrics-prove-real-time-analytics-roi"',
        '"@type": "FAQPage"', 'Book a Demo',
        '<h1 class="article-h1">The Business Case for Real-Time Analytics in Logistics</h1>',
    ], 8, "EN")
    assert s[:s.index('</head>')].count('FAQPage') == 0, "head FAQPage still present"
    save(EN, s)
    print("EN done")

# ---------------- zh-CN ----------------
CN_FAQ = [
    ("物流企业为什么需要实时分析，而不是继续依赖批量报表？",
     "批量报表的问题是滞后：货件在边境延误的时刻最值钱——那是备选路线还能保住交付窗口的唯一时刻，而日末报告发现问题时的补救成本已经产生。实时分析把异常发现时间从小时级压缩到分钟级，直接减少加急运费、违约金和冷链损失这些物流最大的可避免成本池。"),
    ("实时物流分析需要接入哪些数据源？",
     "核心是TMS（运输管理）、WMS（仓储管理）和ERP系统，加上实时数据流：车辆GPS与远程信息处理、仓库扫描事件和IoT传感器，以及天气、路况、港口状态等外部数据。MCP风格的受管连接器可以在不重建数据架构的前提下接入这些系统，语义层则确保准时率等指标对所有客户和服务等级定义一致。"),
    ("部署实时分析需要多久？需要重建数据仓库吗？",
     "托管式对话BI服务通常约两周即可在物流企业现有的仓库和业务系统上部署，连接器、语义层和治理均由服务商运营。自建实时平台则是需要专职工程团队的跨季度项目。先以托管服务捕获异常管理的首季度ROI，再决定内部建设的深度，是回报最快的路径。"),
    ("对话式BI在物流运营中如何实际使用？",
     "运营人员在常用的聊天和IM工具中用自然语言提问，例如\u201c今天哪些货件有延误风险？\u201d，即可获得按优先级排序的清单，附带风险因素和建议动作。当检测到延误、偏航或温度异常时，告警立即触达相应团队——响应以分钟计，而不是等到日末报告。"),
]

CN_H2 = [
    ('当前格局与关键趋势', '为什么实时分析正在重塑物流行业的竞争格局？'),
    ('实施框架与最佳实践', '如何搭建物流实时分析的实施框架？'),
    ('衡量影响与展示价值', '如何衡量物流实时分析的业务影响？'),
    ('克服常见挑战', '物流实时分析落地的常见挑战如何克服？'),
    ('从试点到规模化生产的路径', '如何从试点走向规模化生产？'),
    ('技术基础设施与实施考量', '物流实时分析需要怎样的技术基础设施？'),
]

def process_cn():
    s = load(ZHCN)
    h1 = body_h1(s)
    assert '物流' in h1 and '实时分析' in h1, "wrong file? h1=" + h1
    changed = False
    for old, new in CN_H2:
        if f'>{new}</h2>' not in s:
            s = rep1(s, f'>{old}</h2>', f'>{new}</h2>', 'cn-h2-' + old)
            changed = True
    toc_entries = [(o, n) for o, n in CN_H2]
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{n}</a>' for o, n in toc_entries)
    if changed or 'toc-mobile-link">为什么实时分析' not in s:
        def mob_repl(m):
            return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
        s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
        assert s2 != s or mob in s, "cn toc-mobile replace failed"
        s = s2
    if '物流企业为什么需要实时分析' not in s:
        new_faq = '<div class="faq-list">\n' + build_faq_list(CN_FAQ) + '\n                </div>\n            </section>'
        s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'cn-faq')
        s = re_dl(s, JSONLD_RX, build_jsonld(CN_FAQ).replace('\\', '\\\\'), 'cn-jsonld')
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "数据质量自动化让数据治理从被动补救转向主动预防。",
        ], "CN-excerpt")
    integrity(s, [
        '?v=20260901', '预约演示', '"@type": "FAQPage"',
        '为什么实时分析正在重塑物流行业的竞争格局', '如何搭建物流实时分析的实施框架',
        'id="技术基础设施与实施考量"',
    ], 8, "zh-CN")
    assert s[:s.index('</head>')].count('FAQPage') == 0, "cn head FAQPage present"
    save(ZHCN, s)
    print("zh-CN done")

# ---------------- zh-TW ----------------
TW_FAQ = [
    ("物流企業為什麼需要即時分析，而不是繼續依賴批量報表？",
     "批量報表的問題是滯後：貨件在邊境延誤的時刻最值錢——那是備選路線還能保住交付窗口的唯一時刻，而日末報告發現問題時的補救成本已經產生。即時分析把異常發現時間從小時級壓縮到分鐘級，直接減少加急運費、違約金和冷鏈損失這些物流最大的可避免成本池。"),
    ("即時物流分析需要接入哪些資料來源？",
     "核心是TMS（運輸管理）、WMS（倉儲管理）和ERP系統，加上即時資料流：車輛GPS與遠程資訊處理、倉庫掃描事件和IoT感測器，以及天氣、路況、港口狀態等外部資料。MCP風格的受管連接器可以在不重建資料架構的前提下接入這些系統，語義層則確保準時率等指標對所有客戶和服務等級定義一致。"),
    ("部署即時分析需要多久？需要重建資料倉儲嗎？",
     "託管式對話BI服務通常約兩週即可在物流企業現有的倉儲和業務系統上部署，連接器、語義層和治理均由服務商營運。自建即時平臺則是需要專職工程團隊的跨季度專案。先以託管服務捕獲異常管理的首季度ROI，再決定內部建設的深度，是回報最快的路徑。"),
    ("對話式BI在物流營運中如何實際使用？",
     "營運人員在常用的聊天和IM工具中用自然語言提問，例如「今天哪些貨件有延誤風險？」，即可獲得按優先級排序的清單，附帶風險因素和建議動作。當偵測到延誤、偏航或溫度異常時，警報立即觸達相應團隊——回應以分鐘計，而不是等到日末報告。"),
]

TW_H2 = [
    ('real-time-analytics-architecture-for-logistics', '物流即時分析需要怎樣的技術架構？'),
    ('high-value-use-cases', '哪些物流用例的即時分析投資回報最高？'),
    ('building-the-business-case', '如何構建物流即時分析的商業論證？'),
    ('規模化推廣的關鍵成功因素', '如何從試點走向規模化推廣？'),
    ('技術基礎設施與實施考量', '物流即時分析需要怎樣的技術基礎設施？'),
    ('中國市場特有的實施優勢', '為什麼中國物流企業能更快實現即時分析的價值？'),
    ('規模化推廣的關鍵成功因素-2', '如何保障即時分析平臺的長期成功？'),
]

TW_LEAD_OLD = 'MCP（模型上下文協議）正在改變企業AI系統訪問資料的方式。與傳統的REST API或GraphQL不同，MCP為AI模型提供了標準化的上下文感知資料訪問，使AI智慧體能夠理解資料的業務含義、安全約束和訪問權限。這種能力使AI系統能夠更準確地回答業務問題，同時自動遵守資料安全和合規要求。MCP正在成為企業AI資料訪問的事實標準，其價值在於創建了一次構建、多次複用的整合資產，為平台化AI部署提供了基礎。'
TW_LEAD_NEW = '物流行業每小時都在產生資料——車輛GPS、倉庫掃描、冷鏈溫度、通關狀態——但大多數物流分析仍依賴滯後數小時甚至數天的批量快照，問題在盲區中醞釀，決策建立在過期數字上。即時分析透過對話式BI把物流從被動響應轉為主動優化：異常在發生當下被發現，路線在狀況變化時被調整，倉儲瓶頸在影響出貨前被紓解。基於行業基準的ROI測算顯示，這筆投資通常在一年以內收回。'
TW_PARA1_NEW = '物流即時分析的技術架構分為四層。邊緣層從車輛（GPS、車聯網）、倉庫（掃描設備、IoT感測器）和外部資料源（天氣、路況、港口狀態）持續採集事件。串流層對事件即時處理、富化和分流。連接器層——以MCP的精神標準化——讓分析引擎以受治理的方式訪問TMS、WMS、ERP和CRM等記錄系統，使即時訊號能結合完整業務語境被解讀。頂層是價值實現所在：AI模型在即時資料流上運行路線優化、貨件風險預測、倉儲瓶頸偵測和需求預測，並以對話式BI介面交付——物流經理問「今天哪些貨件有延誤風險」，得到的是帶風險因素和建議動作的優先級清單。'
TW_TLDR_OLD = '行業研究表明，在The Business Case for Real-Time Analytics in Logistics | 蜂啟諮詢|The Cost of Batch Analytics in Logistics領域進行策略性投資的企業比延遲採用的組織價值實現速度快35%，投資回報率高28%，基於2026年企業基準資料。採用MCP標準化資料訪問和語義層治理的組織，平均部署時間縮短40%。'
TW_TLDR_NEW = '麥肯錫研究顯示，進階分析可將物流預測誤差降低30-50%、總物流成本降低多達15%。即時分析結合對話式BI，讓異常發現時間從小時級壓縮到分鐘級，直接削減加急運費、違約金和冷鏈損失。'

TW_CN_PARA1_OLD = '在2026年的商業環境中，企業AI正從實驗性試點轉向生產級部署，各行業的組織正加速採用AI驅動的解決方案，這是由基礎技術的成熟和日益增強的競爭壓力所推動的。大語言模型、MCP等標準化資料訪問協議以及不斷增長的監管要求的融合，正在創造一個策略性強、執行良好的實施能將市場領導者與落後者區分開來的格局。企業AI的成功不再取決於單一技術的突破，而是取決於正確的基礎設施、治理框架和組織能力的系統性建設。那些能夠在資料質量、治理合規和用戶體驗之間取得平衡的企業，正在從AI投資中捕獲不成比例的價值。'
TW_CN_PARA1_NEW = '中國物流企業在即時分析落地上有三個結構性優勢。第一，IM原生部署渠道：企業微信、釘釘和飛書的普及意味著對話式BI可以直接嵌入運營團隊每天都在用的工具，無需推廣新介面，採用阻力遠低於西方同行。第二，基礎設施跳代：許多物流企業直接從分散的系統躍入雲原生資料平臺，沒有沉重遺留倉儲的遷移負擔，MCP風格連接器接入TMS、WMS和ERP的速度更快。第三，規模效應：單一區域市場、高密度的配送網絡和統一的監管環境，使即時資料流的邊際成本低於跨國多司法管轄區的運營。'
TW_CN_PARA2_OLD = '2026年的企業AI格局正在經歷深刻變革。隨著大語言模型能力的持續提升和MCP（模型上下文協議）等標準化資料訪問框架的成熟，企業AI正從概念驗證階段邁向規模化生產部署。然而，成功的關鍵不僅在於選擇正確的AI技術，更在於構建正確的資料基礎設施和治理框架。那些能夠在資料質量、治理合規和用戶體驗之間取得平衡的企業，正在從AI投資中捕獲不成比例的價值，而那些忽視這些基礎工作的企業則繼續在試點和生產之間反覆循環。'
TW_CN_PARA2_NEW = '實踐中的路徑也印證了這些優勢。領先的物流企業通常從貨物追蹤和異常管理起步——這是即時可見性回報最快的場景——在獲得首批ROI證明後，再擴展到動態路線優化和倉儲吞吐優化。語義層在其中承擔關鍵角色：物流術語的口徑分歧（不同客戶、不同運輸方式對「準時送達」的定義不同）在語義層被統一編碼，AI答案才能跨場景保持一致。對中國物流企業而言，真正的競爭優勢不在於更早採用AI，而在於更短的「從資料到行動」鏈路——異常發現得早，決策做得快，客戶承諾守得住。'

def process_tw():
    s = load(ZHTW)
    h1 = body_h1(s)
    assert '物流' in h1 and '即時分析' in h1, "wrong file? h1=" + h1
    if '物流即時分析需要怎樣的技術架構' in s:
        print("TW already processed, skip")
        return
    # 0) junk lead appears twice: article-lead + first section paragraph
    n = s.count(TW_LEAD_OLD)
    assert n == 2, f"[tw-lead] expected 2 occurrences, got {n}"
    s = s.replace(TW_LEAD_OLD, TW_LEAD_NEW, 1)
    s = rep1(s, TW_LEAD_OLD, TW_PARA1_NEW, 'tw-para1')
    # tldr junk title text
    s = rep1(s, TW_TLDR_OLD, TW_TLDR_NEW, 'tw-tldr')
    # generic template paragraphs in China-advantage section
    s = rep1(s, TW_CN_PARA1_OLD, TW_CN_PARA1_NEW, 'tw-cnpara1')
    s = rep1(s, TW_CN_PARA2_OLD, TW_CN_PARA2_NEW, 'tw-cnpara2')
    # 1) H2 question-form conversions (keep ids)
    for hid, new in TW_H2:
        old_html = f'<h2 id="{hid}">'
        # find existing text for this id
        m = re.search(re.escape(old_html) + r'(.*?)</h2>', s, re.S)
        assert m, f"tw h2 not found: {hid}"
        if m.group(1) != new:
            s = rep1(s, m.group(0), old_html + new + '</h2>', 'tw-h2-' + hid)
    # 2) TOC sync
    toc_entries = [(hid, new) for hid, new in TW_H2]
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{n}</a>' for o, n in toc_entries)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
    assert s2 != s or mob in s, "tw toc-mobile replace failed"
    s = s2
    # 3) FAQ + JSON-LD
    new_faq = '<div class="faq-list">\n' + build_faq_list(TW_FAQ) + '\n                </div>\n            </section>'
    s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'tw-faq')
    s = re_dl(s, JSONLD_RX, build_jsonld(TW_FAQ).replace('\\', '\\\\'), 'tw-jsonld')
    # 4) excerpts
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "資料質量自動化讓資料治理從被動補救轉向主動預防。",
        ], "TW-excerpt")
    integrity(s, [
        '?v=20260901', '預約示範', '"@type": "FAQPage"',
        '物流即時分析需要怎樣的技術架構', '為什麼中國物流企業能更快實現即時分析的價值',
        'id="規模化推廣的關鍵成功因素-2"', 'id="規模化推廣的關鍵成功因素"',
    ], 8, "zh-TW")
    assert s.count('id="規模化推廣的關鍵成功因素"') + s.count('id="規模化推廣的關鍵成功因素-2"') == 2, "tw duplicate id check"
    assert s[:s.index('</head>')].count('FAQPage') == 0, "tw head FAQPage present"
    save(ZHTW, s)
    print("zh-TW done")

if __name__ == "__main__":
    process_en()
    process_cn()
    process_tw()
    print("ALL DONE")
