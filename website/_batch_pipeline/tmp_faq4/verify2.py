# -*- coding: utf-8 -*-
import re, os, json, html
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
paths=[l.strip() for l in open(os.path.join(ROOT,"_batch_pipeline/wo_faq_4.txt"),encoding="utf-8") if l.strip()]
CJK=re.compile(r'[\u4e00-\u9fff]')
def txt(s): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',s)).strip()
bad=[]
EN_LEGIT={"MCP","2025","AI ROI","BI","ROI","SaaS","RAG","LLM","ETL","API","CRM","KPI","Dashboard"}
for p in paths:
    src=open(os.path.join(ROOT,p),encoding="utf-8").read()
    iss=[]
    # div/span/h2/h3 平衡
    for tag in ("div","span","h2","h3","section","button"):
        o=len(re.findall(r'<%s\b'%tag,src)); c=len(re.findall(r'</%s>'%tag,src))
        if o!=c: iss.append("%s %d/%d"%(tag,o,c))
    # 任务B：可见英文卡片分类
    for m in re.finditer(r'recommended-card-cat">([^<]*)<',src):
        if m.group(1) and not CJK.search(m.group(1)): iss.append("EN-CAT:%s"%m.group(1))
    # 任务C：英文标签（仅允许白名单）
    for m in re.finditer(r'article-tag-pill">([^<]*)<',src):
        t=m.group(1)
        if t and not CJK.search(t) and t not in EN_LEGIT: iss.append("EN-TAG:%s"%t)
    # 标题唯一 & 长度
    hs=[txt(m.group(2)) for m in re.finditer(r'<(h[23])\b[^>]*>(.*?)</\1>',src,re.S)]
    hs=[h for h in hs if h]
    if len(hs)!=len(set(hs)): iss.append("标题重复")
    for h in hs:
        if len(h)>20: iss.append("标题过长(%d):%s"%(len(h),h))
    # 其它残留英文（可见文本节点，长度>3且全为ASCII字母）
    body=re.sub(r'<(script|style)\b.*?</\1>','',src,flags=re.S)
    for m in re.finditer(r'>([^<>]{4,})<',body):
        t=m.group(1).strip()
        if re.fullmatch(r'[A-Za-z][A-Za-z0-9 &\-\'’:/\.]{3,}',t) and t not in EN_LEGIT:
            iss.append("EN-TEXT:%r"%t)
    if iss: bad.append((p,iss))
print("FAILS",len(bad))
for p,i in bad:
    print(p.split('/')[-1]); [print("   ",x) for x in dict.fromkeys(i)]
