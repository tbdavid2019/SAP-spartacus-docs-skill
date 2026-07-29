#!/usr/bin/env python3
"""Generate a deterministic index for a prepared documentation snapshot."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


def extract_title(file_path: Path) -> str:
    content = file_path.read_text(encoding="utf-8")
    frontmatter = FRONTMATTER.search(content)
    if frontmatter:
        for line in frontmatter.group(1).splitlines():
            key, separator, value = line.partition(":")
            if separator and key.strip() == "title" and value.strip():
                return value.strip().strip("\"'")
    heading = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if heading:
        return heading.group(1).strip()
    if file_path.name.lower() == "index.md":
        return file_path.parent.name.replace("-", " ").replace("_", " ").title()
    return file_path.stem.replace("-", " ").replace("_", " ").title()


def generate_index(root_dir: Path | str) -> str:
    root = Path(root_dir)
    metadata_path = root / "SOURCE.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    categories: dict[str, list[str]] = defaultdict(list)

    for file_path in sorted(root.rglob("*.md")):
        if file_path.name.upper() in {"INDEX.MD", "SKILL_INDEX.MD"}:
            continue
        relative = file_path.relative_to(root)
        category = relative.parent.as_posix()
        if category == ".":
            category = "General"
        categories[category].append(
            f"- [{extract_title(file_path)}]({relative.as_posix()})"
        )

    commit = metadata["commit"]
    commit_url = metadata["source"].removesuffix(".git") + f"/commit/{commit}"
    lines = [
        "# SAP Spartacus Documentation Index",
        "",
        f"Source snapshot: [`{commit[:12]}`]({commit_url}) "
        f"from `{metadata['branch']}`",
        "",
        f"Synced at: `{metadata['synced_at']}`",
        "",
        "Use this index to locate the prepared local Markdown files. "
        "Confirm version-sensitive guidance against the compatibility and migration pages.",
        "",
    ]
    for category in sorted(
        categories, key=lambda item: (item != "General", item.casefold())
    ):
        display = " > ".join(
            part.replace("_", " ").replace("-", " ").title()
            for part in category.split("/")
        )
        lines.append(f"## {display}")
        lines.extend(categories[category])
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "docs_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "docs",
    )
    args = parser.parse_args()
    output = args.docs_dir / "SKILL_INDEX.md"
    content = generate_index(args.docs_dir)
    if output.exists() and output.read_text(encoding="utf-8") == content:
        print(f"Index unchanged: {output}")
        return
    output.write_text(content, encoding="utf-8")
    print(f"Generated {output}")


if __name__ == "__main__":
    main()
