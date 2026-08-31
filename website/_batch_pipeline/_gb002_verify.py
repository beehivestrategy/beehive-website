#!/usr/bin/env python3
"""Guardrail verification for gbatch_002: head/footer/share untouched, versioned assets intact,
   JSON-LD valid, HTML well-formed, no duplicate ids."""
import json
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb002_lib import path_for, SLUGS

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
BK = os.path.join(ROOT, '_batch_pipeline/_backup_gb002run')
PFX = {'en': 'en.', 'zh-cn': 'cn.', 'zh-tw': 'tw.'}

LD_RE = re.compile(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I)
VOID = {'img', 'br', 'hr', 'meta', 'link', 'input', 'source', 'path', 'circle', 'line',
        'polyline', 'rect', 'use', 'stop', 'polygon', 'ellipse'}


def strip_faq_ld(doc):
    """Remove FAQPage JSON-LD blocks so head comparison ignores the permitted edit."""
    def repl(m):
        return '' if 'FAQPage' in m.group(2) else m.group(0)
    return re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?</script>)', repl, doc, flags=re.S | re.I)


def head_of(doc):
    e = doc.find('</head>')
    return doc[:e]


def footer_of(doc):
    s = doc.find('<footer')
    return doc[s:] if s >= 0 else ''


def share_of(doc):
    return '\n'.join(re.findall(r'<[^>]*class="[^"]*share[^"]*"[^>]*>', doc))


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d:
            self.ids.append(d['id'])
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f'stray </{tag}>')
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f'unclosed <{self.stack.pop()}> before </{tag}>')
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(f'unexpected </{tag}>')


def main():
    problems = []
    for slug in SLUGS:
        for lang in ('en', 'zh-cn', 'zh-tw'):
            p = path_for(slug, lang)
            new = open(p, encoding='utf-8').read()
            old = open(os.path.join(BK, PFX[lang] + slug + '.html'), encoding='utf-8').read()
            tag = f'{slug}/{lang}'

            if strip_faq_ld(head_of(new)) != strip_faq_ld(head_of(old)):
                problems.append(f'{tag}: <head> changed beyond FAQPage JSON-LD')
            if footer_of(new) != footer_of(old):
                problems.append(f'{tag}: <footer> changed')
            if share_of(new) != share_of(old):
                problems.append(f'{tag}: share markup changed')

            for asset in ('/css/article.css?v=20260826', '/js/article.js?v=20260826'):
                if asset in old and asset not in new:
                    problems.append(f'{tag}: lost {asset}')

            # root-relative / language-prefixed links preserved
            old_links = set(re.findall(r'(?:href|src)="((?:zh-(?:cn|tw))?/(?:blog|css|js|assets|contact|solution|about|services|pricing|training|industries|case-studies|security|privacy|terms|cookies)[^"]*)"', old))
            new_links = set(re.findall(r'(?:href|src)="((?:zh-(?:cn|tw))?/(?:blog|css|js|assets|contact|solution|about|services|pricing|training|industries|case-studies|security|privacy|terms|cookies)[^"]*)"', new))
            lost = old_links - new_links
            lost = {l for l in lost if not l.startswith('blog/')}
            if lost:
                problems.append(f'{tag}: root-relative links lost: {sorted(lost)[:5]}')

            # exactly one FAQPage JSON-LD, valid JSON
            lds = [m.group(1) for m in LD_RE.finditer(new)]
            faq = [s for s in lds if 'FAQPage' in s]
            if len(faq) != 1:
                problems.append(f'{tag}: {len(faq)} FAQPage JSON-LD blocks')
            else:
                try:
                    d = json.loads(faq[0])
                    if d.get('@type') != 'FAQPage' or len(d.get('mainEntity', [])) < 3:
                        problems.append(f'{tag}: FAQPage JSON-LD malformed')
                except Exception as e:
                    problems.append(f'{tag}: FAQPage JSON-LD invalid JSON ({e})')
            for s in lds:
                try:
                    json.loads(s)
                except Exception as e:
                    problems.append(f'{tag}: other JSON-LD invalid ({e})')

            # well-formed + unique ids
            c = Checker()
            c.feed(new)
            c.close()
            if c.errors:
                problems.append(f'{tag}: html issues {c.errors[:3]}')
            if c.stack:
                problems.append(f'{tag}: unclosed tags {c.stack[:3]}')
            dupes = {i for i in c.ids if c.ids.count(i) > 1}
            dupes.discard('')
            if dupes:
                problems.append(f'{tag}: duplicate ids {sorted(dupes)[:5]}')

    if problems:
        print('PROBLEMS:')
        for p_ in problems:
            print(' -', p_)
    else:
        print('ALL GUARDRAIL CHECKS PASSED')


if __name__ == '__main__':
    main()
