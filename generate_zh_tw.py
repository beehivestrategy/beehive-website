#!/usr/bin/env python3
"""Generate zh-HK HTML files from zh-CN files using OpenCC (Simplified → Traditional).

This script:
1. Converts body text from Simplified to Traditional Chinese using OpenCC
2. Updates lang attribute to zh-HK
3. Updates canonical URLs from /zh-cn/ to /zh-hk/
4. Updates hreflang tags from zh-CN to zh-HK
5. Updates og:locale to zh_HK
6. Updates language switcher to show zh-HK as active
7. Keeps GTM, structured data, and all structural markup intact
"""

import os
import re
from pathlib import Path
from opencc import OpenCC

cc = OpenCC('s2t')

BASE_DIR = Path(__file__).parent / 'website'
ZH_CN_DIR = BASE_DIR / 'zh-cn'
ZH_TW_DIR = BASE_DIR / 'zh-hk'

# Ensure zh-hk directory exists
ZH_TW_DIR.mkdir(parents=True, exist_ok=True)

PAGES = [
    'solution.html',
    'services.html',
    'industries.html',
    'about.html',
    'case-studies.html',
]

def transform_page(content: str) -> str:
    """Apply all zh-CN → zh-HK transformations."""
    
    # 1. lang attribute
    content = content.replace('lang="zh-CN"', 'lang="zh-HK"')
    
    # 2. hreflang: Replace existing zh-CN line with zh-HK (before canonical URL change)
    content = re.sub(
        r'<link rel="alternate" hreflang="zh-CN" href="https://www\.beehivestrategy\.com/zh-cn/',
        '<link rel="alternate" hreflang="zh-HK" href="https://www.beehivestrategy.com/zh-hk/',
        content
    )
    
    # 3. Canonical URLs (NOT hreflang zh-CN — we add that back after this step)
    content = content.replace('href="https://www.beehivestrategy.com/zh-cn/', 'href="https://www.beehivestrategy.com/zh-hk/')
    
    # 4. Add zh-CN hreflang line after en hreflang (AFTER canonical URL change, so /zh-cn/ stays)
    def add_zh_cn_hreflang(m):
        en_line = m.group(0)
        page_path = m.group(1)
        zh_cn_line = f'\n  <link rel="alternate" hreflang="zh-CN" href="https://www.beehivestrategy.com/zh-cn/{page_path}">'
        return en_line + zh_cn_line
    
    content = re.sub(
        r'<link rel="alternate" hreflang="en" href="https://www\.beehivestrategy\.com/([^"]+)">',
        add_zh_cn_hreflang,
        content
    )
    
    # 5. og:locale
    content = content.replace('content="zh_CN"', 'content="zh_HK"')
    
    # 5. Language switcher: set zh-hk as active, zh-cn as inactive
    content = content.replace(
        '<a href="/zh-cn/" role="menuitem" class="active" data-lang="zh-cn"><span>简体中文</span><span class="lang-code">简</span></a>',
        '<a href="/zh-cn/" role="menuitem" data-lang="zh-cn"><span>简体中文</span><span class="lang-code">简</span></a>'
    )
    content = content.replace(
        '<a href="/zh-hk/" role="menuitem" data-lang="zh-hk"><span>繁體中文</span><span class="lang-code">繁</span></a>',
        '<a href="/zh-hk/" role="menuitem" class="active" data-lang="zh-hk"><span>繁體中文</span><span class="lang-code">繁</span></a>'
    )
    
    # 6. Current lang label shows 繁 instead of 简
    content = content.replace(
        '<span id="current-lang-label">简</span>',
        '<span id="current-lang-label">繁</span>'
    )
    
    # 7. Convert Chinese text using OpenCC (Simplified → Traditional)
    # We use a careful approach: only convert text that OpenCC recognizes as Chinese
    content = cc.convert(content)
    
    return content


def main():
    for page in PAGES:
        src_path = ZH_CN_DIR / page
        dst_path = ZH_TW_DIR / page
        
        if not src_path.exists():
            print(f"[SKIP] {src_path} not found")
            continue
        
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        transformed = transform_page(content)
        
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(transformed)
        
        print(f"[OK] {page} → zh-hk/ ({len(transformed)} chars)")


if __name__ == '__main__':
    main()
