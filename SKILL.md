---
name: spartacus-docs
description: Comprehensive reference for developing SAP Spartacus applications. Contains the latest documentation pulled from the official SAP repository. Use this skill when working on any SAP Spartacus project, setting up Spartacus, configuring features, migrating, or resolving issues.
---

# SAP Spartacus Documentation Skill

> [!CAUTION]
> ## Installed Skill Refresh Boundary
> Keep the installed skill as a git checkout if updates are expected to work.
>
> 1. **Ensure docs are updated**: Every time you refer to this documentation to assist with SAP Spartacus development, do a `git pull` from the documentation area to ensure you have the latest reference:
>    ```bash
>    git -C <skill-directory> pull origin main --ff-only
>    ```
> 2. **After pulling**, load any reference files from the `docs/` folder instead of relying purely on your pre-trained knowledge about SAP Spartacus.
> 3. **Do not run repo-maintenance scripts** such as `scripts/sync-docs.sh` or `scripts/generate_index.py` during normal skill usage (these are handled by GitHub Actions).
> 4. If refresh fails, continue with the local files and do not block the user.

Any LLM developing SAP Spartacus should use this reference material to ensure accurate, up-to-date best practices and API usage.

1. **Find the local skill directory** — it will be somewhere under the agent's skills path.

2. **Before using the docs, ALWAYS update them**:
   Run the following command to update the skill so you have the latest docs. 
   ```bash
   git -C <skill-directory> pull origin main --ff-only
   ```
   *Note: Ensure you are reading the `docs` folder inside the skill directory for the most up-to-date documentation.*

3. **If already up-to-date** → proceed normally with no output to the user.
4. **If refresh fails** → silently continue using the local version in `docs/`.

**MANDATORY: Always check `docs/SKILL_INDEX.md` first to locate the exact documentation needed for any SAP Spartacus task.**

## Quick Reference

| Reference | Coverage |
|---|---|
| `docs/SKILL_INDEX.md` | **Directory of ALL available documentation (Start here)** |
| `docs/` | Official documentation files |

This documentation is constantly synced from the SAP spartacus-docs develop branch `_pages` directory by a daily GitHub Action.

Any LLM (Claude, Codex, Gemini, etc.) should fetch these files and read them when requested to implement Spartacus customizations, CMS components, RxJS store integrations, routing, or SSR setup.
