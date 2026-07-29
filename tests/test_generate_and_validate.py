import json
import tempfile
import unittest
from pathlib import Path

from scripts.generate_index import generate_index
from scripts.validate_docs import ValidationError, validate_docs


class GenerateAndValidateTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.docs = Path(self.temp_dir.name) / "docs"
        (self.docs / "home").mkdir(parents=True)
        (self.docs / "home" / "compatibility-matrix.md").write_text(
            "---\ntitle: Compatibility Matrix\n---\n\nMatrix.\n",
            encoding="utf-8",
        )
        (self.docs / "install" / "backend").mkdir(parents=True)
        (self.docs / "install" / "backend" / "installing-sap-commerce-cloud.md").write_text(
            "---\ntitle: Installing SAP Commerce Cloud\n---\n\nInstall.\n",
            encoding="utf-8",
        )
        (self.docs / "dev").mkdir()
        (self.docs / "dev" / "authentication.md").write_text(
            "---\ntitle: Authentication\n---\n\nAuth.\n",
            encoding="utf-8",
        )
        (self.docs / "SOURCE.json").write_text(
            json.dumps(
                {
                    "source": "https://github.com/SAP/spartacus-docs.git",
                    "branch": "develop",
                    "commit": "c" * 40,
                    "source_committed_at": "2026-07-28T14:23:08Z",
                    "synced_at": "2026-07-29T04:00:00Z",
                    "markdown_file_count": 3,
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_index_is_deterministic_and_records_upstream_revision(self):
        first = generate_index(self.docs)
        second = generate_index(self.docs)

        self.assertEqual(first, second)
        self.assertIn("cccccccccccc", first)
        self.assertIn("2026-07-29T04:00:00Z", first)
        self.assertNotIn("Last Updated:", first)

    def test_validation_accepts_a_complete_consistent_snapshot(self):
        (self.docs / "SKILL_INDEX.md").write_text(
            generate_index(self.docs), encoding="utf-8"
        )

        report = validate_docs(
            self.docs,
            minimum_markdown_files=3,
            required_paths=(
                "home/compatibility-matrix.md",
                "install/backend/installing-sap-commerce-cloud.md",
                "dev/authentication.md",
            ),
        )

        self.assertEqual(report.markdown_file_count, 3)
        self.assertEqual(report.indexed_file_count, 3)

    def test_validation_rejects_unresolved_jekyll_instructions(self):
        (self.docs / "dev" / "authentication.md").write_text(
            "{% include docs/feature_version.html %}\n", encoding="utf-8"
        )
        (self.docs / "SKILL_INDEX.md").write_text(
            generate_index(self.docs), encoding="utf-8"
        )

        with self.assertRaisesRegex(ValidationError, "unresolved Jekyll"):
            validate_docs(self.docs, minimum_markdown_files=3, required_paths=())
