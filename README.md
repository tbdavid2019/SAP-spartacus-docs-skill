# SAP Spartacus Documentation Skill

An installable agent skill backed by a daily, source-traceable snapshot of the official SAP Spartacus documentation.

The repository prepares the SAP `spartacus-docs` `develop` branch for local LLM use by expanding Jekyll includes, rewriting internal links, generating a deterministic index, and validating the snapshot before it replaces the previous version.

## Install

### npm installation

With Node.js 22.20 or later and Git, run this from your project:

```bash
npx -y sap-spartacus-docs-skill@latest
```

The default target is Codex at `.agents/skills/spartacus-docs`. Use `--global` for a user installation or `--agent openclaw` to select OpenClaw. Re-run the same command with the same options to update the installed snapshot. The npm package fetches the validated GitHub `main` snapshot and reports its skill and upstream commits.

### Git checkout installation

Use the canonical repository URL and install it into a directory named `spartacus-docs`, matching the skill name.

### Codex

```bash
git clone https://github.com/tbdavid2019/SAP-spartacus-docs-skill.git \
  ~/.codex/skills/spartacus-docs
bash ~/.codex/skills/spartacus-docs/scripts/install-skill.sh
```

### OpenClaw

```bash
git clone https://github.com/tbdavid2019/SAP-spartacus-docs-skill.git \
  ~/.openclaw/skills/spartacus-docs
bash ~/.openclaw/skills/spartacus-docs/scripts/install-skill.sh
```

### Gemini CLI / Antigravity

```bash
git clone https://github.com/tbdavid2019/SAP-spartacus-docs-skill.git \
  ~/.gemini/antigravity/skills/spartacus-docs
bash ~/.gemini/antigravity/skills/spartacus-docs/scripts/install-skill.sh
```

The installer updates an existing git checkout, clones into a new or empty target, rejects occupied non-git directories, and verifies that `SKILL.md` and the documentation index exist.

## AI Agent Installation Contract

When a user asks an AI agent to install this repository:

1. Identify the agent and installation scope. For a new npm installation, run `npx -y sap-spartacus-docs-skill@latest` with the appropriate options.
2. Update an existing installation with its original method. For a Git checkout, clone if needed and run `scripts/install-skill.sh` from the installed checkout.
3. Read the installed `SKILL.md` and check `docs/SOURCE.json`, `docs/SKILL_INDEX.md`, and `references/task-map.md`.
4. Report the installed path and both commits. Use the local snapshot for ordinary questions and run repository-maintenance tools only when maintaining this repository.

## 中文安裝說明

需要 Node.js 22.20 以上與 Git。在專案目錄執行：

```bash
npx -y sap-spartacus-docs-skill@latest
```

預設安裝到 `.agents/skills/spartacus-docs`。可加 `--global` 全域安裝，或用 `--agent openclaw` 指定宿主。npm 安裝後，重跑相同指令與選項即可取得 GitHub 上的新快照。既有 Git checkout 請沿用 `scripts/install-skill.sh` 更新。平常查詢直接使用本機文件。

已知主題可從 `SKILL.md` 或 `references/task-map.md` 直達相關文件，需要探索目錄時再查 `docs/SKILL_INDEX.md` 的對應章節。

## Snapshot Model

- Upstream: `https://github.com/SAP/spartacus-docs.git`
- Branch: `develop`
- Schedule: daily at 04:00 UTC; GitHub may start scheduled jobs later
- Provenance: `docs/SOURCE.json`
- Navigation: `docs/SKILL_INDEX.md`
- Validation: required core pages, complete index coverage, valid source SHA, no unresolved Jekyll includes/links, no trailing whitespace, and consistent Markdown file metadata

A daily snapshot can lag upstream by up to one synchronization cycle. It is not a real-time mirror.

## Maintainer Commands

Normal skill users should not run these commands. Repository maintainers can refresh and verify the snapshot with:

```bash
sh scripts/sync-docs.sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_docs.py docs
```

The synchronization flow clones into an isolated staging directory, prepares and validates the complete snapshot, then promotes it. A fetch, transformation, or validation failure leaves the existing `docs/` directory unchanged.

### Release the npm installer

The daily GitHub sync publishes documentation snapshots. To release a new installer, update `package.json` and the lockfile, then prepare the matching `v<version>` tag. For the first release, locally test `npm pack` and publish the tarball with `npm publish <tarball> --access public`. For later releases, configure npm Trusted Publishing for `publish-npm.yml` when ready to publish, then push the tag. The first OIDC publish must succeed within two days of adding the trust configuration.

## License

Repository-authored automation and skill instructions are licensed under [AGPL-3.0](LICENSE).

Synchronized SAP Spartacus documentation remains under its upstream Apache-2.0 terms. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and `docs/UPSTREAM_LICENSE.txt`.
