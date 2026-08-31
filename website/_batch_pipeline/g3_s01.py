#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "ai-threat-detection-enterprise-20260118"

EN_NEW = """
<h2 id="what-does-a-modern-ai-threat-detection-architecture-look-like">What Does a Modern AI Threat Detection Architecture Look Like?</h2>
<p>Enterprises rarely fail at AI threat detection because they picked the wrong model. They fail because the architecture around the model is thin. A modern detection stack has five layers, and each one is a place where programs quietly break.</p>
<table>
<thead>
<tr><th>Layer</th><th>What it does</th><th>Failure mode when weak</th></tr>
</thead>
<tbody>
<tr><td>Telemetry ingestion</td><td>Normalises identity, endpoint, network, cloud and email logs into a common schema</td><td>Models see only a fraction of the attack surface and miss lateral movement</td></tr>
<tr><td>Entity resolution</td><td>Resolves users, devices, service accounts and workloads into stable identities</td><td>One person looks like five different actors and every baseline fragments</td></tr>
<tr><td>Baselining and scoring</td><td>Builds behavioural profiles and assigns risk scores to deviations</td><td>Either constant false positives or silent, expensive misses</td></tr>
<tr><td>Correlation</td><td>Chains weak signals from multiple sources into one incident narrative</td><td>Analysts receive hundreds of unrelated alerts instead of ten real incidents</td></tr>
<tr><td>Response and feedback</td><td>Proposes containment, records analyst decisions, and retrains the models</td><td>The system never improves and analysts quietly stop trusting it</td></tr>
</tbody>
</table>
<p>Two design choices matter more than the rest. First, resolve identities before you model behaviour: an employee who signs in from a laptop, a phone and a VDI session should produce one baseline, not three. Second, keep the correlation layer explainable. A risk score that cannot name its inputs — new country, unrecognised device, access to the payroll table at 03:00 — will not survive contact with a sceptical analyst, a works council, or a regulator asking why an account was suspended.</p>
<p>Practically, this architecture does not require a new platform. Ingestion usually already exists in the SIEM or the log lake. The entity resolution and baselining layers are where new work concentrates, and they are the layers that decide whether the program produces ten incidents a day or ten thousand alerts.</p>
<h2 id="how-do-you-detect-insider-risk-and-credential-abuse">How Do You Detect Insider Risk and Credential Abuse?</h2>
<p>Credential abuse is the hardest detection problem precisely because nothing looks anomalous at the moment of login. The attacker has the correct username and the correct password, frequently from the same country and the same device class as the legitimate user. Verizon's 2024 Data Breach Investigations Report attributes 68 percent of breaches to a non-malicious human element, which means the patterns that follow a valid login — not the login itself — are where AI detection earns its keep.</p>
<p>The signals that separate a compromised account from a legitimate one are behavioural rather than static. A service account that normally reads a handful of tables suddenly enumerates hundreds. A finance user who downloads 40 MB a quarter exports 4 GB in an afternoon. An engineer who has never touched the customer schema runs an unfiltered query against it at 02:00 on a Sunday. Each signal alone is unremarkable, and a rule-based system will discard all three. Chained together and compared against a per-entity baseline, they describe an exfiltration in progress.</p>
<p>Insider risk needs a stricter governance posture than external threat detection, and enterprises that skip this step end up in trouble with employee representatives and regulators alike. Three rules hold up in practice. Monitor access patterns and data movement rather than message content. Route any investigation through HR and legal before enforcement action. Document the model's decision inputs so that an employee who is questioned can be shown the reason. Handled this way, behavioural detection protects company data without turning the security team into a surveillance function nobody trusts.</p>
<h2 id="what-should-a-90-day-ai-threat-detection-pilot-include">What Should a 90-Day AI Threat Detection Pilot Include?</h2>
<p>A pilot that runs longer than ninety days is a program, not a pilot, and it will be judged on promise rather than evidence. The pilots that convert into sustained funding share a recognisable shape.</p>
<ol>
<li><strong>Pick one surface.</strong> Identity is usually the right choice: it carries the highest breach involvement, the cleanest telemetry, and the shortest path to a visible win. Email and cloud workloads are the usual second and third choices.</li>
<li><strong>Baseline before you detect.</strong> Spend the first two to three weeks building behavioural baselines and recording current mean time to detect and contain. Without that "before" number the pilot cannot prove anything.</li>
<li><strong>Set the success threshold in advance.</strong> A credible target is a 30 to 50 percent reduction in time-to-detect on the chosen surface, or a measurable drop in false-positive rate at constant coverage. "Improved visibility" is not a target.</li>
<li><strong>Run in shadow mode for two weeks.</strong> Let the model score live traffic while analysts continue working as usual, then compare what the model flagged against what the team actually escalated.</li>
<li><strong>Instrument the analyst experience.</strong> Measure how long it takes to go from question to answer. If an analyst still needs forty minutes and three separate tools to investigate one alert, detection is fast and response is not.</li>
<li><strong>Report outcomes, not activity.</strong> Close the pilot with the MTTD and MTTC delta, the false-positive rate, and the two or three incidents the program caught that the previous process would have missed entirely.</li>
</ol>
<p>The most common pilot mistake is scoping too broadly. Three surfaces at once produces three inconclusive results; one surface produces a number the CFO can act on before the next budget cycle.</p>
<h2 id="how-does-ai-detection-fit-with-your-existing-siem-and-data-lake">How Does AI Detection Fit With Your Existing SIEM and Data Lake?</h2>
<p>Almost every enterprise already owns the hard part: years of logs in a SIEM or a cloud object store, identity data in the directory, endpoint telemetry from the EDR agent. The instinct to replace that stack before detecting anything is the single most expensive mistake in the category. Detection models need history, and a platform migration resets the clock on exactly the asset that makes behavioural baselining possible.</p>
<p>The pattern that works is additive. Connect the existing sources through read-only connectors, build the entity and baseline layers on top, and push risk-scored incidents back into the tools analysts already use — the SIEM console, the case manager, or increasingly the chat tool where the team coordinates during an incident. None of this requires re-architecting the warehouse, and it preserves the option to migrate later on evidence rather than on hope.</p>
<p>There is one genuine prerequisite: retention. Behavioural baselines degrade quickly when you can only see thirty days of history, because quarterly close cycles, seasonal hiring and contractor populations all look like anomalies inside a one-month window. Most enterprises find that ninety days to a year of identity and network telemetry is enough to produce stable baselines — and extending retention on those two sources costs a fraction of any platform purchase.</p>
"""

