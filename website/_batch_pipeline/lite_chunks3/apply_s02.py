# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch
from opencc import OpenCC

ROOT = '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website'
SLUG = 'preventing-ai-hallucinations-enterprise'

EN_TOC = [
    ('what-causes-ai-hallucinations-in-enterprise-systems', 'What Causes AI Hallucinations in Enterprise Systems?'),
    ('why-are-hallucinations-more-dangerous-in-the-enterprise', 'Why Are Hallucinations More Dangerous in the Enterprise Than in Consumer Chat?'),
    ('how-do-you-ground-an-ai-system-in-enterprise-data', 'How Do You Ground an AI System in Enterprise Data?'),
    ('which-guardrails-actually-reduce-hallucinations-at-scale', 'Which Guardrails Actually Reduce Hallucinations at Scale?'),
    ('how-should-you-measure-and-monitor-hallucination-rates', 'How Should You Measure and Monitor Hallucination Rates?'),
    ('what-does-a-hallucination-resistant-architecture-look-like', 'What Does a Hallucination-Resistant Architecture Look Like?'),
]

EN_PROSE = """
<p class="article-lead"><strong>An AI hallucination in a consumer chat window is an annoyance. The same failure inside an enterprise workflow is a decision, a customer commitment, or a regulatory filing — and it carries the full authority of your brand.</strong> That asymmetry is why hallucination control has moved from a research curiosity to a board-level concern in 2025. The good news is that most enterprise hallucinations are not mysterious model failures. They are predictable consequences of missing context, ambiguous grounding data, weak retrieval, and the absence of a mechanism that lets the system say "I don't know". This article breaks down where hallucinations come from in production systems, which defences actually work, and how to build the measurement layer that keeps the problem from returning after you have fixed it once.</p>
<h2 id="what-causes-ai-hallucinations-in-enterprise-systems">What Causes AI Hallucinations in Enterprise Systems?</h2>
<p>A hallucination is a fluent, confident output that is not supported by the information the system was supposed to use. It is worth being precise about that definition, because it separates three very different failure classes that enterprises routinely lump together. The first is factual fabrication: the model invents a figure, a policy clause, or a customer record that does not exist. The second is misattribution: the model uses real information but attaches it to the wrong entity, period, or product. The third is stale confidence: the model answers correctly according to last quarter's truth, which is now wrong.</p>
<p>In enterprise deployments, the dominant cause is not the model's training. It is context failure. The model was asked a question it had no data to answer, and instead of declining it produced the most plausible completion. That happens for four structural reasons: retrieval returned nothing relevant, retrieval returned the wrong chunk, the retrieved data was correct but the question was ambiguous, or the prompt gave the model no licensed way to abstain.</p>
<p>Data quality is the second root cause, and it is the one enterprises underestimate. If your warehouse holds four definitions of "active customer" and two versions of the same revenue table, the model will pick one and state it flatly. Research consistently attributes a large share of analytics rework to poor data quality, and generative AI does not reduce that tax — it launders it, presenting contradictory source data as one confident answer. This is the same problem that makes data mesh and data-product work a prerequisite rather than a nicety: a model cannot be more accurate than the semantics it is allowed to read.</p>
<p>The third cause is prompt and orchestration design. Instructions that invite elaboration ("provide a comprehensive answer with context") push models to fill gaps with plausible narrative. Systems with no citation requirement let fabrication pass unnoticed. Agents with broad tool access and no verification step chain a small error into a large one. In most post-incident reviews we run, the model itself is the least guilty component.</p>
<h2 id="why-are-hallucinations-more-dangerous-in-the-enterprise">Why Are Hallucinations More Dangerous in the Enterprise Than in Consumer Chat?</h2>
<p>Consumer users approach AI output with a healthy degree of scepticism and a low cost of being wrong: they ask for a recipe, get a bad one, and move on. Enterprise users operate under three conditions that invert this. First, the output is embedded in a workflow, so it is acted upon rather than read. Second, the output is branded, internally trusted, and often presented alongside company data, which transfers the authority of the data to the answer. Third, errors propagate downstream into reports, filings, and customer communications, where detection happens weeks later and attribution is nearly impossible.</p>
<p>Consider a claims assistant that fabricates a policy exclusion. The adjuster denies a legitimate claim, the customer escalates, and the regulator eventually asks how the decision was made. Or a sales assistant that invents a discount threshold; the deal is quoted, signed, and margin-eroding before anyone checks. In both cases the technical error is small and the business consequence is not. The cost of a hallucination is not the cost of being wrong; it is the cost of being wrong at scale, inside a process, with an audit trail that points back at you.</p>
<p>There is also a second-order cost that is easier to miss: trust collapse. Enterprise AI adoption depends on users believing the system. A handful of visible fabrications will suppress adoption for a year, regardless of the accuracy improvements that follow. Teams that launch without abstention behaviour and citations tend to burn their credibility budget early and spend the rest of the programme trying to earn it back.</p>
<h2 id="how-do-you-ground-an-ai-system-in-enterprise-data">How Do You Ground an AI System in Enterprise Data?</h2>
<p>Grounding means constraining generation to a defined, governed body of evidence, and making the system show its work. In practice there are five layers, and they are cumulative — each one closes a gap the previous one leaves open.</p>
<ol>
<li><strong>Define the answerable set.</strong> Decide which questions the system is permitted to answer and which must be refused. Scope discipline prevents more hallucinations than any model upgrade.</li>
<li><strong>Connect a governed retrieval layer.</strong> Point retrieval at curated data products with agreed definitions, not at raw tables. Lineage and semantics are what make an answer defensible.</li>
<li><strong>Require citations.</strong> Every factual claim in the answer must reference a retrievable source. If the model cannot cite it, the answer must not ship.</li>
<li><strong>Structure the output.</strong> Ask for a defined schema — value, unit, period, source, confidence — rather than free prose. Structured answers are checkable; prose is not.</li>
<li><strong>Verify before returning.</strong> Run a cheap deterministic check against the source system: does the returned number reconcile with the query that produced it?</li>
</ol>
<p>The retrieval layer deserves the most attention, because it is where most enterprise RAG systems are weakest. Naive chunking splits documents at arbitrary boundaries, so retrieval returns half a policy and the model completes the other half from prior belief. Semantic chunking aligned to document structure, metadata filtering by product line and time period, and hybrid keyword-plus-vector search each remove a distinct failure mode. Equally important is freshness: retrieval must know which version of the truth applies to a question asked today, which means the catalogue — not the model — owns the recency decision.</p>
<p>This is also where conversational analytics earns its place. When a business user asks a question in WeCom, DingTalk, Feishu, Teams, or WhatsApp and the system answers from live governed data with the source attached, the hallucination surface collapses: there is no gap between the question and the system of record for the model to fill in. At Beehive Strategy we deploy exactly this pattern as a managed service in about two weeks, connecting to the warehouse you already run rather than rebuilding it, because the fastest way to reduce fabrication is to remove the opportunity.</p>
<h2 id="which-guardrails-actually-reduce-hallucinations-at-scale">Which Guardrails Actually Reduce Hallucinations at Scale?</h2>
<p>Not all defences are equal. Some reduce hallucinations meaningfully; others produce compliance theatre. The table below scores the common techniques against what we observe in production.</p>
<table class="article-table"><thead><tr><th>Technique</th><th>What it prevents</th><th>Implementation cost</th><th>Effectiveness</th></tr></thead><tbody><tr><td>Scope definition and refusal policy</td><td>Answers to questions the system has no data for</td><td>Low</td><td>High</td></tr><tr><td>Governed retrieval over curated data products</td><td>Conflicting definitions, stale truth</td><td>Medium</td><td>High</td></tr><tr><td>Mandatory citation and source display</td><td>Undetected fabrication</td><td>Low</td><td>High</td></tr><tr><td>Structured output with typed fields</td><td>Unit, period and entity confusion</td><td>Low</td><td>Medium-High</td></tr><tr><td>Deterministic post-verification</td><td>Arithmetic and reconciliation errors</td><td>Medium</td><td>High</td></tr><tr><td>Confidence thresholds and abstention</td><td>Low-evidence answers presented as fact</td><td>Medium</td><td>Medium-High</td></tr><tr><td>Human-in-the-loop for high-impact actions</td><td>Downstream business damage</td><td>High</td><td>High (for the actions covered)</td></tr><tr><td>Prompt wording alone ("be accurate")</td><td>Nothing measurable</td><td>Very low</td><td>Very low</td></tr><tr><td>Generic disclaimers</td><td>Nothing; shifts liability language only</td><td>Very low</td><td>Very low</td></tr></tbody></table>
<p>Two entries in that table deserve emphasis. Abstention is the single most under-used control: a system that says "I don't have governed data on that" is more useful than one that guesses, because it tells the user what to fix. And post-verification is what separates a demo from a production system — a deterministic reconciliation check catches the class of errors that language models make reliably and that no amount of prompt engineering eliminates.</p>
<p>Guardrails also need to be graded by consequence. A low-impact answer can ship with a citation and a confidence label. A high-impact action — approving credit, denying a claim, committing price — should require human confirmation regardless of how confident the system appears. Calibrating oversight to consequence, not to confidence, is the design principle that keeps governance proportionate.</p>
<h2 id="how-should-you-measure-and-monitor-hallucination-rates">How Should You Measure and Monitor Hallucination Rates?</h2>
<p>You cannot control what you do not measure, and hallucination rates are measurable if you design for it. Start with a golden set: two hundred to five hundred real questions with verified answers, drawn from the domains the system actually serves, each labelled with the source that justifies it. Run that set on every change — model version, prompt revision, retrieval tuning, data refresh — and track four metrics: answer accuracy against the verified answer, citation correctness (is the cited source the one that supports the claim?), abstention precision (did the system refuse when it should have?) and abstention rate overall.</p>
<p>Abstention metrics are the ones most teams omit, and they are diagnostic. A falling abstention rate with flat accuracy usually means the system has become more willing to guess, which is the early warning sign of a future incident. A rising abstention rate usually means retrieval has regressed or the underlying data products have drifted. Both are actionable in a way that a single accuracy number is not.</p>
<p>In production, complement the golden set with live signals. Track the share of answers that carry a citation, the share of conversations where the user re-asks the same question in different words (a strong implicit signal that the first answer failed), explicit thumbs-down rates, and the frequency with which users export an answer to verify it elsewhere. Then close the loop: every flagged answer becomes a reviewed case, every confirmed hallucination becomes a new golden-set item, and every recurring class of error gets traced to its root cause in data, retrieval, or prompt — not simply patched at the output layer.</p>
<ul>
<li><strong>Baseline before launch.</strong> Record accuracy, citation correctness, and abstention behaviour on the golden set before a single user sees the system.</li>
<li><strong>Gate every change.</strong> No model, prompt, or retrieval change ships without a golden-set run and a comparison against the baseline.</li>
<li><strong>Monitor drift monthly.</strong> Data changes silently; retrieval quality moves with it. Re-run the full set on a schedule, not only on releases.</li>
<li><strong>Trace, do not patch.</strong> Classify each incident by root cause and fix the layer that produced it.</li>
<li><strong>Report to the business.</strong> Publish accuracy and abstention trends to stakeholders; trust is maintained by transparency, not by perfection.</li>
</ul>
<h2 id="what-does-a-hallucination-resistant-architecture-look-like">What Does a Hallucination-Resistant Architecture Look Like?</h2>
<p>A hallucination-resistant architecture is less exotic than it sounds. It has a governed data layer at the bottom — data products with owners, definitions, lineage, and access control. It has a retrieval layer that respects those semantics and knows which version of the truth to serve. It has an orchestration layer that defines scope, requires citations, enforces structured output, and permits abstention. It has a verification layer that reconciles answers against source systems before they are shown. And it has a measurement layer that turns every failure into a regression test.</p>
<p>The sequencing matters as much as the components. Teams that start with the model and work downwards tend to build impressive demos that cannot be trusted in production. Teams that start with the data layer and work upwards build slower at first, then accelerate, because every subsequent layer rests on something that already has an owner and a definition. This is the same ordering discipline that separates successful data mesh programmes from stalled ones: govern first, expose to AI second, scale third.</p>
<p>One more practical note on rollout. Hallucination control is easier to sustain when the first deployment is narrow and instrumented rather than broad and impressive. Pick a single domain where the answer is checkable — a finance reconciliation question, an inventory position, a policy lookup — and where a wrong answer is visible quickly. Ship with citations and abstention switched on from day one, even if that means the system declines a fifth of early questions, because that fifth is your roadmap. Then widen the answerable set deliberately, one data product at a time, as retrieval quality and definition coverage improve.</p>
<p>Finally, design the user experience for fallibility. Show the source. Show the freshness of the data behind the answer. Make it one tap to escalate to a human. Give users a clear way to say "this is wrong" and a visible acknowledgement when they do. Systems that admit uncertainty are trusted more, not less — and in enterprise deployment, trust is the difference between a tool people use and a tool they were told to use. Start with one high-value domain, instrument it properly, prove the hallucination rate is acceptable, and then expand. That is how you get accurate AI answers that survive contact with real business decisions.</p>
"""

