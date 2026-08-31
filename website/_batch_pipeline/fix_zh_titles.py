#!/usr/bin/env python3
"""Repair half-translated zh-CN / zh-TW article titles.

Bug: a word-substitution pass left titles like
  "From SQL to 自然语言: The 演进 of 数据 Queries"
i.e. English scaffolding with a few Chinese words swapped in.

Fix: replace with proper human-quality zh-CN titles (below), convert to
zh-TW with OpenCC (s2twp), and update every place the title appears in the
document: <title>, <h1>, og:title, twitter:title.

Idempotent: reruns are no-ops once titles are correct.
Run: python3 fix_zh_titles.py [--dry]
"""
import os, re, sys, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

# slug -> proper zh-CN title (translated, not word-substituted)
CN_TITLES = {
    "ai-consulting-delivery-models": "AI 咨询交付模式：从顾问建议到落地实施",
    "ai-consulting-delivery-models-20260126": "AI 咨询交付模式：从顾问建议到落地实施",
    "ai-ethics-in-enterprise-beyond-compliance": "企业 AI 伦理：从合规走向信任",
    "anatomy-of-analytics-failure-metric-drift-and-trust-gaps": "分析失败剖析：指标漂移、定义含混与信任落差",
    "beyond-dashboards-the-shift-to-conversational-analytics": "超越仪表板：向对话式分析的转变",
    "building-a-data-driven-culture-from-strategy-to-practice": "构建数据驱动文化：从战略到实践",
    "building-an-ai-center-of-excellence": "搭建 AI 卓越中心：架构、角色与常见陷阱",
    "case-study-consultancy-cut-reporting-time-mcp-bi": "案例研究：某咨询公司如何将报告时间缩短 71%",
    "chatbi-vs-traditional-bi-total-cost-of-ownership": "ChatBI 对比传统 BI：总体拥有成本分析",
    "customer-journey-analytics-with-ai-from-click-to-purchase": "AI 驱动的客户旅程分析：从点击到购买",
    "edge-computing-and-ai-bringing-intelligence-to-the-factory-floor": "边缘计算与 AI：把智能带到车间一线",
    "from-sql-to-natural-language-the-evolution-of-data-queries": "从 SQL 到自然语言：数据查询的演进之路",
    "inventory-forecasting-with-machine-learning": "用机器学习做库存预测：零售商实战指南",
    "mcp-vs-traditional-apis-why-context-protocol-changes-everything": "MCP 对比传统 API：上下文协议为何改变一切",
    "multi-turn-conversations-in-bi-how-ai-maintains-context": "BI 中的多轮对话：AI 如何维持上下文",
    "natural-language-to-sql-how-ai-understands-your-data": "自然语言转 SQL：AI 如何理解你的数据",
    "open-source-vs-proprietary-ai-making-the-right-choice": "开源与闭源商业 AI：如何为企业做出正确选择",
    "pipl-compliance-for-ai-systems-a-practical-guide": "AI 系统的个人信息保护法合规实践指南",
    "retail-demand-forecasting-ai": "AI 零售需求预测：兼顾准确性与敏捷性",
    "smart-factory-data-architecture-from-sensors-to-insights": "智能工厂数据架构：从传感器到业务洞察",
    "the-rise-of-ai-agent-marketplaces": "AI 智能体市场的崛起：企业需要了解什么",
    "what-is-mcp-model-context-protocol-explained": "什么是 MCP？为企业管理者解读模型上下文协议",
}


def get_h1_raw(html):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not m:
        return None
    inner = m.group(1)
    # strip any nested tags to get the text as it appears
    return re.sub(r"<[^>]+>", "", inner).strip()


def replace_title(html, old, new):
    """Replace the old title text everywhere it appears (title, h1, og, twitter)."""
    if not old or old == new:
        return html, 0
    n = html.count(old)
    if n:
        html = html.replace(old, new)
    return html, n


def main():
    dry = "--dry" in sys.argv
    try:
        from opencc import OpenCC
        # MUST match the site's own generator (generate_zh_tw.py uses 's2t').
        # s2twp would convert 数据 -> 資料, which contradicts the existing
        # zh-TW bodies that use 數據. Consistency beats locale purity here.
        cc = OpenCC("s2t")
    except Exception as e:
        print("OpenCC unavailable:", e)
        return

    total_files = 0
    total_repl = 0
    skipped = []

    for slug, cn_title in CN_TITLES.items():
        tw_title = cc.convert(cn_title)
        for sub, new_title in (("zh-cn", cn_title), ("zh-tw", tw_title)):
            p = os.path.join(ROOT, sub, "blog/articles", slug + ".html")
            if not os.path.exists(p):
                skipped.append(p)
                continue
            html = open(p, encoding="utf-8").read()
            old = get_h1_raw(html)
            if not old:
                skipped.append(p + " (no h1)")
                continue
            if old == new_title:
                continue  # already fixed
            html2, n = replace_title(html, old, new_title)
            if n and not dry:
                open(p, "w", encoding="utf-8").write(html2)
            if n:
                total_files += 1
                total_repl += n
                print(f"{'[dry] ' if dry else ''}{sub}/{slug}: {n}x")
                print(f"      OLD: {old}")
                print(f"      NEW: {new_title}")

    # ---- PASS 2 -------------------------------------------------------
    # Generic sweep: any zh-TW title that is still half-translated but whose
    # zh-CN counterpart is already clean -> derive zh-TW from zh-CN via s2t.
    # Catches slugs where only the zh-TW file went stale.
    import glob
    FILLER = re.compile(r"\b(?:the|of|for|to|and|in|from|with|a|an|is|are|how|why|what)\b", re.I)

    def half_translated(t):
        cjk = len(re.findall(r"[\u4e00-\u9fff]", t))
        return cjk > 0 and len(FILLER.findall(t)) >= 2

    p2_files = 0
    for p in sorted(glob.glob(os.path.join(ROOT, "zh-tw/blog/articles/*.html"))):
        slug = os.path.basename(p)[:-5]
        html = open(p, encoding="utf-8").read()
        old = get_h1_raw(html)
        if not old or not half_translated(old):
            continue
        cn_path = os.path.join(ROOT, "zh-cn/blog/articles", slug + ".html")
        if not os.path.exists(cn_path):
            continue
        cn_title = get_h1_raw(open(cn_path, encoding="utf-8").read())
        if not cn_title or half_translated(cn_title):
            continue  # zh-CN is also bad -> needs a human/model translation
        new_title = cc.convert(cn_title)
        html2, n = replace_title(html, old, new_title)
        if n and not dry:
            open(p, "w", encoding="utf-8").write(html2)
        if n:
            p2_files += 1
            total_files += 1
            total_repl += n
            print(f"{'[dry] ' if dry else ''}[pass2] zh-tw/{slug}: {n}x")
            print(f"      OLD: {old}")
            print(f"      NEW: {new_title}")

    print(f"\npass2 (zh-TW derived from clean zh-CN): {p2_files} files")
    print(f"{'[DRY RUN] ' if dry else ''}files updated: {total_files}, total replacements: {total_repl}")
    if skipped:
        print("skipped:", len(skipped))
        for s in skipped[:5]:
            print("   ", s)


if __name__ == "__main__":
    main()
