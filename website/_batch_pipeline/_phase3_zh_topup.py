# -*- coding: utf-8 -*-
"""
Phase 3: top up zh-CN / zh-TW article-content to >= 3500 CJK by appending
genuine, topic-specific question-H2 prose INSIDE <article id="article-content">.
Idempotent: only adds if current count < floor. Preserves <head>, footer, paths.
"""
import re, os, html as _html
from opencc import OpenCC

BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
cc = OpenCC('s2t')  # simplified -> traditional

SLUGS = ["competitive-advantage-through-ai","agentic-workflows-enterprise-automation",
"text-to-sql-accuracy-enterprise-trust","mcp-vs-traditional-apis-why-context-protocol-changes-everything",
"case-study-consultancy-cut-reporting-time-mcp-bi",
"event-driven-architecture-for-ai-agent-orchestration-a-2026-update",
"the-future-of-work-ai-augmented-decision-making"]

# Simplified-Chinese genuine content per slug: list of (h2, [paragraphs])
CONTENT = {
"competitive-advantage-through-ai": [
 ("企业应如何将人工智能优势转化为可衡量的竞争壁垒？",
  ["许多企业把模型准确率当作终点，却忽略了真正的壁垒来自数据回路与决策延迟。当专有数据在受治理的语义层上持续流动，模型每周都在用企业自身的业务结果重新训练，竞争对手即使复制算法也无法复制这条回路。",
   "建议设立一个以业务指标为锚的复盘机制，把每次决策的可信度、耗时与回报记录下来，使人工智能能力随运营沉淀为组织记忆，最终形成难以模仿的结构性优势。"]),
],
"agentic-workflows-enterprise-automation": [
 ("企业如何为智能体工作流建立可靠的评估与回滚机制？",
  ["智能体一旦获得执行权限，错误会被迅速放大。稳妥的做法是先在小范围只读场景验证，记录每一步的工具调用与理由，再用离线回放对比人工决策。",
   "只有当自动化结果与专家判断的一致率稳定在高位，才逐步开放写入与编排权限，并为每个关键动作保留一键回滚，确保风险始终可控。"]),
],
"text-to-sql-accuracy-enterprise-trust": [
 ("如何提升企业环境中 Text-to-SQL 的可信度与可解释性？",
  ["准确率的瓶颈往往不在模型，而在语义层。当指标口径、维度与同义词被明确定义，Text-to-SQL 生成的查询更容易对齐业务意图。",
   "建议引入查询血缘与置信度提示：对低置信结果主动追问澄清，对高风险聚合展示中间步骤，让分析师在秒级内判断结果可否采信。配合人工抽检与语义校验，企业才能把自助式分析真正交给业务用户。"]),
 ("企业应在哪些场景优先落地 Text-to-SQL？",
  ["优先选择查询模式稳定、口径清晰、错误成本可控的场景，例如标准报表自助取数与异常归因初筛。避免在口径频繁变动或合规敏感的核心核算上一步到位，先用人工在环的方式积累信任。"]),
],
"mcp-vs-traditional-apis-why-context-protocol-changes-everything": [
 ("企业应如何规划从传统 API 到 MCP 的迁移路径？",
  ["不必推倒重来。MCP 通常封装既有 REST 与 GraphQL 接口，因此迁移可以从增量开始：先为高频、跨系统的取数场景接入 MCP 服务器，让智能体获得统一发现与权限层。",
   "随着连接器复用率提升，原本分散的集成成本会显著下降。建议以治理能力为红线，把鉴权、审计与速率限制前移到协议层，避免在每个智能体里重复实现。"]),
],
"case-study-consultancy-cut-reporting-time-mcp-bi": [
 ("这家咨询公司是如何把周报时间压缩到数小时的？",
  ["关键在于把分散在邮件、表格与 BI 工具中的项目数据，通过 MCP 服务器统一接入受治理的语义层。顾问用自然语言提出取数问题，系统自动拼装跨源查询并返回带血缘的说明，省去了手工核对口径的往返。",
   "原本需要多人协作、跨时区确认的周报，现在由一位顾问在对话中完成初稿，其余时间用于判断与建议，交付质量反而更高。"]),
 ("这类落地给其他专业服务团队带来哪些启示？",
  ["第一，先把高频、低创造性的取数动作自动化，而不是追求端到端替代专家。第二，语义层与治理必须先行，否则加速只会放大错误。第三，用可解释的输出建立信任：当顾问能看到每一步数据来源，他们才敢把结果直接交给客户。"]),
 ("复制该模式需要哪些前提条件？",
  ["需要相对标准化的项目数据结构、明确的指标口径，以及愿意先在小范围试点的团队。技术债越低，接入 MCP 的收益越明显，推广也越顺畅。"]),
],
"event-driven-architecture-for-ai-agent-orchestration-a-2026-update": [
 ("事件驱动架构如何降低智能体编排的耦合度？",
  ["当每个能力以事件而非同步调用暴露，智能体只需发布意图、订阅结果，无需了解下游实现。新能力可以即插即用地接入，故障也被限制在单个消费者内，不会沿调用链雪崩。",
   "这种解耦让编排逻辑更稳定，也更容易在合规要求变化时替换某一环节，而不必重构整条链路。"]),
 ("企业落地事件驱动智能体时应注意什么？",
  ["首先是事件契约的版本治理，避免生产者与消费者因字段变更而失配；其次是可观测性，必须为每条事件保留轨迹与重放能力，便于审计与排错；最后是幂等与顺序保障，确保同一事件被重复消费不会产生副作用。"]),
 ("事件驱动与批处理应当如何取舍？",
  ["对延迟敏感、需要即时反应的决策采用事件驱动；对口径重算、历史回测等重计算任务保留批处理。两者通过同一语义层共享指标定义，既保证实时性，也不牺牲一致性。"]),
],
"the-future-of-work-ai-augmented-decision-making": [
 ("人工智能增强决策会如何重塑岗位与技能？",
  ["变化不在于岗位消失，而在于岗位内涵转移：重复性的取数、汇总与初稿撰写被自动承担，人的时间回到判断、沟通与责任界定上。能够把业务问题转化为可验证假设、并解读模型输出的员工，价值会显著上升。",
   "组织需要重新设计绩效与协作方式，让人工智能成为思考的延伸而非替代。"]),
 ("领导者应如何为人工智能增强的团队建立信任？",
  ["信任来自透明与可解释。当每一次建议都附带数据来源、置信区间与适用边界，团队才敢采纳。领导者应要求关键决策保留人工确认环节，并把失败当作改进回路的输入，而非追责的终点。"]),
 ("哪些职能会最先被人工智能增强？",
  ["分析、运营、营销与客服等知识密集型职能最先受益，因为它们的产出高度依赖信息整合与表达。财务、法务等强合规职能则以后台辅助与风险提示的方式渐进引入，在可控范围内释放专家精力。"]),
 ("企业应如何衡量人工智能对工作的真实影响？",
  ["不要只盯着成本节省，更要跟踪决策周期、返工率与一线员工的满意度。当决策更快、错误更少、员工把时间花在更高价值的事务上，人工智能增强才算真正生效。建议用双周复盘持续校准目标，避免把工具采用率误当作业务成果。"]),
],
}

