#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 11: designing-natural-language-interfaces-for-enterprise-data
EN 1394 -> ~2600 ; CN/TW 1978 -> ~3600 ; build FAQ ; H2 -> questions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_by_text, build_faq, s2t_fixed

SLUG = "designing-natural-language-interfaces-for-enterprise-data"
NAV = '            <nav class="article-nav" aria-label="Article navigation">'

EN_NEWS = """<h2 id="how-should-the-interface-handle-ambiguity">How Should the Interface Handle Ambiguity in Business Language?</h2>
<p>Enterprise questions are ambiguous in ways that consumer queries are not, and the ambiguity usually sits in the business vocabulary rather than in the grammar. "Revenue" might mean booked, recognised, or collected. "Last quarter" might mean the fiscal or the calendar quarter. "Active customer" has a definition that differs between the product, finance, and sales teams, and each team is convinced theirs is the obvious one. A natural language interface that resolves these silently produces confidently wrong answers; one that asks about all of them produces a conversation tree that users abandon.</p>
<p>The design that works separates ambiguity into two classes. Resolvable ambiguity — where one interpretation is overwhelmingly likely given the user's role, history, and phrasing — should be resolved silently, with the assumption stated in the answer: "Revenue (recognised, calendar Q3)." Unresolvable ambiguity — where two interpretations are genuinely plausible and produce materially different numbers — earns exactly one clarifying question with concrete options drawn from the semantic layer, not an open-ended prompt. The dividing line is a confidence threshold, and the threshold should be tuned per metric, because finance definitions are worth asking about and headcount counts usually are not.</p>
<p>The semantic layer is what makes both halves work. When "active customer" has one governed definition with a named owner, most ambiguity disappears before it reaches the user, and the remaining cases are few enough that a single clarifying question is not annoying. This is why evaluating a natural language interface is largely an evaluation of the semantic layer behind it: interfaces built over well-governed models ask far fewer questions and are right far more often, without any change to the language model itself.</p>
<h2 id="what-does-multilingual-handling-require">What Does Multilingual Question Handling Require?</h2>
<p>In any enterprise operating across regions, the same question arrives in several languages and in mixed form — an English metric name inside a Chinese sentence, or a pinyin abbreviation for a product line. Treating this as a translation problem produces a fragile system: translate first, then parse, and every translation error becomes a query error that is hard to reproduce. The more robust design resolves to a canonical internal question representation, so that a Chinese phrasing and an English phrasing of the same request map to the same semantic request regardless of surface language.</p>
<p>The practical requirements follow from that design. Entity resolution must be multilingual — product names, region names, and customer segments need aliases in every language in use, maintained as data rather than as prompt engineering. Number, date, and unit parsing must be locale-aware, because a quarter must resolve identically whether written as Q3 or as the local equivalent, and because a date written as 10/12 means different things in different markets. And the answer must be returned in the language of the question, including the narrative rationale, since a user who asked in Chinese and received an English explanation has not really been answered.</p>
<p>Two failure modes are worth designing against. The first is the silent language switch, where a mixed-language question causes the interface to answer in the wrong language — jarring, but easy to fix with an explicit language policy. The second is more damaging: a term that exists in one language's business vocabulary but not another's, which causes the interface to guess rather than ask. Maintaining the semantic layer's terminology in every supported language, and flagging gaps as coverage items rather than letting the model improvise, is what keeps a multilingual deployment trustworthy.</p>
<h2 id="how-do-you-design-for-governed-access">How Do You Design for Governed Access and Permissions?</h2>
<p>A natural language interface is a new front door to the data estate, and it must enforce the same permissions as every existing door — which is harder than it sounds, because the question is expressed in business language while permissions are expressed in rows, columns, and roles. The design rule is that permissions are resolved at the semantic layer, never in the generated query. The interface should not generate SQL that filters by user role; it should query a governed model that already knows what the asking user may see. Otherwise every new question type becomes a potential permission bypass, and the audit story becomes unanswerable.</p>
<p>Three behaviours follow. The interface must answer as the authenticated user, propagating identity from the channel — Teams, WeChat Work, Slack, or the browser — through to the data layer, so that a question asked in a shared chat returns only what that user may see. It must fail closed and informatively: a clear statement that the user lacks access to a given dataset is far better than an empty result or a generic error, because it tells the user whether to request access or ask a different question. And it must log the question, the resolved semantic request, the data returned, and the user, because that log is the evidence base for access reviews and for any subsequent investigation.</p>
<p>The governance payoff is real but requires one discipline: permissions must be defined once and inherited everywhere. If row-level security is configured separately for the dashboard tool, the export path, and the conversational interface, those three configurations will diverge within a year, and the conversational layer will become either the most or the least permissive door in the estate — usually discovered at the worst possible time.</p>
"""

