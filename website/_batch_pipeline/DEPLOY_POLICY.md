# Deploy Policy — beehivestrategy.com (HARD RULE)

> **Last updated: 2026-11-15** | Status: git + CI 路径已验证；⚠️ 当前被 CI 凭据阻塞

## 🔴 当前状态（2026-11-15 实测，优先级高于下文一切描述）

- **本文件是部署流程的唯一权威**：`git push origin main` → `.github/workflows/deploy-cloudflare.yml` → Cloudflare Pages `beehive-strategy-v2`（dev）。
  Obsidian《Website Deployment — Cloudflare Pages (SSOT)》2026-09-24 版曾写「没有 deploy workflow / push 不会部署」，**该说法已实测证伪并于 2026-11-15 校正**；`~/.workbuddy-ai/skills/beehive-cloudflare-deploy/SKILL.md` 同样已校正。
- `main` 内容已就位：`085bd8a09`，`verify_v4` 27/27、`verify_site` 3,673 页 ALL PASS（含新增 SEO/GEO 闸门）。
- **唯一阻塞**：workflow 引用 `secrets.CLOUDFLARE_API_TOKEN`，仓库实测只有 `CLOUDFLARE_ACCOUNT_ID` / `DEVTO_API_KEY` / `OPENROUTER_API_KEY`。run `43603297094` 因 wrangler `In a non-interactive environment, it's necessary to set a CLOUDFLARE_API_TOKEN` 失败。
- 本机 `~/.workbuddy/cloudflare_api_token` active 但 **DNS-only**（`/user`、`/accounts`、`/pages/projects`、`wrangler pages deploy` 全 403）；本机 wrangler OAuth 已过期；故**不能直接本机上传绕过**。
- 修复：Cloudflare Dashboard → My Profile → API Tokens → 给现有 token 加 `Account → Cloudflare Pages : Edit`，或新建同权限 token 并写入 `CLOUDFLARE_API_TOKEN` secret，然后 `gh run rerun 43603297094`。**写 GitHub secret 属于写账号，须 Kenneth 逐字授权。**
- CI 部署目录是 **`website/`**；`website_deploy_clean/`（未纳入 git、401 MB、停留在 2026-10-15）已弃用，**不得作为部署源**。
- 🔴 PROD 仍需 Kenneth 逐字说 `DEPLOY-PROD`；`staging` / `prod` 分支本轮完全未碰。

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
   > ⚠️ 2026-11-15 补注：本机直传实测是在**鉴权层**被 403 拒绝（DNS-only token），
   > 说明该 Dashboard 开关是否真的已关尚未被独立验证。**不要把「403」误读成「直传已禁用」**；
   > 在 token 拿到 Pages:Edit 后需重新确认开关状态，否则 CI 与手动上传会同时可用。
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