CN_NEW = """
<h2 id="what-does-a-modern-ai-threat-detection-architecture-look-like">现代AI威胁检测架构是什么样的？</h2>
<p>企业在AI威胁检测上的失败，很少是因为选错了模型，而是因为模型周围的架构太薄。一套现代检测栈包含五层，每一层都是项目悄然崩溃的地方。</p>
<table>
<thead>
<tr><th>层级</th><th>作用</th><th>薄弱时的失效表现</th></tr>
</thead>
<tbody>
<tr><td>遥测采集</td><td>将身份、终端、网络、云端与邮件日志归一化为统一模式</td><td>模型只能看到攻击面的一小部分，横向移动完全漏检</td></tr>
<tr><td>实体解析</td><td>将用户、设备、服务账号与工作负载归并成稳定身份</td><td>同一个人被拆成五个主体，行为基线全部碎片化</td></tr>
<tr><td>基线与评分</td><td>建立行为画像，对偏离赋予风险分值</td><td>要么持续误报，要么沉默漏检</td></tr>
<tr><td>关联分析</td><td>把多源弱信号串联成一条完整的事件叙事</td><td>分析师收到数百条无关告警，而不是十个真实事件</td></tr>
<tr><td>响应与反馈</td><td>提出处置建议，记录分析师决策，并回馈训练模型</td><td>系统永不进步，分析师逐渐失去信任</td></tr>
</tbody>
</table>
<p>其中有两个设计选择比其余都重要。第一，先做实体解析，再做行为建模：同一名员工从笔记本、手机和虚拟桌面登录，应该产生一条基线，而不是三条。第二，让关联层保持可解释。一个说不清输入来源的风险分——新国家、陌生设备、凌晨三点访问薪酬表——经不起分析师的质疑，也经不起监管方追问"为什么冻结这个账号"。</p>
<p>实践中，这套架构并不需要新平台。采集层通常已经存在于SIEM或日志湖中；实体解析与基线层才是新工作集中的地方，也正是决定项目每天产出十个事件还是一万条告警的地方。</p>
<h2 id="how-do-you-detect-insider-risk-and-credential-abuse">如何检测内部风险与凭证滥用？</h2>
<p>凭证滥用是最难的检测问题，原因恰恰在于登录发生的那一刻没有任何异常。攻击者持有正确的用户名和密码，而且常常来自与真实用户相同的国家与设备类型。Verizon《2024年数据泄露调查报告》指出，68%的泄露涉及非恶意的人为因素，这意味着真正有价值的信号出现在合法登录之后的行为里，而不是登录本身。</p>
<p>区分账号失陷与正常使用的信号是行为性的，而非静态的。平时只读取几张表的服务账号突然枚举数百张；一个季度下载40MB的财务人员在一个下午导出了4GB；从未接触过客户库的工程师在周日凌晨对它发起无过滤查询。单独看，三个信号都不值得报警，基于规则的系统会把它们全部丢弃。但把它们串起来、再与逐实体的行为基线比对，它们描述的是一次正在进行中的数据外泄。</p>
<p>相比外部威胁检测，内部风险需要更严格的治理姿态，跳过这一步的企业往往会在员工代表和监管方两头出问题。实践中有三条规则站得住脚：只监控访问模式与数据流动，不监控通信内容；任何调查在采取处置动作之前都要经过人力与法务；记录模型的决策输入，让被约谈的员工能看到理由。这样做，行为检测既保护了公司数据，又不会把安全团队变成一个人人提防的监控部门。</p>
<h2 id="what-should-a-90-day-ai-threat-detection-pilot-include">90天的AI威胁检测试点应该包含什么？</h2>
<p>超过90天的试点已经不是试点，而是一个项目，它会被按"前景"而不是"证据"来评判。那些最终拿到持续预算的试点，形状大致相同。</p>
<ol>
<li><strong>只选一个面。</strong>身份通常是最优选择：它涉及的泄露比例最高、遥测最干净、也最快能拿出可见成果。邮件与云工作负载通常是第二和第三选择。</li>
<li><strong>先建基线，再谈检测。</strong>用最初两到三周建立行为基线，并记录当前的平均检测时间与平均遏制时间。没有这个"之前"的数字，试点无法证明任何事情。</li>
<li><strong>提前定好成功阈值。</strong>可信的目标是在所选面上把检测耗时降低30%到50%，或者在覆盖率不变的前提下显著压低误报率。"可见性提升"不是目标。</li>
<li><strong>影子运行两周。</strong>让模型对真实流量打分，同时分析师照常工作，然后把模型标记的内容与团队实际升级的内容做对比。</li>
<li><strong>量化分析师体验。</strong>测量从一个问题到得到一个答案需要多久。如果分析师仍然需要四十分钟和三套工具才能查清一条告警，那么检测是快的，响应是慢的。</li>
<li><strong>汇报结果，而不是活动。</strong>用MTTD与MTTC的变化、误报率，以及两三个"旧流程会完全漏掉、新流程抓到了"的真实事件来收尾。</li>
</ol>
<p>试点最常见的错误是范围铺得太开。同时做三个面，会得出三个不确定的结论；只做一个面，会得到一个CFO能在下一个预算周期前据此行动的数字。</p>
<h2 id="how-does-ai-detection-fit-with-your-existing-siem-and-data-lake">AI检测如何与现有SIEM和数据湖配合？</h2>
<p>几乎每家企业都已经拥有了最难的部分：SIEM或云对象存储里数年的日志、目录服务中的身份数据、EDR代理采集的终端遥测。在检测到任何东西之前就想着替换这套栈，是这个领域里最昂贵的一个错误。检测模型需要历史数据，而平台迁移恰好会把行为基线赖以成立的资产清零。</p>
<p>可行的模式是叠加式的。通过只读连接器接入现有数据源，在其上构建实体层与基线层，再把带风险分的事件推回分析师已经在用的工具——SIEM控制台、工单系统，或者越来越多情况下，团队在事件期间用来协同的聊天工具。这一切都不需要重构数仓，也保留了日后基于证据而非基于希望来做迁移的选项。</p>
<p>只有一个真正的前提：留存周期。当只能看到三十天历史时，行为基线会迅速退化，因为季度结账周期、季节性招聘和外包人员流动在单月窗口里都长得像异常。多数企业发现，九十天到一年的身份与网络遥测足以产出稳定的基线——而延长这两类数据源的留存，成本只是任何一次平台采购的零头。</p>
"""

