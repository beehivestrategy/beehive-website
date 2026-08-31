#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "data-lineage-tracking-ai-governance"

EN_NEW = """
<h2 id="what-should-data-lineage-actually-capture">What Should Data Lineage Actually Capture?</h2>
<p>"We have lineage" is meaningless without a granularity answer, because table-level lineage and column-level lineage support completely different guarantees. Four levels matter, and most organisations need the top three before AI answers can be defended.</p>
<table>
<thead>
<tr><th>Level</th><th>What it records</th><th>What it lets you answer</th><th>What it cannot answer</th></tr>
</thead>
<tbody>
<tr><td>Table or dataset</td><td>Which datasets feed which downstream assets</td><td>Which reports and models break if this source changes</td><td>Whether a specific figure in a specific answer is affected</td></tr>
<tr><td>Column or field</td><td>Field-to-field transformations across each hop</td><td>Which upstream field produced this metric, and through what logic</td><td>Whether the transformation was approved, or what the value was at a point in time</td></tr>
<tr><td>Run or execution</td><td>Which pipeline run produced which version of which partition, with status</td><td>Whether the data behind an answer was complete and fresh when it was generated</td><td>Who authorised a change to the transformation logic</td></tr>
<tr><td>Business or semantic</td><td>Metric definitions, owners, certified status, access decisions</td><td>Who owns this number, is it certified, and was the access that produced it authorised</td><td>Nothing — this is the layer that makes the others defensible</td></tr>
</tbody>
</table>
<p>The failure pattern is buying column-level lineage and stopping there. Technically impressive, and it still cannot tell a regulator who approved the discount logic or whether the partition was complete when the executive asked. The semantic layer is what converts lineage from a data-engineering artefact into evidence.</p>
<p>One more requirement is easy to overlook: point-in-time reconstruction. When someone challenges a decision made in March, the question is not what the pipeline does today — it is what the data looked like on the day the answer was given. That requires snapshotting both the transformation logic and the underlying state, and it is the requirement most often discovered during an audit rather than during design.</p>
<h2 id="how-do-you-implement-lineage-in-a-modern-data-stack">How Do You Implement Lineage in a Modern Data Stack?</h2>
<p>The sequencing matters more than the tooling. Six steps, in this order:</p>
<ol>
<li><strong>Define the critical path first.</strong> List the data assets that feed high-stakes decisions — board reporting, regulatory filings, AI answers to executives. Twenty assets usually cover most of the risk, and scope discipline here is what keeps the programme funded.</li>
<li><strong>Turn on automated capture where it already exists.</strong> Warehouse query history, orchestration metadata, and BI tool exports already contain most table-level lineage. Harvest it before building anything.</li>
<li><strong>Parse SQL for column-level detail on the critical path only.</strong> Parsing every query in the estate is expensive and mostly noise. Parse the transformations that produce critical assets.</li>
<li><strong>Unify into one metadata layer.</strong> Warehouse catalogue, orchestration, BI, and ML platforms each hold fragments. A single graph fed by all of them is the prerequisite for impact analysis that anyone trusts.</li>
<li><strong>Attach ownership and certification.</strong> Every critical node gets a named owner and a certification state, enforced in the change workflow — not in a spreadsheet that rots.</li>
<li><strong>Close the loop into consumption.</strong> Surface lineage where decisions happen: in the dashboard, in the AI answer, in the approval flow for a breaking change. Lineage nobody sees is lineage nobody uses.</li>
</ol>
<p>The teams that succeed make lineage a byproduct of normal engineering: instrument at the point of change, harvest what the platforms already emit, and add manual documentation only where automation genuinely cannot reach. Hand-maintained lineage diagrams fail within two quarters, without exception.</p>
<h2 id="how-does-lineage-support-ai-answerability-and-audit">How Does Lineage Support AI Answerability and Audit?</h2>
<p>Conversational analytics changes the audience for lineage. When an executive asks a question in Slack and receives an answer in seconds, the lineage requirement moves from the data team's backlog to the moment of decision — and it has to be satisfied in seconds too, not in a two-week investigation.</p>
<p>In practice that means every AI-generated answer carries its provenance: the source tables, the metric definitions, the transformation logic, the freshness of the underlying data, and the authorisation under which the query ran. When the answer can show its work, the conversation moves from "is this number right?" to "what do we do about it?" — which is where the value was always supposed to be.</p>
<p>The audit case is the same mechanism pointed backwards. Regulatory questions are unusually consistent across jurisdictions: which data produced this output, under what approvals, with what controls, and can you demonstrate it rather than assert it. An organisation with column-level lineage, run-level history, and semantic-layer ownership can answer all four from the system. An organisation without them answers from memory, which is how findings get written.</p>
<p>There is a cost argument underneath the compliance one. Gartner's long-standing estimate puts the average financial impact of poor data quality at $12.9 million per year, and a large share of that is time spent investigating numbers nobody can trace. Lineage converts a two-week investigation into a two-minute lookup, and that saving is usually enough to fund the programme on its own.</p>
<h2 id="what-does-lineage-cost-and-how-do-you-justify-it">What Does Lineage Cost and How Do You Justify It?</h2>
<p>The honest answer is that lineage costs less than most data programmes and is justified less often than it should be, because the benefit shows up as avoided work rather than new capability. Three numbers make the case.</p>
<p><strong>Investigation time.</strong> Measure how long it takes today to trace a disputed figure end to end, and how many people are involved. Multiply by the number of disputes per quarter. Most enterprises find this is the single largest hidden cost in their analytics operation.</p>
<p><strong>Change risk.</strong> Count production incidents in the last year caused by an upstream change whose downstream impact was unknown. Each one has a cost, and lineage-backed impact analysis is the direct control.</p>
<p><strong>Deployment friction.</strong> Every AI use case that stalls in review because nobody can attest to the data is a delayed benefit. Organisations with lineage on the critical path move through governance review faster; the ones without it either accept undocumented risk or stop.</p>
<p>Present those three, then commit to a coverage target measured quarterly: percentage of critical assets with automated, current lineage, with a named date by which every asset feeding an executive-facing AI answer is covered. A coverage number that moves is the difference between a funded programme and a one-off project.</p>
"""

