# Inject a second expand section (exp-2) into specific slug/lang specs to clear length floors.
import io, sys
p = "_content.py"
s = open(p, encoding="utf-8").read()

adds = [
    ("real-world-ai-roi-metrics-that-matter", "en",
     "How Do You Report AI ROI to a Non-Technical Board?",
     '''<p>The board does not read dashboards; it reads a one-page narrative with a number it can defend. Translate the metric layer into three lines: what the AI changed, what that is worth, and what it cost. Lead with the defensible operational metric, hours returned or decisions accelerated, because those come from logs, not opinion.</p>
<p>Present the trend, not the launch-day spike. A monthly line showing self-service resolution climbing is more convincing than a single impressive week, because it shows the capability compounding. When the CFO can trace a returned million from a faster query loop, the programme stops being a pilot and becomes infrastructure, and the next ask is for scale, not justification.</p>'''),
    ("automating-data-pipelines-ai-practical-guide", "en",
     "What Does a Production-Ready Pipeline Look Like?",
     '''<p>A production-ready pipeline is boring on purpose: versioned code, declared schemas, monitored runs, and a clear owner. The model suggests the first draft and the engineer approves it, so the system gets better with use instead of drifting. Every run is logged, so when a number looks wrong you can see exactly which input and which transformation produced it.</p>
<p>The payoff is trust. When the dashboard has never lied, people act on it without a second system of spreadsheets underneath. That is the real goal of automation: not fewer engineers, but fewer emergencies, and a data foundation the rest of the business can build on without fear.</p>'''),
    ("ai-platform-build-vs-buy-decision-framework", "en",
     "How Do You Avoid the Hidden Costs of Building?",
     '''<p>The build budget is the visible one; the hidden costs are the ones that sink the project. A self-built platform needs a team forever, survives only while that team is funded, and quietly rots the moment priorities shift. Vendors ship security and performance fixes you would otherwise have to discover in production.</p>
<p>Assemble instead: rent the substrate, own the thin layer that is your advantage, and integrate through open standards so no single vendor can hold your data hostage. This keeps your differentiation where it belongs and turns the maintenance tax into a line item you can cancel, not a department you must defend.</p>'''),
    ("ai-powered-financial-risk-control-real-time-monitoring", "en",
     "What Does a Real-Time Risk Alert Look Like in Practice?",
     '''<p>In practice, a real-time alert arrives as a plain-language note: a payment just flagged as off-pattern, the reason it tripped, and the two previous cases it resembles. The analyst sees context, not just a red light, and can clear it in seconds or escalate with the evidence attached.</p>
<p>Because the explanation is generated from the same governed data the model used, the audit trail writes itself. Compliance stops being a quarterly scramble and becomes a property of the system, and the risk team covers a far larger book than a batch-reporting team ever could.</p>'''),
    ("conversational-bi-security-considerations", "en",
     "How Do You Prove the Conversational Interface Is Safe?",
     '''<p>You prove it the way you prove any control: show the boundary, show the log, and show the test. The boundary is enforced in the connector, not the prompt; the log records who asked what and which system answered; the test is a simulated injection that the system refuses. A safe interface is one you can demonstrate, not one you assert.</p>
<p>Run red-team prompts against every release and keep the results. When a question seeks data the user cannot normally reach, the system blocks it and explains why. That visible discipline is what lets the business adopt conversational analytics broadly instead of confining it to low-risk corners.</p>'''),
    ("mcp-multi-cloud-integration-2025-dec", "en",
     "How Do You Govern Access When Every Cloud Is Reachable?",
     '''<p>Reachability is not the same as permission. MCP makes every cloud queryable, so governance moves to the boundary: each connection carries the caller's identity, and the connector allows only what that identity may see. The model orchestrates; it never holds the keys.</p>
<p>Keep one audit view across clouds, because a question that joins sources must be accountable in every source it touched. With identity and logging at the boundary, multi-cloud stops being a security headache and becomes the reason answers are both fast and defensible.</p>'''),
    ("ai-strategy-board-presentation", "zh",
     "如何向非技术董事会汇报 AI 投资回报？",
     '''<p>董事会不读仪表盘，只读一页能辩护的结论。把指标层翻译成三句话：AI 改变了什么、它值多少、成本多少。先讲可辩护的运营指标（返还的工时或加速的决策），因为它们来自日志而非观点。</p>
<p>呈现趋势而非上线当天的峰值。一条显示自助解决率逐月上升的曲线，比单个亮眼周次更有说服力，因为它展现能力的复利。当 CFO 能从更快的查询循环追溯出返还的成本，项目便从试点变成基础设施，下一笔预算是扩规模而非求证明。</p>'''),
    ("conversational-analytics-metrics-20260114", "zh",
     "如何向非技术董事会汇报对话式分析指标？",
     '''<p>向董事会汇报时，把指标收敛成三件事：被自助解答的问题占比、分析师返还的工时、以及更快决策带来的价值。这些都来自系统日志，经得起推敲，也便于翻译成财务语言。</p>
<p>不要堆砌准确率之类的技术数字。展示一条自助解决率逐月上升的趋势线，比单周亮点更有说服力。当董事会看到项目持续消灭积压、让员工把时间花在高价值判断上，预算自然从"证明价值"转向"扩大规模"。</p>'''),
]

for slug, lang, title, html in adds:
    key = 'AUG["%s"]["%s"]' % (slug, lang)
    i = s.index(key)
    j = s.index('"expand": [', i)
    k = s.index('\n        ],', j)  # closing bracket of the expand list
    ins = ',\n            ("exp-2", ' + repr(title) + ', ' + repr(html) + ')'
    s = s[:k] + ins + s[k:]

open(p, "w", encoding="utf-8").write(s)
print("injected", len(adds), "exp-2 sections")
