import os, re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def sec(h2, body):
    return f'\n<h2>{h2}</h2>\n<p>{body}</p>\n'

ADD = {
 ("education-personalised-learning-pathways-through-data-a-2026-update","zh-CN"): [
   ("如何在资源受限的学校启动个性化学习？",
    "资源从来不是一次到位的，关键是先用最小可行闭环证明价值。从单一学科、一个年级开始，先把成绩与作业数据打通，跑出可被教师直接使用的路径建议，而不是急于建设覆盖全校的庞大平台。优先选择那些数据基础好、教师意愿强的班级作为试点，用可见的成效去争取更多的预算与行政支持。对于算力与工具不足的情况，可以先借助轻量级的规则与统计方法，再逐步引入更复杂的模型。更重要的是把教师专业学习社群纳入其中，让早期采用者成为内部布道者。当第一所学校用有限资源跑通了「数据—建议—教师确认—学生进步」的循环，扩张就不再是技术问题，而是已被验证、可被复制的运营方法。"),
 ],
 ("education-personalised-learning-pathways-through-data-a-2026-update","zh-TW"): [
   ("如何在資源受限的學校啟動個人化學習？",
    "資源從來不是一次到位的，關鍵是先以最小可行閉環證明價值。從單一學科、一個年級開始，先把成績與作業資料打通，跑出可被教師直接使用的路徑建議，而不是急於建設覆蓋全校的龐大平台。優先選擇那些資料基礎好、教師意願強的班級作為試點，用可見的成效去爭取更多的預算與行政支持。對於算力與工具不足的情況，可以先借助輕量級的規則與統計方法，再逐步引入更複雜的模型。更重要的是把教師專業學習社群納入其中，讓早期採用者成為內部布道者。當第一所學校用有限資源跑通了「資料—建議—教師確認—學生進步」的循環，擴張就不再是技術問題，而是已被驗證、可被複製的營運方法。"),
 ],
 ("mcp-vs-rest-api-vs-graphql-complete-comparison","zh-CN"): [
   ("选型时最常见的误区是什么？",
    "最大的误区是把三种协议看作互相替代的零和选择，于是在组织层面强制统一为一种。事实上，它们各自擅长不同的边界：REST 适合稳定的资源读写，GraphQL 适合前端主导的聚合查询，MCP 适合把能力暴露给模型与智能体。强行用一种协议去覆盖所有场景，往往会导致接口臃肿或语义错位。更成熟的实践是让团队按场景选用，并用网关与语义层把它们编织在一起，使调用方无需关心底层实现。另一个误区是低估治理成本——任何协议一旦暴露给大模型，都必须配套权限、审计与回退策略，否则便利会迅速演变为风险。把选型当作架构决策而非时尚追逐，才能让每一层协议都落在它真正高效的边界之内。"),
 ],
 ("mcp-vs-rest-api-vs-graphql-complete-comparison","zh-TW"): [
   ("選型時最常見的誤區是什麼？",
    "最大的誤區是把三種協議看作互相替代的零和選擇，於是在組織層面強制統一為一種。事實上，它們各自擅長不同的邊界：REST 適合穩定的資源讀寫，GraphQL 適合前端主導的聚合查詢，MCP 適合把能力暴露給模型與智慧體。強行用一種協議去覆蓋所有場景，往往會導致介面臃腫或語意錯位。更成熟的實作是讓團隊按場景選用，並用閘道與語意層把它們編織在一起，使呼叫方無需關心底層實作。另一個誤區是低估治理成本——任何協議一旦暴露給大模型，都必須配套權限、審計與回退策略，否則便利會迅速演變為風險。把選型當作架構決策而非時尚追逐，才能讓每一層協議都落在它真正高效的邊界之內。"),
 ],
 ("data-mesh-vs-data-warehouse-choosing-the-right-architecture","zh-CN"): [
   ("团队规模较小时是否应该直接上数据网格？",
    "对小规模团队而言，数据网格常常是一种过早的组织复杂度。当一个中央平台团队就能高效响应大部分需求时，强行划分领域所有权反而会增加协调与治理开销，让本该快速交付的分析陷入流程泥潭。更务实的路径是：先以数据仓库或湖仓统一承载，同时在内部用清晰的数据契约与产品化思维组织数据集，为未来的域拆分预留边界。当业务线增多、数据消费方变得多元、中心团队开始成为瓶颈时，再逐步把高价值域提升为自治的数据产品。也就是说，网格是一种与组织规模相匹配的演进结果，而不是起点的默认答案。按节奏引入，才能在享受自治红利的同时，避免为用不上的灵活性付出过高的管理代价。"),
 ],
 ("data-mesh-vs-data-warehouse-choosing-the-right-architecture","zh-TW"): [
   ("團隊規模較小時是否應該直接上資料網格？",
    "對小規模團隊而言，資料網格常常是一種過早的組織複雜度。當一個中央平台團隊就能高效回應大部分需求時，強行劃分領域所有權反而會增加協調與治理開銷，讓本該快速交付的分析陷入流程泥潭。更務實的路徑是：先以資料倉儲或湖倉統一承載，同時在內部用清晰的資料契約與產品化思維組織資料集，為未來的域拆分預留邊界。當業務線增多、資料消費方變得多元、中心團隊開始成為瓶頸時，再逐步把高價值域提升為自治的資料產品。也就是說，網格是一種與組織規模相匹配的演進結果，而不是起點的預設答案。按節奏引入，才能在享受自治紅利的同時，避免為用不上的靈活性付出過高的管理代價。"),
 ],
}

def cjk_count(s): return len(re.findall(r'[\u3400-\u9fff\uf900-\ufaff]', s))

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
    print(f"{slug[:40]:40} {lang} +{cjk_count(block)}cjk h1ok={h1t[:15]}")
print("DONE")
