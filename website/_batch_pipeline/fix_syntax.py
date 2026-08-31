import re
p = "_content.py"
s = open(p, encoding="utf-8").read()
# A broken fragment looks like:
#   ("exp-1", '''Question?''',
#    <p>para1</p>          <- opener ''' was wrongly stripped
#   <p>para2</p>'''),
# Fix: add ''' right before <p> on the line immediately after the question-title line.
pat = re.compile(r"'',\n(\s*)<p>")
def repl(m):
    return "'',\n" + m.group(1) + "'''<p>"
s2 = pat.sub(repl, s)
open(p, "w", encoding="utf-8").write(s2)
print("applied; remaining '','',\\n< p> occurrences:", len(pat.findall(s2)))
