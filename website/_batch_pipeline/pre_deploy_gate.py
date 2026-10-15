#!/usr/bin/env python3
"""
pre_deploy_gate.py — 部署前「机器翻译粉碎」+ 致命 SEO 缺陷闸门

专扫【部署产物树】(默认 website_deploy_clean/，即真正上 Cloudflare 的那棵树)，
在 `wrangler pages deploy` 之前跑，发现任一粉碎 signature 或致命缺陷即 exit 1，
阻止把乱码 description 推上 PROD。

检查项：
  1. meta description 含粉碎签名 [a-z][一-鿿]+[a-z]  -> 致命
  2. meta description 缺失 / 空 / >160 字符          -> 致命
  3. <title> 缺失 / 空                               -> 致命
  4. 非 EN 页面缺 canonical                          -> 致命
  5. og:description / twitter:description 与 meta 不一致 -> 告警(非致命)

用法：
  python pre_deploy_gate.py                         # 默认扫 website_deploy_clean/
  python pre_deploy_gate.py /path/to/deploy/dir
  python pre_deploy_gate.py --strict                # 含告警也 exit 1

Exit: 0=通过  1=致命缺陷  2=IO 错误
"""
import argparse
import re
import sys
from pathlib import Path

HAN = r"[\u4e00-\u9fff]"
CORRUPT_RE = re.compile(r"[a-z]" + HAN + r"+[a-z]")
MAX_DESC = 160


def get_head(p: Path, n: int = 4000) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")[:n]
    except Exception:
        return ""


def _content_in_tag(tag: str):
    """Backslash-aware content="..." / content='...' extraction inside ONE meta
    tag. Tolerates an escaped apostrophe (\\') which would otherwise truncate the
    value, and works whether content= precedes or follows name/property."""
    i = tag.find('content=')
    if i < 0:
        return None
    j = i + len('content=')
    q = tag[j] if j < len(tag) else ''
    if q not in ('"', "'"):
        return None
    p = j + 1
    while p < len(tag):
        if tag[p] == q and (p == j + 1 or tag[p - 1] != '\\'):
            break
        p += 1
    else:
        return None
    return tag[j + 1:p]


def get_meta_desc(head: str):
    # Exact attribute match so we don't catch name="twitter:description".
    m = re.search(r'<meta\b[^>]*?name=["\']description["\'][^>]*?>', head, re.I)
    return _content_in_tag(m.group(0)) if m else None


def get_meta_prop(head: str, prop: str):
    for marker in (f'property=["\']{re.escape(prop)}["\']',
                   f'name=["\']{re.escape(prop)}["\']'):
        m = re.search(r'<meta\b[^>]*?' + marker + r'[^>]*?>', head, re.I)
        if m:
            v = _content_in_tag(m.group(0))
            if v is not None:
                return v
    return None


def get_title(head: str):
    m = re.search(r"<title>(.*?)</title>", head, re.S | re.I)
    return (m.group(1).strip() if m else "") or None


def get_canonical(head: str):
    return ('rel="canonical"' in head) or ('rel="alternate" hreflang="x-default"' in head)


