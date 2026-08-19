#!/bin/sh
set -eu

# Build and promote a validated snapshot of the official SAP documentation.

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=${SPARTACUS_SKILL_ROOT:-$(dirname "$SCRIPT_DIR")}
REPO_URL=${SPARTACUS_UPSTREAM_REPO:-https://github.com/SAP/spartacus-docs.git}
SOURCE_BRANCH=${SPARTACUS_UPSTREAM_BRANCH:-develop}
FORCE_SYNC=${SPARTACUS_FORCE_SYNC:-0}
DEST_DOCS="$REPO_ROOT/docs"
WORK_DIR=$(mktemp -d "$REPO_ROOT/.sync-work.XXXXXX")
UPSTREAM_DIR="$WORK_DIR/upstream"
STAGED_DOCS="$WORK_DIR/docs"
BACKUP_DOCS="$WORK_DIR/previous-docs"

cleanup() {
    if [ -d "$BACKUP_DOCS" ] && [ ! -d "$DEST_DOCS" ]; then
        mv "$BACKUP_DOCS" "$DEST_DOCS"
    fi
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT HUP INT TERM

validate_snapshot() {
    python3 "$SCRIPT_DIR/validate_docs.py" "$1"
}

echo "Fetching SAP Spartacus documentation from $SOURCE_BRANCH..."
git clone \
    --depth 1 \
    --filter=blob:none \
    --sparse \
    --branch "$SOURCE_BRANCH" \
    "$REPO_URL" \
    "$UPSTREAM_DIR"
git -C "$UPSTREAM_DIR" sparse-checkout set --skip-checks \
    _pages \
    _includes/docs \
    _data \
    LICENSE.txt

SOURCE_COMMIT=$(git -C "$UPSTREAM_DIR" rev-parse HEAD)
SOURCE_COMMITTED_AT=$(git -C "$UPSTREAM_DIR" show -s --format=%cI HEAD)

if [ "$FORCE_SYNC" != "1" ] && [ -f "$DEST_DOCS/SOURCE.json" ]; then
    CURRENT_COMMIT=$(
        python3 -c \
            'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get("commit", ""))' \
            "$DEST_DOCS/SOURCE.json"
    )
    if [ "$CURRENT_COMMIT" = "$SOURCE_COMMIT" ]; then
        validate_snapshot "$DEST_DOCS"
        echo "Documentation is already at upstream commit ${SOURCE_COMMIT%????????????????????????????}."
        exit 0
    fi
fi

SYNCED_AT=$(date -u "+%Y-%m-%dT%H:%M:%SZ")
python3 "$SCRIPT_DIR/prepare_docs.py" \
    --pages-dir "$UPSTREAM_DIR/_pages" \
    --includes-dir "$UPSTREAM_DIR/_includes/docs" \
    --data-dir "$UPSTREAM_DIR/_data" \
    --output-dir "$STAGED_DOCS" \
    --source-repo "$REPO_URL" \
    --source-branch "$SOURCE_BRANCH" \
    --source-commit "$SOURCE_COMMIT" \
    --source-committed-at "$SOURCE_COMMITTED_AT" \
    --synced-at "$SYNCED_AT" \
    --upstream-license "$UPSTREAM_DIR/LICENSE.txt"

python3 "$SCRIPT_DIR/generate_index.py" "$STAGED_DOCS"
validate_snapshot "$STAGED_DOCS"

if [ -d "$DEST_DOCS" ]; then
    mv "$DEST_DOCS" "$BACKUP_DOCS"
fi

if ! mv "$STAGED_DOCS" "$DEST_DOCS"; then
    if [ -d "$BACKUP_DOCS" ]; then
        mv "$BACKUP_DOCS" "$DEST_DOCS"
    fi
    echo "Failed to promote the validated documentation snapshot." >&2
    exit 1
fi

FILE_COUNT=$(find "$DEST_DOCS" -type f -name "*.md" ! -name "SKILL_INDEX.md" | wc -l)
echo "Promoted upstream commit ${SOURCE_COMMIT%????????????????????????????} with $FILE_COUNT Markdown files."
