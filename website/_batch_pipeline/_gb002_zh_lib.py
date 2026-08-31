#!/usr/bin/env python3
"""Apply Simplified-Chinese sections to zh-CN and their Traditional equivalents to zh-TW."""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb002_lib import apply_ops
from opencc import OpenCC

CC = OpenCC('s2twp')


def apply_zh(slug, marker_cn, sections):
    """sections: [(h2_cn, body_cn), ...] inserted before marker_cn (or '__FAQ__')."""
    before_cn = marker_cn
    c1 = apply_ops(slug, 'zh-cn', inserts=sections, before=before_cn)
    if marker_cn == '__FAQ__':
        before_tw = '__FAQ__'
    else:
        before_tw = CC.convert(marker_cn)
    tw_sections = [(CC.convert(h), CC.convert(b)) for h, b in sections]
    c2 = apply_ops(slug, 'zh-tw', inserts=tw_sections, before=before_tw)
    return c1, c2
