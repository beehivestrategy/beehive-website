# -*- coding: utf-8 -*-
import re, os, json, sys

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
CJK = re.compile(r'[\u4e00-\u9fff]')

COMMON_CN = {
    'Data Quality Automation From Reactive To Proactive Part 2': '数据质量自动化：从被动到主动（二）',
    'Cfo Guide Ai Budget Allocation': 'CFO指南：AI预算分配',
    'Technology': '技术',
}
COMMON_TW = {
    'Data Quality Automation From Reactive To Proactive Part 2': '資料品質自動化：從被動到主動（二）',
    'Cfo Guide Ai Budget Allocation': 'CFO指南：AI預算分配',
    'Technology': '技術',
}

# ---------- FAQ content for the 8 zh-tw files ----------
FAQ = {
'zh-tw/blog/articles/ai-agent-memory-persistence-patterns.html': [
 ("長期運行的AI智能體為什麼需要獨立的記憶層？",
  "若每次對話都從零開始，智能體無法累積業務語境，也難以承接跨週期的任務。本文指出，2025年企業架構的競爭焦點已從單次回答品質轉向持續性能力；採用標準化MCP協議的組織整合時間減少47%，正是因為記憶與資料存取被收斂到可治理的單一層級。"),
 ("記憶持久化在生產環境最容易踩到哪些坑？",
  "最常見的錯誤是把記憶當成單純的技術快取，忽略權限與資料分級。文中提到，58%的組織在擴展AI系統時將其列為首要挑戰；而事先定義整合邊界的組織，回報的整合問題少45%、上市時間快30%。建議在寫入前就訂清楚誰能讀、保存多久、何時清除。"),
 ("智能體記憶與MCP標準化協議是什麼關係？",
  "MCP為智能體連接企業資料來源提供通用協議，讓記憶不再依附於各系統的私有介面。文中指出，基於該標準的即時整合方案在新增部署中的佔比已從2024年的23%升至2025年上半年的41%，反映企業正把記憶層從專案級提升為平台級資產。"),
 ("該如何為記憶層的投資設定回報預期？",
  "建議以分階段驗證取代一次性上線：先在高價值、低風險的用例中確認記憶帶來的決策改善，再逐步擴大範圍。文中指出，領先行業的AI投資回本期已從24個月縮短至14個月；把持續優化視為長期旅程的企業，成功率比同業平均高出3.2倍。"),
],
'zh-tw/blog/articles/ai-agent-orchestration-patterns-production.html': [
 ("生產環境的編排與概念驗證有什麼本質差別？",
  "概念驗證只需證明單一路徑可行，生產編排則要同時處理失敗重試、權限邊界與可觀測性。本文指出，2025年最成功的企業採用分階段部署模型，先全面評估現有能力，再以有針對性的試點產生可衡量結果，之後才擴展到更廣泛的企業架構用例。"),
 ("為什麼編排在2025年成為企業AI的關鍵瓶頸？",
  "因為單一智能體的能力已相對成熟，瓶頸轉移到多個智能體如何協同。文中提到，58%的組織在擴展AI系統時將其列為首要挑戰；而事先定義整合邊界的組織，回報的整合問題少45%、上市時間快30%，顯示編排紀律比模型選型更決定成敗。"),
 ("編排層該自建還是採用標準化協議？",
  "建議優先採用標準化協議。文中指出，採用標準化MCP協議的組織相比使用專有解決方案者，整合時間減少47%；基於該標準的即時整合方案在新增部署佔比已從2024年的23%升至2025年上半年的41%，自建的差異化空間正快速縮小。"),
 ("編排失效時的風險該如何控制？",
  "應把治理前置到架構設計，而非事後補救。文中指出，設立專責治理團隊的組織回報監管發現少55%、新市場合規時間快40%；同時建議為每個編排環節預留可隨時介入的開關，並以定期能力評估機制追蹤最佳實務的變化。"),
],
'zh-tw/blog/articles/ai-agent-safety-guardrails-production.html': [
 ("防護欄與傳統應用安全控制有何不同？",
  "傳統控制防的是可預期的輸入，防護欄要處理的是模型自主產生的不確定行為。本文建議把安全視為架構設計的一部分：事先定義整合邊界的組織，回報的整合問題少45%、上市時間快30%，明顯優於上線後才補強的做法。"),
 ("上線前最少需要建立哪些防護機制？",
  "至少包含權限最小化、輸出攔截與完整稽核軌跡三層。文中提到，建立專責治理團隊的組織回報監管發現少55%、新市場合規時間快40%；同時提醒，58%的組織在擴展AI系統時已將相關治理列為首要挑戰，這是普遍課題。"),
 ("防護欄會不會拖慢智能體的回應速度？",
  "取決於設計位置。把控制放在標準化協議層，而非讓每個應用各自實作，可避免重複開銷。文中指出，採用標準化MCP協議的組織整合時間減少47%；基於該標準的即時整合方案在新增部署佔比已從2024年的23%升至2025年上半年的41%，兼顧了安全與效率。"),
 ("防護規則上線後該如何持續維運？",
  "應建立定期的能力評估機制，持續追蹤業界最佳實務與威脅型態的變化，並依業務需求調整策略方向。文中指出，把治理視為持續旅程而非一次性專案的企業，長期成功率比同業平均高出3.2倍，證明反覆迭代比靜態規則可靠。"),
],
'zh-tw/blog/articles/ai-agent-testing-strategies-enterprise.html': [
 ("智能體為什麼不能用傳統軟體測試方法驗收？",
  "傳統測試假設相同輸入會得到相同輸出，智能體的回應則帶有變異性。本文建議改以分階段部署模型驗證：先全面評估現有能力，再以有針對性的試點產生可衡量結果，之後才擴展到更廣泛的企業架構用例，讓可靠性在真實場景中逐步被證明。"),
 ("測試應該覆蓋到哪些層面才算完整？",
  "除功能正確性，還需覆蓋權限邊界、異常輸入與合規軌跡。文中指出，事先定義整合與部署要求的組織，回報的整合問題少45%、上市時間快30%；而設立專責治理團隊者，監管發現少55%、新市場合規時間快40%。"),
 ("測試環境與生產環境的落差該如何彌補？",
  "關鍵是把資料存取標準化，讓測試環境能安全取得與生產同構的資料。文中提到，採用標準化MCP協議的組織整合時間減少47%；基於該標準的即時整合方案在新增部署佔比已從2024年的23%升至2025年上半年的41%，降低了環境之間的對接成本。"),
 ("測試投入要多久才能看到回報？",
  "建議以高價值、低風險的用例先行，累積可衡量的改善後再擴大範圍。文中指出，領先行業的AI投資回本期已從24個月縮短至14個月；而把可靠性建設視為持續旅程的企業，長期成功率比同業平均高出3.2倍。"),
],
'zh-tw/blog/articles/ai-agentic-workflows-automation-platform.html': [
 ("智能體工作流與傳統流程自動化有什麼本質差異？",
  "傳統自動化依賴事先寫死的規則，智能體工作流能依據上下文自行決定下一步。本文指出，2025年最有效的部署並非全面替換既有流程，而是先深刻理解現有工作方式，再以洞察增強人類決策，形成系統與領域專家互補的協作關係。"),
 ("從單一智能體擴展到多智能體協同時會遇到什麼？",
  "主要挑戰是邊界與責任歸屬。文中提到，58%的組織在擴展AI系統時將其列為首要挑戰；而事先定義整合邊界的組織，回報的整合問題少45%、上市時間快30%，說明協同規範必須在擴展之前就寫清楚。"),
 ("自動化平台該自建還是採用標準化協議？",
  "建議以標準化協議為底座，把工程資源留給業務差異化。文中指出，採用標準化MCP協議的組織整合時間減少47%；基於該標準的即時整合方案在新增部署佔比已從2024年的23%升至2025年上半年的41%，重複造輪子的空間正快速縮小。"),
 ("平台建好後如何維持長期價值？",
  "應建立定期的能力評估機制，追蹤最佳實務並隨業務變化調整方向。文中指出，把自動化建設視為持續旅程而非一次性專案的企業，長期成功率比同業平均高出3.2倍；領先行業的AI投資回本期也已從24個月縮短至14個月。"),
],
'zh-tw/blog/articles/ai-budgeting-2026-fiscal-year-planning.html': [
 ("2026財年AI預算該從試點還是平台開始分配？",
  "數據給出明確訊號：72%的企業至少有一個AI試點在生產環境運行，但只有23%擴展到單一部門之外。預算重點應從「再多幾個試點」轉向讓既有試點跨出單一部門，否則投入會持續卡在驗證階段，難以形成規模效應。"),
 ("AI預算該由IT部門還是業務單位主導？",
  "研究顯示，設有專責AI職能的組織，其價值實現速度比把AI職責分散在IT部門的組織快2.8倍。預算責任應交給能直接對業務結果負責的單位，IT則專注於資料基礎與平台治理，兩者以跨職能治理機制對齊。"),
 ("高階主管的支持對預算回報有多大影響？",
  "影響遠大於技術選型或預算規模。針對50個企業部署的分析顯示，成功最強的預測因素是高階主管支持與跨職能治理的一致程度；由C級主管積極推動的公司，價值實現速度快3.2倍，使用者滿意度高67%。"),
 ("2026財年該把多少預算留給資料基礎？",
  "建議優先於應用層。經驗顯示，在啟動AI計畫前先投資強大資料基礎的組織，表現始終優於同時並行建置資料品質與AI能力的組織。此外應保留治理預算：設有專責治理團隊者回報監管發現少55%、新市場合規時間快40%。"),
],
'zh-tw/blog/articles/ai-copyright-global-policies-august-2025.html': [
 ("企業現在最該追蹤哪些AI版權法域的變化？",
  "截至2025年8月，監管格局在多個法域同步推進：東盟的新框架、美國各州陸續成文的規定，以及更新的歐盟AI法案實施指南，都需要全球合規團隊持續關注。建議以法域為單位指派責任人，而非等法規生效才啟動評估。"),
 ("跨法域營運時，合規架構該怎麼設計？",
  "建議以最嚴格的法域為基準建立共同底線，再依各地要求疊加。文中指出，設有專責治理團隊的組織回報監管發現少55%、新市場合規時間快40%；相較之下，事後逐案補救的成本明顯更高。"),
 ("AI版權合規會吃掉多少AI專案預算？",
  "傳統上整合工作可能消耗專案預算的40%至60%。文中指出，MCP等標準化協議透過為AI智能體連接企業資料來源提供通用介面，消除了這項長期障礙，讓預算從重複的對接工作轉向治理與應用本身。"),
 ("合規投入如何轉化為可衡量的商業價值？",
  "合規不只是成本。研究顯示，設有專責AI治理職能的組織，價值實現速度比把職責分散在IT部門者快2.8倍；而把治理視為持續旅程的企業，長期成功率比同業平均高出3.2倍，顯示治理成熟度與商業回報高度相關。"),
],
'zh-tw/blog/articles/ai-ethics-board-setup-corporate-governance.html': [
 ("AI倫理委員會該由哪些成員組成才有效？",
  "建議橫跨法務、風險、資料與業務單位，並由C級主管擔任召集人。針對50個企業部署的分析顯示，成功最強的預測因素不是技術選型或預算規模，而是高階主管支持與跨職能治理的一致程度；由C級主管積極推動的公司價值實現速度快3.2倍。"),
 ("倫理委員會與既有治理機制該如何分工？",
  "不必另起爐灶，而是把AI議題嵌入既有的風險與合規流程，再增設跨職能的審議環節。研究顯示，設有專責治理職能的組織，價值實現速度比把AI職責分散在IT部門者快2.8倍，關鍵在於責任歸屬清楚，而非組織數量多。"),
 ("委員會成立後應優先審議哪些議題？",
  "建議從高影響、低風險的用例切入，先建立判斷標準與紀錄機制，再逐步擴大到高風險場景。文中提到，72%的企業至少有一個AI試點在生產環境運行，但只有23%擴展到單一部門之外，顯示審議需求會隨規模快速成長。"),
 ("如何向董事會證明倫理治理帶來回報？",
  "可從合規效率與價值實現兩個面向衡量。設有專責治理團隊的組織回報監管發現少55%、新市場合規時間快40%；而把治理視為持續旅程的企業，長期成功率比同業平均高出3.2倍，兩者都能轉化為董事會可追蹤的指標。"),
],
}

