#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "what-is-mlops-machine-learning-operations"

EN_NEW = """
<h2 id="what-does-a-minimum-viable-mlops-setup-look-like">What Does a Minimum Viable MLOps Setup Look Like?</h2>
<p>The most common reason MLOps programmes stall is that teams read the capability list of a mature platform and try to build all of it. A minimum viable setup is smaller than most teams expect, and it is achievable in one quarter with three or four engineers.</p>
<table>
<thead>
<tr><th>Capability</th><th>Minimum viable version</th><th>Why it comes first</th></tr>
</thead>
<tbody>
<tr><td>Version control for data and code</td><td>Training data referenced by immutable version, model artefacts stored with metadata</td><td>Without it nothing is reproducible, and every incident becomes an archaeology exercise</td></tr>
<tr><td>Automated training pipeline</td><td>One command reproduces a model from a pinned data version and code commit</td><td>Manual retraining is where the 70 to 90 percent failure rate is manufactured</td></tr>
<tr><td>Model registry</td><td>Stored artefacts with version, owner, metrics, and approval state</td><td>This is the system of record that governance and rollback both depend on</td></tr>
<tr><td>Deployment with rollback</td><td>Staged rollout and a tested path back to the previous version</td><td>Models fail in production; the question is whether recovery takes minutes or weeks</td></tr>
<tr><td>Basic drift monitoring</td><td>Feature distribution alerts and a labelled performance sample</td><td>Silent degradation is the failure mode that destroys trust in ML</td></tr>
</tbody>
</table>
<p>Everything else — feature stores, automated retraining, sophisticated experiment tracking, cost attribution — comes after these five work on one real production model. The sequencing matters because each capability is only valuable once the one below it is stable. A feature store on top of unreproducible training is an expensive way to be wrong consistently.</p>
<p>Pick the pilot deliberately. The right first model has real production traffic, a business owner who will notice if it degrades, and enough complexity to exercise the pipeline without being the company's most critical system. Fraud scoring, demand forecasting, and document classification are all good first candidates; credit decisioning and clinical triage are not.</p>
<h2 id="how-do-you-detect-and-handle-model-drift-in-production">How Do You Detect and Handle Model Drift in Production?</h2>
<p>Drift is not one problem, and treating it as one is why monitoring often fails to fire until the business has already noticed. Three distinct phenomena need three distinct detectors.</p>
<p><strong>Data drift</strong> is a change in the input distribution: the population the model scores no longer looks like the population it was trained on. Detect it with statistical distance measures — population stability index or Kolmogorov-Smirnov tests on key features — with alert thresholds set per feature rather than globally. A two-standard-deviation rule on a handful of important features catches most real cases without drowning the team in noise.</p>
<p><strong>Concept drift</strong> is a change in the relationship between inputs and the outcome: the world changed, so the same inputs now imply different results. This is harder, because it can only be measured against ground truth, which usually arrives late. The practical approach is a labelled sample of live traffic — a few hundred cases reviewed per period — that lets you estimate real performance rather than proxying it.</p>
<p><strong>Upstream data drift</strong> is the one teams forget: a pipeline changed, a source system renamed a field, a join started dropping rows, and the model is now scoring on subtly different inputs. This is a data quality problem wearing a model monitoring costume, and it is caught by schema and volume checks at the input boundary, not by statistics on the features.</p>
<p>Handling drift requires a decision rule written before it happens. Define thresholds for investigate, retrain, and roll back; name who makes each call; and decide what happens to traffic while a model is suspect. Teams that define the escalation path in advance recover in days. Teams that improvise discover, during the incident, that nobody owns the decision.</p>
<h2 id="how-do-you-govern-models-for-regulated-industries">How Do You Govern Models for Regulated Industries?</h2>
<p>Regulators in financial services, healthcare, and under the EU AI Act ask a consistent set of questions, and MLOps is what makes the answers reproducible rather than reconstructed. Five artefacts cover most of what an examiner will request.</p>
<ul>
<li><strong>Model inventory with risk classification.</strong> Every model in production, its purpose, its owner, and its risk tier. Tiering determines the depth of everything else, so it has to be maintained as models are deployed, not assembled before an examination.</li>
<li><strong>Training data provenance.</strong> Which dataset version trained which model version, with lineage back to source systems. This is the question that cannot be answered retrospectively if versioning was not in place from the start.</li>
<li><strong>Validation evidence.</strong> Pre-deployment test results covering accuracy, fairness across relevant segments, and performance under stress conditions — retained with the model version they apply to.</li>
<li><strong>Change and approval history.</strong> Who approved each version, when, on what evidence, and what changed. Approval records living in email threads are the most common examination finding.</li>
<li><strong>Ongoing monitoring evidence.</strong> Drift and performance reports with the actions taken in response. Monitoring that produces reports nobody acts on is worse than no monitoring, because it documents the failure to respond.</li>
</ul>
<p>The pattern across all five is that they are produced by the pipeline rather than written about it. Governance built as documentation around a manual process fails the first time the model changes; governance emitted by an automated pipeline stays current by default.</p>
<h2 id="what-are-the-most-common-mlops-anti-patterns">What Are the Most Common MLOps Anti-Patterns?</h2>
<p>Five patterns reliably convert an MLOps investment into an expensive disappointment.</p>
<p><strong>Notebook-to-production handoff.</strong> A data scientist trains in a notebook and hands an artefact to engineering, who rewrite it. The rewrite diverges, accuracy changes, and nobody can explain why. The fix is a single training pipeline that runs identically in development and production.</p>
<p><strong>Monitoring the model but not the pipeline.</strong> Teams watch accuracy and miss the upstream schema change that broke the feature computation three weeks ago. Instrument the input boundary and the feature pipeline, not just the predictions.</p>
<p><strong>Buying the platform before defining the process.</strong> Vendors will sell the full capability set. Without an agreed process for promotion, approval, and rollback, the platform becomes a costly place to store untended artefacts.</p>
<p><strong>Automating retraining before automating validation.</strong> Retraining on a schedule without automated gates means a degraded model can be promoted automatically. Validation gates come first; automatic promotion is the last capability to add, not the first.</p>
<p><strong>Treating MLOps as a tooling purchase.</strong> The hard part is the operating model: who owns a model in production, who is paged when it degrades, and who approves a change. Tooling without those answers produces a platform nobody operates.</p>
"""

