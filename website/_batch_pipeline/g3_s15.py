#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "data-marketplace-enterprise-data-monetization-strategy"

EN_NEW = """
<h2 id="what-are-the-main-data-monetization-models">What Are the Main Data Monetization Models?</h2>
<p>"Monetization" is used loosely, which is why programmes get funded against the wrong expectations. Four distinct models exist, and they have very different prerequisites, timelines, and risk profiles.</p>
<table>
<thead>
<tr><th>Model</th><th>How value is realised</th><th>Prerequisites</th><th>Typical horizon</th></tr>
</thead>
<tbody>
<tr><td>Internal efficiency</td><td>Reuse of governed data products reduces duplicated work and shortens analytics delivery</td><td>Catalogue, ownership, quality monitoring</td><td>3 to 6 months</td></tr>
<tr><td>Process improvement</td><td>Data products improve decisions that already drive P&amp;L — pricing, inventory, collections</td><td>Semantic layer, integration into decisions</td><td>6 to 12 months</td></tr>
<tr><td>Data-as-a-product (external)</td><td>Packaged data products sold or licensed to partners and customers</td><td>Proven lineage, rights verification, usage metering, audit</td><td>12 to 24 months</td></tr>
<tr><td>Insight services</td><td>Analytics or benchmarking delivered as a service on top of proprietary data</td><td>All of the above plus a delivery capability</td><td>18 to 36 months</td></tr>
</tbody>
</table>
<p>The sequencing matters more than the ambition. Internal efficiency is where nearly every successful programme starts, because it builds the catalogue, ownership and quality discipline that every other model depends on, and it does so without external legal exposure. Organisations that begin with external sales typically discover their lineage and rights documentation is not defensible, and the programme stalls in legal review.</p>
<p>The honest framing for a board is that monetization is a maturity sequence rather than a single initiative. Value compounds as the underlying governance matures, and the governance is the same asset that de-risks AI, analytics and reporting.</p>
<h2 id="how-do-you-price-and-package-a-data-product">How Do You Price and Package a Data Product?</h2>
<p>Pricing data is genuinely difficult because the usual anchors fail: marginal cost is near zero, value is highly context-dependent, and the buyer often cannot evaluate the product before purchase. Three models cover most cases, and the choice should follow how consumers actually use the product.</p>
<ul>
<li><strong>Subscription.</strong> Flat periodic fee for access. Simplest to administer and easiest to forecast, and the right default when usage is steady and predictable. Its weakness is leaving money on the table from heavy users and overcharging light ones.</li>
<li><strong>Usage-based.</strong> Charged by query, record, or API call. Aligns price with value received and scales down for occasional consumers, which accelerates adoption. It requires usage metering you can defend in a dispute, which is a real infrastructure requirement rather than a reporting nicety.</li>
<li><strong>Value-based.</strong> Priced against the outcome the data enables — a share of savings, a per-decision fee. Highest potential return and highest negotiation cost. It works when the outcome is measurable and attributable, which in practice means it is reserved for a small number of high-value products.</li>
</ul>
<p>Packaging matters as much as pricing. A data product should ship with a documented definition, a freshness commitment, a support contact, and a stated scope of permitted use. Buyers — internal or external — are not purchasing a table; they are purchasing a reliable answer to a class of questions. Products described in those terms sell faster and generate fewer disputes.</p>
<p>Start simple. Most programmes begin with a single internal charging model or no charge at all, instrument usage carefully, and introduce pricing once consumption patterns are understood. Pricing designed before usage data exists is guesswork with a spreadsheet attached.</p>
<h2 id="what-governance-is-required-before-external-sharing">What Governance Is Required Before External Sharing?</h2>
<p>External monetization multiplies consequences, because a mistake becomes a contractual and regulatory matter rather than an internal correction. Six capabilities must be demonstrable before the first external product ships, and "demonstrable" means evidence, not intention.</p>
<ol>
<li><strong>Proven lineage.</strong> For every field in the product, the path back to its source system and the transformations applied. Anything less makes it impossible to answer a customer's question about provenance, or a regulator's.</li>
<li><strong>Sensitivity classification.</strong> Automated classification of personal, confidential, and regulated content, applied at the point of publication rather than during periodic review.</li>
<li><strong>Consent and usage-rights verification.</strong> Documented confirmation that the organisation may share this data for this purpose, including any third-party data incorporated along the way.</li>
<li><strong>Access control and entitlement.</strong> Per-customer scoping enforced at query time, so a customer cannot retrieve rows outside their licence.</li>
<li><strong>Audit trails.</strong> Who accessed what, when, under which entitlement, and what was returned — retained for the contract period.</li>
<li><strong>De-identification where required.</strong> Documented technique, tested effectiveness, and a re-identification risk assessment, not a claim that data has been anonymised.</li>
</ol>
<p>Two governance practices prevent the most common external failures. First, require a named owner per data product who signs off on each release — shared ownership here means no ownership. Second, maintain a permitted-use register: for each product, the uses customers have contracted for, with monitoring for deviations. Most disputes in this category are permitted-use disputes, not quality disputes.</p>
<h2 id="how-do-you-launch-a-marketplace-without-a-big-bang">How Do You Launch a Marketplace Without a Big Bang?</h2>
<p>The most common failure is treating the marketplace as a platform project: build the full catalogue, migrate everything, then open the doors. That approach takes two years and delivers nothing for the first eighteen months. Four steps work better.</p>
<p><strong>Start with ten products, not a thousand.</strong> Choose datasets with known demand, clear ownership, and clean lineage. The catalogue's credibility comes from the quality of its first entries, and ten excellent products generate more adoption than a thousand mediocre ones.</p>
<p><strong>Launch to one demanding consumer group.</strong> Pick the team that files the most requests today, and make them successful. Their usage produces the evidence — reduced request volume, faster delivery — that funds the next phase, and their feedback surfaces the gaps in the semantic layer faster than any internal review.</p>
<p><strong>Instrument the exchange from day one.</strong> Track search-to-access conversion, time-to-access, reuse rates, and the questions that return nothing. The last metric is the most valuable: unanswered searches are the specification for the next ten products.</p>
<p><strong>Measure both sides of the ledger.</strong> Value side: direct revenue, cost savings from reuse, acceleration of analytics delivery. Health side: catalogue coverage, reuse rates, time-to-access, and unanswered-search rate. Programmes that report only the value side get cut when the health metrics quietly deteriorate.</p>
<p>Remember the ratio that governs this work: technology is roughly 30 percent of marketplace success, and the organisational side — product ownership, incentives, and capability — is the rest. The data product manager role, part product manager and part data steward, is the single biggest lever, and most enterprises have to create it rather than assign it.</p>
"""

