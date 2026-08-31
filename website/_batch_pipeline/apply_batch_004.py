# -*- coding: utf-8 -*-
"""Batch part 4: final zh-CN/zh-TW top-ups for 5 slugs still <3500 CJK.
One H2 each. Idempotent via unique ids. Never touches head/footer/links."""
import os, re
from opencc import OpenCC

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
cc = OpenCC('s2t')

ZH_TOPUP4 = {
"treasury-management-ai-agents": '''
<h2 id="treasury-metrics">如何衡量财务代理的运营表现？</h2>
<p>代理上线后，衡量其表现不能只看"省了多少人力"，而要建立在风险可控前提下的效率提升。建议设置三层指标。第一层是准确性：建议被采纳的比例、被驳回的原因分布，以及误操作被拦截的次数——这些反映代理的判断质量。</p>
<p>第二层是时效：从异常被标记到行动完成的端到端耗时，相比纯人工流程缩短了多少。第三层是覆盖度：当前有多少类例行任务已交由代理处理，以及代理在峰值时段的稳定性。三者结合，才能判断代理是真正创造价值，还是仅在低风险任务上做表面文章。</p>
<p>最关键的护栏指标是"零未授权动作"：任何超出预设边界的执行都应被即时拦截并告警。当这一指标长期为零，且前两层指标持续改善，代理才值得被赋予更大的权限范围。</p>
''',
"iot-data-platforms-manufacturing": '''
<h2 id="iot-security">物联网数据平台的安全要点是什么？</h2>
<p>物联网平台的安全挑战来自其物理暴露面：成千上万的边缘设备分布在工厂、仓库与户外，攻击者触达它们的成本远低于触达中心机房。因此安全设计必须从设备身份开始——每台设备都应拥有唯一且可轮换的凭证，而非共享密钥或出厂默认口令。</p>
<p>数据传输需全程加密，并在边缘侧完成完整性校验，防止中间人篡改遥测。平台侧则应对设备做微隔离：即便单个设备被攻陷，其横向移动能力也应被严格限制。固件更新必须由中心签名并集中推送，避免现场设备运行未经验证的版本。</p>
<p>最后，安全与治理是一体两面：设备注册、退役与权限变更都应进入审计日志。一个能回答"此刻网络上有哪些设备、各自在做什么"的平台，才算真正具备安全可控的物联网能力。</p>
''',
"data-mesh-governance-balancing-central-and-local-control": '''
<h2 id="mesh-success-factors">数据网格成功的隐性因素有哪些？</h2>
<p>多数数据网格项目把注意力放在技术上，却忽略了两个隐性因素，而它们往往决定成败。其一是信任文化：领域团队必须相信，把数据做成产品不会让自己背上无限责任，也不会被中心团队事后收编。没有这种信任，所有权只会停留在名义上。</p>
<p>其二是发现与可观测性：再好的数据产品，如果消费方找不到、看不懂、信不过，也等于零。目录的搜索体验、数据血缘的透明度、以及质量与新鲜度的实时可见，是驱动采用的隐形引擎。许多项目在管道上投入巨大，却在发现体验上吝啬，结果产品无人问津。</p>
<p>还有一层是激励对齐：当领域团队的考核与数据产品的消费广度挂钩，质量会自然提升；当中心团队的成效取决于领域的成功，赋能才会真正发生。把这三件事做扎实，技术架构才能发挥出原本设想的价值。</p>
''',
"voice-activated-analytics-for-hands-free-operations-a-2026-update": '''
<h2 id="voice-privacy">语音分析的隐私边界应如何划定？</h2>
<p>语音天然比文字更敏感，因为它可能在无意中采集到同事对话、客户信息甚至背景中的私人内容。划定隐私边界的第一原则是可逆同意：用户明确知晓自己正在被聆听，并随时可以关闭。任何在用户不知情下常开的麦克风，都会迅速侵蚀信任。</p>
<p>技术上应采用边缘侧的语音处理：原始音频尽量不在设备外留存，仅将识别出的结构化查询与结果上送，并附带来源标识。对必须留存用于训练的片段，应做去标识化并获得明示授权。访问控制要与业务角色绑定，确保敏感场景的语音数据不会被越权调阅。</p>
<p>最后，建立透明的留存与删除政策：用户应能查询"我的哪些语音被记录、保留多久、用于何处"，并在离职或项目结束时彻底清除。隐私不是合规的包袱，而是语音分析能否被组织接纳的前提条件。</p>
''',
"real-time-data-streaming-for-ai-powered-decision-making": '''
<h2 id="stream-org">实时数据流需要怎样的组织能力？</h2>
<p>实时流处理的技术选型常被过度讨论，组织能力却常被低估。最大的缺口是"事件思维"：团队习惯了表与批处理，习惯于"数据在某刻已经准备好"；而流处理要求他们思考"数据在流动中如何被校验、如何补数、如何容忍迟到"。这种思维转变培训，比选哪个代理更影响成败。</p>
<p>其次是运维所有权。一条常驻的流管道需要明确的待命责任：谁来响应消费滞后？谁来处理schema变更导致的断裂？谁批准新的事件源接入？模糊的所有权会让管道在无人负责中悄悄腐化。建议设立跨职能的流数据值守小组，把告警、回放与修复流程标准化。</p>
<p>最后是产品化视角：把实时数据当作面向内部消费方的产品来运营，提供稳定的契约、清晰的文档与版本策略。当组织具备这三层能力，实时流才从炫技项目变成可靠的生产力。</p>
''',
}

