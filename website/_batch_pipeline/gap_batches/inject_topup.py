import os, re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def sec(h2, body):
    return f'\n<h2>{h2}</h2>\n<p>{body}</p>\n'

ADD = {
 ("education-personalised-learning-pathways-through-data-a-2026-update","en"): [
   ("What Does Responsible Personalisation Look Like in Practice?",
    "Responsible personalisation puts guardrails in front of the model, not after it. Define which attributes are never used for segmentation, require human review before any high-stakes intervention, and keep an audit log of every path change. When students and teachers can see and challenge the logic, trust compounds and the system earns the right to personalise more deeply over time."),
 ],
 ("ai-regulatory-sandbox-participation","zh-CN"): [
   ("沙盒结束后，如何把成果转化为正式合规能力？",
    "沙盒的价值在于把不确定的监管互动变成可复用的能力。项目收尾时，应把验证过的模型文档、风险缓释措施与监控指标固化为正式的模型卡片与上架流程，使后续同类场景可以直接套用，而不必每次都重新走一遍沙盒。同时要把沙盒中建立的反馈通道保留下来，作为持续合规的一部分。监管方通常欢迎这种「从试点到生产」的清晰路径，因为它降低了系统性风险，也让企业能够在获批范围内更快扩展创新应用，把一次性的准入优势转化为长期的可信运营能力。"),
 ],
 ("ai-regulatory-sandbox-participation","zh-TW"): [
   ("沙盒結束後，如何把成果轉化為正式合規能力？",
    "沙盒的價值在於把不確定的監管互動變成可複用的能力。專案收尾時，應把驗證過的模型文件、風險舒緩措施與監控指標固化為正式的模型卡片與上架流程，使後續同類場景可以直接套用，而不必每次都重新走一遍沙盒。同時要把沙盒中建立的回饋通道保留下來，作為持續合規的一部分。監管方通常歡迎這種「從試點到生產」的清晰路徑，因為它降低了系統性風險，也讓企業能夠在獲批範圍內更快擴展創新應用，把一次性的准入優勢轉化為長期可信的營運能力。"),
 ],
 ("retail-fraud-detection-ai","zh-CN"): [
   ("如何衡量零售欺诈检测的投入回报？",
    "衡量回報不能只看拦截金额，还要把误拦造成的真实顾客流失、人工审核成本与品牌信任一并计入。最稳健的做法是用净避免损失（拦截欺诈减去误伤订单的折现损失）除以平台与审核投入，得到可横向比较的投资回报率。建议每月复盘一次阈值与规则，因为促销季与黑产手法变化会快速改变成本结构。当模型在降低欺诈损失的同时把误拦率控制在顾客可感知的低位，零售业务的转化与复购才会同步改善，人工智能欺诈检测的价值才真正落到了损益表上，而不是停留在演示文稿里。"),
 ],
 ("retail-fraud-detection-ai","zh-TW"): [
   ("如何衡量零售诈欺检测的投入回报？",
    "衡量回报不能只看拦截金额，还要把误拦造成的真实顾客流失、人工审核成本与品牌信任一并计入。最稳健的做法是用净避免损失（拦截诈欺减去误伤订单的折现损失）除以平台与审核投入，得到可横向比较的投资报酬率。建议每月复盘一次阈值与规则，因为促销季与黑产手法变化会快速改变成本结构。当模型在降低诈欺损失的同时把误拦率控制在顾客可感知的低位，零售业务的转化与复购才会同步改善，人工智能诈欺检测的价值才真正落到了损益表上，而不是停留在简报里。"),
 ],
 ("mcp-vs-rest-api-vs-graphql-complete-comparison","zh-CN"): [
   ("MCP 与现有 API 网关是什么关系？",
    "MCP 并不取代 API 网关，而是运行在它上层的能力编排层。网关继续负责认证、限流、路由与可观测性这些横向能力，MCP 服务器则把已经受网关保护的接口进一步封装成模型可理解的「工具」。这意味着企业既不必抛弃既有的安全投资，也能让大模型以受控方式调用后台能力。在实践中，治理边界更加清晰：网关团队守住系统级防线，MCP 层定义业务语义与工具权限。当一次调用既经过网关的策略校验，又符合 MCP 的工具授权，组织在获得智能编排灵活性的同时，依然保留了对每一次访问的可审计控制，避免了 AI 原生架构常见的「特权泛化」风险。"),
 ],
 ("mcp-vs-rest-api-vs-graphql-complete-comparison","zh-TW"): [
   ("MCP 與現有 API 閘道是什麼關係？",
    "MCP 並不取代 API 閘道，而是運行在它上層的能力編排層。閘道繼續負責認證、限流、路由與可觀測性這些橫向能力，MCP 伺服器則把已經受閘道保護的介面進一步封裝成模型可理解的「工具」。這意味著企業既不必拋棄既有的安全投資，也能讓大模型以受控方式呼叫後台能力。在實作中，治理邊界更加清晰：閘道團隊守住系統級防線，MCP 層定義業務語意與工具權限。當一次呼叫既經過閘道的策略校驗，又符合 MCP 的工具授權，組織在獲得智慧編排靈活性的同時，依然保留對每一次存取的可審計控制，避免了 AI 原生架構常見的「特權泛化」風險。"),
 ],
 ("data-mesh-vs-data-warehouse-choosing-the-right-architecture","zh-CN"): [
   ("数据网格与数据仓库能否并存而非二选一？",
    "绝大多数成熟企业最终走向的是并存，而非互斥。数据仓库继续承担报表、监管报送与历史归档等需要强一致与集中优化的负载；数据网格则负责把分散在各业务域的运营数据产品化，服务于快速变化的分析与 AI 场景。关键的不是站队，而是用明确的边界划分职责：哪些数据必须集中、哪些数据应当由域自治。借助语义层，两套体系可以共享同一套业务定义，既避免了口径冲突，又保留了各自的性能优势。把这个问题从「谁取代谁」重新定义为「如何分工」，往往能让架构演进更平稳，也让既有投资得到延续，而不是在每一次技术潮流中被推倒重来。"),
 ],
 ("data-mesh-vs-data-warehouse-choosing-the-right-architecture","zh-TW"): [
   ("資料網格與資料倉儲能否並存而非二選一？",
    "絕大多數成熟企業最終走向的是並存，而非互斥。資料倉儲繼續承擔報表、監管報送與歷史歸檔等需要強一致與集中優化的負載；資料網格則負責把分散在各業務域的營運資料產品化，服務於快速變化的分析與 AI 場景。關鍵的不是站隊，而是用明確的邊界劃分職責：哪些資料必須集中、哪些資料應當由域自治。借助語意層，兩套體系可以共享同一套業務定義，既避免了口徑衝突，又保留了各自的效能優勢。把這個問題從「誰取代誰」重新定義為「如何分工」，往往能讓架構演進更平穩，也讓既有投資得到延續，而不是在每一次技術潮流中被推倒重來。"),
 ],
 ("education-personalised-learning-pathways-through-data-a-2026-update","zh-CN"): [
   ("教师与学生在个性化路径中各自的角色是什么？",
    "个性化并不削弱人的作用，而是重新分配角色。教师的角色从统一讲授者转变为路径的设计者与意义的赋予者：他们依据平台建议，结合对个体差异的判断，决定何时加速、何时放慢、何时介入情感支持。学生则从被动接收者变为学习的共同作者，能够在可视化看板中理解自己的进展，并就目标与节奏表达偏好，这种能动性本身就能提升坚持度与成效。技术负责处理重复性的诊断与推荐，人类负责处理动机、关系与价值观这类无法被算法替代的部分。当三者——数据、教师、学生——形成闭环，个性化学习才不再是冷冰冰的适配引擎，而是一套有温度、可问责、持续进化的教与学系统，也更容易在学校的治理框架内获得长期信任与资源支持。"),
 ],
 ("education-personalised-learning-pathways-through-data-a-2026-update","zh-TW"): [
   ("教師與學生在個人化路徑中各自的角色是什麼？",
    "個人化並不削弱人的作用，而是重新分配角色。教師的角色從統一講授者轉變為路徑的設計者與意義的賦予者：他們依據平台建議，結合對個體差異的判斷，決定何時加速、何時放慢、何時介入情感支持。學生則從被動接收者變為學習的共同作者，能夠在視覺化看板中理解自己的進展，並就目標與節奏表達偏好，這種能動性本身就能提升堅持度與成效。技術負責處理重複性的診斷與推薦，人類負責處理動機、關係與價值觀這類無法被演算法替代的部分。當三者——資料、教師、學生——形成閉環，個人化學習才不再是冷冰冰的適配引擎，而是一套有溫度、可問責、持續進化的教與學系統，也更容易在學校的治理框架內獲得長期信任與資源支持。"),
 ],
}

def cjk_count(s): return len(re.findall(r'[\u3400-\u9fff\uf900-\ufaff]', s))
def en_words(s): return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))

for (slug, lang), sections in ADD.items():
    prefix = "" if lang=="en" else lang.lower()+"/"
    p = os.path.join(ROOT, prefix+"blog/articles/"+slug+".html")
    with open(p, encoding='utf-8') as f:
        html = f.read()
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    h1t = re.sub(r'<[^>]+>','',h1.group(1)).strip() if h1 else ""
    block = "".join(sec(h2,b) for h2,b in sections)
    anchor = re.search(r'<section class="faq-section"', html)
    if not anchor:
        print(f"NO FAQ ANCHOR: {slug} {lang}"); continue
    html2 = html[:anchor.start()] + block + html[anchor.start():]
    with open(p, "w", encoding='utf-8') as f:
        f.write(html2)
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html2, re.S)
    body = m.group(1) if m else html2
    if lang=="en":
        print(f"{slug[:40]:40} {lang} +{en_words(block)}w h1ok={h1t[:25]}")
    else:
        print(f"{slug[:40]:40} {lang} +{cjk_count(block)}cjk h1ok={h1t[:15]}")
print("DONE")
