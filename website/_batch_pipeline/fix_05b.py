import os, sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline")
from fixlib import s2tw, insert_expand
ROOT="/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
SLUG="agentic-ai-workflows-enterprise-automation"

EXTRA='''
<h2 id="why-im-native-delivery-matters-zh">为什么 IM 原生交付对代理 AI 至关重要？</h2>
<p>代理 AI 的价值，最终取决于它能否被人真正使用。把智能体塞进又一个独立应用， adoption 往往在上线后悄然衰减；而把它放进团队每天已在使用的聊天工具——企业微信、钉钉、飞书、Teams——采用成本几乎为零。</p>
<p>当智能体就在对话里回答问题、发起动作，员工无需学习新工具，价值也随对话自然发生。这正是蜂启咨询把 MCP 连接器、多语言语义层与 IM 原生交付结合的原因：企业一次构建，便可在多种智能体用例中复用。</p>

<h2 id="what-are-common-pitfalls-zh">代理 AI 项目有哪些常见陷阱？</h2>
<p>第一个陷阱是把试点当成硬仗。团队庆祝演示、宣布胜利，却发现试点跑在干净的手工数据上，生产系统永远看不到那种数据。解药是从第一天就用连接器和语义层对接真实源系统。</p>
<p>第二个陷阱是上线后无人对结果负责。一个改进了无人负责的指标的 AI，会被悄悄弃用；而绑定到业务负责人目标的 AI，会被捍卫、资助与改进。第三个陷阱是忽视智能体周边的人力工作流——培训、审阅流程重构、清晰叙事。</p>

<h2 id="how-to-govern-agentic-ai-zh">如何治理生产中的代理 AI？</h2>
<p>治理不是可选文书，而是部署的前置条件。领先的团队从第一个迭代起内建四项实践：访问控制（智能体继承人工同等权限）、审计日志（每次回答可重建）、评估（定期打分以发现漂移）、人工检查点（高风险动作保持人工把关）。</p>
<p>这些实践在合规评审中迅速显现价值。把它们作为平台能力交付——可被每个智能体复用——而非按用例重复构建，正是平台模式在速度与安全性上双双胜出的原因，也让企业能更快地采用新模型能力。</p>
'''

for lang,pre in [("zh-cn","zh-cn/blog/articles/"),("zh-tw","zh-tw/blog/articles/")]:
    p=os.path.join(ROOT,pre+SLUG+".html")
    t=open(p,encoding='utf-8').read()
    html = s2tw(EXTRA) if lang=="zh-tw" else EXTRA
    t=insert_expand(t, html)
    if lang=="zh-tw":
        t=t.replace('預約演示','預約示範')
    open(p,'w',encoding='utf-8').write(t)
print("done 05b")
