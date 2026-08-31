# -*- coding: utf-8 -*-
import re, os
import opencc
cc = opencc.OpenCC('s2twp')
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = "what-is-rag-retrieval-augmented-generation"

# Chinese (Simplified) appendix sections to append before the FAQ section
cn_append = '''
<h2 id="how-to-measure-rag-effectiveness">企业如何衡量 RAG 系统的效果？</h2>
<p>RAG 的可信度必须被量化，而不能靠感觉。领先的组织从第一天起就追踪三个指标：答案忠实度（回答是否可由检索到的来源证实）、引用准确率（所引来源是否真的支撑了结论）、以及检索召回率（相关文档是否确实被召回）。这些指标应对照一份带标注的小问题集来计算，并在每次知识库更新后重跑。一个无法证明自己答案的部署，无论听起来多流畅，都还没达到生产就绪。</p>
<h2 id="rag-and-data-governance">RAG 与数据治理如何协同？</h2>
<p>检索的质量上限由数据治理的质量决定。访问控制必须在检索阶段强制执行，这样用户只会看到被授权的内容；而数据质量——去重、主数据管理、清晰的指标定义——决定了检索回来的上下文是否可信。在 Beehive Strategy 的对话式 BI 中，这套控制骑在语义层与数据层之上，使得 grounding 既准确又可审计，而不是依赖提示词里的临时约束。</p>
<h2 id="rag-security-compliance">部署 RAG 时有哪些安全与合规考量？</h2>
<p>因为 RAG 把企业数据拉进模型的上下文，数据边界就是安全边界。涉及个人数据或受监管内容的语料，应在检索前做脱敏与分类，并保留完整的访问日志以备审计。对受监管行业而言，可追溯的引用同时满足了合规与信任：当监管者问"这个回答依据什么"时，系统应能回放到具体的来源记录。把 RAG 当作受治理技术栈中的一层来对待，才能让它在风控严格的环境中落地。</p>
'''

tw_append = cc.convert(cn_append)

for lang, ap in (("zh-cn", cn_append), ("zh-tw", tw_append)):
    p = os.path.join(ROOT, "%s/blog/articles/%s.html"%(lang, slug))
    h = open(p, encoding='utf-8').read()
    if '<section class="faq-section"' not in h:
        raise SystemExit("no faq anchor in "+p)
    # insert appendix right before the faq-section
    h = h.replace('<section class="faq-section"', ap + '\n            <section class="faq-section"', 1)
    open(p, 'w', encoding='utf-8').write(h)
    print("wrote", p)

for lang, ap in (("zh-cn", cn_append), ("zh-tw", tw_append)):
    p = os.path.join(ROOT, "%s/blog/articles/%s.html"%(lang, slug))
    h = open(p, encoding='utf-8').read()
    b = re.search(r'<article class="article-content" id="article-content">(.*?)</article>', h, re.S).group(1)
    print(lang, "total cjk=", len(re.findall(r'[\u4e00-\u9fff]', b)), "faq=", b.count('faq-item'), "jsonld=", 'FAQPage' in h, "css=", h.count('article.css?v=20260826'), "js=", h.count('article.js?v=20260826'), "footer=", h.count('footer class="footer"'))
