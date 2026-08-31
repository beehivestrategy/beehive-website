#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "data-contract-enforcement-in-production-pipelines"

EN_NEW = """
<h2 id="what-should-a-data-contract-actually-contain">What Should a Data Contract Actually Contain?</h2>
<p>A contract that only specifies column names and types catches the failure that hurts least. Renames and type changes are the failures engineers already fear; the expensive ones are semantic — a field that keeps its name and changes its meaning. A useful contract has five sections.</p>
<table>
<thead>
<tr><th>Section</th><th>What it specifies</th><th>Failure it prevents</th></tr>
</thead>
<tbody>
<tr><td>Schema</td><td>Field names, types, nullability, and uniqueness constraints</td><td>Breaking renames and type changes reaching consumers unannounced</td></tr>
<tr><td>Semantics</td><td>Plain-language definition, units, and the business meaning of each field</td><td>Silent meaning drift: "revenue" excluding refunds this quarter and including them next</td></tr>
<tr><td>Service levels</td><td>Freshness target, expected row volume range, and delivery schedule</td><td>Consumers acting on a partition that arrived late or incomplete</td></tr>
<tr><td>Quality rules</td><td>Assertions consumers depend on: non-null rates, accepted value ranges, referential integrity</td><td>Duplicate or malformed records entering downstream models and dashboards</td></tr>
<tr><td>Ownership and change</td><td>Named producer and consumer owners, versioning rules, deprecation policy, escalation path</td><td>Changes with nobody accountable and consumers with no route to object</td></tr>
</tbody>
</table>
<p>The ownership section is the one that determines whether the contract survives. A schema without a named producer owner is a description, not an agreement, because there is no one who can be asked to fix it. Write the owner into the contract file itself rather than into a separate registry that nobody updates.</p>
<p>Keep contracts small enough to be read. Contracts that try to describe an entire warehouse become unmaintainable and get bypassed; contracts covering the ten to twenty datasets that actually drive decisions get enforced and stay current.</p>
<h2 id="where-should-contract-checks-run-in-the-pipeline">Where Should Contract Checks Run in the Pipeline?</h2>
<p>Enforcement location determines whether a contract prevents incidents or merely documents them. Four checkpoints, each catching a different class of failure.</p>
<ol>
<li><strong>Producer CI — schema and contract validation on pull request.</strong> The producer's change is validated against the contract before merge, so breaking changes fail the build rather than the dashboard. This is the highest-value checkpoint and the cheapest place to fail.</li>
<li><strong>Producer deploy — compatibility check against registered consumer expectations.</strong> Before a new version ships, the registry is queried for downstream consumers and the change is classified as compatible, breaking, or ambiguous. Only compatible changes deploy automatically.</li>
<li><strong>Ingestion boundary — runtime validation of incoming data.</strong> Schema, volume, and quality assertions run as data arrives, with quarantining of records that fail. This catches the drift that no code change caused: an upstream system altering its export format.</li>
<li><strong>Consumer CI — contract change notification.</strong> When a contract version changes, downstream consumers are notified with the diff and their own tests run against the new version in a staging environment.</li>
</ol>
<p>Two design rules follow from this layout. Validation must fail loudly at the producer's build and quietly at runtime — a loud runtime failure stops production for a problem the consumer may not care about, while a silent one hides the issue entirely. The usual resolution is to fail the producer build, quarantine at ingestion, and alert rather than halt downstream.</p>
<p>And every check must be versioned with the contract. A check that lives in a separate configuration file drifts out of sync with the contract it supposedly enforces, which is how organisations end up with contracts that pass and pipelines that break.</p>
<h2 id="how-do-you-roll-out-contracts-across-many-teams">How Do You Roll Out Contracts Across Many Teams?</h2>
<p>The rollout failure mode is a mandate: contracts required everywhere, tooling provided, adoption near zero. Three phases work better.</p>
<p><strong>Phase one — prove the loop on one dataset.</strong> Choose a dataset with an active, engaged consumer and a history of incidents: a revenue table or a customer master. Write the contract with the consumer rather than for them, wire the checks, and wait for the first catch. The incident a contract prevents is worth more than any amount of internal advocacy, so pick a dataset likely to produce one.</p>
<p><strong>Phase two — make the path easy before making it mandatory.</strong> Build a template, one command to scaffold a contract, and a shared library of common quality rules. Adoption at this stage should be voluntary and visibly faster than the alternative. Teams should choose contracts because writing one is less work than the incident review that follows not having one.</p>
<p><strong>Phase three — enforce at the boundary, not at the team.</strong> Rather than requiring every team to adopt, require every dataset crossing a domain boundary to carry a contract. This focuses enforcement where the organisational handoffs actually are, and it lets internal datasets within a team's own ownership stay informal until they matter.</p>
<p>Throughout, resist the temptation to mandate coverage percentages. Coverage without quality is worse than low coverage, because it produces a registry of contracts nobody trusts. Track the number of incidents caught by contracts instead — it is the metric that sustains the programme.</p>
<h2 id="how-do-you-measure-whether-contract-enforcement-is-working">How Do You Measure Whether Contract Enforcement Is Working?</h2>
<p>Four measures tell you whether contract enforcement is real or decorative, and only one of them is about coverage.</p>
<ul>
<li><strong>Incidents caught pre-production.</strong> The count of breaking changes rejected at the producer's CI before reaching consumers. This is the number that justifies the programme, and it should rise then plateau.</li>
<li><strong>Time to detect a contract violation.</strong> From the moment bad data arrives to the moment someone is alerted. Contracts collapse this from days to minutes, and the delta is the most persuasive metric for sceptical engineers.</li>
<li><strong>Mean time to resolution.</strong> A contract that fires without a named owner produces an alert nobody acts on. Track how long violations stay open; if it is growing, the ownership section is not being filled in.</li>
<li><strong>Coverage of high-value datasets.</strong> Percentage of datasets feeding board reporting, regulatory filings, or AI answers that carry an enforced, current contract. Coverage on the long tail is not worth pursuing.</li>
</ul>
<p>Report these quarterly alongside the incident count they prevented. IDC has put the average annual cost of poor data quality at $12.9 million per organisation, and programmes that cannot connect their own numbers to that figure tend to be cut in the next planning cycle — not because the work was ineffective, but because it was invisible.</p>
"""