# ---------- per-file translations ----------
CN = {}

def add(rel, h=None, toc=None, tags=None, extra=None):
    d = CN.setdefault(rel, {'h': {}, 'toc': {}, 'tags': {}, 'extra': []})
    if h: d['h'].update(h)
    if toc: d['toc'].update(toc)
    if tags: d['tags'].update(tags)
    if extra: d['extra'].extend(extra)

A = 'zh-cn/blog/articles/'

add(A+'manufacturing-digital-twin-ai-predictive-simulation.html',
    h={'Domain-Specific Implementation Patterns': '行业特定实施模式',
       'ROI Measurement and Value Realization': 'ROI衡量与价值实现',
       'Overcoming Industry-Specific Barriers': '跨越行业特定障碍'},
    tags={'Predictive Simulation': '预测性仿真'})

add(A+'mcp-protocol-security-enterprise-deployment.html',
    tags={'data integration': '数据集成'})

add(A+'mcp-standardization-enterprise-interoperability-future.html',
    h={'Technical Architecture and Implementation？': '技术架构与实施？',
       'Integration with Enterprise Systems？': '与企业系统的集成？',
       'Performance Optimization and Cost Management？': '性能优化与成本管理？'},
    toc={'Technical Architecture and Implementation': '技术架构与实施',
         'Integration with Enterprise Systems': '与企业系统的集成',
         'Performance Optimization and Cost Management': '性能优化与成本管理'},
    tags={'Enterprise Ecosystem': '企业生态系统', 'Interoperability': '互操作性',
          'Standardization': '标准化'})

