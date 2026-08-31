#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb001_apply as A
from _gb001_apply import apply

SLUG = "agentic-rag-architecture-enterprise-knowledge"

# ------------------------------------------------------------------ EN
EN_SECTIONS = [
 ("how-does-agentic-rag-handle-permissions-and-access-control",
  "How Does Agentic RAG Handle Permissions and Access Control?",
  """<p>Permissions are the single most underestimated part of an agentic RAG build. The rule is simple to state and easy to break: the retrieval layer must inherit the access rights of the source system for the identity of the person asking. That means filtering <strong>before</strong> ranking, not after. If you retrieve broadly and then strip out documents the user may not see, you have already leaked: result counts, snippet text, and "no results because everything was filtered" are all information an attacker can probe with.</p>
<p>The practical pattern is permission-aware indexing. At ingest, every chunk is tagged with the access control list of its source document, and the retrieval query carries the caller's identity or group memberships as a mandatory filter. Three details decide whether this holds up. First, re-index when ACLs change — stale permission tags are the most common real-world leak, and they appear months after go-live when someone is reorganised. Second, cache keys must include the permission set; sharing evidence caches across users is a silent breach. Third, the agent's tool calls need their own scopes, so the planner cannot route around a document restriction by calling a SQL tool that reads the same data.</p>
<p>The cleanest way to get this right is to let the agent query through the same governed roles, row-level security, and column masking that a human analyst would use, rather than giving the agent a broad service account. When the retrieval layer sits on top of a semantic layer that already enforces entitlement, permissions stop being a separate project.</p>"""),

 ("what-does-agentic-rag-cost-at-enterprise-scale",
  "What Does Agentic RAG Cost at Enterprise Scale?",
  """<p>Agentic RAG costs more per question than single-pass RAG, and the multiple is driven by design choices you control. A simple lookup that routes straight to one retrieval pass and a short synthesis costs roughly the same as ordinary RAG. A multi-hop question that decomposes into three sub-questions, runs hybrid retrieval for each, re-ranks, synthesizes, and then runs a verification pass costs several times more — five to fifteen times is a normal range — because you are paying for planning tokens, multiple retrieval calls, a larger context window, and a second model invocation to check the answer.</p>
<p>Four levers bring that back down. Routing is the biggest: most organisations find that 60–80% of real questions are simple lookups, so a cheap classifier that sends only genuinely multi-step questions into the agentic loop cuts blended cost by more than half. Caching helps next — caching retrieved evidence for recurring sub-queries, invalidated on source updates, typically removes 30–50% of retrieval spend. Model selection matters: small models handle query classification and re-ranking at a fraction of the cost of a frontier model, which should be reserved for final synthesis. And capping loop iterations is essential, because an unbounded self-correction loop can silently multiply cost on the questions that are already failing.</p>
<p>The metric to manage is cost per <strong>trusted</strong> answer, not cost per query. Cheap answers that users re-ask, escalate, or ignore are more expensive than they look.</p>"""),

 ("which-failure-modes-break-agentic-rag-in-production",
  "Which Failure Modes Break Agentic RAG in Production?",
  """<ul>
<li><strong>Planning failure:</strong> the agent decomposes the question incorrectly and answers a different, easier question confidently. Detect it by reviewing the plan trace against the original question, not by reading the final answer.</li>
<li><strong>Retrieval failure:</strong> the plan is right but the evidence is wrong or missing — hybrid search returns topically similar but factually irrelevant chunks. Detect with a grounding score that measures how much of the answer is supported by cited spans.</li>
<li><strong>Scope failure:</strong> the agent reaches data the requester should not see, usually through a tool path rather than the document index. Detect with tool-level authorisation logs and periodic red-team queries.</li>
<li><strong>Verification theatre:</strong> the verifier shares the generator's model and context, so both make the same mistake and the check passes. Use independent checks instead — reconcile numbers against a direct warehouse query, and confirm that quoted text actually appears in the cited chunk.</li>
<li><strong>Stale index:</strong> documents change but embeddings do not, and the system answers confidently from superseded policy or pricing. Detect with freshness SLAs per source and a visible source timestamp on every answer.</li>
<li><strong>Loop thrash:</strong> the system retries without new information and burns budget before returning nothing. Cap iterations and fall back to an explicit "insufficient evidence" response.</li>
</ul>
<p>Every one of these has a detector and a fallback, and the fallback matters as much as the detector: a system that declines well is trusted, while a system that improvises is quietly abandoned.</p>"""),

 ("what-belongs-in-an-agentic-rag-evaluation-harness",
  "What Belongs in an Agentic RAG Evaluation Harness?",
  """<p>The evaluation harness is what turns agentic RAG from a demo into a service. It starts with a golden set of 100–500 questions drawn from real user logs rather than invented ones, each paired with a verified answer and the source citations that support it. Stratify the set by question class — simple lookup, multi-hop, aggregation, comparison over time — because an aggregate score will hide the failure of one class behind the success of the others, and that one class is usually the reason the deployment was commissioned.</p>
<p>Track six metrics. Faithfulness or grounding measures what share of the answer is supported by retrieved evidence. Retrieval precision and recall measure whether the right chunks were fetched at all. Answer correctness is graded against the verified answer, with a human rubric or a calibrated model judge. Refusal rate, split into correct and incorrect refusals, catches both over-cautious and over-confident behaviour. Latency at p50 and p95 shows what users actually experience. Cost per answered question keeps the economics honest.</p>
<p>Wire the harness into deployment as a gate: re-run it on every change to prompts, retrievers, chunking, or models, and block the release when grounding or correctness drops beyond a defined threshold. Then close the loop by adding every production failure to the golden set, so the harness improves as the system does.</p>"""),
]

