# -*- coding: utf-8 -*-
"""Batch part 3: second-round top-ups to clear floors.
EN: +1 H2 each for 5 files (<2500). zh-CN/zh-TW: +1 H2 each for 7 files (<3500).
Idempotent via unique ids. Never touches head/footer/links."""
import os, re
from opencc import OpenCC

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
cc = OpenCC('s2t')

# ---- EN second-round ----
EN_TOPUP2 = {
"treasury-management-ai-agents": '''
<h2 id="treasury-pilot-roadmap">What Does a Safe Treasury Agent Rollout Look Like?</h2>
<p>A safe rollout is boring by design. Begin in simulation: the agent operates against a mirrored ledger with no ability to move real funds, so the team can watch its decisions and tune thresholds without consequences. Only after the simulated behaviour is predictable do you grant read-only access to production liquidity data.</p>
<p>The next step is proposal mode, where the agent prepares recommended actions for a human to approve — typically a senior treasury analyst or the treasurer. Approval rates and override reasons become a feedback loop that sharpens the agent. Execution mode, with tightly bounded instructions and hard spending caps, is the final stage and should cover only the highest-confidence, lowest-impact tasks first.</p>
<p>Throughout, keep the supervisory layer's freeze switch one click away, and review every agent's permission scope quarterly. Rollouts that respect this sequence earn trust; those that jump straight to autonomous execution tend to earn a headline instead.</p>
''',
"voice-activated-analytics-for-hands-free-operations-a-2026-update": '''
<h2 id="voice-metrics">How Should You Measure Voice Analytics Success?</h2>
<p>Voice analytics is easy to demo and hard to prove, so instrument it from day one. The first metric is comprehension accuracy on real utterances — not the vendor's benchmark, but your users' actual questions, including accent, noise, and shop-floor jargon. Track how often the system asks a clarifying question or falls back to typing; a rising fallback rate signals confusion, not failure.</p>
<p>The second metric is task completion: did the user get the number they needed without switching devices? The third is adoption among the intended users — a voice tool that supervisors won't use on a busy shift has failed regardless of accuracy. Pair these with a qualitative channel: let users flag a wrong answer in one tap.</p>
<p>Together these metrics separate genuine utility from novelty. Report them monthly to the same sponsor who funded the pilot, and tie continued investment to movement in adoption rather than to demo impressiveness.</p>
''',
"conversational-bi-for-executives-dashboard-replacement": '''
<h2 id="exec-adoption-playbook">What Adoption Playbook Makes Executive Conversational BI Stick?</h2>
<p>Executives adopt conversational BI only when it survives the first awkward question. The playbook starts with a guided first session: pre-load the assistant with the ten questions the leader actually asks each month, so the first experience is a win, not a blank stare. Pair the launch with a short "ask, don't dig" norm — reward leaders who get answers by asking in the meeting.</p>
<p>Assign a champion in each function to curate the semantic layer behind the questions, closing gaps the moment a leader hits a missing metric. Publish a weekly "top questions asked" note so leaders see peers using it, which drives peer-driven adoption faster than any mandate. And build a visible escalation path: when the assistant can't answer, a human analyst follows up within the hour.</p>
<p>Stickiness comes from these small operating rituals, not from the technology. Programs that institutionalise the habit outlast the initial enthusiasm and become part of how the leadership team works.</p>
''',
"real-time-data-streaming-for-ai-powered-decision-making": '''
<h2 id="streaming-pitfalls">What Are the Most Common Real-Time Streaming Pitfalls?</h2>
<p>The first pitfall is building for latency you don't need, then paying for it forever in infrastructure and on-call load. The second is treating streaming as separate from the warehouse, which produces two sources of truth that inevitably disagree in a board meeting. The third is neglecting schema governance: events mutate as producers change, and without enforced contracts the downstream models silently break.</p>
<p>A subtler pitfall is assuming "real-time" means "always on everything." Most value concentrates in a few use cases; streaming the long tail of low-value events just burns money. Finally, teams underestimate the operational muscle required — someone must own alerts, backfills, and late-arriving data, or the pipeline quietly rots.</p>
<p>Avoiding these traps is less about the broker you choose and more about discipline: start narrow, share one store with batch, enforce contracts, and assign clear ownership before scaling.</p>
''',
"iot-data-platforms-manufacturing": '''
<h2 id="iot-governance">What Governance Keeps an IoT Data Platform Trustworthy?</h2>
<p>An IoT platform is only as trustworthy as the data it serves, and trust erodes fastest at the edge. Establish data-quality contracts at ingestion: every sensor stream must declare its unit, frequency, and expected range, and readings outside bounds are flagged rather than silently averaged away. Without this, a mis-calibrated sensor becomes a confident lie feeding every dashboard.</p>
<p>Governance also means lifecycle discipline. Assets enter and leave the fleet; an unretired sensor keeps reporting phantom output that pollutes cross-plant comparisons. Maintain a single registry of active assets, version the asset model, and require change approval for anything that affects a shared metric. Security is part of governance too: edge devices are physical and exposed, so firmware updates and access must be centrally controlled.</p>
<p>When governance is baked into the platform rather than bolted on, leaders trust the numbers — and trust is what turns raw telemetry into decisions.</p>
''',
}