add(A+'month-ahead-enterprise-ai-events-february-2026.html',
    h={'Regulatory Milestones to Watch？': '值得关注的监管里程碑？',
       'Making Events Actionable？': '如何把会议转化为行动？',
       'February Planning Checklist？': '二月规划清单？'},
    toc={'Regulatory Milestones to Watch': '值得关注的监管里程碑',
         'Making Events Actionable': '如何把会议转化为行动',
         'February Planning Checklist': '二月规划清单'},
    tags={'AI Events': 'AI活动', 'Enterprise AI News': '企业AI动态',
          'Industry Calendar': '行业日历'})

add(A+'natural-language-generation-automated-business-reporting.html',
    h={'MCP and Semantic Layers: The NLG Infrastructure': 'MCP与语义层：NLG基础设施',
       'Practical Implementation Patterns': '实践中的实施模式',
       'Measuring NLG Return on Investment': '衡量NLG投资回报'},
    tags={'Automated Reporting': '自动化报告'})

add(A+'omnichannel-retail-analytics-unifying-online-and-offline-data.html',
    h={'Recommended Articles': '推荐文章',
       'Women In Data Building Inclusive Ai Teams': '女性与数据：打造包容的AI团队',
       'Why Data Strategy Needs Ai Agent Layer 2026': '为何数据策略需要AI智能体层',
       'Vector Databases Enterprise Search 2026 Practical Guide': '向量数据库企业搜索实践指南',
       'Inventory Forecasting With Machine Learning': '用机器学习做库存预测',
       'Customer Journey Analytics With AI': '用AI分析客户旅程',
       'Omnichannel Retail Analytics: Unifying Online and Offline Data': '全渠道零售分析：统一线上与线下数据'},
    toc={'The Data Silo Problem': '数据孤岛问题',
         'Building the Unified Customer Profile': '构建统一客户档案',
         'Cross-Channel Attribution': '跨渠道归因',
         'Real-Time Inventory Visibility': '实时库存可见',
         'What Should Retailers Do First?': '零售商应该先做什么？',
         'Privacy and Compliance Across Channels': '跨渠道的隐私与合规',
         'Key Takeaways': '关键要点',
         'Conclusion': '结语'},
    tags={'customer journey': '客户旅程', 'omnichannel': '全渠道',
          'retail analytics': '零售分析', 'retail data integration': '零售数据集成',
          'unified commerce': '统一商务'},
    extra=[('Table of Contents', '目录'), ('Topics', '主题'),
           ('Share this article', '分享本文'), ('Related Articles', '相关文章'),
           ('Retail', '零售'),
           ('Beehive Strategy · March 29, 2026 · 5 min read', 'Beehive Strategy · 2026年3月29日 · 5 分钟阅读')])