CN_NEW = """
<h2 id="what-should-a-data-contract-actually-contain">一份数据契约到底应该包含什么？</h2>
<p>只规定字段名和类型的契约，抓住的是伤害最小的那一类失败。改名和类型变更是工程师本来就担心的问题；真正昂贵的失败是语义性的——一个字段名字没变，含义却变了。一份有用的契约包含五个部分。</p>
<table>
<thead>
<tr><th>部分</th><th>规定什么</th><th>防止哪类失败</th></tr>
</thead>
<tbody>
<tr><td>模式</td><td>字段名、类型、可空性与唯一性约束</td><td>破坏性改名和类型变更在未经通知的情况下触达消费方</td></tr>
<tr><td>语义</td><td>每个字段的通俗定义、单位与业务含义</td><td>静默的语义漂移：这一季度"收入"不含退款，下一季度却包含</td></tr>
<tr><td>服务水平</td><td>时效性目标、预期数据量区间与交付节奏</td><td>消费方基于迟到或不完整的分区做出判断</td></tr>
<tr><td>质量规则</td><td>消费方所依赖的断言：非空率、可接受取值区间、引用完整性</td><td>重复或畸形记录进入下游模型与仪表盘</td></tr>
<tr><td>责任与变更</td><td>具名的生产方与消费方责任人、版本规则、下线策略、升级路径</td><td>变更无人负责，消费方也没有提出异议的通道</td></tr>
</table>
<p>决定契约能否存活的是责任部分。一份没有具名生产方责任人的模式描述只是一份说明，而不是一份协议，因为没有人可以被要求去修它。把责任人写进契约文件本身，而不是写进一个没人更新的独立注册表。</p>
<p>契约要保持短到能被读完。试图描述整个数据仓库的契约会变得无法维护并最终被绕过；覆盖真正驱动决策的那十到二十个数据集的契约，才会被执行并保持最新。</p>
<h2 id="where-should-contract-checks-run-in-the-pipeline">契约检查应该跑在流水线的哪些位置？</h2>
<p>执行位置决定了契约是阻止了事故，还是仅仅记录了事故。四个检查点，各自捕捉不同类别的失败。</p>
<ol>
<li><strong>生产方CI——在拉取请求上校验模式与契约。</strong>生产方的变更在合并之前就对照契约被校验，因此破坏性变更会让构建失败，而不是让仪表盘失败。这是价值最高的检查点，也是失败成本最低的位置。</li>
<li><strong>生产方部署——对照已注册的消费方期望做兼容性检查。</strong>新版本发布前，向注册表查询下游消费方，并把变更归类为兼容、破坏或存疑。只有兼容的变更才能自动部署。</li>
<li><strong>接入边界——对进入的数据做运行时校验。</strong>模式、数据量与质量断言在数据到达时执行，并对未通过的记录做隔离。这捕捉的是任何代码变更都没有引发的漂移：上游系统改了自己的导出格式。</li>
<li><strong>消费方CI——契约变更通知。</strong>当契约版本变化时，下游消费方会收到带差异说明的通知，其自身的测试也会在预发布环境中针对新版本运行。</li>
</ol>
<p>由这个布局可推出两条设计规则。校验必须在生产方的构建阶段大声失败，而在运行时安静失败——运行时的大声失败会为消费方可能并不关心的问题停掉生产，而完全静默则会把问题彻底掩盖。通常的处理方式是：让生产方的构建失败，在接入环节隔离，对下游则告警而不中断。</p>
<p>并且，每一项检查都必须与契约一起版本化。存放在独立配置文件里的检查，会与它本应执行的契约逐渐失去同步，这正是"契约全部通过、流水线却依然崩掉"的成因。</p>
<h2 id="how-do-you-roll-out-contracts-across-many-teams">如何在多个团队之间推广契约？</h2>
<p>推广中最常见的失败方式是强制推行：要求处处都有契约，工具也提供了，采用率却接近于零。分三个阶段推进效果更好。</p>
<p><strong>第一阶段——在一个数据集上跑通闭环。</strong>选一个有积极参与的消费方、且有事故历史的数据集：收入表或客户主数据。与消费方一起写契约，而不是替他们写；接好检查；然后等第一次拦截发生。契约所阻止的那起事故，比任何内部宣讲都更有价值，所以要挑一个很可能出事的数据集。</p>
<p><strong>第二阶段——在强制之前先让路径变得容易。</strong>提供一个模板、一条命令即可脚手架出契约，以及一套常用质量规则的共享库。这一阶段的采用应当是自愿的，而且要明显比替代方案更快。团队选择契约，应该是因为写一份比事后做事故复盘更省事。</p>
<p><strong>第三阶段——在边界上执行，而不是在团队上执行。</strong>与其要求每个团队都采用，不如要求每一个跨域边界的数据集都必须带契约。这会把执行力度集中在真正存在组织交接的地方，也让团队自有的内部数据集在变得重要之前保持非正式状态。</p>
<p>整个过程要克制住规定覆盖率的冲动。没有质量的覆盖率比低覆盖率更糟，因为它产出的注册表里全是没有人信任的契约。改为跟踪"契约拦截了多少起事故"——这才是能支撑项目走下去的指标。</p>
<h2 id="how-do-you-measure-whether-contract-enforcement-is-working">如何判断契约执行是否真的有效？</h2>
<p>有四项指标能告诉你契约执行是真实的还是装饰性的，而其中只有一项与覆盖率有关。</p>
<ul>
<li><strong>在生产前被拦截的事故数。</strong>在生产方CI阶段被拒绝、从而没有触达消费方的破坏性变更数量。这是证明项目价值的数字，它应当先上升，然后趋于平稳。</li>
<li><strong>发现契约违规的耗时。</strong>从坏数据到达到有人收到告警之间的时间。契约会把这个时间从数天压缩到数分钟，而这个变化量对持怀疑态度的工程师最有说服力。</li>
<li><strong>平均修复时间。</strong>一份触发了却没有具名责任人的契约，只会产出一条没有人处理的告警。跟踪违规保持未解决状态的时间；如果它在变长，说明责任部分没有被认真填写。</li>
<li><strong>高价值数据集的覆盖率。</strong>支撑董事会报告、监管报送或AI回答的数据集里，带有被执行且保持最新契约的比例。长尾数据集的覆盖率不值得追求。</li>
</ul>
<p>每季度把这些指标与它们所避免的事故数量一起汇报。IDC估计数据质量低劣给单个组织造成的年平均成本为1290万美元；而无法把自己这些数字与这一数字建立联系的项目，往往会在下一个规划周期被砍掉——原因不是工作没有成效，而是成效不可见。</p>
"""

