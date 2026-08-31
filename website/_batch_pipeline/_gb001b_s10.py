#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 10: what-is-federated-learning
EN 1566 -> ~2650 ; CN/TW 2225 -> ~3650 ; H2 -> questions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_by_text, s2t_fixed

SLUG = "what-is-federated-learning"

EN_NEWS = """<h2 id="how-does-federated-learning-compare-to-other-pet">How Does Federated Learning Compare to Other Privacy-Enhancing Technologies?</h2>
<p>Federated learning is one of several privacy-enhancing technologies, and choosing between them is a design decision rather than a matter of preference. Differential privacy protects individual records by adding calibrated statistical noise, and it composes naturally with federated learning — it is typically applied to the model updates rather than being an alternative to federation. The trade-off is explicit and tunable: more noise means a stronger privacy guarantee and lower model accuracy. Secure multi-party computation allows several parties to compute a function jointly without any party seeing the others' inputs, which is stronger than federation but far more expensive in communication and compute. Homomorphic encryption permits computation directly on encrypted data, and while it is the strongest option in principle, the overhead currently restricts it to narrow workloads.</p>
<p>The practical distinction is that federated learning keeps raw data in place and moves only the model, which makes it uniquely suited to settings where data cannot legally or practically be centralised at all — cross-border banking, multi-hospital research, on-device learning at consumer scale. Secure multi-party computation and homomorphic encryption are better suited to settings where a specific computation must be jointly performed and the overhead is acceptable. Most production deployments combine approaches: federated training for the learning loop, secure aggregation to protect updates in transit, and differential privacy to bound what the updates reveal.</p>
<p>One caveat deserves emphasis because it is widely misunderstood. Federated learning is not anonymity. Model updates can, under some conditions, leak information about the training data — membership inference and gradient inversion attacks are real and documented. This is precisely why differential privacy and secure aggregation are considered part of a serious deployment rather than optional extras, and why any claim that federation alone makes data sharing compliant should be treated with scepticism by a privacy officer.</p>
<h2 id="what-does-non-iid-data-do">What Does Non-IID Data Do to a Federated Model?</h2>
<p>Non-IID data — the situation where each client's local distribution differs from the global distribution — is the central technical problem in federated learning, and it manifests in three distinct ways. Feature skew occurs when the input distributions differ: one hospital's imaging equipment produces different pixel characteristics than another's. Label skew occurs when the outcome distribution differs: a branch in a commercial district sees a different mix of fraud types than a rural branch. Quantity skew, the most common in practice, occurs when clients hold wildly different amounts of data, so that naive averaging lets a few large clients dominate the global model.</p>
<p>The effect on training is that local updates point in different directions, and simple averaging — the FedAvg approach — can oscillate or converge to a model that serves the majority distribution and performs poorly on minority participants. That last failure matters commercially, because fairness across participants is usually the reason the consortium was formed. Mitigations exist and are chosen per deployment: FedProx adds a proximal term that constrains how far a local update can drift from the global model, which stabilises training under heterogeneity; SCAFFOLD uses control variates to correct client drift explicitly; and personalised or clustered federation trains distinct models for groups of similar clients rather than forcing one model on all.</p>
<p>Diagnosing the problem matters as much as choosing the mitigation, and the diagnostic is simpler than it sounds: measure each client's local performance against the global model, and look at the spread. A model that performs well on average but badly at a subset of clients is exhibiting heterogeneity failure, and the right response may be clustering rather than more tuning. Teams that skip the diagnostic often spend months tuning an aggregation algorithm for a problem that was really about participant grouping.</p>
<h2 id="how-do-you-validate-a-federated-model">How Do You Validate and Monitor a Federated Model?</h2>
<p>Validation in a federated setting is harder than in centralised training because no single party holds a representative holdout set. Three practices cover the gap. The first is a federated evaluation round: the orchestrator distributes the current global model to participants, who score it on their own held-out local data and return only the metrics. This produces per-client performance without moving data, and it is the only way to see the heterogeneity spread described above.</p>
<p>The second is a centrally held, non-sensitive benchmark where one exists. Many consortia can assemble a small public or synthetic validation set that any participant could legally hold, which gives a stable reference point across training rounds even though it may not represent every client. The third is shadow evaluation against the incumbent system: run the federated model alongside whatever is in production today and compare decisions on live traffic, which is the most convincing evidence for participants who are being asked to trust a model they cannot inspect.</p>
<p>Monitoring after deployment borrows from conventional MLOps, with two additions. Contribution monitoring tracks which participants are actually sending useful updates and which have gone silent, because in a federated fleet attrition is silent — a hospital that stops contributing does not raise an error, it just quietly stops improving the model. And update-quality monitoring screens incoming updates for poisoning, using robust aggregation methods that limit the influence of any single client's contribution. Together these make the difference between a federation that decays quietly and one whose participants can see their own contribution reflected in a model that keeps improving.</p>
"""

