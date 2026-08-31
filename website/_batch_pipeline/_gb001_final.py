#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final compliance check for gbatch_001."""
import sys, os, re, json, html as ihtml
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb001_lib as L

ROOT = L.ROOT
SLUGS = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]
PHRASE = {"en": "Book a Demo", "zh-CN": "预约演示", "zh-TW": "預約示範"}
PREFIX = {"en": "/blog/articles/", "zh-CN": "/zh-cn/blog/articles/", "zh-TW": "/zh-tw/blog/articles/"}
BAD = ["Lorem", "TODO", "TBD", "coming soon", "占位", "待补充", "{{", "lorem ipsum"]

fails = []
for s in SLUGS:
    row = [s]
    for lang in ("en", "zh-CN", "zh-TW"):
        h = L.read(s, lang)
        problems = []
        # 1 length
        m = L.metric(h, lang)
        floor = 2500 if lang == "en" else 3500
        if m < floor:
            problems.append(f"LEN {m}<{floor}")
        # 2 faq section + h3 count
        fs = re.search(r'<section class="faq-section".*?</section>', h, re.S)
        if not fs:
            problems.append("NOFAQ")
        else:
            h3 = re.findall(r'<h3[^>]*>(.*?)</h3>', fs.group(0), re.S)
            if len(h3) < 3:
                problems.append(f"H3={len(h3)}")
            answers = re.findall(r'<div class="faq-answer-inner">(.*?)</div>', fs.group(0), re.S)
            if len(answers) != len(h3):
                problems.append(f"QA mismatch {len(h3)}/{len(answers)}")
            page_qa = [(re.sub(r'<[^>]+>', '', q).strip(), re.sub(r'<[^>]+>', '', a).strip())
                       for q, a in zip(h3, answers)]
            # 3 JSON-LD right after FAQ must match
            tail = h[fs.end():]
            lm = re.search(r'<script type="application/ld\+json">\s*(\{.*?"FAQPage".*?\})\s*</script>', tail, re.S)
            if not lm:
                problems.append("LD_NOT_AFTER_FAQ")
            else:
                try:
                    obj = json.loads(lm.group(1))
                    ld_qa = [(x["name"], x["acceptedAnswer"]["text"]) for x in obj["mainEntity"]]
                    if len(ld_qa) < 3:
                        problems.append(f"LD_N={len(ld_qa)}")
                    if [(ihtml.unescape(a), ihtml.unescape(b)) for a, b in ld_qa] != page_qa:
                        problems.append("LD_MISMATCH")
                except Exception as e:
                    problems.append("LD_INVALID")
        # 4 CTA
        cm = re.search(r'<a[^>]*class="article-cta-btn"[^>]*>(.*?)</a>', h, re.S)
        if not cm or PHRASE[lang] not in cm.group(1):
            problems.append("CTA")
        # 5 recommended hrefs
        for href in L.rec_hrefs(h):
            if not href.startswith(PREFIX[lang]):
                problems.append(f"HREF {href}")
        # 6 placeholders
        for b in BAD:
            if b.lower() in L.body_of(h).lower():
                problems.append(f"PLACEHOLDER:{b}")
        # 7 stray latin words in zh
        if lang != "en":
            body = re.sub(r'<script.*?</script>', ' ', L.body_of(h), flags=re.S)
            txt = re.sub(r'<[^>]+>', ' ', body)
            words = set(re.findall(r'\b[A-Za-z]{4,}\b', txt))
            words -= {"MCP", "LangGraph", "CrewAI", "AutoGen", "LlamaIndex", "Semantic", "Kernel",
                      "Microsoft", "Teams", "WhatsApp", "DingTalk", "WeChat", "Gartner", "McKinsey",
                      "Sentinel", "NDVI", "LangChain", "Blackboard", "Autonomous", "Router",
                      "Orchestrator", "Workers", "Hierarchical", "Pipeline", "Golden", "PDF",
                      "ERP", "API", "ROI", "token", "APAC", "executive", "sponsor", "Team", "GPU",
                      "Docker", "Kubernetes", "ONNX", "OpenTelemetry", "Google", "Drive", "Excel",
                      "Harvest", "HubSpot", "Jira", "Slack", "Agent", "Orchestration", "PyTorch",
                      "TensorFlow", "HuggingFace", "Pinecone", "Milvus", "Weaviate", "Qdranta",
                      "Istio", "Linkerd", "Sentinel", "ETL", "CTO", "NLP", "LLM", "Agents", "TCO",
                      "Monday", "NetSuite", "Notion", "Python", "Salesforce", "SharePoint", "Workday",
                      "Toggl", "Xero"}
            if words:
                problems.append("EN_IN_ZH:" + ",".join(sorted(words)[:6]))
        row.append(f"{lang} {m} {'OK' if not problems else ' | '.join(problems)}")
    if any("OK" not in c.split(" ", 2)[2] for c in row[1:]):
        fails.append(s)
    print(" :: ".join(row))
print("\nSLUGS WITH ISSUES:", len(fails), fails)