FAQ = {
 "EN": [
  ("What is the difference between data lineage and a data catalogue?",
   "A catalogue describes what data exists, who owns it, and what it means. Lineage describes how data moves: which upstream assets produced a given field, through which transformations, and what depends on it downstream. Most modern platforms combine both, but the distinction matters when scoping - a catalogue without lineage cannot answer impact analysis or provenance questions."),
  ("Is column-level lineage always necessary?",
   "Not for every asset. Column-level lineage is expensive to maintain and mostly noise on low-stakes data. Apply it to the critical path: the assets feeding board reporting, regulatory filings, and AI answers to decision-makers. Table-level lineage with good ownership metadata is sufficient for the long tail."),
  ("Can lineage be retrofitted onto an existing warehouse?",
   "Yes, and harvesting what the platform already records is the cheapest starting point - warehouse query history and orchestration metadata usually contain most table-level lineage. Retrofitting is harder for historical point-in-time reconstruction, which is why snapshotting should begin now even if the rest of the programme is phased."),
  ("How does lineage relate to AI governance specifically?",
   "AI consumes data at a speed that makes manual attestation impossible, so governance has to be automated to exist at all. Lineage is the mechanism: it lets every AI answer carry its provenance, lets reviewers see what a change would affect before approving it, and lets auditors reconstruct how a specific output was produced months later."),
 ],
 "zh-CN": [
  ("数据血缘与数据目录有什么区别？",
   "数据目录描述有哪些数据、归谁所有、含义是什么；数据血缘描述数据如何流动：某个字段由哪些上游资产产生、经过了哪些转换、下游又有哪些依赖。现代平台通常把二者合在一起，但在界定范围时必须区分——没有血缘的目录无法回答影响分析和来源追溯的问题。"),
  ("是否所有资产都需要字段级血缘？",
   "并非如此。字段级血缘的维护成本高，而低价值数据上的血缘大多是噪音。应把它用在关键路径上：支撑董事会报告、监管报送以及面向决策者的AI回答的资产。对于长尾数据，表级血缘加上完整的责任人元数据已经足够。"),
  ("可以在已有数仓上补建血缘吗？",
   "可以，而采集平台已经记录下来的信息是最便宜的起点——数仓的查询历史与编排元数据通常已经包含了大部分表级血缘。历史时点重建则难以补做，这也是为什么即使项目分阶段推进，快照机制也应该从现在就开始。"),
  ("血缘与AI治理的关系是什么？",
   "AI消费数据的速度使人工证明变得不可能，因此治理必须自动化才谈得上存在。血缘正是这一机制：它让每个AI回答都携带来源信息，让评审人员在批准变更前看到影响范围，也让审计方能在数月之后重建某个输出是如何产生的。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<section class="faq-section"'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n\n            " + anchor, 1)
    ren = {
        "The Data Governance Imperative for AI": "Why Is Data Governance Non-Negotiable for AI?",
        "Framework Design and Implementation": "How Should a Lineage Framework Be Designed and Implemented?",
        "Operational Challenges and Solutions": "What Operational Challenges Break Lineage Programs?",
        "Measurement and Continuous Improvement": "How Do You Measure Lineage Coverage and Improve It?",
        "Building a Sustainable Governance Model": "What Does a Sustainable Lineage Governance Model Look Like?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    ren_cn = {
        "AI时代的数据治理迫切性": "为什么AI时代的数据治理不可或缺？",
        "框架设计与实施": "血缘框架应该如何设计与落地？",
        "运营挑战与解决方案": "哪些运营挑战会拖垮血缘项目？",
        "衡量与持续改进": "如何衡量血缘覆盖率并持续改进？",
        "构建可持续的治理模式": "可持续的血缘治理模式是什么样的？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
