#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "agentic-workflows-enterprise-software-feb2025"

EN_SECTIONS = [
 ("how-do-you-set-the-right-autonomy-boundary-for-an-agent",
  "How Do You Set the Right Autonomy Boundary for an Agent?",
  """<p>Bounded autonomy is only meaningful if the boundary is written down. For every agent, produce a one-page decision-rights statement with three lists: what the agent may decide and execute alone, what it must escalate before acting, and what it must never do under any circumstances. The lists should be defined by consequence, not by technology. A useful test is to ask what the worst credible outcome is if the agent is wrong and nobody notices for a week — if that answer involves money moving, a customer communication, or a record that others depend on, the action belongs on the escalate list.</p>
<p>In practice the boundary is built from four dials. Scope limits which tools and datasets the agent can reach. Thresholds set the amounts and volumes it may act on without approval — a refund cap, an order value, a number of records affected. Reversibility distinguishes actions that can be undone, such as drafting a report, from actions that cannot, such as sending it. And blast radius caps the number of records or customers any single run can touch, so a systematic error is contained by design rather than discovered at scale.</p>
<p>Write the escalation path as a named role, not a queue. "Escalate to the on-call revenue analyst" gets resolved; "escalate to the finance team" does not. Then instrument it: track escalation rate and escalation accuracy, because an agent that escalates everything is a copilot with extra steps, and one that escalates nothing is an unbounded agent waiting for its first incident.</p>"""),

 ("how-do-you-stop-prompt-injection-becoming-an-execution-risk",
  "How Do You Stop Prompt Injection Becoming an Execution Risk?",
  """<p>Prompt injection changes category once an agent can act. In a chat assistant, a malicious instruction produces a bad answer — embarrassing, recoverable. In an agent with tool access, the same instruction produces a tool call: a data export, a message, a transaction. The attacker does not need to compromise your model; they only need to place text where the agent will read it — a support ticket, a document in the retrieval index, a field in a CRM record, a web page the agent fetches.</p>
<p>The defense is layered, because no single control is sufficient. Keep untrusted content clearly separated from instructions, so retrieved text is treated as data to be reasoned about rather than as commands. Validate every tool call against a schema and an allowlist of permitted tools and parameter ranges before execution, so an injected instruction that asks for an unlisted action fails closed. Resolve permissions per requesting user at call time rather than granting the agent a broad service identity, which is what turns a single compromised run into an organisation-wide exposure. Filter inputs and outputs at the gateway for injection patterns and for sensitive data leaving the boundary. And monitor action patterns at runtime, alerting on anomalies such as a sudden spike in export volume or an agent reaching a system it has never touched.</p>
<p>Finally, treat the audit trail as a control, not a log file. Recording every plan, tool call, and outcome is what lets you answer "what did the agent do and why" in minutes instead of days — and that answerability is what makes bounded autonomy defensible to risk, audit, and the business.</p>"""),

 ("what-should-you-measure-once-an-agentic-workflow-is-live",
  "What Should You Measure Once an Agentic Workflow Is Live?",
  """<p>Agentic workflows fail quietly when they are measured only by activity. Volume metrics — tasks processed, hours saved — tell you the agent is busy, not that it is working. A useful measurement set has four layers. Task outcomes measure whether the work was actually completed correctly: resolution rate, rework rate, and the share of runs that end without human correction. Quality measures correctness against a reviewed sample, which is the only way to detect an agent that is confidently wrong. Trust measures behaviour: escalation rate, override rate, and how often users accept the agent's output without editing it. Economics measure cost per completed task and the fully loaded time saved, net of review effort.</p>
<p>Pair these with operational Service Level Objectives: availability, p50 and p95 latency per task, and a budget ceiling per run. Publish them where the business can see them, reviewed on the same cadence as any other process — weekly at first, monthly once stable. The most diagnostic single number is the override rate: if humans are rewriting most of the agent's output, the workflow is not automated, it is relocated.</p>
<p>Close the loop by routing every failure into a review queue, then into the golden set of test cases used before each release. Programs that do this see quality compound; programs that do not see the same defects recur with growing volume.</p>"""),

 ("what-does-a-90-day-agentic-workflow-rollout-look-like",
  "What Does a 90-Day Agentic Workflow Rollout Look Like?",
  """<p>The rollout that works is narrow, auditable, and boring on purpose. Days 1 to 20 are discovery and selection: inventory candidate workflows and score each on four axes — how well the process is understood, how clean and governed the underlying data is, how visible the value is, and how containable the failure is. Pick the one that scores well on all four, not the one with the largest headline number. Analytics and reporting usually wins, because the data is governed, the output is verifiable, and mistakes are cheap.</p>
<p>Days 21 to 50 build the agent and its guardrails: connect the governed data sources through connectors that enforce permissions, define the decision-rights statement, wire escalation to a named role, and stand up logging for every plan, tool call, and outcome. Build the golden set of 50 to 100 representative tasks with verified answers before you let anyone use it, because you cannot detect a regression you never defined.</p>
<p>Days 51 to 75 run a supervised pilot with a small group: every action reviewed, every failure categorised, thresholds tuned against observed behaviour. Days 76 to 90 remove supervision for the actions that have proven safe, publish the metrics, and write the runbook — kill switch, rollback, on-call owner. Only then start the second workflow, and repeat the sequence. Organisations that try to launch five agents at once spend the same calendar time and end up with five ungoverned pilots.</p>"""),
]

