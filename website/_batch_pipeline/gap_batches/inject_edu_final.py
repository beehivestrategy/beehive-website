import os, re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def sec(h2, body):
    return f'\n<h2>{h2}</h2>\n<p>{body}</p>\n'

ADD = {
 ("education-personalised-learning-pathways-through-data-a-2026-update","zh-CN"): [
   ("如何让学生真正参与自己的学习路径？",
    "参与感来自可控感与可见的进展。把路径建议用学生能理解的语言呈现，允许他们在安全范围内调整节奏与目标，并及时给出「你为什么被推荐这个」的解释。当学生看到自己的选择带来真实的进步，内在动机就会被激活，个性化也从外部施加变成了自我驱动。"),
 ],
 ("education-personalised-learning-pathways-through-data-a-2026-update","zh-TW"): [
   ("如何讓學生真正參與自己的學習路徑？",
    "參與感來自可控感與可見的進展。把路徑建議用學生能理解的語言呈現，允許他們在安全範圍內調整節奏與目標，並及時給出「你為什麼被推薦這個」的解釋。當學生看到自己的選擇帶來真實的進步，內在動機就會被激活，個人化也從外部施加變成了自我驅動。"),
 ],
}

def cjk_count(s): return len(re.findall(r'[\u3400-\u9fff\uf900-\ufaff]', s))

for (slug, lang), sections in ADD.items():
    prefix = "" if lang=="en" else lang.lower()+"/"
    p = os.path.join(ROOT, prefix+"blog/articles/"+slug+".html")
    with open(p, encoding='utf-8') as f:
        html = f.read()
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    h1t = re.sub(r'<[^>]+>','',h1.group(1)).strip() if h1 else ""
    block = "".join(sec(h2,b) for h2,b in sections)
    anchor = re.search(r'<section class="faq-section"', html)
    if not anchor:
        print(f"NO FAQ ANCHOR: {slug} {lang}"); continue
    html2 = html[:anchor.start()] + block + html[anchor.start():]
    with open(p, "w", encoding='utf-8') as f:
        f.write(html2)
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html2, re.S)
    body = m.group(1) if m else html2
    print(f"{slug[:40]:40} {lang} +{cjk_count(block)}cjk h1ok={h1t[:15]}")
print("DONE")
