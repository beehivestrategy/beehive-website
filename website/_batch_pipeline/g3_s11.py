#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "china-pipl-enforcement-update-summer-2025"

EN_NEW = """
<h2 id="what-has-enforcement-actually-cost-companies">What Has Enforcement Actually Cost Companies?</h2>
<p>Enforcement patterns matter more than statutory maxima, because the maximum is rarely what a company pays. Reading the public record since 2021, four observations shape how compliance teams should plan.</p>
<p>First, penalties are increasingly calculated against a defined base rather than imposed as flat sums, and the base is usually revenue or the value of the data processing in question. That changes the risk model: the same violation costs a large enterprise materially more than a small one, which is the opposite of how many compliance programmes are resourced relative to business size.</p>
<p>Second, the named defendant is often the individual as well as the entity. PIPL provisions allow penalties against responsible individuals, and enforcement practice has used them. This is the detail that moves compliance from a legal-team concern to a management one, because the person signing off on a processing activity has personal exposure.</p>
<p>Third, the trigger is frequently documentation rather than harm. Companies are penalised for not having filed a required assessment, for not having a complete processing inventory, or for not being able to produce consent records — even where no data breach occurred. Compliance-by-PDF fails here: a policy document that was never operationalised produces no evidence.</p>
<p>Fourth, remediation orders accompany fines and are usually the larger operational cost. Being told to restructure a data flow, delete unlawfully collected data, or suspend a cross-border transfer while a filing is completed costs far more than the penalty line, and it arrives with a deadline.</p>
<h2 id="how-do-cross-border-transfer-mechanisms-work-in-practice">How Do Cross-Border Transfer Mechanisms Work in Practice?</h2>
<p>Cross-border transfer remains the single highest-frequency enforcement area, and it is where multinationals most often discover that their documentation does not match their architecture. Three mechanisms exist, and choosing among them is a threshold question, not a preference.</p>
<table>
<thead>
<tr><th>Mechanism</th><th>Typical trigger</th><th>What it requires</th><th>Practical timeline</th></tr>
</thead>
<tbody>
<tr><td>CAC security assessment</td><td>High-volume processors, important data, or transfers by critical information infrastructure operators</td><td>A regulator-run assessment of the transfer, the recipient, and the data protection impact</td><td>Several months; plan for it as a project</td></tr>
<tr><td>Standard contract</td><td>Most commercial transfers below the assessment thresholds</td><td>Execution of the CAC-standard contract plus a personal information protection impact assessment, then filing</td><td>Weeks to file, plus assessment work</td></tr>
<tr><td>Certification</td><td>Specific sectors and intra-group arrangements</td><td>Accredited third-party certification of protection practices</td><td>Varies by scheme availability</td></tr>
</tbody>
</table>
<p>Two failure modes recur. The first is threshold error: companies assume the standard contract route applies when their volume or data classification puts them in assessment territory. The thresholds have been adjusted over time, and a programme built against the 2023 thresholds may now be wrong. The second is architectural mismatch: the filing describes a data flow that engineering changed two releases ago. Reconciling the filed documentation with the actual system state is unglamorous work and it is exactly what an inspection tests.</p>
<p>One practical discipline helps more than any other: maintain a register of every outbound flow with its mechanism, filing reference, and last review date, and review it whenever a system changes rather than on an annual cycle. Most findings in this area are register failures, not architecture failures.</p>
<h2 id="what-does-an-evidence-first-compliance-programme-contain">What Does an Evidence-First Compliance Programme Contain?</h2>
<p>Compliance-by-PDF produces documents; compliance-by-evidence produces artefacts that can be produced on request. The difference is operational, and it is what the 2025 enforcement pattern tests. Five artefacts make up the core.</p>
<ul>
<li><strong>A processing inventory that is generated, not written.</strong> Maintained from data discovery and pipeline metadata rather than from a survey, because surveys are stale the day they are completed. If the inventory is a spreadsheet maintained by hand, assume it is wrong.</li>
<li><strong>Consent and lawful basis records tied to specific processing purposes.</strong> Not a general privacy notice, but a record showing which basis applies to which activity and where consent was captured.</li>
<li><strong>Completed impact assessments for the activities that require them.</strong> Cross-border transfers, sensitive personal information, and automated decision-making each carry assessment obligations, and the assessment must pre-date the activity.</li>
<li><strong>Filings and their references.</strong> Standard contract filings, security assessment submissions, certification records — each with a date and an owner.</li>
<li><strong>Response runbooks for rights requests and incidents.</strong> Documented, tested, and timed, because both carry statutory deadlines that begin when the request arrives, not when the team notices it.</li>
</ul>
<p>The test is a timed retrieval exercise. Pick any processing activity and ask the team to produce, within an hour, the inventory entry, the lawful basis, the assessment, and the filing. Programmes that can do this are inspection-ready. Programmes that cannot usually discover the gap during the inspection itself, which is the worst possible time.</p>
<h2 id="how-should-you-handle-data-subject-rights-requests-in-china">How Should You Handle Data Subject Rights Requests in China?</h2>
<p>Rights handling is the area most likely to generate an individual complaint, and complaints are a common enforcement trigger. The operational requirements are straightforward but the deadline discipline is not.</p>
<p>PIPL grants individuals rights of access, correction, deletion, explanation of processing rules, and portability, along with specific rules around consent withdrawal and deceased persons' information. Each carries an obligation to respond, and the clock starts on receipt. In practice the bottleneck is rarely the policy; it is locating the data. A request that names an individual requires the organisation to find every system holding their information, including backups, analytics stores, and logs — which is precisely what the inventory described above is for.</p>
<p>Three practices prevent most failures. Route requests to a single intake point rather than letting them land with whoever received the email. Maintain a mapping from data categories to systems, so a deletion request becomes a defined work order rather than an investigation. And log the response with its timestamp, because demonstrating that a response was timely is a separate obligation from responding at all.</p>
<p>Where a request cannot be fulfilled in full — because a statutory retention requirement applies to part of the data, for example — the correct response explains which parts were actioned and why the remainder was not. Silence and partial action without explanation are what convert a routine request into a complaint.</p>
"""