add(A+'preparing-data-team-ai-augmented-era.html',
    h={'The AI-Augmented Data Team Structure': 'AI增强型数据团队结构',
       'Upskilling Framework for Data Teams': '数据团队技能提升框架',
       'Measuring Data Team Transformation': '衡量数据团队转型成效'},
    tags={'AI Skills': 'AI技能', 'Data Culture': '数据文化', 'Data Teams': '数据团队',
          'Workforce Transformation': '劳动力转型'})

add(A+'preparing-gdpr-like-regulations-asia-pacific.html',
    h={'Compliance Challenges for AI Deployment': 'AI部署的合规挑战',
       'Building a Multi-Jurisdiction Compliance Architecture': '构建跨司法管辖区合规架构',
       'Actionable Recommendations': '可落地的行动建议'},
    tags={'AI Compliance': 'AI合规', 'Asia Pacific Regulation': '亚太监管',
          'GDPR Asia': '亚洲GDPR'})

add(A+'real-cost-poor-data-governance.html',
    h={'What Does Mature Governance Look Like?': '成熟的数据治理长什么样？',
       'What Does Governance for the AI Era Look Like?': 'AI时代的数据治理长什么样？',
       'How Do You Build a Governance Framework That Works?': '如何建立真正有效的数据治理框架？'},
    toc={'What Mature Governance Looks Like': '成熟的数据治理长什么样？',
         'Governance for the AI Era': 'AI时代的数据治理长什么样？',
         'Building a Governance Framework That Works': '如何建立真正有效的数据治理框架？'})

