# -*- coding: utf-8 -*-
import re, os
import opencc

base = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = "vector-search-patterns-for-enterprise-knowledge-bases-a-2026-update"
cc = opencc.OpenCC('s2twp.json')

FAQ_SECTION = '''
<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">
                <h2 class="faq-section-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                    Frequently Asked Questions
                </h2>
                <div class="faq-list">
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">1</span><span>What is vector search and why does it matter for enterprise knowledge bases?</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">Vector search retrieves documents by meaning rather than exact keywords, turning text into embeddings and returning the closest matches. For enterprise knowledge bases — which are mostly unstructured, messy, and acronym-heavy — it is the retrieval backbone of trustworthy AI assistants, because a model that retrieves and cites real documents answers accurately instead of inventing plausible fiction.</div></div>
                    </div>
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">2</span><span>What is the difference between dense, sparse, and hybrid search?</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">Dense vectors capture meaning and handle paraphrases but can miss exact terms like product codes; sparse methods such as BM25 nail keyword precision but struggle with synonyms. Hybrid search fuses both and is the default for enterprise content that mixes prose and identifiers. Choose the fusion weight on a labeled set of real employee questions, not a public benchmark, and add a reranker to lift hard queries.</div></div>
                    </div>
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">3</span><span>How do you measure whether retrieval is actually working in production?</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">Measure on the questions employees actually ask, sampled weekly, not a fixed benchmark: check top-k recall with a human judge and whether the answer is correct, and track plausible-but-wrong returns and abandonment. A 100 to 300 question golden set re-run weekly catches chunking regressions and embedding drift before users do. If users stop rephrasing and start opening citations, retrieval is working.</div></div>
                    </div>
                </div>
            </section>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "What is vector search and why does it matter for enterprise knowledge bases?", "acceptedAnswer": {"@type": "Answer", "text": "Vector search retrieves documents by meaning rather than exact keywords, turning text into embeddings and returning the closest matches. For enterprise knowledge bases, which are mostly unstructured, messy, and acronym-heavy, it is the retrieval backbone of trustworthy AI assistants, because a model that retrieves and cites real documents answers accurately instead of inventing plausible fiction."}}, {"@type": "Question", "name": "What is the difference between dense, sparse, and hybrid search?", "acceptedAnswer": {"@type": "Answer", "text": "Dense vectors capture meaning and handle paraphrases but can miss exact terms like product codes; sparse methods such as BM25 nail keyword precision but struggle with synonyms. Hybrid search fuses both and is the default for enterprise content that mixes prose and identifiers. Choose the fusion weight on a labeled set of real employee questions, not a public benchmark, and add a reranker to lift hard queries."}}, {"@type": "Question", "name": "How do you measure whether retrieval is actually working in production?", "acceptedAnswer": {"@type": "Answer", "text": "Measure on the questions employees actually ask, sampled weekly, not a fixed benchmark: check top-k recall with a human judge and whether the answer is correct, and track plausible but wrong returns and abandonment. A 100 to 300 question golden set re-run weekly catches chunking regressions and embedding drift before users do. If users stop rephrasing and start opening citations, retrieval is working."}}]}</script>'''