CN_NEW = """
<h2 id="what-are-the-most-common-mlops-anti-patterns">MLOps最常见的反面模式有哪些？</h2>
<p>有五种模式会稳定地把MLOps投资变成一次昂贵的失望。</p>
<p><strong>从笔记本直接交付生产。</strong>数据科学家在笔记本里训练出模型，把产出物交给工程团队重写。重写过程产生偏差，效果发生变化，而没有人能解释原因。解决办法只有一条：同一条训练流水线，在开发环境与生产环境中完全一致地运行。</p>
<p><strong>只监控模型，不监控流水线。</strong>团队盯着准确率，却漏掉了三周前破坏特征计算的上游模式变更。监控对象必须是输入边界和特征流水线，而不只是预测结果。</p>
<p><strong>流程未定，先买平台。</strong>厂商会推销完整的能力集。如果没有就晋级、审批和回滚达成一致的流程，平台只会变成一个昂贵的、无人打理的产出物仓库。</p>
<p><strong>先自动化重训，再自动化验证。</strong>按计划重训却没有自动化的准入门禁，等于让一个退化的模型被自动晋级。验证门禁必须先行；自动晋级是最后才添加的能力，而不是第一个。</p>
<p><strong>把MLOps当成一次工具采购。</strong>最难的部分是运营模式：生产环境中的模型归谁所有，退化时呼叫谁，变更由谁批准。没有这些答案，工具只会产出一个无人运营的平台。</p>
<p>这五个反面模式有一个共同点：它们都是组织问题伪装成技术问题。工具可以买到，运营模式不能。决定MLOps成败的，是能不能说清楚每个生产模型的责任人、升级路径和审批机制——而不是采购了哪一套平台。</p>
"""

