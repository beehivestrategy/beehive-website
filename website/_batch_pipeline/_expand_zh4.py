import os
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = "synthetic-data-generation-for-safe-ai-development"
marker = "syn-closing2-zh"
block = '''
<h2 id="syn-closing2-zh">合成数据如何进入生产流程？</h2>
<p>进入生产的做法是把合成数据嵌入既有训练流水线：标注真实切片作验证，每批合成经保真与泄露测试后才准入。把它当受版本化与审计的常规输入，团队便能在合规前提下持续扩数据。合成数据不是一次性技巧，而是可治理、可追踪的训练资产。</p>
'''
p = os.path.join(ROOT, "zh-cn/blog/articles", slug + ".html")
html = open(p, encoding="utf-8").read()
if marker in html:
    print("[DONE]")
else:
    anchor = '<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">'
    html = html.replace(anchor, block + "\n" + anchor, 1)
    open(p, "w", encoding="utf-8").write(html)
    print("[OK]")
