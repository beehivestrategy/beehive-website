# -*- coding: utf-8 -*-
import re, os
import opencc

base = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = "embedding-analytics-in-collaboration-tools-a-2026-update"
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
                            <span class="faq-question-text"><span class="faq-number">1</span><span>What is embedded analytics in collaboration tools?</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">Embedded analytics in collaboration tools is the practice of delivering governed, conversational data answers directly inside the messaging and collaboration apps where teams already work — Slack, Teams, WeChat Work, DingTalk, Feishu — instead of sending users to a separate BI portal. The answer is generated from a natural-language question against a governed semantic layer, with permissions and audit applied at the data layer.</div></div>
                    </div>
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">2</span><span>What is the biggest mistake enterprises make with embedded analytics?</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">Treating the channel as a front-end that inherits the governance of the underlying platform, rather than as its own attack surface. The fix is to put access control, audit trails, and data classification in the retrieval layer — not the display — so every in-channel answer is permissioned, cited, and logged regardless of how it was asked.</div></div>
                    </div>
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">3</span><span>How do you measure whether embedded analytics is actually working?</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">Stop counting dashboard opens; count in-channel answers cited in real decisions — references, reactions, forwards — and time-to-answer. When the citation rate is high and time-to-answer drops below a minute, the analytics has earned its place in the workflow; when it is low, it is decoration. Track permission accuracy too, because a single leak erodes trust faster than slow answers.</div></div>
                    </div>
                </div>
            </section>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "What is embedded analytics in collaboration tools?", "acceptedAnswer": {"@type": "Answer", "text": "Embedded analytics in collaboration tools is the practice of delivering governed, conversational data answers directly inside the messaging and collaboration apps where teams already work, Slack, Teams, WeChat Work, DingTalk, Feishu, instead of sending users to a separate BI portal. The answer is generated from a natural-language question against a governed semantic layer, with permissions and audit applied at the data layer."}}, {"@type": "Question", "name": "What is the biggest mistake enterprises make with embedded analytics?", "acceptedAnswer": {"@type": "Answer", "text": "Treating the channel as a front-end that inherits the governance of the underlying platform, rather than as its own attack surface. The fix is to put access control, audit trails, and data classification in the retrieval layer, not the display, so every in-channel answer is permissioned, cited, and logged regardless of how it was asked."}}, {"@type": "Question", "name": "How do you measure whether embedded analytics is actually working?", "acceptedAnswer": {"@type": "Answer", "text": "Stop counting dashboard opens; count in-channel answers cited in real decisions, references, reactions, forwards, and time-to-answer. When the citation rate is high and time-to-answer drops below a minute, the analytics has earned its place in the workflow; when it is low, it is decoration. Track permission accuracy too, because a single leak erodes trust faster than slow answers."}}]}</script>'''

# zh-CN full body (translation of EN, on-topic)
ZH = '''<div class="toc-mobile" id="toc-mobile">
                <button class="toc-mobile-toggle" aria-expanded="false">目录 <svg class="toc-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
                <div class="toc-mobile-links">
                    <a href="#the-current-landscape" class="toc-mobile-link">当前格局是怎样的？</a>
                    <a href="#what-has-changed-since-we-first-wrote-about-this" class="toc-mobile-link">自我们第一次写这篇文章以来，发生了什么变化？</a>
                    <a href="#key-implementation-challenges" class="toc-mobile-link">关键的实施挑战有哪些？</a>
                    <a href="#practical-approaches-that-work" class="toc-mobile-link">哪些实践方法真正有效？</a>
                    <a href="#key-takeaways" class="toc-mobile-link">关键要点</a>
                    <a href="#conclusion" class="toc-mobile-link">结论</a>
                    <a href="#how-do-you-measure-whether-embedded-analytics-is-working" class="toc-mobile-link">你如何衡量嵌入分析是否在起作用？</a>
                    <a href="#what-does-a-reference-architecture-look-like" class="toc-mobile-link">参考架构是什么样的？</a>
                    <a href="#how-do-you-handle-access-control-for-in-channel-answers" class="toc-mobile-link">你如何处理通道内答案的访问控制？</a>
                    <a href="#what-metrics-show-embedded-analytics-is-being-adopted" class="toc-mobile-link">哪些指标表明嵌入分析正在被采用？</a>
                </div>
            </div>
