#!/usr/bin/env bash
# =============================================================================
# deploy.sh — HARD-RULE ENFORCER for beehivestrategy.com
# -----------------------------------------------------------------------------
# The rule (single source of truth = git):
#   dev     <- branch `main`      -> CF project `beehive-strategy-v2`
#   staging <- branch `staging`   -> CF project `beehive-strategy-v2-staging`
#   prod    <- branch `prod`      -> CF project `beehivestrategy`
# Promotion flow is enforced:  main --> staging --> prod  (prod only via merge)
#
# This script REFUSES to run unless every guard below passes. It is the local
# safety net; Cloudflare's "disable direct uploads" setting is the real gate.
# =============================================================================
set -euo pipefail

ENV="${1:-}"
if [[ -z "$ENV" || ! "$ENV" =~ ^(dev|staging|prod)$ ]]; then
  echo "Usage: ./deploy.sh <dev|staging|prod>" >&2
  exit 2
fi

# --- Guard 1: working tree must be clean (no uncommitted changes) -----------
if [[ -n "$(git status --porcelain)" ]]; then
  echo "❌ GUARD 1 FAILED — working tree is dirty. Commit or stash first." >&2
  git status --short >&2
  exit 1
fi

# --- Guard 2: map env -> required branch + CF project -----------------------
case "$ENV" in
  dev)     REQ_BRANCH=main;    PROJECT=beehive-strategy-v2 ;;
  staging) REQ_BRANCH=staging; PROJECT=beehive-strategy-v2-staging ;;
  prod)    REQ_BRANCH=prod;    PROJECT=beehivestrategy ;;
esac

# --- Guard 3: you must be on the env's required branch ----------------------
CUR=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CUR" != "$REQ_BRANCH" ]]; then
  echo "❌ GUARD 3 FAILED — deploy to '$ENV' requires branch '$REQ_BRANCH' (you are on '$CUR')." >&2
  echo "   Fix:  git checkout $REQ_BRANCH" >&2
  exit 1
fi

# --- Guard 4: prod only via promotion (staging must be merged into prod) ----
if [[ "$ENV" == "prod" ]]; then
  if ! git merge-base --is-ancestor staging HEAD; then
    echo "❌ GUARD 4 FAILED — 'staging' is not merged into 'prod'." >&2
    echo "   Flow must be:  main -> staging -> prod." >&2
    exit 1
  fi
  echo "⚠️  PROD DEPLOY requested. Type the exact phrase to confirm:"
  echo -n "    > "
  read -r CONF
  [[ "$CONF" == "DEPLOY-PROD" ]] || { echo "aborted (no confirmation)."; exit 1; }
fi

# --- Deploy (manual fallback; normally CF auto-deploys from the branch) -----
DEPLOY_DIR="${DEPLOY_DIR:-website}"
if ! command -v wrangler >/dev/null 2>&1; then
  echo "❌ wrangler not found. Install: npm i -g wrangler  (or rely on CF git auto-deploy)." >&2
  exit 1
fi

echo "→ Deploying '$ENV' (branch '$CUR') to Cloudflare project '$PROJECT'"
wrangler pages deploy "$DEPLOY_DIR" --project-name "$PROJECT"
echo "✅ Done. Verify: https://$PROJECT.pages.dev  (prod: https://www.beehivestrategy.com)"