FAQ = {
 "EN": [
  ("What is the difference between MLOps and DevOps?",
   "MLOps extends DevOps with ML-specific challenges: data versioning, model validation, drift monitoring, and experiment tracking. Code is deterministic and data is not, so the artefacts under version control, the tests that gate promotion, and the signals that indicate failure are all different in kind rather than degree."),
  ("What tools are commonly used in MLOps?",
   "MLflow, Kubeflow, Airflow, Prefect, Weights and Biases, DVC, and cloud-native services from AWS, GCP and Azure. Tool choice matters less than consolidation: organisations succeed by operating a small set of tools well rather than assembling a best-of-breed stack nobody owns."),
  ("What is model drift and why does it matter?",
   "Model drift occurs when production data patterns change, causing model performance to degrade. It matters because degradation is silent: without monitoring, a model can lose 5 to 10 percent accuracy within weeks of deployment in a volatile environment and nobody notices until a business stakeholder does."),
  ("How long does it take to implement MLOps?",
   "A minimum viable setup - versioned training data, an automated training pipeline, a model registry, deployment with rollback, and basic drift monitoring - is achievable in one quarter with three or four engineers, built around one real production model. Full maturity across a portfolio typically takes 12 to 18 months."),
 ],
 "zh-CN": [
  ("MLOps与DevOps有什么区别？",
   "MLOps在DevOps之上叠加了机器学习特有的挑战：数据版本化、模型验证、漂移监控和实验追踪。代码是确定性的，数据不是，因此被版本控制的对象、把关晋级的测试、以及指示失效的信号，在性质上而非程度上都完全不同。"),
  ("MLOps通常使用哪些工具？",
   "常见的有MLflow、Kubeflow、Airflow、Prefect、Weights and Biases、DVC，以及AWS、GCP和Azure的云原生服务。工具选型的重要性远不如收敛：成功的企业是把少量工具用好，而不是拼一套无人负责的最佳组合。"),
  ("什么是模型漂移，它为什么重要？",
   "模型漂移是指生产环境中的数据模式发生变化，导致模型效果退化。它的重要性在于退化是静默的：如果没有监控，在波动较大的环境中，模型可能在部署后数周内就损失5%到10%的准确率，而直到业务方察觉才有人发现。"),
  ("落地MLOps需要多长时间？",
   "一个最小可用集——版本化的训练数据、自动化的训练流水线、模型注册表、带回滚的部署，以及基础的漂移监控——由三到四名工程师围绕一个真实的生产模型，用一个季度即可建成。要在整个模型组合上达到成熟，通常需要12到18个月。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<h2 id="beehive-strategy-and-mlops">Beehive Strategy and MLOps</h2>'
    if anchor not in b:
        anchor = '<section class="faq-section"'
    b = b.replace(anchor, EN_NEW.strip() + "\n" + anchor, 1)
    ren = {
        "The MLOps Lifecycle": "What Does the MLOps Lifecycle Include?",
        "Key MLOps Components": "Which Components Make Up an MLOps Platform?",
        "Beehive Strategy and MLOps": "How Does Beehive Strategy Apply MLOps?",
        "Key Considerations for Implementation": "What Should You Consider Before Implementing MLOps?",
        "Beehive Strategy Comprehensive Approach": "What Does Beehive Strategy Deliver?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    anchor_cn = '<h2 id="总结与关键建议">总结与关键建议</h2>'
    if anchor_cn not in b:
        anchor_cn = '<section class="faq-section"'
    b = b.replace(anchor_cn, CN_NEW.strip() + "\n" + anchor_cn, 1)
    ren_cn = {
        "MLOps生命周期": "MLOps生命周期包含哪些阶段？",
        "为什么企业需要MLOps": "为什么企业需要MLOps？",
        "蜂启咨询与MLOps": "蜂启咨询如何实践MLOps？",
        "核心优势与技术特点": "MLOps平台包含哪些核心组件？",
        "实施策略与成功要素": "落地MLOps需要考虑什么？",
        "行业应用与未来展望": "MLOps在各行业的应用与未来走向是什么？",
        "总结与关键建议": "总结与关键建议是什么？",
        "蜂启咨询的综合解决方案": "蜂启咨询提供什么样的整体方案？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
