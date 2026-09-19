# Deploy Policy — beehivestrategy.com (HARD RULE)

> **Last updated: 2026-09-19** | Status: enforced via git + CI + Cloudflare settings

## The rule (no exceptions)

**Git is the single source of truth. Nothing reaches any environment except through a
git push to the correct branch. No manual `wrangler pages deploy` from a laptop working
tree. No deploying uncommitted files.**

```
        main ──push──▶ dev      (CF: beehive-strategy-v2)
                         │
        staging ─push──▶ staging  (CF: beehive-strategy-v2-staging)
                         │
        prod ──push───▶ prod     (CF: beehive-strategy)
```

Promotion order is **main → staging → prod**. `prod` only ever receives a merge from
`staging`, so content cannot reach production without first passing staging.

> **Cloudflare reality (verified 2026-09-19):** all three Pages projects are
> Direct-Upload with **production branch = `main`**. Routing is by **project name**,
> not git branch — every deploy uses `wrangler pages deploy . --project-name <X>
> --branch main`. The git branch only selects *which project* the CI deploys to.

## How it is enforced (3 layers)

1. **Cloudflare Pages setting** — in each project's dashboard, turn **OFF
   "Allow direct uploads"**. This makes `wrangler pages deploy` from a laptop impossible;
   the only deploy path is git. *(This is the real gate — set it once.)*
2. **GitHub Actions** (`.github/workflows/deploy-cloudflare.yml`) — pushes to `main` /
   `staging` / `prod` auto-deploy to the matching project. Fully observable in the Actions tab.
3. **Local guard** (`deploy.sh`) — refuses to run if the working tree is dirty, if you're on
   the wrong branch, or if `staging` isn't merged into `prod`. Belt-and-suspenders.

## Required GitHub secrets

- `CLOUDFLARE_API_TOKEN` (Pages: Edit permission)
- `CLOUDFLARE_ACCOUNT_ID`

## Daily workflow

```bash
# 1. Develop / regenerate content on main, then commit + push
git add -A && git commit -m "..." && git push origin main      # → dev auto-deploys

# 2. Promote to staging
git checkout staging && git merge main && git push origin staging   # → staging deploys

# 3. Promote to prod (explicit)
git checkout prod && git merge staging && git push origin prod       # → prod deploys
git checkout main
```

Manual fallback (only if CF git auto-deploy is off): `bash website/_batch_pipeline/deploy.sh <dev|staging|prod>`
— must be on the matching branch, tree clean, and (for prod) type `DEPLOY-PROD`.

## Aligning the 3 environments RIGHT NOW (2026-09-19)

Current state: `main` = `staging` = `prod` (git) = commit `c542f049`. But **all 3 live
sites are stale** vs git (prod is missing the 09-19 article; dev/staging are pre-V2).
To bring every environment to the git truth:

```bash
# dev  — already triggered by pushing this policy; or:
git push origin main                                  # → dev deploys c542f049

# staging
git checkout staging && git merge main && git push origin staging   # → staging deploys

# prod (NEEDS EXPLICIT GO — PROD lock)
git checkout prod && git merge staging && git push origin prod       # → prod deploys
git checkout main
```

## Recovered local work

The 47 recap edits that diverged from `origin/main` (longer local regen) are preserved in
branch **`kenneth-local-recap-edits`** (`ffebc750`) — recoverable, not lost. To revive:
`git checkout kenneth-local-recap-edits`, resolve conflicts vs `main`, then promote through
staging. Do NOT merge them blindly — they conflict with the live short recaps.
