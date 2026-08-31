# -*- coding: utf-8 -*-
"""Phase 3b: extra top-up for event-driven & future-of-work zh (still <3500 ideographs)."""
import re, os, html as _html
from opencc import OpenCC
BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
cc = OpenCC('s2t')

EXTRA = {
"event-driven-architecture-for-ai-agent-orchestration-a-2026-update": [
 ("事件驱动架构在合规与审计方面有何优势？",
  ["事件天然带有时间戳与发起方，使每一次智能体动作都可被完整回溯。当监管要求说明某项决策的依据时，团队可以直接调取相关事件流，证明数据来源与处理顺序符合要求，而不必在事后拼凑日志。",
   "这种可审计性在金融、医疗与政务等强监管行业尤为关键，也是事件驱动架构相较临时脚本编排的显著长处。"]),
 ("如何为事件驱动智能体设定成本与速率边界？",
  ["应为每个事件流设置速率上限与预算阈值，当消费成本异常上升时自动降级或暂停，防止失控的编排产生意外账单。结合语义层的访问策略，确保智能体只能触及被授权的数据域，从机制上降低越权风险。"]),
],
"the-future-of-work-ai-augmented-decision-making": [
 ("企业应如何缓解人工智能增强带来的焦虑与阻力？",
  ["阻力往往来自不确定性。透明的试点、可见的成效与对员工再技能的投资，比自上而下的强制推广更有效。让一线团队参与工具设计，把人工智能定位为减轻枯燥劳动的助手，而非绩效考核的监视者，可以显著降低抵触。",
   "与此同时，建立清晰的问责边界，明确人工智能提供建议、人做最终决定，能让员工把注意力放在更高价值的工作上，逐步形成人与系统互相增强的正向循环，使组织整体决策质量稳步提升。"]),
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
for slug, cn_secs in EXTRA.items():
    tw_secs = [(cc.convert(h2), [cc.convert(p) for p in paras]) for h2,paras in cn_secs]
    for lang, sub, secs in [("cn","zh-cn/blog/articles", cn_secs),("tw","zh-tw/blog/articles", tw_secs)]:
        fn = os.path.join(BASE, sub, slug+".html")
        raw = open(fn, encoding="utf-8").read()
        head0 = raw[:raw.index("<body")]
        m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', raw, re.S)
        before = cjk_of(m.group(1))
        if before >= 3500:
            report.append((slug, lang, before, before, "skip"))
            continue
        start = m.start()
        close = raw.index("</article>", start)
        add = build_sections(secs)
        new_raw = raw[:close] + "\n" + add + raw[close:]
        assert new_raw[:new_raw.index("<body")] == head0
        assert "?v=20260826" in new_raw
        open(fn,"w",encoding="utf-8").write(new_raw)
        mm = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', new_raw, re.S)
        report.append((slug, lang, before, cjk_of(mm.group(1)), "added"))
print("===== PHASE 3b =====")
for r in report: print(r)
print("DONE phase3b")
