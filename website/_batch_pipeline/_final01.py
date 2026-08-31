import re, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib01 import ROOT, path, load, body, strip_tags

BASE_TITLE = {
 "fall-conference-roundup-ai-announcements-oct2025": ("Fall 2025 AI Conference Roundup: Key Enterprise Takeaways | Beehive St","企业AI实践指南 | Beehive Strategy","企業AI實踐指南 | Beehive Strategy"),
 "mcp-enterprise-data-access-security-patterns": ("MCP Security Patterns for Enterprise Data Access: Zero-Trust Implement","数据实践指南 | Beehive Strategy","數據實踐指南 | Beehive Strategy"),
 "professional-services-ai-leverage-growth": ("How Professional Services Firms Can Leverage AI for Growth | Beehive S","专业服务公司如何利用AI实现增长 | Beehive Strategy","專業服務公司如何利用AI實現增長 | Beehive Strategy"),
 "ai-governance-board-level-oversight": ("AI Governance at Board Level: What Directors Need to Know | Beehive St","董事会层面的AI治理：董事需要了解什么 | Beehive Strategy","董事會層面的AI治理：董事需要了解什麼 | Beehive Strategy"),
 "real-time-data-streaming-for-ai-powered-decision-making-a-2026-update": ("Real-Time Data Streaming for AI-Powered Decision Making: A 2026 Update","面向AI驱动决策的实时数据流：2026年更新 | Beehive Strategy","面向AI驅動決策的即時資料流：2026年更新 | Beehive Strategy"),
 "energy-efficiency-ai-manufacturing": ("Energy Efficiency Through AI in Manufacturing | Beehive Strategy","通过AI提升制造业能源效率 | Beehive Strategy","通過AI提升製造業能源效率 | Beehive Strategy"),
 "what-is-ai-agent-autonomous-system": ("What Is an AI Agent? Understanding Autonomous Systems | Beehive Strate","什么是AI智能体？理解自主系统 | Beehive Strategy","什麼是AI智能體？理解自主系統 | Beehive Strategy"),
 "chinese-manufacturers-ai-quality-control": ("How Chinese Manufacturers Are Using AI for Quality Control | Beehive S","中国制造商如何利用AI进行质量控制 | Beehive Strategy","中國製造商如何利用AI進行品質控制 | Beehive Strategy"),
 "microsoft-teams-analytics-dashboards": ("Analytics Inside Microsoft Teams: Beyond the Dashboard Link | Beehive ","Microsoft Teams内的分析：不止于仪表盘链接 | Beehive Strategy","Microsoft Teams內的分析：不止於儀表盤鏈接 | Beehive Strategy"),
 "logistics-route-optimization-ai-real-time": ("AI Route Optimization for Logistics: Real-Time Decision | Beehive Stra","物流AI路径优化：规模化实时决策 | Beehive Strategy","物流AI路徑優化：規模化即時決策 | Beehive Strategy"),
 "enterprise-ai-security-threat-landscape-2026": ("The Enterprise AI Security Threat Landscape in 2026: Attacks, Vulnerab","企业AI 威胁态势实践指南 | Beehive Strategy","企業AI 威脅態勢實踐指南 | Beehive Strategy"),
 "financial-services-ai-fraud-detection-real-time": ("Real-Time AI Fraud Detection in Financial Services: Architecture and I","银行业反欺诈系统：实时AI架构设计方案 | Beehive Strategy","銀行業反欺詐系統：實時AI架構設計方案 | Beehive Strategy"),
 "ai-powered-forecasting-weather-to-warehouse": ("AI-Powered Forecasting: From Weather to Warehouse | Beehive Strategy","AI驱动预测：从天气到仓库 | Beehive Strategy","AI驅動預測：從天氣到倉庫 | Beehive Strategy"),
 "best-data-catalog-tools-governance-discovery-2026": ("Best Data Catalog Tools for Governance and Discovery | Beehive Strateg","最佳数据目录工具：治理与发现 | Beehive Strategy","最佳數據目錄工具：治理與發現 | Beehive Strategy"),
 "voice-interface-enterprise-analytics-accessibility": ("Voice Interfaces Analytics: Accessibility &amp; Hands-Free Data | Beeh","企业分析语音界面：无障碍与免提数据探索 | Beehive Strategy","企業分析語音介面：無障礙與免提數據探索 | Beehive Strategy"),
}

def grab(h, pat):
    m = re.search(pat, h, re.S)
    return strip_tags(m.group(1)).strip() if m else None

problems = []
slugs = [l.strip() for l in open(sys.argv[1]) if l.strip()]
for slug in slugs:
    for i, lang in enumerate(("EN", "CN", "TW")):
        h = load(slug, lang)
        t = grab(h, r'<title>(.*?)</title>')
        exp = BASE_TITLE[slug][i]
        if not t.startswith(exp[:60]):
            problems.append("TITLE CHANGED %s %s: %r" % (slug, lang, t))
        for tag in ("og:title", "twitter:title"):
            v = grab(h, r'property="%s" content="(.*?)"' % tag) or grab(h, r'name="%s" content="(.*?)"' % tag)
            if v is None:
                problems.append("%s missing %s %s" % (slug, lang, tag))
        # head integrity
        head = h[:h.index("</head>")] if "</head>" in h else ""
        if '/css/article.css?v=20260826' not in head:
            problems.append("CSS VER %s %s" % (slug, lang))
        # footer + share
        if "<footer" not in h:
            problems.append("FOOTER %s %s" % (slug, lang))
        if h.count('article-share-btn') < 3:
            problems.append("SHARE %s %s" % (slug, lang))
        # single article region
        if h.count('<article') != 1:
            problems.append("ARTICLE COUNT %s %s = %d" % (slug, lang, h.count('<article')))
        # FAQ json-ld count
        if len(re.findall(r'"@type"\s*:\s*"FAQPage"', h)) != 1:
            problems.append("LD COUNT %s %s" % (slug, lang))
        # FAQ visible vs jsonld questions
        fb = re.search(r'class="faq-section".*?</section>', body(h), re.S)
        if not fb:
            problems.append("NO FAQ SECTION %s %s" % (slug, lang)); continue
        vis = [strip_tags(x).strip() for x in re.findall(
            r'<span class="faq-question-text">.*?</span><span>(.*?)</span>', fb.group(0), re.S)]
        lds = re.findall(r'"@type"\s*:\s*"Question",\s*"name":\s*"(.*?)"', h)
        if len(vis) < 3:
            problems.append("FAQ H3 %s %s = %d" % (slug, lang, len(vis)))
        # TOC anchor targets exist
        for m in re.finditer(r'<a href="#([^"]*)" class="(?:toc-link|toc-mobile-link)"', h):
            if 'id="%s"' % m.group(1) not in h:
                problems.append("BROKEN TOC ANCHOR %s %s %s" % (slug, lang, m.group(1)))
        # no leftover placeholders
        for bad in ("lorem ipsum", "TODO", "PLACEHOLDER", "{{"):
            if bad.lower() in body(h).lower():
                problems.append("PLACEHOLDER %s %s: %s" % (slug, lang, bad))

print("PROBLEMS:", len(problems))
for p in problems:
    print("  -", p)
print("OK" if not problems else "FAIL")
