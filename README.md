# SAP Spartacus Documentation Skill (Auto-Sync Version)

> [!IMPORTANT]
> ### 🤖 Instructions for AI Agent Installation / AI 助手安裝指引
>
> **English:** If a user provides you with this repository URL and asks you to "install" or "setup" this skill, follow these steps:
> 1.  **Install via Git Clone**: Run `git clone https://github.com/tbdavid2019/spartacus-docs-skill.git <skill-directory>`.
> 2.  **Updating the Skill**: To update the skill later, navigate to the directory and run `git pull`.
> 3.  **Load Skill Metadata**: Read `SKILL.md` to understand the specialized workflows.
> 4.  **Initialize Context**: **Each time you use this codebase, you MUST `git pull` from the documentation area `docs` to ensure your reference is the newest.** Always consult `docs/SKILL_INDEX.md` first to locate specific documentation files.
> 5.  **Do Not Run Maintenance Scripts During Normal Use**: Do not run `scripts/sync-docs.sh`, `scripts/generate_index.py`, or other repo-maintenance scripts unless explicitly asked to refresh this repository.
> 6.  **Usage**: Any LLM developing SAP Spartacus applications can use this as their main reference material to avoid hallucinations and leverage the exact Spartacus API.
>
> **繁體中文：** 如果使用者提供此倉庫網址並要求你「安裝」或「設定」此技能服務，請遵循以下步驟：
> 1.  **安裝技能指令**：執行 `git clone https://github.com/tbdavid2019/spartacus-docs-skill.git <安裝目標目錄>`。
> 2.  **更新技能**：之後若要更新，請切換至該目錄並執行 `git pull`。
> 3.  **載入技能**：讀取 `SKILL.md` 以了解此技能的工作流程。
> 4.  **初始化環境**：**每次使用前，請務必先執行 `git pull` 確保 `docs` 目錄內的文件是最新的。** 每當需要查詢特定功能或維護指引時，請優先參考 `docs/SKILL_INDEX.md`。
> 5.  **一般使用時不要執行維護腳本**：除非明確要求，否則不要執行 `scripts/sync-docs.sh` 或 `scripts/generate_index.py`。
> 6.  **用途說明**：任何 LLM 在開發 SAP Spartacus 都可以用到這份參考資料，藉此避免幻覺，掌握最新的 Spartacus API 和設定。

---

## What is This?

This is an Agent Skill designed for AI coding assistants (like Claude, Codex, Gemini CLI). It constantly pulls the latest SAP Spartacus storefront documentation from the official upstream repository (`https://github.com/SAP/spartacus-docs/tree/develop/_pages`). 

Once installed, the AI assistant gains up-to-date knowledge of SAP Spartacus and can help you with customizations, SSR issues, state management, layouts, routing, and component overrides based on actual official docs.

## Setup for AI Agents

Provide the repository link to your AI agent and ask it to read the `README.md` and `SKILL.md`. Or, directly install it into your agent's skill directory.

**For OpenClaw:**
```bash
git clone https://github.com/tbdavid2019/spartacus-docs-skill.git ~/.openclaw/skills/spartacus-docs-skill
```

**For Gemini CLI / Antigravity:**
```bash
git clone https://github.com/tbdavid2019/spartacus-docs-skill.git ~/.gemini/antigravity/skills/spartacus-docs
```

**For Claude Code:**
(Add it to your current project space, or prompt Claude to read the global path if you set one up).

## Updating the Documentation

This skill's `docs/` folder is synced from the official Spartacus repository. To get the latest docs automatically:
```bash
sh scripts/sync-docs.sh
```

Or rely on the **Auto-Sync Documentation** workflow in GitHub Actions, which runs every day at 04:00 UTC.