ZH_FAQ_ANCHOR_CN = '<section class="faq-section" id="faq" aria-label="常见问题">'
ZH_FAQ_ANCHOR_TW = '<section class="faq-section" id="faq" aria-label="常見問題">'

def insert_before(s, anchor, block):
    idx = s.find(anchor)
    if idx == -1: return None
    return s[:idx] + block + s[idx:]

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

log=[]
for slug, cn_block in ZH_TOPUP4.items():
    tw_block = cc.convert(cn_block)
    for (lang, sub, anchor) in [('zh-CN','zh-cn',ZH_FAQ_ANCHOR_CN),('zh-TW','zh-tw',ZH_FAQ_ANCHOR_TW)]:
        p = os.path.join(ROOT, sub+"/blog/articles", slug + ".html")
        s = open(p, encoding='utf-8').read()
        blk = cn_block if lang=='zh-CN' else tw_block
        uid = re.search(r'id="([^"]+)"', blk)
        if uid and uid.group(1) in s:
            log.append((lang, slug, "SKIP(idempotent)")); continue
        if anchor not in s:
            log.append((lang, slug, "FAQ anchor missing")); continue
        ns = insert_before(s, anchor, blk)
        open(p,'w',encoding='utf-8').write(ns)
        log.append((lang, slug, f"OK cjk={cjk_count(article(ns))} faq={faq_items(ns)}"))

print("==== APPLY LOG (round 4) ====")
for r in log: print(r)

# full final verify of all 45
slugs=open(os.path.join(ROOT,"_batch_pipeline/gap_batches/gbatch_001.txt")).read().split()
print("\n==== FINAL VERIFY (all 45, floor EN>=2500 / zh>=3500) ====")
any_below=False
for slug in slugs:
    for path, lang in [("blog/articles/%s.html"%slug,'EN'),
                      ("zh-cn/blog/articles/%s.html"%slug,'zh-CN'),
                      ("zh-tw/blog/articles/%s.html"%slug,'zh-TW')]:
        s=open(os.path.join(ROOT,path),encoding='utf-8').read()
        a=article(s); w=word_count(a) if lang=='EN' else cjk_count(a)
        ok = (w>=2500) if lang=='EN' else (w>=3500)
        if not ok: any_below=True
        flag='' if ok else '  <-- BELOW FLOOR'
        print(f"{lang:5} {slug[:44]:44} metric={w:5} faq={faq_items(s):2} jsonld={s.count('FAQPage')}{flag}")
print("\nANY BELOW FLOOR:", any_below)