EN_FAQ = [
 ("What is the difference between RAG and agentic RAG?",
  "Standard RAG retrieves relevant chunks once and passes them to a model to read. Agentic RAG adds a planning step that decomposes the question, tool use that lets the system query databases and APIs rather than only a vector index, and a verification loop that checks the draft answer against the evidence and retries when grounding is weak. The practical difference shows up on multi-step questions: standard RAG answers from whatever looks similar, while agentic RAG assembles evidence deliberately and can decline when the evidence is insufficient."),
 ("When is plain RAG good enough, and when do you need the agentic loop?",
  "Plain RAG is enough when questions are single-hop lookups — a definition, a policy clause, one metric from one table. You need the agentic loop when the question spans sources or requires decomposition, such as explaining a margin variance across regions or comparing a contract term against delivered performance. The cost-effective design routes simple questions through the fast path and sends only genuinely multi-step questions into the loop."),
 ("How much does agentic RAG actually improve answer accuracy?",
  "On multi-hop questions, published retrieval-evaluation work on agentic loops with self-correction reports faithfulness improvements in the 25–40% range over single-shot retrieval. The gain is smaller on simple lookups, where both approaches perform similarly, which is why routing matters: the improvement is concentrated exactly where the extra cost is justified."),
 ("How long does it take to deploy agentic RAG over enterprise data?",
  "A focused deployment on one question class typically takes eight to twelve weeks: two to three weeks to connect the governed data sources and semantic layer, three to four weeks to build the planning, retrieval, and verification pipeline, and the remainder to build the golden-set evaluation harness and tune grounding. Organisations that already have a semantic layer move faster because the retrieval target is defined; those that must first model their metrics should budget for that as a separate workstream."),
 ("Does agentic RAG require rebuilding our data warehouse or knowledge base?",
  "No. Agentic RAG sits on top of what you already have. Documents are indexed where they live, and structured questions are answered by querying the warehouse or semantic layer through the same roles and security policies a human analyst would use. The work is in the retrieval, grounding, and evaluation layers — not in migrating data. The one prerequisite is that access control must be enforceable at query time, which usually means consolidating entitlements rather than rebuilding storage."),
]

EN_RENAMES = {
 "understanding-the-current-technology-landscape": "What Does the Current Agentic RAG Landscape Look Like?",
 "technical-architecture-and-integration-patterns": "Which Technical Architecture and Integration Patterns Work Best?",
 "performance-benchmarks-and-optimization-strategies": "How Do You Benchmark and Optimize Agentic RAG Performance?",
}