def cjk_of(art):
    t = _html.unescape(re.sub(r'<[^>]+>',' ', art))
    return sum(1 for c in t if '一'<=c<='鿿')

def build_sections(cn_sections):
    out=""
    for h2, paras in cn_sections:
        out += f'            <h2>{_html.escape(h2, quote=True)}</h2>\n'
        for p in paras:
            out += f'            <p>{_html.escape(p, quote=True)}</p>\n'
    return out

report=[]
for slug in SLUGS:
    cn_secs = CONTENT[slug]
    tw_secs = [(cc.convert(h2), [cc.convert(p) for p in paras]) for h2,paras in cn_secs]
    for lang, sub, secs in [("cn","zh-cn/blog/articles", cn_secs),("tw","zh-tw/blog/articles", tw_secs)]:
        fn = os.path.join(BASE, sub, slug+".html")
        raw = open(fn, encoding="utf-8").read()
        head0 = raw[:raw.index("<body")]
        m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', raw, re.S)
        art = m.group(1)
        before = cjk_of(art)
        if before >= 3500:
            report.append((slug, lang, before, before, "skip (already >=3500)"))
            continue
        # locate close of article-content (first </article> after its open)
        start = m.start()
        close = raw.index("</article>", start)
        add = build_sections(secs)
        # insert inside article-content, before its closing tag
        new_raw = raw[:close] + "\n" + add + raw[close:]
        assert new_raw[:new_raw.index("<body")] == head0, "HEAD CHANGED "+slug+" "+lang
        assert "?v=20260826" in new_raw
        open(fn,"w",encoding="utf-8").write(new_raw)
        # recompute
        mm = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', new_raw, re.S)
        after = cjk_of(mm.group(1))
        report.append((slug, lang, before, after, "added"))

print("===== PHASE 3 REPORT =====")
for r in report: print(r)
print("DONE phase3")
