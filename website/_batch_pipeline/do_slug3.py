# -*- coding: utf-8 -*-
import re, os
import opencc

base = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = "computer-vision-quality-assurance"
cc = opencc.OpenCC('s2twp.json')

# On-topic prose only; existing FAQ section + head JSON-LD are preserved.
ZH_PROSE = '''<div class="toc-mobile" id="toc-mobile">
                <button class="toc-mobile-toggle" aria-expanded="false">目录 <svg class="toc-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
                <div class="toc-mobile-links">
                    <a href="#understanding-the-current-landscape" class="toc-mobile-link">你应如何理解当前的视觉QA格局？</a>
                    <a href="#key-principles-and-strategic-framework" class="toc-mobile-link">关键原则与战略框架是什么？</a>
                    <a href="#implementation-approach-and-best-practices" class="toc-mobile-link">哪些实施方法与最佳实践有效？</a>
                    <a href="#why-do-vision-qa-projects-fail-in-manufacturing" class="toc-mobile-link">为什么视觉QA项目在制造业会失败？</a>
                    <a href="#measuring-success-and-demonstrating-roi" class="toc-mobile-link">你如何衡量成功并展示ROI？</a>
                    <a href="#common-pitfalls-and-how-to-avoid-them" class="toc-mobile-link">常见的陷阱有哪些，如何避免？</a>
                    <a href="#how-to-get-started-with-ai-visual-inspection" class="toc-mobile-link">如何开始AI视觉检测？</a>
                    <a href="#key-takeaways" class="toc-mobile-link">关键要点</a>
                    <a href="#conclusion" class="toc-mobile-link">结论</a>
                </div>
            </div>
<p class="article-lead">计算机视觉正悄然成为生产线上质量保证的标准工具：AI驱动的视觉检测系统现在能发现人类检测员遗漏的缺陷，以人类无法匹敌的速度，并以已降至中型企业也能采用的价格点。&#x201C;AI视觉检测准备好上工厂车间了吗？&#x201D;的简短答案是肯定的——但前提是，它用正确的缺陷数据训练、与产线集成而非外挂、并像它所检测的设备一样被严格监控。</p>
<h2 id="understanding-the-current-landscape">你应如何理解当前的视觉QA格局？</h2>
<p>制造业质量的经济学从未像现在这样有利于自动化。McKinsey Global Institute估计，制造与供应链中的AI应用每年可产生1.2万亿到2万亿美元的经济影响，而视觉检测是该估计中最成熟的用例之一。机器视觉市场随之扩张：MarketsandMarkets预计其到2027年将增长到约192亿美元，由半导体、汽车、电子和消费品生产商驱动。</p>
<p>自动化在工厂车间本身也在加速。国际机器人联合会报告，2022年全球安装了约55.3万台工业机器人，当时创纪录，而每条产线都需要验证其产出。传统方法——人工检测员的目视检查，或为每零件手工调参的基于规则的视觉系统——难以跟上更高的吞吐、更小的缺陷容差，以及过于复杂、无法用简单阈值规则处理的零件。</p>
<p>能力差距现在站在技术一边。深度学习视觉模型从标注图像而非手工编码规则学习缺陷模式，这使它们适应性极强：在一个产线上训练的模型，几天就能为新零件重新训练，而基于规则的系统可能需要数月工程。加上相机与边缘计算成本的下降，这把AI检测从汽车与电子巨头，带入了中型制造商的预算。</p>
<h2 id="key-principles-and-strategic-framework">关键原则与战略框架是什么？</h2>
<p>四条原则把成功的AI检测部署与昂贵的实验区分开。其一是模型之前先有缺陷数据。视觉模型的好坏取决于其训练图像，而制造商一贯低估所需的标注缺陷数据量——包括稀有和新颖的缺陷。早早投资数据捕获、标注流水线和合成缺陷生成的团队，构建出在生产中真正站得住的模型。</p>
<p>其二是产线集成，而非实验室演示。一个在精选工作台有效、却无法应对产线振动、光照变化和换产的系统，交付不了任何价值。部署必须考虑产线的物理与运营现实，包括缺陷如何被处置——拒收、标记返工，还是反馈给工艺。</p>
<p>其三是改变而非消失的人力角色。操作员从盯着零件，转为处理异常队列、训练数据和模型反馈——这种角色转变需要培训与变革管理，而非仅仅是软件。其四是持续监控：随着工具磨损和材料变化，缺陷分布会漂移，因此必须把模型性能跟踪和重新训练排期作为常规维护的一部分。</p>
<h2 id="implementation-approach-and-best-practices">哪些实施方法与最佳实践有效？</h2>
<p>实施分三个阶段。第一阶段，8到12周，是发现与数据：选择业务价值最清晰的检测点，为产线装检测捕获图像，并与质量和制造工程师一起构建标注数据集。此阶段还应在训练任何模型之前，定义验收标准——缺陷检测率、误报率和吞吐影响。</p>
<p>第二阶段是在单条产线或工位的90天试点，先以影子模式运行，把模型与当前检测对比，然后在生产中由操作员复核异常。试点确立真实世界的准确率数字与重训节奏。第三阶段扩展到更多产线和工位，标准化共享工具。一个生产的视觉QA能力通常包括：</p>
<ul>
<li>按产线速度与零件几何尺寸选定的相机、光照与边缘计算</li>
<li>带版本化数据集与标注工具的标注图像仓库</li>
<li>用于缺陷检测与分类、可按产线重训的深度学习模型</li>
<li>与产线控制系统集成，使缺陷自动触发拒收、返工或告警</li>
<li>随时间对照人工验证样本跟踪模型精度的漂移监控</li>
</ul>
<p>一个模式在成功部署中反复出现：来自检测系统的数据成为战略资产。跨产线聚合的缺陷模式，揭示上游工艺问题、供应商质量问题和设计弱点——价值远超检测点本身。</p>
<h2 id="why-do-vision-qa-projects-fail-in-manufacturing">为什么视觉QA项目在制造业会失败？</h2>
<p>大多数视觉QA失败可追溯于数据，而非算法。第一原因是缺陷数据不足：真实产线关于最重要的缺陷的例子很少，因为良品远多于次品，于是模型在微小、有偏的样本上训练，在第一个新颖缺陷上就失败。第二原因是对准确率不切实际的预期：团队承诺近乎完美的检测，发现捕捉缺陷与淹没误报之间不可避免的权衡，并在数字低于推销时失去干系人信心。</p>
<p>第三原因是低估集成。模型是容易的部分；产线集成——触发拒收机制、处理换产、应对光照漂移、与MES接口——才是进度拖延和预算耗尽之处。第四原因是把部署当作完成。没有监控和重训，准确率随产线变化而衰减，上线时令人印象深刻的系统，在几个月内被操作员悄悄绕过。</p>
<h2 id="measuring-success-and-demonstrating-roi">你如何衡量成功并展示ROI？</h2>
<p>视觉QA的ROI以捕捉的缺陷和避免的成本衡量。运营指标包括缺陷检测率、误报率、检测吞吐与标记时延。业务指标包括逃逸缺陷——到达客户的次品占比——加上返工、报废、保修索赔和避免的召回成本；这些才是真正金钱所在，因为在汽车与电子中，逃逸缺陷的成本通常比在产线捕捉它们高出一个数量级。McKinsey关于预测与质量分析的工作，例如，指出当维护与质量数据结合时，停机减少30%–50%——这一数字显示了检测数据如何复合成更广阔的经营价值。</p>
<p>战略指标捕捉更广泛的影响：缺陷趋势数据喂给供应商记分卡、设计反馈和持续改进计划。开始前要建立的基线是当前不良质量成本——报废、返工、保修和客户影响——因为该基线把每个捕捉到的缺陷变成财务可验证的节省。</p>
<h2 id="common-pitfalls-and-how-to-avoid-them">常见的陷阱有哪些，如何避免？</h2>
<p>四个陷阱反复出现。其一是未理解缺陷经济学就先买相机和软件——投资检测却不知哪些缺陷逃逸成本最高。其二是忽视误报问题：一个标记太多良品的系统，要么停线，要么被调到无用，所以误报率值得与检测率一样多的设计关注。</p>
<p>其三是糟糕的图像数据卫生——不一致的光照、未标注的捕获、无版本化——悄悄毒害每个重训周期。其四是忽视人：不理解或不信任系统的操作员会覆盖它，所以培训、反馈环和清晰的异常处理工作流，与模型同等重要。从一开始就为人在回路设计的组织，持续胜过把部署当作纯技术事件的那些。</p>
<h2 id="how-to-get-started-with-ai-visual-inspection">如何开始AI视觉检测？</h2>
<p>选一个逃逸缺陷成本最高、环境稳定的检测点——高产量产线上的瓶颈工位是理想选择。在训练任何东西之前，捕获并标注90天图像，因为决定成败的是数据集，而非模型。把模型与当前检测一起以影子模式运行，确立诚实的准确率数字，然后上线，由操作员复核异常，并定义重训节奏。</p>
<p>并规划检测数据在产线之外的用途。当缺陷分析能在整个组织中被查询时，价值复加：一位工程师问&#x201C;本周哪个供应商导致了缺陷激增？&#x201D;，或一位厂长探究&#x201C;换产之后良率如何变化？&#x201D;，都应实时得到答案。这正是受管理的对话层所能——蜂启咨询的对话式BI连接到质量数据，让团队用自然语言从聊天中追问良率、缺陷与根因，约两周内部署，无需重建数据仓库。检测系统不再是点方案，而成为工厂每天管理质量的方式的一部分。</p>
<h2 id="key-takeaways">关键要点</h2>
<ul>
<li>缺陷数据是约束条件——训练前捕获并标注数月而非数周的图像</li>
<li>显式设计误报权衡；产线无法信任的系统会被绕过</li>
<li>与产线和异常工作流集成，而非仅与相机</li>
<li>监控精度并按计划重训；缺陷分布随工具和材料变化而漂移</li>
<li>开始前衡量不良质量成本，使每个捕捉的缺陷变成可验证的美元</li>
<li>把检测数据变成团队能实时查询的全厂智能</li>
</ul>
<h2 id="conclusion">结论</h2>
<p>计算机视觉已从实验室演示走向产线，因为它现在以工业速度工作、几天适应新零件、并在避免的逃逸缺陷上收回成本。捕获价值的制造商把它当作以模型为中心的数据计划——投资标注数据、与产线集成、让人留在回路中、并随时间监控性能。结果不仅是更少的缺陷，而是一个持续学习、并在数秒内回答关于自身性能问题的质量运营。</p>
<p>对制造领导者的实际建议是，从最痛的检测点起步，用数据而非演示证明价值，并把检测视为一条持续的数据流，而非一次性项目。当视觉检测与对话式分析相连，质量团队不再等待月度报告，而是在缺陷出现的当天就追问根因——这正是运营从被动走向主动的转折点，也是AI视觉检测从&#x201C;省钱工具&#x201D;升级为&#x201C;竞争能力&#x201D;的地方。</p>

<!--AUTOEXPAND-START-->
<h2 id="how-do-you-choose-the-right-camera-and-optics">你如何选择正确的相机与光学？</h2>
<p>模型精度吸引注意力，但相机与光学决定天花板。一个小于可分辨像素的缺陷，无论收集多少数据都无法被学习。实用规则是：把光学系统尺寸定为让最小的关注缺陷至少跨3到5个像素，然后选择光照以在该缺陷上最大化对比度。暗场光照揭示反光表面的划痕；背光隔离轮廓；结构光发现深度。我们评审过的大多数失败试点，不是数据问题——而是光照问题，在传感器之前就让信号不可见。</p>
<p>第二个决策是边缘与服务器推理。产线速度与延迟预算通常把检测推到靠近相机的边缘，避免网络抖动并把判定留在工位。但边缘部署提高了模型打包、空中更新和漂移监控的门槛，因为地面上退化的模型会静默失败，直到不良品运出。我们建议两层设置：边缘做实时合格/不合格，服务器端副本持续重评样本以检测漂移。这种拆分在关键处给你速度，在保护品牌处给你监督。</p>
<p>第三个常被忽视的决策是标注策略本身。缺陷标注的一致性，比标注数量更影响模型上限：不同标注员对&#x201C;轻微划痕&#x201D;的判定若不一致，模型学到的边界就会模糊。成功的团队建立标注规范、用交叉校验控制质量，并把标注本身当作受治理的资产——这与他们在语义层上所做的，是同一套纪律。</p>
<p>最后，把视觉检测当作一项会被审计的能力来运营。记录每次拒收的依据、每个模型的版本与精度，并在质量评审中定期复核，能让系统在产线变化中保持可信。那些把这视为工程纪律而非一次性项目的制造商，往往在第一年就看到逃逸缺陷与保修成本的双重下降。</p>
<!--AUTOEXPAND-END-->'''

