#!/bin/bash
set -euo pipefail

REPO_URL="${SPARTACUS_SKILL_REPO:-https://github.com/tbdavid2019/SAP-spartacus-docs-skill.git}"
SOURCE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${1:-$SOURCE_DIR}"

if [[ -d "$TARGET_DIR/.git" ]]; then
    echo "Updating the skill checkout in $TARGET_DIR..."
    git -C "$TARGET_DIR" pull --ff-only origin main
elif [[ -e "$TARGET_DIR" ]]; then
    if find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -print -quit | grep -q .; then
        echo "Refusing to install: $TARGET_DIR is not an empty directory or git checkout." >&2
        exit 1
    fi
    git clone "$REPO_URL" "$TARGET_DIR"
else
    mkdir -p "$(dirname "$TARGET_DIR")"
    git clone "$REPO_URL" "$TARGET_DIR"
fi

if [[ ! -f "$TARGET_DIR/SKILL.md" ]] || [[ ! -f "$TARGET_DIR/docs/SKILL_INDEX.md" ]]; then
    echo "Installation validation failed: required skill files are missing." >&2
    exit 1
fi

echo "Skill ready in $TARGET_DIR"