ZH = '''<div class="toc-mobile" id="toc-mobile">
                <button class="toc-mobile-toggle" aria-expanded="false">目录 <svg class="toc-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
                <div class="toc-mobile-links">
                    <a href="#the-current-landscape" class="toc-mobile-link">当前格局是怎样的？</a>
                    <a href="#the-core-vector-search-patterns" class="toc-mobile-link">核心的向量搜索模式有哪些？</a>
                    <a href="#key-implementation-challenges" class="toc-mobile-link">关键的实施挑战有哪些？</a>
                    <a href="#how-do-you-know-your-retrieval-is-working" class="toc-mobile-link">你如何知道检索在起作用？</a>
                    <a href="#practical-approaches-that-work" class="toc-mobile-link">哪些实践方法真正有效？</a>
                    <a href="#key-takeaways" class="toc-mobile-link">关键要点</a>
                    <a href="#conclusion" class="toc-mobile-link">结论</a>
                    <a href="#how-do-you-choose-between-dense-sparse-and-hybrid" class="toc-mobile-link">你如何在稠密、稀疏与混合搜索之间选择？</a>
                    <a href="#how-do-you-evaluate-embedding-models" class="toc-mobile-link">你如何为你的语料评估嵌入模型？</a>
                    <a href="#what-is-the-role-of-a-vector-database-versus-search" class="toc-mobile-link">向量数据库与经典搜索各自的角色是什么？</a>
                    <a href="#how-do-you-measure-retrieval-in-production" class="toc-mobile-link">你如何在生产中衡量检索是否起作用？</a>
                </div>
            </div>
<p class="article-lead">每个企业AI助手的好坏，取决于它的检索。到了2026年，向量搜索是知识库问答背后的检索骨架，而一个有用助手与一个流畅的幻觉制造者之间的差别，不在模型，而在它周围的搜索模式。本文涵盖生产中有效的模式、悄悄降低质量的错误，以及如何为企业知识设计检索。</p>
<h2 id="the-current-landscape">当前格局是怎样的？</h2>
<p>检索增强生成（RAG）已成为企业AI的默认架构，到2026年大多数生产部署都依赖某种形式的向量搜索。原因在于 grounding：从组织自有文档中检索并引用它们的模型，能产生可被信任、审计和改进的答案。没有检索，同一个模型会编造看似合理的虚构。</p>
<p>数据是无情的。非结构化内容占企业数据的绝大部分，而知识库出了名地混乱——重复、版本漂移、缩略语和孤立文档的积累速度快于任何团队清理的速度。向量搜索比关键词搜索处理得更好，但只有当周围的模式——分块、元数据、混合排序、重排——被刻意设计时才会如此。2026年版的经典错误，是把向量库当作黑盒：嵌入是不透明的，无法解释为何某文档被检索到（或没被检索到）的团队，最终靠直觉调试；而成功的团队保持关键词信号、元数据和显式的分块来源可见，让每个检索决策都可被检视。</p>
<p>我们在亚太服务企业的经验显示同一条弧线：把检索当作一门学科而非一次库调用的团队，得到用户信任的助手；把它当作插件的团队，得到在第二周就失败、并被悄悄放弃的演示。</p>
<p>模型选择也比团队预期的更不重要。检索质量更多由语料准备、分块和排序模式驱动，而非由流行哪个嵌入模型驱动；在忽视分块的同时追逐模型升级的团队，是在打磨管道错误的一端。</p>
<h2 id="the-core-vector-search-patterns">核心的向量搜索模式有哪些？</h2>
<p>五种模式主导生产系统。混合搜索结合稠密嵌入与关键词及BM25匹配，通常在企业内容上比纯向量搜索提升20%–40%的检索质量。元数据过滤在排序前缩小搜索空间。分块策略控制文档如何被拆成可检索单元。重排把第二个、更强的模型应用于前几名候选。上下文组装决定模型在提示中实际看到什么。</p>
<p>上下文组装常常是好的检索系统与好的答案之间的差别：如果提示被无关文本挤满，检索到正确分块也毫无意义。控制上下文预算——多少分块、多少文本、什么顺序——的企业，始终比把所有东西倒进提示的企业看到更高的答案质量。</p>
<p>模式选择依赖于内容：法律文档需要带引用支持的条款感知分块；支持知识库需要带新鲜度加权的混合搜索；技术手册需要把图与其标题保留在一起的图像感知分块。没有普适的最佳模式——只有针对你的语料和用户真正会问的问题类型调优过的模式。</p>
<p>2026年值得关注的第六种模式是查询重写。企业问题常常是碎片、充满缩略语，或基于过时的知识库理解表述；在嵌入前结合上下文重写查询，对检索的提升不亚于任何排序改动，且实现成本低。</p>
<h2 id="key-implementation-challenges">关键的实施挑战有哪些？</h2>
<p>分块是第一个、也最被低估的挑战。被切到边界之外的文档，会产生任何模型都无法修复的检索遗漏；分块大小、重叠和感知结构的切分，必须对照真实问题的金标准集调优，而非猜测。分块也影响成本：更小的分块意味着更多检索调用和更多token，更大的分块则稀释相关性——正确大小取决于文档类型和问题粒度，唯一诚实的方法是对金标准集度量。</p>
<p>嵌入漂移是第二个。模型随新版本被重新嵌入，嵌入随语言和内容的改变而老化，混合版本的索引产生不一致的检索。企业需要重新嵌入流水线和版本化索引，而非一次性任务——否则索引会悄悄偏离它本应服务的内容。</p>
<p>第三个是评估。团队凭感觉判断检索；生产系统需要问答文档对的金标准集，用recall-at-k和答案级准确率度量，在每次变更时重跑。没有它，静默退化成为常态，信任在一次次错过的答案中慢慢侵蚀。</p>
<p>访问控制是随部署增长而增加的第四个挑战。企业知识库包含机密材料，检索必须在查询时——而不仅是在索引时——尊重权限；跳过权限感知检索的团队，会在第一次安全审查中发现泄漏。</p>
<h2 id="how-do-you-know-your-retrieval-is-working">你如何知道检索在起作用？</h2>
<p>当助手在固定评估集上的答案可衡量地改善、当用户不再改写问题、当答案记录显示引用被打开和核实时，你就知道检索在起作用。在我们的部署中，我们跟踪检索命中率、引用使用率，以及从知识回答的问题相对于诚实的"我不知道"回答的比例——最后一个是健康系统最清晰的信号。</p>
<p>建立信心的实用路径是一个小的金标准集——100到300个带已知好答案的真实问题——每周重跑。这样做的团队及早发现分块回退和嵌入漂移；跳过的团队在用户抱怨和放弃的会话中发现问题。</p>
<p>还要对用户体验做埋点：跟踪哪些答案被接受、哪些被重问、哪些问题完全没答案。最后一类是金矿——它显示知识库在哪里有检索无法弥补的缺口，以及内容策展下一步应聚焦何处。</p>
<h2 id="practical-approaches-that-work">哪些实践方法真正有效？</h2>
<p>从混合搜索和元数据过滤起步。它们是杠杆最高、风险最低的模式，能立即修复"问题与文档表述不同就检索不到有用内容"的经典失败。</p>
<p>让检索成为对话式、IM原生的。在我们的经验中，最快的采用来自用户在WeChat Work、钉钉、飞书、WhatsApp或Microsoft Teams中查询知识库，并收到带内联引用的答案——蜂启咨询作为管理服务在两周内部署的模式，语义层与检索由做过的人调优。</p>
<p>持续监控：金标准集上的检索质量、嵌入索引健康度与使用分析。从第一天起的自动监控，防止困扰众多知识库助手的逐渐退化。</p>
<p>最后，为内容卫生而非仅为基础设施预算。一个分块良好、去重、带权限标签的知识库，表现远优于一个更大但混乱的知识库；把策展当作持续职能而非一次性清理的团队，其助手才保持可靠。</p>
<h2 id="key-takeaways">关键要点</h2>
<ul>
<li>混合搜索（稠密+关键词）通常在企业内容上比纯向量搜索提升20%–40%的检索质量</li>
<li>非结构化内容占企业数据的绝大部分——知识库需要为混乱而设计的检索</li>
<li>针对语料调优分块：法律用条款感知，支持用新鲜度感知，手册用图像感知</li>
<li>对你的索引做版本化并重新嵌入；嵌入漂移会静默降低检索</li>
<li>维护一个100–300问题的金标准集，每周重跑</li>
<li>在现有IM工具中对话式地交付答案，内建引用与监控</li>
</ul>
<h2 id="conclusion">结论</h2>
<p>在2026年，一个受喜爱的知识助手与一个尴尬助手之间的差别，是检索，而非模型。混合搜索、调优的分块、重排与持续评估，把向量索引变成可信的企业能力。</p>
<p>围绕语料设计模式，对照金标准集度量，并在工作发生之处交付答案。刻意而为的检索，正是让企业AI值得部署的原因。</p>

<!--AUTOEXPAND-START-->
<h2 id="how-do-you-choose-between-dense-sparse-and-hybrid">你如何在稠密、稀疏与混合搜索之间选择？</h2>
<p>稠密向量捕捉含义、善于处理释义，但可能错过产品代码或法律条款等精确术语。稀疏方法——BM25与学习型稀疏——精准命中关键词，但苦于同义。混合搜索融合二者，通常用加权和或学习型排序器组合分数，对于企业知识库它是我们推荐的默认，因为内部内容混合了散文与标识符。选择不是哲学问题：在有标注的查询集（取自真实员工问题）上调权重，而非在公开基准上。</p>
<p>2026年的 refinement 是重排。一个便宜的双编码器检索几百个候选，然后一个交叉编码器对前十个重排以得到最终答案。这种两阶段模式保持低延迟，同时提升困难查询的相关性——那些朴素向量匹配返回看似合理却错误文档的查询。加入重排的企业报告更少的"找到了东西但不是对的"抱怨，而这正是驱动内部搜索采用率的指标。</p>
<h2 id="how-do-you-evaluate-embedding-models">你如何为你的语料评估嵌入模型？</h2>
<p>公开基准分数很少预测你自己文档上的相关性，所以评估必须是本地的。方法是标注查询集：几百个取自员工真实搜索方式的问题，每个配一个应胜出的文档。对候选运行它，度量top-k召回，以及更有用的——返回的文档是否回答了问题。领域语言——产品代码、内部缩略语、合同条款——是通用模型跌倒之处，所以在你的词汇上微调或提示的模型，常胜过更大的通用模型。评估集是资产；模型选择是可随新模型到来而替换的参数。</p>
<p>第二个轴是运营适配。嵌入延迟、索引大小与更新成本在模型间差异巨大，一个在实验室完美但无法每晚重新索引的模型，会在生产中失败。我们建议短名单2–3个、在标注集上受度量的bake-off、以及随模型改进每季度一次常态复评。把嵌入选择当作可度量、可修订的决策——而非一次性选取——的企业，避免了让内部搜索在上线六个月后感觉坏掉的静默相关性衰减，并与快速进步的领域保持同步。</p>
<h2 id="what-is-the-role-of-a-vector-database-versus-search">向量数据库与经典搜索各自的角色是什么？</h2>
<p>二者是互补，而非对手。经典搜索——关键词、过滤、排序——在精确匹配需求上无可匹敌：一个保单号、一个状态、一个命名实体。向量搜索胜在含义：与来源表述不同的问题仍能找到它。服务员工的知识库需要二者，这正是混合模式主导的原因。向量数据库通过存储嵌入、在规模上提供快速近似最近邻查找赢得位置；经典索引通过保证精确术语永不丢失赢得位置。假装一方取代另一方，是团队发布既漏掉显而易见、又漏掉意图的搜索的方式。</p>
<p>在架构中，向量库通常位于现有搜索服务旁，用融合或重排步骤把两个信号组合成一个答案。运营关注的是新鲜度：向量索引必须反映文档更新，否则用户得到昨天的真相。第二个关注是成本——当向量搜索检索一个重排器精炼的小候选集、而非扫描一切时，更便宜。把经典与向量搜索作为由重排器连接的、不同且被充分理解的层的企业，得到精度与召回，而无需强迫每个查询通过单一、妥协的机制。</p>
<h2 id="how-do-you-measure-retrieval-in-production">你如何在生产中衡量检索是否起作用？</h2>
<p>生产检索是在员工真正问的问题上度量，每周抽样，而非在固定基准上。对每个抽样查询，检查返回的文档是否是一个人本会打开的那个——即带人工判断的top-k召回——以及从中抽取的答案是否正确。跟踪"看似合理却错误"的返回率，因为这是悄悄侵蚀信任的失败：系统看起来对，却不对。第二个信号是放弃——当用户改写或退回到搜索，检索错过了。我们建议一个从真实日志刷新的常态评估集，每月打分，任何下降触发重嵌或重排器调优。在自己的实时问题上而非公开排行榜上度量检索的企业，及早发现相关性衰减，并保持知识库可信到人们持续使用它。</p>
<!--AUTOEXPAND-END-->

<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">
                <h2 class="faq-section-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                    常见问题
                </h2>
                <div class="faq-list">
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">1</span><span>什么是向量搜索，它为何对企业知识库重要？</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">向量搜索按含义而非精确关键词检索文档，把文本变成嵌入并返回最接近的匹配。对于企业知识库——它们大多是非结构化、混乱、充满缩略语——它是可信AI助手的检索骨架，因为检索并引用真实文档的模型能准确回答，而不是编造看似合理的虚构。</div></div>
                    </div>
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">2</span><span>稠密、稀疏与混合搜索的区别是什么？</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">稠密向量捕捉含义、善于处理释义，但可能错过产品代码等精确术语；BM25之类的稀疏方法精准命中关键词，却苦于同义。混合搜索融合二者，是企业内容（混合散文与标识符）的默认选择。融合权重应在取自真实员工问题的有标注集上调优，而非在公开基准上；并加入重排器以拉升困难查询。</div></div>
                    </div>
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">3</span><span>你如何在生产中衡量检索是否真的起作用？</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">在员工真正问的问题上度量，每周抽样，而非固定基准：检查带人工判断的top-k召回与答案是否正确，并跟踪"看似合理却错误"的返回与放弃率。一个100–300问题的金标准集每周重跑，能在用户之前发现分块回退和嵌入漂移。当用户不再改写问题、并开始打开引用时，检索就在起作用。</div></div>
                    </div>
                </div>
            </section>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "什么是向量搜索，它为何对企业知识库重要？", "acceptedAnswer": {"@type": "Answer", "text": "向量搜索按含义而非精确关键词检索文档，把文本变成嵌入并返回最接近匹配。对于企业知识库，它们大多非结构化、混乱、充满缩略语，它是可信AI助手的检索骨架，因为检索并引用真实文档的模型能准确回答，而不是编造看似合理的虚构。"}}, {"@type": "Question", "name": "稠密、稀疏与混合搜索的区别是什么？", "acceptedAnswer": {"@type": "Answer", "text": "稠密向量捕捉含义、善于处理释义，但可能错过产品代码等精确术语；BM25之类的稀疏方法精准命中关键词，却苦于同义。混合搜索融合二者，是企业内容，混合散文与标识符，的默认选择。融合权重应在取自真实员工问题的有标注集上调优，而非公开基准；并加入重排器以拉升困难查询。"}}, {"@type": "Question", "name": "你如何在生产中衡量检索是否真的起作用？", "acceptedAnswer": {"@type": "Answer", "text": "在员工真正问的问题上度量，每周抽样，而非固定基准：检查带人工判断的top-k召回与答案是否正确，并跟踪看似合理却错误的返回与放弃率。一个100到300问题的金标准集每周重跑，能在用户之前发现分块回退和嵌入漂移。当用户不再改写问题并开始打开引用时，检索就在起作用。"}]}</script>'''

