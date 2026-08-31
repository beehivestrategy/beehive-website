#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 02: small-language-models-for-cost-effective-enterprise-ai"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import run, replace_once, path_of, s2t_fixed

SLUG = "small-language-models-for-cost-effective-enterprise-ai"

# ---- 1. repair two garbled passages in EN ----
EN_FIX_1_OLD = "When the task is narrow, repetitive, and latency-sensitive. A classification model for invoice line items,"
EN_FIX_1_NEW = "Choose a small language model when the task is narrow, repetitive, and latency-sensitive. A classification model for invoice line items,"

EN_FIX_2_OLD = "The emerging best practice is model routing: a small model handles the l-tuning effort (data labelling, training runs, evaluation), an inference footprint sized to the throughput requirement, and an ongoing maintenance commitment for retraining when the task drifts."
EN_FIX_2_NEW = "The emerging best practice is model routing: a small model handles the routine majority of requests and escalates low-confidence cases to a frontier model. The business case then weighs the fine-tuning effort (data labelling, training runs, evaluation), an inference footprint sized to the throughput requirement, and an ongoing maintenance commitment for retraining when the task drifts — against the frontier alternative's per-token cost at the same volume."

EN_NEWS = """<h2 id="how-should-you-size-a-small-language-model">How Should You Size a Small Language Model for the Task?</h2>
<p>Sizing is an empirical question with a useful starting map. In the 1B to 3B band, models handle tight classification, routing, and extraction over short contexts — intent labels, invoice field capture, ticket triage — and can often run on CPU or a single consumer-grade GPU, which makes them attractive for edge and on-premises deployments where no accelerator is available. The 7B to 9B band is the current workhorse: it absorbs instruction-following and light multi-step reasoning, handles summarisation over several pages of context, and is the range where fine-tuning most often produces a model that matches frontier quality on a narrow task. The 13B to 14B band is reserved for tasks that need genuine reasoning or long-context synthesis — comparing contract clauses across a long document, or reconciling conflicting figures in a financial narrative — and it is the point at which the cost advantage over frontier APIs narrows enough that the decision deserves a fresh business case.</p>
<p>Two techniques widen the usable range of a given size. Quantisation — running weights at 8-bit or 4-bit precision rather than 16-bit — typically cuts memory and compute by two to four times with a small, measurable accuracy cost, and that cost is usually recovered by fine-tuning on the target task. Distillation, in which a larger teacher model generates training signal for a smaller student, is how many production small models reach accuracy levels their parameter count alone would not suggest. Neither technique removes the need to measure: quantisation and distillation behave differently per task, and the only defensible answer is an accuracy run against your own golden dataset at the quantisation level you actually intend to deploy.</p>
<p>On fine-tuning method, the practical default for enterprises is parameter-efficient fine-tuning — LoRA and related adapter approaches — rather than full fine-tuning. Adapters train a small number of additional weights against a frozen base model, which reduces training compute by roughly an order of magnitude, keeps the base model intact for other tasks, and produces adapters that can be swapped per task at inference time. Full fine-tuning still wins when the target task sits far from the base model's pretraining distribution, or when every point of accuracy justifies the training cost. For the majority of enterprise classification and extraction work, however, adapters deliver most of the benefit at a fraction of the cost and operational risk.</p>
<h2 id="what-does-a-reliable-slm-evaluation-process-look-like">What Does a Reliable SLM Evaluation Process Look Like?</h2>
<p>Evaluation is where small-model programmes succeed or quietly fail, and the failure is rarely dramatic. A team tunes a 7B model, sees accuracy improve on a handful of hand-checked examples, and ships. Months later the model is handling a materially different mix of inputs and nobody can say whether accuracy has moved, because no baseline was recorded and no fixed test set exists to re-run. The remedy is unglamorous and cheap: a golden dataset of a few hundred to a few thousand labelled examples per task, held out from training, stratified across the cases that matter most — including the edge cases and the rare classes, which are exactly where a small model degrades first.</p>
<p>With a golden set in place, three practices carry most of the value. Measure per label, not just overall accuracy: a model scoring 94% overall can be failing badly on the 6% of cases that carry the most business consequence, and an aggregate metric hides that. Automate the run so every retraining and every quantisation change is scored against the same set before promotion, turning model updates into a gated pipeline rather than a judgement call. And sample production traffic for periodic human review, because the golden set ages — the language of customer requests, the format of supplier invoices, and the taxonomy of support tickets all drift, and drift is invisible without fresh labels.</p>
<p>Rollout discipline follows from the same instrumentation. Shadow deployment — running the small model alongside the incumbent frontier model or human process and comparing outputs without acting on them — gives a safe read on real traffic before any user is exposed. Canary release to a small percentage of traffic, with an automatic rollback trigger tied to the accuracy or escalation-rate metric, bounds the damage of a bad promotion. Only a programme with this scaffolding can honestly claim that a small model is cheaper, because without it the cost of a silent accuracy regression is simply moved off the invoice and onto the business.</p>
<h2 id="which-workloads-are-the-best-first-slm-candidates">Which Enterprise Workloads Are the Best First SLM Candidates?</h2>
<p>The best first candidates share four properties, and checking them explicitly prevents the most common SLM disappointment — picking a task that was never narrow to begin with. The task must be well-defined, with an output that can be specified precisely enough for a label to be uncontroversial: this clause is or is not a termination provision; this ticket is billing, technical, or provisioning. It must be high-volume, because amortisation is the entire economic argument. It must be stable, meaning the label set and input distribution do not change every quarter. And it must carry a tolerable error cost, or a cheap verification step, so that the residual error rate is manageable rather than existential.</p>
<p>Using those criteria, the reliable first movers are remarkably consistent across industries. Document and form extraction — invoices, contracts, claims, purchase orders — is almost always the highest-volume, most stable language work in an enterprise, and it is where small models most often replace both a frontier API and a brittle rules engine. Classification and routing of inbound text, from support tickets to expense line items, is the second, and it tends to improve sharply with domain fine-tuning because internal taxonomies are idiosyncratic by definition. Structured summarisation — condensing a case history or a call transcript into a fixed template — is the third, and it benefits from the fact that the output format is constrained, which is precisely the condition under which small models do well.</p>
<p>The tasks to keep on frontier models for now are equally consistent: open-ended drafting, multi-document reasoning where the relevant facts are unbound, anything requiring current world knowledge, and low-volume analytical work where cost is immaterial next to the quality requirement. A useful way to hold both lists is a quarterly portfolio review that re-buckets workloads as volume and stability change — because a task that starts as exploratory often becomes high-volume and stable within a year, and that is the moment its cost profile justifies revisiting.</p>
"""

