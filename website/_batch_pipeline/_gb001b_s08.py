#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 08: feature-store-architecture-for-ml-model-consistency-part-3
EN 1357 -> ~2600 ; CN/TW 1837/1850 -> ~3600 ; build FAQ ; H2 -> questions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_by_text, build_faq, s2t_fixed

SLUG = "feature-store-architecture-for-ml-model-consistency-part-3"
NAV = '            <nav class="article-nav" aria-label="Article navigation">'

EN_NEWS = """<h2 id="what-does-training-serving-skew-actually-look-like">What Does Training-Serving Skew Actually Look Like?</h2>
<p>Skew is the reason feature stores exist, and it is worth describing concretely because the failure is almost always mundane. A data scientist computes a feature in a notebook — say, the count of transactions in the trailing seven days — using a query that runs over the full historical table. At serving time, an engineer reimplements the same idea against a streaming store or a cached table, and the two implementations disagree at the boundaries: whether the current day is included, how a refund is treated, what happens with a transaction whose timestamp arrives late. The model was trained on one definition and scored on another, and the difference is invisible in offline evaluation because both sides look correct in isolation.</p>
<p>The second common form is temporal leakage, which is subtler and more damaging. A feature computed over the full historical table can inadvertently include information from the future relative to the prediction point — a customer's status after the event being predicted, an aggregate that uses rows that had not yet occurred at scoring time. Offline accuracy looks excellent because the model has been shown the answer; production accuracy collapses. Point-in-time correctness — computing each feature exactly as it would have appeared at the prediction timestamp — is the property that prevents this, and it is the single most valuable guarantee a feature store provides.</p>
<p>The third form is the one that appears after deployment: drift between the distribution the model was trained on and the distribution it now sees. This is not an implementation bug but a change in the world, and no amount of careful engineering prevents it. What prevents damage is detection — measuring the serving distribution continuously against the training baseline, with thresholds tied to decision impact rather than to statistical convention. A feature whose mean has moved two percent may be irrelevant to one model and catastrophic to another, which is why thresholds belong to the model's owner, not to the platform's defaults.</p>
<h2 id="how-should-you-design-feature-versioning">How Should You Design Feature Versioning and Lineage?</h2>
<p>Versioning answers one question: given a prediction made on a particular date, exactly which feature values and which transformation code produced it? Answering it requires versioning three things together. The transformation logic must be versioned as code, in source control, with the version recorded at both training and serving time. The feature values must be versioned by point-in-time state, so that a historical reconstruction returns what was actually known then rather than what is known now. And the model artefact must be versioned with a resolved reference to both — not to a feature name, but to a specific version of a specific transformation.</p>
<p>Lineage is the connective tissue that makes those versions navigable. Upstream lineage records which source tables and columns feed a feature, so that a change in a source system can be traced to every affected model before it ships. Downstream lineage records which models consume a feature, so that retiring or altering one is a decision with a known blast radius. Most teams build downstream lineage first because it is needed for incident response; the upstream direction is what turns a schema change from an outage into a scheduled review.</p>
<p>Two practical rules keep this tractable. Version at the granularity of the feature definition rather than the whole store, because versioning everything together couples unrelated models and makes every change expensive. And make the version reference immutable in the model artefact: a model that resolves "latest" at scoring time cannot be reproduced, and reproducibility is precisely what an audit, an incident review, or a regulator will ask for. The cost of discipline here is a few lines of metadata at training time; the cost of its absence is an unanswerable question at the worst possible moment.</p>
<h2 id="what-should-you-measure-to-detect-decay">What Should You Measure to Detect Decay Early?</h2>
<p>Four families of measurement catch most decay, and they are useful precisely because they move before model accuracy does. Distribution drift compares the serving distribution of each feature against the training baseline — population stability index, Kolmogorov–Smirnov statistics, or simply tracked quantiles, depending on the audience. Missingness and default rates catch pipeline breakage that would otherwise present as a gentle accuracy decline: a join that started failing, a source column that went null, a lookup that silently returns the default. Cardinality drift catches categorical features that have grown new values the model has never seen, which is common after a product launch or a regional expansion.</p>
<p>The fourth family is the one most often omitted and most diagnostic: feature attribution stability. If the relative importance of features shifts substantially between training and production, the model is relying on different signal than it was validated on, which usually means something upstream changed even when every individual distribution looks acceptable. Tracking top-k feature attributions per scoring window is cheap and catches the failures that per-feature monitoring misses.</p>
<p>Measurements only matter with routing attached, and this is where most programmes stall. Every metric needs a threshold with a rationale, an owner who receives the alert, and a pre-agreed first response — investigate, roll back, recalibrate, or retrain. A drift dashboard with none of those produces alert fatigue within two months, after which the monitoring exists on paper and degradation is once again discovered by a stakeholder. The test of a monitoring design is not whether it detects drift but whether the third alert in a month still produces a response.</p>
<h2 id="how-do-you-roll-out-a-feature-store">How Do You Roll Out a Feature Store Without Boiling the Ocean?</h2>
<p>The failure mode of feature store programmes is ambition: a plan to migrate every model and every feature before any value is demonstrated. The rollout that works is narrower. Pick one model that matters, has known consistency problems, and has an owner who will invest in the fix — fraud scoring, credit decisioning, demand forecasting, and churn are the usual candidates because their drift is observable in business metrics. Migrate that model's features into the store with point-in-time correct definitions, run it in shadow alongside the incumbent for a scoring cycle, and compare. One model done properly produces the reference implementation, the political proof, and the templates that every subsequent migration reuses.</p>
<p>The second phase expands within the same domain rather than across the enterprise, because adjacent models in a domain share features and therefore share the benefit — migrating a second fraud model costs a fraction of the first. Only in the third phase should the programme become horizontal, and by then the product owner has a curation backlog, an admission process that teams understand, and evidence of reduced time-to-model that funds the platform work. Programmes that invert this order typically reach phase three with a large store, a thin curation practice, and a sceptical finance function.</p>
<p>The measure of a successful rollout is not the number of features in the store. It is the time to answer "which features did this model use, and were they behaving as expected?" — ideally hours, and never dependent on the person who built the model still being employed. Tracking that single metric from the first migration onward is the clearest signal of whether the store is becoming the memory of the estate or merely another silo with better tooling.</p>
"""

