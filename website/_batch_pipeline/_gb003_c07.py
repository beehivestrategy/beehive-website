#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 slug 07 — ai-data-privacy-enterprise-balancing-innovation"""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import process, stats
from opencc import OpenCC
_T2S = OpenCC('t2s')
from _gb001_s2t import s2tw

SLUG = 'ai-data-privacy-enterprise-balancing-innovation'

EN_RENAMES = {
    'The Global AI Regulatory Landscape':
        'What Does the Global AI Regulatory Landscape Require?',
    'Building a Compliant AI Program':
        'How Do You Build a Compliant AI Program?',
    'Cross-Border Data and AI Compliance':
        'How Should Cross-Border Data Compliance Be Handled?',
    'Preparing for Future Regulation':
        'How Do You Prepare for Regulation That Has Not Landed Yet?',
}

EN_INSERTS = [
    ('Which Privacy-Enhancing Techniques Actually Work in Enterprise AI?',
     'which-privacy-enhancing-techniques-actually-work-in-enterprise-ai',
     '<p>Gartner has predicted that by 2026, 60 percent of AI projects will use privacy-enhancing technologies, up from less than 5 percent in 2023. That projection is only useful if the techniques are chosen for the threat they actually address, because each one protects something different and costs something different.</p>'
     '<ul>'
     '<li><strong>Pseudonymisation and tokenisation.</strong> Replace direct identifiers with reversible tokens held in a separate, tightly controlled store. Cheap, effective against casual exposure in logs and analytics, and insufficient on its own — re-identification through quasi-identifiers remains possible.</li>'
     '<li><strong>Aggregation and k-anonymity thresholds.</strong> Suppress any result that describes fewer than k individuals. This is the single highest-value control for conversational analytics, because it prevents an apparently innocuous question from returning a one-person answer.</li>'
     '<li><strong>Differential privacy.</strong> Add calibrated statistical noise so that an individual record cannot be inferred from outputs. Appropriate for published statistics and model training at scale; it costs accuracy, so it belongs where aggregate release is the goal, not in operational reporting.</li>'
     '<li><strong>Federated learning.</strong> Train where the data lives and move only model updates. Powerful for genuinely distributed or locality-bound data, and heavy to operate — justified when data cannot move legally, not as a default.</li>'
     '<li><strong>Confidential computing and encryption in use.</strong> Protect data while it is being processed, which closes the gap that encryption at rest and in transit leaves open. Increasingly available from major cloud providers and worth requiring for the highest-sensitivity workloads.</li>'
     '<li><strong>Synthetic data.</strong> Useful for testing, development, and sharing with vendors, and dangerous as a privacy guarantee unless formally evaluated, because generative models can memorise and reproduce training records.</li>'
     '</ul>'
     '<p>The practical pattern is layering: minimise first, then pseudonymise, then enforce suppression thresholds at the query layer, then apply encryption and access control around whatever remains. Most privacy incidents in AI systems are not cryptographic failures; they are over-collection and over-broad retrieval, both of which minimisation solves before any advanced technique is needed.</p>'),

    ('How Does Privacy by Design Change an AI Architecture?',
     'how-does-privacy-by-design-change-an-ai-architecture',
     '<p>Privacy by design is an architectural commitment, not a review step. It changes four specific parts of the stack, and the changes are visible in the design document rather than the compliance report.</p>'
     '<ol>'
     '<li><strong>Data minimisation at ingestion.</strong> The pipeline collects only the fields each declared use case needs, with a documented justification per field. Fields without a justification are not ingested, which reduces the exposure surface before any control is applied.</li>'
     '<li><strong>Purpose limitation encoded in metadata.</strong> Every dataset carries the purposes for which it may be used, and the query layer enforces them. A dataset marked for service improvement cannot be pulled into a marketing model, not because a reviewer said so but because the access layer refuses the request.</li>'
     '<li><strong>Access control enforced where data lives.</strong> Identity, role, and jurisdiction filters are applied at the data and retrieval layers, so an AI system inherits the same entitlements as the person asking. This is also what prevents the most common AI privacy failure: an assistant retrieving records its user could never open directly.</li>'
     '<li><strong>Accountability by default.</strong> Every interaction between an AI system and personal data is logged — who asked, what was read, which policy applied, what was returned — so a demonstration of compliance is a query rather than a reconstruction project.</li>'
     '</ol>'
     '<p>Two consequences follow. First, privacy stops being a gate at the end of the project: because the constraints are in the architecture, compliant use cases move faster, not slower. Second, the controls become reusable — each new AI use case inherits them, so the marginal compliance cost of the next deployment approaches zero while the cost for competitors rebuilding case by case stays where it was.</p>'),

    ('What Should a Cross-Border AI Data Strategy Cover?',
     'what-should-a-cross-border-ai-data-strategy-cover',
     '<p>Multinationals face a patchwork: GDPR in Europe, PIPL with its localisation and transfer conditions in China, sector rules in financial services and health, and a shifting set of US state frameworks. More than 80 percent of multinationals must comply with two or more AI regulatory frameworks simultaneously, and the practical problem is that "compliant" means different things in each.</p>'
     '<p>The workable strategy has four parts. Map the flows first: where personal data is collected, where it is stored, where models are trained, and where inference happens — most organisations discover inference and logging paths they never documented. Then classify by jurisdiction and sensitivity, and decide which workloads must stay local; training a model in one region and serving it in another is a very different legal question from shipping raw records across a border. Then choose a transfer mechanism per flow — standard contractual clauses, adequacy decisions, certification, or explicit consent — and record the choice against the flow rather than in a policy document. Finally, enforce locality technically: region-pinned storage, region-pinned model endpoints, and retrieval filters that prevent a query served in one jurisdiction from reaching data held in another.</p>'
     '<p>The pattern that fails is treating cross-border compliance as a legal exercise with an engineering afterthought. The pattern that works is the reverse: make the jurisdiction of every dataset a machine-readable attribute, and let the access layer enforce it. Legal then reviews a small number of enforceable rules instead of auditing hundreds of applications.</p>'),
]