ZH_SIDEBAR = '''<nav class="toc-links">
                    <a href="#the-current-landscape" class="toc-link">当前格局是怎样的？</a>
                    <a href="#the-core-vector-search-patterns" class="toc-link">核心的向量搜索模式有哪些？</a>
                    <a href="#key-implementation-challenges" class="toc-link">关键的实施挑战有哪些？</a>
                    <a href="#how-do-you-know-your-retrieval-is-working" class="toc-link">你如何知道检索在起作用？</a>
                    <a href="#practical-approaches-that-work" class="toc-link">哪些实践方法真正有效？</a>
                    <a href="#key-takeaways" class="toc-link">关键要点</a>
                    <a href="#conclusion" class="toc-link">结论</a>
                    <a href="#how-do-you-choose-between-dense-sparse-and-hybrid" class="toc-link">你如何在稠密、稀疏与混合搜索之间选择？</a>
                    <a href="#how-do-you-evaluate-embedding-models" class="toc-link">你如何为你的语料评估嵌入模型？</a>
                    <a href="#what-is-the-role-of-a-vector-database-versus-search" class="toc-link">向量数据库与经典搜索各自的角色是什么？</a>
                    <a href="#how-do-you-measure-retrieval-in-production" class="toc-link">你如何在生产中衡量检索是否起作用？</a>
                </nav>'''