EN_FAQ = [
    ("What is an AI hallucination in an enterprise context?",
     "It is a fluent, confident output that is not supported by the data the system was supposed to use. In enterprises it appears in three forms: factual fabrication (inventing a figure, clause or record), misattribution (real information attached to the wrong entity or period), and stale confidence (an answer that was correct for last quarter's truth). Each has a different root cause and a different fix."),
    ("Can prompt engineering alone prevent hallucinations?",
     "No. Prompt wording changes tone and formatting but does not give the model access to missing data, and it cannot reliably stop fabrication when retrieval has failed. The controls that measurably reduce hallucinations are governance-side: a defined answerable scope, retrieval over curated data products, mandatory citations, structured output, deterministic post-verification, and an explicit abstention path."),
    ("How do we measure our hallucination rate?",
     "Build a golden set of a few hundred real questions with verified, sourced answers, then run it on every model, prompt, retrieval and data change. Track answer accuracy, citation correctness, abstention precision, and overall abstention rate. In production, complement this with live signals such as citation coverage, re-ask rate, and explicit user feedback, and convert every confirmed failure into a new golden-set item."),
    ("Should the system ever refuse to answer?",
     "Yes, and it should be designed to. Abstention is the most under-used hallucination control: an answer of \"I do not have governed data on that\" is more valuable than a plausible guess because it tells the user what to fix. Track abstention precision alongside accuracy, because a falling abstention rate with flat accuracy usually means the system has simply become more willing to guess."),
    ("How does retrieval-augmented generation reduce hallucinations?",
     "RAG constrains generation to a defined evidence set and lets the system cite its sources, which removes the gap the model would otherwise fill from prior belief. It only works when the retrieval layer is trustworthy: curated data products with agreed definitions, structure-aware chunking, metadata filtering, hybrid search, and freshness awareness. Poor RAG over ungoverned data can make hallucinations harder to detect, not less likely."),
]