add(A+'retail-ai-customer-lifetime-value-prediction.html',
    h={'Domain-Specific Implementation Patterns': '行业特定实施模式',
       'ROI Measurement and Value Realization': 'ROI衡量与价值实现',
       'Overcoming Industry-Specific Barriers': '跨越行业特定障碍'},
    tags={'Customer Lifetime Value': '客户终身价值', 'ML Models': 'ML模型',
          'Marketing Analytics': '营销分析'})

add(A+'rise-agentic-workflows-enterprise-software.html',
    h={'The Technology Stack for Agentic Workflows': '智能体工作流的技术栈',
       'Agentic Workflows in Practice': '智能体工作流实践',
       'Challenges and Risk Mitigation': '挑战与风险缓解'},
    tags={'AI Architecture': 'AI架构', 'Agentic Workflows': '智能体工作流',
          'Enterprise Automation': '企业自动化'})

add(A+'small-language-models-enterprise-efficiency-cost.html',
    h={'Technical Architecture and Implementation？': '技术架构与实施？',
       'Integration with Enterprise Systems？': '与企业系统的集成？',
       'Performance Optimization and Cost Management？': '性能优化与成本管理？'},
    toc={'Technical Architecture and Implementation': '技术架构与实施',
         'Integration with Enterprise Systems': '与企业系统的集成',
         'Performance Optimization and Cost Management': '性能优化与成本管理'},
    tags={'Cost Efficiency': '成本效益', 'Model Selection': '模型选型',
          'Small Language Models': '小型语言模型'})