ZH_NEWS = """<h2 id="界面应如何处理业务语言的歧义">界面应当如何处理业务语言中的歧义？</h2>
<p>企业场景中的问题在歧义方式上与消费级查询不同，而且歧义通常出现在业务词汇里，而不是语法里。营收可能指已签约、已确认或已回款。上季度可能指财季，也可能指自然季度。活跃客户在产品、财务与销售三个团队里各有一套定义，而每个团队都坚信自己那套才是显然的那一套。一个静默消解这些歧义的自然语言界面，会产出自信的错误答案；而一个对每处歧义都发问的界面，则会造出一棵用户会放弃的对话树。</p>
<p>奏效的设计把歧义分成两类。可消解歧义——在给定用户角色、历史与问法的前提下，某种解释压倒性地更可能——应当静默消解，并在答案中说明所采用的假设，例如注明采用的是已确认口径与自然年第三季度。不可消解歧义——两种解释都真正说得通，且会产生实质性不同的数字——才配得上一次澄清提问，并且要提供来自语义层的具体选项，而不是开放式追问。两者的分界是一个置信度阈值，且这个阈值应当按指标逐一调整，因为财务口径值得追问，而人数统计通常不值得。</p>
<p>语义层正是让这两半都成立的基础。当活跃客户只有一个带具名负责人的受治理定义时，大部分歧义在到达用户之前就消失了，剩下的少数情形少到一次澄清提问并不令人厌烦。正因如此，对一个自然语言界面的评估，很大程度上是对其背后语义层的评估：架构在治理良好的模型之上的界面，提问次数少得多、正确率高得多，而语言模型本身一点都不用改。</p>
<h2 id="多语言问题处理需要什么">多语言问题处理需要什么？</h2>
<p>在任何跨区域经营的企业里，同一个问题会以多种语言、以及混合形式出现——中文句子里夹着英文指标名，或者用拼音缩写指代某条产品线。把它当成翻译问题来处理，会产出一个脆弱的系统：先翻译再解析，则每一个翻译错误都会变成一个难以复现的查询错误。更稳健的设计是解析到一个统一的内部问题表示，使同一请求的中英文两种表述映射到同一个语义请求，而不论表层语言是什么。</p>
<p>实际操作要求随之而来。实体解析必须是多语言的——产品名、区域名、客户分层都需要在每种在用语言下备好别名，并且作为数据来维护，而不是靠提示词工程。数字、日期与单位的解析必须感知区域惯例，因为一个季度无论写成 Q3 还是本地写法都必须解析出相同结果，而写成 10/12 的日期在不同市场代表不同的日子。此外，答案必须以提问所用的语言返回，包括叙述性解释在内，因为一个用中文提问却收到英文推理说明的用户，其实并没有被回答。</p>
<p>有两种失败模式值得针对性设计。其一是静默语言切换——混合语言的问题导致界面用错误的语言回答，这很突兀，但用一个显式的语言策略就能修好。其二是更具破坏性的：某个术语只存在于一种语言的业务词汇里，界面于是猜测而不是提问。把语义层的术语在每种受支持语言下都维护好，并把缺口标记为覆盖待办、而不是让模型即兴发挥，才是多语言部署保持可信的关键。</p>
<h2 id="如何为受治理的访问与权限做设计">如何为受治理的访问与权限做设计？</h2>
<p>自然语言界面是通往数据资产体系的一扇新门，它必须执行与所有既有门相同的权限——这比听起来更难，因为问题是用业务语言表达的，而权限是用行、列与角色表达的。设计规则是：权限在语义层解析，绝不在生成的查询里解析。界面不应生成按用户角色过滤的 SQL，而应当查询一个已经知道提问用户可见范围的受治理模型。否则每一种新的问题类型都可能成为一次权限绕过，而审计的故事也就变得无法回答。</p>
<p>三项行为随之而来。界面必须以已认证用户的身份作答，把身份从渠道——Teams、企业微信、Slack 或浏览器——一路透传到数据层，使得在共享群聊里提出的问题，只返回该用户有权看到的内容。它必须以关闭并告知的方式失败：明确说明用户无权访问某类数据，远好于返回一个空结果或一句笼统报错，因为它告诉用户应该去申请权限，还是换个问法。它还必须记录问题、解析后的语义请求、返回的数据以及用户身份，因为这份日志是权限评审与任何后续调查的证据基础。</p>
<p>治理上的回报是真实的，但需要一条纪律：权限必须一次定义、处处继承。如果行级安全在仪表板工具、导出通道与对话式界面上各配一套，这三套配置会在一年内发散，而对话层将变成整个体系里最宽松或最严格的那扇门——而这一发现通常出现在最糟糕的时刻。</p>
"""