EN_FAQ = [
 ("What is an agentic workflow in enterprise software?",
  "An agentic workflow is a process in which a software agent pursues a defined goal by planning its own steps, choosing and calling tools, adapting when conditions change, and deciding when to stop or escalate. It differs from traditional automation, which executes a fixed sequence and breaks when the environment deviates from the script. In practice, enterprise agentic workflows are bounded: the agent operates within explicit permissions and thresholds, and escalates to a named human role at defined decision points."),
 ("How is an agentic workflow different from RPA?",
  "RPA follows a predetermined script in a predetermined order and fails on exceptions. An agentic workflow plans at runtime, selects among available tools, recovers from unexpected states, and recognises when a task is complete or beyond its authority. That adaptability is why agents handle unstructured inputs and variable processes, and also why they need governance that RPA never required: permissions, audit trails, and escalation rules."),
 ("How much autonomy should we give an enterprise agent?",
  "Enough to complete the task, and no more. Define autonomy by consequence: actions that are reversible, low-value, and internal can run without approval, while anything involving money, customer communication, or records others depend on should require human confirmation. Start read-only, prove reliability on audited runs, then widen scope one action class at a time."),
 ("Which workflow should we automate with an agent first?",
  "Choose the workflow that scores well on four axes: the process is well understood, the underlying data is governed and current, the value is visible to a business owner, and the failure mode is containable. Analytics and reporting usually satisfies all four, which is why conversational BI is the common first agent — it delivers real-time answers with full auditability and no write access."),
 ("What security controls does an agentic workflow require?",
  "At minimum: least-privilege tool access resolved per requesting user at call time, schema and allowlist validation of every tool call before execution, separation of untrusted retrieved content from instructions, input and output filtering at the gateway, runtime monitoring for anomalous action patterns, and an immutable audit trail of every plan, tool call, and outcome. Read-only defaults plus a tested kill switch should be in place before the first production run."),
]

EN_RENAMES = {
 "the-technology-landscape-in-early-2025": "What Did the Technology Landscape Look Like in Early 2025?",
 "architectural-patterns-and-implementation-strategies": "Which Architectural Patterns and Implementation Strategies Work?",
 "security-and-operational-considerations": "What Security and Operational Considerations Matter Most?",
}

EN = {"renames": EN_RENAMES, "sections": EN_SECTIONS, "faq": EN_FAQ,
      "excerpts": [
        "How to architect enterprise AI agents: the runtime, tool, and memory layers that make them dependable.",
        "Using AI scenario planning to stress-test supply chains before disruption hits.",
        "Demand sensing with AI: shortening the signal-to-decision loop in volatile markets."]}

ZHCN_RENAMES = {
 "2025年初的技术格局": "2025年初的技术格局是什么样的？",
 "架构模式与实施策略": "哪些架构模式与实施策略最有效？",
 "安全与运营考虑": "安全与运营上需要注意什么？",
}

ZHCN_FAQ = [
 ("企业软件中的智能体工作流是什么？",
  "智能体工作流是指软件智能体为达成既定目标，自行规划步骤、选择并调用工具、在环境变化时调整策略，并判断何时应当停止或上报的流程。它不同于传统自动化——后者按固定顺序执行，一旦环境偏离脚本就会中断。实践中的企业智能体工作流都是有边界的：智能体在明确的权限与阈值内运行，并在预设的决策点上报给具名的人工角色。"),
 ("智能体工作流与RPA有什么区别？",
  "RPA按预先设定的脚本和顺序执行，遇到异常就失败。智能体工作流在运行时做规划，从可用工具中做选择，能从意外状态中恢复，并能判断任务已完成或已超出自身权限。这种适应性正是智能体能处理非结构化输入和可变流程的原因，也正因如此，它需要RPA从未要求过的治理能力：权限管理、审计追踪与上报规则。"),
 ("企业应该给智能体多少自主权？",
  "够完成任务即可，不要再多。自主权应按后果来界定：可逆、低价值、内部使用的动作可以免审批执行；涉及资金、客户沟通或他人所依赖的数据记录的动作，则必须经人工确认。建议从只读起步，在经过审计的运行中验证可靠性后，再逐类放开操作权限。"),
 ("第一个用智能体自动化的工作流应该选哪个？",
  "选择在四个维度上都表现良好的流程：流程本身被充分理解、底层数据已受治理且是最新状态、价值对业务负责人清晰可见、失败模式可控。分析与报告类流程通常四个维度全部满足，这也是对话式BI常成为首个智能体的原因——它能提供带完整审计能力的实时答案，且不需要写入权限。"),
 ("智能体工作流需要哪些安全控制？",
  "至少包括：调用时按请求用户身份解析的最小权限工具访问、执行前对每个工具调用做模式与白名单校验、把检索到的不可信内容与指令明确分离、在网关做输入输出过滤、对异常动作模式做运行时监控，以及对每一次规划、工具调用与结果的不可篡改审计追踪。首次投入生产之前，还应落实只读默认值与经过演练的一键停止开关。"),
]

