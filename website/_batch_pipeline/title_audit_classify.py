#!/usr/bin/env python3
"""标题审计分类：真问题 vs 简繁同形误报；重复组模式分类"""
import json, re

r = json.load(open('/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/title_audit.json'))

# 简体专用字采样表（足够区分常见词）
SIMP = set('设习么们业无发员应层观觉证质变经线构统练计议译记购贸费资标权欢术测环确简证据级架构维银铁门问间关闻阅阅队阳阴际陆陈险随隐难韩页顶顷项顺须顾顿颁预领频颖风飘饭饮马驱驶验骏高鱼鸟鸡鸣麦黄')
# 补充常见简体字
SIMP |= set('个为乐书买云产从众优会传伤伦体余佣侦侧侨俭债倾偿储儿兑兰关兴兹养兽写军农冲决况冻净 减凑凛凤凭凯击凿划刘则刚创删别剂剑剥剧劝办务动励劲劳势勋匀区医华协单卖卢卫厂厅历厉压厌厕厢厦厨县参双发变叙叠叶号叹吁后吓吕吗吨听启吴呕呗员呛呜周咏咙唤啧啸喷喽嘱嚣团园围图圆圣场坏块坚坛坝坞坟坠垄垒垦垫埙墙壮声壳壶处备复够头夸夹夺奋奖奥妆妇妈妸娴婴婴婵孙学孪宁宝实宠审宪宫宽宾寝对寻导寿将尔尘尝尴尸尽层屉届属屡屿岁岂岗岛岭峡峥峦崭嵘币帅师帐帘帜带幕庙废张强彻径御忆忧怀态怜怪怿恸恹恺恻恼恽悦悯惊惧惨惩惫惬惭惮惯愕愠愤愦愿慑懒戏战户扎扑执扩扫扬扰抚抛抡抢护报担拟拢拣拥拦拧拨择挂挚挛挝挞挟挠挡挣挤挥捞损捡换捣据掷掸掺揽搀搁搂搅携摄摆摇摈摊撑撒撵擞攒敌敛数斋斓斗斩断旧时旷昼显晋晒晓晕晖暂暧机杀杂条杨极构枢枣柜柠栀栅标栈栉栋栌栎栏树桠桢档桥桦桧桨桩梦检椟椭楼榄榈榉槛槟横樱檀欢欤欧歼殇残殒殓殡毁毂毕毙毡气氢氩汇汉汤汹沟沥沦沧沫泸泺泻泼泽泾洁洒浅浆浇浊测济浏浑浒浓涂涌涛涝涟涡涣涤润涧涨涩渍渎渐渔渗温游湾湿溃溅滚滞满滤滥滦滨滩灯灵灶灸灼炀炉炔烟烦烨烩烫烬热焕焖爱爷牍牵牺犊状犹狈狞独狭狮狰狱狲猡猛猎猫献玑玛玮环现玺珐珑珐珲琏琛琨琬琮琰瑶瑾璀璃璇璁璋璎璐璩璫瓒瓯瓴瓷甈画疯疱疲疴疵疸疼疾痈痉痊痍痒痘痛痨痪痴痹痿瘁瘅瘆瘊瘘瘗瘛瘜瘠疯瘢瘥瘴瘵瘸瘾癞癣癫癞皑皱盏盐监盒盗盘 盹盯眙眦眯睢睚瞌瞑瞒瞟瞟瞳瞻矫矬矗矶础硅硕硖硗硝硫硬碍碎碛碜碱碴磋碻碌磁磙磚磡磴磷磺磵矶礓礌礴矿砀码砖砗砚砜砝砧砮硅砹砺砻祢祯祷祸禀禅秃穷窃窍窄窈窕窑窜窝窥窦竖笃笋笑笔笕笙笺笼笾笸筹签简箍箅箓箔箦箧箨箩箪箫篓篙篚篝篡篥篮篱篷簌簏簖簦籁籀齿龃龄龅龆龇龈龉龊龋龌龙龚龛龟')
def has_simp(t): return any(c in SIMP for c in t)

real_cn_eq_tw = [x for x in r['cn_eq_tw'] if has_simp(x['title'])]
same_form = [x for x in r['cn_eq_tw'] if not has_simp(x['title'])]
print('=== cn_eq_tw 分类 ===')
print('真问题（含简体专用字，未转繁体）:', len(real_cn_eq_tw))
for x in real_cn_eq_tw: print('  ', x['slug'], '|', x['title'][:55])
print('简繁同形（合法，无需处理）:', len(same_form))
for x in same_form: print('  ', x['slug'], '|', x['title'][:55])

# 重复组分类（对三语言都跑）
print()
for lang in ('en', 'cn', 'tw'):
    variants, junk = [], []
    for x in r['exact_dup'][lang]:
        slugs = x['slugs']
        dated = [s for s in slugs if re.search(r'-202[456]\d{4}$', s)]
        if dated:  # 含日期后缀 slug 的组 → 重发布变体
            variants.append(x)
        else:
            junk.append(x)
    n_dups = len(r['exact_dup'][lang])
    print('--- %s exact_dup %d 组: 重发布变体组=%d, 其他=%d' % (lang, n_dups, len(variants), len(junk)))
    for x in junk[:12]:
        print(f'  [{len(x["slugs"])}] {x["title"][:48]}')
        for s in x['slugs'][:6]: print('      ', s)

# prefix 样本
print()
print('=== en prefix_dup 样本（5 个）===')
for x in r['prefix_dup']['en'][:5]:
    print(' base:', x['base']['title'][:55])
    print('  ext:', x['ext']['title'][:65])
