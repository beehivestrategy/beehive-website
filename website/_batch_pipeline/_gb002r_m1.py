#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass 1 (mechanical): recommended-card hrefs + excerpts, zh-TW s2twp conversion."""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb002r_lib as L

SLUGS = [l.strip() for l in open('/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/gap_batches/gbatch_002.txt') if l.strip()]

EX_EN = {
    "supply-chain-resilience-ai-demand-sensing":
        "How AI demand sensing shortens the signal-to-action loop so planners see a shift weeks before orders move.",
    "supply-chain-resilience-ai-scenario-planning":
        "A practical model for stress-testing supply chains with AI-generated scenarios before disruption arrives.",
    "technical-architecture-enterprise-ai-agents":
        "The layers, guardrails and orchestration choices behind enterprise AI agents that survive production.",
    "vector-databases-enterprise-search-2026-practical-guide":
        "What it takes to run vector search at enterprise scale — indexing, hybrid retrieval and cost control.",
    "why-data-strategy-needs-ai-agent-layer-2026":
        "Why a governed agent layer turns a warehouse from a reporting backlog into an answers-on-demand service.",
    "women-in-data-building-inclusive-ai-teams":
        "How inclusive data teams shrink model blind spots and improve the decisions AI systems support.",
}
EX_ZH = {
    "ai-competitive-moat-2026":
        "企業在2026年如何把數據、流程與人才沉澱為難以複製的AI競爭壁壘。",
    "cfo-guide-ai-budget-allocation":
        "CFO如何在控制風險的前提下分配AI預算，並把投入與可衡量的業務回報掛鉤。",
    "data-quality-automation-from-reactive-to-proactive-part-2":
        "把數據質量從事後補救轉為前置預防的自動化機制與落地路徑。",
    "data-visualization-ai-insights":
        "用可視化設計把AI洞察變成可執行的決策動作，而不是更多的圖表。",
    "enterprise-data-governance-framework-steps":
        "五步建立可落地的數據治理框架，讓指標口徑、責任與訪問規則清晰可查。",
    "generative-ai-enterprise-search":
        "生成式AI如何讓企業搜索從關鍵詞匹配升級為可直接引用的答案。",
}
EX_ZH_CN = {
    "ai-competitive-moat-2026":
        "企业在2026年如何把数据、流程与人才沉淀为难以复制的AI竞争壁垒。",
    "cfo-guide-ai-budget-allocation":
        "CFO如何在控制风险的前提下分配AI预算，并把投入与可衡量的业务回报挂钩。",
    "data-quality-automation-from-reactive-to-proactive-part-2":
        "把数据质量从事后补救转为前置预防的自动化机制与落地路径。",
    "data-visualization-ai-insights":
        "用可视化设计把AI洞察变成可执行的决策动作，而不是更多的图表。",
    "enterprise-data-governance-framework-steps":
        "五步建立可落地的数据治理框架，让指标口径、责任与访问规则清晰可查。",
    "generative-ai-enterprise-search":
        "生成式AI如何让企业搜索从关键词匹配升级为可直接引用的答案。",
}

# manual zh-TW heading overrides (after opencc)
TW_H2 = {
    "conversational-bi-executives-natural-language-queries": [
        ("Architecture and Technical Foundation", "對話式BI的技術架構與基礎設施是什麼？"),
        ("Implementation Best Practices", "企業應該如何落地對話式BI？"),
        ("Measuring Conversational BI Impact", "如何衡量對話式BI的實際成效？"),
    ],
    "anatomy-of-analytics-failure-metric-drift-and-trust-gaps": [
        ("故障一：公制漂移", "失敗之一：指標漂移是什麼？"),
        ("失敗之二：定義模糊", "失敗之二：為什麼定義模糊會拖垮分析？"),
        ("失敗三：信任差距", "失敗之三：信任差距是怎麼形成的？"),
        ("解決方案：將受控指標作爲產品", "解決方案：為什麼要把受控指標當成產品？"),
        ("要點", "本文要點是什麼？"),
        ("結論", "企業該從哪一步開始修復信任？"),
    ],
    "supply-chain-demand-forecasting-ai": [
        ("爲什麼重要", "為什麼AI需求預測如此重要？"),
        ("常見挑戰", "導入AI需求預測的常見挑戰有哪些？"),
        ("如何開始", "企業應該如何開始導入？"),
        ("核心要點", "本文的核心要點是什麼？"),
    ],
    "multi-turn-conversations-in-bi-how-ai-maintains-context": [
        ("上下文窗口問題", "什麼是上下文窗口問題？"),
        ("參考分辨率", "AI如何解析代詞與省略指代？"),
        ("上下文窗口管理策略", "上下文窗口應該如何管理？"),
        ("何時重置上下文", "什麼時候該重置上下文？"),
        ("要點", "本文要點是什麼？"),
        ("結論", "設計多輪對話的下一步是什麼？"),
    ],
    "real-estate-ai-property-valuation": [
        ("理解当前格局", "AI物業估值的當前格局是什麼？"),
        ("关键原则与戰略框架", "AI估值的關鍵原則與戰略框架是什麼？"),
        ("實施方法与最佳實踐", "企業應該如何實施AI估值？"),
        ("衡量成功与展示投資回報率", "如何衡量AI估值的投資回報？"),
        ("常见陷阱及规避方法", "AI估值有哪些常見陷阱？"),
        ("關鍵要點", "本文的關鍵要點是什麼？"),
        ("结论", "企業導入AI估值的下一步是什麼？"),
    ],
    "pipl-compliance-for-ai-systems-a-practical-guide": [
        ("AI 系統的 PIPL 要求", "PIPL對AI系統提出了哪些要求？"),
        ("數據本地化實踐", "數據本地化在實踐中如何落地？"),
        ("自動決策合規性", "自動化決策需要滿足哪些合規要求？"),
        ("審計追蹤和責任", "企業該如何建立審計追蹤與問責機制？"),
        ("要點", "本文要點是什麼？"),
        ("結論", "合規工作應該從哪裡開始？"),
    ],
}

changed = []
for slug in SLUGS:
    for lang, pat in L.LANGS:
        rel = pat % slug
        h = L.read(rel)
        o = h
        h = L.fix_rec_hrefs(h, lang)
        h = L.fill_excerpts(h, EX_EN if lang == "EN" else (EX_ZH_CN if lang == "zh-CN" else EX_ZH))
        if lang == "zh-TW":
            h = L.map_art(h, L.opencc_inner)
            for old, new in TW_H2.get(slug, []):
                h = L.retitle_h2(h, [(old, new)])
        if h != o:
            L.guard(rel, o, h)
            L.write(rel, h)
            changed.append(rel)
print("changed %d files" % len(changed))
for c in changed:
    print("  ", c)