FAQ = {
 "EN": [
  ("How is AI threat detection different from signature-based SIEM rules?",
   "Signature rules match known-bad indicators, so they only catch attacks that have been seen before and documented. AI detection builds a behavioural baseline for each user, device, service account and workload, then scores deviations from that baseline. That is what lets it surface novel techniques, credential abuse and insider activity that no signature would ever match."),
  ("How much historical data do behavioural models need before they are useful?",
   "Plan on 90 days to one year of identity and network telemetry for stable baselines. Thirty days is usually too short: quarterly close cycles, seasonal hiring and contractor populations all look anomalous inside a one-month window. If retention is short, extend it on identity and network logs first, since those two sources carry most of the detection value."),
  ("Can we deploy AI threat detection without replacing our SIEM?",
   "Yes, and in most cases you should. The additive pattern connects existing log, identity, endpoint and cloud sources through read-only connectors, layers entity resolution and baselining on top, and pushes risk-scored incidents back into the console analysts already use. Replacing the SIEM first resets the history that behavioural baselines depend on."),
  ("What results should we expect from an AI threat detection pilot in the first 90 days?",
   "A realistic target is a 30 to 50 percent reduction in mean time to detect on the chosen surface, or a measurable drop in false-positive rate at constant coverage. You should also expect a shorter question-to-answer cycle for analysts. Anything framed as improved visibility without a baseline number is not a result you can take to the CFO."),
 ],
 "zh-CN": [
  ("AI威胁检测与基于签名的SIEM规则有什么区别？",
   "签名规则匹配已知的恶意指标，因此只能捕捉到此前出现过并被记录成规则的攻击。AI检测则为用户、设备、服务账号和工作负载分别建立行为基线，再对偏离基线的行为打分。正因如此，它能够发现签名永远匹配不到的新手法、凭证滥用和内部人员活动。"),
  ("行为模型需要多少历史数据才真正有用？",
   "建议准备90天到一年的身份与网络遥测数据，以建立稳定的基线。30天通常太短：季度结账周期、季节性招聘和外包人员流动，在一个月的窗口里都长得像异常。如果留存周期不足，优先延长身份日志与网络日志，这两类数据源承载了绝大部分检测价值。"),
  ("不替换现有SIEM，也能部署AI威胁检测吗？",
   "可以，而且在大多数情况下就应该这样做。叠加式方案通过只读连接器接入现有的日志、身份、终端与云端数据源，在其上构建实体解析与基线层，再把带风险分的事件推回分析师已在使用的控制台。先替换SIEM会清零行为基线所依赖的历史数据。"),
  ("在最初90天的试点里，应该期待什么样的结果？",
   "现实的目标是在所选面上把平均检测耗时降低30%到50%，或者在覆盖率不变的前提下显著压低误报率。此外，分析师的提问到得到答案的周期也应当明显缩短。任何只用\u201c可见性提升\u201d来描述、却没有基线数字支撑的说法，都不是能拿给CFO看的结果。"),
 ],
}

