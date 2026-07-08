#!/usr/bin/env python3
"""
Generate multi-language (zh-CN, zh-TW) versions of the Beehive Strategy website.

== NEW APPROACH (July 2026) ==
The old string-replacement approach was replaced because it produced fragmented,
word-by-word translations that mixed English and Chinese. The new approach:

1. **zh-CN pages**: Manually written as complete, cohesive Chinese HTML documents.
   Each page is translated as a whole by a fluent Chinese speaker, preserving
   natural sentence flow, context-appropriate terminology, and complete coverage
   of all content (meta tags, JSON-LD, body text, etc.).

2. **zh-TW pages**: Auto-generated from zh-CN using OpenCC (Simplified → Traditional).
   The conversion handles:
   - lang="zh-CN" → lang="zh-TW"
   - Canonical URLs: /zh-cn/ → /zh-tw/
   - hreflang tags: zh-CN → zh-TW (and adds zh-CN back)
   - og:locale: zh_CN → zh_TW
   - Language switcher: zh-tw active, zh-cn inactive
   - Current lang label: 简 → 繁

== USAGE ==
    python generate_zh_tw.py          # Generate zh-TW pages from zh-CN
    python update_sitemap.py          # Regenerate sitemap with all hreflang
    python update_nav.py              # Update nav across all pages (if needed)

== FILES ==
    website/zh-cn/*.html              # Manually written Simplified Chinese pages
    website/zh-tw/*.html              # Auto-generated Traditional Chinese pages
    generate_zh_tw.py                 # OpenCC-based zh-TW generator
"""

import os
import shutil
from pathlib import Path

WEBSITE_DIR = Path(__file__).parent / "website"
ZH_CN_DIR = WEBSITE_DIR / "zh-cn"
ZH_TW_DIR = WEBSITE_DIR / "zh-tw"

ASSETS_TO_COPY = ["css", "js", "assets"]


def copy_static_assets():
    """Copy CSS, JS, and image assets to language directories."""
    for lang_dir in [ZH_CN_DIR, ZH_TW_DIR]:
        for asset in ASSETS_TO_COPY:
            src = WEBSITE_DIR / asset
            dst = lang_dir / asset
            if src.exists():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"  Copied {asset}/ to {lang_dir.name}/")


def main():
    print("Beehive Strategy — Multi-Language Generator")
    print("=" * 50)
    print()
    print("Note: zh-CN pages are now hand-written (not auto-translated).")
    print("Use generate_zh_tw.py for OpenCC-based zh-TW generation.")
    print()
    print("Copying static assets...")
    copy_static_assets()
    print()
    print("Done. Next steps:")
    print("  1. python generate_zh_tw.py     # Generate zh-TW from zh-CN")
    print("  2. python update_sitemap.py     # Regenerate sitemap")
    print()


if __name__ == "__main__":
    main()