EN_FAQ = [
    ('Can innovation and privacy really coexist in enterprise AI?',
     'Yes, and privacy by design is the mechanism. When privacy requirements enter the AI architecture as first-class constraints — data minimisation, purpose limitation, access control enforced where data lives, and accountability logging — privacy and performance stop being a trade-off. Systems built this way collect less data, retrieve less broadly, and produce answers that are easier to defend, which is also better engineering: the most common AI privacy failures are over-collection and over-broad retrieval, not weak cryptography.'),
    ('Which privacy regulations matter most for enterprise AI?',
     'Four shape most programmes. The EU GDPR sets the baseline for personal data protection, with fines up to 20 million euros or 4 percent of global turnover. The EU AI Act adds binding obligations for high-risk AI systems that process personal data. China\'s PIPL requires localisation for certain personal information and imposes strict conditions on cross-border transfer, with penalties up to 50 million RMB or 5 percent of prior-year revenue. The United States is moving from sector-specific rules toward broader state-level frameworks with intensifying enforcement. Most multinationals must satisfy two or more of these simultaneously.'),
    ('What is the single most effective privacy control for conversational AI?',
     'Suppression thresholds at the query layer. Any result that describes fewer than k individuals is withheld, which prevents an innocuous-sounding question — "what is the average bonus in the Zurich office?" — from returning a one-person answer. Combined with access control that makes the assistant inherit the permissions of the person asking, it addresses the two failure modes that actually occur: inadvertent disclosure through aggregation, and retrieval of records the requester could never open directly.'),
    ('How should cross-border data flows be handled for AI training and inference?',
     'Map the flows first, including inference and logging paths that are usually undocumented. Classify by jurisdiction and sensitivity, then decide which workloads must remain local — training in one region and serving in another is a materially different legal question from transferring raw records. Select a transfer mechanism per flow, such as standard contractual clauses or adequacy decisions, and record it against that specific flow. Then enforce locality technically through region-pinned storage and endpoints, so compliance is a property of the architecture rather than a promise in a policy.'),
    ('How do you prepare for AI regulation that has not taken effect yet?',
     'Build to the strictest applicable standard and keep the evidence. Concretely: maintain a live inventory of AI systems and the data they can reach; keep purpose and retention metadata machine-readable so rules can be changed without re-architecture; log every AI-to-data interaction so compliance can be demonstrated on demand; and design controls to be swappable, because specific technical requirements will change while the underlying obligations — minimisation, purpose limitation, accountability — do not. Organisations that can produce evidence quickly spend less on every future compliance cycle.'),
]

ZH_RENAMES = {
    '当前格局与关键趋势': '全球AI监管格局对企业提出了哪些要求？',
    '实施框架与最佳实践': '如何在AI架构中落实隐私设计？',
    '衡量影响与展示价值': '如何衡量隐私投入与创新的平衡？',
    '克服常见挑战': '平衡隐私与创新时最常见的挑战是什么？',
    '中国市场特有的实施优势': '中国市场在隐私合规落地上的优势是什么？',
    '规模化推广的关键成功因素': '规模化推广隐私合规能力的关键是什么？',
}

