#!/usr/bin/env python3
"""Prepare a self-contained, LLM-readable Spartacus documentation snapshot."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


OFFICIAL_SITE = "https://sap.github.io/spartacus-docs"
TRANSFORMATION_NOTICE = (
    "<!-- Mechanically prepared from SAP/spartacus-docs under Apache-2.0; "
    "Jekyll directives and links were normalized. See docs/SOURCE.json and "
    "docs/UPSTREAM_LICENSE.txt in the skill root. -->"
)
CAPTURED_VERSION_NOTE = re.compile(
    r"{%\s*capture\s+version_note\s*%}\s*"
    r"(.*?)"
    r"\s*{%\s*endcapture\s*%}\s*"
    r"{%\s*include\s+docs/feature_version\.html\s+content=version_note\s*%}",
    re.DOTALL,
)
LINKED_PAGE_TITLE = re.compile(
    r'{%\s*assign\s+linkedpage\s*=\s*site\.pages\s*\|\s*where:\s*"name",\s*'
    r'"([^"]+)"\s*%}\s*{{\s*linkedpage\[0\]\.title\s*}}'
)
JEKYLL_PAGE_LINK = re.compile(
    r"{{\s*site\.baseurl\s*}}{%\s*link\s+_pages/([^%]+?)\s*%}"
)
LOCAL_MARKDOWN_LINK = re.compile(
    r"(\[[^\]]*\]\()([^) \t]+\.md(?:#[^)]*)?)(\))"
)
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


@dataclass(frozen=True)
class Feature:
    name: str
    spa_version: str
    cx_version: str
    path: str
    anchor: str = ""


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _extract_title(content: str, path: Path) -> str:
    match = FRONTMATTER.search(content)
    if match:
        for line in match.group(1).splitlines():
            key, separator, value = line.partition(":")
            if separator and key.strip() == "title" and value.strip():
                return _unquote(value)
    heading = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if heading:
        return heading.group(1).strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def _extract_features(content: str, relative_path: str) -> list[Feature]:
    match = FRONTMATTER.search(content)
    if not match:
        return []

    features: list[Feature] = []
    current: dict[str, str] | None = None
    in_features = False
    for line in match.group(1).splitlines():
        if re.match(r"^feature\s*:\s*$", line):
            in_features = True
            continue
        if in_features and line and not line[0].isspace() and not line.startswith("-"):
            break
        item = re.match(r"^\s*-\s+name\s*:\s*(.+?)\s*$", line)
        if item:
            if current:
                features.append(_feature_from_mapping(current, relative_path))
            current = {"name": _unquote(item.group(1))}
            continue
        field = re.match(
            r"^\s+(spa_version|cx_version|anchor)\s*:\s*(.*?)\s*$", line
        )
        if current is not None and field:
            current[field.group(1)] = _unquote(field.group(2))
    if current:
        features.append(_feature_from_mapping(current, relative_path))
    return features


def _feature_from_mapping(values: dict[str, str], relative_path: str) -> Feature:
    return Feature(
        name=values["name"],
        spa_version=values.get("spa_version", "n/a"),
        cx_version=values.get("cx_version", "n/a"),
        path=relative_path,
        anchor=values.get("anchor", ""),
    )


def _escape_table(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ").strip()


def _feature_table(features: list[Feature], from_directory: Path) -> str:
    lines = [
        "| Feature | Spartacus Version | Commerce Cloud Version |",
        "| --- | ---: | ---: |",
    ]
    for feature in sorted(features, key=lambda item: item.name.casefold()):
        relative_path = Path(
            os.path.relpath(feature.path, start=from_directory)
        ).as_posix()
        target = f"{relative_path}{feature.anchor}"
        lines.append(
            f"| [{_escape_table(feature.name)}]({target}) "
            f"| {_escape_table(feature.spa_version)} "
            f"| {_escape_table(feature.cx_version)} |"
        )
    return "\n".join(lines)


def _events_table(events_path: Path) -> str:
    if not events_path.is_file():
        raise ValueError(f"missing events data: {events_path}")
    lines = ["| Event | File Path |", "| --- | --- |"]
    with events_path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            lines.append(
                f"| {_escape_table(row['name'])} | `{_escape_table(row['path'])}` |"
            )
    return "\n".join(lines)


def _render_version_note(match: re.Match[str]) -> str:
    note = match.group(1)
    replacements = {
        "{{ site.version_note_part1 }}": "This feature is introduced with version",
        "{{ site.version_note_part1a }}": (
            "This functionality is introduced with version"
        ),
        "{{ site.version_note_part2 }}": "of the Spartacus libraries.",
        "{{ site.version_note_forTUA }}": "of the TUA Spartacus libraries.",
    }
    for source, replacement in replacements.items():
        note = note.replace(source, replacement)
    note = " ".join(note.split())
    return f"> **Note:** {note}"


def _relative_page_link(current_path: Path, pages_dir: Path, target: str) -> str:
    target_path = pages_dir / target.strip()
    return Path(os.path.relpath(target_path, start=current_path.parent)).as_posix()


def _repair_local_markdown_link(
    match: re.Match[str],
    current_path: Path,
    pages_dir: Path,
    page_paths_by_name: dict[str, list[Path]],
) -> str:
    target_with_anchor = match.group(2)
    if target_with_anchor.startswith(("http://", "https://")):
        return match.group(0)
    target, separator, anchor = target_with_anchor.partition("#")
    candidate = (
        pages_dir / target.lstrip("/")
        if target.startswith("/")
        else current_path.parent / target
    )
    if candidate.is_file():
        return match.group(0)

    root_candidate = pages_dir / target.lstrip("./")
    if root_candidate.is_file():
        repaired = _relative_page_link(
            current_path, pages_dir, root_candidate.relative_to(pages_dir).as_posix()
        )
    else:
        matches = page_paths_by_name.get(Path(target).name, [])
        if len(matches) == 1:
            repaired = _relative_page_link(
                current_path, pages_dir, matches[0].relative_to(pages_dir).as_posix()
            )
        else:
            repaired = f"{OFFICIAL_SITE}/{Path(target).stem}/"
    if separator:
        repaired = f"{repaired}#{anchor}"
    return f"{match.group(1)}{repaired}{match.group(3)}"


def _render_page(
    source_path: Path,
    pages_dir: Path,
    titles_by_filename: dict[str, str],
    page_paths_by_name: dict[str, list[Path]],
    frontend_requirements: str,
    features: list[Feature],
    events_table: str,
) -> str:
    content = source_path.read_text(encoding="utf-8")
    frontmatter = FRONTMATTER.search(content)
    if frontmatter:
        content = (
            content[: frontmatter.end()]
            + "\n"
            + TRANSFORMATION_NOTICE
            + "\n"
            + content[frontmatter.end() :]
        )
    else:
        content = TRANSFORMATION_NOTICE + "\n\n" + content
    content = CAPTURED_VERSION_NOTE.sub(_render_version_note, content)
    content = content.replace(
        "{% include docs/frontend_requirements.html %}",
        frontend_requirements.strip(),
    )
    content = content.replace(
        "{% include docs/feature_version_table.html %}",
        _feature_table(features, source_path.relative_to(pages_dir).parent),
    )
    content = content.replace("{% include docs/events_table.html %}", events_table)
    content = LINKED_PAGE_TITLE.sub(
        lambda match: titles_by_filename.get(match.group(1), match.group(1)),
        content,
    )
    content = JEKYLL_PAGE_LINK.sub(
        lambda match: _relative_page_link(source_path, pages_dir, match.group(1)),
        content,
    )
    content = LOCAL_MARKDOWN_LINK.sub(
        lambda match: _repair_local_markdown_link(
            match, source_path, pages_dir, page_paths_by_name
        ),
        content,
    )
    content = re.sub(r"{%\s*(?:raw|endraw)\s*%}", "", content)
    content = content.replace("{{ site.baseurl }}", OFFICIAL_SITE)
    content = content.replace("{{ site.product_name }}", "Spartacus Storefront")
    normalized = "\n".join(line.rstrip() for line in content.splitlines())
    return normalized + ("\n" if content.endswith("\n") else "")


def prepare_snapshot(
    *,
    pages_dir: Path,
    includes_dir: Path,
    data_dir: Path,
    output_dir: Path,
    source_repo: str,
    source_branch: str,
    source_commit: str,
    source_committed_at: str,
    synced_at: str,
    upstream_license: Path | None,
) -> None:
    """Copy and normalize upstream pages into a validated staging directory."""
    source_pages = sorted(pages_dir.rglob("*.md"))
    if not source_pages:
        raise ValueError(f"source contains no Markdown files: {pages_dir}")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError(f"output directory must be empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    frontend_path = includes_dir / "frontend_requirements.html"
    if not frontend_path.is_file():
        raise ValueError(f"missing required include: {frontend_path}")
    frontend_requirements = frontend_path.read_text(encoding="utf-8")

    titles_by_filename: dict[str, str] = {}
    page_paths_by_name: dict[str, list[Path]] = {}
    features: list[Feature] = []
    for page in source_pages:
        content = page.read_text(encoding="utf-8")
        relative = page.relative_to(pages_dir).as_posix()
        titles_by_filename[page.name] = _extract_title(content, page)
        page_paths_by_name.setdefault(page.name, []).append(page)
        features.extend(_extract_features(content, relative))

    events_table = _events_table(data_dir / "events.csv")
    for page in source_pages:
        relative = page.relative_to(pages_dir)
        destination = output_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            _render_page(
                page,
                pages_dir,
                titles_by_filename,
                page_paths_by_name,
                frontend_requirements,
                features,
                events_table,
            ),
            encoding="utf-8",
        )

    if upstream_license is not None:
        if not upstream_license.is_file():
            raise ValueError(f"missing upstream license: {upstream_license}")
        shutil.copyfile(upstream_license, output_dir / "UPSTREAM_LICENSE.txt")

    metadata = {
        "source": source_repo,
        "branch": source_branch,
        "commit": source_commit,
        "source_committed_at": source_committed_at,
        "synced_at": synced_at,
        "markdown_file_count": len(source_pages),
        "transform": "Jekyll includes and links normalized for local LLM use",
    }
    (output_dir / "SOURCE.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pages-dir", type=Path, required=True)
    parser.add_argument("--includes-dir", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-repo", required=True)
    parser.add_argument("--source-branch", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--source-committed-at", required=True)
    parser.add_argument("--synced-at", required=True)
    parser.add_argument("--upstream-license", type=Path)
    args = parser.parse_args()

    prepare_snapshot(
        pages_dir=args.pages_dir,
        includes_dir=args.includes_dir,
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        source_repo=args.source_repo,
        source_branch=args.source_branch,
        source_commit=args.source_commit,
        source_committed_at=args.source_committed_at,
        synced_at=args.synced_at,
        upstream_license=args.upstream_license,
    )


if __name__ == "__main__":
    main()