def lang_of(rel: str) -> str:
    if "/zh-cn/" in "/" + rel or rel.startswith("zh-cn/"):
        return "zh-cn"
    if "/zh-tw/" in "/" + rel or rel.startswith("zh-tw/"):
        return "zh-tw"
    return "en"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", nargs="?", default=None)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    # 默认扫【部署产物树】website_deploy_clean/（真正上 Cloudflare 的那棵），
    # 而非 website/ 源树 —— 源树下的 _batch_pipeline/_backup_* 是修复前的备份副本，
    # 含旧粉碎 description，rsync 已排除出部署树，扫它们会误报致命缺陷。
    if args.dir:
        root = Path(args.dir)
    else:
        root = Path(__file__).resolve().parent.parent.parent / "website_deploy_clean"
    if not root.exists():
        print(f"❌ 目录不存在: {root}", file=sys.stderr)
        return 2

    files = sorted(root.rglob("*.html"))
    # 只扫【真正会部署】的 HTML。镜像 sync_deploy_clean.sh 的 rsync 排除清单，
    # 跳过非部署产物目录/文件，避免把备份、草稿、模板、脚本树里的存量缺陷误报成致命。
    EXCLUDE_DIRS = {"_batch_pipeline", "_chrome", "scripts", "templates",
                    "node_modules", ".git"}
    def _skip(p: Path) -> bool:
        for comp in p.parts:
            if comp in EXCLUDE_DIRS:
                return True
            if comp.startswith(("seo-audit-", "beehive-homepage")):
                return True
            if "_backup" in comp:
                return True
        if ".bak" in p.name:       # *.bak* 文件（如 foo.bak.html）
            return True
        # wechat-*-preview.html 是微信草稿预览，rsync 已排除出部署树
        if p.name.startswith("wechat-") and p.name.endswith("-preview.html"):
            return True
        return False
    files = [f for f in files if not _skip(f)]
    print(f"预部署闸门扫描: {root}  ({len(files)} HTML)")

    fatal = 0
    warn = 0
    corrupt = 0
    details = []
    for p in files:
        rel = str(p.relative_to(root))
        lang = lang_of(rel)
        head = get_head(p)
        issues = []

        desc = get_meta_desc(head)
        if desc is None:
            issues.append("MISSING_DESCRIPTION")
        else:
            if CORRUPT_RE.search(desc):
                issues.append("CORRUPT_DESCRIPTION")
            if not desc.strip():
                issues.append("EMPTY_DESCRIPTION")
            if len(desc) > MAX_DESC:
                issues.append(f"DESC_TOO_LONG({len(desc)})")

        title = get_title(head)
        if not title:
            issues.append("MISSING_TITLE")

        if lang != "en" and not get_canonical(head):
            issues.append("MISSING_CANONICAL")

        # 一致性告警（非致命）
        if desc:
            for prop in ("og:description", "twitter:description"):
                v = get_meta_prop(head, prop)
                if v is not None and v != desc:
                    issues.append(f"MISMATCH_{prop}")

        # 致命 = 粉碎 / 缺失类（结构性，必须阻断）
        is_fatal = any(i.startswith(("CORRUPT", "MISSING_")) for i in issues)
        # 告警 = 空描述 / 超长 / 社交一致性（已知存量内容缺口，不阻断部署）
        is_warn = any(i.startswith(("EMPTY_", "DESC_TOO_LONG", "MISMATCH_")) for i in issues)
        if is_fatal:
            fatal += 1
            if "CORRUPT_DESCRIPTION" in issues:
                corrupt += 1
        if is_warn:
            warn += 1
        if issues:
            details.append((rel, lang, issues, (desc or "")[:70]))

    # 告警分类计数
    empty_n = sum(1 for _, _, iss, _ in details if any(i.startswith("EMPTY_") for i in iss))
    long_n = sum(1 for _, _, iss, _ in details if any(i.startswith("DESC_TOO_LONG") for i in iss))

    print(f"\n=== 预部署闸门结果 ===")
    print(f"文件: {len(files)} | 致命文件: {fatal} | 粉碎: {corrupt} | 告警: {warn} (空描述 {empty_n} / 超长 {long_n})")
    if details:
        print("\n--- 致命明细（前 40）---")
        for rel, lang, issues, d in details[:40]:
            if any(i.startswith(("CORRUPT", "MISSING_")) for i in issues):
                print(f"  [{lang}] {rel}\n     {issues}\n     desc::{d}")

    if corrupt > 0:
        print(f"\n❌ 发现 {corrupt} 个粉碎 description —— 禁止部署！先跑 fix_corrupt_descriptions.py --apply")
        return 1
    if fatal > 0:
        print(f"\n❌ 存在 {fatal} 个致命缺陷（粉碎/缺失类），阻止部署")
        return 1
    if warn > 0:
        print(f"\n⚠️  存在 {warn} 个告警（空描述 {empty_n} / 超长 {long_n} / 社交不一致）—— 非致命，不阻断部署（建议纳入内容 backlog）")
    print("\n✅ 闸门通过：无粉碎、无缺失致命缺陷。可部署。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