ZH_TOC = [
    ('企业系统中的AI幻觉由什么造成', '企业系统中的 AI 幻觉由什么造成？'),
    ('为什么幻觉在企业环境中比在消费级聊天中更危险', '为什么幻觉在企业环境中比在消费级聊天中更危险？'),
    ('如何让AI系统在企业数据上获得可靠依据', '如何让 AI 系统在企业数据上获得可靠依据？'),
    ('哪些护栏能在规模化下真正减少幻觉', '哪些护栏能在规模化下真正减少幻觉？'),
    ('应当如何衡量与监控幻觉率', '应当如何衡量与监控幻觉率？'),
    ('抗幻觉的企业级架构长什么样', '抗幻觉的企业级架构长什么样？'),
]

ZH_PROSE = """
<p class="article-lead"><strong>在消费级聊天窗口里，AI 幻觉只是个小麻烦；同样的失败发生在企业工作流内部，就变成了一个决策、一项对客户的承诺或一份监管报送文件——而且它带着你品牌的全部权威。</strong>正是这种不对称，让幻觉治理在 2025 年从研究趣闻上升为董事会级议题。好消息是：企业级的大多数幻觉并不是神秘的模型失灵，而是上下文缺失、依据数据含混、检索薄弱，以及系统缺少"我不知道"这条退路所导致的必然结果。本文拆解生产系统中幻觉的来源、真正奏效的防御手段，以及如何建立度量层，让问题在你修好一次之后不会卷土重来。</p>
<h2 id="企业系统中的AI幻觉由什么造成">企业系统中的 AI 幻觉由什么造成？</h2>
<p>AI 幻觉指的是：一段流畅而自信的输出，并不被它本应依据的信息所支持。这个定义值得精确，因为它把企业里习惯混为一谈的三类失败区分开了。第一类是事实捏造：模型编造了一个数字、一条政策条款或一条根本不存在的客户记录。第二类是归因错误：模型用的是真实信息，却把它安在了错误的主体、期间或产品上。第三类是过期自信：模型按上一季度的真相给出了"正确"答案，而那个真相现在已经变了。</p>
<p>在企业部署中，主因并不是模型的训练，而是上下文失败。模型被问到一个它没有任何数据可以回答的问题，于是它没有选择拒答，而是产出了最"像样"的续写。导致这种情形的结构性原因有四个：检索没有返回任何相关内容；检索返回了错误的片段；检索到的数据是对的，但问题本身有歧义；或者，提示词没有给模型任何被许可的弃权方式。</p>
<p>数据质量是第二个根因，也是企业最容易低估的一个。如果你的仓库里存在四种"活跃客户"的定义、同一张收入表的两个版本，模型会挑一种并斩钉截铁地陈述出来。研究反复表明，分析工作中的大量返工源自数据质量低下；生成式 AI 并没有降低这笔税，而是把它"洗白"了——把互相矛盾的源数据包装成一个自信的答案。这也正是为什么数据网格与数据产品的工作是前置条件而非锦上添花：模型不可能比它被允许读取的语义更准确。</p>
<p>第三个成因是提示词与编排设计。那些鼓励展开的指令——"请给出一个全面的、带背景的回答"——会推动模型用看似合理的叙述去填补空白；没有引用要求的系统会让捏造毫无阻碍地通过；工具权限过宽且缺少校验环节的 Agent，会把一个小错误串成一个大错误。在我们做过的大多数事后复盘里，模型本身往往是责任最轻的那一环。</p>
<h2 id="为什么幻觉在企业环境中比在消费级聊天中更危险">为什么幻觉在企业环境中比在消费级聊天中更危险？</h2>
<p>消费级用户带着天然的怀疑来使用 AI，而且犯错的代价很低：问个菜谱，得到一份难吃的，翻篇就过去了。企业用户面对的三个条件恰好把这一切反转过来。第一，输出嵌在工作流里，因此它是被"执行"的，而不只是被"阅读"的。第二，输出带着品牌、在内部被信任，而且常常与公司数据并列展示，数据的权威因此转移到了答案上。第三，错误会向下游传播到报表、报送文件和客户沟通中，几周后才被发现，到那时几乎无法归因。</p>
<p>设想一个理赔助手捏造了一条免责条款：核赔员据此拒赔了一位合理索赔的客户，客户升级投诉，监管最终来问这个决策是怎么做出的。再设想一个销售助手编造了一个折扣阈值：报价发出、合同签下、利润被侵蚀，之后才有人去核对。两例中技术错误都很小，业务后果却并不小。幻觉的代价不是"答错"的代价，而是"在流程中、规模化地、带着一条最终指向你的审计轨迹答错"的代价。</p>
<p>还有一种二阶成本更容易被忽略：信任崩塌。企业 AI 的采用取决于用户是否相信这个系统。几次肉眼可见的捏造，就足以压制一年的采用率，无论之后准确率提升多少。那些在上线时没有弃权机制、没有引用展示的团队，往往早早烧光了自己的信誉预算，剩下的项目周期都在试图把它赚回来。</p>
<h2 id="如何让AI系统在企业数据上获得可靠依据">如何让 AI 系统在企业数据上获得可靠依据？</h2>
<p>"有据可依"意味着把生成过程约束在一个明确且受治理的证据集合内，并要求系统展示它的推理依据。实践中有五个层次，它们是叠加关系——每一层都在补上前一层的缺口。</p>
<ol>
<li><strong>划定可回答集合。</strong>明确哪些问题允许系统回答、哪些必须拒绝。范围纪律比任何模型升级都能防止更多幻觉。</li>
<li><strong>接入受治理的检索层。</strong>让检索指向定义一致的、经过整理的数据产品，而不是原始表。血缘与语义才是答案站得住脚的原因。</li>
<li><strong>强制引用。</strong>答案中的每一条事实性陈述都必须指向一个可取回的来源；模型引不出来，这个答案就不能发出去。</li>
<li><strong>结构化输出。</strong>要求一个既定 schema——数值、单位、期间、来源、置信度——而不是自由散文。结构化答案可校验，散文不可校验。</li>
<li><strong>返回前先校验。</strong>对源系统跑一次廉价的确定性检查：这个返回值与生成它的查询是否对得上？</li>
</ol>
<p>检索层最值得投入，因为多数企业的 RAG 系统恰恰在这里最薄弱。朴素的切分把文档在任意位置切开，检索因此只返回了半份政策，剩下半份由模型凭先验补全。按文档结构做语义切分、按产品线与时间区间做元数据过滤、以及"关键词 + 向量"的混合检索，各自消除一种不同的失败模式。新鲜度同样重要：检索必须知道，对于今天提出的这个问题，适用的是哪一版真相——而这个"新旧"判断应当由目录来掌握，而不是模型。</p>
<p>这也正是对话式分析的价值所在。当业务用户在企业微信、钉钉、飞书、Teams 或 WhatsApp 里提问，而系统从实时的受治理数据中作答并附上来源时，幻觉的暴露面就塌缩了：问题与记录系统之间不存在可供模型填补的空隙。蜂启咨询正是以托管服务方式部署这一模式，约两周即可上线，对接的是你已经在跑的仓库而非重建它——因为减少捏造最快的方式，是让捏造没有机会发生。</p>
<h2 id="哪些护栏能在规模化下真正减少幻觉">哪些护栏能在规模化下真正减少幻觉？</h2>
<p>并非所有防御手段都等价。有些能显著减少幻觉，有些只是合规表演。下表按我们在生产环境中观察到的情况，为常见手法打分。</p>
<table class="article-table"><thead><tr><th>手法</th><th>能防住什么</th><th>实施成本</th><th>有效性</th></tr></thead><tbody><tr><td>范围界定与拒答策略</td><td>对系统本无数据的问题作答</td><td>低</td><td>高</td></tr><tr><td>基于整理后数据产品的受治理检索</td><td>定义冲突、真相过期</td><td>中</td><td>高</td></tr><tr><td>强制引用与来源展示</td><td>未被发现的捏造</td><td>低</td><td>高</td></tr><tr><td>带类型字段的结构化输出</td><td>单位、期间与主体的混淆</td><td>低</td><td>中高</td></tr><tr><td>确定性后置校验</td><td>算术与对账错误</td><td>中</td><td>高</td></tr><tr><td>置信度阈值与弃权</td><td>把证据不足的答案当作事实呈现</td><td>中</td><td>中高</td></tr><tr><td>高影响动作的人工复核</td><td>下游业务损失</td><td>高</td><td>高（仅限被覆盖的动作）</td></tr><tr><td>仅靠提示词措辞（"请务必准确"）</td><td>无可测量的效果</td><td>极低</td><td>极低</td></tr><tr><td>笼统免责声明</td><td>无实际效果，只转移责任措辞</td><td>极低</td><td>极低</td></tr></tbody></table>
<p>表中有两项值得强调。其一是弃权：它是最被低估的一个控制项。一个会说"这方面我没有受治理的数据"的系统，比一个会瞎猜的系统更有用，因为它告诉用户该去补什么。其二是后置校验：它正是演示系统与生产系统的分界线——一次确定性的对账检查，能抓住语言模型必然会犯、而任何提示工程都消除不了的那类错误。</p>
<p>护栏还需要按后果分级。低影响的答案，带引用和置信度标签就可以放行；高影响的动作——批准授信、拒赔、承诺价格——无论系统显得多么自信，都应当要求人工确认。把审核力度对齐到后果而不是置信度，正是让治理保持相称的设计原则。</p>
<h2 id="应当如何衡量与监控幻觉率">应当如何衡量与监控幻觉率？</h2>
<p>无法度量就无法控制；只要设计得当，幻觉率是可度量的。先建一个"黄金集"：从系统真正服务的领域中抽取两百到五百个真实问题，每题都配有经过核实的答案，并标注支撑该答案的来源。每次变更——模型版本、提示词修订、检索调优、数据刷新——都跑一遍这个集合，并跟踪四项指标：对照标准答案的回答准确率、引用正确性（被引用的来源是否真的支撑该陈述？）、弃权精确度（系统在该拒的时候拒了吗？）以及总体弃权率。</p>
<p>弃权指标是多数团队会漏掉的，而它恰恰具有诊断价值。弃权率下降而准确率持平，通常意味着系统变得更敢于猜测，这正是未来事故的早期信号；弃权率上升，通常意味着检索退化了，或底层数据产品发生了漂移。两者都比单看一个准确率数字更可执行。</p>
<p>在生产环境中，还要用实时信号补充黄金集：带引用的答案占比、用户换一种说法重问同一问题的比例（这是首次回答失败的强隐式信号）、明确的点踩率，以及用户把答案导出到别处核实的频率。然后闭合回路：每一个被标记的答案都进入人工复核，每一个被确认的幻觉都成为一条新的黄金集条目，每一类反复出现的错误都追溯到它在数据、检索或提示词中的根因——而不是只在输出层打补丁。</p>
<ul>
<li><strong>上线前先建基线。</strong>在任何一个用户看到系统之前，就在黄金集上记录准确率、引用正确性与弃权行为。</li>
<li><strong>每次变更都设卡。</strong>任何模型、提示词或检索的改动，都必须跑一遍黄金集并与基线对比后才能发布。</li>
<li><strong>按月监控漂移。</strong>数据在无声地变，检索质量随之而动。按计划定期全量重跑，而不是只在发版时跑。</li>
<li><strong>追溯而非打补丁。</strong>按根因给每起事故分类，修复产生它的那一层。</li>
<li><strong>向业务侧汇报。</strong>把准确率与弃权趋势发给干系人；信任靠透明维持，而不是靠完美。</li>
</ul>
<h2 id="抗幻觉的企业级架构长什么样">抗幻觉的企业级架构长什么样？</h2>
<p>抗幻觉架构听起来玄，其实并不复杂。最底层是受治理的数据层：数据产品，有负责人、有定义、有血缘、有访问控制。其上是尊重这些语义、并知道该提供哪一版真相的检索层。再上是编排层：界定范围、强制引用、约束结构化输出、允许弃权。然后是校验层：在答案展示之前与源系统对账。最后是度量层：把每一次失败转化为一条回归测试。</p>
<p>顺序与组件同样重要。从模型开始、向下推进的团队，往往能做出令人惊艳但无法在生产中信任的演示；从数据层开始、向上推进的团队起初慢一些，随后会加速，因为此后每一层都建立在已有负责人和定义的东西之上。这与区分成功与停滞的数据网格项目所遵循的顺序纪律是同一条：先治理，再向 AI 开放，然后才谈规模化。</p>
<p>最后，把用户体验也按"会犯错"来设计。展示来源，展示答案背后数据的新鲜度，让升级到人工只需一次点击。给用户一个清晰的"这是错的"按钮，并在他们按下时给出可见的回应。承认不确定性的系统反而更受信任——在企业部署中，信任正是"人们真的在用的工具"与"人们被要求去用的工具"之间的分野。从一个高价值领域起步，把它测好，证明幻觉率可接受，然后再扩张。这才是让准确的 AI 答案在真实业务决策面前站得住脚的方法。</p>
"""