EN_FAQ = [
    ("What makes a natural language interface for enterprise data different from a chatbot?",
     "An enterprise data interface is a decision tool, not a conversation partner. It optimises for the fewest turns to a correct answer, exposes the query and filters behind every response, enforces the same row-level permissions as any other data tool, and states its uncertainty rather than guessing. A chatbot is judged on how pleasant the exchange is; a data interface is judged on whether the number can be defended in a meeting."),
    ("How do you handle ambiguous business terms such as revenue or active customer?",
     "Resolve them in the semantic layer, not in the model. Give each term one governed definition with a named owner, so most ambiguity disappears before it reaches the user. Where two interpretations remain genuinely plausible and produce different numbers, ask exactly one clarifying question with concrete options — and state the assumption in the answer whenever you resolve silently."),
    ("Should the interface show the generated SQL to users?",
     "Show the logic, in the vocabulary the user understands. For most business users that means the metric, the filters, the date range, and the source — not raw SQL. For analysts, exposing the SQL is valuable and cheap. The principle is that a user should be able to see why an answer came out the way it did, and spot a wrong filter at a glance."),
    ("How accurate does the interface need to be?",
     "Accurate on your own questions, not on public benchmarks. Published text-to-SQL benchmarks exceed 90% on clean schemas, but enterprise schemas are messier and use jargon no benchmark contains. Build a corpus of real questions your users ask, score answers against ground truth, and track the trend — a system that improves weekly is more valuable than one with a fixed static accuracy."),
    ("How do you keep a natural language interface secure?",
     "Resolve permissions at the semantic layer rather than in generated queries, propagate the authenticated user's identity from the channel through to the data, fail closed with an informative message when access is denied, and log every question, resolved request, and result. Define permissions once and let every interface inherit them, so configurations cannot diverge over time."),
]