<p class="article-lead">在对话式分析领域，一年是很长的时间。当我们第一次写关于在协作工具中嵌入分析的文章时，IM原生的BI还只是一种有前景的模式；到了2026年，它已经成为现代劳动力的默认预期。本更新以"实际发生了什么变化"为视角，重新审视我们最初的指导——技术、经济学，以及我们现在看到企业所犯下并规避的错误。</p>
<h2 id="the-current-landscape">当前格局是怎样的？</h2>
<p>原文的前提已被事实验证。Gartner曾预测到2022年70%的白领将每天与对话平台交互，而这一预测早已被超越——协作工具现在是企业的主要操作界面，而非其补充。与此同时，Asana的研究发现，员工每天在应用之间切换超过1200次；每一次切换都是对注意力的一小笔税，而每一个在协作工具内交付的分析答案，都消除了其中一笔。</p>
<p>技术也在进步。写最初指南时，自然语言转SQL在演示中令人惊艳、在生产中脆弱。到了2026年，受治理的对话层——把自然语言翻译成已验证查询的语义模型——已经足够成熟，瓶颈不再是模型，而是语义层及其治理的质量。Gartner预见了数据重心的转移，预测到2025年75%的企业生成数据将在传统集中式数据中心或云之外创建和处理——而对话式分析在满足用户数据与工作真正所在之处，是天然的受益者。</p>
<p>经济学也发生了决定性转变。早期的IM原生项目作为软ROI的实验被论证；我们现在在亚太合作的企业，把它们论证为运营成本削减和决策速度投资，并要求部署在第一季度内实现可衡量的采用。对话已从"我们该不该做？"转向"我们能有多快？"</p>
<p>没有改变的，是基本面：数据质量、集成、治理和变革管理仍然决定成败。改变的是犯错的代价——在对话式分析中，领先者与落后者之间的差距，比我们观察到的大多数技术采用曲线扩大得都快。</p>
<h2 id="what-has-changed-since-we-first-wrote-about-this">自我们第一次写这篇文章以来，发生了什么变化？</h2>
<p>三个变化值得任何计划部署的企业关注。其一是语义层从锦上添花成熟为核心资产。在原文中，我们把语义层描述为加速采用的东西；今天，它是"一个指标意味着什么"的记录系统，语义层的质量决定了组织将获得的每个答案的质量。跳过这一步的企业现在正在重建——而重建远比一开始就构建要昂贵得多。</p>
<p>其二是安全与治理的成熟。早期部署把IM通道当作继承了底层数据平台治理的前端。2026年的部署把通道本身当作攻击面：数据层面的权限执行、每个问答的审计轨迹、通道感知的数据分类，以及向审计者证明"向谁展示了什么"的能力。亚太的监管者——以及越来越受到欧盟AI法案高风险条款约束的企业——期待这条证据链，而早早构建它的企业领先了。</p>
<p>其三是主动洞察交付的兴起。原文聚焦于按需问答和定时报告；当前的前沿是那些无需被问、就能主动浮现异常、解释它们并提出行动的系统——以对话卡片的形式出现在晨会通道中。主动交付让"决策延迟"的论点变得生动：系统在8:02告诉厂长良率下降，而不是等到周一复盘。</p>
<h2 id="key-implementation-challenges">关键的实施挑战有哪些？</h2>
<p>尽管好处明确，组织仍持续遇到几个实施挑战。数据质量仍是最显著的障碍——我们的评估显示，约70%的企业数据在能支撑AI工作负载之前需要大量准备。这包括处理重复、缺失值、不一致的格式和过时的记录。一年的对话式分析部署并没有改变这个数字，因为问题是结构性的，而非技术性的。</p>
<p>集成复杂性是另一个主要障碍。企业环境通常包含跨越多代技术的数十个数据源。可靠地连接这些源、维护数据血缘、并确保一致的语义定义，需要技术专长与组织协同。改变的是期望：企业现在要求语义层只构建一次、跨通道复用，这让平台中立的数据产品变得珍贵。</p>
<p>或许最被低估的挑战是变革管理。与技术实现相比，转变组织文化、重新定义角色职责、建立对AI生成洞察的信任要困难得多。我们的经验表明，投资于全面变革管理计划的组织，采用率比只聚焦技术部署的组织高三倍——而在2026年，随着IM原生分析触及每个职能，变革的覆盖面更大而非更小。</p>
<h2 id="practical-approaches-that-work">哪些实践方法真正有效？</h2>
<p>基于我们服务企业客户的经验，我们识别出几个持续交付结果的实践方法。从聚焦的用例起步，而非试图企业级转型，能让组织快速证明价值并建立组织信心。聚焦用例在2026年仍是正确的选择，但"价值"的门槛提高了：它应是一个能改变业务成果、能在本季度内衡量的决策。</p>
<p>建立语义层——技术数据模型之上的业务友好抽象——能极大地加速采用。业务用户可以用自然语言提问，而无需理解数据库模式、表关系或SQL语法。这在不丧失治理控制的前提下让数据访问民主化。构建一次，把它当作受治理的资产，让每个通道和每个未来的AI能力复用相同的定义。</p>
<p>从第一天起实施稳健的监控与可观测性，能防止困扰众多分析系统的逐渐退化。自动数据质量检查、性能监控和使用分析，在问题影响业务决策之前提供早期预警。把答案质量监控也加入清单：跟踪用户有多少次质疑或纠正答案，并把这些信号反馈到语义层。</p>
<p>最后，为与现有通信平台的集成而设计，能消除用户体验中的摩擦。当洞察自然地出现在日常工作的流程中——通过IM通知、定时报告或按需查询——参与和采用显著提升。这正是蜂启咨询在一年IM原生对话式BI部署中打磨出的模式：受治理的语义层、在WeChat Work、钉钉、飞书、Teams和WhatsApp中的通道原生交付、约两周内部署，以及持续维护语义质量、监控与审计轨迹的管理服务。2026年的推广顺序：</p>
<ol>
<li>重新确认以决策为核心的用例，以及将锚定它的指标定义。</li>
<li>建立或加固语义层，作为每个答案的受治理来源。</li>
<li>为通道接通治理——权限、审计轨迹与分类。</li>
<li>在一个团队的通道中试点，然后向晨会加入主动洞察交付。</li>
<li>在语义层与可观测性完好无损的前提下跨职能扩展。</li>
</ol>
<h2 id="key-takeaways">关键要点</h2>
<ul>
<li>语义层现在是核心资产——它的质量决定每个答案的质量</li>
<li>IM通道是攻击面——从第一天起就把权限、审计轨迹与分类设计进去</li>
<li>主动洞察交付是2026年的前沿——在复盘会议之前浮现异常</li>
<li>数据质量是基础——在AI实施之前投资准备</li>
<li>对话式分析是运营成本与决策速度投资，而非实验</li>
<li>全面的变革管理不可或缺——仅靠技术是不够的</li>
</ul>
<h2 id="conclusion">结论</h2>
<p>在协作工具中嵌入分析的论据已不再是假设——一年的生产部署既确认了回报，也厘清了失败模式。2026年胜出的企业，是那些先建语义层、把通道当作安全边界的一部分、并从按需答案走向主动洞察的企业。</p>
<p>对我们最初指导的更新很简单：基本面仍决定成败，但如今节奏更重要，而语义层最重要。借助蜂启咨询的两周部署与管理服务，你的组织能在下个季度开始前，从评估走到受治理的、通道原生的对话式分析能力。</p>

