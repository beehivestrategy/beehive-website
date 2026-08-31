import os, re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
BATCH = os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")
slugs = [l.strip() for l in open(BATCH) if l.strip()]

MAP = {
 "The Current Landscape": "What Does the Current Landscape Look Like?",
 "What Happens Without Board Buy-In": "What Happens When There Is No Board Buy-In?",
 "How Conversational Access Changes the Math": "How Does Conversational Access Change the Math?",
 "The Architecture Behind Sub-Second Decisions": "What Architecture Powers Sub-Second Decisions?",
 "When to Use REST API": "When Should You Use a REST API?",
 "When to Use GraphQL": "When Should You Use GraphQL?",
 "How MCP Powers Conversational BI": "How Does MCP Power Conversational BI?",
 "理解当前格局": "如何理解当前格局？",
 "关键原则与战略框架": "哪些原则决定战略框架的成败？",
 "实施方法与最佳实践": "应如何落地实施方法与最佳实践？",
 "衡量成功与展示投资回报率": "如何衡量成功并展示投资回报率？",
 "常见陷阱及规避方法": "常见陷阱有哪些，如何规避？",
 "2025年AI驱动的行业转型": "2025年AI驱动的行业转型是怎样的？",
 "金融服务：AI作为竞争差异化因素": "金融服务中AI如何成为竞争差异化因素？",
 "人机协作的必要性": "为什么人机协作不可或缺？",
 "行业格局与AI采用动态": "行业格局与AI采用动态是怎样的？",
 "关键用例与实施模式": "有哪些关键用例与实施模式？",
 "克服实施挑战": "如何克服实施挑战？",
 "行业最佳实践与成功案例分析": "有哪些行业最佳实践与成功案例？",
 "行业数字化转型深度分析": "行业数字化转型深度分析是怎样的？",
 "战略实施路径与关键成功因素": "战略实施路径与关键成功因素是什么？",
 "企业实施路线图与成功因素": "企业实施路线图与成功因素是什么？",
 "传统BI的局限性与变革的理由": "传统BI有哪些局限性，为何要变革？",
 "核心技术组件": "有哪些核心技术组件？",
 "实施策略与最佳实践": "应如何实施策略与最佳实践？",
 "对话式BI的进阶能力与未来演进": "对话式BI有哪些进阶能力与未来演进？",
 "对话式BI技术架构深度解析": "对话式BI技术架构如何深度解析？",
 "有治理无执行的陷阱": "有治理无执行会落入哪些陷阱？",
 "为什么董事会级别支持不可妥协": "为什么董事会级别支持不可妥协？",
 "没有董事会支持会怎样": "没有董事会支持会怎样？",
 "建立有效的董事会级AI治理": "如何建立有效的董事会级AI治理？",
 "企业AI治理的监管环境": "企业AI治理面临怎样的监管环境？",
 "常见误区与事实澄清": "有哪些常见误区与事实澄清？",
 "蜂启咨询如何帮助": "蜂启咨询如何帮助您？",
 "理解當前格局": "如何理解當前格局？",
 "關鍵原則與戰略框架": "哪些原則決定戰略框架的成敗？",
 "實施方法與最佳實踐": "應如何落地實施方法與最佳實踐？",
 "衡量成功與展示投資回報率": "如何衡量成功並展示投資回報率？",
 "常見陷阱及規避方法": "常見陷阱有哪些，如何規避？",
 "2025年AI驅動的行業轉型": "2025年AI驅動的行業轉型是怎樣的？",
 "金融服務：AI作为競爭差异化因素": "金融服務中AI如何成為競爭差異化因素？",
 "人機協作的必要": "為什麼人機協作不可或缺？",
 "行業格局與AI採用動態": "行業格局與AI採用動態是怎樣的？",
 "關鍵用例與實施模式": "有哪些關鍵用例與實施模式？",
 "克服實施挑戰": "如何克服實施挑戰？",
 "行業最佳實踐與成功案例分析": "有哪些行業最佳實踐與成功案例？",
 "行業數位轉型深度分析": "行業數位轉型深度分析是怎樣的？",
 "戰略實施路徑與關鍵成功因素": "戰略實施路徑與關鍵成功因素是什麼？",
 "企業實施路線圖與成功因素": "企業實施路線圖與成功因素是什麼？",
 "傳統BI的局限性與變革的理由": "傳統BI有哪些局限性，為何要變革？",
 "核心技術組件": "有哪些核心技術組件？",
 "實施策略與最佳實踐": "應如何實施策略與最佳實踐？",
 "對話式BI的進階能力與未來演進": "對話式BI有哪些進階能力與未來演進？",
 "對話式BI技術架構深度解析": "對話式BI技術架構如何深度解析？",
 "有治理無執行的陷阱": "有治理無執行會落入哪些陷阱？",
 "為什麼董事會級別支持不可妥協": "為什麼董事會級別支持不可妥協？",
 "沒有董事會支持會怎樣": "沒有董事會支持會怎樣？",
 "建立有效的董事會級AI治理": "如何建立有效的董事會級AI治理？",
 "企業AI治理的監管環境": "企業AI治理面臨怎樣的監管環境？",
 "常見誤區與事實澄清": "有哪些常見誤區與事實澄清？",
 "蜂啟諮詢如何幫助": "蜂啟諮詢如何幫助您？",
}

total = 0
for slug in slugs:
    for lang, prefix in [("en",""),("zh-CN","zh-cn/"),("zh-TW","zh-tw/")]:
        p = os.path.join(ROOT, prefix+"blog/articles/"+slug+".html")
        if not os.path.exists(p):
            continue
        h = open(p, encoding='utf-8').read()
        # build alternation of all statement keys
        keys = list(MAP.keys())
        alt = "(?:" + "|".join(re.escape(k) for k in keys) + ")"
        pat = re.compile(r'(<h2[^>]*>)(' + alt + r')(</h2>)')
        def repl(m):
            global total
            # find which key matched by exact text
            txt = m.group(2)
            total += 1
            return m.group(1) + MAP[txt] + m.group(3)
        h2_new, n = pat.subn(repl, h)
        if n:
            open(p, "w", encoding='utf-8').write(h2_new)
            print(f"  {lang} {slug[:36]:36} -> {n} H2")
print("TOTAL H2 converted:", total)
