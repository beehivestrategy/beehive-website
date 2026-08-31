import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline")
from lib import *

slug = "data-quality-at-scale-monitoring-alerting-remediation"
h = read(slug, "blog/articles")
before = article_metric(h, "EN")
m = re.search(r'(</div>\s*</div>\s*<div class="container">\s*)([\s\S]*?)(\s*<section class="recommended-section")', h, re.S)
if m and 'id="how-do-you-scale-data-quality' in m.group(2):
    block = m.group(2)
    # remove block from its misplaced location
    h2 = h[:m.start()] + m.group(1) + m.group(3) + h[m.end():]
    # insert inside article-content before </article>
    h2 = h2.replace('</article>', '\n'+block+'\n</article>', 1)
    write(slug, "blog/articles", h2)
    after = article_metric(h2, "EN")
    print(f"{slug}: EN {before} -> {after} {'OK' if after>=2500 else 'SHORT'}")
else:
    print("pattern not matched; block:", (m.group(2)[:50] if m else 'NO MATCH'))