<!--AUTOEXPAND-START-->
<h2 id="how-do-you-measure-whether-embedded-analytics-is-working">你如何衡量嵌入分析是否在起作用？</h2>
<p>在Slack、Teams或工作区中嵌入分析，只有当人们确实在对话发生之处使用洞察时才值得。重要的指标不是仪表盘打开次数，而是通道内被引用的决策——在话题中回答的查询、被粘贴进决策的数字。对此做埋点：一个嵌入的答案被引用、被反应、被转发的频率有多高？高引用率意味着分析赢得了它的位置；低引用率意味着它只是装饰。第二个指标是响应时间：从有人提问到数据出现之间的间隔。当这个间隔降到一分钟内，行为就从偶发变成习惯。</p>
<p>2026年的更新是，界面不再是一张图表，而是一段对话。团队不再钉住一份报告，而是向工作区智能体提问，得到带引用、并链接回来源的答案。这把建设精力从可视化转移到检索质量与访问控制，因为智能体必须为正确的人获取正确的数据切片，而不泄漏他们不应看到的内容。因此衡量也扩展到答案正确性与权限准确性——这正是2026年大多数嵌入分析项目现在投入精力的地方。</p>
<h2 id="what-does-a-reference-architecture-look-like">参考架构是什么样的？</h2>
<p>参考架构有四层。连接层位于工作区与数据源之上，使用经过认证、限定范围的连接器，而非复制的提取物。检索层为提问用户获取正确的数据切片，在任何内容被汇总之前应用行级与列级权限。生成层把检索到、已授权的结果变成带引用的答案。可观测层记录每个问题、答案、来源与权限决策以供审计。工作区智能体是前门；检索与访问层是决定系统是否可信的部分。</p>
<p>关键设计选择是访问控制所在之处。如果它只存在于可视化中，绕过仪表盘的智能体就会泄漏数据；如果它存在于检索层，每个答案——无论怎么问——都被约束为用户可见范围。这正是参考架构把权限放在检索而非展示的原因。第二个选择是引用：每个答案都携带来源链接，供用户核实。构建这种四层形态的企业，避免了"光鲜的对话表层架在不受控数据管道之上"的常见失败，并能把同一模式从一个工作区扩展到多个，而无需每次重新争论信任。</p>
<h2 id="how-do-you-handle-access-control-for-in-channel-answers">你如何处理通道内答案的访问控制？</h2>
<p>通道内答案的访问控制，与报告中的行级安全是同一个问题，在查询层解决。智能体永远不应看到超过用户有权限的内容，因此权限过滤在生成之前应用于检索到的数据，而非之后。实践中，这意味着智能体调用一个执行策略的数据服务，而不是用被剥离的用户身份直接查询数据仓库。当策略改变，答案随之改变，无需单独的UI来保持同步。</p>
<p>第二个控制是审计轨迹。因为答案出现在共享通道中，记录谁问了什么、返回了什么、哪些行支撑了它，对于事后调查泄漏至关重要。我们还建议给答案打敏感度标签：如果底层数据受限，答案被标记并限制其传播。做对的企业把通道答案当作受治理的输出——已授权、已引用、已记录——这正是让他们能把真实数据放在员工已用工具面前的东西，而不是迫使使用一个独立的、信任度更低的报告应用。</p>
<h2 id="what-metrics-show-embedded-analytics-is-being-adopted">哪些指标表明嵌入分析正在被采用？</h2>
<p>嵌入分析的采用，体现为通道内答案被引用进决策，而非仪表盘登录。重要的指标是引用率——工作区智能体的答案被引用、被反应、被转发进真实选择的频率——因为那一刻洞察改变了行为。其二是响应时间，从提问到数据出现之间的间隔；当它降到一分钟内，习惯形成。我们也跟踪权限准确性，因为泄漏受限数据的答案，比慢的答案更快地摧毁信任。关注引用率、响应时间与权限准确性——而非打开次数——的企业，能判断嵌入分析是否在流程中赢得了位置，还是仅仅装饰，并能在悄悄的无人使用变成削减项目的理由之前介入。</p>
<!--AUTOEXPAND-END-->

