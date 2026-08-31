# -*- coding: utf-8 -*-
import re, os
import opencc

base = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = "what-is-conversational-bi-chatbi-explained"
cc = opencc.OpenCC('s2twp.json')

NEW_H2 = '''
<h2 id="对话式bi与传统仪表盘有何不同">对话式BI与传统仪表盘BI有何不同？</h2>
<p>传统BI依赖预先构建的仪表盘与报表：业务人员必须从固定视图中寻找答案，或向数据团队提交需求、等待数日。对话式BI把这一关系颠倒——用户用自然语言直接提问，系统即时生成查询、返回答案与可视化。差别不在&#x201C;能不能看图&#x201D;，而在&#x201C;谁掌控提问&#x201D;：仪表盘由报表设计者预设问题，ChatBI由提问者实时定义问题。</p>
<p>这种转变的实际意义是决策速度的跃升。当一位区域经理在晨会上被问到&#x201C;为什么华南毛利下滑&#x201D;，他不再需要等到下午的数据提取，而是当场追问并拿到可追溯的答案。蜂启咨询的对话式BI把语义层作为唯一真相来源，确保无论是仪表盘还是对话，返回的都是同一口径的数字——一致性正是组织信任平台的前提。对企业而言，真正的收益不是少点几次鼠标，而是把&#x201C;提问到决策&#x201D;的循环从天压缩到分钟。</p>
<p>需要澄清的是，对话式BI并不会取代仪表盘，而是补足它：例行监控仍由仪表盘承载，而临时的、跨维度的&#x201C;为什么&#x201D;类追问，交给对话。两者共用同一语义层，正是企业避免数字口径分裂、防止&#x201C;同一个指标三套数&#x201D;的关键，也是蜂启咨询在每次部署中首先夯实的部分。</p>'''

LINK_MOBILE = '<a href="#对话式bi与传统仪表盘有何不同" class="toc-mobile-link">对话式BI与传统仪表盘BI有何不同？</a>'
LINK_SIDEBAR = '<a href="#对话式bi与传统仪表盘有何不同" class="toc-link">对话式BI与传统仪表盘BI有何不同？</a>'

zh_p = base + "/zh-cn/blog/articles/" + slug + ".html"
h = open(zh_p, encoding='utf-8').read()
# insert new H2 before AUTOEXPAND-START
marker = '<!--AUTOEXPAND-START-->'
assert marker in h
h = h.replace(marker, NEW_H2 + "\n" + marker, 1)
# add TOC links
h = h.replace('class="toc-mobile-link">总结与关键建议</a>', 'class="toc-mobile-link">总结与关键建议</a>\n                    ' + LINK_MOBILE, 1)
h = h.replace('class="toc-link">总结与关键建议</a>', 'class="toc-link">总结与关键建议</a>\n                    ' + LINK_SIDEBAR, 1)
open(zh_p, 'w', encoding='utf-8').write(h)

# regenerate zh-TW
zhcn = open(zh_p, encoding='utf-8').read()
m = re.search(r'<main>.*</main>', zhcn, re.S)
tw_main = cc.convert(m.group(0))
tw_main = tw_main.replace('/zh-cn/', '/zh-tw/').replace('zh-cn/', 'zh-tw/').replace('预约演示', '預約示範')
zhtw = open(base + "/zh-tw/blog/articles/" + slug + ".html", encoding='utf-8').read()
zhtw = re.sub(r'<main>.*</main>', tw_main, zhtw, flags=re.S)
open(base + "/zh-tw/blog/articles/" + slug + ".html", 'w', encoding='utf-8').write(zhtw)
print("slug9 done")
