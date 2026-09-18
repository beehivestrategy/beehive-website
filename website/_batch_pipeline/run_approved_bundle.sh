#!/bin/bash
# ============================================================
# Approval-gated one-shot bundle (Task #805 收口)
# 用法:
#   bash run_approved_bundle.sh titles    APPROVED-BY-KENNETH   # 标题修复
#   bash run_approved_bundle.sh canonical APPROVED-BY-KENNETH   # 变体 canonical
#   bash run_approved_bundle.sh all       APPROVED-BY-KENNETH   # 两者一起
# 第二个参数必须逐字为 APPROVED-BY-KENNETH，否则拒绝执行（LOCKED 门禁）。
# 步骤: apply → 重跑标题审计 → sync clean copy → 打印部署命令
# ============================================================
set -e
MODE="${1:-}"
GATE="${2:-}"
BP="/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline"
PY="/Users/kennethkwok/.workbuddy/binaries/python/versions/3.13.12/bin/python3"

if [ "$GATE" != "APPROVED-BY-KENNETH" ]; then
  echo "❌ 拒绝执行：需要逐字批准参数 APPROVED-BY-KENNETH"; exit 1
fi
case "$MODE" in
  titles|canonical|all) ;;
  *) echo "❌ 用法: run_approved_bundle.sh <titles|canonical|all> APPROVED-BY-KENNETH"; exit 1 ;;
esac

echo "=== [1/4] 写入修复（mode=$MODE）==="
if [ "$MODE" = "titles" ] || [ "$MODE" = "all" ]; then
  (cd "$BP" && "$PY" apply_title_fixes.py --apply)
fi
if [ "$MODE" = "canonical" ] || [ "$MODE" = "all" ]; then
  (cd "$BP" && "$PY" apply_variant_canonical.py --apply)
fi

echo "=== [2/4] 重跑标题审计验证（约 7 分钟）==="
(cd "$BP" && "$PY" title_audit.py && "$PY" -c "
import json
a = json.load(open('$BP/title_audit.json'))
print('audit summary:', json.dumps(a.get('summary', {}), ensure_ascii=False))
")

echo "=== [3/4] 同步 website_deploy_clean ==="
bash "$BP/sync_deploy_clean.sh"

echo "=== [4/4] 部署命令（Kenneth 本机终端执行）==="
cat << 'EOF'
cd "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website_deploy_clean" && npx -y wrangler@4 pages deploy . --project-name=beehive-strategy-v2 --branch=main --commit-dirty=true
cd "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website_deploy_clean" && npx -y wrangler@4 pages deploy . --project-name=beehive-strategy-v2-staging --branch=main --commit-dirty=true
cd "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website_deploy_clean" && npx -y wrangler@4 pages deploy . --project-name=beehive-strategy --branch=main --commit-dirty=true
EOF
echo "✅ bundle 完成"