TW_RENAMES = {
    'Building a Compliant AI Program': '如何打造合規的AI專案體系？',
    'Cross-Border Data and AI Compliance': '跨境數據與AI合規該如何處理？',
    'Preparing for Future Regulation': '尚未生效的法規該如何提前準備？',
    '常見問題': '常見問題',
    '規模化推廣的關鍵成功因素': '規模化推廣隱私合規能力的關鍵是什麼？',
    '技術基礎設施與實施考量': '技術基礎設施與實施上有哪些考量？',
    '中國市場特有的實施優勢': '華語市場在隱私合規落地上的優勢是什麼？',
}

ZH_FAQ = [
    ('在企業AI中，創新與隱私真的可以共存嗎？',
     '可以，而實現機制就是"隱私設計"。當隱私要求在架構階段就作為一等約束進入AI系統——數據最小化、目的限制、在數據所在位置執行訪問控制、以及完整的責任留痕——隱私與性能就不再是一對取捨。按這種方式構建的系統採集更少數據、檢索範圍更窄、答案更容易辯護，而這本身也是更好的工程實踐：AI系統中最常見的隱私事故來自過度採集與過寬的檢索，而不是加密不夠強。'),
    ('哪些隱私法規對企業AI影響最大？',
     '多數企業的合規體系由四部法規塑造。歐盟GDPR設定了個人數據保護的基線，罰則最高可達2000萬歐元或全球營業額的4%。歐盟《AI法案》對處理個人數據的高風險AI系統增加了強制義務。中國《個人信息保護法》對部分個人信息要求本地化存儲，並對跨境傳輸設定嚴格條件，罰則最高可達5000萬元人民幣或上一年度營業額的5%。美國則正從行業性規則轉向更廣泛的州級框架，執法力度持續加強。多數跨國企業需要同時滿足其中兩部以上。'),
    ('對話式AI最有效的隱私控制是什麼？',
     '在查詢層設置抑制閾值。任何描述個體數量少於k人的結果都應被拒絕返回，這能防止一個聽起來無害的問題——"蘇黎世辦公室的平均獎金是多少？"——返回實質上指向某一個人的答案。再配合讓助手繼承提問者權限的訪問控制，就能覆蓋兩類真正會發生的失效模式：聚合查詢導致的非故意披露，以及檢索到提問者本人無權直接打開的記錄。'),
    ('AI訓練與推理中的跨境數據流應該如何處理？',
     '先繪製數據流圖，包括通常沒有被記錄的推理與日誌路徑。再按司法轄區與敏感度分類，確定哪些工作負載必須留在本地——在一個地區訓練模型再到另一個地區提供服務，與直接跨境傳輸原始記錄是完全不同的法律問題。然後為每條數據流選擇傳輸機制（標準合同條款、充分性認定等），並把選擇記錄到具體的數據流上，而不是寫在政策文件裡。最後用區域固定的存儲與服務端點在技術上強制落實，讓合規成為架構的屬性，而不是文件中的承諾。'),
    ('如何為尚未生效的AI法規提前做準備？',
     '按適用的最嚴格標準建設，並持續保留證據。具體包括：維護一份實時更新的AI系統清單，記錄它們能夠訪問哪些數據；把用途與留存期限做成機器可讀的元數據，使規則調整不需要重構架構；記錄每一次AI與數據的交互，以便在需要時隨時出示合規證明；讓控制措施可替換，因為具體的技術要求會變，而最小化、目的限制、問責這些底層義務不會變。能夠快速出示證據的企業，在未來每一次合規週期中的成本都更低。'),
]


def run():
    b = {lg: stats(SLUG, lg) for lg in ('en', 'zh-cn', 'zh-tw')}
    process(SLUG, 'en', h2_renames=EN_RENAMES, inserts=EN_INSERTS, faq=EN_FAQ, drop_body_faq=True)
    ZH_FAQ_CN = [(_T2S.convert(q), _T2S.convert(a)) for q, a in ZH_FAQ]
    process(SLUG, 'zh-cn', h2_renames=ZH_RENAMES, faq=ZH_FAQ_CN)
    process(SLUG, 'zh-tw', h2_renames=TW_RENAMES, faq=[(s2tw(q), s2tw(a)) for q, a in ZH_FAQ_CN],
            drop_body_faq=True)
    for lg in ('en', 'zh-cn', 'zh-tw'):
        print(lg, b[lg], '->', stats(SLUG, lg))


if __name__ == '__main__':
    run()
