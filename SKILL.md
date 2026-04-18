---
name: spartacus-docs
description: Comprehensive reference for developing SAP Spartacus applications. Contains synced official docs plus a task workflow for setup, SAP Commerce/Hybris integration, version checks, authentication, CORS, migration, and troubleshooting.
---

# SAP Spartacus Documentation Skill

Use this skill for any SAP Spartacus or Composable Storefront task: fresh setup, SAP Commerce/Hybris integration, feature configuration, routing, CMS customization, authentication, SSR, migration, or production issues.

## Refresh Boundary

Keep the installed skill as a git checkout if updates are expected to work.

1. Find the local skill directory.
2. Before using the docs, update the skill:
   ```bash
   git -C <skill-directory> pull origin main --ff-only
   ```
3. After pulling, read from the local `docs/` folder instead of relying on model memory.
4. Do not run repo-maintenance scripts such as `scripts/sync-docs.sh` or `scripts/generate_index.py` during normal usage.
5. If refresh fails, continue with the local files and do not block the user.

## Required Entry Point

Always check `docs/SKILL_INDEX.md` first to locate the exact documentation needed.

If the task is about setup, integration, or production errors, do not answer from one file alone. Read the relevant files from the lookup map below and then synthesize.

## Core Lookup Map

Use these files first for common tasks:

| Task | Start Here |
| --- | --- |
| Find the right doc | `docs/SKILL_INDEX.md` |
| Version compatibility | `docs/home/compatibility-matrix.md` |
| Fresh storefront install | `docs/install/frontend/building-the-spartacus-storefront-from-libraries.md` |
| Schematics / `ng add` | `docs/install/schematics.md` |
| SAP Commerce / Hybris backend setup | `docs/install/backend/installing-sap-commerce-cloud.md` and version pages under `docs/install/backend/` |
| CORS | `docs/install/cors.md` |
| OCC base URL | `docs/dev/configuring-base-url.md` |
| Authentication | `docs/dev/authentication.md` and `docs/dev/session-management.md` |
| SSR | files under `docs/dev/ssr/` |
| Migrations / 2211 updates | files under `docs/home/updating-to-version-*` |

## Working Rules

1. Prefer the local docs over model memory if there is any conflict.
2. When the docs are version-specific, repeat the exact version in the answer.
3. If the docs do not contain a direct page for the user's exact version or scenario, say that you are making a constrained inference from the nearest official pages.
4. For install or integration questions, explicitly separate:
   - facts directly supported by the local docs
   - inferences based on adjacent versions or related docs
5. When troubleshooting, give the user a validation sequence, not just a pile of references.

## Workflow For Setup And SAP Commerce/Hybris Integration

Use this flow for any question like "install Spartacus", "connect Hybris", "wire SAP Commerce", "why does login fail", or "why is OCC not working".

1. Identify the exact versions first:
   - SAP Commerce / Hybris version
   - Spartacus version
   - Angular version if relevant
   - whether the backend is `2211.xx` or `2211-jdk21.x`
2. Read `docs/home/compatibility-matrix.md` before recommending package versions or feature setup.
3. Read the relevant backend install page under `docs/install/backend/`.
4. Read `docs/install/frontend/building-the-spartacus-storefront-from-libraries.md` and `docs/install/schematics.md`.
5. Read `docs/install/cors.md` and `docs/dev/configuring-base-url.md`.
6. If login, registration, guest checkout, ASM, or token issues are involved, also read `docs/dev/authentication.md` and `docs/dev/session-management.md`.
7. Answer in this order:
   - version alignment
   - backend readiness
   - OCC reachability
   - frontend install
   - auth setup
   - CORS
   - validation steps

## Mandatory Version Split For 2211 Authentication

Do not treat all `2211` installs the same.

### If the backend is `2211.xx`

- Read `docs/dev/authentication.md` and `docs/dev/session-management.md`.
- Treat this as the legacy 2211 line unless the docs clearly indicate `jdk21`.
- Resource Owner Password Flow may still be required.
- If using legacy SAP Commerce 2211 authentication, the docs state that `authorizationCodeFlowByDefault` must be set to `false`.

### If the backend is `2211-jdk21.1` or newer

- Read `docs/dev/authentication.md` and `docs/dev/session-management.md`.
- Authorization Code Flow is the default direction.
- The docs state that the client credentials used with Spartacus should be set to `Public`.
- Be careful not to recommend the older `client_secret` pattern as the default unless the docs for that exact setup require it.

## Troubleshooting Order

When the user reports a broken setup, check these in order:

1. Version mismatch between Spartacus and SAP Commerce.
2. Backend actually starts and OCC endpoints respond.
3. Correct `baseSite`, `occPrefix`, and `baseUrl`.
4. OAuth flow and client type match the Commerce version.
5. CORS headers, methods, and credentials settings.
6. Only then investigate storefront code, SSR, or feature-module issues.

## Minimum Questions To Ask When Context Is Missing

If the user asks for install or integration help and the context is missing, request these specifics early:

- Exact SAP Commerce version
- Exact Spartacus version
- Exact base site
- Whether they use SAP Commerce auth or an external IdP
- Whether the problem is fresh install, migration, or runtime failure

## Output Style

For implementation guidance:

1. Give a short diagnosis of the situation.
2. Provide an ordered step-by-step plan.
3. Name the local docs used.
4. Call out any version-dependent branches explicitly.
5. For production issues, end with the next concrete verification step.

This repo is synced from the SAP `spartacus-docs` documentation source. Use it as the primary factual base whenever you answer Spartacus questions.
