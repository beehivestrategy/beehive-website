import sys
sys.path.insert(0, "_batch_pipeline")
from _lib01 import *

SLUG = "chinese-manufacturers-ai-quality-control"

EN_ADD = """
<h2 id="how-do-you-build-and-maintain-a-defect-model-that-keeps-working">How Do You Build and Maintain a Defect Model That Keeps Working?</h2>
<p>The model is rarely the hard part of AI quality control; the labelled data and the maintenance regime are. A vision model needs examples of every defect class it is expected to recognise, and in a healthy production line the defect classes are, by definition, rare. That class imbalance is the central engineering problem: a model trained on 99 percent good units will learn to predict "good" and be right 99 percent of the time while catching nothing. The remedies are well understood — targeted collection of defect examples from historical rework records, deliberate over-sampling of failure classes, synthetic defect generation, and metrics that weight recall on the defect class far above overall accuracy.</p>
<p>Collection strategy comes first. Most plants already have the raw material: years of rework tickets, warranty returns, and QA photographs that were never labelled for training. Mining that archive is almost always faster than waiting for new defects to occur on the line, and it is the step that separates a six-week project from a six-month one. Where the archive is thin, plants run deliberate defect campaigns — running the process out of specification under supervision to generate real examples of each failure mode — because synthetic images rarely capture the lighting, occlusion, and material variance of a real production environment.</p>
<p>Maintenance is where programmes quietly decay. Defect appearance drifts as tooling wears, as material lots change, and as camera optics age, and a model that was 98 percent accurate at commissioning can fall below 90 percent within two quarters without anyone noticing, because nobody re-labels what the model already classified. The defence is a standing regime: hold out a sample of every shift's output for human re-inspection, compare human and model verdicts weekly, and retrain on a fixed cadence with a defined trigger — commonly, any defect class whose recall drops below an agreed floor.</p>
<table class="article-table">
<thead><tr><th>Lifecycle stage</th><th>Key activity</th><th>Failure it prevents</th></tr></thead>
<tbody>
<tr><td>Class definition</td><td>Agree a bounded, named defect taxonomy with the quality team</td><td>Ill-defined classes that no model can learn</td></tr>
<tr><td>Data collection</td><td>Mine rework and warranty archives; run supervised defect campaigns</td><td>Waiting months for rare defects to occur naturally</td></tr>
<tr><td>Labelling</td><td>Two-pass labelling with adjudication on disagreement</td><td>Noisy labels that cap achievable accuracy</td></tr>
<tr><td>Validation</td><td>Test on a held-out set from a different shift and material lot</td><td>Overfitting to one lighting or batch condition</td></tr>
<tr><td>Monitoring</td><td>Weekly human re-inspection of a sampled output</td><td>Silent accuracy decay after commissioning</td></tr>
<tr><td>Retraining</td><td>Fixed cadence plus recall-drop trigger per defect class</td><td>Model drift turning into escaped defects</td></tr>
</tbody>
</table>
<h2 id="what-does-it-take-to-scale-from-one-line-to-twenty">What Does It Take to Scale From One Line to Twenty?</h2>
<p>Most AI quality programmes succeed on the pilot line and stall at the fourth. The pilot benefits from the best engineer, the cleanest data, and a quality manager who is personally invested; line four has none of those advantages and a slightly different camera angle. Scaling is therefore an exercise in removing per-line craft, and it is won or lost on four decisions.</p>
<p>The first decision is standardising the physical setup. Fixed mounting, fixed lighting, fixed focal distance, and a documented calibration procedure turn each new line from a modelling problem into an installation. Plants that skip this discover that every line requires its own model, and the programme cost scales linearly instead of flattening. The second decision is centralising model management: one registry, one version per model, one deployment pipeline, and an audit record of which model is running on which line. Without it, nobody can answer the question that follows the first escaped defect: which model version inspected that unit?</p>
<p>The third decision is federating the data while keeping inference local. Inspection images are large and often subject to customer confidentiality agreements, so the pattern that works is edge inference with only classifications, metadata, and sampled thumbnails moving to a central store. That keeps bandwidth and privacy costs flat while still enabling the cross-plant analytics that make the data strategic. The fourth decision is governance of the human workflow: when the model flags a unit, somebody must own the disposition, and that ownership has to be defined per plant before go-live rather than discovered afterwards.</p>
<table class="article-table">
<thead><tr><th>Scaling challenge</th><th>Symptom at line 4-20</th><th>Standardised response</th></tr></thead>
<tbody>
<tr><td>Hardware variance</td><td>Every line needs its own model</td><td>Fixed mounting, lighting, and calibration procedure</td></tr>
<tr><td>Model sprawl</td><td>Unknown version running on a specific line</td><td>Central model registry with deployment audit</td></tr>
<tr><td>Data gravity</td><td>Bandwidth and confidentiality blockers</td><td>Edge inference; only metadata and thumbnails centrally</td></tr>
<tr><td>Workflow ownership</td><td>Flagged units pile up unreviewed</td><td>Named disposition owner per plant before go-live</td></tr>
<tr><td>Skills scarcity</td><td>Rollout gated on a handful of engineers</td><td>Managed service for platform and model operations</td></tr>
</tbody>
</table>
<p>Plants that get these four right typically find that the marginal cost of the tenth line is a fraction of the first, which is the point at which AI quality control stops being a project and becomes standard production equipment — the position Chinese manufacturers have already reached in electronics and automotive components, and the position available to any manufacturer willing to standardise before scaling.</p>
"""

H2FIX = {
    "EN": [
        ("the-scale-of-chinese-manufacturing-ai-deployment", "How Large Is the Scale of Chinese Manufacturing AI Deployment?"),
        ("edge-computing-makes-it-economically-viable", "Why Does Edge Computing Make AI Inspection Economically Viable?"),
        ("data-infrastructure-and-analytics", "What Data Infrastructure and Analytics Does It Require?"),
        ("implementation-lessons-and-best-practices", "What Are the Implementation Lessons and Best Practices?"),
    ],
    "CN": [
        ("ai质量检测的技术架构", "AI 质量检测的技术架构是什么？"),
        ("实施模式与价值", "实施模式与价值是什么？"),
        ("中国市场特有的实施优势", "中国市场特有的实施优势有哪些？"),
        ("规模化推广的关键成功因素", "规模化推广的关键成功因素有哪些？"),
        ("从试点到规模化生产的路径", "从试点到规模化生产的路径如何规划？"),
        ("技术基础设施与实施考量", "技术基础设施与实施考量是什么？"),
        ("组织准备与能力建设", "组织准备与能力建设如何推进？"),
        ("roi衡量与商业论证", "ROI 衡量与商业论证如何构建？"),
    ],
    "TW": [
        ("edge-computing-makes-it-economically-viable", "Why Does Edge Computing Make AI Inspection Economically Viable?"),
        ("data-infrastructure-and-analytics", "What Data Infrastructure and Analytics Does It Require?"),
        ("implementation-lessons-and-best-practices", "What Are the Implementation Lessons and Best Practices?"),
        ("規模化推廣的關鍵成功因素", "規模化推廣的關鍵成功因素有哪些？"),
        ("技術基礎設施與實施考量", "技術基礎設施與實施考量是什麼？"),
        ("中國市場特有的實施優勢", "中國市場特有的實施優勢有哪些？"),
        ("規模化推廣的關鍵成功因素-2", "規模化推廣的關鍵成功因素有哪些？"),
    ],
}

process(SLUG, H2FIX, adds={"EN": EN_ADD}, tag=SLUG[:24])