ZHCN = {"renames": ZHCN_RENAMES, "faq": ZHCN_FAQ,
        "excerpts": [
          "企业AI智能体的架构方法：让系统可靠的运行时、工具与记忆三层设计。",
          "用AI情景规划在供应链受扰动之前完成压力测试。",
          "用AI做需求感知，缩短波动市场中的信号到决策链路。"]}

ZHTW_RENAMES = {
 "2025年初的技術格局": "2025年初的技術格局是什麼樣的？",
 "架構模式与實施策略": "哪些架構模式與實施策略最有效？",
 "安全与營運考虑": "安全與營運上需要注意什麼？",
}

ZHTW_FAQ = [
 ("企業軟體中的智慧體工作流程是什麼？",
  "智慧體工作流程是指軟體智慧體為達成既定目標，自行規劃步驟、選擇並呼叫工具、在環境變化時調整策略，並判斷何時應停止或上報的流程。它不同於傳統自動化——後者依固定順序執行，一旦環境偏離腳本就會中斷。實務中的企業智慧體工作流程都是有邊界的：智慧體在明確的權限與門檻內運作，並在預設的決策點上報給具名的人員角色。"),
 ("智慧體工作流程與RPA有什麼不同？",
  "RPA按預先設定的腳本與順序執行，遇到例外就失敗。智慧體工作流程在執行時做規劃，從可用工具中做選擇，能從意外狀態中恢復，並能判斷任務已完成或已超出自身權限。這種適應性正是智慧體能處理非結構化輸入與多變流程的原因，也正因如此，它需要RPA從未要求過的治理能力：權限管理、稽核軌跡與上報規則。"),
 ("企業應該給智慧體多少自主權？",
  "夠完成任務即可，不要再多。自主權應按後果界定：可逆、低價值、內部使用的動作可以免核准執行；涉及資金、客戶溝通或他人所依賴的資料記錄的動作，則必須經人工確認。建議從唯讀起步，在經過稽核的執行中驗證可靠性後，再逐類放開操作權限。"),
 ("第一個用智慧體自動化的工作流程應該選哪一個？",
  "選擇在四個面向上都表現良好的流程：流程本身被充分理解、底層資料已受治理且為最新狀態、價值對業務負責人清晰可見、失敗模式可控。分析與報告類流程通常四個面向全部滿足，這也是對話式BI常成為首個智慧體的原因——它能提供具備完整稽核能力的即時答案，且不需要寫入權限。"),
 ("智慧體工作流程需要哪些安全控制？",
  "至少包括：呼叫時依請求使用者身分解析的最小權限工具存取、執行前對每個工具呼叫做結構描述與白名單校驗、把檢索到的不可信內容與指令明確分離、在閘道做輸入輸出過濾、對異常動作模式做執行時監控，以及對每一次規劃、工具呼叫與結果的不可竄改稽核軌跡。首次上線之前，還應落實唯讀預設值與經過演練的一鍵停止開關。"),
]

ZHTW = {"renames": ZHTW_RENAMES, "faq": ZHTW_FAQ,
        "excerpts": [
          "企業AI智慧體的架構方法：讓系統可靠的執行環境、工具與記憶三層設計。",
          "用AI情境規劃在供應鏈受擾動之前完成壓力測試。",
          "用AI做需求感知，縮短波動市場中的訊號到決策鏈路。"]}

if __name__ == "__main__":
    for lang, spec in (("en", EN), ("zh-CN", ZHCN), ("zh-TW", ZHTW)):
        b, a, n = apply(SLUG, lang, spec)
        print(f"{SLUG} {lang}: {b} -> {a}  [{', '.join(n)}]")
