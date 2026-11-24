#!/usr/bin/env python3
"""Build a clean, production-only Cloudflare Pages tree from git-tracked files.

Cloudflare Pages Direct Upload (wrangler pages deploy) does not honour
.assetsignore the way Workers Static Assets does. This script materialises
<repo>/_deploy_prod from `git ls-files website`, removing internal tooling,
drafts, orphan assets and byte-identical duplicates. The source of truth stays
in website/ and git; the generated directory is disposable and git-ignored.
"""

from __future__ import annotations

import fnmatch
import hashlib
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPO / "website"
SOURCE_PREFIX = "website/"
DEPLOY_ROOT = REPO / "_deploy_prod"

# Internal tooling / drafts / audit output never belongs in a public deploy.
EXCLUDED_DIRS = {
    ".github",
    ".trae-html-share-packages",
    "_batch_pipeline",
    "_chrome",
    "beehive-homepage",
    "beehive-homepage-draft",
    "i18n",
    "node_modules",
    "scripts",
    "seo-audit-report",
    "seo-audit-summary",
    "templates",
}

EXCLUDED_ROOT_FILES = {
    ".assetsignore",
    ".gitignore",
    "bing_wm_login_options.png",
    "gsc_mirror_audit_report.txt",
    "url_defects.json",
    "weixin-drafts-full.png.jpg",
    "zh-quality-followup-2026-09-01.txt",
}

EXCLUDED_ROOT_GLOBS = (
    "*.md",
    "*.py",
    "*.zip",
    "audit_*.txt",
    "gen-*.py",
    "wechat-cover-*.jpg",
)

EXCLUDED_EXACT_FILES = {
    "seo-geo-strategy/GEO_CITATION_BASELINE.md",
    "seo-geo-strategy/geo_citation_tracking.csv",
}

