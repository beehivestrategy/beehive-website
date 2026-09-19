#!/usr/bin/env bash
# =============================================================================
# deploy.sh — HARD-RULE ENFORCER for beehivestrategy.com
# -----------------------------------------------------------------------------
# Cloudflare reality (verified 2026-09-19):
#   - All 3 Pages projects are Direct-Upload with production branch = `main`.
#   - Routing is by PROJECT NAME, not git branch. `--branch main` marks a
#     production deploy; any other branch value becomes a Preview.
#   - Projects:  dev=beehive-strategy-v2 | staging=beehive-strategy-v2-staging
#                | prod=beehive-strategy  (serves beehivestrategy.com)
#
# Promotion discipline (the "hard rule"): content must pass through
#   dev  ->  staging  ->  prod, in that order. prod requires typing DEPLOY-PROD.
# Nothing is uploaded from a dirty tree.
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

# --- Map env -> Cloudflare project ------------------------------------------
case "$ENV" in
  dev)     PROJECT=beehive-strategy-v2 ;;
  staging) PROJECT=beehive-strategy-v2-staging ;;
  prod)    PROJECT=beehive-strategy ;;
esac

# --- Guard 2: prod only via explicit confirmation ---------------------------
if [[ "$ENV" == "prod" ]]; then
  echo "⚠️  PROD DEPLOY requested (project: $PROJECT => beehivestrategy.com)."
  echo "    Type the exact phrase to confirm:"
  echo -n "    > "
  read -r CONF
  [[ "$CONF" == "DEPLOY-PROD" ]] || { echo "aborted (no confirmation)."; exit 1; }
fi

# --- Deploy (always --branch main => production on these projects) ----------
DEPLOY_DIR="${DEPLOY_DIR:-website}"
if ! command -v wrangler >/dev/null 2>&1; then
  echo "❌ wrangler not found. Install: npm i -g wrangler" >&2
  exit 1
fi

echo "→ Deploying '$ENV' to Cloudflare project '$PROJECT' (production)"
wrangler pages deploy "$DEPLOY_DIR" --project-name "$PROJECT" --branch main --commit-dirty
echo "✅ Done. Verify:"
case "$ENV" in
  dev)     echo "   https://beehive-strategy-v2.pages.dev" ;;
  staging) echo "   https://beehive-strategy-v2-staging.pages.dev" ;;
  prod)    echo "   https://www.beehivestrategy.com" ;;
esac
