# Deploy Policy — beehivestrategy.com (HARD RULE)

> **Last updated: 2026-11-15 23:24 HKT** | Status: **PROD 已上线**，git + CI 路径全绿

## ✅ 当前状态（2026-11-15 23:24 HKT 实测，优先级高于下文一切描述）

- **本文件是部署流程的唯一权威**：`git push origin <branch>` → `.github/workflows/deploy-cloudflare.yml` → 对应 Cloudflare Pages 项目（`main`=dev / `staging`=staging / `prod`=PROD）。
  Obsidian《Website Deployment — Cloudflare Pages (SSOT)》2026-09-24 版曾写「没有 deploy workflow / push 不会部署」，**该说法已实测证伪并于 2026-11-15 校正**；`~/.workbuddy-ai/skills/beehive-cloudflare-deploy/SKILL.md` 同样已校正。
- **2026-11-15 Kenneth 逐字授权 `DEPLOY-PROD`**，按硬规则 `main → staging → prod` 完成晋升：
  - staging `705c543c8`（run `43729439940` SUCCESS）→ prod `39d937b83`（run `43729600832` SUCCESS）
  - PROD deployment **`71c3370d-d3c7-4fe7-a1cd-81f10316355c`** / commit `39d937b83d` / 2026-11-15T15:24Z
  - 线上 `https://www.beehivestrategy.com` = `accenture.css?v=20261114.03`，与 dev 首页 SHA 完全一致；三语 / 核心页 / SEO 端点全 200；sitemap 3,665 URLs；`/pricing` 301→`/contact`
- **回滚基线**：deployment `2fdc7154-dd3b-4691-b61d-62b2e0453d51`（commit `6c5246e539`，2026-10-04，`styles.css?v=20260830`）；本地备份分支 `backup/pre-prod-deploy-20261115` → `77353ca45`。
- **CI 凭据已修复**：repo secret `CLOUDFLARE_API_TOKEN` 已写入（共 4 个 secret）；Cloudflare token `WorkBuddy Cloudflare Token` 权限 = `Account.Cloudflare Pages : Edit + Zone.DNS`，token 值未变（`/user/tokens/verify` active、`/accounts/…/pages/projects` 200）。
- 部署前门禁：`verify_v4` **27/27**、`verify_site` **3,676 页 ALL PASS**（含 SEO/GEO 闸门 #9）。
- CI 部署目录是 **`website/`**；`website_deploy_clean/`（未纳入 git、401 MB、停留在 2026-10-15）已弃用，**不得作为部署源**。
- ⚠️ Cloudflare API 列 Pages 项目时**不要带 `per_page` 参数**（会返回 400 `8000024 Invalid list options`）。
- 剩余人工项：Cloudflare Dashboard `Security → Bots → AI Crawl Control → Bots = DISABLED`（GEO 放行 AI 爬虫）。
- 🔴 后续任何 PROD 部署仍须 Kenneth 逐字说 `DEPLOY-PROD`；自动化通知、沉默或推测均不等于授权。
- 🔴 **三语同步铁律（Kenneth 2026-11-16：「when ever we update we update all 3 languages」）**：任何页面 / 内容更新必须**同批覆盖 EN / zh-CN / zh-HK**，只改一语视为未完成。部署前必跑 `python3 _v4/verify_site.py` —— Gate 10 从磁盘派生公开页注册表、比对三语 `<main>` 结构签名，并用 `git diff` 硬拦「本次更新只动了一语」；历史漂移登记在 `TRILINGUAL_LEGACY_EXEMPT` 并逐页清零。补齐工具 `_v4/trilingual_apply.py`。跨午夜更新后须重建 `sitemap*.xml` + `llms.txt`（否则 lastmod 被判陈旧）。

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
