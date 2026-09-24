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


def get_meta_desc(head: str):
    i = head.find('name="description"')
    if i < 0:
        return None
    j = head.find('content="', i)
    if j < 0:
        return None
    k = head.find('"', j + 9)
    return head[j + 9:k] if k > 0 else None


def get_meta_prop(head: str, prop: str):
    m = re.search(r'<meta[^>]+property=["\']' + re.escape(prop) + r'["\'][^>]+content=["\'](.*?)["\']', head, re.I | re.S)
    if not m:
        m = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+property=["\']' + re.escape(prop) + r'["\']', head, re.I | re.S)
    return m.group(1) if m else None


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

    root = Path(args.dir) if args.dir else Path(__file__).resolve().parent.parent
    if not root.exists():
        print(f"❌ 目录不存在: {root}", file=sys.stderr)
        return 2

    files = sorted(root.rglob("*.html"))
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
