#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 12: why-mlops-critical-production-ai-systems
EN 1978 -> ~2700 ; CN/TW 2059 -> ~3600 ; H2 -> questions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_by_text, s2t_fixed

SLUG = "why-mlops-critical-production-ai-systems"
# NOTE: this file's FAQ section is indented with 8 spaces, not 12
ANCHOR = '        <section class="faq-section"'

EN_NEWS = """<h2 id="what-does-a-minimum-viable-mlops-stack-look-like">What Does a Minimum Viable MLOps Stack Look Like?</h2>
<p>The minimum viable stack is smaller than most platform roadmaps suggest, and it fits into five capabilities that can be built in a quarter for the first handful of models. Version control for data, code, and configuration, so that any training run can be reproduced from a commit hash. An automated training pipeline that takes a registered dataset and a configuration to a candidate model artefact without manual steps. A model registry that records every artefact with its metrics, its lineage, and its promotion status. A deployment path with at least one staging gate and a documented rollback. And monitoring that tracks the inputs, the outputs, and the outcome the model influences.</p>
<p>The sequencing matters more than the tooling. Teams that buy an end-to-end platform first and then look for problems to solve with it routinely end up with expensive shelfware, because the platform's assumptions do not match the organisation's actual failure modes. The alternative is to instrument the models already in production, find out what actually breaks — a feature pipeline that silently returns stale data, a retraining step nobody owns, a rollback that has never been tested — and build the thinnest thing that fixes it. That thin version becomes the template every subsequent model inherits.</p>
<p>Two capabilities are worth over-investing in relative to their apparent cost. Automated retraining is the first: retraining that requires a person to remember, schedule, and verify is retraining that happens late, and late retraining is the single most common cause of silent degradation. Tested rollback is the second, because the ability to revert a bad model in minutes is what makes shipping frequent model updates safe — and without it, teams ship rarely, which makes every release larger and riskier.</p>
<h2 id="how-should-you-structure-ownership">How Should You Structure MLOps Ownership and Teams?</h2>
<p>MLOps fails organisationally far more often than technically, and the failure is almost always the same: a gap between the team that builds the model and the team that runs it. Data scientists are measured on model quality at handoff; platform engineers are measured on uptime. Nobody is measured on whether the model still works in month six, so nobody notices when it stops. The fix is a named owner per production model, with accountability for its behaviour after deployment, not just for its accuracy at launch.</p>
<p>Three operating models work, and the choice depends on scale. In the embedded model, the data science team owns the model through production and borrows platform capability as needed — this works up to roughly ten models and keeps ownership unambiguous. In the platform model, a central MLOps team owns the pipelines, registry, and monitoring, while model teams own their models' behaviour; this scales well but requires a crisp interface between the two, usually expressed as a supported template. In the product-team model, a cross-functional team owns a business domain's models end to end, which is the strongest arrangement and the most demanding of engineering maturity.</p>
<p>Whichever model applies, one practice is non-negotiable: a recurring review where model performance, drift, and business impact are examined together with the stakeholders who depend on the outputs. That meeting is where a technical metric becomes a business decision, and where the retraining backlog gets prioritised against real consequences. Teams that hold it catch degradation while it is still cheap to fix; teams that skip it discover problems through complaints, at which point the cost is measured in trust rather than in compute.</p>
"""

