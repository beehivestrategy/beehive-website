import os, re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
BATCH = os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")
slugs = [l.strip() for l in open(BATCH) if l.strip()]

MAP = {
 # mixed-simplified/traditional zh-TW universal template phrases
 "关键原则与戰略框架": "哪些原則決定戰略框架的成敗？",
 "實施方法与最佳實踐": "應如何落地實施方法與最佳實踐？",
 "衡量成功与展示投資回報率": "如何衡量成功並展示投資回報率？",
 "2025年AI驱動的行業轉型": "2025年AI驅動的行業轉型是怎樣的？",
 "關鍵原則與策略框架": "哪些原則決定策略框架的成敗？",
 # mcp "when to use" phrases (zh-CN and zh-TW variants)
 "何时使用REST API": "何時應該使用 REST API？",
 "何时使用GraphQL": "何時應該使用 GraphQL？",
}

total = 0
for slug in slugs:
    for lang, prefix in [("en",""),("zh-CN","zh-cn/"),("zh-TW","zh-tw/")]:
        p = os.path.join(ROOT, prefix+"blog/articles/"+slug+".html")
        if not os.path.exists(p):
            continue
        h = open(p, encoding='utf-8').read()
        keys = list(MAP.keys())
        alt = "(?:" + "|".join(re.escape(k) for k in keys) + ")"
        pat = re.compile(r'(<h2[^>]*>)(' + alt + r')(</h2>)')
        def repl(m):
            global total
            txt = m.group(2)
            total += 1
            return m.group(1) + MAP[txt] + m.group(3)
        h2_new, n = pat.subn(repl, h)
        if n:
            open(p, "w", encoding='utf-8').write(h2_new)
            print(f"  {lang} {slug[:34]:34} -> {n} H2")
print("TOTAL:", total)
