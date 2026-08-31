#!/usr/bin/env python3
import re, sys, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
LATIN = re.compile(r'[A-Za-z]+')
TRAD = set('萬與專業叢東絲丟兩嚴喪個豐臨為麗舉麼義烏樂喬習鄉書買亂乾亂爭虧亞產畝親褻嚲億僅僕從侖倉儀們價眾優會傘偉傳傷倫偽佇佈體佔併來侖俠係促俄俁儉俗俘保倉信個倍倒倖倘候倚俱倡們值傾假偌偉側偵偶偷傭償傀傅備傑傘傭傳僅傾傷價儀儂億儀儉儈儉儐償儕儘儔儖儼償儷儸儺儻兒兀允兌兗黨內兩冊寫軍農冠冢冤冥冪冬沖決況冶凍准凈涼凜幾凡凱擊函鑿刀刁刍分切刈刊刍包匆匍匏匕匯匱區協華協卑賣南博卜占卡盧鹵臥衛卻廠厘厚原厠厥廈廚厲壓厭厴庫廁廂廄廈廚廝廩廬廳參叉發叔取受敘叟叢口句叫召叮可台叼史右叼號司叻叼吁吃各合吉吊吋同名后吏吐向吒嚇君吶吝吞吟吠吡吳呆呈呂呆呃呀吵吶吸吹吻吼吾呀呆呈呂呃呀吶味呵咄咕咖呣呸咭咦咧咨咪咫哞哩哦哪哭哮哲哺哼哽唇唉唐唑唔啊唉唄員哥哦哩哪哭哮哲哺哼哽唇唉唐唑唔啊唉唄員哥哦哩哪哭哺哼哽唇唉唐唑唔啊唉唄員哥哦唕唧唬售唯唱唳唷唸唷唺啡啃啄商啊問啕啞啟啡啃啄商啊問啡啃啄商啊問啡啃啄商啊問啡啃啄商啊問啡啃啄商啊問啡啃啄商啊問啡啃啄商啊問啡啃啄商啊問啡啃啄商啊問啡啃啄商啊問啡啃啄商啊問啡啃啄商啊問')
SIMP = set('万与专业丛东丝丢两严丧个丰临为丽举么义乌乐乔习乡书买乱干乱争亏亚产亩亲亵亸亿仅仆从仑仓仪们价众优会伞伟传伤伦伪伫布体占并来仑侠系促俄俣俭俗俘保仓信个倍倒幸倘候倚俱倡们值倾假偌伟侧侦偶偷佣偿傀傅备杰伞佣传仅倾伤价仪侬亿仪俭侩俭傧偿侪尽俦傩俪俪俨俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪俪')

def body_of(path):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', s, re.S)
    if not m:
        m = re.search(r'<article[^>]*>(.*?)</article>', s, re.S)
    return (m.group(1) if m else ''), s

def strip_tags(html):
    html = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    html = re.sub(r'<style.*?</style>', ' ', html, flags=re.S)
    html = re.sub(r'<!--.*?-->', ' ', html, flags=re.S)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&[a-z]+;', ' ', html)
    return html

def audit(slug):
    out = []
    for lang, prefix in [('EN', 'blog'), ('CN', 'zh-cn/blog'), ('TW', 'zh-tw/blog')]:
        p = os.path.join(ROOT, prefix, 'articles', slug + '.html')
        if not os.path.exists(p):
            out.append(f'{lang}: MISSING'); continue
        body, full = body_of(p)
        text = strip_tags(body)
        cjk = len(CJK.findall(text)); words = len(LATIN.findall(text))
        title = re.search(r'<title>(.*?)</title>', full, re.S)
        title = title.group(1).strip() if title else ''
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', full, re.S)
        h1 = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else ''
        # title corruption check
        t_cjk = len(CJK.findall(title)); t_lat = len(LATIN.findall(title))
        corrupt = ''
        if lang == 'EN' and t_cjk > 0: corrupt = 'TITLE_HAS_CJK'
        if lang in ('CN','TW'):
            if t_cjk == 0: corrupt = 'TITLE_NO_CJK'
            mixed = bool(re.search(r'[\u4e00-\u9fff]\s*[A-Za-z]{3,}|[A-Za-z]{3,}\s*[\u4e00-\u9fff]', title))
            if mixed: corrupt = (corrupt + '+MIXED') if corrupt else 'TITLE_MIXED'
        h2s = [re.sub(r'<[^>]+>', '', h).strip() for h in re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)]
        faqsec = 'faq-section' in body
        faq_qs = re.findall(r'<h3 class="faq-question-text"[^>]*>.*?<span>(.*?)</span>', body, re.S)
        if not faq_qs:
            faq_qs = [re.sub(r'<[^>]+>', '', h).strip() for h in re.findall(r'<h3[^>]*>(.*?)</h3>', body, re.S)]
        ld_count = len(re.findall(r'"@type"\s*:\s*"FAQPage"', full))
        # recommended hrefs
        recs = re.findall(r'<a class="recommended-card"[^>]*href="([^"]*)"', full)
        exp = {'EN': '/blog/articles/', 'CN': '/zh-cn/blog/articles/', 'TW': '/zh-tw/blog/articles/'}[lang]
        bad_rec = [r for r in recs if not r.startswith(exp)]
        cta_ok = 'article-cta-btn' in full
        phrase = {'EN': 'Book a Demo', 'CN': '预约演示', 'TW': '預約示範'}[lang]
        phrase_ok = phrase in full
        out.append(f'{lang}: w={words} cjk={cjk} h2={len(h2s)} faqsec={int(faqsec)} faqQ={len(faq_qs)} ld={ld_count} rec={len(recs)} badrec={len(bad_rec)} cta={int(cta_ok)}/{int(phrase_ok)} {corrupt}')
        out.append(f'    title={title!r}')
        out.append(f'    h1={h1!r}')
        out.append(f'    h2s={h2s}')
    return '\n'.join(out)

if __name__ == '__main__':
    for slug in [l.strip() for l in open(sys.argv[1]) if l.strip()]:
        print('==== ' + slug)
        print(audit(slug))