ZH_NEWS = """<h2 id="最小可行的MLOps技术栈长什么样">最小可行的MLOps技术栈长什么样？</h2>
<p>最小可行技术栈比多数平台路线图所设想的要小，它可以收敛为五项能力，针对首批几个模型，一个季度内就能建成。其一，对数据、代码与配置做版本管理，使任何一次训练都能凭一个提交哈希复现。其二，一条自动化训练管道，从已注册的数据集与配置直接产出候选模型产物，无需人工步骤。其三，一个模型注册表，记录每个产物及其指标、血缘与晋升状态。其四，一条至少含一道预发布关卡、并有书面回滚方案的部署路径。其五，对模型输入、输出以及它所影响的业务结果做监控。</p>
<p>排序比工具更重要。先买一套端到端平台、再去找问题来适配它的团队，常常得到昂贵的架子货，因为平台的假设与组织真实的失败模式对不上。替代做法是：先给已经在生产的模型装上仪表，找出真正会坏的地方——一条静默返回陈旧数据的特征管道、一个无人负责的重训步骤、一次从未演练过的回滚——然后构建能修好它的最薄方案。这个薄版本会成为此后每个模型继承的模板。</p>
<p>有两项能力值得相对于表面成本超额投入。第一是自动化重训：需要有人记得、去排期、再去验证的重训，一定是迟到的重训，而迟到的重训是静默衰减最常见的原因。第二是演练过的回滚：能够在几分钟内撤回一个坏模型，才让频繁的模型更新变得安全；没有它，团队就很少发布，而这使得每次发布的变更更大、风险更高。</p>
<h2 id="MLOps的所有权与团队应如何组织">MLOps的所有权与团队应当如何组织？</h2>
<p>MLOps 在组织层面失败的频率远高于技术层面，而失败几乎总是同一个模式：构建模型的团队与运行模型的团队之间出现了断层。数据科学家的考核指标是交付时的模型质量，平台工程师的考核指标是在线可用率，没有人被考核"模型在第六个月是否仍然有效"，于是当它失效时也没人察觉。解决办法是为每个生产模型指定一位具名负责人，对模型部署之后的行为负责，而不只是对上线时的准确率负责。</p>
<p>有三种运营模式可行，选择取决于规模。嵌入式模式下，数据科学团队端到端拥有模型，按需借用平台能力——这在大约十个模型以内运转良好，且所有权没有歧义。平台模式下，一个中央 MLOps 团队拥有管道、注册表与监控，而模型团队拥有各自模型的行为——这种模式扩展性良好，但两者之间需要清晰的接口，通常体现为一套受支持的模板。产品团队模式下，一个跨职能团队端到端拥有某个业务域的模型，这是最牢固的安排，也对工程成熟度要求最高。</p>
<p>无论采用哪种模式，有一项实践不可妥协：定期召开评审会，把模型表现、漂移与业务影响放在一起，与依赖这些输出的利益相关方共同检视。正是在这个会议上，技术指标才变成业务决策，重训待办才得以对照真实后果排优先级。坚持开这个会的团队，能在代价还很低的时候抓住衰减；跳过它的团队，则通过投诉发现问题，而那时的代价是用信任而非算力来计量的。</p>
"""

EN_H2 = [
    ("5 Reasons MLOps Is Critical for Production AI", "Why Is MLOps Critical for Production AI?"),
    ("Core Components of an MLOps Platform", "What Are the Core Components of an MLOps Platform?"),
    ("Common MLOps Pitfalls to Avoid", "Which MLOps Pitfalls Should You Avoid?"),
    ("Building the Business Case for MLOps", "How Do You Build the Business Case for MLOps?"),
    ("MLOps vs. Ad-Hoc AI Deployment", "How Does MLOps Compare to Ad-Hoc AI Deployment?"),
    ("How Beehive Strategy Helps", "How Does Beehive Strategy Help?"),
]
CN_H2 = [
    ("MLOps对生产级AI至关重要的5个原因", "为什么MLOps对生产级AI至关重要？"),
    ("MLOps vs. 临时AI部署", "MLOps与临时式AI部署相比如何？"),
    ("蜂启咨询如何帮助", "蜂启咨询能提供哪些帮助？"),
]
TW_H2 = [
    ("MLOps對生產級AI至關重要的5個原因", "爲什麼MLOps對生產級AI至關重要？"),
    ("MLOps vs. 臨時AI部署", "MLOps與臨時式AI部署相比如何？"),
    ("蜂啓諮詢如何幫助", "蜂啓諮詢能提供哪些幫助？"),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    assert h.count(ANCHOR) == 1, h.count(ANCHOR)
    h = h.replace(ANCHOR, "\n" + EN_NEWS + "\n" + ANCHOR)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body expanded")

    cn = path_of(SLUG, "cn")
    h = open(cn, encoding="utf-8").read()
    assert h.count(ANCHOR) == 1, h.count(ANCHOR)
    h = h.replace(ANCHOR, "\n" + ZH_NEWS + "\n" + ANCHOR)
    open(cn, "w", encoding="utf-8").write(h)
    print("CN body expanded")

    tw = path_of(SLUG, "tw")
    h = open(tw, encoding="utf-8").read()
    assert h.count(ANCHOR) == 1, h.count(ANCHOR)
    h = h.replace(ANCHOR, "\n" + s2t_fixed(ZH_NEWS) + "\n" + ANCHOR)
    open(tw, "w", encoding="utf-8").write(h)
    print("TW body expanded")

    for old, new in EN_H2:
        retitle_by_text(en, old, new)
    for old, new in CN_H2:
        retitle_by_text(path_of(SLUG, "cn"), old, new)
    for old, new in TW_H2:
        retitle_by_text(path_of(SLUG, "tw"), old, new)
    print("H2s converted in en/cn/tw")