ZH_NEWS = """<h2 id="训练与推理偏差到底长什么样">训练与推理偏差到底长什么样？</h2>
<p>偏差正是特征存储存在的理由，值得具体描述，因为这种失败几乎总是平淡无奇的。一位数据科学家在笔记本里算出一个特征——比如"过去七天的交易笔数"——用的是跑在全量历史表上的查询。到了推理时，工程师针对流式存储或缓存表重新实现同一个想法，两者在边界上产生了分歧：当天是否计入、退款如何处理、时间戳迟到的事务怎么算。模型用一种定义训练，用另一种定义打分，而这个差异在离线评估中是不可见的，因为两边单独看都正确。</p>
<p>第二种常见形态是时间泄漏，它更隐蔽、也更具破坏性。在全量历史表上计算的特征，可能无意中包含了相对于预测时点属于未来的信息——客户在被预测事件之后的状态，或者用到了打分时尚未发生的行的聚合值。离线效果看起来极好，因为模型已经看到了答案；上线后效果崩塌。时点正确性——严格按照预测时间戳当时所能看到的样子计算每个特征——正是防止这一点的性质，也是特征存储能提供的最有价值的一项保证。</p>
<p>第三种形态出现在部署之后：模型训练时所见的分布与它现在所见的分布之间发生了漂移。这不是实现缺陷，而是世界发生了变化，再仔细的工程也无法阻止。能阻止损害的是检测——持续把推理分布与训练基线做比对，并把阈值与决策影响挂钩，而不是与统计惯例挂钩。某个特征的均值移动了百分之二，对一个模型可能无关紧要，对另一个可能是灾难，正因为如此，阈值应当属于模型负责人，而不属于平台的默认值。</p>
<h2 id="特征版本与血缘应如何设计">特征版本与血缘应当如何设计？</h2>
<p>版本管理只回答一个问题：给定某个特定日期做出的一次预测，究竟是哪些特征值、哪些转换代码产出了它？要回答这个问题，需要把三样东西一起做版本管理。转换逻辑必须作为代码纳入版本控制，并在训练与推理两个时点都记录版本号。特征值必须按"时点状态"做版本管理，使历史重建返回的是当时实际已知的情况，而不是现在已知的情况。模型产物则必须带着对前两者的确定性引用一起版本化——不是引用特征名称，而是引用某个转换的特定版本。</p>
<p>血缘是把这些版本变得可导航的结缔组织。上游血缘记录哪些源表与源字段喂给了某个特征，使源系统的变更能在上线前被追踪到每一个受影响的模型。下游血缘记录哪些模型消费了某个特征，使停用或修改一个特征成为一个爆炸半径已知的决定。多数团队先建下游血缘，因为事件响应需要它；而上游方向才是把一次 schema 变更从"事故"变成"计划内评审"的关键。</p>
<p>两条实用规则能让这件事保持可控。按特征定义的粒度做版本管理，而不是整个存储一起版本化，因为整体版本化会把不相关的模型耦合在一起，让每一次变更都变得昂贵。并且在模型产物中让版本引用不可变：一个在打分时解析为"最新"的模型是不可复现的，而可复现性恰恰是审计、事件复盘或监管方会索要的东西。在这里守纪律的代价，只是训练时多写几行元数据；而不守纪律的代价，是在最糟糕的时刻遇到一个无法回答的问题。</p>
<h2 id="应度量什么才能尽早发现衰减">应当度量什么，才能尽早发现模型衰减？</h2>
<p>四类度量能抓住大部分衰减，它们之所以有用，恰恰因为它们在模型准确率之前就开始移动。分布漂移把每个特征的推理分布与训练基线做比较——群体稳定性指数、KS 统计量，或者干脆跟踪分位数，取决于受众是谁。缺失率与默认值率能抓住那些本会表现为"准确率缓慢下滑"的管道故障：某个 join 开始失败、源字段变成了空值、某个查询静默返回默认值。基数漂移能抓住那些出现了模型从未见过的新取值的类别特征，这在产品上线或区域扩张之后很常见。</p>
<p>第四类最常被忽略，也最具诊断价值：特征归因稳定性。如果特征之间的相对重要性在训练与生产之间发生了显著变化，说明模型依赖的信号与它当初被验证时的不同，这通常意味着上游发生了变化——即便每个单独的分布看起来都还可以接受。按打分窗口跟踪前 k 个特征归因成本很低，却能抓住逐特征监控漏掉的那些失败。</p>
<p>度量只有在接上了路由之后才有意义，而这正是多数项目停滞的地方。每项度量都需要一个带理由的阈值、一个接收告警的负责人，以及一个事先约定的第一响应动作——排查、回滚、重新校准或重训。一个三者皆无的漂移看板会在两个月内造成告警疲劳，此后监控只存在于纸面上，衰减再次由业务方首先发现。监控设计的检验标准不是它能否检测到漂移，而是一个月内的第三条告警是否仍然能得到响应。</p>
<h2 id="如何稳步落地特征存储">如何稳步落地特征存储，而不至于一口吃成胖子？</h2>
<p>特征存储项目的典型失败模式是野心过大：计划在证明任何价值之前，把所有模型和所有特征都迁移过去。真正奏效的落地方式要窄得多。选一个重要的、已知存在一致性问题的、且负责人愿意投入修复的模型——欺诈打分、信贷决策、需求预测、流失预测是常见候选，因为它们的漂移能在业务指标上被观察到。把这个模型的特征以时点正确的定义迁入存储，让它与现有模型并行跑一个打分周期做影子对比。一个模型做扎实了，就有了参考实现、组织层面的证明，以及后续每次迁移都可复用的模板。</p>
<p>第二阶段在同一领域内扩展，而不是跨企业扩展，因为同一领域内的相邻模型共享特征，因而共享收益——迁移第二个欺诈模型的成本只是第一个的一小部分。只有到第三阶段，项目才应转为横向推进；而那时，产品负责人已经拥有了策展待办清单、团队已经理解的上线评审流程，以及能证明"建模周期缩短"的证据来支撑平台投入。把这个顺序颠倒的项目，通常在到达第三阶段时拥有一个大而全的存储、薄弱的策展实践，以及一个持怀疑态度的财务部门。</p>
<p>衡量落地是否成功的标准，不是存储里有多少个特征，而是回答"这个模型用了哪些特征、它们当时表现是否正常"所需的时间——理想是几小时，且绝不依赖于当初构建模型的人是否还在职。从第一次迁移起就跟踪这一个指标，是判断存储正在成为整个资产体系的记忆、还是只是一个工具更好看的孤岛的最清晰信号。</p>
"""

