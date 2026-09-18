#!/bin/bash
# Canonical rsync: website/ -> website_deploy_clean/ (2026-09-02 定稿规则)
# Excludes internal-only files; keeps .well-known, llms.txt, verification files.
set -e
SRC="/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/"
DST="/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website_deploy_clean/"

rsync -a --delete --delete-excluded \
  --exclude='_batch_pipeline/' \
  --exclude='_chrome/' \
  --exclude='scripts/' \
  --exclude='templates/' \
  --exclude='node_modules/' \
  --exclude='.git/' \
  --exclude='seo-audit-*/' \
  --exclude='beehive-homepage*/' \
  --exclude='*.bak*' \
  --exclude='zip/' \
  --exclude='website-audit-report.md' \
  --exclude='gsc_mirror_audit_report.txt' \
  --exclude='url_defects.json' \
  --exclude='zh-quality-followup-2026-09-01.txt' \
  --exclude='wechat-*-preview.html' \
  --exclude='weixin-drafts-full.png.jpg' \
  --exclude='gen-batch.py' \
  --exclude='gen-what-is.py' \
  --exclude='beehive-strategy-v2-prompt.md' \
  --exclude='overview.md' \
  "$SRC" "$DST"

echo "--- file count ---"
find "$DST" -type f | wc -l