FAQ = {
 "EN": [
  ("What is a data contract?",
   "A data contract is a versioned agreement between a data producer and its consumers, specifying schema, semantic definitions, freshness and volume service levels, quality rules, and named owners. Enforced in CI/CD and at the ingestion boundary, it converts implicit assumptions into verifiable commitments."),
  ("How is a data contract different from a schema registry?",
   "A schema registry stores the structure of data; a contract adds the commitments around it - semantics, freshness targets, quality assertions, ownership, and a change process. Structure alone will not catch the expensive failure: a field that keeps its name and changes its meaning."),
  ("Who should approve a breaking schema change?",
   "The change is proposed as a versioned contract update, validated against registered consumer expectations, and approved jointly by the producer owner and the affected consumer owners. In organisations without contracts the answer is nobody - the change ships and consumers discover the breakage in production."),
  ("Will contract enforcement slow down delivery?",
   "Initially slightly, then not at all. Teams adopting contracts voluntarily usually find that writing one is less work than the incident review that follows not having one. The key is making the producer's CI the place where changes fail, rather than letting consumers discover breakage in production."),
 ],
 "zh-CN": [
  ("什么是数据契约？",
   "数据契约是数据生产方与消费方之间的一份带版本管理的协议，规定模式、语义定义、时效性与数据量服务水平、质量规则，以及具名责任人。在CI/CD与接入边界执行后，它把隐性假设转化为可验证的承诺。"),
  ("数据契约与模式注册表有什么不同？",
   "模式注册表存放数据的结构；契约则在其之上补充了承诺——语义、时效性目标、质量断言、责任归属和变更流程。仅有结构无法捕捉最昂贵的那类失败：一个字段名字没变，含义却变了。"),
  ("破坏性的模式变更应该由谁批准？",
   "变更应以带版本的契约更新形式提出，对照已注册的消费方期望做校验，并由生产方责任人与受影响的消费方责任人共同批准。在没有契约的组织里，答案是“没有人”——变更直接上线，消费方在生产环境中才发现故障。"),
  ("执行契约会拖慢交付吗？",
   "初期会略微变慢，之后完全不会。自愿采用契约的团队通常会发现，写一份契约比事后做事故复盘更省事。关键在于让变更失败在生产方的CI阶段，而不是让消费方在生产环境中才发现故障。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<h2 id="key-takeaways">Key Takeaways</h2>'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n" + anchor, 1)
    ren = {
        "The Current Landscape": "Why Do Production Pipelines Break?",
        "Key Implementation Challenges": "What Makes Data Contract Adoption Hard?",
        "Practical Approaches That Work": "What Implementation Approach Actually Works?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    anchor = '<h2 id="关键要点">关键要点</h2>'
    assert anchor in b
    b = b.replace(anchor, CN_NEW.strip() + "\n" + anchor, 1)
    ren_cn = {
        "理解当前格局": "为什么生产流水线会出问题？",
        "关键原则与战略框架": "落地数据契约难在哪里？",
        "实施方法与最佳实践": "什么样的实施路径真正有效？",
        "衡量成功与展示投资回报率": "如何衡量契约执行的成效？",
        "常见陷阱及规避方法": "常见的陷阱有哪些，如何规避？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    for old, new in [('id="理解当前格局"', 'id="why-do-production-pipelines-break"'),
                     ('id="关键原则与战略框架"', 'id="what-makes-contract-adoption-hard"'),
                     ('id="实施方法与最佳实践"', 'id="what-implementation-approach-works"'),
                     ('id="衡量成功与展示投资回报率"', 'id="how-do-you-measure-contract-enforcement"'),
                     ('id="常见陷阱及规避方法"', 'id="common-pitfalls-and-how-to-avoid-them"'),
                     ('id="关键要点"', 'id="key-takeaways"'),
                     ('id="结论"', 'id="conclusion"')]:
        b = b.replace(old, new)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
