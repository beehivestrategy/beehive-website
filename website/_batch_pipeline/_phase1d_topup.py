# -*- coding: utf-8 -*-
import re, os
BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
ZH = {
"competitive-advantage-through-ai": {
"cn": "<p>最容易被低估的，是速度本身的战略价值。当竞争对手还在等月度报告时，能在当天用自有数据回答关键问题的企业，已经在定价、留客与资源配置上占了先手。决策延迟是竞争中最不被衡量的维度，却往往是最具决定性的。把「从问题到行动」的时间当作核心指标来追踪，企业才会发现：真正的优势不在模型多先进，而在谁先回答、且答案根植于只有自己才有的数据。</p>",
"tw": "<p>最容易被低估的，是速度本身的戰略價值。當競爭對手還在等月度報告時，能在當天用自有資料回答關鍵問題的企業，已經在定價、留客與資源配置上佔了先手。決策延遲是競爭中最不被衡量的維度，卻往往是最具決定性的。把「從問題到行動」的時間當作核心指標來追蹤，企業才會發現：真正的優勢不在模型多先進，而在誰先回答、且答案根植於只有自己才有的資料。</p>"},
"agentic-workflows-enterprise-automation": {
"cn": "<p>衡量智能体工作流时，别被「自动化了多少」误导，要看「决策快了多少、且错了多少」。一个把周期从三天压到四小时、但把错误悄悄推给客户的智能体，价值为负。健康的标志是例外率随时间下降、返工率可控、且每个动作都可追溯。把这些指标每周摊在赞助者面前，程序才会由证据而非演示引导。企业真正买到的，不是某个聪明的机器人，而是一套让下一个自动化越来越便宜、越来越安全的平台。</p>",
"tw": "<p>衡量智能體工作流時，別被「自動化了多少」誤導，要看「決策快了多少、且錯了多少」。一個把週期從三天壓到四小時、但把錯誤悄悄推給客戶的智能體，價值為負。健康的標誌是例外率隨時間下降、返工率可控、且每個動作都可追溯。把這些指標每週攤在贊助者面前，程式才會由證據而非示範引導。企業真正買到的，不是某個聰明的機器人，而是一套讓下一個自動化越來越便宜、越來越安全的平台。</p>"},
"why-edge-ai-manufacturing-logistics-energy": {
"cn": "<p>边缘AI的回报常以「避免的损失」而非「新增的收入」呈现，这使它容易被传统ROI框架低估。一条因即时检测而少出的次品、一个因本地推理而未停的产线、一次因场站优化而省下的调度成本，都是实打实的毛利保护。董事会若只看新增营收，会错过边缘AI最稳健的价值。把它框定为风险降低与毛利保护，其次才是产能扩张，企业才会在重工所与能源领域获得持续资助，并把第一个站点的经验复制成整个资产群的受管平台。</p>",
"tw": "<p>邊緣AI的回報常以「避免的損失」而非「新增的收入」呈現，這使它容易被傳統ROI框架低估。一條因即時檢測而少出的次品、一個因本地推理而未停的產線、一次因場站優化而省下的調度成本，都是實打實的毛利保護。董事會若只看新增營收，會錯過邊緣AI最穩健的價值。把它框定為風險降低與毛利保護，其次才是產能擴張，企業才會在重工業與能源領域獲得持續資助，並把第一個站點的經驗複製成整個資產群的受管平台。</p>"},
"text-to-sql-accuracy-enterprise-trust": {
"cn": "<p>信任不是一次上线就能获得的，而是每次答案都可解释、可审计、可纠错所累积的结果。当用户能看见生成的SQL、触及的表与采用的语义定义，他们才会把对话中的数字用于决策。把「展示你的工作」当作产品原则，而非合规负担，text-to-sql才会从聪明的玩具变为可靠的接口。企业真正需要的，不是更流畅的模型，而是能让业务有信心说「这个回答我可以签字」的整套机制。</p>",
"tw": "<p>信任不是一次上線就能獲得的，而是每次答案都可解釋、可審計、可糾錯所累積的結果。當用戶能看見生成的SQL、觸及的表與採用的語意定義，他們才會把對話中的數字用於決策。把「展示你的工作」當作產品原則，而非合規負擔，text-to-sql才會從聰明的玩具變為可靠的介面。企業真正需要的，不是更流暢的模型，而是能讓業務有信心說「這個回答我可以簽字」的整套機制。</p>"},
}
def ins(html, block):
    if '<section class="faq-section"' in html:
        idx = html.index('<section class="faq-section"')
    else:
        idx = html.index('<nav class="article-nav"')
    return html[:idx] + block + "\n" + html[idx:]
def cjk(s): return len(re.findall(r'[\u3400-\u9fff\uf900-\ufaff]', s))
for slug, langs in ZH.items():
    for lg, p in langs.items():
        sub = "zh-cn/blog/articles" if lg=="cn" else "zh-tw/blog/articles"
        fn = os.path.join(BASE, sub, slug + ".html")
        html = open(fn, encoding="utf-8").read()
        head0 = html[:html.index("<body")]
        new = ins(html, p)
        assert new[:new.index("<body")] == head0 and "?v=20260826" in new
        open(fn, "w", encoding="utf-8").write(new)
        print("ZH d", slug, lg, cjk(new[new.index('<article class="article-content" id="article-content">'):new.rindex('</article>')]))
print("DONE phase1d")
