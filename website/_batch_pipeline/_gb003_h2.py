import re,sys
sys.path.insert(0,'/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import path_for, ART_OPEN, H2_RE, clean
slug,lang=sys.argv[1],sys.argv[2]
h=open(path_for(slug,lang),encoding='utf-8').read()
ai=h.find(ART_OPEN); ae=h.find('</article>',ai)
for m in H2_RE.finditer(h[ai:ae]):
    print(repr(m.group(2)), '|', clean(m.group(3)))
