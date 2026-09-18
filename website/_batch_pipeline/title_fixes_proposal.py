#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task #805: title fix proposal generator.
Input : title_bad_list.json (88 entries, ~10 false positives kept as-is)
Output: title_fixes_proposal.json + title_fixes_proposal.html
Each fix: slug -> new zh-CN title (hand-translated from EN original),
          new zh-TW title = OpenCC s2twp(zh-CN).
"""
import json, html, os
from opencc import OpenCC

BASE = os.path.dirname(os.path.abspath(__file__))
cc = OpenCC('s2twp')

# slug -> new zh-CN title (drafted from EN original title)
FIXES = {
    # --- junk family: "框架指南" ---
    "ai-budget-justification-framework-q4-planning": "AI 预算论证框架：Q4 规划实操指南",
    "ai-data-governance-framework-implementation-steps": "AI 数据治理框架落地实施：企业分步指南",
    "ai-data-quality-framework-year-end-nov2025": "AI 数据质量框架：年终评估要点",
    "ai-model-governance-year-end-2025": "AI 模型治理：年终框架评估",
    "ai-roi-framework-2025-annual-review": "AI ROI 框架：2025 年度绩效回顾",
    "ai-roi-measurement-framework-enterprise-2026": "衡量 AI ROI：2026 年企业投资评估框架",
    "ai-strategy-2026-planning-framework-oct2025": "AI 战略 2026 规划框架：入门指南",
    "data-quality-year-end-audit-framework-oct2025": "数据质量年终审计：框架与最佳实践",
    "enterprise-ai-risk-management-framework-proactive": "主动式 AI 风险管理：预测与化解 AI 故障的企业框架",
    "enterprise-ai-roi-year-end-evaluation-nov2025": "企业 AI ROI：年终评估框架",
    # --- junk family: "X实践指南" (uninformative) ---
    "ai-conversational-analytics-energy-sector-optimization": "能源行业对话式分析：优化运营与可持续发展",
    "ai-powered-financial-risk-control-real-time-monitoring": "AI 驱动的金融风险控制：实时监控实践",
    "ai-talent-retention-strategies-year-end-oct2025": "AI 人才保留策略：年终规划要点",
    "conversational-analytics-nlg-automated-insight-reports": "自然语言生成（NLG）：自动化洞察报告实战",
    "conversational-bi-finance-year-end-close-2025": "对话式 BI 助力财务年终结算",
    "data-governance-year-end-compliance-report-oct2025": "数据治理年终合规报告指南",
    "data-marketplace-enterprise-data-monetization-strategy": "企业数据市场：数据变现的策略与架构",
    "data-privacy-impact-assessment-ai-dpia": "AI 系统的数据保护影响评估（DPIA）",
    "data-security-conversational-bi-ciso-perspective": "对话式 BI 安全防护：CISO 视角",
    "digital-transformation-ai-first-enterprise-modernization": "AI 优先的企业现代化：智能体时代的数字化转型",
    "edge-ai-retail-decision-intelligence-oct2025": "边缘 AI 赋能零售决策智能",
    "edge-ai-telecommunications-network-optimization": "电信行业边缘 AI：5G 时代的网络优化",
    "enterprise-ai-architecture-trends-2025-dec": "企业 AI 架构趋势：2025 年度回顾",
    "enterprise-ai-august-2026-month-ahead-trends": "企业 AI 月度前瞻：2026 年 8 月关键趋势与事件",
    "enterprise-ai-platform-build-vs-buy-decision-2026": "2026 年企业 AI 平台：自建还是采购？决策框架",
    "enterprise-ai-scaling-strategies-2026-nov2025": "2026 年企业 AI 规模化扩展策略",
    "eu-ai-act-compliance-enterprise-checklist-2026": "2026 年企业欧盟 AI 法案合规清单：准备事项一览",
    "fall-conference-roundup-ai-announcements-oct2025": "2025 秋季 AI 大会盘点：企业关键要点",
    "holiday-retail-analytics-ai-insights-dec2025": "假日零售分析：AI 驱动的 12 月洞察",
    "llm-deployment-production-enterprise-best-practices": "LLM 生产环境部署：可靠性与成本的企业最佳实践",
    "manufacturing-digital-twin-ai-predictive-simulation": "制造业数字孪生与 AI：智能工厂的预测性仿真",
    "mcp-enterprise-adoption-benchmark-nov2025": "MCP 企业采纳基准：2025 年调研结果",
    "mcp-enterprise-data-access-security-patterns": "MCP 企业数据访问安全模式：零信任实施",
    "mcp-multi-cloud-integration-2025-dec": "MCP 多云集成：2025 年企业部署现状",
    "mcp-security-best-practices-enterprise-nov2025": "MCP 企业部署安全最佳实践",
    "mcp-standardization-enterprise-dec2025": "MCP 标准化：2025 年 12 月企业采纳现状",
    "mcp-standardization-enterprise-interoperability-future": "MCP 标准化与企业互操作性：未来之路",
    "mlops-enterprise-deployment-best-practices": "企业级 MLOps：模型部署最佳实践",
    "nl2sql-accuracy-improvement-enterprise-oct2025": "提升企业 NL2SQL 准确率的实践",
    "real-estate-ai-market-analysis-2025": "房地产 AI 市场分析：PropTech 如何发力",
    "real-estate-ai-market-intelligence-investment-decisions": "AI 市场情报助力房地产投资决策：从直觉到数据驱动",
    "real-time-analytics-holiday-season-ai-oct2025": "假日季实时分析：AI 应用指南",
    "retail-ai-customer-lifetime-value-prediction": "零售 AI 客户生命周期价值预测：模型与方法",
    "retail-ai-dynamic-pricing-competitive-intelligence": "零售 AI 动态定价：用竞争情报优化定价",
    "retail-black-friday-ai-analytics-2025": "2025 黑色星期五：AI 驱动的零售分析",
    "semantic-layer-conversational-bi-self-service-analytics": "语义层：自助式对话分析的基础",
    "small-language-models-enterprise-efficiency-cost": "企业级小语言模型（SLM）：兼顾效率与质量",
    "small-language-models-enterprise-efficiency": "企业 SLM 战略：高性价比的 AI 路线",
    "technology-trends-2025-roundup-ai": "2025 年科技趋势盘点：定义年度的 AI",
    "top-data-quality-tools-enterprise-2026": "2026 年企业级数据质量工具 Top 榜",
    # --- tiny (extreme truncation) ---
    "mcp-vs-rest-api-vs-graphql-complete-comparison": "MCP vs REST API vs GraphQL：全方位对比",
    "rag-retrieval-augmented-generation-enterprise-knowledge": "超越聊天机器人的 RAG：企业知识管理的检索增强生成",
    # --- junk/tiny: "什么是？" ---
    "what-is-mlops-machine-learning-operations": "什么是 MLOps？企业实战手册",
    "what-is-mlops": "什么是 MLOps？机器学习运营详解",
    "what-is-text-to-sql-natural-language-query": "什么是 Text-to-SQL？革新业务数据查询",
    "what-is-text-to-sql": "什么是 Text-to-SQL？自然语言数据库查询入门",
    # --- half-translated (中英夹杂破碎) ---
    "ai-healthcare-data-interoperability": "医疗数据互操作性中的 AI：打破数据孤岛",
    "ai-model-evaluation-metrics-that-matter-for-business": "AI 模型评估：业务视角的关键指标",
    "algorithmic-trading-ai-risk-management": "算法交易与 AI 风险管理",
    "auto-generated-visualizations-how-ai-picks-the-right-chart": "自动生成可视化：AI 如何选对图表",
    "building-semantic-layer-self-service-analytics": "构建语义层：自助式分析的秘诀",
    "case-study-logistics-ai-route-optimization": "案例研究：物流公司借助 AI 路径优化节省 23% 燃油成本",
    "competitive-advantage-through-ai": "借助 AI 构建竞争优势：战略框架",
    "data-contract-implementation": "数据契约（Data Contracts）：规模化保障 Schema 质量",
    "data-governance-operating-model": "可规模化扩展的数据治理运营模型",
    "data-mesh-vs-data-warehouse-choosing-the-right-architecture": "Data Mesh vs 数据仓库：如何选择合适的架构",
    "data-quality-at-scale-monitoring-alerting-remediation": "规模化数据质量：监控、告警与修复",
    "data-stewardship-roles-responsibilities": "数据管护（Data Stewardship）：角色、职责与最佳实践",
    "designing-natural-language-interfaces-for-enterprise-data": "为企业数据设计自然语言交互界面",
    "digital-twin-enterprise-transformation-20260125": "数字孪生企业转型：超越炒作概念",
    "digital-twin-enterprise-transformation": "数字孪生企业转型：超越炒作概念",
    "ai-governance-frameworks-enterprise-data-platforms": "企业数据平台的 AI 治理框架",
    "mlops-for-enterprise-deploying-models-at-scale": "企业 MLOps：规模化部署模型",
    "modern-data-stack-evaluation": "现代数据栈评估：自建、采购还是组合？",
    "natural-language-to-sql-how-ai-understands-your-data": "自然语言转 SQL：AI 如何理解你的数据",
    "supply-chain-ai-predictive-logistics-and-demand-planning": "供应链 AI：预测性物流与需求规划",
    "text-to-sql-transformation-modern-bi-platforms": "释放企业洞察：现代 BI 中的 Text-to-SQL",
    # --- tw-only fix (cn already good) ---
    "what-is-reverse-etl": "什么是反向 ETL（Reverse ETL）？概念与架构详解",
}

# false positives (audit flagged, but titles are fine) — kept for the report
KEEP = [
    "ai-vendor-risk-assessment-framework", "anthropic-claude-enterprise-deployment-framework-2026",
    "best-chatbi-tools-2026-enterprise-comparison", "cloudflare-os-open-source-ai-agent-platform-2026",
    "microsoft-teams-analytics-dashboards", "regtech-ai-compliance-financial-services",
    "snowflake-databricks-genie-conversational-ai", "text-to-sql-accuracy-benchmark-2026",
    "what-is-data-quality-management-framework", "cross-border-data-transfer-framework-2025-compliance",
]

# republish-variant pairs inside the fix list (same content, two slugs)
VARIANTS = [
    ["digital-twin-enterprise-transformation-20260125", "digital-twin-enterprise-transformation"],
    ["what-is-mlops-machine-learning-operations", "what-is-mlops"],
    ["what-is-text-to-sql-natural-language-query", "what-is-text-to-sql"],
]

def main():
    with open(os.path.join(BASE, "title_bad_list.json"), encoding="utf-8") as f:
        bad = {e["slug"]: e for e in json.load(f)}

    proposal = []
    for slug, new_cn in FIXES.items():
        src = bad[slug]
        new_tw = cc.convert(new_cn)
        proposal.append({
            "slug": slug,
            "en": src["en"],
            "old_cn": src["cn"], "new_cn": new_cn,
            "old_tw": src["tw"], "new_tw": new_tw,
            "changed_cn": src["cn"].strip() != new_cn.strip(),
            "changed_tw": src["tw"].strip() != new_tw.strip(),
        })

    with open(os.path.join(BASE, "title_fixes_proposal.json"), "w", encoding="utf-8") as f:
        json.dump(proposal, f, ensure_ascii=False, indent=1)

    # HTML report
    rows = []
    for i, p in enumerate(proposal, 1):
        cn_chg = "" if p["changed_cn"] else "（cn 不变）"
        tw_chg = "" if p["changed_tw"] else "（tw 不变）"
        rows.append(
            "<tr><td>%d</td><td class='slug'>%s</td>"
            "<td class='en'>%s</td>"
            "<td class='old'>%s</td><td class='new'>%s</td>"
            "<td class='old'>%s</td><td class='new'>%s</td></tr>" % (
                i, html.escape(p["slug"]), html.escape(p["en"]),
                html.escape(p["old_cn"]), html.escape(p["new_cn"] + " " + cn_chg),
                html.escape(p["old_tw"]), html.escape(p["new_tw"] + " " + tw_chg)))

    keep_rows = "".join("<li>%s</li>" % html.escape(s) for s in KEEP)
    var_rows = "".join("<li>%s ↔ %s</li>" % tuple(html.escape(x) for x in v) for v in VARIANTS)

    doc = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>标题修复提案 — %d 篇</title><style>
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;margin:24px;color:#1a1a1a;background:#fafafa}
h1{font-size:22px}h2{font-size:17px;margin-top:28px}
table{border-collapse:collapse;width:100%%;font-size:12px;background:#fff}
th,td{border:1px solid #ddd;padding:5px 7px;text-align:left;vertical-align:top}
th{background:#2B9E8B;color:#fff;position:sticky;top:0}
td.slug{font-family:monospace;font-size:11px;color:#666;word-break:break-all}
td.en{color:#555;font-style:italic}
td.old{color:#c0392b;text-decoration:line-through}
td.new{color:#1a7a4c;font-weight:600}
.box{background:#fff;border:1px solid #ddd;border-radius:8px;padding:14px 18px;margin:14px 0}
ul{margin:6px 0;padding-left:20px}.warn{color:#b8860b}</style></head><body>
<h1>📝 标题修复提案 — %d 篇 zh-CN + zh-TW</h1>
<p>来源：title_bad_list.json（88 条低质量标题审计）→ 剔除 %d 条误报 → <b>%d 篇待改</b>。新 zh-CN 标题均从 EN 原文重译；zh-TW 用 OpenCC s2twp 自动转换；仅改标题，不动 URL/slug 与正文。</p>
<div class="box"><b>⚠️ 决策项 — 重发布变体对（同内容双 slug，本次标题改法为"两页同题"）：</b><ul>%s</ul>
<span class="warn">更优解是下线其中一个重复页（301/删除），属删除类操作需另行批准；若两页都保留，则两页标题保持一致即可。</span></div>
<div class="box"><b>误报保留（%d 篇，不改）：</b><ul>%s</ul></div>
<h2>修复明细（%d 篇）</h2>
<table><tr><th>#</th><th>slug</th><th>EN 原标题</th><th>zh-CN 现状</th><th>zh-CN 新标题</th><th>zh-TW 现状</th><th>zh-TW 新标题</th></tr>
%s</table></body></html>""" % (
        len(proposal), len(proposal), len(KEEP), len(proposal),
        var_rows, len(KEEP), keep_rows, len(proposal), "".join(rows))

    out_html = os.path.join(BASE, "title_fixes_proposal.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(doc)

    cn_only = sum(1 for p in proposal if p["changed_cn"])
    tw_only = sum(1 for p in proposal if p["changed_tw"] and not p["changed_cn"])
    print("proposal entries: %d | cn changed: %d | tw-only: %d" % (len(proposal), cn_only, tw_only))
    print("html:", out_html)

if __name__ == "__main__":
    main()
