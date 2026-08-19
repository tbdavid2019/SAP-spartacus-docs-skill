# Changelog

## 2026-08-19

### Fixed

- Upgraded `actions/setup-python` from v5 to v7 so the workflow uses the Node.js 24 runtime and no longer emits the Node.js 20 deprecation warning.
- Removed the arbitrary default requirement for at least 300 Markdown files; synchronization now relies on required-page, index, link, and metadata validation while retaining an optional explicit minimum for manual checks.

## 2026-07-29

### Fixed

- Corrected every installation example to use the canonical `tbdavid2019/SAP-spartacus-docs-skill` repository.
- Replaced the destructive in-place sync with a fail-fast staged workflow that validates before promotion and restores the previous snapshot on failure.
- Removed the invalid `.tmp_repo` gitlink and ignored temporary synchronization directories and generated Python cache files.
- Changed the installer to clone new targets, update git checkouts, reject occupied non-git directories, and verify required skill files.
- Eliminated daily timestamp-only commits by recording and comparing the upstream commit.
- Kept integrity checks active even when the upstream commit is unchanged.

### Added

- Added `docs/SOURCE.json` with the upstream repository, branch, commit, commit time, sync time, file count, and transformation description.
- Added deterministic expansion of Jekyll version notes, frontend requirements, feature compatibility data, event tables, internal links, and asset URLs.
- Added automatic repair of locally resolvable Markdown links, official-site fallbacks for removed pages, and broken-link validation.
- Added an Apache-2.0 license copy and third-party attribution for synchronized SAP documentation.
- Added a source-level transformation notice to every prepared upstream Markdown file.
- Added unit and integration tests for rendering, indexing, validation, installer failure behavior, and preservation of the current snapshot after synchronization failure.
- Added CI concurrency and timeout controls, immutable official action revisions, tests before synchronization, and native git commit logic.
- Added broader LLM task routing, source provenance rules, deprecation checks, safety boundaries, answer requirements, and an OpenAI skill interface definition.

### Updated

- Refreshed the documentation snapshot to SAP upstream commit `6b0a1aaf17e6eb6443ab861d5bb7db9fa7205aab`.
- Added the upstream `221121.17` SNOW fix page.
- Generated complete local feature compatibility and event tables.
