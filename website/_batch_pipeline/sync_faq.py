import re,json,sys
CJK=re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
TPL='''                    <div class="faq-item">
                        <h3 class="faq-question-heading" style="margin:0;font-weight:inherit;font-size:inherit;line-height:inherit;"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">{n}</span><span>{q}</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{a}</div></div>
                    </div>'''
def run(path):
    s=open(path,encoding='utf-8').read()
    lds=re.findall(r'(<script type="application/ld\+json">)(.*?)(</script>)',s,re.S)
    faq=[x for x in lds if '"FAQPage"' in x[1]]
    assert len(faq)==1, f"{path}: FAQPage ld count={len(faq)}"
    d=json.loads(faq[0][1]); ents=d["mainEntity"]
    items="\n".join(TPL.format(n=i+1,q=e["name"],a=e["acceptedAnswer"]["text"]) for i,e in enumerate(ents))
    newlist='<div class="faq-list">\n'+items+'\n                </div>'
    s2,n1=re.subn(r'<div class="faq-list">.*?</div>\s*</section>', newlist+'\n            </section>', s, count=1, flags=re.S)
    assert n1==1, "accordion replace failed"
    # remove duplicate in-article faq block
    s3,n2=re.subn(r'\n\s*<div class="faq-section">.*?</div>\s*\n', '\n\n', s2, count=1, flags=re.S)
    assert n2==1, f"in-article faq remove failed {path}"
    open(path,'w',encoding='utf-8').write(s3)
    print(f"OK {path} faqQ={len(ents)}")
for p in sys.argv[1:]:
    run(p)