ZH_FAQ = [
    ("在企业语境中，什么是 AI 幻觉？",
     "它指的是一段流畅而自信、却并不被其本应依据的数据所支持的输出。在企业中通常表现为三种形态：事实捏造（编造数字、条款或记录）、归因错误（真实信息被安在错误的主体或期间上）、以及过期自信（按上一季度真相给出的「正确」答案）。三者根因不同，修法也不同。"),
    ("仅靠提示词工程能防止幻觉吗？",
     "不能。提示词措辞能改变语气与格式，却无法给模型补上缺失的数据，也无法在检索失败时可靠地阻止捏造。可度量地减少幻觉的控制项都在治理侧：明确的可回答范围、基于整理后数据产品的检索、强制引用、结构化输出、确定性后置校验，以及一条明确的弃权路径。"),
    ("我们该如何衡量自己的幻觉率？",
     "建立一个黄金集：从真实业务中抽取数百个问题，每个都配上经过核实并标注来源的答案。此后每次模型、提示词、检索或数据的变更都跑一遍，跟踪回答准确率、引用正确性、弃权精确度与总体弃权率。在生产中再用实时信号补充：引用覆盖率、重问率、显式反馈，并把每一个被确认的失败转化为新的黄金集条目。"),
    ("系统应该拒答吗？",
     "应该，而且要主动设计拒答能力。弃权是最被低估的幻觉控制项：一句「这方面我没有受治理的数据」比一个看似合理的猜测更有价值，因为它告诉用户该去补什么。要把弃权精确度与准确率一起跟踪——弃权率下降而准确率持平，通常意味着系统只是变得更敢于猜测了。"),
    ("检索增强生成（RAG）是如何减少幻觉的？",
     "RAG 把生成过程约束在一个明确的证据集合内，并让系统引用来源，从而消除了模型原本会用先验去填补的空隙。它只有在检索层可信时才有效：定义一致的数据产品、按结构切分、元数据过滤、混合检索与新鲜度感知。在缺乏治理的数据上做粗糙的 RAG，可能让幻觉更难被发现，而不是更少发生。"),
]

cc = OpenCC('s2twp')
to_tw = cc.convert
TW_TOC = [(i, to_tw(t)) for i, t in ZH_TOC]

def main():
    patch.apply(os.path.join(ROOT, 'blog/articles/%s.html' % SLUG), EN_TOC, EN_PROSE, EN_FAQ,
                tail_h2='What Are the Key Takeaways for Enterprise Teams?', cta='Book a Demo')
    patch.apply(os.path.join(ROOT, 'zh-cn/blog/articles/%s.html' % SLUG), ZH_TOC, ZH_PROSE, ZH_FAQ,
                tail_h2='企业团队应当记住哪些关键结论？', cta='预约演示')
    patch.apply(os.path.join(ROOT, 'zh-tw/blog/articles/%s.html' % SLUG), TW_TOC, to_tw(ZH_PROSE),
                [(to_tw(q), to_tw(a)) for q, a in ZH_FAQ],
                tail_h2=to_tw('企業團隊應當記住哪些關鍵結論？'), cta='預約示範')

if __name__ == '__main__':
    main()
