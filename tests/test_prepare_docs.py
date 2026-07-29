import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.prepare_docs import prepare_snapshot


class PrepareDocsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.pages = self.root / "_pages"
        self.includes = self.root / "_includes" / "docs"
        self.data = self.root / "_data"
        self.output = self.root / "docs"
        self.pages.mkdir(parents=True)
        self.includes.mkdir(parents=True)
        self.data.mkdir(parents=True)
        (self.root / "LICENSE.txt").write_text(
            "Apache License\nVersion 2.0\n", encoding="utf-8"
        )

        (self.includes / "frontend_requirements.html").write_text(
            "<p>Use supported Node.js and Angular versions.</p>\n",
            encoding="utf-8",
        )
        (self.pages / "guide").mkdir()
        (self.pages / "guide" / "target.md").write_text(
            "---\ntitle: Target Page\n---\n\n# Target\n",
            encoding="utf-8",
        )
        (self.pages / "guide" / "source.md").write_text(
            """---
title: Source Page
feature:
- name: Source Feature
  spa_version: 1.2
  cx_version: 2211
---

{% capture version_note %}
{{ site.version_note_part1 }} 1.2 {{ site.version_note_part2 }}
{% endcapture %}

{% include docs/feature_version.html content=version_note %}

{% include docs/frontend_requirements.html %}

[Target]({{ site.baseurl }}{% link _pages/guide/target.md %})
[Target from stale path](wrong/target.md)
[Removed page](missing.md#old-section)

![Diagram]({{ site.baseurl }}/assets/images/diagram.png)
""",
            encoding="utf-8",
        )
        (self.pages / "home").mkdir()
        (self.pages / "home" / "feature-release-versions.md").write_text(
            "---\ntitle: Feature Compatibility\n---\n\n"
            "{% include docs/feature_version_table.html %}\n",
            encoding="utf-8",
        )
        (self.pages / "events.md").write_text(
            "---\ntitle: Events\n---\n\n{% include docs/events_table.html %}\n",
            encoding="utf-8",
        )
        with (self.data / "events.csv").open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "path"])
            writer.writeheader()
            writer.writerow({"name": "CartEvent", "path": "cart.events.ts"})

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_expands_jekyll_dependencies_and_records_source(self):
        prepare_snapshot(
            pages_dir=self.pages,
            includes_dir=self.includes,
            data_dir=self.data,
            output_dir=self.output,
            source_repo="https://github.com/SAP/spartacus-docs.git",
            source_branch="develop",
            source_commit="a" * 40,
            source_committed_at="2026-07-28T14:23:08Z",
            synced_at="2026-07-29T04:00:00Z",
            upstream_license=self.root / "LICENSE.txt",
        )

        source = (self.output / "guide" / "source.md").read_text(encoding="utf-8")
        self.assertIn(
            "> **Note:** This feature is introduced with version 1.2 "
            "of the Spartacus libraries.",
            source,
        )
        self.assertIn(
            "<!-- Mechanically prepared from SAP/spartacus-docs under Apache-2.0;",
            source,
        )
        self.assertIn("Use supported Node.js and Angular versions.", source)
        self.assertIn("[Target](target.md)", source)
        self.assertIn("[Target from stale path](target.md)", source)
        self.assertIn(
            "[Removed page](https://sap.github.io/spartacus-docs/missing/#old-section)",
            source,
        )
        self.assertIn(
            "https://sap.github.io/spartacus-docs/assets/images/diagram.png",
            source,
        )
        self.assertNotIn("{% include", source)
        self.assertNotIn("{% link", source)
        self.assertNotIn("{{ site.", source)
        self.assertFalse(
            any(line.endswith((" ", "\t")) for line in source.splitlines())
        )

        features = (self.output / "home" / "feature-release-versions.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "| [Source Feature](../guide/source.md) | 1.2 | 2211 |", features
        )

        events = (self.output / "events.md").read_text(encoding="utf-8")
        self.assertIn("| CartEvent | `cart.events.ts` |", events)

        metadata = json.loads((self.output / "SOURCE.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["commit"], "a" * 40)
        self.assertEqual(metadata["markdown_file_count"], 4)
        self.assertTrue((self.output / "UPSTREAM_LICENSE.txt").is_file())

    def test_rejects_an_empty_source_snapshot(self):
        for path in self.pages.rglob("*.md"):
            path.unlink()

        with self.assertRaisesRegex(ValueError, "no Markdown"):
            prepare_snapshot(
                pages_dir=self.pages,
                includes_dir=self.includes,
                data_dir=self.data,
                output_dir=self.output,
                source_repo="https://github.com/SAP/spartacus-docs.git",
                source_branch="develop",
                source_commit="b" * 40,
                source_committed_at="2026-07-28T14:23:08Z",
                synced_at="2026-07-29T04:00:00Z",
                upstream_license=None,
            )