# ---- zh-CN second-round (simplified); converted for zh-TW ----
ZH_TOPUP2 = {
"how-to-choose-conversational-bi-platform": '''
<h2 id="bi-change-management">如何选择能推动采纳的变革管理方式？</h2>
<p>对话式BI的技术选型只是成功的一半，另一半是变革管理。许多项目在工具上线后无人问津，根源在于没有设计采纳路径。有效的变革管理从一次引导式首次体验开始：提前把领导者每月真正会问的十个问题载入助手，让第一次使用就是一次成功而非尴尬的冷场。同时建立“提问而非翻找”的团队规范——在会议中通过提问获得答案的领导者应被公开认可。</p>
<p>为每个职能指派一名召集人，负责维护问题背后的语义层，并在领导者遇到缺失指标时第一时间补齐。每周发布“本周被问最多的问题”简报，让领导者看到同事正在使用，这种同侪驱动的采纳比任何行政命令都更有效。还要建立可见的升级通道：当助手无法回答时，人工分析师应在一小时内跟进。</p>
<p>粘性来自这些细小的运营习惯，而非技术本身。将习惯制度化的项目，往往能熬过最初的热情，最终成为领导团队的工作方式。衡量变革管理的标准也很简单：活跃提问的领导者比例是否逐月上升。</p>
''',
"treasury-management-ai-agents": '''
<h2 id="treasury-rollout">财务代理的安全上线路线应如何设计？</h2>
<p>安全的代理上线应当刻意显得“无趣”。第一步在仿真环境中进行：代理面对一份镜像账本运行，无权触达真实资金，团队可观察其决策并调优阈值而不承担后果。只有当仿真行为可预测后，才授予其对生产流动性数据的只读权限。</p>
<p>下一步是建议模式，代理准备推荐动作交由人工批准——通常是资深资金分析师或资金主管。批准率与驳回原因构成反馈环，持续打磨代理。执行模式带有严格边界的指令与硬性支出上限，应作为最后阶段，且仅先覆盖置信度最高、影响最小的任务。</p>
<p>在整个过程中，监督层的冻结开关应一键可达，并每季度复核每个代理的权限范围。遵循这一顺序的上线能赢得信任；那些直接跳到自主执行的上线，往往赢得的是一则负面新闻。上线节奏的把控，本质上是风险与速度之间的纪律权衡。</p>
''',
"iot-data-platforms-manufacturing": '''
<h2 id="iot-governance">什么治理让物联网数据平台值得信任？</h2>
<p>物联网平台的可信度取决于它所提供的数据质量，而信任往往在边缘处最先崩塌。应在摄取环节建立数据质量契约：每条传感器流必须声明其单位、频率与预期区间，超出边界的读数应被标记而非被悄然平均掉。否则，一个失准的传感器会变成喂养所有仪表板的“自信谎言”。</p>
<p>治理还意味着生命周期纪律。资产会进入也会退出机队；一个未退役的传感器会持续上报虚假输出，污染跨厂比较。应维护一份统一的活跃资产注册表，对资产模型做版本管理，并要求任何影响共享指标的变更都需审批。安全同样是治理的一部分：边缘设备物理暴露，固件更新与访问必须集中管控。</p>
<p>当治理内建于平台而非事后补丁，领导者才会信任这些数字——而信任，正是原始遥测转化为决策的前提。治理成熟的标志是：跨厂查询结果的偏差能在分钟级被定位到具体设备。</p>
''',
"data-mesh-governance-balancing-central-and-local-control": '''
<h2 id="mesh-org-design">数据网格需要怎样的组织结构支撑？</h2>
<p>数据网格常被误认为纯技术架构，但它真正考验的是组织结构。去中心化的数据产品需要一类新型角色——领域数据负责人，他们既懂业务事件，又对数据的质量与时效负责。这个角色必须被正式授权，而非由工程师兼职，否则所有权会再次悬空。</p>
<p>中心团队的角色也随之转变：从“生产数据”转为“提供平台与标准”。它应设立一个治理委员会，由各领域的负责人组成，负责裁决跨领域的契约冲突与核心定义争议。这种联邦结构避免了两种极端：中心过度审批造成的瓶颈，以及领域各自为政造成的定义分裂。</p>
<p>组织设计的关键，是让激励与责任对齐。当领域团队的绩效与其数据产品被消费的程度挂钩，质量自然会提升；当中心团队的成效取决于领域的成功而非管控的数量，赋能才会真正发生。结构对了，技术才落得下去。</p>
''',
"enterprise-data-products-operating-model-that-makes-data-useful": '''
<h2 id="edp-lifecycle">数据产品应如何管理其生命周期？</h2>
<p>数据产品不是发布一次就结束，而是像软件产品一样有完整的生命周期。起点是立项：明确它服务的决策、消费方是谁、以及成功指标是什么。接着是构建与发布到自助目录，附带清晰的服务级协议与数据契约，让消费方能即取即用。</p>
<p>运营阶段最容易被忽视。需要持续监控契约合规、新鲜度与文档完整度，并按消费方的反馈迭代。当底层源系统变更时，数据产品必须随之演进，而非默默断裂。到了退役阶段，应提前通知消费方、提供迁移路径，并从目录中正式下架，避免留下无人认领的“僵尸数据产品”。</p>
<p>生命周期管理的成熟度，体现在能否回答两个问题：当前有多少个数据产品处于活跃状态？其中有多少个正被跨领域消费？能把这两件事说清楚的组织，才真正跑通了数据产品运营模式。</p>
''',
"voice-activated-analytics-for-hands-free-operations-a-2026-update": '''
<h2 id="voice-metrics">应如何衡量语音分析的成功？</h2>
<p>语音分析很容易做演示，却很难证明价值，因此必须从第一天起就做好埋点。第一个指标是真实语料下的理解准确率——不是厂商的基准，而是你用户实际提出的问题，包含口音、噪声与车间行话。追踪系统追问澄清或回退打字的频率；回退率上升代表困惑，而非失败。</p>
<p>第二个指标是任务完成度：用户是否无需切换设备就拿到了所需数字？第三个是目标用户的采纳率——一个主管在繁忙班次不愿使用的语音工具，无论准确率多高都已失败。将这些与一条质性通道结合：让用户一键标记错误答案。</p>
<p>这些指标共同区分了真实效用与噱头。每月向资助试点的同一位发起人汇报，并把持续投入与采纳率的提升挂钩，而非与演示的精彩程度挂钩。衡量得当，语音分析才能从秀场走向产线。</p>
''',
"real-time-data-streaming-for-ai-powered-decision-making": '''
<h2 id="stream-pitfalls">实时流处理最常见的陷阱是什么？</h2>
<p>第一个陷阱是为不需要的延迟买单，然后永远在基础设施与值班成本上偿还。第二个是把流处理与数据仓库割裂对待，产生两个事实来源，最终在董事会上自相矛盾。第三个是忽视schema治理：生产者变更导致事件悄然变形，缺乏强制契约的下游模型会静默崩溃。</p>
<p>一个更隐蔽的陷阱是假设“实时”等于“一切常开”。多数价值集中在少数用例上；把长尾低价值事件也流式化，只是白白烧钱。最后，团队低估了所需的运维肌肉——必须有人负责告警、补数与迟到数据，否则管道会悄悄腐化。</p>
<p>避开这些陷阱，更多关乎纪律而非你选了哪个代理：起步要窄、与批处理共享单一存储、强制契约、并在扩规模前明确所有权。能守住纪律的团队，才会让实时数据真正驱动决策，而非驱动账单。</p>
''',
}