ZH_NEWS = """<h2 id="联邦学习与其他隐私增强技术如何比较">联邦学习与其他隐私增强技术相比如何？</h2>
<p>联邦学习是多种隐私增强技术之一，在它们之间做选择属于设计决策，而非偏好问题。差分隐私通过加入经过标定的统计噪声来保护个体记录，它与联邦学习天然可组合——通常作用于模型更新，而不是作为联邦的替代方案。其权衡是显式且可调的：噪声越大，隐私保证越强，模型精度越低。安全多方计算允许多方在不看到彼此输入的前提下共同计算某个函数，它比联邦更强，但通信与算力开销大得多。同态加密允许直接在密文上计算，原则上是最强的选项，但目前的开销把它限制在很窄的工作负载上。</p>
<p>实践中的区别在于：联邦学习让原始数据留在原地、只移动模型，这使它特别适合那些数据根本无法合法或实际集中的场景——跨境银行业务、多医院联合研究、消费级设备上的端侧学习。安全多方计算与同态加密更适合"必须共同执行某项特定计算、且开销可接受"的场景。多数生产部署会组合使用：用联邦训练做学习循环，用安全聚合保护传输中的更新，再用差分隐私限定更新所能泄露的信息。</p>
<p>有一点值得强调，因为它被广泛误解：联邦学习不等于匿名化。在某些条件下，模型更新会泄露训练数据的信息——成员推断攻击与梯度反演攻击是真实存在且有文献记录的。正因如此，差分隐私与安全聚合被视为严肃部署的组成部分，而不是可选配件；也正因如此，任何"仅靠联邦就使数据共享合规"的说法，都应当被隐私负责人以怀疑的眼光看待。</p>
<h2 id="非独立同分布数据会带来什么影响">非独立同分布数据会给联邦模型带来什么影响？</h2>
<p>非独立同分布数据——即每个客户端的局部分布与全局分布不一致——是联邦学习的核心技术问题，它以三种不同方式表现出来。特征偏移指输入分布不同：一家医院的影像设备产生的像素特征与另一家不同。标签偏移指结果分布不同：商业区的分行看到的欺诈类型组合与乡村分行不同。数量偏移在实践中最常见，指各客户端持有的数据量差异悬殊，以至于朴素平均会让少数几个大客户端主导全局模型。</p>
<p>对训练的影响是：各方的局部更新指向不同方向，而简单平均——即 FedAvg 方法——可能来回震荡，或收敛到一个服务多数分布、却在少数参与方上表现糟糕的模型。后一种失败在商业上尤其重要，因为跨参与方的公平性通常正是联盟成立的原因。缓解手段是存在的，并且需要按部署逐一选择：FedProx 增加一个近端项，限制局部更新偏离全局模型的幅度，从而在异质性下稳定训练；SCAFFOLD 用控制变量显式校正客户端漂移；而个性化或分群联邦则为相似的客户端群体训练不同模型，而不是强行用一个模型覆盖所有人。</p>
<p>诊断问题与选择缓解手段同样重要，而诊断比想象中简单：测量每个客户端在全局模型上的局部表现，然后看离散程度。一个平均表现良好、却在某些客户端上表现很差的模型，正在表现出异质性失败，而正确的应对可能是分群，而不是继续调参。跳过诊断的团队，往往会花几个月去调一个聚合算法，而问题的根源其实在于参与方分组。</p>
<h2 id="如何验证与监控联邦模型">应当如何验证与监控联邦模型？</h2>
<p>联邦场景下的验证比集中式训练更难，因为没有任何一方持有具有代表性的留出集。三项实践可以补上这个缺口。其一是联邦评估轮次：编排方把当前全局模型下发给各参与方，各方在自己的留出数据上打分，只回传指标。这样能在不移动数据的前提下得到逐客户端的表现，也是观察上述异质性离散度的唯一方法。</p>
<p>其二是——只要存在——一个集中持有的、非敏感的基准集。许多联盟可以拼出一个任何参与方都能合法持有的小型公开或合成验证集，从而在训练轮次之间提供稳定的参照点，即便它未必能代表每一个客户端。其三是针对现有系统的影子评估：让联邦模型与当前生产环境中的系统并行运行，在真实流量上比较决策，对于那些被要求信任一个自己无法检查的模型的参与方来说，这是最有说服力的证据。</p>
<p>部署后的监控沿用常规 MLOps，但多了两项。贡献度监控跟踪哪些参与方确实在发送有用的更新、哪些已经静默，因为在联邦集群中，流失是无声的——一家停止贡献的医院不会报错，它只是悄悄地不再改进模型。更新质量监控则筛查传入的更新是否被投毒，采用稳健聚合方法来限制任何单一客户端贡献的影响力。这两项合在一起，决定了一个联邦体系是悄然衰败，还是让参与方看到自己的贡献反映在一个持续改进的模型上。</p>
"""

