import os, re
ROOT="/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

TW_H2={
 "2025-in-review-enterprise-ai-pilot-to-production":{
   "Conversational BI Became the Primary Interface":"How Did Conversational BI Become the Primary Interface?",
   "China and Asia-Pacific Led Enterprise AI Adoption":"Why Did China and Asia-Pacific Lead Enterprise AI Adoption?",
   "Looking Ahead to 2026":"What Should Enterprises Expect as They Look Ahead to 2026?",
   "規模化推廣的關鍵成功因素":"規模化推廣有哪些關鍵成功因素？",
   "技術基礎設施與實施考量":"技術基礎設施與實施需考量哪些重點？",
   "中國市場特有的實施優勢":"中國市場有哪些特有的實施優勢？",
 },
 "2025-year-review-enterprise-ai-transformation":{
   "核心收益與投資回報考量":"企業 AI 轉型能帶來哪些核心收益與投資回報？",
   "實施路線圖與後續步驟":"企業應如何規劃 AI 轉型的實施路線圖與後續步驟？",
   "案例分析與行業洞察":"有哪些值得借鑑的案例分析與行業洞察？",
   "未來展望與行動建議":"面向未來企業應採取哪些行動建議？",
   "關鍵成功因素與常見陷阱":"企業 AI 轉型有哪些關鍵成功因素與常見陷阱？",
   "蜂啟諮詢的專業洞察":"蜂啟諮詢對此有哪些專業洞察？",
 },
 "2026-outlook-enterprise-ai-strategy":{
   "核心收益與投資回報考量":"2026 年企業 AI 戰略能帶來哪些核心收益與投資回報？",
   "實施路線圖與後續步驟":"企業應如何規劃 2026 年的實施路線圖與後續步驟？",
   "案例分析與行業洞察":"有哪些值得借鑑的案例分析與行業洞察？",
   "未來展望與行動建議":"面向 2026 年企業應採取哪些行動建議？",
   "關鍵成功因素與常見陷阱":"2026 年企業 AI 戰略有哪些關鍵成功因素與常見陷阱？",
   "蜂啟諮詢的專業洞察":"蜂啟諮詢對此有哪些專業洞察？",
 },
}
TW_EXCERPTS={
 "2025-in-review-enterprise-ai-pilot-to-production":[
   "回顧 2025 年企業 AI 如何從孤立試點走向生產級平台。",
   "為何平台化 AI——連接器、語義層、IM 原生交付——勝過一次性試點專案。",
 ],
 "2025-year-review-enterprise-ai-transformation":[
   "2025 年企業 AI 轉型如何從試點走向生產的年度回顧。",
 ],
 "2026-outlook-enterprise-ai-strategy":[
   "2026 年企業 AI 戰略展望：主權資料、多模型編排與即時分析。",
 ],
}

def conv_h2(t, h2map):
    idmap={}
    def repl(m):
        pre, inner, post = m.group(1), m.group(2), m.group(3)
        txt=re.sub(r'<[^>]+>','',inner).strip()
        if txt in h2map:
            new=h2map[txt]; mm=re.search(r'id="([^"]+)"', pre)
            if mm: idmap[mm.group(1)]=new
            return pre+new+post
        return m.group(0)
    t2=re.sub(r'(<h2[^>]*>)(.*?)(</h2>)', repl, t, flags=re.S)
    for hid,new in idmap.items():
        t2=re.sub(r'(<a [^>]*href="#'+re.escape(hid)+r'"[^>]*>)(.*?)(</a>)',
                  lambda mm: mm.group(1)+new+mm.group(3), t2, flags=re.S)
    return t2

def fill_excerpts(t, excerpts):
    i=[0]
    def repl(m):
        if i[0]<len(excerpts):
            v=excerpts[i[0]]; i[0]+=1
            return '<p class="recommended-card-excerpt">'+v+'</p>'
        return m.group(0)
    return re.sub(r'<p class="recommended-card-excerpt"></p>', repl, t)

for slug in TW_H2:
    p=os.path.join(ROOT,"zh-tw/blog/articles/"+slug+".html")
    t=open(p,encoding='utf-8').read()
    t=conv_h2(t, TW_H2[slug])
    t=fill_excerpts(t, TW_EXCERPTS.get(slug,[]))
    open(p,'w',encoding='utf-8').write(t)
    print("fixed tw", slug)
