# SAP Spartacus Documentation Skill

An installable agent skill backed by a daily, source-traceable snapshot of the official SAP Spartacus documentation.

The repository prepares the SAP `spartacus-docs` `develop` branch for local LLM use by expanding Jekyll includes, rewriting internal links, generating a deterministic index, and validating the snapshot before it replaces the previous version.

## Install

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

1. Clone the canonical URL into the agent's skill directory using the final folder name `spartacus-docs`.
2. Run `scripts/install-skill.sh` from the installed checkout.
3. Read `SKILL.md`.
4. Confirm that `docs/SOURCE.json` and `docs/SKILL_INDEX.md` exist.
5. Do not run repository-maintenance scripts during installation or ordinary skill use.

Do not claim installation success after copying files into a non-git directory. Installed copies receive later daily snapshots only after `git pull` or rerunning the installer.

## 中文安裝說明

請使用正確的 canonical URL，並把最終 skill 目錄命名為 `spartacus-docs`：

```bash
git clone https://github.com/tbdavid2019/SAP-spartacus-docs-skill.git \
  <你的-agent-skills目錄>/spartacus-docs
bash <你的-agent-skills目錄>/spartacus-docs/scripts/install-skill.sh
```

安裝後請讓 LLM 讀取 `SKILL.md`，並以 `docs/SOURCE.json` 與 `docs/SKILL_INDEX.md` 作為來源版本和文件導航入口。

來源 repo 每日同步，不代表已安裝的 checkout 會自動更新。已安裝版本需執行 `git pull --ff-only` 或重新執行 installer。

## Snapshot Model

- Upstream: `https://github.com/SAP/spartacus-docs.git`
- Branch: `develop`
- Schedule: daily at 04:00 UTC; GitHub may start scheduled jobs later
- Provenance: `docs/SOURCE.json`
- Navigation: `docs/SKILL_INDEX.md`
- Validation: at least 300 Markdown files, required core pages, complete index coverage, valid source SHA, no unresolved Jekyll includes/links, and no trailing whitespace

A daily snapshot can lag upstream by up to one synchronization cycle. It is not a real-time mirror.

## Maintainer Commands

Normal skill users should not run these commands. Repository maintainers can refresh and verify the snapshot with:

```bash
sh scripts/sync-docs.sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_docs.py docs
```

The synchronization flow clones into an isolated staging directory, prepares and validates the complete snapshot, then promotes it. A fetch, transformation, or validation failure leaves the existing `docs/` directory unchanged.

## License

Repository-authored automation and skill instructions are licensed under [AGPL-3.0](LICENSE).

Synchronized SAP Spartacus documentation remains under its upstream Apache-2.0 terms. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and `docs/UPSTREAM_LICENSE.txt`.