def main():
    # --- EN: insert new sections before Key Takeaways, rename statement H2s ---
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<h2 id="key-takeaways">Key Takeaways</h2>'
    assert anchor in b, "anchor missing"
    b = b.replace(anchor, EN_NEW.strip() + "\n" + anchor, 1)
    ren = {
        "Understanding the Current Landscape": "Why Has the Threat Landscape Outgrown the Traditional SOC?",
        "Key Principles and Strategic Framework": "What Principles Should Govern an AI Threat Detection Program?",
        "Implementation Approach and Best Practices": "How Should Enterprises Implement AI Threat Detection?",
        "Measuring Success and Demonstrating ROI": "How Do You Measure Success and Prove ROI to the Board?",
        "Common Pitfalls and How to Avoid Them": "What Are the Most Common Pitfalls and How Do You Avoid Them?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    # --- zh-CN: repair garbage strings, insert translated sections ---
    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    b = b.replace("自建ing 主动安全与 AI驱动的 威胁 detection", "构建主动安全与AI驱动的威胁检测能力")
    anchor = '<h2 id="关键要点">关键要点</h2>'
    assert anchor in b, "cn anchor missing"
    b = b.replace(anchor, CN_NEW.strip() + "\n" + anchor, 1)
    ren_cn = {
        "理解当前格局": "为什么威胁格局已经超出了传统SOC的能力？",
        "关键原则与战略框架": "AI威胁检测项目应该遵循哪些原则？",
        "实施方法与最佳实践": "企业应该如何落地AI威胁检测？",
        "衡量成功与展示投资回报率": "如何衡量成效并向董事会证明投资回报？",
        "常见陷阱及规避方法": "最常见的陷阱有哪些，如何规避？",
    }
    for old, new in ren_cn.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    b = b.replace('id="理解当前格局"', 'id="why-has-the-threat-landscape-outgrown-the-traditional-soc"')
    b = b.replace('id="关键原则与战略框架"', 'id="what-principles-should-govern-ai-threat-detection"')
    b = b.replace('id="实施方法与最佳实践"', 'id="how-should-enterprises-implement-ai-threat-detection"')
    b = b.replace('id="衡量成功与展示投资回报率"', 'id="how-do-you-measure-success-and-prove-roi"')
    b = b.replace('id="常见陷阱及规避方法"', 'id="what-are-the-most-common-pitfalls"')
    b = b.replace('id="关键要点"', 'id="key-takeaways"')
    b = b.replace('id="结论"', 'id="conclusion"')
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(
        SLUG,
        bodies={},
        faq=FAQ,
        tw_from_cn=True,
        faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"},
    )
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

import re
main()
