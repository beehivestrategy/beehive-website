#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "federated-learning-data-governance-challenges"

EN_NEW = """
<h2 id="how-do-you-detect-and-contain-a-poisoned-node">How Do You Detect and Contain a Poisoned Node?</h2>
<p>Node quality heterogeneity is the risk that turns federated learning from an architecture into a liability. A node with stale records, mislabelled data, or deliberately adversarial inputs does not fail loudly — it shifts the global model slightly, every round, in a direction nobody authorised. Four controls make the network defensible.</p>
<table>
<thead>
<tr><th>Control</th><th>What it does</th><th>What it catches</th></tr>
</thead>
<tbody>
<tr><td>Per-node quality scoring</td><td>Scores each node on freshness, completeness, schema conformance and label consistency before its update is accepted</td><td>Stale or corrupted local data degrading the global model</td></tr>
<tr><td>Update validation</td><td>Tests each node's contribution against a held-out validation set held at the coordinator</td><td>Updates that degrade model performance rather than improve it</td></tr>
<tr><td>Byzantine-robust aggregation</td><td>Uses trimmed mean or median-based aggregation rather than a plain average</td><td>Single nodes pushing extreme updates to steer the model</td></tr>
<tr><td>Contribution weighting and quarantine</td><td>Weights updates by historical quality and isolates nodes that fail validation repeatedly</td><td>Persistent poisoning and compromised participants</td></tr>
</tbody>
</table>
<p>The control most often skipped is the held-out validation set. Coordinators reason that holding data centrally defeats the purpose of federation, and it would — if the validation set were large. In practice a small, representative, centrally-held validation sample is what makes update validation possible at all, and most federated programmes find a way to assemble one under the same approvals that govern the rest of the work.</p>
<p>Containment matters as much as detection. Define in advance what happens when a node fails validation twice: automatic quarantine, notification to the node's named owner, and a documented path back into the network. Programmes that improvise this decision during an incident discover that no one is certain who may exclude a participant.</p>
<h2 id="what-privacy-techniques-actually-protect-gradients">What Privacy Techniques Actually Protect Gradients?</h2>
<p>The uncomfortable finding in the privacy literature is that sharing model updates is not the same as sharing nothing. Published research has repeatedly demonstrated that gradients can be reverse-engineered to reconstruct training samples, sometimes with high fidelity. Governance that treats updates as inherently anonymous is governance built on an assumption that has been falsified.</p>
<p>Three techniques do the real work, and they compose.</p>
<ul>
<li><strong>Secure aggregation.</strong> Cryptographic protocols let the coordinator compute the sum of updates without ever seeing any individual node's contribution. This defeats straightforward inspection of a single participant's gradient, and it is the baseline control most mature programmes implement first.</li>
<li><strong>Differential privacy.</strong> Calibrated noise is added to updates before they leave the node, bounding how much any single record can influence the result. It comes with an explicit accuracy cost, and the privacy budget — epsilon — has to be chosen deliberately and recorded, because it is the number a regulator will ask about.</li>
<li><strong>Update clipping and subsampling.</strong> Bounding the magnitude of any single update limits the influence one participant or one record can exert, and it makes the differential privacy accounting meaningful rather than nominal.</li>
</ul>
<p>What none of these techniques does is make the legal question disappear. Regulators in several jurisdictions treat model updates as personal data in some circumstances, which means the transfer of an update across a border can be a regulated transfer even though no raw record moved. Technical protection and legal review are complements, not substitutes, and programmes that present encryption as an answer to a transfer question tend to have that answer rejected.</p>
<h2 id="how-do-you-score-and-weight-node-contributions">How Do You Score and Weight Node Contributions?</h2>
<p>Naive federated averaging weights every node equally, which means a node with a hundred clean records counts as much as a node with a hundred thousand. Contribution weighting fixes the model quality problem and, just as importantly, makes governance legible.</p>
<p>A workable contribution score combines four inputs: the volume of local data, its measured quality at the last audit, the historical usefulness of the node's updates, and the strategic importance of the domain the node covers. Weighting by volume alone reintroduces the quality problem; weighting by quality alone can let a tiny, pristine node dominate. Most programmes land on volume weighted by a quality multiplier, with a floor so that small domains are not silenced.</p>
<p>The governance value is that the score is an artefact. When a node's data degrades, its contribution weight falls automatically and its owner receives a notification with a specific remediation list. When an auditor asks how the network ensures that poor-quality participants cannot distort outcomes, the answer is a documented scoring rule and a log of its application rather than an assurance.</p>
<p>Publish the scoring rule to participants. Federated programmes depend on the continued willingness of semi-autonomous teams to stay in the network, and opaque weighting is one of the fastest ways to lose them. Transparency about how contribution is measured is what converts governance from a constraint imposed by the centre into a term of participation that everyone has agreed to.</p>
<h2 id="what-does-cross-border-federated-governance-require-legally">What Does Cross-Border Federated Governance Require Legally?</h2>
<p>The appeal of federated learning in a cross-border context is obvious: train on data that never leaves its jurisdiction. The legal reality is more nuanced, and getting it wrong is expensive because the mistake surfaces during an audit rather than during design.</p>
<p>Three questions need written answers before the first training round. First, is the model update itself personal data in the relevant jurisdictions? The answer varies, and the conservative assumption — that it may be — is the one most programmes adopt. Second, if it is, what is the lawful basis for transferring it? Standard contractual clauses, adequacy decisions, and binding corporate rules each have conditions that a federated topology must satisfy, and the conditions attach to the update even though the raw data stayed home. Third, which regulator has jurisdiction over the coordinator, and what does that regulator expect to see in the audit trail?</p>
<p>Beyond transfer mechanics, cross-border programmes need a per-node legal register: the jurisdictions in play, the applicable framework for each, the lawful basis relied on, and the date of the last review. This register is small and it is the first document an examiner asks for. Programmes that maintain it alongside the technical node inventory move through review in weeks; programmes that assemble it on request spend months and usually discover a gap they cannot retroactively close.</p>
<p>One practical note: legal review should cover the update protocol, not just the data. Several programmes have discovered late that their aggregation schedule creates a transfer pattern nobody assessed — for example, an intermediate partial model that crosses a border on its way to the coordinator.</p>
"""