EN = {"renames": EN_RENAMES, "sections": EN_SECTIONS, "faq": EN_FAQ,
      "excerpts": [
        "How to architect enterprise AI agents: the runtime, tool, and memory layers that make them dependable.",
        "Using AI scenario planning to stress-test supply chains before disruption hits.",
        "Demand sensing with AI: shortening the signal-to-decision loop in volatile markets."]}

# ------------------------------------------------------------------ zh-CN
ZHCN_RENAMES = {
 "理解当前技术格局": "当前智能体RAG的技术格局是怎样的？",
 "技术架构与集成模式": "哪些技术架构与集成模式最有效？",
 "性能基准与优化策略": "如何做智能体RAG的性能基准与优化？",
 "企业部署最佳实践与实施建议": "企业部署有哪些最佳实践与实施建议？",
 "企业实施路线图与成功因素": "企业实施路线图与关键成功因素是什么？",
 "战略实施路径与关键成功因素": "战略实施路径应如何设计？",
 "企业实施路线图与成功因素-2": "企业实施路线图中最容易被忽略的是什么？",
}

ZHCN_FAQ = [
 ("智能体RAG与传统RAG有什么区别？",
  "传统RAG只做一次检索，把相关片段交给模型阅读后作答。智能体RAG增加了三个环节：规划环节把问题拆解为子问题；工具调用让系统能查询数据库和API，而不只是向量索引；验证环节把草稿答案与证据核对，证据不足时改写检索并重试。差异主要体现在多步问题上——传统RAG只能依据相似片段作答，而智能体RAG会有意识地拼装证据，并在证据不足时明确拒答。"),
 ("什么时候普通RAG就够用，什么时候需要智能体循环？",
  "如果问题属于单跳查询——一个定义、一条政策条款、一张表里的一个指标——普通RAG完全够用。当问题跨数据源或需要拆解时，比如解释各区域利润率差异、或把合同条款与实际交付表现对比，就需要智能体循环。成本最优的做法是设置路由：简单问题走快速通道，只有真正的多步问题才进入循环。"),
 ("智能体RAG能把答案准确率提升多少？",
  "在多跳问题上，检索评估领域关于带自我修正的智能体循环的研究显示，忠实度相比单轮检索提升约25%到40%。在简单查询上提升很小，两种方案表现接近，这也正是路由机制重要的原因：改进恰好集中在值得付出额外成本的那一类问题上。"),
 ("在企业数据上部署智能体RAG需要多久？",
  "针对单一问题类别的聚焦部署通常需要8到12周：2到3周接入受治理的数据源与语义层，3到4周搭建规划、检索与验证流水线，其余时间用于构建黄金集评估体系和调优接地效果。已有语义层的企业进度更快，因为检索目标已经定义清楚；还需要先梳理指标体系的组织，应把建模工作作为独立工作流另行排期。"),
 ("智能体RAG是否需要重建数据仓库或知识库？",
  "不需要。智能体RAG构建在现有资产之上：文档在原地建立索引，结构化问题通过查询数据仓库或语义层来回答，并且沿用与人类分析师相同的角色与安全策略。工作集中在检索、接地与评估层，而不是数据迁移。唯一的先决条件是访问控制必须能在查询时生效，这通常意味着要整合权限体系，而不是重建存储。"),
]

ZHCN = {"renames": ZHCN_RENAMES, "faq": ZHCN_FAQ,
        "excerpts": [
          "企业AI智能体的架构方法：让系统可靠的运行时、工具与记忆三层设计。",
          "用AI情景规划在供应链受扰动之前完成压力测试。",
          "用AI做需求感知，缩短波动市场中的信号到决策链路。"]}

# ------------------------------------------------------------------ zh-TW (converted)
import _gb001_s2t as T

ZHTW = T.spec_s2tw(ZHCN)

if __name__ == "__main__":
    for lang, spec in (("en", EN), ("zh-CN", ZHCN), ("zh-TW", ZHTW)):
        b, a, n = apply(SLUG, lang, spec)
        print(f"{SLUG} {lang}: {b} -> {a}  [{', '.join(n)}]")