TEXT_SUFFIXES = {".html", ".css", ".js", ".json", ".txt", ".xml", ".md"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif", ".ico"}
ASSET_RE = re.compile(
    r'([A-Za-z0-9._/\\-]+\.(?:jpg|jpeg|png|webp|svg|gif|ico))(?:\?[^\s"\'<>]*)?',
    re.I,
)

COVER_PREFIX = "assets/blog/covers/"
COVER_LOCALES = ("zh-cn", "zh-tw")
SVG_PREFIX = "assets/blog/svg/"

# Cloudflare Pages limits: 2,000 static + 100 dynamic redirects.
MAX_STATIC_REDIRECTS = 2_000
MAX_DYNAMIC_REDIRECTS = 100
MAX_DEPLOY_FILES = 19_800


def is_public(rel: str) -> bool:
    parts = Path(rel).parts
    if parts[0] in EXCLUDED_DIRS:
        return False
    if rel in EXCLUDED_EXACT_FILES:
        return False
    if len(parts) == 1:
        if rel in EXCLUDED_ROOT_FILES:
            return False
        if any(fnmatch.fnmatch(rel, pattern) for pattern in EXCLUDED_ROOT_GLOBS):
            return False
    return True


def tracked_website_files() -> list[str]:
    output = subprocess.check_output(
        ["git", "ls-files", "website"],
        cwd=REPO,
        text=True,
    ).splitlines()
    return [line[len(SOURCE_PREFIX) :] for line in output if line.startswith(SOURCE_PREFIX)]


def collect_reference_basenames(rels: list[str]) -> set[str]:
    """Collect every asset basename mentioned in public text files."""
    basenames: set[str] = set()
    for rel in rels:
        if Path(rel).suffix.lower() not in TEXT_SUFFIXES:
            continue
        path = SOURCE_ROOT / rel
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as handle:
                for line in handle:
                    for match in ASSET_RE.findall(line):
                        basenames.add(os.path.basename(match).lower())
        except OSError:
            continue
    return basenames


def unreferenced_images(rels: list[str], basenames: set[str]) -> set[str]:
    orphans = set()
    for rel in rels:
        if Path(rel).suffix.lower() not in IMAGE_SUFFIXES:
            continue
        lower = rel.lower()
        if lower in basenames or Path(rel).name.lower() in basenames:
            continue
        orphans.add(rel)
    return orphans


def byte_identical_cover_groups(rels: list[str], en_names: set[str]) -> dict[str, set[str]]:
    """Return locale -> files that can be rewritten to an identical en cover."""
    en_hashes = {
        name: hashlib.md5((SOURCE_ROOT / f"{COVER_PREFIX}en/{name}").read_bytes()).hexdigest()
        for name in en_names
    }
    groups: dict[str, set[str]] = {}
    for locale in COVER_LOCALES:
        prefix = f"{COVER_PREFIX}{locale}/"
        files = {rel for rel in rels if rel.startswith(prefix)}
        if not files:
            continue
        if not all(
            Path(rel).name in en_hashes
            and hashlib.md5((SOURCE_ROOT / rel).read_bytes()).hexdigest()
            == en_hashes[Path(rel).name]
            for rel in files
        ):
            continue
        groups[locale] = files
    return groups


def duplicate_svg_rewrites(rels: list[str]) -> dict[str, str]:
    """Map duplicate SVG paths to one canonical path per identical-content group."""
    hashes: dict[str, list[str]] = defaultdict(list)
    for rel in rels:
        if not rel.startswith(SVG_PREFIX) or not rel.lower().endswith(".svg"):
            continue
        digest = hashlib.md5((SOURCE_ROOT / rel).read_bytes()).hexdigest()
        hashes[digest].append(rel)

    rewrites: dict[str, str] = {}
    for group in hashes.values():
        if len(group) < 2:
            continue
        canonical = min(group)
        for rel in group:
            if rel != canonical:
                rewrites[rel] = canonical
    return rewrites


def count_existing_redirects() -> tuple[int, int]:
    static = dynamic = 0
    source = SOURCE_ROOT / "_redirects"
    for line in source.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        fields = stripped.split()
        if len(fields) < 3 or not fields[-1].isdigit():
            continue
        if "*" in fields[0] or ":" in fields[0]:
            dynamic += 1
        else:
            static += 1
    return static, dynamic


def main() -> int:
    tracked = tracked_website_files()
    public = sorted(rel for rel in tracked if is_public(rel))
    internal_docs = {rel for rel in public if rel in EXCLUDED_EXACT_FILES or rel.startswith("i18n/")}
    scan_set = [rel for rel in public if rel not in internal_docs]

    basenames = collect_reference_basenames(scan_set)
    orphans = unreferenced_images(scan_set, basenames)

    cover_scan = [rel for rel in scan_set if rel not in orphans]
    en_names = {
        Path(rel).name
        for rel in cover_scan
        if rel.startswith(f"{COVER_PREFIX}en/")
    }
    cover_groups = byte_identical_cover_groups(cover_scan, en_names)
    cover_skips = set().union(*cover_groups.values()) if cover_groups else set()

    svg_rewrites = duplicate_svg_rewrites([rel for rel in scan_set if rel not in orphans])

    skip = internal_docs | orphans | cover_skips | set(svg_rewrites)
    kept = [rel for rel in public if rel not in skip]

    if len(kept) > MAX_DEPLOY_FILES:
        print(
            f"ERROR: production tree would contain {len(kept):,} files, "
            f"above the safe limit of {MAX_DEPLOY_FILES:,}.",
            file=sys.stderr,
        )
        return 1

    static_before, dynamic_before = count_existing_redirects()
    static_added = len(svg_rewrites)
    dynamic_added = len(cover_groups)
    if static_before + static_added > MAX_STATIC_REDIRECTS:
        print("ERROR: too many static redirects.", file=sys.stderr)
        return 1
    if dynamic_before + dynamic_added > MAX_DYNAMIC_REDIRECTS:
        print("ERROR: too many dynamic redirects.", file=sys.stderr)
        return 1

    if DEPLOY_ROOT.exists():
        shutil.rmtree(DEPLOY_ROOT)
    DEPLOY_ROOT.mkdir(parents=True)

    for rel in kept:
        destination = DEPLOY_ROOT / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        # _redirects is edited below, so it must be a private copy, not a link.
        if rel == "_redirects":
            shutil.copy2(SOURCE_ROOT / rel, destination)
            continue
        try:
            os.link(SOURCE_ROOT / rel, destination)
        except OSError:
            shutil.copy2(SOURCE_ROOT / rel, destination)

    extra_rules: list[str] = [
        "",
        "# === Generated by build_prod_tree.py: deduplicate identical assets ===",
    ]
    for locale in sorted(cover_groups):
        extra_rules.append(
            f"/{COVER_PREFIX}{locale}/* /{COVER_PREFIX}en/:splat 200"
        )
    for source, canonical in sorted(svg_rewrites.items()):
        extra_rules.append(f"/{source} /{canonical} 200")

    with (DEPLOY_ROOT / "_redirects").open("a", encoding="utf-8") as handle:
        handle.write("\n".join(extra_rules) + "\n")

    print(f"Production deploy tree: {DEPLOY_ROOT}")
    print(f"Tracked public files: {len(public):,}")
    print(f"Final files:          {len(kept):,} (Cloudflare Free cap: 20,000)")
    print(f"  orphan images:      {len(orphans):,}")
    print(f"  cover duplicates:   {len(cover_skips):,} ({dynamic_added} wildcard rewrites)")
    print(f"  svg duplicates:     {len(svg_rewrites):,} exact rewrites")
    print(f"  internal docs:      {len(internal_docs):,}")
    print(
        f"Redirects: static {static_before}+{static_added}, "
        f"dynamic {dynamic_before}+{dynamic_added}"
    )
    for directory, count in Counter(Path(rel).parts[0] for rel in kept).most_common(12):
        print(f"  {count:6,d}  {directory}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
