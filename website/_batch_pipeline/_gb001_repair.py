#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repair mangled English fragments left in zh bodies by an earlier automated pass.
Edits the article body region only — <head> is never touched."""
import sys, re
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb001_lib as L

SLUGS = [l.strip() for l in open(L.ROOT + "/_batch_pipeline/gap_batches/gbatch_001.txt") if l.strip()]

# ordered: most specific first
CN = [
 ("AI gent 治理在产品ion已成为", "生产环境中的AI智能体治理已成为"),
 ("AI gent 治理在产品ion举措", "AI智能体治理举措"),
 ("AI gent 治理在产品ion", "AI智能体治理"),
 ("AI gent 评估指标", "AI智能体评估指标"),
 ("AI gent 编排", "AI智能体编排"),
 ("AI gent 组合模式", "AI智能体组合模式"),
 ("AI gent 治理", "AI智能体治理"),
 ("AI gent", "AI智能体"),
 ("产品ion-grde systems", "生产级系统"),
 ("治理在产品ion", "治理"),
 ("using AI 与 saellite da 为 precision 农业", "把AI与卫星数据用于精准农业"),
 ("designing multi-gent systems 为 complex enterprise workflows", "为复杂企业工作流设计多智能体系统"),
 ("mesuring per为mce 超越 simple 准确性 scores", "衡量超越简单准确性的性能表现"),
 ("estblishing 框架与 gurdrils 为 u到nomous AI", "为自主AI建立框架与护栏"),
 ("moving 从 pro到type 到", "从原型走向"),
 ("简化客户 deliverbles 与 AI 自动化", "用AI自动化简化客户交付物"),
 (" antidote是以用例驅動的方法", " 解药是以用例驱动的方法"),
 ("明确AIa收入增长", "明确AI在收入增长"),
 ("使企业级agentic ai处理", "使企业级的智能体AI处理"),
 ("作为专门的安层来检查和过滤LLM", "作为专门的安全层来检查和过滤LLM"),
 ("AI 为自动化客户报告", "面向自动化客户报告的AI"),
]

TW = [
 ("AI gent 治理在产品ion已成为", "生產環境中的AI智慧體治理已成為"),
 ("AI gent 治理在产品ion举措", "AI智慧體治理举措"),
 ("AI gent 治理在产品ion", "AI智慧體治理"),
 ("AI gent 评估指标", "AI智慧體评估指标"),
 ("AI gent 编排", "AI智慧體编排"),
 ("AI gent 组合模式", "AI智慧體组合模式"),
 ("AI gent 治理", "AI智慧體治理"),
 ("AI gent", "AI智慧體"),
 ("产品ion-grde systems", "生產級系統"),
 ("治理在产品ion", "治理"),
 ("using AI 与 saellite da 为 precision 农业", "把AI與衛星資料用於精準農業"),
 ("designing multi-gent systems 为 complex enterprise workflows", "为複雜企業工作流設計多智慧體系統"),
 ("mesuring per为mce 超越 simple 准确性 scores", "衡量超越簡單準確性的效能表現"),
 ("estblishing 框架与 gurdrils 为 u到nomous AI", "为自主AI建立框架與護欄"),
 ("moving 从 pro到type 到", "从原型走向"),
 ("简化客户 deliverbles 与 AI 自動化", "用AI自動化簡化客戶交付物"),
 (" antidote是以用例驅動的方法", " 解藥是以用例驅動的方法"),
 ("明确AIa收入增長", "明确AI在收入增長"),
 ("使企業級agentic ai處理", "使企業級的智慧體AI處理"),
 ("作为專门的安层来檢查和篩選LLM", "作为專門的安全層來檢查和篩選LLM"),
 ("AI 为自動化客户报告", "面向自動化客户报告的AI"),
]

total = 0
for s in SLUGS:
    for lang, pairs in (("zh-CN", CN), ("zh-TW", TW)):
        h = L.read(s, lang)
        m = re.search(r'(<article class="article-content" id="article-content">)(.*?)(</article>)', h, re.S)
        if not m:
            continue
        body = m.group(2)
        orig = body
        for a, b in pairs:
            body = body.replace(a, b)
        if body != orig:
            h = h[:m.start(2)] + body + h[m.end(2):]
            L.write(s, lang, h)
            n = sum(orig.count(a) for a, _ in pairs)
            total += n
            print(f"{lang} {s}: {n} fragment(s) repaired")
print("TOTAL", total)