add(A+'smes-benefit-ai-agents-practical-guide.html',
    h={'High-Value AI Use Cases for SMEs': '中小企业的高价值AI用例',
       'Implementation Guide for SMEs': '中小企业实施指南',
       'SME Success Stories': '中小企业成功案例'},
    tags={'SME AI': '中小企业AI', 'Small Business': '小型企业'})

add(A+'state-enterprise-llm-deployment-china.html',
    h={'MCP and Domestic Platform Integration': 'MCP与国产平台集成',
       'Conversational BI for SOE Decision-Making': '面向国企决策的对话式BI',
       'Implementation Roadmap for SOEs': '国企实施路线图'},
    tags={'AI Regulation China': '中国AI监管', 'China LLM': '中国大模型',
          'Domestic AI Models': '国产AI模型', 'Enterprise AI China': '中国企业AI'})

add(A+'state-of-data-quality-enterprise-audits.html',
    h={'The AI Impact: Why Data Quality Matters More Now': 'AI的影响：为何数据质量更关键',
       'Common Data Quality Failure Patterns': '常见数据质量失效模式',
       'Building a Data Quality Monitoring Framework': '建立数据质量监控框架'},
    tags={'Data Audits': '数据审计', 'Enterprise Data': '企业数据'})

add(A+'supply-chain-ai-demand-forecasting-accuracy.html',
    h={'Domain-Specific Implementation Patterns': '行业特定实施模式',
       'ROI Measurement and Value Realization': 'ROI衡量与价值实现',
       'Overcoming Industry-Specific Barriers': '跨越行业特定障碍'},
    tags={'AI Methods': 'AI方法'})

add(A+'supply-chain-ai-optimization-summer-2025.html',
    tags={'industry solutions': '行业解决方案'})

add(A+'telecommunications-ai-network-optimization.html',
    tags={'industry solutions': '行业解决方案'})

add(A+'top-mcp-connectors-data-integration-2026.html',
    h={'Top 10 MCP Connectors Ranked': '十大MCP连接器排名'},
    tags={'AI Tools': 'AI工具', 'Data Integration': '数据集成',
          'MCP Connectors': 'MCP连接器'})

add(A+'vector-databases-enterprise-search-2026-practical-guide.html',
    h={'Technical Architecture and Implementation': '技术架构与实施',
       'Integration with Enterprise Systems': '与企业系统的集成',
       'Performance Optimization and Cost Management': '性能优化与成本管理'},
    tags={'AI Infrastructure': 'AI基础设施', 'Vector Databases': '向量数据库'})

add(A+'why-data-strategy-needs-ai-agent-layer-2026.html',
    h={'Why Does the Agent Layer Matter Now?': '为何智能体层现在至关重要？',
       'How Does the AI Agent Layer Work in Practice?': 'AI智能体层在实践中如何运作？',
       'How Do You Build Your AI Agent Layer: A Roadmap?': '构建AI智能体层的路线图？'},
    toc={'Why the Agent Layer Matters Now': '为何智能体层现在至关重要？',
         'How the AI Agent Layer Works in Practice': 'AI智能体层在实践中如何运作？',
         'Building Your AI Agent Layer: A Roadmap': '构建AI智能体层的路线图？'})

# zh-tw per-file
TW_FILES = {}
for rel in FAQ:
    TW_FILES[rel] = {'h': {}, 'toc': {}, 'tags': {}}