en_p = base + "/blog/articles/" + slug + ".html"
h = open(en_p, encoding='utf-8').read()
e = h.find('<nav class="article-nav"')
if 'faq-question-h3' not in h[:e]:
    h = h[:e] + FAQ_SECTION + "\n" + h[e:]
    open(en_p, 'w', encoding='utf-8').write(h)
    print("EN: FAQ inserted")
else:
    print("EN: FAQ already present, skipped")

zh_p = base + "/zh-cn/blog/articles/" + slug + ".html"
h = open(zh_p, encoding='utf-8').read()
s = h.find('<div class="toc-mobile" id="toc-mobile">')
e = h.find('<nav class="article-nav"')
h = h[:s] + ZH + "\n" + h[e:]
open(zh_p, 'w', encoding='utf-8').write(h)
h = open(zh_p, encoding='utf-8').read()
si = h.find('<nav class="toc-links">')
ei = h.find('</nav>', si)
h = h[:si] + ZH_SIDEBAR + h[ei+len('</nav>'):]
open(zh_p, 'w', encoding='utf-8').write(h)

zhcn = open(zh_p, encoding='utf-8').read()
m = re.search(r'<main>.*</main>', zhcn, re.S)
tw_main = cc.convert(m.group(0))
tw_main = tw_main.replace('/zh-cn/', '/zh-tw/').replace('zh-cn/', 'zh-tw/').replace('预约演示', '預約示範')
zhtw = open(base + "/zh-tw/blog/articles/" + slug + ".html", encoding='utf-8').read()
zhtw = re.sub(r'<main>.*</main>', tw_main, zhtw, flags=re.S)
open(base + "/zh-tw/blog/articles/" + slug + ".html", 'w', encoding='utf-8').write(zhtw)
print("slug13 done")
