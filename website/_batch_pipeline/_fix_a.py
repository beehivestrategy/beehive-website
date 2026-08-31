import re, os

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = open(os.path.join(ROOT, "_batch_pipeline/batches/batch_007.txt"), encoding="utf-8").read().split()

def path(lang, slug):
    if lang == "en": return os.path.join(ROOT, f"blog/articles/{slug}.html")
    return os.path.join(ROOT, f"{lang}/blog/articles/{slug}.html")

# ---------- 1) H2 question conversion (all 54) ----------
qmark = {"en":"?", "zh-cn":"？", "zh-tw":"？"}
h2_re = re.compile(r'(<h2[^>]*id="[^"]*"[^>]*>)(.*?)(</h2>)', re.S)

def conv_h2(h, lang):
    def repl(m):
        pre, txt, post = m.group(1), m.group(2), m.group(3)
        t = re.sub(r'<[^>]+>', '', txt).strip()
        if t.endswith('?') or t.endswith('？'):
            return m.group(0)
        # append question mark to the heading text
        newtxt = txt.rstrip()
        # avoid double punctuation
        if newtxt.endswith(('。','.','!','！')):
            newtxt = newtxt[:-1]
        return pre + newtxt + qmark[lang] + post
    return h2_re.sub(repl, h)

# ---------- 2) FAQ + JSON-LD for the 2 bare slugs ----------
FAQ = {
 "federated-learning-for-privacy-preserving-enterprise-ai": {
  "en": [
    ("What is federated learning and why does it matter for enterprise privacy?",
     "Federated learning trains models across distributed datasets that never leave their owners' control, sharing only encrypted model updates. It matters because it lets enterprises build AI on data that regulation or competitiveness forbids centralising."),
    ("Does federated learning fully guarantee privacy on its own?",
     "No. Model updates can leak information through gradients, so production systems combine federated learning with differential privacy and secure aggregation, and document a clear threat model before deployment."),
    ("Where should an enterprise start with federated learning?",
     "Start with a real problem that centralised training cannot solve because data cannot move, write the threat model first, run a small pilot federation to calibrate the privacy-accuracy trade-off, then institutionalise the federation as a durable capability."),
  ],
  "zh-cn": [
    ("什么是联邦学习，它为何对企业隐私如此重要？",
     "联邦学习在永不离开数据拥有方控制范围的数据集上训练模型，只共享加密后的模型更新。它的重要性在于，企业可以基于那些受监管或出于竞争考量而无法集中的数据来构建人工智能。"),
    ("联邦学习本身就能完全保证隐私吗？",
     "不能。模型更新可能通过梯度泄露信息，因此生产系统会将联邦学习与差分隐私和安全聚合结合使用，并在部署前形成清晰的威胁模型文档。"),
    ("企业应从何处着手开展联邦学习？",
     "从中央化训练因数据无法移动而无法解决的真实问题入手，先编写威胁模型，运行一个小型试点联邦来校准隐私与准确率的权衡，再将联邦能力建设成可持续的能力。"),
  ],
  "zh-tw": [
    ("什麼是聯邦學習，它為何對企業隱私如此重要？",
     "聯邦學習在永不離開資料擁有方控制範圍的資料集上訓練模型，只共享加密後的模型更新。它的重要性在於，企業可以基於那些受監管或出於競爭考量而無法集中的資料來建構人工智慧。"),
    ("聯邦學習本身就能完全保證隱私嗎？",
     "不能。模型更新可能透過梯度洩露資訊，因此生產系統會將聯邦學習與差分隱私和安全聚合結合使用，並在部署前形成清晰的威脅模型文件。"),
    ("企業應從何處著手開展聯邦學習？",
     "從中央化訓練因資料無法移動而無法解決的真實問題入手，先編寫威脅模型，運行一個小型試點聯邦來校準隱私與準確率的權衡，再將聯邦能力建構成可持續的能力。"),
  ],
 },
 "multi-lingual-analytics-supporting-global-teams": {
  "en": [
    ("What is multi-lingual analytics and why do global teams need it?",
     "It is the ability to query, model, and visualise enterprise data across languages and locales from one governed layer, so regional teams work in their own language while leadership sees a consistent picture."),
    ("How do you keep metrics consistent across languages and regions?",
     "A single semantic layer defines each metric once and serves it through localised labels and formats, so a revenue figure means the same thing whether a user asks in English, Simplified Chinese, or Traditional Chinese."),
    ("What are the biggest pitfalls in multi-lingual analytics deployments?",
     "The main pitfalls are translating dashboards without governing definitions, mixing locales in one dataset, and ignoring encoding or right-to-left issues; all are avoided with a governed semantic layer and explicit locale handling."),
  ],
  "zh-cn": [
    ("什么是多语言分析，全球团队为何需要它？",
     "多语言分析是指从统一且受治理的层面，跨语言和地区查询、建模并可视化企业数据，让区域团队用自己熟悉的语言工作，同时让管理层看到一致的全貌。"),
    ("如何在不同语言和地区之间保持指标一致？",
     "统一的语义层对每个指标只定义一次，并通过本地化的标签与格式提供服务，因此无论用户使用英文、简体中文还是繁体中文提问，收入数字的含义都完全相同。"),
    ("多语言分析落地时最大的陷阱是什么？",
     "主要陷阱包括只翻译仪表盘却不治理定义、在同一数据集中混淆地区，以及忽视编码或从右到左的排版问题；这些都可以通过受治理的语义层和明确的地区处理来避免。"),
  ],
  "zh-tw": [
    ("什麼是多語言分析，全球團隊為何需要它？",
     "多語言分析是指從統一且受治理的層面，跨語言和地區查詢、建模並視覺化企業資料，讓區域團隊用自己熟悉的語言工作，同時讓管理層看到一致的全貌。"),
    ("如何在不同語言和地區之間保持一致的指標？",
     "統一的語義層對每個指標只定義一次，並透過本地化的標籤與格式提供服務，因此無論使用者使用英文、簡體中文還是繁體中文提問，收入數字的含義都完全相同。"),
    ("多語言分析落地時最大的陷阱是什麼？",
     "主要陷阱包括只翻譯儀表板卻不治理定義、在同一資料集中混淆地區，以及忽視編碼或從右到左的排版問題；這些都可以透過受治理的語義層和明確的地區處理來避免。"),
  ],
 },
}