FAQ = {
 "EN": [
  ("What changed in China's data protection regime in 2025?",
   "Three things: the amended Data Security Law took effect on September 1, 2025 with sharper penalties; cross-border transfer rules settled into the March 2024 framework with active enforcement against filing gaps; and enforcement focus shifted from definitional guidance to operational evidence - inventories, assessments and filings rather than policy documents."),
  ("Which cross-border transfer mechanism applies to our company?",
   "It depends on processor classification, data volume and whether important data is involved. High-volume processors, critical information infrastructure operators, and transfers of important data generally require a CAC security assessment; most other commercial transfers use the CAC standard contract with a supporting impact assessment and filing. Verify current thresholds rather than relying on prior-year determinations."),
  ("How long does a cross-border transfer filing take?",
   "A standard contract filing can be prepared in weeks once the impact assessment is complete, but the assessment itself usually takes longer because it requires an accurate map of the data flow. A CAC security assessment should be planned as a multi-month project. The common mistake is sequencing the filing before the architecture is documented."),
  ("What is the most common cause of enforcement findings?",
   "Documentation gaps rather than data breaches. Companies are penalised for missing filings, incomplete processing inventories, absent impact assessments, and delayed rights responses - frequently with no underlying breach at all. Remediation orders accompanying the fine are usually the larger operational cost, since they arrive with deadlines."),
 ],
 "zh-CN": [
  ("2025年中国的个人信息保护制度发生了哪些变化？",
   "主要有三点：修订后的《数据安全法》于2025年9月1日生效，处罚更为严厉；跨境传输规则在2024年3月的框架下趋于稳定，监管对备案缺口的执法趋于活跃；执法重心也从概念性指引转向运营证据——清查清单、影响评估和备案文件，而不再是政策文档。"),
  ("我们公司适用哪一种跨境传输机制？",
   "这取决于处理者类型、数据量级以及是否涉及重要数据。高量级处理者、关键信息基础设施运营者，以及涉及重要数据的传输，通常需要通过网信办的安全评估；其他多数商业传输使用网信办标准合同，并配套完成个人信息保护影响评估与备案。应核实当前阈值，而不是沿用往年的判断。"),
  ("跨境传输备案需要多长时间？",
   "在影响评估完成的前提下，标准合同备案可在数周内准备好，但评估本身通常耗时更久，因为它需要一张准确的数据流地图。网信办安全评估则应按一个跨月的项目来规划。最常见的错误是在架构尚未完成文档化之前就去排备案的档期。"),
  ("导致执法发现问题最常见的原因是什么？",
   "是文档缺口，而不是数据泄露。企业被处罚的原因多为缺失备案、清查清单不完整、影响评估缺位，以及权利响应超期——而且往往并不存在底层的泄露事件。随罚款一并下达的整改令，由于附带截止期限，其运营成本通常更高。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<section class="faq-section"'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n\n            " + anchor, 1)
    ren = {
        "The Regulatory Landscape in Mid-2025": "What Does the Regulatory Landscape Look Like in Mid-2025?",
        "Key Compliance Requirements": "What Are the Core Compliance Requirements?",
        "Cross-Jurisdictional Challenges": "How Do Multinationals Handle Cross-Jurisdictional Conflict?",
        "Implementation Strategies": "What Implementation Approach Actually Works?",
        "Preparing for the Next Wave of Regulation": "How Should You Prepare for the Next Wave of Regulation?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    ren_cn = {
        "2025年中期的监管格局": "2025年中期的监管格局是什么样的？",
        "关键合规要求": "核心合规要求有哪些？",
        "跨司法管辖区挑战": "跨国企业如何应对跨司法管辖区的冲突？",
        "实施策略": "什么样的实施路径真正有效？",
        "为下一波监管浪潮做准备": "如何为下一波监管浪潮做准备？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