TW_FILES['zh-tw/blog/articles/ai-agent-memory-persistence-patterns.html']['tags'] = {'data integration': '資料整合'}
TW_FILES['zh-tw/blog/articles/ai-agent-orchestration-patterns-production.html']['tags'] = {'data integration': '資料整合'}
TW_FILES['zh-tw/blog/articles/ai-agent-safety-guardrails-production.html']['tags'] = {'data integration': '資料整合'}
TW_FILES['zh-tw/blog/articles/ai-agent-testing-strategies-enterprise.html']['tags'] = {'data integration': '資料整合'}
TW_FILES['zh-tw/blog/articles/ai-agentic-workflows-automation-platform.html']['tags'] = {'data integration': '資料整合'}
TW_FILES['zh-tw/blog/articles/ai-budgeting-2026-fiscal-year-planning.html']['tags'] = {'AI ROI': 'AI投資回報'}
TW_FILES['zh-tw/blog/articles/ai-copyright-global-policies-august-2025.html']['tags'] = {'regulation': '法規'}
TW_FILES['zh-tw/blog/articles/ai-ethics-board-setup-corporate-governance.html']['tags'] = {'AI ROI': 'AI投資回報'}

# ---------- replacement helpers ----------
def sub_text(src, pattern, mapping, group=1):
    """pattern: compiled regex with one capturing group holding the text"""
    def rep(m):
        t = m.group(group)
        if t in mapping:
            return m.group(0)[:m.start(group) - m.start(0)] + mapping[t] + m.group(0)[m.end(group) - m.start(0):]
        return m.group(0)
    return pattern.sub(rep, src), None

P_HEAD = re.compile(r'(<h[1-6]\b[^>]*>)((?:(?!</h[1-6]\b).)*?)(</h[1-6]>)', re.S)
P_TOC = re.compile(r'(<a\b[^>]*class="[^"]*toc-link[^"]*"[^>]*>)((?:(?!</a>).)*?)(</a>)', re.S)
P_TAG = re.compile(r'(<span class="article-tag-pill">)((?:(?!</span>).)*?)(</span>)', re.S)
P_CAT = re.compile(r'(<span class="recommended-card-cat">)((?:(?!</span>).)*?)(</span>)', re.S)
P_CPILL = re.compile(r'(<span class="article-cat-pill">)((?:(?!</span>).)*?)(</span>)', re.S)
P_SHEAD = re.compile(r'(<div class="sidebar-heading">)((?:(?!</div>).)*?)(</div>)', re.S)
P_REL = re.compile(r'(<h4 class="sidebar-related-title">)((?:(?!</h4>).)*?)(</h4>)', re.S)
P_TOGGLE = re.compile(r'(<button class="toc-mobile-toggle"[^>]*>)((?:(?!</button>).)*?)(</button>)', re.S)
P_META = re.compile(r'(<div class="article-meta-text">)((?:(?!</div>).)*?)(</div>)', re.S)

def apply_map(src, pattern, mapping, counter, label):
    def rep(m):
        t = re.sub(r'\s+', ' ', m.group(2)).strip()
        if t in mapping:
            counter[label] += 1
            return m.group(1) + mapping[t] + m.group(3)
        return m.group(0)
    return pattern.sub(rep, src)