EN_H2 = [
    ("What is Federated Learning? — A Concise Definition", "What Is Federated Learning? — A Concise Definition"),
    ("Key Components of Federated Learning", "What Are the Key Components of Federated Learning?"),
    ("Why Federated Learning Matters for Enterprises", "Why Does Federated Learning Matter for Enterprises?"),
    ("Common Use Cases", "Which Use Cases Suit Federated Learning Best?"),
    ("How Federated Learning Fits into Beehive Strategy's Approach",
     "How Does Federated Learning Fit Into Beehive Strategy's Approach?"),
    ("Getting Started with Federated Learning", "How Should You Get Started With Federated Learning?"),
]
CN_H2 = [
    ("什么是联邦学习？——简明定义", "什么是联邦学习？"),
    ("联邦学习的关键组件", "联邦学习的关键组件有哪些？"),
    ("为什么联邦学习对企业很重要", "为什么联邦学习对企业很重要？"),
    ("常见使用场景", "哪些使用场景最适合联邦学习？"),
    ("联邦学习如何融入蜂启咨询的方法", "联邦学习如何融入蜂启咨询的方法？"),
    ("联邦学习入门指南", "应当如何着手引入联邦学习？"),
]
TW_H2 = [
    ("什麼是聯邦學習？——簡明定義", "什麼是聯邦學習？"),
    ("聯邦學習的關鍵組件", "聯邦學習的關鍵組件有哪些？"),
    ("爲什麼聯邦學習對企業很重要", "爲什麼聯邦學習對企業很重要？"),
    ("常見使用場景", "哪些使用場景最適合聯邦學習？"),
    ("聯邦學習如何融入蜂啓諮詢的方法", "聯邦學習如何融入蜂啓諮詢的方法？"),
    ("聯邦學習入門指南", "應當如何着手引入聯邦學習？"),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    anchor = '            <section class="faq-section"'
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + EN_NEWS + "\n" + anchor)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body expanded")

    cn = path_of(SLUG, "cn")
    h = open(cn, encoding="utf-8").read()
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + ZH_NEWS + "\n" + anchor)
    open(cn, "w", encoding="utf-8").write(h)
    print("CN body expanded")

    tw = path_of(SLUG, "tw")
    h = open(tw, encoding="utf-8").read()
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + s2t_fixed(ZH_NEWS) + "\n" + anchor)
    open(tw, "w", encoding="utf-8").write(h)
    print("TW body expanded")

    for old, new in EN_H2:
        retitle_by_text(en, old, new)
    for old, new in CN_H2:
        retitle_by_text(path_of(SLUG, "cn"), old, new)
    for old, new in TW_H2:
        retitle_by_text(path_of(SLUG, "tw"), old, new)
    print("H2s converted in en/cn/tw")