EN_FAQ = [
    ("What is a feature store in machine learning?",
     "A feature store is a shared system for defining, computing, storing, and serving the input variables a machine learning model uses. Its defining guarantee is that the same feature definition is used for training and for live scoring, which eliminates training-serving skew, and that historical feature values can be reconstructed exactly as they appeared at any past prediction time, which makes models reproducible."),
    ("Why does training-serving skew happen?",
     "Because the training feature and the serving feature are usually implemented twice by different people against different systems. The two implementations agree on the main case and disagree at the boundaries — whether the current day is included, how late-arriving records are treated, how nulls are defaulted. A feature store removes the duplication by making one registered definition serve both paths."),
    ("How do you detect feature drift early?",
     "Track four families of measurement continuously against the training baseline: distribution drift, missingness and default rates, categorical cardinality, and feature attribution stability. Each needs a threshold tied to the business decision, a named owner, and a pre-agreed response. Monitoring without those three produces alert fatigue and decay is again discovered by a stakeholder."),
    ("Who should own a feature store?",
     "A named product owner with a curation mandate and a budget. Feature engineering sits between data engineering and ML engineering, and without an owner the store accumulates undocumented duplicates. The owner admits new features against a documented definition, retires features that lose consumers, and mediates conflicts between teams."),
    ("How long does a feature store implementation take?",
     "A first production migration of one model and its features typically takes six to twelve weeks: feature discovery and definition, point-in-time correct backfills, serving integration, and a shadow-mode comparison. Broad adoption across a model portfolio is a programme of two to four quarters, and should follow — not precede — that first demonstrated migration."),
]