# ---- zh-CN additions (Simplified) ----
ZH_NEWS = """<h2 id="如何为任务选定小模型规模">如何为任务选定小模型的规模？</h2>
<p>规模选择是一个实证问题，但有一张可用的起始地图。1B至3B区间适合上下文较短的紧致任务——意图打标、发票字段抽取、工单分派——往往可以在CPU或单张消费级GPU上运行，这使它们在没有加速器的边缘与本地部署场景中很有吸引力。7B至9B区间是当前的骨干：它足以承接指令遵循与轻度多步推理，能够处理数页上下文的摘要任务，也是微调最常产生"在窄任务上比肩前沿模型"效果的区间。13B至14B区间留给真正需要推理或长上下文综合的任务——跨长文档比对合同条款、或在财务叙述中核对相互矛盾的口径——到这一档，相比前沿API的成本优势已经收窄到值得重新做一次商业论证的程度。</p>
<p>有两种技术可以拓宽给定规模的可用范围。量化——以8位或4位精度而非16位运行权重——通常能把显存与算力需求压缩2至4倍，代价是可度量的小幅精度损失，而这损失通常可以通过在目标任务上微调补回来。蒸馏——由更大的教师模型为更小的学生模型生成训练信号——是许多生产环境中的小模型能达到其参数量本不该达到的准确度的原因。两种技术都不能免除度量的义务：量化与蒸馏在不同任务上表现不同，唯一站得住脚的答案，是在你真正打算部署的那个量化等级上，用你自己的黄金数据集跑一次准确率测试。</p>
<p>在微调方式上，企业更实用的默认选择是参数高效微调——LoRA及同类适配器方案——而非全量微调。适配器在冻结基座模型的前提下训练少量新增权重，把训练算力降低约一个数量级，同时保持基座模型可复用于其他任务，并产出的可按需切换的适配器。当目标任务与基座模型的预训练分布相距甚远，或每一点准确率都值得付出训练成本时，全量微调仍然更优；但对于多数企业级分类与抽取工作，适配器以极小的成本与运维风险换来了大部分收益。</p>
<h2 id="可靠的小模型评估流程长什么样">可靠的小模型评估流程长什么样？</h2>
<p>评估是小模型项目成功或悄然失败的地方，而这种失败很少是戏剧性的。一个团队微调了7B模型，在几个手工检查的样本上看到准确率提升，于是上线。数月之后，模型面对的输入分布已经明显不同，却没有人能说清准确率是否下滑——因为既没有记录基线，也没有固定的测试集可以重跑。补救办法既不炫目也不昂贵：为每个任务准备一个几百到几千条标注样本的黄金数据集，与训练集严格隔离，并按最重要的场景分层覆盖——尤其是边界情况与稀有类别，那正是小模型最先退化的地方。</p>
<p>有了黄金集之后，三项实践承载了大部分价值。第一，按标签度量，而不只看整体准确率：一个整体94%的模型，可能在业务后果最重的那6%的样本上表现糟糕，而聚合指标会把这一点藏起来。第二，把评估自动化，让每次重训与每次量化变更在晋升前都对同一测试集打分，把模型更新变成一条带门禁的流水线，而不是一次主观判断。第三，对生产流量抽样做定期人工复核，因为黄金集会老化——客户提问的措辞、供应商发票的格式、工单的分类体系都会漂移，而没有新标注，漂移就是不可见的。</p>
<p>发布纪律来自同一套度量设施。影子部署——让小模型与现有的前沿模型或人工流程并行运行、比对输出但不据此行动——能在任何用户被影响之前，用真实流量得到安全的结论。灰度发布配合与准确率或升级率挂钩的自动回滚触发器，则把一次错误晋升的损失限定在可控范围内。只有具备这套 scaffolding 的项目，才能诚实地宣称小模型更便宜；否则，静默精度回退的成本只是从账单上挪到了业务身上。</p>
<h2 id="哪些企业负载最适合作为小模型首批场景">哪些企业负载最适合作为小模型的首批场景？</h2>
<p>最合适的首批场景共有四个特征，逐一核对可以避免小模型最常见的失望——选了一个本来就不窄的任务。任务必须定义清晰，输出可以被精确规定到标注不产生争议的程度：这个条款算或不算终止条款；这张工单属于账单、技术还是开通。任务必须是高频的，因为摊销就是全部的经济论据。任务必须稳定，即标签集与输入分布不会每季度变化。任务的错误成本必须可承受，或者存在廉价的复核环节，使残余错误率可以被管理而非成为生存问题。</p>
<p>按这几条标准筛下来，可靠的先行者在不同行业间惊人地一致。单据与表单抽取——发票、合同、理赔、采购订单——几乎总是企业内体量最大、最稳定的语言类工作，也是小模型最常同时取代前沿API与脆弱规则引擎的地方。入站文本的分类与分派——从客服工单到费用明细——是第二类，而且它往往在领域微调后提升显著，因为企业内部分类体系天生就是特殊的。结构化摘要——把一段案件历史或通话录音压缩进固定模板——是第三类，它受益于输出格式受限这一条件，而这恰恰是小模型表现最好的场景。</p>
<p>暂时应留在前沿模型上的任务同样一致：开放式起草、相关事实边界不明的跨文档推理、任何依赖时效世界知识的任务，以及成本相对质量要求可以忽略不计的低频分析工作。要把两份清单都管住，一个有用的做法是每季度做一次组合评审，随体量与稳定性的变化重新分桶——因为一个起初属于探索性的任务，往往在一年内变成高频且稳定的任务，而那正是其成本结构值得重新审视的时刻。</p>
"""

if __name__ == "__main__":
    en_path = path_of(SLUG, "en")
    h = open(en_path, encoding="utf-8").read()
    assert h.count(EN_FIX_1_OLD) == 1, h.count(EN_FIX_1_OLD)
    h = h.replace(EN_FIX_1_OLD, EN_FIX_1_NEW)
    anchor = '            <section class="faq-section"'
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + EN_NEWS + "\n" + anchor)
    open(en_path, "w", encoding="utf-8").write(h)
    print("EN done")

    spec = {"slug": SLUG, "ops": [
        {"file": "cn", "anchor": '            <section class="faq-section"',
         "pos": "before", "block_cn": "\n" + ZH_NEWS + "\n"},
        {"file": "tw", "anchor": '            <section class="faq-section"',
         "pos": "before", "block_cn": "\n" + ZH_NEWS + "\n"},
    ]}
    run(spec)