ZH_SIDEBAR = '''<nav class="toc-links">
                    <a href="#understanding-the-current-landscape" class="toc-link">你应如何理解当前的视觉QA格局？</a>
                    <a href="#key-principles-and-strategic-framework" class="toc-link">关键原则与战略框架是什么？</a>
                    <a href="#implementation-approach-and-best-practices" class="toc-link">哪些实施方法与最佳实践有效？</a>
                    <a href="#why-do-vision-qa-projects-fail-in-manufacturing" class="toc-link">为什么视觉QA项目在制造业会失败？</a>
                    <a href="#measuring-success-and-demonstrating-roi" class="toc-link">你如何衡量成功并展示ROI？</a>
                    <a href="#common-pitfalls-and-how-to-avoid-them" class="toc-link">常见的陷阱有哪些，如何避免？</a>
                    <a href="#how-to-get-started-with-ai-visual-inspection" class="toc-link">如何开始AI视觉检测？</a>
                    <a href="#key-takeaways" class="toc-link">关键要点</a>
                    <a href="#conclusion" class="toc-link">结论</a>
                </nav>'''

zh_p = base + "/zh-cn/blog/articles/" + slug + ".html"
h = open(zh_p, encoding='utf-8').read()
s = h.find('<div class="toc-mobile" id="toc-mobile">')
e = h.find('<section class="faq-section" id="faq"')
h = h[:s] + ZH_PROSE + "\n" + h[e:]
open(zh_p, 'w', encoding='utf-8').write(h)
h = open(zh_p, encoding='utf-8').read()
si = h.find('<nav class="toc-links">')
ei = h.find('</nav>', si)
h = h[:si] + ZH_SIDEBAR + h[ei+len('</nav>'):]
open(zh_p, 'w', encoding='utf-8').write(h)

zhcn = open(zh_p, encoding='utf-8').read()
m = re.search(r'<main>.*</main>', zhcn, re.S)
tw_main = cc.convert(m.group(0))
tw_main = tw_main.replace('/zh-cn/', '/zh-tw/').replace('zh-cn/', 'zh-tw/').replace('预约演示', '預約示範')
zhtw = open(base + "/zh-tw/blog/articles/" + slug + ".html", encoding='utf-8').read()
zhtw = re.sub(r'<main>.*</main>', tw_main, zhtw, flags=re.S)
open(base + "/zh-tw/blog/articles/" + slug + ".html", 'w', encoding='utf-8').write(zhtw)
print("slug3 done")