FAQ = {
 "EN": [
  ("Does federated learning remove the need for data governance?",
   "No - it relocates governance obligations rather than eliminating them. Because no one can inspect centralised data, oversight has to move to the node level: per-node quality scoring, local lineage, update validation, and distributed audit logging. Enterprises with mature governance report materially faster federated deployment than those treating it as a privacy shortcut."),
  ("Can model updates really leak training data?",
   "Yes. Published research has repeatedly demonstrated that gradients can be reverse-engineered to reconstruct training samples. That is why secure aggregation, differential privacy with a recorded privacy budget, and update clipping are baseline controls rather than optional enhancements - and why legal review should treat updates as potentially personal data."),
  ("How do you handle a node with consistently poor data quality?",
   "Score every node on freshness, completeness, schema conformance and label consistency, then weight its contribution by that score and quarantine it after repeated validation failures. The key is defining the quarantine and remediation path in advance, with a named owner for each node and a documented route back into the network."),
  ("How long does federated governance maturity take?",
   "Most enterprises reach federated governance maturity within 18 to 24 months, following three phases: per-node baselines and monitoring in months one to three, cross-node lineage and secure aggregation in months four to nine, and contribution-weighted predictive governance from month ten. Discovering the requirements during an audit is far more expensive than designing them in."),
 ],
 "zh-CN": [
  ("联邦学习是否就不再需要数据治理了？",
   "不是——它只是把治理义务从一个位置转移到了另一个位置，而不是消除了它们。由于没有人能检查集中式的数据，监督必须下沉到节点层：逐节点质量评分、本地血缘、更新验证，以及分布式审计日志。治理成熟的企业报告称，其联邦部署速度明显快于那些把联邦学习当成隐私捷径的对手。"),
  ("模型更新真的会泄露训练数据吗？",
   "会。已发表的研究多次证明，梯度可以被逆向工程以重建训练样本。正因如此，安全聚合、带记录的隐私预算的差分隐私，以及更新裁剪是基线控制，而不是可选增强——也正因如此，法律评审应当把更新视为可能是个人数据。"),
  ("如何处理数据质量持续偏低的节点？",
   "对每个节点在时效性、完整性、模式一致性和标注一致性上打分，据此对其贡献加权，并在多次验证失败后将其隔离。关键在于提前定义隔离与修复路径，为每个节点指定责任人，并规定回归网络的明确流程。"),
  ("达到联邦治理成熟需要多久？",
   "多数企业在18到24个月内达到联邦治理成熟，分三个阶段推进：第1到3个月建立逐节点基线与监控，第4到9个月建立跨节点血缘与安全聚合，第10个月起转向按贡献加权的预测性治理。在审计过程中才发现这些要求，代价远高于在设计阶段就纳入它们。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<section class="faq-section"'
    if anchor not in b:
        anchor = '<section[^>]*faq-section'
    assert anchor in b, "anchor"
    b = b.replace(anchor, EN_NEW.strip() + "\n\n            " + anchor, 1)
    ren = {
        "The New Imperative for Data Governance": "Why Does Federated Learning Change the Governance Imperative?",
        "Modern Governance Framework Architecture": "What Does a Federated Governance Architecture Look Like?",
        "Implementation Roadmap and Success Metrics": "What Should an Implementation Roadmap and Its Metrics Include?",
        "Data Governance Organizational Architecture and Operating Model": "Who Owns Governance in a Federated Network?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    b = b.replace("其federated", "其联邦").replace("大federated", "大联邦")
    b = b.replace("的data", "的数据").replace("施data", "施数据")
    ren_cn = {
        "数据治理的新紧迫性": "为什么联邦学习改变了治理的紧迫性？",
        "现代治理框架架构": "联邦治理框架架构是什么样的？",
        "实施路线图与成功指标": "实施路线图与成功指标应该如何设定？",
        "数据治理的技术实现与工具生态": "技术实现与工具生态需要考虑什么？",
        "数据治理组织架构与运营模式": "联邦网络中的治理由谁负责？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    dup = "战略实施路径与关键成功因素"
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(dup) + r'(</h2>)', r'\g<1>' + "战略实施路径与关键成功因素是什么？" + r'\g<2>', b, count=1)
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape("企业实施路线图与成功因素") + r'(</h2>)', r'\g<1>' + "企业实施路线图的关键成功因素有哪些？" + r'\g<2>', b, count=1)
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape("行业数字化转型深度分析") + r'(</h2>)', r'\g<1>' + "行业数字化转型中有哪些可借鉴的经验？" + r'\g<2>', b, count=1)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