FAQ = {
 "EN": [
  ("What is the difference between a data catalog and a data marketplace?",
   "A catalog describes what data exists; a marketplace makes it consumable - with packaging, pricing where applicable, self-service access, and usage metering. The marketplace operationalises the catalog's inventory into products users can actually acquire and reuse."),
  ("How should enterprises price data products?",
   "Match the model to how consumers actually use the product: subscription where usage is steady, usage-based where it varies and metering is defensible, value-based where the outcome is measurable and attributable. Start with a simple model, instrument usage, and evolve pricing once consumption patterns are clear."),
  ("What governance is required before external monetization?",
   "Proven lineage, automated sensitivity classification, verified consent and usage rights, per-customer access control enforced at query time, complete audit trails, and tested de-identification where required. External monetization should begin only after these are demonstrated on internal products."),
  ("Should every enterprise try to sell its data externally?",
   "No. External sales require governance maturity that many organisations do not yet have, and attempting them first multiplies legal and reputational risk. Most successful programmes start with internal efficiency and process improvement, building the catalogue, ownership and quality discipline that external models later depend on."),
 ],
 "zh-CN": [
  ("数据目录与数据市场有什么区别？",
   "目录描述有哪些数据存在；市场则让数据变得可消费——包含打包、在适用情况下的定价、自助式访问和用量计量。市场把目录中的清单运营化为用户真正能够获取和复用的产品。"),
  ("企业应该如何为数据产品定价？",
   "让定价模式匹配消费方实际的使用方式：用量稳定的采用订阅制；用量波动且计量可辩护的采用按量计费；结果可度量且可归因的采用价值定价。从简单模式起步，认真记录用量，等消费模式清晰之后再演进定价。"),
  ("在对外变现之前需要哪些治理能力？",
   "可证明的血缘、自动化的敏感度分级、经过核验的同意与使用权、在查询时执行的按客户访问控制、完整的审计轨迹，以及在需要时经过有效性测试的脱敏。对外变现只应在这些能力已于内部产品上得到证明之后开始。"),
  ("每家企业都应该尝试对外销售数据吗？",
   "不是。对外销售要求企业具备许多组织尚未达到的治理成熟度，而一开始就做这件事会成倍放大法律与声誉风险。多数成功的项目从内部效率与流程改进起步，先建立目录、责任归属和质量纪律，而这些正是对外模式日后所依赖的基础。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<section class="faq-section"'
    if anchor not in b:
        anchor = '<section[^>]*faq-section'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n\n            " + anchor, 1)
    ren = {
        "The Strategic Context for Enterprise AI": "What Is the Strategic Context for Data Monetization?",
        "Framework for Strategic Decision-Making": "What Framework Should Guide the Decision?",
        "Organizational Change and Capability Building": "How Do You Build the Required Organisational Capability?",
        "Measuring Strategic Impact": "How Do You Measure Strategic Impact?",
        "Frequently Asked Questions": "What Questions Do Executives Ask First?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b, count=1)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    ren_cn = {
        "当前格局与关键趋势": "当前格局与关键趋势是什么？",
        "实施框架与最佳实践": "实施框架与最佳实践有哪些？",
        "衡量影响与展示价值": "如何衡量影响并展示价值？",
        "克服常见挑战": "如何克服常见的挑战？",
        "风险管理与合规框架": "风险管理与合规框架应该如何设计？",
        "价值实现与持续改进": "如何实现价值并持续改进？",
        "中国市场特有的实施优势": "中国市场有哪些特有的实施优势？",
        "规模化推广的关键成功因素": "规模化推广的关键成功因素有哪些？",
        "常见问题": "高管最先会问哪些问题？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b, count=1)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    s = F.load(SLUG, "zh-TW")
    b = F.get_body(s)
    ren_tw = {
        "Framework for Strategic Decision-Making": "決策框架應該如何設計？",
        "Organizational Change and Capability Building": "如何構建所需的組織能力？",
        "Measuring Strategic Impact": "如何衡量戰略影響？",
        "常見問題": "高階主管最先會問哪些問題？",
        "規模化推廣的關鍵成功因素": "規模化推廣的關鍵成功因素有哪些？",
        "技術基礎設施與實施考量": "技術基礎設施與實施上需要考慮什麼？",
        "中國市場特有的實施優勢": "中國市場有哪些特有的實施優勢？",
    }
    for old, new in ren_tw.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + F.S2TWP.convert(new) + r'\g<2>', b, count=1)
    F.save(SLUG, "zh-TW", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