def faq_html(qa):
    items = []
    for i,(q,a) in enumerate(qa,1):
        items.append(f'''                    <div class="faq-item">
                        <button class="faq-question" aria-expanded="false">
                            <h3 class="faq-question-text"><span class="faq-number">{i}</span>{q}</h3>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{a}</div></div>
                    </div>''')
    inner = "\n".join(items)
    return f'''            <section class="faq-section" id="faq" aria-label="Frequently Asked Questions">
                <h2 class="faq-section-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                    Frequently Asked Questions
                </h2>
                <div class="faq-list">
{inner}
                </div>
'''

def faq_jsonld(qa):
    me = []
    for q,a in qa:
        me.append('    {\n      "@type": "Question",\n      "name": '+repr(q)+',\n      "acceptedAnswer": {\n        "@type": "Answer",\n        "text": '+repr(a)+'\n      }\n    }')
    body = ",\n".join(me)
    return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
''' + body + '''
  ]
}
</script>'''

for slug in slugs:
    for lang in ("en","zh-cn","zh-tw"):
        p = path(lang, slug)
        if not os.path.exists(p): 
            print("MISSING", p); continue
        h = open(p, encoding="utf-8").read()
        orig = h
        # H2 conversion
        h = conv_h2(h, lang)
        # bare-slug FAQ insertion
        if slug in FAQ and 'class="faq-section"' not in h:
            qa = FAQ[slug][lang]
            block = faq_html(qa) + faq_jsonld(qa) + "</section>"
            # insert before article-nav
            anchor = '<nav class="article-nav"'
            if anchor in h:
                h = h.replace(anchor, block + "\n\n            " + anchor, 1)
            else:
                # fallback: before recommended-section
                h = h.replace('<section class="recommended-section"', block + "\n\n" + '<section class="recommended-section"', 1)
        if h != orig:
            open(p,"w",encoding="utf-8").write(h)
            print(f"{lang} {slug}: updated")
print("DONE A")
