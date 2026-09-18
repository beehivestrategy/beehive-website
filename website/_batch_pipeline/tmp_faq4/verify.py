# -*- coding: utf-8 -*-
import re, os, json, html
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
paths=[l.strip() for l in open(os.path.join(ROOT,"_batch_pipeline/wo_faq_4.txt"),encoding="utf-8") if l.strip()]
CJK=re.compile(r'[\u4e00-\u9fff]')
PROTECT=("BI","ROI","SaaS","RAG","LLM","MCP","ETL","API","CRM","KPI","Dashboard")
def txt(s):
    s=re.sub(r'<[^>]+>','',s); s=html.unescape(s); return re.sub(r'\s+',' ',s).strip()
fails=[]; nq_total=0
for p in paths:
    src=open(os.path.join(ROOT,p),encoding="utf-8").read()
    b=os.path.join(ROOT,"_batch_pipeline/tmp_faq4/backup",os.path.basename(p))
    ob=open(b,encoding="utf-8").read() if os.path.exists(b) else src
    iss=[]
    # ① undefined
    if 'undefined' in src: iss.append("undefined残留 x%d"%src.count('undefined'))
    # ② 纯英文 h2/h3
    for m in re.finditer(r'<(h2|h3)\b[^>]*>(.*?)</\1>', src, re.S):
        t=txt(m.group(2))
        if t and not CJK.search(t): iss.append("EN-H:%s"%t)
    # ③ FAQ 可见 vs JSON-LD
    m=re.search(r'<div class="faq-list">(.*?)\n\s*</div>\s*</section>', src, re.S)
    if not m: iss.append("找不到faq-list"); fails.append((p,iss)); continue
    parts=re.split(r'<div class="faq-item">', m.group(1))[1:]
    vis_q=[];vis_a=[]
    for blk in parts:
        qm=re.search(r'class="faq-question-text"[^>]*>(.*)$', blk, re.S)
        qinner=qm.group(1)
        q=re.sub(r'<span class="faq-number">\d+</span>\s*','',qinner)
        q=txt(re.split(r'</span>|</h3>', q)[0])
        vis_q.append(q)
        am=re.search(r'faq-answer-inner">(.*?)</div>', blk, re.S)
        vis_a.append(txt(am.group(1)) if am else None)
    names=[];texts=[]
    for mm in re.finditer(r'<script type="application/ld\+json"[^>]*>((?:(?!</script>).)*)</script>', src, re.S):
        try: j=json.loads(mm.group(1))
        except Exception as e: iss.append("LD解析失败:%s"%e); continue
        st=[j] if isinstance(j,dict) else j
        for o in st:
            if isinstance(o,dict) and o.get("@type")=="FAQPage":
                for x in o.get("mainEntity",[]):
                    names.append(x.get("name")); texts.append(x["acceptedAnswer"]["text"])
    if len(vis_q)!=4: iss.append("可见FAQ=%d"%len(vis_q))
    if names!=vis_q: iss.append("Q不一致 vis=%s ld=%s"%(vis_q,names))
    if texts!=vis_a: iss.append("A不一致")
    for a in vis_a:
        if not a or not(60<=len(re.sub(r'\s','',a))<=110): iss.append("答案字数=%s"%len(a or ''))
    if len(set(vis_q))!=4: iss.append("问题重复")
    nq_total+=len(vis_q)
    # ④ div 差一致
    d1=len(re.findall(r'<div\b',src))-len(re.findall(r'</div>',src))
    d0=len(re.findall(r'<div\b',ob))-len(re.findall(r'</div>',ob))
    if d1!=d0: iss.append("div差 %d->%d"%(d0,d1))
    # 附加
    if re.search(r'&lt;(div|span|h2|h3)\b', src): iss.append("标签被转义")
    nums=re.findall(r'faq-number">(\d+)</span>', src)
    if nums!=['1','2','3','4']: iss.append("编号:%s"%nums)
    if iss: fails.append((p,iss))
print("可见问答总数:",nq_total," FAILS:",len(fails))
for p,i in fails: print(p); [print("   ",x) for x in i]
