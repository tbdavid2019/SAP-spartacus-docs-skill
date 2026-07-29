#!/usr/bin/env python3
"""Validate a prepared SAP Spartacus documentation snapshot."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


DEFAULT_REQUIRED_PATHS = (
    "home/compatibility-matrix.md",
    "install/backend/installing-sap-commerce-cloud.md",
    "install/schematics.md",
    "dev/authentication.md",
    "dev/session-management.md",
)
INDEX_LINK = re.compile(r"^- \[.*\]\((.+\.md(?:#[^)]+)?)\)\s*$")
UNRESOLVED_JEKYLL = (
    "{% include",
    "{% link",
    "{{ site.baseurl }}",
    "{{ site.version_note_",
)


class ValidationError(ValueError):
    pass


@dataclass(frozen=True)
class ValidationReport:
    markdown_file_count: int
    indexed_file_count: int
    source_commit: str


def validate_docs(
    docs_dir: Path | str,
    *,
    minimum_markdown_files: int = 300,
    required_paths: Sequence[str] = DEFAULT_REQUIRED_PATHS,
) -> ValidationReport:
    root = Path(docs_dir)
    metadata_path = root / "SOURCE.json"
    index_path = root / "SKILL_INDEX.md"
    if not metadata_path.is_file():
        raise ValidationError(f"missing source metadata: {metadata_path}")
    if not index_path.is_file():
        raise ValidationError(f"missing generated index: {index_path}")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    commit = metadata.get("commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValidationError("SOURCE.json contains an invalid upstream commit")

    markdown_files = sorted(
        path
        for path in root.rglob("*.md")
        if path.name.upper() not in {"INDEX.MD", "SKILL_INDEX.MD"}
    )
    if len(markdown_files) < minimum_markdown_files:
        raise ValidationError(
            f"snapshot has {len(markdown_files)} Markdown files; "
            f"minimum is {minimum_markdown_files}"
        )
    if metadata.get("markdown_file_count") != len(markdown_files):
        raise ValidationError(
            "SOURCE.json markdown_file_count does not match the snapshot"
        )

    missing = [path for path in required_paths if not (root / path).is_file()]
    if missing:
        raise ValidationError(f"missing required documentation: {', '.join(missing)}")

    unresolved: list[str] = []
    for path in markdown_files:
        content = path.read_text(encoding="utf-8")
        if any(token in content for token in UNRESOLVED_JEKYLL):
            unresolved.append(path.relative_to(root).as_posix())
    if unresolved:
        raise ValidationError(
            "unresolved Jekyll instructions remain in: " + ", ".join(unresolved[:10])
        )

    indexed_paths: set[str] = set()
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = INDEX_LINK.match(line)
        if match:
            indexed_paths.add(match.group(1).split("#", 1)[0])
    expected_paths = {path.relative_to(root).as_posix() for path in markdown_files}
    if indexed_paths != expected_paths:
        omitted = sorted(expected_paths - indexed_paths)
        dangling = sorted(indexed_paths - expected_paths)
        raise ValidationError(
            f"index mismatch; omitted={omitted[:10]}, dangling={dangling[:10]}"
        )

    return ValidationReport(
        markdown_file_count=len(markdown_files),
        indexed_file_count=len(indexed_paths),
        source_commit=commit,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docs_dir", type=Path)
    parser.add_argument("--minimum-markdown-files", type=int, default=300)
    args = parser.parse_args()
    report = validate_docs(
        args.docs_dir, minimum_markdown_files=args.minimum_markdown_files
    )
    print(
        "Validated "
        f"{report.markdown_file_count} Markdown files at "
        f"{report.source_commit[:12]}"
    )


if __name__ == "__main__":
    main()