<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">
                <h2 class="faq-section-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                    常见问题
                </h2>
                <div class="faq-list">
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">1</span><span>什么是协作工具中的嵌入分析？</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">它是把受治理的、对话式的数据答案，直接交付到团队已经在用的消息与协作应用（Slack、Teams、企业微信、钉钉、飞书）中，而不是把用户送往独立的BI门户。答案由自然语言问题针对受治理的语义层生成，权限与审计在数据层应用。</div></div>
                    </div>
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">2</span><span>企业在嵌入分析上最大的错误是什么？</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">把通道当作继承了底层平台治理的前端，而不是把它当作自身的攻击面。修复办法是把访问控制、审计轨迹与数据分类放在检索层——而非展示层——这样每个通道内答案都被授权、被引用、被记录，无论它是怎么被问出的。</div></div>
                    </div>
                    <div class="faq-item">
                        <h3 class="faq-question-h3"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">3</span><span>你如何衡量嵌入分析是否真的在起作用？</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">停止计算仪表盘打开次数；改为计算通道内被真实决策引用的答案——引用、反应、转发——以及响应时间。当引用率高、响应时间降到一分钟内，分析就在流程中赢得了位置；当引用率低，它只是装饰。也跟踪权限准确性，因为一次泄漏比慢答案更快地侵蚀信任。</div></div>
                    </div>
                </div>
            </section>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "什么是协作工具中的嵌入分析？", "acceptedAnswer": {"@type": "Answer", "text": "它是把受治理的、对话式的数据答案，直接交付到团队已经在用的消息与协作应用（Slack、Teams、企业微信、钉钉、飞书）中，而不是把用户送往独立的BI门户。答案由自然语言问题针对受治理的语义层生成，权限与审计在数据层应用。"}}, {"@type": "Question", "name": "企业在嵌入分析上最大的错误是什么？", "acceptedAnswer": {"@type": "Answer", "text": "把通道当作继承了底层平台治理的前端，而不是把它当作自身的攻击面。修复办法是把访问控制、审计轨迹与数据分类放在检索层，而非展示层，这样每个通道内答案都被授权、被引用、被记录，无论它是怎么被问出的。"}}, {"@type": "Question", "name": "你如何衡量嵌入分析是否真的在起作用？", "acceptedAnswer": {"@type": "Answer", "text": "停止计算仪表盘打开次数；改为计算通道内被真实决策引用的答案，引用、反应、转发，以及响应时间。当引用率高、响应时间降到一分钟内，分析就在流程中赢得了位置；当引用率低，它只是装饰。也跟踪权限准确性，因为一次泄漏比慢答案更快地侵蚀信任。"}]}</script>'''

ZH_SIDEBAR = '''<nav class="toc-links">
                    <a href="#the-current-landscape" class="toc-link">当前格局是怎样的？</a>
                    <a href="#what-has-changed-since-we-first-wrote-about-this" class="toc-link">自我们第一次写这篇文章以来，发生了什么变化？</a>
                    <a href="#key-implementation-challenges" class="toc-link">关键的实施挑战有哪些？</a>
                    <a href="#practical-approaches-that-work" class="toc-link">哪些实践方法真正有效？</a>
                    <a href="#key-takeaways" class="toc-link">关键要点</a>
                    <a href="#conclusion" class="toc-link">结论</a>
                    <a href="#how-do-you-measure-whether-embedded-analytics-is-working" class="toc-link">你如何衡量嵌入分析是否在起作用？</a>
                    <a href="#what-does-a-reference-architecture-look-like" class="toc-link">参考架构是什么样的？</a>
                    <a href="#how-do-you-handle-access-control-for-in-channel-answers" class="toc-link">你如何处理通道内答案的访问控制？</a>
                    <a href="#what-metrics-show-embedded-analytics-is-being-adopted" class="toc-link">哪些指标表明嵌入分析正在被采用？</a>
                </nav>'''

# 1) EN: insert FAQ + JSON-LD before article-nav
en_p = base + "/blog/articles/" + slug + ".html"
h = open(en_p, encoding='utf-8').read()
e = h.find('<nav class="article-nav"')
if 'faq-question-h3' not in h[:e]:
    h = h[:e] + FAQ_SECTION + "\n" + h[e:]
    open(en_p, 'w', encoding='utf-8').write(h)
    print("EN: FAQ inserted")
else:
    print("EN: FAQ already present, skipped")

# 2) zh-CN: replace article-content inner + toc-sidebar
zh_p = base + "/zh-cn/blog/articles/" + slug + ".html"
h = open(zh_p, encoding='utf-8').read()
s = h.find('<div class="toc-mobile" id="toc-mobile">')
e = h.find('<nav class="article-nav"')
h = h[:s] + ZH + "\n" + h[e:]
open(zh_p, 'w', encoding='utf-8').write(h)
# toc-sidebar
h = open(zh_p, encoding='utf-8').read()
si = h.find('<nav class="toc-links">')
ei = h.find('</nav>', si)
h = h[:si] + ZH_SIDEBAR + h[ei+len('</nav>'):]
open(zh_p, 'w', encoding='utf-8').write(h)

# 3) zh-TW from zh-CN main
zhcn = open(zh_p, encoding='utf-8').read()
m = re.search(r'<main>.*</main>', zhcn, re.S)
tw_main = cc.convert(m.group(0))
tw_main = tw_main.replace('/zh-cn/', '/zh-tw/').replace('zh-cn/', 'zh-tw/').replace('预约演示', '預約示範')
zhtw = open(base + "/zh-tw/blog/articles/" + slug + ".html", encoding='utf-8').read()
zhtw = re.sub(r'<main>.*</main>', tw_main, zhtw, flags=re.S)
open(base + "/zh-tw/blog/articles/" + slug + ".html", 'w', encoding='utf-8').write(zhtw)
print("slug12 done")