CN_FAQ = [
    ("面向企业数据的自然语言界面与聊天机器人有什么不同？",
     "企业数据界面是决策工具，而不是对话伙伴。它优化的是用最少的轮次得到正确答案，会暴露每个回答背后的查询与过滤条件，执行与其他数据工具相同的行级权限，并陈述自身的不确定性而不是猜测。聊天机器人以交互是否愉快为评判标准；数据界面的评判标准则是这个数字能否在会议上站得住。"),
    ("像营收、活跃客户这类歧义业务术语应当如何处理？",
     "在语义层消解它们，而不是交给模型。给每个术语一个有具名负责人的受治理定义，让大部分歧义在到达用户之前就消失。当确实存在两种都说得通、且会产生不同数字的解释时，只提一个澄清问题并给出具体选项；而在静默消解的情况下，必须在答案中说明所采用的假设。"),
    ("界面应当向用户展示生成的 SQL 吗？",
     "要展示的是逻辑，而且要用用户能理解的词汇。对多数业务用户来说，这意味着指标、过滤条件、日期区间与数据来源，而不是原始 SQL。对分析师而言，暴露 SQL 既有用又不昂贵。原则是：用户应当能看出答案为何是现在这样，并能一眼发现一个错误的过滤条件。"),
    ("界面需要多高的准确率才够用？",
     "要在你自己的问题上准确，而不是在公开基准上准确。已发布的文本转 SQL 基准在干净的数据结构上已超过九成，但企业的数据结构更混乱，且包含基准里没有的行话。建立一个由用户真实提问构成的语料库，对照真实答案打分，并跟踪趋势——一个每周都在改进的系统，比一个准确率固定不变的系统更有价值。"),
    ("如何保证自然语言界面的安全性？",
     "在语义层解析权限，而不是在生成的查询里解析；把已认证用户的身份从渠道一路透传到数据层；在无访问权限时以关闭并告知的方式失败；并记录每一个问题、解析后的请求与返回结果。权限只定义一次，让所有界面继承，配置才不会随时间发散。"),
]

EN_H2 = [
    ("Principle 1: Optimise for Speed, Not Conversation",
     "Why Should You Optimise for Speed Rather Than Conversation?"),
    ("Principle 2: Show Your Work", "Why Must the Interface Show Its Work?"),
    ("Principle 3: Choose the Right Response Format",
     "How Should the Interface Choose a Response Format?"),
    ("Principle 4: Handle the 'I Don't Know' Gracefully",
     "How Should the Interface Handle Not Knowing?"),
    ("Key Takeaways", "What Are the Key Takeaways?"),
    ("Conclusion", "Where Should You Start?"),
]
CN_H2 = [
    ("原则 1：优化速度而不是对话", "为什么应当优化速度而不是对话？"),
    ("原则 2：展示你的作品", "为什么界面必须展示它的推理过程？"),
    ("原则 3：选择正确的响应格式", "界面应当如何选择响应格式？"),
    ('原则 4：优雅地处理"我不知道"', "界面应当如何优雅地处理不知道的情况？"),
    ("要点", "核心要点是什么？"),
    ("结论", "应当从哪里开始？"),
]
TW_H2 = [
    ("原則 1：優化速度而不是對話", "爲什麼應當優化速度而不是對話？"),
    ("原則 2：展示你的作品", "爲什麼介面必須展示它的推理過程？"),
    ("原則 3：選擇正確的響應格式", "介面應當如何選擇響應格式？"),
    ('原則 4：優雅地處理"我不知道"', "介面應當如何優雅地處理不知道的情況？"),
    ("要點", "核心要點是什麼？"),
    ("結論", "應當從哪裏開始？"),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    assert h.count(NAV) == 1
    h = h.replace(NAV, "\n" + EN_NEWS + "\n" + build_faq(EN_FAQ, "en") + "\n" + NAV)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body + FAQ done")

    cn = path_of(SLUG, "cn")
    h = open(cn, encoding="utf-8").read()
    assert h.count(NAV) == 1
    h = h.replace(NAV, "\n" + ZH_NEWS + "\n" + build_faq(CN_FAQ, "cn") + "\n" + NAV)
    open(cn, "w", encoding="utf-8").write(h)
    print("CN body + FAQ done")

    tw = path_of(SLUG, "tw")
    h = open(tw, encoding="utf-8").read()
    assert h.count(NAV) == 1
    tw_faq = [(s2t_fixed(q), s2t_fixed(a)) for q, a in CN_FAQ]
    h = h.replace(NAV, "\n" + s2t_fixed(ZH_NEWS) + "\n" + build_faq(tw_faq, "tw") + "\n" + NAV)
    open(tw, "w", encoding="utf-8").write(h)
    print("TW body + FAQ done")

    for old, new in EN_H2:
        retitle_by_text(en, old, new)
    for old, new in CN_H2:
        retitle_by_text(path_of(SLUG, "cn"), old, new)
    for old, new in TW_H2:
        retitle_by_text(path_of(SLUG, "tw"), old, new)
    print("H2s converted in en/cn/tw")