CN_FAQ = [
    ("机器学习中的特征存储是什么？",
     "特征存储是一套共享系统，用于定义、计算、存储并提供机器学习模型所用的输入变量。它的核心保证是：训练与线上打分使用同一套特征定义，从而消除训练—推理偏差；并且任何历史时点的特征值都能被精确重建，使模型具备可复现性。"),
    ("为什么会出现训练—推理偏差？",
     "因为训练侧特征与推理侧特征通常由不同的人在两套系统上各实现一次。两者在主要情形下一致，却在边界上产生分歧：当天是否计入、迟到记录如何处理、空值如何取默认值。特征存储通过让同一份注册定义同时服务两条路径，消除了这种重复实现。"),
    ("如何尽早发现特征漂移？",
     "持续对照训练基线跟踪四类度量：分布漂移、缺失率与默认值率、类别基数、以及特征归因稳定性。每一项都需要一个与业务决策挂钩的阈值、一位具名负责人，以及一个事先约定的响应动作。缺少这三者的监控会造成告警疲劳，衰减最终还是由业务方首先发现。"),
    ("特征存储应当由谁负责？",
     "应当由一位有策展授权和预算的具名产品负责人负责。特征工程处于数据工程与机器学习工程之间，没有负责人，存储就会堆满无文档的重复特征。负责人按书面定义审核新特征上线、停用失去消费方的特征，并调解团队之间的口径冲突。"),
    ("落地特征存储需要多长时间？",
     "首个模型及其特征完成一次生产级迁移通常需要六到十二周：特征盘点与定义、时点正确的回填、推理侧集成、以及影子模式的对比。在整个模型组合中推广是一个二到四个季度的项目，并且应当发生在——而不是先于——第一次成功的示范迁移之后。"),
]

EN_H2 = [
    ("Key Implementation Challenges", "What Are the Key Implementation Challenges?"),
    ("Practical Approaches That Work", "Which Practical Approaches Actually Work?"),
    ("Key Takeaways", "What Are the Key Takeaways?"),
    ("Conclusion", "Where Does This Leave the ML Estate?"),
]
CN_H2 = [
    ("理解当前格局", "当前的特征存储格局是怎样的？"),
    ("关键原则与战略框架", "特征存储的关键原则与战略框架是什么？"),
    ("实施方法与最佳实践", "实施特征存储的最佳实践有哪些？"),
    ("衡量成功与展示投资回报率", "应当如何衡量成功并证明投资回报？"),
    ("常见陷阱及规避方法", "有哪些常见陷阱、又该如何规避？"),
    ("关键要点", "核心要点是什么？"),
    ("结论", "结论是什么？"),
]
TW_H2 = [
    ("理解當前格局", "當前的特徵儲存格局是怎樣的？"),
    ("關鍵原則與策略框架", "特徵儲存的關鍵原則與策略框架是什麼？"),
    ("實施方法與最佳實踐", "實施特徵儲存的最佳實踐有哪些？"),
    ("衡量成功與展示投資回報率", "應當如何衡量成功並證明投資回報？"),
    ("常見陷阱及規避方法", "有哪些常見陷阱、又該如何規避？"),
    ("關鍵要點", "核心要點是什麼？"),
    ("結論", "結論是什麼？"),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    assert h.count(NAV) == 1
    h = h.replace(NAV, "\n" + EN_NEWS + "\n" + build_faq(EN_FAQ, "en") + "\n" + NAV)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body + FAQ done")

    cn = path_of(SLUG, "cn")
    h = open(cn, encoding="utf-8").read()
    assert h.count(NAV) == 1
    h = h.replace(NAV, "\n" + ZH_NEWS + "\n" + build_faq(CN_FAQ, "cn") + "\n" + NAV)
    open(cn, "w", encoding="utf-8").write(h)
    print("CN body + FAQ done")

    tw = path_of(SLUG, "tw")
    h = open(tw, encoding="utf-8").read()
    assert h.count(NAV) == 1
    tw_faq = [(s2t_fixed(q), s2t_fixed(a)) for q, a in CN_FAQ]
    h = h.replace(NAV, "\n" + s2t_fixed(ZH_NEWS) + "\n" + build_faq(tw_faq, "tw") + "\n" + NAV)
    open(tw, "w", encoding="utf-8").write(h)
    print("TW body + FAQ done")

    for old, new in EN_H2:
        retitle_by_text(en, old, new)
    for old, new in CN_H2:
        retitle_by_text(path_of(SLUG, "cn"), old, new)
    for old, new in TW_H2:
        retitle_by_text(path_of(SLUG, "tw"), old, new)
    print("H2s converted in en/cn/tw")