EN_FAQ_ANCHOR = '<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">'
ZH_FAQ_ANCHOR_CN = '<section class="faq-section" id="faq" aria-label="常见问题">'
ZH_FAQ_ANCHOR_TW = '<section class="faq-section" id="faq" aria-label="常見問題">'

def insert_before(s, anchor, block):
    idx = s.find(anchor)
    if idx == -1: return None
    return s[:idx] + block + s[idx:]

def has_faq(s): return '<section class="faq-section"' in s

def cjk_count(s): return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', s))
def word_count(s):
    t = re.sub(r'<[^>]+>',' ',s); t = re.sub(r'&[a-z]+;',' ',t)
    return len(re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*", t))
def article(s):
    m = re.search(r'<article\b[^>]*id="article-content"[^>]*>(.*?)</article>', s, re.S)
    return m.group(1) if m else ''
def faq_items(s):
    m = re.search(r'<section class="faq-section"[^>]*>(.*?)</section>', s, re.S)
    return 0 if not m else len(re.findall(r'class="faq-item"', m.group(1)))

log = []

# EN
for slug, block in EN_TOPUP2.items():
    p = os.path.join(ROOT, "blog/articles", slug + ".html")
    s = open(p, encoding='utf-8').read()
    uid = re.search(r'id="([^"]+)"', block)
    if uid and uid.group(1) in s:
        log.append(("EN", slug, "SKIP(idempotent)")); continue
    if EN_FAQ_ANCHOR not in s:
        log.append(("EN", slug, "FAQ anchor missing")); continue
    ns = insert_before(s, EN_FAQ_ANCHOR, block)
    open(p,'w',encoding='utf-8').write(ns)
    log.append(("EN", slug, f"OK words={word_count(article(ns))}"))

# zh
for slug, cn_block in ZH_TOPUP2.items():
    tw_block = cc.convert(cn_block)
    for (lang, sub, anchor) in [('zh-CN','zh-cn',ZH_FAQ_ANCHOR_CN),('zh-TW','zh-tw',ZH_FAQ_ANCHOR_TW)]:
        p = os.path.join(ROOT, sub+"/blog/articles", slug + ".html")
        s = open(p, encoding='utf-8').read()
        blk = cn_block if lang=='zh-CN' else tw_block
        uid = re.search(r'id="([^"]+)"', blk)
        if uid and uid.group(1) in s:
            log.append((lang, slug, "SKIP(idempotent)")); continue
        if not has_faq(s):
            log.append((lang, slug, "no faq (unexpected)")); continue
        if anchor not in s:
            log.append((lang, slug, "FAQ anchor missing")); continue
        ns = insert_before(s, anchor, blk)
        open(p,'w',encoding='utf-8').write(ns)
        log.append((lang, slug, f"OK cjk={cjk_count(article(ns))} faq={faq_items(ns)}"))

print("==== APPLY LOG (round 3) ====")
for r in log: print(r)

# final verify of the affected files
slugs_all = open(os.path.join(ROOT,"_batch_pipeline/gap_batches/gbatch_001.txt")).read().split()
affected = set(list(EN_TOPUP2.keys()) + list(ZH_TOPUP2.keys()))
print("\n==== VERIFY affected + any still below floor ====")
for slug in slugs_all:
    if slug not in affected: continue
    for path, lang in [("blog/articles/%s.html"%slug,'EN'),
                      ("zh-cn/blog/articles/%s.html"%slug,'zh-CN'),
                      ("zh-tw/blog/articles/%s.html"%slug,'zh-TW')]:
        s = open(os.path.join(ROOT,path),encoding='utf-8').read()
        a = article(s); w = word_count(a) if lang=='EN' else cjk_count(a)
        flag = '' if (lang=='EN' and w>=2500) or (lang!='EN' and w>=3500) else '  <-- BELOW FLOOR'
        print(f"{lang:5} {slug[:46]:46} metric={w:5} faq={faq_items(s):2} jsonld={s.count('FAQPage')}{flag}")