# ---------- FAQ rebuild ----------
def rebuild_faq(src, qa):
    # 1. visible questions
    idx = {'n': 0}
    def rep_q(m):
        i = idx['n']; idx['n'] += 1
        return m.group(1) + str(i + 1) + m.group(3) + qa[i][0] + m.group(4)
    src, nq = re.subn(r'(<span class="faq-question-text"><span class="faq-number">)(\d+)(</span><span>)undefined(</span>)',
                      rep_q, src)
    # 2. visible answers
    idx['n'] = 0
    def rep_a(m):
        i = idx['n']; idx['n'] += 1
        return m.group(1) + qa[i][1] + m.group(2)
    src, na = re.subn(r'(<div class="faq-answer-inner">)undefined(</div>)', rep_a, src)
    assert nq == 3 and na == 3, (nq, na)

    # 3. clone a 4th item after the last faq-item
    starts = [m.start() for m in re.finditer(r'<div class="faq-item">', src)]
    last = starts[-1]
    pos = last
    depth = 0
    while True:
        m = re.compile(r'<div\b|</div>').search(src, pos)
        if m.group(0) == '<div':
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = m.end()
                break
        pos = m.end()
    block = src[last:end]
    indent = block[:len(block) - len(block.lstrip())]
    newblock = block
    newblock = re.sub(r'(<span class="faq-question-text"><span class="faq-number">)\d+', r'\g<1>4', newblock, count=1)
    newblock = re.sub(r'(<span class="faq-question-text"><span class="faq-number">\d+</span><span>)[^<]*(</span>)',
                      lambda m: m.group(1) + qa[3][0] + m.group(2), newblock, count=1)
    newblock = re.sub(r'(<div class="faq-answer-inner">)[^<]*(</div>)',
                      lambda m: m.group(1) + qa[3][1] + m.group(2), newblock, count=1)
    src = src[:end] + '\n' + indent + newblock.lstrip() + src[end:]

    # 4. JSON-LD FAQPage
    def rep_ld(m):
        data = json.loads(m.group(1))
        if data.get('@type') != 'FAQPage':
            return m.group(0)
        data['mainEntity'] = [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]
        body = json.dumps(data, ensure_ascii=False, indent=2)
        return '<script type="application/ld+json">\n' + body + '\n</script>'
    src, nld = re.subn(r'<script type="application/ld\+json">(.*?)</script>', rep_ld, src, flags=re.S)
    return src, nld

# ---------- main ----------
def process(rel, dry=False):
    p = os.path.join(ROOT, rel)
    src = open(p, encoding='utf-8').read()
    orig = src
    d0 = len(re.findall(r'<div\b', src)) - len(re.findall(r'</div>', src))
    counter = {'h': 0, 'toc': 0, 'tag': 0, 'cat': 0, 'faq': 0}

    tw = rel.startswith('zh-tw')
    common = COMMON_TW if tw else COMMON_CN
    cfg = TW_FILES.get(rel) if tw else CN.get(rel)

    hmap = dict(common)
    hmap.update(cfg['h'] if cfg else {})
    src = apply_map(src, P_HEAD, hmap, counter, 'h')

    tocmap = dict(hmap)
    tocmap.update(cfg['toc'] if cfg else {})
    src = apply_map(src, P_TOC, tocmap, counter, 'toc')

    tagmap = dict(common)
    tagmap.update(cfg['tags'] if cfg else {})
    src = apply_map(src, P_TAG, tagmap, counter, 'tag')
    src = apply_map(src, P_CAT, tagmap, counter, 'cat')

    if cfg and cfg.get('extra'):
        emap = dict(cfg['extra'])
        src = apply_map(src, P_SHEAD, emap, counter, 'cat')
        src = apply_map(src, P_CPILL, emap, counter, 'cat')
        src = apply_map(src, P_TOGGLE, emap, counter, 'cat')
        src = apply_map(src, P_META, emap, counter, 'cat')
        src = apply_map(src, P_REL, hmap, counter, 'h')

    if rel in FAQ:
        src, _ = rebuild_faq(src, FAQ[rel])
        counter['faq'] = 4

    d1 = len(re.findall(r'<div\b', src)) - len(re.findall(r'</div>', src))
    if d0 != d1:
        print('!! DIV DELTA CHANGED', rel, d0, d1)
        return None
    if not dry:
        open(p, 'w', encoding='utf-8').write(src)
    return counter

if __name__ == '__main__':
    files = [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/wo_faq_3.txt')) if l.strip()]
    lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, len(files))
    dry = '--dry' in sys.argv
    tot = {'h': 0, 'toc': 0, 'tag': 0, 'cat': 0, 'faq': 0}
    for f in files[lo:hi]:
        c = process(f, dry)
        if c is None:
            print('SKIP', f)
            continue
        for k in tot:
            tot[k] += c[k]
        print('%-70s h=%d toc=%d tag=%d cat=%d faq=%d' % (os.path.basename(f), c['h'], c['toc'], c['tag'], c['cat'], c['faq']))
    print('TOTAL', tot, 'DRY' if dry else 'WRITTEN')
